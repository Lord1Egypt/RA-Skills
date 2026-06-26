#!/usr/bin/env python3
"""
pic-gen: Banana (Flux) 图片生成器
"""

import argparse
import os
import sys
import json
import time
import yaml
import requests

try:
    import banana_dev as banana
    BANANA_SDK_AVAILABLE = True
except ImportError:
    BANANA_SDK_AVAILABLE = False
    banana = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config", "models.yaml")


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def get_api_key(config: dict) -> str:
    api_key = config.get("models", {}).get("banana", {}).get("api_key", "")
    if not api_key:
        api_key = os.environ.get("BANANA_API_KEY", "")
    return api_key


def generate_image(prompt: str, api_key: str = None, model_key: str = None,
                   size: str = "1024x1024", steps: int = 50, guidance: float = 3.5,
                   seed: int = -1, download: bool = False, output: str = ".") -> dict:
    """
    通过 Banana API 调用 Flux 模型生成图片
    """
    if not api_key:
        return {"error": "Banana API Key 未设置，请在 config/models.yaml 中配置 banana.api_key"}
    if not BANANA_SDK_AVAILABLE:
        return {"error": "banana-dev 未安装，请运行: pip install banana-dev"}
    if not model_key:
        return {"error": "Banana Model Key 未设置，请在 config/models.yaml 中配置 banana.model_key"}

    # 尺寸映射 (width x height)
    size_map = {
        "1024*1024": (1024, 1024),
        "1024*768": (1024, 768),
        "768*1024": (768, 1024),
        "1280*720": (1280, 720),
        "720*1280": (720, 1280),
    }
    w, h = size_map.get(size, (1024, 1024))

    payload = {
        "modelInputs": {
            "prompt": prompt,
            "num_inference_steps": steps,
            "guidance": guidance,
            "width": w,
            "height": h,
            "seed": seed
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    url = f"https://api.banana.dev/start/fetch/v4/{model_key}"

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        data = response.json()

        if response.status_code != 200:
            return {"error": f"请求失败 ({response.status_code}): {data}"}

        # Banana 返回 call_id 用于查询
        call_id = data.get("call_id", "")
        if not call_id:
            return {"error": f"无法获取 call_id: {data}"}

        result = {"call_id": call_id, "status": "submitted"}

        if download or True:  # 默认等待
            result = wait_for_completion(call_id, api_key, download, output)

        return result

    except Exception as e:
        return {"error": f"生成失败: {str(e)}"}


def wait_for_completion(call_id: str, api_key: str, download: bool, output: str,
                        max_wait: int = 180) -> dict:
    """轮询 Banana 查询结果"""
    if not BANANA_SDK_AVAILABLE:
        return {"error": "banana-dev 未安装，请运行: pip install banana-dev"}

    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            result = banana.check_model(api_key, call_id)
            outputs = result.get("modelOutputs", [])

            if outputs:
                output_data = outputs[0]
                if "images" in output_data:
                    urls = output_data["images"]
                    res = {"status": "succeeded", "images": urls, "call_id": call_id}
                    if download and urls:
                        res["files"] = download_images(urls, output)
                    return res
                elif "image" in output_data:
                    url = output_data["image"]
                    res = {"status": "succeeded", "images": [url], "call_id": call_id}
                    if download:
                        res["files"] = download_images([url], output)
                    return res

            # 检查是否还在运行
            state = result.get("state", "")
            if state in ["started", "running"]:
                time.sleep(10)
            else:
                return {"status": state, "raw": result}

        except Exception as e:
            return {"error": f"查询失败: {str(e)}"}

    return {"status": "timeout", "error": "等待超时"}


def download_images(urls: list, output_dir: str) -> list:
    os.makedirs(output_dir, exist_ok=True)
    files = []
    for i, url in enumerate(urls):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                ext = "png"
                filepath = os.path.join(output_dir, f"pic_gen_flux_{int(time.time())}_{i+1}.{ext}")
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                files.append(filepath)
        except Exception as e:
            files.append({"index": i, "error": str(e)})
    return files


def main():
    parser = argparse.ArgumentParser(description="pic-gen Banana/Flux 图片生成")
    parser.add_argument("--prompt", "-p", required=True, help="图片提示词")
    parser.add_argument("--model", default="flux-dev", help="Banana 模型名")
    parser.add_argument("--size", "-s", default="1024x1024", help="图片尺寸")
    parser.add_argument("--steps", type=int, default=50, help="推理步数")
    parser.add_argument("--guidance", type=float, default=3.5, help="引导强度")
    parser.add_argument("--seed", type=int, default=-1, help="随机种子（-1 为随机）")
    parser.add_argument("--download", "-d", action="store_true", help="下载图片")
    parser.add_argument("--output", "-o", default="./output", help="下载目录")
    parser.add_argument("--api-key", "-k", help="Banana API Key")
    parser.add_argument("--model-key", "-m", help="Banana Model Key")
    args = parser.parse_args()

    config = load_config()
    banana_cfg = config.get("models", {}).get("banana", {})

    api_key = args.api_key or get_api_key(config) or banana_cfg.get("api_key")
    model_key = (
        args.model_key
        or os.environ.get("BANANA_MODEL_KEY")
        or banana_cfg.get("model_key", "flux-dev")
    )

    result = generate_image(
        prompt=args.prompt,
        api_key=api_key,
        model_key=model_key,
        size=args.size.replace("*", "x"),
        steps=args.steps,
        guidance=args.guidance,
        seed=args.seed,
        download=args.download,
        output=args.output
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
