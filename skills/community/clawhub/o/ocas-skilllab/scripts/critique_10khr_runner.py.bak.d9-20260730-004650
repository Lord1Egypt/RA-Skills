#!/usr/bin/env python3
"""
10khr_runner.py — Autonomous skill improvement engine.

Grinds on the lowest-scoring ocas-* / util-* skill until it hits 50/50,
then moves to the next one. After every 5 skills improved, re-runs
the full library assessment.

Usage:
    python3 10khr_runner.py [--skills-dir <dir>] [--report-only] [--all-profiles]

Workflow:
    1. Find all ocas-* and util-* skills across the entire skill library
    2. Score each using the critique rubric (via agent invocation)
    3. Sort by score (lowest first)
    4. For each skill below 50/50:
        a. Run critique.iterate until 50/50
        b. Log learnings to journal
    5. After every 5 skills, re-assess entire library
    6. Update the learning journal with new patterns discovered

Directory discovery:
    By default, scans the active profile's skills directory and all subdirectories.
    With --all-profiles, scans all profiles under ~/.hermes/profiles/.
    Always uses recursive glob — skills may live at any depth (e.g.,
    infrastructure/util-vps-cleanup, software-development/ocas-10xeng).
"""

import json
import io
import os
import py_compile
import re
import sys
import glob
from datetime import datetime, timezone

# ─── Configuration ───────────────────────────────────────────────────────────

# Default: scan the indigo profile (active profile) recursively
# Resolve against HERMES_ROOT or ~/.hermes to avoid broken ~ expansion
# when HOME is set to a profile chroot (e.g., ~/.hermes/profiles/indigo/home)
_HERMES_ROOT = os.environ.get("HERMES_ROOT", os.path.expanduser("~/.hermes"))
DEFAULT_SKILLS_DIR = os.path.join(_HERMES_ROOT, "profiles", "indigo", "skills")
DEFAULT_PROFILE_SKILLS_DIR = os.path.join(_HERMES_ROOT, "skills")
TARGET_SCORE = 50
REASSESS_INTERVAL = 5  # re-score full library after N skills improved
STATE_FILE = os.path.join(_HERMES_ROOT, "skills", "ocas-critique", "commons", "data", "ocas-critique", "10khr-state.json")

# ─── Helpers ─────────────────────────────────────────────────────────────────


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "version": 1,
        "started_at": None,
        "last_run": None,
        "skills_improved": 0,
        "total_iterations": 0,
        "skill_history": [],
        "current_target": None,
    }


def save_state(state: dict):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def find_all_skills(skills_dir: str = None, all_profiles: bool = False) -> list:
    """
    Return sorted list of (name, path) tuples for all ocas-* and util-* skills.

    Uses recursive glob to find skills at any depth:
      - ~/.hermes/profiles/indigo/skills/ocas-foo/SKILL.md
      - ~/.hermes/profiles/indigo/skills/infrastructure/util-bar/SKILL.md
      - ~/.hermes/profiles/koda/skills/software-development/ocas-baz/SKILL.md

    Deduplicates by skill name (first found wins).
    """
    search_roots = []

    if all_profiles:
        # Scan all profiles under <HERMES_ROOT>/profiles/
        # Use HERMES_ROOT (NOT expanduser("~/.hermes/profiles")): under a profile
        # chroot (HOME=~/.hermes/profiles/<profile>/home) expanduser resolves to
        # the active profile's home, silently dropping every OTHER profile (e.g. koda).
        # Confirmed bug 2026-07-15 — --all-profiles reported 60 skills and missed
        # koda/ocas-eng-debug until this was fixed.
        profiles_dir = os.path.join(_HERMES_ROOT, "profiles")
        if os.path.isdir(profiles_dir):
            for profile in sorted(os.listdir(profiles_dir)):
                profile_skills = os.path.join(profiles_dir, profile, "skills")
                if os.path.isdir(profile_skills):
                    search_roots.append(profile_skills)
        # Also include the default profile
        if os.path.isdir(DEFAULT_PROFILE_SKILLS_DIR):
            search_roots.append(DEFAULT_PROFILE_SKILLS_DIR)
    elif skills_dir:
        search_roots.append(skills_dir)
    else:
        # Default: active profile + default profile
        search_roots.append(DEFAULT_SKILLS_DIR)
        if os.path.isdir(DEFAULT_PROFILE_SKILLS_DIR):
            search_roots.append(DEFAULT_PROFILE_SKILLS_DIR)

    seen = set()
    seen_realpaths = set()
    results = []

    for root in search_roots:
        # Resolve the root to its real path to avoid symlink duplicates
        real_root = os.path.realpath(root)
        if real_root in seen_realpaths:
            continue
        seen_realpaths.add(real_root)

        # Recursive glob: finds SKILL.md at any depth
        for path in sorted(glob.glob(f"{root}/**/SKILL.md", recursive=True)):
            real_path = os.path.realpath(path)
            name = os.path.basename(os.path.dirname(real_path))
            # Only include ocas-* and util-* prefixed skills
            if not (name.startswith("ocas-") or name.startswith("util-")):
                continue
            if name in seen:
                continue
            if ".archive" in real_path:
                continue
            seen.add(name)
            results.append((name, real_path))

    return results



