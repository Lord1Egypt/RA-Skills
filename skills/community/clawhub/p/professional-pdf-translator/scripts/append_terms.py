"""
PDF Batch Translator — 动态专属词表追加工具
用法: python append_terms.py --file <path> --terms "English: 中文" "Another: 另一个"
自动以 UTF-8 编码追加，避免 GBK 乱码。
"""

import argparse
import os
import json
import sys


def append_terms(file_path, terms):
    try:
        abs_path = os.path.abspath(file_path)
        dir_path = os.path.dirname(abs_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        # 如果文件不存在，显式以 UTF-8 创建（避免 Windows 默认 GBK）
        if not os.path.exists(abs_path):
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write('')

        # 读取现有内容，检查是否需要在追加前补换行
        needs_newline = False
        if os.path.getsize(abs_path) > 0:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content and not content.endswith('\n'):
                    needs_newline = True

        with open(abs_path, 'a', encoding='utf-8') as f:
            if needs_newline:
                f.write('\n')
            for term in terms:
                f.write(f"{term}\n")

        return {"status": "success", "appended_count": len(terms), "file": abs_path}

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="追加术语到专属词表文件")
    parser.add_argument("--file", required=True, help="专属词表 md 文件的绝对路径")
    parser.add_argument("--terms", nargs="+", default=[], help='要追加的术语，例如 "Apple: 苹果"')
    args = parser.parse_args()

    result = append_terms(args.file, args.terms)
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
