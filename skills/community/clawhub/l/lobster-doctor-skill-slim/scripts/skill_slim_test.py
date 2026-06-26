#!/usr/bin/env python3
"""
skill_slim_test.py — 验证精简后的 description 是否影响技能匹配准确性

测试方法：模拟模型的技能匹配流程（关键词匹配），对比精简前后的匹配结果。
"""

import os
import re
import sys
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILL_DIRS = [
    Path.home() / ".npm-global" / "lib" / "node_modules" / "openclaw" / "skills",
    Path.home() / ".openclaw" / "skills",
    WORKSPACE / "skills",
]

CORE_SKILLS = {"lobster-doctor"}

# 模拟用户输入 + 期望匹配的技能
TEST_CASES = [
    ("帮我写一个 Python 爬虫", "coding-agent"),
    ("帮我发一条推特", "twitter-post"),
    ("今天天气怎么样", "weather"),
    ("搜索 Claude Code 最新动态", "web-search"),
    ("帮我看看这个 PDF", "pdf"),
    ("做个股票分析", "stock-analysis"),
    ("生成一张图片", "nano-banana-pro"),
    ("帮我检查 GitHub PR", "github"),
    ("写一篇博客文章", "blog-writer"),
    ("给这篇文章去掉AI味", "humanizer"),
    ("创建一个新技能", "skill-creator"),
    ("做市场调研", "market-research"),
    ("查看今天的热榜", "daily-trending"),
    ("帮我做品牌规范", "cs-brand-guidelines"),
    ("优化内容让 ChatGPT 引用", "cs-ai-seo"),
    ("追踪竞品价格变化", "competitor-intel-monitor"),
    ("总结这个网页", "summarize"),
    ("查询基金新闻", "fund-news-daily"),
    ("AI行业日报", "ai-news-zh"),
    ("清理一下 workspace", "lobster-doctor"),
    ("记录今天的支出", "expense-tracker-oc"),
    ("语音转文字", "openai-whisper"),
    ("生成字幕", "volcengine-ata-subtitle"),
    ("查询东方财富数据", "mx_data"),
    ("做个3D模型", "ai-3d-generation"),
    ("检查服务器安全", "healthcheck"),
    ("搜索记忆", "memory-tree"),
    ("管理通知", "sonoscli"),
    ("视频抽帧", "video-frames"),
    ("做个体检", "lobster-doctor"),
]


def parse_frontmatter(content):
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return None, None
    fm = fm_match.group(1)
    desc_match = re.search(r'^description:\s*(.+?)(?=\n^[a-z]|\n---|\Z)', fm, re.MULTILINE | re.DOTALL)
    if desc_match:
        raw = desc_match.group(1).strip().strip('"\'')
        raw = re.sub(r'^\s*>\s*', '', raw, flags=re.MULTILINE).strip()
        return None, re.sub(r'\s+', ' ', raw)
    return None, ""


def clean_description(raw_desc):
    """精简逻辑（和 skill_slim.py 一致）"""
    desc = raw_desc
    result_parts = []

    activate_match = re.search(r'Activate when user mentions?:\s*(.+?)(?:\.\s*$|\.\s*[A-Z])', desc)
    if activate_match:
        keywords = activate_match.group(1).strip().rstrip('.')
        result_parts.append(keywords)

    triggers_match = re.search(r'Trigger(?:s)? phrases?:\s*"(.+?)"', desc)
    if not triggers_match:
        triggers_match = re.search(r'Trigger(?:s)?:\s*"(.+?)"', desc)
    if triggers_match:
        result_parts.append(triggers_match.group(1).strip())

    not_for_match = re.search(r'NOT for:\s*(.+?)(?:\.\s|$)', desc)
    if not_for_match:
        result_parts.append(f"NOT for: {not_for_match.group(1).strip().rstrip('.')}")

    use_when_match = re.search(r'(?:Activates?|Use) when (?:the )?user mentions?:\s*(.+?)(?:\.\s|$)', desc)
    if use_when_match and not activate_match:
        result_parts.append(use_when_match.group(1).strip().rstrip('.'))

    if not result_parts:
        first_sentence = re.split(r'(?<=[.。])\s', desc)[0]
        if len(first_sentence) > 200:
            first_sentence = first_sentence[:200] + "..."
        result_parts.append(first_sentence)

    slim = " | ".join(result_parts)
    if len(slim) < 20:
        core = desc.split('.')[0] if '.' in desc else desc
        if len(core) > 200:
            core = core[:200] + "..."
        slim = core
    return slim


