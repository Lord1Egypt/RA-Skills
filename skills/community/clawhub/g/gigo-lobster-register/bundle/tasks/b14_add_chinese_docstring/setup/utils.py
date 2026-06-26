import re
from datetime import datetime


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "-", text)


def parse_iso_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def chunk_list(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]


def safe_divide(a, b, default=0):
    if b == 0:
        return default
    return a / b


def merge_dicts(*dicts):
    out = {}
    for d in dicts:
        out.update(d)
    return out
