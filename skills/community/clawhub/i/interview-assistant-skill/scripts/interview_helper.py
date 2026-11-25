#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""面试评估助手 - 离线评估脚本。

输入候选人简历、岗位 JD、面试记录，输出五维度结构化评估表（技术能力/
相关经验/沟通表达/文化匹配/潜力），并给出优势、风险与录用建议。

纯标准库实现，零第三方依赖。支撑 interview-assistant-skill 的"可独立运行"。
评分采用可解释的关键词信号统计，非黑盒模型。
"""

import argparse
import os
import re
import sys


# 各维度的正向 / 负向信号词（可解释启发式）
SIGNALS = {
    "技术能力": {
        "pos": ["扎实", "深入", "原理", "源码", "架构", "优化", "调试", "经验丰富", "熟练", "主导"],
        "neg": ["不清楚", "不了解", "不会", "模糊", "没接触", "回避"],
    },
    "相关经验": {
        "pos": ["同类项目", "同体量", "主导", "负责", "上线", "交付", "规模", "亿级", "千万级", "高并发"],
        "neg": ["无相关", "较少", "学生项目", "demo", "练习"],
    },
    "沟通表达": {
        "pos": ["逻辑清晰", "条理", "复述", "确认", "举例", "结构化", "表达清楚"],
        "neg": ["答非所问", "混乱", "绕", "词不达意"],
    },
    "文化匹配": {
        "pos": ["协作", "主动", "担责", "反馈", "透明", "复盘", "owner", "主人翁"],
        "neg": ["推诿", "甩锅", "指责", "被动"],
    },
    "潜力": {
        "pos": ["学习", "自驱", "成长", "钻研", "好奇", "开源", "博客", "认证", "获奖"],
        "neg": ["安于现状", "不想", "无所谓"],
    },
}


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def score_dimension(text, dim):
    cfg = SIGNALS[dim]
    pos = sum(text.count(w) for w in cfg["pos"])
    neg = sum(text.count(w) for w in cfg["neg"])
    # 基线 3 分，正向+0.5/个(上限+2)，负向-0.5/个(下限-2)
    raw = 3 + min(pos, 4) * 0.5 - min(neg, 4) * 0.5
    return max(1, min(5, round(raw)))


def verdict(scores):
    avg = sum(scores.values()) / len(scores)
    if avg >= 4.2:
        return "强烈推荐"
    if avg >= 3.5:
        return "推荐"
    if avg >= 2.8:
        return "待定（建议二面验证关键项）"
    return "不推荐"


def needs_verify(text):
    """返回标『待验证』的维度（信号偏弱）。"""
    out = []
    for dim in SIGNALS:
        pos = sum(text.count(w) for w in SIGNALS[dim]["pos"])
        neg = sum(text.count(w) for w in SIGNALS[dim]["neg"])
        if pos == 0 and neg == 0:
            out.append(dim)
    return out


def render(name, jd_text, resume_text, notes_text):
    dims = list(SIGNALS.keys())
    scores = {d: score_dimension(notes_text + " " + resume_text, d) for d in dims}

    lines = [f"# 面试评估表 · {name or '候选人'}", ""]
    lines.append("| 维度 | 评分(1-5) | 信号说明 |")
    lines.append("|------|----------|----------|")
    for d in dims:
        s = scores[d]
        bar = "★" * s + "☆" * (5 - s)
        lines.append(f"| {d} | {s} {bar} | 基于记录关键词信号 |")
    lines.append("")
    lines.append(f"**综合录用建议：{verdict(scores)}**")
    lines.append("")

    verify = needs_verify(notes_text)
    if verify:
        lines.append("## 待验证项（记录中缺少信号，建议二面重点考察）")
        for d in verify:
            lines.append(f"- {d}")
        lines.append("")

    # JD 关键词命中（简单匹配）
    jd_kw = re.findall(r"[一-龥]{2,4}", jd_text)
    jd_kw = [w for w in jd_kw if len(w) >= 2][:30]
    hit = [w for w in jd_kw if w in (resume_text + notes_text)]
    if hit:
        lines.append("## 岗位要求匹配（JD 关键词命中）")
        lines.append("、".join(sorted(set(hit))[:15]))
        lines.append("")

    lines.append("> 本表由 interview-assistant-skill 离线生成，评分基于可解释的关键词信号统计，仅供辅助决策，最终录用由人判断。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="面试评估助手")
    ap.add_argument("--resume", required=True)
    ap.add_argument("--jd", required=True)
    ap.add_argument("--notes", required=True)
    ap.add_argument("--output", default="评估表.md")
    ap.add_argument("--name", default="")
    args = ap.parse_args()

    for p in (args.resume, args.jd, args.notes):
        if not os.path.isfile(p):
            print(f"错误：文件不存在 {p}", file=sys.stderr)
            sys.exit(1)

    out = render(args.name, read_text(args.jd), read_text(args.resume), read_text(args.notes))
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"已生成评估表：{args.output}")


if __name__ == "__main__":
    main()
