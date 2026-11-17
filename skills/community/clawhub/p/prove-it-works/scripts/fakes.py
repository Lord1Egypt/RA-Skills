#!/usr/bin/env python3
"""Quiet fakes for Prove It Works v2: changes that make the checks pass without the work being done.

Each detector reads the change (added and removed lines, plus the new file text where structure
matters) and returns findings in the 4-part format. Called from diffcheck.inspect with:
  view   - the change with minified/generated/vendored files emptied and lines capped
  change - the full change (paths, statuses, old/new text)
Python 3.8+ standard library only.
"""

import ast
import os
import re

from common import (JS_EXT, PY_EXT, base_of, ext_of, finding, is_comment_line, is_doc, is_test_path, path_tokens,
                    posix, read_text, stem_word, task_words, tree_files_with)
import diffcheck as DC

ERROR_TASK_RE = re.compile(r"\b(raises?|raising|throws?|throwing|errors?|exceptions?|rejects?|invalid|unknown|fails?|failing|"
                           r"validat\w*|exits? (?:with )?(?:code|status)|must not (?:accept|allow))\b", re.I)


def _added_set(f):
    return set(ln for ln, _ in f.added)


def _new_lines_text(change, f):
    txt = change.new_text(f.path)
    return (txt or "").splitlines()


def _indent(s):
    return len(s) - len(s.lstrip(" \t"))


# ---------------------------------------------------------------------------
# Swallowed exceptions (cause 13)
# ---------------------------------------------------------------------------

PY_EXCEPT_RE = re.compile(r"^(\s*)except\b\s*(.*?)\s*:\s*(.*)$")
JS_CATCH_RE = re.compile(r"\bcatch\s*(?:\(\s*[\w$]*\s*(?::\s*\w+)?\s*\))?\s*\{(.*)$")
JS_PROMISE_CATCH_RE = re.compile(r"\.catch\s*\(\s*(?:\(\s*[\w$]*\s*\)|[\w$]+)\s*=>\s*(\{\s*\}|null|undefined|\[\]|\{\}|0|false|''|\"\")\s*\)|"
                                 r"\.catch\s*\(\s*(?:noop|\(\)\s*=>\s*\{\s*\})\s*\)")
LITERAL_RET_RE = re.compile(r"^return\s+(None|null|undefined|0|0\.0|-1|False|false|True|true|''|\"\"|\[\]|\{\}|\(\)|[\w.]+\(\))\s*;?\s*$|^return\s*;?\s*$")


def swallowed_exceptions(view, change, task):
    out = []
    err_task = bool(task and ERROR_TASK_RE.search(task))
    for f in view.files:
        p = f.path
        if f.binary or f.skip or f.status == "D" or not f.added or not DC._source_file(p):
            continue
        e = ext_of(p)
        added = _added_set(f)
        hits = []  # (ln, text, kind, tier)
        if e in PY_EXT:
            lines = _new_lines_text(change, f)
            for i, line in enumerate(lines, 1):
                m = PY_EXCEPT_RE.match(line)
                if not m or i not in added:
                    continue
                clause = m.group(2).strip()
                broad = clause in ("", "Exception", "BaseException") or bool(re.match(r"^\(?\s*(Exception|BaseException)\b", clause)) \
                    or re.match(r"^(Exception|BaseException)\s+as\s+\w+$", clause) is not None
                body, comment = [], False
                if m.group(3).strip():
                    body = [m.group(3).strip()]
                else:
                    base = len(m.group(1))
                    for nxt in lines[i:i + 6]:
                        if not nxt.strip():
                            continue
                        if _indent(nxt) <= base:
                            break
                        if nxt.strip().startswith("#"):
                            comment = True
                            continue
                        body.append(nxt.strip())
                if not body:
                    continue
                if len(body) == 1 and body[0] in ("pass", "...", "continue", "return", "return None"):
                    tier = "problem" if broad and not comment else "check"
                    hits.append((i, line, "`except %s: %s`" % (clause or "", body[0]), tier))
                elif len(body) == 1 and LITERAL_RET_RE.match(body[0]) and broad:
                    hits.append((i, line, "`except %s: %s`" % (clause, body[0]), "problem" if err_task and not comment else "check"))
        elif e in JS_EXT:
            lines = _new_lines_text(change, f)
            for i, line in enumerate(lines, 1):
                if i not in added:
                    continue
                s = DC.strip_strings_comments(line, e)
                m = JS_PROMISE_CATCH_RE.search(s)
                if m:
                    hits.append((i, line, "`.catch(...)` that drops the error", "problem" if err_task else "check"))
                    continue
                m = JS_CATCH_RE.search(line)
                if not m:
                    continue
                rest = m.group(1)
                body, comment = [], False
                if "}" in rest:
                    inner = rest.split("}", 1)[0].strip()
                    if inner.startswith("//") or inner.startswith("/*"):
                        comment = True
                        inner = ""
                    body = [inner] if inner else []
                    closed = True
                else:
                    closed = False
                    for nxt in lines[i:i + 6]:
                        st = nxt.strip()
                        if not st:
                            continue
                        if st.startswith("}"):
                            closed = True
                            break
                        if st.startswith(("//", "/*", "*")):
                            comment = True
                            continue
                        body.append(st)
                if not closed:
                    continue
                if not body:
                    hits.append((i, line, "empty `catch` block", "check" if comment else "problem"))
                elif len(body) == 1 and LITERAL_RET_RE.match(body[0].rstrip(";") + ";" if body[0].startswith("return") else body[0]):
                    hits.append((i, line, "`catch` that returns `%s`" % body[0].rstrip(";")[:40], "problem" if err_task and not comment else "check"))
        for tier in ("problem", "check"):
            hs = [h for h in hits if h[3] == tier]
            if not hs:
                continue
            out.append(finding(
                13, "Exception swallowed in %s" % p,
                "The change catches an error in %s and %s (%s), so a failure becomes a silent wrong result%s." % (
                    p, "does nothing with it" if any("pass" in h[2] or "empty" in h[2] or "drops" in h[2] for h in hs) else "returns a default",
                    "; ".join(h[2] for h in hs[:3]),
                    "; the task describes error behaviour, which this path now hides" if err_task else ""),
                [DC._ev(p, ln, t) for ln, t, _, _ in hs[:4]],
                "The checks pass because nothing raises any more: invalid input, a bug or an outage is hidden instead of reported, and the "
                "behaviour the task asked for on errors never happens.",
                ["Let the error propagate (or catch only the specific exception you expect and handle it for real); add a test for the failure case."],
                file=p, line=hs[0][0], tier=tier))
    return out


