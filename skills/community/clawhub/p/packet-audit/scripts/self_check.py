#!/usr/bin/env python3
"""Self-check for the packet-audit package.

One named rule per thing that has broken a release before. Each rule returns a
boolean and a human-readable detail, and the script exits non-zero when any rule
fails, so a publish can gate on it.

Rules:
  RC1  version in SKILL.md, the engine constant, and CHANGELOG agree
  RC2  every bundled profile loads and validates
  RC3  the shipped scripts import no network module
  RC4  no author-absolute path is shipped
  RC5  no floating version in install commands
  RC6  every shipped module compiles
  RC7  the CLI answers --list-profiles
  RC8  no HTML comments in shipped markdown
  RC9  the test suite is present and non-trivial
  RC10 the SKILL.md declares its tool scope
"""

from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
ENGINE = ROOT / "scripts" / "packet_audit.py"
CHECKLIST = ROOT / "CHANGELOG.md"

checks: list[dict] = []


def record(name: str, ok: bool, detail: str) -> None:
    checks.append({"name": name, "ok": bool(ok), "detail": detail})


def frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}, text
    block = match.group(1)
    meta = {}
    line = re.search(r"^metadata:\s*(\{.*\})\s*$", block, re.M)
    if line:
        try:
            meta = json.loads(line.group(1))
        except json.JSONDecodeError:
            meta = {"_parse_error": line.group(1)}
    name = re.search(r"^name:\s*(\S+)\s*$", block, re.M)
    description = re.search(r"^description:\s*(.+)$", block, re.M)
    return {"meta": meta, "name": name.group(1) if name else "",
            "description": description.group(1).strip() if description else ""}, text[match.end():]


def rule_version() -> None:
    text = SKILL.read_text(encoding="utf-8")
    head, _ = frontmatter(text)
    meta = head.get("meta", {})
    skill_version = str(meta.get("version", ""))
    engine_version = re.search(r'^TOOL_VERSION = "([^"]+)"', ENGINE.read_text(encoding="utf-8"), re.M)
    engine_version = engine_version.group(1) if engine_version else ""
    changelog = CHECKLIST.read_text(encoding="utf-8")
    top = re.search(r"^##\s*v?([0-9][0-9A-Za-z.\-]*)", changelog, re.M)
    changelog_version = top.group(1) if top else ""
    ok = bool(skill_version) and skill_version == engine_version == changelog_version
    record("RC1 version agrees across SKILL.md, engine, CHANGELOG", ok,
           f"skill={skill_version!r} engine={engine_version!r} changelog={changelog_version!r}")


def rule_profiles() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import packet_audit as pa
    failures = []
    profiles = sorted((ROOT / "profiles").glob("*.json"))
    for path in profiles:
        try:
            pa.load_profile(path)
        except Exception as exc:  # noqa: BLE001 - any profile failure is a failure
            failures.append(f"{path.name}: {exc}")
    record("RC2 every bundled profile validates", not failures and bool(profiles),
           f"{len(profiles)} profile(s); " + ("; ".join(failures) if failures else "all valid"))


def rule_no_network() -> None:
    pattern = re.compile(r"^\s*(?:import|from)\s+(socket|ssl|urllib|http|requests|httpx|aiohttp|ftplib|telnetlib)\b", re.M)
    offenders = []
    for path in sorted((ROOT / "scripts").glob("*.py")):
        if pattern.search(path.read_text(encoding="utf-8")):
            offenders.append(path.name)
    record("RC3 shipped scripts import no network module", not offenders,
           ", ".join(offenders) if offenders else "no network imports")


def rule_no_absolute_paths() -> None:
    pattern = re.compile(r"(?:[A-Za-z]:\\\\?Users\\\\|[A-Za-z]:\\\\?LYGO|/home/[a-z]|/Users/[A-Za-z])")
    skip = {".git", "__pycache__"}
    offenders = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in skip for part in path.parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".pdf", ".pyc"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if pattern.search(text):
            offenders.append(path.relative_to(ROOT).as_posix())
    record("RC4 no author-absolute path is shipped", not offenders,
           ", ".join(offenders) if offenders else "none found")


