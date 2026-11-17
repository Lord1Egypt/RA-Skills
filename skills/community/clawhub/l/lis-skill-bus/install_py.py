#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""install_skillbus.cmd 的 Python 助手（纯 stdlib，跨平台）。不碰 bus 核心逻辑。

用法: python3 install_py.py [--apply|--uninstall|--dry-run]
环境变量: CODEX_HOME, BUS_DIR, SECTION_LINE
"""
import datetime
import os
import sys
from pathlib import Path


def _read(p: Path):
    if not p.exists():
        return []
    try:
        return p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []


def _backup(p: Path):
    b = p.with_name(p.name + ".skillbus." + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".bak")
    if p.exists():
        p.replace(b)
        print(f"已备份原配置 -> {b}")
    return b


def _apply() -> int:
    home = os.environ.get("CODEX_HOME", "")
    bus = os.environ.get("BUS_DIR", "")
    sec = os.environ.get("SECTION_LINE", "[mcp_servers.lis-skill-bus]")
    if not home or not bus:
        print("[error] 需要 CODEX_HOME 与 BUS_DIR 环境变量", file=sys.stderr)
        return 2
    cfg = Path(home) / "config.toml"
    if sec in _read(cfg):
        print("bus 已注册，跳过 config 写入（幂等）")
        return 0
    # 保留既有内容：先备份一份，再向原文件追加新段
    b = str(cfg) + ".skillbus." + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".bak"
    if cfg.exists():
        open(b, "wb").write(cfg.read_bytes())
        print(f"已备份原配置 -> {b}")
    command = str(Path(bus) / "skillbus.py").replace("\\", "\\\\").replace('"', '\\"')
    block = "\n" + sec + '\ntype = "stdio"\ncommand = "' + command + '"\nargs = ["serve"]\n'
    with cfg.open("a", encoding="utf-8", newline="\n") as f:
        f.write(block)
    print(f"已写入 {cfg}（原文件已备份，可用 --uninstall 回滚）")
    return 0


def _uninstall() -> int:
    home = os.environ.get("CODEX_HOME", "")
    sec = os.environ.get("SECTION_LINE", "[mcp_servers.lis-skill-bus]")
    if not home:
        print("[error] 需要 CODEX_HOME", file=sys.stderr)
        return 2
    cfg = Path(home) / "config.toml"
    lines = _read(cfg)
    if sec not in lines:
        print("未注册，无需卸载。")
        return 0
    _backup(cfg)
    out = []
    skip = False
    for ln in lines:
        stripped = ln.strip()
        if not skip and stripped == sec:
            skip = True
            continue
        if skip:
            if stripped.startswith("["):
                skip = False
            else:
                continue
        out.append(ln)
    with cfg.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    print(f"已移除 {sec}（config 已备份；bus 文件保留）")
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--apply"
    if mode == "--dry-run":
        print("dry-run：基于环境变量 CODEX_HOME/BUS_DIR 校验，不写文件")
        sys.exit(0)
    sys.exit(_apply() if mode == "--apply" else _uninstall() if mode == "--uninstall" else 2)
