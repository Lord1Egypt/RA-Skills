#!/usr/bin/env python3
"""
OpenViking CLI Wrapper — Agent 可直接调用的上下文操作工具。
支持 add / search / ls / tree / abstract / overview / read / info / commit / stats 命令。
每次操作自动追踪 token 消耗，展示分层加载相比全量加载的节省效果。
"""

import argparse
import glob
import json
import os
import sys
import textwrap
import time

STATS_FILE = os.path.expanduser("~/.openviking/session_stats.json")


# ─── Session Token Tracker ───────────────────────────────────────────

class SessionTracker:
    """追踪会话级 token 消耗：实际消耗 vs 全量加载假设值"""

    def __init__(self):
        self._data = self._load()

    def _load(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return self._empty()

    @staticmethod
    def _empty():
        return {
            "session_start": time.strftime("%Y-%m-%d %H:%M:%S"),
            "ops": [],
            "totals": {"actual": 0, "full_load": 0},
        }

    def _save(self):
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def record(self, op: str, uri: str, layer: str, actual: int, full_load: int):
        entry = {
            "time": time.strftime("%H:%M:%S"),
            "op": op,
            "uri": uri,
            "layer": layer,
            "actual_tokens": actual,
            "full_load_tokens": full_load,
            "saved_tokens": full_load - actual,
        }
        self._data["ops"].append(entry)
        self._data["totals"]["actual"] += actual
        self._data["totals"]["full_load"] += full_load
        self._save()
        return entry

    def reset(self):
        self._data = self._empty()
        self._save()

    @property
    def totals(self):
        return self._data["totals"]

    @property
    def ops(self):
        return self._data["ops"]

    @property
    def session_start(self):
        return self._data.get("session_start", "?")

    def print_summary_line(self):
        t = self.totals
        actual = t["actual"]
        full = t["full_load"]
        saved = full - actual
        if full > 0:
            pct = saved / full * 100
            print(f"\n📊 会话累计 | 实际: {actual:,} tokens | 全量: {full:,} tokens | 节省: {saved:,} ({pct:.1f}%)")
        else:
            print(f"\n📊 会话累计 | 实际: {actual:,} tokens")


tracker = SessionTracker()


# ─── Helpers ─────────────────────────────────────────────────────────

def _estimate_tokens(text):
    if not text:
        return 0
    cn_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    en_chars = len(text) - cn_chars
    return int(cn_chars * 1.0 + en_chars / 4.0)


def _get_full_load_tokens(client, uri):
    """获取资源 L2 全文 token 数，作为"全量加载"基准"""
    try:
        full_text = str(client.read(uri))
        return _estimate_tokens(full_text)
    except Exception:
        return 0


def get_client(path=None):
    try:
        import openviking as ov
    except ImportError:
        print("ERROR: openviking 未安装。运行: pip install openviking", file=sys.stderr)
        sys.exit(1)

    workspace = path or os.environ.get(
        "OPENVIKING_WORKSPACE",
        os.path.expanduser("~/openviking_workspace"),
    )
    client = ov.SyncOpenViking(path=workspace)
    client.initialize()
    return client


# ─── Commands ────────────────────────────────────────────────────────

def cmd_add(args):
    client = get_client()
    target = args.target

    if target.startswith("http://") or target.startswith("https://"):
        result = client.add_resource(path=target)
        print(f"已添加 URL: {target}")
        print(f"结果: {result}")
    elif os.path.isdir(target):
        pattern = os.path.join(target, "**", "*.*")
        files = glob.glob(pattern, recursive=True)
        added = 0
        for f in files:
            if os.path.isfile(f) and not f.startswith("."):
                try:
                    client.add_resource(path=f)
                    added += 1
                    print(f"  + {f}")
                except Exception as e:
                    print(f"  ! {f}: {e}", file=sys.stderr)
        print(f"\n共添加 {added} 个文件")
    elif os.path.isfile(target):
        result = client.add_resource(path=target)
        print(f"已添加文件: {target}")
        print(f"结果: {result}")
    else:
        print(f"ERROR: 路径不存在: {target}", file=sys.stderr)
        sys.exit(1)

    if args.wait:
        print("等待语义处理完成...")
        client.wait_processed()
        print("处理完成 ✓")

    client.close()


def cmd_search(args):
    client = get_client()
    results = client.find(args.query, limit=args.limit)

    if not results.resources:
        print("未找到匹配结果")
        client.close()
        return

    total_actual = 0
    total_full = 0

    print(f"找到 {len(results.resources)} 个结果:\n")
    for i, r in enumerate(results.resources, 1):
        score = f"{r.score:.4f}" if hasattr(r, "score") else "N/A"
        abstract_text = ""
        if hasattr(r, "abstract") and r.abstract:
            abstract_text = str(r.abstract)

        print(f"  {i}. [{score}] {r.uri}")
        if abstract_text:
            print(f"     {textwrap.shorten(abstract_text, width=80)}")

        actual = _estimate_tokens(abstract_text) if abstract_text else 0
        full = _get_full_load_tokens(client, r.uri)
        total_actual += actual
        total_full += full

        print(f"     [L0: {actual} tokens | 全量: {full} tokens]")
        print()

    tracker.record("search", args.query, "L0", total_actual, total_full)
    tracker.print_summary_line()
    client.close()


def cmd_ls(args):
    client = get_client()
    uri = args.uri or "viking://resources"
    result = client.ls(uri)
    print(f"目录: {uri}\n")
    if hasattr(result, "__iter__"):
        for item in result:
            print(f"  {item}")
    else:
        print(result)
    client.close()


def cmd_tree(args):
    client = get_client()
    uri = args.uri or "viking://resources"
    try:
        result = client.tree(uri, depth=args.level)
        print(result)
    except AttributeError:
        print(f"tree 命令需要 ov CLI 支持，尝试: ov tree {uri} -L {args.level}")
    client.close()


def cmd_abstract(args):
    client = get_client()
    result = client.abstract(args.uri)
    content = str(result)

    print(f"═══ L0 摘要 ({args.uri}) ═══\n")
    print(content)

    actual = _estimate_tokens(content)
    full = _get_full_load_tokens(client, args.uri)

    print(f"\n[L0: {actual} tokens | 全量: {full} tokens | 节省: {full - actual} tokens]")
    tracker.record("abstract", args.uri, "L0", actual, full)
    tracker.print_summary_line()
    client.close()


def cmd_overview(args):
    client = get_client()
    result = client.overview(args.uri)
    content = str(result)

    print(f"═══ L1 概览 ({args.uri}) ═══\n")
    print(content)

    actual = _estimate_tokens(content)
    full = _get_full_load_tokens(client, args.uri)

    print(f"\n[L1: {actual} tokens | 全量: {full} tokens | 节省: {full - actual} tokens]")
    tracker.record("overview", args.uri, "L1", actual, full)
    tracker.print_summary_line()
    client.close()


def cmd_read(args):
    client = get_client()
    result = client.read(args.uri)
    content = str(result)

    print(f"═══ L2 全文 ({args.uri}) ═══\n")
    if args.head:
        lines = content.splitlines()
        display = "\n".join(lines[: args.head])
        print(display)
        if len(lines) > args.head:
            print(f"\n... (截断，共 {len(lines)} 行)")
    else:
        print(content)

    actual = _estimate_tokens(content)

    print(f"\n[L2 全文: {actual} tokens — 此次为全量读取，无节省]")
    tracker.record("read", args.uri, "L2", actual, actual)
    tracker.print_summary_line()
    client.close()


def cmd_info(args):
    config_file = os.environ.get(
        "OPENVIKING_CONFIG_FILE",
        os.path.expanduser("~/.openviking/ov.conf"),
    )

    print("═══ OpenViking 状态 ═══\n")

    if os.path.exists(config_file):
        print(f"配置文件: {config_file} ✓")
        try:
            with open(config_file) as f:
                conf = json.load(f)
            vlm = conf.get("vlm", {})
            emb = conf.get("embedding", {}).get("dense", {})
            print(f"VLM:       {vlm.get('provider', '?')} / {vlm.get('model', '?')}")
            print(f"Embedding: {emb.get('provider', '?')} / {emb.get('model', '?')} (dim={emb.get('dimension', '?')})")
            print(f"Workspace: {conf.get('storage', {}).get('workspace', '?')}")
        except Exception as e:
            print(f"配置读取错误: {e}")
    else:
        print(f"配置文件: {config_file} ✗ (未找到)")

    print()
    try:
        client = get_client()
        print("OpenViking 连接: ✓")
        client.close()
    except Exception as e:
        print(f"OpenViking 连接: ✗ ({e})")

    try:
        import openviking
        print(f"版本: {openviking.__version__}")
    except Exception:
        pass


def cmd_commit(args):
    client = get_client()
    try:
        result = client.commit()
        print("记忆提取已触发")
        print(f"结果: {result}")
    except Exception as e:
        print(f"记忆提取失败: {e}", file=sys.stderr)
    client.close()


def cmd_stats(args):
    """展示当前会话的 token 消耗汇总"""
    ops = tracker.ops
    t = tracker.totals
    actual = t["actual"]
    full = t["full_load"]
    saved = full - actual

    print(f"═══ Token 消耗统计 ═══")
    print(f"  会话开始: {tracker.session_start}")
    print(f"  操作次数: {len(ops)}")
    print()

    if not ops:
        print("  暂无操作记录。使用 search/abstract/overview/read 后自动记录。")
        return

    print(f"  {'#':<4} {'时间':<10} {'操作':<10} {'层级':<5} {'实际':>8} {'全量':>8} {'节省':>8} {'URI'}")
    print(f"  {'─'*4} {'─'*10} {'─'*10} {'─'*5} {'─'*8} {'─'*8} {'─'*8} {'─'*30}")

    for i, op in enumerate(ops, 1):
        uri_short = op["uri"][:30] + "..." if len(op["uri"]) > 30 else op["uri"]
        print(
            f"  {i:<4} {op['time']:<10} {op['op']:<10} {op['layer']:<5} "
            f"{op['actual_tokens']:>8,} {op['full_load_tokens']:>8,} {op['saved_tokens']:>8,} {uri_short}"
        )

    print()
    print(f"  ┌─────────────────────────────────────┐")
    print(f"  │  全量加载 (传统方式): {full:>10,} tokens │")
    print(f"  │  实际消耗 (分层加载): {actual:>10,} tokens │")
    print(f"  │  节省 token 数量:     {saved:>10,} tokens │")
    if full > 0:
        pct = saved / full * 100
        print(f"  │  节省比例:            {pct:>9.1f}%        │")
    print(f"  └─────────────────────────────────────┘")

    if args.reset:
        tracker.reset()
        print("\n  ✓ 统计数据已重置")


# ─── Main ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="viking",
        description="OpenViking CLI Wrapper — Agent 上下文操作工具（含 token 追踪）",
    )
    sub = parser.add_subparsers(dest="command", help="可用命令")

    p_add = sub.add_parser("add", help="添加资源（文件/目录/URL）")
    p_add.add_argument("target", help="文件路径、目录路径或 URL")
    p_add.add_argument("--wait", action="store_true", help="等待语义处理完成")

    p_search = sub.add_parser("search", help="语义搜索")
    p_search.add_argument("query", help="搜索查询")
    p_search.add_argument("--limit", type=int, default=5, help="最大结果数")

    p_ls = sub.add_parser("ls", help="浏览资源目录")
    p_ls.add_argument("uri", nargs="?", help="viking:// URI")

    p_tree = sub.add_parser("tree", help="树形展示资源")
    p_tree.add_argument("uri", nargs="?", help="viking:// URI")
    p_tree.add_argument("-L", "--level", type=int, default=3, help="展示层级")

    p_abstract = sub.add_parser("abstract", help="读取 L0 摘要")
    p_abstract.add_argument("uri", help="viking:// URI")

    p_overview = sub.add_parser("overview", help="读取 L1 概览")
    p_overview.add_argument("uri", help="viking:// URI")

    p_read = sub.add_parser("read", help="读取 L2 全文")
    p_read.add_argument("uri", help="viking:// URI")
    p_read.add_argument("--head", type=int, help="只显示前 N 行")

    sub.add_parser("info", help="检查服务状态和配置")
    sub.add_parser("commit", help="提取当前会话记忆")

    p_stats = sub.add_parser("stats", help="查看 token 消耗统计")
    p_stats.add_argument("--reset", action="store_true", help="重置统计数据")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    handlers = {
        "add": cmd_add,
        "search": cmd_search,
        "ls": cmd_ls,
        "tree": cmd_tree,
        "abstract": cmd_abstract,
        "overview": cmd_overview,
        "read": cmd_read,
        "info": cmd_info,
        "commit": cmd_commit,
        "stats": cmd_stats,
    }

    handlers[args.command](args)


if __name__ == "__main__":
    main()
