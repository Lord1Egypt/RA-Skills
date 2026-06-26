import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = REPO_ROOT / "manifest.json"
SKILL_PATH = REPO_ROOT / "SKILL.md"
INSTALL_PATH = REPO_ROOT / "install.sh"

REQUIRED_FIELDS = ["install", "filesystem_writes", "capabilities", "network_access"]


def _load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_skill_required_fields() -> dict:
    text = SKILL_PATH.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    front_matter = parts[1]
    data: dict[str, object] = {}
    for line in front_matter.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in REQUIRED_FIELDS and value:
            data[key] = json.loads(value)
    return data


def test_manifest_has_all_required_fields():
    manifest = _load_manifest()
    for field in REQUIRED_FIELDS:
        assert field in manifest, f"manifest missing {field}"


def test_skill_md_matches_manifest():
    manifest = _load_manifest()
    skill_fields = _load_skill_required_fields()
    for field in REQUIRED_FIELDS:
        assert field in skill_fields, f"SKILL.md missing {field}"
        assert skill_fields[field] == manifest[field]


def test_install_script_matches_declared_writes():
    manifest = _load_manifest()
    declared = manifest["filesystem_writes"][0]
    line = None
    for raw in INSTALL_PATH.read_text(encoding="utf-8").splitlines():
        if raw.startswith("# DECLARES_WRITES:"):
            line = raw
            break
    assert line is not None, "install.sh missing DECLARES_WRITES header"
    header_path = line.split(":", 1)[1].strip()
    assert header_path == declared


def test_no_undeclared_write_paths():
    script = INSTALL_PATH.read_text(encoding="utf-8")
    for line in script.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "cp " in stripped or stripped.startswith("mkdir "):
            assert "$TARGET" in stripped or "$STATE_DIR" in stripped


def test_validate_metadata_script_exits_zero():
    env = os.environ.copy()
    result = subprocess.run(
        ["python3", str(REPO_ROOT / "tools" / "validate_metadata.py")],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_linters_marked_optional_in_manifest():
    manifest = _load_manifest()
    requires = manifest.get("requires", {})
    bins = requires.get("bins", [])
    optional_bins = requires.get("optional_bins", [])
    # Required bins are simple strings in the bins array
    assert "codex" in bins
    assert "git" in bins
    # Linters are in optional_bins, not in required bins
    assert "ruff" in optional_bins
    assert "flake8" in optional_bins
    assert "pylint" in optional_bins
    assert "ruff" not in bins
    assert "flake8" not in bins
    assert "pylint" not in bins


def test_env_vars_declared_in_manifest():
    manifest = _load_manifest()
    requires = manifest.get("requires", {})
    envs = {item["name"]: item for item in requires.get("env", [])}
    expected = {
        "OPENCLAW_WORKSPACE",
        "GOVERNED_WORK_DIR",
        "GOVERNED_DB_PATH",
        "GOVERNED_AUTH_TOKEN",
        "CODEX_CLI",
        "GOVERNED_NO_NETWORK",
        "GOVERNED_NO_DB",
        "GOVERNED_DB_MODE",
    }
    assert expected.issubset(envs.keys())
    for name in expected:
        assert envs[name].get("optional") is True
