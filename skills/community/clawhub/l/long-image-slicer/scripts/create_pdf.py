#!/usr/bin/env python3
"""
从切片图片生成 PDF v5
- A4 大小
- 每页一张切片
- **左右边距固定 2cm**
- **按高度缩放，确保所有切片完整显示**
- 页码在右下角（距右边 1cm，距底部 0.5cm）

使用方法：
    python3 create_pdf.py <切片目录> [输出 PDF 路径]
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import black
import os
import sys

# 配置 - 使用命令行参数
if len(sys.argv) < 2:
    print("用法：python3 create_pdf.py <切片目录> [输出 PDF 路径]")
    print("示例：python3 create_pdf.py /path/to/slices /path/to/output.pdf")
    sys.exit(1)

SLICES_DIR = sys.argv[1]
OUTPUT_PDF = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(SLICES_DIR), "slices_v7.pdf")

# PDF 页面设置
PAGE_WIDTH, PAGE_HEIGHT = A4  # 21.0cm x 29.7cm

# 边距配置
LEFT_MARGIN = 2 * cm       # 左边距固定 2cm
RIGHT_MARGIN = 2 * cm      # 右边距固定 2cm
TOP_MARGIN = 1 * cm        # 上边距
BOTTOM_MARGIN = 1 * cm     # 下边距

# 页码位置（右下角）
# 距页面右边缘 1cm，距页面下边缘 0.5cm
PAGE_NUM_X = PAGE_WIDTH - 1 * cm
PAGE_NUM_Y = 0.5 * cm

def get_slice_files(slices_dir):
    files = [f for f in os.listdir(slices_dir) if f.endswith('.jpg')]
    files.sort()
    return [os.path.join(slices_dir, f) for f in files]

def calculate_scale_for_max_height(slice_files):
    """根据最高切片计算缩放比例，确保所有切片完整显示"""
    max_height = 0
    for slice_path in slice_files:
        img_width, img_height = canvas.ImageReader(slice_path).getSize()
        if img_height > max_height:
            max_height = img_height
    
    # 可用高度
    available_height = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    
    # 计算缩放比例（让最高切片刚好适应可用高度）
    scale = available_height / max_height
    
    return scale, max_height, available_height

def create_pdf(slice_files, output_path):
    # 计算缩放比例
    scale, max_height, available_height = calculate_scale_for_max_height(slice_files)
    
    # 计算缩放后宽度
    scaled_width = 781 * scale
    
    # 计算实际左右边距（居中显示）
    actual_side_margin = (PAGE_WIDTH - scaled_width) / 2
    
    print(f"创建 PDF (左右边距 2cm + 高度优先)...")
    print(f"  页面大小：A4 ({PAGE_WIDTH/cm:.1f}cm x {PAGE_HEIGHT/cm:.1f}cm)")
    print(f"  最高切片：{max_height}px")
    print(f"  可用高度：{available_height/cm:.1f}cm")
    print(f"  缩放比例：{scale:.4f} cm/px")
    print(f"  缩放后宽度：{scaled_width/cm:.1f}cm")
    print(f"  实际左右边距：{actual_side_margin/cm:.1f}cm")
    print(f"  上边距：{TOP_MARGIN/cm:.1f}cm")
    print(f"  下边距：{BOTTOM_MARGIN/cm:.1f}cm")
    print(f"  页码位置：右下 (距页面右边缘 1cm, 距下边缘 0.5cm)")
    print(f"  切片数量：{len(slice_files)}")
    
    c = canvas.Canvas(output_path, pagesize=A4)
    
    for i, slice_path in enumerate(slice_files):
        if i > 0:
            c.showPage()
        
        page_num = i + 1
        img_width, img_height = canvas.ImageReader(slice_path).getSize()
        
        # 计算缩放后高度
        scaled_height = img_height * scale
        
        # 垂直居中
        y_position = (PAGE_HEIGHT - scaled_height) / 2
        
        # 水平居中
        x_position = (PAGE_WIDTH - scaled_width) / 2
        
        c.drawImage(slice_path, x_position, y_position, width=scaled_width, height=scaled_height)
        
        # 页码（右下角，距页面右边缘 1cm，距下边缘 0.5cm）
        c.setFont("Helvetica", 9)
        c.setFillColor(black)
        page_num_text = f"{page_num} / {len(slice_files)}"
        c.drawRightString(PAGE_WIDTH - 1 * cm, 0.5 * cm, page_num_text)
        
        print(f"  第 {page_num} 页：{os.path.basename(slice_path)} ({scaled_width/cm:.1f}cm x {scaled_height/cm:.1f}cm)")
    
    c.save()
    print(f"  保存：{output_path}")

def main():
    print("=" * 50)
    print("切片图片转 PDF v5 - 2cm 边距 + 高度优先")
    print("=" * 50)
    
    slice_files = get_slice_files(SLICES_DIR)
    
    if not slice_files:
        print(f"错误：未找到切片文件")
        return
    
    create_pdf(slice_files, OUTPUT_PDF)
    
    file_size = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print("=" * 50)
    print("✅ PDF 生成完成!")
    print(f"  输出：{OUTPUT_PDF}")
    print(f"  大小：{file_size:.1f} MB")
    print(f"  页数：{len(slice_files)}")
    print("=" * 50)

if __name__ == "__main__":
    main()
