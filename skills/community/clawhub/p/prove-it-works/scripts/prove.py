#!/usr/bin/env python3
"""Prove It Works: run the project's real checks and inspect the change before saying "done".

Usage:
  python3 prove.py <repo> [--base REF] [--task-file F | --task TEXT]
                   [--only tests,build,typecheck,lint,rules] [--timeout SECS]
                   [--json] [--ledger] [--hook]

1. Works out the change: uncommitted work vs HEAD; on a clean tree, the branch
   vs its merge-base with the default branch (or the last commit); or --base.
2. Detects the project's real commands (package.json scripts with the right
   package manager, Makefile targets, pyproject task tables, pytest/unittest,
   ruff/flake8/mypy, cargo, go) and runs each with a timeout, offline, in the
   repo folder. Missing dependencies mean NOT RUN, never PASS.
3. Inspects the change for the quiet ways "done" is not done (causes 5-17).
4. Checks the written project rules and the Never Twice rules.

First line: "PROVEN: all N checks passed, no problems in the change" or
"NOT DONE: X failing checks, Y problems in the change".

Read-only on the repo except <repo>/.shipsnag/ (ledger). The project's own
commands may write their usual outputs (build folders, caches); the change is
read before any command runs. Standard library only.
"""

import argparse
import json
import os
import re
import shlex
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (JS_LOCKS, needs_shell, split_cmd, UNSAFE_NAME_RE, auto_command_unsafe, base_of, command_is_safe, ext_of,  # noqa: E402
                    finding, install_signal_handlers, is_dirty, load_change, load_json_text,
                    load_toml, no_em_dash, posix, python_exe, read_text, redact_text, repo_root, resolve_exe,
                    run_cmd, run_git, set_deadline, tail, time_left, write_ledger, dec)

KINDS = ("test", "build", "typecheck", "lint")
KIND_CAUSE = {"test": 1, "build": 2, "typecheck": 3, "lint": 4, "rule": 8}
KIND_LABEL = {"test": "tests", "build": "build", "typecheck": "typecheck", "lint": "lint", "rule": "required by a rule"}
ONLY_ALIASES = {"test": "test", "tests": "test", "build": "build", "typecheck": "typecheck", "types": "typecheck",
                "type": "typecheck", "tsc": "typecheck", "lint": "lint", "rules": "rule", "rule": "rule"}

NODE_SCRIPT_NAMES = {
    "test": ["test", "test:unit", "test:all", "tests"],
    "build": ["build", "compile"],
    "typecheck": ["typecheck", "type-check", "check-types", "types", "tsc", "check:types", "types:check", "typecheck:all", "lint:types"],
    "lint": ["lint", "lint:all", "eslint", "lint:js", "lint:check"],
}
MAKE_TARGETS = {
    "test": ["test", "tests", "unit", "test-unit"],
    "build": ["build", "compile"],
    "typecheck": ["typecheck", "type-check", "types", "mypy", "check-types", "tsc"],
    "lint": ["lint", "lint-check", "check-lint", "flake8", "ruff"],
}
PY_TASK_NAMES = {
    "test": ["test", "tests", "unit"],
    "build": ["build"],
    "typecheck": ["typecheck", "type-check", "types", "mypy"],
    "lint": ["lint", "check-lint", "ruff", "flake8"],
}
SHELL_BUILTINS = {"echo", "exit", "true", "false", "cd", "sh", "bash", "cat", "mkdir", "cp", "mv", "rm", "test",
                  "[", "env", "set", "export", "sleep", "printf", "node", "npm", "pnpm", "yarn", "bun", "npx",
                  "python", "python3", "make", "exec", "if", "then", "fi", "for", "do", "done", "while", "time",
                  "touch", "ls", "find", "grep", "sed", "awk", "xargs", "tee", "rimraf", "del", "deno"}
NPM_DEFAULT_TEST = re.compile(r"no test specified", re.I)
CANT_SEE = [
    "CI-only differences: another Node or Python version, missing secrets or services in CI, OS differences (cause 18). Compare the versions in your CI config with the ones used here.",
    "Flaky tests, or tests that depend on time, network or order (cause 19). One green run is not proof they are stable; rerun anything that failed once.",
    "Anything only a human or a browser can judge: visual layout, real user flows, copy, UX (cause 20). Say what still needs a look by hand.",
    "Whether the change does what the task meant, beyond the names and files the task mentions (cause 15). Claude's review pass covers this.",
]


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

def _check(kind, name, cmd, source, cwd, shell=False, status=None, reason=None):
    if isinstance(cmd, list):
        display = " ".join(shlex.quote(c) if re.search(r"\s", c) else c for c in cmd)
    else:
        display = cmd
    return {"kind": kind, "name": name, "cmd": cmd, "display": display, "shell": shell, "source": source,
            "cwd": cwd, "status": status, "reason": reason, "exit": None, "seconds": 0.0, "tail": [],
            "counts": {}, "required_by": [], "failed_tests": [], "excerpt": [], "inferred": False}


def detect_pm(d, pkg, rules):
    pm_field = (pkg or {}).get("packageManager") if isinstance(pkg, dict) else None
    if isinstance(pm_field, str) and pm_field:
        name = pm_field.split("@")[0].strip()
        if name in ("npm", "pnpm", "yarn", "bun"):
            return name, "packageManager field"
    for lk, pm in (("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lockb", "bun"), ("bun.lock", "bun"),
                   ("package-lock.json", "npm"), ("npm-shrinkwrap.json", "npm")):
        if os.path.exists(os.path.join(d, lk)):
            return pm, lk
    for r in rules or []:
        if r["kind"] == "pm" and r.get("pm"):
            return r["pm"], r["source"]
    return "npm", "default (no lockfile)"


def _script_bins(script, scripts, depth=0):
    """Executables a package.json script needs, plus scripts it calls."""
    bins = []
    if depth > 3 or not script:
        return bins
    for seg in re.split(r"&&|\|\||;|\|", script):
        try:
            toks = shlex.split(seg.strip())
        except ValueError:
            toks = seg.split()
        while toks and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[0]):
            toks = toks[1:]
        if not toks:
            continue
        t0 = toks[0]
        if t0 in ("cross-env", "dotenv", "env-cmd", "run-s", "run-p", "npm-run-all", "concurrently"):
            bins.append(t0)
            rest = [t for t in toks[1:] if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t) and not t.startswith("-")]
            if t0 in ("cross-env", "dotenv", "env-cmd") and rest:
                bins.append(rest[0])
            continue
        if t0 in ("npm", "pnpm", "yarn", "bun"):
            rest = [t for t in toks[1:] if not t.startswith("-")]
            if rest and rest[0] in ("run", "run-script") and len(rest) > 1:
                bins += _script_bins(scripts.get(rest[1], ""), scripts, depth + 1)
            elif rest and rest[0] in ("exec", "x", "dlx") and len(rest) > 1:
                bins.append(rest[1])
            elif rest and rest[0] in scripts:
                bins += _script_bins(scripts.get(rest[0], ""), scripts, depth + 1)
            elif rest and rest[0] == "test" and "test" in scripts:
                bins += _script_bins(scripts.get("test", ""), scripts, depth + 1)
            continue
        if t0 == "npx":
            rest = [t for t in toks[1:] if not t.startswith("-")]
            if rest:
                bins.append("npx:" + rest[0])
            continue
        if t0 not in SHELL_BUILTINS and not t0.startswith((".", "/", "$")):
            bins.append(t0)
    return bins


KNOWN_NODE_BINS = {
    "tsc", "eslint", "prettier", "biome", "jest", "vitest", "mocha", "ava", "next", "vite", "webpack", "rollup", "esbuild",
    "tsup", "tsx", "ts-node", "playwright", "cypress", "turbo", "nx", "lerna", "svelte-check", "svelte-kit", "vue-tsc",
    "astro", "remix", "nuxt", "nuxi", "ng", "react-scripts", "prisma", "drizzle-kit", "oxlint", "standard", "xo",
    "stylelint", "c8", "nyc", "concurrently", "run-s", "run-p", "npm-run-all", "cross-env", "rimraf", "wrangler", "expo",
    "react-native", "tap", "uvu", "karma", "jasmine", "nodemon", "husky", "lint-staged", "knip", "typedoc", "changeset",
    "vitepress", "docusaurus", "storybook", "sb", "eleventy", "gatsby", "parcel", "dotenv", "env-cmd", "tsc-alias",
    "tailwindcss", "postcss", "babel", "swc", "rspack", "microbundle", "ncc", "pkgroll", "unbuild", "vue-cli-service",
    "electron", "electron-builder", "detox", "openapi-typescript", "graphql-codegen", "eslint_d", "dprint", "rome",
    "type-coverage", "attw", "publint", "size-limit", "commitlint", "semantic-release", "svelte-package", "solid-start"}
SYSTEM_BINS = {"node", "sh", "bash", "python", "python3", "make", "go", "cargo", "deno", "bun", "git", "npm", "pnpm",
               "yarn", "npx", "ruby", "php", "java", "dotnet", "true", "false", "test", "uv", "poetry"}


def _has_node_modules(d, stop):
    cur = os.path.abspath(d)
    stop = os.path.abspath(stop)
    for _ in range(8):
        if os.path.isdir(os.path.join(cur, "node_modules")):
            return True
        if cur == stop or os.path.dirname(cur) == cur:
            break
        cur = os.path.dirname(cur)
    return False


def _node_bin_found(name, d, declared):
    """A package binary counts only when it is installed locally (node_modules/.bin): a global
    eslint, tsc or prettier is a different version and its result is not the project's result."""
    exe = resolve_exe(name, d)
    if not exe:
        return None
    if name in SYSTEM_BINS:
        return exe
    if "node_modules" in exe.replace("\\", "/"):
        return exe
    if name in KNOWN_NODE_BINS or name in declared:
        return None
    return exe


