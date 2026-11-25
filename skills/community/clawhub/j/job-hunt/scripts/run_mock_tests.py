#!/usr/bin/env python3
"""Run a candidate's mock-coding solution against the hidden cases.

Usage:
    python3 scripts/run_mock_tests.py --dir <workspace>/mock/code/round-<n>/<Qn> \
        --cmd "python3 solution.py" [--build "g++ -O2 -o sol sol.cpp"] [--timeout 5]

The directory holds `cases.json` — written by the interviewer BEFORE the candidate's
code is seen, so the cases test the problem and not the solution — and the files the
candidate wrote. Each case is fed to `--cmd` on stdin, in that directory, and its
stdout compared with `expected` (trailing whitespace on each line and trailing blank
lines ignored; anything else is a difference). Any language works: a function-style
problem gets a small driver that reads stdin, calls the function and prints the
answer in one canonical form.

cases.json:  [{"name": "empty input", "stdin": "0\\n\\n", "expected": "0"}, ...]

Writes `result.json` beside them: every case's outcome, the totals, the derived
status, and the SHA-256 of cases.json and of each file in the directory as it was
when the cases ran (after any build). check_mock.py compares a round's SOLVE record with this file and
recomputes those hashes, so "all tests pass" can only be said about the code that
actually ran.

exit 0 — the cases ran (whatever they returned; a failing solution is a result).
exit 2 — could not run: no directory, no or unreadable cases.json, no candidate file.
A build that fails is a result, not exit 2: every case is recorded as failed with
the compiler's output, because a solution that does not compile in the room fails.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import signal
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal

CASES = "cases.json"
RESULT = "result.json"
# Enough of a wrong answer to see what went wrong, not a megabyte of it.
KEEP = 2000


class CannotRun(RuntimeError):
    """An input is missing or malformed — nothing was executed."""


def normalize_output(text: str) -> str:
    lines = [line.rstrip() for line in (text or "").replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def load_cases(qdir: pathlib.Path) -> list:
    path = qdir / CASES
    if not path.is_file():
        raise CannotRun(f"{path} is missing — write the hidden cases before running")
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CannotRun(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(cases, list) or not cases:
        raise CannotRun(f"{path} must be a non-empty JSON list of cases")
    for i, case in enumerate(cases):
        if not isinstance(case, dict) or not all(
                isinstance(case.get(k), str) for k in ("name", "stdin", "expected")):
            raise CannotRun(
                f"{path} case {i}: every case needs string fields name, stdin, expected")
    return cases


def candidate_files(qdir: pathlib.Path) -> list:
    """The files the candidate (or the driver) wrote: everything except the cases,
    the result, hidden files and caches."""
    return sorted(
        p for p in qdir.rglob("*")
        if p.is_file() and p.name not in (CASES, RESULT)
        and not any(part.startswith(".") or part == "__pycache__"
                    for part in p.relative_to(qdir).parts))


def file_hashes(qdir: pathlib.Path, files) -> dict:
    return {p.relative_to(qdir).as_posix(): journal.sha256_file(p) for p in files}


def status_of(passed: int, total: int) -> str:
    if passed == total:
        return "all_passed"
    return "none_passed" if passed == 0 else "some_failed"


def _kill_tree(proc: subprocess.Popen) -> None:
    """Kill the command and everything it started. Killing only the shell left a
    timed-out solution running: `cd x && python3 sol.py` with an infinite loop kept
    one process per timed-out case at full CPU after the runner had returned."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    else:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


