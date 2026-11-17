#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真书统计基线校准器 — 用 7700 本人手写小说算真实分布

用法:
  python calibrate_baselines.py --input "E:\你的真书目录" --output "output"

输出:
  - baselines.json      所有指标的统计数据
  - baselines_report.md 可读报告
  - samples.txt         抽样文本（供人工验证）
"""

import os
import re
import json
import sys
import math
import glob
from collections import Counter
from datetime import datetime

# ============ 配置 ============
# 每章最大读取字符数（完整覆盖一章）
MAX_CHAPTER_READ_BYTES = 100 * 1024
# 只处理 .txt 和 .md 文件
ALLOWED_EXTS = {".txt", ".md"}
# 每本书最多分析 3 章（开头/中间/结尾各一）
MAX_CHAPTERS_PER_BOOK = 3
# 统计采样上限（防止内存爆炸）
MAX_TOTAL_CHAPTERS = 30000


# ============ 统计指标 ============

STATS = {
    "total_files": 0,
    "total_chapters": 0,
    "total_chars": 0,
    "total_sentences": 0,
    "total_paragraphs": 0,
    "total_words": 0,  # 中文词（粗略分词）
    
    # 句长分布
    "sentence_length_chars": [],   # 每句汉字数
    "sentence_length_words": [],   # 每句词数
    
    # 段落分布
    "paragraph_length_sents": [],  # 每段句子数
    "paragraph_length_chars": [],  # 每段汉字数
    "single_sentence_paragraphs": 0,  # 单句段数量
    
    # 对话统计
    "dialogue_ratio": [],  # 每章的对话占比
    "dialogue_line_count": [],
    
    # 禁用词统计
    "ai_high_freq_words": {},  # 禁用词出现频率
    "ai_connectives": {},
    
    # 动作密度
    "verb_density": [],  # 每千字动作词数
    "action_verbs_per_1000chars": [],
    
    # 句式特征
    "long_sentence_ratio": [],   # >30字句占比
    "super_long_sentence_count": [],  # >50字句
    "dash_count_per_1000chars": [],
    "colon_count_per_1000chars": [],
    
    # 感官描写密度
    "sense_words_per_1000chars": [],
}

# 33个AI禁用词（来自 Humanizer-zh + oh-story banned-words）
AI_BANNED_WORDS = [
    "毋庸置疑", "不可否认", "值得一提的是", "总而言之", "众所周知",
    "命运的齿轮", "从某种意义上说", "在某种程度上", "显而易见",
    "由此可见", "综上所述", "不可忽视", "值得注意的是",
    "此外", "至关重要", "深入探讨", "强调", "持久的",
    "增强", "培养", "获得", "突出", "相互作用",
    "复杂", "关键", "格局", "证明", "宝贵",
    "充满活力", "深刻", "独特", "某种程度上",
    "首先", "其次", "最后", "因此", "不得不说",
]

# AI连接词（高频）
AI_CONNECTIVES = [
    "随着", "因此", "此外", "不仅", "而且",
    "同时", "总之", "由此可见", "所以说",
    "然而", "但是", "不过", "所以",
]

# 感官描写的触发词（中文）
SENSE_WORDS = [
    "看见", "听到", "闻到", "尝到", "触摸",
    "脚步声", "气味", "味道", "触感", "声音",
    "透过", "沿着", "光线", "温度", "手感",
]

# 动作动词（常用网文动作词）
ACTION_VERBS = [
    "攥", "握", "捏", "掐", "拧", "扯", "拽", "拉", "推", "抱",
    "踢", "踹", "踩", "踏", "蹲", "跪", "趴", "躺", "靠", "站",
    "转", "扭", "侧", "仰", "低", "抬", "歪", "点", "摇", "晃",
    "眯", "瞪", "瞥", "扫", "盯", "看", "望", "眨", "闭", "睁",
    "咬", "舔", "抿", "咧", "噘", "吸", "呼", "叹", "喘", "咽",
    "抖", "颤", "缩", "弓", "挺", "弯", "绷", "松", "僵", "软",
    "走", "跑", "跳", "冲", "退", "追", "躲", "闪", "钻", "爬",
    "摔", "砸", "扔", "丢", "接", "抓", "放", "拿", "摸", "敲",
]

# 引导对话的标点
QUOTE_PAIRS = [
    ("\u201c", "\u201d"),  # " "
    ("\u300c", "\u300d"),  # 「」
    ("\u2018", "\u2019"),  # ' '
    ("\uff62", "\uff63"),  # ｢ ｣
]


def is_chinese_char(ch):
    """判断是否为中文字符"""
    return '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf'


def extract_chinese_chars(text):
    """提取文本中的汉字"""
    return [ch for ch in text if is_chinese_char(ch)]


def extract_chinese_sentences(text):
    """按句号/感叹号/问号/省略号分割句子，返回句子列表"""
    sents = re.split(r'[。！？…\n]+', text)
    return [s.strip() for s in sents if len(extract_chinese_chars(s)) >= 2]


def extract_paragraphs(text):
    """按自然换行分割段落，过滤空段"""
    paras = [p.strip() for p in text.split('\n') if len(extract_chinese_chars(p)) >= 10]
    if not paras:
        # fallback: 每500字切一段，避免TXT无换行
        _chars = list(text)
        for i in range(0, len(_chars), 500):
            p = ''.join(_chars[i:i+500]).strip()
            if len(extract_chinese_chars(p)) >= 10:
                paras.append(p)
    return paras


def count_dialogue_chars(text):
    """统计对话字符数：引号对内的字符（不含引号本身）"""
    quote_pairs = [("\u201c","\u201d"),("\u300c","\u300d"),("\u2018","\u2019"),("\uff62","\uff63"),('"','"')]
    in_quote = None
    count = 0
    for ch in text:
        if in_quote:
            if ch == in_quote[1]:
                in_quote = None
            else:
                count += 1
        else:
            for op, cl in quote_pairs:
                if ch == op:
                    in_quote = (op, cl)
                    break
    return count


def analyze_chapter(text, filename=""):
    """分析单章文本，返回统计结果"""
    result = {}
    chinese_chars = extract_chinese_chars(text)
    total_chars = len(chinese_chars)
    
    if total_chars < 50:  # 太短的跳过
        return None
    
    # --- 句子级统计 ---
    sentences = extract_chinese_sentences(text)
    if not sentences:
        return None
    
    sent_lengths_chars = [len(extract_chinese_chars(s)) for s in sentences]
    sent_lengths_words = [max(1, s // 2) for s in sent_lengths_chars]  # 粗略
    
    # --- 段落级统计 ---
    paragraphs = extract_paragraphs(text)
    para_length_sents = []
    para_length_chars = []
    single_sent_paras = 0
    
    for p in paragraphs:
        p_sents = extract_chinese_sentences(p)
        p_chars = len(extract_chinese_chars(p))
        para_length_sents.append(len(p_sents))
        para_length_chars.append(p_chars)
        if len(p_sents) == 1:
            single_sent_paras += 1
    
    # --- 对话统计 ---
    dialogue_chars = count_dialogue_chars(text)
    dialogue_ratio = dialogue_chars / max(total_chars, 1)
    
    # --- 禁用词统计 ---
    banned_counts = {}
    for word in AI_BANNED_WORDS:
        c = text.count(word)
        if c > 0:
            banned_counts[word] = c
    
    connective_counts = {}
    for word in AI_CONNECTIVES:
        c = text.count(word)
        if c > 0:
            connective_counts[word] = c
    
    # --- 长句统计 ---
    long_sents = sum(1 for l in sent_lengths_chars if l > 30)
    super_long_sents = sum(1 for l in sent_lengths_chars if l > 50)
    
    # --- 标点 ---
    dash_count = text.count("——") + text.count("—") + text.count("--")
    colon_count = text.count("：")
    comma_count = text.count("，")
    period_count = text.count("。")
    exclamation_count = text.count("！")
    question_count = text.count("？")
    ellipsis_count = text.count("……")
    pause_count = text.count("、")
    semicolon_count = text.count("；")
    quote_count = text.count('\u201c') + text.count('\u300c') + text.count('\u2018') + text.count('\uff62')
    
    # --- 动作动词 ---
    verb_count = 0
    for v in ACTION_VERBS:
        verb_count += text.count(v)
    
    # --- 感官描写 ---
    sense_count = 0
    for w in SENSE_WORDS:
        sense_count += text.count(w)
    
    # --- 对话行数（含引号的行）---
    dialogue_lines = 0
    for line in text.split('\n'):
        if any(q in line for q in ['\u201c', '\u300c', '\u2018', '\uff62', '"']):
            dialogue_lines += 1
    
    result = {
        "chars": total_chars,
        "sentences": len(sentences),
        "paragraphs": len(paragraphs),
        "avg_sent_len_chars": sum(sent_lengths_chars) / max(len(sent_lengths_chars), 1),
        "avg_para_len_sents": sum(para_length_sents) / max(len(para_length_sents), 1),
        "avg_para_len_chars": sum(para_length_chars) / max(len(para_length_chars), 1),
        "sent_lengths_chars": sent_lengths_chars,
        "para_length_sents": para_length_sents,
        "single_sent_para_ratio": single_sent_paras / max(len(paragraphs), 1),
        "dialogue_ratio": dialogue_ratio,
        "dialogue_lines": dialogue_lines,
        "banned_words": banned_counts,
        "connectives": connective_counts,
        "long_sent_ratio": long_sents / max(len(sentences), 1),
        "super_long_count": super_long_sents,
        "dash_per_1000": dash_count / max(total_chars, 1) * 1000,
        "colon_per_1000": colon_count / max(total_chars, 1) * 1000,
        "verb_per_1000": verb_count / max(total_chars, 1) * 1000,
        "sense_per_1000": sense_count / max(total_chars, 1) * 1000,
        "comma_per_1000": comma_count / max(total_chars, 1) * 1000,
        "period_per_1000": period_count / max(total_chars, 1) * 1000,
        "exclamation_per_1000": exclamation_count / max(total_chars, 1) * 1000,
        "question_per_1000": question_count / max(total_chars, 1) * 1000,
        "ellipsis_per_1000": ellipsis_count / max(total_chars, 1) * 1000,
        "pause_per_1000": pause_count / max(total_chars, 1) * 1000,
        "semicolon_per_1000": semicolon_count / max(total_chars, 1) * 1000,
        "quote_per_1000": quote_count / max(total_chars, 1) * 1000,
        "comma_period_ratio": comma_count / max(period_count, 1),
        "excl_ques_per_1000": (exclamation_count + question_count) / max(total_chars, 1) * 1000,
    }
    return result


def compute_distribution(values):
    """计算一组数值的分布统计"""
    if not values:
        return {"min": 0, "max": 0, "mean": 0, "median": 0,
                "p5": 0, "p25": 0, "p75": 0, "p95": 0, "std": 0}
    
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mean = sum(sorted_vals) / n
    variance = sum((x - mean) ** 2 for x in sorted_vals) / n
    
    def percentile(p):
        idx = int(n * p / 100)
        return sorted_vals[min(idx, n - 1)]
    
    return {
        "min": round(sorted_vals[0], 2),
        "max": round(sorted_vals[-1], 2),
        "mean": round(mean, 2),
        "median": round(percentile(50), 2),
        "p5": round(percentile(5), 2),
        "p25": round(percentile(25), 2),
        "p75": round(percentile(75), 2),
        "p95": round(percentile(95), 2),
        "std": round(math.sqrt(variance), 2),
        "count": n,
    }


def scan_directory(root_dir):
    """扫描目录，找到所有 .txt 和 .md 文件"""
    files = []
    for ext in ALLOWED_EXTS:
        pattern = os.path.join(root_dir, "**", f"*{ext}")
        found = glob.glob(pattern, recursive=True)
        files.extend(found)
    
    # 过滤太大/太小的文件
    valid = []
    for f in files:
        try:
            size = os.path.getsize(f)
            if 500 <= size <= MAX_CHAPTER_READ_BYTES:
                valid.append(f)
        except OSError:
            continue
    
    return valid


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="真书统计基线校准器 — 用真人手写小说算真实分布"
    )
    parser.add_argument("--input", "-i", required=True,
                        help="小说目录路径")
    parser.add_argument("--output", "-o", default=".",
                        help="输出目录（默认当前目录）")
    parser.add_argument("--sample", action="store_true",
                        help="输出抽样文本用于人工验证")
    parser.add_argument("--genre", "-g", default="general",
                        help="小说类型标签（general/xianxia/dushi/yanqing/xuanyi 等），文件名会带上")
    parser.add_argument("--max-files", type=int, default=0,
                        help="最多处理的文件数（0=不限）")
    
    args = parser.parse_args()
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 扫描目录: {args.input}")
    all_files = scan_directory(args.input)
    print(f"  找到 {len(all_files)} 个有效文件")
    
    if args.max_files > 0:
        import random
        random.shuffle(all_files)
        all_files = all_files[:args.max_files]
        print(f"  抽样 {len(all_files)} 个文件")
    
    # 逐文件分析
    chapters_analyzed = 0
    all_results = []
    sample_texts = []
    
    for i, filepath in enumerate(all_files):
        if chapters_analyzed >= MAX_TOTAL_CHAPTERS:
            break
        
        try:
            with open(filepath, "rb") as rf:
                text = rf.read(MAX_CHAPTER_READ_BYTES).decode("gbk", errors="ignore")
        except Exception:
            continue
        
        result = analyze_chapter(text, os.path.basename(filepath))
        if result:
            all_results.append(result)
            chapters_analyzed += 1
            
            if args.sample and len(sample_texts) < 50:
                sample_texts.append({
                    "file": filepath,
                    "text": text[:300],
                    "stats": {k: result[k] for k in result 
                              if k not in ("sent_lengths_chars", "para_length_sents",
                                           "banned_words", "connectives")}
                })
        
        if (i + 1) % 500 == 0:
            print(f"  [{i+1}/{len(all_files)}] 已分析 {chapters_analyzed} 章")
    
    print(f"\n分析完成: {chapters_analyzed} 章")
    
    # 汇总统计
    print("\n=== 汇总统计 ===")
    
    baselines = {}
    
    # 连续值分布
    continuous_metrics = {
        "avg_sent_len_chars": "平均句长（汉字数）",
        "avg_para_len_sents": "平均段落句子数",
        "avg_para_len_chars": "平均段落汉字数",
        "single_sent_para_ratio": "单句段占比",
        "dialogue_ratio": "对话字符占比",
        "long_sent_ratio": "长句（>30字）占比",
        "super_long_count": "超长句（>50字）数",
        "dash_per_1000": "破折号密度（/千字）",
        "colon_per_1000": "冒号密度（/千字）",
        "verb_per_1000": "动作动词密度（/千字）",
        "sense_per_1000": "感官描写密度（/千字）",
        "comma_per_1000": "逗号密度（/千字）",
        "period_per_1000": "句号密度（/千字）",
        "exclamation_per_1000": "感叹号密度（/千字）",
        "question_per_1000": "问号密度（/千字）",
        "ellipsis_per_1000": "省略号密度（/千字）",
        "pause_per_1000": "顿号密度（/千字）",
        "semicolon_per_1000": "分号密度（/千字）",
        "quote_per_1000": "引号密度（/千字）",
        "comma_period_ratio": "逗号:句号比",
        "excl_ques_per_1000": "感叹号+问号密度（/千字）",
    }
    
    for key, label in continuous_metrics.items():
        values = [r[key] for r in all_results]
        dist = compute_distribution(values)
        baselines[key] = dist
        print(f"  {label}:")
        print(f"    均值={dist['mean']} 中位={dist['median']} "
              f"P5={dist['p5']} P25={dist['p25']} P75={dist['p75']} P95={dist['p95']}")
    
    # 禁用词统计
    print("\n  禁用词出现频率:")
    total_banned = Counter()
    for r in all_results:
        for w, c in r["banned_words"].items():
            total_banned[w] += c
    
    baselines["banned_word_freq"] = {}
    sorted_banned = sorted(total_banned.items(), key=lambda x: -x[1])
    for w, c in sorted_banned[:20]:
        rate = c / max(chapters_analyzed, 1)
        baselines["banned_word_freq"][w] = rate
        print(f"    {w}: {rate:.4f} 次/章 ({c} 次)")
    
    # 连接词统计
    print("\n  AI连接词出现频率:")
    total_conn = Counter()
    for r in all_results:
        for w, c in r["connectives"].items():
            total_conn[w] += c
    
    baselines["connective_freq"] = {}
    sorted_conn = sorted(total_conn.items(), key=lambda x: -x[1])
    for w, c in sorted_conn:
        rate = c / max(chapters_analyzed, 1)
        baselines["connective_freq"][w] = rate
        print(f"    {w}: {rate:.4f} 次/章 ({c} 次)")
    
    # 元数据
    baselines["meta"] = {
        "total_chapters": chapters_analyzed,
        "total_files_scanned": len(all_files),
        "scan_date": datetime.now().isoformat(),
        "source_dir": args.input,
        "genre": args.genre,
    }
    
    # 写入 JSON
    suffix = f"_{args.genre}" if args.genre != "general" else ""
    json_path = os.path.join(args.output, f"baselines{suffix}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(baselines, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 基线已保存: {json_path}")
    
    # 写入可读报告
    report_path = os.path.join(args.output, "baselines_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 真书统计基线报告\n\n")
        f.write(f"扫描日期: {baselines['meta']['scan_date']}\n")
        f.write(f"扫描目录: {baselines['meta']['source_dir']}\n")
        f.write(f"分析章节: {baselines['meta']['total_chapters']}\n")
        f.write(f"扫描文件: {baselines['meta']['total_files_scanned']}\n\n")
        
        f.write("## 核心指标\n\n")
        f.write("| 指标 | 均值 | 中位 | P5 | P25 | P75 | P95 | 标准差 |\n")
        f.write("|:-----|:----:|:----:|:--:|:---:|:---:|:---:|:-----:|\n")
        for key, label in continuous_metrics.items():
            d = baselines.get(key, {})
            f.write(f"| {label} | {d.get('mean', '-')} | {d.get('median', '-')} "
                    f"| {d.get('p5', '-')} | {d.get('p25', '-')} "
                    f"| {d.get('p75', '-')} | {d.get('p95', '-')} "
                    f"| {d.get('std', '-')} |\n")
        
        f.write("\n## 禁用词出现频率\n\n")
        f.write("| 词 | 次/章 |\n|:---|:----:|\n")
        for w, rate in sorted_banned[:20]:
            f.write(f"| {w} | {rate:.4f} |\n")
        
        # 标点统计见 baselines.json 的 punct_rates


        f.write("\n## AI连接词出现频率\n\n")
        f.write("| 词 | 次/章 |\n|:---|:----:|\n")
        for w, rate in sorted_conn:
            f.write(f"| {w} | {rate:.4f} |\n")
        
        f.write("\n## 校准建议\n\n")
        f.write("基于真实分布，建议调整以下检测阈值：\n\n")
        
        # 自动生成校准建议
        sent_mean = baselines.get("avg_sent_len_chars", {}).get("mean", 20)
        dash_mean = baselines.get("dash_per_1000", {}).get("mean", 0.5)
        single_mean = baselines.get("single_sent_para_ratio", {}).get("mean", 0.3)
        verb_mean = baselines.get("verb_per_1000", {}).get("mean", 30)
        comma_ratio = baselines.get("comma_period_ratio", {}).get("mean", 3.7)
        excl_ques = baselines.get("excl_ques_per_1000", {}).get("mean", 9.5)
        
        f.write(f"- **平均句长阈值**: 建议设为 {sent_mean:.1f}±{(sent_mean*0.3):.1f} 字\n")
        f.write(f"- **破折号密度阈值**: 建议设为 {dash_mean:.2f}/千字（超过此值可能AI味）\n")
        f.write(f"- **单句段占比**: 真书中位数 {single_mean:.1%}，偏离 ±15% 需注意\n")
        f.write(f"- **动作动词密度**: 真书均值 {verb_mean:.1f}/千字\n")
        f.write(f"- **逗号:句号比**: 真书 {comma_ratio:.1f}:1\n")
        f.write(f"- **感叹号+问号密度**: 真书 {excl_ques:.1f}/千字\n")

        # 标点特征表
        f.write("\n## 标点特征\n\n")
        f.write("| 比值 | 值 | AI嫌疑阈值 |\n")
        f.write("|:----|:--:|:----------:|\n")
        f.write(f"| 逗号:句号比 | {comma_ratio:.1f}:1 | < 2.0:1 或 > 6.0:1 |\n")
        f.write(f"| 感叹号+问号密度 | {excl_ques:.1f}/千字 | < 3.0/千字 |\n")
        f.write(f"| 破折号密度 | {dash_mean:.2f}/千字 | > {dash_mean*3:.2f}/千字 |\n")
        f.write(f"| 冒号密度 | {baselines.get('colon_per_1000', {}).get('mean', 0):.2f}/千字 | > 9.7/千字 |\n")
    
    print(f"✅ 报告已保存: {report_path}")
    
    # 可选：抽样文本
    if args.sample and sample_texts:
        sample_path = os.path.join(args.output, "samples.json")
        with open(sample_path, "w", encoding="utf-8") as f:
            json.dump(sample_texts[:50], f, ensure_ascii=False, indent=2)
        print(f"✅ 抽样文本已保存: {sample_path}")
    
    print("\n🎉 完成！")


if __name__ == "__main__":
    main()
