from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse, urlunparse

from .analysis import safe_text
from .models import PreflightCheck, PreflightReport, PublishPropertyRequest
from .publish import gt_publish_payload


Runner = Callable[..., subprocess.CompletedProcess[str]]
Which = Callable[[str], str | None]

GT_BRIDGE_MODE = "bridge"
GT_API_MODE = "api"
_LISTING_ID_RE = re.compile(r"/(\d+)(?:[/?#]|$)")


class GTCoreSkillError(RuntimeError):
    pass


def _candidate_roots(custom_root: str | Path | None, env: dict[str, str]) -> list[Path]:
    cwd = Path.cwd()
    codex_home = Path(env.get("CODEX_HOME") or (Path.home() / ".codex")).expanduser()
    roots: list[Path] = []
    for raw_value in (
        custom_root,
        env.get("GT_CORE_SKILL_ROOT"),
        env.get("PROPERTY_GT_SKILL_ROOT"),
        cwd / ".agents" / "skills" / "gt-core-skill",
        cwd / ".agents" / "skills" / "gumtree-skills",
        cwd / "skills" / "gt-core-skill",
        cwd / "skills" / "gumtree-skills",
        codex_home / "skills" / "gt-core-skill",
        codex_home / "skills" / "gumtree-skills",
        Path.home() / ".codex" / "skills" / "gt-core-skill",
        Path.home() / ".codex" / "skills" / "gumtree-skills",
        "/Users/a58/Desktop/gt-core-skill/gt-core-skill-cli/gt-core-skill/gumtree-skills",
        str(Path.home() / "Desktop" / "gt-core-skill" / "gt-core-skill-cli" / "gt-core-skill" / "gumtree-skills"),
        "/Users/a58/Desktop/gt-core-skill/gumtree-skills",
        str(Path.home() / "Desktop" / "gt-core-skill" / "gumtree-skills"),
        "/Users/a58/Desktop/gt-core-skill",
        str(Path.home() / "Desktop" / "gt-core-skill"),
    ):
        if not raw_value:
            continue
        candidate = Path(raw_value).expanduser()
        for expanded in (
            candidate,
            candidate / "gumtree-skills",
            candidate / "gt-core-skill-cli" / "gt-core-skill" / "gumtree-skills",
        ):
            if expanded not in roots:
                roots.append(expanded)
    return roots


def resolve_gt_skill_root(
    custom_root: str | Path | None = None,
    env: dict[str, str] | None = None,
    runner: Runner | None = None,
) -> tuple[Path, str]:
    env = env or os.environ
    runner = runner or subprocess.run
    bridge_match: tuple[Path, str] | None = None
    api_match: tuple[Path, str] | None = None
    for candidate in _candidate_roots(custom_root, env):
        mode = probe_gt_skill_mode(candidate, runner=runner)
        if mode == GT_BRIDGE_MODE and bridge_match is None:
            bridge_match = (candidate, mode)
        elif mode == GT_API_MODE and api_match is None:
            api_match = (candidate, mode)
    if bridge_match:
        return bridge_match
    if api_match:
        return api_match
    raise GTCoreSkillError("Unable to locate gt-core-skill. Set GT_CORE_SKILL_ROOT or PROPERTY_GT_SKILL_ROOT.")


def resolve_gt_publish_skill_root(
    custom_root: str | Path | None = None,
    env: dict[str, str] | None = None,
    runner: Runner | None = None,
) -> Path:
    env = env or os.environ
    runner = runner or subprocess.run
    for candidate in _candidate_roots(custom_root, env):
        if probe_gt_publish_capability(candidate, runner=runner):
            return candidate
    raise GTCoreSkillError("Unable to locate gt-core-skill with publish-listing support.")


