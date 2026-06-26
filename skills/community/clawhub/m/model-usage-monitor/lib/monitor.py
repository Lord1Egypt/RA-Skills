#!/usr/bin/env python3
"""
Model Usage Monitor v2 - OpenClaw 模型使用监控与缓存分析
增强版：会话级明细 + 每小时趋势 + Opus 告警

约束：全部使用本地 Ollama，零 API 调用

Usage:
    python3 model_usage_monitor_v2.py --report daily
    python3 model_usage_monitor_v2.py --alert-check  # 检查告警条件
    python3 model_usage_monitor_v2.py --live
"""

import json
import re
import os
import sys
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

# 配置路径
WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
LOG_DIR = os.path.expanduser("~/.openclaw/logs")
SESSIONS_DIR = os.path.expanduser("~/.openclaw/agents/main/sessions")
SEMANTIC_LOG = os.path.join(WORKSPACE_DIR, ".lib", "semantic_check.log")
GATEWAY_LOG = os.path.join(LOG_DIR, "gateway.log")
ALERT_STATE_FILE = os.path.join(WORKSPACE_DIR, ".lib", ".model_monitor_alerts.json")

# 模型定价（每百万tokens，USD）
MODEL_PRICING = {
    "claude-haiku-4.5": {"input": 0.80, "output": 4.00, "cache_write": 1.00, "cache_read": 0.08},
    "claude-sonnet-4.6": {"input": 3.00, "output": 15.00, "cache_write": 3.75, "cache_read": 0.30},
    "claude-opus-4.6": {"input": 15.00, "output": 75.00, "cache_write": 18.75, "cache_read": 1.50},
    "gemini-2.5-flash": {"input": 0.15, "output": 0.60, "cache_write": 0.00, "cache_read": 0.00},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00, "cache_write": 0.00, "cache_read": 0.00},
    "gpt-5.1-codex-mini": {"input": 0.50, "output": 2.00, "cache_write": 0.00, "cache_read": 0.00},
    "gpt-5.3-codex": {"input": 2.00, "output": 8.00, "cache_write": 0.00, "cache_read": 0.00},
    "gpt-5.4": {"input": 5.00, "output": 20.00, "cache_write": 0.00, "cache_read": 0.00},
    "glm-4.7": {"input": 0.50, "output": 2.00, "cache_write": 0.00, "cache_read": 0.00},
    "glm-5": {"input": 2.00, "output": 8.00, "cache_write": 0.00, "cache_read": 0.00},
    "k2p5": {"input": 2.00, "output": 8.00, "cache_write": 0.00, "cache_read": 0.00},
}

# 模型池映射
POOL_MODELS = {
    "Highspeed": ["claude-haiku-4.5", "gemini-2.5-flash", "gpt-5.3-codex", "glm-4.7"],
    "Intelligence": ["claude-sonnet-4.6", "claude-opus-4.6", "glm-5"],
    "Humanities": ["claude-sonnet-4.6", "gemini-2.5-pro", "gpt-5.4"],
    "Agentic": ["claude-opus-4.6", "gpt-5.3-codex"],
}

# 告警阈值
ALERT_THRESHOLDS = {
    "opus_calls_per_hour": 5,      # Opus 每小时调用超过 5 次告警
    "opus_cost_per_hour": 0.50,    # Opus 每小时成本超过 $0.50 告警
    "total_cost_per_hour": 2.00,   # 总成本每小时超过 $2 告警
}


