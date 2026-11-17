#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""import_skill.py — install keelwright from a portable .zip on a new machine

Unpacks the exported .zip, verifies file integrity against _MANIFEST.json, installs
the skill to the Hermes skills directory, runs post-install checks, and reports.

Stdlib only. Usage:
  python import_skill.py keelwright-export-20260725T120000Z.zip
  python import_skill.py keelwright-export-*.zip --force
"""
import zipfile, hashlib, os, sys, time, argparse, json
from pathlib import Path

KEELWRIGHT_SKILLS = Path(os.environ.get(
    "KEELWRIGHT_SKILLS",
    os.path.expanduser("~/.keelwright/skills")))

SKILL_NAME = "keelwright"
INSTALL_TO = KEELWRIGHT_SKILLS / SKILL_NAME

# Post-install checks as ARGUMENT VECTORS, never shell strings.
# {skill} is substituted as a single argv element, so a path containing spaces,
# quotes, &, ; or | is passed verbatim to the process instead of being parsed by a
# shell. Building these as strings + shell=True was a command-injection vector: the
# install path is attacker-influenceable via KEELWRIGHT_SKILLS.
# Each entry: (label, [argv...]) — {skill} placeholders are replaced per element.
POST_INSTALL_CHECKS = [
    ("SKILL.md YAML", ["{python}", "{skill}/scripts/_check_yaml.py", "{skill}/SKILL.md"]),
    ("snapshot verify", ["{python}", "{skill}/scripts/snapshot_skill.py", "verify"]),
    ("validate_run.py", ["{python}", "{skill}/scripts/validate_run.py"]),
    ("workspace_guard.py", ["{python}", "{skill}/scripts/workspace_guard.py"]),
]


def verify_manifest(zf: zipfile.ZipFile, manifest_data: dict) -> list:
    """Verify every file in the manifest exists in the zip with matching sha256."""
    errors = []
    for entry in manifest_data.get("entries", []):
        path = entry["path"]
        expected_sha = entry["sha256"]
        try:
            info = zf.getinfo(path)
        except KeyError:
            errors.append(f"[MISSING] {path} in manifest but not in zip")
            continue
        data = zf.read(path)
        actual_sha = hashlib.sha256(data).hexdigest()
        if actual_sha != expected_sha:
            errors.append(f"[TAMPER] {path}: manifest={expected_sha[:12]} actual={actual_sha[:12]}")
    return errors


def find_skills_dir() -> Path:
    """Auto-detect the agent's skills directory across runtimes (Hermes, OpenClaw, Cursor, Codex, Cline...)."""
    candidates = [
        Path(os.environ.get("KEELWRIGHT_SKILLS", "")) if os.environ.get("KEELWRIGHT_SKILLS") else None,
        Path(os.path.expanduser("~/.keelwright/skills")),
        Path(os.path.expanduser("~/AppData/Local/hermes/skills")),
        Path(os.path.expanduser("~/.local/share/hermes/skills")),
        Path(os.path.expanduser("~/.hermes/skills")),
        Path(os.path.expanduser("~/.openclaw/skills")),
        Path(os.path.expanduser("~/.cursor/skills")),
        Path(os.path.expanduser("~/.config/codex/skills")),
        Path(os.path.expanduser("~/.config/cline/skills")),
    ]
    candidates = [c for c in candidates if c]
    for c in candidates:
        if c.exists():
            return c
    # Default neutral path (runtime-agnostic)
    return Path(os.path.expanduser("~/.keelwright/skills"))


def extract_skill(zf: zipfile.ZipFile, target: Path, include_internal: bool):
    """Extract skill files to target, skipping internal/ unless requested."""
    target.mkdir(parents=True, exist_ok=True)
    skip_prefixes = () if include_internal else ("internal/", "backups/")
    count = 0
    max_files = 5000
    max_total_bytes = 200 * 1024 * 1024
    total_bytes = 0
    for info in zf.infolist():
        if info.is_dir():
            continue
        if getattr(info, "is_symlink", lambda: False)():
            continue
        arcname = info.filename
        # Skip non-skill files (QA run data lives elsewhere)
        if arcname.startswith("kw-qa/") or arcname.startswith("2026"):
            continue
        if arcname.startswith("_"):
            continue  # manifest, context-transfer
        if not include_internal and any(arcname.startswith(p) for p in skip_prefixes):
            print(f"  [SKIP] {arcname}")
            continue
        # Extract
        data = zf.read(info.filename)
        if total_bytes + len(data) > max_total_bytes:
            print(f"  [BLOCK] archive size budget exceeded — stopping extraction")
            break
        if count >= max_files:
            print(f"  [BLOCK] archive file count budget exceeded — stopping extraction")
            break
        dest = (target / arcname).resolve()
        # ZIP-SLIP GUARD: reject any entry that escapes the install target.
        target_resolved = target.resolve()
        if dest != target_resolved and target_resolved not in dest.parents:
            print(f"  [BLOCK] {arcname} escapes install dir — skipped (zip-slip)")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        total_bytes += len(data)
        count += 1
    return count