def simple_match_score(query, desc, name):
    """简单关键词匹配评分（模拟模型的粗筛）"""
    query_lower = query.lower()
    desc_lower = desc.lower()
    name_lower = name.lower()
    score = 0

    # 技能名直接匹配
    if any(word in name_lower for word in query_lower.split()):
        score += 10

    # description 中的关键词命中
    query_words = [w for w in query_lower.split() if len(w) > 1]
    for word in query_words:
        if word in desc_lower:
            score += 3

    # description 和 query 的公共子串
    for i in range(len(query_lower) - 1):
        bigram = query_lower[i:i+2]
        if bigram in desc_lower:
            score += 1

    return score


def scan_skills():
    skills = {}
    for d in SKILL_DIRS:
        if not d.exists():
            continue
        for name in sorted(os.listdir(d)):
            skill_path = d / name / "SKILL.md"
            if not skill_path.exists() or name in skills:
                continue
            try:
                with open(skill_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                _, raw_desc = parse_frontmatter(content)
                if raw_desc is not None:
                    skills[name] = {'desc': raw_desc, 'slim': clean_description(raw_desc)}
            except:
                pass
    return skills


def match_best(query, skills, use_slim=False):
    """找匹配度最高的技能"""
    best_name = None
    best_score = 0
    for name, info in skills.items():
        desc = info['slim'] if use_slim else info['desc']
        score = simple_match_score(query, desc, name)
        if score > best_score:
            best_score = score
            best_name = name
    return best_name


def main():
    print("🦞 龙虾医生 — 技能瘦身准确性测试\n")

    skills = scan_skills()
    print(f"加载 {len(skills)} 个技能，{len(TEST_CASES)} 个测试用例\n")

    correct_original = 0
    correct_slim = 0
    results = []

    for query, expected in TEST_CASES:
        orig_match = match_best(query, skills, use_slim=False)
        slim_match = match_best(query, skills, use_slim=True)

        orig_ok = (orig_match == expected)
        slim_ok = (slim_match == expected)

        if orig_ok:
            correct_original += 1
        if slim_ok:
            correct_slim += 1

        # 标记结果
        if orig_ok and slim_ok:
            status = "✅"
        elif orig_ok and not slim_ok:
            status = "⚠️ 精简后丢失"
        elif not orig_ok and slim_ok:
            status = "🆕 精简后反而对"
        else:
            status = "❌ 都不对"

        results.append((query, expected, orig_match, slim_match, status))

    # 输出结果
    print(f"{'输入':30s} {'期望':20s} {'原始匹配':20s} {'精简匹配':20s} 结果")
    print("─" * 95)

    regression = []
    for query, expected, orig, slim, status in results:
        if "丢失" in status or "不对" in status:
            regression.append((query, expected, orig, slim, status))
        print(f"{query:30s} {expected:20s} {orig or '(无)':20s} {slim or '(无)':20s} {status}")

    print("─" * 95)
    orig_rate = correct_original / len(TEST_CASES) * 100
    slim_rate = correct_slim / len(TEST_CASES) * 100
    print(f"\n📊 匹配准确率:")
    print(f"   原始: {correct_original}/{len(TEST_CASES)} ({orig_rate:.0f}%)")
    print(f"   精简: {correct_slim}/{len(TEST_CASES)} ({slim_rate:.0f}%)")
    print(f"   差异: {slim_rate - orig_rate:+.0f}%")

    if regression:
        print(f"\n⚠️ {len(regression)} 个回归用例需要人工确认:")
        for query, expected, orig, slim, status in regression:
            print(f"   {query}")
            print(f"     期望: {expected}, 原始: {orig}, 精简: {slim}")
            print(f"     精简desc: {skills[expected]['slim'][:100]}")
    else:
        print("\n✅ 无回归！精简后匹配准确率与原始一致。")


if __name__ == "__main__":
    main()