# ---------------------------------------------------------------------------
# Special-casing the test input (cause 13)
# ---------------------------------------------------------------------------

LIT = r"(-?\d+(?:\.\d+)?|'[^'\n]{1,60}'|\"[^\"\n]{1,60}\")"
JS_SPECIAL_RE = re.compile(r"\bif\s*\(\s*(?:[\w$.\[\]'\"]+\s*===?\s*%s|%s\s*===?\s*[\w$.\[\]'\"]+)\s*\)\s*\{?\s*return\s+%s" % (LIT, LIT, LIT))
PY_SPECIAL_RE = re.compile(r"\bif\s+(?:[\w.\[\]'\"]+\s*==\s*%s|%s\s*==\s*[\w.\[\]'\"]+)\s*:\s*return\s+%s" % (LIT, LIT, LIT))
PY_SPECIAL_HEAD_RE = re.compile(r"^\s*if\s+(?:[\w.\[\]'\"]+\s*==\s*%s|%s\s*==\s*[\w.\[\]'\"]+)\s*:\s*$" % (LIT, LIT))
TRIVIAL_LITS = {"0", "1", "-1", "2", "10", "100", "''", '""', "0.0", "1.0"}


def _distinctive(lit):
    if lit in TRIVIAL_LITS:
        return False
    if lit[0] in "'\"":
        return len(lit) >= 5
    return "." in lit or len(lit.lstrip("-")) >= 3


def _lit_in(lit, text):
    if lit[0] in "'\"":
        return lit[1:-1] in text
    return re.search(r"(?<![\w.])%s(?![\w])" % re.escape(lit), text) is not None


def special_casing(view, change, task):
    out = []
    test_text = None
    for f in view.files:
        p = f.path
        if f.binary or f.skip or f.status == "D" or not f.added or not DC._source_file(p):
            continue
        e = ext_of(p)
        hits = []
        adds = list(f.added)
        for idx, (ln, t) in enumerate(adds):
            m = None
            if e in JS_EXT:
                m = JS_SPECIAL_RE.search(t)
            elif e in PY_EXT:
                m = PY_SPECIAL_RE.search(t)
                if not m and PY_SPECIAL_HEAD_RE.match(t) and idx + 1 < len(adds):
                    m2 = re.match(r"^\s*return\s+%s\s*$" % LIT, adds[idx + 1][1])
                    if m2:
                        m = PY_SPECIAL_RE.search(t.rstrip() + " return " + m2.group(1))
            if not m:
                continue
            lits = [g for g in m.groups() if g]
            if len(lits) < 2:
                continue
            inp, outp = lits[0], lits[-1]
            if not (_distinctive(inp) and _distinctive(outp)):
                continue
            if test_text is None:
                parts = [change.new_text(g.path) or "" for g in change.files if is_test_path(g.path) and g.status != "D"]
                test_text = "\n".join(parts) + "\n" + (task or "")
            if _lit_in(inp, test_text) and _lit_in(outp, test_text):
                hits.append((ln, t, inp, outp))
                continue
            raw = inp[1:-1] if inp[0] in "'\"" else inp
            for rel in (tree_files_with(change.repo, [raw], limit=50) or []):
                if is_test_path(rel):
                    tt = read_text(os.path.join(change.repo, rel), 1024 * 1024) or ""
                    if _lit_in(inp, tt) and _lit_in(outp, tt):
                        hits.append((ln, t, inp, outp))
                        break
        if hits:
            out.append(finding(
                13, "Special case for a test input in %s" % p,
                "The change in %s returns a fixed answer for exactly the input the tests (or the task) use: %s." % (
                    p, "; ".join("`%s` -> `%s`" % (i, o) for _, _, i, o in hits[:3])),
                [DC._ev(p, ln, t) for ln, t, _, _ in hits[:3]],
                "The test passes because the code recognises the test case, not because the logic is right; every other input still gets the old behaviour.",
                ["Remove the special case and fix the general calculation, then add a second test with a different input."],
                file=p, line=hits[0][0]))
    return out


