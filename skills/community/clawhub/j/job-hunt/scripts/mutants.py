#!/usr/bin/env python3
"""Mutation testing: break the code on purpose and see whether the suite notices.

Why this exists as a checked-in tool rather than a one-off measurement. On
2026-08-23 an audit generated 421 mutants against this repo and 98 of them
SURVIVED — the suite stayed green with the code deliberately broken — and the
survivors were concentrated exactly where the damage is highest: render_cv.py
32/64, check_claims.py 11/26, check_shortlist.py 8/46. Six content branches of
`build_latex` and four of `render_docx` could each be turned into `if False:`
with 1062 tests still passing.

A number measured once is a number that rots. What makes this actionable is the
BASELINE: the survivors known at the time are recorded in `mutants-baseline.json`
with a note each, and `--ci` fails only on survivors that are NOT in it. So the
existing debt does not block anyone, and a change that makes the suite blinder
than it already was does.

    exit 0  no new survivors
    exit 1  new survivors, printed one per line
    exit 2  could not run

Usage:
    python3 scripts/mutants.py --ci                 # the three highest-damage files
    python3 scripts/mutants.py --targets scripts/check_apply.py
    python3 scripts/mutants.py --targets ... --record   # rewrite the baseline
    python3 scripts/mutants.py --ci --targets scripts/render_cv.py --shard 2/3

`--record` is deliberately not something CI can do: a harness that updates its own
baseline reports success by forgetting.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASELINE = pathlib.Path(__file__).resolve().parent / "mutants-baseline.json"

# The files where a surviving mutant costs the most: the gate that authorises
# delivery, the gate the skill calls its highest-value rule, and the renderer
# whose output is the only artifact an employer ever sees.
DEFAULT_TARGETS = (
    "scripts/check_apply.py",
    "scripts/check_claims.py",
    "scripts/render_cv.py",
)

# Which test modules exercise which target, so a killed mutant dies in seconds
# instead of costing a full suite run. Survival is always confirmed against the
# WHOLE suite — a mutant that only the targeted module misses is still killed.
FAST_TESTS = {
    "check_apply.py": ["test_check_apply.py", "test_receipts_bind_to_bytes.py",
                       "test_structured_only_apply.py"],
    "check_claims.py": ["test_check_claims.py"],
    "render_cv.py": ["test_render_cv.py", "test_render_artifact_integrity.py",
                     "test_render_pdf_compile.py"],
}


class Unattributable(RuntimeError):
    """The suite failed on the unmutated copy — no verdict can be attributed."""


class Mutation:
    __slots__ = ("path", "lineno", "original", "mutated", "operator", "span",
                 "occurrence")

    def __init__(self, path, lineno, original, mutated, operator, span=1,
                 occurrence=0):
        self.path, self.lineno = path, lineno
        self.original, self.mutated, self.operator = original, mutated, operator
        # Which occurrence of this identical line within the file. Without it,
        # every `findings.append(` in a file shares one key — measured: 7 sites in
        # check_apply.py, 54 mutants across 23 keys in render_cv.py — so ONE
        # recorded survivor silently pre-waives all the others, including sites
        # added later. Line-number-independent still: inserting code elsewhere
        # does not renumber these, only inserting an identical line above one does.
        self.occurrence = occurrence
        # How many source lines this mutant REPLACES. `findings.append(` is
        # routinely a multi-line call, and replacing only its opening line leaves
        # the continuation lines dangling — a SyntaxError, which fails the suite
        # and is then indistinguishable from the suite catching the mutation.
        # That would inflate the kill rate with mutants that tested nothing.
        self.span = span

    @property
    def key(self) -> str:
        """Identity that survives edits ELSEWHERE in the file.

        Deliberately not the line number: renaming a variable forty lines up
        would renumber every entry and silently empty the baseline, which is the
        failure mode a baseline exists to prevent.
        """
        payload = "\x00".join([self.path, self.operator,
                               " ".join(self.original.split()),
                               " ".join(self.mutated.split()),
                               str(self.occurrence)])
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def describe(self) -> str:
        return (f"{self.path}:{self.lineno} [{self.operator}]\n"
                f"      - {self.original.strip()}\n"
                f"      + {self.mutated.strip()}")


# ── operators ─────────────────────────────────────────────────────────────────

_COMPARISONS = (
    (re.compile(r"(?<![=!<>])==(?!=)"), "!=", "eq->ne"),
    (re.compile(r"!=(?!=)"), "==", "ne->eq"),
    (re.compile(r"(?<![<>=!])<=(?!=)"), ">", "le->gt"),
    (re.compile(r"(?<![<>=!])>=(?!=)"), "<", "ge->lt"),
    (re.compile(r"\bnot in\b"), "in", "notin->in"),
)
_IF = re.compile(r"^(\s*)(el)?if\s+.+:\s*(#.*)?$")
_APPEND = re.compile(r"^(\s*)(?:findings|out|results)\.append\(")


def _skip(line: str) -> bool:
    stripped = line.strip()
    return (not stripped or stripped.startswith("#")
            or stripped.startswith('"""') or stripped.startswith("'''"))