def parse_semantic_log(lines: int = 1000) -> Dict:
    """解析语义路由日志"""
    stats = {
        "total_requests": 0,
        "branch_distribution": defaultdict(int),
        "task_type_distribution": defaultdict(int),
        "pool_distribution": defaultdict(int),
        "grade_distribution": defaultdict(int),
        "avg_context_score": [],
        "skill_dispatch_count": 0,
        "dedup_blocked": 0,
        "circuit_blocked": 0,
        "hourly_distribution": defaultdict(lambda: defaultdict(int)),  # hour -> metric -> count
    }
    
    if not os.path.exists(SEMANTIC_LOG):
        return stats
    
    try:
        with open(SEMANTIC_LOG, 'r', encoding='utf-8', errors='ignore') as f:
            log_lines = f.readlines()[-lines:]
    except Exception as e:
        print(f"Warning: Cannot read semantic log: {e}", file=sys.stderr)
        return stats
    
    pattern = re.compile(
        r'\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})[^\]]*\]\s+(.+?)\s+\|\s+'
        r'(\w+)\s+'
        r'(\w+)\s+'
        r'([📊🔑🔍⚙️🛡️○])\s+'
        r'score=([\d.]+)\s+'
        r'grade=(\w+)'
        r'(?:\s+\|\s+skill_dispatch=(\w+))?'
        r'(?:\s+skill=([\w-]+))?'
        r'(?:\s+blocked=([\w-]+))?'
    )
    
    for line in log_lines:
        match = pattern.search(line)
        if match:
            timestamp_str, message, branch, task_type, icon, score, grade = match.groups()[:7]
            dispatch, skill, blocked = match.groups()[7:]
            
            stats["total_requests"] += 1
            stats["branch_distribution"][branch] += 1
            stats["task_type_distribution"][task_type] += 1
            stats["grade_distribution"][grade] += 1
            stats["avg_context_score"].append(float(score))
            
            if dispatch == "True":
                stats["skill_dispatch_count"] += 1
            if blocked == "dedup_window":
                stats["dedup_blocked"] += 1
            if blocked == "circuit_open":
                stats["circuit_blocked"] += 1
            
            # 按小时分布
            try:
                hour = timestamp_str[:13]  # 2026-03-10T08
                stats["hourly_distribution"][hour]["requests"] += 1
                stats["hourly_distribution"][hour][f"branch_{branch}"] += 1
                stats["hourly_distribution"][hour][f"task_{task_type}"] += 1
            except:
                pass
    
    if stats["avg_context_score"]:
        stats["avg_context_score"] = sum(stats["avg_context_score"]) / len(stats["avg_context_score"])
    else:
        stats["avg_context_score"] = 0.0
    
    return stats


def parse_gateway_log(lines: int = 2000) -> Dict:
    """解析 Gateway 日志获取模型切换和缓存事件"""
    stats = {
        "model_switches": defaultdict(int),
        "cache_fallbacks": 0,
        "session_models": defaultdict(set),
        "model_timeline": [],
        "hourly_model_usage": defaultdict(lambda: defaultdict(int)),  # hour -> model -> count
    }
    
    if not os.path.exists(GATEWAY_LOG):
        return stats
    
    try:
        with open(GATEWAY_LOG, 'r', encoding='utf-8', errors='ignore') as f:
            log_lines = f.readlines()[-lines:]
    except Exception as e:
        print(f"Warning: Cannot read gateway log: {e}", file=sys.stderr)
        return stats
    
    switch_pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.[\d]+Z\s+'
        r'\[gateway\].*?'
        r'(?:session model (?:reconciled|patched) to|reconcile skipped \(model unchanged: )\s+'
        r'(custom-llmapi-lovbrowser-com/|zai/|kimi-coding/)?'
        r'([\w/\-.]+)'
    )
    
    cache_pattern = re.compile(
        r'context fallback from cache \((\d+)\)\s+for\s+([\w:]+)'
    )
    
    for line in log_lines:
        match = switch_pattern.search(line)
        if match:
            timestamp, prefix, model = match.groups()
            full_model = f"{prefix or ''}{model}".strip('/')
            short_model = extract_model_name(full_model)
            
            stats["model_switches"][short_model] += 1
            stats["model_timeline"].append({
                "time": timestamp,
                "model": short_model,
            })
            
            # 按小时统计
            hour = timestamp[:13]
            stats["hourly_model_usage"][hour][short_model] += 1
        
        cache_match = cache_pattern.search(line)
        if cache_match:
            cache_ttl, session = cache_match.groups()
            stats["cache_fallbacks"] += 1
    
    return stats