def probe_gt_skill_mode(root: str | Path, *, runner: Runner | None = None) -> str | None:
    runner = runner or subprocess.run
    root_path = Path(root).expanduser()
    cli_path = root_path / "scripts" / "cli.py"
    if not cli_path.exists():
        return None
    completed = runner(
        [sys.executable, "-B", "scripts/cli.py", "--help"],
        cwd=str(root_path),
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if completed.returncode != 0:
        return None
    help_text = f"{completed.stdout}\n{completed.stderr}".lower()
    if "home-recommend" in help_text and "detail" in help_text and "search" in help_text:
        return GT_BRIDGE_MODE
    if "search-listings" in help_text:
        return GT_API_MODE
    return None


def probe_gt_publish_capability(root: str | Path, *, runner: Runner | None = None) -> bool:
    runner = runner or subprocess.run
    root_path = Path(root).expanduser()
    cli_path = root_path / "scripts" / "cli.py"
    if not cli_path.exists():
        return False
    completed = runner(
        [sys.executable, "-B", "scripts/cli.py", "--help"],
        cwd=str(root_path),
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if completed.returncode != 0:
        return False
    help_text = f"{completed.stdout}\n{completed.stderr}".lower()
    return "publish-listing" in help_text


def canonicalize_gumtree_url(url: str | None) -> str | None:
    raw = safe_text(url)
    if not raw:
        return None
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = parsed.netloc.lower()
    if host.endswith("gumtree.com"):
        host = "www.gumtree.com"
    path = parsed.path.rstrip("/") or parsed.path
    canonical = parsed._replace(scheme="https", netloc=host, path=path, params="", query="", fragment="")
    return urlunparse(canonical)


def extract_gumtree_listing_id(url: str | None) -> str | None:
    canonical = canonicalize_gumtree_url(url)
    if not canonical:
        return None
    match = _LISTING_ID_RE.search(canonical)
    return match.group(1) if match else None


class GTCoreSkillClient:
    source_name = "gt-core-skill"

    def __init__(
        self,
        *,
        skill_root: str | Path | None = None,
        runner: Runner | None = None,
        which: Which | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self.env = env or os.environ
        self.runner = runner or subprocess.run
        self.which = which or shutil.which
        self.skill_root, self.runtime_mode = resolve_gt_skill_root(skill_root, self.env, runner=self.runner)
        self.detail_supported = self.runtime_mode == GT_BRIDGE_MODE
        self._selected_runner: str | None = None
        self._selected_prefix: list[str] | None = None
        self._warnings: list[str] = []

    def doctor(self, *, run_browser_smoke: bool = True) -> PreflightReport:
        checks: list[PreflightCheck] = []
        root = self.skill_root
        cli_path = root / "scripts" / "cli.py"
        checks.append(PreflightCheck(name="skill_root", ok=root.exists(), message=f"gt-core-skill root: {root}"))
        checks.append(
            PreflightCheck(
                name="cli_entry",
                ok=cli_path.exists(),
                message=f"CLI entry {'found' if cli_path.exists() else 'missing'} at {cli_path}",
            )
        )
        mode = probe_gt_skill_mode(root, runner=self.runner)
        checks.append(
            PreflightCheck(
                name="capability_probe",
                ok=mode is not None,
                message=f"Detected GT mode: {mode or 'unknown'}",
                detail={"runtime_mode": mode},
            )
        )
        prefix, runner_name, runtime_check, warnings = self._select_runtime()
        checks.append(runtime_check)
        ok = all(check.ok for check in checks if check.name in {"skill_root", "cli_entry", "capability_probe", "runtime_smoke"})
        logged_in: bool | None = None
        if ok and run_browser_smoke and self.runtime_mode == GT_BRIDGE_MODE:
            browser_check, logged_in = self._browser_smoke(prefix, runner_name)
            checks.append(browser_check)
            ok = ok and browser_check.ok
            if logged_in is False:
                warnings.append("Gumtree 当前未登录，但公开搜索与详情抓取仍可用。")
        else:
            checks.append(
                PreflightCheck(
                    name="browser_smoke",
                    ok=True,
                    message="Bridge login smoke skipped." if self.runtime_mode == GT_BRIDGE_MODE else "API mode login smoke skipped.",
                )
            )
        if runtime_check.ok:
            self._selected_runner = runner_name
            self._selected_prefix = prefix
        else:
            self._selected_runner = None
            self._selected_prefix = None
        return PreflightReport(
            ok=ok,
            skill_root=str(root),
            selected_runner=runner_name if runtime_check.ok else None,
            checks=checks,
            warnings=warnings,
            source_name=self.source_name,
            runtime_mode=self.runtime_mode,
            detail_supported=self.detail_supported,
            logged_in=logged_in,
        )

    def search_property(
        self,
        *,
        keyword: str,
        country: str,
        city: str,
        lang: str,
        max_results: int,
        query_text: str = "",
        search_location: str = "",
    ) -> list[dict[str, Any]]:
        if self.runtime_mode == GT_BRIDGE_MODE:
            payload = self._run_json(
                [
                    "search",
                    "--keyword",
                    keyword,
                    "--limit",
                    str(max_results),
                    "--search-location",
                    safe_text(search_location) or safe_text(city) or "uk",
                ],
                timeout=180,
            )
            return [self._normalize_bridge_listing(item) for item in payload.get("items", []) if isinstance(item, dict)]
        payload = self._run_json(
            [
                "search-listings",
                "--keyword",
                keyword,
                "--limit",
                str(max_results),
            ]
        )
        return [self._normalize_api_listing(item) for item in payload.get("items", []) if isinstance(item, dict)]

    def browse_property(
        self,
        *,
        country: str,
        city: str,
        lang: str,
        max_results: int,
        query_text: str = "",
        search_location: str = "",
    ) -> list[dict[str, Any]]:
        keyword = safe_text(query_text)
        if not keyword:
            keyword = "flat"
            self._warnings.append("GT 无分类 browse 接口，已使用默认关键词 flat。")
        return self.search_property(
            keyword=keyword,
            country=country,
            city=city,
            lang=lang,
            max_results=max_results,
            query_text=query_text,
            search_location=search_location,
        )

    def get_listing_detail(self, *, url: str) -> dict[str, Any]:
        canonical_url = canonicalize_gumtree_url(url)
        if not self.detail_supported:
            return {
                "url": canonical_url,
                "detail_fetched": False,
                "detail_degraded": True,
                "detail_degraded_reason": "GT 当前运行模式不支持详情补全",
            }
        payload = self._run_json(["detail", "--url", canonical_url or url], timeout=180)
        return self._normalize_bridge_detail(payload)

    def drain_warnings(self) -> list[str]:
        warnings = list(dict.fromkeys(self._warnings))
        self._warnings.clear()
        return warnings

    def _select_runtime(self) -> tuple[list[str], str, PreflightCheck, list[str]]:
        warnings: list[str] = []
        if self.runtime_mode == GT_BRIDGE_MODE:
            uv_path = self.which("uv")
            if uv_path:
                prefix = ["uv", "run", "python", "scripts/cli.py"]
                check = self._smoke_runtime(prefix, "uv")
                if check.ok:
                    return prefix, "uv", check, warnings
                warnings.append(f"GT bridge uv runtime smoke failed: {check.detail.get('stderr', '')}")
            venv_python = self.skill_root / ".venv" / "bin" / "python"
            if venv_python.exists():
                prefix = [str(venv_python), "scripts/cli.py"]
                check = self._smoke_runtime(prefix, "venv")
                if check.ok:
                    return prefix, "venv", check, warnings
            return [], "unavailable", PreflightCheck(
                name="runtime_smoke",
                ok=False,
                message="Neither uv nor project .venv passed GT bridge help smoke.",
            ), warnings
        python3 = self.which("python3")
        if python3:
            prefix = ["python3", "scripts/cli.py"]
            check = self._smoke_runtime(prefix, "python3")
            if check.ok:
                return prefix, "python3", check, warnings
        python3 = python3 or "python3"
        prefix = [python3, "-m", "gumtree_skills"]
        check = self._smoke_runtime(prefix, "python_module")
        if check.ok:
            return prefix, "python_module", check, warnings
        return [], "unavailable", PreflightCheck(
            name="runtime_smoke",
            ok=False,
            message="Neither python3 scripts/cli.py nor python -m gumtree_skills passed GT API help smoke.",
        ), warnings

    def _smoke_runtime(self, prefix: list[str], runtime_name: str) -> PreflightCheck:
        completed = self._run(prefix + ["--help"], timeout=45, check=False)
        ok = completed.returncode == 0
        return PreflightCheck(
            name="runtime_smoke",
            ok=ok,
            message=f"{runtime_name} runtime {'passed' if ok else 'failed'} GT help smoke.",
            detail={"stdout": completed.stdout.strip()[:300], "stderr": completed.stderr.strip()[:300]},
        )

    def _browser_smoke(self, prefix: list[str], runtime_name: str) -> tuple[PreflightCheck, bool | None]:
        completed = self._run(prefix + ["check-login"], timeout=90, check=False)
        if completed.returncode != 0:
            return (
                PreflightCheck(
                    name="browser_smoke",
                    ok=False,
                    message=f"{runtime_name} runtime failed GT check-login smoke.",
                    detail={"stdout": completed.stdout.strip()[:300], "stderr": completed.stderr.strip()[:300]},
                ),
                None,
            )
        logged_in = None
        try:
            payload = json.loads(completed.stdout or "{}")
        except json.JSONDecodeError:
            payload = {}
        if isinstance(payload, dict) and payload.get("ok") is True:
            logged_in = payload.get("logged_in")
        return (
            PreflightCheck(
                name="browser_smoke",
                ok=True,
                message=f"{runtime_name} runtime passed GT check-login smoke.",
                detail={"stdout": completed.stdout.strip()[:300], "stderr": completed.stderr.strip()[:300]},
            ),
            logged_in if isinstance(logged_in, bool) else None,
        )

    def _ensure_runtime(self) -> tuple[list[str], str]:
        if self._selected_prefix and self._selected_runner:
            return self._selected_prefix, self._selected_runner
        report = self.doctor(run_browser_smoke=False)
        if not report.ok and report.selected_runner is None:
            raise GTCoreSkillError("gt-core-skill runtime preflight failed.")
        if not self._selected_prefix or not self._selected_runner:
            raise GTCoreSkillError("gt-core-skill runtime unavailable after preflight.")
        return self._selected_prefix, self._selected_runner

    def _run_json(self, args: list[str], *, timeout: int = 120) -> dict[str, Any]:
        prefix, _runtime_name = self._ensure_runtime()
        completed = self._run(prefix + args, timeout=timeout, check=False)
        if completed.returncode != 0:
            raise GTCoreSkillError(
                f"gt-core-skill command failed ({completed.returncode}): {' '.join(prefix + args)}\n"
                f"stdout: {completed.stdout}\nstderr: {completed.stderr}"
            )
        try:
            return json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise GTCoreSkillError(f"gt-core-skill returned invalid JSON: {completed.stdout[:500]}") from exc

    def _run(self, command: list[str], *, timeout: int, check: bool) -> subprocess.CompletedProcess[str]:
        return self.runner(
            command,
            cwd=str(self.skill_root),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=check,
        )

    def _normalize_bridge_listing(self, item: dict[str, Any]) -> dict[str, Any]:
        url = canonicalize_gumtree_url(item.get("url"))
        listing_id = extract_gumtree_listing_id(url)
        return {
            "id": listing_id or url or safe_text(item.get("title")),
            "listing_id": listing_id,
            "title": safe_text(item.get("title")),
            "price": _format_gt_price(item.get("price")),
            "location": safe_text(item.get("location")) or None,
            "url": url,
            "image_url": None,
            "images": [],
            "description": safe_text(item.get("description")) or None,
            "posted_time": safe_text(item.get("age")) or None,
            "category": safe_text(item.get("category")) or None,
            "raw": dict(item),
        }

    def _normalize_bridge_detail(self, payload: dict[str, Any]) -> dict[str, Any]:
        item = payload.get("item") or {}
        attributes = item.get("attributes") if isinstance(item.get("attributes"), dict) else {}
        url = canonicalize_gumtree_url(item.get("url") or payload.get("detail_url"))
        listing_id = extract_gumtree_listing_id(url)
        images = [safe_text(image) for image in item.get("image_urls") or [] if safe_text(image)]
        return {
            "id": listing_id or url or safe_text(item.get("title")),
            "listing_id": listing_id,
            "title": safe_text(item.get("title")),
            "price": safe_text(item.get("price")) or None,
            "location": safe_text(item.get("location")) or None,
            "url": url,
            "image_url": images[0] if images else None,
            "images": images,
            "description": safe_text(item.get("description")) or None,
            "posted_time": safe_text(attributes.get("Posted") or item.get("age")) or None,
            "seller_name": safe_text(item.get("seller_name")) or None,
            "category": safe_text(item.get("category")) or None,
            "detail_fetched": True,
            "attributes": attributes,
            "bedrooms_text": safe_text(attributes.get("Number Of Bedrooms") or attributes.get("Bedrooms")) or None,
            "bathrooms_text": safe_text(attributes.get("Number Of Bathrooms") or attributes.get("Bathrooms")) or None,
            "property_type": safe_text(attributes.get("Property Type")) or None,
            "date_available": safe_text(attributes.get("Date Available")) or None,
            "seller_type": safe_text(attributes.get("Seller Type")) or None,
            "raw": payload,
        }

    def _normalize_api_listing(self, item: dict[str, Any]) -> dict[str, Any]:
        url = canonicalize_gumtree_url(item.get("publicWebsiteUrl"))
        listing_id = extract_gumtree_listing_id(url) or safe_text(item.get("id"))
        image_url = safe_text(item.get("primaryImageUrl")) or None
        price = _format_gt_price(item.get("price"))
        return {
            "id": listing_id or url or safe_text(item.get("title")),
            "listing_id": listing_id or None,
            "title": safe_text(item.get("title")),
            "price": price,
            "location": safe_text(item.get("primaryLocation")) or None,
            "url": url,
            "image_url": image_url,
            "images": [image_url] if image_url else [],
            "description": safe_text(item.get("description")) or None,
            "posted_time": str(item.get("publishedDate")) if item.get("publishedDate") is not None else None,
            "seller_name": None,
            "category": safe_text(item.get("primaryCategory")) or None,
            "detail_fetched": False,
            "detail_degraded_reason": "GT 当前运行模式不支持详情补全",
            "raw": dict(item),
        }


def _format_gt_price(value: Any) -> str | None:
    if isinstance(value, (int, float)):
        integer = int(value)
        if integer == value:
            return f"£{integer:,}"
        return f"£{value:,.2f}"
    text = safe_text(value)
    if not text:
        return None
    return text


class GTPublishSkillClient:
    source_name = "gt-core-skill"
    runtime_mode = "api-publish"
    detail_supported = False

    def __init__(
        self,
        *,
        skill_root: str | Path | None = None,
        runner: Runner | None = None,
        which: Which | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self.env = env or os.environ
        self.runner = runner or subprocess.run
        self.which = which or shutil.which
        self.skill_root = resolve_gt_publish_skill_root(skill_root, self.env, runner=self.runner)
        self._selected_runner: str | None = None
        self._selected_prefix: list[str] | None = None
        self.last_command: list[str] = []

    def doctor(self, *, run_browser_smoke: bool = True) -> PreflightReport:
        root = self.skill_root
        cli_path = root / "scripts" / "cli.py"
        checks = [
            PreflightCheck(name="skill_root", ok=root.exists(), message=f"gt-core-skill publish root: {root}"),
            PreflightCheck(
                name="cli_entry",
                ok=cli_path.exists(),
                message=f"CLI entry {'found' if cli_path.exists() else 'missing'} at {cli_path}",
            ),
            PreflightCheck(
                name="publish_capability",
                ok=probe_gt_publish_capability(root, runner=self.runner),
                message="publish-listing capability detected.",
            ),
        ]
        prefix, runner_name, runtime_check = self._select_runtime()
        checks.append(runtime_check)
        ok = all(check.ok for check in checks if check.name in {"skill_root", "cli_entry", "publish_capability", "runtime_smoke"})
        if runtime_check.ok:
            self._selected_runner = runner_name
            self._selected_prefix = prefix
        else:
            self._selected_runner = None
            self._selected_prefix = None
        return PreflightReport(
            ok=ok,
            skill_root=str(root),
            selected_runner=runner_name if runtime_check.ok else None,
            checks=checks,
            warnings=[],
            source_name=self.source_name,
            runtime_mode=self.runtime_mode,
            detail_supported=self.detail_supported,
        )

    def publish_property(
        self,
        request: PublishPropertyRequest,
        *,
        submit: bool = False,
        save_draft: bool = False,
        dry_run: bool = True,
    ) -> dict[str, Any]:
        payload = gt_publish_payload(request)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            payload_file = handle.name
        args = ["publish-listing", "--payload-file", payload_file]
        if request.publish_endpoint:
            args.extend(["--endpoint", request.publish_endpoint])
        if not submit:
            args.append("--dry-run")
        return self._run_json(args, timeout=120)

    def _select_runtime(self) -> tuple[list[str], str, PreflightCheck]:
        python3 = self.which("python3")
        if python3:
            prefix = ["python3", "scripts/cli.py"]
            check = self._smoke_runtime(prefix, "python3")
            if check.ok:
                return prefix, "python3", check
        python3 = python3 or "python3"
        prefix = [python3, "-m", "gumtree_skills"]
        check = self._smoke_runtime(prefix, "python_module")
        if check.ok:
            return prefix, "python_module", check
        return [], "unavailable", PreflightCheck(
            name="runtime_smoke",
            ok=False,
            message="Neither python3 scripts/cli.py nor python -m gumtree_skills passed GT publish help smoke.",
        )

    def _smoke_runtime(self, prefix: list[str], runtime_name: str) -> PreflightCheck:
        completed = self._run(prefix + ["publish-listing", "--help"], timeout=45, check=False)
        ok = completed.returncode == 0
        return PreflightCheck(
            name="runtime_smoke",
            ok=ok,
            message=f"{runtime_name} runtime {'passed' if ok else 'failed'} GT publish help smoke.",
            detail={"stdout": completed.stdout.strip()[:300], "stderr": completed.stderr.strip()[:300]},
        )

    def _ensure_runtime(self) -> tuple[list[str], str]:
        if self._selected_prefix and self._selected_runner:
            return self._selected_prefix, self._selected_runner
        report = self.doctor(run_browser_smoke=False)
        if not report.ok and report.selected_runner is None:
            raise GTCoreSkillError("gt-core-skill publish runtime preflight failed.")
        if not self._selected_prefix or not self._selected_runner:
            raise GTCoreSkillError("gt-core-skill publish runtime unavailable after preflight.")
        return self._selected_prefix, self._selected_runner

    def _run_json(self, args: list[str], *, timeout: int = 120) -> dict[str, Any]:
        prefix, _runtime_name = self._ensure_runtime()
        self.last_command = prefix + args
        completed = self._run(self.last_command, timeout=timeout, check=False)
        if completed.returncode != 0:
            raise GTCoreSkillError(
                f"gt-core-skill publish command failed ({completed.returncode}): {' '.join(self.last_command)}\n"
                f"stdout: {completed.stdout}\nstderr: {completed.stderr}"
            )
        try:
            return json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise GTCoreSkillError(f"gt-core-skill returned invalid JSON: {completed.stdout[:500]}") from exc

    def _run(self, command: list[str], *, timeout: int, check: bool) -> subprocess.CompletedProcess[str]:
        return self.runner(
            command,
            cwd=str(self.skill_root),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=check,
        )
