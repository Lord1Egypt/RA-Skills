"""Repeatable synthetic CLI smoke tests. Keeps results and never deletes directories."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

BUNDLE = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(BUNDLE / "tools"))
from workspace import Workspace, configure_console, inside, write_json_new, write_text_new


def main():
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(BUNDLE), help="工具包/工作区根目录")
    parser.add_argument("--ffmpeg", help="程序名或 FFmpeg 路径；否则使用配置/PATH")
    parser.add_argument("--ffprobe", help="程序名或 ffprobe 路径；否则使用配置/PATH")
    args = parser.parse_args()
    workspace = Workspace(args.root)
    def executable(name):
        value = getattr(args, name)
        if value:
            candidate = shutil.which(value)
            if not candidate and Path(value).is_file():
                candidate = str(Path(value).absolute())
        else:
            candidate = workspace.tool(name)
        if not candidate:
            raise ValueError(f"缺少 {name}，请传 --{name} 或配置 PATH")
        return candidate
    ffmpeg, ffprobe = executable("ffmpeg"), executable("ffprobe")
    from PIL import Image
    suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8]
    case = workspace.output(workspace.path("cache") / ("workspace_tests_" + suffix))
    case.mkdir(parents=True, exist_ok=False)
    config = dict(workspace.config)
    config["executables"] = {"ffmpeg": ffmpeg, "ffprobe": ffprobe, "exiftool": None}
    # Generated test configuration is local evidence, not a file to share.
    write_json_new(case / "workspace_config.json", config)
    for path_key, filename in (("templates", "交付检查清单.md"), ("resources", "style.default.json")):
        source = inside(workspace.path(path_key), filename)
        destination = case / workspace.paths[path_key] / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as target, source.open("rb") as stream:
            shutil.copyfileobj(stream, target)
    theme_name = "synthetic"
    theme = case / workspace.paths["sources"] / theme_name
    theme.mkdir(parents=True, exist_ok=False)
    exif = Image.Exif()
    exif[36867] = "2026:01:02 03:04:05"
    exif[274] = 6
    Image.new("RGB", (120, 80), "#76b4c9").save(theme / "IMG_20260102_030405.jpg", exif=exif)
    Image.new("RGB", (80, 120), "#f4cf68").save(theme / "photo.png")
    write_text_new(theme / "clip.txt", "Synthetic companion; not real footage.\n")
    creation = subprocess.run([ffmpeg, "-hide_banner", "-v", "error", "-nostdin", "-f", "lavfi", "-i", "testsrc2=size=120x80:rate=10", "-t", "2", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-n", str(theme / "clip.mp4")], capture_output=True, encoding="utf-8", errors="replace", timeout=60)
    if creation.returncode:
        raise RuntimeError("合成视频创建失败：" + creation.stderr[-2000:])
    write_text_new(case / "brief.txt", "Synthetic test only; no private material.\n")
    before_hash = hashlib.sha256((theme / "clip.mp4").read_bytes()).hexdigest()
    checks = []
    logs = case / "test_logs"
    logs.mkdir()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    def run_case(label, script, arguments, expected=0):
        result = subprocess.run([sys.executable, str(BUNDLE / "tools" / script), "--root", str(case), *arguments], capture_output=True, encoding="utf-8", errors="replace", timeout=180, env=env, cwd=case)
        filename = f"{len(checks)+1:02d}.log"
        write_text_new(logs / filename, result.stdout + "\nSTDERR:\n" + result.stderr)
        checks.append({"name": label, "expected_exit": expected, "actual_exit": result.returncode, "passed": result.returncode == expected, "log": "test_logs/" + filename})
    catalog = Path(workspace.paths["catalog"])
    cache = Path(workspace.paths["cache"])
    manifest = (catalog / "manifest_v001.json").as_posix()
    contact_dir = (cache / "contacts_v001").as_posix()
    run_case("doctor_synthetic_libx264", "workspace.py", ["doctor"])
    run_case("topics", "workspace.py", ["topics"])
    project_args = ["new", "synthetic_project", "--themes", theme_name, "--brief", "brief.txt"]
    run_case("new_project", "workspace.py", project_args)
    run_case("reject_existing_project", "workspace.py", project_args, 1)
    run_case("reject_missing_theme", "workspace.py", ["new", "missing_theme_project", "--themes", "missing_theme", "--brief", "brief.txt"], 1)
    inventory_args = ["inventory", "--themes", theme_name, "--out", manifest]
    run_case("inventory", "media.py", inventory_args)
    run_case("reject_existing_manifest", "media.py", inventory_args, 1)
    run_case("reject_output_in_sources", "media.py", ["inventory", "--themes", theme_name, "--out", (Path(workspace.paths["sources"]) / "forbidden.json").as_posix()], 1)
    run_case("reject_path_traversal", "media.py", ["inventory", "--themes", theme_name, "--out", "../forbidden.json"], 1)
    contact_args = ["contacts", "--manifest", manifest, "--out", contact_dir, "--samples", "5"]
    run_case("contacts_actual_decode", "media.py", contact_args)
    run_case("reject_existing_contacts", "media.py", contact_args, 1)
    run_case("reject_missing_local_ASR_model", "transcribe.py", ["--input", (Path(workspace.paths["sources"]) / theme_name / "clip.mp4").as_posix(), "--model", "models/does_not_exist", "--out", (cache / "asr_missing_model").as_posix()], 1)
    try:
        manifest_data = json.loads((case / manifest).read_text(encoding="utf-8"))
        contacts_data = json.loads((case / contact_dir / "contacts.json").read_text(encoding="utf-8"))
        video_frames = [frame for asset in contacts_data["assets"] if asset["kind"] == "videos" for frame in asset["frames"]]
        checks.append({"name": "review_flags_false_and_actual_pts_present", "passed": all(not any(asset["review"].values()) for asset in manifest_data["assets"] + contacts_data["assets"]) and len(video_frames) == 5 and all(frame.get("decoded_pts_seconds") is not None for frame in video_frames)})
        checks.append({"name": "capture_candidates_unselected", "passed": any(len(asset["capture_time"]["candidates"]) >= 2 and asset["capture_time"]["selected_capture_time"] is None for asset in manifest_data["assets"])})
    except (OSError, KeyError, ValueError) as exc:
        checks.extend([{"name": "review_flags_false_and_actual_pts_present", "passed": False, "error": str(exc)}, {"name": "capture_candidates_unselected", "passed": False, "error": "dependent output missing"}])
    checks.append({"name": "original_unchanged", "passed": hashlib.sha256((theme / "clip.mp4").read_bytes()).hexdigest() == before_hash})
    report = {"schema_version": 1, "scope": "synthetic_media_only", "checks": checks, "passed": sum(check["passed"] for check in checks), "total": len(checks), "ASR_inference_tested": False, "listening_performed": False, "continuous_playback_performed": False, "cleanup": "not_performed_test_directory_retained"}
    write_json_new(case / "test_report.json", report)
    print(json.dumps({"report": workspace.relative(case / "test_report.json"), "passed": report["passed"], "total": report["total"], "test_directory_retained": True}, ensure_ascii=False, indent=2))
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, ImportError, subprocess.SubprocessError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        raise SystemExit(1)
