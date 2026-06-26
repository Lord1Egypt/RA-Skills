from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


Runner = Callable[..., subprocess.CompletedProcess[str]]


class PublicOsmMapClient:
    def __init__(
        self,
        *,
        skill_root: str | Path | None = None,
        fixture_dir: str | Path | None = None,
        runner: Runner | None = None,
    ) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        self.skill_root = Path(skill_root) if skill_root else repo_root / "public-osm-map-context-skill"
        self.fixture_dir = Path(fixture_dir) if fixture_dir else None
        self.runner = runner or subprocess.run

    def doctor(self) -> dict[str, Any]:
        return self._run_json(["doctor"])

    def analyze_batch(self, *, listings: list[dict[str, Any]], destination: str = "", city: str = "") -> dict[str, Any]:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            json.dump({"listings": listings}, handle, ensure_ascii=False, indent=2)
            input_path = Path(handle.name)
        args = [
            "analyze-batch",
            "--input",
            str(input_path),
            "--city",
            city,
        ]
        if destination:
            args.extend(["--destination", destination])
        if self.fixture_dir:
            args.extend(["--fixture-dir", str(self.fixture_dir)])
        try:
            return self._run_json(args)
        finally:
            input_path.unlink(missing_ok=True)

    def _run_json(self, args: list[str], *, timeout: int = 120) -> dict[str, Any]:
        command = [sys.executable, "scripts/cli.py", *args]
        completed = self.runner(
            command,
            cwd=str(self.skill_root),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"public-osm-map-context-skill failed ({completed.returncode}): {' '.join(command)}\n"
                f"stdout: {completed.stdout}\nstderr: {completed.stderr}"
            )
        return json.loads(completed.stdout)
