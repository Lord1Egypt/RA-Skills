#!/usr/bin/env python3
"""火一五小红书"案例苏格拉底学习" — 单案例对话式拆解。

为什么需要
==========
allen_method.md 里 11 案例 + jiaoxia_brand 等都是"看着学"。
看 ≠ 会。让用户先回答问题，再看老师答 — 是真正的"认知激活"。

工作模式
========
1. 选案例 → 读 frontmatter
2. 显示原文 / 范本
3. 抛 N 个苏格拉底问题，用户逐题回答（可以"我不知道"）
4. 给出范本解读 + 用户答案对比
5. 学习记录存 ~/.xiaohongshu/profile/case_studies.jsonl

LLM 增强（可选）
================
- 设置 XHS_LLM_PROVIDER=anthropic 后，对每个用户答案给个性化反馈
- 没设也能跑（直接给范本解读）

用法
----

    # 列所有案例
    python3 case_study.py list

    # 学某个案例（苏格拉底模式）
    python3 case_study.py study allen_lingqu

    # 直接看完整范本（跳过提问）
    python3 case_study.py show allen_lingqu

    # 找标签相关
    python3 case_study.py related 节气

    # 看自己的学习历史
    python3 case_study.py history
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore  # noqa: E402

try:
    import llm_helper
except ImportError:
    llm_helper = None  # type: ignore

_CASES_DIR = Path(__file__).resolve().parent.parent / "data" / "case_library"


# =====================================================================
# 案例文件解析
# =====================================================================


@dataclass
class CaseDoc:
    case_id: str
    title: str
    source: str
    date: str
    tags: List[str] = field(default_factory=list)
    key_techniques: List[str] = field(default_factory=list)
    raw: str = ""                                  # 全文
    sections: Dict[str, str] = field(default_factory=dict)
    questions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def parse_case(path: Path) -> Optional[CaseDoc]:
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None

    # 解析 YAML frontmatter
    fm = {}
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end > 0:
            fm_text = text[4:end]
            body = text[end + 5:]
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k, v = k.strip(), v.strip()
                    if v.startswith("[") and v.endswith("]"):
                        v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
                    fm[k] = v

    # 解析 sections（按 ## 分块）
    sections: Dict[str, str] = {}
    current_h = ""
    buf: List[str] = []
    for ln in body.splitlines():
        if ln.startswith("## "):
            if current_h:
                sections[current_h] = "\n".join(buf).strip()
            current_h = ln[3:].strip()
            buf = []
        else:
            buf.append(ln)
    if current_h:
        sections[current_h] = "\n".join(buf).strip()

    # 提取苏格拉底问题（从"苏格拉底问题"段提取数字开头的列表）
    q_section = ""
    for k in sections:
        if "苏格拉底" in k or "问题" in k:
            q_section = sections[k]
            break
    questions: List[str] = []
    if q_section:
        for ln in q_section.splitlines():
            ln = ln.strip()
            m = re.match(r"^\d+\.\s*\*?\*?(.+?)\*?\*?$", ln)
            if m:
                questions.append(m.group(1))

    return CaseDoc(
        case_id=fm.get("case_id", path.stem),
        title=fm.get("title", path.stem),
        source=fm.get("source", "?"),
        date=str(fm.get("date", "")),
        tags=list(fm.get("tags", [])),
        key_techniques=list(fm.get("key_techniques", [])),
        raw=text,
        sections=sections,
        questions=questions,
    )


def list_cases() -> List[CaseDoc]:
    cases: List[CaseDoc] = []
    for p in sorted(_CASES_DIR.glob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        c = parse_case(p)
        if c:
            cases.append(c)
    return cases


def find_case(case_id: str) -> Optional[CaseDoc]:
    # 精准匹配 → 后缀匹配
    direct = _CASES_DIR / f"{case_id}.md"
    if direct.exists():
        return parse_case(direct)
    # 模糊：找包含的
    candidates = [p for p in _CASES_DIR.glob("*.md") if case_id in p.stem]
    if len(candidates) == 1:
        return parse_case(candidates[0])
    if len(candidates) > 1:
        print(f"⚠️ 多个匹配：{[c.stem for c in candidates]}", file=sys.stderr)
    return None


# =====================================================================
# 历史
# =====================================================================


def append_history(store: ProfileStore, entry: Dict[str, Any]) -> None:
    p = store.root / "case_studies.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_history(store: ProfileStore) -> List[Dict[str, Any]]:
    p = store.root / "case_studies.jsonl"
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


# =====================================================================
# 子命令
# =====================================================================


def cmd_list(args: argparse.Namespace) -> int:
    cases = list_cases()
    if not cases:
        print("（案例库是空的，看 data/case_library/README.md）")
        return 0
    print(f"📚 案例库 — 共 {len(cases)} 个案例\n")
    by_source: Dict[str, List[CaseDoc]] = {}
    for c in cases:
        by_source.setdefault(c.source, []).append(c)
    for src, items in by_source.items():
        print(f"## {src}")
        for c in items:
            tags_brief = ", ".join(c.tags[:3]) if c.tags else "?"
            print(f"  • {c.case_id:<22} {c.title[:30]}  [{tags_brief}]")
        print()
    print("─" * 50)
    print("学习单个案例：python3 scripts/case_study.py study <case_id>")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    case = find_case(args.case_id)
    if not case:
        print(f"❌ 找不到案例 {args.case_id}", file=sys.stderr)
        return 1
    print(case.raw)
    return 0


def cmd_related(args: argparse.Namespace) -> int:
    cases = list_cases()
    keyword = args.keyword
    hits = [c for c in cases
            if keyword in c.title or keyword in " ".join(c.tags)
            or keyword in " ".join(c.key_techniques)]
    if not hits:
        print(f"（没找到与 '{keyword}' 相关的案例）")
        return 0
    print(f"🔍 与 '{keyword}' 相关的 {len(hits)} 个案例：\n")
    for c in hits:
        tags = ", ".join(c.tags)
        print(f"  • {c.case_id}  {c.title}  [{tags}]")
    return 0


def cmd_history(args: argparse.Namespace) -> int:
    store = ProfileStore()
    h = load_history(store)
    if not h:
        print("（你还没学过任何案例。先 `case_study.py study <case_id>`）")
        return 0
    by_case: Dict[str, int] = {}
    for r in h:
        by_case[r.get("case_id", "?")] = by_case.get(r.get("case_id", "?"), 0) + 1
    print(f"📚 你学过 {len(h)} 次（{len(by_case)} 个不同案例）：\n")
    for cid, n in sorted(by_case.items(), key=lambda x: -x[1]):
        print(f"  • {cid}  ({n} 次)")
    return 0


def _llm_feedback(case: CaseDoc, q: str, user_answer: str,
                  reference: str = "") -> str:
    if not llm_helper or not llm_helper.is_enabled() or not user_answer.strip():
        return ""
    prompt = (
        f"案例：{case.title}（{case.source}）\n"
        f"标签：{', '.join(case.tags)}\n"
        f"老师的问题：{q}\n"
        f"学生的回答：{user_answer}\n"
        f"范本视角：{reference[:500] if reference else '（暂无）'}\n\n"
        f"基于 Allen 文案体系（缓存里 allen_method.md），给一句话反馈："
        f"学生答得 '对在哪 / 缺在哪 / 离范本还差什么'。≤ 80 字，要中肯。"
    )
    text = llm_helper.call(prompt, tier="balanced",
                           cached_assets=["allen_method"], max_tokens=200)
    return text or ""


def cmd_study(args: argparse.Namespace) -> int:
    case = find_case(args.case_id)
    if not case:
        print(f"❌ 找不到案例 {args.case_id}", file=sys.stderr)
        print("跑 `case_study.py list` 看所有案例", file=sys.stderr)
        return 1

    store = ProfileStore()
    print("\n" + "📖" * 30)
    print(f"  案例学习：{case.title}")
    print(f"  来源：{case.source}    标签：{', '.join(case.tags)}")
    print("📖" * 30)
    print()

    # 显示原文 / 范本
    if "原文 / 范本" in case.sections:
        print("─" * 60)
        print("原文 / 范本")
        print("─" * 60)
        print(case.sections["原文 / 范本"])
        print()

    if not case.questions:
        print("⚠️ 这个案例没有定义苏格拉底问题（直接看范本解读）")
        if "范本解读（先回答上面再看）" in case.sections:
            print(case.sections["范本解读（先回答上面再看）"])
        elif "范本解读" in case.sections:
            print(case.sections["范本解读"])
        return 0

    # 苏格拉底问答
    print("─" * 60)
    print(f"🎓 进入苏格拉底学习模式（{len(case.questions)} 个问题）")
    print("─" * 60)
    print("规则：先你自己回答（可以'不知道'），再看老师答。")
    print()

    answers: List[Dict[str, Any]] = []
    for i, q in enumerate(case.questions, 1):
        print()
        print(f"❓ 问题 {i}/{len(case.questions)}：{q}")
        ans = input("  你的回答 > ").strip()
        if ans.lower() in ("skip", "跳过", ""):
            ans = "(跳过)"
        answers.append({"q": q, "a": ans})

        # LLM 即时反馈（可选）
        if not args.no_llm:
            fb = _llm_feedback(case, q, ans)
            if fb:
                print(f"  💡 反馈：{fb}")

    # 显示范本解读
    print()
    print("=" * 60)
    print("📚 范本解读（老师视角）")
    print("=" * 60)
    ref_section = ""
    for k in case.sections:
        if "范本解读" in k:
            ref_section = case.sections[k]
            break
    if ref_section:
        print(ref_section)
    else:
        print("（这个案例还没有写范本解读）")

    # 你能学到的
    if "你能学到的" in case.sections:
        print()
        print("─" * 60)
        print("📦 你能学到的")
        print("─" * 60)
        print(case.sections["你能学到的"])

    # 记录历史
    append_history(store, {
        "at": dt.datetime.now().isoformat(timespec="seconds"),
        "case_id": case.case_id,
        "title": case.title,
        "answers": answers,
    })
    print()
    print(f"✓ 已记录到 {store.root}/case_studies.jsonl")
    return 0


# =====================================================================
# 入口
# =====================================================================


def main() -> int:
    p = argparse.ArgumentParser(prog="case_study.py", description="案例苏格拉底学习")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="列所有案例").set_defaults(func=cmd_list)

    pst = sub.add_parser("study", help="学习一个案例（苏格拉底模式）")
    pst.add_argument("case_id")
    pst.add_argument("--no-llm", action="store_true")
    pst.set_defaults(func=cmd_study)

    psh = sub.add_parser("show", help="直接看完整范本")
    psh.add_argument("case_id")
    psh.set_defaults(func=cmd_show)

    pre = sub.add_parser("related", help="找相关案例")
    pre.add_argument("keyword")
    pre.set_defaults(func=cmd_related)

    sub.add_parser("history", help="看自己学过哪些").set_defaults(func=cmd_history)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
