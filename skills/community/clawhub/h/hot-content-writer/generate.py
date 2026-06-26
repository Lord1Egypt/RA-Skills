#!/usr/bin/env python3
"""
✍️ 热点文案生成器 v1.0
输入热点话题，AI自动生成多平台爆款文案
"""

import argparse
import json
import sys
import os
import re
from datetime import datetime

# ============================================================
# 平台模板配置
# ============================================================

PLATFORMS = {
    "xiaohongshu": {
        "name": "小红书",
        "emoji": "📕",
        "max_words": 1000,
        "features": ["emoji丰富", "分段短小", "标题吸睛", "hashtag标签", "互动引导"],
        "structure": "标题hook → 痛点/场景 → 干货内容 → 互动结尾 → 标签"
    },
    "douyin": {
        "name": "抖音",
        "emoji": "🎵",
        "max_words": 500,
        "features": ["口语化", "节奏感强", "开头3秒抓人", "行动号召"],
        "structure": "爆点开头 → 内容主体 → 引导关注/互动"
    },
    "gongzhonghao": {
        "name": "公众号",
        "emoji": "💬",
        "max_words": 2000,
        "features": ["深度分析", "逻辑清晰", "排版美观", "引导分享"],
        "structure": "标题 → 引言 → 正文(小标题分段) → 总结 → 引导关注"
    },
    "weibo": {
        "name": "微博",
        "emoji": "📢",
        "max_words": 300,
        "features": ["短平快", "话题标签", "观点鲜明", "互动性强"],
        "structure": "观点/热点 → 简短评论 → 话题标签 → 互动提问"
    },
    "zhihu": {
        "name": "知乎",
        "emoji": "📖",
        "max_words": 1500,
        "features": ["专业深度", "数据支撑", "逻辑严谨", "个人经验"],
        "structure": "问题引入 → 分析论证 → 案例/数据 → 结论建议"
    }
}

# ============================================================
# 风格配置
# ============================================================

STYLES = {
    "professional": {
        "name": "专业干货",
        "emoji": "📊",
        "tone": "专业、权威、数据驱动，提供有价值的干货信息",
        "keywords": ["数据显示", "研究表明", "核心要点", "实操方法"]
    },
    "casual": {
        "name": "轻松种草",
        "emoji": "🌿",
        "tone": "轻松、亲切、像朋友推荐，有代入感",
        "keywords": ["强烈推荐", "亲测有效", "姐妹们", "必入"]
    },
    "funny": {
        "name": "幽默搞笑",
        "emoji": "😂",
        "tone": "幽默、有趣、有梗，让人看了想笑想转发",
        "keywords": ["笑死", "真实了", "破防了", "绝了"]
    },
    "emotional": {
        "name": "情感共鸣",
        "emoji": "💔",
        "tone": "走心、有温度、引发情感共鸣",
        "keywords": ["你有没有", "其实", "突然明白", "后来才发现"]
    },
    "controversial": {
        "name": "争议话题",
        "emoji": "🔥",
        "tone": "观点鲜明、有争议性、引发讨论",
        "keywords": ["说实话", "不接受反驳", "说真的", "扎心"]
    }
}

# ============================================================
# AI提示词生成
# ============================================================

def build_prompt(topic, platform, style, audience=None, word_count=None, versions=1):
    """构建AI生成提示词"""
    
    plat = PLATFORMS.get(platform, PLATFORMS["xiaohongshu"])
    sty = STYLES.get(style, STYLES["casual"])
    
    target_words = word_count or plat["max_words"]
    
    prompt = f"""你是一位资深自媒体运营专家，擅长创作爆款内容。请根据以下要求生成文案：

## 话题
{topic}

## 目标平台
{plat['emoji']} {plat['name']}

## 平台特点
- 最佳字数：{target_words}字左右
- 内容特点：{', '.join(plat['features'])}
- 内容结构：{plat['structure']}

## 文案风格
{sty['emoji']} {sty['name']}：{sty['tone']}
- 参考用语：{', '.join(sty['keywords'])}
"""

    if audience:
        prompt += f"\n## 目标人群\n{audience}\n"

    prompt += f"""
## 输出要求

请严格按以下JSON格式输出（{versions}个版本）：

```json
{{
  "titles": ["标题1", "标题2", "标题3"],
  "content": "完整文案内容",
  "hashtags": ["#标签1", "#标签2", "#标签3"],
  "tips": "发布建议（最佳时间、配图建议等）"
}}
```

## 注意事项
1. 标题要有吸引力，控制在20字以内
2. 内容要原创、有价值、有感染力
3. 适当使用emoji增加可读性
4. 标签选择热门且相关的
5. 符合{plat['name']}平台的内容调性
"""

    return prompt