# ── Execution- and AST-based checks (2026-07-26) ──────────────────────────
# This scorer used to read source text and infer behaviour. It cannot: a script
# containing the string "--help" may still crash before argparse ever runs, and
# a 478-line file can be 19k tokens. Observe instead of inferring.

SCRIPT_TIMEOUT = 30
EXECUTE_CHECKS = True          #: D8/D9 run the skill's scripts. Off for untrusted trees.

# \W+ deliberately: matches shell form (reset --hard) AND subprocess list form
# (["git", "reset", "--hard"]). A whitespace-only regex misses every list form,
# which is how scripts actually invoke git.
DESTRUCTIVE = [
    (re.compile(r"reset\W+--hard"), "git reset --hard"),
    (re.compile(r"clean\W+-[a-z]*f[a-z]*d\b"), "git clean -fd"),
    (re.compile(r"\brm\W+-[a-z]*r[a-z]*f\b"), "rm -rf"),
    (re.compile(r"\bDROP\W+TABLE\b", re.I), "DROP TABLE"),
    (re.compile(r"shutil\.rmtree\("), "shutil.rmtree"),
    (re.compile(r"push\W+--force(?!-with-lease)"), "git push --force"),
]
GUARD = re.compile(r"dry[_-]?run|confirm|are you sure|input\(|refus|abort|--force\b", re.I)

STDLIB_OK = re.compile(
    r"^(?:os|sys|re|io|json|argparse|subprocess|pathlib|datetime|time|glob|shutil|"
    r"typing|collections|itertools|functools|math|random|hashlib|base64|csv|sqlite3|"
    r"urllib|tempfile|textwrap|logging|unittest|py_compile|dataclasses|enum|uuid|ast|"
    r"traceback|warnings|copy|string|struct|socket|threading|queue|signal|platform|"
    r"curses|shlex|select|errno|stat|difflib|pprint|pickle|gzip|tarfile|zipfile|"
    r"secrets|statistics|decimal|fractions|numbers|operator|bisect|heapq|array|"
    r"configparser|getpass|inspect|importlib|contextlib|abc|__future__)$")


def _run(cmd, cwd=None):
    import subprocess
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=SCRIPT_TIMEOUT)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return 1, str(e)


def check_scripts_help(script_dir, execute=True):
    """Do the scripts ACTUALLY answer --help? Returns (ok, broken, total)."""
    import os
    if not os.path.isdir(script_dir):
        return [], [], 0
    scripts = sorted(f for f in os.listdir(script_dir) if f.endswith((".py", ".sh")))
    ok, broken = [], []
    for name in scripts:
        path = os.path.join(script_dir, name)
        if execute:
            cmd = ["bash", path, "--help"] if name.endswith(".sh") else [sys.executable, path, "--help"]
            rc, _ = _run(cmd, cwd=script_dir)
            ok.append(name) if rc == 0 else broken.append("%s (rc=%d)" % (name, rc))
        else:
            try:
                src = io.open(path, encoding="utf-8", errors="ignore").read()
            except (OSError, UnicodeDecodeError):
                continue
            ok.append(name) if "--help" in src else broken.append(name)
    return ok, broken, len(scripts)


