#!/usr/bin/env python3
"""Change inspection for Prove It Works (causes 5-17 from the cause list).

Looks only at the change (working tree vs a base ref): added and removed lines,
added, deleted and renamed files. Every finding uses the 4-part format
(Finding, Evidence, Impact, Fix) and carries the cause numbers it maps to.

Tiers: "problem" blocks PROVEN; "check" is listed for Claude to read and decide.

Usage (standalone): python3 diffcheck.py <repo> [--base REF] [--task-file F] [--json]
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (BINARY_EXT, CODE_EXT, DOC_EXT, JS_EXT, JS_LOCKS, LOCKFILES, PY_EXT,  # noqa: E402
                    SECRET_PATTERNS, SKIP_DIRS, TS_EXT, FileChange, base_of, content_skip_reason, ext_of, finding,
                    generated_marker, glob_match, is_cli_path,
                    is_comment_line, is_doc, is_env_file, is_env_template, is_lockfile,
                    is_manifest, is_migration, is_snapshot, is_test_path, load_json_text,
                    load_toml, path_tokens, posix, read_text, redact, run_git, split_ident,
                    stem_word, strip_strings_comments, task_paths, task_words, tree_files_with, tree_has)

REMOVAL_WORDS_RE = re.compile(r"\b(remove|removing|delete|deleting|drop|dropping|deprecate|retire|get rid|clean ?up|rip out)\b", re.I)


def _ev(path, ln, text, n=160):
    t = text.strip()
    if len(t) > n:
        t = t[:n - 3] + "..."
    return "%s:%s: %s" % (path, ln, t) if ln else "%s: %s" % (path, t)


def _is_code(path):
    return ext_of(path) in CODE_EXT and not is_doc(path)


def _source_file(path):
    """Production code: a code file that is not a test, fixture, mock, story or seed."""
    if not _is_code(path) or is_test_path(path):
        return False
    parts = set(posix(path).lower().split("/")[:-1])
    if parts & {"mocks", "__mocks__", "fixtures", "__fixtures__", "seeds", "seed", "stories", "storybook",
                "examples", "example", "demo", "testdata", "test-utils", "testutils", "e2e"}:
        return False
    b = base_of(path).lower()
    if ".stories." in b or b.startswith(("seed", "mock", "fake", "fixture")):
        return False
    return True


# ---------------------------------------------------------------------------
# Cause 5 and 6: focused, skipped, deleted and weakened tests
# ---------------------------------------------------------------------------

FOCUS_RE = re.compile(
    r"\b(?:describe|it|test|context|suite|specify)\.only\s*\(|\b(?:fit|fdescribe|fcontext)\s*\(\s*['\"`]|"
    r"@pytest\.mark\.only\b|\{\s*only\s*:\s*true\s*\}")
SKIP_RE = re.compile(
    r"\b(?:describe|it|test|context|suite|specify)\.skip\s*\(\s*(?:['\"`]|\)|true\b)|\b(?:xit|xdescribe|xtest|xcontext|xspecify)\s*\(|"
    r"@unittest\.skip\b(?!If|Unless)|@(?:pytest\.)?mark\.skip\b(?!if)|\bpytest\.skip\s*\(|self\.skipTest\s*\(|"
    r"\bt\.Skip(?:Now|f)?\s*\(|#\[ignore\]|@Disabled\b|@Ignore\b|\{\s*skip\s*:\s*(?:true|['\"`])|"
    r"@(?:pytest\.)?mark\.xfail\b|\b(?:it|test)\.todo\s*\(|\bunittest\.expectedFailure\b")
COND_SKIP_RE = re.compile(r"@unittest\.skip(?:If|Unless)\b|@pytest\.mark\.skipif\b|\.skipIf\s*\(|\.runIf\s*\(|"
                          r"\b(?:describe|it|test)\.skip\s*\(\s*(?!['\"`)]|true\b)[^\s)]")
CONST_SKIP_RE = re.compile(r"(?:\.skipIf|skipIf|\bskipif|skip_if)\s*\(\s*(?:True|true|1|!0|['\"]True['\"]|not\s+False)\s*[,)]|"
                           r"(?:skipUnless|\.runIf|run_if)\s*\(\s*(?:False|false|0|None|null)\s*[,)]|"
                           r"\bskip\s*:\s*(?:true|1)\b|@pytest\.mark\.skipif\s*\(\s*(?:True|1|['\"]True['\"])")
TEST_DECL_RE = re.compile(r"\b(?:it|test|specify)\s*\(\s*['\"`]|^\s*(?:async\s+)?def\s+test_?\w*\s*\(|^\s*func\s+Test\w+\(|#\[test\]")
ASSERT_RE = re.compile(
    r"\bexpect\s*\(|\bassert(?:_\w+)?\s*[\.(]|\bassert\s+\S|self\.assert\w+\s*\(|\bshould\.\w|\.should\.|"
    r"\bt\.(?:equal|deepEqual|is|ok|true|false|throws|notThrows|like|match|strictEqual|deepStrictEqual)\s*\(|"
    r"\bassert(?:Equals?|True|False|That|Null|NotNull|Throws)\s*\(|\brequire\.\w+\s*\(t,|\bassert!\s*\(|\bassert_eq!\s*\(")
STRICT_RE = re.compile(
    r"\.toBe\s*\((?!\s*\))|\.toEqual\s*\(|\.toStrictEqual\s*\(|\.toMatchObject\s*\(|\.toHaveBeenCalledWith\s*\(|"
    r"\.toThrow\s*\(\s*\S|\.toHaveLength\s*\(|\.toContain\s*\(|strictEqual\s*\(|deepStrictEqual\s*\(|deepEqual\s*\(|"
    r"\bassert\.equal\s*\(|\.assertEqual\s*\(|\.assertEquals\s*\(|\.assertDictEqual|\.assertListEqual|\.assertRaises\s*\(\s*\w|"
    r"\.assertIn\s*\(|\bassert\s+[^#\n]*?(?:==|!=|\bis\b|\bin\b)|assert_eq!|t\.(?:equal|deepEqual|is)\s*\(|\.to\.(?:equal|eql|deep)")
LOOSE_RE = re.compile(
    r"\.toBeTruthy\s*\(|\.toBeDefined\s*\(|\.toBeFalsy\s*\(|\.not\.toBeNull\s*\(|\.not\.toBeUndefined\s*\(|"
    r"\.toBeGreaterThan(?:OrEqual)?\s*\(\s*-?0\s*\)|\.toThrow\s*\(\s*\)|\.toHaveBeenCalled\s*\(\s*\)|expect\.anything\(|"
    r"\bassert\.ok\s*\(|\bassert\s*\(\s*[^,)]+\)|\.assertTrue\s*\(|\.assertIsNotNone\s*\(|\.assertFalse\s*\(|"
    r"\bassert\s+(?![^#\n]*(?:==|!=|\bis\b|\bin\b|<|>))[\w.\[\]()]+\s*$|t\.(?:ok|true|truthy)\s*\(|\.to\.be\.ok\b|\.to\.exist\b|"
    r"\.toBeCloseTo\s*\([^,]+,\s*-?[01]\s*\)|\bassert\.match\s*\(|\.toMatch\s*\(\s*/|\bassertRegex(?:pMatches)?\s*\(|"
    r"\.assertRegex(?:pMatches)?\s*\(|\bassert\s+re\.(?:match|search|fullmatch)\s*\(|\.to\.match\s*\(|expect\.stringMatching\s*\(|"
    r"expect\.any\s*\(|\.toBeGreaterThanOrEqual\s*\(\s*0\s*\)|\.toBeLessThan(?:OrEqual)?\s*\(\s*Infinity|>=\s*0\s*\)?\s*;?\s*$")
BAD_OUTPUT_RE = re.compile(r"\bNaN\b|\bundefined\b|\[object Object\]|Invalid Date|\bnull\b|\bInfinity\b|Error:|Traceback")


def _code_content(text):
    return text.strip() and not is_comment_line(text)


def new_lines(f):
    """Added lines that are really new: a line removed and re-added elsewhere (moved,
    re-indented) is not something this change introduced."""
    gone = Counter(t.strip() for _, t in f.removed if t.strip())
    out = []
    for ln, t in f.added:
        k = t.strip()
        if k and gone.get(k, 0) > 0:
            gone[k] -= 1
            continue
        out.append((ln, t))
    return out


def _commented_assert(text):
    """A commented-out assertion: the comment body itself is assertion code, not prose about one."""
    s = text.strip()
    if not is_comment_line(s) or not s.startswith(("//", "#")):
        return False
    body = re.sub(r"^(//+|#+)\s?", "", s).strip()
    return bool(re.match(r"^(?:await\s+)?(?:expect\s*\(|assert(?:\w+)?\s*[.(]|assert\s+\S|self\.assert\w+\s*\(|"
                         r"t\.(?:equal|deepEqual|is|ok|true|false|throws|like|match)\s*\(|\w+\.should\.)", body)) and \
        bool(re.search(r"[);]\s*$|==|!=", body))


def check_tests(change, task):
    out = []
    task = task or ""
    removal_task = bool(REMOVAL_WORDS_RE.search(task))
    tw = task_words(task)
    for f in change.files:
        p = f.path
        test_like = is_test_path(p) and not is_snapshot(p)
        e = ext_of(p)
        if f.binary or f.skip:
            continue
        # focused tests (cause 5)
        if (test_like or e in JS_EXT) and f.status != "D":
            hits = [(ln, t) for ln, t in new_lines(f) if _code_content(t) and FOCUS_RE.search(t)]
            if hits and (test_like or any(re.search(r"\b(describe|it|test)\s*\(", t) for _, t in f.added)):
                out.append(finding(
                    5, "Focused test left in %s" % p,
                    "The change adds %s in %s, so the runner can run only the focused test%s and skip the rest of the suite." % (
                        "a focused test (.only / fit / fdescribe)" if len(hits) == 1 else "%d focused tests" % len(hits), p,
                        "" if len(hits) == 1 else "s"),
                    [_ev(p, ln, t) for ln, t in hits[:4]],
                    "A green run proves almost nothing: every other test in the file or suite silently stops running.",
                    ["Remove `.only` / `fit` / `fdescribe` and run the full suite again."],
                    file=p, line=hits[0][0]))
        if not test_like:
            continue
        if f.status == "D":
            words = set(path_tokens(p)) - {"test", "tests", "spec"}
            asked = removal_task and bool(set(stem_word(w) for w in words) & tw)
            out.append(finding(
                6, "Test file deleted: %s" % p,
                "The change deletes the test file %s (%d lines)%s." % (p, len(f.removed), "; the task asks to remove something related, so confirm this was intended" if asked else ""),
                ["%s (deleted)" % p] + [_ev(p, ln, t) for ln, t in f.removed if TEST_DECL_RE.search(t)][:3],
                "Everything those tests protected is now unprotected, and the suite still passes, so nobody notices.",
                ["Restore %s, or replace it with tests for the new behaviour if the task really removed that feature." % p],
                file=p, tier="check" if asked else "problem"))
            continue
        reasons, ev = [], []
        skips = [(ln, t) for ln, t in new_lines(f) if _code_content(t) and (SKIP_RE.search(t) or CONST_SKIP_RE.search(t))]
        if skips:
            reasons.append("%s skipped" % ("a test is" if len(skips) == 1 else "%d tests are" % len(skips)))
            ev += [_ev(p, ln, t) for ln, t in skips[:3]]
        a_commented = [(ln, t) for ln, t in new_lines(f) if _commented_assert(t)]
        if a_commented:
            reasons.append("%d assertion%s commented out" % (len(a_commented), "" if len(a_commented) == 1 else "s"))
            ev += [_ev(p, ln, t) for ln, t in a_commented[:3]]
        # compare hunk by hunk: a new test elsewhere in the file must not hide a weakened one
        deficit, rem_ev, loose_ev = 0, [], []
        for h in (f.hunks if f.status != "A" else []):
            hr = [(ln, t) for ln, t in h["removed"] if _code_content(t) and ASSERT_RE.search(t)]
            ha = [(ln, t) for ln, t in h["added"] if _code_content(t) and ASSERT_RE.search(t)]
            if len(hr) > len(ha):
                deficit += len(hr) - len(ha)
                added_norm = set(re.sub(r"\s+", "", t) for _, t in ha)
                rem_ev += [(ln, t) for ln, t in hr if re.sub(r"\s+", "", t) not in added_norm]
            s_rem = sum(1 for _, t in h["removed"] if _code_content(t) and STRICT_RE.search(t))
            s_add = sum(1 for _, t in h["added"] if _code_content(t) and STRICT_RE.search(t))
            l_rem = sum(1 for _, t in h["removed"] if _code_content(t) and LOOSE_RE.search(t))
            la = [(ln, t) for ln, t in h["added"] if _code_content(t) and LOOSE_RE.search(t) and not STRICT_RE.search(t)]
            if s_rem > s_add and len(la) > l_rem:
                loose_ev += la
        if deficit:
            reasons.append("%d assertion%s removed" % (deficit, "" if deficit == 1 else "s"))
            ev += ["removed %s" % _ev(p, ln, t) for ln, t in rem_ev[:3]]
        if loose_ev:
            reasons.append("exact assertions replaced with looser ones")
            ev += ["now %s" % _ev(p, ln, t) for ln, t in loose_ev[:3]]
        d_add = sum(1 for _, t in f.added if _code_content(t) and TEST_DECL_RE.search(t))
        d_rem = sum(1 for _, t in f.removed if _code_content(t) and TEST_DECL_RE.search(t))
        if d_rem > d_add and f.status != "A":
            n = d_rem - d_add
            reasons.append("%d test case%s removed" % (n, "" if n == 1 else "s"))
            ev += ["removed %s" % _ev(p, ln, t) for ln, t in f.removed if TEST_DECL_RE.search(t)][:2]
        if reasons:
            tier = "problem"
            if removal_task and not skips and not a_commented:
                tier = "check"
            out.append(finding(
                6, "Tests weakened in %s" % p,
                "In %s the change leaves the tests weaker than before: %s." % (p, "; ".join(reasons)),
                ev[:6],
                "The suite now passes without checking what it used to check, so a green run no longer proves the behaviour works.",
                ["Restore the removed or loosened assertions and un-skip the tests, then make the code pass them. "
                 "If an expectation really changed, assert the new exact value instead of a looser one."],
                file=p, line=(skips or a_commented or [(None, "")])[0][0], tier=tier, also=[5] if skips else []))
        changed_expect = []
        for h in (f.hunks if f.status != "A" else []):
            hr = [t for _, t in h["removed"] if _code_content(t) and STRICT_RE.search(t)]
            ha = [(ln, t) for ln, t in h["added"] if _code_content(t) and STRICT_RE.search(t)]
            if hr and ha and len(hr) == len(ha):
                for (ln, t), old_t in zip(ha, hr):
                    shape_new = re.sub(r"(['\"`]).*?\1|-?\d+(?:\.\d+)?", "#", t).strip()
                    shape_old = re.sub(r"(['\"`]).*?\1|-?\d+(?:\.\d+)?", "#", old_t).strip()
                    if shape_new == shape_old and t.strip() != old_t.strip():
                        changed_expect.append((ln, t, old_t))
        if changed_expect and not reasons:
            out.append(finding(
                6, "Expected values changed in %s" % p,
                "%d existing assertion%s in %s now expect%s a different value." % (
                    len(changed_expect), "" if len(changed_expect) == 1 else "s", p, "s" if len(changed_expect) == 1 else ""),
                ["%s:%s: was `%s`, now `%s`" % (p, ln, o.strip()[:80], t.strip()[:80]) for ln, t, o in changed_expect[:3]],
                "If the task did not ask for the new behaviour, the test was edited to match a bug.",
                ["Check each new expected value against the task. If the task did not change that behaviour, restore the old value and fix the code."],
                file=p, line=changed_expect[0][0], tier="check"))
        cond = [(ln, t) for ln, t in new_lines(f) if COND_SKIP_RE.search(t) and not CONST_SKIP_RE.search(t)]
        if cond:
            out.append(finding(
                6, "Conditional skip added in %s" % p,
                "The change adds a conditional skip in %s." % p, [_ev(p, ln, t) for ln, t in cond[:3]],
                "If the condition is true where the tests run (CI, this machine), the test silently does not run.",
                ["Confirm the condition is a real platform limit, not a way around a failure."],
                file=p, line=cond[0][0], tier="check"))
    # snapshots
    for f in change.files:
        if not is_snapshot(f.path) or f.status not in ("M", "D", "R") or f.binary:
            continue
        added = " ".join(t for _, t in f.added)
        removed = " ".join(t for _, t in f.removed)
        bad = sorted(set(BAD_OUTPUT_RE.findall(added)) - set(BAD_OUTPUT_RE.findall(removed)))
        expl = set(stem_word(w) for w in re.findall(r"[A-Za-z]{4,}", added)) & tw
        mentions = re.search(r"\bsnapshots?\b", task, re.I)
        if f.status == "D" and not mentions:
            tier = "problem"
        elif bad:
            tier = "problem"
        elif mentions or expl:
            tier = "check"
        else:
            tier = "problem"
        out.append(finding(
            6, "Snapshot updated: %s" % f.path,
            "The change %s the snapshot %s (+%d/-%d lines)%s." % (
                "deletes" if f.status == "D" else "rewrites", f.path, len(f.added), len(f.removed),
                (", and the new snapshot contains %s" % ", ".join("`%s`" % b for b in bad)) if bad else
                ("" if (mentions or expl) else ", and nothing in the task asks for different output")),
            [_ev(f.path, ln, t) for ln, t in f.added[:3]] or ["%s (deleted)" % f.path],
            "Updating snapshots to whatever the code now prints turns a failing test into a passing one without checking the output is right.",
            ["Diff the old and new snapshot by eye. If the new output is wrong, restore the snapshot and fix the code; "
             "only re-record when the task asked for the new output."],
            file=f.path, tier=tier))
    # test command weakened (package.json scripts, pytest addopts, jest ignore patterns)
    for f in change.files:
        b = base_of(f.path).lower()
        if f.binary or f.status == "D":
            continue
        weak = []
        if b == "package.json":
            old = load_json_text(change.old_text(f.old_path) or "") or {}
            new = load_json_text(change.new_text(f.path) or "") or {}
            os_ = (old.get("scripts") or {}) if isinstance(old, dict) else {}
            ns_ = (new.get("scripts") or {}) if isinstance(new, dict) else {}
            for k in ("test", "test:unit", "test:ci"):
                if k in os_ and ns_.get(k) != os_.get(k):
                    weak.append(("scripts.%s: `%s` -> `%s`" % (k, os_.get(k), ns_.get(k))))
        for ln, t in f.added:
            if re.search(r"--passWithNoTests|--test-name-pattern|--testNamePattern|--testPathIgnorePatterns|"
                         r"testPathIgnorePatterns|--deselect|--ignore[= ]|(?:^|\s)-k\s|\|\|\s*(?:true|exit 0)|--grep\b|"
                         r"--onlyChanged|--findRelatedTests|--exclude\b", t) and \
                    (b in ("package.json", "pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini", "makefile")
                     or b.startswith(("jest.config", "vitest.config", "vite.config", ".mocharc"))):
                weak.append(_ev(f.path, ln, t))
        if weak:
            loud = any(re.search(r"passWithNoTests|name-pattern|NamePattern|Ignore|deselect|ignore|-k\s|\|\||grep|onlyChanged|findRelated|exclude", w) for w in weak)
            out.append(finding(
                5, "Test command changed in %s" % f.path,
                "The change edits how tests are selected or run in %s." % f.path, weak[:4],
                "A narrowed or forgiving test command can make the suite pass while most tests never run.",
                ["Restore the original test command and run the full suite."],
                file=f.path, tier="problem" if loud else "check", also=[6]))
    return out


# ---------------------------------------------------------------------------
# Cause 5: new test files the project's test command never collects
# ---------------------------------------------------------------------------

TEST_BODY_RE = re.compile(r"\bunittest\.TestCase\b|^\s*(?:async\s+)?def\s+test\w*\s*\(|"
                          r"\b(?:it|test|describe)\s*\(\s*['\"`]|^\s*func\s+Test\w+\(|#\[test\]", re.M)
NODE_TEST_NAME_RE = re.compile(r"^(?:test|test-.+|.+[.\-_]test)\.[cm]?js$")
JEST_NAME_RE = re.compile(r"^.+\.(?:test|spec)\.[cm]?[jt]sx?$")


def _ini_value(text, sections, key):
    cur = None
    val = None
    for line in (text or "").splitlines():
        m = re.match(r"^\s*\[([^\]]+)\]\s*$", line)
        if m:
            cur = m.group(1).strip()
            continue
        if cur in sections:
            m = re.match(r"^\s*%s\s*=\s*(.*)$" % re.escape(key), line)
            if m:
                val = m.group(1).strip()
            elif val is not None and line[:1] in (" ", "\t") and line.strip():
                val += " " + line.strip()
            elif line.strip():
                if val is not None:
                    return val
    return val


def _pytest_files(root):
    for name, sections in (("pytest.ini", ("pytest",)), ("pyproject.toml", ("tool.pytest.ini_options",)),
                           ("setup.cfg", ("tool:pytest",)), ("tox.ini", ("pytest",))):
        txt = read_text(os.path.join(root, name))
        if not txt:
            continue
        v = _ini_value(txt, sections, "python_files")
        if v:
            pats = re.findall(r"[\w*?.\-\[\]]+\.py", v)
            if pats:
                return pats, "%s python_files" % name
    return ["test_*.py", "*_test.py"], "pytest's default python_files"


def _discovery_rules(expanded, root):
    """Turn what a test command really runs into (language, start_dir or None, matcher, description) rules.
    Returns None when the command lists its test files explicitly (nothing to judge)."""
    import fnmatch
    rules = []
    for seg in re.split(r"&&|\|\||;|\n", expanded or ""):
        seg = seg.strip()
        m = re.search(r"-m\s+unittest\b(.*)$", seg)
        if m:
            args = m.group(1).split()
            pos = [a for a in args if not a.startswith("-")]
            if pos and pos[0] != "discover":
                return None
            start, pattern = ".", "test*.py"
            for i, a in enumerate(args):
                if a in ("-s", "--start-directory") and i + 1 < len(args):
                    start = args[i + 1]
                elif a in ("-p", "--pattern") and i + 1 < len(args):
                    pattern = args[i + 1]
            rest = [a for i, a in enumerate(args) if not a.startswith("-") and a != "discover" and
                    not (i > 0 and args[i - 1] in ("-s", "-p", "-t", "--start-directory", "--pattern", "--top-level-directory"))]
            if rest:
                start = rest[0]
                if len(rest) > 1:
                    pattern = rest[1]
            pattern = pattern.strip("'\"")
            rules.append(("py", start.strip("'\"").rstrip("/") or ".", lambda p, pat=pattern: fnmatch.fnmatch(base_of(p), pat),
                          "`unittest discover` only collects files matching `%s`%s" % (pattern, "" if start == "." else " under `%s/`" % start)))
            continue
        m = re.search(r"(?:^|\s|/)pytest\b(.*)$", seg)
        if m and not re.search(r"pytest\.|pytest-", seg[m.start():m.start() + 12]):
            args = m.group(1).split()
            pos = [a for a in args if not a.startswith("-") and not re.match(r"^[\w.]+=", a)]
            if any(a.endswith(".py") or "::" in a for a in pos):
                return None
            pats, src = _pytest_files(root)
            starts = [a.rstrip("/") for a in pos if os.path.isdir(os.path.join(root, a))] or [None]
            for st in starts:
                rules.append(("py", st, lambda p, pats=pats: any(fnmatch.fnmatch(base_of(p), x) for x in pats),
                              "pytest only collects files matching %s (%s)" % (", ".join("`%s`" % x for x in pats), src)))
            continue
        m = re.search(r"\bnode\b(?:\s+--?[\w-]+(?:=\S+)?)*\s+--test\b(.*)$", seg)
        if m:
            args = [a.strip("'\"") for a in m.group(1).split() if not a.startswith("-")]
            if args:
                rules.append(("js", None, lambda p, args=args: any(glob_match(p, a) or p.startswith(a.rstrip("/") + "/") or p == a for a in args),
                              "`node --test` only runs %s" % ", ".join("`%s`" % a for a in args)))
            else:
                rules.append(("js", None, lambda p: bool(NODE_TEST_NAME_RE.match(base_of(p))) or
                              ("test" in posix(p).split("/")[:-1] and ext_of(p) in (".js", ".mjs", ".cjs")),
                              "`node --test` without arguments only runs files named `*.test.js`, `*-test.js`, `*_test.js`, "
                              "`test-*.js` or `test.js`, or any .js file under a `test/` folder"))
            continue
        for tool in ("jest", "vitest"):
            if re.search(r"(?:^|\s|/)%s\b(?![\w.-])" % tool, seg):
                cfg = [n for n in os.listdir(root) if n.startswith(("%s.config" % tool, "vite.config"))] if os.path.isdir(root) else []
                pkg = load_json_text(read_text(os.path.join(root, "package.json")) or "") or {}
                if cfg or (isinstance(pkg, dict) and tool in pkg):
                    break
                if tool == "jest":
                    rules.append(("js", None, lambda p: bool(JEST_NAME_RE.match(base_of(p))) or "__tests__" in posix(p).split("/")[:-1],
                                  "jest's default testMatch only runs `*.test.js` / `*.spec.js` files or files under `__tests__/`"))
                else:
                    rules.append(("js", None, lambda p: bool(JEST_NAME_RE.match(base_of(p))),
                                  "vitest's default include only runs `*.test.*` / `*.spec.*` files"))
                break
    return rules


def check_test_discovery(change, test_runs, skip_paths=()):
    """New test files that the project's test command will never collect, so the tests the change
    adds (or moves) never run. test_runs: [(display, expanded_text, cwd_rel)] from prove.py."""
    out = []
    if not change.ok or not test_runs:
        return out
    by_lang = {}
    for display, expanded, cwd_rel in test_runs:
        root = os.path.join(change.repo, cwd_rel) if cwd_rel and cwd_rel != "." else change.repo
        rules = _discovery_rules(expanded, root)
        if rules is None:
            return out
        for lang, start, matcher, desc in rules:
            by_lang.setdefault(lang, []).append((display, cwd_rel or ".", start, matcher, desc))
    for f in change.files:
        p = f.path
        if f.status not in ("A", "R") or p in skip_paths or f.binary:
            continue
        e = ext_of(p)
        lang = "py" if e in PY_EXT else "js" if e in JS_EXT else None
        if not lang or lang not in by_lang:
            continue
        b = base_of(p)
        if b in ("conftest.py", "__init__.py", "setup.py") or b.startswith(("helper", "util", "fixture", "factory", "mock")):
            continue
        txt = change.new_text(p) or ""
        if not TEST_BODY_RE.search(txt) or not (is_test_path(p) or re.search(r"\bunittest\.TestCase\b|from node:test|require\(['\"]node:test", txt)):
            continue
        collected, reasons = False, []
        for display, cwd_rel, start, matcher, desc in by_lang[lang]:
            rel = p
            if cwd_rel not in (".", ""):
                if not p.startswith(cwd_rel.rstrip("/") + "/"):
                    continue
                rel = p[len(cwd_rel.rstrip("/")) + 1:]
            if start not in (None, ".") and not rel.startswith(start.strip("./").rstrip("/") + "/"):
                reasons.append((display, desc))
                continue
            if matcher(rel):
                collected = True
                break
            reasons.append((display, desc))
        if collected or not reasons:
            continue
        n_tests = len(re.findall(r"^\s*(?:async\s+)?def\s+test\w*\s*\(|\b(?:it|test)\s*\(\s*['\"`]", txt, re.M))
        out.append(finding(
            5, "New tests never run: %s" % p,
            "The change adds %s%s, but the project's test command never collects it: %s." % (
                p, " with %d test%s" % (n_tests, "" if n_tests == 1 else "s") if n_tests else "", reasons[0][1]),
            ["test command: `%s`" % reasons[0][0], "%s (new file) does not match" % p],
            "The checks pass without running these tests, so whatever they were meant to prove is unproven.",
            ["Rename or move %s so the test command picks it up (match the existing test files' naming), then rerun and "
             "confirm the test count went up." % p],
            file=p))
    return out


# ---------------------------------------------------------------------------
# Cause 9: debug leftovers
# ---------------------------------------------------------------------------

JS_LOG_RE = re.compile(r"\bconsole\.(log|debug|dir|trace|table|time|timeEnd|count)\s*\(")
JS_DEBUGGER_RE = re.compile(r"(^|[;{}\s])debugger\s*;?\s*$")
PY_PRINT_RE = re.compile(r"^\s*(?:print|pprint|pp)\s*\(")
PY_BREAK_RE = re.compile(r"\bbreakpoint\s*\(\s*\)|\b(?:i?pdb|pudb)\.set_trace\s*\(|^\s*import\s+i?pdb\b|\bfrom\s+i?pdb\s+import\b")
OTHER_DEBUG_RE = re.compile(r"\bbinding\.pry\b|^\s*byebug\b|\bdbg!\s*\(|\bvar_dump\s*\(|\bdd\s*\(\s*\$|\bprint_r\s*\(|\bspew\.Dump\s*\(")
OPERATIONAL_MSG_RE = re.compile(r"listening|started|starting|running on|ready|serving|server (?:is )?up|connected to|done in|built in|usage:|"
                                r"[\"'`]\s*(?:Usage|Options|Commands|Examples?|Arguments|Flags)\b|[\"'`]\s{2,}-{1,2}[a-z]", re.I)
COMMENTED_CODE_RE = re.compile(
    r"[;{}]\s*$|\)\s*;?\s*$|=>|===|!==|^\s*(?:const|let|var|return|if|for|while|def|class|import|from|function|await|print|console\.|self\.|this\.)\b.*[(=:.]|"
    r"^\s*[\w.\[\]]+\s*(?:=|\+=|-=)\s*\S")
DOC_TAG_RE = re.compile(r"^\s*(?:@\w+|eslint|prettier|ts-|type:|noqa|pylint|istanbul|c8|TODO|FIXME|NOTE|XXX|HACK)\b|https?://", re.I)


def _py_main_lines(text):
    """Line numbers inside def main/cli/run or the __main__ block (where print is the output)."""
    lines = text.splitlines()
    inside = set()
    cur, cur_indent = None, 0
    for i, l in enumerate(lines, 1):
        m = re.match(r"^(\s*)(?:async\s+)?def\s+(\w+)", l)
        if m:
            cur = m.group(2) if m.group(2) in ("main", "cli", "run", "_main", "run_cli", "entry", "entrypoint") or \
                m.group(2).startswith(("cmd_", "command_", "print_", "show_", "report", "render")) else None
            cur_indent = len(m.group(1))
            if cur:
                inside.add(i)
            continue
        if re.match(r"^if\s+__name__\s*==", l):
            cur, cur_indent = "__main__", -1
            continue
        if cur and (not l.strip() or len(l) - len(l.lstrip()) > cur_indent):
            inside.add(i)
        elif l.strip():
            cur = None
    return inside


def check_debug(change):
    out = []
    for f in change.files:
        p = f.path
        e = ext_of(p)
        if f.binary or f.status == "D" or not _is_code(p) or f.skip or not f.added:
            continue
        test = is_test_path(p)
        hits = []
        new_text = None
        added = new_lines(f)
        if e in JS_EXT:
            cli = is_cli_path(p)
            if not cli:
                new_text = change.new_text(p) or ""
                cli = new_text.startswith("#!") or "process.argv" in new_text
            for ln, t in added:
                if not _code_content(t):
                    continue
                if JS_DEBUGGER_RE.search(strip_strings_comments(t, e)):
                    hits.append((ln, t, "debugger statement"))
                elif not test and not cli and JS_LOG_RE.search(strip_strings_comments(t, e)) \
                        and not OPERATIONAL_MSG_RE.search(t) and "eslint-disable" not in t:
                    hits.append((ln, t, "console.%s" % JS_LOG_RE.search(t).group(1)))
        elif e in PY_EXT:
            cli = is_cli_path(p)
            if not cli and not test:
                new_text = change.new_text(p) or ""
                old = change.old_text(f.old_path) or ""
                cli = "__name__" in new_text and "__main__" in new_text or \
                    len(re.findall(r"^\s*print\s*\(", old, re.M)) >= 2 or "argparse" in new_text or "click" in new_text
            main_ctx = None
            if cli and not is_cli_path(p):
                main_ctx = _py_main_lines(change.new_text(p) or "")
            for ln, t in added:
                if not _code_content(t):
                    continue
                if PY_BREAK_RE.search(t):
                    hits.append((ln, t, "debugger breakpoint"))
                elif not test and PY_PRINT_RE.search(t) and "file=" not in t:
                    if not cli or (main_ctx is not None and ln not in main_ctx):
                        hits.append((ln, t, "print()"))
        else:
            for ln, t in added:
                if _code_content(t) and OTHER_DEBUG_RE.search(t):
                    hits.append((ln, t, "debug call"))
        # commented-out code blocks (2+ consecutive added comment lines that read as code)
        if not test:
            run = []
            prev = None
            for ln, t in added:
                s = t.strip()
                code_like = False
                if s.startswith(("//", "#")) and not s.startswith(("#!", "///", "#region", "#endregion", "#pragma")):
                    body = re.sub(r"^(//+|#+|/\*+|\*+|--)\s?", "", s).rstrip("*/").strip()
                    if body and not DOC_TAG_RE.search(body) and COMMENTED_CODE_RE.search(body) and \
                            not re.match(r"^[A-Z][a-z]+(\s+[a-z]+){3,}", body):
                        code_like = True
                if code_like and (prev is None or ln == prev + 1):
                    run.append((ln, t))
                elif code_like:
                    if len(run) >= 2:
                        hits.append((run[0][0], run[0][1], "commented-out code (%d lines)" % len(run)))
                    run = [(ln, t)]
                else:
                    if len(run) >= 2:
                        hits.append((run[0][0], run[0][1], "commented-out code (%d lines)" % len(run)))
                    run = []
                prev = ln
            if len(run) >= 2:
                hits.append((run[0][0], run[0][1], "commented-out code (%d lines)" % len(run)))
        if hits:
            kinds = sorted(set(k.split(" (")[0] for _, _, k in hits))
            out.append(finding(
                9, "Debug leftovers in %s" % p,
                "The change leaves %s in %s (%s)." % ("a debug leftover" if len(hits) == 1 else "%d debug leftovers" % len(hits), p, ", ".join(kinds)),
                [_ev(p, ln, t) + ("" if k.startswith("console") or k == "print()" else "  [%s]" % k) for ln, t, k in hits[:5]],
                "Debug output leaks data into logs and the browser console; a stray debugger or breakpoint() halts the program.",
                ["Delete the debug lines (or use the project's logger if the output is really needed)."],
                file=p, line=hits[0][0]))
    return out


# ---------------------------------------------------------------------------
# Cause 10: secrets and env files
# ---------------------------------------------------------------------------

KEY_FILE_EXT = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".ppk", ".p8"}
KEY_FILE_NAMES = {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", "credentials.json", "service-account.json",
                  ".npmrc", ".pypirc", ".netrc", ".git-credentials"}
GENERIC_SECRET_RE = re.compile(
    r"(?i)\b([\w.-]*(?:secret|passw(?:or)?d|pwd|api[_-]?key|apikey|access[_-]?key|auth[_-]?token|"
    r"token|private[_-]?key|client[_-]?secret|credential)[\w.-]*)[\"']?\s*(?:[:=]|=>)\s*[\"']([^\"'\s]{10,})[\"']")
ENV_LINE_RE = re.compile(r"^\s*(?:export\s+)?([A-Z][A-Z0-9_]*(?:SECRET|PASSWORD|PASS|KEY|TOKEN|CREDENTIALS?|DSN|DATABASE_URL)[A-Z0-9_]*)\s*=\s*['\"]?([^'\"\s#]{8,})")
PLACEHOLDER_RE = re.compile(r"(?i)your|example|sample|dummy|placeholder|changeme|change[-_]me|xxx|\*\*\*|<|>|\$\{|\{\{|process\.env|"
                            r"os\.environ|getenv|todo|replace|insert|fake|redacted|test[-_]?(?:key|secret|token)|^(.)\1+$|none|null|undefined|secret123|password123")


LABEL_KEY_RE = re.compile(r"(?i)(?:label|message|msg|text|title|placeholder|description|desc|hint|error|name|id|ids|field|"
                          r"url|uri|path|route|endpoint|type|header|param|operation|op|event|action|key_?name|prefix|suffix)$")
TEXTS_DIRS = {"lang", "langs", "locale", "locales", "i18n", "intl", "messages", "translations", "l10n", "strings"}


def _texts_path(path):
    return bool(set(posix(path).lower().split("/")[:-1]) & TEXTS_DIRS)


def _secretish_value(v):
    """Real secrets mix letters with digits or symbols. Identifiers, slugs and labels do not
    ('auth:session-key', 'get-api-keys', 'listApiKeys')."""
    if re.match(r"^[A-Za-z]+(?:[\-_.:/ ][A-Za-z]+)*$", v):
        return False
    if " " in v.strip():
        return False
    return True


def _entropy(s):
    if not s:
        return 0.0
    n = float(len(s))
    return -sum((c / n) * math.log(c / n, 2) for c in Counter(s).values())


def _env_placeholder(raw):
    """A value in a real env file (not a template) is a placeholder only when it is mostly
    placeholder text. A long random-looking token that happens to contain a word like "fake" or
    "test" (sk_live_8Hq...fake...Zr2) is still shaped like a live key, and env files are where live
    keys end up, so it is treated as one."""
    v = raw.strip().strip("'\"")
    if not PLACEHOLDER_RE.search(v):
        return False
    rest = PLACEHOLDER_RE.sub("", v)
    if len(v) >= 20 and len(rest) >= 16 and re.search(r"\d", rest) and re.search(r"[A-Za-z]", rest) and _entropy(rest) >= 3.5:
        return False
    return True


def check_secrets(change):
    out = []
    for f in change.files:
        p = f.path
        b = base_of(p).lower()
        if f.status == "D":
            continue
        e = ext_of(p)
        if is_env_file(p) and not is_env_template(p) and f.status in ("A", "M", "R"):
            names, secretish = [], []
            for _, t in f.added:
                m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", t)
                if m and m.group(2).strip().strip("'\"") and not _env_placeholder(m.group(2)):
                    names.append(m.group(1))
                    val = m.group(2).strip().strip("'\"")
                    if re.search(r"SECRET|PASSWORD|PASSWD|TOKEN|KEY|CREDENTIAL|DSN|DATABASE_URL|PRIVATE|AUTH", m.group(1), re.I) or \
                            any(rx.search(val) for _, rx in SECRET_PATTERNS) or (len(val) >= 16 and _entropy(val) >= 3.5):
                        secretish.append(m.group(1))
            tracked_before = f.status != "A" and change.old_text(f.old_path) is not None
            if tracked_before and not secretish:
                continue
            out.append(finding(
                10, "Env file in the change: %s" % p,
                "The change %s %s%s. The next `git add .` commits it." % (
                    "adds" if f.status == "A" else "edits", p,
                    (" with values for %s" % ", ".join(names[:6])) if names else ""),
                ["%s (%s, not gitignored)" % (p, "new file" if f.status == "A" else "tracked file")] +
                ["%s sets %s=<redacted>" % (p, n) for n in (secretish or names)[:3]],
                "Anything committed is readable by everyone with the repo and stays in history even after deletion.",
                ["Keep %s out of git: add `.env*` (with `!.env.example`) to .gitignore and move the values to an untracked env file. "
                 "If a real secret was ever committed or pushed, rotate it." % p],
                file=p, tier="problem" if secretish else "check"))
            continue
        if (e in KEY_FILE_EXT or b in KEY_FILE_NAMES) and f.status == "A" and not b.endswith(".pub"):
            out.append(finding(
                10, "Credential file added: %s" % p,
                "The change adds %s, a private key or credentials file." % p, ["%s (new file)" % p],
                "Whoever can read the repo can use the key.",
                ["Remove it from the change, add it to .gitignore and load it from a secret store or env var."],
                file=p))
            continue
        if f.binary or f.skip:
            continue
        test = is_test_path(p)
        hits = []
        for ln, t in new_lines(f):
            found = None
            for label, rx in SECRET_PATTERNS:
                m = rx.search(t)
                if not m:
                    continue
                val = m.group(0)
                if label == "Database URL with password":
                    if re.search(r"@(localhost|127\.0\.0\.1|0\.0\.0\.0|db|postgres|mysql|redis|mongo|host\.docker\.internal)[:/]", val) or \
                            PLACEHOLDER_RE.search(m.group(1)):
                        continue
                if PLACEHOLDER_RE.search(val) and label != "Private key":
                    continue
                found = (label, val)
                break
            if not found and not test and e not in DOC_EXT and not _texts_path(p):
                m = GENERIC_SECRET_RE.search(t)
                if m and not PLACEHOLDER_RE.search(m.group(2)) and _entropy(m.group(2)) >= 3.3 and \
                        not re.match(r"^[a-z]+(\.[a-z]+)+$", m.group(2)) and not re.search(r"[/\\]|\.(js|ts|py|json)$", m.group(2)) and \
                        _secretish_value(m.group(2)) and not LABEL_KEY_RE.search(m.group(1)):
                    found = ("Hardcoded %s" % m.group(1), m.group(2))
                else:
                    m = ENV_LINE_RE.search(t)
                    if m and not PLACEHOLDER_RE.search(m.group(2)) and _entropy(m.group(2)) >= 3.0 and _secretish_value(m.group(2)):
                        found = ("Hardcoded %s" % m.group(1), m.group(2))
            if found:
                hits.append((ln, found[0], found[1]))
        if hits:
            google_only = all(h[1] == "Google API key" for h in hits)
            out.append(finding(
                10, "Secret added in %s" % p,
                "The change adds %s in %s." % (", ".join(sorted(set(h[1] for h in hits))), p),
                ["%s:%d: %s `%s`" % (p, ln, label, redact(val)) for ln, label, val in hits[:4]],
                "Once committed, the secret is readable by everyone with the repo and stays in git history.",
                ["Move it to an env var read at runtime (process.env.X / os.environ['X']) and keep the value out of git. "
                 "If it was ever pushed or shared, revoke it at the provider and issue a new one."],
                file=p, line=hits[0][0], tier="check" if google_only else "problem"))
    return out


# ---------------------------------------------------------------------------
# Cause 11: dependencies and lockfiles
# ---------------------------------------------------------------------------

DEP_TASK_RE = re.compile(r"\b(install|dependency|dependencies|package|library|libraries|upgrade|bump|update (?:the )?(?:deps|dependencies|packages)|lockfile|lock file|npm audit|security update|version)\b", re.I)


def _norm_pkg(n):
    return re.sub(r"[-_.]+", "-", n.lower()).strip()


def _py_req_names(lines):
    out = {}
    for t in lines:
        s = t.split("#", 1)[0].strip()
        if not s or s.startswith(("-", "git+", "http")):
            continue
        m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._\-]*)(\[[^\]]*\])?\s*(.*)$", s)
        if m:
            out[_norm_pkg(m.group(1))] = m.group(3).strip()
    return out


def _pyproject_deps(text):
    d = load_toml(text or "") or {}
    out = {}
    proj = d.get("project") or {}
    for s in proj.get("dependencies") or []:
        out.update(_py_req_names([s]))
    for grp in (proj.get("optional-dependencies") or {}).values():
        for s in grp or []:
            out.update(_py_req_names([s]))
    for grp in (d.get("dependency-groups") or {}).values():
        for s in grp or []:
            if isinstance(s, str):
                out.update(_py_req_names([s]))
    poetry = (d.get("tool") or {}).get("poetry") or {}
    for k, v in (poetry.get("dependencies") or {}).items():
        if k.lower() != "python":
            out[_norm_pkg(k)] = str(v)
    for g in (poetry.get("group") or {}).values():
        for k, v in ((g or {}).get("dependencies") or {}).items():
            out[_norm_pkg(k)] = str(v)
    return out


def _cargo_deps(text):
    d = load_toml(text or "") or {}
    out = {}
    for sec in ("dependencies", "dev-dependencies", "build-dependencies"):
        for k, v in (d.get(sec) or {}).items():
            out[_norm_pkg(k)] = str(v)
    return out


def _pkg_json_deps(text):
    d = load_json_text(text or "") or {}
    out = {}
    if not isinstance(d, dict):
        return out
    for sec in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        v = d.get(sec)
        if isinstance(v, dict):
            for k, ver in v.items():
                out[k] = str(ver)
    return out


def _manifest_deps(path, text):
    b = base_of(path).lower()
    if text is None:
        return None
    if b == "package.json":
        return _pkg_json_deps(text)
    if b == "pyproject.toml":
        return _pyproject_deps(text)
    if b == "cargo.toml":
        return _cargo_deps(text)
    if re.match(r"^requirements([-_.][\w.-]+)?\.(txt|in)$", b):
        return _py_req_names(text.splitlines())
    if b == "go.mod":
        return dict((m.group(1), m.group(2)) for m in re.finditer(r"^\s*(?:require\s+)?([\w.\-/]+\.[\w.\-/]+)\s+(v[\w.\-+]+)", text, re.M))
    if b == "gemfile":
        return dict((m.group(1), "") for m in re.finditer(r"^\s*gem\s+['\"]([\w\-]+)['\"]", text, re.M))
    if b in ("pipfile",):
        return _pyproject_deps(text.replace("[packages]", "[tool.poetry.dependencies]"))
    return None


def _named_in_task(name, task):
    if not task:
        return False
    low = task.lower()
    n = name.lower()
    cands = {n, n.split("/")[-1], n.lstrip("@"), _norm_pkg(n), n.replace("-", " "), n.replace("-", "_")}
    return any(c and re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(c), low) for c in cands if len(c) >= 2)


def check_deps(change, task):
    out = []
    task = task or ""
    generic_ok = bool(DEP_TASK_RE.search(task))
    dep_dirs = {}
    for f in change.files:
        if f.status == "D" or not is_manifest(f.path) or f.binary:
            continue
        old = _manifest_deps(f.old_path, change.old_text(f.old_path)) if f.status != "A" else {}
        new = _manifest_deps(f.path, change.new_text(f.path))
        if new is None or old is None:
            continue
        if f.status == "A" and not f.untracked and not old:
            # a brand new package manifest: judged by scope, not here
            pass
        added = [k for k in new if k not in old]
        changed = [k for k in new if k in old and new[k] != old[k]]
        d = os.path.dirname(f.path)
        if added or changed:
            dep_dirs[d] = f.path
        if f.status == "A":
            continue
        unasked_add = [k for k in added if not _named_in_task(k, task)]
        unasked_chg = [k for k in changed if not _named_in_task(k, task)]
        if not unasked_add and not unasked_chg:
            continue
        locks = [g.path for g in change.files if is_lockfile(g.path) and os.path.dirname(g.path) == d]
        parts = []
        if unasked_add:
            parts.append("adds %s %s" % ("dependency" if len(unasked_add) == 1 else "dependencies", ", ".join("`%s`" % k for k in unasked_add[:6])))
        if unasked_chg:
            parts.append("changes the version of %s" % ", ".join("`%s` (%s -> %s)" % (k, old[k], new[k]) for k in unasked_chg[:4]))
        tier = "check" if generic_ok and not unasked_add else ("check" if generic_ok and len(unasked_add) <= 1 and re.search(r"\b(install|add)\b.*\b(package|dependency|library)\b", task, re.I) else "problem")
        if not task.strip():
            tier = "check"
        out.append(finding(
            11, "Dependency change %s in %s" % ("not asked for" if task.strip() else "to confirm", f.path),
            ("The change %s in %s, and the task does not ask for %s." if task.strip() else
             "The change %s in %s. No task was given, so confirm %s intended.") % (
                " and ".join(parts), f.path, ("it" if len(unasked_add) + len(unasked_chg) == 1 else "them") +
                ("" if task.strip() else (" is" if len(unasked_add) + len(unasked_chg) == 1 else " are"))),
            ["%s: %s" % (f.path, "; ".join(parts))] + ["%s (lockfile also changed)" % l for l in locks[:2]],
            "Every new package is more install time, bundle size and supply-chain risk, and a version change can break code the task never touched.",
            ["Remove the dependency change unless it is really needed; if it is, say why in your summary so the person can approve it."],
            file=f.path, files=locks, tier=tier))
    out += _lockfile_not_updated(change, dep_dirs)
    for f in change.files:
        if not is_lockfile(f.path) or f.status == "D":
            continue
        d = os.path.dirname(f.path)
        if d in dep_dirs:
            continue
        b = base_of(f.path).lower()
        other = None
        if b in JS_LOCKS and f.status == "A":
            for lk, pm in JS_LOCKS.items():
                if lk != b and os.path.exists(os.path.join(change.repo, d, lk)) and pm != JS_LOCKS[b]:
                    other = lk
        if other:
            out.append(finding(
                11, "Second lockfile added: %s" % f.path,
                "The change adds %s next to the existing %s: the dependencies were installed with %s instead of %s." % (
                    f.path, other, JS_LOCKS[b], JS_LOCKS[other]),
                ["%s (new file, %d lines)" % (f.path, len(f.added)), "%s (existing lockfile)" % os.path.join(d, other).replace("\\", "/")],
                "Two lockfiles drift apart; installs stop being reproducible and CI may use different versions than you tested.",
                ["Remove %s from the change and install with %s." % (f.path, JS_LOCKS[other])],
                file=f.path))
            continue
        if re.search(r"\b(lock ?file|upgrade|bump|update (?:the )?(?:deps|dependencies|packages)|npm audit|security)\b", task, re.I):
            continue
        man_changed = any(g.path == os.path.join(d, m).replace("\\", "/").lstrip("/") for g in change.files
                          for m in ("package.json", "pyproject.toml", "Cargo.toml", "Gemfile", "composer.json"))
        churn = [t for _, t in f.added + f.removed if t.strip()]
        if man_changed and f.status != "A" and len(churn) <= 6 and all(re.search(r"^\s*\"?(version|name)\"?\s*[:=]", t) for t in churn):
            continue
        new_names = _lock_names(t for _, t in f.added) - _lock_names(t for _, t in f.removed)
        versions_only = f.status != "A" and not new_names
        tier = "check" if (versions_only or not task.strip()) else "problem"
        out.append(finding(
            11, "Lockfile changed without a manifest change: %s" % f.path,
            "The change %s %s (+%d/-%d lines), but no dependency in the manifest changed%s%s." % (
                "adds" if f.status == "A" else "rewrites", f.path, len(f.added), len(f.removed),
                " and the task does not ask for an upgrade" if task.strip() else "",
                "; only versions of packages already in it changed (like a security update)" if versions_only else
                ("; it adds %s" % ", ".join("`%s`" % n for n in sorted(new_names)[:4]) if new_names else "")),
            ["%s (%s)" % (f.path, "new file" if f.status == "A" else "modified")],
            "Unrelated lockfile churn changes installed versions for everyone and hides real changes in review.",
            ["Restore %s unless the task needed it; if an install rewrote it, reinstall with the project's package manager and the existing lockfile." % f.path],
            file=f.path, tier=tier))
    return out


LOCK_NAME_RES = [re.compile(r'^\s*"(?:node_modules/)+(@?[^"]+?)"\s*:\s*\{'),          # npm v2/v3
                 re.compile(r"^\s{2}'?/?(@?[\w.\-]+(?:/[\w.\-]+)?)@\d"),                # pnpm
                 re.compile(r'^"?(@?[\w.\-]+(?:/[\w.\-]+)?)@[\^~<>=*\d]'),                # yarn v1
                 re.compile(r'^\s*name\s*=\s*"([\w.\-]+)"')]                            # poetry, uv, Cargo


def _lock_names(lines):
    out = set()
    for t in lines:
        for rx in LOCK_NAME_RES:
            m = rx.match(t)
            if m:
                out.add(m.group(1).lower())
                break
    return out


LOCK_FOR = {"package.json": ("package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb"),
            "pyproject.toml": ("poetry.lock", "uv.lock", "pdm.lock"),
            "pipfile": ("Pipfile.lock",), "cargo.toml": ("Cargo.lock",), "go.mod": ("go.sum",),
            "gemfile": ("Gemfile.lock",), "composer.json": ("composer.lock",)}


def _tracked(change, rel):
    code, out = run_git(change.repo, ["ls-files", "--", rel])
    return code == 0 and bool(out.strip())


def _lockfile_not_updated(change, dep_dirs):
    """A dependency added or re-versioned in a manifest whose (tracked) lockfile the change did not
    touch: `npm ci`, `pnpm install --frozen-lockfile`, `poetry install` and friends fail in CI."""
    out = []
    changed = set(f.path for f in change.files)
    for d, mpath in dep_dirs.items():
        names = LOCK_FOR.get(base_of(mpath).lower())
        if not names:
            continue
        parts = d.split("/") if d else []
        lock = None
        for i in range(len(parts), -1, -1):
            pre = "/".join(parts[:i])
            for n in names:
                cand = (pre + "/" + n) if pre else n
                if os.path.isfile(os.path.join(change.repo, cand)):
                    lock = cand
                    break
            if lock:
                break
        if not lock or lock in changed or not _tracked(change, lock):
            continue
        out.append(finding(
            11, "Lockfile not updated: %s" % lock,
            "The change edits the dependencies in %s but leaves %s unchanged, so the lockfile no longer matches the manifest." % (mpath, lock),
            ["%s: dependencies changed" % mpath, "%s: not in the change" % lock],
            "A frozen install in CI (`npm ci`, `pnpm install --frozen-lockfile`, `poetry install`, `cargo build --locked`) fails, "
            "or other machines install different versions than the ones you tested.",
            ["Run the project's install command so it updates %s, and include it in the change." % lock],
            file=mpath, files=[lock]))
    return out


# ---------------------------------------------------------------------------
# Cause 12: edited migrations
# ---------------------------------------------------------------------------

def check_migrations(change):
    out = []
    for f in change.files:
        if f.status not in ("M", "D", "R") or not (is_migration(f.old_path) or is_migration(f.path)):
            continue
        if f.status == "R" and not f.added and not f.removed:
            verb = "renames"
        else:
            verb = {"D": "deletes", "R": "renames and edits"}.get(f.status, "edits")
        if change.old_text(f.old_path) is None and not f.binary:
            continue
        out.append(finding(
            12, "Existing migration %s: %s" % ("edited" if verb == "edits" else verb.split()[0][:-1] + "d", f.old_path),
            "The change %s %s, a migration that already exists in the base. Databases that already ran it will never run the new version." % (verb, f.old_path),
            ["%s (+%d/-%d lines)" % (f.path, len(f.added), len(f.removed))] + [_ev(f.path, ln, t) for ln, t in f.added[:2]],
            "Production and teammates' databases keep the old schema while fresh databases get the new one: the code works locally and fails in production.",
            ["Restore %s and put the change in a new migration file (the next number or timestamp)." % f.old_path],
            file=f.path, files=[f.old_path]))
    return out


# ---------------------------------------------------------------------------
# Cause 13: stubs and placeholders
# ---------------------------------------------------------------------------

TODO_RE = re.compile(r"(?://|#|/\*|\*|<!--|--)\s*(?:TODO|FIXME|XXX|HACK)\b")
TODO_CI_RE = re.compile(r"(?://|#|/\*|\*|<!--|--)\s*(?:todo|fixme)\s*[:(]", re.I)
NOTIMPL_RE = re.compile(r"NotImplementedError|NotImplementedException|\bunimplemented!\s*\(|\btodo!\s*\(|"
                        r"['\"`][^'\"`]*\bnot (?:yet )?implemented\b[^'\"`]*['\"`]|['\"`]\s*(?:TODO|stub)\s*['\"`]", re.I)
COMMENT_START_RE = re.compile(r"//|#|/\*|\*")
MOCK_WORDS_RE = re.compile(r"\b(mock(?:ed)?|fake|dummy|stub(?:bed)?|placeholder|hard-?coded|"
                           r"for now|not real|until [^\n]{0,80}?(?:ready|done|implemented)|replace (?:this|later|me))\b", re.I)


class _MockComment(object):
    """A mock/placeholder word after a comment marker. Two linear searches instead of one
    `marker.*word` regex, which was quadratic on long lines (minified files hung for minutes)."""

    @staticmethod
    def search(text):
        m = COMMENT_START_RE.search(text)
        if not m:
            return None
        return MOCK_WORDS_RE.search(text, m.end())


MOCK_COMMENT_RE = _MockComment()
MOCK_IDENT_RE = re.compile(r"\b(?:mock|fake|dummy|stub)[A-Z_]\w*|\b(?:MOCK|FAKE|DUMMY|STUB)_[A-Z_]+\b|\b(?:mock|fake|dummy)(?:Data|Users?|Response|Result|Items?|Orders?|Products?)\b")


def check_stubs(change):
    out = []
    for f in change.files:
        p = f.path
        if f.binary or f.status == "D" or not _source_file(p) or f.skip or not f.added:
            continue
        e = ext_of(p)
        hits = []
        lines = list(f.added)
        fresh = set(ln for ln, _ in new_lines(f))
        for i, (ln, t) in enumerate(lines):
            s = t.strip()
            if not s or ln not in fresh:
                continue
            if TODO_RE.search(t) or TODO_CI_RE.search(t):
                hits.append((ln, t, "TODO/FIXME"))
            elif NOTIMPL_RE.search(t):
                hits.append((ln, t, "not implemented"))
            elif MOCK_COMMENT_RE.search(t) and not is_comment_line(s) and re.search(r"\breturn\b|=\s*[\[{\"'\d]|=\s*(?:true|false|True|False|None|null)\b", t):
                hits.append((ln, t, "mock or hardcoded value"))
            elif is_comment_line(s) and MOCK_COMMENT_RE.search(t) and i + 1 < len(lines) and \
                    re.search(r"\breturn\b|=\s*[\[{\"'\d]", lines[i + 1][1]):
                hits.append((ln, t, "mock or hardcoded value"))
            elif _code_content(t) and MOCK_IDENT_RE.search(strip_strings_comments(t, e)):
                hits.append((ln, t, "mock data in production code"))
            elif e in JS_EXT and re.search(r"^\s*(?:export\s+)?(?:async\s+)?function\s+[\w$]+\s*\([^)]*\)\s*\{\s*\}\s*;?\s*$", t):
                hits.append((ln, t, "empty function body"))
            elif e in PY_EXT and re.match(r"^\s*(?:async\s+)?def\s+\w+\s*\(", t):
                # function whose whole body is pass / ... / return None
                body = []
                for ln2, t2 in lines[i + 1:i + 4]:
                    if t2.strip() and not t2.strip().startswith(("\"\"\"", "'''", "#")):
                        body.append(t2.strip())
                    if len(body) >= 2:
                        break
                prev = lines[i - 1][1].strip() if i > 0 else ""
                if body and body[0] in ("pass", "...", "return None", "return") and \
                        (len(body) == 1 or not body[1].startswith((" ",))) and not prev.startswith(("@abstractmethod", "@overload", "@abc.abstractmethod", "@property")):
                    nxt = body[1] if len(body) > 1 else ""
                    if not nxt or re.match(r"^(def|class|@|async def|[A-Za-z_]\w*\s*=)", nxt):
                        txt = change.new_text(p) or ""
                        if not re.search(r"\b(Protocol|ABC|abstractmethod)\b", txt):
                            hits.append((ln, t, "empty function body"))
        if hits:
            kinds = sorted(set(k for _, _, k in hits))
            out.append(finding(
                13, "Unfinished code in %s" % p,
                "The change leaves %s in %s (%s)." % ("a placeholder" if len(hits) == 1 else "%d placeholders" % len(hits), p, ", ".join(kinds)),
                [_ev(p, ln, t) for ln, t, _ in hits[:5]],
                "The feature looks done and the checks may pass, but this path does nothing real (or returns made-up data) when someone uses it.",
                ["Implement the missing part, or tell the person plainly what is left and why, instead of saying done."],
                file=p, line=hits[0][0]))
    return out


# ---------------------------------------------------------------------------
# Cause 14: type and lint escapes
# ---------------------------------------------------------------------------

JSDOC_ANY_RE = re.compile(r"@(?:param|type|returns?|typedef|property|prop|arg|argument|template|satisfies)\s*\{\s*(?:any|\*)(?:\[\])?\s*\}")
TS_ANY_RE = re.compile(r"(?::\s*|\bas\s+|<|\bArray<|\bRecord<\s*\w+\s*,\s*)any\b(?!\w)|\bany\[\]")
ESCAPE_RE = re.compile(
    r"@ts-ignore|@ts-expect-error|@ts-nocheck|eslint-disable|biome-ignore|oxlint-disable|deno-lint-ignore|"
    r"#\s*type:\s*ignore|#\s*noqa\b|#\s*pylint:\s*disable|#\s*pyright:\s*ignore|#\s*mypy:\s*ignore|#\s*ruff:\s*noqa|"
    r"//\s*nolint\b|#!?\[allow\(|@SuppressWarnings|#pragma warning disable|@Suppress\(|// swiftlint:disable|# rubocop:disable")
CONFIG_LOOSEN_RE = re.compile(
    r"\"?(strict|noImplicitAny|strictNullChecks|noImplicitReturns|noUnusedLocals|noUnusedParameters|checkJs)\"?\s*:\s*false|"
    r"\"?(skipLibCheck|allowJs)\"?\s*:\s*true(?=.*allowJs)|"
    r"[\"']?[@\w/\-]+[\"']?\s*:\s*(?:[\"']off[\"']|0)\s*,?\s*$|"
    r"^\s*(ignore_errors|ignore_missing_imports)\s*=\s*(?:true|True)|^\s*disallow_\w+\s*=\s*(?:false|False)|"
    r"^\s*strict\s*=\s*(?:false|False)|^\s*(?:extend-)?ignore\s*=|^\s*per-file-ignores\s*=|^\s*disable\s*=")
LINT_CONFIG_RE = re.compile(r"^(tsconfig[\w.\-]*\.json|jsconfig\.json|\.eslintrc(\.\w+)?|eslint\.config\.\w+|biome\.jsonc?|"
                            r"mypy\.ini|\.mypy\.ini|\.flake8|setup\.cfg|tox\.ini|pyproject\.toml|ruff\.toml|\.ruff\.toml|\.pylintrc|pylintrc|"
                            r"pyrightconfig\.json|\.golangci\.ya?ml|clippy\.toml)$", re.I)


def check_escapes(change):
    out = []
    for f in change.files:
        p = f.path
        if f.binary or f.status == "D" or f.skip or not f.added:
            continue
        e = ext_of(p)
        b = base_of(p)
        hits = []
        if _is_code(p):
            for ln, t in new_lines(f):
                if not t.strip():
                    continue
                m = ESCAPE_RE.search(t)
                if m:
                    hits.append((ln, t, m.group(0).strip()))
                    continue
                if e in JS_EXT and JSDOC_ANY_RE.search(t):
                    hits.append((ln, t, "JSDoc {any}"))
                    continue
                if e in TS_EXT and not is_comment_line(t):
                    if TS_ANY_RE.search(strip_strings_comments(t, e)):
                        hits.append((ln, t, "any"))
        elif LINT_CONFIG_RE.match(b):
            for ln, t in new_lines(f):
                if is_comment_line(t):
                    continue
                if b.lower() in ("setup.cfg", "tox.ini", "pyproject.toml") and not re.search(r"ignore|disable|strict|disallow", t):
                    continue
                if CONFIG_LOOSEN_RE.search(t):
                    hits.append((ln, t, "checker setting loosened"))
        if hits:
            test = is_test_path(p) or (is_cli_path(p) and all("no-console" in t or "T201" in t for _, t, _ in hits))
            kinds = sorted(set(k for _, _, k in hits))
            out.append(finding(
                14, "Type or lint escape added in %s" % p,
                "The change switches off the type checker or linter in %s (%s) instead of fixing what it reported." % (p, ", ".join("`%s`" % k for k in kinds[:5])),
                [_ev(p, ln, t) for ln, t, _ in hits[:5]],
                "The check passes because it was told not to look, so the error it was reporting is still there.",
                ["Remove the escape and fix the underlying type or lint error. If an escape is truly needed, keep it narrow and say why in a comment."],
                file=p, line=hits[0][0], tier="check" if test else "problem"))
    return out


# ---------------------------------------------------------------------------
# Cause 16: exported signatures
# ---------------------------------------------------------------------------

def _split_params(s):
    depth, cur, out = 0, "", []
    for ch in s:
        if ch in "([{<":
            depth += 1
        elif ch in ")]}>":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return [x.strip() for x in out if x.strip()]


def _param_types(params):
    """The type annotation of each parameter ('' when none)."""
    out = []
    for p in _split_params(re.sub(r"/\*.*?\*/", "", params or "", flags=re.S)):
        p = re.sub(r"#.*$", "", p).strip()
        if not p or p in ("self", "cls", "/", "*"):
            continue
        depth, cut = 0, None
        for i, ch in enumerate(p):
            if ch in "{[(<":
                depth += 1
            elif ch in "}])>":
                depth -= 1
            elif ch == ":" and depth == 0:
                cut = i
                break
        t = p[cut + 1:] if cut is not None else ""
        out.append(re.sub(r"\s+", "", t.split("=")[0]))
    return out


def _param_info(params, lang):
    """[(name, optional)] for a parameter string."""
    res = []
    for p in _split_params(re.sub(r"/\*.*?\*/", "", params or "", flags=re.S)):
        p = re.sub(r"#.*$", "", p).strip()
        if not p or p in ("self", "cls", "/", "*"):
            continue
        opt = "=" in p or p.startswith(("*", "...")) or re.match(r"^[\w$]+\?", p) is not None
        name = re.split(r"[:=?]", p.lstrip("*").lstrip("."), 1)[0].strip()
        if lang == "go":
            name = p.split()[0] if p.split() else p
        if p.startswith(("{", "[")):
            name = "<destructured>"
        res.append((name, opt))
    return res


def _exports(text, ext):
    """name -> params string (None for non-callables)."""
    out = {}
    if not text:
        return out
    if ext in JS_EXT:
        for m in re.finditer(r"^\s*export\s+(?:default\s+)?(?:async\s+)?function\s*\*?\s*([\w$]+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)", text, re.M):
            out[m.group(1)] = m.group(2)
        for m in re.finditer(r"^\s*export\s+(?:const|let|var)\s+([\w$]+)\s*(?::[^=]+)?=\s*(?:async\s+)?(?:function\s*[\w$]*\s*)?\(([^)]*)\)", text, re.M):
            out[m.group(1)] = m.group(2)
        for m in re.finditer(r"^\s*export\s+(?:const|let|var)\s+([\w$]+)\s*=\s*(?:async\s+)?([\w$]+)\s*=>", text, re.M):
            out[m.group(1)] = m.group(2)
        for m in re.finditer(r"^\s*export\s+(?:default\s+)?(?:abstract\s+)?(?:class|interface|type|enum)\s+([\w$]+)", text, re.M):
            out.setdefault(m.group(1), None)
        cjs = set()
        for m in re.finditer(r"module\.exports\s*=\s*\{([^}]*)\}", text):
            for part in m.group(1).split(","):
                part = part.strip()
                if not part:
                    continue
                k = re.split(r"\s*:\s*", part)
                cjs.add((k[0].strip(), (k[1].strip() if len(k) > 1 else k[0].strip())))
        for m in re.finditer(r"(?:module\.)?exports\.([\w$]+)\s*=\s*(?:async\s+)?(?:function\s*[\w$]*\s*\(([^)]*)\)|\(([^)]*)\)\s*=>)?", text):
            if m.group(2) is not None or m.group(3) is not None:
                out[m.group(1)] = m.group(2) if m.group(2) is not None else m.group(3)
            else:
                cjs.add((m.group(1), m.group(1)))
        m = re.search(r"module\.exports\s*=\s*(?:async\s+)?function\s*([\w$]*)\s*\(([^)]*)\)", text)
        if m:
            out[m.group(1) or "default"] = m.group(2)
        for exported, local in cjs:
            if not re.match(r"^[\w$]+$", local):
                continue
            fm = re.search(r"^\s*(?:async\s+)?function\s*\*?\s*%s\s*\(([^)]*)\)" % re.escape(local), text, re.M) or \
                re.search(r"^\s*(?:const|let|var)\s+%s\s*=\s*(?:async\s+)?(?:function\s*[\w$]*\s*)?\(([^)]*)\)" % re.escape(local), text, re.M)
            out[exported] = fm.group(1) if fm else None
        for m in re.finditer(r"^\s*export\s*\{([^}]*)\}", text, re.M):
            for part in m.group(1).split(","):
                bits = part.strip().split(" as ")
                local = bits[0].strip()
                name = (bits[1] if len(bits) > 1 else bits[0]).strip()
                if not local:
                    continue
                fm = re.search(r"^\s*(?:async\s+)?function\s*\*?\s*%s\s*\(([^)]*)\)" % re.escape(local), text, re.M) or \
                    re.search(r"^\s*(?:const|let|var)\s+%s\s*=\s*(?:async\s+)?\(([^)]*)\)" % re.escape(local), text, re.M)
                out[name] = fm.group(1) if fm else None
    elif ext in PY_EXT:
        allm = re.search(r"^__all__\s*=\s*[\[(]([^\])]*)[\])]", text, re.M)
        names = set(re.findall(r"['\"](\w+)['\"]", allm.group(1))) if allm else None
        for m in re.finditer(r"^(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)", text, re.M):
            n = m.group(1)
            if (names is not None and n in names) or (names is None and not n.startswith("_")):
                out[n] = m.group(2)
        for m in re.finditer(r"^class\s+(\w+)", text, re.M):
            n = m.group(1)
            if (names is not None and n in names) or (names is None and not n.startswith("_")):
                out.setdefault(n, None)
    elif ext == ".go":
        for m in re.finditer(r"^func\s+(?:\([^)]*\)\s*)?([A-Z]\w*)\s*\(([^)]*)\)", text, re.M):
            out[m.group(1)] = m.group(2)
    elif ext == ".rs":
        for m in re.finditer(r"^\s*pub\s+(?:async\s+)?fn\s+(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)", text, re.M):
            out[m.group(1)] = m.group(2)
    return out


def check_signatures(change, task):
    out = []
    task = task or ""
    asked_api = re.search(r"\b(signature|rename|renaming|refactor|breaking change|public api|change the api|new parameter|parameter)\b", task, re.I)
    for f in change.files:
        p = f.path
        e = ext_of(p)
        if f.status not in ("M", "R") or f.binary or f.skip or not _source_file(p) or e not in (JS_EXT | PY_EXT | {".go", ".rs"}):
            continue
        if is_cli_path(p) and e in PY_EXT:
            continue
        old_t, new_t = change.old_text(f.old_path), change.new_text(p)
        if not old_t or new_t is None:
            continue
        old_e, new_e = _exports(old_t, e), _exports(new_t, e)
        removed_text = "\n".join(t for _, t in f.removed)
        lang = "go" if e == ".go" else ("py" if e in PY_EXT else "js")
        hits = []
        for name, params in old_e.items():
            if not re.search(r"\b%s\b" % re.escape(name), removed_text) and name != "default":
                continue
            if name not in new_e:
                if _named_in_task(name, task) and REMOVAL_WORDS_RE.search(task):
                    continue
                if re.search(r"\b%s\b" % re.escape(name), new_t):
                    continue
                hits.append((name, "removed or renamed (no longer exported)", None))
                continue
            if params is None or new_e[name] is None:
                continue
            a, b = _param_info(params, lang), _param_info(new_e[name], lang)
            if [x[0] for x in a] == [x[0] for x in b] and [x[1] for x in a] == [x[1] for x in b]:
                continue
            ta, tb = _param_types(params), _param_types(new_e[name])
            if lang == "js" and len(a) == len(b) and ta == tb and all(t for t in ta) and [x[1] for x in a] == [x[1] for x in b]:
                continue  # renamed or destructured differently, same types: callers are unaffected
            compatible = len(b) >= len(a) and [x[0] for x in b[:len(a)]] == [x[0] for x in a] and all(o for _, o in b[len(a):])
            if compatible and all((not ao) or bo for (_, ao), (_, bo) in zip(a, b)):
                continue
            # asked for: the task names the function together with one of the new or removed parameters
            changed_params = set(x[0] for x in a) ^ set(x[0] for x in b)
            if _named_in_task(name, task) and any(_named_in_task(cp, task) for cp in changed_params if len(cp) >= 3):
                continue
            hits.append((name, "(%s) -> (%s)" % (re.sub(r"\s+", " ", params.strip()), re.sub(r"\s+", " ", new_e[name].strip())), None))
        if hits:
            out.append(finding(
                16, "Exported API changed in %s" % p,
                "The change alters what %s exports: %s. The task does not ask for an API change." % (
                    p, "; ".join("`%s` %s" % (n, d) for n, d, _ in hits[:4])),
                ["%s: `%s` %s" % (p, n, d) for n, d, _ in hits[:4]],
                "Every caller of %s that the change did not update (other modules, other packages, users of a library) breaks at runtime or build time." % ("it" if len(hits) == 1 else "them"),
                ["Keep the old signature (add new parameters as optional at the end, or add a new function), or update every caller and say so in your summary."],
                file=p, tier="check" if asked_api else "problem"))
    return out


# ---------------------------------------------------------------------------
# Cause 17: large or generated files
# ---------------------------------------------------------------------------

GEN_DIR_ALWAYS = {"node_modules", "__pycache__", "coverage", ".nyc_output", ".next", ".nuxt", ".svelte-kit",
                  ".turbo", ".parcel-cache", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".venv",
                  "venv", "htmlcov", ".gradle", ".cache", "storybook-static"}
GEN_DIR_MAYBE = {"dist", "build", "out", "target", ".output"}
GEN_FILE_RE = re.compile(r"\.(?:min\.js|min\.css|bundle\.js|chunk\.js|map|pyc|pyo|class|o|obj|so|dll|dylib|exe|log|tsbuildinfo)$|^\.DS_Store$|^Thumbs\.db$|\.egg-info", re.I)
DATA_EXT = {".sql", ".csv", ".tsv", ".json", ".jsonl", ".ndjson", ".xml", ".dump", ".bak", ".db", ".sqlite", ".sqlite3", ".parquet", ".log", ".har"}


def _dir_tracked_in_base(change, top):
    code, out = run_git(change.repo, ["ls-files", "-z", "--", top + "/"])
    if code != 0:
        return False
    added = set(f.path for f in change.files if f.status == "A")
    return any(p and p not in added for p in out.decode("utf-8", "replace").split("\0"))


CACHE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".nox", ".cache", ".parcel-cache",
              ".turbo", "coverage", ".nyc_output", "htmlcov"}


def build_output_dirs(repo):
    """Folders the project's own build writes to (running the checks creates them)."""
    dirs = set()
    pkg = load_json_text(read_text(os.path.join(repo, "package.json")) or "") or {}
    scripts = pkg.get("scripts") if isinstance(pkg, dict) and isinstance(pkg.get("scripts"), dict) else {}
    b = " ".join(str(v) for k, v in scripts.items() if "build" in k)
    if re.search(r"\b(vite|webpack|rollup|parcel|esbuild|tsup|microbundle|ncc)\b", b):
        dirs.add("dist")
    if "react-scripts" in b:
        dirs.add("build")
    if re.search(r"\bnext\b", b):
        dirs |= {".next", "out"}
    if re.search(r"\btsc\b", b):
        ts = load_json_text(re.sub(r"//.*", "", read_text(os.path.join(repo, "tsconfig.json")) or "")) or {}
        od = ((ts.get("compilerOptions") or {}).get("outDir") if isinstance(ts, dict) else None)
        dirs.add(posix(od).strip("./").split("/")[0] if od else "dist")
    for m in re.finditer(r"\b(?:node|python3?)\s+([\w./\-]+\.(?:js|mjs|cjs|py))", b):
        txt = read_text(os.path.join(repo, m.group(1))) or ""
        for dname in ("dist", "build", "out", "public/build"):
            if re.search(r"['\"/]%s['\"/]" % re.escape(dname), txt):
                dirs.add(dname)
    if os.path.isfile(os.path.join(repo, "setup.py")) or os.path.isfile(os.path.join(repo, "pyproject.toml")):
        dirs |= {"build", "dist"} if re.search(r"python3? -m build|setup\.py (?:build|sdist|bdist)", b) else set()
    return dirs


ARCHIVE_EXT_RE = re.compile(r"\.(?:tgz|tar|tar\.gz|tar\.bz2|tar\.xz|zip|7z|rar|whl|egg|jar|war|ear|nupkg|gem|crate|vsix|"
                            r"apk|aab|ipa|dmg|pkg|msi|deb|rpm|snap)$", re.I)


def check_large(change, task=None):
    out = []
    tracked_cache = {}
    artifact_dirs = build_output_dirs(change.repo)
    asset_task = bool(task and ASSET_TASK_RE.search(task))
    for f in change.files:
        if f.status not in ("A", "M", "R"):
            continue
        p = f.path
        parts = posix(p).split("/")
        low = [x.lower() for x in parts]
        b = parts[-1]
        why = None
        if f.folder_files:
            top = low[0] if low else ""
            gen = next((x for x in low if x in GEN_DIR_ALWAYS or x in GEN_DIR_MAYBE or x in CACHE_DIRS), None)
            soft = bool(gen) or top in artifact_dirs or p.lower() in artifact_dirs
            out.append(finding(
                17, "Untracked folder not gitignored: %s/ (%d files)" % (p, f.folder_files),
                "The folder %s/ (%d files) is new, untracked and not in .gitignore%s." % (
                    p, f.folder_files, "; it looks like build or cache output" if soft else ""),
                ["%s/ (%d untracked files, not listed one by one)" % (p, f.folder_files)],
                "The next `git add .` commits all of it: the repo grows, review drowns, and a copied or generated folder goes stale.",
                ["Add %s/ to .gitignore, or delete it if it is not needed; if it is real source, add it on purpose and say why." % p],
                file=p, tier="check" if soft else "problem"))
            continue
        if f.status == "A" and ARCHIVE_EXT_RE.search(b) and not is_test_path(p):
            out.append(finding(
                17, "Package or archive file in the change: %s" % p,
                "The change adds %s (%s), a packaged or archived build artifact." % (p, _size(f.size)),
                ["%s (new %s file)" % (p, ext_of(p).lstrip(".") or "archive")],
                "Build artifacts in git go stale immediately, bloat history forever, and can ship old code to whoever installs from the repo.",
                ["Remove %s from the change and add `*%s` (or the output folder) to .gitignore; publish packages through the registry instead." % (p, ext_of(p))],
                file=p, tier="check" if asset_task else "problem"))
            continue
        gen_dir = next((x for x in low[:-1] if x in GEN_DIR_ALWAYS or x.endswith(".egg-info")), None)
        if gen_dir == "coverage" and ext_of(p) in CODE_EXT and set(low[:low.index("coverage")]) & {"test", "tests", "src", "lib", "__tests__", "e2e"}:
            gen_dir = None  # a source folder that happens to be called coverage
        if gen_dir:
            why = "generated or installed output (%s/)" % gen_dir
        elif GEN_FILE_RE.search(b):
            why = "a generated or compiled file"
        else:
            maybe = next((i for i, x in enumerate(low[:-1]) if x in GEN_DIR_MAYBE), None)
            if maybe is not None and f.status == "A":
                top = "/".join(parts[:maybe + 1])
                if top not in tracked_cache:
                    tracked_cache[top] = _dir_tracked_in_base(change, top)
                if not tracked_cache[top]:
                    head = "\n".join(t for _, t in f.added[:40])
                    if ext_of(p) == ".map" or f.binary or any(len(t) > 300 for _, t in f.added[:40]) or \
                            "sourceMappingURL" in head or re.search(r"webpackChunk|__vite|__webpack_require__|@generated|Generated by", head) or \
                            re.search(r"[.\-_][0-9a-f]{8,}\.(js|css|mjs)$", b):
                        why = "build output (%s/)" % parts[maybe]
        if not why and (is_lockfile(p) or is_snapshot(p)):
            continue
        if not why and f.status == "M":
            continue  # already in the repo before this change: size alone is not new
        if not why:
            if f.binary and f.size > 200 * 1024:
                why = "a %s binary file" % _size(f.size)
            elif f.size > 1024 * 1024:
                why = "a %s file" % _size(f.size)
            elif ext_of(p) in DATA_EXT and f.size > 256 * 1024 and not is_lockfile(p):
                why = "a %s data file" % _size(f.size)
            elif f.status == "A" and not f.binary and f.added and \
                    re.search(r"@generated|DO NOT EDIT|auto-?generated|autogenerated|generated by", "\n".join(t for _, t in f.added[:6]), re.I) and \
                    not is_lockfile(p) and not is_snapshot(p) and f.size > 50 * 1024:
                why = "a large generated file (%s); some projects commit generated code on purpose" % _size(f.size)
        tier = "problem"
        if why and "on purpose" in why:
            tier = "check"
        if why and f.status in ("M", "R") and not f.untracked:
            tier = "check"
            why += "; it was already tracked before this change, so the project keeps it in git on purpose"
        if why and f.untracked:
            if (gen_dir in CACHE_DIRS) or (gen_dir is None and GEN_FILE_RE.search(b) and ext_of(b) in (".pyc", ".pyo")):
                tier = "check"
                why += "; untracked, probably left by a local test run, but not gitignored"
            elif low and low[0] in artifact_dirs or "/".join(low[:2]) in artifact_dirs:
                tier = "check"
                why += "; the project's own build writes here, so it may be output of running the build, but it is not gitignored"
        if why:
            out.append(finding(
                17, "Generated or large file in the change: %s" % p,
                "The change adds %s: %s." % (p, why),
                ["%s (%s, %s)" % (p, "new file" if f.status == "A" else "modified", _size(f.size))],
                "Generated and large files bloat the repo forever, hide the real change in review, and go stale the moment the source changes.",
                ["Remove %s from the change and add its folder or pattern to .gitignore; regenerate it in the build instead." % p],
                file=p, tier=tier))
    return _group_generated(out)


