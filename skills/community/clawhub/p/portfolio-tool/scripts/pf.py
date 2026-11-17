#!/usr/bin/env python3
"""
Portfolio_tool 后端 API 命令行封装（零依赖，仅用标准库 urllib）。

用法:
  python pf.py METHOD PATH [--data '{"k":"v"}'] [--q key=value ...]

示例:
  python pf.py GET  portfolios?mine=true
  python pf.py GET  portfolios/12
  python pf.py POST sync/portfolio-funds --data '{}'
  python pf.py GET  sync/portfolio-funds/status/<job_id>
  python pf.py POST user/login --data '{"username":"alice","password":"secret"}'

环境变量:
  PORTFOLIO_API  后端地址，默认 http://localhost:8000
  PORTFOLIO_AID  匿名用户 ID（X-Anonymous-Id）；写入操作的“我的组合”必须提供
"""
import sys
import os
import json
import hashlib
import urllib.request
import urllib.error
import urllib.parse

BASE = os.environ.get("PORTFOLIO_API", "http://localhost:8000").rstrip("/")


def _machine_fingerprint() -> str:
    """基于本机特征生成稳定匿名 ID（同一台机器恒定）。优先级同后端 mcp_server。"""
    parts = []
    for p in ("/etc/machine-id", "/var/lib/dbus/machine-id", "/etc/hostid"):
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                val = f.read().strip()
                if val:
                    parts.append(f"mid={val}")
                    break
        except Exception:
            pass
    if not parts:
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
            ) as k:
                parts.append("wg=" + winreg.QueryValueEx(k, "MachineGuid")[0])
        except Exception:
            pass
    if not parts:
        import getpass
        import platform
        import socket
        import uuid as _uuid
        node = _uuid.getnode()
        mac = ":".join(f"{(node >> (8 * i)) & 0xff:02x}" for i in reversed(range(6)))
        parts.append(
            f"fb={socket.gethostname()}|{mac}|{getpass.getuser()}|{platform.system()}"
        )
    raw = "|".join(parts)
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def ensure_aid() -> str:
    """
    取得匿名用户 ID：PORTFOLIO_AID → ~/.portfolio/aid → 首次按本机特征生成并持久化。
    保证兜底 CLI 在不同会话/重启后复用同一用户 ID。
    """
    aid = (os.environ.get("PORTFOLIO_AID") or "").strip()
    if aid:
        return aid
    aid_file = os.path.expanduser("~/.portfolio/aid")
    try:
        with open(aid_file, encoding="utf-8") as f:
            aid = f.read().strip()
            if aid:
                return aid
    except Exception:
        pass
    aid = _machine_fingerprint()
    try:
        os.makedirs(os.path.dirname(aid_file), exist_ok=True)
        with open(aid_file, "w", encoding="utf-8") as f:
            f.write(aid + "\n")
    except Exception:
        pass
    return aid


AID = ensure_aid()


def _print(body: str) -> None:
    try:
        print(json.dumps(json.loads(body), ensure_ascii=False, indent=2))
    except Exception:
        print(body)


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)

    method = sys.argv[1].upper()
    path = sys.argv[2].lstrip("/")
    if not path.startswith("api/"):
        path = "api/" + path

    data = None
    params = {}
    i = 3
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--data" and i + 1 < len(sys.argv):
            data = sys.argv[i + 1].encode("utf-8")
            i += 2
        elif a == "--q" and i + 1 < len(sys.argv):
            k, _, v = sys.argv[i + 1].partition("=")
            params[k] = v
            i += 2
        else:
            i += 1

    url = f"{BASE}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    if AID:
        headers["X-Anonymous-Id"] = AID

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            _print(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}")
        _print(e.read().decode("utf-8", "replace"))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"连接失败: {e.reason}\n请确认后端已启动且 PORTFOLIO_API 指向正确地址")
        sys.exit(3)


if __name__ == "__main__":
    main()
