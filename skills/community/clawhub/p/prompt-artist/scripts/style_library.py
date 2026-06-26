#!/usr/bin/env python3
"""Art style library browser."""

import argparse, json, sys

CATEGORIES = {
    "photography": {
        "name": "📷 摄影风格",
        "styles": {
            "cinematic": "电影感 — 戏剧性灯光, 浅景深, 电影质感",
            "photorealistic": "超写实 — 8K, DSLR, 专业摄影",
            "vintage": "复古 — 胶片感, 褪色, 怀旧",
            "portrait": "人像 — 柔光, 散景, 特写",
            "landscape": "风景 — 广角, 黄金时刻, 壮丽",
        }
    },
    "illustration": {
        "name": "🖌️ 插画风格",
        "styles": {
            "anime": "动漫 — 赛璐璐, 鲜艳色彩, 日系",
            "watercolor": "水彩 — 柔和边缘, 纸质感",
            "oil_painting": "油画 — 笔触, 画布质感, 古典",
            "sketch": "素描 — 铅笔, 线条, 石墨",
            "ink_wash": "水墨 — 中国传统, 写意",
        }
    },
    "digital_art": {
        "name": "💻 数字艺术",
        "styles": {
            "3d_render": "3D渲染 — Octane, C4D, 体积光",
            "pixel_art": "像素画 — 16-bit, 复古游戏",
            "cyberpunk": "赛博朋克 — 霓虹, 未来, 暗黑",
            "fantasy": "奇幻 — 魔法, 史诗, 神秘",
            "surreal": "超现实 — 达利风格, 梦幻",
        }
    },
    "traditional": {
        "name": "🏛️ 传统艺术",
        "styles": {
            "ukiyo_e": "浮世绘 — 日本木版画",
            "ink_wash": "水墨画 — 中国传统",
            "pop_art": "波普艺术 — 安迪沃霍尔",
            "minimalist": "极简 — 简洁, 留白",
        }
    },
}


def list_styles(category=None):
    if category and category in CATEGORIES:
        cats = {category: CATEGORIES[category]}
    else:
        cats = CATEGORIES
    return cats


def format_output(cats):
    lines = ["🎨 风格库", ""]
    for key, cat in cats.items():
        lines.append(f"{cat['name']}")
        for style, desc in cat["styles"].items():
            lines.append(f"  • {style}: {desc}")
        lines.append("")
    lines.append(f"共 {sum(len(c['styles']) for c in cats.values())} 种风格")
    lines.append("使用: --style <style_name> 应用风格")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true", help="List all styles")
    p.add_argument("--category", default=None, choices=list(CATEGORIES.keys()))
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = list_styles(a.category)
    if a.json:
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    else:
        print(format_output(data))
