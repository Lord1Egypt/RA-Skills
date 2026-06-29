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

    assert parsed.ok is True
    assert "Revenue increased" in parsed.text


def test_parse_text_file_strips_utf8_bom(tmp_path):
    resume = tmp_path / "resume.txt"
    resume.write_text("Candidate summary\n", encoding="utf-8-sig")

    parsed = parse_document(resume)

    assert parsed.ok is True
    assert parsed.text == "Candidate summary"
    assert not parsed.text.startswith("\ufeff")


def test_parse_text_normalizes_trailing_whitespace(tmp_path):
    resume = tmp_path / "resume.txt"
    resume.write_text("\n\nLine one   \nLine two\t \n\n", encoding="utf-8")

    parsed = parse_document(resume)

    assert parsed.ok is True
    assert parsed.text == "Line one\nLine two"


def test_parse_pdf_uses_pypdf_pdf_reader(monkeypatch, tmp_path):
    calls = []

    class FakePage:
        def __init__(self, text):
            self._text = text

        def extract_text(self):
            return self._text

    class FakePdfReader:
        def __init__(self, path):
            calls.append(path)
            self.pages = [FakePage("First page"), FakePage("Second page")]

    fake_pypdf = types.ModuleType("pypdf")
    fake_pypdf.PdfReader = FakePdfReader
    monkeypatch.setitem(sys.modules, "pypdf", fake_pypdf)

    resume = tmp_path / "resume.pdf"
    parsed = parse_document(resume)

    assert parsed.ok is True
    assert parsed.text == "First page\nSecond page"
    assert calls == [resume]


def test_parse_docx_uses_docx_document(monkeypatch, tmp_path):
    calls = []

    class FakeParagraph:
        def __init__(self, text):
            self.text = text

    class FakeDocument:
        def __init__(self, path):
            calls.append(path)
            self.paragraphs = [FakeParagraph("Intro"), FakeParagraph("Experience")]

    fake_docx = types.ModuleType("docx")
    fake_docx.Document = FakeDocument
    monkeypatch.setitem(sys.modules, "docx", fake_docx)

    resume = tmp_path / "resume.docx"
    parsed = parse_document(resume)

    assert parsed.ok is True
    assert parsed.text == "Intro\nExperience"
    assert calls == [resume]


def test_parse_pdf_error_returns_parse_error(monkeypatch, tmp_path):
    class FakePdfReader:
        def __init__(self, path):
            raise RuntimeError("bad pdf")

    fake_pypdf = types.ModuleType("pypdf")
    fake_pypdf.PdfReader = FakePdfReader
    monkeypatch.setitem(sys.modules, "pypdf", fake_pypdf)

    parsed = parse_document(tmp_path / "resume.pdf")

    assert parsed.ok is False
    assert parsed.error is not None
    assert parsed.error.startswith("parse_error:")
    assert parsed.error == "parse_error: bad pdf"


def test_parse_empty_file_returns_empty_text_error(tmp_path):
    resume = tmp_path / "empty.txt"
    resume.write_text(" \n\t\n", encoding="utf-8")

    parsed = parse_document(resume)

    assert parsed.ok is False
    assert parsed.error == "empty_text"


def test_parse_unsupported_extension_returns_error(tmp_path):
    resume = tmp_path / "resume.xlsx"
    resume.write_text("not supported", encoding="utf-8")

    parsed = parse_document(resume)

    assert parsed.ok is False
    assert parsed.error == "unsupported_extension"


def test_discover_resumes_filters_supported_files(tmp_path):
    (tmp_path / "a.md").write_text("A", encoding="utf-8")
    (tmp_path / "b.markdown").write_text("B", encoding="utf-8")
    (tmp_path / "c.txt").write_text("C", encoding="utf-8")
    (tmp_path / "d.pdf").write_text("D", encoding="utf-8")
    (tmp_path / "e.docx").write_text("E", encoding="utf-8")
    (tmp_path / "f.PDF").write_text("F", encoding="utf-8")
    (tmp_path / "z.xlsx").write_text("ignored", encoding="utf-8")

    resumes = discover_resumes(tmp_path)

    assert [path.name for path in resumes] == [
        "a.md",
        "b.markdown",
        "c.txt",
        "d.pdf",
        "e.docx",
        "f.PDF",
    ]
