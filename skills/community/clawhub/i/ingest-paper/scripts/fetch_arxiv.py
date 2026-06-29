# -*- coding: utf-8 -*-
"""
fetch_arxiv.py — 下载 arxiv 论文的 PDF 和元数据

用法：
    python3 fetch_arxiv.py --url "https://arxiv.org/abs/2401.12345"
    python3 fetch_arxiv.py --url "2401.12345"

输出单行 JSON：
    {"success": true, "arxiv_id": "...", "title": "...", "authors": [...],
     "published": "...", "primary_category": "...", "categories": [...],
     "abstract": "...", "pdf_path": "/tmp/paperkb/arxiv_2401.12345.pdf"}
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET

import requests

from kb_common import ensure_tmp

_ATOM = "{http://www.w3.org/2005/Atom}"
_ARXIV = "{http://arxiv.org/schemas/atom}"


def _out(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def _fail(error: str, message: str) -> None:
    _out({"success": False, "error": error, "message": message})
    sys.exit(0)


def extract_arxiv_id(url_or_id: str) -> str | None:
    """从各种形式中提取 arxiv ID（支持版本号）。

    支持：
      https://arxiv.org/abs/2401.12345 / abs/2401.12345v2
      https://arxiv.org/pdf/2401.12345.pdf / pdf/2401.12345v1
      纯 ID：2401.12345 / 2401.12345v3
      旧式 ID：cs/0112017
    """
    s = url_or_id.strip()
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", s)
    if m:
        return m.group(1)
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([a-z\-]+(?:\.[A-Z]{2})?/\d{7}(?:v\d+)?)", s)
    if m:
        return m.group(1)
    m = re.fullmatch(r"([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", s)
    if m:
        return m.group(1)
    m = re.fullmatch(r"([a-z\-]+(?:\.[A-Z]{2})?/\d{7}(?:v\d+)?)", s)
    if m:
        return m.group(1)
    return None


def fetch_metadata(arxiv_id: str) -> dict:
    """调用 arxiv API 获取元数据。"""
    api_url = "http://export.arxiv.org/api/query"
    resp = requests.get(api_url, params={"id_list": arxiv_id, "max_results": 1},
                        timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    entry = root.find(f"{_ATOM}entry")
    if entry is None:
        raise ValueError(f"arxiv API 未返回 {arxiv_id} 的记录")
    title_el = entry.find(f"{_ATOM}title")
    if title_el is None or not (title_el.text or "").strip():
        raise ValueError(f"arxiv 记录 {arxiv_id} 缺少标题（ID 可能不存在）")
    title = re.sub(r"\s+", " ", title_el.text).strip()
    abstract_el = entry.find(f"{_ATOM}summary")
    abstract = re.sub(r"\s+", " ", abstract_el.text).strip() if abstract_el is not None and abstract_el.text else ""
    authors = [
        a.find(f"{_ATOM}name").text.strip()
        for a in entry.findall(f"{_ATOM}author")
        if a.find(f"{_ATOM}name") is not None
    ]
    published_el = entry.find(f"{_ATOM}published")
    published = published_el.text[:10] if published_el is not None and published_el.text else ""
    categories = [c.get("term") for c in entry.findall(f"{_ATOM}category") if c.get("term")]
    primary_el = entry.find(f"{_ARXIV}primary_category")
    primary = primary_el.get("term") if primary_el is not None else (categories[0] if categories else "")
    return {
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "published": published,
        "categories": categories,
        "primary_category": primary,
    }


def download_pdf(arxiv_id: str) -> str:
    """下载 PDF 到确定性路径 /tmp/paperkb/arxiv_{id}.pdf（路径丢失可重建）。"""
    tmp = ensure_tmp()
    safe_id = arxiv_id.replace("/", "_")
    pdf_path = tmp / f"arxiv_{safe_id}.pdf"
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    with requests.get(url, stream=True, timeout=120,
                      headers={"User-Agent": "paper-kb/1.0"}) as resp:
        resp.raise_for_status()
        with open(pdf_path, "wb") as fh:
            for chunk in resp.iter_content(chunk_size=1 << 16):
                fh.write(chunk)
    if pdf_path.stat().st_size < 1024:
        raise ValueError("下载的 PDF 异常小，可能下载失败")
    return str(pdf_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="arxiv 链接或纯 ID")
    args = parser.parse_args()

    arxiv_id = extract_arxiv_id(args.url)
    if not arxiv_id:
        _fail("invalid_arxiv_url",
              f"无法从「{args.url}」中识别出 arxiv ID。请确认链接格式。")
    try:
        meta = fetch_metadata(arxiv_id)
    except Exception as exc:  # noqa: BLE001
        _fail("metadata_failed", f"获取 arxiv 元数据失败：{exc}")
    try:
        pdf_path = download_pdf(arxiv_id)
    except Exception as exc:  # noqa: BLE001
        _fail("download_failed", f"下载 PDF 失败：{exc}")

    _out({
        "success": True,
        "arxiv_id": arxiv_id,
        "pdf_path": pdf_path,
        **meta,
    })


if __name__ == "__main__":
    main()
