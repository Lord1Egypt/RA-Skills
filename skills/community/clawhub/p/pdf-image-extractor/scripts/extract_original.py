"""
PDF图片提取器 - 原始高清模式
保持PDF图片的原始分辨率，适合印刷用途
"""

import fitz
import os
import re

def safe_filename(name):
    """生成安全的文件名"""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name

def extract_original_images(pdf_path, output_folder):
    """提取PDF中原始高清图片"""
    print(f"\n📄 处理: {pdf_path}")
    
    pdf_name = safe_filename(os.path.splitext(os.path.basename(pdf_path))[0])
    pdf_output = os.path.join(output_folder, pdf_name)
    os.makedirs(pdf_output, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    total_images = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # 跳过太小的图片（可能是图标）
            if len(image_bytes) < 10000:
                continue
            
            output_path = os.path.join(
                pdf_output, 
                f"page{page_num+1:03d}_img{img_index+1:02d}.{image_ext}"
            )
            
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            
            total_images += 1
            size_kb = os.path.getsize(output_path) // 1024
            if total_images % 100 == 0:
                print(f"  📊 已提取 {total_images} 张... (最新: {size_kb}KB)")
    
    doc.close()
    print(f"✅ {pdf_name} 完成：{total_images} 张图片")
    return total_images

def main():
    # ============ 配置区域 ============
    pdf_folder = r"E:\AI家具链\家具素材库"
    output_folder = os.path.join(pdf_folder, "extract_original")
    # =================================
    
    os.makedirs(output_folder, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    
    print("=" * 50)
    print("🖨️  原始高清模式 - 保持100%清晰度")
    print("=" * 50)
    print(f"🔍 找到 {len(pdf_files)} 个PDF")
    print(f"📁 输出位置: {output_folder}")
    
    total = 0
    for pdf_file in sorted(pdf_files):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        total += extract_original_images(pdf_path, output_folder)
    
    print(f"\n🎉 完成！共提取 {total} 张高清图片")
    print(f"📁 保存位置: {output_folder}")

if __name__ == "__main__":
    main()