def rule_no_floating_versions() -> None:
    # The version lives in the frontmatter's `metadata` dict, so read it from there: the old
    # hardcoded "1.0.0" kept passing after the package moved to 1.1.0 and the shipped docs
    # went on telling readers to install the previous release. If the version cannot be read,
    # the rule fails rather than skipping the check.
    head, _body = frontmatter(SKILL.read_text(encoding="utf-8"))
    current = str((head.get("meta") or {}).get("version", "")).strip()
    if not current:
        record("RC5 install commands are pinned", False, "no version in SKILL.md metadata")
        return
    # Only install commands are checked. A changelog entry recording an old release as prose is
    # history, not an instruction, and flagging it would push the author to rewrite the record.
    offenders = []
    for path in sorted(ROOT.rglob("*.md")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            low = line.lower()
            if "clawhub" not in low or "install" not in low:
                continue
            if "clawhub@latest" in low:
                offenders.append(f"{path.name}:{number}: clawhub@latest")
            for pinned in re.findall(r"packet-audit@([0-9][0-9A-Za-z.\-]*)", line):
                if pinned != current:
                    offenders.append(
                        f"{path.name}:{number}: pins packet-audit@{pinned}, current is {current}")
    record("RC5 install commands are pinned", not offenders,
           "; ".join(sorted(set(offenders))) if offenders else f"pinned at {current}")


def rule_compiles() -> None:
    failures = []
    for path in sorted(ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            py_compile.compile(str(path), doraise=True, cfile=str(Path(tempfile.gettempdir()) / "pa_check.pyc"))
        except py_compile.PyCompileError as exc:
            failures.append(f"{path.name}: {exc.msg}")
    record("RC6 every shipped module compiles", not failures,
           "; ".join(failures) if failures else "all modules compile")


def rule_cli() -> None:
    result = subprocess.run([sys.executable, str(ENGINE), "--list-profiles"],
                            capture_output=True, text=True, timeout=60, cwd=str(ROOT))
    ok = result.returncode == 0 and "rental-us" in result.stdout
    record("RC7 the CLI answers --list-profiles", ok,
           (result.stdout or result.stderr).strip().splitlines()[0] if (result.stdout or result.stderr) else "no output")


def rule_no_html_comments() -> None:
    offenders = [p.name for p in sorted(ROOT.rglob("*.md"))
                 if "<!--" in p.read_text(encoding="utf-8")]
    record("RC8 no HTML comments in shipped markdown", not offenders,
           ", ".join(offenders) if offenders else "none")


def rule_tests() -> None:
    suites = sorted((ROOT / "tests").glob("test_*.py"))
    if not suites:
        record("RC9 the test suite is present and non-trivial", False, "no tests/test_*.py")
        return
    count = sum(len(re.findall(r"^\s+def test_", p.read_text(encoding="utf-8"), re.M))
                for p in suites)
    record("RC9 the test suite is present and non-trivial", count >= 15,
           f"{count} test method(s) in {len(suites)} suite(s)")


def rule_scope() -> None:
    text = SKILL.read_text(encoding="utf-8")
    head, body = frontmatter(text)
    description = head.get("description", "")
    has_scope = "permissions:" in body or "## Permissions" in body
    has_bound = "When not to use" in body or "Do not use" in body
    tight = 40 <= len(description) <= 700
    ok = has_scope and has_bound and tight
    record("RC10 SKILL.md declares tool scope and a when-not-to-use bound", ok,
           f"permissions={has_scope} bound={has_bound} description_chars={len(description)}")


def main() -> int:
    rules = [rule_version, rule_profiles, rule_no_network, rule_no_absolute_paths,
             rule_no_floating_versions, rule_compiles, rule_cli, rule_no_html_comments,
             rule_tests, rule_scope]
    for rule in rules:
        try:
            rule()
        except Exception as exc:  # noqa: BLE001 - a crashing rule is a failing rule
            record(rule.__name__, False, f"rule raised {type(exc).__name__}: {exc}")
    failed = [c["name"] for c in checks if not c["ok"]]
    payload = {"ok": not failed, "failed": failed, "checks": checks}
    print(json.dumps(payload, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
