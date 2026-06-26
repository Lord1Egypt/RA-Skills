#!/usr/bin/env python3
"""
MiniMax Image Generation Script
支持 image-01 和 image-01-live 模型
"""

import argparse
import json
import os
import sys
import time
import requests


BASE_URL = "https://api.minimaxi.com"

# 支持的模型
MODELS = {
    "image-01": {
        "name": "image-01",
        "description": "画面表现细腻，支持文生图、图生图",
        "supports_aspect_ratios": ["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"],
        "supports_custom_size": True,
        "supports_style": False,
    },
    "image-01-live": {
        "name": "image-01-live",
        "description": "手绘、卡通等画风增强，支持文生图并进行画风设置",
        "supports_aspect_ratios": ["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16"],
        "supports_custom_size": False,
        "supports_style": True,
    },
}

# 支持的画风 (仅 image-01-live)
STYLES = [
    "realistic", "animation", "comic", "watercolor", 
    "oil_painting", "sketch", "cartoon", "hand_drawn"
]

# 支持的比例
ASPECT_RATIOS = ["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"]


def get_models():
    """返回支持的模型列表"""
    return MODELS


def list_models():
    """列出所有可用模型"""
    print("\n📋 支持的模型:")
    print("-" * 80)
    print(f"{'模型':<20} {'说明':<40} {'支持比例':<20}")
    print("-" * 80)
    for model_id, info in MODELS.items():
        ratios = ", ".join(info["supports_aspect_ratios"][:3]) + "..."
        print(f"{model_id:<20} {info['description']:<40} {ratios:<20}")
    print("-" * 80)


