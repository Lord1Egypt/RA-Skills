import re

# 论文章节标题模式（中英双语；行首匹配，标题行 ≤40 字符；
# 支持编号式标题「1 引言 / 2. Methods」；标题行不得含句末/分句标点）
def _is_heading_line(stripped):
    if not stripped or len(stripped) > 40:
        return False
    if re.search(r"[。．！？!?]", stripped):
        return False
    cm = re.match(r"^[^：:]{1,12}[：:](.+)", stripped)
    if cm and len(cm.group(1).strip()) > 0:
        return False
    return True


def _num_prefix():
    return r"^(?:\d+(?:[.．、]\d+)*[.．、]?\s*)?"


_SECTION_PATTERNS = [
    ("abstract", re.compile(_num_prefix() + r"(摘\s*要|abstract)\b[:：]?", re.I)),
    ("introduction", re.compile(_num_prefix() + r"(引\s*言|绪\s*论|introduction)\b[:：]?", re.I)),
    ("methods", re.compile(_num_prefix() + r"(方\s*法|材料与方法|方法与材料|对象与方法|materials? and methods|patients? and methods|methods?)\b[:：]?", re.I)),
    ("results", re.compile(_num_prefix() + r"(结\s*果|results?)\b[:：]?", re.I)),
    ("discussion", re.compile(_num_prefix() + r"(讨\s*论|discussion)\b[:：]?", re.I)),
    ("conclusion", re.compile(_num_prefix() + r"(结\s*论|conclusions?)\b[:：]?", re.I)),
    ("references", re.compile(_num_prefix() + r"(参\s*考\s*文\s*献|references?)\b[:：]?", re.I)),
]
