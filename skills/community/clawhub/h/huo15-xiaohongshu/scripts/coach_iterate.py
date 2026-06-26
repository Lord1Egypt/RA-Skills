#!/usr/bin/env python3
"""火一五小红书"渐进式教练" — 一次只 focus 一维。

为什么这是必要的
================
Allen 给贾维斯的最终评价：**「认知到位了，输出还没跟上」**。
看出问题 ≠ 写得出来。critique 一次给 6 维全反馈 = 信息过载，用户不知道先改哪。

`coach_iterate` 把"诊断报告"改成"教练课"：
1. 跑一次扫描，挑出**当前最差的一维**作为 focus
2. 只针对这一维给 (what, why, how, example) 四件套
3. 用户改完后跑同一命令 → 自动对比该维分数变化
4. 升了 → 给下一维 / 没升 → 同一维继续追问 + 换个角度
5. 6 维都过 7 分 → 结业

记录在 `~/.xiaohongshu/profile/iter_sessions/<draft-id>/iter.jsonl`，
形成完整改稿轨迹，可作为练习成绩留存。

用法
----

    # 第一轮：助手挑出最该改的一维（比如 ai_speak）
    python3 coach_iterate.py --in draft.md

    # 用户改完，再跑同一命令（同一文件）
    # 助手对比上一次的分，决定继续 ai_speak 还是切下一维
    python3 coach_iterate.py --in draft.md

    # 强制 focus 某一维
    python3 coach_iterate.py --in draft.md --focus ai_speak

    # 看完整轨迹
    python3 coach_iterate.py --in draft.md --history

    # 重置当前文件的 session
    python3 coach_iterate.py --in draft.md --reset
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_aesthetic import aesthetic_score  # noqa: E402
from xhs_profile import ProfileStore  # noqa: E402
from xhs_writer import load_draft  # noqa: E402

try:
    import llm_helper
except ImportError:
    llm_helper = None  # type: ignore


# 一维维度的 focus 顺序（差的优先 + 大类影响优先）
_DIM_PRIORITY = [
    "ab_validation",   # v3.5: AB 点是否兑现（如果有 AB 点，最高优先）
    "jarvis_trap",     # 系统性思路偏差
    "ai_speak",        # AI 腔（最容易识别）
    "teach_vs_lead",   # 教 vs 带
    "resonance",       # 共鸣度（最难修）
    "breath",          # 留白
    "invitation",      # 邀请语
]

_DIM_LABELS = {
    "ab_validation": "AB 点兑现（A→B 是否真发生）",
    "jarvis_trap": "范本范（攻略 vs 范本）",
    "ai_speak": "去 AI 腔",
    "teach_vs_lead": "带读者（不教读者）",
    "resonance": "共鸣度（共同记忆 vs 冷知识）",
    "breath": "留白度（留出填情绪空间）",
    "invitation": "邀请语（邀请 vs 任务指令）",
}

# 每一维的"教练话术"模板
_FOCUS_GUIDANCE: Dict[str, Dict[str, str]] = {
    "ab_validation": {
        "intro": "你设了 AB 点，但读者读完不一定真从 A 到了 B。",
        "question": "假装你是 A 状态的读者，读完这篇，你的看法 / 感受真的变成 B 了吗？",
        "exercise": "对每个段落问：这一段把读者推近 B 了吗？没推近的删掉或重写。",
    },
    "jarvis_trap": {
        "intro": "你的开头/引导/角色/语气/结尾里，至少有 2 维偏向'攻略型'。",
        "question": "Allen 说：你在'教读者怎么做'，还是'展示什么样的人已经在做'？",
        "exercise": "把 1 处 '你应该 X' 改成 '有人在 X' / '一个粉丝告诉我 X'。",
    },
    "ai_speak": {
        "intro": "正文里有汇报化 / 模板化 / 装腔词 — 写小红书必须用人话。",
        "question": "把每个被识别的词大声念一遍 — 你日常会和朋友这样说吗？",
        "exercise": "把命中的所有 AI 腔词换成口语，看 ai_speak_patterns.json 替换库。",
    },
    "teach_vs_lead": {
        "intro": "你的正文像在'讲课' — 命令式 / 教官式词太多。",
        "question": "如果你在咖啡馆和朋友说这件事，你还会说 '你应该 X' 吗？",
        "exercise": "把 '你应该 / 必须 / 记住' 改成 '我自己 / 不妨试试 / 有时候'。",
    },
    "resonance": {
        "intro": "场景里没有共同记忆词 — 读者看不见自己。",
        "question": "你写的场景，邻居 / 同事 / 大学同学，他们都有过吗？",
        "exercise": "加 1~2 个具体画面（草地/晚风/凉席/翻箱倒柜），不要冷知识。",
    },
    "breath": {
        "intro": "段落太长 / 编号太规整 — 像说明书，不像生活记录。",
        "question": "读者扫读时，眼睛能在哪里落下来歇一会儿？",
        "exercise": "把长句在自然停顿处断开，关键句独立成段。删 '1.2.3.' 换 emoji 锚点。",
    },
    "invitation": {
        "intro": "结尾或互动处用了任务指令 / 没用邀请语。",
        "question": "如果你的笔记是一封信，你会在结尾写 '关注我'，还是写 '你呢，告诉我你的'？",
        "exercise": "把 '想看的扣 1' 改成 '你那一天是怎样的，留个故事给我'。",
    },
}


# =====================================================================
# 数据存档
# =====================================================================


def session_dir(store: ProfileStore, draft_path: Path) -> Path:
    """把 draft 文件路径哈希成稳定的 session id。"""
    abspath = str(draft_path.resolve())
    sid = hashlib.sha1(abspath.encode("utf-8")).hexdigest()[:10]
    d = store.root / "iter_sessions" / sid
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_history(sess_dir: Path) -> List[Dict[str, Any]]:
    p = sess_dir / "iter.jsonl"
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


def append_history(sess_dir: Path, entry: Dict[str, Any]) -> None:
    p = sess_dir / "iter.jsonl"
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def snapshot_draft(sess_dir: Path, draft_path: Path, round_no: int) -> None:
    """把当前草稿快照存进 session。"""
    target = sess_dir / f"round_{round_no:02d}.md"
    shutil.copy(draft_path, target)


# =====================================================================
# 决策：下一步 focus 哪一维
# =====================================================================


def decide_focus(
    by_dim: Dict[str, Dict[str, Any]],
    history: List[Dict[str, Any]],
    threshold: int = 7,
    ab_meta: Optional[Dict[str, Any]] = None,
) -> Optional[str]:
    """挑下一个要 focus 的维度。返回 None 表示全部 ≥ threshold（结业）。

    v3.5: 如果 ab_meta 有 AB 点且 ab_validated 不是 True，优先 focus ab_validation。
    """
    # 上一轮 focus 的维度
    last_focus = history[-1]["focus"] if history else None
    last_score = history[-1]["after_score"] if history else None

    # 当前各维度分数
    current: Dict[str, int] = {k: v["score"] for k, v in by_dim.items()}

    # v3.5: AB 点优先（如果设了 AB 但还没验证通过）
    if ab_meta and (ab_meta.get("ab_a_view") or ab_meta.get("ab_b_view")):
        if ab_meta.get("ab_validated") is not True:
            # 已经 focus 过 ab_validation 但还没 graduate → 继续
            ab_attempts = sum(1 for h in history if h.get("focus") == "ab_validation")
            if ab_attempts < 3:  # 最多追 3 轮
                return "ab_validation"

    # 如果上一轮的 focus 没升上去，继续 focus 它
    if last_focus and last_focus in current:
        if current[last_focus] < threshold:
            if last_score is not None and current[last_focus] <= last_score + 1:
                return last_focus

    # 否则挑当前最差的一维（按优先级 tie-break）
    candidates = [k for k in _DIM_PRIORITY if k in current and current[k] < threshold]
    if not candidates:
        return None

    candidates.sort(key=lambda k: (current[k], _DIM_PRIORITY.index(k)))
    return candidates[0]


# =====================================================================
# 渲染单维度反馈
# =====================================================================


def render_focus_card(
    focus: str,
    info: Dict[str, Any],
    round_no: int,
    score_change: Optional[int] = None,
    enriched: str = "",
) -> str:
    parts = []
    parts.append("=" * 60)
    parts.append(f"🎯 第 {round_no} 轮教练课  ｜  本轮 focus：{_DIM_LABELS[focus]}")
    parts.append("=" * 60)
    parts.append("")
    parts.append(f"当前该维度得分：{info['score']}/10", )
    if score_change is not None:
        sign = "+" if score_change >= 0 else ""
        emoji = "📈" if score_change > 0 else "➖" if score_change == 0 else "📉"
        parts.append(f"上一轮变化：{emoji} {sign}{score_change}")
    parts.append("")

    g = _FOCUS_GUIDANCE.get(focus, {})

    parts.append(f"💡 现在专心改这一维（其他维度先放一放）：")
    parts.append(f"   {g.get('intro', '')}")
    parts.append("")

    if info.get("issues"):
        parts.append("📋 命中位置：")
        for x in info["issues"]:
            parts.append(f"   • {x}")
        parts.append("")

    parts.append(f"🤔 自检问题：")
    parts.append(f"   {g.get('question', '')}")
    parts.append("")

    parts.append(f"✏️  本轮练习：")
    parts.append(f"   {g.get('exercise', '')}")
    parts.append("")

    if info.get("suggestions"):
        parts.append("📝 改写建议（前 3 条）：")
        for s in info["suggestions"][:3]:
            parts.append(f"   → {s}")
        parts.append("")

    if enriched:
        parts.append("─" * 50)
        parts.append("🤖 LLM 增强建议：")
        parts.append(enriched)
        parts.append("")

    parts.append("─" * 50)
    parts.append("改完后，跑同一命令再来一轮：")
    parts.append("   python3 scripts/coach_iterate.py --in <你的草稿>")
    return "\n".join(parts)


def render_graduation(by_dim: Dict[str, Dict[str, Any]],
                      history: List[Dict[str, Any]]) -> str:
    parts = ["", "🎓" * 30, ""]
    parts.append(f"🎉 恭喜！6 维都达标，你的文案已经走出 AI / 攻略陷阱。")
    parts.append("")
    parts.append("各维度最终得分：")
    for k in _DIM_PRIORITY:
        if k in by_dim:
            parts.append(f"   {_DIM_LABELS[k]:<28} {by_dim[k]['score']}/10  ✓")
    parts.append("")
    parts.append(f"本次改稿历经 {len(history)} 轮：")
    for h in history:
        parts.append(f"   Round {h['round']}: focus {_DIM_LABELS.get(h['focus'], h['focus'])} "
                     f"{h['before_score']} → {h['after_score']}")
    parts.append("")
    parts.append("下一步：")
    parts.append("   python3 scripts/assistant.py publish <draft>")
    return "\n".join(parts)


# =====================================================================
# LLM 增强（针对当前 focus 维度）
# =====================================================================


def llm_enrich_focus(focus: str, draft_text: str) -> str:
    if not llm_helper or not llm_helper.is_enabled():
        return ""
    label = _DIM_LABELS.get(focus, focus)
    prompt = (
        f"以下是一篇小红书草稿，本轮训练只 focus 一个维度：**{label}**。\n\n"
        f"{draft_text[:1500]}\n\n"
        f"请基于 Allen 文案体系（缓存里的 allen_method.md），"
        f"针对这个维度给我 1 段 100~150 字的具体改写示意 — "
        f"挑出原文里最该改的 1 处，写出改后版本，不要泛泛建议。"
    )
    text = llm_helper.call(
        prompt, tier="balanced",
        cached_assets=["allen_method", "ai_speak"],
        max_tokens=400,
    )
    return text or ""


# =====================================================================
# 主流程
# =====================================================================


def cmd_main(args: argparse.Namespace) -> int:
    draft_path = Path(args.path)
    if not draft_path.exists():
        print(f"❌ 找不到草稿：{draft_path}", file=sys.stderr)
        return 1
    draft = load_draft(str(draft_path))

    store = ProfileStore()
    sess_dir = session_dir(store, draft_path)

    if args.reset:
        if sess_dir.exists():
            shutil.rmtree(sess_dir)
        sess_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ 已重置 session：{sess_dir}", file=sys.stderr)

    history = load_history(sess_dir)

    if args.history:
        if not history:
            print("（这个草稿还没有训练历史。先跑一次 coach_iterate.py --in <draft>）")
            return 0
        for h in history:
            print(f"Round {h['round']}: focus={h['focus']} "
                  f"{h['before_score']} → {h['after_score']} "
                  f"(total {h['before_total']} → {h['after_total']})")
        return 0

    # 跑分
    score = aesthetic_score(draft.title, draft.content)

    # v3.5: 如果 draft 在 drafts/<id>/ 目录里，读 meta.json 拿 AB 点
    ab_meta = None
    parent = draft_path.parent
    if (parent / "meta.json").exists():
        try:
            ab_meta = json.loads((parent / "meta.json").read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    # 决定 focus
    if args.focus:
        focus = args.focus
        if focus != "ab_validation" and focus not in score.by_dim:
            print(f"❌ 无效维度 {focus}（可用：{', '.join(_DIM_PRIORITY)}）", file=sys.stderr)
            return 1
    else:
        focus = decide_focus(score.by_dim, history, ab_meta=ab_meta)

    round_no = len(history) + 1

    # 全部达标 → 结业
    if focus is None:
        print(render_graduation(score.by_dim, history))
        # 记录结业
        append_history(sess_dir, {
            "round": round_no,
            "at": dt.datetime.now().isoformat(timespec="seconds"),
            "focus": "graduated",
            "before_score": None,
            "after_score": None,
            "before_total": history[-1]["after_total"] if history else score.total,
            "after_total": score.total,
        })
        return 0

    # 计算分数变化（如果上一轮 focus 是同一维）
    score_change = None
    if history and history[-1]["focus"] == focus:
        score_change = score.by_dim[focus]["score"] - history[-1]["after_score"]

    # v3.5: ab_validation 是虚拟维度（不在 score.by_dim 里）
    if focus == "ab_validation":
        if ab_meta:
            info = {
                "score": 5 if ab_meta.get("ab_validated") is None else (
                    9 if ab_meta.get("ab_validated") else 3),
                "issues": [
                    f"A 看法：{ab_meta.get('ab_a_view', '?')}",
                    f"B 看法：{ab_meta.get('ab_b_view', '?')}",
                ],
                "suggestions": [
                    "用 `drafts ab <id> --validate` 让 LLM 判定 A→B 是否兑现",
                    "改完后再 validate，看分数变化",
                ],
            }
        else:
            info = {"score": 5, "issues": ["（这个 draft 不在 drafts 目录，无 AB 点）"],
                    "suggestions": ["建议把草稿挪进 drafts/，再设 AB 点"]}
    else:
        info = score.by_dim[focus]

    # LLM 增强
    enriched = ""
    if not args.no_llm:
        full_text = f"{draft.title}\n\n{draft.content}"
        enriched = llm_enrich_focus(focus, full_text)

    # 输出
    print(render_focus_card(focus, info, round_no, score_change, enriched))

    # 存档
    snapshot_draft(sess_dir, draft_path, round_no)
    append_history(sess_dir, {
        "round": round_no,
        "at": dt.datetime.now().isoformat(timespec="seconds"),
        "focus": focus,
        "before_score": history[-1]["after_score"] if history and history[-1]["focus"] == focus else None,
        "after_score": info["score"],
        "before_total": history[-1]["after_total"] if history else None,
        "after_total": score.total,
    })

    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="coach_iterate.py",
                                description="渐进式教练 — 一次只 focus 一维")
    p.add_argument("--in", dest="path", required=True, help="草稿文件路径")
    p.add_argument("--focus", default="",
                   help=f"强制 focus 某维：{', '.join(_DIM_PRIORITY)}")
    p.add_argument("--history", action="store_true", help="查看本草稿的训练历史")
    p.add_argument("--reset", action="store_true", help="重置本草稿的 session")
    p.add_argument("--no-llm", action="store_true", help="不调 LLM 增强")
    args = p.parse_args()
    return cmd_main(args)


if __name__ == "__main__":
    sys.exit(main())