def run_checks(skill_dir: Path):
    """Run post-install verification checks.

    SECURITY: this EXECUTES code from the freshly imported skill. Never call it
    implicitly — it must stay behind the explicit --run-checks flag, because a .zip is
    untrusted input and its manifest is self-attested (an attacker who edits a script
    also recomputes its SHA256, so integrity verification does not establish trust).

    Commands run as argument vectors with shell=False: no shell parses the install
    path, so metacharacters in it cannot become commands.
    """
    import subprocess
    results = []
    skill_str = str(skill_dir).replace("\\", "/")
    for label, argv_template in POST_INSTALL_CHECKS:
        argv = [part.replace("{skill}", skill_str).replace("{python}", sys.executable)
                for part in argv_template]
        try:
            r = subprocess.run(
                argv, shell=False, capture_output=True, text=True, timeout=30,
                encoding="utf-8", errors="replace",
                cwd=str(skill_dir))
            output = (r.stdout + r.stderr).strip()
            ok = r.returncode == 0
            results.append((label, ok, output.split("\n")[0] if output else "no output"))
        except subprocess.TimeoutExpired:
            results.append((label, False, "TIMEOUT"))
        except Exception as e:
            results.append((label, False, str(e)[:80]))
    return results


def import_skill(zip_path: Path, force: bool = False, include_internal: bool = True,
                 run_post_checks: bool = False):
    if not zip_path.exists():
        print(f"[ERROR] {zip_path} not found"); return 1

    # Defense-in-depth: reject malformed/malicious export filenames.
    # Expected pattern: keelwright-export-<YYYYMMDD>T<HHMMSS>Z.zip
    import re
    if not re.fullmatch(r"keelwright-export-\d{8}T\d{6}Z\.zip", zip_path.name):
        print(f"[ERROR] Unexpected archive name '{zip_path.name}'. "
              f"Expected 'keelwright-export-YYYYMMDDTHHMMSSZ.zip'. "
              f"Refusing to install (possible tampered/untrusted source).")
        return 1

    print(f"Import from: {zip_path} ({zip_path.stat().st_size//1024}KB)")

    with zipfile.ZipFile(zip_path) as zf:
        # 1. Read manifest
        if "_MANIFEST.json" not in zf.namelist():
            print("[FAIL] No _MANIFEST.json — integrity cannot be verified. "
                  "Refusing to install unverified archive.")
            return 1
        manifest = json.loads(zf.read("_MANIFEST.json"))

        # 2. Verify integrity
        print("\n--- Integrity check ---")
        errors = verify_manifest(zf, manifest)
        if errors:
            for e in errors:
                print(f"  {e}")
            print(f"\n[FAIL] {len(errors)} integrity errors — refusing to install.")
            return 1
        print(f"  All {len(manifest.get('entries', []))} files verified OK")

        # 3. Check target
        env_override = os.environ.get("KEELWRIGHT_SKILLS")
        if env_override:
            INSTALL_TO = Path(env_override) / SKILL_NAME
        else:
            INSTALL_TO = find_skills_dir() / SKILL_NAME
        if INSTALL_TO.exists() and not force:
            print(f"\n[STOP] {INSTALL_TO} already exists. Use --force to overwrite.")
            return 1

        # 4. Extract
        print(f"\n--- Install to {INSTALL_TO} ---")
        count = extract_skill(zf, INSTALL_TO, include_internal)
        print(f"  Installed {count} files")

        # 5. Extract context-transfer prompt — INSIDE the skill dir only.
        # It used to land in ~/kw-qa/, i.e. outside the install target: content from an
        # untrusted archive was planted into a shared working directory that other runs
        # read from, with nothing tying it to the skill it came from. Keeping it under
        # the skill keeps every imported byte inside one reviewable, removable tree.
        if "_CONTEXT-TRANSFER-PROMPT.md" in zf.namelist():
            ct_dest = INSTALL_TO / "imported" / "CONTEXT-TRANSFER-PROMPT.md"
            ct_dest.parent.mkdir(parents=True, exist_ok=True)
            ct_dest.write_bytes(zf.read("_CONTEXT-TRANSFER-PROMPT.md"))
            print(f"  Context-transfer prompt → {ct_dest}")
            print(f"  (from the archive — review before feeding it to an agent)")

    # 6. Post-install checks — OPT-IN ONLY.
    # These execute code from the archive you just unpacked. A .zip is untrusted input,
    # and step 2 proves only self-consistency (the manifest ships inside the same file),
    # never provenance. So running them is a separate, explicit decision.
    all_ok = True
    if run_post_checks:
        print(f"\n--- Post-install checks (executing code from the imported skill) ---")
        for label, ok, output in run_checks(INSTALL_TO):
            print(f"  [{'OK' if ok else 'FAIL'}] {label}: {output}")
            all_ok = all_ok and ok
    else:
        print(f"\n--- Post-install checks: SKIPPED ---")
        print(f"  These run shell commands from the imported skill, so they are opt-in.")
        print(f"  Inspect {INSTALL_TO}, then re-run with --run-checks if you trust it.")

    # 7. Summary
    print(f"\n=== IMPORT {'SUCCESS' if all_ok else 'PARTIAL'} ===")
    print(f"  Skill: {INSTALL_TO}")
    print(f"  Files: {count}")
    if not run_post_checks:
        print(f"  Status: installed, unverified (checks skipped — see --run-checks)")
    elif all_ok:
        print(f"  Status: ready to use. Load with skill_view(name='keelwright')")
    else:
        print(f"  Status: installed but some checks failed — review above")
    return 0 if all_ok else 1


def main():
    parser = argparse.ArgumentParser(description="Import keelwright skill from .zip")
    parser.add_argument("zipfile", help="Path to the exported .zip")
    parser.add_argument("--force", action="store_true", help="Overwrite existing skill")
    parser.add_argument("--no-internal", action="store_true", help="Skip internal/ files")
    parser.add_argument("--run-checks", action="store_true",
                        help="Run post-install checks. WARNING: executes shell commands "
                             "from the imported skill — only for archives you trust.")
    args = parser.parse_args()
    return import_skill(Path(args.zipfile), args.force, not args.no_internal,
                        args.run_checks)


if __name__ == "__main__":
    exit(main())
