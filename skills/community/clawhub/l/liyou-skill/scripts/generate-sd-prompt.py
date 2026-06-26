#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
璃幽 SD 关键词生成器
用于生成优化的 Stable Diffusion 提示词

用法：
    python generate-sd-prompt.py --character "璃幽" --style "anime" --emotion "gentle"
"""

import argparse
import json
from pathlib import Path

# 基础关键词库
QUALITY_TAGS = [
    "masterpiece", "best quality", "ultra-detailed", "high resolution", "8k"
]

STYLE_TAGS = {
    "anime": ["anime style", "cel shading", "vibrant colors", "clean lines"],
    "realistic": ["photorealistic", "realistic", "detailed skin texture"],
    "painting": ["digital painting", "concept art", "illustration"],
}

EMOTION_TAGS = {
    "gentle": ["gentle smile", "kind eyes", "warm expression", "soft lighting"],
    "happy": ["bright smile", "sparkling eyes", "happy", "cheerful"],
    "melancholic": ["melancholic expression", "sad eyes", "pensive", "soft shadows"],
    "focused": ["focused expression", "serious eyes", "determined"],
    "playful": ["playful smile", "wink", "mischievous", "energetic"],
}

POSE_TAGS = {
    "standing": ["standing", "full body", "elegant pose"],
    "sitting": ["sitting", "crossed legs", "relaxed"],
    "lying": ["lying down", "propped on elbow", "lazy pose"],
    "action": ["dynamic pose", "in motion", "flowing hair"],
}

# 璃幽专属特征
LIYOU_FEATURES = [
    "1girl", "solo",
    "deep purple hair", "long hair", "gradient hair", "silver tips",
    "heterochromia", "golden left eye", "purple-red right eye",
    "pale skin", "gentle smile", "small fangs",
    "witch outfit", "dark purple dress", "moon pattern",
    "magic pendant"
]

# 负面提示词
NEGATIVE_PROMPT = [
    "(worst quality, low quality:1.4)",
    "bad anatomy", "bad hands", "bad feet",
    "text", "watermark", "signature", "username",
    "blurry", "jpeg artifacts",
    "ugly", "deformed", "extra limbs", "missing limbs",
    "mutated hands", "poorly drawn hands",
    "poorly drawn face", "mutation",
    "disfigured", "gross proportions",
    "cartoon", "3d", "cgi", "render", "sketch"
]


def generate_prompt(character: str, style: str = "anime", emotion: str = "gentle", 
                    pose: str = "standing", custom_tags: list = None) -> str:
    """生成 SD 提示词"""
    
    # 基础质量标签
    prompt_parts = [f"({', '.join(QUALITY_TAGS[:3])}:1.3)"]
    
    # 风格标签
    if style in STYLE_TAGS:
        prompt_parts.extend(STYLE_TAGS[style])
    
    # 角色特征
    if character.lower() == "璃幽" or character.lower() == "liyou":
        prompt_parts.extend(LIYOU_FEATURES)
    
    # 情绪标签
    if emotion in EMOTION_TAGS:
        prompt_parts.extend(EMOTION_TAGS[emotion])
    
    # 姿态标签
    if pose in POSE_TAGS:
        prompt_parts.extend(POSE_TAGS[pose])
    
    # 自定义标签
    if custom_tags:
        prompt_parts.extend(custom_tags)
    
    # 组合提示词
    prompt = ", ".join(prompt_parts)
    
    return prompt


def generate_negative_prompt() -> str:
    """生成负面提示词"""
    return ", ".join(NEGATIVE_PROMPT)


def save_to_file(prompt: str, negative: str, output_path: str):
    """保存到文件"""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    content = f"""# SD 提示词
**生成时间：** {Path(output_path).stat().st_mtime}

## 正面提示词
```
{prompt}
```

## 负面提示词
```
{negative}
```

## 使用建议
- **采样步数：** 20-30
- **CFG Scale：** 7-9
- **模型推荐：** 动漫风格模型
- **分辨率：** 512x768 或 768x1024（竖图）
"""
    
    output.write_text(content, encoding='utf-8')
    print(f"✓ 已保存到：{output_path}")


def main():
    parser = argparse.ArgumentParser(description="璃幽 SD 关键词生成器")
    parser.add_argument("--character", type=str, default="璃幽", help="角色名")
    parser.add_argument("--style", type=str, default="anime", 
                       choices=["anime", "realistic", "painting"], help="风格")
    parser.add_argument("--emotion", type=str, default="gentle",
                       choices=["gentle", "happy", "melancholic", "focused", "playful"], 
                       help="情绪")
    parser.add_argument("--pose", type=str, default="standing",
                       choices=["standing", "sitting", "lying", "action"], help="姿态")
    parser.add_argument("--tags", type=str, nargs="+", help="自定义标签")
    parser.add_argument("--output", type=str, help="输出文件路径")
    
    args = parser.parse_args()
    
    # 生成提示词
    prompt = generate_prompt(
        character=args.character,
        style=args.style,
        emotion=args.emotion,
        pose=args.pose,
        custom_tags=args.tags
    )
    
    negative = generate_negative_prompt()
    
    # 输出结果
    print("\n" + "="*60)
    print("🌸 璃幽 SD 关键词生成器")
    print("="*60)
    print(f"\n角色：{args.character}")
    print(f"风格：{args.style}")
    print(f"情绪：{args.emotion}")
    print(f"姿态：{args.pose}")
    print("\n正面提示词:")
    print("-" * 60)
    print(prompt)
    print("\n负面提示词:")
    print("-" * 60)
    print(negative)
    print("="*60)
    
    # 保存文件
    if args.output:
        save_to_file(prompt, negative, args.output)


if __name__ == "__main__":
    main()
