# -*- coding: utf-8 -*-
"""
check_duplicate.py — 三层查重

用法：
    python3 check_duplicate.py --open_id ou_xxx --title "论文标题" \
        [--arxiv_id 2401.12345] [--text_path /tmp/paperkb/xxx.txt]

三层逻辑（命中任意一层即返回）：
    第一层  arxiv_id 完全一致           → duplicate（确定重复）
    第二层  标题归一化后完全一致         → duplicate（确定重复）
    第三层  标题相似度>0.92 或 内容指纹相似度>0.90
                                        → possible_duplicate（疑似，需问用户）

输出单行 JSON：
    {"success": true, "duplicate": false}
    {"success": true, "duplicate": true, "match_type": "arxiv_id",
     "existing": {...已存在文档的目录条目...}}
    {"success": true, "duplicate": false, "possible_duplicate": true,
     "match_type": "similar_title", "similarity": 0.95, "existing": {...}}
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

import kb_common as kb


def _out(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def _fail(error: str, message: str) -> None:
    _out({"success": False, "error": error, "message": message})
    sys.exit(0)


def _ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--arxiv_id", default="")
    parser.add_argument("--text_path", default="",
                        help="正文 txt 路径，提供时启用内容指纹比对")
    args = parser.parse_args()

    user = kb.get_user_by_open_id(args.open_id)
    if user is None:
        _fail("user_not_registered", "该用户尚未注册，请先完成初始化。")

    catalog = kb.read_catalog(user["gitea_username"])
    docs = catalog["documents"]

    norm_title = kb.normalize_for_match(args.title)
    fingerprint = ""
    if args.text_path and Path(args.text_path).exists():
        fingerprint = kb.make_fingerprint(
            Path(args.text_path).read_text(encoding="utf-8", errors="ignore"))

    # 第一层：arxiv_id 精确匹配
    if args.arxiv_id:
        base_id = args.arxiv_id.split("v")[0]
        for d in docs:
            existing_id = (d.get("arxiv_id") or "").split("v")[0]
            if existing_id and existing_id == base_id:
                _out({"success": True, "duplicate": True,
                      "match_type": "arxiv_id", "existing": d})
                return

    # 第二层：标题精确匹配（归一化后）
    for d in docs:
        if kb.normalize_for_match(d.get("title", "")) == norm_title:
            _out({"success": True, "duplicate": True,
                  "match_type": "title", "existing": d})
            return

    # 第三层：相似度
    best = None
    best_score = 0.0
    best_type = ""
    for d in docs:
        t_sim = _ratio(norm_title, kb.normalize_for_match(d.get("title", "")))
        if t_sim > best_score:
            best, best_score, best_type = d, t_sim, "similar_title"
        if fingerprint and d.get("fingerprint"):
            f_sim = _ratio(fingerprint, d["fingerprint"])
            if f_sim > best_score:
                best, best_score, best_type = d, f_sim, "similar_content"

    if best is not None and (
        (best_type == "similar_title" and best_score > 0.92)
        or (best_type == "similar_content" and best_score > 0.90)
    ):
        _out({"success": True, "duplicate": False, "possible_duplicate": True,
              "match_type": best_type, "similarity": round(best_score, 3),
              "existing": best})
        return

    _out({"success": True, "duplicate": False})


if __name__ == "__main__":
    main()