# ---------------------------------------------------------------------------
# Tests that cannot fail: tautologies, the function under test redefined, real code stubbed out (cause 6)
# ---------------------------------------------------------------------------

TAUTOLOGY_RE = re.compile(
    r"\bassert(?:\.ok)?\s*\(\s*(?:true|1|!0)\s*[,)]|\bexpect\s*\(\s*(true|1|null|undefined|'[^']*'|\"[^\"]*\")\s*\)\s*\.\s*(?:toBe|toEqual|toStrictEqual)\s*\(\s*\1\s*\)|"
    r"\bexpect\s*\(\s*true\s*\)\s*\.toBeTruthy\s*\(\s*\)|\bassert\s+(?:True|1)\s*(?:#.*)?$|self\.assertTrue\s*\(\s*(?:True|1)\s*\)|"
    r"self\.assert(?:Equal|Equals)\s*\(\s*(\d+|True|None|'[^']*')\s*,\s*\2\s*\)|\bassert\s+(\d+|True|'[^']*')\s*==\s*\3\s*$|"
    r"\bassert\.(?:strictEqual|equal|deepEqual|deepStrictEqual)\s*\(\s*(\d+|true|'[^']*')\s*,\s*\4\s*[,)]")
LOCAL_DEF_RE = re.compile(r"^\s*(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s+)?(?:\([^)]*\)|[\w$]+)\s*=>|"
                          r"^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(|^\s*def\s+([A-Za-z_]\w*)\s*\(")
CONST_BODY_RE = re.compile(r"=>\s*(?:-?\d[\d_.]*|'[^']*'|\"[^\"]*\"|true|false|null|undefined|\[\s*\]|\{\s*\})\s*[;,)]?\s*(?://.*)?$|"
                           r"\breturn\s+(?:-?\d[\d_.]*|'[^']*'|\"[^\"]*\"|True|False|None|true|false|null)\s*;?\s*\}?\s*(?://.*|#.*)?$")
STUB_ARROW_RE = re.compile(r"(?<![\w$.])([A-Za-z_$][\w$]*)\s*:\s*(?:\([^()]*\)|[\w$]+)\s*=>\s*([-+*/()\d_.\s]+|'[^']*'|\"[^\"]*\"|true|false|null)\s*(?=[,}\n])")
STUB_LAMBDA_RE = re.compile(r"(?<![\w.])([A-Za-z_]\w*)\s*=\s*lambda[^:]*:\s*([-+*/()\d_.\s]+|'[^']*'|\"[^\"]*\"|True|False|None)\s*(?=[,)\n])")


def _defined_in_source(repo, name, skip_paths=()):
    files = tree_files_with(repo, [name], skip_paths, limit=200) or []
    rx = re.compile(r"(?:function\s*\*?\s*%s\s*\(|(?:const|let|var)\s+%s\s*=|def\s+%s\s*\(|export\s*\{[^}]*\b%s\b|"
                    r"exports\.%s\s*=)" % ((re.escape(name),) * 5))
    for rel in files:
        if is_test_path(rel) or ext_of(rel) not in (JS_EXT | PY_EXT):
            continue
        if rx.search(read_text(os.path.join(repo, rel), 1024 * 1024) or ""):
            return rel
    return None


