#!/usr/bin/env python3
"""
发票 OCR 测试脚本 - 对单张发票图片/PDF 运行 OCR 并输出识别结果

用法：
  python test_ocr.py <invoice_image_or_pdf>
  python test_ocr.py invoice.jpg --json        # JSON 格式输出
  python test_ocr.py invoice.pdf --verbose     # 显示详细 OCR 文本
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 添加 bot 目录到 Python 路径（优先使用环境变量 BOT_DIR）
_DEFAULT_BOT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "invoice-approval-bot"
BOT_DIR = Path(os.environ.get("BOT_DIR", str(_DEFAULT_BOT_DIR)))
sys.path.insert(0, str(BOT_DIR))

from invoice_ocr import ocr_invoice
from invoice_qr_verify import scan_and_verify
from pdf_preprocessor import preprocess_file
from invoice_handler import format_invoice_summary


def test_single_image(image_path: str, verbose: bool = False) -> dict:
    """测试单张图片的 OCR 识别

    Args:
        image_path: 图片文件路径
        verbose: 是否显示原始 OCR 文本

    Returns:
        识别结果 dict
    """
    with open(image_path, "rb") as f:
        file_bytes = f.read()

    filename = os.path.basename(image_path)

    # PDF 预处理
    images = preprocess_file(file_bytes, filename)
    print(f"📂 文件: {filename}")
    print(f"📄 页数: {len(images)}")

    results = []
    for i, (img_bytes, page_desc) in enumerate(images):
        page_label = page_desc or f"图片 {i+1}"
        print(f"\n{'─' * 40}")
        print(f"🔍 处理: {page_label} ({len(img_bytes) // 1024} KB)")

        # OCR 识别
        try:
            invoice = ocr_invoice(img_bytes)
        except Exception as e:
            print(f"❌ OCR 异常: {e}")
            continue

        # 二维码验真
        try:
            qr_result = scan_and_verify(img_bytes, invoice)
            invoice["qr_verified"] = qr_result["is_verified"]
            invoice["qr_raw"] = qr_result.get("qr_raw", "")
            invoice["qr_msg"] = "✅ 验真通过" if qr_result["is_verified"] else (
                qr_result.get("error", "⚠️ 不一致")
            )
        except Exception as e:
            invoice["qr_verified"] = False
            invoice["qr_msg"] = f"验真异常: {e}"

        results.append(invoice)

        # 输出识别结果
        summary = format_invoice_summary(invoice)
        print(summary)

        if verbose and invoice.get("_raw_texts"):
            print("\n📝 原始 OCR 文本:")
            for text in invoice["_raw_texts"][:30]:
                print(f"   {text}")

    return results


def main():
    parser = argparse.ArgumentParser(description="发票 OCR 测试工具")
    parser.add_argument("file", help="发票图片或 PDF 文件路径")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细 OCR 文本")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    if args.json:
        # JSON 输出模式
        with open(args.file, "rb") as f:
            file_bytes = f.read()

        images = preprocess_file(file_bytes, os.path.basename(args.file))
        all_results = []
        for img_bytes, _ in images:
            try:
                invoice = ocr_invoice(img_bytes)
                qr_result = scan_and_verify(img_bytes, invoice)
                invoice["qr_verified"] = qr_result["is_verified"]
                # 清理不可序列化的字段
                clean_invoice = {
                    k: v for k, v in invoice.items()
                    if not k.startswith("_")
                }
                all_results.append(clean_invoice)
            except Exception as e:
                all_results.append({"error": str(e)})

        print(json.dumps(all_results, ensure_ascii=False, indent=2, default=str))
    else:
        # 人类可读输出
        print("╔══════════════════════════════════╗")
        print("║     发票 OCR 测试工具           ║")
        print("╚══════════════════════════════════╝")
        test_single_image(args.file, verbose=args.verbose)


if __name__ == "__main__":
    main()
