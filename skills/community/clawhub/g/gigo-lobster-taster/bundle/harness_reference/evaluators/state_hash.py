"""比对 workdir 下指定文件的内容/hash/pattern。"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path


def file_score(path: Path, cfg: dict) -> float:
    if not path.exists():
        return 0.0
    text = path.read_text(errors="ignore")
    score = 100.0
    for pat in cfg.get("forbidden_patterns", []):
        if re.search(pat, text):
            return 0.0
    required_patterns = cfg.get("required_patterns", [])
    missing_required = 0
    for pat in required_patterns:
        if not re.search(pat, text):
            missing_required += 1
    if required_patterns:
        score *= max(0.0, 1.0 - 0.28 * missing_required)
    expected = cfg.get("expected_hash", {}).get(str(path.name))
    if expected:
        actual = "sha256:" + hashlib.sha256(text.encode()).hexdigest()
        if actual != expected:
            score *= 0.5
    return score


def score(workdir: Path, ev_cfg: dict) -> tuple[float, dict]:
    files = ev_cfg.get("files", [])
    if not files:
        return 100.0, {}
    file_scores = {f: file_score(workdir / f, ev_cfg) for f in files}
    avg = sum(file_scores.values()) / len(file_scores)
    return avg, {"file_scores": file_scores}
