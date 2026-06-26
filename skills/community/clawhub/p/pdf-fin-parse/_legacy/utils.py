"""通用工具：配置加载、页范围解析、logger 等。"""
from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any


def load_config(path: str | None) -> dict[str, Any]:
    """加载 YAML 配置；为空时返回默认配置。环境变量 ${VAR} 自动展开。"""
    import yaml

    if path is None:
        default = Path(__file__).resolve().parents[3] / "config" / "skill.config.example.yaml"
        path = str(default)
    text = Path(path).read_text(encoding="utf-8")
    text = _expand_env(text)
    return yaml.safe_load(text) or {}


def _expand_env(text: str) -> str:
    return re.sub(r"\$\{(\w+)\}", lambda m: os.environ.get(m.group(1), ""), text)


def parse_page_range(spec: str | None, total_pages: int) -> list[int]:
    """'1-10,15,20-25' → [1..10, 15, 20..25]，1-based。spec=None 返回全部。"""
    if not spec:
        return list(range(1, total_pages + 1))
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return sorted(p for p in set(out) if 1 <= p <= total_pages)


def get_logger(name: str, log_file: Path | None = None, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger
