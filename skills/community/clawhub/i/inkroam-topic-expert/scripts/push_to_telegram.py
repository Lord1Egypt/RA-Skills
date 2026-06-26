#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送选题到 Telegram
使用 OpenClaw 的 message tool
"""

import json
import sys
import argparse
import subprocess


def format_topic_message(topic, index):
    """格式化单个选题消息"""
    topic_id = topic.get("topic_id", "unknown")
    score = topic.get("score", 0)
    original_title = topic.get("original_title", "")
    theme_options = topic.get("theme_options", [])
    viewpoints = topic.get("viewpoints", [])
    reference_materials = topic.get("reference_materials", [])
    recommended_theme = topic.get("recommended_theme", "")
    
    message = f"""【选题推荐 #{index:03d}】评分：{score}分

📌 原始热点：{original_title}

💡 主题方案：
1. {theme_options[0] if len(theme_options) > 0 else ''}（推荐）
2. {theme_options[1] if len(theme_options) > 1 else ''}
3. {theme_options[2] if len(theme_options) > 2 else ''}

🎯 观点要点：
1. {viewpoints[0] if len(viewpoints) > 0 else ''}
2. {viewpoints[1] if len(viewpoints) > 1 else ''}
3. {viewpoints[2] if len(viewpoints) > 2 else ''}
4. {viewpoints[3] if len(viewpoints) > 3 else ''}
5. {viewpoints[4] if len(viewpoints) > 4 else ''}

📎 参考素材：
{chr(10).join(f'- {m}' for m in reference_materials)}

---
回复操作：
✅ 确认 - 立即生成文章
📝 修改 - 调整三要素
⏰ 稍后 - 加入待写清单
❌ 跳过 - 不适合

选题ID：{topic_id}
"""
    
    return message


def push_to_telegram(topics):
    """推送到 Telegram"""
    for idx, topic in enumerate(topics, 1):
        message = format_topic_message(topic, idx)
        
        # 使用 OpenClaw message tool
        # 这里需要通过 OpenClaw 的方式调用
        # 暂时先打印消息，实际使用时需要集成 OpenClaw
        
        print(f"\n{'='*50}")
        print(message)
        print(f"{'='*50}\n")
        
        # TODO: 实际推送逻辑
        # 需要通过 OpenClaw 的 message tool 或者直接调用 Telegram API


def main():
    parser = argparse.ArgumentParser(description="推送选题到 Telegram")
    parser.add_argument("--data", default="/tmp/three_elements.json", help="三要素数据文件")
    
    args = parser.parse_args()
    
    # 读取数据
    with open(args.data, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    topics = data.get("topics", [])
    
    if not topics:
        print("⚠️  没有选题需要推送", file=sys.stderr)
        return
    
    print(f"📱 准备推送 {len(topics)} 个选题到 Telegram...", file=sys.stderr)
    
    push_to_telegram(topics)
    
    print(f"\n✅ 推送完成：{len(topics)} 个选题", file=sys.stderr)


if __name__ == '__main__':
    main()
