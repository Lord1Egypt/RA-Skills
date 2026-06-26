#!/usr/bin/env python3
"""
pic-gen: 通义万相图片生成器
调用 DashScope API 生成图片
"""

import argparse
import os
import sys
import json
import time
import yaml
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config", "models.yaml")


def load_config() -> dict:
    """加载配置文件"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def get_api_key(config: dict) -> str:
    """获取 API Key"""
    api_key = config.get("models", {}).get("qwen", {}).get("api_key", "")
    if not api_key:
        api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    return api_key


def generate_image(prompt: str, api_key: str = None,
                    size: str = "1024*1024", count: int = 1,
                    negative_prompt: str = "",
                    download: bool = False, output: str = ".",
                    wait: bool = True) -> dict:
    """
    调用通义万相生成图片

    Args:
        prompt: 提示词
        api_key: DashScope API Key
        size: 图片尺寸，如 "1024*1024"
        count: 生成数量（1-4）
        negative_prompt: 负面提示词
        download: 是否下载图片
        output: 下载目录
        wait: 是否等待完成

    Returns:
        dict: 结果，包含 task_id 和图片 URL
    """
    if not api_key:
        return {"error": "API Key 未设置，请在 config/models.yaml 中配置 qwen.api_key"}

    url = "https://dashscope.aliyuncs.com/api/v1/services/a2xt2g4x/draw/image-synthesis"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 尺寸映射
    size_map = {
        "1024*1024": [1024, 1024],
        "1024*768": [1024, 768],
        "768*1024": [768, 1024],
        "1280*720": [1280, 720],
        "720*1280": [720, 1280],
    }
    wh = size_map.get(size, [1024, 1024])

    payload = {
        "model": "qwen-image-2.0-pro",
        "input": {
            "prompt": prompt,
            "negative_prompt": negative_prompt
        },
        "parameters": {
            "size": f"{wh[0]}*{wh[1]}",
            "n": count
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        resp_json = response.json()

        if response.status_code != 200:
            return {"error": f"请求失败 ({response.status_code}): {resp_json}"}

        # 解析任务 ID
        task_id = None
        if "output" in resp_json and "task_id" in resp_json["output"]:
            task_id = resp_json["output"]["task_id"]
        elif "request_id" in resp_json:
            task_id = resp_json["request_id"]

        if not task_id:
            return {"error": f"无法获取 task_id: {resp_json}"}

        result = {"task_id": task_id, "status": "submitted"}

        if wait:
            # 轮询等待完成
            result = wait_for_completion(task_id, api_key, download, output)

        return result

    except requests.exceptions.Timeout:
        return {"error": "请求超时，请检查网络或稍后重试"}
    except Exception as e:
        return {"error": f"生成失败: {str(e)}"}


def wait_for_completion(task_id: str, api_key: str, download: bool, output: str, max_wait: int = 120) -> dict:
    """轮询等待图片生成完成"""
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()

            if resp.status_code != 200:
                return {"error": f"查询失败: {data}"}

            status = data.get("output", {}).get("task_status", "UNKNOWN")

            if status == "succeeded":
                images = data.get("output", {}).get("results", [])
                urls = [item.get("url") or item.get("image_url") for item in images if item]
                result = {"status": "succeeded", "images": urls, "task_id": task_id}

                if download and urls:
                    result["files"] = download_images(urls, output)

                return result

            elif status == "failed":
                return {"status": "failed", "error": "图片生成失败", "detail": data}

            elif status in ("pending", "running", "wait"):
                time.sleep(3)

            else:
                return {"status": status, "raw": data}

        except Exception as e:
            return {"error": f"查询失败: {str(e)}"}

    return {"status": "timeout", "error": "等待超时，请稍后用 task_id 查询"}


def download_images(urls: list, output_dir: str) -> list:
    """下载图片到本地"""
    os.makedirs(output_dir, exist_ok=True)
    files = []

    for i, url in enumerate(urls):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                ext = "png"  # 通义万相返回 PNG
                filepath = os.path.join(output_dir, f"pic_gen_{int(time.time())}_{i+1}.{ext}")
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                files.append(filepath)
        except Exception as e:
            files.append({"index": i, "error": str(e)})

    return files


def main():
    parser = argparse.ArgumentParser(description="pic-gen 通义万相图片生成")
    parser.add_argument("--prompt", "-p", required=True, help="图片提示词")
    parser.add_argument("--size", "-s", default="1024*1024",
                        help="图片尺寸，默认 1024*1024")
    parser.add_argument("--count", "-c", type=int, default=1,
                        help="生成数量（1-4）")
    parser.add_argument("--negative-prompt", "-n", default="",
                        help="负面提示词")
    parser.add_argument("--download", "-d", action="store_true",
                        help="生成后下载图片")
    parser.add_argument("--output", "-o", default="./output",
                        help="下载目录")
    parser.add_argument("--wait", "-w", action="store_true", default=True,
                        help="等待生成完成")
    parser.add_argument("--no-wait", action="store_true",
                        help="不等待，立即返回 task_id")
    parser.add_argument("--api-key", "-k", help="API Key（也可在 config 中设置）")
    args = parser.parse_args()

    config = load_config()
    api_key = args.api_key or get_api_key(config)

    if args.no_wait:
        args.wait = False

    result = generate_image(
        prompt=args.prompt,
        api_key=api_key,
        size=args.size,
        count=args.count,
        negative_prompt=args.negative_prompt,
        download=args.download,
        output=args.output,
        wait=args.wait
    )

    if "error" in result:
        print(f"❌ 错误: {result['error']}", file=sys.stderr)
        sys.exit(1)
    elif result.get("status") == "succeeded":
        for url in result.get("images", []):
            print(f"✅ 图片生成成功: {url}")
        for f in result.get("files", []):
            if isinstance(f, str):
                print(f"📁 已保存: {f}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