def fake_tests(view, change, task, skip_paths=()):
    out = []
    for f in view.files:
        p = f.path
        if f.binary or f.skip or f.status == "D" or not f.added or not is_test_path(p) or ext_of(p) not in (JS_EXT | PY_EXT):
            continue
        fresh = [(ln, t) for ln, t in DC.new_lines(f) if t.strip() and not is_comment_line(t)]
        reasons, ev = [], []
        taut = [(ln, t) for ln, t in fresh if TAUTOLOGY_RE.search(t)]
        if taut:
            reasons.append("%d assertion%s that can never fail" % (len(taut), "" if len(taut) == 1 else "s"))
            ev += [DC._ev(p, ln, t) for ln, t in taut[:2]]
        # the function under test redefined inside the test file
        text = change.new_text(p) or ""
        local = {}
        added_map = dict(f.added)
        for ln, t in fresh:
            m = LOCAL_DEF_RE.match(t)
            if m:
                nm = next(g for g in m.groups() if g)
                if len(nm) >= 3 and not nm.startswith(("mock", "fake", "stub", "make", "build", "create", "setup", "helper", "test", "_")):
                    # only a stand-in that returns a fixed value counts (a local helper that computes is fine)
                    body = t + " " + (added_map.get(ln + 1) or "")
                    if CONST_BODY_RE.search(body):
                        local[nm] = (ln, t)
        for nm, (ln, t) in local.items():
            called = re.search(r"(?:expect|assert\w*|self\.assert\w+)\s*\([^\n]*\b%s\s*\(" % re.escape(nm), text) or \
                re.search(r"\bassert\s+[^\n]*\b%s\s*\(" % re.escape(nm), text)
            imported = re.search(r"import[^\n]*\b%s\b|require\([^\n]*\)[^\n]*\b%s\b|\b%s\b[^\n]*=\s*require\(" % ((re.escape(nm),) * 3), text)
            if not called or imported:
                continue
            src = _defined_in_source(change.repo, nm, set(skip_paths) | {p})
            if src:
                reasons.append("it defines its own `%s` instead of testing the one in %s" % (nm, src))
                ev.append(DC._ev(p, ln, t))
        # real code stubbed out: an injected option that replaces a real default function with a constant
        stubs = []
        for ln, t in fresh:
            for rx in (STUB_ARROW_RE, STUB_LAMBDA_RE):
                for m in rx.finditer(t):
                    stubs.append((ln, t, m.group(1), m.group(2).strip()))
        if stubs:
            src_text = "\n".join(change.new_text(g.path) or "" for g in change.files
                                 if g.status != "D" and not g.binary and DC._source_file(g.path))
            for ln, t, nm, val in stubs:
                m = re.search(r"(?<![\w$.])%s\s*(?:=|\?\?|\|\||\bor\b)\s*([A-Za-z_$][\w$]*)\b" % re.escape(nm), src_text)
                if not m:
                    continue
                real = m.group(1)
                if real in ("None", "null", "undefined", "true", "false", "True", "False") or not re.search(
                        r"(?:function\s+%s\b|def\s+%s\b|import[^\n]*\b%s\b|(?:const|let)\s+%s\s*=)" % ((re.escape(real),) * 4), src_text):
                    continue
                reasons.append("it replaces the real `%s` with a constant (`%s: ... => %s`), so the code it was meant to prove never runs" % (real, nm, val))
                ev.append(DC._ev(p, ln, t))
                break
        if reasons:
            out.append(finding(
                6, "Test cannot fail: %s" % p,
                "In %s %s." % (p, "; ".join(reasons[:3])),
                ev[:5],
                "A green run proves nothing about the real code: the test checks a constant or its own copy of the logic.",
                ["Import and call the real code, assert on its actual result, and stub only external services (network, clock, disk)."],
                file=p, line=(taut or [(None, "")])[0][0]))
    return out


# ---------------------------------------------------------------------------
# Coverage thresholds lowered, timeouts and retries raised (cause 6)
# ---------------------------------------------------------------------------

COV_KEY_RE = re.compile(r"(fail_under|fail-under|cov-fail-under|coverageThreshold|minimum_coverage|min_coverage|"
                        r"check-coverage|\b(?:lines|branches|functions|statements)\b|threshold)\W*?(\d+(?:\.\d+)?)", re.I)
TIMEOUT_KEY_RE = re.compile(r"(testTimeout|test-timeout|jest\.setTimeout|setTimeout|hookTimeout|timeout|retries|retry|retryTimes|"
                            r"reruns|maxRetries|flaky)\W*?(\d+)", re.I)
TEST_CFG_RE = re.compile(r"^(pyproject\.toml|setup\.cfg|tox\.ini|pytest\.ini|\.coveragerc|package\.json|codecov\.ya?ml|"
                         r"(?:jest|vitest|vite|playwright|cypress|karma|mocha|ava|\.mocharc|\.nycrc|\.c8rc)[\w.\-]*|makefile|"
                         r"sonar-project\.properties|phpunit\.xml(?:\.dist)?)$", re.I)


def _is_ci_file(p):
    p = posix(p).lower()
    return (p.startswith(".github/workflows/") and p.endswith((".yml", ".yaml"))) or base_of(p) in (
        ".gitlab-ci.yml", "azure-pipelines.yml", "bitbucket-pipelines.yml", ".travis.yml", "jenkinsfile") or \
        p.startswith((".circleci/", ".buildkite/")) and p.endswith((".yml", ".yaml"))