def generate_image(
    api_key: str,
    model: str,
    prompt: str,
    aspect_ratio: str = "1:1",
    width: int = None,
    height: int = None,
    n: int = 1,
    seed: int = None,
    prompt_optimizer: bool = False,
    aigc_watermark: bool = False,
    response_format: str = "url",
    input_image: str = None,
    style: str = None,
) -> dict:
    """
    生成图片
    
    Args:
        api_key: API Key
        model: 模型名称
        prompt: 图像描述
        aspect_ratio: 宽高比
        width: 自定义宽度 (仅 image-01)
        height: 自定义高度 (仅 image-01)
        n: 生成数量
        seed: 随机种子
        prompt_optimizer: 是否开启 prompt 自动优化
        aigc_watermark: 是否添加水印
        response_format: 返回格式 (url/base64)
        input_image: 输入图片 (图生图)
        style: 画风 (仅 image-01-live)
    
    Returns:
        dict: 包含图片URL的结果
    """
    if model not in MODELS:
        raise ValueError(f"不支持的模型: {model}")
    
    model_info = MODELS[model]
    
    # 验证比例
    if aspect_ratio not in model_info["supports_aspect_ratios"]:
        raise ValueError(
            f"模型 {model} 不支持比例 {aspect_ratio}。"
            f"支持的比例: {', '.join(model_info['supports_aspect_ratios'])}"
        )
    
    # 验证自定义尺寸
    if width or height:
        if not model_info["supports_custom_size"]:
            raise ValueError(f"模型 {model} 不支持自定义尺寸")
        if width and not (512 <= width <= 2048 and width % 8 == 0):
            raise ValueError("宽度必须在 512-2048 范围内，且是 8 的倍数")
        if height and not (512 <= height <= 2048 and height % 8 == 0):
            raise ValueError("高度必须在 512-2048 范围内，且是 8 的倍数")
        if (width and not height) or (height and not width):
            raise ValueError("宽度和高度必须同时设置")
    
    # 验证画风
    if style and not model_info["supports_style"]:
        raise ValueError(f"模型 {model} 不支持画风设置")
    if style and style not in STYLES:
        raise ValueError(f"不支持的画风: {style}。可用画风: {', '.join(STYLES)}")
    
    # 验证数量
    if not 1 <= n <= 9:
        raise ValueError("生成数量必须在 1-9 范围内")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # 构建请求体
    data = {
        "model": model,
        "prompt": prompt,
        "n": n,
        "response_format": response_format,
        "prompt_optimizer": prompt_optimizer,
    }
    
    # 添加比例或自定义尺寸
    if width and height:
        data["width"] = width
        data["height"] = height
    else:
        data["aspect_ratio"] = aspect_ratio
    
    # 添加可选参数
    if seed:
        data["seed"] = seed
    
    if aigc_watermark:
        data["aigc_watermark"] = aigc_watermark
    
    # 图生图模式
    if input_image:
        # 注意: MiniMax 图生图需要使用不同的 API 端点
        # 这里使用 image_01 的图生图能力
        data["image_url"] = input_image
    
    # 添加画风 (仅 image-01-live)
    # 注意: style 参数可能需要特定格式，目前 image-01-live 不带 style 也可生成
    if style and model_info["supports_style"]:
        print(f"   ⚠️ 警告: style 参数当前可能不稳定")
    
    print(f"\n🎨 正在生成图片...")
    print(f"   模型: {model}")
    print(f"   描述: {prompt[:50]}...")
    print(f"   比例: {aspect_ratio}")
    print(f"   数量: {n}")
    
    # 调用 API (文生图)
    if not input_image:
        response = requests.post(
            f"{BASE_URL}/v1/image_generation",
            headers=headers,
            json=data,
            timeout=60
        )
    else:
        # 图生图使用不同的端点
        response = requests.post(
            f"{BASE_URL}/v1/image_generation",
            headers=headers,
            json=data,
            timeout=60
        )
    
    if response.status_code != 200:
        error_msg = response.text
        try:
            error_data = response.json()
            if "base_resp" in error_data:
                error_msg = error_data["base_resp"].get("status_msg", error_msg)
        except:
            pass
        raise RuntimeError(f"API 调用失败: {error_msg}")
    
    result = response.json()
    
    # 检查返回结果
    if result.get("base_resp", {}).get("status_code") != 0:
        raise RuntimeError(f"生成失败: {result.get('base_resp', {}).get('status_msg', '未知错误')}")
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="MiniMax Image Generation - AI图片生成工具"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        default=os.environ.get("MINIMAX_API_KEY"),
        help="MiniMax API Key (或设置环境变量 MINIMAX_API_KEY)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="image-01",
        choices=list(MODELS.keys()),
        help="模型名称 (默认: image-01)"
    )
    
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="图像描述 (必填, 除 --list-models 外)"
    )
    
    parser.add_argument(
        "--aspect-ratio",
        type=str,
        default="1:1",
        choices=ASPECT_RATIOS,
        help="宽高比 (默认: 1:1)"
    )
    
    parser.add_argument(
        "--width",
        type=int,
        help="自定义宽度 (仅 image-01, 512-2048, 必须是 8 的倍数)"
    )
    
    parser.add_argument(
        "--height",
        type=int,
        help="自定义高度 (仅 image-01, 512-2048, 必须是 8 的倍数)"
    )
    
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="生成数量 1-9 (默认: 1)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        help="随机种子 (用于复现结果)"
    )
    
    parser.add_argument(
        "--prompt-optimizer",
        action="store_true",
        help="开启 prompt 自动优化"
    )
    
    parser.add_argument(
        "--aigc-watermark",
        action="store_true",
        help="添加水印"
    )
    
    parser.add_argument(
        "--response-format",
        type=str,
        default="url",
        choices=["url", "base64"],
        help="返回格式 (默认: url)"
    )
    
    parser.add_argument(
        "--input-image",
        type=str,
        help="输入图片 URL (图生图模式)"
    )
    
    parser.add_argument(
        "--style",
        type=str,
        choices=STYLES,
        help="画风 (仅 image-01-live)"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="列出所有可用模型"
    )
    
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="JSON 格式输出结果"
    )
    
    args = parser.parse_args()
    
    # 列出模型
    if args.list_models:
        list_models()
        return
    
    # 检查 API Key
    if not args.api_key:
        print("❌ 错误: 请提供 API Key")
        print("   使用 --api-key 参数或设置环境变量 MINIMAX_API_KEY")
        sys.exit(1)
    
    # 检查 prompt (除非是列出模型)
    if not args.prompt:
        print("❌ 错误: 请提供 --prompt 参数")
        sys.exit(1)
    
    try:
        result = generate_image(
            api_key=args.api_key,
            model=args.model,
            prompt=args.prompt,
            aspect_ratio=args.aspect_ratio,
            width=args.width,
            height=args.height,
            n=args.n,
            seed=args.seed,
            prompt_optimizer=args.prompt_optimizer,
            aigc_watermark=args.aigc_watermark,
            response_format=args.response_format,
            input_image=args.input_image,
            style=args.style,
        )
        
        # 提取图片 URL
        image_urls = result.get("data", {}).get("image_urls", [])
        
        if args.output_json:
            print(json.dumps({
                "model": args.model,
                "urls": image_urls,
                "count": len(image_urls),
                "task_id": result.get("id"),
            }, indent=2, ensure_ascii=False))
        else:
            print("\n✅ 生成成功!")
            print(f"   数量: {len(image_urls)}")
            for i, url in enumerate(image_urls, 1):
                print(f"   [{i}] {url}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
