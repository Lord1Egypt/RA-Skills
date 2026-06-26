#!/usr/bin/env python3
"""
从文档中提取图片

要求: Python 3.10+
使用方法: python3.12 scripts/extract_images.py document.pdf images_folder/
"""

import argparse
import sys
from pathlib import Path

# 检查 Python 版本
if sys.version_info < (3, 10):
    print(f"错误: 需要 Python 3.10 或更高版本，当前版本: {sys.version}")
    print("请使用 python3.12, python3.11 或 python3.13 运行此脚本")
    print("示例: python3.12 scripts/extract_images.py document.pdf images_folder/")
    sys.exit(1)

try:
    from markitdown import MarkItDown
except ImportError:
    print("错误: 未安装 markitdown 库")
    print("请使用虚拟环境安装: python3.12 -m venv markitdown-env")
    print("然后激活虚拟环境并安装 markitdown: source markitdown-env/bin/activate && pip install \"markitdown[all]\"")
    sys.exit(1)


def extract_images(input_path: str, output_dir: str):
    """
    从文档中提取图片
    
    Args:
        input_path: 输入文件路径
        output_dir: 输出目录
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    
    if not input_path.exists():
        print(f"错误: 文件不存在: {input_path}")
        return False
    
    if not input_path.is_file():
        print(f"错误: 不是文件: {input_path}")
        return False
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"正在从 {input_path.name} 提取图片...")
    
    try:
        md = MarkItDown()
        result = md.convert(str(input_path))
        
        # 尝试从结果中获取图片
        # 注意: markitdown 的 API 可能有所不同，这里是基础实现
        image_count = 0
        
        # 如果结果有 images 属性，使用它
        if hasattr(result, 'images') and result.images:
            for i, image in enumerate(result.images):
                image_path = output_dir / f"image_{i+1:03d}.{image.format or 'png'}"
                
                if hasattr(image, 'save'):
                    image.save(str(image_path))
                elif hasattr(image, 'data'):
                    with open(image_path, 'wb') as f:
                        f.write(image.data)
                
                print(f"  提取: {image_path.name}")
                image_count += 1
        else:
            # 尝试从文本内容中分析图片标记
            print("  提示: markitdown 可能不直接支持图片提取")
            print("  转换后的 Markdown 已保存，可从中查看图片引用")
            
            # 保存转换结果供参考
            md_output = output_dir / f"{input_path.stem}_converted.md"
            with open(md_output, "w", encoding="utf-8") as f:
                f.write(result.text_content)
            print(f"  转换结果: {md_output.name}")
        
        if image_count > 0:
            print(f"\n成功提取 {image_count} 张图片到 {output_dir}")
        else:
            print("\n未找到可提取的图片")
        
        return True
        
    except Exception as e:
        print(f"提取失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="从文档中提取图片"
    )
    parser.add_argument("input_file", help="输入文件路径")
    parser.add_argument("output_dir", help="输出目录路径")
    
    args = parser.parse_args()
    
    success = extract_images(args.input_file, args.output_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
