#!/usr/bin/env python3
"""
weibo_style_analysis.py — 微博书面风格分析
用法: python3 weibo_style_analysis.py <微博JSON文件> [--output <输出路径>]

分析维度:
  - 帖子长度分布
  - 标点符号使用频率（感叹号/问号/省略号）
  - emoji 使用习惯
  - 团队代发 vs 本人发言分类
  - 高频用词/表达
  - 书面风格画像生成
"""

import re, json, sys, os, argparse
from collections import Counter


# 广告/代言关键词
AD_KEYWORDS = [
    '旗舰店', '天猫', '京东', '全球代言', '品牌代言', '品牌大使', '品牌挚友',
    '品牌好友', '代言人', '官方旗舰', '官方直播', '购买链接', '戳链接',
    '限时优惠', '折扣', '同款', '上新', '新品发售'
]

# 团队代发线索词
TEAM_PATTERNS = [
    r'#\S+#.*@\S+.*#\S+#',  # 多个hashtag + @搭档
    r'全球品牌', r'品牌全球', r'荣誉出席',
    r'很高兴成为', r'很荣幸成为', r'很开心受邀',
]


def classify_post(post):
    """分类: personal / ad / team / repost"""
    text = post.get('text', '')

    if not post.get('is_original', True):
        return 'repost'

    # 广告检测
    for kw in AD_KEYWORDS:
        if kw in text:
            return 'ad'

    # 团队代发检测
    for pat in TEAM_PATTERNS:
        if re.search(pat, text):
            return 'team'

    # 短文本 + 口语化 = 大概率本人
    if len(text) < 30:
        return 'personal'

    # 含多个品牌hashtag
    hashtags = re.findall(r'#([^#]+)#', text)
    brand_tags = [h for h in hashtags if any(kw in h for kw in ['代言', '品牌', '旗舰', '官方'])]
    if len(brand_tags) >= 2:
        return 'team'

    return 'personal'


def analyze_weibo_style(posts):
    """微博书面风格分析"""

    # 分类
    categories = {'personal': [], 'ad': [], 'team': [], 'repost': []}
    for p in posts:
        cat = classify_post(p)
        categories[cat].append(p)

    personal = categories['personal']
    if not personal:
        return {"error": "没有找到个人微博（全部是广告/团队/转发）"}

    all_text = '\n'.join(p['text'] for p in personal)
    total_chars = len(all_text)

    # 帖子长度分析
    lengths = [len(p['text']) for p in personal]
    avg_len = sum(lengths) / len(lengths)
    short = sum(1 for l in lengths if l < 30)      # 短微博
    medium = sum(1 for l in lengths if 30 <= l < 100)  # 中等
    long = sum(1 for l in lengths if l >= 100)      # 长微博

    # 标点分析
    excl = all_text.count('！') + all_text.count('!')
    ques = all_text.count('？') + all_text.count('?')
    ellipsis = all_text.count('…') + all_text.count('...')
    period = all_text.count('。')

    # emoji分析
    emoji_pattern = re.compile(
        "[\U0001F300-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0\U0000FE00-\U0000FE0F\U0001F1E0-\U0001F1FF]"
    )
    emojis = emoji_pattern.findall(all_text)
    emoji_count = len(emojis)
    emoji_freq = Counter(emojis)

    # 高频词（2字以上）
    words_2 = re.findall(r'[\u4e00-\u9fff]{2,4}', all_text)
    word_freq = Counter(words_2).most_common(20)

    # 特殊表达
    multi_excl = len(re.findall(r'[！!]{2,}', all_text))  # 连续感叹号
    haha = len(re.findall(r'哈{2,}', all_text))
    repeated_chars = len(re.findall(r'(.)\1{2,}', all_text))  # 重复字符 aaa

    result = {
        "total_posts": len(posts),
        "classification": {
            "personal": len(personal),
            "ad": len(categories['ad']),
            "team": len(categories['team']),
            "repost": len(categories['repost']),
            "personal_ratio": f"{len(personal)/len(posts)*100:.0f}%"
        },
        "post_length": {
            "avg": round(avg_len, 1),
            "short_lt30": {"count": short, "pct": f"{short/len(personal)*100:.0f}%"},
            "medium_30to100": {"count": medium, "pct": f"{medium/len(personal)*100:.0f}%"},
            "long_gte100": {"count": long, "pct": f"{long/len(personal)*100:.0f}%"},
        },
        "punctuation": {
            "exclamation": {"count": excl, "per_1k": round(excl/(total_chars/1000), 1) if total_chars > 0 else 0},
            "question": {"count": ques, "per_1k": round(ques/(total_chars/1000), 1) if total_chars > 0 else 0},
            "ellipsis": {"count": ellipsis},
            "period": {"count": period},
            "multi_exclamation": multi_excl,  # "！！！" 这种
        },
        "emoji": {
            "total": emoji_count,
            "per_post": round(emoji_count/len(personal), 2) if personal else 0,
            "top_5": dict(emoji_freq.most_common(5)),
        },
        "expression_habits": {
            "haha_count": haha,
            "repeated_chars": repeated_chars,
        },
        "top_words": word_freq[:15],
        "sample_personal_posts": [p['text'][:150] for p in personal if len(p['text']) > 5][:10],
    }

    return result


def print_report(result):
    """打印分析报告"""
    print(f"\n{'='*50}")
    print(f"微博书面风格分析报告")
    print(f"{'='*50}")

    c = result['classification']
    print(f"\n📊 帖子分类: 总{result['total_posts']}条")
    print(f"  ✅ 个人发言: {c['personal']} ({c['personal_ratio']})")
    print(f"  📢 广告代言: {c['ad']}")
    print(f"  👥 团队代发: {c['team']}")
    print(f"  🔄 转发: {c['repost']}")

    pl = result['post_length']
    print(f"\n📏 帖子长度:")
    print(f"  平均: {pl['avg']} 字")
    print(f"  短(<30字): {pl['short_lt30']['count']} ({pl['short_lt30']['pct']})")
    print(f"  中(30-100字): {pl['medium_30to100']['count']} ({pl['medium_30to100']['pct']})")
    print(f"  长(≥100字): {pl['long_gte100']['count']} ({pl['long_gte100']['pct']})")

    p = result['punctuation']
    print(f"\n✏️ 标点风格:")
    print(f"  感叹号: {p['exclamation']['count']}次 ({p['exclamation']['per_1k']}/千字)")
    print(f"  问号: {p['question']['count']}次 ({p['question']['per_1k']}/千字)")
    print(f"  省略号: {p['ellipsis']['count']}次")
    print(f"  连续感叹号(！！！): {p['multi_exclamation']}次")

    e = result['emoji']
    print(f"\n😊 emoji:")
    print(f"  总使用: {e['total']}次 (平均{e['per_post']}/条)")
    if e['top_5']:
        print(f"  TOP 5: {' '.join(f'{k}({v})' for k,v in e['top_5'].items())}")

    print(f"\n💬 个人微博示例:")
    for i, s in enumerate(result['sample_personal_posts'][:5], 1):
        print(f"  {i}. 「{s}」")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='微博书面风格分析')
    parser.add_argument('input', help='微博JSON文件路径')
    parser.add_argument('--output', default=None, help='输出JSON路径')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        posts = json.load(f)

    result = analyze_weibo_style(posts)
    print_report(result)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 分析结果已保存到 {args.output}")
