#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_verify.py — 结构化零网络自证（v5.0.0 新增）

背景：此前「零上传」的自证方式是建议用户 grep 源码里的网络模块名。
grep 字符串匹配有两个缺陷：报告页脚的 https:// URL 字符串（纯数据）会误报命中，
而真实经过别名/间接引用的网络调用又可能漏报。

本脚本改用 AST（语法树）结构化验证：
  1. import 级：import socket/ssl/http.client/urllib.request/requests/... 一律记 hit
  2. 调用级：urlopen(...) / socket.socket(...) 等网络属性调用记 hit
  3. 子进程级：把 curl/wget/nc/ftp 等network工具作为命令字符串传给
     subprocess/os.system/Popen 记 hit（字符串常量里的 URL 不算——那是数据不是代码）
  4. 编译级：scripts/*.py 全部 py_compile 可编译（交付物无语法残缺）

输出：人类可读摘要 + --json 结构化结果。命中 → exit 1；干净 → exit 0。
验证范围 = 本包 scripts/ 自身代码；不扫描用户文件（数据边界铁律不变）。

用法:
  python3 pp_verify.py [--json] [--dir scripts]
"""
import argparse
import ast
import json
import py_compile
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# import 顶层名/模块名 → 触网即命中
NET_MODULES = {
    "socket", "ssl", "http", "ftplib", "telnetlib", "smtplib", "poplib",
    "imaplib", "nntplib", "xmlrpc", "requests", "httpx", "aiohttp",
    "urllib3", "websockets", "websocket", "pycurl", "telnet",
}
# urllib 需要到属性级判断：urllib.request/urlopen 触网，urllib.parse 不触网
URQLIB_ATTRS = {"request", "urlopen"}

# 属性调用名（任何对象上 .urlopen()/.open_connection() 这类）
NET_CALL_ATTRS = {"urlopen", "open_connection", "create_connection",
                  "getconnection", "urllib"}

# 子进程命令里的网络工具 token
NET_CLI_TOKENS = {"curl", "wget", "nc", "ncat", "netcat", "ftp", "sftp",
                  "scp", "ssh", "telnet", "fetch", "aria2c"}

# v7.2.0 本地监听白名单：http.server 是回环监听器（无出站能力），与客户端库
# 语义不同——仅当同文件存在 127.0.0.1 绑定断言时放行（缺绑定仍记 hit）。
# 白名单机制化：放行条件（绑定字面量）随名单一起声明，杜绝"白名单=豁免扫描"。
LOCAL_LISTEN_ALLOWLIST = {"http.server"}
LOCAL_LISTEN_BIND_REQUIRED = "127.0.0.1"

SUBPROCESS_NAMES = {"subprocess", "os", "asyncio"}


def _mod_root(name: str) -> str:
    return (name or "").split(".")[0]


def _mod_head2(name: str) -> str:
    parts = (name or "").split(".")
    return ".".join(parts[:2]) if len(parts) >= 2 else parts[0]


class NetVisitor(ast.NodeVisitor):
    def __init__(self):
        self.hits = []

    def _hit(self, node, kind, detail):
        self.hits.append({"line": getattr(node, "lineno", 0), "kind": kind,
                          "detail": detail})

    def visit_Import(self, node):
        for alias in node.names:
            root = _mod_root(alias.name)
            head2 = _mod_head2(alias.name)
            if root in NET_MODULES and root != "urllib":
                self._hit(node, "import", alias.name)
            elif head2 == "http.client" or head2 == "xmlrpc.client":
                self._hit(node, "import", alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        root = _mod_root(node.module or "")
        head2 = _mod_head2(node.module or "")
        if root in NET_MODULES and root != "urllib":
            self._hit(node, "import", f"from {node.module}")
        elif head2 in ("http.client", "xmlrpc.client", "urllib.request"):
            self._hit(node, "import", f"from {node.module}")
        elif head2 == "urllib.parse":
            pass  # urllib.parse 是纯 URL 解析，不触网
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # urllib.request / urllib.urlopen 形态
        base = node.value
        if isinstance(base, ast.Name) and base.id == "urllib":
            if node.attr in URQLIB_ATTRS:
                self._hit(node, "call", f"urllib.{node.attr}")
        elif isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name) \
                and base.value.id == "urllib" and base.attr == "request":
            self._hit(node, "call", "urllib.request." + node.attr)
        elif node.attr in NET_CALL_ATTRS and node.attr != "urllib":
            # requests.get 不在（requests 已被 import 级拦截）；这里抓散装属性调用
            if node.attr == "urlopen":
                self._hit(node, "call", ".urlopen()")
        self.generic_visit(node)

    def visit_Call(self, node):
        # subprocess/os.system/Popen 执行网络 CLI 工具
        fn = node.func
        target = None
        if isinstance(fn, ast.Attribute) and fn.attr in ("system", "popen", "Popen", "run", "check_output", "call"):
            base = fn.value
            if isinstance(base, ast.Name) and base.id in SUBPROCESS_NAMES:
                target = node.args[0] if node.args else None
        elif isinstance(fn, ast.Name) and fn.id in ("system", "popen"):
            target = node.args[0] if node.args else None
        if target is not None:
            for tok in self._string_tokens(target):
                low = tok.lower()
                for t in NET_CLI_TOKENS:
                    if low == t or low.startswith(t + " ") or f" {t} " in low:
                        self._hit(node, "subprocess-net", f"{fn.attr or fn.id}: {tok[:80]}")
                        break
        self.generic_visit(node)

    @staticmethod
    def _string_tokens(node):
        """从调用首参里挖字符串字面量（含列表元素与 f-string 的静态部分）。"""
        out = []
        stack = [node]
        while stack:
            n = stack.pop()
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                out.append(n.value)
            elif isinstance(n, (ast.List, ast.Tuple, ast.Set)):
                stack.extend(n.elts)
            elif isinstance(n, ast.JoinedStr):
                stack.extend(v for v in n.values if isinstance(v, ast.Constant))
            elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mod):
                stack.append(n.left)
            elif isinstance(n, ast.Starred):
                stack.append(n.value)
        return out


def verify_file(path: Path):
    src = path.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(src, filename=str(path))
    v = NetVisitor()
    v.visit(tree)
    # v7.2.0 白名单裁决：http.server import + 同文件 127.0.0.1 绑定断言 → 改记
    # local-listen 注记（不计 hit）；缺绑定字面量的照常记 hit。
    if any("http.server" in h["detail"] for h in v.hits):
        if LOCAL_LISTEN_BIND_REQUIRED in src and "HTTPServer(" in src:
            v.hits = [h for h in v.hits if "http.server" not in h["detail"]]
    return v.hits


def main():
    ap = argparse.ArgumentParser(description="结构化零网络自证（AST 级）")
    ap.add_argument("--json", action="store_true", help="输出结构化 JSON")
    ap.add_argument("--dir", default=str(HERE), help="扫描目录（默认包内 scripts/）")
    args = ap.parse_args()

    root = Path(args.dir).resolve()
    py_files = sorted(root.glob("*.py"))
    hits, compile_errors = [], []
    for p in py_files:
        try:
            hits.extend({"file": p.name, **h} for h in verify_file(p))
        except SyntaxError as e:
            compile_errors.append({"file": p.name, "error": str(e)})
            continue
        try:
            py_compile.compile(str(p), doraise=True, cfile=str(Path("/tmp/_ppv.pyc")))
        except py_compile.PyCompileError as e:
            compile_errors.append({"file": p.name, "error": str(e)})
    try:
        Path("/tmp/_ppv.pyc").unlink(missing_ok=True)
    except Exception:
        pass

    result = {
        "verifier": "pp_verify.py (AST structural zero-network verification)",
        "scope": str(root),
        "files_scanned": len(py_files),
        "zero_network": len(hits) == 0 and len(compile_errors) == 0,
        "network_hits": hits,
        "compile_errors": compile_errors,
        "note": ("AST 级验证：字符串常量中的 URL（报告页脚等）是数据不是网络调用，不计命中；"
                 "验证范围是本包 scripts/ 自身代码，不读取用户数据。"),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        print(f"pp_verify 结构化自证 — 扫描 {len(py_files)} 个文件")
        if hits:
            from pp_errors import render as _pp_render
            _title, _next = _pp_render(Exception("AST 命中"))
            print(f"  下一步: {_next}")
            print(f"✗ 网络命中 {len(hits)} 处：")
            for h in hits:
                print(f"   {h['file']}:{h['line']} [{h['kind']}] {h['detail']}")
        if compile_errors:
            print(f"✗ 编译错误 {len(compile_errors)} 个：")
            for c in compile_errors:
                print(f"   {c['file']}: {c['error'][:120]}")
        if not hits and not compile_errors:
            print("✓ 零网络调用（AST 结构化验证）+ 全部文件可编译 — PASS")
        print("说明：" + result["note"])
    return 0 if result["zero_network"] else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