def _statement_span(lines: list, index: int) -> int:
    """How many lines the statement starting at `index` occupies, by paren balance."""
    depth, span = 0, 0
    for line in lines[index:]:
        code = line.split("#", 1)[0]
        depth += code.count("(") + code.count("[") + code.count("{")
        depth -= code.count(")") + code.count("]") + code.count("}")
        span += 1
        if depth <= 0:
            break
    return max(span, 1)


def generate(path: pathlib.Path, relative: str) -> list:
    """Every mutant for one file, mechanically — never by taste."""
    out = []
    seen: dict = {}

    def nth(operator, original, mutated) -> int:
        signature = (operator, " ".join(original.split()), " ".join(mutated.split()))
        seen[signature] = seen.get(signature, -1) + 1
        return seen[signature]

    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines, 1):
        if _skip(line):
            continue
        # 1. make a guard unreachable — how a content branch dies silently
        m = _IF.match(line)
        if m:
            indent, elif_ = m.group(1), m.group(2) or ""
            mutated = f"{indent}{elif_}if False:"
            out.append(Mutation(relative, i, line, mutated, "guard->False",
                                occurrence=nth("guard->False", line, mutated)))
        # 2. drop a finding — the gate still runs and reports nothing.
        #    Spans the WHOLE call: these are usually multi-line.
        if _APPEND.match(line):
            indent = _APPEND.match(line).group(1)
            span = _statement_span(lines, i - 1)
            mutated = f"{indent}pass  # mutated"
            out.append(Mutation(relative, i, line, mutated, "drop-finding",
                                span=span,
                                occurrence=nth("drop-finding", line, mutated)))
        # 3. invert a comparison
        for pattern, replacement, operator in _COMPARISONS:
            if pattern.search(line):
                mutated = pattern.sub(replacement, line, count=1)
                out.append(Mutation(relative, i, line, mutated, operator,
                                    occurrence=nth(operator, line, mutated)))
                break
    return out


# ── running ───────────────────────────────────────────────────────────────────

# Tests that cannot hold in a COPY of the repo, and are not about the code under
# mutation. test_install.py asserts that ~/.claude/skills/job-hunt is a symlink
# resolving to the repo root — true of the installation, false of any copy. It
# would fail for every mutant, making all of them look killed.
DESELECT = ("test_install.py",)

# No bytecode cache in the mutation copy. A .pyc is trusted when the source's
# mtime (whole seconds) and size match the ones it was compiled from, and most
# operators here keep the size: `==` -> `!=` is the same length. A mutant that
# dies in under a second is restored within the second it was written, so the
# mutated .pyc stays "fresh" and every later run imports the mutant instead of
# the restored source. The last mutant of check_claims.py flips its
# `if __name__ == "__main__":`, the stale module exits on import, and from then
# on the pristine copy fails: the scheduled run of 2026-09-21 stopped on the
# first render_cv.py mutant for exactly that reason. The same race runs the other
# way too: a mutant written in the second after a green run is served the
# pristine .pyc and "survives" without ever running, so a baseline recorded
# before this fix may list survivors that were never tested. Children inherit
# the env, so the python subprocesses the suite spawns write no cache either.
_ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def _run_pytest(cwd: pathlib.Path, targets: list) -> subprocess.CompletedProcess:
    argv = [sys.executable, "-m", "pytest", "-q", "-x", "--no-header", "-p", "no:cacheprovider"]
    for name in DESELECT:
        argv += ["--ignore", str(cwd / "scripts" / "tests" / name)]
    argv += [str(cwd / "scripts" / "tests" / t) for t in targets] if targets else [str(cwd / "scripts" / "tests")]
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", env=_ENV)


def _pytest(cwd: pathlib.Path, targets: list) -> bool:
    """True when the suite PASSES (i.e. the mutant survived this run)."""
    return _run_pytest(cwd, targets).returncode == 0


