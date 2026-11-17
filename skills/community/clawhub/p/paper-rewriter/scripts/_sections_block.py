import re


def _num_prefix():
    return r"^(?:\d+(?:[.．、]\d+)*[.．、]?\s*)?"


def _normalize_heading(stripped):
    """标题行归一（v2.2.0）：剥掉 markdown 前缀（`## 摘要`）与整行加粗包裹
    （`**方法**`），让 .md 稿件的章节标题进入与纯文本同一套判定。

    返回 (归一文本, 是否剥过标记)。只处理「整行即标题」的形态：
    行中混有正文（如 `**摘要** 本文研究了…`）不剥，避免把内容句当标题。"""
    s = stripped
    # v2.3.0：# 后无空格但紧邻 CJK 的形态（#摘要）也收——CommonMark 不认它，
    # 但中文写作场景高频出现，且失败方向（漏检）只会让章节感知失效；
    # 英文 `#1 cause` 类不受影响（lookahead 限汉字）
    m = re.match(r"^#{1,6}(?:\s+|(?=[\u4e00-\u9fff]))", s)
    if m:
        s = s[m.end():]
    if len(s) >= 4 and s.startswith("**") and s.endswith("**"):
        inner = s[2:-2].strip()
        if inner and "**" not in inner:
            s = inner
    return s, (s != stripped)


def _is_heading_line(stripped):
    s, _ = _normalize_heading(stripped)
    if not s or len(s) > 40:
        return False
    if re.search(r"[。．！？!?]", s):
        return False
    cm = re.match(r"^[^：:]{1,12}[：:](.+)", s)
    if cm and len(cm.group(1).strip()) > 0:
        return False
    return True


_SECTION_PATTERNS = [
    ("abstract", re.compile(_num_prefix() + r"(摘\s*要|abstract)[:：]?", re.I)),
    ("introduction", re.compile(_num_prefix() + r"(引\s*言|绪\s*论|introduction)[:：]?", re.I)),
    ("methods", re.compile(_num_prefix() + r"(方\s*法|材料与方法|方法与材料|对象与方法|methods?|materials? and methods|patients? and methods)[:：]?", re.I)),
    ("results", re.compile(_num_prefix() + r"(结\s*果|results?)[:：]?", re.I)),
    ("discussion", re.compile(_num_prefix() + r"(讨\s*论|discussion)[:：]?", re.I)),
    ("conclusion", re.compile(_num_prefix() + r"(结\s*论(?!是)|conclusions?|结论与展望)[:：]?", re.I)),
    ("references", re.compile(_num_prefix() + r"(参\s*考\s*文\s*献|references?)[:：]?", re.I)),
]