def load_config():
    """从config.json加载配置"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    default = {
        "api_provider": "deepseek",
        "api_key": "",
        "api_base": "https://api.deepseek.com",
        "model": "deepseek-chat",
        "max_tokens": 2000,
        "temperature": 0.8
    }
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return {**default, **json.load(f)}
    except Exception:
        return default


def generate_with_api(prompt, api_key=None, api_base=None, model=None):
    """使用OpenAI兼容API生成内容"""
    try:
        import requests
    except ImportError:
        return None, "需要安装requests库: pip install requests"
    
    config = load_config()
    
    # 优先级：参数 > 环境变量 > config.json
    api_key = api_key or os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY") or config.get("api_key")
    api_base = api_base or os.environ.get("OPENAI_API_BASE") or config.get("api_base", "https://api.deepseek.com")
    model = model or os.environ.get("CONTENT_MODEL") or config.get("model", "deepseek-chat")
    max_tokens = config.get("max_tokens", 2000)
    temperature = config.get("temperature", 0.8)
    
    if not api_key:
        return None, "未配置API密钥！请在 config.json 中填入 api_key，或设置 DEEPSEEK_API_KEY 环境变量"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "你是一位资深自媒体运营专家，精通各平台爆款文案创作。输出必须是合法的JSON格式。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        resp = requests.post(f"{api_base}/chat/completions", headers=headers, json=data, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"]
        
        # 记录用量
        usage = result.get("usage", {})
        if usage:
            print(f"[API] 输入: {usage.get('prompt_tokens', '?')} tokens, 输出: {usage.get('completion_tokens', '?')} tokens", file=sys.stderr)
        
        return content, None
    except requests.exceptions.Timeout:
        return None, "API请求超时，请检查网络连接"
    except requests.exceptions.HTTPError as e:
        return None, f"API返回错误: {e.response.status_code} - {e.response.text[:200]}"
    except Exception as e:
        return None, f"API调用失败: {str(e)}"


def parse_ai_response(response_text):
    """解析AI返回的JSON"""
    # 尝试提取JSON代码块
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1)), None
        except json.JSONDecodeError:
            pass
    
    # 尝试直接解析
    try:
        return json.loads(response_text), None
    except json.JSONDecodeError:
        pass
    
    # 返回原始文本
    return {"raw_content": response_text}, "无法解析JSON，返回原始内容"


# ============================================================
# 模板生成（无API时的降级方案）
# ============================================================

def generate_from_template(topic, platform, style):
    """使用模板生成文案框架（不调用API）"""
    
    plat = PLATFORMS.get(platform, PLATFORMS["xiaohongshu"])
    sty = STYLES.get(style, STYLES["casual"])
    
    templates = {
        "xiaohongshu": {
            "casual": {
                "titles": [
                    f"🔥 {topic}！这个方法太绝了",
                    f"后悔没早知道！{topic}攻略来了",
                    f"姐妹们冲！{topic}我亲测有效"
                ],
                "content": f"姐妹们！！！\n\n今天必须跟你们聊聊{topic}！\n\n🌟 为什么重要？\n[此处填写原因]\n\n✅ 具体方法：\n1️⃣ [方法一]\n2️⃣ [方法二]\n3️⃣ [方法三]\n\n💡 小tips：\n[补充建议]\n\n用过的姐妹评论区举个手🙋‍♀️\n\n#{topic.replace(' ', '')} #干货分享 #必看",
                "hashtags": [f"#{topic.replace(' ', '')}", "#干货分享", "#必看"]
            }
        },
        "douyin": {
            "casual": {
                "titles": [
                    f"关于{topic}，90%的人都不知道！",
                    f"{topic}？看这一条就够了",
                    f"千万别再这样做了！{topic}正确方式"
                ],
                "content": f"家人们！\n\n{topic}这件事，\n我真的研究了好久！\n\n今天一次性告诉你们：\n\n👉 [核心观点1]\n👉 [核心观点2]\n👉 [核心观点3]\n\n记住这几点就够了！\n\n点赞收藏，下次找不到就亏了！",
                "hashtags": [f"#{topic.replace(' ', '')}", "#涨知识", "#抖音小助手"]
            }
        },
        "gongzhonghao": {
            "professional": {
                "titles": [
                    f"深度解析：{topic}",
                    f"{topic}——2026年最全指南",
                    f"关于{topic}，这篇文章说透了"
                ],
                "content": f"# {topic}\n\n## 引言\n\n[引出话题的重要性]\n\n## 一、背景分析\n\n[分析现状和趋势]\n\n## 二、核心要点\n\n### 2.1 [要点一]\n\n[详细说明]\n\n### 2.2 [要点二]\n\n[详细说明]\n\n## 三、实操建议\n\n1. [建议一]\n2. [建议二]\n3. [建议三]\n\n## 结语\n\n[总结升华]\n\n---\n*觉得有用的话，点个「在看」吧 👇*",
                "hashtags": []
            }
        },
        "weibo": {
            "casual": {
                "titles": [f"聊聊{topic}"],
                "content": f"【{topic}】\n\n[你的观点]\n\n你们怎么看？评论区聊聊👇\n\n#{topic.replace(' ', '')} #热门话题",
                "hashtags": [f"#{topic.replace(' ', '')}", "#热门话题"]
            }
        },
        "zhihu": {
            "professional": {
                "titles": [
                    f"如何评价{topic}？",
                    f"{topic}，有哪些值得关注的点？",
                    f"关于{topic}，你想知道的都在这里"
                ],
                "content": f"## {topic}\n\n谢邀。\n\n这个问题很有价值，我从以下几个角度来分析：\n\n### 一、现状分析\n\n[分析当前情况]\n\n### 二、核心观点\n\n1. **[观点一]**：[详细说明]\n2. **[观点二]**：[详细说明]\n3. **[观点三]**：[详细说明]\n\n### 三、个人建议\n\n[给出建议]\n\n### 总结\n\n[总结核心要点]\n\n---\n*以上仅为个人观点，欢迎讨论。*\n\n*觉得有帮助的话，点个赞吧 👍*",
                "hashtags": []
            }
        }
    }
    
    plat_templates = templates.get(platform, templates["xiaohongshu"])
    style_templates = plat_templates.get(style, list(plat_templates.values())[0])
    
    return {
        "topic": topic,
        "platform": plat["name"],
        "style": sty["name"],
        **style_templates,
        "word_count": len(style_templates["content"]),
        "generated_at": datetime.now().isoformat(),
        "note": "⚠️ 这是模板生成的框架，请根据实际情况填充内容。如需AI智能生成，请配置API密钥。"
    }


# ============================================================
# 热榜联动
# ============================================================

def get_hot_topics(source="all", top=3):
    """从热榜技能获取话题"""
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(skill_dir)
    
    sources = {
        "bilibili": os.path.join(workspace_dir, "bilibili-hot-daily", "fetch_hot.py"),
        "weibo": os.path.join(workspace_dir, "weibo-hot-daily", "fetch_hot.py"),
        "all": os.path.join(workspace_dir, "daily-hot-aggregator", "fetch_all.py")
    }
    
    script = sources.get(source, sources["all"])
    
    if not os.path.exists(script):
        return [], f"未找到热榜技能脚本: {script}"
    
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, script, "--top", str(top), "--format", "json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            topics = []
            for item in data.get("items", data if isinstance(data, list) else [])[:top]:
                title = item.get("title", item.get("name", ""))
                if title:
                    topics.append(title)
            return topics, None
        else:
            return [], f"热榜脚本执行失败: {result.stderr}"
    except Exception as e:
        return [], f"获取热榜失败: {str(e)}"


# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="✍️ 热点文案生成器 - AI自动生成多平台爆款文案",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--topic", "-t", type=str, help="话题/关键词")
    parser.add_argument("--platform", "-p", type=str, default="xiaohongshu",
                        choices=list(PLATFORMS.keys()),
                        help="目标平台 (默认: xiaohongshu)")
    parser.add_argument("--style", "-s", type=str, default="casual",
                        choices=list(STYLES.keys()),
                        help="文案风格 (默认: casual)")
    parser.add_argument("--all", "-a", action="store_true",
                        help="生成所有平台文案")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    parser.add_argument("--words", "-w", type=int, help="目标字数")
    parser.add_argument("--audience", type=str, help="目标人群")
    parser.add_argument("--versions", "-v", type=int, default=1, help="生成版本数")
    parser.add_argument("--titles-only", action="store_true", help="只生成标题")
    parser.add_argument("--from-hot", action="store_true", help="从热榜获取话题")
    parser.add_argument("--source", type=str, default="all",
                        choices=["all", "bilibili", "weibo"],
                        help="热榜来源 (默认: all)")
    parser.add_argument("--top", type=int, default=3, help="取热榜前N条")
    parser.add_argument("--api", action="store_true", help="使用API生成（需配置密钥）")
    parser.add_argument("--api-key", type=str, help="API密钥")
    parser.add_argument("--api-base", type=str, help="API地址")
    parser.add_argument("--model", type=str, help="模型名称")
    parser.add_argument("--prompt-only", action="store_true", help="只输出提示词，不生成")
    
    args = parser.parse_args()
    
    # 从热榜获取话题
    if args.from_hot:
        topics, err = get_hot_topics(args.source, args.top)
        if err:
            print(json.dumps({"error": err}, ensure_ascii=False, indent=2))
            sys.exit(1)
        if not topics:
            print(json.dumps({"error": "未获取到热榜话题"}, ensure_ascii=False, indent=2))
            sys.exit(1)
        
        results = []
        platforms = list(PLATFORMS.keys()) if args.all else [args.platform]
        
        for topic in topics[:args.top]:
            for platform in platforms:
                if args.api:
                    prompt = build_prompt(topic, platform, args.style, args.audience, args.words, args.versions)
                    if args.prompt_only:
                        results.append({"topic": topic, "platform": platform, "prompt": prompt})
                        continue
                    response, err = generate_with_api(prompt, args.api_key, args.api_base, args.model)
                    if err:
                        results.append({"topic": topic, "platform": platform, "error": err})
                    else:
                        parsed, parse_err = parse_ai_response(response)
                        results.append({
                            "topic": topic,
                            "platform": PLATFORMS[platform]["name"],
                            **parsed
                        })
                else:
                    results.append(generate_from_template(topic, platform, args.style))
        
        output = {"generated_at": datetime.now().isoformat(), "results": results}
    
    elif args.topic:
        platforms = list(PLATFORMS.keys()) if args.all else [args.platform]
        results = []
        
        for platform in platforms:
            if args.api:
                prompt = build_prompt(args.topic, platform, args.style, args.audience, args.words, args.versions)
                if args.prompt_only:
                    print(prompt)
                    return
                response, err = generate_with_api(prompt, args.api_key, args.api_base, args.model)
                if err:
                    results.append({"platform": platform, "error": err})
                else:
                    parsed, parse_err = parse_ai_response(response)
                    results.append({
                        "platform": PLATFORMS[platform]["name"],
                        **parsed
                    })
            else:
                results.append(generate_from_template(args.topic, platform, args.style))
        
        if args.titles_only and len(results) == 1:
            output = {"titles": results[0].get("titles", [])}
        elif len(results) == 1:
            output = results[0]
        else:
            output = {"topic": args.topic, "results": results}
    else:
        parser.print_help()
        sys.exit(1)
    
    # 输出结果
    json_output = json.dumps(output, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"✅ 已保存到 {args.output}")
    else:
        sys.stdout.buffer.write(json_output.encode("utf-8"))
        sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
