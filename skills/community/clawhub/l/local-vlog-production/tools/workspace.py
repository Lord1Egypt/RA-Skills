"""Portable workspace management. Originals are read-only; outputs never overwrite."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys

DEFAULT_ROOT = Path(__file__).absolute().parent.parent
DEFAULT_PATHS = {
    "sources": "素材", "projects": "作品", "catalog": "工作数据/索引",
    "prepared": "工作数据/预处理", "cache": "工作数据/缓存",
    "logs": "工作数据/日志", "resources": "公共资源", "templates": "模板",
}


def now():
    return datetime.now(timezone.utc).isoformat()


def configure_console():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_text_new(path, text):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def write_json_new(path, value):
    write_text_new(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def is_link(path):
    info = Path(path).lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def reject_link_chain(path):
    """Check lexical ancestors before resolving, including Windows junctions."""
    path = Path(os.path.abspath(path))
    for part in reversed((path, *path.parents)):
        if os.path.lexists(part) and is_link(part):
            raise ValueError(f"拒绝符号链接或重解析点：{part}")
    return path


def inside(root, value, *, allow_root=False):
    root = reject_link_chain(root)
    value = Path(value)
    if ".." in value.parts:
        raise ValueError("路径不允许包含 ..")
    candidate = reject_link_chain(value if value.is_absolute() else root / value)
    if not candidate.is_relative_to(root) or (candidate == root and not allow_root):
        raise ValueError("路径必须位于指定工作区内部")
    return candidate


def check_name(name):
    if (not name or name != name.strip() or name.endswith(".") or
            any(c in name for c in '<>:"/\\|?*') or any(ord(c) < 32 for c in name) or
            name in (".", "..")):
        raise ValueError(f"无效文件夹名：{name!r}")
    reserved = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
    reserved |= {f"{prefix}{i}" for prefix in ("COM", "LPT") for i in range(1, 10)}
    if name.split(".")[0].upper() in reserved:
        raise ValueError("不能使用 Windows 保留文件夹名")
    return name


class Workspace:
    def __init__(self, root):
        self.root = reject_link_chain(root)
        if not self.root.is_dir():
            raise ValueError("工作区根目录不存在")
        self.config = read_json(inside(self.root, "workspace_config.json"))
        self.paths = {**DEFAULT_PATHS, **self.config.get("paths", {})}
        for key, value in self.paths.items():
            if Path(value).is_absolute() or Path(value).drive:
                raise ValueError(f"配置 paths.{key} 必须是相对路径")
            inside(self.root, value)
        self.sources = self.path("sources")
        self.executables = dict(self.config.get("executables", {}))
        local = inside(self.root, "environment.local.json")
        if local.is_file():
            self.executables.update(read_json(local).get("executables", {}))

    def path(self, key):
        return inside(self.root, self.paths[key])

    def relative(self, path):
        return inside(self.root, path).relative_to(self.root).as_posix()

    def output(self, value, *, must_be_new=True):
        path = inside(self.root, value)
        if path == self.sources or path.is_relative_to(self.sources):
            raise ValueError("拒绝向素材目录写入派生文件")
        if must_be_new and os.path.lexists(path):
            raise ValueError(f"输出已存在，拒绝覆盖：{self.relative(path)}")
        return path

    def theme_paths(self, names):
        result = []
        for name in dict.fromkeys(names):
            check_name(name)
            path = inside(self.sources, name)
            if not path.is_dir():
                raise ValueError(f"主题尚不存在：{name}")
            result.append((name, path))
        return result

    def tool(self, name):
        value = self.executables.get(name) or name
        if not isinstance(value, str):
            raise ValueError(f"executables.{name} 必须为字符串或 null")
        if Path(value).is_absolute() or "/" in value or "\\" in value:
            candidate = Path(value) if Path(value).is_absolute() else self.root / value
            return str(candidate.absolute()) if candidate.is_file() else None
        return shutil.which(value)


def run_command(command, timeout=60):
    completed = subprocess.run(command, capture_output=True, encoding="utf-8", errors="replace", timeout=timeout)
    return completed.returncode, completed.stdout, completed.stderr


def topics(workspace):
    result = {"source_root": workspace.paths["sources"], "themes": [], "skipped_links": [], "loose_files": []}
    if not workspace.sources.is_dir():
        result["status"] = "source_directory_missing"
        return result
    for path in sorted(workspace.sources.iterdir(), key=lambda p: p.name.casefold()):
        if is_link(path):
            result["skipped_links"].append(path.name)
        elif path.is_dir():
            result["themes"].append(path.name)
        else:
            result["loose_files"].append(path.name)
    return result


def doctor(workspace):
    report = {"schema_version": 1, "checked_at": now(), "python_version": sys.version.split()[0],
              "tools": {}, "modules": {}, "review": {"images_viewed": False, "motion_watched": False, "audio_listened": False}}
    for key in ("ffmpeg", "ffprobe", "exiftool"):
        executable = workspace.tool(key)
        entry = {"available": False, "optional": key == "exiftool"}
        if executable:
            try:
                code, out, err = run_command([executable, "-ver" if key == "exiftool" else "-version"], 20)
                entry.update(available=code == 0, returncode=code, version_output=(out + err)[:1200])
            except (OSError, subprocess.TimeoutExpired) as exc:
                entry["error"] = str(exc)
        else:
            entry["error"] = "未在配置或 PATH 找到程序"
        report["tools"][key] = entry
    for module in ("PIL", "numpy", "faster_whisper"):
        report["modules"][module] = importlib.util.find_spec(module) is not None
    report["libx264"] = {"tested": False, "passed": False}
    ffmpeg = workspace.tool("ffmpeg")
    if report["tools"]["ffmpeg"]["available"]:
        command = [ffmpeg, "-hide_banner", "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=64x64:r=1", "-frames:v", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-f", "null", "-"]
        try:
            code, _, err = run_command(command, 30)
            report["libx264"] = {"tested": True, "passed": code == 0, "returncode": code, "stderr": err[-2000:], "input": "synthetic_black_frame"}
        except (OSError, subprocess.TimeoutExpired) as exc:
            report["libx264"] = {"tested": True, "passed": False, "error": str(exc)}
    report["ready_for_inventory_and_contacts"] = all((report["tools"]["ffmpeg"]["available"], report["tools"]["ffprobe"]["available"], report["modules"]["PIL"], report["libx264"]["passed"]))
    report["ready_for_rendering"] = report["ready_for_inventory_and_contacts"] and report["modules"]["numpy"]
    report["rendering_readiness_scope"] = "base_dependencies_and_synthetic_frame_only; not an end-to-end renderer validation"
    report["not_verified"] = ["real_media_decode", "human_visual_review", "continuous_playback", "audio_listening", "ASR_model_inference", "final_video_rendering"]
    log_dir = workspace.output(workspace.path("logs"), must_be_new=False)
    log_dir.mkdir(parents=True, exist_ok=True)
    target = workspace.output(log_dir / ("doctor_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json"))
    write_json_new(target, report)
    return {"report": workspace.relative(target), "details": report}


def new_project(workspace, name, themes, brief):
    check_name(name)
    selected = [name for name, _ in workspace.theme_paths(themes)]
    brief_path = reject_link_chain(brief)
    text = brief_path.read_text(encoding="utf-8-sig")
    if not text.strip():
        raise ValueError("作品描述文件为空")
    target = workspace.output(workspace.path("projects") / name)
    checklist = inside(workspace.path("templates"), "交付检查清单.md").read_text(encoding="utf-8-sig")
    style_path = inside(workspace.path("resources"), "style.default.json")
    style = read_json(style_path)
    target.mkdir(parents=True, exist_ok=False)
    for folder in ("00_input", "01_analysis", "02_story", "03_edit", "04_review", "05_exports", "logs"):
        (target / folder).mkdir()
    write_text_new(target / "brief.md", text)
    write_text_new(target / "notes.md", "# 已确认事实与待确认问题\n\n尚未审阅素材；不要根据文件名编造人物、经历或对白。\n")
    write_text_new(target / "decisions.md", "# 修改与确认记录\n\n尚无粗剪或正式版确认。后续记录需绑定具体版本与文件。\n")
    write_text_new(target / "交付检查清单.md", checklist)
    write_json_new(target / "style.json", style)
    write_json_new(target / "project_config.json", {"schema_version": 1, "name": name, "created_at": now(), "themes": selected, "source_handling": "reference_only", "style_snapshot": "style.json", "style_source_sha256": hashlib.sha256(style_path.read_bytes()).hexdigest()})
    write_json_new(target / "state.json", {"schema_version": 1, "phase": "input", "created_at": now(), "selected_themes": selected, "brief_supplied": True, "review_status": "not_started", "review": {"images_viewed": False, "video_frames_viewed": False, "motion_watched": False, "audio_listened": False}, "rough_cut_approval": None, "final_delivery": None, "locked": False, "next_action": "inventory_selected_themes"})
    write_json_new(target / "asset_usage.json", {"schema_version": 1, "status": "not_indexed", "references": []})
    return {"created_project": workspace.relative(target), "themes": selected, "media_processing_started": False}


def main():
    configure_console()
    parser = argparse.ArgumentParser(description="便携 Vlog 工作区管理；不修改原片")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="工作区根目录；默认是工具包根目录")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("topics", help="列出素材直接子主题，不递归")
    commands.add_parser("doctor", help="检测工具和合成帧 libx264 编码；不代表实际审阅")
    new = commands.add_parser("new", help="创建作品文件夹和状态，拒绝覆盖")
    new.add_argument("name")
    new.add_argument("--themes", nargs="+", required=True)
    new.add_argument("--brief", required=True, help="用户明确指定的 UTF-8 描述文件")
    args = parser.parse_args()
    try:
        workspace = Workspace(args.root)
        result = topics(workspace) if args.command == "topics" else doctor(workspace) if args.command == "doctor" else new_project(workspace, args.name, args.themes, args.brief)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if args.command == "doctor" and not result["details"]["ready_for_inventory_and_contacts"] else 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"错误：{exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
