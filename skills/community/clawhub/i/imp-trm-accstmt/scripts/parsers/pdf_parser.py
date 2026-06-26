"""
PDF银行对账单解析器
支持国内各银行PDF格式的对账单，包括：
- 文本型PDF（直接提取文字层）
- 图片型PDF（通过可插拔OCR接口识别，默认Tesseract）

覆盖的银行（基于已测试样本）：
- 河南农商银行、平安银行、恒丰银行、浙商银行
- 上海浦东发展银行、郑州银行、珠江村镇银行
- 中国农业发展银行

特点：
- 自动检测 PDF 类型（文本型 / 图片型）
- 启发式定位本方账号、户名、币种、日期范围
- PDF文本为"每行一格"列式输出，解析时按"列数"重新组合为行
- 容忍多行折行（如 00708041500000\\n605 折行账号）
"""

import os
import re
import logging
from typing import Optional, Dict, List, Tuple, Any
from datetime import datetime
from decimal import Decimal, InvalidOperation

import fitz  # PyMuPDF

from parsers.base_parser import BaseParser, ParseError
from core.data_structures import (
    BankStatementData, BankStatementHeader, BalanceInfo, TransactionRecord
)
from core.cosine_similarity import CosineSimilarityMatcher, COMMON_BANK_FIELD_ALIASES

logger = logging.getLogger(__name__)


# =====================================================================
# 可插拔 OCR 抽象
# =====================================================================

class OCRBackend:
    """OCR后端抽象基类 — 子类需实现 `image_to_text`"""

    def image_to_text(self, image: Any, lang: str = "chi_sim+eng") -> str:
        raise NotImplementedError(
            "OCR backend not configured. Install pytesseract + tesseract, "
            "or set a custom OCRBackend via PDFParser.set_ocr_backend()."
        )


class TesseractOCR(OCRBackend):
    """基于 pytesseract 的 OCR 实现（可选安装）"""

    def __init__(self, lang: str = "chi_sim+eng"):
        try:
            import pytesseract  # type: ignore
            self.pytesseract = pytesseract
        except ImportError as e:
            raise ImportError(
                "pytesseract is not installed. Run: pip install pytesseract "
                "(and install tesseract-ocr system package, including "
                "chi_sim language data)."
            ) from e
        self.lang = lang

    def image_to_text(self, image: Any, lang: Optional[str] = None) -> str:
        return self.pytesseract.image_to_string(image, lang=lang or self.lang)


# =====================================================================
# 主解析器
# =====================================================================