def check_module_scope_imports(script_dir):
    """Third-party imports at module scope break --help wherever they're absent.

    Executing --help only proves it works in THIS interpreter. A module-scope
    optional import exits before argparse on any machine lacking it — the exact
    failure an all-deps environment cannot reveal.
    """
    import ast, glob, os
    offenders = []
    for sp in sorted(glob.glob(os.path.join(script_dir, "*.py"))):
        try:
            tree = ast.parse(io.open(sp, encoding="utf-8", errors="ignore").read())
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue
        for node in tree.body:                       # module scope only
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods = [node.module]
            hit = next((m for m in mods if not STDLIB_OK.match(m.split(".")[0])), None)
            if hit:
                offenders.append("%s: %s" % (os.path.basename(sp), hit.split(".")[0]))
                break
    return offenders


def _ref_resolves(skill_dir, ref):
    """True if `ref` resolves anywhere a skill may legitimately point.

    Skills cross-reference each other constantly. Resolving only against
    skill_dir marks all of those dead — the false positive that makes a
    dead-ref check worthless. Try, in order: the skill itself, the skills
    root (handles "ocas-vibes/references/x.md" and "../other-skill/x.md"),
    then the bare basename under any sibling skill's usual subdirs.
    """
    if os.path.exists(os.path.join(skill_dir, ref)):
        return True
    root = os.path.dirname(os.path.abspath(skill_dir.rstrip("/")))
    if os.path.exists(os.path.normpath(os.path.join(root, ref))):
        return True
    if os.path.exists(os.path.normpath(os.path.join(skill_dir, ref))):
        return True
    # Shared helpers live in the AGENT ROOT's scripts/ dir, one level above
    # skills/ — e.g. google_auth.py, which several skills document and use.
    agent_root = os.path.dirname(root)
    if agent_root and os.path.exists(os.path.normpath(os.path.join(agent_root, ref))):
        return True
    base = os.path.basename(ref)
    try:
        siblings = os.listdir(root)
    except OSError:
        return False
    for sib in siblings:
        p = os.path.join(root, sib)
        if not os.path.isdir(p):
            continue
        for sub in ("", "references", "scripts", "assets", "templates"):
            if os.path.exists(os.path.join(p, sub, base)):
                return True
    return False


# Filename TEMPLATES are not missing files: `ingest_cron_YYYYMMDD.py` is a
# naming convention, and flagging it produces nonsense edits.
_PLACEHOLDER = re.compile(
    r"YYYYMMDD|YYYY-MM-DD|<[^>]+>|\{[^}]+\}|\.\.\.|"
    r"^(X|Y|Z|foo|bar|baz|example|template|your_\w+|my_\w+)\.(py|sh|md)$", re.I)


def check_dead_references(skill_dir):
    """Files SKILL.md points at that do not exist anywhere reachable.

    A pointer to a doc that was never written is a promise the skill cannot
    keep; an agent that follows it wastes a turn and loses trust in the rest
    of the file.
    """
    sk = os.path.join(skill_dir, "SKILL.md")
    try:
        text = io.open(sk, encoding="utf-8", errors="ignore").read()
    except OSError:
        return []
    refs = set(re.findall(
        r"(?:[A-Za-z0-9._\-]+/)*(?:references|scripts|assets|templates)/[A-Za-z0-9._\-/]+",
        text))
    dead = []
    for r in refs:
        base = os.path.basename(r)
        if not re.search(r"\.[A-Za-z0-9]{1,5}$", base):
            continue          # a directory mention, not a file
        if _PLACEHOLDER.search(base):
            continue
        if not _ref_resolves(skill_dir, r):
            dead.append(r)
    return sorted(dead)


