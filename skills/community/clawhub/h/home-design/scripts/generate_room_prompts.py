#!/usr/bin/env python3
"""
房间效果图提示词生成器
根据房间类型、风格、尺寸等信息生成专业的 AI 绘画提示词
"""

import argparse
import json
from pathlib import Path


# 风格特征库
STYLE_FEATURES = {
    "现代简约": {
        "keywords": ["modern minimalist", "clean lines", "uncluttered", "functional"],
        "colors": ["white", "light gray", "black accents", "natural wood"],
        "materials": ["laminate floor", "latex paint", "glass", "metal"],
        "lighting": ["recessed lighting", "pendant lights", "natural light"],
        "furniture": ["low-profile", "geometric", "multi-functional"]
    },
    "北欧风格": {
        "keywords": ["nordic", "scandinavian", "cozy", "hygge", "bright"],
        "colors": ["white", "light wood", "pastel blue", "soft gray", "green plants"],
        "materials": ["wood floor", "wool textiles", "linen", "rattan"],
        "lighting": ["warm light", "paper lamps", "candle light"],
        "furniture": ["light wood", "curved", "comfortable"]
    },
    "新中式": {
        "keywords": ["new chinese", "oriental", "zen", "elegant", "traditional modern"],
        "colors": ["dark wood", "cream", "chinese red", "ink black", "jade green"],
        "materials": ["solid wood", "silk", "bamboo", "stone", "bronze"],
        "lighting": ["chinese lantern", "warm ambient", "soft"],
        "furniture": ["ming style", "carved wood", "low seating"]
    },
    "轻奢风格": {
        "keywords": ["light luxury", "elegant", "sophisticated", "refined"],
        "colors": ["champagne", "navy blue", "emerald green", "gold", "marble white"],
        "materials": ["marble", "brass", "velvet", "leather", "mirror"],
        "lighting": ["crystal chandelier", "brass fixtures", "ambient"],
        "furniture": ["tufted", "metallic accents", "plush"]
    },
    "日式风格": {
        "keywords": ["japanese", "zen", "minimalist", "natural", "serene"],
        "colors": ["light wood", "white", "beige", "tatami green", "paper white"],
        "materials": ["tatami", "shoji paper", "bamboo", "light wood", "cotton"],
        "lighting": ["soft diffused", "paper lanterns", "natural"],
        "furniture": ["low", "floor seating", "sliding doors", "built-in"]
    },
    "美式风格": {
        "keywords": ["american", "comfortable", "warm", "traditional", "cozy"],
        "colors": ["warm beige", "navy", "burgundy", "cream", "distressed wood"],
        "materials": ["hardwood", "brick", "leather", "cotton", "wrought iron"],
        "lighting": ["warm", "table lamps", "chandelier"],
        "furniture": ["oversized", "comfortable", "distressed", "classic"]
    },
    "工业风格": {
        "keywords": ["industrial", "urban", "raw", "edgy", "loft"],
        "colors": ["charcoal", "rust", "concrete gray", "black", "brown leather"],
        "materials": ["exposed brick", "concrete", "steel", "reclaimed wood"],
        "lighting": ["edison bulbs", "metal pendants", "track lighting"],
        "furniture": ["metal frame", "leather", "distressed wood", "vintage"]
    },
    "法式风格": {
        "keywords": ["french", "romantic", "elegant", "ornate", "charming"],
        "colors": ["cream", "soft pink", "powder blue", "gold", "white"],
        "materials": ["marble", "gilded wood", "silk", "crystal", "parquet"],
        "lighting": ["crystal chandelier", "candle sconces", "soft"],
        "furniture": ["curved", "ornate", "painted wood", "velvet"]
    }
}