class PDFParser(BaseParser):
    """PDF 银行对账单解析器（文本型 + 可插拔 OCR）"""

    # 文字型 vs 图片型判定的最小文字密度（chars per page）
    MIN_TEXT_CHARS = 40

    # 银行名特征（用于日志/输出），按"优先级"排序，匹配第一个出现的
    BANK_KEYWORDS = [
        ("中国农业发展银行", "中国农业发展银行"),
        ("农业发展银行", "中国农业发展银行"),
        ("河南农商银行", "河南农商银行"),
        ("农商银行", "河南农商银行"),
        ("平安银行", "平安银行"),
        ("恒丰银行", "恒丰银行"),
        ("浙商银行", "浙商银行"),
        ("浦东发展银行", "浦发银行"),
        ("浦发银行", "浦发银行"),
        ("珠江村镇银行", "珠江村镇银行"),
        ("郑州银行", "郑州银行"),
    ]

    # 列头"候选词" — 关键：日期 + 至少一个金额/余额列
    COLUMN_HEADER_HINTS = [
        # (字段名, 列表式列头候选)
        ('tran_date', ['交易日期', '交易时间', '发生日期', '记账日期', '起息日', '交易日',
                       'Transaction', 'Date', '交易流水日期', '记录日期']),
        ('tran_amt', ['发生金额', '发生金额（元）', '交易金额', '本笔金额', '本次金额',
                      '金额', 'Amount', '交易金额（元）']),
        ('creditamount', ['收入', '贷方发生额', '贷方金额', '存入', '存入金额', '贷方',
                          'Credit', '贷方发生额（收入）', '贷方发生额(收入)',
                          '贷方发', '贷方', '生额(收', '生额(收入)']),
        ('debitamount', ['支出', '借方发生额', '借方金额', '支取', '支取金额', '借方',
                         'Debit', '借方发生额（支取）', '借方发生额(支取)',
                         '借方发', '借方', '生额(支', '生额(支取)']),
        ('acct_bal', ['账户余额', '余额', '交易后余额', '交易后余额（元）', '账面余额',
                      '本次余额', 'Balance', 'Ending Balance', 'Account Balance']),
        ('bank_seq_no', ['交易流水号', '凭证号', '流水号', '业务编号', '交易编号',
                         'Teller', 'Serial', '银行流水号', '柜员交易号', '核心流水号',
                         '账户明细编号', '企业流水号', '凭证种类', '凭证种', 'Serial Number']),
        ('to_acct_no', ['对方账号', '对方账户', '对方卡号', '收款账号', '付款账号',
                        '对手账号', 'Counter Account', 'Counterparty']),
        ('to_acct_name', ['对方户名', '对方名称', '收款人', '付款人', '对手名称',
                          'Counter Name', 'Counterparty Name', 'Beneficiary',
                          '对手机构', '对手名称']),
        ('to_acct_bank_name', ['对方银行', '对方开户行', '对方行名', '对方开户机构',
                               '收款行', '付款行', '对方开户行名称', 'Counterparty Bank',
                               'Counterparty Institution']),
        ('remark', ['摘要', '附言', '业务摘要', '交易摘要', 'Memo', 'Remark',
                    '摘要代码', 'Description', 'Abstract Code']),
        ('use_name', ['用途', '资金用途', 'Use', 'Purpose', '用途/附言', '附言']),
        ('dc_flag', ['借贷标志', '收/付', '收入/支出', '冲正标志', '收支标志',
                     '存入/支取', '收付标志', '收/支']),
    ]

    # 银行PDF常见的"开始新行"时间戳模式
    DATE_LINE_PATTERNS = [
        r'^\d{4}-\d{1,2}-\d{1,2}$',                # 2026-03-30
        r'^\d{4}\d{2}\d{2}$',                       # 20260330
        r'^\d{4}/\d{1,2}/\d{1,2}$',                 # 2026/03/30
        r'^\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}:\d{2}$',
        r'^\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}$',        # 20260302170427
    ]
    DATE_LINE_RE = re.compile('|'.join(DATE_LINE_PATTERNS))

    # 时间戳行（被日期引出后的"时间"行）
    TIME_LINE_RE = re.compile(r'^\d{1,2}:\d{2}(:\d{2})?$')

    # 序号行（浙商银行的"1","2"等）— 通常紧跟时间戳
    SEQ_INT_RE = re.compile(r'^\d{1,4}$')

    # "账户明细编号-交易流水号" 开头（恒丰）
    HENGFENG_SEQ_PREFIX = re.compile(r'^\d{8}$')

    # 凭证种/凭证号 之类的小列
    SHORT_TOKEN_RE = re.compile(r'^[一-龥()（）/]+$')

    def __init__(self, ocr_backend: Optional[OCRBackend] = None):
        self.ocr_backend = ocr_backend
        self.similarity_matcher = CosineSimilarityMatcher(
            threshold=0.6, fallback_threshold=0.4
        )

    def set_ocr_backend(self, backend: OCRBackend):
        """注入OCR后端（用于图片型PDF）"""
        self.ocr_backend = backend

    @property
    def format_name(self) -> str:
        return "PDF Bank Statement"

    def detect_format(self, file_path: str) -> bool:
        try:
            self.validate_file(file_path)
            ext = os.path.splitext(file_path)[1].lower()
            if ext != '.pdf':
                return False
            doc = fitz.open(file_path)
            try:
                if doc.page_count == 0:
                    return False
                for page in doc:
                    text = page.get_text() or ''
                    if len(text.strip()) > self.MIN_TEXT_CHARS:
                        return True
                for page in doc:
                    if page.get_images():
                        return True
                return False
            finally:
                doc.close()
        except Exception as e:
            logger.debug(f"PDF format detection failed: {e}")
            return False

    # ------------------------------------------------------------------
    # 主解析流程
    # ------------------------------------------------------------------

    def parse(self, file_path: str, **kwargs) -> BankStatementData:
        self.validate_file(file_path)

        result = BankStatementData()
        result.source_file = os.path.basename(file_path)
        result.source_format = self.format_name

        try:
            doc = fitz.open(file_path)
            try:
                page_texts: List[str] = []
                for page in doc:
                    page_texts.append(page.get_text() or '')

                is_text_based = any(
                    len(t.strip()) > self.MIN_TEXT_CHARS for t in page_texts
                )

                if is_text_based:
                    logger.info("检测到文本型PDF，直接提取文字")
                else:
                    logger.info("检测到图片型PDF，调用OCR")
                    page_texts = self._ocr_pages(doc)

                full_text = '\n'.join(page_texts)
                result.parse_warnings.append(
                    f"提取方式: {'文本层' if is_text_based else 'OCR'}"
                )

                # 银行名
                bank_name = self._detect_bank_name(full_text)
                if bank_name:
                    result.user_provided_bank_name = bank_name
                else:
                    user_bank = kwargs.get('bank_name')
                    if user_bank:
                        result.user_provided_bank_name = user_bank

                # 头部信息
                header_info = self._parse_header(full_text, kwargs)
                result.header.account_number = header_info['account_number']
                if header_info['account_name']:
                    result.header.raw_tags['account_name'] = header_info['account_name']
                result.default_currency = header_info['currency'] or 'CNY'

                # 交易明细 — 优先用位置信息
                transactions = self._parse_transactions_with_positions(
                    doc, page_texts, header_info
                )
                # 备选：纯文本方式
                if not transactions:
                    transactions = self._parse_transactions(full_text, header_info)
                for txn in transactions:
                    result.add_transaction(txn)

                if not result.transactions:
                    result.add_warning("未找到交易记录")
                if not result.header.account_number:
                    result.add_warning("未找到本方账号")

            finally:
                doc.close()
        except Exception as e:
            result.add_error(f"PDF解析失败: {str(e)}")
            logger.exception(e)

        return result

    # ------------------------------------------------------------------
    # OCR 提取
    # ------------------------------------------------------------------

    def _ocr_pages(self, doc: 'fitz.Document') -> List[str]:
        if self.ocr_backend is None:
            raise ParseError(
                "该PDF似乎为图片型（无可提取文字层），且未配置OCR后端。"
                "请安装 tesseract-ocr + pip install pytesseract，"
                "然后通过 PDFParser.set_ocr_backend(TesseractOCR()) 注入；"
                "或使用其它OCR工具先转换PDF为文本型PDF。"
            )

        texts: List[str] = []
        for i, page in enumerate(doc):
            try:
                pix = page.get_pixmap(dpi=300)
                try:
                    from PIL import Image
                    import io
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    text = self.ocr_backend.image_to_text(img) or ''
                except Exception:
                    tmp_path = f"_ocr_page_{i}.png"
                    pix.save(tmp_path)
                    try:
                        from PIL import Image
                        img = Image.open(tmp_path)
                        text = self.ocr_backend.image_to_text(img) or ''
                    finally:
                        if os.path.exists(tmp_path):
                            try:
                                os.remove(tmp_path)
                            except OSError:
                                pass
                texts.append(text)
            except Exception as e:
                logger.warning(f"OCR 第{i+1}页失败: {e}")
                texts.append('')
        return texts

    # ------------------------------------------------------------------
    # 头部解析
    # ------------------------------------------------------------------

    def _detect_bank_name(self, text: str) -> str:
        for kw, full_name in self.BANK_KEYWORDS:
            if kw in text:
                return full_name
        return ''

    def _parse_header(self, text: str, kwargs: dict) -> Dict[str, str]:
        info = {
            'account_number': kwargs.get('account_number', '') or '',
            'account_name': '',
            'currency': '',
            'date_range': ('', ''),
        }

        if not info['account_number']:
            info['account_number'] = self._find_account_number(text)
        info['account_name'] = self._find_account_name(text)
        info['currency'] = self._find_currency(text)
        info['date_range'] = self._find_date_range(text)
        return info

    def _find_account_number(self, text: str) -> str:
        # 多行模式：标签在第一行，数字在第二行
        multiline_patterns = [
            r'账\s*/\s*卡号\s*[:：]?\s*\n\s*([0-9]{8,30})',
            r'(?:^|\n)\s*账号\s*[:：]?\s*\n\s*([0-9]{8,30})',
            r'(?:^|\n)\s*客户账号\s*[:：]?\s*\n\s*([0-9]{8,30})',
            r'(?:^|\n)\s*对公账号\s*[:：]?\s*\n\s*([0-9]{8,30})',
            r'(?:^|\n)\s*银行账号\s*[:：]?\s*\n\s*([0-9]{8,30})',
        ]
        for pat in multiline_patterns:
            m = re.search(pat, text, re.MULTILINE)
            if m:
                return m.group(1).strip()

        # 单行模式：标签 + 数字 在同一行
        single_patterns = [
            r'账\s*/\s*卡号\s*[:：]\s*([0-9]{8,30})',
            r'客户账号\s*[:：]\s*([0-9]{8,30})',
            r'账号\s*[:：]\s*([0-9]{8,30})',
            r'银行账号\s*[:：]\s*([0-9]{8,30})',
            r'对公账号\s*[:：]\s*([0-9]{8,30})',
            r'Account\s*Number\s*[:：]?\s*([0-9]{8,30})',
        ]
        for pat in single_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()

        return ''

    def _find_account_name(self, text: str) -> str:
        # 优先匹配"账户名称"（避免和"客户名称"等冲突）
        candidates = []
        patterns = [
            ('账户名称', r'账户名称\s*[:：]?\s*([^\n\r ]+)'),
            ('客户名称', r'客户名称\s*[:：]?\s*([^\n\r]+)'),
            ('Account Name', r'Account\s*Name\s*[:：]?\s*([^\n\r]+)'),
            ('Customer Name', r'Customer\s*Name\s*[:：]?\s*([^\n\r]+)'),
            ('本方户名', r'本方户名\s*[:：]?\s*([^\n\r]+)'),
            ('客户名', r'客户名\s*[:：]?\s*([^\n\r]+)'),
            ('户名', r'(?:^|\n)\s*户名\s*[:：]?\s*([^\n\r]+)'),
        ]
        for tag, pat in patterns:
            m = re.search(pat, text, re.IGNORECASE | re.MULTILINE)
            if m:
                name = m.group(1).strip()
                # 去除尾部的特殊字符（包括 &nbsp; 等）
                name = re.sub(r'[\s\.,;，。；\xa0 ]+$', '', name)
                # 过滤掉明显是别的字段（包含"账号"、"编号"等）
                if any(kw in name for kw in ['账号', '编号', 'Customer', 'Name']):
                    continue
                # 截断混入的后续字段（如"电子回单编号"之后的都去掉）
                for kw in ['电子回单', '账号：', '币种：', '起止日期', '总笔数']:
                    if kw in name:
                        idx = name.index(kw)
                        name = name[:idx].strip()
                        break
                if 2 <= len(name) <= 80:
                    return name
        return ''

    def _find_currency(self, text: str) -> str:
        if '人民币' in text or 'RMB' in text or 'CNY' in text:
            return 'CNY'
        if '美元' in text or 'USD' in text:
            return 'USD'
        if '欧元' in text or 'EUR' in text:
            return 'EUR'
        if '港币' in text or 'HKD' in text:
            return 'HKD'
        if '日元' in text or 'JPY' in text:
            return 'JPY'
        if '英镑' in text or 'GBP' in text:
            return 'GBP'
        return ''

    def _find_date_range(self, text: str) -> Tuple[str, str]:
        patterns = [
            r'起止日期[：:]\s*([\d\s\-/]+)\s*[-—–~到至]+\s*([\d\s\-/]+)',
            r'起始日期[：:]?\s*([\d\s\-/]+)[\s\S]{0,30}?终止日期[：:]?\s*([\d\s\-/]+)',
            r'查询日期[：:]?\s*([\d\s\-/]+)\s*[-—–~到至]+\s*([\d\s\-/]+)',
            r'账单统计日期\s*[A-Za-z\s]*?\s*([\d/\-]+)\s*[-—–~到至]+\s*([\d/\-]+)',
        ]
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                return m.group(1).strip(), m.group(2).strip()
        return '', ''

    # ------------------------------------------------------------------
    # 交易明细解析 — 基于位置信息
    # ------------------------------------------------------------------

    def _parse_transactions_with_positions(
        self,
        doc: 'fitz.Document',
        page_texts: List[str],
        header_info: Dict[str, str],
    ) -> List[TransactionRecord]:
        """
        使用 PyMuPDF 的位置信息（blocks）解析交易表。

        流程：
        1. 对每页，提取所有 text blocks（含位置）
        2. 找到"表头块" — 用 _find_table_header
        3. 在表头下方的 blocks 按 Y 坐标分行（Y 在同一行的归为一行）
        4. 对每行 blocks 按 X 坐标排序，提取 cell 文本
        5. 解析为 TransactionRecord
        """
        # 收集所有页面的 blocks
        all_rows: List[Tuple[float, List[Tuple[float, str]]]] = []  # [(y_top, [(x, text), ...])]

        for page in doc:
            page_dict = page.get_text("dict")
            # 收集所有 spans: (y0, x0, text)
            spans: List[Tuple[float, float, str]] = []
            for block in page_dict.get("blocks", []):
                if block.get("type") != 0:  # 跳过图片
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if not text:
                            continue
                        y0 = span.get("bbox", [0, 0, 0, 0])[1]
                        x0 = span.get("bbox", [0, 0, 0, 0])[0]
                        spans.append((y0, x0, text))
            if not spans:
                continue
            # 按 Y 分组（同一行 = y 差 < 12pt，容许列头多行折行）
            spans.sort(key=lambda s: (s[0], s[1]))
            current_y = spans[0][0]
            current_row: List[Tuple[float, str]] = []
            for y, x, t in spans:
                if y - current_y > 12:
                    if current_row:
                        all_rows.append((current_y, sorted(current_row, key=lambda c: c[0])))
                    current_row = [(x, t)]
                    current_y = y
                else:
                    current_row.append((x, t))
            if current_row:
                all_rows.append((current_y, sorted(current_row, key=lambda c: c[0])))

        if not all_rows:
            return []

        # 解析
        txns = self._parse_rows_from_blocks(all_rows, header_info)
        if txns:
            return txns

        # 备选策略：日期锚点法（应对"列头乱序散布"型PDF，如浦发）
        txns = self._parse_by_date_anchor(all_rows, header_info)
        return txns

    def _parse_by_date_anchor(
        self,
        all_rows: List[Tuple[float, List[Tuple[float, str]]]],
        header_info: Dict[str, str],
    ) -> List[TransactionRecord]:
        """
        备选策略：日期锚点法
        适用于"列头散布"型PDF（如浦发银行英文+中文混合布局），
        此时没有清晰的表头块。
        策略：
        1. 找到所有日期行（含日期模式的 row）
        2. 围绕每个日期行，按 Y 接近的方向收集附近的 cells
        3. 推断列含义（按 x 位置归类到常见列）
        """
        # 收集所有日期锚点
        date_anchors: List[Tuple[int, float, str, float, str]] = []  # (row_idx, x, date, y, date_cell)
        for i, (y, cells) in enumerate(all_rows):
            for x, t in cells:
                d, tm = self._try_parse_date_time(t)
                if d:
                    date_anchors.append((i, x, d, y, t))

        if not date_anchors:
            return []

        transactions: List[TransactionRecord] = []
        seq_counter = 1

        for row_idx, x_date, d, y_date, date_cell in date_anchors:
            # 在该行和附近几行收集所有 cell
            nearby_cells: List[Tuple[float, float, str]] = []  # (x, y, text)
            for j in range(max(0, row_idx - 5), min(len(all_rows), row_idx + 6)):
                yj, cells = all_rows[j]
                for xj, tj in cells:
                    nearby_cells.append((xj, yj, tj))

            # 按 X 坐标分组（同一列 = x 差 < 25pt）
            nearby_cells.sort(key=lambda c: (c[0], c[1]))
            column_groups: List[List[Tuple[float, float, str]]] = []
            for xj, yj, tj in nearby_cells:
                added = False
                for grp in column_groups:
                    if abs(grp[0][0] - xj) < 25:
                        grp.append((xj, yj, tj))
                        added = True
                        break
                if not added:
                    column_groups.append([(xj, yj, tj)])

            # 对每列的 cell 合并文本（按 y 排序）
            col_texts: List[Tuple[float, str]] = []  # (x, 合并文本)
            for grp in column_groups:
                grp.sort(key=lambda c: c[1])
                # 折叠相邻 y 的短 cell
                merged = []
                cur_y, cur_t = grp[0][1], grp[0][2]
                for _, y, t in grp[1:]:
                    if y - cur_y < 8 and len(cur_t) < 10 and len(t) < 10:
                        cur_t = cur_t + t
                    else:
                        merged.append(cur_t)
                        cur_y, cur_t = y, t
                merged.append(cur_t)
                col_texts.append((grp[0][0], ' '.join(merged)))

            # 转换为 cell 列表（去掉 x 坐标）
            row_cells = [t for _, t in sorted(col_texts, key=lambda c: c[0])]

            txn = self._build_transaction(
                row_cells, {}, header_info, seq_counter
            )
            if txn and txn.value_date:
                transactions.append(txn)
                seq_counter += 1

        return transactions

    def _parse_rows_from_blocks(
        self,
        all_rows: List[Tuple[float, List[Tuple[float, str]]]],
        header_info: Dict[str, str],
    ) -> List[TransactionRecord]:
        """
        从已经按 Y 分组的 blocks 中解析交易记录
        """
        # 找表头：扫描连续行，每行有多个 cell（≥2），且合并后能命中列头关键词
        # 关键：表头行不应包含日期模式（避免把数据行当表头）
        header_row_idx = -1
        header_cells: List[Tuple[float, str]] = []
        column_map: Dict[str, int] = {}

        for i, (_, cells) in enumerate(all_rows):
            if len(cells) < 2:
                continue
            merged = self._merge_adjacent_cells(cells)
            cell_texts = [t for _, t in merged]
            # 跳过明显的数据行（含日期/时间模式）
            full_text = ' '.join(cell_texts)
            if self.DATE_LINE_RE.match(cell_texts[0]) or self._has_date_anywhere(cell_texts):
                # 这是数据行，跳过
                continue
            cmap = self._map_column_headers(cell_texts)
            has_date = 'tran_date' in cmap
            has_amount = any(
                k in cmap for k in ('creditamount', 'debitamount', 'tran_amt', 'acct_bal')
            )
            if has_date and has_amount and len(cmap) >= 2:
                if len(cmap) > len(column_map):
                    header_row_idx = i
                    header_cells = merged
                    column_map = cmap
                if len(cmap) >= 5:
                    break

        if header_row_idx < 0 or not column_map:
            return []

        # 收集所有 header 单元格的 X 位置（用全部 header cells）
        # 这样缺失的列也能被正确处理（cells 直接按 index 对齐到 header cols）
        header_x_positions = [x for x, _ in header_cells]
        max_col_idx = len(header_x_positions)  # 全列数（含未映射的）

        # 数据行：表头之后的所有行
        data_rows = all_rows[header_row_idx + 1:]

        # 过滤页脚/汇总
        data_rows = self._filter_footer_rows(data_rows)

        # 折行回填：把单 cell 续行合并到前一行（"有限公司"、"部"、"行" 等）
        data_rows = self._absorb_wrap_rows(data_rows)

        # 每行 cells → 列表 → 解析为TransactionRecord
        transactions: List[TransactionRecord] = []
        seq_counter = 1
        for _, cells in data_rows:
            # 合并相邻的短 cell（折行）
            merged = self._merge_adjacent_cells(cells)
            # 用 X 位置对齐到表头列
            row_cells = self._align_cells_to_columns(merged, header_x_positions)
            txn = self._build_transaction(row_cells, column_map, header_info, seq_counter)
            if txn:
                transactions.append(txn)
                seq_counter += 1

        return transactions

    def _align_cells_to_columns(
        self,
        cells: List[Tuple[float, str]],
        header_x_positions: List[float],
    ) -> List[str]:
        """
        把 cells 按 X 位置对齐到表头列。
        策略：先用 INDEX 对齐，再用 X 位置做列替换（处理 wrap/缺失列的情况）。

        - 默认 col_count 个 cell 直接按 index 对齐到 col 0..col_count-1
        - 多出的 cell 视为折行（已通过 _merge_adjacent_cells 处理）
        - 缺失列填 ''
        """
        if not header_x_positions:
            return [t for _, t in cells]

        col_count = len(header_x_positions)
        cell_texts = [t for _, t in cells]

        # 简化为：直接按 index 对齐（已通过 _merge_adjacent_cells 处理了折行）
        aligned = ['' for _ in range(col_count)]
        for i in range(min(len(cell_texts), col_count)):
            aligned[i] = cell_texts[i]
        # 如果 cells 多于 col_count，截断（多余的应该被 redistribute 处理了）
        # 如果 cells 少于 col_count，补空
        return aligned

    def _absorb_wrap_rows(
        self,
        data_rows: List[Tuple[float, List[Tuple[float, str]]]],
    ) -> List[Tuple[float, List[Tuple[float, str]]]]:
        """
        折行回填：把单 cell 续行合并到前一行
        启发式：
        - 单 cell 行（n=1）或非常短（n≤2），且文本长度 ≤ 6
        - 看起来像"有限公司"/"部"/"行"等中文短词
        - 把这个 cell 的内容追加到前一行最后一个相同 x 位置的 cell 后
        """
        if len(data_rows) < 2:
            return data_rows

        result: List[Tuple[float, List[Tuple[float, str]]]] = []
        i = 0
        while i < len(data_rows):
            y, cells = data_rows[i]

            # 收集连续的"短 cell 行"（典型折行）
            j = i + 1
            absorbed = []
            while j < len(data_rows):
                next_y, next_cells = data_rows[j]
                # 距离前一行不超过 30pt
                if next_y - y > 30:
                    break
                # 短 cell 行（≤2 cells）
                if len(next_cells) > 2:
                    break
                # 看起来是 wrap：纯中文或短词
                wrap_texts = [t for _, t in next_cells if t.strip()]
                if not wrap_texts:
                    j += 1
                    continue
                # 必须都是 wrap-able 文本
                is_wrap = all(
                    re.match(r'^[一-龥（）()A-Za-z·\.\-]+$', t) and len(t) <= 6
                    for t in wrap_texts
                ) or all(t.isdigit() and len(t) <= 4 for t in wrap_texts)
                if not is_wrap:
                    break
                absorbed.append((next_y, next_cells))
                j += 1

            # 把 absorbed cells 加入到当前行的 cells（按 x 合并到相同 x 位置）
            if absorbed:
                for _, wcells in absorbed:
                    for wx, wt in wcells:
                        # 找当前行中相同 x 的 cell
                        merged_into = False
                        for ci, (cx, ct) in enumerate(cells):
                            if abs(cx - wx) < 3:
                                cells[ci] = (cx, ct + wt)
                                merged_into = True
                                break
                        if not merged_into:
                            # 没找到相同 x — 作为新 cell 追加
                            cells.append((wx, wt))
                # 重新排序 cells
                cells = sorted(cells, key=lambda c: c[0])

            result.append((y, cells))
            i = max(j, i + 1) if absorbed else i + 1

        return result

    def _has_date_anywhere(self, cell_texts: List[str]) -> bool:
        """判断一行 cells 中是否包含日期模式"""
        for t in cell_texts:
            if self.DATE_LINE_RE.match(t.strip()):
                return True
        return False

    def _merge_adjacent_cells(
        self, cells: List[Tuple[float, str]]
    ) -> List[Tuple[float, str]]:
        """
        合并位置相邻且看起来是"折行"的 cell。
        规则：
        - x 完全相同（差 < 3pt）— 直接合并为同一列的多行内容（典型 2-3 行折行）
        - 适配场景：对方户名（公司名）跨 2-3 行、对方账号/流水号跨 2-3 行
        """
        if not cells:
            return cells
        merged: List[Tuple[float, str]] = []
        cur_x, cur_t = cells[0]
        for x, t in cells[1:]:
            # x 完全相同（同列折行）— 总是合并（不论长度）
            if abs(x - cur_x) < 3:
                cur_t = cur_t + t
                continue
            # 不合并
            merged.append((cur_x, cur_t))
            cur_x, cur_t = x, t
        merged.append((cur_x, cur_t))
        return merged

    def _map_column_headers(self, cell_texts: List[str]) -> Dict[str, int]:
        """将列头映射到目标字段。处理折行（cells 多于实际列数）"""
        # 1. 智能合并：将碎片列头拼接成完整列头
        # 例如 ['交易时', '间'] → ['交易时间']
        normalized = self._normalize_column_headers(cell_texts)
        # 2. 精确匹配
        column_map: Dict[str, int] = {}
        for col_idx, header in enumerate(normalized):
            h = header.strip()
            if not h:
                continue
            for field, hints in self.COLUMN_HEADER_HINTS:
                if field in column_map:
                    continue
                for hint in hints:
                    if h == hint or h.replace(' ', '') == hint.replace(' ', ''):
                        column_map[field] = col_idx
                        break
                if field in column_map:
                    break
        return column_map

    def _normalize_column_headers(self, cell_texts: List[str]) -> List[str]:
        """
        列头归一化：把碎片列头拼接成完整列头
        规则：
        - 如果相邻两 cell 拼起来能命中候选词，就合并
        - 否则保留原文
        """
        if len(cell_texts) <= 1:
            return cell_texts

        # 把所有候选词做成 set 便于快速判断
        all_hints = set()
        for _, hints in self.COLUMN_HEADER_HINTS:
            all_hints.update(hints)
        # 把"中英对照"的也加入：把含中文字符的cell合并后再判断
        # 算法：从前往后尝试拼接，找到第一个能命中候选的就停止
        normalized: List[str] = []
        i = 0
        while i < len(cell_texts):
            cur = cell_texts[i].strip()
            # 尝试向后拼接
            best = cur
            for j in range(i + 1, min(i + 6, len(cell_texts) + 1)):
                combined = ''.join(cell_texts[k].strip() for k in range(i, j))
                if combined in all_hints:
                    best = combined
                    normalized.append(best)
                    i = j
                    break
            else:
                # 没有任何拼接命中
                normalized.append(cur)
                i += 1
        return normalized

    def _filter_footer_rows(
        self, rows: List[Tuple[float, List[Tuple[float, str]]]]
    ) -> List[Tuple[float, List[Tuple[float, str]]]]:
        """过滤页脚/汇总行"""
        footer_markers = [
            '生成时间', '打印时间', '提示', '温馨提示', '本交易明细', '如对本',
            '本行对', '查询', '签章处', '总笔数', '收入总金额', '支出总金额',
            '本期合计', '本年累计', '打印日期', '期末余额', '汇总交易笔数',
            '汇总借方', '汇总贷方', 'past 5 years', 'Service Hotline',
            '如需校验', '如有任何疑问', '签章', '第1页', '第2页',
            'coo', 'Cor',
        ]
        result = []
        for y, cells in rows:
            full_text = ''.join(t for _, t in cells)
            is_footer = False
            for marker in footer_markers:
                if marker in full_text and len(full_text) < 80:
                    is_footer = True
                    break
            if not is_footer:
                result.append((y, cells))
        return result

    # ------------------------------------------------------------------
    # 交易明细解析 — 纯文本回退
    # ------------------------------------------------------------------

    def _parse_transactions(
        self, text: str, header_info: Dict[str, str]
    ) -> List[TransactionRecord]:
        """
        解析PDF中的交易明细表

        策略：
        1. 先用文本行模式找到表头块（确定列数 N）
        2. 用 PyMuPDF 的位置信息（blocks）重新按 Y/X 排序组合行
        3. 若位置信息不可用，回退到文本行按列数分组
        """
        lines = [l for l in text.split('\n')]
        lines = [l.rstrip() for l in lines]

        # 1. 找到表头块
        header_block_start, column_count, column_map = self._find_table_header(lines)
        if header_block_start < 0 or column_count <= 0:
            logger.warning("未找到交易明细表头")
            return []

        # 2. 数据从表头块之后开始
        data_lines = lines[header_block_start + column_count:]

        # 3. 终止标记
        end_idx = self._find_data_end(data_lines)
        if end_idx >= 0:
            data_lines = data_lines[:end_idx]

        # 4. 用位置信息组合行（如果有 doc 可用）
        rows = self._group_into_rows(data_lines, column_count)

        # 5. 转为TransactionRecord
        transactions: List[TransactionRecord] = []
        seq_counter = 1
        for row in rows:
            txn = self._build_transaction(row, column_map, header_info, seq_counter)
            if txn:
                transactions.append(txn)
                seq_counter += 1

        return transactions

    def _find_table_header(
        self, lines: List[str]
    ) -> Tuple[int, int, Dict[str, int]]:
        """
        寻找"连续的列头块"。

        由于PDF文本是"每行一格"列式输出，列头表现为：
        L0: 交易时间
        L1: 交易流水号
        L2: 收入
        L3: 支出
        L4: 账户余额
        ...

        Returns:
            (起始行索引, 列数, 列字段→列索引 映射)
        """
        best_start = -1
        best_count = 0
        best_map: Dict[str, int] = {}

        # 列头出现的频次阈值：连续N行中至少要有一行匹配"日期/金额/账号"等关键列
        # 然后这N行中至少能匹配到多个目标字段
        for i in range(len(lines) - 2):
            # 第一行必须是列头候选
            first = lines[i].strip()
            if not first or not self._is_header_candidate(first):
                continue
            # 找连续匹配的最大块
            block_start = i
            block_end = i
            for j in range(i, min(i + 30, len(lines))):
                s = lines[j].strip()
                if not s:
                    break
                if not self._is_header_candidate(s):
                    break
                block_end = j
            block_count = block_end - block_start + 1
            if block_count < 2:
                continue
            # 检查这个块中能匹配多少个目标字段
            block_lines = [lines[k].strip() for k in range(block_start, block_end + 1)]
            column_map = self._map_columns(block_lines)
            # 关键：至少包含日期 + 至少一个金额/余额/借/贷字段
            has_date = 'tran_date' in column_map
            has_amount = any(
                k in column_map for k in ('creditamount', 'debitamount', 'tran_amt', 'acct_bal')
            )
            if has_date and has_amount and len(column_map) >= 2:
                if block_count > best_count:
                    best_start = block_start
                    best_count = block_count
                    best_map = column_map

        return best_start, best_count, best_map

    def _is_header_candidate(self, line: str) -> bool:
        """判断一行是否看起来像列头"""
        if not line or len(line) > 30:
            return False
        # 列头通常是中文2-10个字符，或英文单词
        for field, hints in self.COLUMN_HEADER_HINTS:
            for hint in hints:
                if line == hint or hint in line:
                    return True
        # 也允许纯短中文词（≤10字符）作为列头
        if 2 <= len(line) <= 12 and self.SHORT_TOKEN_RE.match(line):
            return True
        # 允许英文单词
        if 2 <= len(line) <= 30 and re.match(r'^[A-Za-z][A-Za-z\.\s]*$', line):
            return True
        return False

    def _map_columns(self, header_lines: List[str]) -> Dict[str, int]:
        """
        将列头映射到目标字段。先做列头归一化（合并相邻的列头碎片），
        再精确匹配。
        """
        # 1. 列头归一化：合并相邻列头碎片
        # 例如 ["交易时", "间"] → ["交易时间"]
        # 规则：如果相邻两行都是候选，且合并后长度合适
        normalized = self._normalize_headers(header_lines)

        # 2. 精确匹配
        column_map: Dict[str, int] = {}
        for col_idx, header in enumerate(normalized):
            for field, hints in self.COLUMN_HEADER_HINTS:
                if field in column_map:
                    continue
                for hint in hints:
                    if header == hint or header.replace(' ', '') == hint.replace(' ', ''):
                        column_map[field] = col_idx
                        break
                if field in column_map:
                    break
        return column_map

    def _normalize_headers(self, header_lines: List[str]) -> List[str]:
        """
        列头归一化：合并相邻的列头碎片
        规则：
        - 如果当前行很短（≤3字符），且不是数字/时间，尝试与下一行合并
        - 合并时如果命中 COLUMN_HEADER_HINTS 中的某个候选词，就替换为该候选
        - 否则保留原文拼接
        """
        # 先简单合并：相邻两行（其中之一非常短）合成一行
        merged: List[str] = []
        i = 0
        while i < len(header_lines):
            cur = header_lines[i].strip()
            # 尝试与下一行合并
            if (i + 1 < len(header_lines)
                and cur
                and len(cur) <= 3
                and not cur.isdigit()
                and not self.DATE_LINE_RE.match(cur)
                and not self.TIME_LINE_RE.match(cur)
            ):
                nxt = header_lines[i + 1].strip()
                if nxt and len(nxt) <= 5:
                    combined = cur + nxt
                    # 检查合并后是否命中候选
                    replaced = False
                    for _, hints in self.COLUMN_HEADER_HINTS:
                        for hint in hints:
                            if combined == hint or combined.replace(' ', '') == hint.replace(' ', ''):
                                combined = hint
                                replaced = True
                                break
                        if replaced:
                            break
                    merged.append(combined)
                    i += 2
                    continue
            # 不合并：保留原行
            merged.append(cur)
            i += 1

        return merged

    def _find_data_end(self, lines: List[str]) -> int:
        """找到数据区结束位置（首条出现的页脚/汇总信息行）"""
        footer_markers = [
            '生成时间', '打印时间', '提示', '温馨提示', '本交易明细', '如对本',
            '本行对', '查询', '签章处', '总笔数', '收入总金额', '支出总金额',
            '本期合计', '本年累计', '打印日期', '期末余额', '汇总交易笔数',
            '汇总借方', '汇总贷方', 'past 5 years', 'Service Hotline',
            '如需校验', '如有任何疑问', '签章',
        ]
        for i, line in enumerate(lines):
            s = line.strip()
            for marker in footer_markers:
                if marker in s and len(s) < 80:
                    return i
            # 单独的"第N页"也是页脚
            if re.match(r'^第\s*\d+\s*页', s):
                return i
        return -1

    def _group_into_rows(
        self, lines: List[str], column_count: int
    ) -> List[List[str]]:
        """
        将"每行一格"的数据按列重新组合成行。

        核心策略：状态机 + 列索引感知
        - 每行视为"当前行"的下一列
        - 若列索引 >= column_count → 该格是"上一列的折行"，合并到上一列
        - 检测"新行起点"（日期/时间）时重置列索引

        输出每行可能包含 column_count+ 个格（折行合并后多于列数），调用方再处理
        """
        if column_count <= 0:
            return []

        # 过滤空行 / 页脚
        clean_lines = []
        for l in lines:
            s = l.strip()
            if not s:
                continue
            if s in ('_', '-', '—', '~', '·', '—'):
                continue
            clean_lines.append(s)

        rows: List[List[str]] = []
        current_row: List[str] = []
        col_idx = 0  # 当前期望的列索引

        for line in clean_lines:
            # 检测新行起点
            is_new_row = (
                self.DATE_LINE_RE.match(line)
                or (col_idx > 0 and self.SEQ_INT_RE.match(line) and col_idx == 0)
                or (line.isdigit() and 1 <= len(line) <= 4 and col_idx >= column_count)
            )
            if is_new_row and current_row:
                rows.append(current_row)
                current_row = []
                col_idx = 0

            if not current_row:
                # 新行的第一格
                current_row.append(line)
                col_idx = 1
            else:
                if col_idx < column_count:
                    current_row.append(line)
                    col_idx += 1
                else:
                    # 折行：合并到上一格
                    current_row[-1] = current_row[-1] + line

        if current_row:
            rows.append(current_row)

        # 过滤只有1个格的"孤立行"
        rows = [r for r in rows if len(r) >= max(2, column_count // 2)]
        return rows

    def _build_transaction(
        self,
        row_cells: List[str],
        column_map: Dict[str, int],
        header_info: Dict[str, str],
        seq_counter: int,
    ) -> Optional[TransactionRecord]:
        """
        将一行（已经是组合好的列）解析为TransactionRecord
        """
        if len(row_cells) < 2:
            return None

        # col_count: 数据列数 = max(列索引) + 1
        # 因为 cells 已按 index 对齐到 header 全部列
        max_col = max(column_map.values()) if column_map else 0
        # 数据列数应该是 max(数据中实际列数) 和 col_count 的较大值
        col_count = max(max_col + 1, len(row_cells))
        wrapped_cells = list(row_cells)

        if len(wrapped_cells) > col_count:
            wrapped_cells = self._realign_by_position(wrapped_cells, col_count)

        # 如果 cells 少于 column_count，补空
        while len(wrapped_cells) < col_count:
            wrapped_cells.append('')

        row_cells = wrapped_cells[:col_count]

        txn = TransactionRecord()
        txn.account_number = header_info.get('account_number', '')
        txn.currency_code = header_info.get('currency', 'CNY') or 'CNY'

        # 提取日期/时间
        date_value, time_value = '', ''
        ci_date = column_map.get('tran_date')
        if ci_date is not None and ci_date < len(row_cells):
            cell = row_cells[ci_date].strip()
            d, t = self._try_parse_date_time(cell)
            if d:
                date_value = d
                time_value = t
        if not date_value:
            for col_idx in range(len(row_cells)):
                cell = row_cells[col_idx].strip()
                if not cell or cell in ('_', '-'):
                    continue
                d, t = self._try_parse_date_time(cell)
                if d:
                    date_value = d
                    time_value = t
                    break

        if not date_value:
            return None
        txn.value_date = date_value
        txn.transaction_time = time_value

        # 流水号
        seq_found = ''
        for cell in row_cells:
            s = self._extract_seq_no(cell)
            if s:
                seq_found = s
                break
        txn.reference_number = seq_found if seq_found else f"PDF_{seq_counter:06d}"

        # 金额（按 column_map 的列索引分配）
        credit, debit, signed_amt, balance, dc_flag = self._extract_amounts(
            row_cells, column_map
        )
        txn.credit_amount = credit
        txn.debit_amount = debit
        txn.amount = signed_amt if signed_amt else (credit or debit)
        txn.running_balance = balance
        txn.dc_indicator = dc_flag  # 关键：基于列位置决定借贷标识

        # 对方账号
        counter_acct = self._extract_counter_account(row_cells, column_map)
        if counter_acct:
            txn.counterparty_account = counter_acct

        # 对方户名
        counter_name = self._extract_counter_name(row_cells, column_map)
        if counter_name:
            txn.counterparty_name = counter_name

        # 摘要
        remark = self._extract_remark(row_cells, column_map)
        if remark:
            txn.transaction_description = remark

        # 用途
        use = self._extract_use_name(row_cells, column_map)
        if use:
            txn.supplementary_details = use

        return txn

    def _realign_by_position(
        self,
        cells: List[str],
        col_count: int,
    ) -> List[str]:
        """
        当 cells 多于 col_count 时，重新对齐。
        启发式：把多出的 cell 按内容类型合并到正确的逻辑列。
        使用 column_map 来定位正确的列索引（不依赖硬编码 13/14/16）。
        """
        if len(cells) <= col_count:
            return list(cells)

        main = list(cells[:col_count])
        extras = list(cells[col_count:])

        if not extras:
            return main

        # 用 column_map 找各字段的列索引
        # 注意：column_map 是在 _build_transaction 调进来时已知
        # 但这里只收到 cells 和 col_count。我们用以下启发式：
        # 银行对账单常见的列结构（按位置）：
        # 0: 序号, 1: 流水号, 2: 日期, 3: 支出/借, 4: 收入/贷, 5: 余额, ...
        # 但 col_count 是 max_logical_col + 1，cells[col_count-1] 是最右的逻辑列
        # 所以从后往前找合适的列

        for extra in extras:
            extra = extra.strip()
            if not extra:
                continue

            # 规则1：纯数字短串（≤4位）→ 拼到流水号/账号（找最近一个数字 cell）
            if extra.isdigit() and len(extra) <= 4:
                # 找最后几个数字 cell
                for ci in range(len(main) - 1, -1, -1):
                    if main[ci] and main[ci].isdigit() and len(main[ci]) >= 4:
                        main[ci] = main[ci] + extra
                        break
                continue

            # 规则2：含公司/集团/银行/支行/分行/有限 → to_acct_name（中间列之后）
            if any(kw in extra for kw in ['公司', '集团', '银行', '支行', '分行', '有限', '中心', '部']):
                # 找后面 1/3 区域的列（含中文的）
                target_start = col_count * 2 // 3
                for ci in range(target_start, col_count):
                    if main[ci] and any('一' <= c <= '鿿' for c in main[ci]):
                        main[ci] = main[ci] + extra
                        break
                continue

            # 规则3：纯中文短词 → 拼到 to_acct_name（同样找含中文的列）
            if re.match(r'^[一-龥]{1,6}$', extra):
                target_start = col_count * 2 // 3
                for ci in range(target_start, col_count):
                    if main[ci] and any('一' <= c <= '鿿' for c in main[ci]):
                        main[ci] = main[ci] + extra
                        break
                continue

            # 规则4：含"支/营业/网点" → 拼到银行名列
            if any(kw in extra for kw in ['支', '营业', '网点']):
                target_start = col_count * 2 // 3
                for ci in range(target_start, col_count):
                    if main[ci] and any('一' <= c <= '鿿' for c in main[ci]):
                        main[ci] = main[ci] + extra
                        break
                continue

            # 规则5：默认 → 拼到最后一列（通常是 摘要/备注）
            if main:
                main[-1] = main[-1] + extra if main[-1] else extra

        return main

    def _try_parse_date_time(self, text: str) -> Tuple[str, str]:
        """从单元格里识别日期/时间"""
        s = text.strip()
        if not s:
            return '', ''

        # 2026-03-30 17:11:47
        m = re.search(
            r'(\d{4})[-\-/](\d{1,2})[-\-/](\d{1,2})\s+(\d{1,2}):(\d{2}):(\d{2})', s
        )
        if m:
            return (
                f"{m.group(1)}{int(m.group(2)):02d}{int(m.group(3)):02d}",
                f"{int(m.group(4)):02d}{int(m.group(5)):02d}{int(m.group(6)):02d}",
            )
        # 2026-03-30
        m = re.match(r'(\d{4})[-\-/](\d{1,2})[-\-/](\d{1,2})', s)
        if m:
            return (
                f"{m.group(1)}{int(m.group(2)):02d}{int(m.group(3)):02d}",
                '',
            )
        # 20260330
        m = re.match(r'(?<!\d)(\d{8})(?!\d)', s)
        if m:
            return m.group(1), ''
        # 20260302170427
        m = re.match(r'(?<!\d)(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(?!\d)', s)
        if m:
            return (
                f"{m.group(1)}{m.group(2)}{m.group(3)}",
                f"{m.group(4)}{m.group(5)}{m.group(6)}",
            )
        return '', ''

    def _extract_seq_no(self, text: str) -> str:
        """从单格中识别流水号（带字母前缀的）"""
        m = re.search(r'\b([A-Z][0-9]{8,25}|[0-9]{14,25})\b', text)
        if m:
            return m.group(1)
        return ''

    def _extract_amounts(
        self, row_cells: List[str], column_map: Dict[str, int]
    ) -> Tuple[Decimal, Decimal, Decimal, Decimal, str]:
        """提取金额信息

        Returns:
            (credit, debit, signed_amount, balance, dc_flag)
            dc_flag: 'C' = 贷(收入), 'D' = 借(支出), '' = 未确定
        """
        credit = Decimal('0')
        debit = Decimal('0')
        signed_amt = Decimal('0')
        balance = Decimal('0')
        dc_flag = ''

        # 收集所有金额候选：(位置, 值, 是否带符号)
        amt_re = re.compile(
            r'([+\-]?)\s*([0-9]{1,3}(?:,[0-9]{3})*\.[0-9]{2}|[0-9]+\.[0-9]{2}|[0-9]{1,3}(?:,[0-9]{3})+)'
        )

        amounts_by_col: Dict[int, Tuple[str, Decimal]] = {}
        for col_idx, cell in enumerate(row_cells):
            for m in amt_re.finditer(cell):
                sign = m.group(1)
                raw = m.group(2).replace(',', '')
                try:
                    v = Decimal(raw)
                    if sign == '-':
                        v = -v
                    if col_idx not in amounts_by_col:
                        amounts_by_col[col_idx] = (sign or '+', v)
                except InvalidOperation:
                    continue

        # 根据 column_map 分配到 credit/debit/balance/tran_amt
        ci_credit = column_map.get('creditamount')
        ci_debit = column_map.get('debitamount')
        ci_tran = column_map.get('tran_amt')
        ci_bal = column_map.get('acct_bal')

        if ci_credit is not None and ci_credit in amounts_by_col:
            credit = abs(amounts_by_col[ci_credit][1])
        if ci_debit is not None and ci_debit in amounts_by_col:
            debit = abs(amounts_by_col[ci_debit][1])
        if ci_bal is not None and ci_bal in amounts_by_col:
            balance = amounts_by_col[ci_bal][1]

        # tran_amt: 带符号的金额，方向就是 dc_flag
        if ci_tran is not None and ci_tran in amounts_by_col:
            sign, v = amounts_by_col[ci_tran]
            signed_amt = v
            if sign == '-':
                dc_flag = 'D'
                debit = abs(v)
            else:
                dc_flag = 'C'
                credit = abs(v)

        # 关键：dc_flag 优先级 — 基于列位置（支出/存入）判断
        # 1. 优先看哪个金额列非零
        if not dc_flag:
            if debit > 0 and credit == 0:
                dc_flag = 'D'
            elif credit > 0 and debit == 0:
                dc_flag = 'C'
            elif debit > 0 and credit > 0:
                # 两个都非零：取较大的
                dc_flag = 'D' if debit > credit else 'C'

        return credit, debit, signed_amt, balance, dc_flag

    def _extract_counter_account(
        self, row_cells: List[str], column_map: Dict[str, int]
    ) -> str:
        """提取对方账号 - 优先按 column_map，失败则按内容启发式"""
        # 1. 优先按 column_map
        ci = column_map.get('to_acct_no')
        if ci is not None and ci < len(row_cells):
            cell = row_cells[ci].strip()
            # 折行合并：把当前格与下一格拼接（账号经常被拆成 2 段）
            if ci + 1 < len(row_cells):
                nxt = row_cells[ci + 1].strip()
                if nxt and re.match(r'^\d{1,8}$', nxt):
                    merged = cell + nxt
                    if 8 <= len(merged) <= 30 and merged.isdigit():
                        return merged
            # 单格
            if 8 <= len(cell) <= 30 and cell.isdigit():
                return cell
            cleaned = re.sub(r'\s+', '', cell)
            if 8 <= len(cleaned) <= 30 and cleaned.isdigit():
                return cleaned

        # 2. 备选启发式：找"长数字 cell"（8-25位纯数字）
        # 排除本方账号（header 提供的）、日期/时间、其他明显非账号
        candidates = []
        for i, c in enumerate(row_cells):
            d = re.sub(r'\s+', '', c)
            if d.isdigit() and 8 <= len(d) <= 25:
                # 排除日期/时间模式
                if len(d) == 8 and d.startswith(('20', '19')):
                    # 看起来像日期
                    try:
                        y, m, dd = int(d[:4]), int(d[4:6]), int(d[6:8])
                        if 1900 < y < 2100 and 1 <= m <= 12 and 1 <= dd <= 31:
                            continue
                    except ValueError:
                        pass
                if len(d) == 14 and d.startswith(('20', '19')):
                    # 像 yyyymmddHHMMSS
                    continue
                # 排除交易日期（已是 YYYY-MM-DD）
                if re.match(r'^\d{4}-\d{2}-\d{2}$', c.strip()):
                    continue
                candidates.append((i, d))
        if candidates:
            # 取最长的（账号通常比金额大）
            candidates.sort(key=lambda x: -len(x[1]))
            return candidates[0][1]
        return ''

    def _extract_counter_name(
        self, row_cells: List[str], column_map: Dict[str, int]
    ) -> str:
        """提取对方户名 - 优先内容启发式（找含"公司/集团"等的中文 cell），
        失败再回退到按 column_map。"""
        # 1. 优先启发式：找含"公司/集团/银行/支行/分行"的中文片段
        # 注意：合并相邻 cell 来支持"河南水利投资集团有" + "限公司"
        merged_text = ''.join(row_cells)
        m = re.search(
            r'([一-龥][一-龥（）()A-Za-z0-9·\.\-]{2,40}'
            r'(?:有限公司|有限责任公司|股份有限公司|集团|公司|银行|支行|分行))',
            merged_text
        )
        if m:
            return m.group(1)

        # 2. 回退到按 column_map
        ci = column_map.get('to_acct_name')
        if ci is not None and ci < len(row_cells):
            cell = row_cells[ci].strip()
            if 2 <= len(cell) <= 80:
                return cell
        return ''

    def _extract_remark(
        self, row_cells: List[str], column_map: Dict[str, int]
    ) -> str:
        """提取摘要"""
        ci = column_map.get('remark')
        if ci is not None and ci < len(row_cells):
            cell = row_cells[ci].strip()
            if ci + 1 < len(row_cells):
                nxt = row_cells[ci + 1].strip()
                if nxt and not re.match(r'^\d{2,}$', nxt) and len(nxt) <= 30:
                    cell = cell + nxt
            cell = cell.strip()
            if 2 <= len(cell) <= 100:
                return cell
        # 启发式：找含已知关键词的 cell
        keywords = ['资金归集', '同户名划转', '结息', '还息', '入息', '还本', '还款',
                    '贷款发放', '贷款归还', '网银', '跨行转账', '转账', '普通凭证',
                    '其它凭证', '电子转账', '网络转账', '受托支付', '归还贷款',
                    '转入', '转出', '收息', '汇出', '手续费', '代发', '代扣',
                    '联动下拨', '百瑞信托', '普通凭证', '凭证种类']
        for cell in row_cells:
            if any(kw in cell for kw in keywords):
                return cell
        return ''

    def _extract_use_name(
        self, row_cells: List[str], column_map: Dict[str, int]
    ) -> str:
        """提取用途"""
        ci = column_map.get('use_name')
        if ci is not None and ci < len(row_cells):
            cell = row_cells[ci].strip()
            if 2 <= len(cell) <= 100:
                return cell
        return ''


def create_pdf_parser(ocr_backend: Optional[OCRBackend] = None) -> PDFParser:
    """工厂函数：创建PDF解析器"""
    return PDFParser(ocr_backend=ocr_backend)