def _run(cmd: str, qdir: pathlib.Path, stdin: str, timeout: float) -> dict:
    started = datetime.datetime.now()
    # Its own process group, so a timeout reaches the solution and not just the shell.
    # UTF-8 both ways: a locale codec (cp936 on a Chinese Windows) misreads the output.
    group = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt"
             else {"start_new_session": True})
    proc = subprocess.Popen(cmd, shell=True, cwd=qdir, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            encoding="utf-8", errors="replace", **group)
    try:
        out, err = proc.communicate(stdin, timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        try:
            out, _ = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            out = ""
        return {"timed_out": True, "returncode": None, "stdout": (out or "")[:KEEP],
                "stderr": "", "seconds": round(timeout, 3)}
    finally:
        if proc.poll() is None:
            _kill_tree(proc)
    if os.name != "nt":
        _kill_tree(proc)  # anything the solution left running in the background
    return {"timed_out": False, "returncode": proc.returncode,
            "stdout": out[:KEEP], "stderr": err[:KEEP],
            "seconds": round((datetime.datetime.now() - started).total_seconds(), 3)}


def run(qdir, cmd: str, build: str | None = None, timeout: float = 5.0) -> dict:
    qdir = pathlib.Path(qdir)
    if not qdir.is_dir():
        raise CannotRun(f"{qdir} is not a directory")
    cases = load_cases(qdir)
    if not candidate_files(qdir):
        raise CannotRun(f"{qdir} holds no candidate file — save the solution first")
    result = {
        "cmd": cmd,
        "build": build,
        "ran_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "cases_sha256": journal.sha256_file(qdir / CASES),
        "build_ok": True,
        "build_output": "",
    }
    if build:
        built = _run(build, qdir, "", max(timeout, 60.0))
        if built["timed_out"] or built["returncode"] != 0:
            result["build_ok"] = False
            result["build_output"] = (built["stdout"] + built["stderr"])[:KEEP]
    # Hashed AFTER the build. A build never edits the sources, and the binary it
    # writes is the one the cases run against. Hashing before it recorded the
    # previous submission's binary, so every resubmitted C++/Java/Go solution read
    # as STALE_TEST_RESULT at the gate (measured: a changed sol.cpp rebuilt).
    result["solution_sha256"] = file_hashes(qdir, candidate_files(qdir))
    outcomes = []
    for case in cases:
        if not result["build_ok"]:
            outcomes.append({"name": case["name"], "passed": False, "timed_out": False,
                             "expected": case["expected"][:KEEP], "stdout": "",
                             "stderr": "build failed", "seconds": 0})
            continue
        got = _run(cmd, qdir, case["stdin"], timeout)
        passed = (not got["timed_out"] and got["returncode"] == 0
                  and normalize_output(got["stdout"]) == normalize_output(case["expected"]))
        outcomes.append({"name": case["name"], "passed": passed,
                         "timed_out": got["timed_out"], "returncode": got["returncode"],
                         "expected": case["expected"][:KEEP], "stdout": got["stdout"],
                         "stderr": got["stderr"], "seconds": got["seconds"]})
    passed = sum(1 for o in outcomes if o["passed"])
    result.update(cases=outcomes, passed=passed, total=len(outcomes),
                  status=status_of(passed, len(outcomes)))
    (qdir / RESULT).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run a mock-coding solution's hidden cases.")
    parser.add_argument("--dir", required=True, type=pathlib.Path)
    parser.add_argument("--cmd", required=True, help="run command, fed each case on stdin")
    parser.add_argument("--build", default=None, help="optional one-off build command")
    parser.add_argument("--timeout", type=float, default=5.0, help="seconds per case")
    args = parser.parse_args(argv)
    try:
        result = run(args.dir, args.cmd, build=args.build, timeout=args.timeout)
    except CannotRun as exc:
        print(f"cannot run: {exc}", file=sys.stderr)
        return 2
    if not result["build_ok"]:
        print("BUILD FAILED:\n" + result["build_output"])
    for case in result["cases"]:
        mark = "pass" if case["passed"] else ("TIMEOUT" if case["timed_out"] else "FAIL")
        print(f"{mark}  {case['name']}  ({case['seconds']}s)")
    print(f"{result['passed']} of {result['total']} cases passed — status "
          f"{result['status']}; written to {pathlib.Path(args.dir) / RESULT}")
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
