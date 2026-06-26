#!/usr/bin/env python3
"""
Deploy an HTML deck or report to Cloudflare Pages and print a shareable URL.

Usage:
    python scripts/deploy-cloudflare.py presentation.html
    python scripts/deploy-cloudflare.py path/to/html-folder
    python scripts/deploy-cloudflare.py presentation.html --project-name demo-site
"""

from __future__ import annotations

import argparse
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
PAGES_URL_RE = re.compile(r"https://[^\s]+\.pages\.dev[^\s]*", re.IGNORECASE)
WORKERD_PACKAGE_RE = re.compile(r'@cloudflare/workerd-[^"\s]+', re.IGNORECASE)


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


def stage_input(input_path: Path) -> tuple[Path, bool]:
    input_path = input_path.resolve()

    if input_path.is_dir():
        index_file = input_path / "index.html"
        if not index_file.exists():
            raise ValueError(f"HTML folder must contain index.html: {input_path}")
        return input_path, False

    if not input_path.is_file() or input_path.suffix.lower() != ".html":
        raise ValueError(f"Expected an HTML file or folder, got: {input_path}")

    deck_name = sanitize_project_name(input_path.stem)
    staging_dir = Path(tempfile.mkdtemp(prefix=f"kai-html-export-{deck_name}-"))
    html_text = input_path.read_text(encoding="utf-8")

    shutil.copy2(input_path, staging_dir / "index.html")

    for reference in collect_local_references(html_text):
        _copy_reference(input_path.parent, staging_dir, reference)

    assets_dir = input_path.parent / "assets"
    if assets_dir.exists() and assets_dir.is_dir():
        shutil.copytree(assets_dir, staging_dir / "assets", dirs_exist_ok=True)

    return staging_dir, True


def sanitize_project_name(raw_name: str) -> str:
    cleaned = re.sub(r"[^a-z0-9-]+", "-", raw_name.lower()).strip("-")
    return cleaned or "html-share"


def default_project_name(input_path: Path) -> str:
    source = input_path.resolve()
    if source.is_dir():
        return sanitize_project_name(source.name)
    return sanitize_project_name(source.stem)


def _find_wrangler_command() -> list[str]:
    wrangler_path = shutil.which("wrangler")
    if wrangler_path:
        return [wrangler_path]

    npx_path = shutil.which("npx")
    if npx_path:
        return [npx_path, "--yes", "wrangler"]
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


def _extract_missing_workerd_package(output: str) -> str | None:
    match = WORKERD_PACKAGE_RE.search(output)
    return match.group(0) if match else None


def _run_wrangler(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    result = _run(command, cwd=cwd)
    if result.returncode == 0:
        return result

    output = "\n".join(part for part in [result.stdout, result.stderr] if part)
    missing_package = _extract_missing_workerd_package(output)
    if not missing_package or len(command) < 3 or command[2] != "wrangler":
        return result

    retry_command = [command[0], command[1], "--package", "wrangler", "--package", missing_package, "wrangler", *command[3:]]
    return _run(retry_command, cwd=cwd)


def _extract_pages_url(output: str) -> str | None:
    matches = PAGES_URL_RE.findall(output)
    return matches[-1] if matches else None


def _ensure_login(wrangler: list[str]) -> None:
    version_check = _run_wrangler(wrangler + ["--version"])
    version_output = "\n".join(part for part in [version_check.stdout, version_check.stderr] if part).strip()
    if version_check.returncode != 0:
        raise RuntimeError(version_output or "Failed to run Wrangler CLI.")

    whoami = _run_wrangler(wrangler + ["whoami"])
    whoami_output = "\n".join(part for part in [whoami.stdout, whoami.stderr] if part).strip()
    if whoami.returncode != 0 or "not authenticated" in whoami_output.lower():
        raise RuntimeError("Cloudflare login is required. Run `wrangler login` and retry.")


def _ensure_project(wrangler: list[str], project_name: str, branch: str) -> None:
    result = _run_wrangler(wrangler + ["pages", "project", "create", project_name, "--production-branch", branch])
    output = "\n".join(part for part in [result.stdout, result.stderr] if part).strip()
    if result.returncode == 0:
        return
    if "already exists" in output.lower():
        return
    raise RuntimeError(output or f"Failed to create Cloudflare Pages project {project_name}.")


def deploy_with_cloudflare(deploy_dir: Path, *, project_name: str, branch: str = "main") -> str:
    wrangler = _find_wrangler_command()
    _ensure_login(wrangler)
    _ensure_project(wrangler, project_name, branch)

    deploy = _run_wrangler(
        wrangler + ["pages", "deploy", str(deploy_dir), "--project-name", project_name, "--branch", branch]
    )
    output = "\n".join(part for part in [deploy.stdout, deploy.stderr] if part).strip()
    if deploy.returncode != 0:
        raise RuntimeError(output or "Cloudflare deployment failed.")

    url = _extract_pages_url(output)
    if not url:
        raise RuntimeError("Cloudflare deployment finished without a detectable Pages URL.")
    return url


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_path", help="HTML file or folder containing index.html")
    parser.add_argument("--project-name", help="Cloudflare Pages project name")
    parser.add_argument("--branch", default="main", help="Cloudflare Pages branch name (default: main)")
    args = parser.parse_args(argv)

    input_path = Path(args.input_path)
    project_name = sanitize_project_name(args.project_name) if args.project_name else default_project_name(input_path)

    try:
        staging_dir, should_cleanup = stage_input(input_path)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        url = deploy_with_cloudflare(staging_dir, project_name=project_name, branch=args.branch)
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
