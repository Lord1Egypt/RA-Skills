#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给 Hermes 的每个 profile 配独立无头浏览器实例（跨平台通用）。

问题  : 多个 profile / 多个 AI 成员共用浏览器 -> 互相抢焦点、串登录态、
        临时实例（%TEMP%/agent-browser-chrome-*）堆积吃内存。
方案  : 每个 profile 绑一个"固定 user-data-dir + 固定 CDP 端口"的独立实例，
        默认 headless（不弹窗、不抢屏），登录态长期复用。
原理  : Hermes 原生支持 config 里的 browser.cdp_url（连上即用，不再本地 launch），
        且每次调用重读配置（热生效，无需重启网关）。

用法:
  python hermes_browser_provision.py discover              # 只看方案，不写不改
  python hermes_browser_provision.py apply [--dry-run]     # 写 config(自动备份)+拉起
  python hermes_browser_provision.py status                # 实例状态 + 全机浏览器账
  python hermes_browser_provision.py start all|<name> [--headed]
  python hermes_browser_provision.py stop <name>
  python hermes_browser_provision.py stopall
  python hermes_browser_provision.py restart all|<name> [--headed]
  python hermes_browser_provision.py pages <port>
  python hermes_browser_provision.py trim <port> [keep]
  python hermes_browser_provision.py killport <port>
  python hermes_browser_provision.py claim <name> <port> <dir> [binary]  # 认领既有实例

环境变量:
  HERMES_HOME               Hermes 根目录（默认自动探测）
  HERMES_BROWSER_BASE_PORT  起始端口（默认 9410）
依赖: psutil
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

BASE_PORT = int(os.environ.get("HERMES_BROWSER_BASE_PORT", "9410"))
STATE_FILE = "hermes_browser_instances.json"


# ───────────────────────── 定位 ─────────────────────────
def find_hermes_home(explicit=None):
    if explicit:
        return Path(explicit).expanduser()
    env = os.environ.get("HERMES_HOME")
    if env:
        p = Path(env).expanduser()
        if p.exists():
            return p
    cands = []
    if os.name == "nt":
        la = os.environ.get("LOCALAPPDATA")
        if la:
            cands.append(Path(la) / "hermes")
    elif sys.platform == "darwin":
        cands.append(Path.home() / "Library/Application Support/hermes")
    cands += [Path.home() / ".hermes", Path.home() / ".local/share/hermes",
              Path.home() / "AppData/Local/hermes"]
    for c in cands:
        if (c / "config.yaml").exists() or (c / "profiles").is_dir():
            return c
    return cands[0]


def profile_configs(home):
    """返回 [(profile_name, config_path)]；default 就是根 config.yaml"""
    out = []
    if (home / "config.yaml").exists():
        out.append(("default", home / "config.yaml"))
    pd = home / "profiles"
    if pd.is_dir():
        for d in sorted(pd.iterdir()):
            cfg = d / "config.yaml"
            if d.is_dir() and cfg.exists():
                out.append((d.name, cfg))
    return out


def find_browser(kind):
    """跨平台找浏览器可执行文件"""
    names = {"edge": ["msedge"],
             "chromium": ["chromium", "chromium-browser"],
             "chrome": ["google-chrome", "google-chrome-stable", "chromium", "chrome"]}
    if os.name == "nt":
        pf = os.environ.get("ProgramFiles", r"C:\Program Files")
        pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        la = os.environ.get("LOCALAPPDATA", "")
        cands = {
            "chrome": [rf"{pf}\Google\Chrome\Application\chrome.exe",
                       rf"{pf86}\Google\Chrome\Application\chrome.exe",
                       rf"{la}\Google\Chrome\Application\chrome.exe"],
            "edge": [rf"{pf86}\Microsoft\Edge\Application\msedge.exe",
                     rf"{pf}\Microsoft\Edge\Application\msedge.exe"],
            "chromium": [],
        }[kind]
    elif sys.platform == "darwin":
        cands = {
            "chrome": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
            "edge": ["/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"],
            "chromium": ["/Applications/Chromium.app/Contents/MacOS/Chromium"],
        }[kind]
    else:
        cands = {
            "chrome": ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable"],
            "edge": ["/usr/bin/microsoft-edge", "/usr/bin/microsoft-edge-stable"],
            "chromium": ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/snap/bin/chromium"],
        }[kind]
    for c in cands:
        if c and os.path.exists(c):
            return c
    for n in names[kind]:
        w = shutil.which(n)
        if w:
            return w
    return None


