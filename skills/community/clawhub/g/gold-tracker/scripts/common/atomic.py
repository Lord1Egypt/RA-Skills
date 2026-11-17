"""原子写工具（P1-10：归档、日志、状态文件写操作原子化）。

通过「临时文件 + os.replace」保证崩溃/中断时不会留下半截文件，
避免索引等衍生数据损坏后无自愈。
"""

import json
import os
from pathlib import Path


def atomic_write_text(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


def atomic_write_json(path, data):
    atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False))
