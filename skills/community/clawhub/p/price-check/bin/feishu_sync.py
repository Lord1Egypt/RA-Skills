#!/usr/bin/env python3
"""price-check v0.3 飞书多维表格同步模块（opt-in）

通过 lark-cli 把每次查询的 best_deal + Top 3 候选写到飞书多维表格。
配置文件 ~/.openclaw/data/price-check/config.json:
    {
      "feishu_sync": {
        "enabled": true,
        "base_token": "...",
        "table_id": "...",
        "lark_cli_profile": null   // 可选 lark-cli profile name
      }
    }

写入失败 swallow（不影响主输出），日志走 stderr。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

CONFIG_PATH = Path.home() / ".openclaw" / "data" / "price-check" / "config.json"


def _warn(msg: str) -> None:
    print(f"[price-check.feishu] {msg}", file=sys.stderr)


def load_config() -> dict[str, Any]:
    """读 config.json，文件不存在返回默认配置（feishu 未启用）。"""
    if not CONFIG_PATH.exists():
        return {
            "version": "0.3.0",
            "feishu_sync": {"enabled": False},
        }
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        _warn(f"config load failed: {e}")
        return {"feishu_sync": {"enabled": False}}


def save_config(config: dict[str, Any]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


def _lark_cli(args: list[str], profile: Optional[str] = None, timeout: int = 15) -> tuple[bool, str]:
    """run lark-cli 命令。返回 (ok, stdout_or_err)。"""
    cmd = ["lark-cli"] + args
    if profile:
        cmd = ["lark-cli", "--profile", profile] + args
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False,
        )
        if result.returncode != 0:
            return False, result.stderr.strip() or result.stdout.strip()
        return True, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout}s"
    except FileNotFoundError:
        return False, "lark-cli not found in PATH"
    except Exception as e:
        return False, str(e)


def sync_query_to_feishu(query: str, result: dict[str, Any]) -> bool:
    """把一次查询的关键字段同步到飞书多维表格。返回是否成功。"""
    config = load_config()
    fs = config.get("feishu_sync") or {}
    if not fs.get("enabled"):
        return False

    base_token = fs.get("base_token")
    table_id = fs.get("table_id")
    profile = fs.get("lark_cli_profile")
    if not base_token or not table_id:
        _warn("feishu_sync.enabled=true but base_token / table_id 未配置；跑 setup_feishu.py 先")
        return False

    best_deal = result.get("best_deal") or {}
    stats = result.get("stats") or {}
    stats_raw = result.get("stats_raw") or {}

    # 抽 Top 3 安全候选（已去 outlier + flagged + low_relevance）
    flagged_ids = {i.get("goodsId") for i in (result.get("flagged_items") or [])}
    low_ids = {i.get("goodsId") for i in (result.get("low_relevance_items") or [])}
    removed_ids = {i.get("goodsId") for i in (result.get("removed_outliers") or [])}
    safe = [
        i for i in (result.get("all_platforms") or [])
        if i.get("goodsId") not in flagged_ids
        and i.get("goodsId") not in low_ids
        and i.get("goodsId") not in removed_ids
    ]
    safe.sort(key=lambda x: x.get("price", 0))
    top3 = safe[:3]

    def _url(item: dict[str, Any]) -> str:
        return (item.get("buy_url") or "") if item else ""

    def _label(item: dict[str, Any]) -> str:
        if not item:
            return ""
        return f"¥{item.get('price', 0)} {item.get('platform', '')} {item.get('shopName', '')}"

    rel = best_deal.get("relevance") or {}
    history = result.get("history_summary") or {}
    deal_hist = history.get("best_deal_history") or {}
    market_hist = history.get("market") or {}

    fields = {
        "查询词": query,
        "Verdict": result.get("verdict") or "",
        "Verdict依据": result.get("verdict_reason") or "",
        "best_deal价格": best_deal.get("price"),
        "best_deal平台": best_deal.get("platform") or "",
        "best_deal店铺": best_deal.get("shopName") or "",
        "best_deal标题": best_deal.get("title") or "",
        "best_deal搜索链接": best_deal.get("search_url") or "",
        "Top2标签": _label(top3[1]) if len(top3) > 1 else "",
        "Top2搜索链接": top3[1].get("search_url") if len(top3) > 1 and top3[1] else "",
        "Top3标签": _label(top3[2]) if len(top3) > 2 else "",
        "Top3搜索链接": top3[2].get("search_url") if len(top3) > 2 and top3[2] else "",
        "匹配度": rel.get("score"),
        "Condition": best_deal.get("condition") or "",
        "中位数": stats.get("median"),
        "最低价": stats.get("min"),
        "最高价": stats.get("max"),
        "原始条数": stats_raw.get("count"),
        "剔除数": len(result.get("removed_outliers") or []),
        "过滤数": len(result.get("flagged_items") or []),
        "不匹配数": len(result.get("low_relevance_items") or []),
        "Trap提示": result.get("trap_warning") or "",
        # v0.4 历史价字段
        "历史样本数": deal_hist.get("snapshots_count"),
        "历史最低": (deal_hist.get("low") or {}).get("price"),
        "历史最高": (deal_hist.get("high") or {}).get("price"),
        "历史均价": deal_hist.get("avg"),
        "当前位置": deal_hist.get("current_rank"),
        "市场30日中位": market_hist.get("stats_median_30d"),
        "当前/市场比": market_hist.get("current_vs_30d_median"),
    }
    # 删掉 None 值（lark-cli 不接受）
    fields = {k: v for k, v in fields.items() if v not in (None, "")}

    body = json.dumps(fields, ensure_ascii=False)
    ok, msg = _lark_cli(
        [
            "base", "+record-upsert",
            "--base-token", base_token,
            "--table-id", table_id,
            "--json", body,
        ],
        profile=profile,
        timeout=15,
    )
    if not ok:
        _warn(f"sync failed: {msg[:300]}")
    return ok
