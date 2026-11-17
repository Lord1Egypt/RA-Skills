#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标书流水线 v2 · 五段 DAG 接口（模块28，v5.5 新增）

对齐 multi-agent-orchestrator 模板 schema：
  顶层 pipeline_name / version / description / agents / state_store
  节点 id / name / role / type / inputs / outputs / depends_on / retry /
        timeout / fallback(skip|default|abort) / default_value / comment

五段 + 双人工检查点：
  章节拆分(task) -> 并行撰写(for-each) -> 人工检查点1(approval)
  -> 资质填充(task) -> 格式检查(task) -> 人工检查点2(approval)
  -> 合并审校(task)

用法：
  python dag_pipeline.py --list          列出节点与依赖
  python dag_pipeline.py --status        查看各段状态
  python dag_pipeline.py --interfaces    打印五段接口签名
  python dag_pipeline.py --run <node_id> 执行单段（演示模式，实际段由 agent 回调注入）

状态库：~/.workbuddy/output/gov_dag_state.db（可用 --state 覆盖）
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DAG_DEF = {
    "pipeline_name": "gov_bid_drafting_v2",
    "version": "2.0.0",
    "description": "标书流水线 v2：五段 DAG + 双人工检查点",
    "state_store": {"type": "sqlite", "path": "~/.workbuddy/output/gov_dag_state.db"},
    "agents": [
        {"id": "splitter", "role": "chapter-splitter"},
        {"id": "writer", "role": "chapter-writer", "concurrency": "hash-locked"},
        {"id": "qualification", "role": "qualification-filler"},
        {"id": "formatter", "role": "format-checker"},
        {"id": "reviewer", "role": "merge-reviewer"},
    ],
    "nodes": [
        {"id": "n1_split", "name": "章节拆分", "role": "chapter-splitter", "type": "task",
         "inputs": ["bidding_doc"], "outputs": ["chapter_list"], "depends_on": [],
         "retry": 2, "timeout": 300, "fallback": {"strategy": "abort"},
         "comment": "复用 25.1 collab_split 逻辑"},
        {"id": "n2_write", "name": "并行撰写", "role": "chapter-writer", "type": "for-each",
         "inputs": ["chapter_list"], "outputs": ["chapter_files"], "depends_on": ["n1_split"],
         "retry": 1, "timeout": 1800,
         "fallback": {"strategy": "skip", "default_value": "跳过该章节"},
         "comment": "章节级并行；文件哈希锁防并发覆盖（25.2）"},
        {"id": "n3_review1", "name": "人工检查点1", "role": "team-lead", "type": "approval",
         "inputs": ["chapter_files"], "outputs": ["approved_chapters"],
         "depends_on": ["n2_write"], "retry": 0, "timeout": 7200,
         "fallback": {"strategy": "abort"}, "comment": "确认分工与进度，未通过则回退 n2"},
        {"id": "n4_qual", "name": "资质填充", "role": "qualification-filler", "type": "task",
         "inputs": ["approved_chapters"], "outputs": ["qualified_doc"],
         "depends_on": ["n3_review1"], "retry": 2, "timeout": 600,
         "fallback": {"strategy": "default", "default_value": "手动录入"},
         "comment": "复用 16.7 资质匹配填充 + 素材库最新版（16.10 v5.5）"},
        {"id": "n5_format", "name": "格式检查", "role": "format-checker", "type": "task",
         "inputs": ["qualified_doc"], "outputs": ["format_report"],
         "depends_on": ["n4_qual"], "retry": 1, "timeout": 600,
         "fallback": {"strategy": "skip", "default_value": "清单式检查"},
         "comment": "复用 16.9 v5.5 的 10 项扫描，输出整改清单"},
        {"id": "n6_review2", "name": "人工检查点2", "role": "team-lead", "type": "approval",
         "inputs": ["qualified_doc", "format_report"], "outputs": ["final_confirm"],
         "depends_on": ["n5_format"], "retry": 0, "timeout": 3600,
         "fallback": {"strategy": "abort"},
         "comment": "合并前确认；format_report 有高风险项时提示先整改"},
        {"id": "n7_merge", "name": "合并审校", "role": "merge-reviewer", "type": "task",
         "inputs": ["final_confirm"], "outputs": ["merged_doc", "review_report"],
         "depends_on": ["n6_review2"], "retry": 1, "timeout": 900,
         "fallback": {"strategy": "abort"}, "comment": "复用 25.3 merge_review 全文一致性检查"},
    ],
}

DEFAULT_STATE = os.path.expanduser("~/.workbuddy/output/gov_dag_state.db")
LOCK_TIMEOUT = 1800  # 30 分钟


def resolve_state(path=None):
    p = path or DAG_DEF["state_store"]["path"]
    return os.path.expanduser(p)


