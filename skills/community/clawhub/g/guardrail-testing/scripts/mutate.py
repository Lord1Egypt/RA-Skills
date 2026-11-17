#!/usr/bin/env python3
"""mutate.py - prove that a guardrail's tests actually bite. Stdlib only, Python 3.8+.

What it does, and nothing else:
  * copies --repo into a fresh `mktemp -d` directory (one new copy per run);
  * in that COPY only, removes one `FAIL-CLOSED ... END-FAIL-CLOSED` block (or applies one
    --sub OLD NEW) of --file, then runs your --test command there;
  * deletes every copy on exit (unless --keep), and checks that the original --file is
    byte-identical at the end. It never writes inside --repo.

Exit codes (the same contract it asks your guards to follow):
  0  every mutant was killed, and each kill reproduced on a second fresh copy
  2  at least one mutant survived: some guarded block is not proven by the tests
  3  indeterminate: baseline red, canary survived, no mutant, invalid mutant, timeout,
     kill for another reason (--expect), copy escaped the temp dir, usage error.
     Never read 3 as a pass.

Stale-bytecode defence (CPython revalidates a .pyc on source mtime in whole seconds + size
only): every run gets a new copy, an empty PYTHONPYCACHEPREFIX, PYTHONDONTWRITEBYTECODE=1,
`-p no:cacheprovider` for pytest, and __pycache__ purged. `--selftest` proves it.
"""
import argparse, hashlib, os, re, shlex, shutil, subprocess, sys, tempfile, time

OK, SURVIVED, UNKNOWN = 0, 2, 3
MARK = r"(?:#|//|--|;)[ \t]*"
BLOCK = re.compile(r"^([ \t]*)" + MARK + r"FAIL-CLOSED\b[^\n]*\n.*?^[ \t]*" + MARK
                   + r"END-FAIL-CLOSED\b[^\n]*(?:\n|\Z)", re.M | re.S)
OPEN = re.compile(r"^[ \t]*" + MARK + r"FAIL-CLOSED\b", re.M)
CLOSE = re.compile(r"^[ \t]*" + MARK + r"END-FAIL-CLOSED\b", re.M)
NEUTRAL = {".py": "pass", ".sh": ":", ".bash": ":", ".js": ";", ".mjs": ";", ".cjs": ";", ".ts": ";"}
CANARY = {".py": 'raise SystemExit("MUTATE-CANARY")\n', ".sh": "echo MUTATE-CANARY >&2; exit 97\n",
          ".bash": "echo MUTATE-CANARY >&2; exit 97\n", ".js": 'throw new Error("MUTATE-CANARY");\n',
          ".mjs": 'throw new Error("MUTATE-CANARY");\n', ".cjs": 'throw new Error("MUTATE-CANARY");\n',
          ".ts": 'throw new Error("MUTATE-CANARY");\n'}


class Indeterminate(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):  # argparse exits 2 by default: 2 means "survivor" here
        self.print_usage(sys.stderr)
        print("mutate: usage error: %s" % message, file=sys.stderr)
        sys.exit(UNKNOWN)


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def inside(path, root):
    p, r = os.path.realpath(path), os.path.realpath(root)
    return p.startswith(r + os.sep)


def find_mutants(src, ext, neutral, subs):
    muts = []
    opens, closes = len(OPEN.findall(src)), len(CLOSE.findall(src))
    blocks = list(BLOCK.finditer(src))
    if opens != closes or opens != len(blocks):
        raise Indeterminate("unbalanced FAIL-CLOSED markers (%d open, %d end, %d blocks)"
                            % (opens, closes, len(blocks)))
    stmt = neutral or NEUTRAL.get(ext)
    if blocks and not stmt:
        raise Indeterminate("no neutral statement known for %r: pass --neutral" % ext)
    for m in blocks:
        line = src.count("\n", 0, m.start()) + 1
        head = m.group(0).split("\n", 1)[0].strip()
        muts.append(("block L%d %s" % (line, head[:60]),
                     src[:m.start()] + m.group(1) + stmt + "\n" + src[m.end():]))
    for old, new in subs:
        n = src.count(old)
        if n != 1:
            raise Indeterminate("--sub %r matches %d times, needs exactly 1" % (old, n))
        muts.append(("sub %r -> %r" % (old[:40], new[:40]), src.replace(old, new, 1)))
    if not muts:
        raise Indeterminate("no FAIL-CLOSED block and no --sub: nothing proves anything")
    return muts


