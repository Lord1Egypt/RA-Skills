from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from _common import json_dump, machine_meta


class SwiftHelperError(RuntimeError):
    pass


SWIFT_HELPER_SOURCES = {
    "powerstat": ["swift/powerstat_helper.swift", "swift/power_bridge.h"],
    "fanstat": ["swift/fanstat_helper.swift"],
    "gpustat": ["swift/gpustat_helper.swift"],
    "tempstat": ["swift/tempstat_helper.swift"],
}


def ensure_binary(root: Path, helper_name: str) -> Path:
    binary = root / "bin" / helper_name
    source_paths = [root / rel for rel in SWIFT_HELPER_SOURCES[helper_name]]
    build_script = root / "build-swift-helpers.sh"

    needs_build = not binary.exists() or any(binary.stat().st_mtime < path.stat().st_mtime for path in source_paths)
    if needs_build:
        build = subprocess.run(
            ["/bin/zsh", str(build_script), helper_name],
            check=False,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if build.returncode != 0:
            raise SwiftHelperError((build.stderr or build.stdout).strip() or f"build failed for {helper_name}")
    return binary


def run_helper(root: Path, helper_name: str, args: Optional[Iterable[str]] = None, timeout: float = 30) -> Dict[str, Any]:
    binary = ensure_binary(root, helper_name)
    proc = subprocess.run(
        [str(binary), *(list(args or []))],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise SwiftHelperError((proc.stderr or proc.stdout).strip() or f"helper exited {proc.returncode}")
    try:
        return json.loads(proc.stdout)
    except Exception as e:
        raise SwiftHelperError(f"invalid helper json: {e}") from e


def emit_failure(kind: str, message: str, todo: List[str]) -> int:
    json_dump(
        {
            **machine_meta(),
            "kind": kind,
            "implemented": False,
            "supported": False,
            "notes": [message],
            "todo": todo,
        }
    )
    return 1