MEDIA_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".psd", ".heic", ".mp4", ".mov",
             ".webm", ".avi", ".mkv", ".mp3", ".wav", ".ogg", ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z",
             ".rar", ".pdf", ".docx", ".xlsx", ".pptx", ".numbers", ".pages"}
ASSET_TASK_RE = re.compile(r"\b(images?|screenshots?|icons?|logos?|pictures?|photos?|assets?|illustrations?|favicons?|"
                           r"banners?|fonts?|pdfs?|png|jpe?g|svg|gif|webp|videos?|audio|sounds?|archives?|zip|attachments?|"
                           r"fixtures?|sample files?)\b", re.I)


def _tree_mentions(repo, names, skip_paths, exclude):
    """Does any text file in the working tree mention one of these names? (git grep; a capped
    walk outside git, where hitting the cap counts as "mentioned")."""
    sp = set(skip_paths) | {exclude}
    r = None
    for n in names:
        r = tree_has(repo, n, sp, variants=False, ignore_case=False)
        if r:
            return True
    if r is not None:
        return False
    count = 0
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".git")]
        for fn in filenames:
            count += 1
            if count > 8000:
                return True
            full = os.path.join(dirpath, fn)
            rel = posix(os.path.relpath(full, repo))
            if rel in sp or ext_of(fn) in BINARY_EXT or ext_of(fn) in MEDIA_EXT:
                continue
            txt = read_text(full, 1024 * 1024)
            if txt and any(n in txt for n in names):
                return True
    return False


def check_stray_binaries(change, task, skip_paths=()):
    """Cause 17: a binary file (image, archive, document, media) added to the repo that nothing in
    the project refers to and the task did not ask for: a screenshot for the reviewer, an export,
    a download left behind. Larger binaries are reported by check_large whatever their use."""
    out = []
    if not change.ok or (task and ASSET_TASK_RE.search(task)):
        return out
    skip_paths = set(skip_paths)
    for f in change.files:
        p = f.path
        if f.status != "A" or p in skip_paths or not (f.binary or ext_of(p) in MEDIA_EXT):
            continue
        if f.size < 10 * 1024 or (f.binary and f.size > 200 * 1024) or f.size > 1024 * 1024:
            continue
        low = [x.lower() for x in posix(p).split("/")]
        if is_test_path(p) or set(low[:-1]) & (GEN_DIR_ALWAYS | GEN_DIR_MAYBE | {"fixtures", "__fixtures__", "testdata"}):
            continue
        b = base_of(p)
        stem = b.rsplit(".", 1)[0]
        names = [b] + ([stem] if len(stem) >= 6 and not stem.isdigit() else [])
        if _tree_mentions(change.repo, names, skip_paths, p):
            continue
        out.append(finding(
            17, "Binary file nothing uses: %s" % p,
            "The change adds %s (%s), and no file in the project refers to it; the task does not ask for an image, "
            "asset or document." % (p, _size(f.size)),
            ["%s (new %s file, %s)" % (p, ext_of(p).lstrip(".") or "binary", _size(f.size)),
             "searched the working tree for `%s`: no references" % b],
            "Binary files cannot be reviewed as a diff, stay in git history forever even after deletion, and an unused one "
            "is usually a screenshot or export meant for the person, not the repo.",
            ["Remove %s from the change. If it is a screenshot for review, put it in the PR description instead." % p],
            file=p))
    return out


def _group_generated(fs):
    """One finding per generated folder instead of one per file."""
    out, groups = [], {}
    for f in fs:
        parts = f["file"].split("/")
        top = None
        for i, x in enumerate(parts[:-1]):
            if x.lower() in GEN_DIR_ALWAYS or x.lower() in GEN_DIR_MAYBE or x.lower() in CACHE_DIRS:
                top = "/".join(parts[:i + 1])
                break
        if top is None:
            out.append(f)
            continue
        g = groups.get((top, f["tier"]))
        if g is None:
            groups[(top, f["tier"])] = f
            out.append(f)
        else:
            g["files"].append(f["file"])
            g.setdefault("_n", 1)
            g["_n"] += 1
            g["title"] = "Generated files in the change: %s/ (%d files)" % (top, g["_n"])
            if len(g["evidence"]) < 4:
                g["evidence"] += f["evidence"]
    for f in out:
        f.pop("_n", None)
    return out


def _size(n):
    if n >= 1024 * 1024:
        return "%.1f MB" % (n / 1048576.0)
    if n >= 1024:
        return "%d KB" % (n // 1024)
    return "%d bytes" % n


# ---------------------------------------------------------------------------
# Cause 8 (without a written rule): files that say "do not edit"
# ---------------------------------------------------------------------------

GENERATED_HEADER_RE = re.compile(r"@generated|DO NOT EDIT|do not edit|auto-?generated|autogenerated|"
                                 r"generated by|Code generated .* DO NOT EDIT|this file is generated", re.I)


def check_generated_edits(change):
    out = []
    for f in change.files:
        if f.status not in ("M", "D", "R") or f.binary or is_lockfile(f.path) or is_snapshot(f.path):
            continue
        old = change.old_text(f.old_path)
        if not old:
            continue
        head = "\n".join(old.splitlines()[:8])
        m = GENERATED_HEADER_RE.search(head)
        if not m:
            continue
        src = _regen_source(change, f)
        out.append(finding(
            8, "Generated file %s: %s" % ("changed with its source" if src else "edited by hand", f.path),
            ("%s says it is generated (\"%s\" in its header), and the change also edits %s, which looks like its source: "
             "confirm it was regenerated, not edited by hand." % (f.path, m.group(0), src)) if src else
            "%s says it is generated (\"%s\" in its header), and the change edits it directly." % (f.path, m.group(0)),
            ["%s: header says \"%s\"" % (f.path, m.group(0))] + (["source changed too: %s" % src] if src else []) +
            [_ev(f.path, ln, t) for ln, t in f.added[:2]],
            "The next code generation run silently overwrites a hand edit, so the fix disappears.",
            ["Revert the hand edit and change the source the file is generated from (schema, spec or template), then regenerate."
             if not src else "Run the project's generate command and check the file comes out identical."],
            file=f.path, tier="check" if src else "problem"))
    return out


REGEN_SOURCE_EXT = {".json", ".jsonc", ".json5", ".yaml", ".yml", ".toml", ".graphql", ".gql", ".proto", ".prisma",
                    ".sql", ".xml", ".csv", ".tsv", ".thrift", ".avsc", ".hbs", ".mustache", ".tmpl", ".tpl", ".j2"}


def _regen_source(change, gen):
    """A changed file that is plausibly what `gen` is generated from (schema, spec, data, template),
    or None. Lockfiles, manifests, tests, docs and other generated files do not count."""
    stem_toks = set(t for t in path_tokens(gen.path) if t not in ("generated", "gen", "src", "lib", "types", "index"))
    best = None
    for g in change.files:
        p = g.path
        if g is gen or g.status == "D" or is_lockfile(p) or is_manifest(p) or is_test_path(p) or is_doc(p):
            continue
        if GENERATED_HEADER_RE.search("\n".join(t for _, t in g.added[:8])) or (g.skip or "").startswith("generated"):
            continue
        b = base_of(p).lower()
        if ext_of(p) in REGEN_SOURCE_EXT or re.search(r"schema|spec|openapi|swagger|proto|wrangler|codegen|template", b):
            if best is None or (stem_toks & set(path_tokens(p))):
                best = p
    return best


# ---------------------------------------------------------------------------
# Cause 15: what the task names but the change does not contain
# ---------------------------------------------------------------------------

STYLE_WORDS = {"snake_case", "camelcase", "pascalcase", "kebab-case", "upper_case", "screaming_snake_case", "e.g", "i.e"}
BRAND_WORDS = {"iphone", "ipad", "ios", "macos", "ebay", "javascript", "typescript", "github", "gitlab", "youtube",
               "linkedin", "paypal", "wordpress", "openai", "chatgpt", "postgresql", "mysql", "mongodb", "graphql",
               "nodejs", "nextjs", "vscode", "oauth", "websocket", "dynamodb", "fastapi", "pytest", "unittest", "readme",
               "localhost", "devops", "dotenv", "npm", "pnpm", "yarn", "ipados", "watchos", "macbook", "jquery",
               "mariadb", "redis", "sqlite", "eslint", "prettier", "webpack", "vite", "jest", "vitest", "mocha"}
NEG_CTX_RE = re.compile(r"\b(not|never|without|avoid|instead|remove|removing|delete|deleting|drop|replace|replacing|rename|"
                        r"renaming|deprecate|existing|current|currently|old|legacy|don't|doesn't|do not|unlike|from|keep|leave|"
                        r"already|uses?|calls?|see|like|e\.g\.?|such as)\b", re.I)


def _task_identifiers(task):
    out = []
    if not task:
        return out
    for sent in re.split(r"(?<=[.!?\n])\s+", task):
        cands = []
        for m in re.finditer(r"`([^`\n]+)`", sent):
            cands.append((m.start(), m.group(1).strip(), True))
            # a command line in backticks (`search --limit N`): its flags are task items too
            if " " in m.group(1).strip():
                for fm in re.finditer(r"(?<![\w-])(--[a-z][\w-]+)", m.group(1)):
                    cands.append((m.start(), fm.group(1), True))
        plain = re.sub(r"`[^`\n]*`", lambda m: " " * len(m.group(0)), sent)
        for m in re.finditer(r"(?<![\w./-])([a-z]+(?:[A-Z][a-z0-9]+)+)(?![\w./-])|(?<![\w./-])([a-z][a-z0-9]*(?:_[a-z0-9]+)+)(?![\w./-])|"
                             r"(?<![\w./-])([A-Za-z_]\w+)\(\)|(?<![\w-])(--[a-z][\w-]+)", plain):
            tok = next(g for g in m.groups() if g)
            cands.append((m.start(), tok, False))
        for pos, tok, ticked in cands:
            before = sent[max(0, pos - 60):pos]
            last_words = " ".join(before.split()[-6:])
            if NEG_CTX_RE.search(last_words):
                continue
            t = tok.strip().rstrip(".,;:")
            t = re.sub(r"^([A-Za-z_$][\w$.]*)\([^()]*\)$", r"\1", t)
            if t.lower() in STYLE_WORDS or t.lower() in BRAND_WORDS:
                continue
            if " " in t or len(t) < 3:
                continue
            kind = None
            if t.startswith("--") and re.match(r"^--[a-z][\w-]+$", t):
                kind = "flag"
            elif re.match(r"^/[\w\-/:{}]+$", t):
                kind = "route"
            elif re.match(r"^[A-Za-z_$][\w$]*(\.[A-Za-z_$][\w$]*)*$", t):
                if not ticked and not re.search(r"[A-Z_]", t[1:]):
                    continue
                if ticked and re.match(r"^[a-z]+$", t) and len(t) < 4:
                    continue
                kind = "ident"
            elif ticked and re.match(r"^[\w.\-/]+\.\w{1,5}$", t) and "/" in t or (ticked and re.match(r"^[\w\-]+\.(js|ts|py|tsx|jsx|go|rs|sql)$", t)):
                kind = "path"
            if kind:
                creating = bool(re.search(r"\b(create|add|new|write|implement|introduce)\b", " ".join(before.split()[-5:]), re.I))
                out.append((kind, t, creating))
    seen, uniq = set(), []
    for k in out:
        if k[1] not in seen:
            seen.add(k[1])
            uniq.append(k)
    return uniq[:30]


def _norm_ident(s):
    return re.sub(r"[_\-]", "", s).lower()


def _tree_contains(repo, needles, skip_paths):
    """(found, complete): the needles that appear in a code or config file of the working tree,
    compared without case or _/- separators (user_id matches userId). git grep searches every
    tracked and untracked (not ignored) file; outside git a walk stops at 8000 files and then
    complete is False, so nothing may be called missing."""
    found = set()
    for n in needles:
        r = tree_has(repo, n, skip_paths, docs=False)
        if r is None:
            break
        if r:
            found.add(n)
    else:
        return found, True
    found = set()
    left = set(needles)
    count = 0
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".git")]
        for fn in filenames:
            count += 1
            if not left:
                return found, True
            if count > 8000:
                return found, False
            full = os.path.join(dirpath, fn)
            rel = posix(os.path.relpath(full, repo))
            if rel in skip_paths or ext_of(fn) in BINARY_EXT or ext_of(fn) in DOC_EXT:
                continue
            txt = read_text(full, 1024 * 1024)
            if not txt:
                continue
            ntxt = _norm_ident(txt)
            for n in list(left):
                if n in txt or (_norm_ident(n) and _norm_ident(n) in ntxt):
                    found.add(n)
                    left.discard(n)
    return found, True


ARG_PARSER_RE = re.compile(r"\b(argparse|add_argument|click\.option|typer|yargs|commander|minimist|parseArgs|"
                           r"\.option\s*\(|getopt|clap|cobra|flag\.(?:String|Bool|Int)|docopt)\b")


def _flag_variants(flag):
    name = flag.lstrip("-")
    camel = re.sub(r"[-_]([a-z0-9])", lambda m: m.group(1).upper(), name)
    return set([name, name.replace("-", "_"), camel])


def _flag_in(flag, text):
    """Is the command-line flag handled in this code? A literal `--limit`, a quoted option name
    ('limit', "dry_run"), or an option-table key (`limit: { type: 'string' }`). A plain variable
    called `limit` is not enough: that is how a missing flag hides behind unrelated code."""
    if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(flag), text):
        return True
    for v in _flag_variants(flag):
        ev = re.escape(v)
        if re.search(r"['\"]%s['\"]" % ev, text) or re.search(r"(?<![\w$.])%s\s*:\s*\{" % ev, text):
            return True
        if ARG_PARSER_RE.search(text) and re.search(r"\.%s\b" % ev, text):
            return True
    return False


def _tree_has_flags(repo, flags, skip_paths):
    """(found, complete) for command-line flags handled in non-test code files."""
    found = set()
    left = set(flags)
    cands = tree_files_with(repo, [fl.lstrip("-") for fl in flags], skip_paths, limit=400)
    if cands is not None:
        for rel in cands:
            if not left:
                break
            if ext_of(rel) not in CODE_EXT or is_test_path(rel) or rel in skip_paths:
                continue
            txt = read_text(os.path.join(repo, rel), 1024 * 1024) or ""
            for fl in list(left):
                if _flag_in(fl, txt):
                    found.add(fl)
                    left.discard(fl)
        return found, len(cands) < 400 or not left
    count = 0
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".git")]
        for fn in filenames:
            count += 1
            if not left:
                return found, True
            if count > 8000:
                return found, False
            full = os.path.join(dirpath, fn)
            rel = posix(os.path.relpath(full, repo))
            if rel in skip_paths or ext_of(fn) not in CODE_EXT or is_test_path(rel):
                continue
            txt = read_text(full, 1024 * 1024) or ""
            for fl in list(left):
                if _flag_in(fl, txt):
                    found.add(fl)
                    left.discard(fl)
    return found, True