def node_checks(d, rel, rules):
    pkg_txt = read_text(os.path.join(d, "package.json"))
    pkg = load_json_text(pkg_txt or "")
    if not isinstance(pkg, dict):
        return {}, []
    notes = []
    scripts = pkg.get("scripts") if isinstance(pkg.get("scripts"), dict) else {}
    pm, pm_src = detect_pm(d, pkg, rules)
    pm_exe = resolve_exe(pm, d)
    declared = set()
    for sec in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        if isinstance(pkg.get(sec), dict):
            declared |= set(pkg[sec].keys())
    out = {}

    def missing_bins(body):
        miss = []
        for b in _script_bins(body, scripts):
            bn = b[4:] if b.startswith("npx:") else b
            if not _node_bin_found(bn, d, declared) and bn not in miss:
                miss.append(bn)
        return miss
    for kind, names in NODE_SCRIPT_NAMES.items():
        name = next((n for n in names if n in scripts and isinstance(scripts[n], str)), None)
        if not name:
            continue
        if kind == "test" and NPM_DEFAULT_TEST.search(scripts[name]):
            continue
        cmd_display = [pm, "run", name]
        src = "%spackage.json scripts.%s; %s, from %s" % (rel + "/" if rel else "", name, pm, pm_src)
        c = _check(kind, name, [pm_exe or pm, "run", name], src, d)
        c["display"] = " ".join(cmd_display)
        unsafe = auto_command_unsafe(_expand_scripts(scripts[name], scripts))
        if unsafe:
            c["status"], c["reason"] = "NOT RUN", "not run automatically: %s. Run it yourself if it is safe" % unsafe
        elif not pm_exe:
            c["status"], c["reason"] = "NOT RUN", "%s is not installed on this machine (the project uses it: %s)" % (pm, pm_src)
        else:
            missing = missing_bins(scripts[name])
            if missing:
                c["status"] = "NOT RUN"
                c["reason"] = "needs %s, which %s not installed here (no node_modules/.bin entry; a global copy is not the project's version). Run `%s install`, then prove again" % (
                    ", ".join("`%s`" % m for m in missing[:3]), "is" if len(missing) == 1 else "are", pm)
        out.setdefault(kind, []).append(c)
    # scripts with other names, classified by what they run
    for kind, rx in (("typecheck", r"\b(tsc|vue-tsc|svelte-check|mypy|pyright|flow)\b|typecheck|type-check"),
                     ("lint", r"\b(eslint|biome|oxlint|standard|xo|ruff|flake8|pylint|stylelint)\b"),
                     ("test", r"\b(jest|vitest|mocha|ava|tap|node --test|pytest|unittest)\b"),
                     ("build", r"\b(vite build|webpack|rollup|esbuild|tsup|parcel build|next build|tsc -b|tsc --build)\b")):
        if kind in out:
            continue
        for name in sorted(scripts):
            v = scripts[name]
            if not isinstance(v, str) or re.search(r"watch|--watch|\bdev\b|serve|start|fix|format|prepare|install|pre|post", name) or "--watch" in v:
                continue
            if UNSAFE_NAME_RE.search(name) or auto_command_unsafe(_expand_scripts(v, scripts)):
                if re.search(rx, v):
                    notes.append("%spackage.json scripts.%s runs %s checks but was not run automatically: %s." % (
                        rel + "/" if rel else "", name, kind, auto_command_unsafe(_expand_scripts(v, scripts), name)))
                continue
            if re.search(rx, v):
                pm_exe2 = pm_exe
                c = _check(kind, name, [pm_exe2 or pm, "run", name], "%spackage.json scripts.%s (runs %s)" % (rel + "/" if rel else "", name, kind), d)
                c["display"] = "%s run %s" % (pm, name)
                if not pm_exe2:
                    c["status"], c["reason"] = "NOT RUN", "%s is not installed on this machine" % pm
                else:
                    miss = missing_bins(v)
                    if miss:
                        c["status"] = "NOT RUN"
                        c["reason"] = "needs %s, which is not installed here (no node_modules/.bin entry). Run `%s install`, then prove again" % (", ".join("`%s`" % m for m in miss[:3]), pm)
                out[kind] = [c]
                break
    # typecheck / lint without scripts but with config and a local binary
    if "typecheck" not in out and os.path.exists(os.path.join(d, "tsconfig.json")):
        tsc = resolve_exe("tsc", d)
        local = tsc and "node_modules" in tsc
        c = _check("typecheck", "tsc", [tsc or "tsc", "--noEmit"], "%stsconfig.json (no typecheck script)" % (rel + "/" if rel else ""), d)
        c["display"] = "tsc --noEmit"
        c["inferred"] = True
        if not local:
            c["status"], c["reason"] = "NOT RUN", "tsconfig.json exists but TypeScript is not installed locally. Run `%s install`, then prove again" % pm
        out["typecheck"] = [c]
    if "lint" not in out:
        cfg = [f for f in os.listdir(d) if re.match(r"^(\.eslintrc(\.\w+)?|eslint\.config\.\w+)$", f)]
        if cfg:
            es = resolve_exe("eslint", d)
            if es and "node_modules" in es:
                c = _check("lint", "eslint", [es, "."], "%s%s (no lint script)" % (rel + "/" if rel else "", cfg[0]), d)
                c["display"] = "eslint ."
                c["inferred"] = True
                out["lint"] = [c]
            else:
                notes.append("%s exists but there is no lint script and ESLint is not installed locally, so lint was not run." % cfg[0])
    return out, notes


def _expand_scripts(body, scripts, depth=0):
    """A package.json script body with `npm run x` / `pnpm x` calls replaced by their bodies."""
    if depth > 4 or not isinstance(body, str):
        return body or ""
    parts = []
    for seg in re.split(r"(&&|\|\||;)", body):
        st = seg.strip()
        toks = st.split()
        if toks and toks[0] in ("npm", "pnpm", "yarn", "bun"):
            rest = [t for t in toks[1:] if not t.startswith("-")]
            name = rest[1] if rest and rest[0] in ("run", "run-script") and len(rest) > 1 else (rest[0] if rest else None)
            if name in scripts and isinstance(scripts[name], str):
                parts.append(" " + _expand_scripts(scripts[name], scripts, depth + 1) + " ")
                continue
        parts.append(seg)
    return "".join(parts)


def make_targets(d):
    txt = None
    for name in ("Makefile", "makefile", "GNUmakefile"):
        p = os.path.join(d, name)
        if os.path.isfile(p):
            txt = read_text(p)
            break
    if not txt:
        return {}
    targets = set(m.group(1) for m in re.finditer(r"^([A-Za-z0-9_.\-]+)\s*:(?!=)", txt, re.M))
    out = {}
    for kind, names in MAKE_TARGETS.items():
        t = next((n for n in names if n in targets), None)
        if t:
            out[kind] = t
    # other targets, classified by their recipe
    recipes = {}
    cur = None
    for line in txt.splitlines():
        m = re.match(r"^([A-Za-z0-9_.\-]+)\s*:(?!=)", line)
        if m:
            cur = m.group(1)
            recipes[cur] = ""
        elif cur and line.startswith("\t"):
            recipes[cur] += line + "\n"
        elif line.strip() and not line.startswith("#"):
            cur = None
    for kind, _ in KIND_WORDS:
        if kind in out:
            continue
        for t in sorted(recipes):
            if t.startswith(".") or re.search(r"install|clean|deploy|release|publish|watch|dev|serve|run|start|fmt|format|fix|all", t) or \
                    UNSAFE_NAME_RE.search(t):
                continue
            if _kind_of(recipes[t]) == kind and _kind_of(t) in (kind, None):
                out[kind] = t
                break
    return out


def _py_cmd(cmdline, d):
    """Run a declared Python task command; swap a missing `python` for the current interpreter."""
    try:
        toks = shlex.split(cmdline)
    except ValueError:
        return cmdline, True
    if re.search(r"&&|\|\||[;|<>]", cmdline):
        return cmdline, True
    if toks and toks[0] in ("python", "python3", "py") and not resolve_exe(toks[0], d):
        toks[0] = python_exe(d)
    elif toks:
        exe = resolve_exe(toks[0], d)
        if exe:
            toks[0] = exe
    return toks, False


def _pytest_style(d, tdir):
    """Plain test functions or pytest imports: unittest discovery would find nothing."""
    paths = []
    for base in ([os.path.join(d, tdir)] if tdir else []) + [d]:
        try:
            for f in sorted(os.listdir(base)):
                if re.match(r"^test_.*\.py$|.*_test\.py$", f):
                    paths.append(os.path.join(base, f))
        except OSError:
            pass
    for p in paths[:20]:
        txt = read_text(p) or ""
        if re.search(r"^\s*import pytest|^\s*from pytest\b|@pytest\.", txt, re.M):
            return True
        if re.search(r"^def test_\w*\(", txt, re.M) and not re.search(r"TestCase\b", txt):
            return True
    return False


def _importable(py, mod, d):
    r = run_cmd([py, "-c", "import %s" % mod], d, 30)
    return r["exit"] == 0


def python_checks(d, rel):
    files = set(os.listdir(d))
    is_py = bool(files & {"pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "tox.ini", "noxfile.py",
                          "pytest.ini", "Pipfile", "conftest.py", "manage.py"})
    if not is_py:
        has_tests = any(re.match(r"^test_.*\.py$|.*_test\.py$", f) for f in files) or any(
            os.path.isdir(os.path.join(d, t)) and any(re.match(r"^test_.*\.py$|.*_test\.py$", x) for x in os.listdir(os.path.join(d, t)))
            for t in ("tests", "test"))
        if not has_tests:
            return {}, []
    notes = []
    pre = (rel + "/") if rel else ""
    py = python_exe(d)
    pyproject = load_toml(read_text(os.path.join(d, "pyproject.toml")) or "") if "pyproject.toml" in files else {}
    tool = pyproject.get("tool") or {}
    setup_cfg = read_text(os.path.join(d, "setup.cfg")) or "" if "setup.cfg" in files else ""
    tox = read_text(os.path.join(d, "tox.ini")) or "" if "tox.ini" in files else ""
    reqs = ""
    for f in files:
        if re.match(r"^requirements.*\.(txt|in)$", f):
            reqs += (read_text(os.path.join(d, f)) or "") + "\n"
    out = {}
    # 1. declared task tables
    tables = []
    for key, sub in (("poe", "tasks"), ("taskipy", "tasks"), ("pdm", "scripts"), ("rye", "scripts")):
        t = (tool.get(key) or {}).get(sub) if isinstance(tool.get(key), dict) else None
        if isinstance(t, dict):
            tables.append(("[tool.%s.%s]" % (key, sub), t))
    hatch = (((tool.get("hatch") or {}).get("envs") or {}).get("default") or {}).get("scripts") if isinstance(tool.get("hatch"), dict) else None
    if isinstance(hatch, dict):
        tables.append(("[tool.hatch.envs.default.scripts]", hatch))
    for src, table in tables:
        for kind, names in PY_TASK_NAMES.items():
            if kind in out:
                continue
            n = next((x for x in names if x in table), None)
            if not n:
                continue
            v = table[n]
            if isinstance(v, dict):
                v = v.get("cmd") or v.get("shell") or v.get("call")
            if isinstance(v, list):
                v = " && ".join(x for x in v if isinstance(x, str))
            if not isinstance(v, str) or not v.strip():
                continue
            cmd, shell = _py_cmd(v, d)
            c = _check(kind, n, cmd, "%spyproject.toml %s %s" % (pre, src, n), d, shell=shell)
            c["display"] = v
            unsafe = auto_command_unsafe(v)
            if unsafe:
                c["status"], c["reason"] = "NOT RUN", "not run automatically: %s" % unsafe
            out[kind] = [c]
    # 2. test runner
    if "test" not in out:
        pytest_cfg = "pytest.ini" in files or "conftest.py" in files or "pytest" in (tool.get("pytest") or {}) or \
            "ini_options" in (tool.get("pytest") or {}) or "[tool:pytest]" in setup_cfg or "[pytest]" in tox or \
            re.search(r"(?im)^\s*pytest\b", reqs) or "pytest" in json.dumps(pyproject.get("project") or {}) or \
            "pytest" in json.dumps(tool.get("poetry") or {}) or re.search(r"(?m)^\s*commands\s*=.*\bpytest\b", tox)
        tdir = next((t for t in ("tests", "test") if os.path.isdir(os.path.join(d, t))), None)
        if not pytest_cfg:
            pytest_cfg = _pytest_style(d, tdir)
        if pytest_cfg:
            if _importable(py, "pytest", d):
                c = _check("test", "pytest", [py, "-m", "pytest", "-q"], "%spytest config" % pre, d)
                c["display"] = "python -m pytest -q"
            else:
                exe = resolve_exe("pytest", d)
                c = _check("test", "pytest", [exe or "pytest", "-q"], "%spytest config" % pre, d)
                c["display"] = "pytest -q"
                c["env"] = {"PYTHONPATH": d + os.pathsep + os.environ.get("PYTHONPATH", "")}
                if not exe:
                    c["status"], c["reason"] = "NOT RUN", "the tests are written for pytest, but pytest is not installed in this environment. Install the dev dependencies, then prove again"
            c["inferred"] = True
            out["test"] = [c]
        else:
            start = tdir or "."
            pat = "test*.py"
            look = os.listdir(os.path.join(d, start)) if os.path.isdir(os.path.join(d, start)) else []
            if not any(re.match(r"^test.*\.py$", f) for f in look) and any(f.endswith("_test.py") for f in look):
                pat = "*_test.py"
            if any(re.match(r"^test.*\.py$|.*_test\.py$", f) for f in look):
                cmd = [py, "-m", "unittest", "discover", "-s", start, "-p", pat]
                if start == ".":
                    cmd = [py, "-m", "unittest", "discover", "-p", pat]
                c = _check("test", "unittest", cmd, "%s%s (stdlib unittest discovery)" % (pre, start + "/" if start != "." else "test files"), d)
                c["display"] = "python -m unittest discover%s -p \"%s\"" % ((" -s " + start) if start != "." else "", pat)
                c["inferred"] = True
                out["test"] = [c]
    # 3. lint and typecheck tools by config
    def tool_check(kind, mod, args, display, src):
        if _importable(py, mod, d):
            c = _check(kind, mod, [py, "-m", mod] + args, src, d)
        else:
            exe = resolve_exe(mod, d)
            c = _check(kind, mod, [exe or mod] + args, src, d)
            if not exe:
                c["status"], c["reason"] = "NOT RUN", "the project is configured for %s, but it is not installed in this environment" % mod
        c["display"] = display
        c["inferred"] = True
        return c
    if "lint" not in out:
        if "ruff" in tool or "ruff.toml" in files or ".ruff.toml" in files:
            out["lint"] = [tool_check("lint", "ruff", ["check", "."], "ruff check .", "%sruff config" % pre)]
        elif ".flake8" in files or "[flake8]" in setup_cfg or "[flake8]" in tox:
            out["lint"] = [tool_check("lint", "flake8", [], "flake8", "%sflake8 config" % pre)]
    if "typecheck" not in out:
        if "mypy" in tool or "mypy.ini" in files or ".mypy.ini" in files or "[mypy]" in setup_cfg:
            out["typecheck"] = [tool_check("typecheck", "mypy", ["."], "mypy .", "%smypy config" % pre)]
        elif "pyright" in tool or "pyrightconfig.json" in files:
            out["typecheck"] = [tool_check("typecheck", "pyright", [], "pyright", "%spyright config" % pre)]
    if "tox.ini" in files or "noxfile.py" in files:
        notes.append("%s found: its environments were not created (that would install packages); the matching tools were run directly in this environment instead." % ("tox.ini" if "tox.ini" in files else "noxfile.py"))
    return out, notes


