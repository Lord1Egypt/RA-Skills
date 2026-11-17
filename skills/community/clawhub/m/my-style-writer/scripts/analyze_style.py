#!/usr/bin/env python3
"""
文章风格分析脚本 — 扫描 Markdown 文章库，提取写作风格特征。

用法:
  python scripts/analyze_style.py <文章库目录> <输出风格档案路径> [作者笔名] [发布平台]

- 文章库目录：技能目录下的 article-library/
- 输出路径：技能目录下的 references/style-profile.md
- 作者笔名（可选）：用于检测「用笔名自称」的风格特征，如「山哥」
- 发布平台（可选）：默认「公众号」，可传「知乎」「头条」等

示例（在技能根目录下运行）:
  python scripts/analyze_style.py article-library/ references/style-profile.md 山哥 公众号
"""

import sys
import os
import re
import json
from pathlib import Path
from collections import Counter
from datetime import datetime


def load_articles(article_dir: str) -> list[dict]:
    """加载文章库中所有 .md 文件，跳过 templates 子目录"""
    articles = []
    article_path = Path(article_dir)
    if not article_path.exists():
        print(f"[ERROR] 文章库目录不存在: {article_dir}")
        return articles

    for md_file in sorted(article_path.glob("*.md")):
        # 跳过 templates 子目录中的文件
        if "templates" in md_file.parts:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            articles.append({
                "filename": md_file.name,
                "path": str(md_file),
                "content": content,
                "lines": content.split("\n")
            })
            print(f"  [OK] 已加载: {md_file.name}")
        except Exception as e:
            print(f"  [SKIP] 无法读取 {md_file.name}: {e}")
    return articles


def extract_body_text(article: dict) -> str:
    """提取文章正文，跳过 YAML front matter 和元数据头"""
    content = article["content"]
    lines = content.split("\n")

    # 跳过 YAML front matter
    start_idx = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start_idx = i + 1
                break

    body_lines = []
    in_metadata = True
    for line in lines[start_idx:]:
        stripped = line.strip()
        # 跳过元数据行（格式: "- key: value" 或 "key: value"）
        if in_metadata and (stripped.startswith("- ") and ": " in stripped):
            continue
        if in_metadata and re.match(r'^[A-Za-z\u4e00-\u9fff]+[：:]', stripped):
            continue
        # 遇到 "## 正文" 标记后，开始提取正文
        if stripped == "## 正文" or stripped == "## 正文内容":
            in_metadata = False
            continue
        if stripped.startswith("##") and "正文" not in stripped:
            in_metadata = False
        if not in_metadata and stripped:
            body_lines.append(stripped)
    return "\n".join(body_lines)


def analyze_word_preferences(text: str) -> dict:
    """分析用词偏好"""
    # 分词（简单的前向最大匹配 + 标点处理）
    words = []
    # 使用正则提取中文词块
    chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
    all_chinese = ''.join(chinese_chars)

    # 统计 2-4 字词组频率
    bigrams = Counter()
    trigrams = Counter()
    for i in range(len(all_chinese) - 1):
        bigrams[all_chinese[i:i+2]] += 1
    for i in range(len(all_chinese) - 2):
        trigrams[all_chinese[i:i+3]] += 1

    # 高频词（top 30 有意义的）
    top_bigrams = [(w, c) for w, c in bigrams.most_common(100) if len(w) == 2 and c >= 2][:30]
    top_trigrams = [(w, c) for w, c in trigrams.most_common(50) if c >= 2][:15]

    # 检测惯用口语词
    colloquial_patterns = [
        "说实话", "说白了", "讲真", "其实", "反正", "确实",
        "真的", "根本", "完全", "绝对", "简直", "毕竟",
        "所谓", "无非", "说白了", "说穿了",
    ]
    colloquial_found = {}
    for pat in colloquial_patterns:
        count = text.count(pat)
        if count > 0:
            colloquial_found[pat] = count

    # 语气词检测
    tone_words = ["吧", "嘛", "呢", "啊", "哦", "哈", "呗", "呀", "喽"]
    tone_freq = {}
    for tw in tone_words:
        count = text.count(tw)
        if count > 0:
            tone_freq[tw] = count

    return {
        "top_bigrams": top_bigrams,
        "top_trigrams": top_trigrams,
        "colloquial_words": colloquial_found,
        "tone_words": tone_freq,
    }