def thresholds(view, change, task):
    out = []
    for f in view.files:
        p = f.path
        b = base_of(p)
        if f.binary or f.skip or f.status not in ("M", "R"):
            continue
        cfg = bool(TEST_CFG_RE.match(b)) or _is_ci_file(p)
        if not cfg and not is_test_path(p):
            continue
        cov, tmo = [], []
        for h in f.hunks:
            rem = {}
            for _, t in h["removed"]:
                for m in COV_KEY_RE.finditer(t):
                    rem.setdefault(("cov", m.group(1).lower()), float(m.group(2)))
                for m in TIMEOUT_KEY_RE.finditer(t):
                    rem.setdefault(("tmo", m.group(1).lower()), float(m.group(2)))
            for ln, t in h["added"]:
                if not cfg and not re.search(r"setTimeout|retryTimes|retries|timeout", t):
                    continue
                for m in COV_KEY_RE.finditer(t):
                    k = ("cov", m.group(1).lower())
                    if k in rem and float(m.group(2)) < rem[k] and (cfg and ("cov" in t.lower() or "fail" in t.lower() or
                                                                          re.search(r"coverage|nyc|c8|jest|vitest", b + (change.new_text(p) or "")[:20000], re.I))):
                        cov.append((ln, t, "%s %g -> %s" % (m.group(1), rem[k], m.group(2))))
                for m in TIMEOUT_KEY_RE.finditer(t):
                    k = ("tmo", m.group(1).lower())
                    if k in rem and float(m.group(2)) > rem[k]:
                        tmo.append((ln, t, "%s %g -> %s" % (m.group(1), rem[k], m.group(2))))
        if not cov and cfg:
            for ln, t in f.added:
                if re.search(r"--cov-fail-under[= ]0\b|fail_under\s*=\s*0\b|--no-cov\b|coverage\s*[:=]\s*false", t):
                    cov.append((ln, t, "coverage check switched off"))
        if not tmo and (cfg or is_test_path(p)):
            for ln, t in DC.new_lines(f):
                if re.search(r"--reruns\b|\bretryTimes\s*\(|\bretries\s*[:=]\s*[1-9]|@flaky\b|pytest\.mark\.flaky|--retries[= ][1-9]|"
                             r"jest\.setTimeout\s*\(\s*\d{5,}|testTimeout\s*[:=]\s*\d{5,}", t):
                    tmo.append((ln, t, "retries or a long timeout added"))
        if cov:
            out.append(finding(
                6, "Coverage threshold lowered in %s" % p,
                "The change lowers the coverage the checks require in %s (%s)." % (p, "; ".join(x[2] for x in cov[:3])),
                [DC._ev(p, ln, t) for ln, t, _ in cov[:3]],
                "The coverage gate passes because it asks for less, so new untested code gets through.",
                ["Restore the threshold and add tests for the new code instead."],
                file=p, line=cov[0][0], also=[5]))
        if tmo:
            out.append(finding(
                6, "Test timeout or retries raised in %s" % p,
                "The change gives tests more time or more attempts in %s (%s)." % (p, "; ".join(x[2] for x in tmo[:3])),
                [DC._ev(p, ln, t) for ln, t, _ in tmo[:3]],
                "Retries and longer timeouts can turn a real failure or a hang into a pass that only fails sometimes.",
                ["Find out why the test was slow or flaky and fix that; keep the original timeout and retry settings."],
                file=p, line=tmo[0][0], tier="check"))
    return out


# ---------------------------------------------------------------------------
# Neutered test commands: CI jobs switched off, scripts that cannot fail (cause 5)
# ---------------------------------------------------------------------------

CI_OFF_RE = re.compile(r"^\s*(?:-\s*)?if\s*:\s*(?:false|0|\$\{\{\s*false\s*\}\}|'false'|\"false\")\s*$|^\s*continue-on-error\s*:\s*true\b|"
                       r"^\s*allow_failure\s*:\s*true\b|\|\|\s*(?:true|exit 0|:)\s*(?:$|[;'\"])|\bset \+e\b|--passWithNoTests|"
                       r"--pass-with-no-tests|^\s*when\s*:\s*manual\b|\bexit 0\s*$")
CHECK_STEP_RE = re.compile(r"\b(test|tests|pytest|jest|vitest|mocha|unittest|lint|eslint|ruff|flake8|tsc|typecheck|mypy|check|"
                           r"build|coverage|go test|cargo test|rspec|phpunit)\b", re.I)
SCRIPT_OFF_RE = re.compile(r"\|\|\s*(?:true|exit 0|:)\s*$|\|\|\s*(?:true|exit 0|:)\s*[;)]|\bset \+e\b|^\s*exit 0\s*$|;\s*exit 0\s*$|"
                           r"--passWithNoTests|--pass-with-no-tests|--exit-zero\b|--no-fail\b")
RUNNER_RE = re.compile(r"\b(jest|vitest|mocha|ava|tap|tape|node\s+(?:--[\w-]+\s+)*--test|pytest|unittest|nose2?|tox|nox|go\s+test|"
                       r"cargo\s+test|rspec|rake|phpunit|pest|dotnet\s+test|mvn|gradle|gradlew|deno\s+test|bun\s+test|"
                       r"playwright|cypress|karma|jasmine|uvu|lab|c8|nyc|make|turbo|nx|lerna|run-tests|test\.(?:sh|py|js|mjs))\b|"
                       r"(?:^|\s)(?:\./)?(?:scripts|bin|tools)/\S+|\b(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?test", re.I)
ECHO_ONLY_RE = re.compile(r"^\s*(?:(?:echo|printf|true|:|exit\s+0)\b[^&|;]*(?:&&|;|\|\||$)\s*)+$")


