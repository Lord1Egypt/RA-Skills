import fitz  # PyMuPDF
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os
import sys

def extract_qr_code(image_path, output_dir='./qr_output', padding=10):
    """从图片中提取二维码并保存，带白边padding"""
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return None
    
    decoded_objects = decode(img)
    if not decoded_objects:
        print(f"未在 {image_path} 中检测到二维码")
        return None
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    qr_codes = []
    for i, obj in enumerate(decoded_objects):
        points = obj.polygon
        rect_points = np.array(points, dtype=np.int32)
        rect_points = rect_points.reshape((-1, 1, 2))
        
        x, y, w, h = cv2.boundingRect(rect_points)
        
        # 添加白边padding
        x_start = max(x - padding, 0)
        y_start = max(y - padding, 0)
        x_end = min(x + w + padding, img.shape[1])
        y_end = min(y + h + padding, img.shape[0])
        
        qr_code_image = img[y_start:y_end, x_start:x_end]
        
        base_name = os.path.basename(image_path)
        name_without_ext = os.path.splitext(base_name)[0]
        qr_image_path = os.path.join(output_dir, f"qr_{name_without_ext}_{i+1}.png")
        cv2.imwrite(qr_image_path, qr_code_image)
        qr_codes.append(qr_image_path)
        print(f"二维码已保存到: {qr_image_path}")
    
    return qr_codes

def extract_images_from_pdf(pdf_path, output_dir='./qr_output'):
    """从 PDF 提取每一页的图片并检测二维码"""
    if not os.path.exists(pdf_path):
        print(f"PDF 文件不存在: {pdf_path}")
        return
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建输出目录: {output_dir}")
    
    doc = fitz.open(pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    page_output_dir = os.path.join(output_dir, pdf_name + '_pages')
    if not os.path.exists(page_output_dir):
        os.makedirs(page_output_dir)
    
    print(f"PDF 共 {doc.page_count} 页")
    
    all_qr_codes = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        
        img_path = os.path.join(page_output_dir, f"page_{page_num+1}.png")
        pix.save(img_path)
        print(f"提取页面 {page_num+1} 图像到 {img_path}")
        
        qr_codes = extract_qr_code(img_path, output_dir)
        if qr_codes:
            all_qr_codes.extend(qr_codes)
    
    print(f"\n完成！共提取 {len(all_qr_codes)} 个二维码")
    print(f"输出目录: {output_dir}")
    return all_qr_codes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python extract_qr.py <PDF文件路径> [输出目录]")
        print("示例: python extract_qr.py D:/pdftest/text.pdf")
        print("       python extract_qr.py D:/pdftest/text.pdf ./my_qr")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './qr_output'
    
    extract_images_from_pdf(pdf_path, output_dir)
