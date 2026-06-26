#!/usr/bin/env python3
"""
Content Marketing Image - 规范管理与品牌学习工具

功能：
1. 查询平台图片规格（尺寸、安全区、格式）
2. 管理品牌设计语言（品牌色、字体、风格）
3. 自学习：记录生成历史，从反馈中提炼品牌语言
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── 平台规格数据库 ──────────────────────────────────────────────

PLATFORM_SPECS = {
    "wechat-cover": {
        "name": "微信公众号封面",
        "width": 900,
        "height": 383,
        "safe_area": {"top": 0, "bottom": 50, "left": 0, "right": 0},
        "safe_note": "底部50px被标题覆盖，核心内容放在0-333px区域",
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "900:383",
    },
    "wechat-square": {
        "name": "公众号方形缩略图",
        "width": 300,
        "height": 300,
        "safe_area": {"top": 0, "bottom": 0, "left": 0, "right": 0},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "1:1",
        "note": "自动从一级封面裁剪中心区域",
    },
    "wechat-moments-portrait": {
        "name": "朋友圈竖版海报",
        "width": 1080,
        "height": 1920,
        "safe_area": {"top": 50, "bottom": 100, "left": 30, "right": 30},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "9:16",
    },
    "wechat-moments-square": {
        "name": "朋友圈方版海报",
        "width": 1080,
        "height": 1080,
        "safe_area": {"top": 30, "bottom": 30, "left": 30, "right": 30},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "1:1",
    },
    "xiaohongshu-cover": {
        "name": "小红书笔记封面",
        "width": 1242,
        "height": 1660,
        "safe_area": {"top": 50, "bottom": 100, "left": 40, "right": 40},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "3:4",
        "note": "最推荐比例，封面文字3-8字最佳",
    },
    "xiaohongshu-square": {
        "name": "小红书方版封面",
        "width": 1080,
        "height": 1080,
        "safe_area": {"top": 30, "bottom": 30, "left": 30, "right": 30},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "1:1",
    },
    "douyin-cover": {
        "name": "抖音视频封面",
        "width": 1080,
        "height": 1920,
        "safe_area": {"top": 50, "bottom": 150, "left": 50, "right": 50},
        "safe_note": "底部区域被标题/按钮遮挡，核心安全区为画面中心60%（540×1152）",
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "9:16",
    },
    "weibo-horizontal": {
        "name": "微博横版配图",
        "width": 1200,
        "height": 675,
        "safe_area": {"top": 20, "bottom": 20, "left": 30, "right": 30},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "16:9",
    },
    "weibo-square": {
        "name": "微博方版配图",
        "width": 1200,
        "height": 1200,
        "safe_area": {"top": 30, "bottom": 30, "left": 30, "right": 30},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "1:1",
    },
    "weibo-vertical": {
        "name": "微博竖版配图",
        "width": 1200,
        "height": 1500,
        "safe_area": {"top": 30, "bottom": 50, "left": 30, "right": 30},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "4:5",
    },
    "video-cover": {
        "name": "视频号封面",
        "width": 1080,
        "height": 1080,
        "safe_area": {"top": 50, "bottom": 100, "left": 30, "right": 30},
        "safe_note": "底部被视频标题遮挡，核心信息置于顶部",
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "1:1",
    },
    "bilibili-cover": {
        "name": "B站视频封面",
        "width": 1146,
        "height": 717,
        "safe_area": {"top": 20, "bottom": 40, "left": 30, "right": 30},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "16:10",
        "note": "大字标题+高对比度风格",
    },
    "zhihu-cover": {
        "name": "知乎封面",
        "width": 1080,
        "height": 1080,
        "safe_area": {"top": 30, "bottom": 30, "left": 30, "right": 30},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "1:1",
    },
    "taobao-main": {
        "name": "淘宝商品主图",
        "width": 800,
        "height": 800,
        "safe_area": {"top": 20, "bottom": 20, "left": 20, "right": 20},
        "format": ["jpeg", "png"],
        "max_size_mb": 5,
        "ratio": "1:1",
        "note": "首图建议白底",
    },
    "kuaishou-cover": {
        "name": "快手视频封面",
        "width": 1080,
        "height": 1920,
        "safe_area": {"top": 50, "bottom": 150, "left": 50, "right": 50},
        "format": ["jpeg", "png"],
        "max_size_mb": 10,
        "ratio": "9:16",
    },

    # ── 海外平台 ──
    "facebook-square": {
        "name": "Facebook 方版贴文",
        "width": 1200, "height": 1200,
        "safe_area": {"top": 30, "bottom": 30, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "1:1",
    },
    "facebook-landscape": {
        "name": "Facebook 横版贴文",
        "width": 1200, "height": 630,
        "safe_area": {"top": 20, "bottom": 20, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "40:21",
    },
    "facebook-cover": {
        "name": "Facebook 封面照片",
        "width": 1200, "height": 628,
        "safe_area": {"top": 50, "bottom": 50, "left": 30, "right": 30},
        "safe_note": "底部50px被头像和按钮遮挡",
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "300:157",
    },
    "facebook-stories": {
        "name": "Facebook 快拍",
        "width": 1080, "height": 1920,
        "safe_area": {"top": 100, "bottom": 200, "left": 40, "right": 40},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "9:16",
    },
    "instagram-square": {
        "name": "Instagram 方版贴文",
        "width": 1200, "height": 1200,
        "safe_area": {"top": 30, "bottom": 30, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "1:1",
        "note": "推荐 1080×1080 上传，安全区内放置核心内容",
    },
    "instagram-portrait": {
        "name": "Instagram 竖版贴文",
        "width": 630, "height": 1200,
        "safe_area": {"top": 50, "bottom": 100, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "21:40",
    },
    "instagram-stories": {
        "name": "Instagram 快拍",
        "width": 1080, "height": 1920,
        "safe_area": {"top": 150, "bottom": 200, "left": 30, "right": 30},
        "safe_note": "顶部150px和底部200px被UI遮挡",
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "9:16",
    },
    "twitter-square": {
        "name": "X (Twitter) 方版贴文",
        "width": 1200, "height": 1200,
        "safe_area": {"top": 20, "bottom": 20, "left": 20, "right": 20},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "1:1",
    },
    "twitter-landscape": {
        "name": "X (Twitter) 横版贴文",
        "width": 1200, "height": 900,
        "safe_area": {"top": 20, "bottom": 20, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "4:3",
    },
    "twitter-banner": {
        "name": "X (Twitter) 封面横幅",
        "width": 1500, "height": 500,
        "safe_area": {"top": 20, "bottom": 20, "left": 40, "right": 40},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "3:1",
        "note": "头像会遮挡左下角区域",
    },
    "twitter-instream": {
        "name": "X (Twitter) 信息流图片",
        "width": 1600, "height": 900,
        "safe_area": {"top": 20, "bottom": 20, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "16:9",
    },
    "pinterest-pin": {
        "name": "Pinterest 图钉",
        "width": 1000, "height": 1500,
        "safe_area": {"top": 50, "bottom": 100, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "2:3",
        "note": "竖版表现最佳，推荐 2:3 比例",
    },
    "pinterest-square": {
        "name": "Pinterest 方版图钉",
        "width": 1000, "height": 1000,
        "safe_area": {"top": 30, "bottom": 30, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "1:1",
    },
    "pinterest-idea": {
        "name": "Pinterest Idea Pin",
        "width": 1080, "height": 1920,
        "safe_area": {"top": 80, "bottom": 200, "left": 40, "right": 40},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "9:16",
    },
    "linkedin-landscape": {
        "name": "LinkedIn 横版贴文",
        "width": 1200, "height": 627,
        "safe_area": {"top": 20, "bottom": 20, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "1200:627",
    },
    "linkedin-square": {
        "name": "LinkedIn 方版贴文",
        "width": 1080, "height": 1080,
        "safe_area": {"top": 30, "bottom": 30, "left": 30, "right": 30},
        "format": ["jpeg", "png"], "max_size_mb": 10, "ratio": "1:1",
    },
    "linkedin-banner": {
        "name": "LinkedIn 公司封面",
        "width": 1128, "height": 191,
        "safe_area": {"top": 10, "bottom": 10, "left": 20, "right": 20},
        "format": ["jpeg", "png"], "max_size_mb": 5, "ratio": "1128:191",
        "note": "超宽比例，文字精简为主",
    },
}

# ── 平台别名与分组映射 ──────────────────────────────────────────

PLATFORM_ALIASES = {
    "微信公众号": "wechat-cover",
    "公众号": "wechat-cover",
    "微信": "wechat-cover",
    "朋友圈": "wechat-moments-portrait",
    "小红书封面": "xiaohongshu-cover",
    "小红书": "xiaohongshu-cover",
    "抖音": "douyin-cover",
    "微博": "weibo-horizontal",
    "微博横版": "weibo-horizontal",
    "微博方版": "weibo-square",
    "微博竖版": "weibo-vertical",
    "视频号": "video-cover",
    "B站": "bilibili-cover",
    "B站封面": "bilibili-cover",
    "bilibili": "bilibili-cover",
    "知乎": "zhihu-cover",
    "淘宝": "taobao-main",
    "淘宝主图": "taobao-main",
    "快手": "kuaishou-cover",
    "公众号封面": "wechat-cover",
    "朋友圈竖版": "wechat-moments-portrait",
    "朋友圈方版": "wechat-moments-square",
    "facebook": "facebook-square",
    "fb": "facebook-square",
    "Facebook": "facebook-square",
    "Facebook方版": "facebook-square",
    "Facebook横版": "facebook-landscape",
    "Facebook封面": "facebook-cover",
    "Facebook快拍": "facebook-stories",
    "instagram": "instagram-square",
    "ig": "instagram-square",
    "Instagram": "instagram-square",
    "Instagram方版": "instagram-square",
    "Instagram竖版": "instagram-portrait",
    "Instagram快拍": "instagram-stories",
    "twitter": "twitter-square",
    "x": "twitter-square",
    "Twitter": "twitter-square",
    "Twitter方版": "twitter-square",
    "Twitter横版": "twitter-landscape",
    "Twitter横幅": "twitter-banner",
    "Twitter信息流": "twitter-instream",
    "pinterest": "pinterest-pin",
    "Pinterest": "pinterest-pin",
    "Pinterest图钉": "pinterest-pin",
    "Pinterest方版": "pinterest-square",
    "linkedin": "linkedin-landscape",
    "LinkedIn": "linkedin-landscape",
    "LinkedIn横版": "linkedin-landscape",
    "LinkedIn方版": "linkedin-square",
    "LinkedIn封面": "linkedin-banner",
}

SCENE_GROUPS = {
    "social-media": ["wechat-cover", "weibo-horizontal", "xiaohongshu-cover", "douyin-cover"],
    "e-commerce": ["taobao-main"],
    "short-video": ["douyin-cover", "kuaishou-cover", "video-cover"],
    "knowledge": ["zhihu-cover", "bilibili-cover"],
}


# ── 品牌语言管理 ──────────────────────────────────────────────

def _brand_dir() -> Path:
    """获取品牌学习数据目录"""
    return Path.home() / ".content-marketing" / "brands"


def load_brand(brand_name: str) -> dict:
    """加载品牌设计语言配置"""
    brand_file = _brand_dir() / f"{brand_name}.json"
    if brand_file.exists():
        return json.loads(brand_file.read_text(encoding="utf-8"))
    return {
        "name": brand_name,
        "colors": [],
        "fonts": [],
        "style_notes": "",
        "design_patterns": [],
        "avoid_patterns": [],
        "sample_count": 0,
        "generations": [],
    }


def save_brand(brand_data: dict) -> None:
    """保存品牌设计语言配置"""
    brand_dir = _brand_dir()
    brand_dir.mkdir(parents=True, exist_ok=True)
    brand_file = brand_dir / f"{brand_data['name']}.json"
    brand_file.write_text(json.dumps(brand_data, ensure_ascii=False, indent=2), encoding="utf-8")


def record_generation(
    brand_name: str,
    platform: str,
    scene: str,
    prompt: str,
    output_path: str,
    feedback: Optional[str] = None,
    rating: Optional[int] = None,
) -> dict:
    """记录一次图片生成历史"""
    brand = load_brand(brand_name)
    record = {
        "timestamp": datetime.now().isoformat(),
        "platform": platform,
        "scene": scene,
        "prompt": prompt,
        "output_path": output_path,
        "feedback": feedback,
        "rating": rating,
    }
    brand.setdefault("generations", []).append(record)
    brand["sample_count"] = len(brand["generations"])
    save_brand(brand)
    return record


def learn_from_feedback(
    brand_name: str,
    generation_index: int,
    feedback: str,
    rating: int,
    extracted_insights: Optional[dict] = None,
) -> dict:
    """从用户反馈中学习，提炼品牌设计语言"""
    brand = load_brand(brand_name)
    gens = brand.get("generations", [])

    if generation_index < len(gens):
        gens[generation_index]["feedback"] = feedback
        gens[generation_index]["rating"] = rating

    if extracted_insights:
        for key in ["colors", "fonts", "design_patterns", "avoid_patterns"]:
            if key in extracted_insights:
                existing = brand.setdefault(key, [])
                for item in extracted_insights[key]:
                    if item not in existing:
                        existing.append(item)

        if "style_notes" in extracted_insights:
            existing_notes = brand.get("style_notes", "")
            new_note = extracted_insights["style_notes"]
            if new_note not in existing_notes:
                brand["style_notes"] = (
                    existing_notes + "\n" + new_note if existing_notes else new_note
                )

    save_brand(brand)
    return brand


# ── 自定义规格存储 ──────────────────────────────────────────────

CUSTOM_SPECS_FILE = Path.home() / ".content-marketing" / "custom_specs.json"


def _ensure_custom_dir():
    Path.home().joinpath(".content-marketing").mkdir(parents=True, exist_ok=True)


def load_custom_specs() -> dict:
    """加载用户自定义平台规格"""
    if CUSTOM_SPECS_FILE.exists():
        try:
            return json.loads(CUSTOM_SPECS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_custom_spec(custom_key: str, spec: dict):
    """保存自定义平台规格"""
    _ensure_custom_dir()
    specs = load_custom_specs()
    specs[custom_key] = spec
    CUSTOM_SPECS_FILE.write_text(json.dumps(specs, ensure_ascii=False, indent=2), encoding="utf-8")


def delete_custom_spec(custom_key: str) -> bool:
    """删除自定义平台规格"""
    specs = load_custom_specs()
    if custom_key in specs:
        del specs[custom_key]
        CUSTOM_SPECS_FILE.write_text(json.dumps(specs, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    return False


def _gen_custom_key(name: str, w: int, h: int) -> str:
    """生成自定义平台 key: custom_{name}_{w}x{h}"""
    safe = "".join(c if c.isalnum() else "_" for c in name).strip("_").lower() or "custom"
    return f"custom_{safe}_{w}x{h}"


def parse_inline_spec(platform_key: str) -> Optional[dict]:
    """解析内联规格格式: "平台名:宽x高"

    例如: "我的海报:1200x800" → {"name":"我的海报", "width":1200, "height":800}
    """
    if ":" not in platform_key or "x" not in platform_key:
        return None

    parts = platform_key.split(":", 1)
    if len(parts) != 2:
        return None

    name = parts[0].strip()
    dims = parts[1].strip().lower()

    if "x" not in dims:
        return None

    dim_parts = dims.split("x")
    if len(dim_parts) != 2:
        return None

    try:
        w = int(dim_parts[0].strip())
        h = int(dim_parts[1].strip())
    except ValueError:
        return None

    if w <= 0 or h <= 0:
        return None

    ratio = f"{w}:{h}" if w == h else f"{w}:{h}"
    # 化简比例
    from math import gcd
    g = gcd(w, h)
    ratio = f"{w//g}:{h//g}"

    return {
        "name": name,
        "width": w,
        "height": h,
        "safe_area": {"top": 0, "bottom": 0, "left": 0, "right": 0},
        "format": ["png", "jpeg"],
        "max_size_mb": 10,
        "ratio": ratio,
        "note": f"自定义规格（{name}）",
    }


# ── 查询接口 ──────────────────────────────────────────────────


def get_spec(platform_key: str) -> Optional[dict]:
    """查询平台规格，支持别名、自定义规格、内联格式

    优先级: 别名 → 内置规格 → 自定义规格 → 内联解析
    内联格式示例: "我的海报:1200x800"
    """
    key = PLATFORM_ALIASES.get(platform_key, platform_key)

    # 内置规格
    spec = PLATFORM_SPECS.get(key)
    if spec:
        return spec

    # 自定义规格（已保存的）
    custom_specs = load_custom_specs()
    if key in custom_specs:
        return custom_specs[key]

    # 内联格式 "名称:宽x高"
    inline_spec = parse_inline_spec(platform_key)
    if inline_spec:
        return inline_spec

    return None


def list_platforms() -> list[dict]:
    """列出所有平台（含自定义）及其规格概要"""
    result = []
    for key, spec in PLATFORM_SPECS.items():
        result.append({
            "key": key,
            "name": spec["name"],
            "width": spec["width"],
            "height": spec["height"],
            "ratio": spec["ratio"],
        })
    # 自定义规格
    for key, spec in load_custom_specs().items():
        result.append({
            "key": key,
            "name": spec["name"],
            "width": spec["width"],
            "height": spec["height"],
            "ratio": spec.get("ratio", f"{spec['width']}:{spec['height']}"),
        })
    return result


def build_generation_prompt(
    brand_name: str,
    platform_key: str,
    scene_description: str,
    reference_description: Optional[str] = None,
) -> str:
    """根据品牌语言和平台规格构建图片生成 prompt"""
    spec = get_spec(platform_key)
    brand = load_brand(brand_name) if brand_name else {}

    prompt_parts = [scene_description]

    # 加入参考KV描述
    if reference_description:
        prompt_parts.append(f"\nReference style: {reference_description}")

    # 加入品牌设计语言
    if brand:
        colors = brand.get("colors", [])
        if colors:
            prompt_parts.append(f"Brand colors: {', '.join(colors)}")

        style = brand.get("style_notes", "")
        if style:
            prompt_parts.append(f"Style: {style}")

        avoid = brand.get("avoid_patterns", [])
        if avoid:
            prompt_parts.append(f"Avoid: {', '.join(avoid)}")

    # 加入平台尺寸信息
    if spec:
        prompt_parts.append(
            f"Output dimensions: {spec['width']}x{spec['height']}px, "
            f"aspect ratio {spec['ratio']}"
        )

    return "\n".join(prompt_parts)


def build_output_path(
    brand_name: str,
    platform_key: str,
    scene_slug: str,
    output_dir: str = "output",
) -> str:
    """按照规范生成输出文件路径

    格式: output/{brand}/{date}/{platform}_{scene}_{timestamp}.png
    """
    spec = get_spec(platform_key)
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    timestamp = now.strftime("%H%M%S")

    safe_brand = brand_name.replace(" ", "-").lower() if brand_name else "default"
    safe_platform = (spec["name"] if spec else platform_key).replace(" ", "-")
    safe_scene = scene_slug.replace(" ", "-").lower()

    dir_path = Path(output_dir) / safe_brand / date_str
    dir_path.mkdir(parents=True, exist_ok=True)

    filename = f"{safe_platform}_{safe_scene}_{timestamp}.png"
    return str(dir_path / filename)


# ── CLI ──────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  spec_manager.py list                    # 列出所有平台规格")
        print("  spec_manager.py get <platform>          # 查询平台规格")
        print("  spec_manager.py brand <name>            # 显示品牌语言")
        print("  spec_manager.py record <brand> <plat> <scene> <prompt> <path>")
        print("  spec_manager.py feedback <brand> <idx> <rating> <feedback>")
        return

    cmd = sys.argv[1]

    if cmd == "list":
        for p in list_platforms():
            print(f"{p['key']:30s} {p['width']}×{p['height']}  {p['ratio']}")

    elif cmd == "get" and len(sys.argv) >= 3:
        spec = get_spec(sys.argv[2])
        if spec:
            print(json.dumps(spec, ensure_ascii=False, indent=2))
        else:
            print(f"Unknown platform: {sys.argv[2]}", file=sys.stderr)
            sys.exit(1)

    elif cmd == "brand" and len(sys.argv) >= 3:
        brand = load_brand(sys.argv[2])
        print(json.dumps(brand, ensure_ascii=False, indent=2))

    elif cmd == "record" and len(sys.argv) >= 7:
        result = record_generation(
            sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
        )
        print(f"Recorded generation #{result['timestamp']}")

    elif cmd == "feedback" and len(sys.argv) >= 6:
        brand = learn_from_feedback(
            sys.argv[2], int(sys.argv[3]), sys.argv[5], int(sys.argv[4])
        )
        print(f"Updated brand '{brand['name']}' with feedback")

    else:
        print("Invalid command or arguments")
        sys.exit(1)


if __name__ == "__main__":
    main()
