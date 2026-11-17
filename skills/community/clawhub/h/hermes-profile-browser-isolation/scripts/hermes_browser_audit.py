#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""审计浏览器实例是否在屏幕上开窗口（会抢用户焦点）——多 profile 隔离的验收工具。

判据: 登记了 CDP 端口的"后台型"实例，**可见窗口数必须 = 0**。
      别只看命令行有没有 --headless —— renderer/GPU 子进程不带该参数，
      实例也可能被别的机制以有头模式拉起；判据必须是"屏幕上有没有窗口"。

平台支持:
  Windows   窗口级精确（EnumWindows + GetWindowThreadProcessId 按 PID 归属）
  macOS     进程级（System Events visible）
  Linux/X11 进程级（wmctrl -lp，需 wmctrl）
  无 GUI     无窗口概念，headless 天然满足

用法:
  python hermes_browser_audit.py                    # 审计；exit 0=干净，1=有窗口
  python hermes_browser_audit.py --enforce-headless # 有窗口即按端口重启为无头
  python hermes_browser_audit.py --json
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

IS_WIN = os.name == "nt"
IS_MAC = sys.platform == "darwin"


# ───────────────────────── 定位 ─────────────────────────
def hermes_home():
    e = os.environ.get("HERMES_HOME")
    if e and Path(e).expanduser().exists():
        return Path(e).expanduser()
    la = os.environ.get("LOCALAPPDATA")
    cands = ([Path(la) / "hermes"] if la else []) + [
        Path.home() / "Library/Application Support/hermes",
        Path.home() / ".hermes", Path.home() / ".local/share/hermes",
        Path.home() / "AppData/Local/hermes"]
    for c in cands:
        if c and ((c / "config.yaml").exists() or (c / "profiles").is_dir()):
            return c
    return Path.cwd()


def instances(home):
    """实例表 + 各 config 的 cdp_url 汇总为 {name: {port, dir}}（并集）"""
    out = {}
    p = home / "hermes_browser_instances.json"
    if p.exists():
        try:
            for n, v in json.loads(p.read_text(encoding="utf-8")).get("instances", {}).items():
                out[n] = {"port": v.get("port"), "dir": v.get("dir", "")}
        except Exception:
            pass
    cfgs = [("default", home / "config.yaml")]
    pd = home / "profiles"
    if pd.is_dir():
        cfgs += [(d.name, d / "config.yaml") for d in sorted(pd.iterdir())
                 if d.is_dir() and (d / "config.yaml").exists()]
    for n, c in cfgs:
        try:
            m = re.search(r'cdp_url:\s*"?http://127\.0\.0\.1:(\d+)',
                          c.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        if m:
            out.setdefault(n, {})["port"] = int(m.group(1))
            out[n].setdefault("dir", "")
    return out


# ───────────────────────── 可见窗口探测 ─────────────────────────
def visible_pids():
    """{pid: [窗口标题/占位]} —— 屏幕上有可见窗口（或可见进程）的 PID"""
    if IS_WIN:
        return _win()
    if IS_MAC:
        return _mac()
    return _x11()


def _win():
    import ctypes
    from ctypes import wintypes
    u = ctypes.windll.user32
    res = {}
    CB = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def cb(hwnd, _):
        try:
            if not u.IsWindowVisible(hwnd):
                return True
            ln = u.GetWindowTextLengthW(hwnd)
            if ln <= 0:
                return True                      # 无标题 = 隐藏工具窗，不算抢屏
            buf = ctypes.create_unicode_buffer(ln + 1)
            u.GetWindowTextW(hwnd, buf, ln + 1)
            pid = wintypes.DWORD()
            u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            res.setdefault(pid.value, []).append(buf.value)
        except Exception:
            pass
        return True

    u.EnumWindows(CB(cb), 0)
    return res


def _mac():
    s = ('tell application "System Events" to get unix id of every process '
         'whose visible is true')
    try:
        o = subprocess.run(["osascript", "-e", s], capture_output=True,
                           text=True, timeout=25).stdout
        return {int(x): ["(进程可见)"] for x in re.findall(r"\d+", o)}
    except Exception:
        return {}


def _x11():
    try:
        o = subprocess.run(["wmctrl", "-lp"], capture_output=True,
                           text=True, timeout=20).stdout
    except Exception:
        return {}
    res = {}
    for ln in o.splitlines():
        parts = ln.split(None, 4)
        if len(parts) >= 3 and parts[2].isdigit():
            res.setdefault(int(parts[2]), []).append(parts[4] if len(parts) > 4 else "")
    return res


# ───────────────────────── 主体 ─────────────────────────
def _belongs(pid, inst):
    """该 PID 是否属于某个已登记实例；返回实例名或 None"""
    try:
        import psutil
        p = psutil.Process(pid)
        nm = (p.name() or "").lower()
        if not any(k in nm for k in ("chrome", "chromium", "msedge", "brave")):
            return None
        cl = " ".join(p.cmdline()).lower()
    except Exception:
        return None
    for n, v in inst.items():
        udd = (v.get("dir") or "").lower()
        port = v.get("port")
        if (udd and udd in cl) or (port and f"--remote-debugging-port={port}" in cl):
            return n
    return None


def scan(home):
    inst = instances(home)
    vis = visible_pids()
    bad = {}
    for pid, titles in vis.items():
        n = _belongs(pid, inst)
        if n:
            bad.setdefault(n, {"port": inst[n].get("port"),
                               "hits": []})["hits"].append({"pid": pid, "titles": titles[:3]})
    return inst, bad


def main():
    home = hermes_home()
    inst, bad = scan(home)
    if "--json" in sys.argv:
        print(json.dumps({"home": str(home), "instances": inst,
                          "visible_windows": bad}, ensure_ascii=False, indent=2))
        return 1 if bad else 0
    mode = ("Windows 窗口级" if IS_WIN else
            ("macOS 进程级" if IS_MAC else "Linux/X11 进程级"))
    print(f"Hermes home : {home}")
    print(f"判定方式    : {mode}   登记实例 {len(inst)} 个\n")
    for n, v in inst.items():
        flag = "❌ 有可见窗口(抢屏)" if n in bad else "✅ 无可见窗口"
        print(f"  {n:<14} :{str(v.get('port')):<6} {flag}")
        for h in (bad.get(n, {}) or {}).get("hits", []):
            print(f"       pid={h['pid']}  {h['titles']}")
    if not bad:
        print("\n✅ 全部后台型实例可见窗口 = 0（不抢用户焦点）")
        return 0
    if "--enforce-headless" in sys.argv:
        prov = Path(__file__).with_name("hermes_browser_provision.py")
        print("\n[纠偏] 发现可见窗口 → 按端口重启为无头 …")
        for n in bad:
            if prov.exists():
                subprocess.run([sys.executable, str(prov), "restart", n],
                               capture_output=True, text=True, timeout=180)
                print(f"  → {n} :{bad[n]['port']} 已重启为无头")
        time.sleep(3)
        _, again = scan(home)
        if again:
            print(f"\n❌ 仍有可见窗口: {sorted(again)}（可能被外部机制反复拉起）")
            return 1
        print("\n✅ 已全部纠正为无头")
        return 0
    print("\n纠偏: python hermes_browser_audit.py --enforce-headless")
    return 1


if __name__ == "__main__":
    sys.exit(main())
