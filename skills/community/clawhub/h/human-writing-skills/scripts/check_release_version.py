"""Reject plugin tags and mislabeled core releases before marketplace publication."""

import re
import sys
from pathlib import Path


def check_version(value: str, root: Path) -> str:
    version = value.removeprefix("v")
    metadata = (root / "pyproject.toml").read_text(encoding="utf-8")
    expected = re.search(r'^version\s*=\s*"([^"]+)"', metadata, re.MULTILINE)
    if not expected or not re.fullmatch(r"\d+\.\d+\.\d+", version) or version != expected.group(1):
        raise ValueError("Core release version must match pyproject.toml; DSH tags cannot publish core packages.")
    return version


if __name__ == "__main__":
    print(check_version(sys.argv[1], Path(__file__).resolve().parents[1]))
