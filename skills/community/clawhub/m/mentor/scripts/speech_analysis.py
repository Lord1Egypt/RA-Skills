#!/usr/bin/env python3
"""
speech_analysis.py — 口语风格分析脚本
用法: python3 speech_analysis.py <字幕文本文件或目录> [--output <输出路径>]

分析维度:
  - 口头禅/高频词 TOP 15
  - 平均句长 + 句式分布
  - 语气词使用偏好
  - 填充词密度
  - 典型发言片段提取
"""

import re, json, sys, os
from collections import Counter

PATTERNS = {
    '就是': r'就是', '然后': r'然后', '这个': r'这个',
    '那个': r'那个', '其实': r'其实', '对': r'(?:^|[^反])对(?!不)',
    '嗯': r'嗯', '呃': r'呃', '特别': r'特别',
    '可能': r'可能', '反正': r'反正', '确实': r'确实',
    '我觉得': r'我觉得', '怎么说呢': r'怎么说呢',
    '所以': r'所以', '但是': r'但是', '比如说': r'比如说',
    '啊': r'(?:^|[^吗哈])啊', '吧': r'吧', '呢': r'呢',
    '哈哈': r'哈哈', '真的': r'真的', '感觉': r'感觉',
    '会': r'会[有是]', '蛮': r'蛮', '挺': r'挺',
}


def load_text(path):
    """加载文本文件或目录下所有 .txt 文件"""
    if os.path.isdir(path):
        texts = []
        for f in sorted(os.listdir(path)):
            if f.endswith('.txt'):
                with open(os.path.join(path, f), 'r', encoding='utf-8') as fh:
                    texts.append(fh.read())
        return '\n'.join(texts)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()


def analyze(text):
    """执行口语风格分析"""
    total_chars = len(text)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    total_lines = len(lines)

    if total_chars == 0 or total_lines == 0:
        return {"error": "文本为空"}

    # 口头禅统计
    phrase_counts = {}
    for word, pattern in PATTERNS.items():
        count = len(re.findall(pattern, text))
        if count > 0:
            phrase_counts[word] = {
                "count": count,
                "per_1k": round(count / (total_chars / 1000), 1)
            }

    # 排序
    top_phrases = dict(sorted(phrase_counts.items(), key=lambda x: -x[1]['count'])[:15])

    # 句式分析
    lengths = [len(l) for l in lines]
    avg_len = round(sum(lengths) / len(lengths), 1)
    short = sum(1 for l in lengths if l <= 5)
    medium = sum(1 for l in lengths if 5 < l <= 20)
    long = sum(1 for l in lengths if l > 20)

    sentence_distribution = {
        "avg_length": avg_len,
        "short_lte5": {"count": short, "pct": round(short / total_lines * 100)},
        "medium_6to20": {"count": medium, "pct": round(medium / total_lines * 100)},
        "long_gt20": {"count": long, "pct": round(long / total_lines * 100)},
    }

    # 提取典型片段
    interesting = []
    triggers = ['我觉得', '其实', '真的', '确实', '感觉', '怎么说', '说实话', '坦白说']
    for i, line in enumerate(lines):
        for t in triggers:
            if t in line and len(line) > 15 and len(interesting) < 10:
                ctx = line
                if i + 1 < len(lines):
                    ctx += " " + lines[i + 1]
                interesting.append(ctx[:150])
                break

    return {
        "total_chars": total_chars,
        "total_lines": total_lines,
        "top_phrases": top_phrases,
        "sentence_distribution": sentence_distribution,
        "sample_quotes": interesting,
    }


def print_report(result):
    """打印分析报告"""
    print(f"\n{'='*50}")
    print(f"口语风格分析报告")
    print(f"{'='*50}")
    print(f"文本量: {result['total_chars']} 字, {result['total_lines']} 行")

    print(f"\n📊 口头禅排行:")
    for word, data in result['top_phrases'].items():
        bar = '█' * min(int(data['per_1k'] * 3), 30)
        print(f"  {word:10s}: {data['count']:4d}次  ({data['per_1k']:>5.1f}/千字) {bar}")

    dist = result['sentence_distribution']
    print(f"\n📏 句式特征:")
    print(f"  平均句长: {dist['avg_length']} 字")
    print(f"  短句(≤5字):  {dist['short_lte5']['count']:4d} ({dist['short_lte5']['pct']}%)")
    print(f"  中句(6-20字): {dist['medium_6to20']['count']:4d} ({dist['medium_6to20']['pct']}%)")
    print(f"  长句(>20字):  {dist['long_gt20']['count']:4d} ({dist['long_gt20']['pct']}%)")

    if result.get('sample_quotes'):
        print(f"\n💬 典型发言:")
        for i, q in enumerate(result['sample_quotes'], 1):
            print(f"  {i}. 「{q}」")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 speech_analysis.py <文本文件或目录> [--output <json路径>]")
        sys.exit(1)

    text = load_text(sys.argv[1])
    result = analyze(text)

    print_report(result)

    # 可选输出JSON
    if '--output' in sys.argv:
        out_idx = sys.argv.index('--output') + 1
        if out_idx < len(sys.argv):
            with open(sys.argv[out_idx], 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 分析结果已保存到 {sys.argv[out_idx]}")
