#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 Minimax Image Generation Script
neuroXY 专属 AI 画图技能

版本: 1.1.0
作者: neuroXY
许可证: MIT
平台: Windows / macOS / Linux

https://platform.minimaxi.com/docs/api-reference/image-generation-t2i
"""
import argparse
import datetime
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

# ============================================================================
# 版本与常量
# ============================================================================

__version__ = "1.1.0"
__author__ = "neuroXY"
__license__ = "MIT"

APP_NAME = "MinimaxImageGen"
DEFAULT_OUTPUT_DIR = "./output"

ASPECT_RATIOS: Dict[str, Tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1280, 720),
    "4:3": (1152, 864),
    "3:2": (1248, 832),
    "2:3": (832, 1248),
    "3:4": (864, 1152),
    "9:16": (720, 1280),
    "21:9": (1344, 576),
}

MODELS: Dict[str, str] = {
    "image-01": "默认模型，高质量",
    "image-01-live": "动漫/生活风格",
}

STYLE_TYPES: Dict[str, str] = {
    "漫画": "漫画风格",
    "元气": "元气满满",
    "中世纪": "中世纪风格",
    "水彩": "水彩画风",
}

# ============================================================================
# 风格预设
# ============================================================================

STYLE_PRESETS: Dict[str, Dict[str, Any]] = {
    "动漫少女": {
        "prompt_template": "{subject}, 动漫少女, 大眼睛, 精致五官, 飘逸长发",
        "aspect_ratio": "3:4",
        "model": "image-01-live",
        "style_type": "元气",
    },
    "漫画风": {
        "prompt_template": "{subject}, 漫画风格, 简洁线条, 色彩鲜艳",
        "aspect_ratio": "1:1",
        "model": "image-01-live",
        "style_type": "漫画",
    },
    "水彩画": {
        "prompt_template": "{subject}, 水彩画风格, 柔和色彩, 艺术感",
        "aspect_ratio": "16:9",
        "model": "image-01",
    },
    "浮世绘": {
        "prompt_template": "{subject}, 日本浮世绘风格, 传统绘画",
        "aspect_ratio": "16:9",
        "model": "image-01",
    },
    "像素艺术": {
        "prompt_template": "{subject}, 像素艺术风格, 8-bit, 复古游戏",
        "aspect_ratio": "1:1",
        "model": "image-01",
    },
    "证件照": {
        "prompt_template": "{subject}, 专业证件照, 白色背景, 正面",
        "aspect_ratio": "3:4",
        "model": "image-01",
    },
    "肖像": {
        "prompt_template": "{subject}, 人物肖像, 专业摄影, 影棚灯光",
        "aspect_ratio": "3:2",
        "model": "image-01",
    },
    "赛博朋克": {
        "prompt_template": "{subject}, 赛博朋克风格, 霓虹灯光, 未来科技",
        "aspect_ratio": "16:9",
        "model": "image-01",
    },
    "风景画": {
        "prompt_template": "{subject}, 风景画, 油画风格, 艺术感",
        "aspect_ratio": "16:9",
        "model": "image-01",
    },
    "建筑摄影": {
        "prompt_template": "{subject}, 建筑摄影, 专业灯光, 现代建筑",
        "aspect_ratio": "3:2",
        "model": "image-01",
    },
    "萌宠": {
        "prompt_template": "{subject}, 可爱宠物风格, 大眼睛, 毛茸茸",
        "aspect_ratio": "1:1",
        "model": "image-01",
    },
    "美食摄影": {
        "prompt_template": "{subject}, 美食摄影, 专业摆盘, 诱人",
        "aspect_ratio": "1:1",
        "model": "image-01",
    },
    "产品图": {
        "prompt_template": "{subject}, 产品摄影, 纯色背景, 商业摄影",
        "aspect_ratio": "1:1",
        "model": "image-01",
    },
}

# ============================================================================
# 安全函数
# ============================================================================

def sanitize_input(text: str, max_length: int = 1500) -> str:
    """清理和验证用户输入"""
    if not text:
        return ""
    # 移除控制字符
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    text = text[:max_length]
    # 移除潜在危险模式
    dangerous = ['<script', 'javascript:', 'onerror=', 'onclick=']
    for p in dangerous:
        text = re.sub(p, '', text, flags=re.IGNORECASE)
    return text.strip()


def validate_prompt(prompt: str) -> Tuple[bool, Optional[str]]:
    """验证 prompt"""
    if not prompt:
        return False, "Prompt cannot be empty"
    if len(prompt) < 2:
        return False, "Prompt too short"
    if len(prompt) > 1500:
        return False, "Prompt exceeds 1500 chars"
    return True, None


# ============================================================================
# 工具函数
# ============================================================================

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', text)
    text = re.sub(r'-{2,}', '-', text).strip('-')
    return text or "image"


def get_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def load_api_key_from_config() -> str:
    """从 OpenClaw 配置加载 API Key"""
    paths = [
        Path.home() / ".openclaw" / "openclaw.json",
        Path(os.getcwd()).parent / ".openclaw" / "openclaw.json",
    ]
    
    for p in paths:
        if not p.exists():
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            providers = config.get("models", {}).get("providers", {})
            for name, cfg in providers.items():
                if "minimax" in name.lower():
                    if api_key := cfg.get("apiKey", ""):
                        return api_key
                        
            profiles = config.get("auth", {}).get("profiles", {})
            for name, cfg in profiles.items():
                if "minimax" in name.lower():
                    for k in ["apiKey", "api_key", "key"]:
                        if k in cfg:
                            return cfg[k]
        except:
            continue
    return ""


def get_api_key() -> str:
    api_key = os.environ.get("MINIMAX_API_KEY", "").strip()
    if not api_key:
        api_key = load_api_key_from_config()
    if not api_key:
        print("[ERROR] MINIMAX_API_KEY not set")
        print("Set: $env:MINIMAX_API_KEY = 'your-key'")
        sys.exit(1)
    return api_key


# ============================================================================
# 核心类
# ============================================================================

class MinimaxImageGenerator:
    """Minimax 图像生成器"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.minimaxi.com"
        
    def generate(self, prompt: str, model: str = "image-01",
                 aspect_ratio: str = "1:1", count: int = 1,
                 prompt_optimizer: bool = True, style_type: str = "") -> Dict:
        """调用 API 生成图片"""
        
        url = f"{self.base_url}/v1/image_generation"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": "url",
            "n": count,
            "prompt_optimizer": prompt_optimizer,
        }
        
        if style_type and model == "image-01-live":
            payload["style"] = {"style_type": style_type, "style_weight": 0.8}
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        data = json.dumps(payload).encode("utf-8")
        
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, context=ctx, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                
                base_resp = result.get("base_resp", {})
                status_code = base_resp.get("status_code", 0)
                
                if status_code != 0:
                    status_msg = base_resp.get("status_msg", "Unknown error")
                    self._handle_error(status_code, status_msg)
                
                return result
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            self._handle_error(e.code, f"{e.reason}: {error_body}")
        except Exception as e:
            self._handle_error(0, str(e))
    
    def _handle_error(self, code: int, message: str) -> None:
        """处理错误"""
        errors = {
            1002: "Rate limited, try again later",
            1004: "API Key error",
            1008: "Insufficient balance",
            1026: "Content sensitive",
            2013: "Parameter error",
            2049: "Invalid API Key",
        }
        msg = errors.get(code, message)
        print(f"[ERROR] {code}: {msg}" if code else f"[ERROR] {msg}")
        sys.exit(1)
    
    @staticmethod
    def download_image(url: str, filepath: Path) -> bool:
        """下载图片"""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ctx, timeout=60) as response:
                filepath.parent.mkdir(parents=True, exist_ok=True)
                with open(filepath, "wb") as f:
                    f.write(response.read())
            return True
        except Exception as e:
            print(f"[ERROR] Download failed: {e}")
            return False
    
    @staticmethod
    def preview_image(filepath: Path) -> None:
        """跨平台预览图片"""
        try:
            if sys.platform == "win32":
                os.startfile(filepath)
            elif sys.platform == "darwin":
                subprocess.run(["open", str(filepath)], check=True)
            else:
                subprocess.run(["xdg-open", str(filepath)], check=True)
            print(f"[PREVIEW] Opened: {filepath.name}")
        except:
            try:
                webbrowser.open(f"file://{filepath.absolute()}")
                print(f"[PREVIEW] Browser: {filepath.name}")
            except:
                print(f"[INFO] Saved: {filepath}")


