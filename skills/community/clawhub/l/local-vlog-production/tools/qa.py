"""Inspect exported video locally. Technical checks do not constitute viewing or listening."""
import argparse
from collections import deque
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time

FIELDS = ("index", "codec_type", "codec_name", "width", "height", "avg_frame_rate",
          "sample_rate", "channels", "color_space", "color_transfer", "color_primaries", "color_range")
DISPOSITIONS = ("default", "attached_pic", "timed_thumbnails", "still_image")
BLACK = re.compile(r"black_start:(\S+)\s+black_end:(\S+)\s+black_duration:(\S+)")
VOLUME = re.compile(r"\b(mean_volume|max_volume):\s*([-\w.]+) dB")
DECODE_ERROR = re.compile(r"error (?:while|during) decoding|decoding error|corrupt decoded frame|invalid data found when processing input", re.I)


def probe_streams(executable, source, timeout):
    fields = "format=duration:stream=" + ",".join(FIELDS) + ":stream_disposition=" + ",".join(DISPOSITIONS)
    with tempfile.TemporaryFile() as errors:
        probe = subprocess.run([executable, "-v", "error", "-show_entries", fields, "-of", "json", source],
                               stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=errors, timeout=timeout)
        if probe.returncode:
            errors.seek(max(0, errors.tell() - 4000))
            raise ValueError(errors.read().decode("utf-8", "replace") or "Could not read stream metadata")
    return json.loads(probe.stdout)


def selected_streams(streams, kind, requested):
    choices = [s for s in streams if s["codec_type"] == kind]
    if kind == "video":
        choices = [s for s in choices if not any(s.get("disposition", {}).get(k) for k in ("attached_pic", "timed_thumbnails"))]
    if requested is not None:
        indexed = {s["index"]: s for s in choices}
        missing = [n for n in requested if n not in indexed]
        if missing:
            raise ValueError(f"No selectable {kind} stream at file index {missing[0]}")
        return [indexed[n] for n in dict.fromkeys(requested)], len(choices)
    def preference(s):
        flags = s.get("disposition", {})
        quality = int(s.get("channels", 0)) if kind == "audio" else int(s.get("width", 0)) * int(s.get("height", 0))
        return (-int(flags.get("default", 0)), int(flags.get("still_image", 0)), -quality, s["index"])
    return sorted(choices, key=preference), len(choices)


def scan(ffmpeg, source, tracks, operation, idle_timeout):
    """At most one video and one audio per process. FFmpeg progress and diagnostics share one drained pipe."""
    types = {t["codec_type"] for t in tracks}
    filters = operation != "decode"
    command = [ffmpeg, "-hide_banner", "-nostdin", "-nostats", "-stats_period", str(min(0.5, idle_timeout / 4)),
               "-progress", "pipe:1", "-xerror", "-i", source]
    for track in tracks:
        command.extend(["-map", f"0:{track['index']}"])
    if filters and "video" in types:
        command.extend(["-vf", "blackdetect=d=0.12:pix_th=0.10"])
    if filters and "audio" in types:
        command.extend(["-af", "volumedetect"])
    command.extend(["-f", "null", "-"])
    black = []
    levels = {}
    tail = deque(maxlen=12)
    high = {"frame": 0, "out_time_us": 0}
    last_progress = time.monotonic()
    end_seen = False
    decoding_error = False
    reader_error = []
    finished = threading.Event()

    def drain(pipe):
        nonlocal last_progress, end_seen, decoding_error
        try:
            with pipe:
                for line in iter(lambda: pipe.readline(8192), ""):
                    line = line.strip()
                    key, _, value = line.partition("=")
                    if key in high:
                        if value.lstrip("-").isdigit() and int(value) > high[key]:
                            high[key] = int(value)
                            last_progress = time.monotonic()
                    elif key == "progress":
                        end_seen = value == "end"
                    elif not re.match(r"^[\w:]+=", line):
                        tail.append(line[-400:])
                        decoding_error |= bool(DECODE_ERROR.search(line))
                        m = BLACK.search(line)
                        if m:
                            a, b, length = map(float, m.groups())
                            black.append({"start": a, "end": b, "duration": length})
                        m = VOLUME.search(line)
                        if m:
                            levels[m[1]] = m[2]
        except (OSError, ValueError) as exc:
            reader_error.append(str(exc))
        finally:
            finished.set()

    stopped = False
    with subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, encoding="utf-8", errors="replace") as proc:
        worker = threading.Thread(target=drain, args=(proc.stdout,), daemon=True)
        worker.start()
        try:
            while not finished.wait(min(0.25, idle_timeout)):
                if time.monotonic() - last_progress >= idle_timeout:
                    stopped = True
                    break
            if not stopped:
                try:
                    proc.wait(timeout=idle_timeout)
                except subprocess.TimeoutExpired:
                    stopped = True
        finally:
            if proc.poll() is None:
                proc.kill()
            proc.wait()
            worker.join()
    status, detail = "passed", ""
    if stopped:
        status, detail = "incomplete", "No advancing FFmpeg progress before the configured idle timeout."
    elif reader_error:
        status, detail = "incomplete", reader_error[0]
    elif proc.returncode or not end_seen:
        status = "failed" if decoding_error else "incomplete"
        detail = (f"FFmpeg exited with code {proc.returncode}. " + "\n".join(tail))[-4000:]
    elif "video" in types and high["frame"] == 0:
        status, detail = "incomplete", "No decoded video frame was confirmed."
    elif filters and "audio" in types and not {"mean_volume", "max_volume"} <= levels.keys():
        status, detail = "incomplete", "The audio scan ended without complete volume statistics."
    return {"status": status, "detail": detail, "black": black, "levels": levels}