def canary_of(src, ext, canary):
    text = canary or CANARY.get(ext)
    if not text:
        raise Indeterminate("no canary known for %r: pass --canary" % ext)
    if not text.endswith("\n"):
        text += "\n"
    if src.startswith("#!"):
        first, _, rest = src.partition("\n")
        return first + "\n" + text + rest
    return text + src


def syntax_ok(path, ext):
    if ext == ".py":
        try:
            with open(path, encoding="utf-8") as fh:
                compile(fh.read(), path, "exec")
            return True
        except SyntaxError:
            return False
    if ext in (".sh", ".bash"):
        return subprocess.run(["bash", "-n", path], capture_output=True).returncode == 0
    if ext in (".js", ".mjs", ".cjs") and shutil.which("node"):
        return subprocess.run(["node", "--check", path], capture_output=True).returncode == 0
    return True


def purge_pycache(root):
    for d, subdirs, _ in os.walk(root):
        for s in list(subdirs):
            if s in ("__pycache__", ".pytest_cache"):
                shutil.rmtree(os.path.join(d, s), ignore_errors=True)
                subdirs.remove(s)


class Runner:
    def __init__(self, a):
        self.a = a
        self.repo = os.path.realpath(a.repo)
        self.base = tempfile.mkdtemp(prefix="mutate-")
        if inside(self.base, self.repo) or os.path.realpath(self.base) == self.repo:
            raise Indeterminate("temp dir resolved inside the repo: %s" % self.base)
        self.n = 0

    def fresh(self, content):
        """New copy of the repo, target file replaced by `content`. Returns copy root."""
        self.n += 1
        root = os.path.join(self.base, "c%03d" % self.n)
        ign = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "*.pyc", *self.a.ignore)
        shutil.copytree(self.repo, root, symlinks=True, ignore=ign)
        target = os.path.join(root, self.a.file)
        if os.path.islink(target) or not inside(target, self.base):
            raise Indeterminate("target in the copy is a symlink or resolves outside the temp dir")
        if self.a.gap:
            time.sleep(self.a.gap)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(content)
        return root, target

    def run(self, root):
        prefix = tempfile.mkdtemp(prefix="pyc-", dir=self.base)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPYCACHEPREFIX=prefix,
                   MUTATE_ROOT=root)
        env["PYTEST_ADDOPTS"] = (env.get("PYTEST_ADDOPTS", "") + " -p no:cacheprovider").strip()
        purge_pycache(root)
        argv = [x.replace("{root}", root) for x in shlex.split(self.a.test)]
        try:
            p = subprocess.run(argv, cwd=root, env=env, capture_output=True, text=True,
                               timeout=self.a.timeout)
        except subprocess.TimeoutExpired:
            return None, "timeout after %ss" % self.a.timeout
        finally:
            shutil.rmtree(prefix, ignore_errors=True)
        return p.returncode, p.stdout + p.stderr

    def verdict(self, content, ext):
        root, target = self.fresh(content)
        if not syntax_ok(target, ext):
            return "INVALID", None
        rc, out = self.run(root)
        if rc is None:
            return "TIMEOUT", None
        if rc == 0:
            return "SURVIVED", rc
        if self.a.expect and not re.search(self.a.expect, out):
            return "KILLED-ELSEWHERE", rc
        return "KILLED", rc


