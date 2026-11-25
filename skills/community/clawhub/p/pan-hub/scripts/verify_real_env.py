#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真机验证：把沙箱里无法完成的 Range 分片 / rclone / MCP 回归在本机跑一遍。

用法（本机执行，不要加 --apply/--send 之外的重开关）：
  python3 scripts/verify_real_env.py
  python3 scripts/verify_real_env.py --transfer-src alist:src/a --transfer-dst alist:bak/a
可选：
  --split-url <直链>   跳过本地 http.server 分片测试，改用你指定的支持 Range 的直链
"""
from __future__ import annotations

import argparse, json, os, subprocess, sys, tempfile, threading
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = Path(__file__).resolve().parent.parent
PAN = ROOT / "scripts" / "pan.py"
PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"


def sh(args, env=None, timeout=180):
    e = dict(os.environ); e.update(env or {})
    return subprocess.run([sys.executable, str(PAN)] + args, capture_output=True, text=True, env=e, timeout=timeout)


def step(name, ok, note=""):
    print("[%s] %s %s" % (ok, name, ("- " + str(note) if note else "")))


def check_doctor():
    p = sh(["doctor", "--json"])
    if p.returncode != 0:
        return FAIL, p.stderr[:300]
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError:
        return FAIL, "doctor 输出非 JSON"
    if not isinstance(data, dict) or not data.get("checks"):
        return FAIL, json.dumps(data, ensure_ascii=False)[:300]
    names = {str(c[0]) for c in data["checks"]}
    missing_required = [n for n in ("curl",) if n not in names]
    return (PASS, "doctor ok checks=%d" % len(data["checks"])) if not missing_required else (FAIL, "缺少必需项 %s" % missing_required)


def check_range_split(split_url=""):
    tmp = Path(tempfile.mkdtemp(prefix="pan_verify_range_"))
    srv = tmp / "srv"; srv.mkdir()
    reports = tmp / "reports"; reports.mkdir()
    out = tmp / "out"; out.mkdir()
    cfg = tmp / "config.json"
    payload = bytes((i * 31 + 7) % 256 for i in range(8 * 1024 * 1024))  # 8MB 确定性内容
    (srv / "test.bin").write_bytes(payload)
    url = split_url or ""
    if not url:
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), SimpleHTTPRequestHandler)
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        url = "http://127.0.0.1:%d/test.bin" % port
        stop = httpd.shutdown
    else:
        stop = None
    cfg.write_text(json.dumps({"http": {"retries": 2, "retry_delay": 1, "connect_timeout": 10, "timeout": 120,
                                        "report_dir": str(reports), "range_split": False, "range_split_connections": 0}}),
                    encoding="utf-8")
    env = {"PAN_CONFIG": str(cfg), "PAN_LOG": str(tmp / "run.log"), "PYTHONPYCACHEPREFIX": "/tmp/pan-verify-pyc"}
    p = sh(["get", url, "--to", str(out), "--split", "4", "--events"], env=env)
    if stop:
        stop()
    dst = out / "test.bin"
    if p.returncode == 0 and dst.exists() and dst.stat().st_size == len(payload):
        rep = reports / "下载报告.json"
        return PASS, "分片下载成功 size=%d report=%s" % (len(payload), rep.exists())
    return FAIL, (p.stdout + "\n" + p.stderr)[:600]


def check_rclone(transfer_src, transfer_dst):
    which = subprocess.run(["which", "rclone"], capture_output=True, text=True).returncode
    if which != 0:
        return SKIP, "未安装 rclone（brew install rclone / apt install rclone）"
    if not (transfer_src and transfer_dst):
        return SKIP, "传 --transfer-src/--transfer-dst 才做 rclone dry-run 检查"
    p = sh(["transfer", transfer_src, transfer_dst, "--json"])
    try:
        data = json.loads(p.stdout or "{}")
    except json.JSONDecodeError:
        return FAIL, p.stdout[:300]
    if p.returncode == 0 and data.get("ok"):
        return PASS, "transfer dry-run 计划 ok"
    return FAIL, p.stdout[:300]


def check_mcp():
    payload = (
        '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}\n'
        '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n'
    )
    try:
        p = subprocess.run([sys.executable, str(ROOT / "scripts" / "pan_mcp.py")], input=payload,
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return FAIL, str(exc)
    if p.returncode != 0:
        return FAIL, p.stderr[:300]
    outs = []
    for line in p.stdout.strip().splitlines():
        try:
            outs.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    init = next((o for o in outs if isinstance(o, dict) and o.get("id") == 1), None)
    tools = next((o for o in outs if isinstance(o, dict) and o.get("id") == 2), None)
    if not init or not (init.get("result") or {}).get("protocolVersion"):
        return FAIL, "MCP initialize 无 protocolVersion"
    names = [t.get("name") for t in (tools.get("result") or {}).get("tools", [])] if tools else []
    expected = {"pan_doctor", "pan_detect", "pan_dirs", "pan_get_plan"}
    if not expected.issubset(set(names)):
        return FAIL, "tools/list 缺工具 %s" % sorted(expected - set(names))
    return PASS, "MCP initialize+tools ok（仍须注册到 $CODEX_HOME/config.toml 后重启 App 实测）"


def main():
    ap = argparse.ArgumentParser(description="真机验证 pan-hub")
    ap.add_argument("--split-url", default="")
    ap.add_argument("--transfer-src", "--transfer-source", default="")
    ap.add_argument("--transfer-dst", "--transfer-dest", default="")
    ap.add_argument("--only", choices=["doctor", "split", "rclone", "mcp"], default="")
    a = ap.parse_args()

    checks = []
    if not a.only or a.only == "doctor":
        checks.append(("doctor", check_doctor))
    if not a.only or a.only == "split":
        checks.append(("range-split", lambda: check_range_split(a.split_url)))
    if not a.only or a.only == "rclone":
        checks.append(("rclone-transfer", lambda: check_rclone(a.transfer_src, a.transfer_dst)))
    if not a.only or a.only == "mcp":
        checks.append(("mcp", check_mcp))
    for name, fn in checks:
        try:
            ok, note = fn()
        except Exception as exc:  # noqa: BLE001
            ok, note = FAIL, str(exc)[:300]
        step(name, ok, note)
    print("VERIFY_REAL_ENV_DONE")


if __name__ == "__main__":
    main()