def check_frontmatter_parses(skill_dir):
    """Frontmatter must PARSE, not merely contain the right field names.

    The previous check was a regex for `name:`, which matches even when
    unresolved merge-conflict markers sit between the --- fences. Twelve
    public skills shipped that way: every field was "present", the YAML was
    invalid, and the skill would not load for anyone who installed it.
    """
    problems = []
    sk = os.path.join(skill_dir, "SKILL.md")
    try:
        text = io.open(sk, encoding="utf-8", errors="ignore").read()
    except OSError:
        return ["SKILL.md unreadable"]

    if re.search(r"^(<{7} |={7}$|>{7} )", text, re.M):
        problems.append("unresolved merge-conflict markers in SKILL.md")

    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        problems.append("no YAML frontmatter block")
        return problems
    try:
        import yaml
        meta = yaml.safe_load(m.group(1))
    except Exception as e:
        problems.append("frontmatter does not parse: %s" % type(e).__name__)
        return problems
    if not isinstance(meta, dict):
        problems.append("frontmatter is not a mapping")
        return problems
    for field in ("name", "description"):
        if not meta.get(field):
            problems.append("frontmatter missing '%s'" % field)
    return problems


def check_correctness(skill_dir):
    """D8: does the skill demonstrate it works, and is it safe to run?"""
    import glob, os
    findings, score = [], 5

    tdir = os.path.join(skill_dir, "tests")
    if not (os.path.isdir(tdir) and glob.glob(os.path.join(tdir, "test_*.py"))):
        score -= 2; findings.append("no tests")
    else:
        rc, out = _run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=skill_dir)
        if rc != 0:
            score -= 2
            findings.append("tests FAIL: " + (out.strip().splitlines() or ["?"])[-1][:60])

    if not glob.glob(os.path.join(skill_dir, ".github", "workflows", "*.y*ml")):
        score -= 1; findings.append("no CI workflow")

    # Report EVERY unguarded destructive call, sorted (glob order is arbitrary).
    hits = []
    for sp in sorted(glob.glob(os.path.join(skill_dir, "scripts", "*"))):
        if not sp.endswith((".py", ".sh")):
            continue
        try:
            raw = io.open(sp, encoding="utf-8", errors="ignore").read()
        except (OSError, UnicodeDecodeError):
            continue
        code = "\n".join(l for l in raw.splitlines() if not l.lstrip().startswith("#"))
        if GUARD.search(code):
            continue
        # `rm -rf "$VAR"` on a mktemp dir under `set -u` is the standard safe
        # cleanup idiom; flagging it teaches people to ignore this check.
        safe_tmp = "mktemp" in code and re.search(r"set\s+-[a-z]*u", code)
        for rx, lbl in DESTRUCTIVE:
            if rx.search(code) and not (lbl == "rm -rf" and safe_tmp):
                hits.append("%s in %s" % (lbl, os.path.basename(sp)))
    if hits:
        score -= 2; findings.append("unguarded " + "; ".join(sorted(set(hits))))

    for sp in sorted(glob.glob(os.path.join(skill_dir, "scripts", "*.py"))):
        try:
            py_compile.compile(sp, doraise=True)
        except Exception:
            score -= 1; findings.append("%s does not compile" % os.path.basename(sp)); break

    imp = check_module_scope_imports(os.path.join(skill_dir, "scripts"))
    if imp:
        score -= 1
        findings.append("module-scope 3rd-party import (breaks --help without deps): "
                        + ", ".join(imp[:3]))

    gate = os.path.join(skill_dir, "scripts", "check_no_pii.py")
    if os.path.exists(gate):
        rc, _ = _run([sys.executable, gate, "--quiet"], cwd=skill_dir)
        if rc != 0:
            score -= 1; findings.append("PII gate FAILS")

    return max(1, score), findings