def main(argv=None):
    ap = Parser(description="Mutation check for guardrail tests (works on a temp copy only).")
    ap.add_argument("--repo", help="project root to copy (never modified)")
    ap.add_argument("--file", help="guard file, relative to --repo")
    ap.add_argument("--test", help='test command, run in the copy root; "{root}" = copy root')
    ap.add_argument("--sub", nargs=2, action="append", default=[], metavar=("OLD", "NEW"))
    ap.add_argument("--expect", help="regex the failing output must match for a kill to count")
    ap.add_argument("--neutral", help="statement replacing a block (default by extension)")
    ap.add_argument("--canary", help="line that must break the tests (default by extension)")
    ap.add_argument("--ignore", action="append", default=[], help="glob excluded from the copy")
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--gap", type=float, default=1.0, help="seconds before each write")
    ap.add_argument("--keep", action="store_true", help="keep the temp copies")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.repo and a.file and a.test):
        ap.error("--repo, --file and --test are required")
    orig = os.path.join(a.repo, a.file)
    if os.path.isabs(a.file) or not os.path.isfile(orig) or not inside(orig, a.repo):
        ap.error("--file must be a regular file inside --repo")
    if os.path.realpath(a.repo) in a.test:
        ap.error("--test names the real repo path: the mutants would never be exercised")
    before = sha(orig)
    ext = os.path.splitext(a.file)[1].lower()
    with open(orig, encoding="utf-8") as fh:
        src = fh.read()
    r = None
    try:
        muts = find_mutants(src, ext, a.neutral, a.sub)
        r = Runner(a)
        rc, out = r.run(r.fresh(src)[0])
        if rc != 0:
            raise Indeterminate("baseline is not green (rc=%s): a kill would prove nothing\n%s"
                                % (rc, (out or "")[-800:]))
        print("mutate: baseline PASS")
        state, _ = r.verdict(canary_of(src, ext, a.canary), ext)
        if state not in ("KILLED", "KILLED-ELSEWHERE"):
            raise Indeterminate("canary %s: the tests do not load %s from the copy" % (state, a.file))
        print("mutate: canary KILLED (tests load the copied file)")
        survived, unknown = 0, 0
        for i, (label, text) in enumerate(muts, 1):
            state, code = r.verdict(text, ext)
            note = ""
            if state == "KILLED":
                again, _ = r.verdict(text, ext)  # replay every green on a new copy
                note = " (replay: %s)" % again
                if again != "KILLED":
                    state = "FLAKY"
            print("mutant %d  %-9s rc=%s  %s%s" % (i, state, code, label, note))
            survived += state == "SURVIVED"
            unknown += state not in ("KILLED", "SURVIVED")
        if sha(orig) != before:
            raise Indeterminate("the original %s changed during the run: stop and inspect" % a.file)
        if unknown:
            print("RESULT: %d indeterminate of %d -> exit 3" % (unknown, len(muts)))
            return UNKNOWN
        if survived:
            print("RESULT: %d survived of %d -> exit 2" % (survived, len(muts)))
            return SURVIVED
        print("RESULT: %d/%d killed, each replayed on a fresh copy -> exit 0" % (len(muts), len(muts)))
        return OK
    except Indeterminate as e:
        print("RESULT: indeterminate: %s -> exit 3" % e, file=sys.stderr)
        return UNKNOWN
    finally:
        if r and not a.keep:
            shutil.rmtree(r.base, ignore_errors=True)
        elif r:
            print("mutate: copies kept in %s" % r.base)


# ----------------------------------------------------------------------------- selftest
GUARD = '''def allow(fields):
    # FAIL-CLOSED absent input
    if fields is None or fields == "":
        return False
    # END-FAIL-CLOSED
    # FAIL-CLOSED body is refused
    if "body" in fields.split(","):
        return False
    # END-FAIL-CLOSED
    return True
'''
PARTIAL = 'from guard import allow\nassert allow(None) is False, "REFUSE-ABSENT"\nassert allow("id")\n'
FULL = PARTIAL + 'assert allow("id,body") is False, "REFUSE-BODY"\n'


