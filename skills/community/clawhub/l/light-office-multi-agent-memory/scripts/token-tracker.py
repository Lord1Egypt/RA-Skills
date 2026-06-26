#!/usr/bin/env python3
"""
多Agent记忆系统 - Token消耗追踪脚本（通用版）

功能：
  追踪记忆系统的Token消耗，建立成本基线

作者：光光教授 (光光事务所)
版本：v1.0.0
许可证：MIT
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# 配置
# ============================================================

WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", "/tmp/memory-workspace"))
TOKEN_LOG_DIR = WORKSPACE / "token-logs"

# Token成本配置（元/千Token）
TOKEN_COSTS = {
    "qwen3.5-plus": {
        "input": 0.02,
        "output": 0.06
    },
    "qwen3.5-turbo": {
        "input": 0.005,
        "output": 0.015
    },
    "gpt-4": {
        "input": 0.03,
        "output": 0.06
    },
    "claude-3": {
        "input": 0.025,
        "output": 0.075
    }
}

# ============================================================
# Token追踪类
# ============================================================

class TokenTracker:
    """Token消耗追踪器"""
    
    def __init__(self):
        self.token_log_dir = TOKEN_LOG_DIR
        self.token_log_dir.mkdir(parents=True, exist_ok=True)
    
    def log_session(self, session_id, model, input_tokens, output_tokens):
        """记录会话Token消耗"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.token_log_dir / f"{today}.json"
        
        # 读取现有日志
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []
        
        # 计算成本
        cost_config = TOKEN_COSTS.get(model, TOKEN_COSTS["qwen3.5-plus"])
        input_cost = (input_tokens / 1000) * cost_config["input"]
        output_cost = (output_tokens / 1000) * cost_config["output"]
        total_cost = input_cost + output_cost
        
        # 添加新记录
        log_entry = {
            "session_id": session_id,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost": round(input_cost, 4),
            "output_cost": round(output_cost, 4),
            "total_cost": round(total_cost, 4),
            "timestamp": datetime.now().isoformat()
        }
        
        logs.append(log_entry)
        
        # 写入日志
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        return log_entry
    
    def get_daily_report(self, date=None):
        """生成日报"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        log_file = self.token_log_dir / f"{date}.json"
        
        if not log_file.exists():
            return {"error": f"日志文件不存在: {log_file}"}
        
        with open(log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)
        
        # 统计
        total_sessions = len(logs)
        total_input_tokens = sum(log["input_tokens"] for log in logs)
        total_output_tokens = sum(log["output_tokens"] for log in logs)
        total_tokens = total_input_tokens + total_output_tokens
        total_cost = sum(log["total_cost"] for log in logs)
        
        # 按模型统计
        model_stats = {}
        for log in logs:
            model = log["model"]
            if model not in model_stats:
                model_stats[model] = {
                    "sessions": 0,
                    "tokens": 0,
                    "cost": 0
                }
            model_stats[model]["sessions"] += 1
            model_stats[model]["tokens"] += log["total_tokens"]
            model_stats[model]["cost"] += log["total_cost"]
        
        report = {
            "date": date,
            "total_sessions": total_sessions,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_tokens,
            "total_cost": round(total_cost, 4),
            "model_stats": model_stats
        }
        
        return report
    
    def get_monthly_report(self, year_month=None):
        """生成月报"""
        if year_month is None:
            now = datetime.now()
            year_month = f"{now.year}-{now.month:02d}"
        
        # 获取当月所有日志
        logs = []
        for day in range(1, 32):
            date = f"{year_month}-{day:02d}"
            log_file = self.token_log_dir / f"{date}.json"
            if log_file.exists():
                with open(log_file, "r", encoding="utf-8") as f:
                    logs.extend(json.load(f))
        
        if not logs:
            return {"error": f"月报日志不存在: {year_month}"}
        
        # 统计
        total_sessions = len(logs)
        total_tokens = sum(log["total_tokens"] for log in logs)
        total_cost = sum(log["total_cost"] for log in logs)
        
        report = {
            "year_month": year_month,
            "total_sessions": total_sessions,
            "total_tokens": total_tokens,
            "total_cost": round(total_cost, 4)
        }
        
        return report
    
    def get_optimization_suggestions(self):
        """获取优化建议"""
        suggestions = [
            "1. 使用RTK Token压缩（可节省20-40%）",
            "2. 简单任务使用轻量模型（qwen3.5-turbo）",
            "3. 定期清理过期记忆（减少检索Token）",
            "4. 启用记忆压缩（减少上下文Token）"
        ]
        return suggestions


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    tracker = TokenTracker()
    
    print("=" * 60)
    print("多Agent记忆系统 - Token消耗追踪测试")
    print("=" * 60)
    
    # 测试记录
    print("\n[测试1] 记录会话Token")
    entry = tracker.log_session(
        session_id="test-001",
        model="qwen3.5-plus",
        input_tokens=5000,
        output_tokens=3000
    )
    print(f"  记录: {json.dumps(entry, ensure_ascii=False, indent=2)}")
    
    # 生成日报
    print("\n[测试2] 生成日报")
    report = tracker.get_daily_report()
    print(f"  日报: {json.dumps(report, ensure_ascii=False, indent=2)}")
    
    # 优化建议
    print("\n[测试3] 优化建议")
    suggestions = tracker.get_optimization_suggestions()
    for suggestion in suggestions:
        print(f"  {suggestion}")
    
    print("\n✅ Token追踪测试完成")


if __name__ == "__main__":
    main()
