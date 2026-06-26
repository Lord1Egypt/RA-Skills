#!/usr/bin/env python3
"""火一五小红书文案合规扫描 — 发布前必跑。

检测维度
========
1. **绝对化用语**（《广告法》第 9 条 + 平台限流红线）
2. **医疗 / 金融 / 教育**承诺词
3. **站外导流**（微信 / V / QQ / 二维码）
4. **诱导互动**（关注私信 / 评论 666 抽奖等）
5. **平台敏感**（搬运 / 互推 / 涨粉 / 刷粉）
6. **手机号 / 微信号 / QQ 号**正则识别
7. **话题数量**（< 3 或 > 8 都不健康）

数据源：data/sensitive_words.txt + 内置正则。

用法
----

    # 扫一篇 markdown 草稿
    python3 compliance_check.py --in draft.md

    # 扫纯文本
    python3 compliance_check.py --text "免费！100% 包过，加微信详聊"

    # 输出 JSON 给 pipeline
    python3 compliance_check.py --in draft.md --format json

退出码
------
- 0：完全干净
- 1：有警告（轻度，不一定限流）
- 2：有违规（高风险，必须改）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent))

from typing import Optional  # noqa: E402

from xhs_writer import Draft, load_draft, load_sensitive_words  # noqa: E402

# ---------- 正则规则（高风险） ----------

_RULES_HIGH: Dict[str, re.Pattern] = {
    "phone": re.compile(r"(?<!\d)(1[3-9]\d{9}|0\d{2,3}[-\s]?\d{7,8})(?!\d)"),
    "qq": re.compile(r"(?:Q+|q+|扣扣|企鹅)\s*[:：]?\s*\d{5,12}"),
    "wechat_id": re.compile(r"(?:微信号|WX|wx|VX|vx|V[xX]|微信)\s*[:：]?\s*[A-Za-z][\w\-]{4,19}"),
    "url_external": re.compile(r"\b(?:taobao|tmall|jd|pinduoduo|douyin|kuaishou|bilibili)\.com\b", re.I),
}

# ---------- 正则规则（中风险） ----------

_RULES_MEDIUM: Dict[str, re.Pattern] = {
    "induce_follow": re.compile(r"(关注私信|私信领取|关注后私信|私我领|评论\s*\d{2,3}\s*(?:抽奖|送)|点赞过\s*\d+\s*(?:更新|更))"),
    "off_platform_hint": re.compile(r"(主页有(?:联系|微信|VX|号)|简介(?:有|看)(?:微信|VX|联系)|评论解锁)"),
}


def scan_text(text: str, sensitive: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """返回三档命中：high / medium / low (敏感词)。"""
    result = {"high": [], "medium": [], "low": []}

    for name, pat in _RULES_HIGH.items():
        for m in pat.finditer(text):
            result["high"].append({
                "rule": name,
                "match": m.group(0),
                "pos": m.start(),
            })

    for name, pat in _RULES_MEDIUM.items():
        for m in pat.finditer(text):
            result["medium"].append({
                "rule": name,
                "match": m.group(0),
                "pos": m.start(),
            })

    # 敏感词逐一扫
    for w in sensitive:
        if not w:
            continue
        idx = text.find(w)
        if idx >= 0:
            result["low"].append({
                "rule": "sensitive_word",
                "match": w,
                "pos": idx,
            })

    return result


def check_ai_label(text: str, tags: List[str]) -> Optional[Dict[str, str]]:
    """检测 AI 标签合规 — 2026/01 起小红书强制标注 AI 生成内容。

    Returns: 命中提示 dict，没有问题返回 None。
    """
    # 标签里出现 #AI生成 / #AI创作 / #AI生成内容 都算合规
    label_patterns = ["AI生成", "AI创作", "AI辅助", "AIGC", "ai生成", "AI写作", "ai辅助"]
    has_label_in_tags = any(any(p in t for p in label_patterns) for t in tags)
    has_label_in_text = any(p in text for p in label_patterns)
    if has_label_in_tags or has_label_in_text:
        return None

    # 没标 — 高风险（自 2026/01 起强制要求）
    return {
        "rule": "missing_ai_label",
        "severity": "high",
        "message": "未标注 AI 生成内容（自 2026/01 起强制，未标会限流）",
        "fix": "在话题或正文末尾加 #AI生成内容 或 #AI辅助创作。如纯人工创作可忽略此项。",
    }


def render(result: Dict, tag_count: int) -> str:
    out = []
    high = result["high"]
    medium = result["medium"]
    low = result["low"]

    out.append("=== 小红书文案合规扫描 ===")
    out.append("")
    if not (high or medium or low) and 3 <= tag_count <= 6:
        out.append("✓ 干净，可以发布")
        return "\n".join(out)

    if high:
        out.append(f"❌ 高风险（必须改）— {len(high)} 处")
        for h in high:
            out.append(f"   • [{h['rule']}] {h['match']!r}")
        out.append("")

    if medium:
        out.append(f"⚠️  中风险（建议改）— {len(medium)} 处")
        for h in medium:
            out.append(f"   • [{h['rule']}] {h['match']!r}")
        out.append("")

    if low:
        # 去重，只展示前 20
        seen = set()
        unique = []
        for h in low:
            if h["match"] in seen:
                continue
            seen.add(h["match"])
            unique.append(h)
        out.append(f"⚠️  敏感词（建议改）— {len(unique)} 个")
        for h in unique[:20]:
            out.append(f"   • {h['match']!r}")
        if len(unique) > 20:
            out.append(f"   ...省略 {len(unique) - 20} 个")
        out.append("")

    if tag_count < 3:
        out.append(f"⚠️  话题数 {tag_count} 个（建议 3~6 个，否则推荐量很小）")
    elif tag_count > 8:
        out.append(f"⚠️  话题数 {tag_count} 个（超过 8 个会被识别为营销号）")

    out.append("")
    out.append("修改思路：")
    out.append("  • 绝对化词 → 主观表达（'我用着觉得' / '亲测' / '我自己'）")
    out.append("  • 联系方式 → 删除 / 走私信关键词回复（不在文案明示）")
    out.append("  • 医疗承诺 → 改成 '我自己的体验'，避开 '治愈/根治'")
    out.append("  • 诱导互动 → 改成 '评论区聊聊你的想法' 等开放邀请")
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser(prog="compliance_check.py", description="小红书文案合规扫描")
    p.add_argument("--in", dest="path", default="", help="草稿路径 (.md 或 .json)")
    p.add_argument("--text", default="", help="直接传纯文本扫描")
    p.add_argument("--no-ai-label-check", action="store_true",
                   help="跳过 #AI生成内容 必标检查（仅纯人工创作可关）")
    p.add_argument("--format", choices=["text", "json"], default="text")
    args = p.parse_args()

    if args.path:
        draft = load_draft(args.path)
        text = f"{draft.title}\n{draft.content}\n{' '.join(draft.tags)}"
        tag_count = len([t for t in draft.tags if t.strip()])
        tags = draft.tags
    elif args.text:
        text = args.text
        tag_count = len(re.findall(r"#([\w一-鿿]+)", text))
        tags = re.findall(r"#([\w一-鿿]+)", text)
    else:
        print("需要 --in 或 --text", file=sys.stderr)
        return 1

    sensitive = load_sensitive_words()
    result = scan_text(text, sensitive)

    # AI 标签检查（v3.3 加）
    ai_warning = None
    if not args.no_ai_label_check:
        ai_warning = check_ai_label(text, tags)
        if ai_warning:
            result["high"].append({
                "rule": ai_warning["rule"],
                "match": ai_warning["message"],
                "pos": 0,
            })

    if args.format == "json":
        print(json.dumps({
            "high": result["high"],
            "medium": result["medium"],
            "low": result["low"],
            "tag_count": tag_count,
        }, ensure_ascii=False, indent=2))
    else:
        print(render(result, tag_count))

    if result["high"]:
        return 2
    if result["medium"] or result["low"]:
        return 1
    if not (3 <= tag_count <= 6) and tag_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