def cargo_go_checks(d, rel):
    out = {}
    pre = (rel + "/") if rel else ""
    if os.path.isfile(os.path.join(d, "Cargo.toml")):
        exe = resolve_exe("cargo", d)
        for kind, args in (("test", ["test", "--offline"]), ("build", ["build", "--offline"]), ("lint", ["clippy", "--offline"])):
            c = _check(kind, "cargo " + args[0], [exe or "cargo"] + args, "%sCargo.toml" % pre, d)
            c["display"] = "cargo " + " ".join(args)
            if not exe:
                c["status"], c["reason"] = "NOT RUN", "cargo is not installed"
            out[kind] = [c]
    if os.path.isfile(os.path.join(d, "go.mod")):
        exe = resolve_exe("go", d)
        for kind, args in (("test", ["test", "./..."]), ("build", ["build", "./..."]), ("lint", ["vet", "./..."])):
            c = _check(kind, "go " + args[0], [exe or "go"] + args, "%sgo.mod" % pre, d)
            c["display"] = "go " + " ".join(args)
            if not exe:
                c["status"], c["reason"] = "NOT RUN", "go is not installed"
            out.setdefault(kind, []).append(c)
    return out


def other_checks(d, rel):
    """Maven, Gradle, Ruby, PHP, .NET and Deno: the standard test command, offline, when the tool
    is installed; NOT RUN with the install hint when it is not."""
    out = {}
    pre = (rel + "/") if rel else ""
    files = set(os.listdir(d)) if os.path.isdir(d) else set()

    def add(kind, name, cmd, display, src, tool, hint):
        exe = cmd[0] if os.path.isabs(cmd[0]) or cmd[0].startswith("./") else resolve_exe(cmd[0], d)
        if cmd[0].startswith("./") and not os.path.isfile(os.path.join(d, cmd[0][2:])):
            exe = None
        c = _check(kind, name, ([exe] + cmd[1:]) if exe and not cmd[0].startswith("./") else cmd, src, d)
        c["display"] = display
        if not exe:
            c["status"], c["reason"] = "NOT RUN", "%s is not installed on this machine. %s" % (tool, hint)
        out.setdefault(kind, []).append(c)
    if "pom.xml" in files:
        if "mvnw" in files:
            add("test", "mvnw test", ["./mvnw", "-o", "-q", "test"], "./mvnw -o -q test", pre + "pom.xml (Maven wrapper)", "the Maven wrapper", "")
        else:
            add("test", "mvn test", ["mvn", "-o", "-q", "test"], "mvn -o -q test", pre + "pom.xml", "Maven (mvn)", "Install Maven or add the Maven wrapper (mvnw).")
    elif files & {"build.gradle", "build.gradle.kts"}:
        if "gradlew" in files:
            add("test", "gradlew test", ["./gradlew", "test", "--offline", "-q"], "./gradlew test --offline -q", pre + "build.gradle (Gradle wrapper)", "the Gradle wrapper", "")
        else:
            add("test", "gradle test", ["gradle", "test", "--offline", "-q"], "gradle test --offline -q", pre + "build.gradle", "Gradle", "Install Gradle or add the Gradle wrapper (gradlew).")
    if "Gemfile" in files:
        if os.path.isdir(os.path.join(d, "spec")):
            add("test", "rspec", ["bundle", "exec", "rspec"], "bundle exec rspec", pre + "Gemfile + spec/", "Bundler", "Install Ruby and Bundler, run `bundle install`.")
        elif "Rakefile" in files or os.path.isdir(os.path.join(d, "test")):
            add("test", "rake test", ["bundle", "exec", "rake", "test"], "bundle exec rake test", pre + "Gemfile + Rakefile", "Bundler", "Install Ruby and Bundler, run `bundle install`.")
        if ".rubocop.yml" in files:
            add("lint", "rubocop", ["bundle", "exec", "rubocop"], "bundle exec rubocop", pre + ".rubocop.yml", "Bundler", "Run `bundle install`.")
    if "composer.json" in files:
        cj = load_json_text(read_text(os.path.join(d, "composer.json")) or "") or {}
        scr = cj.get("scripts") if isinstance(cj, dict) and isinstance(cj.get("scripts"), dict) else {}
        body = scr.get("test")
        body = " && ".join(x for x in body if isinstance(x, str)) if isinstance(body, list) else body
        if isinstance(body, str) and body.strip():
            unsafe = auto_command_unsafe(body)
            add("test", "composer test", ["composer", "test"], "composer test", pre + "composer.json scripts.test", "Composer", "Install PHP and Composer, run `composer install`.")
            if unsafe:
                out["test"][-1]["status"], out["test"][-1]["reason"] = "NOT RUN", "not run automatically: %s" % unsafe
        elif os.path.isfile(os.path.join(d, "vendor", "bin", "phpunit")):
            add("test", "phpunit", [os.path.join(d, "vendor", "bin", "phpunit")], "vendor/bin/phpunit", pre + "phpunit (vendor/bin)", "PHPUnit", "")
        elif files & {"phpunit.xml", "phpunit.xml.dist"}:
            add("test", "phpunit", ["phpunit"], "phpunit", pre + "phpunit.xml", "PHPUnit", "Run `composer install`.")
    if any(f.endswith((".sln", ".csproj", ".fsproj", ".vbproj")) for f in files):
        add("test", "dotnet test", ["dotnet", "test", "--no-restore"], "dotnet test --no-restore", pre + "*.csproj / *.sln", ".NET SDK (dotnet)", "Install the .NET SDK and run `dotnet restore`.")
    if files & {"deno.json", "deno.jsonc"}:
        dj = load_json_text(re.sub(r"(?m)^\s*//.*$", "", read_text(os.path.join(d, "deno.json" if "deno.json" in files else "deno.jsonc")) or "")) or {}
        tasks = dj.get("tasks") if isinstance(dj, dict) and isinstance(dj.get("tasks"), dict) else {}
        if isinstance(tasks.get("test"), str):
            add("test", "deno task test", ["deno", "task", "test"], "deno task test", pre + "deno.json tasks.test", "Deno", "Install Deno.")
            if auto_command_unsafe(tasks["test"]):
                out["test"][-1]["status"], out["test"][-1]["reason"] = "NOT RUN", "not run automatically: %s" % auto_command_unsafe(tasks["test"])
        else:
            add("test", "deno test", ["deno", "test"], "deno test", pre + "deno.json", "Deno", "Install Deno.")
        add("lint", "deno lint", ["deno", "lint"], "deno lint", pre + "deno.json", "Deno", "Install Deno.")
    return out


UNSUPPORTED_MARKERS = [("Swift", ("Package.swift",)), ("Elixir", ("mix.exs",)), ("Dart/Flutter", ("pubspec.yaml",)),
                       ("Terraform", (".tf",)), ("C/C++ (CMake)", ("CMakeLists.txt",)), ("Haskell", ("stack.yaml", ".cabal")),
                       ("Scala (sbt)", ("build.sbt",)), ("Zig", ("build.zig",)), ("Clojure", ("deps.edn", "project.clj"))]


def unsupported_stacks(repo):
    try:
        names = os.listdir(repo)
    except OSError:
        return []
    out = []
    for label, marks in UNSUPPORTED_MARKERS:
        if any((m in names) or (m.startswith(".") and any(n.endswith(m) for n in names)) for m in marks):
            out.append(label)
    return out


PROJECT_FILES = ("package.json", "pyproject.toml", "setup.py", "Cargo.toml", "go.mod", "Makefile", "requirements.txt",
                 "pom.xml", "build.gradle", "build.gradle.kts", "Gemfile", "composer.json", "deno.json", "deno.jsonc")
DOC_FILES = ("README.md", "README.rst", "README", "CONTRIBUTING.md", ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md",
             "CLAUDE.md", "AGENTS.md", "DEVELOPMENT.md", "HACKING.md")
DOC_RUNNERS = {"python", "python3", "node", "make", "pytest", "ruff", "mypy", "flake8", "pyright", "npm", "pnpm",
               "yarn", "bun", "cargo", "go", "deno", "tsc", "eslint", "uv", "poetry"}
KIND_WORDS = [("typecheck", r"typecheck|type-check|type_check|check_types|check-types|\bmypy\b|\btsc\b|pyright|\btypes\b"),
              ("lint", r"\blint|ruff|flake8|eslint|pylint|\bvet\b|clippy"),
              ("test", r"\btest|unittest|pytest|\bspec\b"),
              ("build", r"\bbuild\b|compile")]
CONVENTIONAL = {"test": ["scripts/test", "scripts/run_tests", "scripts/run-tests", "run_tests", "test"],
                "build": ["scripts/build", "tools/build", "build"],
                "typecheck": ["scripts/typecheck", "scripts/type_check", "scripts/type-check", "scripts/check_types",
                              "scripts/check-types", "scripts/types", "tools/typecheck", "typecheck", "type_check"],
                "lint": ["scripts/lint", "tools/lint", "lint"]}


def _kind_of(cmd):
    for kind, rx in KIND_WORDS:
        if re.search(rx, cmd, re.I):
            return kind
    return None


def documented_commands(d):
    """Check commands written in README / CONTRIBUTING / agent files (code blocks and inline code)."""
    found = {}
    for rel in DOC_FILES:
        txt = read_text(os.path.join(d, rel))
        if not txt:
            continue
        cands = []
        in_code = False
        for line in txt.splitlines():
            st = line.strip()
            if st.startswith(("```", "~~~")):
                in_code = not in_code
                continue
            if in_code:
                cands.append((rel, re.sub(r"^\$\s+", "", st)))
            else:
                cands += [(rel, m.strip()) for m in re.findall(r"`([^`\n]+)`", line)]
        for src, c in cands:
            c = c.split(" #")[0].strip()
            toks = c.split()
            if len(toks) < 2 or toks[0] not in DOC_RUNNERS or not command_is_safe(c):
                continue
            if re.search(r"\b(install|add|init|setup|dev|start|serve|watch|run_server|runserver|migrate|deploy|publish)\b", c):
                continue
            kind = _kind_of(c)
            if kind and kind not in found:
                found[kind] = (c, src)
    return found


