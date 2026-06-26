#!/usr/bin/env python3
"""
PDF Contract Redactor - Main Script
Uses Alibaba Cloud OCR to extract text and redact field values
"""

import sys
import io
import json
import base64
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

FIELDS_TO_REDACT = [
    "法务部归档编号", "归档时间", "申请人工号", "申请人姓名", "申请人部门",
    "申请人部门负责人", "所涉项目名称（如有）", "所涉项目编号（如有）",
    "对方编号（如有）", "合同编号", "合同名称", "合同甲方名称", "合同乙方名称",
    "合同相对方", "相对方所属行业", "相对方是否为世界500强", "相对方是央企/国企",
    "相对方是否为涉密单位", "业务类别", "合同类别", "合同类型", "合同状态",
    "扫描件状态", "对方是否签章", "我方是否签章", "销售、采购标的（非一起译填）",
    "语种", "单价", "合同金额（元）", "币种", "支付/收款方式", "付款/收款条件",
    "合同结算周期", "是否使用公司模板", "用章主体", "印章类型", "签订时间",
    "合同开始时间", "合同到期时间", "收支类型", "我方联系人姓名", "我方联系人电话",
    "对方联系人姓名", "对方联系人电话", "对方邮寄地址", "归档状态", "开票名称",
    "开票账号", "开票银行", "收款名称", "收款账号", "收款银行", "验收时间",
    "验收标准", "合同是否自动续期", "合同续期时间", "合同特殊约定",
    "协议内是否有结算单", "结算单（如有）内容是否填写",
]


@dataclass
class TextBlock:
    text: str
    page: int
    bbox: Tuple[float, float, float, float]
    confidence: float


@dataclass
class FieldValue:
    field_name: str
    value: str
    page: int
    field_bbox: Tuple[float, float, float, float]
    value_bbox: Tuple[float, float, float, float]


class AliyunOCRClient:
    def __init__(self, access_key_id: str, access_key_secret: str):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
    
    def recognize(self, image_bytes: bytes, page_num: int) -> List[TextBlock]:
        import requests
        
        url = "https://ocr.aliyuncs.com"
        params = {
            "Action": "RecognizeAdvanced",
            "Version": "2021-07-07",
            "Format": "JSON",
            "AccessKeyId": self.access_key_id,
            "SignatureMethod": "HMAC-SHA1",
            "Timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "SignatureVersion": "1.0",
            "SignatureNonce": str(int(time.time() * 1000)),
        }
        
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        body = {"ImageURL": f"data:image/png;base64,{image_base64}", "OutputFigure": False}
        
        try:
            response = requests.post(url, params=params, json=body, timeout=60)
            result = response.json()
            
            if "Code" in result and result["Code"] != "Success":
                print(f"API Error: {result.get('Message', 'Unknown')}")
                return []
            
            blocks = []
            data = result.get("Data", {})
            for item in data.get("Contents", []):
                text = item.get("Content", "").strip()
                if not text:
                    continue
                points = item.get("Points", [])
                if points and len(points) >= 4:
                    xs = [p.get("X", 0) for p in points]
                    ys = [p.get("Y", 0) for p in points]
                    bbox = (min(xs), min(ys), max(xs), max(ys))
                else:
                    bbox = (0, 0, 0, 0)
                confidence = item.get("Confidence", 0.9)
                blocks.append(TextBlock(text=text, page=page_num, bbox=bbox, confidence=confidence))
            return blocks
        except Exception as e:
            print(f"API call failed: {e}")
            return []


