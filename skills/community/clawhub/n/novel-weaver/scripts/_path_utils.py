#!/usr/bin/env python3
"""
_path_utils.py — novel-weaver 路径工具
中文路径编码修复：通过 .project 文件缓存绝对路径，避免 Git Bash 中文编码问题。
"""
import json
from pathlib import Path

# 推断 data 目录
_SCRIPTS_DIR = Path(__file__).parent
DATA_DIR = _SCRIPTS_DIR.parent.parent / ".standardization" / "novel-weaver" / "projects"
MODELS_DIR = _SCRIPTS_DIR.parent.parent / ".standardization" / "novel-weaver" / "models"
PROJECT_LOCK = _SCRIPTS_DIR.parent.parent / ".standardization" / "novel-weaver" / ".project"


def resolve_state_path(raw_path: str | None = None) -> str | None:
    """
    获取 novel_state.json 的绝对路径。
    优先级: raw_path 有效 → .project 缓存 → DATA_DIR 自动扫描
    """
    # 1) raw_path 直接有效
    if raw_path:
        p = Path(raw_path)
        if p.exists():
            resolved = str(p.resolve())
            _save_project(resolved)
            return resolved
        # 尝试作为项目名
        proj_path = DATA_DIR / raw_path / "data" / "novel_state.json"
        if proj_path.exists():
            resolved = str(proj_path.resolve())
            _save_project(resolved)
            return resolved

    # 2) .project 缓存
    if PROJECT_LOCK.exists():
        cached = PROJECT_LOCK.read_text(encoding="utf-8").strip()
        if cached and Path(cached).exists():
            return cached

    # 3) DATA_DIR 仅一个项目 → 自动
    if DATA_DIR.exists():
        projects = [d for d in DATA_DIR.iterdir() if (d / "data" / "novel_state.json").exists()]
        if len(projects) == 1:
            sp = projects[0] / "data" / "novel_state.json"
            resolved = str(sp.resolve())
            _save_project(resolved)
            return resolved
        if len(projects) > 1:
            print(f"[路径] 找到 {len(projects)} 个项目，请指定项目名或路径:")
            for d in projects:
                print(f"  {d.name}")
            return None

    return raw_path  # 最后兜底


def _save_project(abs_path: str):
    """缓存到 .project 文件，后续命令免传路径"""
    try:
        PROJECT_LOCK.parent.mkdir(parents=True, exist_ok=True)
        PROJECT_LOCK.write_text(abs_path, encoding="utf-8")
    except Exception:
        pass


def list_projects() -> list[dict]:
    """列出所有项目"""
    result = []
    if not DATA_DIR.exists():
        return result
    for proj_dir in sorted(DATA_DIR.iterdir()):
        sp = proj_dir / "data" / "novel_state.json"
        if sp.exists():
            try:
                d = json.loads(sp.read_text(encoding="utf-8-sig"))
                result.append({
                    "name": d.get("project", proj_dir.name),
                    "path": str(sp.resolve()),
                    "phase": d.get("meta", {}).get("current_phase", "?"),
                    "length": d.get("meta", {}).get("length", "?"),
                    "chapters": len(d.get("chapters", [])),
                    "done": sum(1 for c in d.get("chapters", []) if c.get("status") == "completed"),
                })
            except Exception:
                continue
    return result
