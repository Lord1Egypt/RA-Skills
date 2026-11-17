#!/usr/bin/env python3
"""Cut the posting and the CV into addressable evidence blocks.

Port of marketfit-job-lens src/ai/evidenceBlocks.js. The parameters are fixed by the
skill's shared contract and are load-bearing: 900 characters per block, 80 blocks per
source, split on blank lines or a newline before a bullet / number / CJK numeral,
sentence-split over-long paragraphs on [。.!?], drop chunks under 8 characters.

Why blocks exist: every analytical sentence in an assessment must point at text that
really exists. That is a plausibility bound, not a proof -- it guarantees a claim
points at something real, never that the claim follows from it. Carry that sentence
into the skill's own output; a reader who mistakes it for proof is worse off than one
who was told nothing.

HOW LOOSE THAT BOUND IS DEPENDS ON THE DOCUMENT, AND IT IS LOOSEST EXACTLY WHERE A
POSTING IS SHORT. Paragraphs are packed up to the 900-character ceiling rather than
kept one-per-block, so a small source collapses into very few blocks. Measured
2026-08-10 on a realistic 1502-character posting: TWO blocks, the first 872 characters
covering the title, every must-have and every nice-to-have. A row citing JD-001 for
"PhD required" is then pointing at a slab that also contains the language preference
and the publication venues -- the citation resolves, and localises almost nothing.
This is faithful to the port (marketfit packs identically) and the parameters are
fixed by the shared contract, so it is a recorded limit rather than a bug to fix here.
What follows from it: on a short posting the block reference is close to worthless as
localisation, and the requirement row's own quoted wording is what a reader must
actually check. Do not let a resolving reference stand in for having read the text.

Every length here is counted in CHARACTERS. Not bytes, and not latin display columns.
A nine-character Chinese line is a real line; measuring it in bytes would keep junk and
measuring it in latin width would silently delete a third of a Chinese posting.

Exit 2 still writes a receipt, verdict "could_not_run". The single exception is a
workspace directory that does not exist: there is nothing to append to, and creating it
would leave a journal for a run that never happened, so that case exits 2 silently in
the journal and loudly on stderr.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import journal  # noqa: E402

GATE = "evidence_blocks"

MAX_BLOCK_CHARS = 900
MAX_BLOCKS_PER_SOURCE = 80
MIN_CHUNK_CHARS = 8

_PARAGRAPH_SPLIT = re.compile(r"\n{2,}|\n(?=\s*[-*0-9一二三四五六七八九十])")
_SENTENCE_SPLIT = re.compile(r"(?<=[。.!?])\s+")


def normalize_block_text(value: str) -> str:
    text = str(value or "")
    text = text.replace("\u00a0", " ")   # NBSP: pasted postings are full of them
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_long_paragraph(paragraph: str) -> list[str]:
    if len(paragraph) <= MAX_BLOCK_CHARS:
        return [paragraph]
    sentences = [s for s in _SENTENCE_SPLIT.split(paragraph) if s]
    if len(sentences) <= 1:
        return [paragraph[i:i + MAX_BLOCK_CHARS]
                for i in range(0, len(paragraph), MAX_BLOCK_CHARS)]
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if not current:
            current = sentence
        elif len(current) + 1 + len(sentence) <= MAX_BLOCK_CHARS:
            current = f"{current} {sentence}"
        else:
            chunks.append(current)
            current = sentence
    if current:
        chunks.append(current)
    return chunks


def split_into_chunks(text: str) -> list[str]:
    normalized = normalize_block_text(text)
    paragraphs = [p.strip() for p in _PARAGRAPH_SPLIT.split(normalized)]
    paragraphs = [p for p in paragraphs if p]
    if not paragraphs and normalized:
        paragraphs = [normalized]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        for piece in split_long_paragraph(paragraph):
            if not current:
                current = piece
            elif len(current) + 1 + len(piece) <= MAX_BLOCK_CHARS:
                current = f"{current}\n{piece}"
            else:
                chunks.append(current)
                current = piece
    if current:
        chunks.append(current)
    return [c for c in chunks if len(c) >= MIN_CHUNK_CHARS]


def build_blocks(text: str, prefix: str, source: str) -> tuple[list[dict], int]:
    """(blocks, chunks the source actually produced).

    The second value is returned rather than discarded because the ceiling below it
    is a DELETION. Measured on a 147KB posting: 129 chunks, 80 kept, 39% of the
    document gone — and the receipt read `BLOCKS: 81`, which is exactly what a
    complete run of a shorter posting looks like. Every analytical sentence in an
    assessment is supposed to point at a block; a citation into the dropped tail
    cannot resolve, and there was nothing anywhere saying a tail existed.
    """
    chunks = split_into_chunks(text)
    kept = chunks[:MAX_BLOCKS_PER_SOURCE]
    return ([{"id": f"{prefix}-{index + 1:03d}", "source": source, "text": chunk}
             for index, chunk in enumerate(kept)], len(chunks))


def flatten_yaml_to_text(obj, prefix: str = "") -> str:
    """Render a parsed YAML document as one leaf per paragraph.

    The master profile is YAML, and assess must be able to cite it. Chunking the raw
    file would put YAML punctuation inside blocks; flattening to "path: value" lines
    keeps every block quotable by a human reviewer checking a citation.
    """
    parts: list[str] = []
    if isinstance(obj, dict):
        for key in obj:
            child = f"{prefix}.{key}" if prefix else str(key)
            parts.append(flatten_yaml_to_text(obj[key], child))
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            parts.append(flatten_yaml_to_text(item, f"{prefix}[{index}]"))
    else:
        parts.append(f"{prefix}: {obj}" if prefix else str(obj))
    return "\n\n".join(p for p in parts if p)


def read_source(path: pathlib.Path) -> str:
    """The source as text. Raises journal.YamlUnreadable on an unusable input.

    Both branches raise it — a .txt that cannot be read is the same class of failure
    as a .yaml that cannot be parsed, and main() routes both to the same cannot_run.
    Silently returning "" instead would produce ZERO blocks, and zero blocks is a
    state the rest of assess mode reads as "the posting says nothing".
    """
    if path.suffix.lower() in {".yaml", ".yml"}:
        return flatten_yaml_to_text(journal.load_yaml(path))
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise journal.YamlUnreadable(path, f"is not valid UTF-8 ({exc.reason})") from exc
    except OSError as exc:
        raise journal.YamlUnreadable(
            path, f"could not be read ({exc.strerror or exc})") from exc


def cannot_run(workspace: pathlib.Path, reason: str, code: str = "NO_INPUT") -> int:
    """Exactly one receipt on the could-not-run path, then exit 2.

    A skipped gate produces no output, and no output looks exactly like a clean run --
    so the one state that most needs a receipt is this one. The exception is a
    workspace directory that is not there: nothing to append to, and conjuring one
    would leave a journal for a run that never happened.

    `code` is NO_INPUT for a file that is absent and journal.UNREADABLE_INPUT for one
    that is present and unusable. Those are different instructions to the reader.
    """
    print(f"cannot run: {reason}", file=sys.stderr)
    if workspace.is_dir():
        journal.receipt(workspace, GATE, {}, "could_not_run", [f"{code}: {reason}"])
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build evidence blocks for an assessment.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--jd", type=pathlib.Path, default=None)
    parser.add_argument("--cv", type=pathlib.Path, default=None)
    parser.add_argument("--out", type=pathlib.Path, default=None)
    args = parser.parse_args(argv)

    workspace = args.workspace
    jd_path = args.jd or workspace / "posting-source.txt"
    cv_path = args.cv or workspace / "cv-source.txt"
    out_path = args.out or workspace / "evidence-blocks.json"

    if not workspace.is_dir():
        return cannot_run(workspace, f"workspace {workspace} does not exist")
    for label, path in (("posting-source.txt", jd_path), ("cv source", cv_path)):
        if not path.exists():
            return cannot_run(workspace, f"{label} not found at {path}")

    blocks: list[dict] = []
    findings: list[str] = []
    for prefix, source, path in (("JD", "jd", jd_path), ("CV", "cv", cv_path)):
        try:
            text = read_source(path)
        except journal.YamlUnreadable as exc:
            return cannot_run(workspace, str(exc), journal.UNREADABLE_INPUT)
        produced, total = build_blocks(text, prefix, source)
        blocks += produced
        if total > MAX_BLOCKS_PER_SOURCE:
            findings.append(
                f"SOURCE_TRUNCATED: {path.name} produced {total} blocks and only the "
                f"first {MAX_BLOCKS_PER_SOURCE} were kept — {total - MAX_BLOCKS_PER_SOURCE} "
                f"were dropped, so nothing in the assessment can cite the tail of this "
                f"source and a citation into it will simply not resolve. Split the "
                f"source, or say in the assessment which part of it was read")

    payload = {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": {
            "jd": {"path": str(jd_path), "sha256": journal.sha256_file(jd_path)},
            "cv": {"path": str(cv_path), "sha256": journal.sha256_file(cv_path)},
        },
        "blocks": blocks,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    journal.receipt(
        workspace, GATE,
        {"jd": payload["sources"]["jd"]["sha256"], "cv": payload["sources"]["cv"]["sha256"]},
        "recorded", [f"BLOCKS: {len(blocks)}"] + findings)
    print(f"BLOCKS: {len(blocks)} written to {out_path}")
    for finding in findings:
        print(finding)
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
