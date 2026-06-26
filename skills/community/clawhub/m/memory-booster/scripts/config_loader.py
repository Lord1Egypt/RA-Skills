#!/usr/bin/env python3
"""
memory-booster 配置加载器
所有脚本通过此模块获取 memory_dirs 等配置。
优先级：config.json 指定 > 自动检测 > 硬编码默认值
"""
import json
import os
import re
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent  # memory-booster 根目录
CONFIG_PATH = SKILL_DIR / "config.json"
HOME = Path.home()


def _auto_detect_memory_dirs():
    """自动检测所有有实际内容的 workbuddy memory 目录"""
    candidates = []
    diary_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")

    # 策略1：扫描 HOME 下所有 WorkBuddy 工作区（只保留有日记的）
    wb_base = HOME / "WorkBuddy"
    if wb_base.is_dir():
        for child in sorted(wb_base.iterdir()):
            if child.is_dir():
                mem = child / ".workbuddy" / "memory"
                if mem.is_dir():
                    # 必须至少有 1 个日记文件或 MEMORY.md 才算有效
                    has_content = any(
                        diary_pattern.match(f.name) or f.name == "MEMORY.md"
                        for f in mem.iterdir() if f.suffix == ".md"
                    )
                    if has_content:
                        # Claw 工作区优先（排最前面）
                        if child.name in ("Claw", "claw"):
                            candidates.insert(0, str(mem))
                        else:
                            candidates.append(str(mem))

    # 策略2：全局 .workbuddy/memory（有内容才加）
    global_mem = HOME / ".workbuddy" / "memory"
    if global_mem.is_dir():
        has_content = any(
            diary_pattern.match(f.name) or f.name == "MEMORY.md"
            for f in global_mem.iterdir() if f.suffix == ".md"
        )
        if has_content:
            candidates.append(str(global_mem))

    # 策略3：当前目录往上找 .workbuddy/memory
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        mem = parent / ".workbuddy" / "memory"
        if mem.is_dir():
            has_content = any(
                diary_pattern.match(f.name) or f.name == "MEMORY.md"
                for f in mem.iterdir() if f.suffix == ".md"
            )
            if has_content and str(mem) not in candidates:
                candidates.append(str(mem))
            break

    return candidates


def load_config():
    """加载配置，返回 (memory_dirs, chroma_db_dir)"""
    memory_dirs = []
    chroma_db_dir = str(SKILL_DIR / "chroma_db")

    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                cfg = json.load(f)
            if cfg.get("memory_dirs"):
                memory_dirs = [d for d in cfg["memory_dirs"] if Path(d).is_dir()]
            if cfg.get("chroma_db_dir"):
                chroma_db_dir = cfg["chroma_db_dir"]
        except (json.JSONDecodeError, IOError):
            pass

    # 如果 config.json 没指定路径，自动检测
    if not memory_dirs:
        memory_dirs = _auto_detect_memory_dirs()

    # 确保 chroma_db 目录存在
    Path(chroma_db_dir).mkdir(parents=True, exist_ok=True)

    return memory_dirs, chroma_db_dir


def get_memory_files(memory_dirs):
    """返回所有需要索引的 .md 文件（去重）"""
    files = {}
    for d in memory_dirs:
        mp = Path(d)
        if not mp.is_dir():
            continue
        for fpath in sorted(mp.iterdir()):
            if fpath.suffix == ".md":
                # 用文件名去重（同名文件取第一个）
                if fpath.name not in files:
                    files[fpath.name] = fpath
    return list(files.values())


def get_memory_md_path(memory_dirs):
    """找到 MEMORY.md 路径"""
    for d in memory_dirs:
        mem_md = Path(d) / "MEMORY.md"
        if mem_md.exists():
            return str(mem_md)

    # 默认：第一个 memory_dir 下创建
    if memory_dirs:
        return str(Path(memory_dirs[0]) / "MEMORY.md")
    return None


if __name__ == "__main__":
    dirs, chroma = load_config()
    print(f"memory_dirs ({len(dirs)}):")
    for d in dirs:
        print(f"  - {d}")
    print(f"chroma_db_dir: {chroma}")
    print(f"MEMORY.md: {get_memory_md_path(dirs)}")
    files = get_memory_files(dirs)
    print(f"memory files: {len(files)}")