def neutered_commands(view, change, task, test_runs=()):
    out = []
    referenced = " ".join(exp for _, exp, _ in (test_runs or ())) + " " + " ".join(d for d, _, _ in (test_runs or ()))
    for f in view.files:
        p = f.path
        b = base_of(p).lower()
        if f.binary or f.skip or f.status == "D":
            continue
        if _is_ci_file(p):
            off = [(ln, t) for ln, t in DC.new_lines(f) if CI_OFF_RE.search(t) and not t.strip().startswith("#")]
            removed_steps = [(ln, t) for ln, t in f.removed if CHECK_STEP_RE.search(t) and re.search(r"\brun\s*:|script\s*:|^\s*-\s+\S", t)
                             and not t.strip().startswith("#")]
            added_norm = set(re.sub(r"\s+", " ", t.strip()) for _, t in f.added)
            removed_steps = [(ln, t) for ln, t in removed_steps if re.sub(r"\s+", " ", t.strip()) not in added_norm]
            if f.status in ("M", "R") and (off or removed_steps):
                ev = [DC._ev(p, ln, t) for ln, t in off[:3]] + ["removed %s" % DC._ev(p, ln, t) for ln, t in removed_steps[:2]]
                out.append(finding(
                    5, "CI check switched off in %s" % p,
                    "The change makes a CI check unable to fail the build in %s (%s)." % (
                        p, ", ".join(sorted(set(("`%s`" % t.strip()[:40]) for _, t in off[:3]))) or "test or lint steps removed"),
                    ev, "CI goes green while the tests or lint it runs fail, so broken code can be merged.",
                    ["Restore the CI job as it was; fix the failing check instead of muting it."],
                    file=p, line=(off or removed_steps)[0][0], also=[6]))
            continue
        shell = ext_of(p) in (".sh", ".bash") or b in ("makefile", "justfile") or \
            ((change.new_text(p) or "")[:40].startswith("#!") and re.search(r"sh\b", (change.new_text(p) or "")[:40]) is not None and ext_of(p) == "")
        if shell and f.status in ("M", "R", "A"):
            hits = [(ln, t) for ln, t in DC.new_lines(f) if SCRIPT_OFF_RE.search(t) and not t.strip().startswith("#")]
            if b in ("makefile", "justfile"):
                for ln, t in DC.new_lines(f):
                    m = re.match(r"^\t?\s*(.+?)\s*\|\|\s*(.+?)\s*$", t)
                    if m and m.group(1).strip() == m.group(2).strip() and CHECK_STEP_RE.search(m.group(1)):
                        out.append(finding(
                            6, "Test command retried in %s" % p,
                            "The change runs the same check twice in %s (`A || A`), so a check that fails once and passes on retry counts as passing." % p,
                            [DC._ev(p, ln, t)], "A flaky or order-dependent failure is hidden instead of fixed.",
                            ["Run the check once and fix whatever makes it fail intermittently."],
                            file=p, line=ln, tier="check"))
                        break
            if hits and f.status != "A":
                used = base_of(p) in referenced or p in referenced or b in ("makefile",) or re.search(r"test|check|lint|ci", b)
                out.append(finding(
                    5, "Script can no longer fail: %s" % p,
                    "The change makes %s ignore failures (%s)%s." % (
                        p, ", ".join(sorted(set("`%s`" % SCRIPT_OFF_RE.search(t).group(0).strip() for _, t in hits[:3]))),
                        ", and the project's test command runs it" if used else ""),
                    [DC._ev(p, ln, t) for ln, t in hits[:3]],
                    "The test run reports success whatever happens inside it, so failing tests pass.",
                    ["Remove the failure-masking and let the command's exit code through."],
                    file=p, line=hits[0][0], tier="problem" if used else "check", also=[6]))
            continue
        if b == "package.json" and f.status in ("M", "R"):
            old = DC.load_json_text(change.old_text(f.old_path) or "") or {}
            new = DC.load_json_text(change.new_text(p) or "") or {}
            os_ = (old.get("scripts") or {}) if isinstance(old, dict) else {}
            ns_ = (new.get("scripts") or {}) if isinstance(new, dict) else {}
            for k in ("test", "test:unit", "test:ci", "check", "ci"):
                ov, nv = os_.get(k), ns_.get(k)
                if not isinstance(ov, str) or ov == nv:
                    continue
                if nv is None or (RUNNER_RE.search(ov) and not RUNNER_RE.search(nv or "")) or ECHO_ONLY_RE.match(nv or ""):
                    out.append(finding(
                        5, "Test command no longer runs tests: package.json scripts.%s" % k,
                        "The change replaces scripts.%s `%s` with %s, which does not run the test runner." % (
                            k, ov[:80], "nothing (deleted)" if nv is None else "`%s`" % nv[:80]),
                        ["%s: scripts.%s was `%s`, now %s" % (p, k, ov[:80], "deleted" if nv is None else "`%s`" % nv[:80])],
                        "`npm test` succeeds without running a single test, so every check and CI run is green regardless of the code.",
                        ["Restore the original test script and run the full suite."],
                        file=p, also=[6]))
                    break
    return out


# ---------------------------------------------------------------------------
# Schema changed without a migration (cause 12, check tier)
# ---------------------------------------------------------------------------

