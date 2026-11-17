#!/usr/bin/env python3
"""
Cost Bridge — 成本实测化桥接模块。
白名单检测 cn-llm-router，命中则子进程调用其成本报告命令（--json {start,end} 区间），
回填真实 token/cost 到节点 cost_data 列；未安装则保留估算值，加 `est` 前缀。
两个指标（估算/实测）在报告里分开显示。
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# 白名单：成本来源插件列表（按优先级排序）
COST_SOURCES = [
    {
        "name": "cn-llm-router",
        "detect_path": "~/.workbuddy/skills/cn-llm-router/SKILL.md",
        "cli_path": "~/.workbuddy/skills/cn-llm-router/scripts/cn_llm_router.py",
        "cost_args": ["cost-report", "--json"],
        "version_args": ["--version"]
    }
]

# 估算价格表（每 token ¥）
# 当 cn-llm-router 未安装时使用
ESTIMATED_PRICES = {
    "default": 0.0004,      # 通用默认
    "gpt-4": 0.03,
    "gpt-3.5-turbo": 0.002,
    "claude-3": 0.024,
    "deepseek-chat": 0.001,
    "qwen-turbo": 0.0008,
    "glm-4": 0.001,
    "glm-4-flash": 0.0001,
    "moonshot-v1": 0.012,
    "doubao": 0.0008,
    "spark-generalv3": 0.001,
    "baidu-ernie-4": 0.012,
    "openrouter/auto": 0.001,
    "unknown": 0.0004
}


def detect_cn_llm_router():
    """
    检测 cn-llm-router 是否可用。
    返回 (available: bool, cli_path: str|None, version: str|None)
    """
    for source in COST_SOURCES:
        if source["name"] != "cn-llm-router":
            continue
        cli = Path(os.path.expanduser(source["cli_path"]))
        if cli.exists():
            # 验证可执行性
            try:
                result = subprocess.run(
                    [sys.executable, str(cli)] + source["version_args"],
                    capture_output=True, text=True, timeout=10
                )
                version = None
                if result.returncode == 0:
                    version = result.stdout.strip().split("\n")[0]
                return True, str(cli), version
            except Exception:
                pass
        return False, None, None
    return False, None, None


def get_estimated_cost(node):
    """
    基于节点类型和输出长度估算成本（当 cn-llm-router 不可用时）。
    返回 dict {tokens, cost_rmb, model, est=True}
    """
    cost_data = node.get("cost_data", {})

    # 如果已有真实成本数据（来自 cn-llm-router 回填）
    if cost_data and not cost_data.get("est"):
        return cost_data

    # 检查节点是否有自定义价格
    node_model = node.get("config", {}).get("model", "default")
    node_pricing = node.get("config", {}).get("pricing_per_token")

    # 已提供的 cost_data 含 tokens 但 est=True → 用已有 tokens 更新价格
    if cost_data and "tokens" in cost_data:
        tokens = cost_data["tokens"]
        price = node_pricing or ESTIMATED_PRICES.get(node_model, ESTIMATED_PRICES["default"])
        return {
            "tokens": tokens,
            "cost_rmb": round(tokens * price, 6),
            "model": node_model,
            "est": True
        }

    # 无 cost_data → 根据输出长度估算
    output_data = node.get("output_data", {})
    output_str = json.dumps(output_data, ensure_ascii=False) if isinstance(output_data, dict) else str(output_data)
    # 粗略估算：中文约 1.5 token/字，英文约 0.3 token/字
    char_count = len(output_str)
    est_tokens = int(char_count * 1.2)
    price = node_pricing or ESTIMATED_PRICES.get(node_model, ESTIMATED_PRICES["default"])

    return {
        "tokens": est_tokens,
        "cost_rmb": round(est_tokens * price, 6),
        "model": node_model,
        "est": True
    }


def get_actual_cost(cli_path, run_id=None, start_time=None, end_time=None):
    """
    调用 cn-llm-router 的成本报告命令获取真实成本。
    返回 list of dict 或 None（失败时）
    """
    if not cli_path:
        return None

    args = [sys.executable, cli_path] + ["cost-report", "--json"]

    if run_id:
        args.extend(["--run-id", str(run_id)])

    if start_time:
        args.extend(["--start", start_time.strftime("%Y-%m-%dT%H:%M:%S")])

    if end_time:
        args.extend(["--end", end_time.strftime("%Y-%m-%dT%H:%M:%S")])

    try:
        result = subprocess.run(
            args, capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip())
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "records" in data:
                return data["records"]
            elif isinstance(data, dict):
                return [data]
    except Exception as e:
        pass

    return None


def backfill_node_costs(state, cli_path=None, router_version=None):
    """
    回填节点的真实成本。
    对于每个 cost_data 中 est=True 的节点，尝试从 cn-llm-router 获取实测值。
    返回更新的节点数。
    """
    updated = 0
    if not state or "nodes" not in state:
        return updated

    # 获取流水线的时间范围
    start_time = None
    end_time = None
    created_at = state.get("created_at")
    if created_at:
        try:
            start_time = datetime.fromisoformat(created_at.replace("Z", "+00:00").replace("+00:00", ""))
        except Exception:
            pass

    if state.get("status") in ("completed", "failed"):
        # 已完成 → 用当前时间作为结束
        end_time = datetime.now()
    else:
        end_time = datetime.now()

    # 尝试获取实测成本
    actual_costs = None
    if cli_path:
        actual_costs = get_actual_cost(
            cli_path,
            run_id=state.get("run_id"),
            start_time=start_time,
            end_time=end_time
        )

    if actual_costs:
        # 按节点名/model 匹配
        for record in actual_costs:
            node_id = record.get("node_id") or record.get("agent") or record.get("name", "")
            model = record.get("model", "unknown")
            tokens = record.get("tokens", 0)
            cost = record.get("cost_rmb") or record.get("cost", 0)

            if not node_id:
                continue

            # 查找匹配节点
            for aid, node in state["nodes"].items():
                if aid == node_id or node.get("name", "") == node_id:
                    old_cost = node.get("cost_data", {})
                    if old_cost.get("est", False):
                        # 只有估算值才覆盖
                        node["cost_data"] = {
                            "tokens": tokens,
                            "cost_rmb": round(float(cost), 6),
                            "model": model,
                            "est": False,  # 标记为实测
                            "source": "cn-llm-router",
                            "router_version": router_version
                        }
                        updated += 1
                    break

    return updated


def enrich_pipeline_costs(state_dir, pipeline_name=None):
    """
    主入口：扫描状态目录，对所有流水线回填成本。
    返回 {pipeline_file: updated_count} 的 dict。
    """
    results = {}
    state_path = Path(state_dir)
    if not state_path.exists():
        return results

    # 检测 cn-llm-router
    available, cli_path, version = detect_cn_llm_router()

    for state_file in sorted(state_path.glob("*.json")):
        if pipeline_name and pipeline_name not in state_file.name:
            continue

        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)

            updated = backfill_node_costs(state, cli_path, version)
            if updated > 0:
                # 写回（仅当有实测更新时）
                with open(state_file, "w", encoding="utf-8") as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)

            results[state_file.name] = {
                "updated": updated,
                "cost_source": "cn-llm-router" if available else "estimated_only",
                "router_version": version
            }

        except Exception as e:
            results[state_file.name] = {"error": str(e)}

    return results


def get_cost_summary(state):
    """
    获取成本汇总：分 est（估算）和 actual（实测）两组。
    返回 dict。
    """
    actual_tokens = 0
    actual_cost = 0.0
    est_tokens = 0
    est_cost = 0.0
    has_actual = False
    has_est = False

    for node in state.get("nodes", {}).values():
        cost = node.get("cost_data", {})
        if not cost:
            continue

        if cost.get("est", False):
            est_tokens += cost.get("tokens", 0)
            est_cost += cost.get("cost_rmb", 0)
            has_est = True
        else:
            actual_tokens += cost.get("tokens", 0)
            actual_cost += cost.get("cost_rmb", 0)
            has_actual = True

    # 优先显示实测，估算作为后备
    return {
        "actual_tokens": actual_tokens,
        "actual_cost_rmb": round(actual_cost, 6),
        "est_tokens": est_tokens,
        "est_cost_rmb": round(est_cost, 6),
        "has_actual": has_actual,
        "has_est": has_est,
        "total_tokens": actual_tokens + est_tokens,
        "total_cost_rmb": round(actual_cost + est_cost, 6)
    }


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description="成本桥接：回填实测成本")
    parser.add_argument("state_dir", help="状态文件目录")
    parser.add_argument("--pipeline", help="指定流水线名（可选）")
    parser.add_argument("--check", action="store_true", help="仅检测 cn-llm-router 是否可用")
    parser.add_argument("--summary", action="store_true", help="输出成本汇总")
    args = parser.parse_args()

    if args.check:
        available, cli_path, version = detect_cn_llm_router()
        if available:
            print(f"✅ cn-llm-router 已安装")
            print(f"   CLI: {cli_path}")
            print(f"   版本: {version or 'unknown'}")
        else:
            print(f"⚠️  cn-llm-router 未安装（使用估算价格）")
        sys.exit(0)

    if args.summary:
        # 汇总模式：读取单个状态文件
        state_file = Path(args.state_dir)
        if state_file.is_file():
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
            summary = get_cost_summary(state)
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print("请指定单个状态文件路径（--summary 模式）")
            sys.exit(1)
        return

    # 默认：回填成本
    results = enrich_pipeline_costs(args.state_dir, args.pipeline)
    if results:
        print(f"📊 成本回填完成：")
        for name, info in results.items():
            if "error" in info:
                print(f"   ❌ {name}: {info['error']}")
            else:
                src = info.get("cost_source", "unknown")
                ver = info.get("router_version", "")
                print(f"   ✅ {name}: {info['updated']} 节点更新 (来源: {src} {ver})")
    else:
        print("未找到任何状态文件")


if __name__ == "__main__":
    main()
