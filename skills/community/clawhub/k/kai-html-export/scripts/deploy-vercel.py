#!/usr/bin/env python3
"""
Deploy an HTML deck or report to Vercel and print a shareable URL.

Usage:
    python scripts/deploy-vercel.py presentation.html
    python scripts/deploy-vercel.py path/to/html-folder

Behavior:
1. Accept a single HTML file or a directory with index.html
2. Stage a deployable folder when given a single HTML file
3. Reuse the provided folder directly when given a directory
4. Call Vercel through `vercel` or `npx --yes vercel`
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote


LOCAL_REF_RE = re.compile(
    r"""(?:src|href)\s*=\s*["']([^"']+)["']|url\(\s*['"]?([^'")]+)['"]?\s*\)""",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https://[^\s]+")


def collect_local_references(html_text: str) -> set[str]:
    refs: set[str] = set()
    for match in LOCAL_REF_RE.finditer(html_text):
        raw = match.group(1) or match.group(2) or ""
        candidate = raw.strip()
        if not candidate:
            continue
        candidate = candidate.split("#", 1)[0].split("?", 1)[0].strip()
        if not candidate:
            continue
        lower = candidate.lower()
        if lower.startswith(("http://", "https://", "data:", "mailto:", "tel:")):
            continue
        if candidate.startswith(("/", "\\")):
            continue
        refs.add(candidate)
    return refs


def _safe_source_for_reference(base_dir: Path, reference: str) -> Path | None:
    normalized = unquote(reference).replace("/", "\\")
    source = (base_dir / normalized).resolve()
    try:
        source.relative_to(base_dir.resolve())
    except ValueError:
        return None
    if not source.exists():
        return None
    return source


def _copy_reference(base_dir: Path, staging_dir: Path, reference: str) -> None:
    source = _safe_source_for_reference(base_dir, reference)
    if source is None or source.is_dir():
        return
    target = staging_dir / Path(reference)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def cleanup_staging_dir(staging_dir: Path) -> None:
    shutil.rmtree(staging_dir, ignore_errors=True)


def get_linked_project_id(deploy_dir: Path) -> str | None:
    project_json = deploy_dir / ".vercel" / "project.json"
    if not project_json.exists():
        return None
    try:
        payload = json.loads(project_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    project_id = payload.get("projectId")
    return project_id if isinstance(project_id, str) and project_id else None


def stage_input(input_path: Path) -> tuple[Path, bool]:
    input_path = input_path.resolve()

    if input_path.is_dir():
        index_file = input_path / "index.html"
        if not index_file.exists():
            raise ValueError(f"HTML folder must contain index.html: {input_path}")
        return input_path, False

    if not input_path.is_file() or input_path.suffix.lower() != ".html":
        raise ValueError(f"Expected an HTML file or folder, got: {input_path}")

    deck_name = re.sub(r"[^a-z0-9-]+", "-", input_path.stem.lower()).strip("-") or "html"
    staging_dir = Path(tempfile.mkdtemp(prefix=f"kai-html-export-{deck_name}-"))
    html_text = input_path.read_text(encoding="utf-8")

    shutil.copy2(input_path, staging_dir / "index.html")

    for reference in collect_local_references(html_text):
        _copy_reference(input_path.parent, staging_dir, reference)

    assets_dir = input_path.parent / "assets"
    if assets_dir.exists() and assets_dir.is_dir():
        shutil.copytree(assets_dir, staging_dir / "assets", dirs_exist_ok=True)

    return staging_dir, True


def _find_vercel_command() -> list[str]:
    vercel_path = shutil.which("vercel")
    if vercel_path:
        return [vercel_path]

    npx_path = shutil.which("npx")
    if npx_path:
        return [npx_path, "--yes", "vercel"]
    raise RuntimeError("Node.js is required. Install Node.js so `npx` is available.")


def _run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _extract_deployment_url(output: str) -> str | None:
    stripped = output.lstrip()
    if stripped.startswith("{"):
        try:
            payload, _ = json.JSONDecoder().raw_decode(stripped)
            url = payload.get("deployment", {}).get("url")
            if isinstance(url, str) and url:
                return url
        except json.JSONDecodeError:
            pass

    matches = URL_RE.findall(output)
    return matches[-1] if matches else None


def deploy_with_vercel(deploy_dir: Path) -> str:
    vercel = _find_vercel_command()

    version_check = _run(vercel + ["--version"])
    if version_check.returncode != 0:
        raise RuntimeError(version_check.stderr.strip() or version_check.stdout.strip() or "Failed to run Vercel CLI.")

    whoami = _run(vercel + ["whoami"])
    if whoami.returncode != 0:
        raise RuntimeError("Vercel login is required. Run `npx vercel login` and retry.")

    deploy = _run(vercel + ["deploy", str(deploy_dir), "--yes", "--prod", "--format", "json"])
    output = "\n".join(part for part in [deploy.stdout, deploy.stderr] if part).strip()
    if deploy.returncode != 0:
        raise RuntimeError(output or "Vercel deployment failed.")

    url = _extract_deployment_url(output)
    if not url:
        raise RuntimeError("Vercel deployment finished without a detectable URL.")
    return url


def make_project_public(deploy_dir: Path) -> None:
    project_id = get_linked_project_id(deploy_dir)
    if not project_id:
        return

    vercel = _find_vercel_command()
    payload = json.dumps({"ssoProtection": None})
    fd, payload_path = tempfile.mkstemp(prefix="vercel-project-", suffix=".json")
    os.close(fd)
    payload_file = Path(payload_path)
    try:
        payload_file.write_text(payload, encoding="utf-8")
        result = _run(
            vercel + [
                "api",
                f"/v9/projects/{project_id}",
                "-X",
                "PATCH",
                "-H",
                "Content-Type: application/json",
                "--input",
                str(payload_file),
            ]
        )
    finally:
        payload_file.unlink(missing_ok=True)

    output = "\n".join(part for part in [result.stdout, result.stderr] if part).strip()
    if result.returncode != 0:
        raise RuntimeError(output or f"Failed to disable deployment protection for project {project_id}.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", help="HTML file or folder containing index.html")
    args = parser.parse_args(argv)

    try:
        staging_dir, should_cleanup = stage_input(Path(args.input_path))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        url = deploy_with_vercel(staging_dir)
        make_project_public(staging_dir)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        if should_cleanup:
            cleanup_staging_dir(staging_dir)

    print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
