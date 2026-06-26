#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
giggle.pro Generation API 封装脚本
支持文生图、图生图，多模型：seedream45, midjourney, nano-banana-2, nano-banana-2-fast
API: POST /api/v1/generation/text-to-image, POST /api/v1/generation/image-to-image, GET /api/v1/generation/task/query
"""

import base64
import os
import re
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

class AspectRatio(str, Enum):
    """图像比例枚举"""
    RATIO_1_1 = "1:1"
    RATIO_3_4 = "3:4"
    RATIO_4_3 = "4:3"
    RATIO_16_9 = "16:9"
    RATIO_9_16 = "9:16"
    RATIO_2_3 = "2:3"
    RATIO_3_2 = "3:2"
    RATIO_21_9 = "21:9"


class TaskStatus(str, Enum):
    """任务状态枚举"""
    COMPLETED = "completed"
    FAILED = "failed"
    PROCESSING = "processing"
    PENDING = "pending"


SUPPORTED_MODELS = ("seedream45", "midjourney", "nano-banana-2", "nano-banana-2-fast")


def to_view_url(url: str) -> str:
    """将下载 URL 转换为在线查看 URL"""
    url = url.replace("&response-content-disposition=attachment", "")
    url = url.replace("?response-content-disposition=attachment&", "?")
    url = url.replace("?response-content-disposition=attachment", "")
    url = url.replace("~", "%7E")
    return url


def download_images(image_urls: List[str], output_dir: str) -> List[str]:
    """下载图像到本地"""
    download_path = Path(output_dir).expanduser()
    download_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    downloaded_files = []
    for i, url in enumerate(image_urls, 1):
        try:
            ext = "png"
            if ".jpg" in url or ".jpeg" in url:
                ext = "jpg"
            elif ".webp" in url:
                ext = "webp"
            filename = f"generation_{timestamp}_{i}.{ext}" if len(image_urls) > 1 else f"generation_{timestamp}.{ext}"
            filepath = download_path / filename
            print(f"下载图像 {i}/{len(image_urls)}...", file=sys.stderr)
            headers = {"User-Agent": "Mozilla/5.0", "Referer": url}
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(response.content)
            downloaded_files.append(str(filepath))
            print(f"✓ 图像已下载: {filepath}", file=sys.stderr)
        except Exception as e:
            print(f"✗ 下载失败 (图像 {i}): {e}", file=sys.stderr)
    return downloaded_files


def _parse_reference_image(s: str) -> Dict[str, str]:
    """
    将字符串解析为 reference_images 单元素格式。
    支持：URL、base64、asset_id（自动识别）
    """
    s = s.strip()
    if not s:
        raise ValueError("参考图不能为空")
    if s.startswith(("http://", "https://")):
        return {"url": s}
    if re.match(r"^data:image/[^;]+;base64,", s):
        raise ValueError(
            "参考图包含 data:image/xxx;base64, 前缀，"
            "请直接传递纯 Base64 编码字符串"
        )
    is_short_id = len(s) <= 32 and re.match(r"^[a-zA-Z0-9_-]+$", s)
    if is_short_id:
        return {"asset_id": s}
    try:
        decoded = base64.b64decode(s, validate=True)
        if len(decoded) < 8:
            raise ValueError("Base64 解码后数据过短，不是有效的图片")
    except Exception:
        raise ValueError("参考图不是有效的 Base64 编码")
    return {"base64": s}


class GenerationAPI:
    """giggle.pro Generation API 客户端"""

    BASE_URL = "https://giggle.pro"
    TEXT_TO_IMAGE = "/api/v1/generation/text-to-image"
    IMAGE_TO_IMAGE = "/api/v1/generation/image-to-image"
    QUERY_TASK = "/api/v1/generation/task/query"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "x-auth": api_key,
            "Content-Type": "application/json"
        }

    def text_to_image(
        self,
        prompt: str,
        model: str = "seedream45",
        generate_count: int = 1,
        aspect_ratio: str = "16:9",
        resolution: str = "2K"
    ) -> Dict[str, Any]:
        """文生图"""
        if model not in SUPPORTED_MODELS:
            raise ValueError(f"不支持的模型: {model}，支持: {', '.join(SUPPORTED_MODELS)}")
        payload = {
            "prompt": prompt,
            "generate_count": generate_count,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution
        }
        return self._post(self.TEXT_TO_IMAGE, payload)

    def image_to_image(
        self,
        prompt: str,
        reference_images: List[str],
        model: str = "nano-banana-2-fast",
        generate_count: int = 1,
        aspect_ratio: str = "16:9",
        watermark: bool = False
    ) -> Dict[str, Any]:
        """图生图，支持 URL、base64、asset_id 三种参考图格式"""
        if model not in SUPPORTED_MODELS:
            raise ValueError(f"不支持的模型: {model}，支持: {', '.join(SUPPORTED_MODELS)}")
        refs = []
        for u in reference_images:
            refs.append(_parse_reference_image(u))
        if not refs:
            raise ValueError("图生图需要至少一张参考图（URL、base64 或 asset_id）")
        payload = {
            "prompt": prompt,
            "reference_images": refs,
            "generate_count": generate_count,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "watermark": watermark
        }
        return self._post(self.IMAGE_TO_IMAGE, payload)

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{path}"
        try:
            resp = requests.post(url, headers=self.headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            if result.get("code") != 200:
                raise Exception(result.get("msg", result.get("message", "未知错误")))
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {str(e)}")

    def query_task(self, task_id: str) -> Dict[str, Any]:
        """查询任务状态"""
        url = f"{self.BASE_URL}{self.QUERY_TASK}"
        try:
            resp = requests.get(url, headers=self.headers, params={"task_id": task_id}, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            if result.get("code") != 200:
                raise Exception(result.get("msg", result.get("message", "未知错误")))
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"查询失败: {str(e)}")

    def extract_image_urls(self, task_result: Dict[str, Any]) -> List[str]:
        """从任务结果中提取图像 URL"""
        return task_result.get("data", {}).get("urls", [])


def parse_args():
    parser = argparse.ArgumentParser(
        description='giggle.pro Generation API - 多模型 AI 图像生成',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 文生图
  python generation_api.py --prompt "一只可爱的橘猫" --model midjourney --no-wait --json

  # 图生图（URL / base64 / asset_id）
  python generation_api.py --prompt "转为油画风格" --reference-images "https://example.com/photo.jpg" --no-wait --json

  # 查询任务
  python generation_api.py --query --task-id xxx
        """
    )
    parser.add_argument('--query', action='store_true', help='查询任务')
    parser.add_argument('--prompt', type=str, help='图像描述')
    parser.add_argument('--task-id', type=str, help='任务 ID')
    parser.add_argument('--reference-images', type=str, nargs='+',
                        help='参考图列表，支持 URL、base64 字符串、asset_id')
    parser.add_argument('--generate-count', type=int, default=1, help='生成数量')
    parser.add_argument('--model', type=str, default='seedream45',
                        choices=list(SUPPORTED_MODELS), help='模型')
    parser.add_argument('--aspect-ratio', type=str, default='16:9',
                        choices=['1:1', '3:4', '4:3', '16:9', '9:16', '2:3', '3:2', '21:9'])
    parser.add_argument('--resolution', type=str, default='2K', choices=['1K', '2K', '4K'])
    parser.add_argument('--watermark', action='store_true', help='添加水印')
    parser.add_argument('--download', action='store_true', help='下载到本地')
    parser.add_argument('--output-dir', type=str, default='~/Downloads')
    parser.add_argument('--no-wait', action='store_true', help='异步提交（默认）')
    parser.add_argument('--json', action='store_true', help='JSON 输出')
    return parser.parse_args()


