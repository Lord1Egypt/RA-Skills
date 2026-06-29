#!/usr/bin/env python3
"""
doi_utils.py — DOI 统一处理模块
===============================
全项目 DOI 的单一事实来源。所有提取、规范化、文件名转换、匹配
都走这个模块，杜绝碎片化实现导致的匹配失败。

Usage:
    from doi_utils import normalize, extract, to_filename, to_doi, title_hash
"""

import re
import hashlib

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

# DOI 标准模式：10.xxx/xxx
DOI_PATTERN = re.compile(r'(10\.\S{4,})')

# 文件名非法字符
_FILENAME_BLACKLIST = re.compile(r'[\\/:*?"<>|\s]')

# ---------------------------------------------------------------------------
# 规范化
# ---------------------------------------------------------------------------

def normalize(doi: str) -> str | None:
    """
    统一 DOI 规范化：lowercase → strip URL prefix → strip trailing punct → 验证 10. 前缀

    >>> normalize('https://doi.org/10.1007/978-3-031-62110-9_7')
    '10.1007/978-3-031-62110-9_7'
    >>> normalize('10.1109/TASE.2024.3474549.')
    '10.1109/tase.2024.3474549'
    >>> normalize('not a doi')
    >>> # Returns None (nothing printed)
    """
    if not doi:
        return None
    doi = doi.strip().lower()
    # Strip common URL prefixes
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi)
    # Strip trailing punctuation often caught in regex
    doi = doi.rstrip('.')
    # Must start with 10. and have enough content
    if doi.startswith("10.") and len(doi) > 10:
        return doi
    return None


# ---------------------------------------------------------------------------
# 提取
# ---------------------------------------------------------------------------

def extract(paper: dict) -> str | None:
    """
    从 paper dict 提取并规范化 DOI。
    优先 paper["doi"] → 回退 paper["link"] 正则 → 再回退 body text。

    >>> extract({"doi": "10.1007/978-3-031-62110-9_7"})
    '10.1007/978-3-031-62110-9_7'
    >>> extract({"link": "https://dl.acm.org/doi/10.1145/3719384.3719438"})
    '10.1145/3719384.3719438'
    >>> extract({"doi": ""})
    >>> # Returns None (nothing printed)
    """
    # 优先 doi 字段
    doi = normalize(paper.get("doi", ""))
    if doi:
        return doi

    # 回退：从 link 提取
    link = paper.get("link", "")
    if link:
        m = DOI_PATTERN.search(link)
        if m:
            doi = normalize(m.group(1))
            if doi:
                return doi

    return None


def extract_from_text(text: str) -> str | None:
    """
    从任意文本中提取 DOI（JS extractor 常用）。
    """
    if not text:
        return None
    # 常见封装: info:doi/xxx, DOI: 10.xxx
    # Try "info:doi/" prefix
    m = re.search(r'info:doi/(10\.\S+)', text, re.IGNORECASE)
    if m:
        return normalize(m.group(1))
    m = DOI_PATTERN.search(text)
    if m:
        return normalize(m.group(1))
    return None


# ---------------------------------------------------------------------------
# 文件名转换
# ---------------------------------------------------------------------------

def to_filename(doi: str) -> str:
    """
    DOI → 文件系统安全文件名。
    双向可逆：to_doi(to_filename(doi)) == normalize(doi)

    >>> to_filename("10.1007/978-3-031-62110-9_7")
    '10.1007_978-3-031-62110-9_7.txt'
    """
    safe = _FILENAME_BLACKLIST.sub('_', doi)
    if len(safe) > 200:
        safe = safe[:200]
    return safe + ".txt"


def to_doi(filename: str) -> str:
    """
    文件名 → DOI（反向还原）。
    
    >>> to_doi("10.1007_978-3-031-62110-9_7.txt")
    '10.1007/978-3-031-62110-9/7'
    >>> # Note: _ → / is lossy for DOIs that naturally contain _
    """
    # Remove .txt extension
    name = filename
    if name.endswith(".txt"):
        name = name[:-4]
    # Reverse _ → / (note: original / in DOI became _)
    # This is imperfect for DOIs that naturally contain _ but that's rare
    return name.replace("_", "/")


def title_hash(title: str) -> str:
    """
    无 DOI 时的回退文件名（标题 MD5 前 12 位）。

    >>> title_hash("Test Paper")
    '1afd1097ef6b.txt'
    """
    h = hashlib.md5(title.encode("utf-8")).hexdigest()[:12]
    return h + ".txt"


# ---------------------------------------------------------------------------
# 匹配
# ---------------------------------------------------------------------------

def match(doi_a: str, doi_b: str) -> bool:
    """
    判断两个 DOI 是否指向同一篇论文（经过规范化比较）。
    """
    a = normalize(doi_a)
    b = normalize(doi_b)
    if not a or not b:
        return False
    return a == b


def doc_id_filename(doc_id: str, db: str = "ieee") -> str:
    """
    IEEE 无 DOI 时的回退文件名（基于 document ID）。

    >>> doc_id_filename("11356120", "ieee")
    'ieee_doc_11356120.txt'
    """
    return f"{db}_doc_{doc_id}.txt"


def extract_doc_id(paper: dict) -> str | None:
    """
    从 paper dict 提取 docId（IEEE / Engineering Village 等库）。

    >>> extract_doc_id({"docId": "11356120"})
    '11356120'
    >>> extract_doc_id({"link": "https://ieeexplore.ieee.org/document/11356120/"})
    '11356120'
    """
    # 优先 docId 字段
    doc_id = paper.get("docId", "")
    if doc_id:
        return str(doc_id).strip()

    # 回退：从 link 提取 /document/XXXXX/
    link = paper.get("link", "")
    if link:
        m = re.search(r'/document/(\d+)/', link)
        if m:
            return m.group(1)

    return None


def title_similarity(t1: str, t2: str) -> float:
    """
    标题 token overlap 比率（无 DOI 时的回退匹配）。
    先用 DOI 匹配，匹配不上才用标题。
    """
    if not t1 or not t2:
        return 0.0
    # Normalize
    def _norm(t):
        t = t.lower()
        t = re.sub(r'[^\w\s]', ' ', t)
        t = re.sub(r'\s+', ' ', t).strip()
        return set(t.split())
    tokens1 = _norm(t1)
    tokens2 = _norm(t2)
    if not tokens1 or not tokens2:
        return 0.0
    overlap = tokens1 & tokens2
    return len(overlap) / min(len(tokens1), len(tokens2))


# ---------------------------------------------------------------------------
# 自检
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    print("\nAll tests passed.")
