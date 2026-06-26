"""
PDF图片提取器 - 压缩优化模式
输出小体积图片，适合社交平台分享
"""

import fitz
import os
import re
from PIL import Image
import io

def safe_filename(name):
    """生成安全的文件名"""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name

def compress_image(image_bytes, max_size=400, max_kb=50):
    """压缩图片到指定大小，适合社交分享"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # 转换为RGB
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        elif img.mode == 'L':
            img = img.convert('RGB')
        
        w, h = img.size
        
        # 跳过太小的图片
        if w < 150 or h < 150:
            return None
        
        # 计算新尺寸
        if w > h:
            new_w = min(w, max_size)
            new_h = int(h * (new_w / w))
        else:
            new_h = min(h, max_size)
            new_w = int(w * (new_h / h))
        
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)
        
        # 逐步降低质量直到文件小于max_kb
        for quality in [80, 60, 40]:
            output = io.BytesIO()
            img_resized.save(output, format='JPEG', quality=quality, optimize=True)
            result = output.getvalue()
            
            if len(result) <= max_kb * 1024:
                return result
        
        return result
    except Exception as e:
        return None

def extract_compress_images(pdf_path, output_folder, max_size=400, max_kb=50):
    """提取PDF图片并压缩优化"""
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
            
            # 跳过太小的图片
            if len(image_bytes) < 10000:
                continue
            
            # 压缩
            compressed = compress_image(image_bytes, max_size=max_size, max_kb=max_kb)
            if compressed is None:
                continue
            
            output_path = os.path.join(
                pdf_output, 
                f"分享图_{total_images+1:04d}.jpg"
            )
            
            with open(output_path, "wb") as f:
                f.write(compressed)
            
            total_images += 1
            if total_images % 100 == 0:
                size_kb = len(compressed) // 1024
                print(f"  📊 已处理 {total_images} 张... (最新: {size_kb}KB)")
    
    doc.close()
    print(f"✅ {pdf_name} 完成：{total_images} 张图片")
    return total_images

def main():
    # ============ 配置区域 ============
    pdf_folder = r"E:\AI家具链\家具素材库"
    output_folder = os.path.join(pdf_folder, "extract_compress_share")
    max_size = 400      # 最大边像素
    max_kb = 50         # 最大文件大小(KB)
    # =================================
    
    os.makedirs(output_folder, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    
    print("=" * 50)
    print("📱 压缩优化模式 - 适合社交分享")
    print("=" * 50)
    print(f"🔍 找到 {len(pdf_files)} 个PDF")
    print(f"📐 最大尺寸: {max_size}px")
    print(f"📦 最大体积: {max_kb}KB")
    print(f"📁 输出位置: {output_folder}")
    
    total = 0
    for pdf_file in sorted(pdf_files):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        total += extract_compress_images(pdf_path, output_folder, max_size, max_kb)
    
    print(f"\n🎉 完成！共处理 {total} 张分享图片")
    print(f"📁 保存位置: {output_folder}")

if __name__ == "__main__":
    main()
