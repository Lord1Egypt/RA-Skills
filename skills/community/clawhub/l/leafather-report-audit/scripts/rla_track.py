#!/usr/bin/env python3
"""rla_track.py — 运行时录像：不改业务代码，记录它跑过的每一条 SQL。

用法：
    python3 scripts/rla_track.py --ledger ledger.json -- python3 build_report.py [参数...]
    python3 scripts/rla_track.py --ledger ledger.json --trace-only -- python3 build_report.py

    同样能录 Node 出的报告（2026-10-25 起）：
    python3 scripts/rla_track.py --ledger ledger.json -- node build_report.mjs

做的事：
    1. Python 业务：生成一个 sitecustomize.py 注入子进程（Python 启动自动加载）
       Node 业务：用 NODE_OPTIONS=--require 注入 rla_track_node.cjs（Node 启动自动加载）
       两者可同时注入——谁跑谁录，互不干扰
    2. 钩子只**记录 SQL**，绝不碰结果（碰了会吃掉业务数据 —— 实测踩过）
    3. 子进程跑完，把 SQL 日志落成 .jsonl，供 rla_collect.py 复算成账本

为什么用 sitecustomize / --require：
    业务代码一行不用改，怎么启动都行。审计对它是隐身的。

⚠️ Node 侧录像的两个前提（不满足会「装上了但一条没录到」，静默）：
    * 业务所在项目要能解析到 @duckdb/node-api（装在该项目 node_modules 下，
      或用 RLA_NODE_MODULES 指定）；目前只支持 duckdb，pg/mysql 走 --command。
    * 技能目录路径不要带空格（NODE_OPTIONS 不解析引号）。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HOOK_SOURCE = r'''
"""自动注入的审计钩子：只记录 SQL，不改任何业务行为。"""
import json as _json
import os as _os
import threading as _threading
import traceback as _traceback

_LOG = _os.environ.get("RLA_TRACE")
_LOCK = _threading.Lock()


def _emit(kind, sql, extra=None):
    if not _LOG:
        return
    try:
        frame = _traceback.extract_stack()[-4]
        rec = {
            "ts": __import__("time").time(),
            "kind": kind,
            "sql": str(sql),
            "file": frame.filename,
            "line": frame.lineno,
        }
        if extra:
            rec.update(extra)
        line = _json.dumps(rec, ensure_ascii=False)
        with _LOCK:
            with open(_LOG, "a", encoding="utf-8") as f:
                f.write(line + "\n")
    except Exception:
        pass  # 审计自己出错，绝不打扰业务


def _wrap_sql(fn, kind):
    def wrapper(query, *args, **kwargs):
        _emit(kind, query)
        return fn(query, *args, **kwargs)      # 先记后跑，返回值原样透传
    wrapper.__name__ = getattr(fn, "__name__", "wrapped")
    return wrapper


def _install():
    try:
        import duckdb
        if hasattr(duckdb, "sql"):
            duckdb.sql = _wrap_sql(duckdb.sql, "duckdb.sql")
        conn_cls = getattr(duckdb, "DuckDBPyConnection", None)
        if conn_cls is not None and hasattr(conn_cls, "execute"):
            _orig = conn_cls.execute

            def _exec(self, query, *a, **k):
                _emit("duckdb.execute", query)
                return _orig(self, query, *a, **k)
            conn_cls.execute = _exec
    except Exception:
        pass

    try:
        import sqlite3
        _orig_sq = sqlite3.Connection.execute

        def _sq(self, sql, *a, **k):
            _emit("sqlite3.execute", sql)
            return _orig_sq(self, sql, *a, **k)
        sqlite3.Connection.execute = _sq
    except Exception:
        pass

    try:
        import pandas as pd
        if hasattr(pd, "read_sql"):
            _orig_rs = pd.read_sql

            def _rs(sql, con, *a, **k):
                _emit("pandas.read_sql", sql)
                return _orig_rs(sql, con, *a, **k)
            pd.read_sql = _rs
        for name in ("read_parquet", "read_csv", "read_excel"):
            if hasattr(pd, name):
                _orig_r = getattr(pd, name)

                def _mk(orig, nm):
                    def _r(path, *a, **k):
                        _emit("pandas." + nm, str(path))
                        return orig(path, *a, **k)
                    return _r
                setattr(pd, name, _mk(_orig_r, name))
    except Exception:
        pass


_install()
'''


def main() -> int:
    ap = argparse.ArgumentParser(description="运行时录像：记录业务脚本跑过的 SQL")
    ap.add_argument("--ledger", required=True, help="输出账本 JSON 路径")
    ap.add_argument("--trace-only", action="store_true", help="只录像，不生成账本")
    ap.add_argument("--mount", action="append", default=[], help='"视图名=路径"，复算时挂数据源，可重复')
    ap.add_argument("--report-name", default="未命名报告")
    ap.add_argument("--report-files", default="", help="报告文件，逗号分隔")
    ap.add_argument("--data-as-of", default="")
    ap.add_argument("--agent", default="")
    ap.add_argument("--metrics", default=None, help="metrics.yaml（可选，给数字贴稳定身份）")
    ap.add_argument("cmd", nargs=argparse.REMAINDER, help="-- 之后是真正要跑的命令")
    args = ap.parse_args()

    cmd = [c for c in args.cmd if c != "--"]
    if not cmd:
        print("❌ 用法：rla_track.py --ledger l.json -- python3 build_report.py", file=sys.stderr)
        return 2

    ledger_path = Path(args.ledger).expanduser().resolve()
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    trace_path = ledger_path.with_suffix(".trace.jsonl")
    if trace_path.exists():
        trace_path.unlink()

    hook_dir = Path(tempfile.mkdtemp(prefix="rla_hook_"))
    (hook_dir / "sitecustomize.py").write_text(HOOK_SOURCE, encoding="utf-8")

    env = dict(os.environ)
    # PYTHONPATH 里既有钩子目录（sitecustomize），也有技能 scripts 目录 ——
    # 后者是为了让业务脚本能 `from rla_note import note`（非 SQL 数字登记）
    _skill_scripts = str(Path(__file__).resolve().parent)
    env["PYTHONPATH"] = os.pathsep.join(
        [str(hook_dir), _skill_scripts]
        + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else []))
    env["RLA_TRACE"] = str(trace_path)
    env["RLA_LEDGER"] = str(ledger_path)
    # 非 SQL 数字的登记缓冲区（rla_note.note() 往这里追加）。
    # 每次跑之前清空，避免上一轮的残留混进本次账本。
    notes_path = ledger_path.with_suffix(".notes.jsonl")
    if notes_path.exists():
        notes_path.unlink()
    env["RLA_NOTES"] = str(notes_path)

    # Node 录像：--require 注入（Node 侧没有 sitecustomize 的等价物）。
    # 与 Python 钩子并存无害——Python 钩子只在 Python 进程生效，Node 钩子只在 Node 进程生效。
    node_hook = Path(__file__).resolve().parent / "rla_track_node.cjs"
    if node_hook.exists():
        if " " in str(node_hook):
            print("[rla_track] ⚠️ 技能目录路径含空格，NODE_OPTIONS 无法解析，"
                  "Node 报告不会被录像（Python 报告不受影响）", file=sys.stderr)
        else:
            prev = env.get("NODE_OPTIONS", "").strip()
            env["NODE_OPTIONS"] = f"--require {node_hook}" + (f" {prev}" if prev else "")
            env["RLA_TRACE_NODE"] = str(trace_path)

    print(f"[rla_track] 开始录像 → {trace_path.name}", file=sys.stderr)
    print(f"[rla_track] 业务命令：{' '.join(cmd)}", file=sys.stderr)
    t0 = time.time()

    try:
        proc = subprocess.run(cmd, env=env)
    finally:
        shutil.rmtree(hook_dir, ignore_errors=True)

    n = 0
    if trace_path.exists():
        n = sum(1 for _ in trace_path.open(encoding="utf-8"))
    n_note = 0
    if notes_path.exists():
        n_note = sum(1 for _ in notes_path.open(encoding="utf-8"))
    print(f"[rla_track] 录像结束：{n} 条查询记录"
          + (f"｜note 登记 {n_note} 条" if n_note else "")
          + f"｜耗时 {time.time() - t0:.1f}s", file=sys.stderr)

    if proc.returncode != 0:
        print(f"[rla_track] ⚠️ 业务命令退出码 {proc.returncode}，录像仍保留", file=sys.stderr)
        return proc.returncode

    if args.trace_only:
        return 0

    # 自动接上采集器：把 SQL 日志变成账本
    here = Path(__file__).resolve().parent
    collect = here / "rla_collect.py"
    if not collect.exists():
        print("[rla_track] 未找到 rla_collect.py，仅留下 trace 文件", file=sys.stderr)
        return 0
    r = subprocess.run([sys.executable, str(collect),
                        "--trace", str(trace_path), "--ledger", str(ledger_path),
                        "--report-name", args.report_name,
                        "--report-files", args.report_files,
                        "--data-as-of", args.data_as_of,
                        "--agent", args.agent,
                        *(["--metrics", args.metrics] if args.metrics else []),
                        *sum([["--mount", m] for m in args.mount], [])])
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
