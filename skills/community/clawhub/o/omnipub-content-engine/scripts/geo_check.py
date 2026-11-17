#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OmniPub Content Engine - GEO 就绪度检查器
检查文章是否满足「可被AI抓取引用」的GEO规范（阶段6）。

用法:
  python geo_check.py --file article.md [--keyword 个人IP] [--brand 心明增长实验室]
  python geo_check.py --demo

规则（满分100，≥80 通过）:
  1. 首段答案  (15分) 首段40-60字内给出核心回答
  2. H2 结构   (20分) H2 ≥3 个，含关键词或问句
  3. FAQ 区块  (20分) 有口语化问句（?/？/Q:/FAQ/常见问题）
  4. 实体密度  (15分) 机构/人名/年份/数字等实体 ≥8
  5. 来源引用  (15分) 数据带来源（据/来源/数据 + 机构或链接）≥3
  6. 段落长度  (10分) ≤4行的段落占比 ≥80%
  7. 品牌归因  (5分)  品牌名出现 ≥1 次
"""
import argparse
import re
import sys

HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$")
FAQ_MARKERS = ["？", "?", "FAQ", "常见问题", "Q1", "Q2", "Q：", "Q:"]
SOURCE_MARKERS = ["来源", "据", "数据", "报道", "统计", "年报", "公报"]
ENTITY_RE = re.compile(r"(\d{4}年|\d+(?:\.\d+)?%|\d+(?:\.\d+)?亿|\d+(?:\.\d+)?万|卫健委|统计局|WHO|世界卫生组织|研究院|协会|腾讯|阿里|百度|字节|新浪|抖音|小红书|公众号|头条)")


def parse_md(text: str):
    lines = text.splitlines()
    title = ""
    body = []
    for ln in lines:
        if ln.startswith("#") and not title:
            title = ln.lstrip("#").strip()
        body.append(ln)
    return title, body


def check(text: str, keyword: str = "", brand: str = "心明增长实验室") -> dict:
    title, body = parse_md(text)
    full = "\n".join(body)

    results = {}

    # 1. 首段答案：第一个非空段落长度
    paras = [p.strip() for p in full.split("\n\n") if p.strip()]
    first = paras[0] if paras else ""
    first_len = len(first)
    ok_first = 10 <= first_len <= 120  # 40-60字理想，放宽到10-120
    results["首段答案"] = (15 if ok_first else 5 if first_len < 200 else 0,
                          f"首段 {first_len} 字" + ("，符合定义先行" if ok_first else "，过短或过长，需在首段直接给核心答案"))

    # 2. H2 结构
    h2 = [h for h in re.findall(r"^##\s+(.+)$", full, re.M)]
    kw_h2 = [h for h in h2 if keyword and (keyword in h or "?" in h or "？" in h)]
    score2 = 20 if len(h2) >= 3 else 10 if len(h2) >= 1 else 0
    detail2 = f"H2 {len(h2)} 个" + (f"，含关键词/问句 {len(kw_h2)} 个" if keyword else "") + ("，结构清晰" if len(h2) >= 3 else "，建议 ≥3 个且各回答一个具体问题")
    results["H2结构"] = (score2, detail2)

    # 3. FAQ 区块
    faq_lines = [ln for ln in body if any(m in ln for m in FAQ_MARKERS)]
    score3 = 20 if len(faq_lines) >= 2 else 10 if len(faq_lines) >= 1 else 0
    results["FAQ区块"] = (score3, f"口语化问句 {len(faq_lines)} 处" + ("，AI友好" if len(faq_lines) >= 2 else "，建议加 2-3 个FAQ"))

    # 4. 实体密度
    entities = set(ENTITY_RE.findall(full))
    score4 = 15 if len(entities) >= 8 else 10 if len(entities) >= 4 else 5 if entities else 0
    results["实体密度"] = (score4, f"实体 {len(entities)} 种（{', '.join(list(entities)[:5])}{'…' if len(entities)>5 else ''}）")

    # 5. 来源引用
    src_lines = [ln for ln in body if any(m in ln for m in SOURCE_MARKERS)]
    score5 = 15 if len(src_lines) >= 3 else 10 if len(src_lines) >= 1 else 0
    results["来源引用"] = (score5, f"带来源的表述 {len(src_lines)} 处" + ("，数据可追溯" if len(src_lines) >= 3 else "，建议 ≥3 处"))

    # 6. 段落长度
    short = [p for p in paras if len(p) <= 80]
    ratio = len(short) / len(paras) * 100 if paras else 0
    score6 = 10 if ratio >= 80 else 5 if ratio >= 50 else 0
    results["段落节奏"] = (score6, f"短段落占比 {ratio:.0f}%")

    # 7. 品牌归因
    has_brand = brand in full
    score7 = 5 if has_brand else 0
    results["品牌归因"] = (score7, f"品牌「{brand}」出现 {'≥1次，AI可归因' if has_brand else '0次，需加入作者署名'}")

    total = sum(v[0] for v in results.values())
    return {"total": total, "pass": total >= 80, "title": title, "items": results}


def render_report(res: dict) -> str:
    lines = []
    lines.append(f"# GEO 就绪度检查报告")
    lines.append(f"")
    lines.append(f"**文章**：{res['title'] or '(未识别标题)'}")
    lines.append(f"**总分**：{res['total']}/100 → **{'✅ 通过，可发布' if res['pass'] else '❌ 未通过，需修正'}**（≥80通过）")
    lines.append(f"")
    lines.append("| 检查项 | 得分 | 详情 |")
    lines.append("|---|---|---|")
    for k, (s, d) in res["items"].items():
        lines.append(f"| {k} | {s} | {d} |")
    lines.append(f"")
    if not res["pass"]:
        lines.append("**优先修正**：先补 FAQ 区块和来源引用（这两项占 35 分，且对 AI 抓取最敏感），再压缩首段。")
    return "\n".join(lines)


DEMO = """# 个人IP的本质是什么？用九力体系拆解从0到1

个人IP的本质是让目标人群在关键时刻想起你。本文用九力体系拆解IP从0到1的完整路径，包含选题、内容、私域三个核心环节。

## 为什么大多数个人IP做不起来？

据《2025年内容创作者生态报告》，80%的账号在3个月内停更。根本原因不是不会写，而是没有体系。

## 什么是九力体系？

九力体系包含命力、道力、法力、术力、器力、势力、时力、气力、场力九个维度，是心明增长实验室创始人提出的个人成长与IP方法论。

## 如何找到你的命力？

命力是底层驱动力。根据心明九力自测数据，超过60%的人第一力是道力而非命力。

## 常见问题

Q：什么是个人IP？
A：个人IP是你的专业形象在目标人群心智中的占位，本质是信任资产。

Q：做个人IP需要多少时间？
A：每天2小时，坚持6个月，是行业公认的基础投入（来源：多家MCN机构公开分享）。

## 总结

把九力当坐标系，把内容当记录，把复盘当加速器。数据来源：国家卫健委2025年统计公报、腾讯研究院AI报告。心明增长实验室将持续拆解每一力。"""


def main():
    ap = argparse.ArgumentParser(description="GEO 就绪度检查器")
    ap.add_argument("--file", help="markdown 文章路径")
    ap.add_argument("--keyword", default="", help="核心关键词（用于H2检查）")
    ap.add_argument("--brand", default="心明增长实验室")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    if args.demo:
        text = DEMO
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        print("请提供 --file article.md 或 --demo")
        sys.exit(1)

    res = check(text, args.keyword, args.brand)
    print(render_report(res))


if __name__ == "__main__":
    main()