def conventional_scripts(d):
    out = {}
    for kind, stems in CONVENTIONAL.items():
        for stem in stems:
            for ext, runner in ((".py", "python"), (".js", "node"), (".mjs", "node"), (".sh", "sh")):
                rel = stem + ext
                if os.path.isfile(os.path.join(d, rel)):
                    out[kind] = (rel, runner)
                    break
            if kind in out:
                break
    return out


def _cmd_check(kind, cmdline, src, d):
    if needs_shell(cmdline):
        c = _check(kind, cmdline.split()[0], cmdline, src, d, shell=needs_shell(cmdline))
    else:
        toks = shlex.split(cmdline)
        if toks[0] in ("python", "python3") and not resolve_exe(toks[0], d):
            toks[0] = python_exe(d)
        if toks[0] in ("python", "python3") and len(toks) >= 3 and toks[1] == "-m" and toks[2] in ("pytest", "mypy", "ruff", "flake8") \
                and not _importable(resolve_exe(toks[0], d) or python_exe(d), toks[2], d) and resolve_exe(toks[2], d):
            toks = toks[2:]
            pyenv = True
        else:
            pyenv = False
        exe = resolve_exe(toks[0], d) if toks[0] not in ("python", "python3") else (resolve_exe(toks[0], d) or python_exe(d))
        c = _check(kind, toks[0], [exe or toks[0]] + toks[1:], src, d)
        if pyenv:
            c["env"] = {"PYTHONPATH": d + os.pathsep + os.environ.get("PYTHONPATH", "")}
        if not exe:
            c["status"], c["reason"] = "NOT RUN", "`%s` is not installed on this machine" % toks[0]
    c["display"] = cmdline
    return c


def project_dirs(repo, change):
    dirs = [""]
    if change and change.ok:
        for f in change.files:
            parts = posix(f.path).split("/")[:-1]
            while parts:
                rel = "/".join(parts)
                if any(os.path.isfile(os.path.join(repo, rel, pf)) for pf in PROJECT_FILES):
                    if rel not in dirs and not any(seg in ("node_modules", "vendor") for seg in parts):
                        dirs.append(rel)
                    break
                parts.pop()
    return dirs[:MAX_PROJECT_DIRS], dirs[MAX_PROJECT_DIRS:]


MAX_PROJECT_DIRS = 6


def detect_checks(repo, change, rules):
    checks, notes = [], []
    dirs, dropped = project_dirs(repo, change)
    if dropped:
        notes.append("Monorepo: the change touches %d project folders; checks ran in %d (%s) and NOT in %s. Run the proof with "
                     "--only or inside those folders, or run the workspace's own test command." % (
                         len(dirs) + len(dropped), len(dirs), ", ".join(x or "." for x in dirs),
                         ", ".join(dropped[:8]) + (" and %d more" % (len(dropped) - 8) if len(dropped) > 8 else "") + " (not tested)"))
    for rel in dirs:
        d = os.path.join(repo, rel) if rel else repo
        mk = make_targets(d)
        node, n1 = node_checks(d, rel, rules)
        pyc, n2 = python_checks(d, rel)
        cg = cargo_go_checks(d, rel)
        for k, v in other_checks(d, rel).items():
            cg.setdefault(k, []).extend(v)
        notes += n1 + n2
        make_exe = resolve_exe("make", d)
        docs = documented_commands(d)
        conv = conventional_scripts(d)
        pre = rel + "/" if rel else ""
        for kind in KINDS:
            if kind in mk:
                c = _check(kind, mk[kind], [make_exe or "make", mk[kind]], "%sMakefile target %s" % (pre, mk[kind]), d)
                c["display"] = "make %s" % mk[kind]
                unsafe = auto_command_unsafe(expand_command(c))
                if unsafe:
                    c["status"], c["reason"] = "NOT RUN", "not run automatically: %s" % unsafe
                elif not make_exe:
                    c["status"], c["reason"] = "NOT RUN", "make is not installed on this machine"
                checks.append(c)
                continue
            cands = []
            for src in (node, pyc, cg):
                cands += src.get(kind, [])
            declared = [c for c in cands if not c["inferred"]]
            if declared:
                checks += declared
            elif kind in docs:
                checks.append(_cmd_check(kind, docs[kind][0], "%s%s (documented command)" % (pre, docs[kind][1]), d))
            elif cands:
                checks += cands
            elif kind in conv:
                path_, runner = conv[kind]
                c = _cmd_check(kind, "%s %s" % (runner, path_), "%s%s (conventional script, not declared anywhere)" % (pre, path_), d)
                body = read_text(os.path.join(d, path_)) or ""
                unsafe = auto_command_unsafe("\n".join(l for l in body.splitlines() if not l.strip().startswith("#"))) if runner == "sh" else \
                    (None if not re.search(r"\b(shutil\.rmtree|os\.remove|rmSync|unlinkSync|rmdirSync|requests\.(?:get|post|put|delete)|"
                                           r"fetch\(|urllib\.request|http\.client|https?\.request|git\s+push|npm\s+publish|deploy)", body) else
                     "the script deletes files, uses the network or deploys")
                if unsafe:
                    c["status"], c["reason"] = "NOT RUN", "not run automatically: %s" % unsafe
                checks.append(c)
    for c in checks:
        c["where"] = posix(os.path.relpath(c["cwd"], repo)) if c["cwd"] != repo else "."
    return checks, notes


def _make_recipes(d):
    txt = None
    for name in ("Makefile", "makefile", "GNUmakefile"):
        if os.path.isfile(os.path.join(d, name)):
            txt = read_text(os.path.join(d, name))
            break
    recipes, prereqs, variables = {}, {}, {}
    cur = None
    for line in (txt or "").splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*[?:+]?=\s*(.*)$", line)
        if m and not line.startswith("\t"):
            variables[m.group(1)] = m.group(2).strip()
            cur = None
            continue
        m = re.match(r"^([A-Za-z0-9_.\-]+)\s*:(?!=)(.*)$", line)
        if m:
            cur = m.group(1)
            recipes[cur] = ""
            prereqs[cur] = m.group(2).split("#")[0].split()
        elif cur and line.startswith("\t"):
            recipes[cur] += line.strip().lstrip("@-") + "\n"
        elif line.strip() and not line.startswith("#"):
            cur = None
    return recipes, prereqs, variables


def expand_command(c, depth=0):
    """What a check command really runs: package.json script bodies and Makefile recipes,
    followed through `npm run x` and make prerequisites. Used to read test discovery settings."""
    d = c["cwd"]
    text = c["display"]
    if depth > 3:
        return text
    toks = text.split()
    if not toks:
        return text
    if toks[0] in ("npm", "pnpm", "yarn", "bun"):
        pkg = load_json_text(read_text(os.path.join(d, "package.json")) or "") or {}
        scripts = pkg.get("scripts") if isinstance(pkg, dict) and isinstance(pkg.get("scripts"), dict) else {}
        rest = [t for t in toks[1:] if not t.startswith("-")]
        name = rest[1] if rest and rest[0] in ("run", "run-script") and len(rest) > 1 else (rest[0] if rest else None)
        body = scripts.get(name) if name else None
        if isinstance(body, str):
            parts = []
            for seg in re.split(r"(&&|\|\||;)", body):
                st = seg.strip()
                if st and st.split()[0] in ("npm", "pnpm", "yarn", "bun"):
                    parts.append(expand_command(dict(c, display=st), depth + 1))
                else:
                    parts.append(seg)
            return "".join(parts)
        return text
    if toks[0] == "make" or os.path.basename(toks[0]) == "make":
        recipes, prereqs, variables = _make_recipes(d)
        out = []

        def walk(t, n):
            if n > 6 or t not in recipes:
                return
            for pr in prereqs.get(t, []):
                walk(pr, n + 1)
            out.append(recipes[t])
        for t in [x for x in toks[1:] if not x.startswith("-")] or [next(iter(recipes), "")]:
            walk(t, 0)
        body = "".join(out)
        for _ in range(3):
            body = re.sub(r"\$[({]([A-Za-z_][A-Za-z0-9_]*)[)}]", lambda m: variables.get(m.group(1), m.group(0)), body)
        return body or text
    return text


def _norm_cmd(s):
    toks = s.strip().split()
    if len(toks) >= 2 and toks[0] in ("npm", "pnpm", "yarn", "bun") and toks[1] not in ("run", "run-script", "exec", "x", "dlx"):
        toks = [toks[0], "run"] + toks[1:]
    if toks and toks[0] == "python3":
        toks[0] = "python"
    return " ".join(toks)


def add_required(checks, rules, repo):
    for r in rules:
        if r["kind"] != "require-cmd":
            continue
        cmd = r["pattern"].strip()
        dup = next((c for c in checks if _norm_cmd(c["display"]) == _norm_cmd(cmd)), None)
        if dup:
            dup["required_by"].append(r["source"])
            continue
        argv, sh = split_cmd(cmd, repo)
        c = _check("rule", cmd.split()[0], argv, "required by %s" % r["source"], repo, shell=sh)
        c["display"] = cmd
        c["required_by"].append(r["source"])
        c["where"] = "."
        if not r.get("safe", command_is_safe(cmd)):
            c["status"], c["reason"] = "NOT RUN", "the rule's command does not look like a read-only check (it may install, delete or deploy), so it was not run automatically"
        else:
            first = cmd.split()[0]
            if first not in ("make",) and not resolve_exe(first, repo):
                c["status"], c["reason"] = "NOT RUN", "`%s` is not installed on this machine" % first
        checks.append(c)


# ---------------------------------------------------------------------------
# Running and reading output
# ---------------------------------------------------------------------------

FILE_LIKE_RE = re.compile(r"^(?:/|[A-Za-z]:\\|\.{0,2}/)?[\w@.\-/\\ ]+\.(?:c|m)?[jt]sx?$")


