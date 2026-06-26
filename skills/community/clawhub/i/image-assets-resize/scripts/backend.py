#!/usr/bin/env python3
"""
Image generation backends for image-assets-resize.

Supports:
  - gpt-image-2 (via OpenAI-compatible /v1/images/*)
  - Nano Banana 2 / Pro (via OpenAI-compatible /v1/chat/completions)
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

from utils import encode_image_base64


# ── Config ──────────────────────────────────────────────────

CONFIG_DIR = Path.home() / ".content-marketing"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "backend": "gpt-image-2",
    "base_url": "https://api.openai.com/v1",
    "api_key_env": "OPENAI_API_KEY",
    "model": {
        "gpt-image-2": "gpt-image-2",
        "nano-banana-2": "gemini-3.1-flash-image-preview",
        "nano-banana-pro": "gemini-3-pro-image-preview",
    },
}

BACKEND_CHOICES = ["gpt-image-2", "nano-banana-2", "nano-banana-pro"]
BACKEND_LABELS = {
    "gpt-image-2": "GPT Image 2 (OpenAI)",
    "nano-banana-2": "Nano Banana 2 (Gemini 3.1 Flash Image)",
    "nano-banana-pro": "Nano Banana Pro (Gemini 3 Pro Image)",
}


def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return {}


def save_config(cfg: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def get_backend_name(config: dict) -> str:
    return config.get("backend", "gpt-image-2")


def get_model_name(config: dict) -> str:
    backend = get_backend_name(config)
    models = config.get("model", DEFAULT_CONFIG["model"])
    return models.get(backend, DEFAULT_CONFIG["model"].get(backend, backend))


def get_api_key(config: dict) -> str:
    # priority: config file key > env var > DEFAULT_CONFIG env
    if config.get("api_key"):
        return config["api_key"]
    env_name = config.get("api_key_env", "OPENAI_API_KEY")
    return os.environ.get(env_name, "")


def get_base_url(config: dict) -> str:
    return config.get("base_url", DEFAULT_CONFIG["base_url"]).rstrip("/")


# ── 尺寸工具（共享） ───────────────────────────────────────


MIN_GPT_PIXELS = 1_000_000


def calc_gpt_size(target_w: int, target_h: int) -> tuple[str, float]:
    """计算最接近目标尺寸的合法生成尺寸（16倍数 + ≥1MP）"""
    target_pixels = target_w * target_h

    if target_w % 16 == 0 and target_h % 16 == 0 and target_pixels >= MIN_GPT_PIXELS:
        return f"{target_w}x{target_h}", 1.0

    scale = max(1.0, (MIN_GPT_PIXELS / target_pixels) ** 0.5)
    w = round(target_w * scale / 16) * 16
    h = round(target_h * scale / 16) * 16

    for _ in range(20):
        if w * h >= MIN_GPT_PIXELS:
            break
        w += 16
        h = round(target_h * (w / target_w) / 16) * 16

    actual_scale = target_w / w
    return f"{w}x{h}", actual_scale


# ── 工具函数 ──────────────────────────────────────────────


def _parse_size(size_str: str) -> tuple[int, int]:
    parts = size_str.split("x")
    return int(parts[0]), int(parts[1])


# ── 后端抽象 ──────────────────────────────────────────────


class ImageBackend(ABC):
    """图片生成后端抽象"""

    config: dict

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def generate(self, prompt: str, output_path: str, size: str, quality: str, timeout: int) -> dict:
        ...

    @abstractmethod
    def edit(self, image_path: str, prompt: str, output_path: str, size: str, quality: str, timeout: int) -> dict:
        ...


# ── GPT Image 2 后端 ──────────────────────────────────────


def _find_gpt2_script() -> str:
    script_dir = Path(__file__).parent.resolve()
    candidates = [
        str(script_dir.parent.parent / "gpt-image-2-api" / "scripts" / "gpt_image2.py"),
        str(script_dir.parent / "gpt-image-2-api" / "scripts" / "gpt_image2.py"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]


class GPTImage2Backend(ImageBackend):
    """通过 gpt_image2.py CLI 调用 gpt-image-2"""

    def _run(self, cmd: list[str], timeout: int, output_path: str = "") -> dict:
        result = {"success": False, "output_path": output_path, "error": None, "time_elapsed": 0}
        start = time.time()
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                timeout=timeout + 30,
            )
            result["time_elapsed"] = round(time.time() - start, 1)
            if proc.returncode == 0:
                result["success"] = True
                result["stdout"] = proc.stdout
            else:
                result["error"] = (proc.stderr or proc.stdout).strip()
        except subprocess.TimeoutExpired:
            result["error"] = f"超时（{timeout}s）"
        except Exception as e:
            result["error"] = str(e)
        return result

    def generate(self, prompt, output_path, size, quality, timeout):
        script = _find_gpt2_script()
        cmd = [
            sys.executable or "python", script, "generate", prompt,
            "-o", output_path, "--quality", quality,
            "--size", size, "--timeout", str(timeout),
        ]
        return self._run(cmd, timeout, output_path)

    def edit(self, image_path, prompt, output_path, size, quality, timeout):
        script = _find_gpt2_script()
        cmd = [
            sys.executable or "python", script, "edit", image_path, prompt,
            "-o", output_path, "--quality", quality,
            "--size", size, "--timeout", str(timeout),
        ]
        return self._run(cmd, timeout, output_path)


# ── Nano Banana 后端 ──────────────────────────────────────


class NanoBananaBackend(ImageBackend):
    """通过 OpenAI-compatible /v1/chat/completions 调用 Nano Banana"""

    def _call_api(self, body: dict, output_path: str, timeout: int) -> dict:
        result = {"success": False, "output_path": output_path, "error": None, "time_elapsed": 0}
        start = time.time()

        api_key = get_api_key(self.config)
        base_url = get_base_url(self.config)
        if not api_key:
            return {**result, "error": "未配置 API 密钥"}

        endpoint = f"{base_url}/chat/completions"

        try:
            import urllib.request
            import urllib.error

            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            req = urllib.request.Request(
                endpoint, data=data,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=timeout) as resp:
                result["time_elapsed"] = round(time.time() - start, 1)
                raw = resp.read().decode("utf-8")

            resp_data = json.loads(raw)

            if "error" in resp_data:
                result["error"] = str(resp_data["error"])
                return result

            # 从 chat/completions 响应中提取图片
            content = resp_data["choices"][0]["message"]["content"]
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "image_url":
                        url = item["image_url"]["url"]
                        if url.startswith("data:image"):
                            b64_data = url.split(",", 1)[1]
                            img_bytes = base64.b64decode(b64_data)
                            with open(output_path, "wb") as f:
                                f.write(img_bytes)
                            result["success"] = True
                            return result
                result["error"] = "响应中未找到图片数据"
            elif isinstance(content, str):
                # 部分代理返回纯文本描述而非图片
                result["error"] = f"模型返回文本而非图片: {content[:100]}"
            else:
                result["error"] = f"未知响应格式: {type(content)}"

        except urllib.error.HTTPError as e:
            result["error"] = f"HTTP {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            result["error"] = f"请求失败: {e.reason}"
        except Exception as e:
            result["error"] = str(e)

        return result

    def generate(self, prompt: str, output_path: str, size: str, quality: str, timeout: int) -> dict:
        model = get_model_name(self.config)
        body = {
            "model": model,
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "max_tokens": 4000,
        }
        return self._call_api(body, output_path, timeout)

    def edit(self, image_path: str, prompt: str, output_path: str, size: str, quality: str, timeout: int) -> dict:
        model = get_model_name(self.config)

        # 读取图片并编码
        img_b64 = encode_image_base64(image_path)

        ext = Path(image_path).suffix.lower()
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
        mime_type = mime.get(ext, "image/png")

        body = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{img_b64}"}},
                    ],
                }
            ],
            "max_tokens": 4000,
        }
        return self._call_api(body, output_path, timeout)


# ── 工厂 ──────────────────────────────────────────────────


def create_backend(config: dict) -> ImageBackend:
    backend_name = get_backend_name(config)
    if backend_name.startswith("nano-banana"):
        return NanoBananaBackend(config)
    return GPTImage2Backend(config)


# ── 设置向导 ──────────────────────────────────────────────


def run_setup_wizard():
    """交互式配置向导"""
    existing = load_config()

    print(f"\n{'='*55}")
    print(f"  内容营销图片工具 — 初始化配置")
    print(f"{'='*55}\n")

    # 选择后端
    print("选择图片生成模型：")
    for i, key in enumerate(BACKEND_CHOICES, 1):
        print(f"  [{i}] {BACKEND_LABELS[key]}")
    default_idx = BACKEND_CHOICES.index(existing.get("backend", "gpt-image-2")) + 1
    choice = input(f"\n请输入编号 (1-{len(BACKEND_CHOICES)}) 默认 [{default_idx}]: ").strip()
    if not choice:
        choice = str(default_idx)
    try:
        backend = BACKEND_CHOICES[int(choice) - 1]
    except (ValueError, IndexError):
        backend = "gpt-image-2"

    # API 地址
    default_url = existing.get("base_url", DEFAULT_CONFIG["base_url"])
    url = input(f"API 地址 默认 [{default_url}]: ").strip() or default_url

    # API 密钥（留空则不修改）
    if existing.get("api_key"):
        key_hint = f"（已配置 {existing['api_key'][:6]}...，留空保持不变）"
    else:
        key_hint = "（留空则从环境变量读取）"
    key = input(f"API 密钥 {key_hint}: ").strip()

    # 环境变量名
    default_env = existing.get("api_key_env", "OPENAI_API_KEY")
    env_name = input(f"API 密钥环境变量名 默认 [{default_env}]: ").strip() or default_env

    config = {
        "backend": backend,
        "base_url": url,
        "api_key_env": env_name,
    }
    if key:
        config["api_key"] = key

    save_config(config)

    print(f"\n{'='*55}")
    print(f"  ✓ 配置已保存至 {CONFIG_FILE}")
    print(f"  后端: {BACKEND_LABELS[backend]}")
    print(f"  API: {url}")
    print(f"{'='*55}")


def show_config_info():
    """显示当前配置信息"""
    config = load_config()
    if not config:
        print("未配置，请运行 --setup 初始化")
        return

    backend = get_backend_name(config)
    print(f"后端:     {BACKEND_LABELS.get(backend, backend)}")
    print(f"模型:     {get_model_name(config)}")
    print(f"API地址:  {get_base_url(config)}")
    env_name = config.get("api_key_env", "")
    key = get_api_key(config)
    if key:
        print(f"API密钥:  {key[:8]}...{key[-4:]}")
    else:
        print(f"API密钥:  未配置（从环境变量 {env_name} 读取）")

    cfg_file = CONFIG_FILE
    if cfg_file.exists():
        print(f"配置文件: {cfg_file}")


# ── CLI ──────────────────────────────────────────────────


def main():
    import argparse
    parser = argparse.ArgumentParser(description="图片生成后端管理")
    parser.add_argument("--setup", action="store_true", help="运行配置向导")
    parser.add_argument("--show-config", action="store_true", help="显示当前配置")

    args = parser.parse_args()

    if args.setup:
        run_setup_wizard()
    elif args.show_config:
        show_config_info()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