def analyze_sentence_structure(text: str) -> dict:
    """分析句式结构"""
    # 分句
    sentences = re.split(r'[。！？!?\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 2]

    if not sentences:
        return {}

    lengths = [len(s) for s in sentences]
    avg_len = sum(lengths) / len(lengths)
    short_sentences = sum(1 for l in lengths if l <= 15)
    medium_sentences = sum(1 for l in lengths if 15 < l <= 40)
    long_sentences = sum(1 for l in lengths if l > 40)

    total = len(sentences)
    short_ratio = short_sentences / total if total > 0 else 0
    long_ratio = long_sentences / total if total > 0 else 0

    # 句式类型
    question_count = sum(1 for s in sentences if s.endswith("？") or s.endswith("?"))
    exclamation_count = sum(1 for s in sentences if s.endswith("！") or s.endswith("!"))
    rhetorical_q = len(re.findall(r'(难道|不是吗|对吧|是不是|对不对)', text))

    return {
        "sentence_count": total,
        "avg_length": round(avg_len, 1),
        "short_sentence_ratio": round(short_ratio, 2),
        "long_sentence_ratio": round(long_ratio, 2),
        "question_count": question_count,
        "exclamation_count": exclamation_count,
        "rhetorical_question_count": rhetorical_q,
        "style": "短句为主" if short_ratio > 0.5 else ("长句为主" if long_ratio > 0.3 else "长短结合"),
    }


def analyze_paragraph_rhythm(lines: list[str]) -> dict:
    """分析段落节奏"""
    # 过滤空行和标题行
    paragraphs = []
    current = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append("\n".join(current))
                current = []
        elif stripped.startswith("#"):
            if current:
                paragraphs.append("\n".join(current))
                current = []
            paragraphs.append(stripped)  # 标题算独立段落
        else:
            current.append(stripped)
    if current:
        paragraphs.append("\n".join(current))

    para_lengths = [len(p) for p in paragraphs if p]
    if not para_lengths:
        return {}

    avg_para_len = sum(para_lengths) / len(para_lengths)
    short_paras = sum(1 for l in para_lengths if l <= 80)
    medium_paras = sum(1 for l in para_lengths if 80 < l <= 200)
    long_paras = sum(1 for l in para_lengths if l > 200)

    return {
        "paragraph_count": len(paragraphs),
        "avg_paragraph_length": round(avg_para_len, 1),
        "short_paragraph_ratio": round(short_paras / len(paragraphs), 2) if paragraphs else 0,
        "long_paragraph_ratio": round(long_paras / len(paragraphs), 2) if paragraphs else 0,
        "rhythm": "短段落节奏" if short_paras / len(paragraphs) > 0.6 else "混合节奏",
    }


def analyze_emoji_usage(text: str) -> dict:
    """分析 emoji 使用模式"""
    emoji_pattern = re.compile(
        r'[\U0001F300-\U0001F9FF]|'  # 各种符号和象形文字
        r'[\U0001FA00-\U0001FA6F]|'  # 扩展
        r'[\U0001FA70-\U0001FAFF]|'  # 扩展
        r'[\u2600-\u27BF]|'          # 杂项符号
        r'[\u2B50\u2764\u2705\u274C\u26A0]'  # 常见 emoji
    )
    emojis = emoji_pattern.findall(text)
    emoji_counter = Counter(emojis)
    return {
        "total_emoji_count": len(emojis),
        "unique_emojis": len(emoji_counter),
        "top_emojis": emoji_counter.most_common(10),
        "sections_with_emoji": len(re.findall(r'[📌🔴🟢🔵🟡🟠🟣⚫⚪✅❌🔥💡🎯💰📊📈📉🚀⏰🎉]', text)),
        "pattern": "高密度使用" if len(emojis) > 15 else ("中等使用" if len(emojis) > 5 else "少量使用"),
    }


def analyze_structure(text: str) -> dict:
    """分析结构组织习惯"""
    # 标题编号方式
    chinese_numbering = len(re.findall(r'[一二三四五六七八九十]、', text))
    arabic_numbering = len(re.findall(r'\d[\.、]', text))
    roman_numbering = len(re.findall(r'[IVX]+[\.、]', text))

    # 是否有导语
    has_intro = bool(re.search(r'(导语|导读|先说|先聊|先说结论)', text))

    # 结尾特征
    has_cta = bool(re.search(r'(评论区|留言|点赞|在看|转发|关注|评论|聊聊)', text[-300:]))

    # 分段标记
    divider_count = len(re.findall(r'[━━─—…]{3,}|\*{3,}|-{3,}', text))

    return {
        "numbering_style": "中文数字" if chinese_numbering > arabic_numbering else "阿拉伯数字",
        "has_intro": has_intro,
        "has_cta_ending": has_cta,
        "divider_usage": "使用分隔线" if divider_count > 0 else "不使用分隔线",
        "section_count": len(re.findall(r'^#{1,3}\s', text, re.MULTILINE)),
    }


def analyze_person_usage(text: str, pen_name: str = "") -> dict:
    """分析人称使用。pen_name：作者笔名，用于检测「用笔名自称」特征"""
    first_person = text.count("我") + text.count("我们")
    second_person = text.count("你") + text.count("你们")
    # 避免重复计算"大家"
    collective = text.count("大家") + text.count("各位") + text.count("读者")

    total = first_person + second_person + collective

    # 笔名检测：优先使用传入的笔名，再兜底通用称谓（不写死任何具体人名）
    name_patterns = [p for p in (pen_name, "笔者", "我本人") if p]
    if name_patterns:
        name_re = "|".join(re.escape(p) for p in name_patterns)
        self_ref_style = "用笔名自称" if re.search(name_re, text) else "用「我」自称"
    else:
        self_ref_style = "用「我」自称"

    return {
        "first_person_count": first_person,
        "second_person_count": second_person,
        "collective_count": collective,
        "dominant_person": "第一人称为主" if first_person > second_person else "第二人称为主",
        "self_reference_style": self_ref_style,
    }


def generate_style_report(all_analyses: list[dict], articles: list[dict], platform: str = "公众号") -> str:
    """生成 Markdown 格式的风格档案。platform：主要发布平台，默认「公众号」"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 汇总分析结果
    report = f"""# 写作风格档案

## 基本信息
- 作者笔名：待填写
- 分析文章数：{len(articles)}
- 分析日期：{now}
- 主要发布平台：{platform}

## 风格定位
[基于分析自动推断，建议人工确认]

## 用词偏好

### 高频词汇
{_format_word_list(all_analyses)}

### 惯用口语
{_format_colloquial(all_analyses)}

### 语气词偏好
{_format_tone_words(all_analyses)}

## 句式结构
{_format_sentence_stats(all_analyses)}

## 段落节奏
{_format_paragraph_stats(all_analyses)}

## 语气语调
{_format_tone(all_analyses)}

## 修辞手法

### Emoji 使用模式
{_format_emoji(all_analyses)}

### 修辞偏好
[需人工分析：比喻、反问、设问、对比、列数据等]

## 结构组织
{_format_structure(all_analyses)}

## 情感表达
- 情感基调分布：[需人工分析]
- 金句密度：[需人工分析]

## 写作禁忌
- 应避免过度书面化的表达
- [需人工补充]

## 句式模板库

### 常用开头
[需人工提炼]

### 常用过渡
[需人工提炼]

### 常用结尾
[需人工提炼]

---

> 此档案由 `analyze_style.py` 自动生成，建议人工审查并标注需要调整的部分。
> 当文章库新增文章后，重新运行分析以更新此档案。
"""
    return report


def _format_word_list(analyses: list[dict]) -> str:
    lines = []
    for a in analyses:
        words = a.get("words", {})
        bigrams = words.get("top_bigrams", [])[:10]
        trigrams = words.get("top_trigrams", [])[:5]
    all_bigrams = Counter()
    all_trigrams = Counter()
    for a in analyses:
        words = a.get("words", {})
        for w, c in words.get("top_bigrams", []):
            all_bigrams[w] += c
        for w, c in words.get("top_trigrams", []):
            all_trigrams[w] += c

    if all_bigrams:
        lines.append("- 高频 2 字词：" + "、".join(f"「{w}」" for w, _ in all_bigrams.most_common(10)))
    if all_trigrams:
        lines.append("- 高频 3 字词：" + "、".join(f"「{w}」" for w, _ in all_trigrams.most_common(8)))
    return "\n".join(lines) if lines else "- [数据不足]"


def _format_colloquial(analyses: list[dict]) -> str:
    combined = Counter()
    for a in analyses:
        cw = a.get("words", {}).get("colloquial_words", {})
        for w, cnt in cw.items():
            combined[w] += cnt
    if combined:
        items = [f"「{w}」({c}次)" for w, c in combined.most_common(10)]
        return "- " + "、".join(items)
    return "- [数据不足]"


def _format_tone_words(analyses: list[dict]) -> str:
    combined = Counter()
    for a in analyses:
        tw = a.get("words", {}).get("tone_words", {})
        for w, cnt in tw.items():
            combined[w] += cnt
    if combined:
        items = [f"「{w}」({c}次)" for w, c in combined.most_common(8)]
        return "- " + "、".join(items)
    return "- [数据不足]"


def _format_sentence_stats(analyses: list[dict]) -> str:
    avg_lengths = [a["sentences"]["avg_length"] for a in analyses if a.get("sentences")]
    if not avg_lengths:
        return "- [数据不足]"
    avg = sum(avg_lengths) / len(avg_lengths)
    lines = [
        f"- 平均句长：{avg:.1f} 字",
    ]
    sample = analyses[0].get("sentences", {})
    if sample:
        lines.append(f"- 句式倾向：{sample.get('style', '未知')}")
        lines.append(f"- 短句占比：{sample.get('short_sentence_ratio', 0)*100:.0f}%")
        lines.append(f"- 反问句数：{sample.get('rhetorical_question_count', 0)} 处")
    return "\n".join(lines)


def _format_paragraph_stats(analyses: list[dict]) -> str:
    sample = analyses[0].get("paragraphs", {}) if analyses else {}
    if not sample:
        return "- [数据不足]"
    lines = [
        f"- 典型段落长度：{sample.get('avg_paragraph_length', 0):.0f} 字",
        f"- 节奏特点：{sample.get('rhythm', '未知')}",
    ]
    return "\n".join(lines)


def _format_tone(analyses: list[dict]) -> str:
    lines = []
    for a in analyses:
        pu = a.get("person_usage", {})
        if pu:
            lines.append(f"- 人称倾向：{pu.get('dominant_person', '未知')}")
            lines.append(f"- 自称方式：{pu.get('self_reference_style', '未知')}")
            break
    return "\n".join(lines) if lines else "- [数据不足]"


def _format_emoji(analyses: list[dict]) -> str:
    emojis = []
    for a in analyses:
        e = a.get("emoji", {})
        emojis.extend(e.get("top_emojis", []))
    combined = Counter()
    for em, cnt in emojis:
        combined[em] += cnt
    if combined:
        top = combined.most_common(10)
        return "- 常用 emoji：" + " ".join(f"{em}" for em, _ in top) + f"\n- 使用密度：{'高' if len(emojis) > 20 else '中'}"
    return "- [未检测到 emoji 使用]"


def _format_structure(analyses: list[dict]) -> str:
    sample = analyses[0].get("structure", {}) if analyses else {}
    if not sample:
        return "- [数据不足]"
    lines = [
        f"- 标题编号：{sample.get('numbering_style', '未知')}",
        f"- 是否有导语：{'是' if sample.get('has_intro') else '否'}",
        f"- 结尾 CTA：{'是' if sample.get('has_cta_ending') else '否'}",
        f"- 章节数量：{sample.get('section_count', 0)} 个",
    ]
    return "\n".join(lines)


def analyze_single_article(article: dict, pen_name: str = "") -> dict:
    """分析单篇文章"""
    body = extract_body_text(article)
    if len(body) < 100:
        print(f"  [WARN] {article['filename']}: 正文过短（{len(body)} 字），跳过分析")
        return {}

    return {
        "filename": article["filename"],
        "body_length": len(body),
        "words": analyze_word_preferences(body),
        "sentences": analyze_sentence_structure(body),
        "paragraphs": analyze_paragraph_rhythm(article["lines"]),
        "emoji": analyze_emoji_usage(body),
        "structure": analyze_structure(body),
        "person_usage": analyze_person_usage(body, pen_name),
    }


def main():
    if len(sys.argv) < 3:
        print("用法: python scripts/analyze_style.py <文章库目录> <输出风格档案路径> [作者笔名] [发布平台]")
        sys.exit(1)

    article_dir = sys.argv[1]
    output_path = sys.argv[2]
    pen_name = sys.argv[3] if len(sys.argv) > 3 else ""
    platform = sys.argv[4] if len(sys.argv) > 4 else "公众号"

    print("=" * 50)
    print("  文章风格分析器")
    print("=" * 50)

    # 1. 加载文章
    print("\n📖 加载文章库...")
    articles = load_articles(article_dir)
    if not articles:
        print("[ERROR] 未找到任何文章，请将 .md 文章放入文章库目录")
        sys.exit(1)
    print(f"共加载 {len(articles)} 篇文章")

    # 2. 逐篇分析
    print("\n🔍 分析中...")
    all_analyses = []
    for article in articles:
        print(f"  分析: {article['filename']}...")
        result = analyze_single_article(article, pen_name)
        if result:
            all_analyses.append(result)
            print(f"    → 正文 {result['body_length']} 字，平均句长 {result['sentences'].get('avg_length', 'N/A')} 字")

    if not all_analyses:
        print("[ERROR] 没有成功分析任何文章")
        sys.exit(1)

    # 3. 生成风格档案
    print("\n📝 生成风格档案...")
    report = generate_style_report(all_analyses, articles, platform)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report, encoding="utf-8")

    print(f"\n✅ 风格档案已保存至: {output_path}")
    print(f"   分析了 {len(all_analyses)} 篇文章")
    print("=" * 50)

    # 同时输出 JSON 摘要供程序使用
    json_path = output_file.parent / f"{output_file.stem}.json"
    json_data = {
        "analysis_date": datetime.now().isoformat(),
        "article_count": len(all_analyses),
        "articles": all_analyses,
    }
    json_path.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📊 详细数据已保存至: {json_path}")


if __name__ == "__main__":
    main()