# ============================================================================
# 主程序
# ============================================================================

def build_prompt(preset: str, subject: str) -> str:
    if preset and preset in STYLE_PRESETS:
        return STYLE_PRESETS[preset]["prompt_template"].format(subject=subject)
    return subject


def apply_preset_defaults(args) -> None:
    """应用预设默认参数"""
    if hasattr(args, 'preset') and args.preset in STYLE_PRESETS:
        info = STYLE_PRESETS[args.preset]
        if args.aspect_ratio == "1:1":
            args.aspect_ratio = info.get("aspect_ratio", "1:1")
        args.model = info.get("model", args.model)


def list_presets() -> None:
    print("\n" + "=" * 50)
    print(" Available Style Presets")
    print("=" * 50)
    print(f"{'Preset':<12} {'Model':<16} {'Aspect':<8}")
    print("-" * 50)
    for name, info in STYLE_PRESETS.items():
        print(f"{name:<12} {info.get('model', 'image-01'):<16} {info.get('aspect_ratio', '1:1'):<8}")
    print()
    print(f"Total: {len(STYLE_PRESETS)} presets")


def main():
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME} v{__version__} - neuroXY AI Image Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python gen.py -p "可爱猫咪"
  python gen.py -s "小猫" --preset 萌宠 --preview
  python gen.py --list-presets

