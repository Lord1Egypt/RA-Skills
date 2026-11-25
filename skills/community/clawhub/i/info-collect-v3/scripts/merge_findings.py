#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把零散检索结果合并成一份可交付的情报 md（info-collect-v3）。

输入 findings.json 结构（字段均可缺省，缺了就少一节）：
{
  "task": {"question": "...", "subject": "...", "period": "...", "geo": ["..."], "granularity": "..."},
  "conclusions": [{"text": "...", "confidence": "确定|待验证", "basis": "依据强弱"}],
  "facts": [{"fact": "...", "value": "...", "source": "...", "time": "2026-09", "type": "事实|观点|推测"}],
  "sections": [{"dimension": "...", "points": ["...", "..."]}],
  "conflicts": [{"dimension": "...", "a": "...", "b": "...", "reason": "..."}],
  "gaps": [{"gap": "...", "why": "...", "impact": "高|中|低", "fix": "..."}],
  "sources": [{"name": "...", "type": "官方|行业|一手", "where": "URL 或位置", "time": "..."}]
}

用法：python3 scripts/merge_findings.py findings.json --out report.md [--title "..."]
"""
import argparse
import json
import sys

REQUIRED = ("source", "time")


def esc(v):
    return ("" if v is None else str(v)).replace("|", "／").replace("\n", " ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="情报整理报告")
    a = ap.parse_args()

    d = json.load(open(a.json_file, encoding="utf-8"))
    facts = d.get("facts") or []
    dead = [f for f in facts if not all(f.get(k) for k in REQUIRED)]
    task = d.get("task") or {}

    L = [f"# {a.title}", ""]
    if task:
        L += ["## 〇、情报任务书", "",
              f"- 决策问题：**{esc(task.get('question'))}**",
              f"- 主体：{esc(task.get('subject'))} ｜ 时间：{esc(task.get('period'))} ｜ 地域：{esc(', '.join(task.get('geo') or []))} ｜ 颗粒度：{esc(task.get('granularity'))}",
              ""]

    L += ["## 一、核心结论（先行）", ""]
    cons = d.get("conclusions") or []
    if cons:
        sure = [c for c in cons if c.get("confidence") == "确定"]
        guess = [c for c in cons if c.get("confidence") != "确定"]
        if sure:
            L.append("**确定性结论**")
            L += [f"{i+1}. {esc(c.get('text'))}" for i, c in enumerate(sure)]
            L.append("")
        if guess:
            L.append("**待验证推断（已标依据强弱）**")
            L += [f"{i+1}. {esc(c.get('text'))}（依据：{esc(c.get('basis') or '未标注')}）"
                  for i, c in enumerate(guess)]
            L.append("")
    else:
        L += ["（待补）", ""]

    L += ["## 二、关键事实表", "", "| # | 事实 | 数据/口径 | 来源 | 时间 | 性质 |",
          "|---|---|---|---|---|---|"]
    for i, f in enumerate(facts, 1):
        L.append(f"| {i} | {esc(f.get('fact'))} | {esc(f.get('value'))} | {esc(f.get('source'))} | "
                 f"{esc(f.get('time'))} | {esc(f.get('type') or '事实')} |")
    if not facts:
        L.append("| - | 待补 | | | | |")
    L.append("")

    secs = d.get("sections") or []
    if secs:
        L += ["## 三、分维度整理", ""]
        for s in secs:
            L.append(f"### {esc(s.get('dimension'))}")
            L += [f"- {esc(p)}" for p in (s.get("points") or [])]
            L.append("")

    L += ["## 四、矛盾数据并列", "", "| 维度 | 口径 A | 口径 B | 差异原因 |", "|---|---|---|---|"]
    confl = d.get("conflicts") or []
    for c in confl:
        L.append(f"| {esc(c.get('dimension'))} | {esc(c.get('a'))} | {esc(c.get('b'))} | {esc(c.get('reason'))} |")
    if not confl:
        L.append("| - | 未发现 | - | - |")
    L.append("")

    L += ["## 五、信息缺口（本报告最值钱的一节）", "",
          "| 缺口 | 为什么查不到 | 影响程度 | 补法 |", "|---|---|---|---|"]
    for g in d.get("gaps") or []:
        L.append(f"| {esc(g.get('gap'))} | {esc(g.get('why'))} | {esc(g.get('impact'))} | {esc(g.get('fix'))} |")
    if not d.get("gaps"):
        L.append("| 待补 | | | |")
    L.append("")

    L += ["## 六、来源清单", "", "| # | 来源 | 类型 | 链接/位置 | 时间 |", "|---|---|---|---|---|"]
    for i, s in enumerate(d.get("sources") or [], 1):
        L.append(f"| {i} | {esc(s.get('name'))} | {esc(s.get('type'))} | {esc(s.get('where'))} | {esc(s.get('time'))} |")
    if not d.get("sources"):
        L.append("| - | 待补 | | | |")
    L.append("")

    if dead:
        L += ["## 七、待补证据的事实（系统提示，交付前应清理）", "",
              "以下事实缺来源或时间，不符合\"可追溯\"要求：", ""]
        L += [f"- {esc(f.get('fact'))}（缺：{', '.join(k for k in REQUIRED if not f.get(k))}）" for f in dead]
        L.append("")

    L += ["> 本报告为决策辅助：结论基于所列公开来源，重大决策建议叠加实地核验。"]

    open(a.out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"已写入 {a.out}")
    if dead:
        print(f"⚠️ 有 {len(dead)} 条事实缺来源/时间，已在报告第七节标出", file=sys.stderr)


if __name__ == "__main__":
    main()
