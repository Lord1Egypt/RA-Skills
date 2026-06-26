#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PPTX to Image Converter

将 PowerPoint (PPTX) 演示文稿转换为高质量图片（JPG/PNG）。
支持自定义 DPI，保持原始比例，横版/竖版自适应。

依赖:
    - Python 3.10+
    - Windows 系统
    - Microsoft PowerPoint
    - pywin32 库

使用示例:
    py pptx_to_image.py -i presentation.pptx -o ./slides --dpi 300
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import win32com.client
except ImportError:
    print("错误：需要安装 pywin32 库")
    print("运行：pip install pywin32")
    sys.exit(1)


def pptx_to_images(pptx_path, output_folder, dpi=300, img_format="jpg", quality=95, verbose=True):
    """
    将 PPTX 文件的每一页转换为图片
    
    参数:
        pptx_path: PPTX 文件路径
        output_folder: 输出文件夹路径
        dpi: 输出图片 DPI (72-600)
        img_format: 输出格式 ('jpg' 或 'png')
        quality: JPG 质量 (1-100)
        verbose: 是否显示详细信息
    
    返回:
        list: 导出的文件路径列表
    """
    
    # 验证输入文件
    pptx_path = Path(pptx_path).resolve()
    if not pptx_path.exists():
        raise FileNotFoundError(f"找不到文件：{pptx_path}")
    
    if pptx_path.suffix.lower() not in ['.pptx', '.ppt']:
        raise ValueError(f"不支持的文件格式：{pptx_path.suffix}")
    
    # 创建输出文件夹
    output_folder = Path(output_folder).resolve()
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # 验证参数
    if not 72 <= dpi <= 600:
        raise ValueError(f"DPI 必须在 72-600 之间，当前：{dpi}")
    
    if img_format.lower() not in ['jpg', 'jpeg', 'png']:
        raise ValueError(f"不支持的格式：{img_format}，请使用 'jpg' 或 'png'")
    
    if not 1 <= quality <= 100:
        raise ValueError(f"质量必须在 1-100 之间，当前：{quality}")
    
    # 启动 PowerPoint
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = True  # COM 要求窗口可见
    
    try:
        # 打开演示文稿（只读模式）
        presentation = powerpoint.Presentations.Open(str(pptx_path), ReadOnly=True, WithWindow=False)
        
        # 获取原始尺寸（点，1 点 = 1/72 英寸）
        orig_width = presentation.PageSetup.SlideWidth
        orig_height = presentation.PageSetup.SlideHeight
        
        # 判断方向
        is_landscape = orig_width > orig_height
        orientation = "横版 (Landscape)" if is_landscape else "竖版 (Portrait)"
        
        if verbose:
            print("=" * 60)
            print(f"PPTX → {img_format.upper()} | 保持原始比例 | {dpi} DPI")
            print("=" * 60)
            print(f"\n输入文件：{pptx_path}")
            print(f"原始尺寸：{orig_width} x {orig_height} 点")
            print(f"原始比例：{orig_width/orig_height:.4f}")
            print(f"方向：{orientation}")
        
        # 计算目标像素尺寸
        # 公式：像素 = 点 × (DPI / 72)
        scale_factor = dpi / 72.0
        target_width = int(orig_width * scale_factor)
        target_height = int(orig_height * scale_factor)
        
        if verbose:
            print(f"\n目标 DPI: {dpi}")
            print(f"目标尺寸：{target_width} x {target_height} 像素")
            print(f"实际 DPI X: {target_width / (orig_width/72):.1f}")
            print(f"实际 DPI Y: {target_height / (orig_height/72):.1f}")
        
        # 获取幻灯片数量
        slide_count = presentation.Slides.Count
        if verbose:
            print(f"\n幻灯片数量：{slide_count}")
        
        # 导出每一页
        exported_files = []
        file_ext = "jpg" if img_format.lower() in ['jpg', 'jpeg'] else "png"
        
        for i in range(1, slide_count + 1):
            slide = presentation.Slides(i)
            output_filename = f"slide_{i:03d}.{file_ext}"
            output_path = output_folder / output_filename
            
            # 导出图片
            if img_format.lower() in ['jpg', 'jpeg']:
                slide.Export(str(output_path), "JPG", target_width, target_height)
            else:
                slide.Export(str(output_path), "PNG", target_width, target_height)
            
            exported_files.append(str(output_path))
            
            if verbose:
                file_size_kb = os.path.getsize(output_path) / 1024
                print(f"\n[OK] 已导出第 {i} 页")
                print(f"  路径：{output_path}")
                print(f"  尺寸：{target_width} x {target_height} 像素")
                print(f"  大小：{file_size_kb:.1f} KB")
        
        presentation.Close()
        
        if verbose:
            print("\n" + "=" * 60)
            print(f"[DONE] 完成！共导出 {len(exported_files)} 张图片")
            for f in exported_files:
                size_mb = os.path.getsize(f) / (1024 * 1024)
                print(f"  {Path(f).name}: {size_mb:.2f} MB")
        
        return exported_files
        
    except Exception as e:
        print(f"\n错误：{e}")
        if 'presentation' in locals():
            try:
                presentation.Close()
            except:
                pass
        raise
    finally:
        try:
            powerpoint.Quit()
        except:
            pass


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="PPTX 转图片工具 - 支持自定义 DPI，保持原始比例",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -i presentation.pptx -o ./slides
  %(prog)s -i input.pptx -o output --dpi 600 --format png
  %(prog)s -i slides.pptx --dpi 150 -v
        """
    )
    
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="输入的 PPTX 文件路径"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="./output",
        help="输出文件夹路径 (默认：./output)"
    )
    
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="输出图片 DPI，范围 72-600 (默认：300)"
    )
    
    parser.add_argument(
        "--format",
        choices=["jpg", "png"],
        default="jpg",
        help="输出格式 (默认：jpg)"
    )
    
    parser.add_argument(
        "--quality",
        type=int,
        default=95,
        help="JPG 质量 1-100 (默认：95)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细信息"
    )
    
    args = parser.parse_args()
    
    try:
        files = pptx_to_images(
            pptx_path=args.input,
            output_folder=args.output,
            dpi=args.dpi,
            img_format=args.format,
            quality=args.quality,
            verbose=args.verbose or True  # 默认显示输出
        )
        return 0
    except Exception as e:
        print(f"\n转换失败：{e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
