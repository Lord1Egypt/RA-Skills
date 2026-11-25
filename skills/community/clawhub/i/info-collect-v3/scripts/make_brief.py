#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""情报任务书生成器（info-collect-v3）。

用法一（一次性给全）：
  python3 scripts/make_brief.py --question "要不要进示例行业（某区域宠物殡葬服务）" \
      --subject "示例行业：某区域宠物殡葬服务" --dimensions "市场规模,竞争格局,监管政策,渠道成本" \
      --period "近24个月" --geo "示例国全境,重点示例城市A" --granularity "行业+头部玩家" \
      --audience "决策层" --out brief.md

用法二（交互补全）：
  python3 scripts/make_brief.py --interactive --out brief.md
"""
import argparse
import datetime
import json
import sys


def ask(prompt, default=""):
    v = input(f"{prompt}{f'（默认 {default}）' if default else ''}: ").strip()
    return v or default


def build(args):
    dims = [d.strip() for d in (args.dimensions or "").split(",") if d.strip()]
    geos = [g.strip() for g in (args.geo or "").split(",") if g.strip()]
    return {
        "question": args.question,
        "subject": args.subject,
        "dimensions": dims,
        "period": args.period or "近 24 个月",
        "geo": geos,
        "granularity": args.granularity or "行业 + 头部玩家",
        "audience": args.audience or "决策层",
        "created": datetime.date.today().isoformat(),
    }


def render(b):
    dim_rows = "\n".join(
        f"| {i+1} | {d} | 待填：这个维度要回答什么 | 待填：可接受的数据来源 |"
        for i, d in enumerate(b["dimensions"]) or []
    ) or "| 1 | 待补 | | |"
    return f"""# 情报任务书

> 生成日期：{b['created']} ｜ 用途：锁定检索边界，防止跑偏

## 一、决策问题（先答这一条）

**{b['question']}**

- 这份情报给谁看：{b['audience']}
- 他要拿它做什么决定：待补（一句话）
- 如果查不到关键数据，退而求其次能给什么：待补

## 二、检索范围

| 项目 | 取值 |
|---|---|
| 主体 | {b['subject']} |
| 时间范围 | {b['period']} |
| 地域 | {', '.join(b['geo']) or '待补'} |
| 颗粒度 | {b['granularity']} |

## 三、维度拆解

| # | 维度 | 要回答的问题 | 首选来源类型 |
|---|---|---|---|
{dim_rows}

## 四、来源要求（写死，不许省）

1. 至少 **3 类来源交叉**：官方/权威（政策、公告、年报）＋行业（研报、协会、媒体）＋一手（访谈、现场、自有数据）；
2. 每个关键事实标"来源 + 时间 + 性质（事实/观点/推测）"；
3. 矛盾数据**并列呈现**，写明差异原因，不强行抹平；
4. 查不到的写进"缺口表"，**不许用推测补事实**。

## 五、交付形态

- 结论先行（3–5 条，确定性结论与待验证推断分列）
- 关键事实表（事实 / 数据口径 / 来源 / 时间 / 性质）
- 矛盾数据并列表
- 缺口表（缺口 / 为什么查不到 / 影响程度 / 补法）
- 来源清单（序号 / 来源 / 类型 / 链接或位置 / 时间）

## 六、开工前自检

- [ ] 决策问题能用一句话说清，且不是"了解一下"这类空目标
- [ ] 维度不超过 6 个（超过就是没想清）
- [ ] 时间范围写死到月
- [ ] 已确认哪些数据是"必须有"，哪些是"有更好"
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--question")
    ap.add_argument("--subject")
    ap.add_argument("--dimensions")
    ap.add_argument("--period")
    ap.add_argument("--geo")
    ap.add_argument("--granularity")
    ap.add_argument("--audience")
    ap.add_argument("--out", required=True)
    ap.add_argument("--interactive", action="store_true")
    ap.add_argument("--json", help="同时输出一份 JSON，供 merge_findings.py 复用")
    a = ap.parse_args()

    if a.interactive or not a.question:
        print("逐项填写，回车用默认值：")
        a.question = a.question or ask("决策问题（给谁、支持什么决定）")
        a.subject = a.subject or ask("调研主体")
        a.dimensions = a.dimensions or ask("维度（逗号分隔，≤6 个）")
        a.period = a.period or ask("时间范围", "近24个月")
        a.geo = a.geo or ask("地域（逗号分隔）")
        a.granularity = a.granularity or ask("颗粒度", "行业+头部玩家")
        a.audience = a.audience or ask("给谁看", "决策层")

    if not a.question or not a.subject:
        sys.exit("缺少必填：--question / --subject")

    b = build(a)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(render(b))
    print(f"任务书已写入 {a.out}")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(b, f, ensure_ascii=False, indent=2)
        print(f"任务书 JSON 已写入 {a.json}")


if __name__ == "__main__":
    main()