def _flag_home(change, skip_paths):
    """The changed source file where the other command-line options are parsed."""
    best, score = None, 0
    for f in change.files:
        if f.status == "D" or f.path in skip_paths or not _source_file(f.path):
            continue
        txt = change.new_text(f.path) or ""
        n = len(re.findall(r"['\"`]--[a-z][\w-]+", txt)) + (3 if ARG_PARSER_RE.search(txt) else 0) + (2 if is_cli_path(f.path) else 0)
        if n > score:
            best, score = f.path, n
    return best


def check_acceptance(change, task, skip_paths=(), notes=None):
    out = []
    if not task or not change.ok:
        return out
    ids = _task_identifiers(task)
    if not ids:
        return out
    skip_paths = set(skip_paths)
    # Docs and summaries describing a feature are not the feature: only code counts as present.
    code_files = [f for f in change.files if f.path not in skip_paths and not is_doc(f.path) and ext_of(f.path) not in DOC_EXT]
    added_text = "\n".join(t for f in code_files for _, t in f.added)
    added_src = "\n".join(t for f in code_files if not is_test_path(f.path) for _, t in f.added)
    missing = []
    needles = []
    flags = []
    found_items = []
    for kind, tok, creating in ids:
        if kind == "path":
            if creating and not os.path.exists(os.path.join(change.repo, tok)):
                missing.append((kind, tok))
            else:
                found_items.append(tok)
            continue
        if kind == "flag":
            if _flag_in(tok, added_src):
                found_items.append(tok)
            else:
                flags.append(tok)
            continue
        n = tok.split(".")[-1] if kind == "ident" and "." in tok else tok
        if kind == "route":
            n = re.split(r"[{:<]", tok)[0] or tok
        if n in added_text or (kind == "ident" and _norm_ident(n) in _norm_ident(added_text)):
            found_items.append(tok)
            continue
        needles.append((kind, tok, n))
    unsure = []
    if needles:
        present, complete = _tree_contains(change.repo, [n for _, _, n in needles], skip_paths)
        for kind, tok, n in needles:
            if n in present:
                found_items.append(tok)
            elif complete:
                missing.append((kind, tok))
            else:
                unsure.append(tok)
    if flags:
        present, complete = _tree_has_flags(change.repo, flags, skip_paths)
        for fl in flags:
            if fl in present:
                found_items.append(fl)
            elif complete:
                missing.append(("flag", fl))
            else:
                unsure.append(fl)
    if unsure and notes is not None:
        notes.append("Task items not checked (the tree was too large to search outside git): %s." % ", ".join("`%s`" % t for t in unsure[:8]))
    if notes is not None and (found_items or missing):
        notes.append("Task items matched mechanically: %d found in the code (%s)%s. The rest of the task (behaviour, "
                     "edge cases, numbers) is for your review pass: review-checklist section 1." % (
                         len(found_items), ", ".join("`%s`" % t for t in found_items[:8]) or "none",
                         ("; %d missing (%s)" % (len(missing), ", ".join("`%s`" % t for _, t in missing[:6]))) if missing else ""))
    if missing:
        target = None
        if all(k == "flag" for k, _ in missing):
            target = _flag_home(change, skip_paths)
        for p in ([] if target else task_paths(task)):
            if ext_of(p) in CODE_EXT:
                target = p
                break
        doc_claims = []
        for f in change.files:
            if f.path in skip_paths or not (is_doc(f.path) or ext_of(f.path) in DOC_EXT):
                continue
            for ln, t in f.added:
                if any(tok in t for _, tok in missing):
                    doc_claims.append(_ev(f.path, ln, t, 120))
                    break
        ev = ["task: %s" % ", ".join(t for _, t in missing[:6]),
              "searched: %d added lines of code and the working tree's code files" % len(added_text.splitlines())]
        if doc_claims:
            ev += ["documented but not implemented: %s" % doc_claims[0]] + doc_claims[1:2]
        if target and all(k == "flag" for k, _ in missing):
            ev.append("expected in: %s (where the other command-line options are parsed)" % target)
        out.append(finding(
            15, "Named in the task but missing from the code: %s" % ", ".join("`%s`" % t for _, t in missing[:4]),
            "The task names %s, but %s nowhere in the code%s." % (
                ", ".join("`%s`" % t for _, t in missing[:6]), "it appears" if len(missing) == 1 else "they appear",
                " (only the docs mention it)" if doc_claims else ""),
            ev,
            "The checks can all pass while the thing the person asked for does not exist.",
            ["Implement %s as the task describes, or tell the person plainly that it is not done." % ", ".join("`%s`" % t for _, t in missing[:4])],
            file=None, files=[target] if target else []))
    return out


# ---------------------------------------------------------------------------
# Cause 7: scope
# ---------------------------------------------------------------------------

GENERIC_TOKENS = {"src", "lib", "app", "apps", "packages", "package", "pkg", "index", "main", "mod", "init",
                  "test", "tests", "spec", "specs", "js", "ts", "py", "utils", "util", "helpers", "helper",
                  "common", "shared", "core", "internal", "public", "static", "assets", "components", "component",
                  "source", "sources", "modules", "module", "file", "files", "new", "old", "misc", "base", "default",
                  "github", "workflows", "config", "configs", "scripts", "script", "types", "type", "models", "model",
                  "views", "view", "routes", "route", "pages", "page", "services", "service", "api"}
NEUTRAL_RE = re.compile(r"(^|/)(changelog|changes|history)(\.\w+)?$|(^|/)\.gitignore$|(^|/)\.(shipsnag|techfix)/", re.I)


def _imports(text, stem):
    """Does text import or require a module named stem?"""
    if not stem or len(stem) < 3 or stem in ("index", "__init__", "main"):
        return False
    st = re.escape(stem)
    return bool(re.search(r"['\"](?:\.{1,2}/|@/|~/)(?:[\w.@-]+/)*%s(?:\.\w+)?['\"]|^\s*import\s+(?:[\w.]+\.)?%s\b|"
                          r"^\s*from\s+[\w.]*\b%s\s+import\b|^\s*from\s+[\w.]+\s+import\s+.*\b%s\b" % (st, st, st, st), text, re.M))


ALLOWLIST_RE = re.compile(
    r"\b(?:only|just)\s+(?:touch|change|edit|modify|update)\b|"
    r"\b(?:limit|restrict|keep|confine)\s+(?:your\s+|the\s+|all\s+)?(?:changes?|edits?|the change|the work)\s+(?:to|within|inside)\b|"
    r"\b(?:don't|do not|never)\s+(?:touch|change|edit|modify)\s+(?:anything|any (?:other )?files?)\s*(?:else|other than|outside|besides|except|beyond)?\b|"
    r"\bno other files\b|\bnothing else\b", re.I)
STYLE_EXT = {".css", ".scss", ".sass", ".less", ".styl"}


def task_allowlist(task):
    """Files the task explicitly limits the change to ("Only touch a.py, b.py and the tests").
    Returns (sentence, paths, allow_tests, allow_docs) or None."""
    for sent in re.split(r"(?<=[.!?])\s+|\n\s*\n", task or ""):
        if not ALLOWLIST_RE.search(sent):
            continue
        paths = [p for p in task_paths(sent) if p]
        if not paths:
            continue
        low = sent.lower()
        return (re.sub(r"\s+", " ", sent.strip()), paths,
                bool(re.search(r"\b(?:the\s+)?(?:tests?|specs?|test files?)\b", low)),
                bool(re.search(r"\b(?:docs?|documentation|readme)\b", low)))
    return None


def _allowed(path, paths):
    for tp in paths:
        tpn = tp.strip("/")
        if path == tpn or path.endswith("/" + tpn) or path.startswith(tpn.rstrip("/") + "/") or glob_match(path, tpn):
            return True
    return False


def _style_selectors(lines):
    names = set()
    for t in lines:
        if "{" in t or re.match(r"^\s*[.#][\w-]", t):
            for m in re.finditer(r"(?<![\w-])[.#]([A-Za-z_][\w-]{2,})", t.split("{")[0]):
                names.add(m.group(1))
    return names


