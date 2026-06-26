#!/usr/bin/env python3
"""
PDF转图片转换脚本
用于将PDF或OFD文档转换为图片格式，以便进行发票OCR识别

使用方法:
    python pdf_to_image.py <input_path> <output_path> [--dpi DPI] [--format FORMAT]

参数说明:
    input_path: 输入文件路径（支持PDF、OFD格式）
    output_path: 输出图片路径（支持PNG、JPG格式）
    --dpi: 输出图片分辨率，默认150
    --format: 输出图片格式，默认PNG

示例:
    python pdf_to_image.py invoice.pdf invoice.png
    python pdf_to_image.py invoice.pdf output.jpg --dpi 200
"""

import os
import sys
import argparse
from pathlib import Path


def convert_pdf_to_images(input_path: str, output_path: str, dpi: int = 150, output_format: str = "PNG") -> list:
    """
    将PDF文件转换为图片

    Args:
        input_path: PDF文件路径
        output_path: 输出图片路径
        dpi: 输出分辨率
        output_format: 输出格式（PNG/JPG）

    Returns:
        生成的图片文件路径列表

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 不支持的格式
    """
    from pdf2image import convert_from_path

    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")

    if input_file.suffix.lower() != '.pdf':
        raise ValueError(f"不支持的格式: {input_file.suffix}，仅支持PDF格式")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    images = convert_from_path(
        input_path,
        dpi=dpi,
        first_page=None,
        last_page=None,
        fmt=output_format.lower()
    )

    result_paths = []
    if len(images) == 1:
        images[0].save(output_path, output_format.upper())
        result_paths.append(str(output_path))
    else:
        output_stem = output_file.stem
        output_dir = output_file.parent
        for i, image in enumerate(images, 1):
            multi_output_path = output_dir / f"{output_stem}_{i:03d}.{output_format.lower()}"
            image.save(str(multi_output_path), output_format.upper())
            result_paths.append(str(multi_output_path))

    return result_paths


def convert_ofd_to_images(input_path: str, output_path: str, dpi: int = 150, output_format: str = "PNG") -> list:
    """
    将OFD文件转换为图片

    Args:
        input_path: OFD文件路径
        output_path: 输出图片路径
        dpi: 输出分辨率
        output_format: 输出格式

    Returns:
        生成的图片文件路径

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: OFD解析失败
    """
    try:
        from ofd2pdf import OFD2PDF
    except ImportError:
        print("警告: ofd2pdf库未安装，将尝试使用备选方案")
        print("安装命令: pip install ofd2pdf")
        raise ValueError("OFD转换需要安装ofd2pdf库")

    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")

    if input_file.suffix.lower() != '.ofd':
        raise ValueError(f"不支持的格式: {input_file.suffix}，仅支持OFD格式")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    temp_pdf = output_file.with_suffix('.pdf')
    ofd_converter = OFD2PDF()
    ofd_converter.convert(input_path, str(temp_pdf), dpi=dpi)

    result_paths = convert_pdf_to_images(str(temp_pdf), output_path, dpi, output_format)

    if temp_pdf.exists():
        temp_pdf.unlink()

    return result_paths


def convert_to_image(input_path: str, output_path: str, dpi: int = 150, output_format: str = "PNG") -> list:
    """
    根据文件类型自动选择转换方式

    Args:
        input_path: 输入文件路径
        output_path: 输出图片路径
        dpi: 输出分辨率
        output_format: 输出格式

    Returns:
        生成的图片文件路径列表
    """
    input_file = Path(input_path)
    suffix = input_file.suffix.lower()

    if suffix == '.pdf':
        return convert_pdf_to_images(input_path, output_path, dpi, output_format)
    elif suffix == '.ofd':
        return convert_ofd_to_images(input_path, output_path, dpi, output_format)
    else:
        raise ValueError(f"不支持的格式: {suffix}，仅支持PDF和OFD格式")


def main():
    parser = argparse.ArgumentParser(
        description='将PDF或OFD文档转换为图片格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('input_path', help='输入文件路径（PDF或OFD）')
    parser.add_argument('output_path', help='输出图片路径')
    parser.add_argument('--dpi', type=int, default=150, help='输出图片分辨率（默认150）')
    parser.add_argument('--format', choices=['PNG', 'JPG', 'png', 'jpg'], default='PNG',
                        help='输出图片格式（默认PNG）')

    args = parser.parse_args()

    try:
        output_format = args.format.upper()
        if output_format == 'JPG':
            output_format = 'JPEG'

        result_paths = convert_to_image(
            args.input_path,
            args.output_path,
            args.dpi,
            output_format
        )

        print(f"转换成功！")
        for path in result_paths:
            print(f"  - {path}")

    except Exception as e:
        print(f"转换失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