# ───────────────────────── CDP ─────────────────────────
def cdp_get(port, path, timeout=3):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except Exception:
        return None


def is_alive(port):
    return cdp_get(port, "/json/version") is not None


# ───────────────────────── 实例表 ─────────────────────────
def load_state(home):
    p = home / STATE_FILE
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"instances": {}}


def save_state(home, st):
    try:
        (home / STATE_FILE).write_text(json.dumps(st, indent=2, ensure_ascii=False),
                                       encoding="utf-8")
    except Exception as e:
        print(f"  [!] 实例表写入失败: {e}")


def plan(home):
    """幂等分配：已登记/已配置的沿用端口，新 profile 从 BASE_PORT 往上找空位。"""
    st = load_state(home)
    inst = st.setdefault("instances", {})
    cfgs = dict(profile_configs(home))
    used = {v.get("port") for v in inst.values()}
    for name, cfg in cfgs.items():
        try:
            t = cfg.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        m = re.search(r'cdp_url:\s*"?http://127\.0\.0\.1:(\d+)', t)
        if m:
            used.add(int(m.group(1)))
            inst.setdefault(name, {})["port"] = int(m.group(1))
    nxt = BASE_PORT
    for name in cfgs:
        cur = inst.setdefault(name, {})
        if not cur.get("port"):
            # 避开：本 home 已声明/登记的端口 + 实际已在监听的端口（别的 home/进程占的）
            while nxt in used or is_alive(nxt):
                nxt += 1
            cur["port"] = nxt
            used.add(nxt)
            nxt += 1
        cur.setdefault("dir", str(home / "browser-profiles" / name))
        cur.setdefault("binary", "chrome")
    st["instances"] = dict(sorted(inst.items()))   # 输出稳定：按 profile 名排序
    return st


def upsert_cdp_url(cfg_path, port, dry_run=False):
    """在 config.yaml 的 browser: 段写/更新 cdp_url（保留其它内容、注释与顺序）。"""
    cfg_path = Path(cfg_path)
    try:
        text = cfg_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"read-error: {e}"
    line = f'  cdp_url: "http://127.0.0.1:{port}"'
    lines = text.splitlines()
    bidx = None
    for i, ln in enumerate(lines):
        if re.match(r'^browser:\s*(#.*)?$', ln):
            bidx = i
            break
    if bidx is None:
        new = text + ("" if text.endswith("\n") else "\n") + f"browser:\n{line}\n"
    else:
        end = len(lines)
        for j in range(bidx + 1, len(lines)):
            if re.match(r'^\S', lines[j]):
                end = j
                break
        hit = False
        for j in range(bidx + 1, end):
            if re.match(r'^\s+cdp_url\s*:', lines[j]):
                lines[j] = line
                hit = True
                break
        if not hit:
            lines.insert(bidx + 1, line)
        new = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    if new == text:
        return "same"
    if dry_run:
        return "would-change"
    bak = cfg_path.with_name(cfg_path.name + ".bak-" + time.strftime("%Y%m%d_%H%M%S"))
    try:
        bak.write_text(text, encoding="utf-8")
        cfg_path.write_text(new, encoding="utf-8")
    except Exception as e:
        return f"write-error: {e}"
    return "changed"