def parse_counts(out):
    c = {}
    tot = re.findall(r"^[#ℹ]\s*tests\s+(\d+)\s*$", out, re.M)
    if tot:
        c["runner"] = "node:test"
        c["total"] = int(tot[-1])
        for k in ("pass", "fail", "skipped", "todo", "cancelled"):
            m = re.findall(r"^[#ℹ]\s*%s\s+(\d+)\s*$" % k, out, re.M)
            if m:
                c[k] = int(m[-1])
        tops, empty, children = 0, 0, 0
        for line in out.splitlines():
            m = re.match(r"^(not )?ok \d+ - (.+?)(?:\s+#\s*(SKIP|TODO).*)?$", line)
            if m:
                tops += 1
                if FILE_LIKE_RE.match(m.group(2).strip()) and children == 0 and not m.group(1):
                    empty += 1
                children = 0
            elif re.match(r"^\s{2,}(not )?ok \d+ - ", line):
                children += 1
        c["empty_files"] = empty
        c["real_total"] = max(0, c["total"] - empty) if tops else c["total"]
        if tops and empty == tops:
            c["real_total"] = 0
        c["failed"] = c.get("fail", 0)
        c["skipped_n"] = c.get("skipped", 0) + c.get("todo", 0)
        return c
    m = re.search(r"^Tests:\s+(.*)$", out, re.M)
    if m:
        c["runner"] = "jest"
        for n, k in re.findall(r"(\d+) (passed|failed|skipped|todo|total)", m.group(1)):
            c[k] = int(n)
        c["real_total"] = c.get("total", 0)
        c["failed"] = c.get("failed", 0)
        c["skipped_n"] = c.get("skipped", 0) + c.get("todo", 0)
        return c
    m = re.search(r"^\s*Tests\s+(.+?)\s*$", out, re.M)
    if m and re.search(r"\d+ (passed|failed)", m.group(1)):
        c["runner"] = "vitest"
        for n, k in re.findall(r"(\d+) (passed|failed|skipped|todo)", m.group(1)):
            c[k] = int(n)
        c["real_total"] = sum(c.get(k, 0) for k in ("passed", "failed", "skipped", "todo"))
        c["failed"] = c.get("failed", 0)
        c["skipped_n"] = c.get("skipped", 0) + c.get("todo", 0)
        return c
    ms = re.findall(r"^=*\s*((?:\d+ (?:passed|failed|errors?|skipped|xfailed|xpassed|deselected|warnings?)(?:, )?)+) in [\d.]+s(?: \([^)]*\))?\s*=*\s*$", out, re.M)
    if ms and re.search(r"\d+ (passed|failed|error|skipped|xfailed|deselected)", ms[-1]):
        c["runner"] = "pytest"
        for n, k in re.findall(r"(\d+) (passed|failed|errors?|skipped|xfailed|xpassed|deselected)", ms[-1]):
            c[k.rstrip("s") if k.startswith("error") else k] = int(n)
        c["real_total"] = sum(c.get(k, 0) for k in ("passed", "failed", "error", "xpassed"))
        c["failed"] = c.get("failed", 0) + c.get("error", 0)
        c["skipped_n"] = c.get("skipped", 0) + c.get("xfailed", 0) + c.get("deselected", 0)
        return c
    m = re.findall(r"^Ran (\d+) tests? in", out, re.M)
    if m:
        c["runner"] = "unittest"
        c["real_total"] = sum(int(x) for x in m)
        c["failed"] = sum(int(x) for x in re.findall(r"(?:failures|errors)=(\d+)", out))
        c["skipped_n"] = sum(int(x) for x in re.findall(r"(?:skipped|expected failures)=(\d+)", out))
        return c
    m = re.search(r"^\s*(\d+) passing", out, re.M)
    if m:
        c["runner"] = "mocha"
        c["passed"] = int(m.group(1))
        f = re.search(r"^\s*(\d+) failing", out, re.M)
        p = re.search(r"^\s*(\d+) pending", out, re.M)
        c["failed"] = int(f.group(1)) if f else 0
        c["skipped_n"] = int(p.group(1)) if p else 0
        c["real_total"] = c["passed"] + c["failed"] + c["skipped_n"]
        return c
    m = re.findall(r"test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored", out)
    if m:
        c["runner"] = "cargo"
        c["real_total"] = sum(int(a) + int(b) for a, b, _ in m)
        c["failed"] = sum(int(b) for _, b, _ in m)
        c["skipped_n"] = sum(int(x) for _, _, x in m)
        return c
    if re.search(r"No tests found|No test files found|no tests ran|collected 0 items\s*$|NO TESTS RAN|Ran 0 tests", out, re.M):
        c["real_total"] = 0
        c["failed"] = 0
        return c
    if re.search(r"^(ok|FAIL|---)\s", out, re.M) or "[no test files]" in out:
        c["runner"] = "go"
        pk = re.findall(r"^(?:ok|FAIL)\s+\S+", out, re.M)
        if not pk and "[no test files]" in out:
            c["real_total"] = 0
        c["failed"] = len(re.findall(r"^--- FAIL", out, re.M))
    return c


EXCERPT_RE = re.compile(r"not ok |^\s*(error|expected|actual|operator|location|code):|AssertionError|Error:|Exception|^FAIL|^ERROR|"
                        r"^FAILED|^E\s{2,}|Traceback|^\s+File \"|\u2716|\u25cf|failing|\bassert\b|panicked|--- FAIL", re.M)


def failure_excerpt(out, n=16):
    lines = [l.rstrip() for l in out.splitlines()]
    keep = []
    for i, l in enumerate(lines):
        if EXCERPT_RE.search(l) and not re.search(r"^\s+at |node:internal|^\s*\.\.\.$", l):
            if l.strip() and l not in keep:
                keep.append(l[:240])
        if len(keep) >= n:
            break
    return keep


def failed_names(out):
    names = []
    for rx in (r"^\s*not ok \d+ - (.+?)\s*$", r"^FAILED (\S+)", r"^(?:FAIL|ERROR): (\S+(?: \([^)]+\))?)",
               r"^\s*● (.+?)\s*$", r"^--- FAIL: (\S+)", r"^\s*✖ (.+?)\s*(?:\(\d|$)"):
        for m in re.finditer(rx, out, re.M):
            n = m.group(1).strip()
            if n and n not in names and not FILE_LIKE_RE.match(n):
                names.append(n)
    return names[:8]


NOT_INSTALLED_RES = [
    (re.compile(r"(?:sh: \d+: |bash: (?:line \d+: )?|/bin/sh: (?:\d+: )?|/usr/bin/(?:env|bash|sh): (?:line \d+: )?|env: |^)['\"]?([\w@./\-]+)['\"]?: (?:command )?not found", re.M), "tool"),
    (re.compile(r"'([\w@./\-]+)' is not recognized as an internal or external command"), "tool"),
    (re.compile(r"(?:^|\s)([\w@./\-]+): No such file or directory\s*$", re.M), "tool?"),
    (re.compile(r"doesn't seem to have been installed|Run \"yarn install\"|run `bundle install`|Bundler::GemNotFound|Could not find gem|"
                r"vendor/autoload\.php|Could not open input file: vendor|composer install"), "deps"),
    (re.compile(r"Corepack must currently be enabled|Error when performing the request|Request to .* failed|getaddrinfo E(?:NOTFOUND|AI_AGAIN)|"
                r"ERR_PNPM_META_FETCH_FAIL|ERR_PNPM_NO_OFFLINE|cannot download it in offline mode|ENOTCACHED|ECONNREFUSED .*registry|"
                r"Could not resolve dependencies|in offline mode|Could not resolve all (?:files|dependencies|artifacts)|No cached version of|"
                r"Could not GET |Could not resolve plugin artifact|Non-resolvable (?:parent POM|import POM)|module lookup disabled by GOPROXY=off|"
                r"attempting to make an HTTP request, but --offline was specified|failed to download from|no matching package named|"
                r"Unable to load the service index|NU1301|NETSDK1004|Assets file .* not found|run a NuGet package restore"), "network"),
    (re.compile(r"No module named (pytest|mypy|ruff|flake8|pyright|coverage|tox|nox|black|pylint)\b"), "tool"),
    (re.compile(r"error: unrecognized arguments: (--cov\S*|-n\b|--xdist\S*|--timeout\S*|--reruns\S*)"), "plugin"),
]
PROJECT_LOAD_RE = re.compile(r"The build could not read \d+ projects?|Non-parseable POM ?(\S*)|Some problems were encountered while processing the POMs|"
                             r"Could not compile (?:settings|build) file|Could not read workspace metadata|"
                             r"pyproject\.toml.*(?:invalid|could not be parsed)|failed to parse manifest at")
TS_MISSING_RE = re.compile(r"error TS2688: Cannot find type definition file for '([^']+)'|Entry point of type library '([^']+)'|"
                           r"error TS2307: Cannot find module '([^'./][^']*)'|error TS2875|Cannot find type definition file for '([^']+)'")
NODE_MISSING_RE = re.compile(r"Cannot find (?:module|package) '([^']+)'|ERR_MODULE_NOT_FOUND[^\n]*?'([^']+)'|"
                             r"ESLint couldn't find (?:the plugin|the config) \"([^\"]+)\"|Failed to load (?:plugin|config|parser) '([^']+)'")


def declared_node_deps(d):
    pkg = load_json_text(read_text(os.path.join(d, "package.json")) or "") or {}
    out = set()
    if isinstance(pkg, dict):
        for sec in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            if isinstance(pkg.get(sec), dict):
                out |= set(pkg[sec].keys())
    return out


def declared_py_deps(d):
    txt = ""
    for f in os.listdir(d):
        if re.match(r"^(requirements.*\.(txt|in)|pyproject\.toml|setup\.cfg|setup\.py|Pipfile|tox\.ini)$", f):
            txt += (read_text(os.path.join(d, f)) or "") + "\n"
    for sub in ("requirements", "requirements.d", "reqs"):
        sd = os.path.join(d, sub)
        if os.path.isdir(sd):
            for f in os.listdir(sd):
                if f.endswith((".txt", ".in")):
                    txt += (read_text(os.path.join(sd, f)) or "") + "\n"
    return set(re.sub(r"[-_.]+", "_", m.lower()) for m in re.findall(r"[A-Za-z][A-Za-z0-9._\-]+", txt))


PY_IMPORT_ALIASES = {"yaml": "pyyaml", "bs4": "beautifulsoup4", "PIL": "pillow", "cv2": "opencv_python",
                     "sklearn": "scikit_learn", "dateutil": "python_dateutil", "jwt": "pyjwt", "dotenv": "python_dotenv",
                     "attr": "attrs", "google": "google", "psycopg2": "psycopg2_binary", "magic": "python_magic"}


def _bare_pkg(name):
    if not name or name.startswith((".", "/", "node:", "#")) or re.match(r"^[A-Za-z]:\\", name):
        return None
    return "/".join(name.split("/")[:2]) if name.startswith("@") else name.split("/")[0]


def missing_dep_reason(c, out):
    """Why a failed command did not really run (a dependency or tool is missing, or it needed the
    network), or None when the failure is real. Missing dependencies are NOT RUN, never FAIL;
    the exception is a package the change itself starts importing without declaring it."""
    d = c["cwd"]
    new_imports = c.get("_new_imports") or set()
    repo = c.get("_repo") or d
    nm_present = _has_node_modules(d, repo)
    for rx, kind in NOT_INSTALLED_RES:
        m = rx.search(out)
        if not m:
            continue
        if kind == "tool?":
            if c.get("exit") != 127:
                continue
            kind = "tool"
        if kind == "tool":
            return "`%s` is not installed here (exit %s); install the project's dependencies or the tool, then prove again" % (m.group(1), c.get("exit"))
        if kind == "plugin":
            return "a pytest plugin the project configures (for `%s`) is not installed here; install the dev dependencies, then prove again" % m.group(1)
        if kind == "network":
            return "the command needed the network (a dependency download), which this check does not allow; install the dependencies, then prove again"
        return "dependencies are not installed; run the project's install command, then prove again"
    if c.get("exit") == 127:
        return "a program the command needs is not installed (exit 127); install the project's tools, then prove again"
    if re.search(r"Aborting as no plugin should be loaded if running as super user|Do not run Composer as root", out):
        return "Composer refuses to run as the root user on this machine (set COMPOSER_ALLOW_SUPERUSER=1 or run as a normal user)"
    m = PROJECT_LOAD_RE.search(out)
    if m:
        manifest = m.group(1) or "the build file"
        changed = c.get("_changed") or set()
        if not any(base_of(p).lower() in ("pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts",
                                          "gemfile", "composer.json", "deno.json", "package.json", "pyproject.toml", "cargo.toml", "go.mod")
                   for p in changed):
            return "the build tool could not load the project (%s), and the change does not touch its build files: an existing setup problem" % manifest
    m = TS_MISSING_RE.search(out)
    if m and (not nm_present or m.group(1) or m.group(2) or m.group(4)):
        name = next((g for g in m.groups() if g), "a type package")
        if not nm_present or not os.path.isdir(os.path.join(d, "node_modules", "@types", name.split("/")[0])):
            return "type definitions for `%s` are not installed (%s); run the install command, then prove again" % (
                name, "no node_modules" if not nm_present else "missing from node_modules")
    for m in NODE_MISSING_RE.finditer(out):
        name = next((g for g in m.groups() if g), None)
        base = _bare_pkg(name)
        if not base:
            continue
        if base in new_imports and base not in declared_node_deps(d):
            continue  # the change imports a package nobody declared: a real failure
        if not nm_present or not os.path.isdir(os.path.join(d, "node_modules", base)):
            return "the package `%s` is not installed (%s). Install the dependencies, then prove again" % (
                base, "no node_modules folder" if not nm_present else "not in node_modules")
    for m in re.finditer(r"No module named '?([\w.]+)'?", out):
        top = m.group(1).split(".")[0]
        if os.path.exists(os.path.join(d, top)) or os.path.exists(os.path.join(d, top + ".py")) or \
                os.path.exists(os.path.join(d, "src", top)) or os.path.exists(os.path.join(repo, top)):
            continue  # the project's own module: a real import error
        if top in new_imports and re.sub(r"[-_.]+", "_", PY_IMPORT_ALIASES.get(top, top).lower()) not in declared_py_deps(d):
            continue  # the change imports a module nobody declared: a real failure
        name = PY_IMPORT_ALIASES.get(top, top)
        return "the Python module `%s` is not installed in this environment. Install the project's dependencies, then prove again" % name
    for m in re.finditer(r"cannot load such file -- ([\w/\-]+)", out):
        return "the Ruby library `%s` is not installed; run `bundle install`, then prove again" % m.group(1)
    # pnpm prints "node_modules missing, did you mean to install?" after ANY failing script when
    # node_modules is absent. It is advice, not proof: only treat it as the cause when the script
    # itself produced no output of its own (it never got to run).
    if ADVISORY_DEPS_RE.search(out) and not _script_spoke(out):
        return "dependencies are not installed (no node_modules); run the project's install command, then prove again"
    return None