def parse_session_files() -> Dict:
    """解析会话文件获取每个会话的模型使用明细"""
    session_stats = {}
    
    if not os.path.exists(SESSIONS_DIR):
        return session_stats
    
    try:
        session_files = [f for f in os.listdir(SESSIONS_DIR) if f.endswith('.jsonl')]
    except Exception:
        return session_stats
    
    for session_file in session_files[:20]:  # 只处理最近20个会话
        session_path = os.path.join(SESSIONS_DIR, session_file)
        session_key = session_file.replace('.jsonl', '')
        
        try:
            with open(session_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            msg_count = 0
            models_used = set()
            last_model = None
            
            for line in lines[-100:]:  # 只读最后100行
                try:
                    data = json.loads(line)
                    msg = data.get('message', {})
                    if msg.get('role') == 'assistant':
                        msg_count += 1
                        # 尝试从 metadata 提取模型
                        metadata = data.get('metadata', {})
                        model = metadata.get('model')
                        if model:
                            short = extract_model_name(model)
                            models_used.add(short)
                            last_model = short
                except:
                    continue
            
            if msg_count > 0:
                session_stats[session_key[:20]] = {
                    "message_count": msg_count,
                    "models_used": list(models_used),
                    "last_model": last_model,
                }
        except Exception:
            continue
    
    return session_stats


def extract_model_name(full_model: str) -> str:
    """从完整模型路径提取简称"""
    if "claude-" in full_model:
        match = re.search(r'claude-([\w-]+)', full_model)
        if match:
            return f"claude-{match.group(1)}"
    if "gemini-" in full_model:
        match = re.search(r'gemini-([\w-]+)', full_model)
        if match:
            return f"gemini-{match.group(1)}"
    if "gpt-" in full_model:
        match = re.search(r'gpt-([\w.-]+)', full_model)
        if match:
            return f"gpt-{match.group(1)}"
    if "glm-" in full_model:
        match = re.search(r'glm-([\w-]+)', full_model)
        if match:
            return f"glm-{match.group(1)}"
    if "k2p5" in full_model:
        return "k2p5"
    return full_model.split("/")[-1] if "/" in full_model else full_model


def estimate_model_usage(semantic_stats: Dict, gateway_stats: Dict) -> Dict:
    """估算各模型使用情况"""
    usage = defaultdict(lambda: {
        "estimated_calls": 0,
        "estimated_input_tokens": 0,
        "estimated_output_tokens": 0,
        "estimated_cost_usd": 0.0,
        "pools": set(),
    })
    
    for model, count in gateway_stats["model_switches"].items():
        usage[model]["estimated_calls"] = count
    
    total_requests = semantic_stats["total_requests"]
    if total_requests > 0:
        avg_input = 3000
        avg_output = 800
        
        for model in usage:
            calls = usage[model]["estimated_calls"]
            usage[model]["estimated_input_tokens"] = calls * avg_input
            usage[model]["estimated_output_tokens"] = calls * avg_output
            
            pricing = MODEL_PRICING.get(model, {"input": 1.0, "output": 3.0})
            input_cost = (calls * avg_input / 1_000_000) * pricing["input"]
            output_cost = (calls * avg_output / 1_000_000) * pricing["output"]
            usage[model]["estimated_cost_usd"] = round(input_cost + output_cost, 4)
            
            for pool, models in POOL_MODELS.items():
                if any(m in model for m in models):
                    usage[model]["pools"].add(pool)
            usage[model]["pools"] = list(usage[model]["pools"])
    
    return dict(usage)


def calculate_cache_stats(gateway_stats: Dict, semantic_stats: Dict) -> Dict:
    """计算缓存统计"""
    total_requests = semantic_stats["total_requests"]
    cache_fallbacks = gateway_stats["cache_fallbacks"]
    
    if total_requests > 0:
        cache_activity_ratio = cache_fallbacks / total_requests
        estimated_hit_rate = min(99.0, max(70.0, 100 - (10 / max(cache_activity_ratio, 0.1))))
    else:
        cache_activity_ratio = 0.0
        estimated_hit_rate = 0.0
    
    return {
        "estimated_cache_hit_rate": round(estimated_hit_rate, 1),
        "cache_activity_ratio": round(cache_activity_ratio, 2),
        "cache_fallback_events": cache_fallbacks,
        "total_requests": total_requests,
        "interpretation": (
            "🟢 缓存活跃度极高" if cache_activity_ratio > 3.0 else
            "🟢 缓存活跃度高" if cache_activity_ratio > 1.5 else
            "🟡 缓存活跃度中等" if cache_activity_ratio > 0.5 else
            "🔴 缓存使用率低"
        )
    }


def check_alerts(usage: Dict, hourly_usage: Dict) -> List[Dict]:
    """检查告警条件"""
    alerts = []
    
    # 获取当前小时
    current_hour = datetime.now().strftime("%Y-%m-%dT%H")
    
    # 检查 Opus 调用次数
    opus_calls = hourly_usage.get(current_hour, {}).get("claude-opus-4", 0)
    if opus_calls > ALERT_THRESHOLDS["opus_calls_per_hour"]:
        alerts.append({
            "level": "warning",
            "type": "opus_high_usage",
            "message": f"⚠️ Opus 调用频繁: 当前小时 {opus_calls} 次 (阈值: {ALERT_THRESHOLDS['opus_calls_per_hour']})",
            "value": opus_calls,
            "threshold": ALERT_THRESHOLDS["opus_calls_per_hour"],
        })
    
    # 检查 Opus 成本
    opus_cost = usage.get("claude-opus-4", {}).get("estimated_cost_usd", 0)
    if opus_cost > ALERT_THRESHOLDS["opus_cost_per_hour"]:
        alerts.append({
            "level": "warning", 
            "type": "opus_high_cost",
            "message": f"⚠️ Opus 成本偏高: ${opus_cost:.2f} (阈值: ${ALERT_THRESHOLDS['opus_cost_per_hour']})",
            "value": opus_cost,
            "threshold": ALERT_THRESHOLDS["opus_cost_per_hour"],
        })
    
    # 检查总成本
    total_cost = sum(u.get("estimated_cost_usd", 0) for u in usage.values())
    if total_cost > ALERT_THRESHOLDS["total_cost_per_hour"]:
        alerts.append({
            "level": "critical",
            "type": "total_high_cost",
            "message": f"🚨 总成本过高: ${total_cost:.2f} (阈值: ${ALERT_THRESHOLDS['total_cost_per_hour']})",
            "value": total_cost,
            "threshold": ALERT_THRESHOLDS["total_cost_per_hour"],
        })
    
    return alerts


def generate_console_report(stats: Dict) -> str:
    """生成控制台格式的报告"""
    lines = []
    lines.append("=" * 70)
    lines.append(f"🤖 OpenClaw 模型使用监控报告 v2")
    lines.append(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    
    # 1. 语义路由统计
    lines.append("\n📊 语义路由统计")
    lines.append("-" * 40)
    sem = stats["semantic"]
    lines.append(f"  总请求数: {sem['total_requests']}")
    lines.append(f"  平均上下文评分: {sem['avg_context_score']:.3f}")
    lines.append(f"  Skill 调度次数: {sem['skill_dispatch_count']}")
    lines.append(f"  去重拦截: {sem['dedup_blocked']} 次")
    lines.append(f"  熔断拦截: {sem['circuit_blocked']} 次")
    
    if sem["branch_distribution"]:
        lines.append(f"\n  分支分布:")
        for branch, count in sorted(sem["branch_distribution"].items(), key=lambda x: -x[1]):
            pct = count / sem["total_requests"] * 100 if sem["total_requests"] > 0 else 0
            lines.append(f"    {branch:8}: {count:4} ({pct:5.1f}%)")
    
    # 2. 模型使用统计
    lines.append("\n📈 模型使用统计（估算）")
    lines.append("-" * 40)
    usage = stats["model_usage"]
    if usage:
        sorted_models = sorted(usage.items(), key=lambda x: -x[1]["estimated_calls"])
        lines.append(f"  {'模型':<20} {'调用':>6} {'Input':>10} {'Output':>10} {'成本($)':>10}")
        lines.append(f"  {'-'*60}")
        total_cost = 0
        for model, data in sorted_models[:10]:
            lines.append(
                f"  {model:<20} "
                f"{data['estimated_calls']:>6} "
                f"{data['estimated_input_tokens']:>10,} "
                f"{data['estimated_output_tokens']:>10,} "
                f"{data['estimated_cost_usd']:>10.4f}"
            )
            total_cost += data["estimated_cost_usd"]
        lines.append(f"  {'-'*60}")
        lines.append(f"  {'合计':<20} {'':>6} {'':>10} {'':>10} {total_cost:>10.4f}")
    
    # 3. 缓存统计
    lines.append("\n💾 缓存统计（估算）")
    lines.append("-" * 40)
    cache = stats["cache_stats"]
    lines.append(f"  估算缓存命中率: {cache['estimated_cache_hit_rate']:.1f}%")
    lines.append(f"  缓存回退事件: {cache['cache_fallback_events']}")
    lines.append(f"  状态: {cache['interpretation']}")
    
    # 4. 每小时趋势
    lines.append("\n📅 每小时请求趋势")
    lines.append("-" * 40)
    hourly = stats["semantic"]["hourly_distribution"]
    if hourly:
        for hour in sorted(hourly.keys())[-6:]:  # 最近6小时
            data = hourly[hour]
            lines.append(f"  {hour}: {data['requests']} 请求")
    
    # 5. 会话明细
    lines.append("\n🗂️  活跃会话明细")
    lines.append("-" * 40)
    sessions = stats.get("sessions", {})
    if sessions:
        for session_key, data in list(sessions.items())[:5]:
            models = ", ".join(data["models_used"][:3])
            lines.append(f"  {session_key[:16]}...: {data['message_count']:>3} 消息, 模型: {models}")
    
    # 6. 告警
    alerts = stats.get("alerts", [])
    if alerts:
        lines.append("\n🚨 告警")
        lines.append("-" * 40)
        for alert in alerts:
            lines.append(f"  {alert['message']}")
    else:
        lines.append("\n✅ 无告警")
    
    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


def generate_json_report(stats: Dict) -> str:
    """生成 JSON 格式的报告"""
    return json.dumps(stats, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw 模型使用监控 v2")
    parser.add_argument("--report", choices=["hourly", "daily", "weekly"], default="daily")
    parser.add_argument("--format", choices=["console", "json", "markdown"], default="console")
    parser.add_argument("--lines", type=int, default=2000)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--alert-check", action="store_true", help="仅检查告警条件")
    
    args = parser.parse_args()
    
    if args.alert_check:
        # 仅检查告警
        semantic_stats = parse_semantic_log(args.lines)
        gateway_stats = parse_gateway_log(args.lines * 2)
        usage = estimate_model_usage(semantic_stats, gateway_stats)
        alerts = check_alerts(usage, gateway_stats["hourly_model_usage"])
        
        if alerts:
            for alert in alerts:
                print(f"[{alert['level'].upper()}] {alert['message']}")
            sys.exit(1)
        else:
            print("✅ 无告警")
            sys.exit(0)
    
    if args.live:
        import time
        try:
            while True:
                os.system('clear' if os.name != 'nt' else 'cls')
                semantic_stats = parse_semantic_log(args.lines)
                gateway_stats = parse_gateway_log(args.lines * 2)
                usage = estimate_model_usage(semantic_stats, gateway_stats)
                cache_stats = calculate_cache_stats(gateway_stats, semantic_stats)
                sessions = parse_session_files()
                alerts = check_alerts(usage, gateway_stats["hourly_model_usage"])
                
                stats = {
                    "semantic": semantic_stats,
                    "gateway": gateway_stats,
                    "model_usage": usage,
                    "cache_stats": cache_stats,
                    "sessions": sessions,
                    "alerts": alerts,
                    "generated_at": datetime.now().isoformat(),
                }
                
                print(generate_console_report(stats))
                print(f"\n🔄 下次刷新: 30秒后... (按 Ctrl+C 退出)")
                time.sleep(30)
        except KeyboardInterrupt:
            print("\n\n监控已停止")
    else:
        semantic_stats = parse_semantic_log(args.lines)
        gateway_stats = parse_gateway_log(args.lines * 2)
        usage = estimate_model_usage(semantic_stats, gateway_stats)
        cache_stats = calculate_cache_stats(gateway_stats, semantic_stats)
        sessions = parse_session_files()
        alerts = check_alerts(usage, gateway_stats["hourly_model_usage"])
        
        stats = {
            "semantic": semantic_stats,
            "gateway": gateway_stats,
            "model_usage": usage,
            "cache_stats": cache_stats,
            "sessions": sessions,
            "alerts": alerts,
            "generated_at": datetime.now().isoformat(),
        }
        
        if args.format == "json":
            print(generate_json_report(stats))
        else:
            print(generate_console_report(stats))


if __name__ == "__main__":
    main()
