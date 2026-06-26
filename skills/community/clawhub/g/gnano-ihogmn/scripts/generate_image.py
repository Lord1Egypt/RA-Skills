#!/usr/bin/env python3
"""
GNano Ihogmn 图片生成脚本
支持动态模型选择和参数配置
"""

import argparse
import base64
import json
import sys
import os
import time
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import requests
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "未找到 requests 模块。请安装: pip install requests"
    }, ensure_ascii=False))
    sys.exit(1)


DEFAULT_API_URL = "https://gnano.ihogmn.top"

RESOLUTION_MAP = {
    "1K": (1024, 1024),
    "2K": (2048, 2048),
    "4K": (4096, 4096)
}

MODEL_PERFORMANCE = {
    "gemini-3.1-flash-image-preview": 100,
    "gemini-2.5-flash-image": 90,
    "gemini-3-pro-image-preview": 70
}


def log_progress(message: str, step: int = None, total: int = None):
    """输出进度信息"""
    progress_data = {
        "type": "progress",
        "message": message,
        "timestamp": time.time()
    }
    if step is not None:
        progress_data["step"] = step
    if total is not None:
        progress_data["total"] = total
    
    print(json.dumps(progress_data, ensure_ascii=False), file=sys.stderr, flush=True)


def convert_to_absolute_path(image_path: str) -> str:
    """将路径转换为绝对路径"""
    if not image_path:
        return ""
    
    image_path = image_path.strip().strip('"').strip("'")
    path = Path(image_path)
    
    if not path.is_absolute():
        path = Path.cwd() / path
    
    abs_path = path.resolve()
    abs_path_str = str(abs_path)
    if os.name == 'nt':
        abs_path_str = abs_path_str.replace('\\', '/')
    
    return abs_path_str


def encode_image(image_path: str, max_size_mb: int = 2) -> Tuple[Optional[str], Optional[str]]:
    """将图片转换为 base64 编码"""
    abs_path = convert_to_absolute_path(image_path)
    path = Path(abs_path)
    
    if not path.exists():
        return None, f"参考图不存在: {abs_path}"
    
    file_size = path.stat().st_size
    max_size = max_size_mb * 1024 * 1024
    if file_size > max_size:
        return None, f"参考图超过{max_size_mb}MB限制"
    
    suffix = path.suffix.lower()
    if suffix in ['.png']:
        mime_type = "image/png"
    elif suffix in ['.jpg', '.jpeg']:
        mime_type = "image/jpeg"
    elif suffix in ['.webp']:
        mime_type = "image/webp"
    elif suffix in ['.gif']:
        mime_type = "image/gif"
    else:
        mime_type = "image/png"
    
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return mime_type, data
    except Exception as e:
        return None, f"读取图片失败: {e}"


def build_api_url(api_url: str, model: str) -> str:
    """构建 API 请求 URL"""
    api_url = api_url.rstrip("/")
    return f"{api_url}/v1beta/models/{model}:generateContent"


def select_best_model(available_models: List[str], preferred_model: str = None) -> str:
    """选择最佳模型"""
    if preferred_model and preferred_model in available_models:
        return preferred_model
    
    scored_models = []
    for model in available_models:
        score = MODEL_PERFORMANCE.get(model, 50)
        scored_models.append((model, score))
    
    scored_models.sort(key=lambda x: x[1], reverse=True)
    return scored_models[0][0] if scored_models else "gemini-3.1-flash-image-preview"


