"""
PDF图片提取器 - 标准尺寸模式
输出800x800正方形图片，适合网站产品展示
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

def resize_to_square(image_bytes, target_size=800, quality=85):
    """调整图片为正方形，保持内容居中"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # 转换为RGB（如果是RGBA或灰度）
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        elif img.mode == 'L':
            img = img.convert('RGB')
        
        w, h = img.size
        
        # 跳过太小的图片
        if w < 200 or h < 200:
            return None
        
        # 计算新尺寸（最大边到target_size）
        if w > h:
            new_w = target_size
            new_h = int(h * (target_size / w))
        else:
            new_h = target_size
            new_w = int(w * (target_size / h))
        
        # 创建白色背景正方形画布
        new_img = Image.new('RGB', (target_size, target_size), (255, 255, 255))
        
        # 居中粘贴
        paste_x = (target_size - new_w) // 2
        paste_y = (target_size - new_h) // 2
        
        img_resized = img.resize((new_w, new_h), Image.LANCZOS)
        new_img.paste(img_resized, (paste_x, paste_y))
        
        # 保存
        output = io.BytesIO()
        new_img.save(output, format='JPEG', quality=quality, optimize=True)
        
        return output.getvalue()
    except Exception as e:
        return None

def extract_standard_images(pdf_path, output_folder, target_size=800):
    """提取PDF图片并调整为标准尺寸"""
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
            
            # 调整尺寸
            resized = resize_to_square(image_bytes, target_size=target_size)
            if resized is None:
                continue
            
            output_path = os.path.join(
                pdf_output, 
                f"{pdf_name}_{total_images+1:04d}.jpg"
            )
            
            with open(output_path, "wb") as f:
                f.write(resized)
            
            total_images += 1
            if total_images % 100 == 0:
                print(f"  📊 已处理 {total_images} 张...")
    
    doc.close()
    print(f"✅ {pdf_name} 完成：{total_images} 张图片")
    return total_images

def main():
    # ============ 配置区域 ============
    pdf_folder = r"E:\AI家具链\家具素材库"
    output_folder = os.path.join(pdf_folder, "extract_standard_800")
    target_size = 800  # 可选: 600, 800, 1000
    # =================================
    
    os.makedirs(output_folder, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
    
    print("=" * 50)
    print("🌐 标准尺寸模式 - 800x800正方形")
    print("=" * 50)
    print(f"🔍 找到 {len(pdf_files)} 个PDF")
    print(f"📐 输出尺寸: {target_size}x{target_size}")
    print(f"📁 输出位置: {output_folder}")
    
    total = 0
    for pdf_file in sorted(pdf_files):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        total += extract_standard_images(pdf_path, output_folder, target_size)
    
    print(f"\n🎉 完成！共处理 {total} 张标准图片")
    print(f"📁 保存位置: {output_folder}")

if __name__ == "__main__":
    main()
