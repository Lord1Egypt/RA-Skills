#!/usr/bin/env python3
"""
图片管理器 - 处理知识库中的图片附件
支持：保存图片、OCR 提取文字、查询图片内容
"""

import os
import json
import hashlib
import shutil
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any, List

ATTACHMENTS_ROOT = os.path.join(os.path.dirname(__file__), "attachments")

def ensure_attachments_dir(business_name: str) -> str:
    """确保业务附件目录存在"""
    dir_path = os.path.join(ATTACHMENTS_ROOT, business_name)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def save_image(image_path: str, business_name: str, question_id: str = None) -> Dict[str, Any]:
    """保存图片到附件目录"""
    if not os.path.exists(image_path):
        return {"status": "error", "message": f"图片文件不存在：{image_path}"}
    
    # 创建业务目录
    business_dir = ensure_attachments_dir(business_name)
    
    # 生成文件名
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp']:
        ext = '.png'
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_id = hashlib.md5(f"{business_name}{timestamp}{os.path.basename(image_path)}".encode()).hexdigest()[:8]
    filename = f"{file_id}{ext}"
    
    # 复制文件
    dest_path = os.path.join(business_dir, filename)
    shutil.copy2(image_path, dest_path)
    
    # 获取文件信息
    file_size = os.path.getsize(dest_path)
    
    return {
        "status": "saved",
        "filename": filename,
        "path": dest_path,
        "relative_path": os.path.join(business_name, filename),
        "size_bytes": file_size,
        "size_kb": round(file_size / 1024, 2),
        "ext": ext,
        "created": datetime.now().isoformat()
    }

def extract_text_ocr(image_path: str) -> Dict[str, Any]:
    """使用 OCR 提取图片中的文字"""
    if not os.path.exists(image_path):
        return {"status": "error", "message": "图片文件不存在"}
    
    try:
        # 尝试使用 pytesseract
        try:
            import pytesseract
            from PIL import Image
            
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            
            return {
                "status": "success",
                "text": text.strip(),
                "method": "pytesseract",
                "extracted_at": datetime.now().isoformat()
            }
        except ImportError:
            pass
        except Exception as e:
            return {"status": "error", "message": f"pytesseract 错误：{str(e)}"}
        
        # 尝试使用系统命令 tesseract
        tesseract_cmd = shutil.which('tesseract')
        if tesseract_cmd:
            try:
                output_base = image_path + "_ocr"
                subprocess.run([
                    tesseract_cmd,
                    image_path,
                    output_base,
                    '-l', 'chi_sim+eng'
                ], check=True, capture_output=True)
                
                output_txt = output_base + ".txt"
                if os.path.exists(output_txt):
                    with open(output_txt, 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                    os.remove(output_txt)  # 清理临时文件
                    
                    return {
                        "status": "success",
                        "text": text,
                        "method": "tesseract_cli",
                        "extracted_at": datetime.now().isoformat()
                    }
            except Exception as e:
                return {"status": "error", "message": f"tesseract 命令错误：{str(e)}"}
        
        # 尝试使用易语言中文 OCR（如果有）
        # 这里可以集成其他 OCR 服务
        
        return {
            "status": "no_ocr",
            "message": "未找到可用的 OCR 引擎。请安装：pip install pytesseract pillow 或 apt install tesseract-ocr tesseract-ocr-chi-sim",
            "suggestion": "可以手动输入图片描述"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"OCR 提取失败：{str(e)}"}

def get_image_info(business_name: str, filename: str) -> Optional[Dict[str, Any]]:
    """获取图片信息"""
    image_path = os.path.join(ATTACHMENTS_ROOT, business_name, filename)
    if not os.path.exists(image_path):
        return None
    
    file_size = os.path.getsize(image_path)
    created = datetime.fromtimestamp(os.path.getctime(image_path))
    modified = datetime.fromtimestamp(os.path.getmtime(image_path))
    
    return {
        "filename": filename,
        "path": image_path,
        "relative_path": os.path.join(business_name, filename),
        "size_bytes": file_size,
        "size_kb": round(file_size / 1024, 2),
        "ext": os.path.splitext(filename)[1],
        "created": created.isoformat(),
        "modified": modified.isoformat()
    }

def list_images(business_name: str = None) -> List[Dict[str, Any]]:
    """列出所有图片"""
    images = []
    
    if not os.path.exists(ATTACHMENTS_ROOT):
        return images
    
    if business_name:
        # 列出特定业务的图片
        business_dir = os.path.join(ATTACHMENTS_ROOT, business_name)
        if os.path.exists(business_dir):
            for f in os.listdir(business_dir):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')):
                    info = get_image_info(business_name, f)
                    if info:
                        images.append(info)
    else:
        # 列出所有业务的图片
        for business in os.listdir(ATTACHMENTS_ROOT):
            business_dir = os.path.join(ATTACHMENTS_ROOT, business)
            if os.path.isdir(business_dir):
                for f in os.listdir(business_dir):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')):
                        info = get_image_info(business, f)
                        if info:
                            info['business'] = business
                            images.append(info)
    
    return sorted(images, key=lambda x: x['created'], reverse=True)

def delete_image(business_name: str, filename: str) -> Dict[str, Any]:
    """删除图片"""
    image_path = os.path.join(ATTACHMENTS_ROOT, business_name, filename)
    if not os.path.exists(image_path):
        return {"status": "not_found", "message": "图片不存在"}
    
    try:
        os.remove(image_path)
        return {"status": "deleted", "message": "已删除图片", "filename": filename}
    except Exception as e:
        return {"status": "error", "message": f"删除失败：{str(e)}"}

def get_stats() -> Dict[str, Any]:
    """获取图片统计"""
    total_images = 0
    total_size = 0
    businesses = {}
    
    if os.path.exists(ATTACHMENTS_ROOT):
        for business in os.listdir(ATTACHMENTS_ROOT):
            business_dir = os.path.join(ATTACHMENTS_ROOT, business)
            if os.path.isdir(business_dir):
                biz_images = 0
                biz_size = 0
                for f in os.listdir(business_dir):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')):
                        biz_images += 1
                        biz_size += os.path.getsize(os.path.join(business_dir, f))
                
                if biz_images > 0:
                    businesses[business] = {
                        "images": biz_images,
                        "size_kb": round(biz_size / 1024, 2)
                    }
                    total_images += biz_images
                    total_size += biz_size
    
    return {
        "total_images": total_images,
        "total_size_kb": round(total_size / 1024, 2),
        "total_size_mb": round(total_size / 1024 / 1024, 2),
        "businesses": businesses
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("图片管理器")
        print("")
        print("用法：python image-manager.py <命令> [参数]")
        print("")
        print("命令:")
        print("  save <业务名> <图片路径>  - 保存图片")
        print("  ocr <图片路径>            - OCR 提取文字")
        print("  list [业务名]             - 列出图片")
        print("  stats                     - 统计信息")
        print("  delete <业务名> <文件名>   - 删除图片")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "save" and len(sys.argv) >= 4:
        result = save_image(sys.argv[3], sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "ocr" and len(sys.argv) >= 3:
        result = extract_text_ocr(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "list":
        business = sys.argv[2] if len(sys.argv) >= 3 else None
        images = list_images(business)
        print(json.dumps(images, ensure_ascii=False, indent=2))
    
    elif cmd == "stats":
        result = get_stats()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "delete" and len(sys.argv) >= 4:
        result = delete_image(sys.argv[2], sys.argv[3])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令：{cmd}")
