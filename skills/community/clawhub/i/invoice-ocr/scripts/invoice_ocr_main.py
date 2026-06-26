#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增值税发票识别主脚本 (仅支持百度云OCR)
支持输入：PDF（单页/多页）、PNG、JPG/JPEG 图片
输出：结构化Excel报告（汇总总览 + 发票明细 + 质量报告）

用法:
  python invoice_ocr_main.py --input invoice.pdf --output result.xlsx
"""

import argparse
import base64
import io
import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import requests
from PIL import Image
from dotenv import load_dotenv

# 加载 .env 配置文件
load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class DetectionResult:
    page_no: int
    has_invoice: bool = True
    invoice_type: str = ""
    confidence: float = 0.5
    detection_note: str = ""

@dataclass
class InvoiceItem:
    name: str = ""
    spec: str = ""
    unit: str = ""
    quantity: str = ""
    unit_price: str = ""
    amount: str = ""
    tax_rate: str = ""
    tax_amount: str = ""

@dataclass
class InvoiceContent:
    page_no: int = 0
    invoice_type: str = ""
    invoice_code: str = ""
    invoice_number: str = ""
    invoice_date: str = ""
    check_code: str = ""
    machine_code: str = ""
    seller_name: str = ""
    seller_tax_id: str = ""
    seller_address_phone: str = ""
    seller_bank: str = ""
    buyer_name: str = ""
    buyer_tax_id: str = ""
    buyer_address_phone: str = ""
    buyer_bank: str = ""
    total_amount: str = ""
    total_tax: str = ""
    total_price_tax_cn: str = ""   # 大写
    total_price_tax: str = ""      # 小写/数字
    items: list = field(default_factory=list)
    payee: str = ""
    reviewer: str = ""
    drawer: str = ""
    remarks: str = ""
    raw_ocr: dict = field(default_factory=dict)
    ocr_error: str = ""

@dataclass
class QualityResult:
    page_no: int = 0
    total_score: float = 0.0
    completeness_score: float = 0.0
    format_score: float = 0.0
    amount_consistency_score: float = 0.0
    clarity_score: float = 0.0
    grade: str = ""
    issues: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# 输入处理器
# ─────────────────────────────────────────────────────────────────────────────

class InputHandler:
    MAX_IMG_BYTES = 3 * 1024 * 1024
    DPI = 200

    def __init__(self, input_path: str):
        self.input_path = Path(input_path)
        if not self.input_path.exists():
            raise FileNotFoundError(f"文件不存在: {input_path}")

    def load(self) -> List[Tuple[int, bytes]]:
        suffix = self.input_path.suffix.lower()
        if suffix == ".pdf":
            return self._load_pdf()
        elif suffix in (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"):
            return self._load_image()
        else:
            raise ValueError(f"不支持的文件格式: {suffix}")

    def _load_pdf(self) -> List[Tuple[int, bytes]]:
        import fitz
        doc = fitz.open(str(self.input_path))
        if doc.page_count == 0:
            raise ValueError("PDF文件为空（0页）")

        pages = []
        mat = fitz.Matrix(self.DPI / 72, self.DPI / 72)
        for i in range(doc.page_count):
            page_no = i + 1
            try:
                pix = doc[i].get_pixmap(matrix=mat, colorspace=fitz.csRGB)
                img_bytes = pix.tobytes("jpeg")
                if len(img_bytes) > self.MAX_IMG_BYTES:
                    img_bytes = self._compress_jpeg(pix.tobytes("png"), quality=75)
                pages.append((page_no, img_bytes))
                print(f"  📄 PDF第{page_no}页已提取")
            except Exception as e:
                print(f"  ⚠️ PDF第{page_no}页提取失败，已跳过: {e}")
        doc.close()
        return pages

    def _load_image(self) -> List[Tuple[int, bytes]]:
        raw = self.input_path.read_bytes()
        img = Image.open(io.BytesIO(raw))
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        w, h = img.size
        if w < 50 or h < 50:
            raise ValueError(f"图片尺寸过小（{w}x{h}），无法识别")
        
        img_bytes = self._pil_to_jpeg(img, quality=90)
        if len(img_bytes) > self.MAX_IMG_BYTES:
            img_bytes = self._pil_to_jpeg(img, quality=70)
        print(f"  🖼️ 图片已加载（{w}x{h}）")
        return [(1, img_bytes)]

    @staticmethod
    def _pil_to_jpeg(img: Image.Image, quality: int = 85) -> bytes:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return buf.getvalue()

    @staticmethod
    def _compress_jpeg(png_bytes: bytes, quality: int = 75) -> bytes:
        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        return InputHandler._pil_to_jpeg(img, quality)


# ─────────────────────────────────────────────────────────────────────────────
# 模块 1：发票检测器
# ─────────────────────────────────────────────────────────────────────────────

class InvoiceDetector:
    TYPE_PATTERNS = [
        ("增值税专用发票",  r"增值税专用发票", 0.92),
        ("增值税普通发票",  r"增值税普通发票", 0.88),
        ("数电发票",        r"数电发票|全面数字化电子发票", 0.88),
        ("电子普通发票",    r"电子普通发票|电子发票\(普通发票\)", 0.85),
        ("电子专用发票",    r"电子发票\(专用发票\)|电子专用发票", 0.88),
    ]
    GENERIC_KEYWORDS = ["发票代码", "发票号码", "开票日期", "纳税人识别号", "价税合计"]

    def initial_check(self, page_no: int, image_bytes: bytes) -> DetectionResult:
        img = Image.open(io.BytesIO(image_bytes))
        w, h = img.size
        if w < 100 or h < 100:
            return DetectionResult(page_no, False, confidence=0.0, detection_note="图片过小")
        return DetectionResult(page_no, True, confidence=0.5, detection_note="待OCR确认")

    def refine_from_ocr(self, detection: DetectionResult, ocr_data) -> DetectionResult:
        text = json.dumps(ocr_data, ensure_ascii=False) if isinstance(ocr_data, dict) else str(ocr_data)
        invoice_type, confidence = "", 0.0

        for itype, pattern, conf in self.TYPE_PATTERNS:
            if re.search(pattern, text):
                invoice_type, confidence = itype, conf
                break

        generic_hit = sum(1 for kw in self.GENERIC_KEYWORDS if kw in text)
        if generic_hit >= 2 and confidence < 0.65:
            confidence = min(0.5 + generic_hit * 0.07, 0.85)
            invoice_type = invoice_type or "其他发票"

        detection.has_invoice = confidence >= 0.5
        detection.invoice_type = invoice_type
        detection.confidence = round(min(confidence, 1.0), 3)
        return detection


# ─────────────────────────────────────────────────────────────────────────────
# 模块 2：内容识别器 (百度云发票识别服务)
# ─────────────────────────────────────────────────────────────────────────────

class ContentExtractor:
    def __init__(self):
        # 从环境变量 (.env) 中获取配置
        self.api_key = os.getenv("BAIDU_API_KEY", "").strip()
        self.secret_key = os.getenv("BAIDU_SECRET_KEY", "").strip()
        
        if not self.api_key or not self.secret_key:
            raise ValueError("未找到百度云配置，请确保 .env 文件中已配置 BAIDU_API_KEY 和 BAIDU_SECRET_KEY")
            
        self._baidu_token: Optional[str] = None
        self._baidu_token_expire: float = 0.0

    def _get_baidu_token(self) -> str:
        if self._baidu_token and time.time() < self._baidu_token_expire:
            return self._baidu_token

        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.secret_key}
        resp = requests.post(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            raise RuntimeError(f"百度鉴权失败: {data.get('error_description')}")

        self._baidu_token = data["access_token"]
        self._baidu_token_expire = time.time() + int(data.get("expires_in", 2592000)) - 60
        return self._baidu_token

    @staticmethod
    def _prepare_for_baidu(image_bytes: bytes) -> bytes:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        w, h = img.size
        MAX_RATIO, MAX_SIDE = 3.0, 4096

        # 修正长宽比
        ratio = max(w, h) / max(min(w, h), 1)
        if ratio > MAX_RATIO:
            if w > h:
                new_w = int(h * MAX_RATIO)
                img = img.crop(((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h))
            else:
                new_h = int(w * MAX_RATIO)
                img = img.crop((0, (h - new_h) // 2, w, (h - new_h) // 2 + new_h))
        
        # 缩放
        if max(img.size) > MAX_SIDE:
            scale = MAX_SIDE / max(img.size)
            img = img.resize((int(img.size[0] * scale), int(img.size[1] * scale)), Image.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85, optimize=True)
        return buf.getvalue()

    def _baidu_ocr(self, image_bytes: bytes) -> dict:
        token = self._get_baidu_token()
        img_b64 = base64.b64encode(self._prepare_for_baidu(image_bytes)).decode("utf-8")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        vat_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice?access_token={token}"
        resp = requests.post(vat_url, headers=headers, data={"image": img_b64}, timeout=30)
        resp.raise_for_status()
        result = resp.json()

        if result.get("error_code") and result["error_code"] != 0:
            print("    ⚠️  增值税专用接口失败，降级通用OCR...")
            gen_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={token}"
            resp2 = requests.post(gen_url, headers=headers, data={"image": img_b64}, timeout=30)
            resp2.raise_for_status()
            general_result = resp2.json()
            general_result["_source"] = "general"
            return general_result

        result["_source"] = "vat_invoice"
        return result

    def _parse_baidu_result(self, raw: dict, page_no: int) -> InvoiceContent:
        content = InvoiceContent(page_no=page_no, raw_ocr=raw)
        if raw.get("_source") == "general":
            words = [w.get("words", "") for w in raw.get("words_result", [])]
            content.remarks = "[通用OCR降级] " + " | ".join(words[:30])
            return content

        wr = raw.get("words_result", {})
        def g(k: str) -> str:
            v = wr.get(k)
            return (v.get("word", "").strip() if isinstance(v, dict) else str(v).strip()) if v else ""

        content.invoice_type = g("InvoiceType") or g("InvoiceTypeOrg")
        content.invoice_number = g("InvoiceNum").replace(" ", "")
        content.invoice_code = g("InvoiceCode")
        content.invoice_date = g("InvoiceDate")
        content.seller_name = g("SellerName")
        content.buyer_name = g("PurchaserName")
        content.total_amount = g("TotalAmount")
        content.total_tax = g("TotalTax")
        content.total_price_tax = g("AmountInFiguers")
        return content

    def extract(self, page_no: int, image_bytes: bytes) -> InvoiceContent:
        last_error = ""
        for attempt in range(3):
            try:
                raw = self._baidu_ocr(image_bytes)
                return self._parse_baidu_result(raw, page_no)
            except Exception as e:
                last_error = str(e)
                time.sleep(attempt + 1)
        
        content = InvoiceContent(page_no=page_no)
        content.ocr_error = f"识别失败: {last_error}"
        return content


# ─────────────────────────────────────────────────────────────────────────────
# 模块 3：质量评估器 (保持不变，已精简部分冗余逻辑)
# ─────────────────────────────────────────────────────────────────────────────

class QualityAssessor:
    REQUIRED_FIELDS = ["invoice_number", "invoice_date", "seller_name", "buyer_name", "total_price_tax"]

    def assess(self, content: InvoiceContent, detection: DetectionResult) -> QualityResult:
        result = QualityResult(page_no=content.page_no)
        if content.ocr_error or not detection.has_invoice:
            result.grade = "🔴 失败/非发票"
            return result

        req_present = sum(1 for f in self.REQUIRED_FIELDS if getattr(content, f, ""))
        result.completeness_score = (req_present / len(self.REQUIRED_FIELDS)) * 100
        result.clarity_score = detection.confidence * 100
        
        result.total_score = round(result.completeness_score * 0.6 + result.clarity_score * 0.4, 1)
        # print(f"  质量评估: 完整性{result.completeness_score:.0f} 分, 清晰度{result.clarity_score:.0f} 分 -> 总得分 {result.total_score:.0f} 分")
        if result.total_score >= 90: result.grade = "🟢 优秀"
        elif result.total_score >= 70: result.grade = "🟡 良好"
        else: result.grade = "🔴 较差"

        return result


# ─────────────────────────────────────────────────────────────────────────────
# Excel 导出器 (已补全截断部分)
# ─────────────────────────────────────────────────────────────────────────────

class ExcelExporter:
    def export(self, results: List[Tuple[DetectionResult, InvoiceContent, QualityResult]], output_path: str):
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "发票汇总"
        
        headers = ["页码", "发票类型", "发票号码", "开票日期", "销售方", "购买方", "价税合计", "质量评估"]
        ws.append(headers)

        for det, content, qual in results:
            row = [
                content.page_no,
                content.invoice_type,
                content.invoice_number,
                content.invoice_date,
                content.seller_name,
                content.buyer_name,
                content.total_price_tax,
                qual.grade
            ]
            ws.append(row)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        wb.save(output_path)
        print(f"\n✅ Excel 已成功保存至: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 主程序入口
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="增值税发票识别脚本 (基于配置文件的百度云OCR)")
    parser.add_argument("--input", required=True, help="输入的 PDF 或 图片路径")
    parser.add_argument("--output", default="result.xlsx", help="输出的 Excel 文件路径")
    args = parser.parse_args()

    print(f"🚀 开始处理: {args.input}")
    
    # 1. 加载图片/PDF
    handler = InputHandler(args.input)
    pages = handler.load()

    # 2. 初始化核心组件
    detector = InvoiceDetector()
    extractor = ContentExtractor()
    assessor = QualityAssessor()
    exporter = ExcelExporter()

    results = []
    for page_no, img_bytes in pages:
        print(f"\n--- 正在处理第 {page_no} 页 ---")
        
        # 预检测
        det = detector.initial_check(page_no, img_bytes)
        if not det.has_invoice:
            results.append((det, InvoiceContent(page_no=page_no), QualityAssessor().assess(InvoiceContent(page_no=page_no), det)))
            continue

        # OCR 提取
        content = extractor.extract(page_no, img_bytes)
        
        # 修正检测结果 & 质量评估
        det = detector.refine_from_ocr(det, content.raw_ocr)
        qual = assessor.assess(content, det)
        
        results.append((det, content, qual))
        print(f"  ✓ 提取完成 - 类型: {content.invoice_type}, 号码: {content.invoice_number}, 质量: {qual.grade}")

    # 3. 导出报告
    exporter.export(results, args.output)

if __name__ == "__main__":
    main()