def aggregate(states):
    if "failed" in states:
        return "failed"
    if states and all(state == "passed" for state in states):
        return "passed"
    return "incomplete"


def inspect(ffmpeg, source, report, multitrack, separate, idle_timeout, target):
    tracks = report["track_checks"]
    def check(group, operation):
        attempt = {"operation": operation, "stream_indices": [t["index"] for t in group], "status": "incomplete"}
        report["attempts"].append(attempt)
        for track in group:
            if operation != "signal":
                track["decode_status"] = "incomplete"
            if operation != "decode":
                track["signal_status"] = "incomplete"
        result = scan(ffmpeg, source, group, operation, idle_timeout)
        attempt["status"] = result["status"]
        if result["detail"]:
            attempt["detail"] = result["detail"]
        for track in group:
            if operation != "signal":
                track["decode_status"] = result["status"]
            if operation != "decode":
                track["signal_status"] = result["status"]
                if result["status"] == "passed":
                    if track["codec_type"] == "video":
                        track["black_intervals_for_review"] = result["black"]
                    else:
                        track["sample_peak_dbfs"] = result["levels"]["max_volume"]
                        track["mean_volume_dbfs"] = result["levels"]["mean_volume"]
        return result["status"]

    groups = [[t] for t in tracks] if multitrack or separate else [tracks]
    for group in groups:
        if not separate and check(group, "decode_and_signal") == "passed":
            if multitrack:
                save_report(report, target)
            continue
        # An inconclusive first pass leaves no publishable partial readings. Retry only affected tracks once.
        for track in group:
            check([track], "decode")
            check([track], "signal")
            save_report(report, target)


def finish_report(report, stopped):
    tracks = report["track_checks"]
    decode = aggregate([t["decode_status"] for t in tracks])
    signals = aggregate([t["signal_status"] for t in tracks])
    report.update(decode_status=decode, signal_status=signals, decode_passed=decode == "passed",
                  signal_scan_passed=signals == "passed")
    report["status"] = "incomplete" if stopped else aggregate([decode, signals])
    if not stopped and report["expected_duration_seconds"] is not None:
        if report["duration_passed"] is False:
            report["status"] = "failed"
        elif report["duration_passed"] is None and report["status"] == "passed":
            report["status"] = "incomplete"
    for track in tracks:
        if track["index"] == report["primary_video_index"]:
            report["black_intervals_for_review"] = track.get("black_intervals_for_review", [])
        if track["index"] == report["primary_audio_index"]:
            report["mean_volume_dbfs"] = track.get("mean_volume_dbfs")
            report["sample_peak_dbfs"] = track.get("sample_peak_dbfs")
    if decode != "passed":
        errors = [a["detail"] for a in report["attempts"] if a.get("detail") and a["operation"] != "signal"]
        report["decode_error"] = (report.get("error") or "\n".join(errors))[-4000:]


