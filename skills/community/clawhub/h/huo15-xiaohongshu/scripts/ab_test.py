#!/usr/bin/env python3
"""火一五小红书"同选题 A/B 测试" — 两版各发，看哪版赢。

为什么需要 A/B
==============
个人号最常见的纠结是"标题用 T2 还是 T3 / 首图选 X 还是 Y / 长版 vs 短版"。
猜没意义 — 同一周内分开 24~48 小时各发一版，让数据告诉你。

工作流
======
1. **plan**     — 给定主题，生成两版草稿（用不同公式 / 骨架）
2. **register** — 两版都发布完后，登记两个 note_id 到一个 ab 实验组
3. **compare**  — 拉双方快照，输出对比报告（哪版赢、赢在哪）

记录在 `~/.xiaohongshu/profile/ab_tests.jsonl`。

用法
----

    # 1) 计划
    python3 ab_test.py plan --topic "干皮护肤" --persona "30+ 干皮女生" \\
        --variant-a "T2,S1" --variant-b "T3,S6" --out-dir /tmp/ab1

    # 2) 两版分别发布完后登记
    python3 ab_test.py register --test-id ab_001 \\
        --note-a 64aaa... --xsec-a tokenA \\
        --note-b 64bbb... --xsec-b tokenB

    # 3) 比较（24~72h 后跑）
    python3 ab_test.py compare --test-id ab_001
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore  # noqa: E402
from xhs_writer import make_draft, save_draft  # noqa: E402


def ab_log_path(store: ProfileStore) -> Path:
    return store.root / "ab_tests.jsonl"


def load_ab(store: ProfileStore) -> List[Dict[str, Any]]:
    p = ab_log_path(store)
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def save_ab(store: ProfileStore, entries: List[Dict[str, Any]]) -> None:
    p = ab_log_path(store)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def _next_test_id(entries: List[Dict[str, Any]]) -> str:
    n = len(entries) + 1
    return f"ab_{n:03d}"


def _parse_variant(v: str) -> Dict[str, str]:
    """变体格式 'T2,S1' 或 'T3,S6'。"""
    parts = [p.strip() for p in v.split(",")]
    return {"formula": parts[0] if parts else "T2",
            "skeleton": parts[1] if len(parts) > 1 else "S1"}


# ---------- 子命令 ----------


def cmd_plan(args: argparse.Namespace) -> int:
    store = ProfileStore()
    profile = store.load_style()
    persona = args.persona or profile.persona
    payoff = args.payoff or ""
    tags = args.tags.split(",") if args.tags else profile.common_tags[:5]

    a = _parse_variant(args.variant_a)
    b = _parse_variant(args.variant_b)

    draft_a = make_draft(args.topic, persona=persona, payoff=payoff,
                        formula=a["formula"], skeleton=a["skeleton"], tags=tags)
    draft_b = make_draft(args.topic, persona=persona, payoff=payoff,
                        formula=b["formula"], skeleton=b["skeleton"], tags=tags)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path_a = out_dir / "variant_a.md"
    path_b = out_dir / "variant_b.md"
    save_draft(draft_a, str(path_a))
    save_draft(draft_b, str(path_b))

    entries = load_ab(store)
    test_id = _next_test_id(entries)
    entry = {
        "test_id": test_id,
        "topic": args.topic,
        "persona": persona,
        "payoff": payoff,
        "variants": {
            "A": {**a, "draft_path": str(path_a), "note_id": "", "xsec_token": ""},
            "B": {**b, "draft_path": str(path_b), "note_id": "", "xsec_token": ""},
        },
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "compared_at": "",
        "winner": "",
    }
    entries.append(entry)
    save_ab(store, entries)

    print(f"✓ A/B 实验 {test_id} 已创建")
    print(f"  主题：{args.topic}    受众：{persona}")
    print(f"  A：{a['formula']} + {a['skeleton']}  →  {path_a}")
    print(f"  B：{b['formula']} + {b['skeleton']}  →  {path_b}")
    print(f"\n下一步：")
    print(f"  1. 完善两版草稿、跑 polish/coach")
    print(f"  2. 间隔 24~48 小时分别发布")
    print(f"  3. python3 scripts/ab_test.py register --test-id {test_id} --note-a ... --note-b ...")
    return 0


def cmd_register(args: argparse.Namespace) -> int:
    store = ProfileStore()
    entries = load_ab(store)
    found = None
    for e in entries:
        if e["test_id"] == args.test_id:
            found = e
            break
    if not found:
        print(f"❌ 没有 test_id={args.test_id}", file=sys.stderr)
        return 1

    if args.note_a:
        found["variants"]["A"]["note_id"] = args.note_a
        found["variants"]["A"]["xsec_token"] = args.xsec_a or ""
        found["variants"]["A"]["published_at"] = dt.datetime.now().isoformat(timespec="seconds")
    if args.note_b:
        found["variants"]["B"]["note_id"] = args.note_b
        found["variants"]["B"]["xsec_token"] = args.xsec_b or ""
        found["variants"]["B"]["published_at"] = dt.datetime.now().isoformat(timespec="seconds")

    save_ab(store, entries)
    print(f"✓ 已登记 {args.test_id}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    store = ProfileStore()
    entries = load_ab(store)
    test = next((e for e in entries if e["test_id"] == args.test_id), None)
    if not test:
        print(f"❌ 没有 test_id={args.test_id}", file=sys.stderr)
        return 1
    a = test["variants"]["A"]
    b = test["variants"]["B"]
    if not (a.get("note_id") and b.get("note_id")):
        print("❌ 还有变体没登记 note_id", file=sys.stderr)
        return 1

    # 拉快照
    if not args.skip_snapshot:
        from xhs_client import XHSClient, load_cookie_from_env
        from xhs_parser import note_to_dict, parse_note_page
        try:
            client = XHSClient(cookie=load_cookie_from_env())
            for v in (a, b):
                html = client.get_explore_page(note_id=v["note_id"],
                                               xsec_token=v.get("xsec_token") or None)
                note = parse_note_page(html, note_id=v["note_id"])
                if note:
                    nd = note_to_dict(note)
                    v["latest_engagement"] = (nd["interactions"]["liked_count"]
                                              + nd["interactions"]["collected_count"]
                                              + nd["interactions"]["comment_count"])
                    v["liked"] = nd["interactions"]["liked_count"]
                    v["collected"] = nd["interactions"]["collected_count"]
                    v["comment"] = nd["interactions"]["comment_count"]
        except Exception as e:
            print(f"⚠️ 抓取失败，使用上次记录的快照（如有）：{e}", file=sys.stderr)

    # 比较
    eng_a = a.get("latest_engagement", 0)
    eng_b = b.get("latest_engagement", 0)
    winner = "A" if eng_a > eng_b else "B" if eng_b > eng_a else "TIE"
    test["winner"] = winner
    test["compared_at"] = dt.datetime.now().isoformat(timespec="seconds")
    save_ab(store, entries)

    print("=" * 50)
    print(f"🏆 A/B 实验 {args.test_id} 对比")
    print("=" * 50)
    print(f"  主题：{test['topic']}")
    print()
    print(f"  A [{a['formula']}+{a['skeleton']}]  互动 {eng_a}")
    print(f"     ({a.get('liked',0)}赞 / {a.get('collected',0)}藏 / {a.get('comment',0)}评)")
    print(f"  B [{b['formula']}+{b['skeleton']}]  互动 {eng_b}")
    print(f"     ({b.get('liked',0)}赞 / {b.get('collected',0)}藏 / {b.get('comment',0)}评)")
    print()
    if winner == "TIE":
        print("  → 两版表现相近，无明显差异")
    else:
        loser = "B" if winner == "A" else "A"
        loser_eng = eng_b if winner == "A" else eng_a
        winner_eng = eng_a if winner == "A" else eng_b
        gap = (winner_eng - loser_eng) / max(1, loser_eng) * 100
        print(f"  🏆 {winner} 胜出（互动高 {gap:.0f}%）")
        win = test["variants"][winner]
        print(f"     建议把 {win['formula']}+{win['skeleton']} 加入风格档案的 favorite_*")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    store = ProfileStore()
    entries = load_ab(store)
    if not entries:
        print("（还没有 A/B 实验）")
        return 0
    print("== A/B 实验历史 ==\n")
    for e in entries:
        a, b = e["variants"]["A"], e["variants"]["B"]
        status = e.get("winner") or ("待比较" if a.get("note_id") and b.get("note_id") else "起草中")
        print(f"  {e['test_id']}  [{e['topic'][:20]}]  "
              f"A={a['formula']}+{a['skeleton']}  B={b['formula']}+{b['skeleton']}  "
              f"→ {status}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="ab_test.py", description="同选题 A/B 测试")
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("plan", help="规划一个 A/B 实验")
    pp.add_argument("--topic", required=True)
    pp.add_argument("--persona", default="")
    pp.add_argument("--payoff", default="")
    pp.add_argument("--variant-a", required=True, help="变体 A：'T2,S1'")
    pp.add_argument("--variant-b", required=True, help="变体 B：'T3,S6'")
    pp.add_argument("--tags", default="")
    pp.add_argument("--out-dir", required=True)
    pp.set_defaults(func=cmd_plan)

    pr = sub.add_parser("register", help="登记两版 note_id")
    pr.add_argument("--test-id", required=True)
    pr.add_argument("--note-a", default="")
    pr.add_argument("--note-b", default="")
    pr.add_argument("--xsec-a", default="")
    pr.add_argument("--xsec-b", default="")
    pr.set_defaults(func=cmd_register)

    pc = sub.add_parser("compare", help="拉快照 + 输出对比")
    pc.add_argument("--test-id", required=True)
    pc.add_argument("--skip-snapshot", action="store_true",
                    help="不抓快照，用现有数据比较")
    pc.set_defaults(func=cmd_compare)

    pl = sub.add_parser("list", help="列出所有实验")
    pl.set_defaults(func=cmd_list)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
