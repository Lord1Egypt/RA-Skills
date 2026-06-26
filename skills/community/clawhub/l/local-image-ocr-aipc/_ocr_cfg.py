"""
Shared helper: resolve OCR_DIR from environment variable or local config file.
All scripts should use: from _ocr_cfg import OCR_DIR
"""
import os

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_CFG_FILE = os.path.join(_THIS_DIR, ".ocr_dir")


def _resolve():
    # 1. Environment variable (works in PowerShell, CMD, and properly-configured bash)
    env_val = os.environ.get("OCR_DIR", "").strip()
    if env_val and env_val != "<OCR_DIR>" and os.path.isdir(env_val):
        return env_val

    # 2. Local config file written by preflight_workdir.py
    if os.path.isfile(_CFG_FILE):
        with open(_CFG_FILE, "r", encoding="utf-8") as f:
            path = f.read().strip()
        if path and os.path.isdir(path):
            return path

    # 3. Fallback: not resolved
    return None


OCR_DIR = _resolve()