def schema_without_migration(view, change, task):
    out = []
    added_paths = [g.path for g in change.files if g.status in ("A", "R")]
    for f in view.files:
        p = f.path
        b = base_of(p).lower()
        if f.binary or f.status not in ("M", "A") or is_test_path(p):
            continue
        kind, mig_dirs, cmd = None, [], None
        d = os.path.dirname(p)
        if b == "schema.prisma" and any(re.search(r"^\s+\w+\s+\w+", t) for _, t in f.added):
            kind, mig_dirs, cmd = "Prisma schema", [os.path.join(d, "migrations")], "npx prisma migrate dev --name <change>"
        elif (b == "models.py" or "/models/" in "/" + p) and ext_of(p) == ".py" and any(re.search(r"=\s*models\.\w+(?:Field|Key)\b|\bColumn\s*\(|mapped_column\s*\(", t) for _, t in f.added):
            app = d if b == "models.py" else d.rsplit("/models", 1)[0]
            mig_dirs = [os.path.join(app, "migrations"), "alembic/versions", "migrations/versions", os.path.join(app, "alembic", "versions")]
            kind, cmd = "model fields", "python manage.py makemigrations (Django) or alembic revision --autogenerate (SQLAlchemy)"
        elif posix(p).endswith("db/schema.rb"):
            kind, mig_dirs, cmd = "Rails schema", [os.path.join(os.path.dirname(d), "db", "migrate"), "db/migrate"], "bin/rails generate migration <Name>"
        elif ext_of(p) in (".ts", ".js") and re.search(r"schema", b) and any(re.search(r"\b(?:pgTable|mysqlTable|sqliteTable)\b|\b(?:integer|text|varchar|boolean|timestamp)\s*\(", t) for _, t in f.added):
            kind, mig_dirs, cmd = "Drizzle schema", ["drizzle", "migrations", os.path.join(d, "migrations"), "drizzle/migrations"], "npx drizzle-kit generate"
        if not kind:
            continue
        mig_dirs = [posix(x).strip("/") for x in mig_dirs]
        existing = [x for x in mig_dirs if x and os.path.isdir(os.path.join(change.repo, x))]
        if not existing:
            continue
        if any(any(ap.startswith(x + "/") for x in existing) for ap in added_paths):
            continue
        out.append(finding(
            12, "Schema changed without a migration: %s" % p,
            "The change edits the %s in %s, but adds no new file under %s." % (kind, p, ", ".join(x + "/" for x in existing)),
            ["%s (+%d/-%d lines)" % (p, len(f.added), len(f.removed)), "no new migration in %s" % ", ".join(existing)],
            "Code and tests use the new schema, but existing databases never get it: the app breaks in production on the first query that touches it.",
            ["Generate a migration for the change (`%s`) and include it." % cmd],
            file=p, tier="check"))
    return out


# ---------------------------------------------------------------------------
# Conflict markers (cause 13)
# ---------------------------------------------------------------------------

def conflict_markers(view, change, task):
    out = []
    for f in view.files:
        if f.binary or f.skip or f.status == "D":
            continue
        starts = [(ln, t) for ln, t in f.added if re.match(r"^<{7}(?: |$)", t)]
        ends = [(ln, t) for ln, t in f.added if re.match(r"^>{7}(?: |$)", t)]
        if starts and ends:
            out.append(finding(
                13, "Merge conflict markers left in %s" % f.path,
                "%s still contains %d unresolved merge conflict%s (`<<<<<<<` / `=======` / `>>>>>>>`)." % (
                    f.path, len(starts), "" if len(starts) == 1 else "s"),
                [DC._ev(f.path, ln, t) for ln, t in (starts[:2] + ends[:1])],
                "The file does not parse (or ships both versions of the code); anything that imports it breaks.",
                ["Resolve each conflict by hand, keep the right version, delete the markers and rerun the checks."],
                file=f.path, line=starts[0][0]))
    return out


# ---------------------------------------------------------------------------
# Hardcoded return that ignores its argument (cause 13)
# ---------------------------------------------------------------------------

def _py_const_value(node):
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.UnaryOp) and isinstance(node.operand, ast.Constant):
        return True
    if isinstance(node, ast.Name) and re.match(r"^[A-Z][A-Z0-9_]*$", node.id):
        return True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("Decimal", "float", "int", "str", "dict", "list", "set", "tuple") \
            and all(_py_const_value(a) for a in node.args) and not node.keywords:
        return True
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)) and not node.elts:
        return True
    if isinstance(node, ast.Dict) and not node.keys:
        return True
    return False


