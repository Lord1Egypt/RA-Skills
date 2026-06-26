#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成笔尖三要素
基于热点选题，生成主题、观点要点、参考素材
"""

import json
import sys
import argparse
import os


def generate_three_elements(topic_data, account_style="墨云风格/专业实操", target_platform="公众号"):
    """
    生成笔尖三要素
    
    Args:
        topic_data: 选题数据 {title, url, source, excerpt, scores}
        account_style: 账号风格
        target_platform: 目标平台
    
    Returns:
        dict: {theme_options, viewpoints, reference_materials, recommended_theme}
    """
    
    title = topic_data.get("title", "")
    url = topic_data.get("url", "")
    excerpt = topic_data.get("excerpt", "")
    source = topic_data.get("source", "")
    
    # 使用 AI 生成三要素的 prompt
    prompt = f"""
你是一个专业的自媒体选题专家，擅长将热点事件转化为高质量的公众号选题。

【热点信息】
标题：{title}
来源：{source}
摘要：{excerpt if excerpt else '无'}
链接：{url}

【账号定位】
风格：{account_style}
平台：{target_platform}
读者：关注 AI 工具、效率提升、自媒体运营的人群

【任务】
请基于这个热点，生成笔尖写作所需的三要素：

1. 主题方案（3个备选标题，要求吸引眼球、符合账号调性）
2. 观点要点（5条核心观点，结合账号定位和读者需求）
3. 参考素材（列出需要补充的素材类型）

【输出格式】
严格按照以下 JSON 格式输出：

{{
  "theme_options": [
    "标题方案1（推荐）",
    "标题方案2",
    "标题方案3"
  ],
  "viewpoints": [
    "核心观点1",
    "核心观点2",
    "核心观点3",
    "可选观点4",
    "可选观点5"
  ],
  "reference_materials": [
    "热点原文链接",
    "相关数据/案例",
    "用户讨论精选"
  ],
  "recommended_theme": "标题方案1"
}}

请直接输出 JSON，不要有任何其他文字。
"""
    
    # 这里应该调用 AI API（Claude/GPT）
    # 为了快速演示，先返回一个模板
    
    # 简单的标题生成逻辑
    theme_options = [
        f"{title}：这背后的3个真相",
        f"关于{title}，你需要知道的5件事",
        f"{title}，普通人如何抓住这波机会？"
    ]
    
    viewpoints = [
        f"事件背景：{title}的来龙去脉",
        "核心影响：对普通人意味着什么",
        "实操建议：如何应对/利用这个趋势",
        "避坑指南：常见误区和注意事项",
        "未来展望：这个趋势会如何发展"
    ]
    
    reference_materials = [
        f"热点原文：{url}",
        "相关数据：行业报告、统计数据",
        "用户讨论：微博/知乎评论精选",
        "专家观点：行业大V的分析"
    ]
    
    result = {
        "topic_id": f"{source}_{topic_data.get('rank', 0)}",
        "original_title": title,
        "score": topic_data.get("scores", {}).get("total", 0),
        "theme_options": theme_options,
        "viewpoints": viewpoints,
        "reference_materials": reference_materials,
        "recommended_theme": theme_options[0],
        "prompt_for_ai": prompt  # 保存 prompt 供后续优化
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description="生成笔尖三要素")
    parser.add_argument("--scored-data", default="/tmp/scored_topics.json", help="打分后的选题数据")
    parser.add_argument("--account-style", default="墨云风格/专业实操", help="账号风格")
    parser.add_argument("--target-platform", default="公众号", help="目标平台")
    parser.add_argument("--top-n", type=int, default=3, help="生成前N个选题的三要素")
    
    args = parser.parse_args()
    
    # 读取打分数据
    with open(args.scored_data, 'r', encoding='utf-8') as f:
        scored_data = json.load(f)
    
    topics = scored_data.get("topics", [])[:args.top_n]
    
    # 生成三要素
    results = []
    for topic in topics:
        three_elements = generate_three_elements(
            topic,
            args.account_style,
            args.target_platform
        )
        results.append(three_elements)
    
    # 输出结果
    output = {
        "timestamp": scored_data.get("timestamp"),
        "total_generated": len(results),
        "topics": results
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    
    # 保存到文件
    output_file = "/tmp/three_elements.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 生成完成：{len(results)} 个选题的三要素", file=sys.stderr)
    print(f"数据已保存到：{output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