def score_skill(skill_name: str, skill_path: str) -> dict:
    """
    Score a skill by reading its SKILL.md and evaluating the 10 rubric dimensions.
    Returns a dict with scores per dimension and total.
    This is a local heuristic score — the agent does the real scoring via critique.assess.
    """
    if not os.path.exists(skill_path):
        return {"total": 0, "dimensions": {}, "error": "SKILL.md not found"}

    with open(skill_path) as f:
        content = f.read()
    lines = content.split("\n")

    scores = {}

    # ── D1: Frontmatter ──
    d1 = 5
    try:
        import yaml
        parts = content.split("---")
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
        else:
            fm = {}
            d1 -= 2
    except Exception:
        fm = {}
        d1 -= 3

    if not fm.get("name"):
        d1 -= 2
    if not fm.get("description"):
        d1 -= 2
    if "license" not in content[:500].lower():
        d1 -= 1
    skill_dir = os.path.dirname(skill_path)
    has_refs = os.path.isdir(os.path.join(skill_dir, "references"))
    if has_refs and "includes" not in str(fm):
        d1 -= 1
    scores["D1"] = max(1, d1)

    # ── D2: Description quality ──
    d2 = 3
    desc = str(fm.get("description", ""))
    if len(desc) > 50:
        d2 += 1
    if "not for" in desc.lower() or "NOT for" in desc:
        d2 += 1
    if fm.get("triggers"):
        d2 = min(5, d2 + 1)
    scores["D2"] = min(5, d2)

    # ── D3: Conciseness (code ratio) ──
    total_lines = len(lines)
    code_lines = sum(1 for l in lines if l.strip().startswith("```"))
    ratio = (code_lines / total_lines * 100) if total_lines > 0 else 0
    if ratio < 15:
        d3 = 5
    elif ratio < 20:
        d3 = 4
    elif ratio < 30:
        d3 = 3
    else:
        d3 = 2
    # Tokens govern context cost; line count is a proxy that long lines defeat
    # (478 lines / ~19k tokens once scored 5/5 here).
    approx_tokens = len(content) / 4
    if approx_tokens > 5000:
        d3 = max(1, d3 - 2)
    elif approx_tokens > 3500:
        d3 = max(1, d3 - 1)
    scores["D3"] = d3

    # ── D4: Structure ──
    d4 = 3
    if has_refs:
        d4 += 1
    if "when to read" in content.lower():
        d4 += 1
    if len(content) / 4 < 5000:
        d4 = min(5, d4 + 1)
    else:
        d4 = max(1, d4 - 1)          # over the token budget IS a structure failure
    scores["D4"] = min(5, d4)

    # ── D5: Instruction clarity ──
    d5 = 3
    if "## pipeline" in content.lower() or "## workflow" in content.lower():
        d5 += 1
    if "## when to use" in content.lower():
        d5 += 1
    if "example" in content.lower():
        d5 = min(5, d5 + 1)
    scores["D5"] = min(5, d5)

    # ── D6: Freedom calibration ──
    d6 = 4
    content_lower = content.lower()
    if "why" in content_lower or "because" in content_lower:
        d6 += 1
    if "default" in content_lower or "override" in content_lower:
        d6 = min(5, d6)
    scores["D6"] = min(5, d6)

    # ── D7: Error handling ──
    d7 = 3
    if "gotcha" in content.lower() or "pitfall" in content.lower():
        d7 += 1
    if "error" in content.lower() and "handling" in content.lower():
        d7 += 1
    scores["D7"] = min(5, d7)

    # ── D8: Correctness & Safety (was a second copy of D4) ──
    # D4 and D8 both scored progressive disclosure — 20% of the total on one
    # property, and nothing at all on whether the skill works or is safe.
    d8, correctness_findings = check_correctness(skill_dir)
    # A SKILL.md promising docs that do not exist is a correctness defect:
    # the agent following the pointer finds nothing. Cap the penalty so a
    # doc problem cannot dominate the safety signal in this dimension.
    # Invalid frontmatter means the skill does not load at all -- a harder
    # failure than anything else measured here, so it is not a soft deduction.
    _fm = check_frontmatter_parses(skill_dir)
    if _fm:
        d8 = max(0, d8 - 2)
        correctness_findings.extend(_fm)
    _dead_refs = check_dead_references(skill_dir)
    if _dead_refs:
        d8 = max(0, d8 - min(2, len(_dead_refs)))
        correctness_findings.append(
            "dead reference%s (%d): %s" % ("" if len(_dead_refs) == 1 else "s",
                                           len(_dead_refs), ", ".join(_dead_refs[:3])))
    scores["D8"] = d8

    # ── D9: Scripts quality (EXECUTED, not inferred) ──
    script_dir = os.path.join(skill_dir, "scripts")
    _ok, broken_help, _n = check_scripts_help(script_dir, execute=EXECUTE_CHECKS)
    if _n == 0 or not broken_help:
        scores["D9"] = 5
    elif len(broken_help) < _n / 2:
        scores["D9"] = 3
    else:
        scores["D9"] = 1

    # ── D10: Completeness ──
    d10 = 3
    if "gotcha" in content.lower() or "pitfall" in content.lower():
        d10 += 1
    if "when not to use" in content.lower():
        d10 += 1
    scores["D10"] = min(5, d10)

    total_score = sum(scores.values())
    return {
        "skill": skill_name,
        "path": skill_path,
        "total": total_score,
        "dimensions": scores,
        "line_count": total_lines,
        "approx_tokens": int(len(content) / 4),
        "scripts_failing_help": broken_help,
        "correctness_findings": correctness_findings,
        "code_ratio": round(ratio, 1),
        "scored_at": datetime.now(timezone.utc).isoformat(),
    }