def generate_image(
    token: str,
    prompt: str,
    api_url: str = None,
    model: str = None,
    available_models: List[str] = None,
    resolution: str = None,
    reference_paths: List[str] = None,
    output_path: str = None,
    max_reference_images: int = 2,
    max_reference_size_mb: int = 2,
    verbose: bool = False
) -> dict:
    """生成图片"""
    start_time = time.time()
    api_url = api_url or DEFAULT_API_URL
    
    if available_models:
        selected_model = select_best_model(available_models, model)
    else:
        selected_model = model or "gemini-3.1-flash-image-preview"
    
    log_progress(f"使用模型: {selected_model}", step=1, total=5)
    
    parts = [{"text": prompt}]
    
    loaded_references = []
    if reference_paths:
        log_progress(f"正在处理 {len(reference_paths)} 张参考图...", step=2, total=5)
        
        if len(reference_paths) > max_reference_images:
            log_progress(f"警告: 最多支持{max_reference_images}张参考图")
            reference_paths = reference_paths[:max_reference_images]
        
        for i, ref_path in enumerate(reference_paths, 1):
            abs_ref_path = convert_to_absolute_path(ref_path)
            mime_type, image_data = encode_image(abs_ref_path, max_reference_size_mb)
            
            if mime_type is None:
                log_progress(f"警告: 跳过参考图 {i}")
                continue
            
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_data
                }
            })
            loaded_references.append(abs_ref_path)
            log_progress(f"已加载参考图 {i}/{len(reference_paths)}")
    
    generation_config = {
        "responseModalities": ["Text", "Image"]
    }
    
    if resolution and resolution in RESOLUTION_MAP:
        width, height = RESOLUTION_MAP[resolution]
        generation_config["imageConfig"] = {
            "width": width,
            "height": height
        }
        log_progress(f"设置分辨率: {resolution}", step=3, total=5)
    
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": generation_config
    }
    
    url = build_api_url(api_url, selected_model)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    log_progress("正在生成图片，请稍候...", step=4, total=5)
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "请求超时，请稍后重试",
            "model": selected_model,
            "elapsed_time": time.time() - start_time
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"网络请求失败: {e}",
            "model": selected_model,
            "elapsed_time": time.time() - start_time
        }
    
    if response.status_code == 401:
        return {
            "success": False,
            "error": "API Token 无效或已过期",
            "model": selected_model,
            "elapsed_time": time.time() - start_time
        }
    elif response.status_code == 429:
        return {
            "success": False,
            "error": "请求过于频繁，请稍后再试",
            "model": selected_model,
            "elapsed_time": time.time() - start_time
        }
    elif response.status_code != 200:
        error_detail = ""
        try:
            error_json = response.json()
            if "error" in error_json:
                error_detail = error_json["error"].get("message", "")
        except:
            error_detail = response.text[:200]
        
        return {
            "success": False,
            "error": f"请求失败: {response.status_code}",
            "details": error_detail,
            "model": selected_model,
            "elapsed_time": time.time() - start_time
        }
    
    result = response.json()
    
    if "candidates" in result and len(result["candidates"]) > 0:
        candidate = result["candidates"][0]
        
        if "finishReason" in candidate:
            finish_reason = candidate["finishReason"]
            if finish_reason not in ["STOP", "MAX_TOKENS", "IMAGE"]:
                return {
                    "success": False,
                    "error": f"生成被中断: {finish_reason}",
                    "model": selected_model,
                    "elapsed_time": time.time() - start_time
                }
        
        if "content" in candidate and "parts" in candidate["content"]:
            for part in candidate["content"]["parts"]:
                if "inlineData" in part:
                    image_data = part["inlineData"]["data"]
                    mime_type = part["inlineData"].get("mimeType", "image/png")
                    
                    try:
                        image_bytes = base64.b64decode(image_data)
                    except Exception as e:
                        return {
                            "success": False,
                            "error": f"解码图片失败: {e}",
                            "model": selected_model,
                            "elapsed_time": time.time() - start_time
                        }
                    
                    if not output_path:
                        output_path = "generated_image.png"
                    
                    output_abs_path = convert_to_absolute_path(output_path)
                    
                    try:
                        output_dir = Path(output_abs_path).parent
                        if not output_dir.exists():
                            output_dir.mkdir(parents=True, exist_ok=True)
                        
                        with open(output_abs_path, "wb") as f:
                            f.write(image_bytes)
                        
                        elapsed = time.time() - start_time
                        log_progress(f"图片生成完成！耗时 {elapsed:.1f} 秒", step=5, total=5)
                        
                        return {
                            "success": True,
                            "output_path": output_abs_path,
                            "model": selected_model,
                            "mime_type": mime_type,
                            "file_size": len(image_bytes),
                            "file_size_mb": round(len(image_bytes) / 1024 / 1024, 2),
                            "references_used": len(loaded_references),
                            "elapsed_time": round(elapsed, 2)
                        }
                    except Exception as e:
                        return {
                            "success": False,
                            "error": f"保存图片失败: {e}",
                            "model": selected_model,
                            "elapsed_time": time.time() - start_time
                        }
                
                elif "text" in part:
                    text_content = part["text"]
                    log_progress(f"文本响应: {text_content}")
    
    return {
        "success": False,
        "error": "未找到生成的图片",
        "model": selected_model,
        "api_response": result,
        "elapsed_time": time.time() - start_time
    }


def main():
    parser = argparse.ArgumentParser(
        description="GNano Ihogmn 图片生成"
    )
    parser.add_argument("--token", "-t", required=True, help="API Token")
    parser.add_argument("--prompt", "-p", required=True, help="图片生成提示词")
    parser.add_argument("--api-url", "-u", default=DEFAULT_API_URL, help=f"API 地址")
    parser.add_argument("--model", "-m", help="模型名称")
    parser.add_argument("--available-models", help="可用模型列表，逗号分隔")
    parser.add_argument("--resolution", "-r", choices=["1K", "2K", "4K"], help="输出分辨率")
    parser.add_argument("--reference", "-ref", help="参考图路径，多个用逗号分隔")
    parser.add_argument("--output", "-o", default="generated_image.png", help="输出图片路径")
    parser.add_argument("--max-ref", type=int, default=2, help="最大参考图数量")
    parser.add_argument("--max-ref-size", type=int, default=2, help="参考图大小限制(MB)")
    parser.add_argument("--verbose", "-v", action="store_true", help="输出详细日志")
    
    args = parser.parse_args()
    
    reference_paths = None
    if args.reference:
        reference_paths = [p.strip() for p in args.reference.split(",") if p.strip()]
    
    available_models = None
    if args.available_models:
        available_models = [m.strip() for m in args.available_models.split(",") if m.strip()]
    
    result = generate_image(
        token=args.token,
        prompt=args.prompt,
        api_url=args.api_url,
        model=args.model,
        available_models=available_models,
        resolution=args.resolution,
        reference_paths=reference_paths,
        output_path=args.output,
        max_reference_images=args.max_ref,
        max_reference_size_mb=args.max_ref_size,
        verbose=args.verbose
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
