#!/usr/bin/env python3
"""
OCR 工具 - 支持本地图片、URL、base64 输入
用法: python3 ocr.py <图片路径或URL或base64> [--lang <语言列表>]
语言: chi_sim(简体中文), chi_tra(繁体), eng, jpn, kor 等
"""

import sys
import os
import re
import base64
import tempfile
import subprocess
import shutil
import argparse


def is_url(s):
    return s.startswith('http://') or s.startswith('https://')

def is_base64(s):
    if len(s) < 100:
        return False
    # 简单的 base64 检测
    pattern = re.compile(r'^[A-Za-z0-9+/=]{50,}$')
    return bool(pattern.match(s))

def download_file(url, tmp_path):
    """下载文件到临时路径"""
    try:
        import urllib.request
        urllib.request.urlretrieve(url, tmp_path)
        return tmp_path
    except Exception as e:
        # 尝试 curl
        result = subprocess.run(['curl', '-s', '-o', tmp_path, url], capture_output=True)
        if result.returncode != 0:
            raise Exception(f"下载失败: {e}")
        return tmp_path

def run_tesseract(image_path, languages='chi_sim+eng', psm=6):
    """运行 tesseract OCR"""
    cmd = ['tesseract', image_path, 'stdout', '--psm', str(psm), '-l', languages]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"OCR 失败: {result.stderr}")
    return result.stdout

def get_image_format(image_path):
    """检测图片格式"""
    import imghdr
    fmt = imghdr.what(image_path)
    return fmt or 'unknown'

def main():
    parser = argparse.ArgumentParser(description='OCR 工具')
    parser.add_argument('image', help='图片路径、URL 或 base64 数据')
    parser.add_argument('--lang', default='chi_sim+eng', help='语言代码，逗号分隔 (默认: chi_sim+eng)')
    parser.add_argument('--psm', type=int, default=6, help='页面分段模式 (默认: 6)')
    parser.add_argument('--raw', action='store_true', help='只输出纯文本，不带位置信息')
    args = parser.parse_args()

    image_input = args.image.strip()
    tmp_file = None

    try:
        # 判断输入类型
        if is_url(image_input):
            print(f"[OCR] 检测为 URL，正在下载...", file=sys.stderr)
            suffix = '.png'
            if '.jpg' in image_input or '.jpeg' in image_input:
                suffix = '.jpg'
            elif '.gif' in image_input:
                suffix = '.gif'
            elif '.webp' in image_input:
                suffix = '.webp'

            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
                tmp_file = f.name
            download_file(image_input, tmp_file)
            image_path = tmp_file

        elif is_base64(image_input):
            print(f"[OCR] 检测为 base64，正在解码...", file=sys.stderr)
            # 去掉可能的 data:image/xxx;base64, 前缀
            if ',' in image_input:
                image_input = image_input.split(',')[1]
            img_data = base64.b64decode(image_input)
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                tmp_file = f.name
                f.write(img_data)
            image_path = tmp_file

        else:
            # 本地文件
            image_path = os.path.expanduser(image_input)
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"文件不存在: {image_path}")

        # 检测格式
        fmt = get_image_format(image_path)
        print(f"[OCR] 图片格式: {fmt}", file=sys.stderr)

        # 运行 OCR
        print(f"[OCR] 正在识别，语言: {args.lang}...", file=sys.stderr)
        text = run_tesseract(image_path, languages=args.lang, psm=args.psm)

        if args.raw:
            print(text.strip())
        else:
            # 输出结构化结果
            print("---RAW_TEXT_START---")
            print(text.strip())
            print("---RAW_TEXT_END---")
            print(f"[OCR] 识别完成，字符数: {len(text.strip())}", file=sys.stderr)

    finally:
        if tmp_file and os.path.exists(tmp_file):
            os.unlink(tmp_file)

if __name__ == '__main__':
    main()
