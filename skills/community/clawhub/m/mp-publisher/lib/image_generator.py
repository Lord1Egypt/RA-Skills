#!/usr/bin/env python3
"""
DMXAPI 图片生成脚本（OpenAI 兼容格式）
=========================================
使用 DMXAPI 的图片生成接口

用法:
    python image_generator.py <prompt> <output_path> [size]
    python image_generator.py --batch <config_json>

环境变量:
    DMX_API_KEY - DMX API密钥（必需）
    DMX_BASE_URL - API地址（可选，默认 https://www.dmxapi.cn）
    DMX_MODEL - 模型名称（可选，默认 gemini-3.1-flash-image-preview）
"""

import requests
import base64
import os
import sys
import json

# ============================================================================
# 配置
# ============================================================================

API_KEY = os.environ.get("DMX_API_KEY", "")
BASE_URL = os.environ.get("DMX_BASE_URL", "https://www.dmxapi.cn")
MODEL = os.environ.get("DMX_MODEL", "gemini-3.1-flash-image-preview")

# 默认尺寸：16:9 横版
DEFAULT_SIZE = "1792x1024"

# ============================================================================
# 图片生成函数
# ============================================================================

def generate_image(
    prompt: str,
    output_path: str,
    size: str = None
) -> bool:
    """
    使用 DMXAPI 生成图片
    
    Args:
        prompt: 图片描述提示词
        output_path: 输出图片路径
        size: 图片尺寸 (256x256, 512x512, 1024x1024, 1792x1024, 1024x1792)
    
    Returns:
        bool: 是否成功
    """
    
    if not API_KEY:
        print("[ERROR] 未配置 DMX_API_KEY 环境变量")
        return False
    
    size = size or DEFAULT_SIZE
    api_url = f"{BASE_URL}/v1/images/generations"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "response_format": "b64_json"
    }
    
    try:
        print(f"[INFO] 正在生成图片: {prompt[:50]}...")
        
        response = requests.post(
            api_url,
            headers=headers,
            json=data,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"[ERROR] API 请求失败: {response.status_code}")
            print(f"[ERROR] 响应内容: {response.text[:500]}")
            return False
        
        result = response.json()
        
        if "data" in result and len(result["data"]) > 0:
            image_data = result["data"][0].get("b64_json", "")
            
            if image_data:
                image_bytes = base64.b64decode(image_data)
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                
                with open(output_path, "wb") as f:
                    f.write(image_bytes)
                
                print(f"[SUCCESS] 图片已保存: {output_path}")
                return True
        
        print(f"[ERROR] 响应中没有找到图片数据")
        return False
        
    except Exception as e:
        print(f"[ERROR] 错误: {e}")
        return False


def generate_batch(config: dict) -> dict:
    """
    批量生成图片
    
    Args:
        config: {
            "output_dir": "输出目录",
            "images": [
                {"name": "cover", "prompt": "..."},
                {"name": "image1", "prompt": "..."},
                ...
            ]
        }
    
    Returns:
        {"success": [...], "failed": [...]}
    """
    results = {"success": [], "failed": []}
    output_dir = config.get("output_dir", ".")
    os.makedirs(output_dir, exist_ok=True)
    
    for img in config.get("images", []):
        name = img.get("name", "image")
        prompt = img.get("prompt", "")
        size = img.get("size", DEFAULT_SIZE)
        
        output_path = os.path.join(output_dir, f"{name}.png")
        
        if generate_image(prompt, output_path, size):
            results["success"].append(output_path)
        else:
            results["failed"].append(name)
    
    return results


# ============================================================================
# 公众号配图专用函数
# ============================================================================

def generate_article_images(article_title: str, output_dir: str) -> dict:
    """
    为公众号文章生成4张配图
    
    Args:
        article_title: 文章标题（用于生成提示词）
        output_dir: 输出目录
    
    Returns:
        {"success": [...], "failed": [...]}
    """
    
    # 从标题提取关键词
    keywords = article_title.replace("：", " ").replace("？", " ").replace("，", " ")
    
    # 生成提示词（科技感风格）
    prompts = {
        "cover": f"Technology abstract background, futuristic digital network, blue and purple gradient, minimalist style, 16:9 aspect ratio, high quality, no text -- {keywords}",
        "image1": f"Abstract technology illustration, data flow visualization, modern geometric shapes, blue tones, clean design, 16:9 aspect ratio, no text",
        "image2": f"Futuristic AI concept art, neural network visualization, glowing nodes and connections, dark background with blue accents, 16:9 aspect ratio, no text",
        "image3": f"Technology innovation concept, abstract digital transformation, modern infographic style, blue and cyan colors, 16:9 aspect ratio, no text"
    }
    
    config = {
        "output_dir": output_dir,
        "images": [
            {"name": "cover", "prompt": prompts["cover"], "size": "1792x1024"},
            {"name": "image1", "prompt": prompts["image1"], "size": "1792x1024"},
            {"name": "image2", "prompt": prompts["image2"], "size": "1792x1024"},
            {"name": "image3", "prompt": prompts["image3"], "size": "1792x1024"}
        ]
    }
    
    return generate_batch(config)


# ============================================================================
# 主函数
# ============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("用法: python image_generator.py --batch <config_json>")
            sys.exit(1)
        
        config = json.loads(sys.argv[2])
        results = generate_batch(config)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        
    elif sys.argv[1] == "--article":
        if len(sys.argv) < 4:
            print("用法: python image_generator.py --article <title> <output_dir>")
            sys.exit(1)
        
        title = sys.argv[2]
        output_dir = sys.argv[3]
        results = generate_article_images(title, output_dir)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        
    else:
        if len(sys.argv) < 3:
            print("用法: python image_generator.py <prompt> <output_path> [size]")
            sys.exit(1)
        
        prompt = sys.argv[1]
        output_path = sys.argv[2]
        size = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_SIZE
        
        success = generate_image(prompt, output_path, size)
        sys.exit(0 if success else 1)
