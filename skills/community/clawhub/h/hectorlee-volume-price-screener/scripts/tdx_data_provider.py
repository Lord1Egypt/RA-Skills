#!/usr/bin/env python3
"""
TDX 数据适配器 V3.3
====================
通过本地 MCP 代理 (127.0.0.1:57400/mcp) 调用通达信接口，
补充科创板(688)和北交所(4/8/920)的 K 线和股票列表。

返回格式与 data_provider 兼容: [{date, open, close, high, low, volume}, ...]
"""

import json
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from mcp_utils import McpClient

STAR_PREFIXES = ("688",)
BJ_PREFIXES = ("4", "8", "920")


def _call_mcp(tool_name: str, arguments: dict) -> Optional[dict]:
    """调用 MCP 工具（通过 McpClient 共享实例）"""
    return McpClient.get().call_tool(tool_name, arguments)


def get_tdx_kline(code: str, setcode: str = "1", want_num: int = 90) -> Optional[List[dict]]:
    """获取单只股票日 K 线，返回 data_provider 兼容格式"""
    result = _call_mcp("tdx-connector_tdx_kline", {
        "code": code, "setcode": setcode, "period": "4", "wantNum": want_num,
    })
    if not result:
        return None

    rows = result.get("Rows")
    if not rows:
        return None

    klines = []
    for row in rows:
        try:
            klines.append({
                "date": row.get("Data", ""),
                "open": float(row.get("Open", 0)),
                "high": float(row.get("High", 0)),
                "low": float(row.get("Low", 0)),
                "close": float(row.get("Close", 0)),
                "volume": float(row.get("Volume", 0)),
            })
        except (ValueError, TypeError):
            continue
    return klines if klines else None


def fetch_tdx_klines_batch(codes: List[str], count: int = 90, workers: int = 5,
                           setcode: str = "1") -> Dict[str, Optional[List[dict]]]:
    """批量获取 K 线（并发）"""
    results = {}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(get_tdx_kline, c, setcode, count): c for c in codes}
        for future in as_completed(futures):
            code = futures[future]
            try:
                results[code] = future.result()
            except Exception:
                results[code] = None
    return results


if __name__ == "__main__":
    print("TDX 适配器初始化中...")
    if McpClient.get().init():
        print("MCP 连接成功 ✓")
        print("测试 中芯国际(688981)...")
        kl = get_tdx_kline("688981", setcode="1", want_num=5)
        if kl:
            print(f"  ✓ 获取 {len(kl)} 根K线")
            print(f"  最新: {kl[-1]['date']} close={kl[-1]['close']} vol={kl[-1]['volume']:.0f}")
        else:
            print("  ✗ K线获取失败")
    else:
        print("MCP 连接失败 ✗")