ADVISORY_DEPS_RE = re.compile(r"node_modules missing, did you mean to install")
PM_NOISE_RE = re.compile(r"^\s*(?:>\s|\$\s|ELIFECYCLE|ERR_PNPM|npm (?:ERR!|error|warn)|WARN\b|warn\b|error Command failed|"
                         r"info Visit|Done in|\S*Command failed with exit code|undefined$)", re.I)


def _script_spoke(out):
    """True when the output has lines from the script itself, not only package-manager banners
    (the `> name script` echo, ELIFECYCLE, WARN lines)."""
    for line in out.splitlines():
        s = line.strip()
        if s and not PM_NOISE_RE.match(s):
            return True
    return False


ECHO_ONLY_RE = re.compile(r"^\s*(?:(?:echo|printf|true|:|exit\s+0)\b[^&|;]*(?:&&|;|\|\||$)\s*)+$")


def run_check(c, timeout):
    if c["status"] == "NOT RUN":
        return c
    res = run_cmd(c["cmd"], c["cwd"], timeout, shell=c["shell"], extra_env=c.get("env"))
    if res.get("budget"):
        c["status"], c["reason"] = "NOT RUN", "the proof's time budget was used up before this check could start (raise --budget or use --only)"
        return c
    c["seconds"] = round(res["seconds"], 2)
    c["exit"] = res["exit"]
    out = redact_text(res["output"])
    c["tail"] = tail(out, 40)
    c["_out"] = out[-200000:]
    if res.get("error"):
        c["status"], c["reason"] = "NOT RUN", "could not start the command: %s" % res["error"]
        return c
    if res["timed_out"]:
        if res.get("budget_cut"):
            c["status"], c["reason"] = "NOT RUN", "stopped when the proof's time budget ran out (raise --budget, or run this check by hand)"
            return c
        c["status"] = "TIMEOUT"
        c["reason"] = "did not finish within %ds (killed)" % timeout
        return c
    if c["kind"] == "test":
        c["counts"] = parse_counts(out)
    failed_n = (c["counts"] or {}).get("failed", 0) if c["kind"] == "test" else 0
    if res["exit"] != 0 or failed_n:
        why = missing_dep_reason(c, out) if res["exit"] != 0 else None
        if why:
            c["status"], c["reason"] = "NOT RUN", why
            return c
        c["status"] = "FAIL"
        if res["exit"] == 0 and failed_n:
            c["masked"] = True
            c["reason"] = "exited 0 but its output reports %d failing test%s (the exit code is masked)" % (failed_n, "" if failed_n == 1 else "s")
        if c["kind"] in ("test", "rule"):
            c["failed_tests"] = failed_names(out)
        c["excerpt"] = failure_excerpt(out)
        if c["kind"] == "test" and c["counts"].get("real_total") == 0 and c["counts"].get("failed", 0) == 0 and \
                re.search(r"NO TESTS RAN|no tests ran|collected 0 items|No tests found|No test files found|Ran 0 tests", out):
            c["status"] = "NO TESTS"
        return c
    if c["kind"] == "test" and c["counts"].get("real_total") == 0:
        c["status"] = "NO TESTS"
        return c
    if c["kind"] == "test" and not c["counts"] and ECHO_ONLY_RE.match(c.get("expanded") or ""):
        c["status"] = "NO TESTS"
        c["reason"] = "the test command only prints a message (`%s`); it runs no tests" % (c.get("expanded") or "").strip()[:80]
        return c
    c["status"] = "PASS"
    return c


LOC_RES = [re.compile(r"^\s*([\w./\\@\-\[\]() ]+?\.(?:py|pyi|ts|tsx|mts|cts|js|jsx|mjs|cjs|vue|svelte|go|rs|rb|php)):(\d+)(?::\d+)?\b", re.M),
           re.compile(r"^\s*([\w./\\@\-\[\]() ]+?\.(?:ts|tsx|mts|cts|js|jsx))\((\d+),\d+\)", re.M),
           re.compile(r"^\s*-->\s*([\w./\\@\-\[\]() ]+?\.\w{1,5}):(\d+):\d+", re.M)]


def preexisting_failure(c, change, repo):
    """For a check the project does not declare (inferred from a config file): when every error
    location it prints is on a line the change did not add, the failure is most likely older
    than the change. Returns the number of such locations, or 0."""
    if not c.get("inferred") or c["status"] != "FAIL" or not change or not change.ok or c.get("masked"):
        return 0
    out = c.get("_out") or ""
    locs = []
    for rx in LOC_RES:
        for m in rx.finditer(out):
            locs.append((m.group(1).strip().replace("\\", "/"), int(m.group(2))))
    if not locs:
        return 0
    added = {}
    for f in change.files:
        added[f.path] = set(ln for ln, _ in f.added) if f.status != "A" else None
    base = os.path.relpath(c["cwd"], repo)
    for path, ln in locs:
        rel = posix(os.path.normpath(os.path.join(base, path))) if not os.path.isabs(path) else posix(os.path.relpath(path, repo))
        rel = rel[2:] if rel.startswith("./") else rel
        if rel in added and (added[rel] is None or ln in added[rel]):
            return 0
    return len(locs)


# ---------------------------------------------------------------------------
# Findings from checks
# ---------------------------------------------------------------------------

def check_findings(checks):
    out = []
    for c in checks:
        st = c["status"]
        if st == "FAIL" and c.get("preexisting"):
            out.append(finding(
                KIND_CAUSE[c["kind"]], "Fails on lines the change did not touch: `%s`" % c["display"],
                "`%s` (not declared by the project; run because its config exists) exits %s, and every error it reports (%d) is on a line this change did not add." % (
                    c["display"], c["exit"], c["preexisting"]),
                ["exit %s after %.1fs (%s)" % (c["exit"], c["seconds"], c["source"])] +
                ["> " + l.strip() for l in (c["excerpt"][:6] or [t for t in c["tail"] if t.strip()][-6:])],
                "Probably an older failure, not caused by this change; it still fails wherever this check runs.",
                ["Tell the person it was already failing (check with `git stash` and a rerun if unsure); fix it only if the task covers it."],
                key="check:pre:%s" % c["display"], tier="check"))
            continue
        if st in ("FAIL", "TIMEOUT"):
            cause = KIND_CAUSE[c["kind"]]
            what = {"test": "Tests fail", "build": "The build fails", "typecheck": "The type check fails",
                    "lint": "Lint fails", "rule": "A command required by a project rule fails"}[c["kind"]]
            if st == "TIMEOUT":
                what = {"test": "Tests", "build": "The build", "typecheck": "The type check", "lint": "Lint",
                        "rule": "A command required by a project rule"}[c["kind"]] + " timed out"
            cnt = c.get("counts") or {}
            detail = ""
            if c["kind"] == "test" and cnt.get("failed"):
                detail = " %d of %s tests failed%s." % (cnt["failed"], cnt.get("real_total", "?"),
                                                         (": " + "; ".join(c["failed_tests"][:4])) if c["failed_tests"] else "")
            elif c["failed_tests"]:
                detail = " Failing: %s." % "; ".join(c["failed_tests"][:4])
            if st == "TIMEOUT":
                txt = "`%s` did not finish within the time limit and was stopped." % c["display"]
            elif c.get("masked"):
                txt = "`%s` exited with code 0, but its output reports failing tests: the exit code is masked (for example by `|| true`).%s" % (c["display"], detail)
            else:
                txt = "`%s` exited with code %s.%s" % (c["display"], c["exit"], detail)
            out.append(finding(
                cause, "%s: `%s`" % (what, c["display"]), txt,
                ["exit %s after %.1fs (%s)%s" % (c["exit"], c["seconds"], c["source"], "; exit code masked" if c.get("masked") else "")] +
                ["> " + l.strip() for l in (c["excerpt"][:10] or [t for t in c["tail"] if t.strip()][-8:])],
                {"test": "Behaviour the tests protect is broken right now; saying done would ship the failure.",
                 "build": "The project cannot be built, so it cannot be deployed.",
                 "typecheck": "The type checker found mismatches the code will hit at runtime or in CI.",
                 "lint": "CI or the pre-merge checks will reject this change.",
                 "rule": "The project says this command must pass before work is done."}[c["kind"]],
                ["Read the output above, fix the code (not the test or the check), and run the proof again."
                 if st == "FAIL" else "Find out why it hangs (a test waiting on network, a watch mode, an open handle); rerun with --timeout if it is just slow."],
                key="check:%s:%s" % (c["kind"], c["display"]), also=[8] if c["required_by"] and cause != 8 else []))
        elif st == "NO TESTS":
            out.append(finding(
                5, "Tests did not really run: `%s` ran 0 tests" % c["display"],
                ("`%s` exited %s: %s." % (c["display"], c["exit"], c["reason"])) if c.get("reason") else
                "`%s` exited %s but ran no tests%s." % (c["display"], c["exit"],
                                                       " (%d test file%s had no tests in them)" % (c["counts"].get("empty_files", 0), "" if c["counts"].get("empty_files", 0) == 1 else "s") if c["counts"].get("empty_files") else ""),
                ["exit %s after %.1fs" % (c["exit"], c["seconds"])] + ["> " + l for l in c["tail"][-6:]],
                "A passing run with zero tests proves nothing about the change.",
                ["Check the test command, file names and filters; restore any tests that were removed or commented out, then rerun."],
                key="check:notests:%s" % c["display"]))
    return _fold_rule_failures(checks, out)


def _signature_lines(c):
    """Distinctive failure lines of a check (no package-manager banners, no short lines)."""
    return [l.strip() for l in (c.get("tail") or []) if len(l.strip()) >= 12 and not PM_NOISE_RE.match(l.strip())]


