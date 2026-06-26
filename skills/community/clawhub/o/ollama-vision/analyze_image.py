#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Vision 分析脚本（API 版本）
调用本地 Ollama 的 qwen3-vl:4b 模型分析图片
支持自动压缩超过 2MB 的图片
"""

import sys
import os
import subprocess
import json
import base64
import requests
import tempfile


def get_ollama_path():
    """获取 Ollama 可执行文件路径"""
    possible_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe"),
        r"C:\Program Files\Ollama\ollama.exe",
        r"C:\Program Files (x86)\Ollama\ollama.exe",
        "ollama"
    ]
    
    for path in possible_paths:
        if os.path.exists(path) or path == "ollama":
            return path
    return None


def check_ollama():
    """检查 Ollama 是否安装和运行"""
    ollama_path = get_ollama_path()
    if not ollama_path:
        return False
    
    try:
        result = subprocess.run(
            [ollama_path, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


def check_model(model_name="qwen3-vl:4b"):
    """检查模型是否已下载"""
    ollama_path = get_ollama_path()
    if not ollama_path:
        return False
    
    try:
        result = subprocess.run(
            [ollama_path, "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return model_name in result.stdout
    except:
        return False


def pull_model(model_name="qwen3-vl:4b"):
    """拉取模型"""
    ollama_path = get_ollama_path()
    if not ollama_path:
        return False
    
    try:
        print(f"正在下载模型 {model_name}，请耐心等待...")
        result = subprocess.run(
            [ollama_path, "pull", model_name],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0
    except:
        return False


def compress_image(image_path, max_size_mb=2):
    """
    压缩图片到指定大小以下（默认 2MB）
    返回压缩后的图片路径（可能是临时文件）
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    
    # 检查原始文件大小
    original_size = os.path.getsize(image_path)
    if original_size <= max_size_bytes:
        return image_path, False  # 无需压缩
    
    print(f"图片大小 {original_size / 1024 / 1024:.2f}MB，超过 {max_size_mb}MB，正在压缩...")
    
    try:
        from PIL import Image
        
        # 打开图片
        img = Image.open(image_path)
        
        # 转换为 RGB（处理 PNG 透明通道等问题）
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # 获取原始尺寸
        width, height = img.size
        
        # 创建临时文件
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"compressed_{os.path.basename(image_path)}")
        
        # 尝试不同的压缩策略
        # 策略1：降低质量
        quality = 95
        while quality >= 30:
            img.save(temp_path, 'JPEG', quality=quality, optimize=True)
            if os.path.getsize(temp_path) <= max_size_bytes:
                compressed_size = os.path.getsize(temp_path)
                print(f"压缩完成：{original_size / 1024 / 1024:.2f}MB → {compressed_size / 1024 / 1024:.2f}MB (质量: {quality}%)")
                return temp_path, True
            quality -= 10
        
        # 策略2：如果质量降低还不够，缩小尺寸
        scale = 0.9
        while scale > 0.3:
            new_width = int(width * scale)
            new_height = int(height * scale)
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            resized_img.save(temp_path, 'JPEG', quality=85, optimize=True)
            
            if os.path.getsize(temp_path) <= max_size_bytes:
                compressed_size = os.path.getsize(temp_path)
                print(f"压缩完成：{original_size / 1024 / 1024:.2f}MB → {compressed_size / 1024 / 1024:.2f}MB (尺寸: {scale*100:.0f}%)")
                return temp_path, True
            
            scale -= 0.1
        
        # 如果还是太大，返回压缩后的版本（可能超过2MB但已经尽力了）
        print(f"警告：无法压缩到 {max_size_mb}MB 以下，使用最佳压缩版本")
        return temp_path, True
        
    except ImportError:
        print("警告：未安装 Pillow，无法进行图片压缩")
        return image_path, False
    except Exception as e:
        print(f"警告：图片压缩失败: {e}")
        return image_path, False


def encode_image(image_path):
    """将图片编码为 base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_image_api(image_path, mode="describe", custom_prompt=None):
    """
    使用 Ollama API 分析图片（支持视觉模型）
    自动压缩超过 2MB 的图片
    
    参数:
        image_path: 图片文件路径
        mode: 分析模式 (describe/ocr/extract)
        custom_prompt: 自定义提示词（仅 extract 模式）
    
    返回:
        分析结果文本
    """
    temp_file = None
    
    try:
        # 检查图片是否存在
        if not os.path.exists(image_path):
            return f"错误：图片不存在 - {image_path}"
        
        # 检查图片格式
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
        ext = os.path.splitext(image_path)[1].lower()
        if ext not in valid_extensions:
            return f"错误：不支持的图片格式 {ext}，支持的格式：{', '.join(valid_extensions)}"
        
        # 检查并压缩图片（如果超过 2MB）
        processed_path, was_compressed = compress_image(image_path, max_size_mb=2)
        if was_compressed:
            temp_file = processed_path
        
        # 检查 Ollama 运行状态
        if not check_ollama():
            return "错误：Ollama 未运行。请启动 Ollama 应用程序。"
        
        # 检查模型
        model_name = "qwen3-vl:4b"
        if not check_model(model_name):
            if not pull_model(model_name):
                return f"错误：无法下载模型 {model_name}，请检查网络连接"
        
        # 根据模式构建提示词
        prompts = {
            "describe": "请详细描述这张图片的内容，包括：\n1. 图片中的主要物体和场景\n2. 图片中的文字内容（如有）\n3. 整体氛围和风格",
            "ocr": "请提取这张图片中的所有文字内容，保持原有排版格式输出。如果图片中没有文字，请说明。",
            "extract": custom_prompt or "请分析这张图片并提取关键信息。"
        }
        
        prompt = prompts.get(mode, prompts["describe"])
        
        # 读取并编码图片
        image_base64 = encode_image(processed_path)
        
        # 构建 API 请求
        api_url = "http://localhost:11434/api/generate"
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False
        }
        
        # 发送请求
        response = requests.post(api_url, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            output = result.get("response", "").strip()
            if not output:
                return "分析完成，但返回结果为空。请检查图片是否有效。"
            return output
        else:
            return f"API 请求失败：HTTP {response.status_code} - {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "错误：无法连接到 Ollama API。请确保 Ollama 已启动并允许 API 访问。"
    except requests.exceptions.Timeout:
        return "错误：分析超时（超过2分钟）。图片可能过大或模型运行缓慢。"
    except Exception as e:
        return f"发生错误：{str(e)}"
    
    finally:
        # 清理临时文件
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python analyze_image.py <图片路径> [mode] [prompt]")
        print("  mode: describe | ocr | extract")
        print("  示例：python analyze_image.py C:\\path\\to\\image.jpg ocr")
        sys.exit(1)
    
    image_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "describe"
    custom_prompt = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = analyze_image_api(image_path, mode, custom_prompt)
    print(result)


if __name__ == "__main__":
    main()