def check_scope(change, task, skip_paths=()):
    """Out-of-scope files. Returns findings (problem for code and config, check for docs)."""
    if not task or not change.ok or not change.files:
        return [], "no task given"
    tw = task_words(task)
    tpaths = task_paths(task)
    tests_asked = bool(re.search(r"\b(tests?|specs?|testing)\b", task, re.I))
    files = [f for f in change.files if f.path not in skip_paths]
    in_scope = set()
    # Folders that only hold the files the task names ("mypkg/" in `mypkg/worker.py`) say where
    # those files are, not that every sibling is in scope.
    named_dirs = set()
    for tp in tpaths:
        if "." in base_of(tp):
            for seg in posix(tp).split("/")[:-1]:
                named_dirs |= set(split_ident(seg))
    dir_only = set()

    ci_asked = bool(re.search(r"\b(?:CI|ci|workflows?|pipelines?|github actions|gitlab ci|continuous integration)\b", task))

    def direct(f):
        p = f.path
        if ci_asked and (posix(p).startswith((".github/workflows/", ".circleci/", ".buildkite/")) or
                         base_of(p).lower() in (".gitlab-ci.yml", "azure-pipelines.yml", "bitbucket-pipelines.yml", ".travis.yml", "jenkinsfile")):
            return True
        for tp in tpaths:
            tpn = tp.strip("/")
            if p == tpn or p.endswith("/" + tpn) or p.startswith(tpn.rstrip("/") + "/") or \
                    (f.old_path == tpn) or base_of(p) == base_of(tpn) and "." in base_of(tpn):
                return True
        parts = posix(p).split("/")
        dir_toks = set(t for seg in parts[:-1] for t in split_ident(seg))
        base_toks = set(path_tokens(parts[-1]))
        toks = [t for t in path_tokens(p) if len(t) >= 3 and t not in GENERIC_TOKENS]
        hit = [t for t in toks if t in tw or stem_word(t) in tw]
        real = [t for t in hit if not (t in named_dirs and t in dir_toks and t not in base_toks)]
        if hit and not real:
            dir_only.add(p)
        return bool(real)

    named = set(t for t in re.findall(r"`([A-Za-z_$][\w$]{4,})`|\b([A-Z][A-Z0-9]*_[A-Z0-9_]{3,})\b|\b([a-z]+(?:[A-Z][a-z0-9]+)+)\b", task)
                for t in t if t)
    for f in files:
        if direct(f):
            in_scope.add(f.path)
        elif named and f.status != "D":
            own = "\n".join(t for _, t in f.added)
            if any(re.search(r"(?<![\w$])%s(?![\w$])" % re.escape(n), own) for n in named):
                in_scope.add(f.path)
    if not in_scope and not task_allowlist(task):
        return [], "the task names no file or area that matches the change"
    for _ in range(3):
        grew = False
        scope_toks = set()
        for p in in_scope:
            scope_toks |= set(stem_word(t) for t in path_tokens(p) if t not in GENERIC_TOKENS and len(t) >= 3)
        added_in_scope = "\n".join(t for f in files if f.path in in_scope for _, t in f.added)
        for f in files:
            if f.path in in_scope:
                continue
            toks = set(stem_word(t) for t in path_tokens(f.path) if t not in GENERIC_TOKENS and len(t) >= 3)
            stem = base_of(f.path).split(".")[0]
            own = "\n".join(t for _, t in f.added)
            if is_test_path(f.path) or is_snapshot(f.path):
                refs = any(base_of(q).split(".")[0] and len(base_of(q).split(".")[0]) >= 3 and base_of(q).split(".")[0] in own
                           for q in in_scope)
                if toks & scope_toks or toks & tw or refs or (tests_asked and f.status != "D"):
                    in_scope.add(f.path)
                    grew = True
                    continue
            elif f.status != "D" and any(_imports(own, base_of(q).split(".")[0]) for q in in_scope if f.path != q):
                in_scope.add(f.path)
                grew = True
                continue
            if stem and _imports(added_in_scope, stem):
                in_scope.add(f.path)
                grew = True
        if not grew:
            break
    in_scope_text = "\n".join(change.new_text(q) or "" for q in in_scope if ext_of(q) in CODE_EXT)
    mentioned = set()
    for f in files:
        if f.path in in_scope and not is_test_path(f.path) and not is_doc(f.path):
            # only words the change newly writes in in-scope code: a rewritten line that already said "color" does not
            # make colors.js related
            old_words = Counter(stem_word(x) for _, t in f.removed for x in split_ident(t) if len(x) >= 4)
            new_words = Counter(stem_word(x) for _, t in f.added for x in split_ident(t) if len(x) >= 4)
            mentioned |= set(w for w, n in new_words.items() if n > old_words.get(w, 0))
    in_scope_all_text = "\n".join(change.new_text(q) or "" for q in in_scope if not is_test_path(q))
    allow = task_allowlist(task)
    out = []
    for f in files:
        p = f.path
        if is_lockfile(p) or is_manifest(p) or NEUTRAL_RE.search(p):
            continue
        if allow:
            # The person drew the line themselves: anything outside it is out of scope, however related.
            sent, apaths, a_tests, a_docs = allow
            a_tests = a_tests or tests_asked
            a_docs = a_docs or bool(re.search(r"\b(?:readme|docs?|documentation|changelog)\b", task, re.I))
            if _allowed(p, apaths) or (a_tests and (is_test_path(p) or is_snapshot(p))) or (a_docs and is_doc(p)):
                continue
            verb = {"A": "adds", "D": "deletes", "R": "renames"}.get(f.status, "edits")
            out.append(finding(
                7, "Outside the task: %s" % p,
                "The task limits the change to %s, and the change %s %s." % (", ".join("`%s`" % x for x in apaths[:5]) +
                                                                               (" and the tests" if a_tests else ""), verb, p),
                ["task: \"%s\"" % (sent if len(sent) <= 160 else sent[:157] + "..."),
                 "%s (%s, +%d/-%d lines)" % (p, verb[:-1] if verb.endswith("s") else verb, len(f.added), len(f.removed))],
                "The person said which files may change; an edit anywhere else is work they did not ask for and will not expect in review.",
                ["Revert %s. If the task cannot be done without it, ask the person first." % p],
                file=p, tier="check" if is_doc(p) else "problem"))
            continue
        if p in in_scope:
            continue
        used = _imports(in_scope_text, base_of(p).split(".")[0])
        stem_toks = set(stem_word(t) for t in split_ident(base_of(p).split(".")[0]) if len(t) >= 4 and t not in GENERIC_TOKENS)
        related = bool(stem_toks) and stem_toks <= mentioned
        styled = False
        if ext_of(p) in STYLE_EXT and f.status != "D":
            sels = _style_selectors(t for _, t in f.added)
            styled = any(re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(s), in_scope_all_text) for s in sels)
        sibling = p in dir_only and not is_test_path(p)
        soft = is_doc(p) or is_env_template(p) or is_snapshot(p) or used or related or styled or sibling
        verb = {"A": "adds", "D": "deletes", "R": "renames"}.get(f.status, "edits")
        if used:
            why = "The change %s %s, which the task does not mention; in-scope code imports it, so check the edit was needed." % (verb, p)
        elif related:
            why = "The change %s %s, which the task does not mention; the in-scope change refers to its name, so check the edit was needed." % (verb, p)
        elif styled:
            why = "The change %s %s, which the task does not mention; it styles markup the in-scope change uses, so check the edit was needed." % (verb, p)
        elif sibling:
            why = "The change %s %s, which the task does not mention; it is in the same package as the files the task names, so check the edit was needed." % (verb, p)
        else:
            why = "The change %s %s, which the task does not mention and no in-scope file uses." % (verb, p)
        out.append(finding(
            7, "Outside the task: %s" % p, why,
            ["%s (%s, +%d/-%d lines)" % (p, verb[:-1] if verb.endswith("s") else verb, len(f.added), len(f.removed))],
            "Unrequested edits widen the blast radius, are easy to miss in review, and can break things the task never touched.",
            ["Revert %s unless the task needs it; if it does, say why in your summary." % p],
            file=p, tier="check" if soft else "problem"))
    return out, "%d of %d changed files match the task" % (len(in_scope), len(files))


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def _merge(findings):
    """Merge problem findings on the same file when they are the same cause, when one is a
    scope finding, or when a lockfile is flagged both as a rule break and as churn."""
    out = []
    by_file = {}
    for f in findings:
        if f["tier"] != "problem" or not f["file"]:
            out.append(f)
            continue
        key = f["file"]
        existing = by_file.setdefault(key, [])
        target = None
        if f["cause"] == 7 and existing:
            target = existing[0]
        else:
            target = next((e for e in existing if e["cause"] == f["cause"] or e["cause"] == 7 or
                           (is_lockfile(key) and {e["cause"], f["cause"]} <= {8, 11})), None)
        if target is None:
            existing.append(f)
            out.append(f)
            continue
        if target["cause"] == 7 and f["cause"] != 7:
            keep, other = f, target
            out[out.index(target)] = keep
            existing[existing.index(target)] = keep
        else:
            keep, other = target, f
        for c in other["causes"]:
            if c not in keep["causes"]:
                keep["causes"].append(c)
        if other["cause"] == 7:
            keep["finding"] += " It is also outside the task's scope."
        elif other["cause"] == keep["cause"]:
            keep["finding"] += " Also: %s." % other["title"]
            keep["evidence"] += [e for e in other["evidence"] if e not in keep["evidence"]][:3]
        else:
            keep["evidence"] += [e for e in other["evidence"] if e not in keep["evidence"]][:2]
        for p_ in other.get("files", []):
            if p_ not in keep["files"]:
                keep["files"].append(p_)
    return out


LINE_CAP = 1000
CHECK_BUDGET = 30


def content_view(change):
    """A copy of the change for the line checks: files that are minified, generated or vendored
    keep their path but lose their lines (they are not hand-written), and every other line is cut
    to LINE_CAP characters so no regex ever sees a 50 MB line. Returns (view, [(path, reason)])."""
    import copy
    view = copy.copy(change)
    files, skipped = [], []
    for f in change.files:
        g = FileChange(f.path, f.status, f.old_path)
        g.binary, g.untracked, g.size, g.folder_files = f.binary, f.untracked, f.size, f.folder_files
        reason = None
        if not f.binary and f.status != "D" and not f.folder_files and (f.added or f.size):
            head = None
            if not f.untracked:
                try:
                    with open(os.path.join(change.repo, f.path), "rb") as fh:
                        head = fh.read(4096).decode("utf-8", "replace")
                except OSError:
                    head = None
            reason = content_skip_reason(f.path, f.added, head)
        f.skip = reason
        g.skip = reason
        if reason:
            skipped.append((f.path, reason))
        else:
            g.added = [(ln, t[:LINE_CAP]) for ln, t in f.added]
            g.removed = [(ln, t[:LINE_CAP]) for ln, t in f.removed]
            g.hunks = [{"removed": [(ln, t[:LINE_CAP]) for ln, t in h["removed"]],
                        "added": [(ln, t[:LINE_CAP]) for ln, t in h["added"]]} for h in f.hunks]
        files.append(g)
    view.files = files
    return view, skipped


class _CheckTimeout(Exception):
    pass


def _timed(name, fn, notes, stopped, *args):
    """Run one check with a hard time budget (SIGALRM where available)."""
    import signal
    import threading
    use_alarm = hasattr(signal, "setitimer") and threading.current_thread() is threading.main_thread()
    old = None
    if use_alarm:
        def _raise(signum, frame):
            raise _CheckTimeout()
        old = signal.signal(signal.SIGALRM, _raise)
        signal.setitimer(signal.ITIMER_REAL, CHECK_BUDGET)
    try:
        return fn(*args) or []
    except _CheckTimeout:
        stopped.append(name)
        notes.append("The %s inspection was stopped after %d s (time budget) and its results are missing." % (name, CHECK_BUDGET))
        return []
    finally:
        if use_alarm:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)


def inspect(change, task=None, mech_rules=(), rule_files=(), skip_paths=(), test_runs=(), info=None):
    """All change findings plus notes about what was or wasn't judged. info (optional dict)
    receives coverage details: skipped files and stopped inspections."""
    import rules as RL
    import fakes as FK
    notes = []
    info = info if info is not None else {}
    if not change.ok:
        return [], [change.reason]
    if change.nochange:
        info.update({"skipped": [], "stopped": [], "files": 0})
        return [], []
    view, skipped = content_view(change)
    stopped = []
    info["skipped"] = skipped
    info["stopped"] = stopped
    info["files"] = len(change.files)
    if skipped:
        kinds = Counter(r.split(" (")[0] for _, r in skipped)
        notes.append("Line checks skipped %d file%s that are not hand-written (%s): %s%s." % (
            len(skipped), "" if len(skipped) == 1 else "s", ", ".join("%d %s" % (n, k) for k, n in kinds.most_common()),
            ", ".join(p for p, _ in skipped[:5]), " and %d more" % (len(skipped) - 5) if len(skipped) > 5 else ""))
    T = lambda name, fn, *a: _timed(name, fn, notes, stopped, *a)  # noqa: E731
    fs = []
    fs += T("tests", check_tests, view, task)
    fs += T("test discovery", check_test_discovery, view, test_runs, set(skip_paths))
    fs += T("debug", check_debug, view)
    fs += T("secrets", check_secrets, view)
    fs += T("dependencies", check_deps, change, task)
    fs += T("migrations", check_migrations, change)
    fs += T("stubs", check_stubs, view)
    fs += T("escapes", check_escapes, view)
    fs += T("signatures", check_signatures, view, task)
    fs += T("large files", check_large, change, task)
    fs += T("stray binaries", check_stray_binaries, change, task, skip_paths)
    fs += T("generated files", check_generated_edits, change)
    fs += T("quiet fakes", FK.check_fakes, view, change, task, test_runs, skip_paths)
    fs += T("project rules", RL.check_rules, [r for r in mech_rules if r["kind"] != "require-cmd"], view, rule_files, task)
    fs += T("task items", check_acceptance, view, task, skip_paths, notes)
    scope, note = check_scope(view, task, skip_paths)
    if task is None:
        notes.append("No task description given, so scope and acceptance criteria were not checked (pass --task or --task-file).")
    elif not scope and "match" not in note:
        notes.append("Scope: %s." % note)
    elif "names no file" in note:
        notes.append("Scope not judged: %s." % note)
    fs += scope
    fs = _merge(fs)
    # stable order: problems first, by cause then file
    fs.sort(key=lambda f: (0 if f["tier"] == "problem" else 1, f["cause"], f["file"] or ""))
    return fs, notes


def main(argv=None):
    import report as R
    ap = argparse.ArgumentParser(description="Inspect a change for the quiet ways 'done' is not done.")
    ap.add_argument("repo")
    ap.add_argument("--base")
    ap.add_argument("--task")
    ap.add_argument("--task-file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    from common import load_change
    import rules as RL
    task = a.task
    if a.task_file:
        task = read_text(a.task_file) or ""
    ch = load_change(a.repo, a.base)
    mech, read, rfiles = RL.parse_rules(os.path.abspath(a.repo))
    fs, notes = inspect(ch, task, mech, rfiles)
    if a.json:
        sys.stdout.write(json.dumps({"change": ch.how or ch.reason, "files": [f.to_json() for f in ch.files],
                                     "findings": fs, "notes": notes}, indent=2) + "\n")
    else:
        for f in fs:
            sys.stdout.write(R.render_finding(f, 0) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
