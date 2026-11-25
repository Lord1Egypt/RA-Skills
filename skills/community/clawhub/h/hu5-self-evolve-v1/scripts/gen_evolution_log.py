#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""进化日志生成器：读取复盘 JSON → 输出 Markdown 进化日志。"""
import json, argparse, datetime

def build(d):
    task = d.get("task", "未命名任务")
    date = d.get("date") or datetime.date.today().strftime("%Y-%m-%d")
    did = d.get("did_right", [])
    pit = d.get("pitfalls", [])
    nxt = d.get("next_time", [])
    arts = d.get("artifacts", [])
    L = [f"# 进化日志 · {task}", "", f"> 日期：{date} ｜ 结论：本次沉淀 {len(did)} 条做法、{len(pit)} 条教训、{len(nxt)} 条改进", ""]
    L.append("## 一、做对了什么（可固化）")
    L += [f"- {x}" for x in did] or ["- （无）"]
    L.append("\n## 二、踩了什么坑（要记住）")
    L += [f"- {x}" for x in pit] or ["- （无）"]
    L.append("\n## 三、下次怎么更快（可执行）")
    L += [f"- {x}" for x in nxt] or ["- （无）"]
    if arts:
        L.append("\n## 四、本次产出")
        L += [f"- {x}" for x in arts]
    L += ["", "---", f"（由 hu5-self-evolve 生成 · {date}）"]
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--out", default=None)
    a = ap.parse_args()
    d = json.load(open(a.input, encoding="utf-8"))
    md = build(d)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(md)
        print("saved:", a.out)
    else:
        print(md)

if __name__ == "__main__":
    main()