def _copy_repo(destination: pathlib.Path) -> None:
    """Copy source without following links or including private output artifacts."""
    generated = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "*.pyc")

    def ignore(directory, names):
        excluded = set(generated(directory, names))
        if pathlib.Path(directory) == ROOT:
            excluded.add("output")  # ignored client reports and old test workspaces
        return excluded

    shutil.copytree(ROOT, destination, symlinks=True, ignore=ignore)


def _tail(proc: subprocess.CompletedProcess, lines: int = 30) -> str:
    """The end of a red run, for the two verdicts that stop the harness. The
    runs of 2026-08-31 and 2026-09-07 said only "not green before mutating",
    and nothing on the page said which test."""
    text = (proc.stdout or "") + (proc.stderr or "")
    return "\n".join(text.rstrip().splitlines()[-lines:])


def survives(work: pathlib.Path, mutation: Mutation) -> bool:
    target = work / mutation.path
    source = target.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    start = mutation.lineno - 1
    ending = "\n" if lines[start].endswith("\n") else ""
    lines[start:start + mutation.span] = [mutation.mutated + ending]
    mutated_source = "".join(lines)
    try:
        compile(mutated_source, str(target), "exec")
    except SyntaxError:
        # Not a mutant at all: it would fail the suite by not importing, which
        # looks exactly like the suite catching it. Reported as invalid, never
        # counted as killed.
        return None
    target.write_text(mutated_source, encoding="utf-8")
    try:
        fast = FAST_TESTS.get(pathlib.Path(mutation.path).name)
        # Cheap pass first: most mutants die here in seconds.
        if fast and not _pytest(work, fast):
            return False
        # Confirm survival against the whole suite — the targeted modules missing
        # it is not the same as the suite missing it.
        if _pytest(work, []):
            return True
        # The suite failed while the targeted modules passed. That CAN mean a
        # distant test caught it — but it is also exactly what a broken
        # environment looks like, and a broken environment marks every mutant
        # "killed" and reports a kill rate near 100%. This happened: one census
        # reported 4 survivors / 99% caught where the true figure was 67 / 79%,
        # and the optimistic number was believed until a survivor was applied by
        # hand. So the failure is attributed only after the PRISTINE copy is shown
        # to be green.
        target.write_text(source, encoding="utf-8")
        pristine = _run_pytest(work, [])
        if pristine.returncode == 0:
            return False            # genuinely killed by a distant test
        raise Unattributable(
            f"the suite fails on the UNMUTATED copy while checking "
            f"{mutation.path}:{mutation.lineno}. Every mutant would be scored "
            f"'killed' from here, which reports blindness as coverage.\n"
            f"{_tail(pristine)}")
    finally:
        target.write_text(source, encoding="utf-8")


def parse_shard(text):
    """"K/N" -> (K, N) with 1 <= K <= N, or None when it is not that."""
    try:
        k, n = (int(part) for part in str(text).split("/"))
    except ValueError:
        return None
    return (k, n) if 1 <= k <= n else None