def _fold_rule_failures(checks, out):
    """A command a rule requires (`npm run check`, `make check`) often just runs the other checks.
    When it fails with the same error lines as a check that already failed, report one problem:
    the check's finding gains cause 8 and a line saying the required command fails because of it."""
    std = [c for c in checks if c["status"] == "FAIL" and c["kind"] != "rule"]
    for c in checks:
        if c["kind"] != "rule" or c["status"] != "FAIL" or not std:
            continue
        rule_out = "\n".join(l.strip() for l in (c.get("tail") or []))
        for s in std:
            sig = _signature_lines(s)
            if not sig or not any(l in rule_out for l in sig[-8:]):
                continue
            target = next((f for f in out if f["key"] == "check:%s:%s" % (s["kind"], s["display"])), None)
            rule_f = next((f for f in out if f["key"] == "check:rule:%s" % c["display"]), None)
            if target is None or rule_f is None:
                continue
            if 8 not in target["causes"]:
                target["causes"].append(8)
            target["evidence"].insert(1, "`%s` (%s) fails with the same error, so it is not a separate problem" % (
                c["display"], ", ".join("required by %s" % r for r in c["required_by"]) or c["source"]))
            out.remove(rule_f)
            break
    return out


def no_test_finding(checks, change):
    if any(c["kind"] == "test" for c in checks):
        return []
    return [finding(
        5, "No test command found",
        "No test script, Makefile target or test runner was found for this project, so nothing proves the change works.",
        ["looked for: package.json scripts.test, Makefile test target, pyproject task tables, pytest/unittest test files, "
         "Cargo.toml, go.mod, Maven, Gradle, Bundler, Composer, .NET and Deno projects"],
        "Without tests, \"done\" rests on reading the code alone.",
        ["Run the feature by hand and show the output, or add a test for the change; say plainly that there is no automated test."],
        key="notests", tier="check")]


# ---------------------------------------------------------------------------
# Main proof
# ---------------------------------------------------------------------------

PY_IMPORT_LINE_RE = re.compile(r"^\s*(?:from\s+([A-Za-z_]\w*)[\w.]*\s+import\b|import\s+([A-Za-z_]\w*))")
JS_IMPORT_LINE_RE = re.compile(r"""(?:\bfrom\s+|\brequire\s*\(\s*|\bimport\s*\(\s*|^\s*import\s+)['"]([^'"]+)['"]""")


