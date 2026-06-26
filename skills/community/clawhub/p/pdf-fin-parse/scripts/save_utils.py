"""结果落盘：单页 → 合并文档 → summary。

目标产物（与 SKILL.md 的"输出目录结构"对应）：
  {output_dir}/
  ├── output.md                # 按页拼接后的 Markdown
  ├── output.json              # 符合 assets/output_schema.json 的结构化 JSON（评测脚本读这个）
  ├── meta.json                # 元信息（耗时、模式、模型、failed_pages 等）
  ├── pages/                   # 每页独立结果（断点恢复用）
  │   ├── p{N}.json            # 模型原始结构化输出
  │   └── p{N}.md              # 该页 Markdown
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# 单页保存
# ---------------------------------------------------------------------------

def save_per_page(pages_dir: Path, page_no: int, page_result: Dict[str, Any]) -> None:
    pages_dir.mkdir(parents=True, exist_ok=True)
    (pages_dir / f"p{page_no}.json").write_text(
        json.dumps(page_result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (pages_dir / f"p{page_no}.md").write_text(
        page_result.get("markdown", ""), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# 合并 → 文档级 JSON（符合 output_schema.json）
# ---------------------------------------------------------------------------

def _merge_doc_json(
    *,
    input_path: str,
    total_pages: int,
    per_page_results: List[Dict[str, Any]],
    engine_tag: str,
) -> Dict[str, Any]:
    """把逐页结果聚合为文档级 JSON。

    - blocks: 跨页平铺，按 page → 原顺序
    - tables: 跨页平铺，table_id 用 "t_{seq:03d}"
    - 每个表的 engine 字段沿用该页的 engine（rules / vlm-normal / vlm-detail），
      不再被文档级 engine_tag 覆盖（router 后路径异构，per-table engine 才准确）
    """
    doc_id = Path(input_path).stem
    all_blocks: List[Dict[str, Any]] = []
    all_tables: List[Dict[str, Any]] = []
    table_seq = 0
    for pr in per_page_results:
        page_no = pr.get("page_no")
        page_engine = pr.get("engine") or engine_tag
        for b in pr.get("blocks") or []:
            b2 = dict(b)
            b2.setdefault("source_page", page_no)
            all_blocks.append(b2)
        for t in pr.get("tables") or []:
            table_seq += 1
            t2 = dict(t)
            t2["table_id"] = f"t_{table_seq:03d}"
            t2.setdefault("source_page", page_no)
            t2["engine"] = page_engine
            confidence = pr.get("confidence")
            if confidence is not None and "confidence" not in t2:
                t2["confidence"] = confidence
            # 防御性补齐 n_rows/n_cols
            cells = t2.get("cells") or []
            if cells:
                t2.setdefault("n_rows", max(c.get("row", 0) for c in cells) + 1)
                t2.setdefault("n_cols", max(c.get("col", 0) for c in cells) + 1)
            else:
                t2.setdefault("n_rows", 1)
                t2.setdefault("n_cols", 1)
            all_tables.append(t2)
    return {
        "doc_id": doc_id,
        "source_file": input_path,
        "pages": total_pages,
        "language": "zh",
        "blocks": all_blocks,
        "tables": all_tables,
    }


def _merge_doc_markdown(per_page_results: List[Dict[str, Any]]) -> str:
    """按页拼接 Markdown，并在每页前加 HTML 注释作锚点（与 byted-las 风格一致）。"""
    parts: List[str] = []
    for pr in per_page_results:
        page_no = pr.get("page_no", "?")
        md = pr.get("markdown", "")
        parts.append(f"\n<!-- page {page_no} -->\n")
        parts.append(md if md.endswith("\n") else md + "\n")
    return "".join(parts)


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

def save_final_outputs(
    out_dir: Path,
    summary: Dict[str, Any],
    per_page_results: List[Dict[str, Any]],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    doc_json = _merge_doc_json(
        input_path=summary["input"],
        total_pages=summary["total_pages"],
        per_page_results=per_page_results,
        engine_tag=summary["engine_tag"],
    )
    (out_dir / "output.json").write_text(
        json.dumps(doc_json, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md = _merge_doc_markdown(per_page_results)
    (out_dir / "output.md").write_text(md, encoding="utf-8")

    meta = {
        "input": summary["input"],
        "output_dir": summary["output_dir"],
        "task_id": summary["task_id"],
        "parse_mode": summary["parse_mode"],
        "model": summary["model"],
        "engine_tag": summary["engine_tag"],
        "total_pages": summary["total_pages"],
        "parsed_pages": summary["page_count"],
        "table_count": summary["table_count"],
        "block_count": summary["block_count"],
        "failed_pages": summary["failed_pages"],
        "wall_time_seconds": summary["wall_time_seconds"],
        "status": summary["status"],
    }
    if "routing" in summary:
        meta["routing"] = summary["routing"]
    (out_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md_size = len(md.encode("utf-8"))
    summary["markdown_size_bytes"] = md_size

    print(
        f"[save] doc={Path(summary['input']).name} "
        f"pages={summary['page_count']}/{summary['total_pages']} "
        f"tables={summary['table_count']} blocks={summary['block_count']} "
        f"failed={len(summary['failed_pages'])} "
        f"md={md_size}B time={summary['wall_time_seconds']}s",
        file=sys.stderr,
    )


# ---------------------------------------------------------------------------
# Summary 构造
# ---------------------------------------------------------------------------

def build_summary(
    *,
    input_path: str,
    output_dir: str,
    task_id: str,
    parse_mode: str,
    model: str,
    total_pages: int,
    per_page_results: List[Dict[str, Any]],
    failed_pages: List[Dict[str, Any]],
    wall_time_seconds: float,
) -> Dict[str, Any]:
    table_count = sum(len(pr.get("tables") or []) for pr in per_page_results)
    block_count = sum(len(pr.get("blocks") or []) for pr in per_page_results)
    status = "COMPLETED" if not failed_pages or per_page_results else "FAILED"
    if failed_pages and per_page_results:
        status = "PARTIAL"
    engine_tag = f"vlm-{parse_mode}"
    return {
        "status": status,
        "task_id": task_id,
        "input": input_path,
        "output_dir": output_dir,
        "parse_mode": parse_mode,
        "model": model,
        "engine_tag": engine_tag,
        "total_pages": total_pages,
        "page_count": len(per_page_results),
        "table_count": table_count,
        "block_count": block_count,
        "failed_pages": failed_pages,
        "wall_time_seconds": wall_time_seconds,
    }


# ---------------------------------------------------------------------------
# 预览（取自合并后的 markdown）
# ---------------------------------------------------------------------------

def extract_preview(_md_size: int, out_dir: Path, max_chars: int = 400) -> str:
    """从 output.md 提取前若干行作预览（跳过 HTML 注释和空行）。"""
    md_path = out_dir / "output.md"
    if not md_path.exists():
        return ""
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    parts: List[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("<!--"):
            continue
        parts.append(s)
        if sum(len(p) for p in parts) > max_chars:
            break
    preview = "\n".join(parts)
    return preview[:max_chars] + ("..." if len(preview) > max_chars else "")