def hardcoded_returns(view, change, task):
    out = []
    tw = task_words(task or "")
    lookup_task = bool(task and re.search(r"\b(look ?up|by (?:the )?\w+|per \w+|from (?:the )?(?:data|file|table|config|database)|depend\w* on)\b", task, re.I))
    for f in view.files:
        p = f.path
        if f.binary or f.skip or f.status == "D" or not f.added or not DC._source_file(p) or ext_of(p) not in PY_EXT:
            continue
        added = _added_set(f)
        try:
            tree = ast.parse(change.new_text(p) or "")
        except (SyntaxError, ValueError):
            continue
        hits = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or node.name.startswith("__"):
                continue
            span = set(range(node.lineno, getattr(node, "end_lineno", node.lineno) + 1))
            if not (span & added):
                continue
            decos = [getattr(d, "id", getattr(d, "attr", "")) for d in node.decorator_list]
            if set(decos) & {"abstractmethod", "property", "overload", "staticmethod", "classmethod", "cached_property"}:
                continue
            params = [a.arg for a in node.args.args + getattr(node.args, "kwonlyargs", []) if a.arg not in ("self", "cls") and not a.arg.startswith("_")]
            if not params:
                continue
            body = list(node.body)
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                body = body[1:]
            if len(body) != 1 or not isinstance(body[0], ast.Return) or body[0].value is None or not _py_const_value(body[0].value):
                continue
            used = set(n.id for n in ast.walk(body[0]) if isinstance(n, ast.Name))
            if used & set(params):
                continue
            hits.append((node.lineno, node.name, params))
        for ln, name, params in hits:
            named = any(stem_word(x) in tw or x in tw for x in params) or name.lower() in tw
            tier = "problem" if (named and lookup_task) else "check"
            out.append(finding(
                13, "Hardcoded result in %s: `%s` ignores %s" % (p, name, ", ".join("`%s`" % x for x in params[:3])),
                "`%s(%s)` in %s returns the same fixed value whatever it is given; %s never used%s." % (
                    name, ", ".join(params), p, ", ".join("`%s`" % x for x in params[:3]) + (" is" if len(params) == 1 else " are"),
                    "; the task says the result depends on it" if tier == "problem" else ""),
                [DC._ev(p, ln, "def %s(%s): return <constant>" % (name, ", ".join(params)))],
                "The tests pass for the one value the constant happens to match; every other input gets a wrong answer.",
                ["Implement the lookup or calculation the task describes (read the data it names) and test it with a second, different input."],
                file=p, line=ln, tier=tier))
    return out


# ---------------------------------------------------------------------------
# Golden / expected-output files rewritten (cause 6)
# ---------------------------------------------------------------------------

GOLDEN_DIR_RE = re.compile(r"(?:^|/)(?:golden|goldens|__golden__|expected|expectations|approved|baselines?)(?:/|$)", re.I)
GOLDEN_NAME_RE = re.compile(r"[._\-](?:golden|expected|approved|baseline)[._\-]|\.(?:golden|expected|approved)$|^expected[._\-]|\.out$", re.I)


def golden_files(view, change, task):
    out = []
    tw = task_words(task or "")
    task_golden = bool(task and re.search(r"\b(golden|expected (?:output|files?)|baselines?|approved|fixtures?|regenerat\w*|re-?record)\b", task, re.I))
    src_changed = any(DC._source_file(g.path) for g in change.files if g.status != "D")
    for f in view.files:
        p = f.path
        if f.binary or f.status not in ("M", "D", "R") or DC.is_snapshot(p):
            continue
        if not (is_test_path(p) or "/testdata/" in "/" + p.lower() or "/fixtures/" in "/" + p.lower()):
            continue
        if not (GOLDEN_DIR_RE.search(posix(p)) or GOLDEN_NAME_RE.search(base_of(p))):
            continue
        if ext_of(p) in (JS_EXT | PY_EXT):
            continue
        added = " ".join(t for _, t in f.added)
        removed = " ".join(t for _, t in f.removed)
        bad = sorted(set(DC.BAD_OUTPUT_RE.findall(added)) - set(DC.BAD_OUTPUT_RE.findall(removed)))
        toks = set(stem_word(t) for t in path_tokens(p) if len(t) >= 3 and t not in ("test", "tests", "golden", "expected", "fixtures", "approved", "out"))
        named = bool(toks & tw)
        expl = set(stem_word(w) for w in re.findall(r"[A-Za-z]{4,}", added)) & tw
        if f.status == "D" or bad:
            tier = "problem"
        elif named or (task_golden and expl):
            tier = "check"
        elif not src_changed:
            tier = "check"
        else:
            tier = "problem"
        out.append(finding(
            6, "Expected-output file rewritten: %s" % p,
            "The change %s %s (+%d/-%d lines) together with the code it checks%s." % (
                "deletes" if f.status == "D" else "rewrites", p, len(f.added), len(f.removed),
                (", and the new expectations contain %s" % ", ".join("`%s`" % x for x in bad)) if bad else
                ("" if tier == "check" else ", and the task does not ask for this output to change")),
            [DC._ev(p, ln, t) for ln, t in f.added[:2]] + ["removed %s" % DC._ev(p, ln, t) for ln, t in f.removed[:2]],
            "Regenerating expected output from whatever the code now prints makes the test pass by definition; a bug in the new output becomes the new expectation.",
            ["Check every changed line against the task by hand. Restore lines whose change the task did not ask for and fix the code instead."],
            file=p, tier=tier))
    return out


def check_fakes(view, change, task, test_runs=(), skip_paths=()):
    fs = []
    fs += swallowed_exceptions(view, change, task)
    fs += special_casing(view, change, task)
    fs += fake_tests(view, change, task, skip_paths)
    fs += thresholds(view, change, task)
    fs += neutered_commands(view, change, task, test_runs)
    fs += schema_without_migration(view, change, task)
    fs += conflict_markers(view, change, task)
    fs += hardcoded_returns(view, change, task)
    fs += golden_files(view, change, task)
    return fs
