"""
发票信息提取器
使用OCR技术从图片和PDF中提取发票信息
"""

import re
import os
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image
import numpy as np

from invoice_model import InvoiceInfo, InvoiceItem


class InvoiceExtractor:
    """发票信息提取器"""

    def __init__(self):
        self.ocr = None
        self._init_ocr()

    def _init_ocr(self):
        """初始化OCR引擎"""
        try:
            from paddleocr import PaddleOCR
            # 使用中文模型
            self.ocr = PaddleOCR(
                lang='ch'
            )
            print("[OK] OCR引擎初始化成功")
        except Exception as e:
            print(f"[FAIL] OCR引擎初始化失败: {e}")
            raise

    def extract_from_file(self, file_path: str) -> Optional[InvoiceInfo]:
        """
        从文件中提取发票信息

        Args:
            file_path: 文件路径（图片或PDF）

        Returns:
            InvoiceInfo对象，提取失败返回None
        """
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"[FAIL] 文件不存在: {file_path}")
            return None

        # 根据文件类型选择提取方式
        suffix = file_path.suffix.lower()

        if suffix in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']:
            return self._extract_from_image(file_path)
        elif suffix == '.pdf':
            return self._extract_from_pdf(file_path)
        else:
            print(f"[FAIL] 不支持的文件格式: {suffix}")
            return None

    def _extract_from_image(self, image_path: Path) -> Optional[InvoiceInfo]:
        """从图片中提取发票信息"""
        try:
            # 使用OCR识别文字
            result = self.ocr.ocr(str(image_path))

            if not result or not result[0]:
                print(f"[FAIL] 未能从图片中识别到文字: {image_path}")
                return None

            # 提取所有文本行
            text_lines = []
            for line in result[0]:
                if line:
                    text = line[1][0]  # 获取识别的文本
                    confidence = line[1][1]  # 获取置信度
                    if confidence > 0.5:  # 过滤低置信度结果
                        text_lines.append(text)

            # 解析发票信息
            invoice_info = self._parse_invoice_text(text_lines)
            invoice_info.source_file = str(image_path)
            invoice_info.extraction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return invoice_info

        except Exception as e:
            print(f"[FAIL] 图片OCR处理失败: {e}")
            # 尝试使用PDF方式处理图片（将图片转为PDF再处理）
            return self._extract_image_as_pdf(image_path)

    def _extract_from_pdf(self, pdf_path: Path) -> Optional[InvoiceInfo]:
        """从PDF中提取发票信息"""
        try:
            # 打开PDF文件
            doc = fitz.open(str(pdf_path))

            all_text_lines = []

            # 遍历每一页
            for page_num in range(len(doc)):
                page = doc[page_num]

                # 首先尝试直接提取文本
                text = page.get_text()
                if text.strip():
                    text_lines = [line.strip() for line in text.split('\n') if line.strip()]
                    all_text_lines.extend(text_lines)
                else:
                    # 如果没有文本，将页面转为图片进行OCR
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2倍分辨率
                    img_data = pix.tobytes("png")

                    # 保存临时图片
                    temp_img_path = Path(".temp/cache") / f"pdf_page_{page_num}.png"
                    temp_img_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(temp_img_path, 'wb') as f:
                        f.write(img_data)

                    # OCR识别
                    result = self.ocr.ocr(str(temp_img_path))
                    if result and result[0]:
                        for line in result[0]:
                            if line:
                                text = line[1][0]
                                confidence = line[1][1]
                                if confidence > 0.5:
                                    all_text_lines.append(text)

                    # 清理临时文件
                    temp_img_path.unlink(missing_ok=True)

            doc.close()

            if not all_text_lines:
                print(f"[FAIL] 未能从PDF中识别到文字: {pdf_path}")
                return None

            # 解析发票信息
            invoice_info = self._parse_invoice_text(all_text_lines)
            invoice_info.source_file = str(pdf_path)
            invoice_info.extraction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return invoice_info

        except Exception as e:
            print(f"[FAIL] PDF处理失败: {e}")
            return None

    def _parse_invoice_text(self, text_lines: List[str]) -> InvoiceInfo:
        """
        从OCR识别的文本中解析发票信息

        Args:
            text_lines: 识别的文本行列表

        Returns:
            InvoiceInfo对象
        """
        invoice = InvoiceInfo()
        full_text = '\n'.join(text_lines)

        # 提取发票代码（10-12位数字）
        invoice.invoice_code = self._extract_invoice_code(full_text)

        # 提取发票号码（8-20位数字）
        invoice.invoice_number = self._extract_invoice_number(full_text)

        # 提取开票日期
        invoice.invoice_date = self._extract_invoice_date(full_text)

        # 提取购买方信息
        invoice.buyer_name = self._extract_buyer_name(text_lines, full_text)
        invoice.buyer_tax_number = self._extract_buyer_tax_number(text_lines, full_text)
        invoice.buyer_address = self._extract_buyer_address(text_lines, full_text)
        invoice.buyer_bank = self._extract_buyer_bank(text_lines, full_text)

        # 提取销售方信息
        invoice.seller_name = self._extract_seller_name(text_lines, full_text)
        invoice.seller_tax_number = self._extract_seller_tax_number(text_lines, full_text)
        invoice.seller_address = self._extract_seller_address(text_lines, full_text)
        invoice.seller_bank = self._extract_seller_bank(text_lines, full_text)

        # 提取金额信息
        invoice.total_amount, invoice.total_tax_amount, invoice.total_amount_with_tax = \
            self._extract_amounts(text_lines, full_text)

        # 提取其他信息
        invoice.remarks = self._extract_remarks(text_lines, full_text)
        invoice.checker = self._extract_person(text_lines, "复核")
        invoice.payee = self._extract_person(text_lines, "收款")
        invoice.issuer = self._extract_person(text_lines, "开票")

        # 提取商品明细
        invoice.items = self._extract_items(text_lines)

        return invoice

    def _extract_invoice_code(self, text: str) -> str:
        """提取发票代码（10-12位数字）"""
        # 优先查找明确标记的发票代码
        patterns = [
            r'发票代码[：:\s]*(\d{10,12})',
            r'代码[：:\s]*(\d{10,12})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return ""

    def _extract_invoice_number(self, text: str) -> str:
        """提取发票号码（8-20位数字）"""
        patterns = [
            r'发票号码[：:\s]*(\d{8,20})',
            r'号码[：:\s]*(\d{8,20})',
            r'No[.：:\s]*(\d{8,20})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return ""

    def _extract_invoice_date(self, text: str) -> str:
        """提取开票日期"""
        patterns = [
            r'(\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日]?)',
            r'开票日期[：:\s]*(\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日]?)',
            r'日期[：:\s]*(\d{4}[年/-]\d{1,2}[月/-]\d{1,2}[日]?)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return ""

    def _extract_buyer_name(self, text_lines: List[str], full_text: str) -> str:
        """提取购买方名称"""
        # 查找购买方信息区域
        buyer_section_start = -1
        buyer_section_end = -1

        for i, line in enumerate(text_lines):
            if '购买方' in line or '购方' in line:
                buyer_section_start = i
            if buyer_section_start >= 0 and ('销售方' in line or '销方' in line):
                buyer_section_end = i
                break

        if buyer_section_start >= 0:
            end = buyer_section_end if buyer_section_end > 0 else min(buyer_section_start + 5, len(text_lines))
            for i in range(buyer_section_start, end):
                name = self._extract_company_name(text_lines[i])
                if name:
                    return name
        return ""

    def _extract_seller_name(self, text_lines: List[str], full_text: str) -> str:
        """提取销售方名称"""
        # 查找销售方信息区域
        seller_section_start = -1

        for i, line in enumerate(text_lines):
            if '销售方' in line or '销方' in line:
                seller_section_start = i
                break

        if seller_section_start >= 0:
            for i in range(seller_section_start, min(seller_section_start + 5, len(text_lines))):
                name = self._extract_company_name(text_lines[i])
                if name:
                    return name
        return ""

    def _extract_company_name(self, text: str) -> str:
        """从文本中提取公司名称"""
        # 匹配公司名称模式
        patterns = [
            r'([^\d\s]{2,}(?:公司|企业|集团|厂|店|部|中心|研究院|事务所|商行|经营部))',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                # 过滤掉太短的或包含特定关键词的
                if len(name) >= 4 and not any(kw in name for kw in ['购买方', '销售方', '名称', '纳税人']):
                    return name
        return ""

    def _extract_buyer_tax_number(self, text_lines: List[str], full_text: str) -> str:
        """提取购买方纳税人识别号"""
        return self._extract_tax_number_in_section(text_lines, ['购买方', '购方'], ['销售方', '销方'])

    def _extract_seller_tax_number(self, text_lines: List[str], full_text: str) -> str:
        """提取销售方纳税人识别号"""
        return self._extract_tax_number_in_section(text_lines, ['销售方', '销方'], ['合计', '价税合计'])

    def _extract_tax_number_in_section(self, text_lines: List[str], start_markers: List[str], end_markers: List[str]) -> str:
        """在指定区域内提取纳税人识别号"""
        collecting = False
        for line in text_lines:
            # 检查是否进入目标区域
            if any(marker in line for marker in start_markers):
                collecting = True
                continue
            # 检查是否离开目标区域
            if collecting and any(marker in line for marker in end_markers):
                break
            if collecting:
                # 纳税人识别号通常是18位数字字母组合，或15-20位
                match = re.search(r'[A-Z0-9]{15,20}', line.replace(' ', ''))
                if match:
                    code = match.group(0)
                    # 验证是否包含字母和数字
                    if any(c.isalpha() for c in code) or len(code) >= 15:
                        return code
        return ""

    def _extract_buyer_address(self, text_lines: List[str], full_text: str) -> str:
        """提取购买方地址电话"""
        return self._extract_address_in_section(text_lines, ['购买方', '购方'], ['销售方', '销方'])

    def _extract_seller_address(self, text_lines: List[str], full_text: str) -> str:
        """提取销售方地址电话"""
        return self._extract_address_in_section(text_lines, ['销售方', '销方'], ['合计', '价税合计'])

    def _extract_address_in_section(self, text_lines: List[str], start_markers: List[str], end_markers: List[str]) -> str:
        """在指定区域内提取地址电话"""
        collecting = False
        for line in text_lines:
            if any(marker in line for marker in start_markers):
                collecting = True
                continue
            if collecting and any(marker in line for marker in end_markers):
                break
            if collecting:
                # 匹配地址+电话的模式
                # 地址通常包含省市区、路街等
                match = re.search(r'([^\d]{3,}.*?\d{3,4}-?\d{7,8})', line)
                if match:
                    return match.group(1).strip()
                # 也可能只有地址
                match = re.search(r'([^\d]{5,}(?:省|市|区|县|路|街|号))', line)
                if match:
                    return match.group(1).strip()
        return ""

    def _extract_buyer_bank(self, text_lines: List[str], full_text: str) -> str:
        """提取购买方开户行及账号"""
        return self._extract_bank_in_section(text_lines, ['购买方', '购方'], ['销售方', '销方'])

    def _extract_seller_bank(self, text_lines: List[str], full_text: str) -> str:
        """提取销售方开户行及账号"""
        return self._extract_bank_in_section(text_lines, ['销售方', '销方'], ['合计', '价税合计'])

    def _extract_bank_in_section(self, text_lines: List[str], start_markers: List[str], end_markers: List[str]) -> str:
        """在指定区域内提取开户行及账号"""
        collecting = False
        for line in text_lines:
            if any(marker in line for marker in start_markers):
                collecting = True
                continue
            if collecting and any(marker in line for marker in end_markers):
                break
            if collecting:
                # 匹配银行+账号的模式
                match = re.search(r'((?:中国|工商|农业|建设|交通|招商|光大|中信|民生|浦发|平安|华夏|兴业|广发|北京|上海|广州|深圳)?(?:银行|支行)[^\d]*\d{10,})', line)
                if match:
                    return match.group(1).strip()
        return ""

    def _extract_amounts(self, text_lines: List[str], full_text: str) -> tuple:
        """提取金额信息（合计金额、税额、价税合计）"""
        total_amount = 0.0
        total_tax = 0.0
        total_with_tax = 0.0

        # 查找金额相关的行
        for line in text_lines:
            line = line.replace(',', '').replace('，', '')

            # 合计金额（不含税）
            if '合计金额' in line or ('合计' in line and '税额' not in line and '价税' not in line):
                match = re.search(r'[元元]?\s*(\d+\.\d{2})', line)
                if match:
                    total_amount = float(match.group(1))

            # 合计税额
            if '合计税额' in line or '税额' in line:
                match = re.search(r'[元元]?\s*(\d+\.\d{2})', line)
                if match:
                    val = float(match.group(1))
                    if val != total_amount:  # 避免重复
                        total_tax = val

            # 价税合计
            if '价税合计' in line or '小写' in line:
                # 优先匹配元符号后面的金额
                match = re.search(r'[元元]\s*(\d+\.\d{2})', line)
                if match:
                    total_with_tax = float(match.group(1))
                else:
                    match = re.search(r'(\d+\.\d{2})', line)
                    if match:
                        total_with_tax = float(match.group(1))

        return total_amount, total_tax, total_with_tax

    def _extract_remarks(self, text_lines: List[str], full_text: str) -> str:
        """提取备注"""
        for i, line in enumerate(text_lines):
            if '备注' in line:
                # 如果备注在同一行
                if len(line) > 5 and not line.strip() == '备注':
                    remark = re.sub(r'^.*?备注[：:\s]*', '', line).strip()
                    if remark:
                        return remark
                # 如果备注在下一行
                elif i + 1 < len(text_lines):
                    next_line = text_lines[i + 1].strip()
                    if next_line and not any(kw in next_line for kw in ['开票人', '复核人', '收款人', '销售方']):
                        return next_line
        return ""

    def _extract_person(self, text_lines: List[str], role: str) -> str:
        """提取人员信息（复核、收款、开票）"""
        for line in text_lines:
            if role in line:
                # 提取人名（通常是2-4个汉字）
                match = re.search(rf'{role}[：:\s]*([^\d\s]{{2,4}})', line)
                if match:
                    return match.group(1).strip()
                # 也可能人名在关键词后面
                parts = line.split(role)
                if len(parts) > 1:
                    name = parts[-1].strip()[:4]
                    if name and all('\u4e00' <= c <= '\u9fff' for c in name):
                        return name
        return ""

    def _extract_items(self, text_lines: List[str]) -> List[InvoiceItem]:
        """提取商品明细"""
        items = []
        in_items_section = False

        for line in text_lines:
            line = line.strip()
            if not line:
                continue

            # 检测是否进入商品明细区域
            if any(kw in line for kw in ['货物或应税劳务', '项目名称', '规格型号', '单位', '数量', '单价']):
                in_items_section = True
                continue

            # 检测是否离开商品明细区域
            if any(kw in line for kw in ['合计', '价税合计', '销售方']) and in_items_section:
                in_items_section = False
                continue

            if in_items_section:
                item = self._parse_item_line(line)
                if item and item.name:
                    items.append(item)

        return items

    def _parse_item_line(self, line: str) -> Optional[InvoiceItem]:
        """解析单行商品明细"""
        item = InvoiceItem()

        # 尝试提取商品名称（通常是中文开头）
        # 过滤掉纯数字行和太短的内容
        name_match = re.search(r'^([\u4e00-\u9fa5][\u4e00-\u9fa5a-zA-Z0-9*]{1,}(?:[、，,]?[\u4e00-\u9fa5]+)*)', line)
        if name_match:
            name = name_match.group(1).strip()
            # 过滤掉非商品名称的内容
            if len(name) >= 2 and not any(kw in name for kw in ['税率', '税额', '规格', '型号', '单位']):
                item.name = name

        # 提取金额（通常是两位小数）
        amounts = re.findall(r'(\d+\.\d{2})', line)
        if len(amounts) >= 1:
            item.amount = float(amounts[0])
        if len(amounts) >= 2:
            item.tax_amount = float(amounts[-1])

        # 提取税率
        tax_rate_match = re.search(r'(\d+)%', line)
        if tax_rate_match:
            item.tax_rate = tax_rate_match.group(1) + '%'

        # 提取规格型号
        spec_match = re.search(r'([\u4e00-\u9fa5a-zA-Z0-9-]{2,})', line)
        if spec_match and not item.name:
            item.specification = spec_match.group(1)

        return item if item.name else None

    def _extract_image_as_pdf(self, image_path: Path) -> Optional[InvoiceInfo]:
        """将图片转为PDF后提取信息（备用方案）"""
        try:
            from PIL import Image
            import io

            print("尝试使用备用方案处理图片...")

            # 打开图片
            img = Image.open(image_path)

            # 转换为RGB模式（如果是RGBA或其他模式）
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # 创建PDF内存文件
            pdf_bytes = io.BytesIO()
            img.save(pdf_bytes, format='PDF', resolution=100.0)
            pdf_bytes.seek(0)

            # 保存临时PDF文件
            temp_pdf_path = Path(".temp/cache") / f"{image_path.stem}.pdf"
            temp_pdf_path.parent.mkdir(parents=True, exist_ok=True)
            with open(temp_pdf_path, 'wb') as f:
                f.write(pdf_bytes.getvalue())

            # 使用PDF提取方法
            invoice = self._extract_from_pdf(temp_pdf_path)

            # 更新源文件路径
            if invoice:
                invoice.source_file = str(image_path)

            # 清理临时文件
            temp_pdf_path.unlink(missing_ok=True)

            return invoice

        except Exception as e:
            print(f"[FAIL] 备用方案处理失败: {e}")
            return None


def extract_invoices_from_directory(directory: str) -> List[InvoiceInfo]:
    """
    从目录中提取所有发票信息

    Args:
        directory: 包含发票文件的目录路径

    Returns:
        InvoiceInfo对象列表
    """
    directory = Path(directory)

    if not directory.exists():
        print(f"[FAIL] 目录不存在: {directory}")
        return []

    # 支持的文件扩展名
    extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.pdf'}

    # 获取所有支持的文件
    files = [f for f in directory.iterdir() if f.suffix.lower() in extensions]

    if not files:
        print(f"[FAIL] 目录中没有找到发票文件: {directory}")
        return []

    print(f"发现 {len(files)} 个待处理文件")

    extractor = InvoiceExtractor()
    invoices = []

    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] 处理: {file_path.name}")
        invoice = extractor.extract_from_file(str(file_path))
        if invoice:
            invoices.append(invoice)
            print(f"[OK] 成功提取: {invoice.invoice_number or '未识别号码'}")
        else:
            print(f"[FAIL] 提取失败")

    return invoices
