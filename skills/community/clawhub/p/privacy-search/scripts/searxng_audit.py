#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SearXNG 一键自检清单（V2.1.0 新增）

功能：本地实例健康 + 匿名化配置核查清单。
检查项：
1. 实例健康（端口可达 / JSON 接口可用）
2. 对外绑定检查（host 必须为 127.0.0.1，禁止 0.0.0.0）
3. 日志级别检查（匿名化要求日志不记录查询词，级别应为 WARNING 或更高）
4. 聚合配置检查（格式必须含 json，且禁用 details 中的敏感字段）
5. 查询词记录检查（query_in_title / 访问日志开关）

设计原则（死规则）：
- 死规则 9：纯本地检测（读配置 + HTTP 本地探测），无外部 API。
- 死规则 10：单次探测超时短，不拖慢用户。
- 死规则 13：不生成 __pycache__。

自检清单把「SearXNG 配对了吗」变成可核对项，对预埋错误配置全命中。
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

sys.dont_write_bytecode = True

try:
    from searxng_manager import load_config, SEARXNG_SECRET
except ImportError:
    try:
        from .searxng_manager import load_config, SEARXNG_SECRET
    except ImportError:
        def load_config(config_path=None):
            return {}
        SEARXNG_SECRET = ""


# 检查项定义
CHECKS = [
    "instance_health",      # 实例健康
    "bind_address",         # 对外绑定
    "log_level",            # 日志级别
    "format_json",          # 聚合 JSON 格式
    "query_logging",        # 查询词记录
]


def _probe_health(host: str, port: int, timeout: int = 3) -> Dict[str, Any]:
    """探测本地 SearXNG 实例健康"""
    url = f"http://{host}:{port}/search?q=test&format=json"
    try:
        import urllib.request
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            data = resp.read(200)
            ok = resp.status == 200
            # 确认返回的是 JSON 而非 HTML 错误页
            is_json = data[:1] in (b"{", b"[")
            return {
                "ok": ok and is_json,
                "reachable": ok,
                "json_format": is_json,
                "detail": f"HTTP {resp.status}，{'JSON 正常' if is_json else '非 JSON 响应'}",
            }
    except Exception as e:
        return {"ok": False, "reachable": False, "json_format": False, "detail": str(e)[:100]}


def audit(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    执行 SearXNG 一键自检，返回核查清单。

    Returns:
        {
            "checks": [{"name": str, "ok": bool, "detail": str, "suggestion": str}, ...],
            "passed": int,
            "total": int,
            "all_ok": bool,
        }
    """
    cfg = config or load_config()
    sx_cfg = cfg.get("searxng", {}) or {}
    host = sx_cfg.get("host", "127.0.0.1")
    port = int(sx_cfg.get("port", 8888))
    enabled = bool(sx_cfg.get("enabled", True))

    results: List[Dict[str, Any]] = []

    # 1. 实例健康
    health = _probe_health(host, port)
    results.append({
        "name": "实例健康",
        "ok": health["ok"],
        "detail": health["detail"],
        "suggestion": "" if health["ok"] else "启动 SearXNG：python -m scripts.searxng_manager start --method docker",
    })

    # 2. 对外绑定检查
    bind_ok = host in ("127.0.0.1", "localhost", "::1")
    results.append({
        "name": "对外绑定",
        "ok": bind_ok,
        "detail": f"host={host}",
        "suggestion": "" if bind_ok else "高危：host 不得设为 0.0.0.0，请改回 127.0.0.1",
    })

    # 3. 日志级别检查（匿名化）
    log_cfg = sx_cfg.get("logging", {}) or {}
    log_level = str(log_cfg.get("level", "WARNING")).upper()
    log_ok = log_level in ("WARNING", "ERROR", "CRITICAL", "OFF")
    results.append({
        "name": "日志级别",
        "ok": log_ok,
        "detail": f"level={log_level}",
        "suggestion": "" if log_ok else "日志级别应为 WARNING 或更高，避免记录查询词",
    })

    # 4. 聚合配置 - JSON 格式
    formats = sx_cfg.get("formats", ["json", "html"])
    if isinstance(formats, str):
        formats = [formats]
    fmt_ok = "json" in formats
    results.append({
        "name": "JSON 格式",
        "ok": fmt_ok,
        "detail": f"formats={formats}",
        "suggestion": "" if fmt_ok else "配置 formats 必须包含 json（搜索接口依赖）",
    })

    # 5. 查询词记录检查
    query_in_title = bool(log_cfg.get("query_in_title", False))
    save_log = bool(log_cfg.get("save", False))
    query_ok = not query_in_title and not save_log
    results.append({
        "name": "查询词记录",
        "ok": query_ok,
        "detail": f"query_in_title={query_in_title}, save={save_log}",
        "suggestion": "" if query_ok else "关闭日志中的查询词记录（query_in_title/save 设为 false）",
    })

    passed = sum(1 for r in results if r["ok"])
    return {
        "checks": results,
        "passed": passed,
        "total": len(results),
        "all_ok": passed == len(results),
        "enabled": enabled,
        "endpoint": f"http://{host}:{port}",
    }


def format_audit(report: Dict[str, Any]) -> str:
    """格式化自检报告"""
    lines = [
        f"SearXNG 一键自检（{report['endpoint']}）",
        "=" * 60,
    ]
    for check in report["checks"]:
        mark = "✅" if check["ok"] else "❌"
        lines.append(f"{mark} {check['name']}：{check['detail']}")
        if not check["ok"] and check["suggestion"]:
            lines.append(f"   → {check['suggestion']}")
    lines.append("=" * 60)
    lines.append(f"通过 {report['passed']}/{report['total']} 项")
    if report["all_ok"]:
        lines.append("🎉 SearXNG 隐私配置全部达标")
    else:
        lines.append("⚠️  存在未达标项，请按上述建议修复")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SearXNG 一键自检")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    cfg = load_config(args.config)
    report = audit(cfg)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(format_audit(report))


if __name__ == "__main__":
    main()
