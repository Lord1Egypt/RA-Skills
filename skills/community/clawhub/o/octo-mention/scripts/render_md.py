#!/usr/bin/env python3
"""octo-mention 人类可读汇总生成器

从 persons.json (octo-mention.persons.v1) 生成 Markdown 汇总，保持 JSON/MD 同步。

用法:
  python3 render_md.py --in openclaw.json --out openclaw.md
"""
import argparse, json


def render(data):
    persons = data.get("persons", {})
    lines = []
    lines.append("# 群成员昵称映射汇总（跨群按人）")
    lines.append("")
    lines.append(f"> schema: {data.get('schema')} | version: {data.get('version')} | "
                 f"updated: {data.get('last_updated')} | persons: {len(persons)}")
    lines.append("")

    humans = {u: p for u, p in persons.items() if p.get("member_type") == "human"}
    bots = {u: p for u, p in persons.items() if p.get("member_type") == "bot"}
    others = {u: p for u, p in persons.items()
              if p.get("member_type") not in ("human", "bot")}

    def emit(p):
        name = p.get("canonical_name") or p.get("uid")
        lines.append(f"## {name}")
        meta = f"uid: `{p['uid']}` | 类型: {p.get('member_type','?')}"
        if p.get("owner"):
            meta += f" | 主人: {p['owner']}"
        if p.get("owns_bots"):
            meta += f" | 拥有bot: {', '.join(p['owns_bots'])}"
        lines.append(meta)
        sg = p.get("seen_in_groups", [])
        lines.append(f"出现群数: {len(sg)}")
        aliases = p.get("aliases", [])
        if aliases:
            lines.append("")
            lines.append("| 称呼 | 类型 | 置信度 | 证据数 | 跨群数 | 说明 |")
            lines.append("|---|---|---:|---:|---:|---|")
            for a in sorted(aliases, key=lambda x: -x.get("confidence", 0)):
                lines.append(
                    f"| {a['alias']} | {a.get('alias_type','')} | "
                    f"{a.get('confidence','')} | {a.get('evidence_count','')} | "
                    f"{len(a.get('groups',[]))} | {a.get('reason','')} |"
                )
        ua = p.get("uncertain_aliases", [])
        if ua:
            lines.append("")
            lines.append("低置信候选: " + ", ".join(
                f"{a['alias']}({a.get('confidence','?')})" for a in ua))
        cf = p.get("conflicts", [])
        if cf:
            lines.append("")
            for c in cf:
                lines.append(f"⚠️ 冲突: {c.get('reason', json.dumps(c, ensure_ascii=False))}")
        lines.append("")

    if humans:
        lines.append("# 人类成员")
        lines.append("")
        for p in humans.values():
            emit(p)
    if bots:
        lines.append("# 机器人成员")
        lines.append("")
        for p in bots.values():
            emit(p)
    if others:
        lines.append("# 类型存疑")
        lines.append("")
        for p in others.values():
            emit(p)

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    data = json.load(open(args.inp, encoding="utf-8"))
    md = render(data)
    open(args.out, "w", encoding="utf-8").write(md)
    print(f"rendered -> {args.out} ({len(md)} chars)")


if __name__ == "__main__":
    main()
