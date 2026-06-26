#!/usr/bin/env python3
"""
读取产品评论CSV文件，输出原始评论数据

用法:
    python read_csv.py <csv_file_path>
    python read_csv.py <csv_file_path> --column <column_name>

输出:
    raw_reviews.txt - 每行一条评论
"""

import sys
import csv
from pathlib import Path


def detect_encoding(file_path):
    """检测文件编码"""
    try:
        import chardet
    except ModuleNotFoundError:
        print("错误: 缺少依赖包 chardet，无法自动识别 CSV 编码")
        print("请先安装依赖：pip install -r requirements.txt")
        sys.exit(1)
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def read_csv(file_path, column_name=None):
    """读取CSV文件并提取评论内容"""
    # 检测编码
    encoding = detect_encoding(file_path)
    print(f"检测到编码: {encoding}")

    reviews = []

    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        reader = csv.DictReader(f)

        if column_name:
            # 使用指定列
            if column_name not in reader.fieldnames:
                print(f"错误: 列 '{column_name}' 不存在")
                print(f"可用列: {', '.join(reader.fieldnames)}")
                return None
            col = column_name
        else:
            # 自动查找包含评论的列
            col = None
            for fieldname in reader.fieldnames:
                fieldname_lower = fieldname.lower()
                if any(keyword in fieldname_lower for keyword in ['评论', 'comment', '内容', 'content', '反馈', 'review', 'text']):
                    col = fieldname
                    print(f"自动识别评论列: {col}")
                    break

            if not col:
                # 使用第一列
                col = reader.fieldnames[0]
                print(f"未找到评论列，使用第一列: {col}")

        # 读取评论
        for i, row in enumerate(reader, 1):
            content = row.get(col, '').strip()
            if content:
                reviews.append((i, content))

    return reviews


def save_reviews(reviews, output_file='raw_reviews.txt'):
    """保存评论到文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for line_num, content in reviews:
            # 格式: [行号] 内容
            f.write(f"[{line_num}] {content}\n")
    print(f"已保存 {len(reviews)} 条评论到 {output_file}")


def main():
    if len(sys.argv) < 2:
        print("用法: python read_csv.py <csv_file_path> [--column <column_name>]")
        sys.exit(1)

    file_path = sys.argv[1]
    column_name = None

    if '--column' in sys.argv:
        idx = sys.argv.index('--column')
        if idx + 1 < len(sys.argv):
            column_name = sys.argv[idx + 1]

    # 检查文件存在
    if not Path(file_path).exists():
        print(f"错误: 文件 '{file_path}' 不存在")
        sys.exit(1)

    # 读取评论
    reviews = read_csv(file_path, column_name)

    if reviews is None:
        sys.exit(1)

    # 保存评论
    save_reviews(reviews)

    # 输出统计
    print(f"\n统计信息:")
    print(f"  总评论数: {len(reviews)}")
    if len(reviews) > 0:
        print(f"\n前3条评论预览:")
        for i, (line_num, content) in enumerate(reviews[:3], 1):
            preview = content[:100] + "..." if len(content) > 100 else content
            print(f"  [{line_num}] {preview}")


if __name__ == '__main__':
    main()
