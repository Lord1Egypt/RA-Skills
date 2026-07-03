#!/usr/bin/env python3
"""
保险条款图片OCR文字提取
支持 PaddleOCR（中文首选）和 Tesseract（备选）
用法: python ocr_extract.py <image_path> [--output <output_txt>] [--engine paddle|tesseract]
"""

import argparse
import os
import sys

ENGINE = None  # 运行时选择


def extract_with_paddleocr(image_path):
    """使用 PaddleOCR 提取文字"""
    try:
        from paddleocr import PaddleOCR
        import numpy as np
        from PIL import Image

        # 如果 PaddleOCR 已初始化，复用实例
        global ENGINE
        if ENGINE is None:
            ENGINE = PaddleOCR(lang='ch', use_gpu=False, show_log=False)

        img = np.array(Image.open(image_path).convert('RGB'))
        result = ENGINE.ocr(img, cls=False)

        if not result or not result[0]:
            return "[提示] PaddleOCR 未能从图片中识别出文字，请确认图片清晰度或尝试其他方式输入。"

        lines = []
        for line in result[0]:
            text = line[1][0]
            if text.strip():
                lines.append(text.strip())

        return "\n".join(lines)
    except ImportError:
        print("[提示] paddleocr 未安装。正在尝试安装...", file=sys.stderr)
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install",
             "paddleocr>=2.7", "paddlepaddle>=2.6",
             "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/",
             "--trusted-host", "pypi.tuna.tsinghua.edu.cn"],
            stdout=sys.stderr, stderr=sys.stderr)
        return extract_with_paddleocr(image_path)
    except Exception as e:
        print(f"[警告] PaddleOCR 处理失败: {e}，尝试 Tesseract 备选...", file=sys.stderr)
        return extract_with_tesseract(image_path)


def extract_with_tesseract(image_path):
    """使用 Tesseract OCR 提取文字"""
    try:
        import pytesseract
        from PIL import Image

        img = Image.open(image_path)
        # 中文识别需要 chi_sim 语言包
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        if not text.strip():
            # 尝试只用英文
            text = pytesseract.image_to_string(img, lang='eng')
        return text.strip()
    except ImportError:
        print("[提示] pytesseract 未安装。正在尝试安装...", file=sys.stderr)
        import subprocess
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install",
             "pytesseract", "Pillow",
             "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/",
             "--trusted-host", "pypi.tuna.tsinghua.edu.cn"],
            stdout=sys.stderr, stderr=sys.stderr)
        print("[提示] 还需要安装 Tesseract OCR 引擎，请访问 https://github.com/UB-Mannheim/tesseract/wiki 下载安装", file=sys.stderr)
        return extract_with_tesseract(image_path)
    except Exception as e:
        return f"[错误] Tesseract OCR 处理失败: {e}\n请确认 Tesseract 已正确安装并配置中文语言包 (chi_sim)。"


def main():
    parser = argparse.ArgumentParser(description='保险条款图片OCR文字提取')
    parser.add_argument('image', help='图片文件路径 (支持 PNG/JPG/JPEG/BMP/TIFF)')
    parser.add_argument('--output', '-o', help='输出文本文件路径')
    parser.add_argument('--engine', choices=['paddle', 'tesseract'], default='paddle',
                        help='OCR引擎选择 (默认: paddle)')

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"错误: 图片文件不存在: {args.image}", file=sys.stderr)
        sys.exit(1)

    # 检查图片格式
    ext = os.path.splitext(args.image)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp'):
        print(f"错误: 不支持的图片格式: {ext}", file=sys.stderr)
        sys.exit(1)

    print(f"正在处理: {args.image}", file=sys.stderr)

    if args.engine == 'paddle':
        text = extract_with_paddleocr(args.image)
    else:
        text = extract_with_tesseract(args.image)

    if not text.strip():
        print("[警告] 未能提取到文字内容。")
        text = "[提示] 未能从图片中提取到文字，请确认：\n1. 图片清晰度是否足够\n2. 图片中包含中文文字\n3. 可尝试更换 OCR 引擎（--engine tesseract）"

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"文字已保存至: {args.output}", file=sys.stderr)
    else:
        print(text)


if __name__ == '__main__':
    main()
