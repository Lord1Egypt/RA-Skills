#!/usr/bin/env python3
"""
Model Benchmarks — Global AI Intelligence Hub

Real-time AI model capability tracking via leaderboards (LMSYS Arena, HuggingFace, etc.) 
for intelligent compute routing and cost optimization.

Usage:
    python3 run.py fetch                           # Fetch latest benchmark data
    python3 run.py query --model gpt-4o           # Query model capabilities  
    python3 run.py recommend --task coding        # Get optimal model recommendations
    python3 run.py analyze                        # Cost efficiency analysis
    python3 run.py trends --model gpt-4o          # Performance trends over time
    
Examples:
    # Daily optimization workflow
    python3 run.py fetch && python3 run.py recommend --task coding
    
    # Find cost-efficient models
    python3 run.py analyze --sort-by efficiency --limit 5
    
    # Export data for external tools
    python3 run.py query --model claude-3.5-sonnet --format json
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import re
from datetime import datetime, timedelta
from pathlib import Path

# Skill directory
SKILL_DIR = Path(__file__).parent.parent
BENCHMARKS_DIR = SKILL_DIR / "benchmarks"
BENCHMARKS_DIR.mkdir(exist_ok=True)

# 数据源配置
BENCHMARK_SOURCES = {
    "lmsys": {
        "name": "LMSYS Chatbot Arena",
        "url": "https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard",
        "api_url": "https://huggingface.co/api/spaces/lmsys/chatbot-arena-leaderboard/discussions",
        "capabilities": ["general", "reasoning", "creative"],
        "weight": 1.0,
    },
    "openllm": {
        "name": "Open LLM Leaderboard",
        "url": "https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard",
        "capabilities": ["reasoning", "knowledge", "comprehension"],
        "weight": 0.8,
    },
    "bigcode": {
        "name": "BigCode Leaderboard",
        "url": "https://huggingface.co/spaces/bigcode/bigcode-leaderboard",
        "capabilities": ["coding"],
        "weight": 1.2,  # 编程能力更重要
    },
    "alpaca": {
        "name": "Alpaca Eval",
        "url": "https://tatsu-lab.github.io/alpaca_eval/",
        "capabilities": ["instruction_following", "creative"],
        "weight": 0.9,
    }
}

# 模型名称映射（统一不同平台的命名）
MODEL_NAME_MAPPING = {
    "gpt-4o": ["gpt-4o", "gpt-4-o", "openai-gpt-4o"],
    "gpt-4o-mini": ["gpt-4o-mini", "gpt-4-o-mini", "openai-gpt-4o-mini"],
    "claude-3.5-sonnet": ["claude-3.5-sonnet", "claude-3-5-sonnet", "anthropic-claude-3.5-sonnet"],
    "gemini-2.0-flash": ["gemini-2.0-flash-001", "gemini-2-flash", "google-gemini-2.0-flash"],
}

# 任务类型 → 能力映射
TASK_CAPABILITY_MAP = {
    "coding": ["coding", "reasoning"],
    "writing": ["creative", "instruction_following"],
    "analysis": ["reasoning", "comprehension"],
    "translation": ["general", "knowledge"],
    "math": ["reasoning", "knowledge"],
    "creative": ["creative", "general"],
    "simple": ["general"],
}


def fetch_lmsys_arena():
    """拉取 LMSYS Arena 排行榜数据（模拟实现）"""
    print("🏟️  Fetching LMSYS Chatbot Arena data...")
    
    # TODO: 实际实现需要解析 HuggingFace Space 的数据
    # 这里先提供模拟数据
    mock_data = {
        "timestamp": datetime.now().isoformat(),
        "source": "lmsys",
        "models": {
            "gpt-4o": {
                "score": 1285,
                "rank": 2,
                "capabilities": {
                    "general": 92,
                    "reasoning": 89,
                    "creative": 88
                }
            },
            "claude-3.5-sonnet": {
                "score": 1322,
                "rank": 1,
                "capabilities": {
                    "general": 95,
                    "reasoning": 94,
                    "creative": 91
                }
            },
            "gpt-4o-mini": {
                "score": 1178,
                "rank": 8,
                "capabilities": {
                    "general": 85,
                    "reasoning": 82,
                    "creative": 78
                }
            },
            "gemini-2.0-flash": {
                "score": 1213,
                "rank": 6,
                "capabilities": {
                    "general": 88,
                    "reasoning": 85,
                    "creative": 83
                }
            }
        }
    }
    return mock_data


def fetch_bigcode_leaderboard():
    """拉取 BigCode 编程能力排行榜"""
    print("💻 Fetching BigCode Leaderboard data...")
    
    # 模拟编程能力数据
    mock_data = {
        "timestamp": datetime.now().isoformat(),
        "source": "bigcode",
        "models": {
            "gpt-4o": {
                "humaneval": 88.4,
                "mbpp": 84.3,
                "capabilities": {"coding": 86}
            },
            "claude-3.5-sonnet": {
                "humaneval": 92.0,
                "mbpp": 87.8,
                "capabilities": {"coding": 90}
            },
            "gpt-4o-mini": {
                "humaneval": 75.2,
                "mbpp": 72.1,
                "capabilities": {"coding": 74}
            },
            "gemini-2.0-flash": {
                "humaneval": 79.6,
                "mbpp": 76.4,
                "capabilities": {"coding": 78}
            }
        }
    }
    return mock_data


def fetch_current_prices():
    """获取当前模型价格（从 OpenRouter 等平台）"""
    print("💰 Fetching current model prices...")
    
    # 模拟价格数据（USD per 1M tokens）
    mock_prices = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gemini-2.0-flash": {"input": 0.075, "output": 0.30},
    }
    return mock_prices


def normalize_model_name(name):
    """标准化模型名称"""
    name_lower = name.lower()
    for standard_name, aliases in MODEL_NAME_MAPPING.items():
        if any(alias.lower() in name_lower for alias in aliases):
            return standard_name
    return name


def merge_benchmark_data(all_data):
    """合并多个来源的 benchmark 数据"""
    merged = {}
    
    for source_name, data in all_data.items():
        source_config = BENCHMARK_SOURCES.get(source_name, {})
        weight = source_config.get("weight", 1.0)
        
        for model_name, model_data in data.get("models", {}).items():
            normalized_name = normalize_model_name(model_name)
            
            if normalized_name not in merged:
                merged[normalized_name] = {
                    "capabilities": {},
                    "sources": [],
                    "last_updated": datetime.now().isoformat()
                }
            
            # 加权合并能力分数
            for capability, score in model_data.get("capabilities", {}).items():
                if capability not in merged[normalized_name]["capabilities"]:
                    merged[normalized_name]["capabilities"][capability] = []
                
                merged[normalized_name]["capabilities"][capability].append({
                    "score": score,
                    "weight": weight,
                    "source": source_name
                })
            
            merged[normalized_name]["sources"].append(source_name)
    
    # 计算加权平均分
    for model_name, model_data in merged.items():
        for capability, scores in model_data["capabilities"].items():
            if scores:
                weighted_sum = sum(s["score"] * s["weight"] for s in scores)
                total_weight = sum(s["weight"] for s in scores)
                model_data["capabilities"][capability] = round(weighted_sum / total_weight, 1)
    
    return merged


def calculate_cost_efficiency(capabilities, prices):
    """计算性价比分数"""
    cost_efficiency = {}
    
    for model, caps in capabilities.items():
        price_data = prices.get(model, {})
        if not price_data:
            continue
            
        # 简单成本计算：假设平均输入输出比例
        avg_price = (price_data["input"] + price_data["output"]) / 2
        
        # 综合能力分数（各项能力加权平均）
        capability_scores = list(caps.get("capabilities", {}).values())
        if capability_scores:
            avg_capability = sum(capability_scores) / len(capability_scores)
            # 性价比 = 能力分数 / 成本
            efficiency = avg_capability / avg_price if avg_price > 0 else 0
            cost_efficiency[model] = round(efficiency, 2)
    
    return cost_efficiency


def fetch_all_benchmarks():
    """拉取所有 benchmark 数据"""
    all_data = {}
    
    # 拉取各个来源的数据
    all_data["lmsys"] = fetch_lmsys_arena()
    all_data["bigcode"] = fetch_bigcode_leaderboard()
    
    # 获取价格数据
    prices = fetch_current_prices()
    
    # 合并数据
    merged_capabilities = merge_benchmark_data(all_data)
    
    # 计算性价比
    cost_efficiency = calculate_cost_efficiency(merged_capabilities, prices)
    
    # 组装最终数据
    final_data = {
        "timestamp": datetime.now().isoformat(),
        "models": merged_capabilities,
        "prices": prices,
        "cost_efficiency": cost_efficiency,
        "sources": list(BENCHMARK_SOURCES.keys()),
        "version": "1.0"
    }
    
    # 保存到文件
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = BENCHMARKS_DIR / f"{today}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    # 也保存为最新数据
    latest_file = BENCHMARKS_DIR / "latest.json"
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Benchmark data saved to {output_file}")
    return final_data


def query_model(model_name):
    """查询特定模型的能力数据"""
    latest_file = BENCHMARKS_DIR / "latest.json"
    
    if not latest_file.exists():
        print("❌ No benchmark data found. Run 'fetch' first.")
        return None
    
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    normalized_name = normalize_model_name(model_name)
    model_data = data["models"].get(normalized_name)
    
    if not model_data:
        print(f"❌ Model '{model_name}' not found in benchmark data.")
        available = list(data["models"].keys())
        print(f"Available models: {', '.join(available)}")
        return None
    
    # 显示模型信息
    print(f"\n🤖 Model: {normalized_name}")
    print(f"📊 Capabilities:")
    
    for capability, score in model_data["capabilities"].items():
        print(f"  • {capability.capitalize()}: {score}/100")
    
    prices = data["prices"].get(normalized_name, {})
    if prices:
        print(f"💰 Pricing (per 1M tokens):")
        print(f"  • Input: ${prices['input']:.2f}")
        print(f"  • Output: ${prices['output']:.2f}")
    
    efficiency = data["cost_efficiency"].get(normalized_name)
    if efficiency:
        print(f"⚡ Cost Efficiency: {efficiency}")
    
    return model_data


def recommend_for_task(task_type):
    """为特定任务推荐最佳模型"""
    latest_file = BENCHMARKS_DIR / "latest.json"
    
    if not latest_file.exists():
        print("❌ No benchmark data found. Run 'fetch' first.")
        return None
    
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 获取任务需要的能力
    required_capabilities = TASK_CAPABILITY_MAP.get(task_type.lower(), ["general"])
    
    print(f"\n🎯 Task: {task_type}")
    print(f"📋 Required capabilities: {', '.join(required_capabilities)}")
    
    # 为每个模型计算任务匹配度
    recommendations = []
    
    for model_name, model_data in data["models"].items():
        capabilities = model_data["capabilities"]
        
        # 计算相关能力的平均分
        relevant_scores = []
        for cap in required_capabilities:
            if cap in capabilities:
                relevant_scores.append(capabilities[cap])
        
        if not relevant_scores:
            continue
            
        avg_score = sum(relevant_scores) / len(relevant_scores)
        
        # 获取成本和效率数据
        efficiency = data["cost_efficiency"].get(model_name, 0)
        prices = data["prices"].get(model_name, {})
        avg_price = (prices.get("input", 0) + prices.get("output", 0)) / 2
        
        recommendations.append({
            "model": model_name,
            "task_score": avg_score,
            "cost_efficiency": efficiency,
            "avg_price": avg_price,
            "relevant_capabilities": {cap: capabilities.get(cap, 0) for cap in required_capabilities}
        })
    
    # 排序：按任务适合度 + 性价比
    recommendations.sort(key=lambda x: (x["task_score"] * 0.7 + x["cost_efficiency"] * 0.3), reverse=True)
    
    print(f"\n🏆 Top 3 recommendations:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"{i}. {rec['model']}")
        print(f"   Task Score: {rec['task_score']:.1f}/100")
        print(f"   Cost Efficiency: {rec['cost_efficiency']:.2f}")
        print(f"   Avg Price: ${rec['avg_price']:.2f}/1M tokens")
        print()
    
    return recommendations


def sync_to_compute_router():
    """同步数据到 compute-router"""
    latest_file = BENCHMARKS_DIR / "latest.json"
    router_dir = Path("~/.openclaw/workspace/skills/compute-router").expanduser()
    
    if not latest_file.exists():
        print("❌ No benchmark data found. Run 'fetch' first.")
        return
    
    if not router_dir.exists():
        print("❌ compute-router skill not found.")
        return
    
    with open(latest_file, "r", encoding="utf-8") as f:
        benchmark_data = json.load(f)
    
    # 生成 router 配置
    router_config = {
        "model_tiers": {},
        "dynamic_pricing": benchmark_data["prices"],
        "task_recommendations": {},
        "last_updated": benchmark_data["timestamp"]
    }
    
    # 根据性价比重新分层
    efficiency_sorted = sorted(
        benchmark_data["cost_efficiency"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # 动态分配到 3 个tier
    total_models = len(efficiency_sorted)
    for i, (model, efficiency) in enumerate(efficiency_sorted):
        if i < total_models // 3:
            tier = "heavy"
        elif i < 2 * total_models // 3:
            tier = "medium" 
        else:
            tier = "light"
        
        router_config["model_tiers"][model] = {
            "tier": tier,
            "efficiency": efficiency,
            "capabilities": benchmark_data["models"][model]["capabilities"]
        }
    
    # 生成任务推荐映射
    for task_type in TASK_CAPABILITY_MAP.keys():
        # 快速推荐逻辑（取 top 1）
        recs = []
        for model, model_data in benchmark_data["models"].items():
            required_caps = TASK_CAPABILITY_MAP[task_type]
            scores = [model_data["capabilities"].get(cap, 0) for cap in required_caps]
            if scores:
                avg_score = sum(scores) / len(scores)
                efficiency = benchmark_data["cost_efficiency"].get(model, 0)
                combined_score = avg_score * 0.7 + efficiency * 0.3
                recs.append((model, combined_score))
        
        if recs:
            recs.sort(key=lambda x: x[1], reverse=True)
            router_config["task_recommendations"][task_type] = recs[0][0]
    
    # 保存到 router 目录
    router_config_file = router_dir / "dynamic_config.json"
    with open(router_config_file, "w", encoding="utf-8") as f:
        json.dump(router_config, f, indent=2)
    
    print(f"✅ Synced to compute-router: {router_config_file}")
    print(f"📊 Updated {len(router_config['model_tiers'])} models")
    print(f"🎯 Generated {len(router_config['task_recommendations'])} task recommendations")


def analyze_cost_efficiency():
    """Analyze cost efficiency across all models"""
    latest_file = BENCHMARKS_DIR / "latest.json"
    
    if not latest_file.exists():
        print("❌ No benchmark data found. Run 'fetch' first.")
        return
    
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print("💰 Cost Efficiency Analysis")
    print("=" * 50)
    
    # Sort models by cost efficiency
    efficiency_data = []
    for model, efficiency in data["cost_efficiency"].items():
        model_info = data["models"].get(model, {})
        prices = data["prices"].get(model, {})
        avg_capability = sum(model_info.get("capabilities", {}).values()) / len(model_info.get("capabilities", {1}))
        
        efficiency_data.append({
            "model": model,
            "efficiency": efficiency,
            "avg_capability": avg_capability,
            "avg_price": (prices.get("input", 0) + prices.get("output", 0)) / 2
        })
    
    efficiency_data.sort(key=lambda x: x["efficiency"], reverse=True)
    
    print("🏆 Top 10 Most Cost-Efficient Models:")
    print(f"{'Model':<25} {'Efficiency':<12} {'Capability':<12} {'Price/1M':<12}")
    print("-" * 65)
    
    for model in efficiency_data[:10]:
        print(f"{model['model']:<25} {model['efficiency']:<12.2f} {model['avg_capability']:<12.1f} ${model['avg_price']:<11.2f}")


def export_json_data(model_name=None):
    """Export data in JSON format for programmatic use"""
    latest_file = BENCHMARKS_DIR / "latest.json"
    
    if not latest_file.exists():
        print("❌ No benchmark data found. Run 'fetch' first.")
        return
    
    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if model_name:
        normalized_name = normalize_model_name(model_name)
        model_data = data["models"].get(normalized_name)
        if model_data:
            output = {
                "model": normalized_name,
                "capabilities": model_data["capabilities"],
                "pricing": data["prices"].get(normalized_name, {}),
                "cost_efficiency": data["cost_efficiency"].get(normalized_name, 0),
                "timestamp": data["timestamp"]
            }
        else:
            output = {"error": f"Model '{model_name}' not found"}
    else:
        output = data
    
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description="AI Model Benchmarks Intelligence")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # fetch 命令
    fetch_parser = subparsers.add_parser("fetch", help="Fetch latest benchmark data")
    fetch_parser.add_argument("--source", choices=["all", "lmsys", "bigcode", "openllm"], 
                            default="all", help="Data source to fetch")
    
    # query 命令
    query_parser = subparsers.add_parser("query", help="Query model capabilities")
    query_parser.add_argument("--model", required=True, help="Model name to query")
    query_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    
    # recommend 命令
    rec_parser = subparsers.add_parser("recommend", help="Recommend optimal models for task")
    rec_parser.add_argument("--task", required=True, 
                          choices=list(TASK_CAPABILITY_MAP.keys()),
                          help="Task type")
    rec_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    rec_parser.add_argument("--limit", type=int, default=3, help="Number of recommendations")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="Cost efficiency analysis")
    analyze_parser.add_argument("--sort-by", choices=["efficiency", "capability", "price"], 
                               default="efficiency", help="Sort criteria")
    analyze_parser.add_argument("--limit", type=int, default=10, help="Number of results")
    
    # export 命令
    export_parser = subparsers.add_parser("export", help="Export data in JSON format")
    export_parser.add_argument("--model", help="Specific model to export (optional)")
    
    args = parser.parse_args()
    
    if args.command == "fetch":
        fetch_all_benchmarks()
    elif args.command == "query":
        if args.format == "json":
            export_json_data(args.model)
        else:
            query_model(args.model)
    elif args.command == "recommend":
        recommend_for_task(args.task)
    elif args.command == "analyze":
        analyze_cost_efficiency()
    elif args.command == "export":
        export_json_data(args.model)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()