# 房间特定元素
ROOM_ELEMENTS = {
    "客厅": {
        "furniture": ["sofa", "coffee table", "TV cabinet", "armchair", "bookshelf"],
        "decor": ["area rug", "curtains", "wall art", "throw pillows", "plants"],
        "features": ["large window", "balcony access", "built-in storage"]
    },
    "卧室": {
        "furniture": ["bed", "nightstand", "wardrobe", "dresser", "vanity"],
        "decor": ["bedding", "curtains", "bedside lamp", "wall art", "rug"],
        "features": ["large window", "built-in closet", "bay window"]
    },
    "儿童房": {
        "furniture": ["single bed", "study desk", "bookshelf", "toy storage", "wardrobe"],
        "decor": ["colorful bedding", "wall decals", "string lights", "playful rug", "educational posters"],
        "features": ["safe corners", "play area", "study nook"]
    },
    "书房": {
        "furniture": ["desk", "office chair", "bookshelf", "filing cabinet", "reading chair"],
        "decor": ["desk lamp", "plants", "wall art", "organizers", "cork board"],
        "features": ["good lighting", "quiet", "built-in desk"]
    },
    "餐厅": {
        "furniture": ["dining table", "dining chairs", "sideboard", "wine rack"],
        "decor": ["table runner", "centerpiece", "pendant light", "wall art", "mirror"],
        "features": ["near kitchen", "natural light", "storage"]
    },
    "厨房": {
        "furniture": ["cabinets", "countertop", "island", "bar stools"],
        "decor": ["backsplash", "pendant lights", "plants", "utensil holder"],
        "features": ["U-shape", "L-shape", "galley", "modern appliances"]
    },
    "卫生间": {
        "furniture": ["vanity", "toilet", "shower", "bathtub", "storage cabinet"],
        "decor": ["mirror", "towels", "plants", "soap dispenser", "bath mat"],
        "features": ["dry-wet separation", "shower room", "window"]
    },
    "玄关": {
        "furniture": ["shoe cabinet", "coat rack", "bench", "console table"],
        "decor": ["mirror", "wall hooks", "rug", "decorative bowl", "art"],
        "features": ["built-in storage", "good lighting", "welcoming"]
    },
    "阳台": {
        "furniture": ["small table", "chairs", "plant stand", "storage cabinet"],
        "decor": ["potted plants", "outdoor rug", "string lights", "cushions"],
        "features": ["large window", "natural light", "greenery"]
    }
}


def generate_prompt(room: str, style: str, size: str, color: str = "", 
                   features: list = None, view_angle: str = "wide angle") -> str:
    """生成单个房间的效果图提示词"""
    
    style_info = STYLE_FEATURES.get(style, STYLE_FEATURES["现代简约"])
    room_info = ROOM_ELEMENTS.get(room, ROOM_ELEMENTS["客厅"])
    
    # 构建提示词
    prompt_parts = [
        f"professional interior design photography of a {room}",
        f"style: {', '.join(style_info['keywords'])}",
        f"size: {size}",
    ]
    
    # 添加颜色
    if color:
        prompt_parts.append(f"color scheme: {color}")
    else:
        prompt_parts.append(f"color scheme: {', '.join(style_info['colors'][:4])}")
    
    # 添加材料
    prompt_parts.append(f"materials: {', '.join(style_info['materials'][:4])}")
    
    # 添加家具
    prompt_parts.append(f"furniture: {', '.join(room_info['furniture'][:5])}")
    
    # 添加装饰
    prompt_parts.append(f"decor: {', '.join(room_info['decor'][:4])}")
    
    # 添加特色
    if features:
        prompt_parts.extend(features)
    else:
        prompt_parts.append(f"features: {', '.join(room_info['features'][:2])}")
    
    # 添加灯光
    prompt_parts.append(f"lighting: {', '.join(style_info['lighting'][:3])}")
    
    # 添加摄影参数
    prompt_parts.extend([
        "photorealistic",
        "8k resolution",
        "architectural digest style",
        "professional lighting",
        "interior design magazine quality",
        f"{view_angle} view",
        "depth of field",
        "natural lighting",
        "highly detailed"
    ])
    
    # 负面提示词
    negative_prompt = "blurry, low quality, distorted, deformed, unnatural, awkward proportions, " \
                     "poorly rendered, unbalanced composition, cluttered, messy, " \
                     "dark, poorly lit, amateur, low resolution"
    
    return {
        "positive_prompt": ", ".join(prompt_parts),
        "negative_prompt": negative_prompt,
        "style": style,
        "room": room,
        "parameters": {
            "width": 1024,
            "height": 768,
            "steps": 30,
            "cfg_scale": 7,
            "seed": -1
        }
    }


def generate_all_rooms(style: str, house_info: dict) -> dict:
    """生成所有房间的效果图提示词"""
    
    rooms_config = {
        "客厅": {
            "size": house_info.get("living_room_size", "8.6㎡ (2.6m×3.3m)"),
            "color": "",
            "features": ["TV wall with built-in storage", "balcony access"]
        },
        "卧室": {
            "size": house_info.get("bedroom_size", "14.3㎡ (3.4m×4.2m)"),
            "color": "",
            "features": ["built-in wardrobe", "bay window"]
        },
        "儿童房": {
            "size": house_info.get("kids_room_size", "10.1㎡ (2.8m×3.6m)"),
            "color": "soft blue and white" if style in ["现代简约", "北欧风格"] else "",
            "features": ["study area", "toy storage", "safe rounded corners"]
        },
        "书房": {
            "size": house_info.get("study_size", "4.9㎡ (2.6m×1.9m)"),
            "color": "",
            "features": ["built-in desk and bookshelf", "tatami platform"]
        },
        "餐厅": {
            "size": house_info.get("dining_room_size", "9.4㎡ (2.6m×3.6m)"),
            "color": "",
            "features": ["sideboard", "pendant lighting"]
        },
        "厨房": {
            "size": house_info.get("kitchen_size", "5.5㎡ (2.3m×2.4m)"),
            "color": "",
            "features": ["U-shape layout", "modern built-in appliances"]
        },
        "卫生间": {
            "size": house_info.get("bathroom_size", "2.4㎡ (1.1m×2.2m)"),
            "color": "",
            "features": ["dry-wet separation", "shower room", "mirror cabinet"]
        },
        "玄关": {
            "size": house_info.get("entrance_size", "3㎡"),
            "color": "",
            "features": ["floor-to-ceiling shoe cabinet", "bench with storage"]
        }
    }
    
    results = {}
    for room, config in rooms_config.items():
        results[room] = generate_prompt(
            room=room,
            style=style,
            size=config["size"],
            color=config["color"],
            features=config["features"]
        )
    
    return results


