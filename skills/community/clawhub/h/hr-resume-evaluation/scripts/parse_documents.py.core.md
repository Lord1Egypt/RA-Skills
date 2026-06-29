---
source: "hr-resume-evaluation/scripts/parse_documents.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# parse_documents.py

- Source file: [[hr-resume-evaluation/scripts/parse_documents.py|parse_documents.py]]
- Folder index: [[hr-resume-evaluation/scripts/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 2.29 KB
- Modified: 2026-06-13T14:49:22

## Summary
- PY source sample: 82 lines.
- Imports: __future__, hashlib, re, dataclasses, pathlib
- Classes: ParsedDocument
- Functions: stable_candidate_id, discover_resumes, parse_document, _read_pdf, _read_docx, _normalize_text

## Related files
- [[hr-resume-evaluation/scripts/evaluate_resumes.py.core|evaluate_resumes.py]] - same folder
- [[hr-resume-evaluation/scripts/llm_client.py.core|llm_client.py]] - same folder
- [[hr-resume-evaluation/scripts/validate_results.py.core|validate_results.py]] - same folder
- [[hr-resume-evaluation/scripts/render_reports.py.core|render_reports.py]] - same folder
- [[hr-resume-evaluation/scripts/__init__.py.core|__init__.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path


SUPPORTED_RESUME_SUFFIXES = {".md", ".markdown", ".txt", ".pdf", ".docx"}
TEXT_SUFFIXES = {".md", ".markdown", ".txt"}


@dataclass(frozen=True)
class ParsedDocument:
    path: Path
    file_name: str
    candidate_id: str
    text: str
    ok: bool
    error: str | None = None


def stable_candidate_id(path: Path) -> str:
    stem = Path(path).stem.strip().lower()
    slug = re.sub(r"[^A-Za-z0-9]+", "-", stem).strip("-")
    if stem.isascii():
        return slug or "candidate"

    digest = hashlib.sha256(stem.encode("utf-8")).hexdigest()[:8]
    return f"{slug}-{digest}" if slug else f"candidate-{digest}"


def discover_resumes(folder: Path) -> list[Path]:
    return sorted(
        path
        for path in Path(folder).iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_RESUME_SUFFIXES
    )


def parse_document(path: Path) -> ParsedDocument:
    path = Path(path)
    candidate_id = stable_candidate_id(path)
    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_RESUME_SUFFIXES:
        return ParsedDocument(path, path.name, ca
```

## Processing notes
- encoding=utf-8-sig