License: {__license__}
        """
    )
    
    parser.add_argument("--prompt", "-p", help="Image description")
    parser.add_argument("--subject", "-s", help="Subject for presets")
    parser.add_argument("--count", "-c", type=int, default=1, help="Count (1-9)")
    parser.add_argument("--aspect-ratio", "-a", default="1:1", choices=list(ASPECT_RATIOS.keys()))
    parser.add_argument("--model", "-m", default="image-01", choices=list(MODELS.keys()))
    parser.add_argument("--no-optimizer", action="store_true")
    parser.add_argument("--preset", choices=list(STYLE_PRESETS.keys()))
    parser.add_argument("--style", choices=list(STYLE_TYPES.keys()))
    parser.add_argument("--list-presets", action="store_true")
    parser.add_argument("--out-dir", "-o", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--version", "-v", action="version", version=f"{__version__}")
    
    args = parser.parse_args()
    
    if args.list_presets:
        list_presets()
        return
    
    if not args.prompt and not args.subject:
        print("[ERROR] Provide --prompt or --subject")
        sys.exit(1)
    
    # 构建 prompt
    if args.prompt:
        args.prompt = sanitize_input(args.prompt)
    
    prompt = args.prompt
    if args.preset and args.subject:
        prompt = build_prompt(args.preset, args.subject)
        apply_preset_defaults(args)
    elif not prompt and args.subject:
        prompt = args.subject
    
    # 验证
    is_valid, err = validate_prompt(prompt)
    if not is_valid:
        print(f"[ERROR] {err}")
        sys.exit(1)
    
    if args.count < 1 or args.count > 9:
        print("[ERROR] Count must be 1-9")
        sys.exit(1)
    
    # 获取 API Key
    api_key = get_api_key()
    
    # 输出目录
    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 打印
    print("=" * 50)
    print(f" {APP_NAME} v{__version__} - {__author__}")
    print("=" * 50)
    print(f"[INFO] Prompt: {prompt[:50]}{'...' if len(prompt) > 50 else ''}")
    print(f"[INFO] Model: {args.model}, Aspect: {args.aspect_ratio}")
    if args.preset:
        print(f"[INFO] Preset: {args.preset}")
    print()
    
    # 生成
    generator = MinimaxImageGenerator(api_key)
    result = generator.generate(
        prompt=prompt,
        model=args.model,
        aspect_ratio=args.aspect_ratio,
        count=args.count,
        prompt_optimizer=not args.no_optimizer,
        style_type=args.style or ""
    )
    
    # 下载
    urls = result.get("data", {}).get("image_urls", [])
    if not urls:
        print("[ERROR] No images returned")
        sys.exit(1)
    
    timestamp = get_timestamp()
    slug = slugify(prompt)[:25]
    saved = []
    
    for i, url in enumerate(urls, 1):
        filepath = output_dir / f"minimax-{timestamp}-{slug}-{i}.png"
        print(f"[{i}/{len(urls)}] Downloading...", end=" ")
        if generator.download_image(url, filepath):
            print("OK")
            saved.append(filepath)
        else:
            print("FAILED")
    
    # 完成
    print()
    print("=" * 50)
    
    if saved:
        print(f"[SUCCESS] {len(saved)} image(s) saved!")
        print("\n[FILES]")
        for f in saved:
            print(f"  - {f.absolute()}")
        
        if args.preview:
            print()
            for f in saved:
                generator.preview_image(f)
    else:
        print("[ERROR] No images saved")
        sys.exit(1)


if __name__ == "__main__":
    main()