def init_state(path=None):
    db = resolve_state(path)
    os.makedirs(os.path.dirname(db), exist_ok=True)
    conn = sqlite3.connect(db)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS dag_nodes (
               node_id TEXT PRIMARY KEY,
               status TEXT DEFAULT 'pending',
               attempts INTEGER DEFAULT 0,
               updated_at TEXT,
               message TEXT
           )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS dag_locks (
               lock_key TEXT PRIMARY KEY,
               token TEXT,
               expire_at INTEGER
           )"""
    )
    conn.commit()
    return conn


def get_status(path=None):
    conn = init_state(path)
    rows = conn.execute(
        "SELECT node_id, status, attempts, updated_at, message FROM dag_nodes ORDER BY node_id"
    ).fetchall()
    conn.close()
    return rows


def set_status(node_id, status, message="", path=None, incr=False):
    conn = init_state(path)
    conn.execute(
        """INSERT INTO dag_nodes(node_id, status, attempts, updated_at, message)
           VALUES(?,?,?,datetime('now'),?)
           ON CONFLICT(node_id) DO UPDATE SET
             status=excluded.status,
             attempts=dag_nodes.attempts + (CASE WHEN ? THEN 1 ELSE 0 END),
             updated_at=datetime('now'),
             message=excluded.message""",
        (node_id, status, 0, message, 1 if incr else 0),
    )
    conn.commit()
    conn.close()


def topological_order(nodes):
    by_id = {n["id"]: n for n in nodes}
    visited, order = set(), []

    def visit(nid):
        if nid in visited:
            return
        visited.add(nid)
        for dep in by_id[nid].get("depends_on", []):
            if dep in by_id:
                visit(dep)
        order.append(nid)

    for n in nodes:
        visit(n["id"])
    return order


def default_concurrency():
    """并行章节数 = min(CPU 逻辑核心 - 2, 4)，死规则10 硬件自适应。"""
    try:
        import psutil

        cpu = psutil.cpu_count(logical=True) or 4
    except Exception:
        cpu = 4
    return max(1, min(cpu - 2, 4))


def acquire_lock(key, token, path=None):
    conn = init_state(path)
    now = int(time.time())
    row = conn.execute("SELECT token, expire_at FROM dag_locks WHERE lock_key=?", (key,)).fetchone()
    if row and row[1] > now and row[0] != token:
        conn.close()
        return False
    conn.execute(
        """INSERT INTO dag_locks(lock_key, token, expire_at) VALUES(?,?,?)
           ON CONFLICT(lock_key) DO UPDATE SET token=excluded.token, expire_at=excluded.expire_at""",
        (key, token, now + LOCK_TIMEOUT),
    )
    conn.commit()
    conn.close()
    return True


def release_lock(key, path=None):
    conn = init_state(path)
    conn.execute("DELETE FROM dag_locks WHERE lock_key=?", (key,))
    conn.commit()
    conn.close()


def run_node(node_id, callback=None, context=None, path=None):
    """执行单段。callback(ctx, node) -> dict；approval 节点需 callback 返回 approved/rejected。"""
    node = next((n for n in DAG_DEF["nodes"] if n["id"] == node_id), None)
    if not node:
        raise SystemExit("未知节点：%s" % node_id)
    if node["type"] == "approval":
        set_status(node_id, "running", "等待人工确认", path, incr=True)
        if callback is None:
            set_status(node_id, "pending", "需在对话中确认", path)
            return {"node": node_id, "status": "pending", "need": "人工确认"}
        result = callback(context or {}, node)
        ok = bool(result.get("approved"))
        set_status(node_id, "approved" if ok else "rejected", result.get("message", ""), path)
        return {"node": node_id, "status": "approved" if ok else "rejected"}

    set_status(node_id, "running", "", path, incr=True)
    try:
        if callback is None:
            set_status(node_id, "done", "演示模式：无回调，仅登记状态", path)
            return {"node": node_id, "status": "done", "demo": True}
        out = callback(context or {}, node)
        set_status(node_id, "done", json.dumps(out, ensure_ascii=False)[:500], path)
        return {"node": node_id, "status": "done", "output": out}
    except Exception as exc:  # noqa: BLE001
        node = next(n for n in DAG_DEF["nodes"] if n["id"] == node_id)
        strategy = node.get("fallback", {}).get("strategy", "abort")
        if strategy == "skip":
            set_status(node_id, "skipped", str(exc), path)
            return {"node": node_id, "status": "skipped", "error": str(exc)}
        if strategy == "default":
            set_status(node_id, "done", "降级默认值：%s" % node.get("fallback", {}).get("default_value"), path)
            return {"node": node_id, "status": "degraded", "default": node.get("fallback", {}).get("default_value")}
        set_status(node_id, "failed", str(exc), path)
        return {"node": node_id, "status": "failed", "error": str(exc)}


INTERFACES = [
    "1. split(bidding_doc) -> chapter_list",
    "2. write_parallel(chapter_list) -> chapter_files",
    "3. check1(chapter_files) -> approved_chapters",
    "4. fill_qualification(approved_chapters) -> qualified_doc",
    "5. check_format(qualified_doc) -> format_report",
    "6. check2(qualified_doc, format_report) -> final_confirm",
    "7. merge_review(final_confirm) -> merged_doc + review_report",
]


def main():
    ap = argparse.ArgumentParser(description="标书流水线 v2 五段 DAG")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--interfaces", action="store_true")
    ap.add_argument("--run", metavar="NODE_ID")
    ap.add_argument("--state", help="覆盖状态库路径")
    ap.add_argument("--concurrency", type=int, default=None)
    args = ap.parse_args()

    if args.list:
        print("pipeline:", DAG_DEF["pipeline_name"], "v" + DAG_DEF["version"])
        for nid in topological_order(DAG_DEF["nodes"]):
            n = next(x for x in DAG_DEF["nodes"] if x["id"] == nid)
            deps = ",".join(n.get("depends_on", [])) or "-"
            print("  %-12s %-8s %-10s deps=%-10s timeout=%ss fallback=%s"
                  % (n["id"], n["name"], n["type"], deps, n.get("timeout"), n.get("fallback", {}).get("strategy")))
        return
    if args.status:
        for row in get_status(args.state):
            print("  %-12s %-10s attempts=%s %s %s" % (row[0], row[1], row[2], row[3] or "", row[4] or ""))
        return
    if args.interfaces:
        print("\n".join(INTERFACES))
        print("concurrency:", args.concurrency or default_concurrency())
        return
    if args.run:
        print(json.dumps(run_node(args.run, path=args.state), ensure_ascii=False, indent=2))
        return
    ap.print_help()


if __name__ == "__main__":
    main()