class ContractRedactor:
    def __init__(self, pdf_path: str, access_key_id: str, access_key_secret: str):
        self.pdf_path = Path(pdf_path)
        self.ocr = AliyunOCRClient(access_key_id, access_key_secret)
    
    def pdf_to_images(self, dpi: int = 200) -> List[bytes]:
        import fitz
        from PIL import Image
        
        doc = fitz.open(self.pdf_path)
        images = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            import io as io_module
            img_bytes = io_module.BytesIO()
            img.save(img_bytes, format='PNG', quality=95)
            images.append(img_bytes.getvalue())
        doc.close()
        return images
    
    def ocr_all_pages(self) -> List[TextBlock]:
        images = self.pdf_to_images()
        all_blocks = []
        for page_num, img_bytes in enumerate(images):
            print(f"OCR page {page_num + 1}/{len(images)}...")
            blocks = self.ocr.recognize(img_bytes, page_num)
            all_blocks.extend(blocks)
        return all_blocks
    
    def find_field_values(self, blocks: List[TextBlock]) -> List[FieldValue]:
        field_values = []
        page_blocks = {}
        for block in blocks:
            if block.page not in page_blocks:
                page_blocks[block.page] = []
            page_blocks[block.page].append(block)
        
        for page_num, blocks_in_page in page_blocks.items():
            for field in FIELDS_TO_REDACT:
                field_blocks = self._find_field_blocks(field, blocks_in_page)
                for field_block in field_blocks:
                    value_block = self._find_value_near_field(field, field_block, blocks_in_page)
                    if value_block and value_block.text != field:
                        field_values.append(FieldValue(
                            field_name=field, value=value_block.text, page=page_num,
                            field_bbox=field_block.bbox, value_bbox=value_block.bbox
                        ))
        return field_values
    
    def _find_field_blocks(self, field: str, blocks: List[TextBlock]) -> List[TextBlock]:
        matches = []
        field_clean = field.replace('（如有）', '').strip()
        for block in blocks:
            text = block.text
            if field in text or field_clean in text:
                matches.append(block)
            elif len(field_clean) >= 4 and field_clean[:4] in text:
                matches.append(block)
        return matches
    
    def _find_value_near_field(self, field: str, field_block: TextBlock, all_blocks: List[TextBlock]) -> Optional[TextBlock]:
        fx0, fy0, fx1, fy1 = field_block.bbox
        field_height = fy1 - fy0
        field_width = fx1 - fx0
        candidates = []
        
        for block in all_blocks:
            if block.bbox == field_block.bbox:
                continue
            vx0, vy0, vx1, vy1 = block.bbox
            is_right = vx0 > fx1 - 10 and abs(vy0 - fy0) < field_height * 2
            is_below = vy0 > fy1 - 10 and vx0 >= fx0 - field_width * 0.3 and vx0 < fx1 + field_width * 2
            
            if is_right or is_below:
                distance = vx0 - fx1 if is_right else vy0 - fy1
                if distance < field_width * 3:
                    candidates.append((block, distance))
        
        if candidates:
            candidates.sort(key=lambda x: x[1])
            return candidates[0][0]
        return None
    
    def create_redacted_pdf(self, output_path: str, field_values: List[FieldValue]) -> None:
        import fitz
        doc = fitz.open(self.pdf_path)
        dpi, pdf_dpi = 200, 72
        scale = pdf_dpi / dpi
        
        values_by_page = {}
        for fv in field_values:
            if fv.page not in values_by_page:
                values_by_page[fv.page] = []
            values_by_page[fv.page].append(fv)
        
        for page_num, page_values in values_by_page.items():
            if page_num >= len(doc):
                continue
            page = doc[page_num]
            for fv in page_values:
                x0, y0, x1, y1 = fv.value_bbox
                pdf_x0, pdf_y0 = x0 * scale, y0 * scale
                pdf_x1, pdf_y1 = x1 * scale, y1 * scale
                padding = 3
                rect = fitz.Rect(pdf_x0 - padding, pdf_y0 - padding, pdf_x1 + padding, pdf_y1 + padding)
                page.draw_rect(rect, color=(0, 0, 0), fill=(0, 0, 0))
        
        doc.save(output_path)
        doc.close()
    
    def export_results(self, field_values: List[FieldValue], output_path: str) -> None:
        data = [{"field_name": fv.field_name, "value": fv.value, "page": fv.page + 1,
                 "field_bbox": fv.field_bbox, "value_bbox": fv.value_bbox} for fv in field_values]
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 4:
        print("Usage: python redact_contract.py <input.pdf> <access_key_id> <access_key_secret> [output.pdf]")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    access_key_id = sys.argv[2]
    access_key_secret = sys.argv[3]
    output_pdf = sys.argv[4] if len(sys.argv) > 4 else input_pdf.replace('.pdf', '_redacted.pdf')
    
    print(f"Processing: {input_pdf}")
    redactor = ContractRedactor(input_pdf, access_key_id, access_key_secret)
    
    blocks = redactor.ocr_all_pages()
    print(f"Found {len(blocks)} text blocks")
    
    field_values = redactor.find_field_values(blocks)
    print(f"Matched {len(field_values)} field-value pairs")
    
    for fv in field_values[:10]:
        print(f"  [{fv.field_name}] = {fv.value[:30]}")
    
    json_path = output_pdf.replace('.pdf', '_fields.json')
    redactor.export_results(field_values, json_path)
    redactor.create_redacted_pdf(output_pdf, field_values)
    
    print(f"Done! Output: {output_pdf}")


if __name__ == "__main__":
    main()
