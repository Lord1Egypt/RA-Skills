#!/usr/bin/env python3
"""Fail early with a readable list when report runtime dependencies are absent."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import re
import sys


DEPENDENCIES = {
    "matplotlib": ("matplotlib", "3.8", "4"),
    "PyMuPDF": ("pymupdf", "1.24", "2"),
    "pypdf": ("pypdf", "4", "7"),
    "reportlab": ("reportlab", "4", "6"),
    "pandas": ("pandas", "2.1", "4"),
    "openpyxl": ("openpyxl", "3.1", "4"),
    "jsonschema": ("jsonschema", "4.20", "5"),
}


def numeric_version(value: str) -> tuple[int, ...]:
    match = re.match(r"^(\d+(?:\.\d+)*)", value)
    if not match:
        raise ValueError("dependency_version_unparseable:" + value)
    return tuple(int(part) for part in match.group(1).split("."))


def in_range(value: str, minimum: str, maximum: str) -> bool:
    actual, low, high = numeric_version(value), numeric_version(minimum), numeric_version(maximum)
    width = max(len(actual), len(low), len(high))
    pad = lambda item: item + (0,) * (width - len(item))
    return pad(low) <= pad(actual) < pad(high)


def inspect_dependencies() -> dict:
    installed = {}
    missing = []
    incompatible = []
    for distribution, (module, minimum, maximum) in DEPENDENCIES.items():
        if importlib.util.find_spec(module) is None:
            missing.append(distribution)
            continue
        try:
            version = importlib.metadata.version(distribution)
            installed[distribution] = version
            if not in_range(version, minimum, maximum):
                incompatible.append({"dependency": distribution, "installed": version,
                                     "required": f">={minimum},<{maximum}"})
        except importlib.metadata.PackageNotFoundError:
            missing.append(distribution)
        except ValueError:
            incompatible.append({"dependency": distribution, "installed": installed.get(distribution, "unknown"),
                                 "required": f">={minimum},<{maximum}"})
    if missing:
        status = "runtime_dependencies_missing"
    elif incompatible:
        status = "runtime_dependencies_incompatible"
    else:
        status = "runtime_dependencies_ready"
    return {
        "status": status,
        "python": ".".join(map(str, sys.version_info[:3])),
        "installed": installed,
        "missing": missing,
        "incompatible": incompatible,
        "requirements_file": "requirements-runtime.txt",
    }


def main() -> int:
    result = inspect_dependencies()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "runtime_dependencies_ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
