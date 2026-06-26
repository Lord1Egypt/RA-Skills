#!/usr/bin/env python3
"""
prompt-zs 基础 JSON 提示词生成器 - Expert 1
基于 prompt-zs 技能，生成专业的 JSON 格式提示词
"""

import json
import sys

def generate_prompt_zs_expert1(content):
    """
    生成 prompt-zs Expert 1 格式的基础提示词
    """
    # 中文详细 Prompt
    cn_prompt = f"{content}，充满活力，阳光明媚的环境，专业表演，专注的动作，热情观众，真实自然的光线，动态构图，专业摄影质量，生动的人物表情和肢体语言，真实的物理互动，积极向上的氛围"

    # 英文详细 Prompt
    en_prompt = f"{content} full of energy bright sunny environment professional performance focused actions enthusiastic audience natural lighting dynamic composition professional photography quality vivid facial expressions and body language realistic physical interactions positive uplifting atmosphere"

    # 中文标签
    cn_tags = "活力，专业，动态，真实，积极，阳光，观众，表演"

    # 英文标签
    en_tags = "energy,professional,dynamic,realistic,positive,sunny,audience,performance"

    return [
        {
            "cn": cn_prompt,
            "en": en_prompt,
            "cn-tag": cn_tags,
            "en-tag": en_tags
        }
    ]

def main():
    if len(sys.argv) < 2:
        print("使用方法: python prompt-zs-基础提示词生成器.py \"内容描述\"")
        print("示例: python prompt-zs-基础提示词生成器.py \"一个小男孩在操场上跳街舞，旁边有很多观看，并且鼓掌\"")
        print("\n输出格式: JSON 数组，包含 cn, en, cn-tag, en-tag 四个字段")
        return

    content = sys.argv[1]

    # 生成提示词
    result = generate_prompt_zs_expert1(content)

    # 输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()