#!/usr/bin/env python3
"""火一五小红书"对标笔记反向拆解" — 给一个爆款 URL，反推出公式 / 骨架 / 钩子 / 情绪曲线 / 关键词。

为什么需要
==========
市场上的同类工具（七燕、XHSPlus、白瓜AI）核心卖点之一就是"对标拆解"：
贴一个爆款 URL，AI 拆出"它是怎么写出来的"。

我们和它们的区别：
- 不做"换个标题就发"的洗稿
- 拆出来的结构 → 进入 baseline 库，让你的风格档案学到这种好结构
- 拆完不止给"换皮模板"，还告诉你**为什么这条爆**

工作流
======
1. 用现有 scrape-note.py 抓笔记（或本地 .json 文件）
2. 规则模式拆解：标题公式（T1~T11） / 正文骨架（S1~S7） / Allen 5 维 / 关键词
3. 可选 LLM 增强（XHS_LLM_PROVIDER=anthropic）：
   - 推断"这条为什么爆"
   - 给出"用相同骨架但换我赛道"的改写示意
4. 输出可以直接 --add-baseline 进 profile

用法
----

    # 从 URL 拆（要 Cookie）
    python3 reverse_engineer.py --url "https://www.xiaohongshu.com/explore/64abc...?xsec_token=..."

    # 从本地 .json 拆（已经抓过的笔记）
    python3 reverse_engineer.py --in /tmp/note.json

    # 加进 baseline 库
    python3 reverse_engineer.py --in /tmp/note.json --add-baseline

    # 输出 markdown 拆解报告
    python3 reverse_engineer.py --in /tmp/note.json --format md --out reverse.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_aesthetic import aesthetic_score  # noqa: E402
from xhs_coach import detect_formula, detect_skeleton  # noqa: E402
from xhs_writer import Draft  # noqa: E402

# llm_helper 是可选的
try:
    import llm_helper
except ImportError:
    llm_helper = None  # type: ignore


# =====================================================================
# 拆解结构
# =====================================================================


@dataclass
class Teardown:
    note_id: str = ""
    url: str = ""
    title: str = ""
    title_len: int = 0
    formula: Optional[str] = None       # T1~T11
    skeleton: Optional[str] = None      # S1~S7
    aesthetic_total: int = 0
    aesthetic_breakdown: Dict[str, int] = field(default_factory=dict)
    hook_first_line: str = ""
    keywords_top10: List[str] = field(default_factory=list)
    interaction_summary: Dict[str, int] = field(default_factory=dict)
    why_it_works: List[str] = field(default_factory=list)   # 规则推断 + LLM
    transferable: List[str] = field(default_factory=list)   # "你可以学的点"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# 抓取 / 加载
# =====================================================================


def load_from_url(url: str) -> Dict[str, Any]:
    """用现有 scrape-note 抓笔记 → dict。"""
    from xhs_client import XHSClient, load_cookie_from_env
    from xhs_parser import note_to_dict, parse_note_page
    # url 解析 note_id 和 xsec_token
    m = re.search(r"/explore/([a-f0-9]+)", url)
    if not m:
        raise ValueError(f"URL 里找不到 note_id：{url}")
    note_id = m.group(1)
    token_m = re.search(r"xsec_token=([^&\s]+)", url)
    xsec_token = token_m.group(1) if token_m else None

    client = XHSClient(cookie=load_cookie_from_env())
    html = client.get_explore_page(note_id=note_id, xsec_token=xsec_token)
    note = parse_note_page(html, note_id=note_id)
    if not note:
        raise RuntimeError("解析失败 — HTML 结构变化或被风控")
    return note_to_dict(note)


def load_from_file(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    return json.loads(p.read_text(encoding="utf-8"))


# =====================================================================
# 规则拆解
# =====================================================================


def extract_keywords(title: str, content: str, top: int = 10) -> List[str]:
    """简单关键词频次（无 jieba 退化版）。"""
    text = f"{title}\n{content}"
    text = re.sub(r"[\s\.,;:!?\"'()\[\]\-_+*&^%$#@~`—…！？，。、：；""''（）【】《》〈〉「」·]+",
                  " ", text)
    tokens = [t for t in text.split() if len(t) >= 2 and not t.isdigit()]
    counts: Dict[str, int] = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    return [k for k, _ in sorted(counts.items(), key=lambda x: -x[1])[:top]]


def first_meaningful_line(content: str) -> str:
    for ln in content.splitlines():
        s = ln.strip()
        if s and not all(ord(c) < 128 and not c.isalnum() for c in s):
            return s[:80]
    return ""


def teardown_rules(note: Dict[str, Any]) -> Teardown:
    title = note.get("title", "") or ""
    content = note.get("content", "") or ""
    inter = note.get("interactions") or {}

    formula = detect_formula(title) or None
    skeleton = detect_skeleton(content) or None
    aes = aesthetic_score(title, content)

    why: List[str] = []
    if formula:
        why.append(f"标题命中 {formula} 公式 — 这种公式的爆款命中率较高")
    if skeleton:
        why.append(f"正文走 {skeleton} 骨架 — 视觉锚点清晰")
    # Allen 维度 ≥ 8 视为强项
    for k, v in aes.by_dim.items():
        if v["score"] >= 8:
            label = {"breath": "留白节奏好", "ai_speak": "没有 AI 腔",
                     "teach_vs_lead": "在带读者", "resonance": "共鸣感强",
                     "invitation": "互动是邀请语",
                     "jarvis_trap": "走的是范本范不是攻略范"}.get(k, k)
            why.append(f"Allen 美学：{label}")

    transferable: List[str] = []
    if formula:
        transferable.append(f"在你赛道复用 {formula} 公式（参考 data/title_templates.md）")
    if skeleton:
        transferable.append(f"在你赛道复用 {skeleton} 骨架（参考 data/content_structures.md）")

    return Teardown(
        note_id=note.get("note_id", "") or "",
        url=note.get("url", "") or "",
        title=title,
        title_len=len(title),
        formula=formula,
        skeleton=skeleton,
        aesthetic_total=aes.total,
        aesthetic_breakdown={k: v["score"] for k, v in aes.by_dim.items()},
        hook_first_line=first_meaningful_line(content),
        keywords_top10=extract_keywords(title, content, 10),
        interaction_summary={
            "liked": int(inter.get("liked_count", 0) or 0),
            "collected": int(inter.get("collected_count", 0) or 0),
            "comment": int(inter.get("comment_count", 0) or 0),
        },
        why_it_works=why,
        transferable=transferable,
    )


# =====================================================================
# LLM 增强
# =====================================================================


def teardown_with_llm(td: Teardown, full_text: str) -> Teardown:
    """让 Claude 给出"为什么爆 + 你赛道怎么用"的更深解读。规则推断不变，附加。"""
    if not llm_helper or not llm_helper.is_enabled():
        return td

    prompt = (
        f"以下是一篇小红书爆款笔记，请深度拆解：\n\n"
        f"标题：{td.title}\n\n"
        f"正文：\n{full_text[:1500]}\n\n"
        f"互动：{td.interaction_summary}\n\n"
        f"基于 Allen 文案体系（缓存里的 allen_method.md），告诉我：\n"
        f"1. 这条爆款最关键的 3 个'写法决策'是什么？\n"
        f"2. 其中哪 2 个是普通号最容易学的？\n"
        f"3. 用相同结构但换我赛道（假设我是 30+ 干皮女生），第一句钩子怎么写？\n"
        f"用 JSON 返回 {{\"key_decisions\": [...3 条], \"easy_to_learn\": [...2 条], "
        f"\"transfer_hook\": \"...\"}}。"
    )
    data = llm_helper.call_json(
        prompt,
        tier="balanced",
        cached_assets=["allen_method", "title_templates", "content_structures"],
        max_tokens=800,
    )
    if not data:
        return td

    if isinstance(data, dict):
        for k in data.get("key_decisions", []) or []:
            td.why_it_works.append(f"[LLM] {k}")
        for k in data.get("easy_to_learn", []) or []:
            td.transferable.append(f"[LLM] {k}")
        if data.get("transfer_hook"):
            td.transferable.append(f"[LLM 改写示意] {data['transfer_hook']}")

    return td


# =====================================================================
# 渲染
# =====================================================================


def render_text(td: Teardown) -> str:
    parts = ["━" * 60, "🔬 对标笔记反向拆解", "━" * 60, ""]
    parts.append(f"标题：{td.title}（{td.title_len} 字）")
    if td.url:
        parts.append(f"URL：{td.url}")
    parts.append(f"互动：{td.interaction_summary.get('liked', 0)}赞 / "
                 f"{td.interaction_summary.get('collected', 0)}藏 / "
                 f"{td.interaction_summary.get('comment', 0)}评")
    parts.append("")

    parts.append(f"📐 标题公式：{td.formula or '（未识别 — 不是经典公式）'}")
    parts.append(f"🏗️  正文骨架：{td.skeleton or '（未识别）'}")
    parts.append(f"🎨 Allen 美学：{td.aesthetic_total}/100")
    if td.aesthetic_breakdown:
        labels = {"breath": "留白", "ai_speak": "去AI腔", "teach_vs_lead": "带读者",
                  "resonance": "共鸣", "invitation": "邀请", "jarvis_trap": "范本范"}
        line = " / ".join(f"{labels.get(k, k)}{v}" for k, v in td.aesthetic_breakdown.items())
        parts.append(f"           {line}")
    parts.append("")

    if td.hook_first_line:
        parts.append(f"🪝 首段钩子：{td.hook_first_line}")
        parts.append("")

    if td.keywords_top10:
        parts.append(f"🔑 高频词：{', '.join(td.keywords_top10)}")
        parts.append("")

    if td.why_it_works:
        parts.append("💡 为什么爆：")
        for w in td.why_it_works:
            parts.append(f"   • {w}")
        parts.append("")

    if td.transferable:
        parts.append("📦 你能学到的：")
        for t in td.transferable:
            parts.append(f"   • {t}")
        parts.append("")

    parts.append("━" * 60)
    parts.append("下一步：")
    parts.append(f"  • 把这条加到 baseline：python3 profile_init.py add <note.json>")
    parts.append(f"  • 用同公式起草新文：python3 write_post.py draft \\")
    if td.formula and td.skeleton:
        parts.append(f"      --formula {td.formula} --skeleton {td.skeleton} --topic <你的主题>")
    return "\n".join(parts)


def render_md(td: Teardown) -> str:
    parts = [f"# 对标拆解：{td.title}\n"]
    parts.append(f"- **URL**: {td.url or '(本地)'}")
    parts.append(f"- **互动**: {td.interaction_summary.get('liked', 0)}赞 / "
                 f"{td.interaction_summary.get('collected', 0)}藏 / "
                 f"{td.interaction_summary.get('comment', 0)}评")
    parts.append(f"- **标题公式**: {td.formula or '?'}")
    parts.append(f"- **正文骨架**: {td.skeleton or '?'}")
    parts.append(f"- **Allen 美学**: {td.aesthetic_total}/100")
    parts.append("")
    if td.hook_first_line:
        parts.append(f"## 首段钩子\n\n> {td.hook_first_line}\n")
    if td.keywords_top10:
        parts.append(f"## 高频关键词\n\n{', '.join(f'`{k}`' for k in td.keywords_top10)}\n")
    if td.why_it_works:
        parts.append("## 为什么爆\n")
        for w in td.why_it_works:
            parts.append(f"- {w}")
        parts.append("")
    if td.transferable:
        parts.append("## 你能学到的\n")
        for t in td.transferable:
            parts.append(f"- {t}")
        parts.append("")
    return "\n".join(parts) + "\n"


# =====================================================================
# 主流程
# =====================================================================


def main() -> int:
    p = argparse.ArgumentParser(prog="reverse_engineer.py", description="对标笔记反向拆解")
    p.add_argument("--url", default="", help="爆款笔记 URL")
    p.add_argument("--in", dest="path", default="", help="或本地 .json 文件")
    p.add_argument("--format", choices=["text", "md", "json"], default="text")
    p.add_argument("--out", default="")
    p.add_argument("--no-llm", action="store_true")
    p.add_argument("--add-baseline", action="store_true",
                   help="拆完后加进 ~/.xiaohongshu/profile/baseline/")
    args = p.parse_args()

    if args.url:
        try:
            note = load_from_url(args.url)
        except Exception as e:
            print(f"❌ 抓取失败：{e}", file=sys.stderr)
            return 1
    elif args.path:
        note = load_from_file(args.path)
    else:
        print("需要 --url 或 --in", file=sys.stderr)
        return 1

    td = teardown_rules(note)
    full_text = f"{note.get('title', '')}\n{note.get('content', '')}"
    if not args.no_llm:
        td = teardown_with_llm(td, full_text)

    if args.add_baseline:
        from xhs_profile import ProfileStore
        store = ProfileStore()
        path = store.add_baseline(note)
        print(f"✓ 已加入 baseline：{path}", file=sys.stderr)

    if args.format == "json":
        out_text = json.dumps(td.to_dict(), ensure_ascii=False, indent=2)
    elif args.format == "md":
        out_text = render_md(td)
    else:
        out_text = render_text(td)

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}", file=sys.stderr)
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
