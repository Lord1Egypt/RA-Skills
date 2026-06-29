#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""input_parser.py — JD 与简历输入解析器（text/url/file 三种入口）。"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urlparse


class InputFetchError(Exception):
    pass


class UnsupportedFormatError(Exception):
    pass


class InputTooLargeError(Exception):
    pass


class InputTooShortError(Exception):
    pass


SITE_SELECTORS = {
    "zhipin.com": ".job-sec .text",
    "lagou.com": ".job_detail",
    "linkedin.com": ".description__text",
}

_KNOWN_FILE_EXTS = (".txt", ".md", ".docx", ".pdf", ".doc")


def detect_input_type(jd_text: str | None = None,
                      jd_url: str | None = None,
                      jd_file: str | None = None) -> str:
    """识别输入种类，互斥校验。"""
    provided = [name for name, val in
                (("text", jd_text), ("url", jd_url), ("file", jd_file)) if val]
    if len(provided) == 0:
        raise ValueError("必须提供 jd_text / jd_url / jd_file 中的一个")
    if len(provided) > 1:
        raise ValueError(f"jd_text / jd_url / jd_file 互斥，但同时收到: {provided}")
    return provided[0]


def fetch_url(url: str, timeout: int = 15) -> str:
    """抓取目标 URL 并基于站点选择器抽取 JD 正文。任何失败均抛 InputFetchError。"""
    try:
        import httpx
        from bs4 import BeautifulSoup
    except ImportError as e:
        raise InputFetchError(
            f"缺少依赖 ({e})，URL 抓取失败，请用 --jd-text 重新运行"
        ) from e

    headers = {"User-Agent": "jd-truth-detector/1.0"}
    try:
        resp = httpx.get(url, headers=headers, timeout=timeout, follow_redirects=True)
        resp.raise_for_status()
    except Exception as e:
        raise InputFetchError(
            f"URL 抓取失败 ({e})，请用 --jd-text 重新运行"
        ) from e

    soup = BeautifulSoup(resp.text, "html.parser")
    host = urlparse(url).hostname or ""
    selector = None
    for site, sel in SITE_SELECTORS.items():
        if site in host:
            selector = sel
            break

    if selector:
        nodes = soup.select(selector)
        if not nodes:
            raise InputFetchError(
                f"在 {host} 找不到选择器 {selector} 对应的内容，请用 --jd-text 重新运行"
            )
        text = "\n".join(n.get_text("\n", strip=True) for n in nodes)
    else:
        # 站点未知 → 退化到 body 全文
        body = soup.body or soup
        text = body.get_text("\n", strip=True)

    if not text.strip():
        raise InputFetchError("URL 抓取失败：解析后正文为空，请用 --jd-text 重新运行")
    return text


def parse_file(path: str | Path) -> str:
    """按扩展名分发解析逻辑。"""
    p = Path(path)
    if not p.exists():
        raise InputFetchError(f"文件不存在: {p}")
    ext = p.suffix.lower()

    if ext in (".txt", ".md"):
        return p.read_text(encoding="utf-8", errors="replace")

    if ext == ".docx":
        try:
            from docx import Document
        except ImportError as e:
            raise UnsupportedFormatError(
                f"缺少 python-docx 依赖 ({e})，无法解析 .docx"
            ) from e
        doc = Document(str(p))
        return "\n".join(par.text for par in doc.paragraphs)

    if ext == ".pdf":
        try:
            import pdfplumber
        except ImportError as e:
            raise UnsupportedFormatError(
                f"缺少 pdfplumber 依赖 ({e})，无法解析 .pdf"
            ) from e
        print(
            "警告: PDF 抽取依赖布局，复杂排版可能丢失格式（建议使用 .txt 或 .md）",
            file=sys.stderr,
        )
        chunks: list[str] = []
        with pdfplumber.open(str(p)) as pdf:
            for page in pdf.pages:
                chunks.append(page.extract_text() or "")
        return "\n".join(chunks)

    if ext == ".doc":
        raise UnsupportedFormatError(
            ".doc 格式暂不支持，请先另存为 .docx 或 .txt"
        )

    raise UnsupportedFormatError(f"不支持的扩展名: {ext}")


def parse_resume(path_or_text: str) -> str:
    """简历入口：路径则解析文件，否则当文本透传，统一截断 20000 字符。"""
    if path_or_text is None:
        return ""
    s = path_or_text.strip()
    is_pathlike = "\n" not in s and any(s.lower().endswith(ext) for ext in _KNOWN_FILE_EXTS)
    text = parse_file(s) if is_pathlike else path_or_text
    if len(text) > 20000:
        text = text[:20000]
    return text


def validate_jd(text: str) -> str:
    """长度校验：过短抛 InputTooShortError，过长抛 InputTooLargeError。"""
    n = len(text or "")
    if n < 200:
        raise InputTooShortError(
            f"JD 长度 {n} 字符 < 200 字符下限，可能是抓取失败或粘贴不完整"
        )
    if n > 50000:
        raise InputTooLargeError(
            f"JD 长度 {n} 字符 > 50000 字符上限，请精简后重试"
        )
    return text
