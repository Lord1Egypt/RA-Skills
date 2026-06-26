#!/usr/bin/env python3
"""火一五小红书"造词工具" — Allen 待修炼方向之一。

Allen 教训
==========
- **「薯你会买」** = 品牌资产（薯）+ 对话感（你）+ 价值观（会买=会生活）
- **「人类丰容」** = 概念迁移（动物丰容 → 人）
- **「人生尽兴指南」** = 形式包装（指南 = 说明书形式）+ 情绪态度

造词三种模式：
1. **谐音造词** — 把品牌发音嵌进熟语
2. **概念迁移** — 跨领域借用（生物 / 建筑 / 心理 / 物理）
3. **形式包装** — 用说明书 / 指南 / 报告 / 档案等形式装情绪

不依赖 LLM，纯规则候选；同时支持 LLM 增强（XHS_LLM_PROVIDER=anthropic）。

用法
----

    # 给品牌词造词候选
    python3 coin_word.py --brand "小红薯" --value "会买=会生活" --n 8

    # 输出 JSON
    python3 coin_word.py --brand "尽兴" --value "活得舒服" --format json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent))


# ---------- 模板库 ----------


_HOMOPHONE_TEMPLATES = [
    "{b}你会{v}",      # 薯你会买
    "{b}的就是好",
    "看{b}就懂{v}",
    "{b}味人生",
    "和{b}相处{v}",
    "{b}是个好习惯",
]


_CROSS_DOMAIN = {
    "生物": [("丰容", "给环境加新鲜感"), ("反刍", "回味"),
            ("光合", "靠自己回血"), ("脱壳", "蜕变"),
            ("筑巢", "营造空间")],
    "建筑": [("留白", "空间感"), ("骨架", "结构感"),
            ("肌理", "细节感"), ("透光", "氛围")],
    "物理": [("惯性", "状态延续"), ("反作用力", "回弹"),
            ("熵减", "整理感"), ("折射", "看见不同面")],
    "音乐": [("低音", "底色"), ("和弦", "组合"),
            ("休止符", "停一停"), ("回旋", "重复")],
    "电影": [("长镜头", "完整感"), ("蒙太奇", "拼接"),
            ("反转", "剧情"), ("彩蛋", "惊喜")],
    "厨房": [("文火", "慢"), ("出锅", "完成感"),
            ("回锅", "再来一遍"), ("撒盐", "提味")],
}


_FORMAT_WRAPPERS = [
    "{title}指南", "{title}手册", "{title}白皮书",
    "{title}小词典", "{title}存档", "{title}剧本",
    "{title}档案", "{title}日记", "{title}图鉴",
    "{title}修炼", "{title}入门", "{title}百宝书",
    "{title}清单", "{title}年报", "{title}地图",
]


def coin_homophone(brand: str, value: str = "") -> List[Dict[str, str]]:
    """谐音造词。"""
    out = []
    if not brand:
        return out
    short = brand[0]                                # 取首字
    val_short = (value.split("=")[0] if "=" in value else value)[:2]  # 取前 2 字
    for t in _HOMOPHONE_TEMPLATES:
        word = t.format(b=short, v=val_short or brand)
        out.append({
            "word": word,
            "type": "谐音造词",
            "explain": f"借用'{short}'的发音，把品牌嵌进对话感的熟语",
        })
    return out


def coin_cross_domain(brand: str, value: str = "") -> List[Dict[str, str]]:
    """概念迁移造词。"""
    out = []
    for domain, items in _CROSS_DOMAIN.items():
        for term, desc in items[:2]:
            word = f"{brand}{term}"
            out.append({
                "word": word,
                "type": f"概念迁移（{domain}）",
                "explain": f"把'{domain}'里的'{term}'（{desc}）借用到品牌语境",
            })
    return out


def coin_format_wrap(brand: str, value: str = "") -> List[Dict[str, str]]:
    """形式包装：用说明书/指南等形式装情绪。"""
    out = []
    title_base = brand if value == "" else f"{brand}{value.split('=')[0][:2]}"
    for t in _FORMAT_WRAPPERS:
        word = t.format(title=title_base)
        out.append({
            "word": word,
            "type": "形式包装",
            "explain": f"借'{t.split('{title}')[1] if '{title}' in t else t}'这种形式包装情绪态度",
        })
    return out


# ---------- LLM 增强（可选） ----------


def llm_enhance(brand: str, value: str, candidates: List[Dict[str, str]]) -> List[Dict[str, str]]:
    provider = os.environ.get("XHS_LLM_PROVIDER", "").lower()
    if provider != "anthropic":
        return candidates
    try:
        from anthropic import Anthropic
        client = Anthropic()
        sys_prompt = (
            "你是品牌创意文案，参考 Allen 的方法（如'薯你会买''人类丰容''人生尽兴指南'）。"
            "针对给定品牌词和价值观，给出 6 个新造词候选 — 三种模式各 2 个："
            "①谐音造词 ②概念迁移 ③形式包装。返回 JSON 数组，每条 {word, type, explain}。"
        )
        msg = client.messages.create(
            model=os.environ.get("XHS_LLM_MODEL", "claude-haiku-4-5-20251001"),
            max_tokens=800,
            system=sys_prompt,
            messages=[{"role": "user",
                       "content": json.dumps({"brand": brand, "value": value}, ensure_ascii=False)}],
        )
        text = msg.content[0].text if msg.content else ""
        try:
            data = json.loads(text)
            if isinstance(data, list):
                return data
        except Exception:
            return candidates
    except Exception:
        return candidates
    return candidates


# ---------- 主流程 ----------


def render_text(brand: str, value: str, candidates: List[Dict[str, str]]) -> str:
    parts = [f"💡 「{brand}」造词候选（价值观：{value or '未指定'}）", ""]
    by_type: Dict[str, List[Dict[str, str]]] = {}
    for c in candidates:
        by_type.setdefault(c["type"], []).append(c)
    for t, items in by_type.items():
        parts.append(f"## {t}")
        for c in items:
            parts.append(f"  • **{c['word']}** — {c['explain']}")
        parts.append("")
    parts.append("─" * 50)
    parts.append("Allen 标准（参考 data/allen_method.md）：")
    parts.append("  ① 品牌资产嵌入  ② 对话感  ③ 价值观可解读")
    parts.append("  好的造词三层都满足；选一个最贴你品牌底色的去用。")
    return "\n".join(parts)


def main() -> int:
    p = argparse.ArgumentParser(prog="coin_word.py", description="品牌造词")
    p.add_argument("--brand", required=True, help="品牌词，如：小红薯 / 尽兴")
    p.add_argument("--value", default="", help="价值观，如：会买=会生活")
    p.add_argument("--n", type=int, default=12, help="返回多少候选")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.add_argument("--no-llm", action="store_true")
    args = p.parse_args()

    candidates: List[Dict[str, str]] = []
    candidates += coin_homophone(args.brand, args.value)[:3]
    candidates += coin_cross_domain(args.brand, args.value)[:6]
    candidates += coin_format_wrap(args.brand, args.value)[:3]

    if not args.no_llm:
        candidates = llm_enhance(args.brand, args.value, candidates)

    candidates = candidates[:args.n]

    if args.format == "json":
        print(json.dumps({"brand": args.brand, "value": args.value, "candidates": candidates},
                         ensure_ascii=False, indent=2))
    else:
        print(render_text(args.brand, args.value, candidates))
    return 0


if __name__ == "__main__":
    sys.exit(main())