# ───────────────────────── 起停 ─────────────────────────
def start_instance(name, info, headless=True):
    port, udd = info["port"], info["dir"]
    if is_alive(port):
        v = cdp_get(port, "/json/version") or {}
        print(f"  [=] {name:<12} :{port} 已在运行  {v.get('Browser', '')}")
        return True
    Path(udd).mkdir(parents=True, exist_ok=True)
    exe = find_browser(info.get("binary", "chrome")) or find_browser("chrome")
    if not exe:
        print(f"  [!] {name}: 未找到浏览器可执行文件（装 Chrome/Edge，或用 claim 指定）")
        return False
    args = [exe, f"--remote-debugging-port={port}", f"--user-data-dir={udd}",
            "--no-first-run", "--no-default-browser-check", "--disable-sync",
            "--disable-background-networking", "--disable-features=Translate"]
    if headless:
        args.append("--headless=new")
    kw = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    if os.name == "nt":
        kw["creationflags"] = 0x00000008 | 0x00000200   # DETACHED_PROCESS | NEW_GROUP
    else:
        kw["start_new_session"] = True
    try:
        subprocess.Popen(args, **kw)
    except Exception as e:
        print(f"  [!] {name}: 启动异常 {e}")
        return False
    for _ in range(24):
        time.sleep(0.5)
        if is_alive(port):
            v = cdp_get(port, "/json/version") or {}
            print(f"  [+] {name:<12} :{port} 启动成功  {v.get('Browser', '')}")
            return True
    print(f"  [!] {name:<12} :{port} 启动失败（12s 未监听）")
    return False


def _kill_by(pred, why):
    try:
        import psutil
    except ImportError:
        print("  [!] 缺 psutil：pip install psutil")
        return 0
    n = 0
    for pid in psutil.pids():                      # 逐个独立快照，别用 process_iter().info
        try:
            p = psutil.Process(pid)
            nm = (p.name() or "").lower()
            if not any(k in nm for k in ("chrome", "chromium", "msedge", "brave")):
                continue
            cl = " ".join(p.cmdline())
        except Exception:
            continue
        if pred(cl):
            try:
                p.kill()
                n += 1
            except Exception:
                pass
    print(f"  [-] {why} 已终止 {n} 进程")
    return n


def stop_instance(name, info):
    return _kill_by(lambda cl: info["dir"].lower() in cl.lower(), f"{name} :{info['port']}")


# ───────────────────────── 命令 ─────────────────────────
def cmd_discover(home):
    st = plan(home)
    print(f"Hermes home : {home}")
    print(f"发现 {len(st['instances'])} 个 profile：\n")
    print(f"{'profile':<14}{'端口':<8}{'实例':<10}{'user-data-dir'}")
    print("-" * 88)
    for n, v in st["instances"].items():
        print(f"{n:<14}{v['port']:<8}{'运行中' if is_alive(v['port']) else '未运行':<10}{v['dir']}")
    save_state(home, st)
    print(f"\n实例表: {home / STATE_FILE}")
    print("落地: python hermes_browser_provision.py apply  （会自动备份 config）")


def cmd_apply(home, dry_run=False, only=None):
    st = plan(home)
    cmap = dict(profile_configs(home))
    names = [only] if only else list(st["instances"])
    for n in names:
        cfg = cmap.get(n)
        if not cfg:
            print(f"  [!] 找不到 profile {n}")
            continue
        r = upsert_cdp_url(cfg, st["instances"][n]["port"], dry_run)
        mark = "+" if r == "changed" else ("=" if r == "same" else "!")
        print(f"  [{mark}] {n:<12} browser.cdp_url -> :{st['instances'][n]['port']}  ({r})")
    save_state(home, st)
    if dry_run:
        print("\n[dry-run] 未改配置、未起进程。去掉 --dry-run 即落地。")
        return
    print()
    for n in names:
        if n in st["instances"]:
            start_instance(n, st["instances"][n])
    print("\n验收: python hermes_browser_audit.py   （可见窗口必须 = 0）")


