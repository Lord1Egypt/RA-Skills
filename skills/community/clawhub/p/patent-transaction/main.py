#!/usr/bin/env python3
"""专利交易 Skill — mchat / CLI 双入口"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Any, Type

_SKILL_DIR = Path(__file__).resolve().parent
_TradeAPI: Type[Any] | None = None


def _get_trade_api_class() -> Type[Any]:
    """mchat 将 main.py 注册为 skill_patent-transaction，不能直接 import trade_api。"""
    global _TradeAPI
    if _TradeAPI is not None:
        return _TradeAPI
    path = _SKILL_DIR / "trade_api.py"
    spec = importlib.util.spec_from_file_location(
        "skill_trade_api_patent_transaction", path
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载 {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _TradeAPI = mod.TradeAPI
    return _TradeAPI


def _execute(command: str, api: Any, **kwargs: Any) -> Any:
    cmd = (command or "search").lower()
    query = kwargs.get("query") or ""
    patent_id = kwargs.get("patent_id") or kwargs.get("an") or ""
    page = int(kwargs.get("page") or 1)
    page_size = int(kwargs.get("page_size") or kwargs.get("pageSize") or 10)

    if cmd == "info":
        r = api._make_request("open")
        return r.get("data", r)
    if cmd == "search":
        r = api.search_products(query, page, page_size)
        return api.format_search_result(r)
    if cmd == "export":
        return api.export_search_excel(query, page, page_size)
    if cmd == "export_orders":
        return api.export_orders_excel(page, page_size)
    if cmd == "detail":
        if not patent_id:
            return "❌ 请提供 patent_id（申请号）"
        return api.get_product_detail(patent_id)
    if cmd == "sellers":
        if not patent_id:
            return "❌ 请提供 patent_id（申请号）"
        return api.get_product_sellers(patent_id)
    if cmd == "orders":
        return api.list_orders(page, page_size)
    if cmd == "open":
        return api.search_open_patent(query, page, page_size)
    if cmd == "demand":
        return api.search_demand(query, page, page_size)
    return {
        "error": (
            f"未知命令: {cmd}，可用: search, export, export_orders, "
            "detail, sellers, orders, open, demand, info"
        )
    }


def run(
    command: str = "search",
    query: str | None = None,
    patent_id: str | None = None,
    page: int = 1,
    page_size: int = 10,
    **kwargs: Any,
) -> Any:
    """mchat 工具入口（勿使用 sys.exit）"""
    try:
        TradeAPI = _get_trade_api_class()
        api = TradeAPI()
        return _execute(
            command,
            api,
            query=query,
            patent_id=patent_id,
            page=page,
            page_size=page_size,
            **kwargs,
        )
    except ValueError as e:
        return {
            "error": str(e),
            "hint": "请在 mchat 管理后台为该技能配置 secrets: TRADE_API_TOKEN",
        }
    except Exception as e:
        return {"error": str(e)}


def main() -> int:
    parser = argparse.ArgumentParser(description="专利交易 Skill")
    sub = parser.add_subparsers(dest="cmd")

    s = sub.add_parser("search", help="搜索在售专利")
    s.add_argument("keyword", nargs="?", default="")
    s.add_argument("--page", type=int, default=1)
    s.add_argument("--page-size", type=int, default=10)

    d = sub.add_parser("detail", help="专利交易详情")
    d.add_argument("an", help="申请号")

    o = sub.add_parser("orders", help="成交记录")
    o.add_argument("--page", type=int, default=1)

    op = sub.add_parser("open", help="开放许可搜索")
    op.add_argument("keyword", nargs="?", default="")

    dm = sub.add_parser("demand", help="采购需求")
    dm.add_argument("keyword", nargs="?", default="")

    info = sub.add_parser("info", help="API 说明")
    info.set_defaults(cmd="info")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 1

    kw = {
        "search": {"command": "search", "query": getattr(args, "keyword", "")},
        "detail": {"command": "detail", "patent_id": args.an},
        "orders": {"command": "orders", "page": args.page},
        "open": {"command": "open", "query": getattr(args, "keyword", "")},
        "demand": {"command": "demand", "query": getattr(args, "keyword", "")},
        "info": {"command": "info"},
    }
    result = run(**kw.get(args.cmd, {"command": args.cmd}))
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
