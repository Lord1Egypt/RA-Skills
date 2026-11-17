#!/usr/bin/env python3
"""Export an explicitly selected local OMR candidate with a bounded handoff.

The wrapper never downloads, installs, or embeds an OMR program or model.  It
only invokes an already-installed local executable and always writes a report,
including when the candidate fails or times out.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from optional_omr_discovery import find_audiveris, find_oemer
from extract_audiveris_anchor_candidates import candidate_note_count, measure_consistency, omr_notehead_count


SUPPORTED = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}

# These messages are emitted by Audiveris after it has recognised a concrete
# musical inconsistency.  An exported MXL can still exist in this situation,
# so export success must not conceal the affected measures from review.
OMR_RISK_PATTERNS = {
    "rhythm_unresolved": "no correct rhythm",
    "missing_time_offset": "no timeOffset",
    "unlinked_symbol": "No chord linked to",
}


def discover(engine: str) -> tuple[str | None, str | None]:
    finder = find_audiveris if engine == "audiveris" else find_oemer
    return finder()


def audiveris_command(executable: str, installation_kind: str | None, output_dir: Path, source: Path) -> tuple[list[str], str]:
    """Build a non-GUI batch command where the official macOS app permits it.

    The macOS ``JavaApplicationStub`` can abort when an agent has no normal
    desktop application registration.  The official bundle contains the same
    signed runtime and JARs, so invoking its documented Java main class keeps
    the process local and avoids a GUI launch.  Other installations retain the
    ordinary CLI command.
    """
    if installation_kind == "macos_app_bundle":
        launcher = Path(executable).resolve()
        contents = launcher.parent.parent
        java = contents / "runtime" / "Contents" / "Home" / "bin" / "java"
        app_dir = contents / "app"
        if java.is_file() and (app_dir / "audiveris.jar").is_file():
            return (
                [str(java), "-Dfile.encoding=UTF-8", "-Djava.awt.headless=true", "-Xms512m", "-Xmx8G",
                 "--add-exports=java.desktop/sun.awt.image=ALL-UNNAMED",
                 "--enable-native-access=ALL-UNNAMED", "-cp", str(app_dir / "*"), "Audiveris",
                 "-batch", "-transcribe", "-export", "-output", str(output_dir), str(source)],
                "macos-bundle-java-batch",
            )
    return [executable, "-batch", "-transcribe", "-export", "-output", str(output_dir), str(source)], "native-cli"


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def geometry_payload(omr_path: Path, musicxml_path: Path) -> dict:
    """Return candidate-only geometry consistency without changing any plan."""
    xml_count = candidate_note_count(musicxml_path)
    head_count = omr_notehead_count(omr_path)
    payload = {
        "candidate_musicxml_note_count": xml_count,
        "candidate_omr_notehead_count": head_count,
        "count_consistent": xml_count == head_count,
    }
    if not payload["count_consistent"]:
        scoped = measure_consistency(omr_path, musicxml_path)
        payload["measure_consistency"] = scoped
        payload["mismatched_measure_scopes"] = [row for row in scoped if not row["consistent"]]
    return payload


def bounded_geometry_payload(omr_path: Path, musicxml_path: Path, timeout: int = 30) -> dict:
    """Run potentially expensive OMR archive parsing in a separately capped child.

    Audiveris can have already written a usable MXL and .omr when the archive
    traversal is unusually slow.  Keeping that traversal in this coordinator
    used to delay the mandatory report indefinitely.  A timeout is diagnostic
    only: it never promotes a candidate and it preserves the exported files.
    """
    command = [sys.executable, str(Path(__file__).resolve()), "--geometry-only", str(omr_path), str(musicxml_path)]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        if completed.returncode != 0:
            return {"status": "unavailable", "reason": completed.stderr[-600:] or "geometry helper failed"}
        data = json.loads(completed.stdout)
        if not isinstance(data, dict):
            raise ValueError("geometry helper returned non-object JSON")
        return data
    except subprocess.TimeoutExpired:
        return {"status": "timed_out", "timeout_seconds": timeout}
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        return {"status": "unavailable", "reason": str(exc)}


def collect_risk_signals(output: str) -> list[dict[str, object]]:
    """Preserve actionable OMR warnings without treating them as score facts."""
    signals: list[dict[str, object]] = []
    for code, needle in OMR_RISK_PATTERNS.items():
        lines = [line.strip() for line in output.splitlines() if needle.lower() in line.lower()]
        if lines:
            signals.append({"code": code, "count": len(lines), "examples": lines[:4]})
    return signals


def acquire_local_omr_lock(timeout: int):
    """Acquire a cross-platform advisory lock for a local OMR process.

    OMR engines are resource-heavy and concurrent books can stall each other.
    OS file locks are released if a host process crashes, unlike a sentinel
    directory, so a failed run cannot permanently block later users.
    """
    lock_path = Path(tempfile.gettempdir()) / "piano-score-fingering-local-omr.lock"
    handle = lock_path.open("a+", encoding="utf-8")
    handle.seek(0)
    handle.write("0")
    handle.flush()
    deadline = time.monotonic() + timeout
    while True:
        try:
            if os.name == "nt":
                import msvcrt
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return handle
        except (BlockingIOError, OSError):
            if time.monotonic() >= deadline:
                handle.close()
                return None
            time.sleep(0.25)


def release_local_omr_lock(handle) -> None:
    if handle is None:
        return
    try:
        if os.name == "nt":
            import msvcrt
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    finally:
        handle.close()


def main() -> int:
    # Private worker mode for bounded_geometry_payload().  Keep this before
    # argparse so the normal user-facing command cannot accidentally bypass
    # the opt-in and output-directory rules.
    if len(sys.argv) == 4 and sys.argv[1] == "--geometry-only":
        try:
            print(json.dumps(geometry_payload(Path(sys.argv[2]), Path(sys.argv[3])), ensure_ascii=False))
            return 0
        except (OSError, ValueError, TypeError, zipfile.BadZipFile, ET.ParseError) as exc:
            print(str(exc), file=sys.stderr)
            return 2
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="local PDF or image score")
    parser.add_argument("--out-dir", type=Path, required=True, help="new local candidate directory")
    parser.add_argument("--allow-local-omr", action="store_true", help="required explicit opt-in")
    parser.add_argument("--engine", choices=("audiveris", "oemer"), default="audiveris",
                        help="separately installed local OMR engine (default: audiveris)")
    parser.add_argument("--timeout", type=int,
                        help="maximum local process time in seconds (Audiveris: 300; Oemer: 90)")
    parser.add_argument("--queue-timeout", type=int, default=30, help="maximum wait for another local OMR task")
    args = parser.parse_args()
    if not args.allow_local_omr:
        parser.error("refusing to run OMR without --allow-local-omr")
    source = args.input.expanduser().resolve()
    if not source.is_file() or source.suffix.lower() not in SUPPORTED:
        parser.error("input must be an existing local PDF or supported image")
    if args.engine == "oemer" and source.suffix.lower() == ".pdf":
        parser.error("Oemer accepts rendered page images, not PDF directly; render the needed page to PNG first")
    timeout = args.timeout if args.timeout is not None else (300 if args.engine == "audiveris" else 90)
    if timeout < 30:
        parser.error("--timeout must be at least 30 seconds")
    if args.queue_timeout < 0:
        parser.error("--queue-timeout must be zero or greater")
    if args.out_dir.exists():
        parser.error("out-dir already exists; use a new directory")
    args.out_dir.mkdir(parents=True)
    report_path = args.out_dir / "omr-candidate-report.json"
    # Persist a receipt before executable discovery or the expensive engine
    # starts.  If the host/session forcibly terminates this wrapper, callers
    # still get an inspectable result instead of an unexplained empty folder.
    write(report_path, {
        "status": "started", "input": str(source), "candidate": args.engine,
        "execution_policy": "single-local-omr-process",
        "candidate_quality": "unavailable", "last_stage": "startup",
        "next_action": "This local candidate run did not reach a final report. Inspect this directory for an engine log or rerun explicitly; do not treat any partial files as verified score facts.",
    })
    executable, installation_kind = discover(args.engine)
    if not executable:
        payload = {
            "status": "unavailable", "input": str(source), "candidate": args.engine,
            "message": f"No locally installed {args.engine} command was found. No software was installed and no data left this machine.",
            "next_action": "Use the visual-facts workflow, or have the user separately install a supported local OMR candidate and explicitly opt in.",
        }
        write(report_path, payload)
        print(json.dumps(payload, ensure_ascii=False))
        return 2

    if args.engine == "audiveris":
        command, launch_mode = audiveris_command(executable, installation_kind, args.out_dir, source)
    else:
        command, launch_mode = [executable, "-o", str(args.out_dir), str(source)], "native-cli"
    lock = acquire_local_omr_lock(args.queue_timeout)
    if lock is None:
        payload = {
            "status": "busy", "input": str(source), "candidate": args.engine, "executable": executable,
            "installation_kind": installation_kind, "launch_mode": launch_mode,
            "execution_policy": "single-local-omr-process", "queue_timeout_seconds": args.queue_timeout,
            "musicxml_candidates": [], "semantic_risk_signals": [], "candidate_quality": "unavailable",
            "message": "Another local OMR task is still running; no second task was started.",
            "next_action": "Return the current report and retry this candidate only after the active local OMR task completes.",
        }
        write(report_path, payload)
        print(json.dumps({key: payload[key] for key in ("status", "candidate_quality", "next_action")}, ensure_ascii=False))
        return 2
    started = time.time()
    try:
        write(report_path, {
            "status": "running", "input": str(source), "candidate": args.engine,
            "executable": executable, "installation_kind": installation_kind,
            "launch_mode": launch_mode, "command": command,
            "execution_policy": "single-local-omr-process", "last_stage": "engine_export",
            "candidate_quality": "unavailable",
            "next_action": "The local engine is running. If this report remains in this state, the host interrupted the run; partial files are not verified score facts.",
        })
        environment = os.environ.copy()
        if args.engine == "oemer":
            # Keep first-run caches inside this new result directory.  This
            # prevents a user-level font/model cache from becoming an
            # implicit dependency or an unexplained write outside the run.
            mpl_cache = args.out_dir / "runtime-cache" / "matplotlib"
            xdg_cache = args.out_dir / "runtime-cache" / "xdg"
            mpl_cache.mkdir(parents=True, exist_ok=True)
            xdg_cache.mkdir(parents=True, exist_ok=True)
            environment["MPLCONFIGDIR"] = str(mpl_cache)
            environment["XDG_CACHE_HOME"] = str(xdg_cache)
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, env=environment)
        status = "candidate_ready" if completed.returncode == 0 else "failed"
        risk_signals = collect_risk_signals(completed.stdout)
        payload = {
            "status": status, "input": str(source), "candidate": args.engine, "executable": executable,
            "installation_kind": installation_kind, "launch_mode": launch_mode,
            "command": command, "return_code": completed.returncode,
            "elapsed_seconds": round(time.time() - started, 3),
            "stdout": completed.stdout[-12000:], "stderr": completed.stderr[-12000:],
            "semantic_risk_signals": risk_signals,
            "candidate_quality": "requires-focused-review" if risk_signals else "no-engine-risk-signals-detected",
        }
    except subprocess.TimeoutExpired as exc:
        payload = {
            "status": "timed_out", "input": str(source), "candidate": args.engine, "executable": executable,
            "installation_kind": installation_kind, "launch_mode": launch_mode,
            "command": command, "timeout_seconds": timeout, "elapsed_seconds": round(time.time() - started, 3),
            "stdout": (exc.stdout or "")[-12000:] if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "")[-12000:] if isinstance(exc.stderr, str) else "",
            "semantic_risk_signals": [],
            "candidate_quality": "unavailable",
        }
    except OSError as exc:
        payload = {
            "status": "failed", "input": str(source), "candidate": args.engine, "executable": executable,
            "installation_kind": installation_kind, "launch_mode": launch_mode,
            "command": command, "elapsed_seconds": round(time.time() - started, 3),
            "stdout": "", "stderr": str(exc), "semantic_risk_signals": [],
            "candidate_quality": "unavailable",
        }
    finally:
        release_local_omr_lock(lock)
    candidates = sorted(str(path) for path in args.out_dir.rglob("*.mxl"))
    candidates.extend(sorted(str(path) for path in args.out_dir.rglob("*.musicxml")))
    omr_projects = sorted(str(path) for path in args.out_dir.rglob("*.omr"))
    payload["execution_policy"] = "single-local-omr-process"
    payload["musicxml_candidates"] = candidates
    payload["omr_project_candidates"] = omr_projects
    if args.engine == "audiveris" and len(candidates) == 1 and len(omr_projects) == 1:
        geometry_consistency = bounded_geometry_payload(Path(omr_projects[0]), Path(candidates[0]))
        payload["geometry_consistency"] = geometry_consistency
        if geometry_consistency.get("status") in {"timed_out", "unavailable"}:
            payload["semantic_risk_signals"].append({
                "code": "geometry_consistency_unavailable",
                "count": 1,
                "examples": ["Audiveris candidate geometry audit did not complete; do not use its coordinates."],
            })
            payload["candidate_quality"] = "requires-focused-review"
        elif not geometry_consistency["count_consistent"]:
            payload["semantic_risk_signals"].append({
                "code": "anchor_count_mismatch",
                "count": len(geometry_consistency["mismatched_measure_scopes"]),
                "examples": [
                    f"page {row['page']} measure {row['measure']} {row['hand']}: "
                    f"OMR {row['omr_noteheads']} head(s) vs MXL {row['musicxml_notes']} note(s)"
                    for row in geometry_consistency["mismatched_measure_scopes"][:12]
                ] or [
                    f"Audiveris project has {geometry_consistency['candidate_omr_notehead_count']} head candidate(s), "
                    f"but its MXL has {geometry_consistency['candidate_musicxml_note_count']} pitched note(s)."
                ],
            })
            payload["candidate_quality"] = "requires-focused-review"
    if payload["status"] == "candidate_ready" and candidates:
        payload["next_action"] = (
            "Run create_semantic_review_ledger.py against the original visual facts; this candidate cannot unlock recognition by itself. "
            "Resolve every semantic_risk_signals item first."
            if payload["semantic_risk_signals"] else
            "Run create_semantic_review_ledger.py against the original visual facts; this candidate cannot unlock recognition by itself."
        )
    else:
        if payload.get("return_code") is not None and int(payload["return_code"]) < 0:
            payload["runtime_failure"] = f"{args.engine} terminated unexpectedly before export; installation discovery does not prove this runtime is usable."
            payload["next_action"] = (
                "Keep the visual-facts workflow. Do not retry automatically; report this local runtime failure and let the user "
                "repair or reinstall the selected OMR tool outside the Skill before explicitly choosing it again."
            )
        else:
            payload["next_action"] = "Keep the current visual-facts workflow; do not treat this OMR output as verified score facts."
    write(report_path, payload)
    print(json.dumps({key: payload[key] for key in ("status", "candidate_quality", "musicxml_candidates", "next_action")}, ensure_ascii=False))
    return 0 if payload["status"] == "candidate_ready" and candidates else 2


if __name__ == "__main__":
    raise SystemExit(main())