def save_report(report, target):
    # Replace only the report this invocation already reserved with exclusive creation.
    handle = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent,
                                         prefix=".qa-", suffix=".tmp", delete=False)
    temp = Path(handle.name)
    try:
        with handle as out:
            json.dump(report, out, ensure_ascii=False, indent=2)
            out.write("\n")
        os.replace(temp, target)
    finally:
        temp.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--expected-duration", type=float)
    parser.add_argument("--video-stream", type=int, action="append", metavar="INDEX", help="Absolute file stream index; repeat to select several, primary first.")
    parser.add_argument("--audio-stream", type=int, action="append", metavar="INDEX", help="Absolute file stream index; repeat to select several, primary first.")
    parser.add_argument("--separate", action="store_true", help="Run independent decode and signal checks for each selected stream.")
    parser.add_argument("--idle-timeout", type=float, default=120, metavar="SECONDS", help="Maximum time without advancing media progress (default 120).")
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    args = parser.parse_args(argv)
    if not math.isfinite(args.idle_timeout) or args.idle_timeout <= 0:
        parser.error("--idle-timeout must be finite and positive.")
    if args.expected_duration is not None and (not math.isfinite(args.expected_duration) or args.expected_duration < 0):
        parser.error("--expected-duration must be finite and nonnegative.")
    root = args.root.resolve()
    source = (root / args.input).resolve()
    target = (root / args.out).resolve()
    config = json.loads((root / "workspace_config.json").read_text(encoding="utf-8-sig"))
    srcdir = (root / config.get("paths", {}).get("sources", "素材")).resolve()
    if not source.is_relative_to(root) or not source.is_file():
        parser.error("Input must exist inside the workspace.")
    if not target.is_relative_to(root) or target.is_relative_to(srcdir) or target.exists():
        parser.error("Report must be a new file inside the workspace, outside sources.")
    exe = config.get("executables", {})
    local = root / "environment.local.json"
    if local.exists():
        exe.update(json.loads(local.read_text(encoding="utf-8-sig")).get("executables", {}))
    def executable(name, override):
        p = Path(override or exe.get(name) or name)
        return str(root / p) if not p.is_absolute() and len(p.parts) > 1 else str(p)

    report = {"schema_version": 1, "file": source.relative_to(root).as_posix(), "status": "incomplete",
              "mode": None, "duration_seconds": None, "streams": [], "expected_duration_seconds": args.expected_duration,
              "duration_passed": None, "decode_passed": False, "decode_status": "incomplete", "decode_error": "",
              "signal_scan_passed": False, "signal_status": "incomplete", "black_intervals_for_review": [],
              "sample_peak_dbfs": None, "mean_volume_dbfs": None, "track_checks": [], "attempts": [],
              "primary_video_index": None, "primary_audio_index": None,
              "warnings": ["Review detected black intervals in context. Peak and mean levels are sample measurements."],
              "visual_frames_reviewed": False, "continuous_playback": False, "actual_listening": False, "user_accepted": False}
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as out:
        json.dump(report, out, ensure_ascii=False)
    cancelled = stopped = False
    try:
        metadata = probe_streams(executable("ffprobe", args.ffprobe), source, args.idle_timeout)
        streams = metadata.get("streams", [])
        report["streams"] = [{**{k: s.get(k) for k in FIELDS}, "disposition": s.get("disposition", {})} for s in streams]
        raw_duration = metadata.get("format", {}).get("duration")
        if raw_duration not in (None, "N/A"):
            duration = float(raw_duration)
            if math.isfinite(duration):
                report["duration_seconds"] = duration
                if args.expected_duration is not None:
                    report["duration_passed"] = abs(duration - args.expected_duration) <= 0.1
        videos, nvideo = selected_streams(streams, "video", args.video_stream)
        audios, naudio = selected_streams(streams, "audio", args.audio_stream)
        if not videos:
            raise ValueError("No playable video stream was found.")
        report["primary_video_index"] = videos[0]["index"]
        report["primary_audio_index"] = audios[0]["index"] if audios else None
        multitrack = nvideo > 1 or naudio > 1
        report["mode"] = "separate" if args.separate else ("per_stream" if multitrack else "single_pass")
        for s in videos + audios:
            report["track_checks"].append({"index": s["index"], "codec_type": s["codec_type"],
                                           "decode_status": "incomplete", "signal_status": "incomplete"})
        save_report(report, target)
        inspect(executable("ffmpeg", args.ffmpeg), source, report, multitrack, args.separate, args.idle_timeout, target)
    except KeyboardInterrupt:
        cancelled = stopped = True
        report["error"] = "Cancelled. Repeat the incomplete checks with --separate and a new --out path."
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        stopped = True
        report["error"] = str(exc)
    finish_report(report, stopped)
    save_report(report, target)
    if report.get("error"):
        print(report["error"], file=sys.stderr)
    print(json.dumps({"report": target.relative_to(root).as_posix(), "status": report["status"],
                      "decode_passed": report["decode_passed"], "duration_passed": report["duration_passed"]}, ensure_ascii=False))
    if cancelled:
        return 130
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    def cancel(signum, frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, cancel)
    if hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, cancel)
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
