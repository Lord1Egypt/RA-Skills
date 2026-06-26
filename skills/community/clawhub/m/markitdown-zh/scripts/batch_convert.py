#!/usr/bin/env python3
"""
批量转换文件夹中的文档为 Markdown

要求: Python 3.10+
使用方法: python3.12 scripts/batch_convert.py input_folder/ output_folder/
"""

import argparse
import sys
from pathlib import Path

# 检查 Python 版本
if sys.version_info < (3, 10):
    print(f"错误: 需要 Python 3.10 或更高版本，当前版本: {sys.version}")
    print("请使用 python3.12, python3.11 或 python3.13 运行此脚本")
    print("示例: python3.12 scripts/batch_convert.py input_folder/ output_folder/")
    sys.exit(1)

try:
    from markitdown import MarkItDown
except ImportError:
    print("错误: 未安装 markitdown 库")
    print("请使用虚拟环境安装: python3.12 -m venv markitdown-env")
    print("然后激活虚拟环境并安装 markitdown: source markitdown-env/bin/activate && pip install \"markitdown[all]\"")
    sys.exit(1)


# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {
    ".pdf", ".csv", ".docx", ".pptx", ".xlsx",
    ".html", ".htm", ".txt", ".rtf", ".xml", ".xls", ".epub"
}


def is_supported_file(file_path: Path) -> bool:
    """检查文件是否支持转换"""
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def batch_convert(input_dir: str, output_dir: str, recursive: bool = True):
    """
    批量转换目录中的文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        recursive: 是否递归处理子目录
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    if not input_dir.exists():
        print(f"错误: 目录不存在: {input_dir}")
        return False
    
    if not input_dir.is_dir():
        print(f"错误: 不是目录: {input_dir}")
        return False
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找所有支持的文件
    if recursive:
        files = list(input_dir.rglob("*"))
    else:
        files = list(input_dir.glob("*"))
    
    supported_files = [f for f in files if f.is_file() and is_supported_file(f)]
    
    if not supported_files:
        print(f"在 {input_dir} 中没有找到支持的文件")
        return True
    
    print(f"找到 {len(supported_files)} 个文件")
    print("-" * 50)
    
    md = MarkItDown()
    success_count = 0
    fail_count = 0
    
    for input_path in supported_files:
        # 计算相对路径以保持目录结构
        rel_path = input_path.relative_to(input_dir)
        output_path = output_dir / rel_path.with_suffix(".md")
        
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"正在转换: {rel_path}")
        
        try:
            result = md.convert(str(input_path))
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.text_content)
            
            print(f"  ✓ 成功: {output_path.name}")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ 失败: {e}")
            fail_count += 1
    
    print("-" * 50)
    print(f"完成: 成功 {success_count}, 失败 {fail_count}")
    
    return fail_count == 0


def main():
    parser = argparse.ArgumentParser(
        description="批量转换文件夹中的文档为 Markdown"
    )
    parser.add_argument("input_dir", help="输入目录路径")
    parser.add_argument("output_dir", help="输出目录路径")
    parser.add_argument(
        "--no-recursive", 
        action="store_true",
        help="不递归处理子目录"
    )
    
    args = parser.parse_args()
    
    success = batch_convert(
        args.input_dir, 
        args.output_dir, 
        recursive=not args.no_recursive
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
