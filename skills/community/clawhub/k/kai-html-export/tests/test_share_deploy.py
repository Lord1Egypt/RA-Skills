"""
Tests for HTML share helpers.

Run: python -m pytest tests/test_share_deploy.py -v
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = ROOT / "SKILL.md"
README_MD = ROOT / "README.md"
README_ZH_MD = ROOT / "README.zh-CN.md"
DEPLOY_VERCEL_SCRIPT = ROOT / "scripts" / "deploy-vercel.py"
DEPLOY_CLOUDFLARE_SCRIPT = ROOT / "scripts" / "deploy-cloudflare.py"
SHARE_ROUTER_SCRIPT = ROOT / "scripts" / "share-html.py"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_script_module(script_path: Path, module_name: str):
    assert script_path.exists(), f"Missing helper: {script_path}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    assert spec and spec.loader, f"Failed to build import spec for {script_path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_deploy_module():
    return load_script_module(DEPLOY_VERCEL_SCRIPT, "deploy_vercel")


def load_cloudflare_module():
    return load_script_module(DEPLOY_CLOUDFLARE_SCRIPT, "deploy_cloudflare")


def load_share_router_module():
    return load_script_module(SHARE_ROUTER_SCRIPT, "share_html")


def test_docs_mention_cloudflare_default_and_sandbox_manual_guidance():
    skill = read_text(SKILL_MD)
    readme = read_text(README_MD)
    readme_zh = read_text(README_ZH_MD)

    assert "share-html.py" in skill
    assert "Cloudflare" in skill
    assert "sandbox" in skill.lower()

    assert "share-html.py" in readme
    assert "Cloudflare" in readme
    assert "Vercel" in readme
    assert "sandbox" in readme.lower()

    assert "share-html.py" in readme_zh
    assert "Cloudflare" in readme_zh
    assert "Vercel" in readme_zh


def test_find_vercel_command_uses_resolved_windows_npx(monkeypatch):
    module = load_deploy_module()

    def fake_which(name: str):
        if name == "vercel":
            return None
        if name == "npx":
            return r"C:\Program Files\nodejs\npx.cmd"
        return None

    monkeypatch.setattr(module.shutil, "which", fake_which)

    command = module._find_vercel_command()

    assert command == [r"C:\Program Files\nodejs\npx.cmd", "--yes", "vercel"]


def test_find_wrangler_command_uses_resolved_windows_npx(monkeypatch):
    module = load_cloudflare_module()

    def fake_which(name: str):
        if name == "wrangler":
            return None
        if name == "npx":
            return r"C:\Program Files\nodejs\npx.cmd"
        return None

    monkeypatch.setattr(module.shutil, "which", fake_which)

    command = module._find_wrangler_command()

    assert command == [r"C:\Program Files\nodejs\npx.cmd", "--yes", "wrangler"]


def test_run_uses_utf8_replace_for_cli_output(monkeypatch):
    module = load_deploy_module()
    captured = {}

    def fake_run(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    module._run(["demo"])

    assert captured["kwargs"]["encoding"] == "utf-8"
    assert captured["kwargs"]["errors"] == "replace"


def test_run_wrangler_retries_with_missing_workerd_package(monkeypatch):
    module = load_cloudflare_module()
    calls = []

    def fake_run(*args, **kwargs):
        command = args[0]
        calls.append(command)
        if len(calls) == 1:
            return SimpleNamespace(
                returncode=1,
                stdout="",
                stderr=(
                    'Error: The package "@cloudflare/workerd-windows-64" could not be found, '
                    "and is needed by workerd."
                ),
            )
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    result = module._run_wrangler([r"C:\Program Files\nodejs\npx.cmd", "--yes", "wrangler", "pages", "deploy"])

    assert result.returncode == 0
    assert calls[1] == [
        r"C:\Program Files\nodejs\npx.cmd",
        "--yes",
        "--package",
        "wrangler",
        "--package",
        "@cloudflare/workerd-windows-64",
        "wrangler",
        "pages",
        "deploy",
    ]


def test_deploy_with_vercel_reads_json_deployment_url(monkeypatch, tmp_path: Path):
    module = load_deploy_module()
    deploy_dir = tmp_path / "deploy"
    deploy_dir.mkdir()

    monkeypatch.setattr(module, "_find_vercel_command", lambda: ["vercel"])

    calls = []

    def fake_run(command, *, cwd=None):
        calls.append(command)
        if command[-1] == "--version":
            return SimpleNamespace(returncode=0, stdout="50.39.0", stderr="")
        if command[-1] == "whoami":
            return SimpleNamespace(returncode=0, stdout="kaisersong", stderr="")
        return SimpleNamespace(
            returncode=0,
            stdout=(
                "{"
                '"status":"ok",'
                '"deployment":{"url":"https://demo-app.vercel.app","deploymentApiUrl":"https://api.vercel.com/v13/deployments/demo"}'
                "}\n"
                "Aliased: https://demo-app-alias.vercel.app\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(module, "_run", fake_run)

    url = module.deploy_with_vercel(deploy_dir)

    assert url == "https://demo-app.vercel.app"
    assert any("--format" in cmd for cmd in calls), "deploy_with_vercel must request JSON output"


def test_deploy_with_cloudflare_creates_project_and_returns_pages_url(monkeypatch, tmp_path: Path):
    module = load_cloudflare_module()
    deploy_dir = tmp_path / "deploy"
    deploy_dir.mkdir()

    monkeypatch.setattr(module, "_find_wrangler_command", lambda: ["wrangler"])
    calls = []

    def fake_run_wrangler(command, *, cwd=None):
        calls.append(command)
        if command[-1] == "--version":
            return SimpleNamespace(returncode=0, stdout="4.80.0", stderr="")
        if command[-1] == "whoami":
            return SimpleNamespace(returncode=0, stdout="Logged in as demo@example.com", stderr="")
        if command[:4] == ["wrangler", "pages", "project", "create"]:
            return SimpleNamespace(returncode=0, stdout="Project created", stderr="")
        return SimpleNamespace(
            returncode=0,
            stdout="Deployment complete: https://demo-site.pages.dev",
            stderr="",
        )

    monkeypatch.setattr(module, "_run_wrangler", fake_run_wrangler)

    url = module.deploy_with_cloudflare(deploy_dir, project_name="demo-site")

    assert url == "https://demo-site.pages.dev"
    assert ["wrangler", "pages", "project", "create", "demo-site", "--production-branch", "main"] in calls
    assert [
        "wrangler",
        "pages",
        "deploy",
        str(deploy_dir),
        "--project-name",
        "demo-site",
        "--branch",
        "main",
    ] in calls


def test_deploy_with_cloudflare_allows_existing_project(monkeypatch, tmp_path: Path):
    module = load_cloudflare_module()
    deploy_dir = tmp_path / "deploy"
    deploy_dir.mkdir()

    monkeypatch.setattr(module, "_find_wrangler_command", lambda: ["wrangler"])

    def fake_run_wrangler(command, *, cwd=None):
        if command[-1] == "--version":
            return SimpleNamespace(returncode=0, stdout="4.80.0", stderr="")
        if command[-1] == "whoami":
            return SimpleNamespace(returncode=0, stdout="Logged in as demo@example.com", stderr="")
        if command[:4] == ["wrangler", "pages", "project", "create"]:
            return SimpleNamespace(returncode=1, stdout="A project with this name already exists.", stderr="")
        return SimpleNamespace(
            returncode=0,
            stdout="Deployment complete: https://demo-site.pages.dev",
            stderr="",
        )

    monkeypatch.setattr(module, "_run_wrangler", fake_run_wrangler)

    url = module.deploy_with_cloudflare(deploy_dir, project_name="demo-site")

    assert url == "https://demo-site.pages.dev"


def test_get_linked_project_id_reads_vercel_project_json(tmp_path: Path):
    module = load_deploy_module()
    deploy_dir = tmp_path / "deploy"
    vercel_dir = deploy_dir / ".vercel"
    vercel_dir.mkdir(parents=True)
    (vercel_dir / "project.json").write_text(
        json.dumps({"projectId": "prj_demo", "orgId": "team_demo", "projectName": "demo-project"}),
        encoding="utf-8",
    )

    assert module.get_linked_project_id(deploy_dir) == "prj_demo"


def test_make_project_public_patches_sso_protection_to_null(monkeypatch, tmp_path: Path):
    module = load_deploy_module()
    deploy_dir = tmp_path / "deploy"
    vercel_dir = deploy_dir / ".vercel"
    vercel_dir.mkdir(parents=True)
    (vercel_dir / "project.json").write_text(
        json.dumps({"projectId": "prj_demo", "orgId": "team_demo", "projectName": "demo-project"}),
        encoding="utf-8",
    )

    monkeypatch.setattr(module, "_find_vercel_command", lambda: ["vercel"])
    captured = {}

    def fake_run(command, *, cwd=None):
        captured["command"] = command
        captured["cwd"] = cwd
        return SimpleNamespace(returncode=0, stdout='{"ssoProtection":null}', stderr="")

    monkeypatch.setattr(module, "_run", fake_run)

    module.make_project_public(deploy_dir)

    assert captured["command"][:5] == ["vercel", "api", "/v9/projects/prj_demo", "-X", "PATCH"]
    assert "--input" in captured["command"]


def test_share_router_detects_explicit_disable_env():
    module = load_share_router_module()

    detected = module.detect_share_environment({"KAI_HTML_EXPORT_DISABLE_AUTO_SHARE": "1"})

    assert detected == "cloud-sandbox"


def test_share_router_explicit_enable_overrides_ci():
    module = load_share_router_module()

    detected = module.detect_share_environment(
        {"KAI_HTML_EXPORT_ENABLE_AUTO_SHARE": "1", "CI": "true", "GITHUB_ACTIONS": "true"}
    )

    assert detected == "local"


def test_share_router_defaults_to_cloudflare_provider(monkeypatch, tmp_path: Path):
    module = load_share_router_module()
    html_path = tmp_path / "report.html"
    html_path.write_text("<!DOCTYPE html>", encoding="utf-8")
    calls = []

    monkeypatch.setattr(module, "detect_share_environment", lambda env=None: "local")

    def fake_run(command, check=False):
        calls.append(command)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    exit_code = module.main([str(html_path)])

    assert exit_code == 0
    assert calls == [[sys.executable, str(DEPLOY_CLOUDFLARE_SCRIPT), str(html_path)]]


def test_share_router_supports_vercel_provider_override(monkeypatch, tmp_path: Path):
    module = load_share_router_module()
    html_path = tmp_path / "report.html"
    html_path.write_text("<!DOCTYPE html>", encoding="utf-8")
    calls = []

    monkeypatch.setattr(module, "detect_share_environment", lambda env=None: "local")

    def fake_run(command, check=False):
        calls.append(command)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    exit_code = module.main(["--provider", "vercel", str(html_path)])

    assert exit_code == 0
    assert calls == [[sys.executable, str(DEPLOY_VERCEL_SCRIPT), str(html_path)]]


def test_share_router_blocks_auto_share_in_cloud_sandbox(monkeypatch, tmp_path: Path, capsys):
    module = load_share_router_module()
    html_path = tmp_path / "report.html"
    html_path.write_text("<!DOCTYPE html>", encoding="utf-8")
    called = False

    monkeypatch.setattr(module, "detect_share_environment", lambda env=None: "cloud-sandbox")

    def fake_run(command, check=False):
        nonlocal called
        called = True
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    exit_code = module.main([str(html_path)])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert called is False
    assert "Automatic sharing is disabled" in captured.err
    assert "Cloudflare Pages" in captured.err


def test_stage_input_directory_accepts_index_html(tmp_path: Path):
    module = load_deploy_module()
    deck = tmp_path / "deck"
    deck.mkdir()
    (deck / "index.html").write_text("<!DOCTYPE html><title>deck</title>", encoding="utf-8")

    staged_dir, should_cleanup = module.stage_input(deck)

    assert staged_dir == deck
    assert should_cleanup is False


def test_stage_input_directory_requires_index_html(tmp_path: Path):
    module = load_deploy_module()
    deck = tmp_path / "deck"
    deck.mkdir()

    with pytest.raises(ValueError, match="index.html"):
        module.stage_input(deck)


def test_stage_input_html_copies_relative_assets(tmp_path: Path):
    module = load_deploy_module()
    deck = tmp_path / "source"
    deck.mkdir()
    (deck / "assets").mkdir()
    (deck / "images").mkdir()
    (deck / "assets" / "logo.png").write_bytes(b"png")
    (deck / "images" / "hero.jpg").write_bytes(b"jpg")
    html = """<!DOCTYPE html>
<html>
<body>
  <img src="assets/logo.png" alt="logo">
  <div style="background-image:url('images/hero.jpg')"></div>
</body>
</html>
"""
    html_path = deck / "presentation.html"
    html_path.write_text(html, encoding="utf-8")

    staged_dir, should_cleanup = module.stage_input(html_path)

    try:
        assert should_cleanup is True
        assert (staged_dir / "index.html").exists()
        assert (staged_dir / "assets" / "logo.png").read_bytes() == b"png"
        assert (staged_dir / "images" / "hero.jpg").read_bytes() == b"jpg"
    finally:
        if should_cleanup and staged_dir.exists():
            module.cleanup_staging_dir(staged_dir)
