#!/usr/bin/env python3
"""Utilities for rolling multi-paper innovation comparison."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


SUPPORTED = {".pdf", ".txt", ".md"}


def read_state(out_dir: Path) -> dict:
    state_path = out_dir / "paper_summ_state.json"
    if not state_path.exists():
        raise SystemExit(f"State file not found: {state_path}")
    return json.loads(state_path.read_text(encoding="utf-8"))


def write_state(out_dir: Path, state: dict) -> None:
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    (out_dir / "paper_summ_state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def safe_stem(path: Path) -> str:
    text = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", path.stem, flags=re.UNICODE)
    return text[:120].strip("._") or "paper"


def extract_pdf(path: Path) -> str:
    errors = []
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        parts = []
        for index, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:  # pragma: no cover - best effort extraction
                text = f"[Page {index} extraction failed: {exc}]"
            parts.append(f"\n\n--- Page {index} ---\n{text}")
        return "".join(parts).strip()
    except Exception as exc:
        errors.append(f"pypdf: {exc}")

    try:
        from PyPDF2 import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        parts = []
        for index, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:  # pragma: no cover
                text = f"[Page {index} extraction failed: {exc}]"
            parts.append(f"\n\n--- Page {index} ---\n{text}")
        return "".join(parts).strip()
    except Exception as exc:
        errors.append(f"PyPDF2: {exc}")

    return "[PDF text extraction failed]\n" + "\n".join(errors)


def extract_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path)
    return path.read_text(encoding="utf-8", errors="replace")


def discover(folder: Path) -> list[Path]:
    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED]
    return sorted(files, key=lambda p: p.name.lower())


def cmd_init(args: argparse.Namespace) -> None:
    folder = Path(args.folder).expanduser().resolve()
    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"Paper folder does not exist: {folder}")
    out_dir = Path(args.out).expanduser().resolve() if args.out else folder

    papers = discover(folder)
    if len(papers) > 20:
        raise SystemExit(f"Found {len(papers)} supported papers; maximum is 20.")
    if not papers:
        raise SystemExit(f"No supported paper files found in: {folder}")

    text_dir = out_dir / "extracted_text"
    text_dir.mkdir(parents=True, exist_ok=True)

    paper_items = []
    for index, paper in enumerate(papers, start=1):
        paper_id = f"P{index:03d}"
        extracted_path = text_dir / f"{paper_id}_{safe_stem(paper)}.txt"
        text = extract_file(paper)
        header = f"Paper ID: {paper_id}\nSource: {paper}\nExtracted at: {datetime.now().isoformat(timespec='seconds')}\n\n"
        extracted_path.write_text(header + text, encoding="utf-8", errors="replace")
        paper_items.append(
            {
                "id": paper_id,
                "source": str(paper),
                "extracted_text": str(extracted_path),
                "status": "unread",
                "title": "",
            }
        )

    state = {
        "paper_folder": str(folder),
        "out_dir": str(out_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "papers": paper_items,
        "syntheses": [],
    }
    write_state(out_dir, state)

    summ = out_dir / "summ.md"
    if not summ.exists():
        summ.write_text(
            "# 多篇论文创新点对比 summ\n\n"
            f"- 论文文件夹: `{folder}`\n"
            f"- 论文数量: {len(papers)}\n"
            f"- 创建时间: {state['created_at']}\n\n"
            "## 论文清单\n\n"
            + "\n".join(f"- {p['id']}: `{Path(p['source']).name}`" for p in paper_items)
            + "\n\n## 单篇论文总结\n\n## 跨论文对比与可融合研究点\n\n## 最终研究机会排序\n\n",
            encoding="utf-8",
        )

    print(json.dumps({"out_dir": str(out_dir), "summ": str(summ), "papers": paper_items}, ensure_ascii=False, indent=2))


def cmd_next(args: argparse.Namespace) -> None:
    out_dir = Path(args.out).expanduser().resolve()
    state = read_state(out_dir)
    for paper in state["papers"]:
        if paper["status"] == "unread":
            print(json.dumps(paper, ensure_ascii=False, indent=2))
            return
    print(json.dumps({"done": True, "summ": str(out_dir / "summ.md")}, ensure_ascii=False, indent=2))


def insert_before_final_sections(summ: Path, content: str, section: str) -> None:
    text = summ.read_text(encoding="utf-8")
    marker = f"\n## {section}\n"
    index = text.find(marker)
    if index == -1:
        text = text.rstrip() + "\n\n" + content.strip() + "\n"
    else:
        text = text[:index].rstrip() + "\n\n" + content.strip() + "\n" + text[index:]
    summ.write_text(text, encoding="utf-8")


def cmd_add_paper(args: argparse.Namespace) -> None:
    out_dir = Path(args.out).expanduser().resolve()
    state = read_state(out_dir)
    paper_id = args.paper_id
    summary = Path(args.summary_file).read_text(encoding="utf-8")
    summ = out_dir / "summ.md"
    insert_before_final_sections(summ, summary, "跨论文对比与可融合研究点")

    found = False
    for paper in state["papers"]:
        if paper["id"] == paper_id:
            paper["status"] = "processed"
            paper["processed_at"] = datetime.now().isoformat(timespec="seconds")
            title_match = re.search(r"^###\s+P\d+\s+-\s+(.+)$", summary, re.MULTILINE)
            if title_match:
                paper["title"] = title_match.group(1).strip()
            found = True
            break
    if not found:
        raise SystemExit(f"Unknown paper id: {paper_id}")
    write_state(out_dir, state)
    print(f"Added paper summary for {paper_id} to {summ}")


def cmd_add_synthesis(args: argparse.Namespace) -> None:
    out_dir = Path(args.out).expanduser().resolve()
    state = read_state(out_dir)
    summary = Path(args.summary_file).read_text(encoding="utf-8")
    summ = out_dir / "summ.md"
    text = summ.read_text(encoding="utf-8")
    marker = "\n## 最终研究机会排序\n"
    index = text.find(marker)
    block = summary.strip() + "\n"
    if index == -1:
        text = text.rstrip() + "\n\n" + block
    else:
        text = text[:index].rstrip() + "\n\n" + block + text[index:]
    summ.write_text(text, encoding="utf-8")

    state["syntheses"].append(
        {
            "title": args.title,
            "papers": [p.strip() for p in args.papers.split(",") if p.strip()],
            "added_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    write_state(out_dir, state)
    print(f"Added synthesis '{args.title}' to {summ}")


def cmd_finalize(args: argparse.Namespace) -> None:
    out_dir = Path(args.out).expanduser().resolve()
    state = read_state(out_dir)
    unread = [p["id"] for p in state["papers"] if p["status"] != "processed"]
    result = {
        "summ": str(out_dir / "summ.md"),
        "total": len(state["papers"]),
        "processed": len(state["papers"]) - len(unread),
        "unread": unread,
        "syntheses": len(state.get("syntheses", [])),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("folder")
    p_init.add_argument("--out")
    p_init.set_defaults(func=cmd_init)

    p_next = sub.add_parser("next")
    p_next.add_argument("out")
    p_next.set_defaults(func=cmd_next)

    p_add = sub.add_parser("add-paper")
    p_add.add_argument("out")
    p_add.add_argument("--paper-id", required=True)
    p_add.add_argument("--summary-file", required=True)
    p_add.set_defaults(func=cmd_add_paper)

    p_syn = sub.add_parser("add-synthesis")
    p_syn.add_argument("out")
    p_syn.add_argument("--title", required=True)
    p_syn.add_argument("--papers", required=True)
    p_syn.add_argument("--summary-file", required=True)
    p_syn.set_defaults(func=cmd_add_synthesis)

    p_fin = sub.add_parser("finalize")
    p_fin.add_argument("out")
    p_fin.set_defaults(func=cmd_finalize)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