def format_prompts_md(prompts: dict, output_path: str):
    """格式化提示词为 Markdown 文档"""
    
    md = "# 房间效果图 AI 绘画提示词\n\n"
    md += "本文档包含每个房间的 AI 绘画提示词，可用于 Stable Diffusion、DALL-E 3、Midjourney 等 AI 图像生成工具。\n\n"
    md += "---\n\n"
    
    for room, data in prompts.items():
        md += f"## {room}\n\n"
        md += f"**风格**: {data['style']}\n\n"
        md += "### 正向提示词\n```text\n"
        md += data['positive_prompt'] + "\n```\n\n"
        md += "### 负向提示词\n```text\n"
        md += data['negative_prompt'] + "\n```\n\n"
        md += "### 生成参数\n"
        md += f"- 分辨率：{data['parameters']['width']}×{data['parameters']['height']}\n"
        md += f"- 步数：{data['parameters']['steps']}\n"
        md += f"- CFG Scale: {data['parameters']['cfg_scale']}\n"
        md += f"- Seed: {data['parameters']['seed']} (随机)\n\n"
        md += "---\n\n"
    
    md += "## 使用指南\n\n"
    md += "### Stable Diffusion WebUI\n"
    md += "1. 打开 Stable Diffusion WebUI\n"
    md += "2. 复制正向提示词到 Prompt 框\n"
    md += "3. 复制负向提示词到 Negative Prompt 框\n"
    md += "4. 设置参数（分辨率、步数等）\n"
    md += "5. 点击 Generate 生成\n\n"
    md += "### Midjourney\n"
    md += "```bash\n"
    md += "/imagine prompt: [正向提示词] --ar 4:3 --v 6\n"
    md += "```\n\n"
    md += "### DALL-E 3\n"
    md += "直接使用正向提示词，DALL-E 3 会自动优化。\n\n"
    md += "### 在线工具推荐\n"
    md += "- **LiblibAI** (哩布哩布): https://www.liblib.ai/\n"
    md += "- **吐司 TusiArt**: https://tusiart.com/\n"
    md += "- **SeaArt**: https://www.seaart.ai/\n"
    md += "- **Leonardo.ai**: https://leonardo.ai/\n"
    
    Path(output_path).write_text(md, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='生成房间效果图 AI 绘画提示词')
    parser.add_argument('--style', required=True, help='装修风格')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    # 房屋信息
    parser.add_argument('--living-room', default='8.6㎡', help='客厅尺寸')
    parser.add_argument('--bedroom', default='14.3㎡', help='卧室尺寸')
    parser.add_argument('--kids-room', default='10.1㎡', help='儿童房尺寸')
    parser.add_argument('--study', default='4.9㎡', help='书房尺寸')
    parser.add_argument('--dining', default='9.4㎡', help='餐厅尺寸')
    parser.add_argument('--kitchen', default='5.5㎡', help='厨房尺寸')
    parser.add_argument('--bathroom', default='2.4㎡', help='卫生间尺寸')
    parser.add_argument('--entrance', default='3㎡', help='玄关尺寸')
    
    args = parser.parse_args()
    
    house_info = {
        "living_room_size": args.living_room,
        "bedroom_size": args.bedroom,
        "kids_room_size": args.kids_room,
        "study_size": args.study,
        "dining_room_size": args.dining,
        "kitchen_size": args.kitchen,
        "bathroom_size": args.bathroom,
        "entrance_size": args.entrance
    }
    
    prompts = generate_all_rooms(args.style, house_info)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.json:
        output_path.write_text(json.dumps(prompts, ensure_ascii=False, indent=2), encoding='utf-8')
    else:
        format_prompts_md(prompts, args.output)
    
    print(f"效果图提示词已生成：{output_path}")
    print(f"共 {len(prompts)} 个房间")


if __name__ == '__main__':
    main()
