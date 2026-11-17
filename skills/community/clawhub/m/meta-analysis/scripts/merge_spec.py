#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_spec.py — 跨轮追问的线程驻留、确定性 spec 合并（ct-* 家族共享）

为什么需要：
    多轮追问时，前一轮已确认的字段必须无损"继承"到本轮，避免 LLM 只读到
    当前句子而漏带早轮参数。本脚本不落盘、不跨轮缓存——prev spec 由 Agent
    从对话里（上一轮回显的设定块）以 stdin JSON 传入，cur 为本轮新解析的 partial / full spec。
    合并 = 字典覆盖（cur 覆盖 prev；cur 缺省字段继承 prev）。纯确定性，无脆弱分类器。

    本文件为 ct-* 家族唯一权威副本，原位于 ct-samplesize/scripts/，已提升至此，
    供所有 NL 对话技能（ct-samplesize / ct-literature / ct-registry / ct-safety / meta-analysis …）
    按 `ct-base/references/continuity.md` 模式 A 调用，避免多副本漂移。

输入（stdin JSON）：
    {
      "prev": {完整或部分的上一轮 spec},
      "cur":  {本轮解析的部分或完整 spec},
      "required": ["test", "effect", ...]   # 可选：合并后校验必填键
    }
    说明：若 prev 为空（首轮/无前情），则 merged 直接等于 cur。

输出（stdout JSON）：
    {
      "merged": {...},
      "inherited": [...],   # 从 prev 继承、cur 未覆盖的字段
      "overridden": [...],  # prev 中有、被 cur 改变值的字段
      "missing_required": [...]  # required 中合并后仍缺失/为空的字段
    }

用法（在脚本所在目录运行；开发态 ct-base/scripts/ 或注入后 <skill>/scripts/ 均可）：
    echo '{"prev":{"test":"ttest_ind","effect":0.5,"alpha":0.05,"power":0.8},"cur":{"power":0.9}}' \
      | python merge_spec.py

退出码：
    0 = 成功（即便 missing_required 非空也返回 0，由调用方决定是否拦截）
    2 = stdin 解析失败 / 非 JSON
"""

import sys
import json


def _is_empty(v):
    return v is None or v == "" or v == [] or v == {}


def merge(prev, cur, required):
    merged = dict(prev) if prev else {}
    inherited = []
    overridden = []

    for k, v in (cur or {}).items():
        if k in merged and merged[k] != v:
            overridden.append(k)
        # k not in merged：新增字段，直接并入；不计入 inherited/overridden 变化审计
        merged[k] = v

    # inherited：prev 有、cur 未提及的字段
    inherited = [k for k in (prev or {}) if k not in (cur or {})]

    missing = [
        k for k in (required or [])
        if k not in merged or _is_empty(merged.get(k))
    ]

    return {
        "merged": merged,
        "inherited": inherited,
        "overridden": overridden,
        "missing_required": missing,
    }


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        # 无前情输入：回显错误，由调用方决定（通常当作首轮，直接以 cur 为 spec）
        print(json.dumps({"error": "empty stdin; treat as first turn (no prev)"},
                         ensure_ascii=False))
        return 0

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "invalid JSON from stdin", "detail": str(e)},
                         ensure_ascii=False))
        return 2

    prev = data.get("prev") or {}
    cur = data.get("cur")
    if cur is None:
        # 只有 prev、没有 cur：原样返回 prev（调用方可能只想校验）
        cur = {}
    required = data.get("required") or []

    out = merge(prev, cur, required)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
