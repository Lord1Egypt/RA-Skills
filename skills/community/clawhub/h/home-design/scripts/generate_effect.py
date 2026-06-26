#!/usr/bin/env python3
"""
房间效果图生成器
支持多种 AI 图像生成后端：Stable Diffusion WebUI API, DALL-E 3, 在线服务等
"""

import argparse
import json
import requests
import base64
from pathlib import Path
from datetime import datetime


def generate_with_sd_webui(prompt: str, negative_prompt: str, 
                           width: int = 1024, height: int = 768,
                           steps: int = 30, cfg_scale: float = 7,
                           sd_url: str = "http://127.0.0.1:7860") -> dict:
    """使用 Stable Diffusion WebUI API 生成图像"""
    
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 1,
        "n_iter": 1,
        "seed": -1,
        "override_settings": {"sd_model_checkpoint": "realisticVisionV60B1_v51VAE"}
    }
    
    try:
        response = requests.post(f"{sd_url}/sdapi/v1/txt2img", json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        
        if "images" in result and len(result["images"]) > 0:
            return {
                "success": True,
                "image_base64": result["images"][0],
                "parameters": result.get("parameters", {})
            }
        else:
            return {"success": False, "error": "No images generated"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_with_dalle3(prompt: str, api_key: str, 
                         size: str = "1024x768", quality: str = "standard") -> dict:
    """使用 DALL-E 3 API 生成图像"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "response_format": "url"
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        
        if "data" in result and len(result["data"]) > 0:
            return {
                "success": True,
                "image_url": result["data"][0]["url"],
                "revised_prompt": result["data"][0].get("revised_prompt", "")
            }
        else:
            return {"success": False, "error": "No images generated"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_with_liblib(prompt: str, negative_prompt: str,
                         api_key: str, model_id: str = "") -> dict:
    """使用 LiblibAI (哩布哩布) API 生成图像"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": 1024,
        "height": 768,
        "steps": 30,
        "cfg_scale": 7,
        "seed": -1,
        "model_id": model_id or "auto"
    }
    
    try:
        response = requests.post(
            "https://api.liblib.ai/v1/generate",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        
        if result.get("success"):
            return {
                "success": True,
                "image_url": result.get("image_url"),
                "task_id": result.get("task_id")
            }
        else:
            return {"success": False, "error": result.get("message", "Unknown error")}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def save_image_from_base64(base64_data: str, output_path: str):
    """保存 base64 图像数据到文件"""
    try:
        # 移除可能的前缀
        if "," in base64_data:
            base64_data = base64_data.split(",")[1]
        
        image_data = base64.b64decode(base64_data)
        Path(output_path).write_bytes(image_data)
        return True
    except Exception as e:
        print(f"保存图像失败：{e}")
        return False


def download_image(url: str, output_path: str) -> bool:
    """下载图像到文件"""
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        Path(output_path).write_bytes(response.content)
        return True
    except Exception as e:
        print(f"下载图像失败：{e}")
        return False


def generate_room_effect(room: str, prompt_data: dict, backend: str = "sd_webui",
                        api_config: dict = None, output_dir: str = "./effects") -> dict:
    """生成单个房间的效果图"""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{room}_{timestamp}.png"
    filepath = output_path / filename
    
    result = {
        "room": room,
        "style": prompt_data.get("style", ""),
        "success": False,
        "filepath": str(filepath)
    }
    
    prompt = prompt_data["positive_prompt"]
    negative = prompt_data.get("negative_prompt", "")
    
    if backend == "sd_webui":
        config = api_config or {}
        sd_response = generate_with_sd_webui(
            prompt=prompt,
            negative_prompt=negative,
            width=prompt_data["parameters"]["width"],
            height=prompt_data["parameters"]["height"],
            steps=prompt_data["parameters"]["steps"],
            cfg_scale=prompt_data["parameters"]["cfg_scale"],
            sd_url=config.get("url", "http://127.0.0.1:7860")
        )
        
        if sd_response["success"]:
            if save_image_from_base64(sd_response["image_base64"], str(filepath)):
                result["success"] = True
                result["message"] = "生成成功"
            else:
                result["error"] = "保存图像失败"
        else:
            result["error"] = sd_response.get("error", "生成失败")
    
    elif backend == "dalle3":
        config = api_config or {}
        dalle_response = generate_with_dalle3(
            prompt=prompt,
            api_key=config.get("api_key", ""),
            size="1024x768"
        )
        
        if dalle_response["success"]:
            if download_image(dalle_response["image_url"], str(filepath)):
                result["success"] = True
                result["message"] = "生成成功"
                result["image_url"] = dalle_response["image_url"]
            else:
                result["error"] = "保存图像失败"
        else:
            result["error"] = dalle_response.get("error", "生成失败")
    
    elif backend == "liblib":
        config = api_config or {}
        liblib_response = generate_with_liblib(
            prompt=prompt,
            negative_prompt=negative,
            api_key=config.get("api_key", ""),
            model_id=config.get("model_id", "")
        )
        
        if liblib_response["success"]:
            # Liblib 可能需要轮询任务状态
            result["success"] = True
            result["message"] = "任务已提交"
            result["image_url"] = liblib_response.get("image_url")
            result["task_id"] = liblib_response.get("task_id")
        else:
            result["error"] = liblib_response.get("error", "生成失败")
    
    else:
        result["error"] = f"不支持的后端：{backend}"
    
    return result


def main():
    parser = argparse.ArgumentParser(description='生成房间效果图')
    parser.add_argument('--prompts', required=True, help='提示词 JSON 文件路径')
    parser.add_argument('--output', required=True, help='输出目录')
    parser.add_argument('--backend', default='sd_webui', 
                       choices=['sd_webui', 'dalle3', 'liblib'],
                       help='AI 后端')
    parser.add_argument('--config', help='API 配置文件路径 (JSON)')
    parser.add_argument('--rooms', nargs='+', help='要生成的房间列表')
    
    args = parser.parse_args()
    
    # 加载提示词
    prompts_path = Path(args.prompts)
    prompts = json.loads(prompts_path.read_text(encoding='utf-8'))
    
    # 加载 API 配置
    api_config = {}
    if args.config:
        config_path = Path(args.config)
        api_config = json.loads(config_path.read_text(encoding='utf-8'))
    
    # 筛选房间
    if args.rooms:
        prompts = {k: v for k, v in prompts.items() if k in args.rooms}
    
    # 生成效果图
    print(f"开始生成效果图，共 {len(prompts)} 个房间...")
    print(f"后端：{args.backend}")
    print(f"输出目录：{args.output}\n")
    
    results = []
    for room, prompt_data in prompts.items():
        print(f"正在生成：{room}...")
        result = generate_room_effect(
            room=room,
            prompt_data=prompt_data,
            backend=args.backend,
            api_config=api_config,
            output_dir=args.output
        )
        results.append(result)
        
        status = "✅ 成功" if result["success"] else f"❌ 失败：{result.get('error', '')}"
        print(f"  {room}: {status}")
    
    # 保存结果报告
    report_path = Path(args.output) / "generation_report.json"
    report_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"\n生成完成！报告已保存到：{report_path}")
    
    # 统计
    success_count = sum(1 for r in results if r["success"])
    print(f"成功：{success_count}/{len(results)}")


if __name__ == '__main__':
    main()