def select_shard(mutations, shard):
    """The K-th of N interleaved slices. Interleaved rather than contiguous so each
    shard gets a similar mix of cheap and expensive regions of the file; the N
    slices are disjoint and together are exactly the input."""
    k, n = shard
    return [m for i, m in enumerate(mutations) if i % n == k - 1]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--targets", nargs="*", default=list(DEFAULT_TARGETS))
    ap.add_argument("--ci", action="store_true",
                    help="fail on survivors absent from the baseline")
    ap.add_argument("--record", action="store_true",
                    help="rewrite the baseline (never available to --ci)")
    ap.add_argument("--limit", type=int, default=0,
                    help="stop after N mutants per file, for a quick local check")
    ap.add_argument("--shard", default="1/1", metavar="K/N",
                    help="test only every Nth mutant starting at the Kth, so one file can "
                         "run as N parallel CI jobs (render_cv.py alone outgrew a 300-minute job)")
    args = ap.parse_args(argv)

    shard = parse_shard(args.shard)
    if shard is None:
        print(f"cannot run: --shard must be K/N with 1 <= K <= N, got {args.shard!r}",
              file=sys.stderr)
        return 2
    if args.record and shard != (1, 1):
        # A shard sees a third of the survivors; rewriting the baseline from it
        # would silently forget the other two thirds.
        print("cannot run: --record needs the whole target, not a shard", file=sys.stderr)
        return 2

    if args.record and args.ci:
        print("cannot run: --record and --ci together would let the harness "
              "update its own baseline, which reports success by forgetting",
              file=sys.stderr)
        return 2

    for relative in args.targets:
        if not (ROOT / relative).is_file():
            print(f"cannot run: {relative} does not exist", file=sys.stderr)
            return 2

    baseline = {}
    if args.ci and not BASELINE.exists():
        # exit 2, not 1. With no baseline every survivor is "new", so --ci would
        # report the whole pre-existing debt as fresh blindness — a check that
        # could not run, wearing the face of a check that failed. The file is
        # committed; if it is absent, something is wrong with the checkout.
        print(f"cannot run: {BASELINE} is missing, so there is nothing to compare "
              f"against. Run `make mutants-record` and commit the result.",
              file=sys.stderr)
        return 2
    if BASELINE.exists():
        try:
            baseline = json.loads(BASELINE.read_text(encoding="utf-8")).get("known_survivors", {})
        except json.JSONDecodeError as exc:
            print(f"cannot run: {BASELINE} will not parse ({exc})", file=sys.stderr)
            return 2

    work_root = pathlib.Path(tempfile.mkdtemp(prefix="job-hunt-mutants-"))
    work = work_root / "repo"
    try:
        try:
            _copy_repo(work)
        except (OSError, shutil.Error) as exc:
            print(f"cannot run: could not copy the source tree: {exc}", file=sys.stderr)
            return 2
        for relative in args.targets:
            if not (work / relative).resolve().is_relative_to(work.resolve()):
                print(f"cannot run: mutation target escapes the isolated copy: {relative}",
                      file=sys.stderr)
                return 2
        pristine = _run_pytest(work, [])
        if pristine.returncode != 0:
            print("cannot run: the suite is not green before mutating — fix that "
                  "first, or every mutant will look like it survived",
                  file=sys.stderr)
            print(_tail(pristine), file=sys.stderr)
            return 2

        found, new, invalid, total = {}, [], 0, 0
        for relative in args.targets:
            mutations = generate(work / relative, relative)
            if args.limit:
                mutations = mutations[:args.limit]
            mutations = select_shard(mutations, shard)
            total += len(mutations)
            print(f"{relative}: {len(mutations)} mutants", file=sys.stderr)
            for n, mutation in enumerate(mutations, 1):
                print(f"  [{n}/{len(mutations)}] {mutation.operator} "
                      f"line {mutation.lineno}", end="\r", file=sys.stderr)
                try:
                    verdict = survives(work, mutation)
                except Unattributable as exc:
                    print(f"\ncannot run: {exc}", file=sys.stderr)
                    return 2
                if verdict is None:
                    invalid += 1          # would not compile: never counted as killed
                    continue
                if verdict:
                    found[mutation.key] = mutation
                    if mutation.key not in baseline:
                        new.append(mutation)
            print(" " * 70, end="\r", file=sys.stderr)

        tested = total - invalid
        print(f"mutants: {total}   tested: {tested}   invalid (would not compile): "
              f"{invalid}   survived: {len(found)}   new since the baseline: {len(new)}")
        if tested:
            print(f"caught: {tested - len(found)}/{tested} "
                  f"({(tested - len(found)) / tested:.0%})")

        if args.record:
            BASELINE.write_text(json.dumps({
                "_comment": [
                    "Mutants that SURVIVE the suite — the code was broken on purpose and",
                    "nothing went red. This file is the debt, recorded so that --ci can fail",
                    "on NEW blindness without blocking on the existing kind.",
                    "",
                    "A key is sha256(path, operator, original, mutated)[:16] — deliberately",
                    "NOT the line number, so editing elsewhere in the file cannot silently",
                    "empty the baseline.",
                    "",
                    "Shrinking this file is the point. Adding to it needs a reason.",
                ],
                "known_survivors": {
                    key: (baseline.get(key) or f"{m.path}:{m.lineno} [{m.operator}] "
                          f"{m.original.strip()[:80]} — recorded, not explained")
                    for key, m in sorted(found.items(), key=lambda kv: (kv[1].path, kv[1].lineno))
                },
            }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            print(f"recorded {len(found)} survivors to {BASELINE.name}")
            return 0

        if new and args.ci:
            print("\nNEW SURVIVING MUTANTS — the suite got blinder than the "
                  "baseline it was measured at:\n")
            for mutation in new:
                print(f"  {mutation.describe()}\n")
            print("Either pin the behaviour with a test, or — if the mutant is "
                  "genuinely equivalent — add its key to "
                  f"{BASELINE.name} with the reason.")
            return 1
        return 0
    finally:
        shutil.rmtree(work_root, ignore_errors=True)


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
