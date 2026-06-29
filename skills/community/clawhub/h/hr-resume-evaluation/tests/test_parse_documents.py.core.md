---
source: "hr-resume-evaluation/tests/test_parse_documents.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# test_parse_documents.py

- Source file: [[hr-resume-evaluation/tests/test_parse_documents.py|test_parse_documents.py]]
- Folder index: [[hr-resume-evaluation/tests/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 4.94 KB
- Modified: 2026-06-13T14:47:17

## Summary
- PY source sample: 174 lines.
- Imports: re, sys, types, pathlib, scripts.parse_documents
- Functions: test_stable_candidate_id_slugifies_file_stem, test_stable_candidate_id_uses_hash_for_non_ascii_stem, test_stable_candidate_id_distinguishes_chinese_stems, test_parse_markdown_utf8_returns_text_and_metadata, test_parse_txt_utf8_returns_text, test_parse_text_file_strips_utf8_bom, test_parse_text_normalizes_trailing_whitespace, test_parse_pdf_uses_pypdf_pdf_reader, test_parse_docx_uses_docx_document, test_parse_pdf_error_returns_parse_error, test_parse_empty_file_returns_empty_text_error, test_parse_unsupported_extension_returns_error

## Related files
- [[hr-resume-evaluation/tests/test_evaluate_resumes.py.core|test_evaluate_resumes.py]] - same folder
- [[hr-resume-evaluation/tests/test_llm_client.py.core|test_llm_client.py]] - same folder
- [[hr-resume-evaluation/tests/test_validate_results.py.core|test_validate_results.py]] - same folder
- [[hr-resume-evaluation/tests/test_render_reports.py.core|test_render_reports.py]] - same folder
- [[hr-resume-evaluation/tests/test_end_to_end_outputs.py.core|test_end_to_end_outputs.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
import re
import sys
import types
from pathlib import Path

from scripts.parse_documents import discover_resumes, parse_document, stable_candidate_id


def test_stable_candidate_id_slugifies_file_stem():
    assert stable_candidate_id(Path("Alice Resume.pdf")) == "alice-resume"


def test_stable_candidate_id_uses_hash_for_non_ascii_stem():
    candidate_id = stable_candidate_id(Path("张三 简历.pdf"))

    assert re.fullmatch(r"candidate-[0-9a-f]{8}", candidate_id)


def test_stable_candidate_id_distinguishes_chinese_stems():
    first_id = stable_candidate_id(Path("张三.md"))
    second_id = stable_candidate_id(Path("李四.md"))

    assert first_id != second_id


def test_parse_markdown_utf8_returns_text_and_metadata(tmp_path):
    resume = tmp_path / "resume.md"
    resume.write_text("# 张三\n\nPython developer\n", encoding="utf-8")

    parsed = parse_document(resume)

    assert parsed.ok is True
    assert parsed.text.startswith("# 张三")
    assert parsed.file_name == "resume.md"


def test_parse_txt_utf8_returns_text(tmp_path):
    resume = tmp_path / "resume.txt"
    resume.write_text("Revenue increased by 18% year over year.\n", encoding="utf-8")

    parsed = parse_document(resume)
```

## Processing notes
- encoding=utf-8-sig