def run_full_assessment(skills_dir: str = None, all_profiles: bool = False) -> list:
    """Score all ocas-* / util-* skills and return sorted list (lowest first)."""
    skills = find_all_skills(skills_dir, all_profiles)
    results = []
    for name, path in skills:
        result = score_skill(name, path)
        results.append(result)
    results.sort(key=lambda r: r["total"])
    return results


def generate_report(assessment: list, state: dict) -> str:
    """Generate a text report of current library state."""
    lines = [
        f"# 10khr Report — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"",
        f"Skills assessed: {len(assessment)}",
        f"Skills improved this session: {state.get('skills_improved', 0)}",
        f"Total iterations: {state.get('total_iterations', 0)}",
        f"",
        f"| Rank | Skill | Score | Band |",
        f"|------|-------|-------|------|",
    ]
    for i, r in enumerate(assessment, 1):
        band = "A" if r["total"] >= 40 else "B" if r["total"] >= 30 else "C"
        marker = " ← current target" if r["skill"] == state.get("current_target") else ""
        lines.append(f"| {i} | {r['skill']} | {r['total']}/50 | {band} |{marker}")

    below_target = [r for r in assessment if r["total"] < TARGET_SCORE]
    lines.extend([
        f"",
        f"Skills below {TARGET_SCORE}/50: {len(below_target)}",
    ])
    if state.get("current_target"):
        lines.append(f"Current grinding target: {state['current_target']}")

    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────


def main():
    import argparse
    parser = argparse.ArgumentParser(description="10khr skill improvement engine")
    parser.add_argument("--skills-dir", default=None,
                        help="Path to skills directory (default: active profile)")
    parser.add_argument("--all-profiles", action="store_true",
                        help="Scan all profiles under ~/.hermes/profiles/")
    parser.add_argument("--report-only", action="store_true",
                        help="Only assess, don't output grinding target")
    args = parser.parse_args()

    report_only = args.report_only
    skills_dir = args.skills_dir
    all_profiles = args.all_profiles
    state = load_state()

    if not state.get("started_at"):
        state["started_at"] = datetime.now(timezone.utc).isoformat()

    # Step 1: Full assessment
    assessment = run_full_assessment(skills_dir, all_profiles)
    state["last_run"] = datetime.now(timezone.utc).isoformat()

    # Step 2: Find lowest-scoring skill below target
    below_target = [r for r in assessment if r["total"] < TARGET_SCORE]

    if not below_target:
        print("All ocas-* / util-* skills are at 50/50. Nothing to grind.")
        print(generate_report(assessment, state))
        save_state(state)
        return

    # Pick the lowest
    target = below_target[0]
    state["current_target"] = target["skill"]

    if report_only:
        print(generate_report(assessment, state))
        save_state(state)
        return

    # Step 3: Output the target for the agent to work on
    print(f"TARGET: {target['skill']} ({target['total']}/50)")
    print(f"PATH: {target['path']}")
    print(f"DIMENSIONS: {json.dumps(target['dimensions'], indent=2)}")
    print(f"\n--- FULL ASSESSMENT ---")
    print(generate_report(assessment, state))

    # Check if we need a re-assessment (every 5 skills)
    improved = state.get("skills_improved", 0)
    if improved > 0 and improved % REASSESS_INTERVAL == 0:
        print(f"\n*** RE-ASSESSMENT TRIGGERED ({improved} skills improved) ***")
        print("Re-running full library assessment before continuing...")

    save_state(state)


if __name__ == "__main__":
    main()