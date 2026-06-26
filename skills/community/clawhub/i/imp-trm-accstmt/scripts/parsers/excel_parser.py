"""
Excel银行对账单解析器
支持国内各家银行的Excel格式银行对账单
"""

import os
import re
import logging
from typing import Optional, Dict, List, Tuple, Any
from datetime import datetime
from decimal import Decimal, InvalidOperation

try:
    import xlrd
except ImportError:
    xlrd = None

try:
    import openpyxl
except ImportError:
    openpyxl = None

from parsers.base_parser import BaseParser, ParseError
from core.data_structures import (
    BankStatementData, BankStatementHeader, BalanceInfo, TransactionRecord
)
from core.cosine_similarity import CosineSimilarityMatcher, COMMON_BANK_FIELD_ALIASES

logger = logging.getLogger(__name__)


class ExcelParser(BaseParser):
    """Excel银行对账单通用解析器"""

    # 银行账号相关的中文标签（支持各种变体）
    ACCOUNT_LABEL_PATTERNS = [
        r'^账号$', r'^账号[:：]?$', r'^账号[:：]\s*',
        r'^账户$', r'^账户[:：]?$',
        r'^卡号$', r'^卡号[:：]?$',
        r'^银行账号$', r'^银行账号[:：]?$',
        r'^客户账号$', r'^客户账号[:：]?$',
        r'^对公账号$', r'^对公账号[:：]?$',
        r'^选择账号$', r'^选择账号[:：]?$',
        r'^本方账号$', r'^本方账号[:：]?$',
        # 支持带空格的变体，如"账　　号"
        r'^账\s*号$', r'^账\s*号[:：]?$',
        r'^账　*号$',  # Unicode全角空格
    ]

    # 账号列名关键字（用于检测某列是否是账号列）
    ACCOUNT_COLUMN_KEYWORDS = [
        '账号', '卡号', '本方账号', '银行账号',
        '账户',  # 广西北部湾银行
    ]

    # 户名/名称相关的中文标签
    NAME_LABEL_PATTERNS = [
        r'^户名[:：]?$',
        r'^账户名称[:：]?$',
        r'^账户名[:：]?$',
        r'^客户名称[:：]?$',
        r'^单位名称[:：]?$',
        r'^户名[:：]',
        r'^企业名称[:：]?$',
    ]

    # 交易日期相关的列名
    DATE_COLUMN_PATTERNS = [
        '交易日期', '交易时间', '发生日期', '记账日期', '日期',
        'Transaction Date', 'Date', 'Trans Date', 'Value Date',
        '交易流水日期', '记录日期', '记账时间'
    ]

    # 流水号相关的列名（各种银行可能有不同的叫法）
    SEQ_NO_COLUMN_PATTERNS = [
        '流水号', '银行流水号', '交易流水号', '唯一流水号',
        '流水', '序号', '参考号', 'Reference',
        '银行流水号', '核心流水号', '柜员交易号', '发起方流水号',
        '对账编号', '流水编号', '交易编号', '业务编号',
        '银行流水号', '交易序号',
    ]

    # 对方账号的别名
    COUNTERPARTY_ACCOUNT_ALIASES = [
        '对方账号', '对方账户', '收款账号', '付款账号',
        '对手账号', '对手账户',
        '对方卡号', '收款人账号', '付款人账号',
        # 招商银行格式：收(付)方账号
        '收(付)方账号', '收(付)方卡号',
        'Counterparty Account', 'Beneficiary Account', 'Payee Account'
    ]

    # 对方名称的别名
    COUNTERPARTY_NAME_ALIASES = [
        '对方名称', '对方户名', '收款人', '付款人',
        '对手名称', '对手户名',
        '对方账户名称', '收款人名称', '付款人名称',
        # 招商银行格式：收(付)方名称
        '收(付)方名称', '收(付)方',
        'Counterparty Name', 'Beneficiary', 'Payee'
    ]

    # 对方银行名称的别名
    COUNTERPARTY_BANK_ALIASES = [
        '对方银行', '对方开户行', '对方行名',
        '对手银行', '对手开户行',
        '收款行', '付款行',
        # 招商银行格式：收(付)方开户行
        '收(付)方开户行', '收(付)方行号',
        '收(付)方地址', '收(付)方省份',
    ]

    def __init__(self):
        self.similarity_matcher = CosineSimilarityMatcher(
            threshold=0.7,
            fallback_threshold=0.5
        )
        # 增强的别名映射
        enhanced_aliases = dict(COMMON_BANK_FIELD_ALIASES)
        enhanced_aliases['to_acct_no'] = COMMON_BANK_FIELD_ALIASES.get('to_acct_no', []) + self.COUNTERPARTY_ACCOUNT_ALIASES
        enhanced_aliases['to_acct_name'] = COMMON_BANK_FIELD_ALIASES.get('to_acct_name', []) + self.COUNTERPARTY_NAME_ALIASES
        enhanced_aliases['to_acct_bank_name'] = COMMON_BANK_FIELD_ALIASES.get('to_acct_bank_name', []) + self.COUNTERPARTY_BANK_ALIASES
        self.similarity_matcher.set_aliases(enhanced_aliases)

    @property
    def format_name(self) -> str:
        return "Excel Bank Statement"

    def detect_format(self, file_path: str) -> bool:
        """
        检测文件是否为Excel格式的银行对账单

        Args:
            file_path: 文件路径

        Returns:
            True if file appears to be Excel format bank statement
        """
        try:
            import pandas as pd

            self.validate_file(file_path)

            # 检查文件扩展名
            ext = os.path.splitext(file_path)[1].lower()
            if ext not in ['.xlsx', '.xls']:
                return False

            # 尝试读取并检查是否包含银行对账单特征
            sheets = self._read_excel(file_path)
            if not sheets:
                return False

            # 日期关键字（需要完整匹配整个词）
            date_keywords = ['交易日期', '交易时间', '发生日期', '记账日期', '交易流水日期', '记账时间', '记录日期']
            # 日期相关的列名字符串（用于检测表头行）
            date_header_keywords = ['交易日期', '交易时间', '对方账号', '对方户名', '借方发生额', '贷方发生额', '支出', '收入', '余额', '摘要', '凭证号', '流水号']
            # 日期格式模式（用于检测数据行）
            date_format_pattern = r'\d{4}-\d{2}-\d{2}'

            # 检查每个sheet
            for sheet_name, df in sheets.items():
                if df is None or df.empty:
                    continue

                # 遍历前20行查找关键字
                for row_idx in range(min(20, len(df))):
                    row = df.iloc[row_idx]
                    row_values = [str(v) for v in row.values if pd.notna(v) and str(v).strip()]
                    row_str = ''.join(row_values)

                    # 检查是否包含完整的日期关键字
                    for keyword in date_keywords:
                        if keyword in row_str:
                            return True

                    # 检查是否包含多个日期相关列名（表头行特征）
                    header_keyword_count = sum(1 for kw in date_header_keywords if kw in row_str)
                    if header_keyword_count >= 2:
                        # 检查后续行是否有日期格式的数据
                        for next_row_idx in range(row_idx + 1, min(row_idx + 10, len(df))):
                            next_row = df.iloc[next_row_idx]
                            next_row_values = [str(v) for v in next_row.values if pd.notna(v)]
                            next_row_str = ''.join(next_row_values)
                            # 检查是否有日期格式
                            if re.search(date_format_pattern, next_row_str):
                                return True

            return False

        except Exception as e:
            logger.debug(f"Format detection failed: {e}")
            return False

    def _read_excel(self, file_path: str) -> Dict[str, 'pd.DataFrame']:
        """
        读取Excel文件
        返回字典，key是sheet名，value是DataFrame
        注意：不使用header参数，让pandas自动处理，让用户代码决定哪一行是表头

        支持格式：
        - .xlsx: openpyxl引擎
        - .xls: xlrd引擎
        - HTML格式文件（伪装成.xls）：使用read_html解析
        """
        import pandas as pd

        try:
            if file_path.endswith('.xlsx'):
                return pd.read_excel(file_path, sheet_name=None, engine='openpyxl', header=None)
            else:
                # 尝试xlrd读取
                try:
                    if xlrd is not None:
                        return pd.read_excel(file_path, sheet_name=None, engine='xlrd', header=None)
                except Exception:
                    pass

                # 尝试HTML读取（某些.xls文件实际上是HTML格式）
                return self._read_html_excel(file_path)

        except Exception as e:
            logger.debug(f"Excel read error: {e}")
            # 尝试HTML读取作为后备
            return self._read_html_excel(file_path)

    def _read_html_excel(self, file_path: str) -> Dict[str, 'pd.DataFrame']:
        """
        尝试读取HTML格式的Excel文件
        某些银行系统导出的.xls文件实际上是HTML格式
        """
        import pandas as pd

        try:
            # 读取文件前几行检查是否为HTML
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(500)

            if '<html' in content.lower() or '<table' in content.lower():
                logger.info(f"检测到HTML格式文件: {file_path}")
                # 使用pandas的read_html读取所有表格
                tables = pd.read_html(file_path, encoding='utf-8', header=None)
                result = {}
                for i, df in enumerate(tables):
                    sheet_name = f"Sheet{i+1}"
                    result[sheet_name] = df
                return result
        except Exception as e:
            logger.debug(f"HTML read error: {e}")

        return {}

    def parse(self, file_path: str, **kwargs) -> BankStatementData:
        """
        解析Excel银行对账单

        Args:
            file_path: 文件路径
            **kwargs:
                - account_number: 手动指定的本方账号
                - bank_name: 手动指定的银行名称

        Returns:
            BankStatementData: 解析后的数据
        """
        import pandas as pd

        self.validate_file(file_path)

        result = BankStatementData()
        result.source_file = os.path.basename(file_path)
        result.source_format = self.format_name

        try:
            # 读取Excel
            sheets = self._read_excel(file_path)
            if not sheets:
                result.add_error("无法读取Excel文件")
                return result

            # 处理每个sheet
            for sheet_name, df in sheets.items():
                if df is None or df.empty:
                    continue

                # 转换为列表形式便于处理
                data_rows = []
                for _, row in df.iterrows():
                    row_list = [v if pd.notna(v) else None for v in row.values]
                    data_rows.append(row_list)

                # 查找账号信息（可能在表头区域）
                account_info = self._find_account_info(data_rows, None)
                if account_info['account_number']:
                    result.header.account_number = account_info['account_number']
                if account_info['account_name']:
                    result.header.raw_tags['account_name'] = account_info['account_name']
                if account_info['currency']:
                    result.default_currency = account_info['currency']

                # 如果没有找到币种，设置为默认值
                if not result.default_currency:
                    result.default_currency = 'CNY'

                # 查找数据开始行（包含"交易日期"或"交易时间"的行）
                header_row_idx, header_row = self._find_header_row(data_rows, None)

                if header_row_idx < 0:
                    result.add_warning(f"Sheet '{sheet_name}': 未找到交易明细表头")
                    continue

                # 映射列索引
                column_mapping = self._map_columns(header_row)

                # 解析交易数据
                data_start_idx = header_row_idx + 1
                for row_idx in range(data_start_idx, len(data_rows)):
                    row = data_rows[row_idx]

                    # 跳过空行
                    if self._is_empty_row(row):
                        continue

                    # 解析交易记录 - 传递默认币种
                    txn = self._parse_transaction_row(
                        row, column_mapping,
                        result.header.account_number,
                        result.default_currency
                    )
                    if txn:
                        result.add_transaction(txn)

            # 验证结果
            if not result.header.account_number:
                result.add_warning("未找到账号信息")

            if not result.transactions:
                result.add_warning("未找到交易记录")

        except Exception as e:
            result.add_error(f"解析失败: {str(e)}")
            logger.exception(e)

        return result

    def _find_account_info(self, data_rows: List, headers: List) -> Dict[str, str]:
        """
        查找账号信息
        支持从表头区域的键值对中提取账号、户名、币种
        支持多种账号列名变体：
        - "账号"、"卡号"、"本方账号"、"银行账号"
        - "账户"（广西北部湾银行）
        - "账　　号"（带空格，如国开行）
        """
        info = {
            'account_number': '',
            'account_name': '',
            'currency': ''
        }

        # 支持的账号标签模式
        account_label_patterns = [
            r'^账号',  # 匹配"账号:"、"账号"等
            r'^账户',  # 匹配"账户:"、"账户"等
            r'^卡号',  # 匹配"卡号:"、"卡号"等
            r'^本方账号',
            r'^银行账号',
            r'^选择账号',
            # 带空格的变体
            r'^账\s+号',  # 英文空格
            r'^账　+号',  # Unicode全角空格（国开行格式）
        ]

        # 遍历前30行查找账号信息
        max_rows = min(30, len(data_rows))

        # 方案A：优先查找包含"银行账号"标签的行（这是最明确的账号标识）
        bank_account_rows = []
        for row_idx in range(max_rows):
            row = data_rows[row_idx]
            if self._is_empty_row(row):
                continue
            row_str = ''.join([str(v) for v in row if v is not None])
            if '银行账号' in row_str:
                bank_account_rows.append((row_idx, row))

        # 如果找到"银行账号"行，在这些行中查找账号
        if bank_account_rows:
            for row_idx, row in bank_account_rows:
                for i, cell in enumerate(row):
                    if cell is None:
                        continue
                    cell_str = str(cell).strip()
                    # 检查是否是"银行账号"标签
                    if cell_str == '银行账号':
                        # 检查后续单元格
                        for j in range(i + 1, min(i + 3, len(row))):
                            if row[j] is not None:
                                next_val = str(row[j]).strip()
                                if self._is_likely_account(next_val):
                                    clean_account = self._clean_account_number(next_val)
                                    if clean_account and len(clean_account) >= 10:  # 银行账号通常10位以上
                                        info['account_number'] = clean_account
                                        break
                        if info['account_number']:
                            break
                if info['account_number']:
                    break

        # 方案B：如果还没找到，查找包含其他账号关键字的行
        if not info['account_number']:
            for row_idx in range(max_rows):
                row = data_rows[row_idx]
                if self._is_empty_row(row):
                    continue

                row_str = ''.join([str(v) for v in row if v is not None])

                # 检查是否包含账号相关的关键字
                has_account_keyword = any(kw in row_str for kw in self.ACCOUNT_COLUMN_KEYWORDS)

                if has_account_keyword:
                    # 方案1：查找账号标签后面的数值（同一行中的键值对）
                    for i, cell in enumerate(row):
                        if cell is None:
                            continue
                        cell_str = str(cell).strip()
                        # 检查是否是账号标签
                        is_account_label = False
                        for pattern in account_label_patterns:
                            if re.match(pattern, cell_str):
                                is_account_label = True
                                break
                        if is_account_label:
                            # 检查后续单元格
                            for j in range(i + 1, min(i + 3, len(row))):
                                if row[j] is not None:
                                    next_val = str(row[j]).strip()
                                    if self._is_likely_account(next_val):
                                        clean_account = self._clean_account_number(next_val)
                                        # 优先找10位以上的账号，但也要接受8-9位的账号
                                        if clean_account and len(clean_account) >= 8:
                                            info['account_number'] = clean_account
                                            break
                            if info['account_number']:
                                break

                    # 方案2：如果没有找到键值对，查找已经是数值型的账号
                    if not info['account_number']:
                        for cell in row:
                            if cell is None:
                                continue
                            cell_str = str(cell).strip()
                            if self._is_likely_account(cell_str):
                                clean_account = self._clean_account_number(cell_str)
                                # 优先选择10位以上的账号，但也要接受8-9位的账号
                                if clean_account and len(clean_account) >= 8:
                                    info['account_number'] = clean_account
                                    break

                if info['account_number']:
                    break

            # 匹配户名/名称 - 查找包含"名称"或"户名"关键字
            if '名称' in row_str or '户名' in row_str:
                for i, cell in enumerate(row):
                    if cell is None:
                        continue
                    cell_str = str(cell).strip()
                    if cell_str in ['户名', '账户名称', '账户名', '客户名称', '单位名称', '企业名称']:
                        for j in range(i + 1, min(i + 3, len(row))):
                            if row[j] is not None:
                                name_val = str(row[j]).strip()
                                # 排除币种、账号等
                                if name_val and name_val not in ['人民币', '美元', '欧元', '港币', '日元', '英镑', 'CNY', 'USD', 'EUR']:
                                    # 检查是否像公司名称
                                    if len(name_val) >= 2 and not name_val.isdigit():
                                        info['account_name'] = name_val
                                        break
                        break

            # 匹配币种 - 在全局查找
            currency_keywords = ['人民币', '美元', '欧元', '港币', '日元', '英镑', 'CNY', 'USD', 'EUR', 'HKD', 'JPY', 'GBP']
            for cell in row:
                if cell is None:
                    continue
                cell_str = str(cell).strip()
                # 检查是否是币种
                if cell_str in currency_keywords:
                    info['currency'] = '人民币' if cell_str in ['人民币', 'CNY'] else cell_str
                    break
                # 检查括号中的币种
                if '（人民币）' in cell_str or '(人民币)' in cell_str or '人民币）' in cell_str:
                    info['currency'] = '人民币'
                    break

        return info

    def _is_likely_account(self, value: str) -> bool:
        """判断字符串是否像银行账号"""
        if not value:
            return False
        # 移除币种信息后再检查
        cleaned = self._clean_account_number(value)
        if not cleaned:
            return False
        # 账号通常是10-25位数字
        if cleaned.isdigit() and 8 <= len(cleaned) <= 25:
            return True
        return False

    def _clean_account_number(self, account_str: str) -> str:
        """
        清理账号中的币种信息
        支持多种格式：
        - 2048274286000188（人民币）
        - CNY123456789
        - USD-123456789
        - 123456789[USD]
        - 账号: 1234567890（人民币）
        """
        if not account_str:
            return ''

        cleaned = str(account_str).strip()

        # 移除各种括号中的币种
        # （人民币）、(人民币)、人民币）
        cleaned = re.sub(r'[（(][一-鿿]{2,4}[）)]$', '', cleaned)
        cleaned = re.sub(r'[一-鿿]{2,4}[）)]$', '', cleaned)

        # (CNY)、[CNY]、CNY
        cleaned = re.sub(r'[（(][A-Z]{3}[)）\]]$', '', cleaned)
        cleaned = re.sub(r'[A-Z]{3}[)）\]]$', '', cleaned)

        # 移除开头的币种代码
        cleaned = re.sub(r'^(CNY|USD|EUR|HKD|JPY|GBP|CNY|人民币|美元|欧元|港币|日元|英镑)[:：\s\-]?', '', cleaned, flags=re.IGNORECASE)

        # 移除方括号中的币种
        cleaned = re.sub(r'[\[【][A-Z]{3}[】\]]$', '', cleaned, flags=re.IGNORECASE)

        # 移除横线后的币种
        cleaned = re.sub(r'[-_][A-Z]{3}$', '', cleaned, flags=re.IGNORECASE)

        # 移除"账号:"、"账号："等前缀
        cleaned = re.sub(r'^账号[:：\s]+', '', cleaned)
        cleaned = re.sub(r'^选择账号[:：\s]+', '', cleaned)

        return cleaned.strip()

    def _find_header_row(self, data_rows: List, headers: List) -> Tuple[int, List]:
        """
        查找包含"交易日期"或"交易时间"的表头行
        返回 (行索引, 行数据)

        表头行特征：包含多个银行对账单列名关键字
        """
        # 表头行应该包含的列名关键字
        header_keywords = [
            '交易日期', '交易时间', '发生日期', '记账日期',
            '交易流水', '凭证号', '流水号',
            '对方账号', '对方户名', '对方名称', '对手账号', '对手户名',
            '借方发生额', '贷方发生额', '借方金额', '贷方金额',
            '支出', '收入', '余额', '摘要', '附言', '备注',
            '本方账号', '本方户名', '银行账号', '账号',
            # 招商银行格式
            '收(付)方账号', '收(付)方名称', '收(付)方开户行',
        ]

        for row_idx, row in enumerate(data_rows[:30]):  # 只检查前30行
            if self._is_empty_row(row):
                continue

            # 检查这一行包含多少个表头关键字
            row_cells = [str(cell) for cell in row if cell is not None]
            row_str = ''.join(row_cells)

            keyword_count = sum(1 for kw in header_keywords if kw in row_str)

            # 如果包含至少3个表头关键字，认为是表头行
            if keyword_count >= 3:
                return row_idx, row

        # 如果没找到，尝试更宽松的匹配：只要包含日期或时间相关列
        relaxed_keywords = ['交易日期', '交易时间', '日期', '时间', '发生额', '借', '贷', '余额']
        for row_idx, row in enumerate(data_rows[:30]):
            if self._is_empty_row(row):
                continue
            row_cells = [str(cell) for cell in row if cell is not None]
            row_str = ''.join(row_cells)
            keyword_count = sum(1 for kw in relaxed_keywords if kw in row_str)
            if keyword_count >= 3:
                return row_idx, row

        return -1, []

    def _map_columns(self, header_row: List) -> Dict[str, int]:
        """
        使用余弦相似度映射列索引到目标字段
        """
        mapping = {}

        # 构建目标字段列表（包含别名）
        target_fields = list(COMMON_BANK_FIELD_ALIASES.keys())
        expanded_targets = list(target_fields)
        for field, aliases in COMMON_BANK_FIELD_ALIASES.items():
            expanded_targets.extend(aliases)

        # 增强的别名
        expanded_targets.extend(self.COUNTERPARTY_ACCOUNT_ALIASES)
        expanded_targets.extend(self.COUNTERPARTY_NAME_ALIASES)
        expanded_targets.extend(self.COUNTERPARTY_BANK_ALIASES)
        expanded_targets.extend(self.DATE_COLUMN_PATTERNS)

        self.similarity_matcher.build_index(expanded_targets)

        # 匹配每个列名 - 按列顺序遍历
        # 关键规则：只设置尚未映射的字段，如果已映射则不覆盖
        # 这样"交易日期"会先匹配到tran_date，"退汇日期"中的"日期"不会覆盖
        for col_idx, header in enumerate(header_row):
            if header is None:
                continue

            header_str = str(header).strip()
            if not header_str:
                continue

            matched_field, score = self.similarity_matcher.match(header_str)

            if matched_field and score >= 0.6:
                # 检查是否在原始目标字段中
                if matched_field in target_fields:
                    # 只有当该字段尚未映射时才设置
                    if matched_field not in mapping:
                        mapping[matched_field] = col_idx
                else:
                    # 找到真实的目标字段
                    for tf in target_fields:
                        if matched_field in COMMON_BANK_FIELD_ALIASES.get(tf, []):
                            # 只有当该目标字段尚未映射时才设置
                            if tf not in mapping:
                                mapping[tf] = col_idx
                                break  # 找到目标后break，避免同一列重复匹配
                        # 检查增强的别名
                        if tf == 'to_acct_no' and matched_field in self.COUNTERPARTY_ACCOUNT_ALIASES:
                            if tf not in mapping:
                                mapping[tf] = col_idx
                                break
                        if tf == 'to_acct_name' and matched_field in self.COUNTERPARTY_NAME_ALIASES:
                            if tf not in mapping:
                                mapping[tf] = col_idx
                                break
                        if tf == 'to_acct_bank_name' and matched_field in self.COUNTERPARTY_BANK_ALIASES:
                            if tf not in mapping:
                                mapping[tf] = col_idx
                                break

        # 手动检查流水号列（各种银行的叫法不同）
        # 优先检查是否已经映射了bank_seq_no，如果没有，检查是否是流水号列
        if 'bank_seq_no' not in mapping:
            for col_idx, header in enumerate(header_row):
                if header is None:
                    continue
                header_str = str(header).strip()
                if not header_str:
                    continue
                # 检查是否匹配流水号模式
                for seq_pattern in self.SEQ_NO_COLUMN_PATTERNS:
                    if seq_pattern in header_str:
                        mapping['bank_seq_no'] = col_idx
                        break
                if 'bank_seq_no' in mapping:
                    break

        return mapping

    def _is_empty_row(self, row: List) -> bool:
        """判断是否为空行"""
        return all(v is None or str(v).strip() == '' or str(v).strip() == 'nan'
                   for v in row)

    def _parse_transaction_row(
        self,
        row: List,
        column_mapping: Dict[str, int],
        default_account: str,
        default_currency: str = '人民币'
    ) -> Optional[TransactionRecord]:
        """解析单行交易数据"""
        try:
            txn = TransactionRecord()

            # 设置默认币种
            txn.currency_code = default_currency if default_currency else 'CNY'

            # 获取账号
            account_idx = column_mapping.get('bankaccount_account')
            if account_idx is not None and account_idx < len(row):
                account = row[account_idx]
                if account:
                    account_str = str(account).strip()
                    clean_account = self._clean_account_number(account_str)
                    if clean_account:
                        txn.account_number = clean_account
            if not txn.account_number:
                txn.account_number = default_account

            # 获取流水号（银行交易流水号）
            seq_no_idx = column_mapping.get('bank_seq_no')
            if seq_no_idx is not None and seq_no_idx < len(row):
                seq_value = row[seq_no_idx]
                if seq_value:
                    seq_str = str(seq_value).strip()
                    # 排除空值和"NONREF"等无效值
                    if seq_str and seq_str.upper() not in ['', 'NONREF', 'NONE', 'NULL']:
                        txn.reference_number = seq_str

            # 获取交易日期和时间 - 需要分离日期和时间
            date_idx = column_mapping.get('tran_date')
            time_idx = column_mapping.get('tran_time')

            # 处理日期和时间列
            # 情况1: 单独的日期列或时间列
            # 情况2: "交易时间"列同时包含日期和时间（如民生银行格式"2025-06-21 00:11:24"）
            processed_cols = set()  # 记录已处理的列索引

            if date_idx is not None and date_idx < len(row):
                date_value = row[date_idx]
                if date_value:
                    date_str = str(date_value).strip()
                    # 分离日期和时间
                    parsed_date, parsed_time = self._parse_date_time(date_str)
                    if parsed_date and not txn.value_date:
                        txn.value_date = parsed_date
                    if parsed_time and not txn.transaction_time:
                        txn.transaction_time = parsed_time
                    processed_cols.add(date_idx)

            # 如果没有单独的时间列，尝试从其他列获取
            if time_idx is not None and time_idx < len(row) and time_idx not in processed_cols:
                time_value = row[time_idx]
                if time_value:
                    time_str = str(time_value).strip()
                    # 如果时间值包含日期（格式如"2025-06-21 00:11:24"），需要分离
                    if ' ' in time_str or 'T' in time_str:
                        parsed_date, parsed_time = self._parse_date_time(time_str)
                        if parsed_time and not txn.transaction_time:
                            txn.transaction_time = parsed_time
                        # 如果value_date还没有设置，从这里提取日期
                        if parsed_date and not txn.value_date:
                            txn.value_date = parsed_date
                    else:
                        txn.transaction_time = self._parse_time(time_str)
                    processed_cols.add(time_idx)

            # 获取借贷标识
            dc_idx = column_mapping.get('dc_flag')
            if dc_idx is not None and dc_idx < len(row):
                dc_value = row[dc_idx]
                if dc_value:
                    txn.dc_indicator = self._parse_dc_flag(str(dc_value))

            # 获取借方金额
            debit_idx = column_mapping.get('debitamount')
            if debit_idx is not None and debit_idx < len(row):
                debit_value = row[debit_idx]
                if debit_value is not None and str(debit_value).strip():
                    try:
                        txn.debit_amount = Decimal(str(debit_value).replace(',', ''))
                        if txn.dc_indicator == '' and txn.debit_amount > 0:
                            txn.dc_indicator = 'D'
                            txn.amount = txn.debit_amount
                    except (InvalidOperation, ValueError):
                        pass

            # 获取贷方金额
            credit_idx = column_mapping.get('creditamount')
            if credit_idx is not None and credit_idx < len(row):
                credit_value = row[credit_idx]
                if credit_value is not None and str(credit_value).strip():
                    try:
                        txn.credit_amount = Decimal(str(credit_value).replace(',', ''))
                        if txn.dc_indicator == '' and txn.credit_amount > 0:
                            txn.dc_indicator = 'C'
                            txn.amount = txn.credit_amount
                    except (InvalidOperation, ValueError):
                        pass

            # 获取金额（如果借贷金额都没有）
            if txn.amount == 0:
                amount_idx = column_mapping.get('tran_amt')
                if amount_idx is not None and amount_idx < len(row):
                    amount = row[amount_idx]
                    if amount is not None:
                        try:
                            txn.amount = Decimal(str(amount).replace(',', ''))
                        except (InvalidOperation, ValueError):
                            txn.amount = Decimal('0')

            # 获取对方账号
            counter_acct_idx = column_mapping.get('to_acct_no')
            if counter_acct_idx is not None and counter_acct_idx < len(row):
                counter_acct = row[counter_acct_idx]
                if counter_acct:
                    counter_acct_str = str(counter_acct).strip()
                    # 清理账号
                    clean_counter_acct = self._clean_account_number(counter_acct_str)
                    txn.counterparty_account = clean_counter_acct if clean_counter_acct else counter_acct_str

            # 获取对方名称
            counter_name_idx = column_mapping.get('to_acct_name')
            if counter_name_idx is not None and counter_name_idx < len(row):
                counter_name = row[counter_name_idx]
                if counter_name:
                    txn.counterparty_name = str(counter_name).strip()

            # 获取摘要
            remark_idx = column_mapping.get('remark')
            if remark_idx is not None and remark_idx < len(row):
                remark = row[remark_idx]
                if remark:
                    txn.transaction_description = str(remark).strip()

            # 获取余额
            balance_idx = column_mapping.get('acct_bal')
            if balance_idx is not None and balance_idx < len(row):
                balance = row[balance_idx]
                if balance is not None and str(balance).strip():
                    try:
                        txn.running_balance = Decimal(str(balance).replace(',', ''))
                    except (InvalidOperation, ValueError):
                        pass

            # 检查是否是有效的数据行
            # 跳过包含表头文字的行
            row_str = ''.join([str(v) for v in row if v is not None])
            header_keywords = ['交易日期', '交易时间', '对方账号', '对方户名', '借方发生额', '贷方发生额',
                            '账户名称', '账号', '表头', '表尾', '合计', '总计', '小计']
            # 关键表头关键字（这些不应该出现在数据行中）
            critical_header_keywords = ['账户名称', '户名:', '表头', '表尾', '合计', '总计', '小计']
            if any(kw in row_str for kw in critical_header_keywords):
                return None  # 跳过包含关键表头关键字的行
            if any(kw in row_str for kw in header_keywords):
                # 检查是否是真正的表头行
                keyword_count = sum(1 for kw in header_keywords if kw in row_str)
                if keyword_count >= 2:
                    return None  # 跳过表头行

            # 跳过垃圾数据行（错误消息行）
            # 检查是否包含特定的错误模式
            garbage_patterns = [
                '超过255',      # 错误,超过255,字符
                '日期格式',      # 日期格式不正确
                '错误',          # 任何错误消息
                '唯一',          # 唯一性错误
                '重复',          # 重复性错误
            ]
            garbage_count = sum(1 for kw in garbage_patterns if kw in row_str)
            if garbage_count >= 1:
                return None  # 跳过包含任何垃圾关键字的行

            # 如果没有有效的交易数据，跳过
            if not txn.value_date and txn.amount == 0:
                return None

            return txn

        except Exception as e:
            logger.debug(f"Row parse error: {e}")
            return None

    def _parse_date(self, date_str: str) -> str:
        """解析日期字符串为 YYYYMMDD 格式"""
        if not date_str:
            return ''

        date_str = date_str.strip()

        # 已经是中国格式
        if re.match(r'^\d{4}-\d{2}-\d{2}', date_str):
            return date_str.replace('-', '')
        if re.match(r'^\d{4}/\d{2}/\d{2}', date_str):
            return date_str.replace('/', '')
        if re.match(r'^\d{8}$', date_str):
            return date_str

        # 尝试常见格式
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S',
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%Y%m%d %H:%M:%S',
            '%Y%m%d%H%M%S',
            '%d/%m/%Y',
            '%m/%d/%Y',
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y%m%d')
            except ValueError:
                continue

        return date_str

    def _parse_date_time(self, date_time_str: str) -> Tuple[str, str]:
        """
        分离日期和时间

        Args:
            date_time_str: 日期时间字符串

        Returns:
            (日期字符串YYYYMMDD, 时间字符串HHMMSS)
        """
        if not date_time_str:
            return '', ''

        date_time_str = date_time_str.strip()

        # 如果包含空格，可能是 "2026-03-21 00:25:11"
        if ' ' in date_time_str:
            parts = date_time_str.split(' ', 1)
            date_part = parts[0]
            time_part = parts[1] if len(parts) > 1 else ''
        elif 'T' in date_time_str:
            # ISO格式 "2026-03-21T00:25:11"
            parts = date_time_str.split('T', 1)
            date_part = parts[0]
            time_part = parts[1] if len(parts) > 1 else ''
        else:
            date_part = date_time_str
            time_part = ''

        # 解析日期
        parsed_date = self._parse_date(date_part)

        # 解析时间
        parsed_time = self._parse_time(time_part) if time_part else ''

        return parsed_date, parsed_time

    def _parse_time(self, time_str: str) -> str:
        """
        解析时间字符串为 HHMMSS 格式
        """
        if not time_str:
            return ''

        time_str = time_str.strip()

        # 已经是HHMMSS格式
        if re.match(r'^\d{6}$', time_str):
            return time_str

        # HH:MM:SS 格式
        if re.match(r'^\d{2}:\d{2}:\d{2}', time_str):
            return time_str.replace(':', '')

        # 尝试从混合字符串中提取时间
        time_match = re.search(r'(\d{2}):(\d{2}):(\d{2})', time_str)
        if time_match:
            return f"{time_match.group(1)}{time_match.group(2)}{time_match.group(3)}"

        # 尝试提取纯数字时间
        time_match = re.search(r'(\d{2})(\d{2})(\d{2})', time_str)
        if time_match:
            return f"{time_match.group(1)}{time_match.group(2)}{time_match.group(3)}"

        return time_str

    def _parse_dc_flag(self, dc_str: str) -> str:
        """解析借贷标识"""
        if not dc_str:
            return ''

        dc_str = dc_str.strip().upper()

        # 收入/存款
        if dc_str in ['C', 'CR', '贷', '收入', '存款', '贷方', '贷记', '转入', 'CRDT', 'DEPOSIT']:
            return 'C'

        # 支出/取款
        if dc_str in ['D', 'DR', '借', '支出', '取款', '借方', '借记', '转出', 'DEBIT', 'WITHDRAWAL']:
            return 'D'

        return ''


def create_excel_parser() -> ExcelParser:
    """工厂函数：创建Excel解析器"""
    return ExcelParser()
