#!/usr/bin/env python3
"""Prepare paper inputs for the evidence-enhanced paper analysis workflow.

This script handles the deterministic parts of the Dify Scheme A workflow:
- validate that at least one local file or URL is provided
- copy local files and download URL inputs into a desktop work directory
- extract text from common document formats
- clean text
- split text into paper sections
- write prompt-ready files for LLM structured extraction and verification
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

MIN_TEXT_LENGTH = 800


def desktop_root() -> Path:
    return Path.home() / "Desktop" / "paper_analysis_results"


def timestamp() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def sanitize_filename(name: str, fallback: str = "paper") -> str:
    name = urllib.parse.unquote(name or "")
    name = name.strip().replace("\\", "/").split("/")[-1]
    name = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "_", name).strip("._")
    return name or fallback


def split_csv(values: Iterable[str] | None) -> list[str]:
    result: list[str] = []
    for value in values or []:
        for item in (value or "").split(","):
            item = item.strip()
            if item:
                result.append(item)
    return result


def safe_copy_file(src: Path, dest_dir: Path) -> Path:
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"local paper file not found: {src}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / sanitize_filename(src.name)
    if dest.exists():
        stem, suffix = dest.stem, dest.suffix
        i = 2
        while True:
            candidate = dest_dir / f"{stem}_{i}{suffix}"
            if not candidate.exists():
                dest = candidate
                break
            i += 1
    shutil.copy2(src, dest)
    return dest


def guess_download_name(url: str, content_type: str | None = None) -> str:
    path_name = sanitize_filename(urllib.parse.urlparse(url).path, "paper")
    if "." in path_name:
        return path_name
    if content_type:
        ct = content_type.lower()
        if "pdf" in ct:
            return path_name + ".pdf"
        if "word" in ct or "docx" in ct:
            return path_name + ".docx"
        if "html" in ct:
            return path_name + ".html"
        if "text" in ct:
            return path_name + ".txt"
    return path_name + ".pdf"


def download_url(url: str, dest_dir: Path, timeout: int = 60, max_retries: int = 2) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 paper-analysis-evidence"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                content_type = resp.headers.get("Content-Type")
                name = guess_download_name(url, content_type)
                dest = dest_dir / name
                if dest.exists():
                    stem, suffix = dest.stem, dest.suffix
                    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
                    dest = dest_dir / f"{stem}_{digest}{suffix}"
                with open(dest, "wb") as f:
                    shutil.copyfileobj(resp, f)
                return dest
        except Exception as exc:  # pragma: no cover - depends on network
            last_error = exc
            if attempt < max_retries:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed to download {url}: {last_error}")


def extract_pdf_text(path: Path) -> str:
    errors: list[str] = []
    for module_name in ("pypdf", "PyPDF2"):
        try:
            module = __import__(module_name)
            reader = module.PdfReader(str(path))
            pages = []
            for page in reader.pages:
                pages.append(page.extract_text() or "")
            text = "\n\n".join(pages).strip()
            if text:
                return text
        except Exception as exc:
            errors.append(f"{module_name}: {exc}")
    try:
        completed = subprocess.run(
            ["pdftotext", str(path), "-"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120,
        )
        text = completed.stdout.strip()
        if text:
            return text
    except Exception as exc:
        errors.append(f"pdftotext: {exc}")
    raise RuntimeError("could not extract PDF text. install pypdf or poppler-utils. " + "; ".join(errors))


def extract_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<[^>]+>", "", xml)
    entities = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&apos;": "'"}
    for k, v in entities.items():
        xml = xml.replace(k, v)
    return xml.strip()


def extract_html_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p>", "\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return text.strip()


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf_text(path)
    if suffix == ".docx":
        return extract_docx_text(path)
    if suffix in {".txt", ".md", ".markdown"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix in {".html", ".htm"}:
        return extract_html_text(path)
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        raise RuntimeError(f"unsupported document format: {path.name}. Use PDF, DOCX, TXT, MD, or HTML. {exc}")


def clean_for_analysis(raw_text: str, min_length: int = MIN_TEXT_LENGTH) -> tuple[str, int, str]:
    if not raw_text or not isinstance(raw_text, str):
        return "", 0, "input text is empty or invalid"
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\nReferences[\s\S]*$", "", text, flags=re.I)
    text = re.sub(r"\nBibliography[\s\S]*$", "", text, flags=re.I)
    text = text.strip()
    word_count = len(text)
    if word_count < min_length:
        return text, word_count, f"text is short ({word_count} chars); extraction may have failed"
    return text, word_count, ""


def normalize_newlines(text: str) -> str:
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def trim_references(text: str) -> str:
    if not text:
        return ""
    patterns = [r"\n\s*(references|bibliography)\s*$", r"\n\s*参考文献\s*$"]
    cut_positions = []
    for p in patterns:
        m = re.search(p, text, flags=re.I | re.M)
        if m:
            cut_positions.append(m.start())
    if cut_positions:
        text = text[:min(cut_positions)]
    return text.strip()


def heading_patterns() -> dict[str, list[str]]:
    return {
        "abstract": [r"abstract", r"摘要"],
        "intro": [r"introduction", r"intro", r"引言", r"绪论"],
        "related": [r"related work", r"background", r"preliminar(?:y|ies)", r"相关工作", r"背景", r"预备知识"],
        "method": [
            r"method", r"methods", r"methodology", r"approach", r"approaches", r"framework", r"model", r"architecture",
            r"proposed method", r"proposed approach", r"our method", r"our approach", r"方法", r"模型", r"框架", r"架构",
        ],
        "experiment": [
            r"experiment", r"experiments", r"experimental setup", r"evaluation", r"evaluations", r"results", r"analysis",
            r"implementation details", r"empirical study", r"实验", r"实验设置", r"实验结果", r"评估", r"结果", r"分析", r"实现细节",
        ],
        "conclusion": [r"conclusion", r"conclusions", r"discussion", r"limitations", r"future work", r"结论", r"讨论", r"局限性", r"未来工作"],
        "tail": [r"acknowledg(?:e)?ments?", r"appendix", r"references", r"bibliography", r"致谢", r"附录", r"参考文献"],
    }


def line_is_heading(line: str) -> bool:
    s = line.strip()
    return bool(s) and len(s) <= 120 and s.count(". ") < 2


def detect_heading_type(line: str, patterns: dict[str, list[str]]) -> str | None:
    s = line.strip()
    if not line_is_heading(s):
        return None
    normalized = re.sub(
        r"^\s*(section\s+)?((\d+(\.\d+)*)|[ivxlcdm]+|第\s*\d+\s*[章节部分])[\.\:\-\s]*",
        "",
        s,
        flags=re.I,
    ).strip()
    for sec_type, pats in patterns.items():
        for pat in pats:
            if re.fullmatch(rf"{pat}", normalized, flags=re.I):
                return sec_type
    for sec_type, pats in patterns.items():
        for pat in pats:
            if re.search(rf"\b{pat}\b", normalized, flags=re.I):
                return sec_type
    return None


def collect_headings(text: str) -> list[dict[str, object]]:
    patterns = heading_patterns()
    headings: list[dict[str, object]] = []
    offset = 0
    for line in text.split("\n"):
        sec_type = detect_heading_type(line, patterns)
        if sec_type:
            headings.append({"type": sec_type, "title": line.strip(), "start": offset})
        offset += len(line) + 1
    headings.sort(key=lambda x: int(x["start"]))
    return headings


def get_section_by_heading(text: str, headings: list[dict[str, object]], target_type: str) -> str:
    candidates = [h for h in headings if h["type"] == target_type]
    if not candidates:
        return ""
    start = int(candidates[0]["start"])
    later = [int(h["start"]) for h in headings if int(h["start"]) > start]
    end = min(later) if later else len(text)
    return text[start:end].strip()


def fallback_window(text: str, keywords: list[str], max_len: int = 10000, search_start: int = 0) -> str:
    window_text = text[search_start:]
    best: int | None = None
    for kw in keywords:
        m = re.search(kw, window_text, flags=re.I)
        if m:
            pos = search_start + m.start()
            if best is None or pos < best:
                best = pos
    if best is None:
        return ""
    start = max(0, best - 150)
    end = min(len(text), start + max_len)
    return text[start:end].strip()


def normalize_section(section: str, max_len: int) -> str:
    if not section:
        return ""
    section = section.strip()
    section = re.sub(r"\n{3,}", "\n\n", section)
    return section[:max_len]


def split_sections(cleaned_text: str) -> dict[str, str]:
    text = trim_references(normalize_newlines(cleaned_text))
    if not text:
        return {
            "abstract_section": "", "intro_section": "", "method_section": "",
            "experiment_section": "", "conclusion_section": "", "paper_body": "",
        }
    headings = collect_headings(text)
    abstract = get_section_by_heading(text, headings, "abstract")
    if not abstract:
        m = re.search(r"(^|\n)\s*(abstract|摘要)\s*\n", text, flags=re.I)
        if m:
            start = m.start()
            next_heads = [int(h["start"]) for h in headings if int(h["start"]) > start]
            end = min(next_heads) if next_heads else min(len(text), start + 6000)
            abstract = text[start:end].strip()
        else:
            intro_heads = [int(h["start"]) for h in headings if h["type"] == "intro"]
            if intro_heads and intro_heads[0] > 200:
                abstract = text[:intro_heads[0]].strip()[:6000]
    intro = get_section_by_heading(text, headings, "intro")
    if not intro:
        m = re.search(r"(introduction|引言|绪论)", text[:max(3000, len(text)//5)], flags=re.I)
        if m:
            start = max(0, m.start() - 100)
            next_heads = [int(h["start"]) for h in headings if int(h["start"]) > start]
            end = min(next_heads) if next_heads else min(len(text), start + 8000)
            intro = text[start:end].strip()
    method = get_section_by_heading(text, headings, "method")
    if not method:
        intro_heads = [int(h["start"]) for h in headings if h["type"] == "intro"]
        method = fallback_window(text, [r"\bmethod\b", r"\bmethods\b", r"\bmethodology\b", r"\bapproach\b", r"\bframework\b", r"\barchitecture\b", r"\bmodel\b", r"方法", r"框架", r"架构", r"模型"], 12000, intro_heads[0] if intro_heads else 0)
    experiment = get_section_by_heading(text, headings, "experiment")
    if not experiment:
        method_heads = [int(h["start"]) for h in headings if h["type"] == "method"]
        experiment = fallback_window(text, [r"\bexperiments?\b", r"\bevaluation\b", r"\bresults\b", r"\banalysis\b", r"\bimplementation details\b", r"实验", r"评估", r"结果", r"分析", r"实现细节"], 12000, method_heads[0] if method_heads else 0)
    conclusion = get_section_by_heading(text, headings, "conclusion")
    if not conclusion:
        conclusion = fallback_window(text, [r"\bconclusion\b", r"\bconclusions\b", r"\bdiscussion\b", r"\blimitations\b", r"\bfuture work\b", r"结论", r"讨论", r"局限", r"未来工作"], 6000, len(text)//2)
    return {
        "abstract_section": normalize_section(abstract, 6000),
        "intro_section": normalize_section(intro, 8000),
        "method_section": normalize_section(method, 12000),
        "experiment_section": normalize_section(experiment, 12000),
        "conclusion_section": normalize_section(conclusion, 6000),
        "paper_body": text[:60000],
    }


STRUCTURED_PROMPT_TEMPLATE = """你是一位严谨的论文信息抽取器。请严格基于给定论文内容，输出一个 JSON 对象，不要输出 Markdown、不要解释、不要加 ```json。

输出字段必须包含：
{{
  "title": "",
  "task": "",
  "background": "",
  "problem_statement": "",
  "method_name": "",
  "method_core": "",
  "datasets": [],
  "baselines": [],
  "metrics": [],
  "main_results": [
    {{"dataset": "", "metric": "", "value": "", "baseline": "", "improvement": ""}}
  ],
  "ablations": [],
  "limitations": [],
  "claims": [],
  "contributions": [],
  "evidence_spans": [
    {{"field": "", "claim": "", "evidence": ""}}
  ]
}}

规则：
1. 只能写原文出现或可直接推出的信息，不要脑补。
2. 优先使用对应章节抽取信息；如果某章节为空或信息不足，必须从全文补充。
3. datasets、baselines、metrics 不允许因为章节为空而直接写空数组，必须先检查全文 paper_body、实验结果、实现细节、表格附近文本是否存在相关信息。
4. 只有在全文中也确实找不到时，才能写空字符串或空数组。
5. evidence_spans 至少给 6 条，每条都必须是原文中的直接证据片段或非常贴近原文的概括。
6. 数值结果优先来自实验部分、结果部分、分析部分或表格附近文本。
7. JSON 键名保持英文；JSON 中的自然语言内容使用 {language}。

论文摘要段：
{abstract_section}

引言段：
{intro_section}

方法段：
{method_section}

实验段：
{experiment_section}

结论段：
{conclusion_section}

全文：
{paper_body}
"""


VERIFICATION_PROMPT_TEMPLATE = """你是一位论文事实核验器。请对下面的结构化抽取结果做一致性校验，并输出 JSON 对象，不要输出 Markdown、不要解释。

输出格式：
{{
  "overall_score": 0,
  "hallucination_risk": "low/medium/high",
  "issues": [
    {{"field": "", "problem": "", "severity": "low/medium/high"}}
  ],
  "verified_claims": [
    {{"claim": "", "status": "supported/weak/unsupported", "evidence": ""}}
  ],
  "final_verdict": ""
}}

评分规则：
- 5：几乎无幻觉，证据充分
- 4：少量不严谨
- 3：有若干缺证据表述
- 2：存在明显不一致
- 1：大量幻觉或错读

要求：
1. JSON 键名保持英文。
2. JSON 中的自然语言内容使用 {language}。
3. 重点检查 datasets、baselines、metrics、main_results 是否遗漏或误抽。
4. 若抽取结果将原文存在的信息写成空数组或空字符串，请在 issues 中明确指出。
5. verified_claims 至少给 4 条。

原文：
{paper_body}

待校验JSON：
{{structured_json}}
"""


@dataclass
class PaperRecord:
    id: str
    source_type: str
    source: str
    input_file: str
    work_dir: str
    raw_text_file: str
    cleaned_text_file: str
    sections_file: str
    structured_prompt_file: str
    verification_prompt_file: str
    structured_json_file: str
    verification_json_file: str
    final_markdown_file: str
    final_html_file: str
    final_docx_file: str
    language: str
    word_count: int
    warning: str = ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def prepare_one(input_path: Path, source_type: str, source: str, batch_dir: Path, language: str, index: int) -> PaperRecord:
    paper_id = f"paper_{index:02d}_{sanitize_filename(input_path.stem, 'paper')}"
    paper_dir = batch_dir / paper_id
    for sub in ["input", "text", "sections", "prompts", "generated", "report"]:
        (paper_dir / sub).mkdir(parents=True, exist_ok=True)
    kept = safe_copy_file(input_path, paper_dir / "input") if input_path.parent != paper_dir / "input" else input_path
    raw = extract_text(kept)
    cleaned, word_count, warning = clean_for_analysis(raw)
    sections = split_sections(cleaned)
    raw_file = paper_dir / "text" / "raw_text.txt"
    cleaned_file = paper_dir / "text" / "cleaned_text.txt"
    sections_file = paper_dir / "sections" / "sections.json"
    structured_prompt = paper_dir / "prompts" / "01_structured_extraction_prompt.md"
    verification_prompt = paper_dir / "prompts" / "02_verification_prompt_template.md"
    structured_json = paper_dir / "generated" / "structured_result.json"
    verification_json = paper_dir / "generated" / "verification_result.json"
    final_md = paper_dir / "report" / "final_report.md"
    final_html = paper_dir / "report" / "final_report.html"
    final_docx = paper_dir / "report" / "final_report.docx"
    write_text(raw_file, raw)
    write_text(cleaned_file, cleaned)
    sections_file.write_text(json.dumps(sections, ensure_ascii=False, indent=2), encoding="utf-8")
    write_text(structured_prompt, STRUCTURED_PROMPT_TEMPLATE.format(language=language, **sections))
    write_text(verification_prompt, VERIFICATION_PROMPT_TEMPLATE.format(language=language, paper_body=sections["paper_body"]))
    if not structured_json.exists():
        write_text(structured_json, "{}\n")
    if not verification_json.exists():
        write_text(verification_json, "{}\n")
    return PaperRecord(
        id=paper_id,
        source_type=source_type,
        source=source,
        input_file=str(kept),
        work_dir=str(paper_dir),
        raw_text_file=str(raw_file),
        cleaned_text_file=str(cleaned_file),
        sections_file=str(sections_file),
        structured_prompt_file=str(structured_prompt),
        verification_prompt_file=str(verification_prompt),
        structured_json_file=str(structured_json),
        verification_json_file=str(verification_json),
        final_markdown_file=str(final_md),
        final_html_file=str(final_html),
        final_docx_file=str(final_docx),
        language=language,
        word_count=word_count,
        warning=warning,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare paper files for evidence-enhanced analysis.")
    parser.add_argument("--language", default="中文", choices=["中文", "英文"], help="Natural language for generated content.")
    parser.add_argument("--files", nargs="*", default=[], help="Local paper files. PDF, DOCX, TXT, MD, HTML are supported.")
    parser.add_argument("--urls", nargs="*", default=[], help="Paper PDF/direct URLs. Multiple comma-separated values are also accepted.")
    parser.add_argument("--output-root", default=str(desktop_root()), help="Root output directory. Defaults to ~/Desktop/paper_analysis_results.")
    args = parser.parse_args()

    files = [Path(p).expanduser().resolve() for p in args.files if p]
    urls = split_csv(args.urls)
    if not files and not urls:
        print("上传的文件和论文URL不能同时为空。", file=sys.stderr)
        return 2

    batch_dir = Path(args.output_root).expanduser() / timestamp()
    downloads_dir = batch_dir / "downloads"
    batch_dir.mkdir(parents=True, exist_ok=True)

    records: list[PaperRecord] = []
    index = 1
    for file_path in files:
        records.append(prepare_one(file_path, "local_file", str(file_path), batch_dir, args.language, index))
        index += 1
    for url in urls:
        downloaded = download_url(url, downloads_dir)
        records.append(prepare_one(downloaded, "url", url, batch_dir, args.language, index))
        index += 1

    manifest = {
        "workflow": "paper-analysis-evidence",
        "language": args.language,
        "created_at": timestamp(),
        "batch_dir": str(batch_dir),
        "papers": [asdict(r) for r in records],
        "next_steps": [
            "For each paper, send prompts/01_structured_extraction_prompt.md to the model and save the JSON-only answer to generated/structured_result.json.",
            "Then send prompts/02_verification_prompt_template.md plus the structured JSON to the model and save the JSON-only answer to generated/verification_result.json.",
            "Run scripts/render_report.py with the manifest to create final_report.md, final_report.html, and final_report.docx.",
        ],
    }
    manifest_path = batch_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "batch_dir": str(batch_dir), "papers": [r.id for r in records]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