def selftest():
    me, py = os.path.abspath(__file__), sys.executable
    fails = []

    def check(name, cond, detail=""):
        print("  %s %s %s" % ("ok  " if cond else "FAIL", name, detail))
        if not cond:
            fails.append(name)

    def harness(repo, test, *extra):
        p = subprocess.run([py, me, "--repo", repo, "--file", "guard.py", "--test", test] + list(extra),
                           capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr

    tmp = tempfile.mkdtemp(prefix="mutate-selftest-")
    try:
        repo = os.path.join(tmp, "repo")
        os.mkdir(repo)
        for name, body in (("guard.py", GUARD), ("test_partial.py", PARTIAL), ("test_full.py", FULL)):
            with open(os.path.join(repo, name), "w") as fh:
                fh.write(body)
        guard_hash = sha(os.path.join(repo, "guard.py"))
        muts = find_mutants(GUARD, ".py", None, [])
        check("two blocks found, mutants of equal size", len(muts) == 2 and len(muts[0][1]) == len(muts[1][1]))
        t_part, t_full = "%s test_partial.py" % shlex.quote(py), "%s test_full.py" % shlex.quote(py)

        rc, out = harness(repo, t_part)
        check("partial tests: block 2 survives -> exit 2", rc == 2 and "SURVIVED" in out, "rc=%s" % rc)
        rc, out = harness(repo, t_full, "--gap", "0")
        check("full tests: all killed -> exit 0", rc == 0, "rc=%s" % rc)

        # Naive loop: one working copy, shared bytecode cache, same-second same-size writes.
        naive = os.path.join(tmp, "naive")
        shutil.copytree(repo, naive)
        shared = os.path.join(tmp, "shared-pyc")
        env = dict(os.environ, PYTHONPYCACHEPREFIX=shared)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        stamp, kills = int(time.time()), []
        for _, text in muts:
            target = os.path.join(naive, "guard.py")
            with open(target, "w") as fh:
                fh.write(text)
            os.utime(target, (stamp, stamp))
            kills.append(subprocess.run([py, "test_partial.py"], cwd=naive, env=env,
                                        capture_output=True).returncode != 0)
        if all(kills):
            check("naive loop reproduces the stale .pyc false green (2/2 'killed')", True)
        else:
            print("  note naive loop did not go stale on this interpreter: kills=%s" % kills)
        rc, out = harness(repo, t_part, "--gap", "0")
        check("same scenario, --gap 0: harness still reports the survivor", rc == 2, "rc=%s" % rc)

        broken = os.path.join(tmp, "broken")
        shutil.copytree(repo, broken)
        with open(os.path.join(broken, "test_full.py"), "a") as fh:
            fh.write("assert False, 'baseline red'\n")
        rc, _ = harness(broken, t_full, "--gap", "0")
        check("red baseline -> exit 3", rc == 3, "rc=%s" % rc)
        rc, _ = harness(repo, "%s -c pass" % shlex.quote(py), "--gap", "0")
        check("tests that never load the file (canary survives) -> exit 3", rc == 3, "rc=%s" % rc)
        rc, _ = harness(repo, t_full, "--gap", "0", "--expect", "NO-SUCH-ASSERTION-ID")
        check("kill for another reason (--expect unmatched) -> exit 3", rc == 3, "rc=%s" % rc)
        rc, _ = harness(repo, t_full, "--gap", "0", "--expect", "REFUSE-(ABSENT|BODY)")
        check("kill by the named assertions -> exit 0", rc == 0, "rc=%s" % rc)
        plain = os.path.join(tmp, "plain")
        shutil.copytree(repo, plain)
        with open(os.path.join(plain, "guard.py"), "w") as fh:
            fh.write("def allow(fields):\n    return True\n")
        rc, _ = harness(plain, t_part, "--gap", "0")
        check("no FAIL-CLOSED block -> exit 3", rc == 3, "rc=%s" % rc)
        p = subprocess.run([py, me, "--no-such-flag"], capture_output=True)
        check("usage error -> exit 3, not 2", p.returncode == 3, "rc=%s" % p.returncode)
        check("original guard.py byte-identical", sha(os.path.join(repo, "guard.py")) == guard_hash)
        check("no __pycache__ left in the repo", not os.path.exists(os.path.join(repo, "__pycache__")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST: %s" % ("PASS" if not fails else "FAIL (%d): %s" % (len(fails), ", ".join(fails))))
    return OK if not fails else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(UNKNOWN)
    except Exception as exc:  # a crash is never a verdict
        print("mutate: crashed: %r -> exit 3" % (exc,), file=sys.stderr)
        sys.exit(UNKNOWN)
