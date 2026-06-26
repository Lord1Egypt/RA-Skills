#!/usr/bin/env python3
"""
商家资料OCR识别与信息提取工具
从营业执照等资料中提取企业信息，用于GEO内容生成

使用方法：
    python extract_business_info.py <图片路径>
    python extract_business_info.py --batch <文件夹路径>
"""

import os
import sys
import json
import argparse
from pathlib import Path

# 需要安装: pip install paddleocr pillow
try:
    from paddleocr import PaddleOCR
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ PaddleOCR 未安装，将使用基础解析模式")

class BusinessInfoExtractor:
    """企业信息提取器"""
    
    def __init__(self):
        self.ocr = None
        if OCR_AVAILABLE:
            try:
                self.ocr = PaddleOCR(use_angle_cls=True, lang='chinese', use_gpu=False)
            except Exception as e:
                print(f"⚠️ OCR初始化失败: {e}")
                self.ocr = None
    
    def extract_from_image(self, image_path: str) -> dict:
        """
        从图片中提取企业信息
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            dict: 提取的企业信息
        """
        result = {
            "enterprise_name": None,
            "credit_code": None,
            "legal_person": None,
            "registered_capital": None,
            "establishment_date": None,
            "business_scope": None,
            "address": None,
            "extraction_confidence": 0.0,
            "raw_text": []
        }
        
        if not os.path.exists(image_path):
            print(f"❌ 文件不存在: {image_path}")
            return result
        
        # OCR识别
        if self.ocr:
            try:
                ocr_result = self.ocr.ocr(image_path, cls=True)
                if ocr_result and ocr_result[0]:
                    text_lines = []
                    for line in ocr_result[0]:
                        if line and len(line) >= 2:
                            text_lines.append(line[1][0])
                    
                    result["raw_text"] = text_lines
                    result.update(self._parse_business_license(text_lines))
            except Exception as e:
                print(f"⚠️ OCR识别失败: {e}")
                result["raw_text"] = ["[OCR识别失败]"]
        else:
            print("📝 请手动输入企业信息")
        
        return result
    
    def _parse_business_license(self, text_lines: list) -> dict:
        """
        解析营业执照文本
        
        Args:
            text_lines: OCR识别出的文本行
            
        Returns:
            dict: 解析后的企业信息
        """
        info = {}
        
        # 企业名称关键词
        name_keywords = ["企业名称", "名称", "公司名称", "名称(字号)"]
        for i, line in enumerate(text_lines):
            for kw in name_keywords:
                if kw in line:
                    # 尝试提取冒号/空格后的内容
                    parts = line.split(kw)
                    if len(parts) > 1:
                        name = parts[-1].strip().lstrip(":：").strip()
                        # 如果当前行没有完整名称，尝试连接下一行
                        if i + 1 < len(text_lines) and not any(k in text_lines[i+1] for k in name_keywords):
                            name += text_lines[i+1]
                        info["enterprise_name"] = name
                        break
        
        # 统一社会信用代码
        credit_keywords = ["统一社会信用代码", "信用代码", "注册号", "证书编号"]
        for line in text_lines:
            for kw in credit_keywords:
                if kw in line:
                    parts = line.split(kw)
                    if len(parts) > 1:
                        code = parts[-1].strip().lstrip(":：").strip()
                        # 信用代码是18位
                        if len(code) >= 18:
                            info["credit_code"] = code[:18]
                        break
        
        # 法定代表人
        legal_keywords = ["法定代表人", "法人代表", "法人", "负责人"]
        for line in text_lines:
            for kw in legal_keywords:
                if kw in line:
                    parts = line.split(kw)
                    if len(parts) > 1:
                        info["legal_person"] = parts[-1].strip().lstrip(":：").strip()
                        break
        
        # 注册资本
        capital_keywords = ["注册资本", "注册资金", "资金"]
        for line in text_lines:
            for kw in capital_keywords:
                if kw in line:
                    parts = line.split(kw)
                    if len(parts) > 1:
                        info["registered_capital"] = parts[-1].strip().lstrip(":：").strip()
                        break
        
        # 成立日期
        date_keywords = ["成立日期", "注册日期", "成立时间", "注册时间", "发照日期"]
        for line in text_lines:
            for kw in date_keywords:
                if kw in line:
                    parts = line.split(kw)
                    if len(parts) > 1:
                        info["establishment_date"] = parts[-1].strip().lstrip(":：").strip()
                        break
        
        # 经营范围
        scope_keywords = ["经营范围", "业务范围", "主营", "许可经营项目", "一般经营项目"]
        scope_text = []
        scope_started = False
        for line in text_lines:
            for kw in scope_keywords:
                if kw in line:
                    scope_started = True
                    parts = line.split(kw)
                    if len(parts) > 1:
                        scope_text.append(parts[-1].strip().lstrip(":："))
                    break
            elif scope_started:
                # 继续收集范围内容直到下一个关键词
                if any(k in line for k in ["住所", "地址", "营业期限", "企业类型", "组成形式"]):
                    break
                scope_text.append(line.strip())
        
        if scope_text:
            info["business_scope"] = " ".join(scope_text)
        
        # 地址
        address_keywords = ["住所", "地址", "经营场所", "场所"]
        for i, line in enumerate(text_lines):
            for kw in address_keywords:
                if kw in line:
                    parts = line.split(kw)
                    if len(parts) > 1:
                        address = parts[-1].strip().lstrip(":：")
                        # 尝试连接多行地址
                        if i + 1 < len(text_lines):
                            next_line = text_lines[i+1]
                            if not any(k in next_line for k in ["经营范围", "注册资本", "成立日期"]):
                                address += next_line
                        info["address"] = address
                        break
        
        return info
    
    def interactive_fill(self) -> dict:
        """
        交互式补充信息（当OCR不完整时）
        
        Returns:
            dict: 完整的企业信息
        """
        print("\n📝 请补充企业信息（直接回车跳过）：\n")
        
        info = {}
        
        fields = [
            ("enterprise_name", "企业名称"),
            ("credit_code", "统一社会信用代码"),
            ("legal_person", "法定代表人"),
            ("registered_capital", "注册资本"),
            ("establishment_date", "成立日期"),
            ("address", "企业地址"),
            ("business_scope", "经营范围（简述）")
        ]
        
        for key, label in fields:
            value = input(f"  {label}: ").strip()
            if value:
                info[key] = value
        
        return info
    
    def save_to_file(self, info: dict, output_path: str):
        """保存信息到JSON文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存到: {output_path}")
    
    def generate_profile(self, info: dict) -> str:
        """
        生成企业简介文本
        
        Args:
            info: 企业信息字典
            
        Returns:
            str: 企业简介
        """
        parts = []
        
        if info.get("enterprise_name"):
            parts.append(f"{info['enterprise_name']}")
        
        if info.get("establishment_date"):
            parts.append(f"成立于{info['establishment_date']}")
        
        if info.get("address"):
            parts.append(f"位于{info['address']}")
        
        if info.get("legal_person"):
            parts.append(f"法定代表人为{info['legal_person']}")
        
        if info.get("business_scope"):
            parts.append(f"主营业务：{info['business_scope'][:100]}...")
        
        return "，".join(parts) if parts else "信息不完整"


def main():
    parser = argparse.ArgumentParser(
        description="商家资料OCR识别与信息提取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python extract_business_info.py 营业执照.jpg
  python extract_business_info.py --batch ./images/
  python extract_business_info.py 营业执照.jpg --output business_info.json
        """
    )
    
    parser.add_argument("input_path", nargs="?", help="图片文件路径或文件夹路径")
    parser.add_argument("--batch", action="store_true", help="批量处理文件夹")
    parser.add_argument("--output", "-o", help="输出JSON文件路径")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式补充信息")
    
    args = parser.parse_args()
    
    extractor = BusinessInfoExtractor()
    
    if args.batch and args.input_path:
        # 批量处理
        folder = Path(args.input_path)
        if not folder.is_dir():
            print(f"❌ 不是有效文件夹: {args.input_path}")
            sys.exit(1)
        
        results = []
        for img_path in folder.glob("*.jpg"):
            print(f"\n📄 处理: {img_path.name}")
            info = extractor.extract_from_image(str(img_path))
            if args.interactive:
                manual_info = extractor.interactive_fill()
                info.update(manual_info)
            results.append({"file": img_path.name, "info": info})
        
        for img_path in folder.glob("*.png"):
            print(f"\n📄 处理: {img_path.name}")
            info = extractor.extract_from_image(str(img_path))
            if args.interactive:
                manual_info = extractor.interactive_fill()
                info.update(manual_info)
            results.append({"file": img_path.name, "info": info})
        
        # 保存结果
        output_file = args.output or folder / "business_info_batch.json"
        extractor.save_to_file(results, str(output_file))
        
    elif args.input_path:
        # 单文件处理
        info = extractor.extract_from_image(args.input_path)
        
        print("\n" + "="*50)
        print("📋 提取结果")
        print("="*50)
        
        for key, value in info.items():
            if key != "raw_text" and value:
                print(f"  {key}: {value}")
        
        if args.interactive:
            manual_info = extractor.interactive_fill()
            info.update(manual_info)
        
        # 保存结果
        output_file = args.output
        if not output_file:
            input_file = Path(args.input_path)
            output_file = str(input_file.parent / f"{input_file.stem}_info.json")
        
        extractor.save_to_file(info, output_file)
        
        # 生成简介
        print("\n" + "="*50)
        print("📝 企业简介（可用于GEO内容）")
        print("="*50)
        print(extractor.generate_profile(info))
        
    else:
        # 纯交互模式
        info = extractor.interactive_fill()
        
        output_file = args.output or "business_info.json"
        extractor.save_to_file(info, output_file)
        
        print("\n" + "="*50)
        print("📝 企业简介")
        print("="*50)
        print(extractor.generate_profile(info))


if __name__ == "__main__":
    main()