def cmd_status(home):
    st = plan(home)
    print(f"{'profile':<14}{'端口':<8}{'状态':<26}{'user-data-dir'}")
    print("-" * 92)
    for n, v in st["instances"].items():
        al = is_alive(v["port"])
        extra = ""
        if al:
            b = (cdp_get(v["port"], "/json/version") or {}).get("Browser", "")
            extra = " " + b.split("/")[-1][:10] + (" (headless)" if "Headless" in b else " (有头!)")
        print(f"{n:<14}{v['port']:<8}{('运行中' + extra) if al else '未运行':<26}{v['dir']}")
    save_state(home, st)
    try:
        import collections
        import psutil
    except ImportError:
        return
    print("\n全机浏览器进程账（按 user-data-dir 归属）:")
    d = collections.defaultdict(lambda: [0, 0])
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
            if not any(k in (p.name() or "").lower()
                       for k in ("chrome", "chromium", "msedge", "brave")):
                continue
            u = [a for a in p.cmdline() if a.startswith("--user-data-dir")]
            k = u[0].split("=", 1)[1] if u else "DEFAULT(用户桌面浏览器)"
            d[k][0] += 1
            d[k][1] += p.memory_info().rss
        except Exception:
            pass
    tot_p = tot_m = 0
    for k, (c, m) in sorted(d.items(), key=lambda x: -x[1][1])[:10]:
        tot_p += c
        tot_m += m
        print(f"  {c:3d}进程 {m / 1048576:7.0f}MB  {k[-62:]}")
    print(f"  ---- 合计 {tot_p} 进程 / {tot_m / 1048576:.0f} MB")


def main():
    a = sys.argv[1:]
    cmd = a[0] if a else "status"
    home = find_hermes_home()
    if cmd == "discover":
        cmd_discover(home)
    elif cmd == "apply":
        rest = [x for x in a[1:] if not x.startswith("--")]
        cmd_apply(home, dry_run="--dry-run" in a, only=(rest[0] if rest else None))
    elif cmd == "status":
        cmd_status(home)
    elif cmd in ("start", "restart"):
        st = plan(home)
        headless = "--headed" not in a
        tgt = [x for x in a[1:] if not x.startswith("--")]
        names = list(st["instances"]) if (not tgt or tgt == ["all"]) else tgt
        if cmd == "restart":
            for n in names:
                if n in st["instances"]:
                    stop_instance(n, st["instances"][n])
            time.sleep(2)
        for n in names:
            if n in st["instances"]:
                start_instance(n, st["instances"][n], headless=headless)
    elif cmd == "stop":
        st = plan(home)
        if a[1] in st["instances"]:
            stop_instance(a[1], st["instances"][a[1]])
        else:
            print(f"  [!] 未登记 profile {a[1]}")
    elif cmd == "stopall":
        st = plan(home)
        for n, v in st["instances"].items():
            stop_instance(n, v)
    elif cmd == "claim":
        st = plan(home)
        n, port, d = a[1], int(a[2]), a[3]
        st["instances"][n] = {"port": port, "dir": d,
                              "binary": a[4] if len(a) > 4 else "chrome"}
        save_state(home, st)
        cfg = dict(profile_configs(home)).get(n)
        if cfg:
            print(f"  [{upsert_cdp_url(cfg, port)}] {n} -> :{port}  ({d})")
        print("  注意: 认领只改端口与登记、不动目录 -> 登录态保留。")
    elif cmd == "pages":
        port = int(a[1])
        pg = [t for t in (cdp_get(port, "/json/list") or []) if t.get("type") == "page"]
        print(f":{port} 共 {len(pg)} 个页面")
        for t in pg:
            print(f"  {(t.get('title') or '')[:40]:<40} {t.get('url', '')[:70]}")
    elif cmd == "trim":
        port = int(a[1])
        keep = int(a[2]) if len(a) > 2 else 1
        pg = [t for t in (cdp_get(port, "/json/list") or []) if t.get("type") == "page"]
        n = 0
        for t in pg[keep:]:
            try:
                urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/json/close/{t['id']}", timeout=3).read()
                n += 1
            except Exception:
                pass
        print(f":{port} 关闭 {n} 个页面，保留 {min(keep, len(pg))} 个")
    elif cmd == "killport":
        _kill_by(lambda cl: f"--remote-debugging-port={a[1]}" in cl, f":{a[1]}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