def _new_imports(change):
    names = set()
    if not change or not change.ok:
        return names
    for f in change.files:
        if f.binary or f.folder_files or f.status == "D":
            continue
        e = ext_of(f.path)
        for _, t in f.added[:5000]:
            if e == ".py":
                m = PY_IMPORT_LINE_RE.match(t)
                if m:
                    names.add(m.group(1) or m.group(2))
            elif e in (".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".mts", ".cts", ".vue", ".svelte"):
                for m in JS_IMPORT_LINE_RE.finditer(t[:1000]):
                    bp = _bare_pkg(m.group(1))
                    if bp:
                        names.add(bp)
    return names


def _memo_path(repo, kind):
    import hashlib
    import tempfile
    h = hashlib.sha1(os.path.abspath(repo).encode("utf-8", "replace")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "prove-it-works-%s-%s.json" % (kind, h))


def _untracked_now(repo):
    code, out = run_git(repo, ["ls-files", "-z", "--others", "--exclude-standard", "--directory", "--no-empty-directory"])
    return set(posix(x).rstrip("/") for x in dec(out).split("\0") if x) if code == 0 else set()


def _load_memo(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _save_memo(path, data):
    try:
        with open(path, "w") as fh:
            json.dump(data, fh)
    except OSError:
        pass


def _pl(n, w):
    return "%d %s%s" % (n, w, "" if n == 1 else "s")


def prove(repo, base=None, task=None, task_src=None, only=None, timeout=300, ignore=(), budget=None, since_ref=None):
    import diffcheck as DC
    import rules as RL
    t0 = time.time()
    repo = os.path.abspath(repo)
    set_deadline(budget)
    res = {"skill": "prove-it-works", "schema_version": 2, "repo": repo, "task_source": task_src, "notes": [], "timings": {}}
    change = load_change(repo, base, ignore, since_ref)
    res["notes"] += change.notes
    t1 = time.time()
    mech, read, rfiles = RL.parse_rules(repo)
    checks, dnotes = detect_checks(repo, change, mech)
    add_required(checks, mech, repo)
    for c in checks:
        if c["kind"] == "test":
            c["expanded"] = expand_command(c)
    test_runs = [(c["display"], c.get("expanded") or expand_command(c), c.get("where") or ".") for c in checks if c["kind"] == "test"]
    info = {}
    findings, notes = DC.inspect(change, task, mech, rfiles, skip_paths=set(ignore), test_runs=test_runs, info=info)
    res["notes"] += notes
    t2 = time.time()
    res["notes"] += dnotes
    if only:
        wanted = set(ONLY_ALIASES.get(x.strip().lower(), x.strip().lower()) for x in only.split(",") if x.strip())
        skipped = [c for c in checks if c["kind"] not in wanted]
        checks = [c for c in checks if c["kind"] in wanted]
        if skipped:
            res["notes"].append("--only %s: skipped %s." % (only, ", ".join("`%s`" % c["display"] for c in skipped)))
    # files the previous proof's own commands created (build output, caches) are not the agent's change
    memo_p = _memo_path(repo, "created")
    prev_created = set(_load_memo(memo_p).get("created") or []) if change.ok else set()
    before = _untracked_now(repo) if change.ok else set()
    imports = _new_imports(change)
    changed_paths = set(f.path for f in change.files) if change.ok else set()
    for c in checks:
        c["_new_imports"], c["_repo"], c["_changed"] = imports, repo, changed_paths
        run_check(c, timeout)
        if c["status"] == "FAIL":
            c["preexisting"] = preexisting_failure(c, change, repo)
    if change.ok:
        after = _untracked_now(repo)
        created = sorted((after - before) | (prev_created & after))
        _save_memo(memo_p, {"created": created[:500]})
    if prev_created:
        for f in findings:
            fp = f.get("file") or ""
            if f["tier"] == "problem" and fp and any(fp == x or fp.startswith(x.rstrip("/") + "/") for x in prev_created):
                f["tier"] = "check"
                f["finding"] += " It appeared when the previous proof ran the project's own commands, so it is probably their output."
    t3 = time.time()
    cf = check_findings(checks)
    if not only or "test" in (ONLY_ALIASES.get(x.strip().lower(), "") for x in only.split(",")):
        cf += no_test_finding(checks, change)
    allf = cf + findings
    failing = [c for c in checks if c["status"] in ("FAIL", "TIMEOUT") and not c.get("preexisting")]
    pre = [c for c in checks if c["status"] == "FAIL" and c.get("preexisting")]
    notrun = [c for c in checks if c["status"] == "NOT RUN"]
    passed = [c for c in checks if c["status"] == "PASS"]
    notests_ran = [c for c in checks if c["status"] == "NO TESTS"]
    # failing checks are counted as checks; everything else at the problem tier is a problem in the change
    change_problems = [f for f in allf if f["tier"] == "problem" and
                       (not f["key"].startswith("check:") or f["key"].startswith("check:notests"))]
    has_test = any(c["kind"] == "test" for c in checks)
    stopped = info.get("stopped") or []
    unsupported = unsupported_stacks(repo)
    gaps = []
    if not change.ok:
        gaps.append("the change was not inspected (%s)" % change.reason)
    elif change.nochange:
        gaps.append("there is no change to inspect")
    if task is None and change.ok and not change.nochange:
        gaps.append("no task was given, so scope and task items were not checked")
    if not has_test and checks and (not only or "test" in only):
        gaps.append("no test command was found")
    for c in pre:
        gaps.append("`%s` fails only on lines the change did not touch (likely pre-existing)" % c["display"])
    if stopped:
        gaps.append("the %s inspection ran out of time" % ", ".join(stopped))
    if unsupported and not checks:
        gaps.append("%s code is not analysed" % ", ".join(unsupported))
    ncheck = len(checks)
    if failing or change_problems:
        status = "NOT DONE"
        verdict = "NOT DONE: %s, %s in the change" % (_pl(len(failing), "failing check"), _pl(len(change_problems), "problem"))
        extra = []
        if notrun:
            extra.append("%s not run" % _pl(len(notrun), "check"))
        if not checks:
            extra.append("no checks found")
        if not change.ok:
            extra.append("change not inspected")
        elif change.nochange:
            extra.append("no change to inspect")
        if extra:
            verdict += ", " + ", ".join(extra)
    elif not checks or (notrun and not passed and not pre):
        status = "NOT VERIFIED"
        if not checks:
            verdict = "NOT VERIFIED: no checks found (no test, build, typecheck or lint command)"
        else:
            verdict = "NOT VERIFIED: %s could not run (%s)" % (_pl(len(notrun), "check"), _notrun_summary(notrun))
        if change.ok and not change.nochange:
            verdict += "; no problems found in the change"
        elif gaps:
            verdict += "; " + gaps[0]
    elif not passed:
        status = "NOT VERIFIED"
        verdict = "NOT VERIFIED: no check passed; %s" % "; ".join(gaps)
    elif notrun:
        status = "NOT VERIFIED"
        verdict = "NOT VERIFIED: %d of %d checks passed, %s could not run (%s)" % (
            len(passed), ncheck, _pl(len(notrun), "check"), _notrun_summary(notrun))
        verdict += "; no problems found in the change" if change.ok and not change.nochange else ("; " + gaps[0] if gaps else "")
    elif gaps:
        status = "CHECKS PASS"
        head = "CHECKS PASS (task not verified)" if (task is None and change.ok and not change.nochange) else "CHECKS PASS (not fully verified)"
        verdict = "%s: %s passed, no problems in the change; %s" % (
            head, ("all %s" % _pl(len(passed), "check")) if not pre else _pl(len(passed), "check"), "; ".join(gaps))
    else:
        status = "PROVEN"
        verdict = "PROVEN: all %s passed, no problems in the change" % _pl(ncheck, "check")
        if only:
            verdict += " (only %s ran)" % only
    nchk = sum(1 for f in allf if f["tier"] == "check")
    if status in ("PROVEN", "CHECKS PASS") and nchk:
        verdict += " (%s to review)" % _pl(nchk, "item")
    coverage_notes = list(gaps)
    if notrun:
        coverage_notes.append("%s not run: %s" % (_pl(len(notrun), "check"), "; ".join(
            "`%s` (%s)" % (c["display"], (c.get("reason") or "")[:90]) for c in notrun[:4])))
    skipped_files = info.get("skipped") or []
    if skipped_files:
        coverage_notes.append("%s skipped by the line checks (minified, generated or vendored)" % _pl(len(skipped_files), "file"))
    if change.shallow:
        coverage_notes.append("shallow clone: history beyond the fetched commits was not available")
    if unsupported:
        coverage_notes.append("not analysed: %s" % ", ".join(unsupported))
    for n in dnotes:
        if n.startswith("Monorepo"):
            coverage_notes.append(n)
    for c in checks:
        c.pop("_out", None)
        c.pop("_new_imports", None)
        c.pop("_repo", None)
        c.pop("_changed", None)
    res.update({
        "verdict": verdict, "status": status,
        "change": {"ok": change.ok, "how": change.how or change.reason, "base": change.base_label,
                   "files": [f.to_json() for f in change.files], "commits": change.commits, "no_change": change.nochange},
        "checks": checks, "findings": [f for f in allf if f["tier"] == "problem"],
        "check_these": [f for f in allf if f["tier"] == "check"],
        "counts": {"checks": len(checks), "passed": len(passed), "failing": len(failing), "not_run": len(notrun),
                   "no_tests": len(notests_ran), "preexisting": len(pre),
                   "problems": len(change_problems), "check_these": nchk},
        "rules": {"files": rfiles, "checked": mech, "read": read},
        "cant_see": CANT_SEE,
        "coverage": {"complete": status == "PROVEN" and not skipped_files and not stopped,
                     "notes": coverage_notes, "files_scanned": info.get("files", 0), "skipped_large": len(skipped_files),
                     "unreadable": 0, "truncated": False, "shallow_history": change.shallow,
                     "history_scanned": None, "unsupported": unsupported},
    })
    _group_counts(res["findings"])
    _group_counts(res["check_these"])
    res["timings"] = {"change_s": round(t1 - t0, 2), "inspect_s": round(t2 - t1, 2), "checks_s": round(t3 - t2, 2),
                      "total_s": round(time.time() - t0, 2)}
    return res


def _group_counts(fs):
    n = {}
    for f in fs:
        n[f["group"]] = n.get(f["group"], 0) + 1
    for f in fs:
        f["group_count"] = n[f["group"]]


def _notrun_summary(notrun):
    rs = " ".join((c.get("reason") or "") for c in notrun)
    if re.search(r"not installed|node_modules|install", rs):
        return "dependencies or tools are not installed"
    if "time budget" in rs:
        return "the time budget ran out"
    if "not run automatically" in rs:
        return "not safe to run automatically"
    if "network" in rs:
        return "they needed the network"
    return "see the checks table"


HOOK_MAX_BLOCKS = 8
HOOK_BUDGET = 500


def _transcript_task(path):
    """(task text, session start ISO timestamp) from a Claude Code transcript (JSONL): the first
    real user prompt plus the latest one, without tool results, commands or system reminders."""
    prompts, start = [], None
    try:
        size = os.path.getsize(path)
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            if size > 30 * 1024 * 1024:
                fh.seek(size - 30 * 1024 * 1024)
                fh.readline()
            for line in fh:
                d = load_json_text(line)
                if not isinstance(d, dict):
                    continue
                if start is None and d.get("timestamp"):
                    start = d.get("timestamp")
                if d.get("type") != "user" or d.get("isMeta"):
                    continue
                content = (d.get("message") or {}).get("content")
                if isinstance(content, list):
                    if any(isinstance(x, dict) and x.get("type") == "tool_result" for x in content):
                        continue
                    content = "\n".join(x.get("text", "") for x in content if isinstance(x, dict) and x.get("type") == "text")
                if not isinstance(content, str):
                    continue
                text = re.sub(r"<system-reminder>.*?</system-reminder>", "", content, flags=re.S).strip()
                if not text or text.startswith(("<command-", "<local-command", "Caveat:", "<bash-", "[Request interrupted")):
                    continue
                prompts.append(text)
    except (OSError, ValueError):
        return None, None
    if not prompts:
        return None, start
    task = prompts[0]
    if len(prompts) > 1 and prompts[-1] != prompts[0]:
        task += "\n\n" + prompts[-1]
    return task[:8000], start


def _fingerprint(root):
    import hashlib
    h = hashlib.sha1()
    for args in (["rev-parse", "HEAD"], ["status", "--porcelain=v1", "-z", "--untracked-files=all"],
                 ["diff", "--no-color", "--no-ext-diff", "HEAD"]):
        code, out = run_git(root, args, timeout=60)
        h.update(out or b"")
        h.update(b"\0")
    return h.hexdigest()


def _hook_say(obj):
    sys.stdout.write(json.dumps(obj) + "\n")


def _hook_summary(res, n=8):
    lines = [res["verdict"]]
    for c in res["checks"]:
        if c["status"] not in ("PASS",):
            lines.append("- %s `%s`: %s" % (KIND_LABEL.get(c["kind"], c["kind"]), c["display"],
                                            c["status"] + (" (%s)" % c["reason"] if c.get("reason") else "")))
    for f in [f for f in res["findings"] if not f["key"].startswith("check:")][:n]:
        lines.append("- %s" % f["title"])
    return lines


def hook_main(a):
    """Claude Code Stop hook (v2).

    - Finds the repo from CLAUDE_PROJECT_DIR, then the hook's cwd (git top-level), so a session
      that cd'ed into a subfolder is still checked as a whole.
    - Proves uncommitted work, commits on a feature branch, and commits made on the default
      branch during the session (HEAD at the first stop is remembered; the transcript's start time
      is used when available). Reads the task from the transcript.
    - Blocks only on NOT DONE, and only when the code changed since the last block; if Claude
      stops again with the same diff, the stop goes through and the person is told it is still
      NOT DONE. Never blocks on NOT RUN, missing checks, timeouts or non-git folders.
    - Skips the run entirely when nothing changed since the last proof (question-only turns).
    """
    import hashlib
    import tempfile
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    data = load_json_text(raw) or {}
    root = None
    for cand in (a.repo, os.environ.get("CLAUDE_PROJECT_DIR"), data.get("cwd"), os.getcwd()):
        if cand and os.path.isdir(cand):
            root = repo_root(cand)
            if root:
                break
    if not root:
        return 0
    key = hashlib.sha1(("%s|%s" % (data.get("session_id") or "", os.path.abspath(root))).encode("utf-8", "replace")).hexdigest()[:20]
    memo_p = os.path.join(tempfile.gettempdir(), "prove-it-works-hook-%s.json" % key)
    memo = _load_memo(memo_p)
    head = dec(run_git(root, ["rev-parse", "--verify", "-q", "HEAD"])[1]).strip() or None
    if "head0" not in memo:
        memo["head0"] = head
    fp = _fingerprint(root)
    if memo.get("last_fp") == fp:
        if memo.get("last_status") == "NOT DONE" and memo.get("told_fp") != fp:
            memo["told_fp"] = fp
            _save_memo(memo_p, memo)
            _hook_say({"systemMessage": no_em_dash("Prove It Works: Claude stopped while the proof still says NOT DONE (nothing changed since it was asked to fix it).\n" +
                                                   "\n".join(memo.get("last_summary") or []))})
        return 0
    task, start = (None, None)
    if data.get("transcript_path"):
        task, start = _transcript_task(data["transcript_path"])
    since_ref = None
    from common import default_branch, git_info, _same_branch
    info = git_info(root) or {}
    db = default_branch(root)
    on_default = (not info.get("branch")) or _same_branch(info.get("branch"), db or info.get("branch"))
    if on_default and info.get("has_head"):
        if memo.get("head0") and memo["head0"] != head:
            since_ref = memo["head0"]
        elif start:
            code, out = run_git(root, ["rev-list", "--reverse", "--since=%s" % start, "HEAD"])
            first = dec(out).split()[0] if code == 0 and out.strip() else None
            if first:
                parent = dec(run_git(root, ["rev-parse", "--verify", "-q", first + "~1"])[1]).strip()
                since_ref = parent or None
    if on_default and not since_ref and not is_dirty(root, ()):
        memo.update({"last_fp": fp, "last_status": "NOTHING"})
        _save_memo(memo_p, memo)
        return 0
    res = prove(root, a.base, task, "transcript" if task else None, a.only, a.timeout, budget=a.budget or HOOK_BUDGET,
                since_ref=since_ref)
    status = res["status"]
    summary = _hook_summary(res)
    memo.update({"last_fp": fp, "last_status": status, "last_summary": summary})
    if res["change"].get("no_change") and status != "NOT DONE":
        _save_memo(memo_p, memo)
        return 0
    if status == "NOT DONE":
        real = [c for c in res["checks"] if c["status"] == "FAIL" and not c.get("preexisting")] or \
            [f for f in res["findings"] if not f["key"].startswith("check:")] or \
            [c for c in res["checks"] if c["status"] == "NO TESTS"]
        if not real:
            # only timeouts: not proof of failure, and blocking would rerun a slow suite on every stop
            memo["last_status"] = "TIMEOUT"
            _save_memo(memo_p, memo)
            _hook_say({"systemMessage": no_em_dash("Prove It Works: not verified, a check timed out in the Stop hook (%s). "
                                                   "Run the proof by hand with a longer --timeout." % "; ".join(summary[1:3]))})
            return 0
        memo["blocks"] = int(memo.get("blocks") or 0) + 1
        if memo["blocks"] > HOOK_MAX_BLOCKS:
            memo["told_fp"] = fp
            _save_memo(memo_p, memo)
            _hook_say({"systemMessage": no_em_dash("Prove It Works: still NOT DONE after %d attempts; letting Claude stop.\n%s" % (
                HOOK_MAX_BLOCKS, "\n".join(summary)))})
            return 0
        memo["last_block_fp"] = fp
        _save_memo(memo_p, memo)
        reason = summary + ["Run prove.py from the prove-it-works skill, show its output, and fix these, or tell the person plainly "
                            "what is not done and why. If something needs the person (installing dependencies, a decision), say so and stop."]
        _hook_say({"decision": "block", "reason": no_em_dash("\n".join(reason))})
        return 0
    if status == "NOT VERIFIED" and memo.get("told_fp") != fp:
        memo["told_fp"] = fp
        _save_memo(memo_p, memo)
        _hook_say({"systemMessage": no_em_dash("Prove It Works: " + res["verdict"] + ". " +
                                               "; ".join("`%s`: %s" % (c["display"], c.get("reason") or "") for c in res["checks"] if c["status"] == "NOT RUN")[:600])})
        return 0
    _save_memo(memo_p, memo)
    return 0


def main(argv=None):
    import report as R
    ap = argparse.ArgumentParser(description="Prove It Works: run the real checks and inspect the change before saying done.")
    ap.add_argument("repo", nargs="?")
    ap.add_argument("--base", help="compare against this ref (default: the merge-base with the default branch on a feature "
                                   "branch, HEAD for uncommitted work on the default branch)")
    ap.add_argument("--task", help="the task description, as text")
    ap.add_argument("--task-file", help="a file holding the task description")
    ap.add_argument("--only", help="comma list of checks to run: tests,build,typecheck,lint,rules")
    ap.add_argument("--timeout", type=int, default=300, help="seconds per command (default 300)")
    ap.add_argument("--budget", type=int, default=None, help="seconds for all commands together (default 540; hook 500)")
    ap.add_argument("--ignore", action="append", default=[], help=argparse.SUPPRESS)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--ledger", action="store_true", help="append a summary line to <repo>/.shipsnag/ledger.md")
    ap.add_argument("--hook", action="store_true", help="Claude Code Stop hook mode (reads hook JSON on stdin)")
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    install_signal_handlers()
    if a.hook:
        try:
            return hook_main(a)
        except Exception:  # a broken hook must never trap the session
            import traceback
            traceback.print_exc(file=sys.stderr)
            return 0
    if not a.repo or not os.path.isdir(a.repo):
        sys.stderr.write("not a directory: %s\n" % a.repo)
        return 2
    task, src = a.task, ("--task" if a.task else None)
    ignore = list(a.ignore)
    if a.task_file:
        task = read_text(a.task_file)
        if task is None:
            sys.stderr.write("cannot read task file: %s\n" % a.task_file)
            return 2
        src = a.task_file
        try:
            rel = posix(os.path.relpath(os.path.abspath(a.task_file), os.path.abspath(a.repo)))
            if not rel.startswith(".."):
                ignore.append(rel)
        except ValueError:
            pass
    try:
        res = prove(a.repo, a.base, task, src, a.only, a.timeout, ignore, budget=a.budget or 540)
    except Exception:
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 2
    if a.json:
        sys.stdout.write(json.dumps(R.to_json(res), indent=2) + "\n")
    else:
        sys.stdout.write(R.render_md(res))
    if a.ledger:
        causes = sorted(set(c for f in res["findings"] for c in f["causes"]))
        write_ledger(res["repo"], "prove-it-works", res["verdict"],
                     "checks %d (%d failing, %d not run) | causes: %s | %.1fs" % (
                         res["counts"]["checks"], res["counts"]["failing"], res["counts"]["not_run"],
                         ",".join(str(c) for c in causes) or "none", res["timings"]["total_s"]))
    return {"PROVEN": 0, "NOT DONE": 1}.get(res["status"], 3)


if __name__ == "__main__":
    sys.exit(main())