def main():
    args = parse_args()

    api_key = os.getenv("GIGGLE_API_KEY")
    if not api_key:
        print("错误: 未找到 GIGGLE_API_KEY，请设置系统环境变量：", file=sys.stderr)
        print("  export GIGGLE_API_KEY=your_api_key", file=sys.stderr)
        print("  API Key 可在 https://giggle.pro/ 账号设置中获取。", file=sys.stderr)
        sys.exit(1)

    client = GenerationAPI(api_key)

    try:
        if args.query:
            if not args.task_id:
                print("错误: --query 需提供 --task-id", file=sys.stderr)
                sys.exit(1)

            try:
                result = client.query_task(args.task_id)
            except Exception as e:
                print(json.dumps({"status": "network_error", "task_id": args.task_id}, ensure_ascii=False))
                print(f"网络异常: {e}", file=sys.stderr)
                sys.exit(0)

            data = result.get("data", {})
            status = data.get("status", "")

            if status == TaskStatus.COMPLETED.value:
                image_urls = client.extract_image_urls(result)
                if not image_urls:
                    print("生成遇到了问题\n\n创作虽已完成但未返回图片。\n\n建议重新生成，我随时待命~")
                    sys.exit(0)
                view_urls = [to_view_url(u) for u in image_urls]
                n = len(view_urls)
                lines = [f"[查看图片 {i+1}]({u})" for i, u in enumerate(view_urls)]
                print("图片已就绪！✨\n")
                print(f"创作已完成" + (f"，共 {n} 张" if n > 1 else "") + " ✨\n")
                print("\n".join(lines))
                print("\n如需调整，随时告诉我~")
                sys.exit(0)
            elif status in ("failed", "error"):
                err_msg = data.get("err_msg", "未知错误")
                if "sensitive" in str(err_msg).lower():
                    err_msg = "输入内容可能包含敏感信息，被服务端拦截"
                print(f"生成遇到了问题\n\n创作未能完成：{err_msg}\n\n建议调整描述后重新尝试，我随时待命~")
                sys.exit(0)
            else:
                print(json.dumps({"status": status, "task_id": args.task_id}, ensure_ascii=False))
                sys.exit(0)

        # 生成模式
        if not args.prompt:
            print("错误: 需要 --prompt", file=sys.stderr)
            sys.exit(1)

        print("创建图像生成任务...", file=sys.stderr)
        if args.reference_images and len(args.reference_images) > 0:
            result = client.image_to_image(
                prompt=args.prompt,
                reference_images=args.reference_images,
                model=args.model,
                generate_count=args.generate_count,
                aspect_ratio=args.aspect_ratio,
                watermark=args.watermark
            )
            print("模式: 图生图", file=sys.stderr)
        else:
            result = client.text_to_image(
                prompt=args.prompt,
                model=args.model,
                generate_count=args.generate_count,
                aspect_ratio=args.aspect_ratio,
                resolution=args.resolution
            )
            print("模式: 文生图", file=sys.stderr)

        task_id = result.get("data", {}).get("task_id")
        print(f"✓ 任务创建成功! TaskID: {task_id}", file=sys.stderr)
        print(json.dumps({"status": "started", "task_id": task_id}, ensure_ascii=False))

    except Exception as e:
        print(f"✗ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
