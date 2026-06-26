#!/usr/bin/env python3
"""
AI 模型消费统计系统
记录 DeepSeek 和 Kimi 的使用情况，估算成本
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

class CostTracker:
    def __init__(self, log_dir="~/.openclaw/cost_logs"):
        self.log_dir = Path(log_dir).expanduser()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 模型成本配置（元/千token）
        self.cost_rates = {
            "deepseek/deepseek-chat": {
                "input": 0.0,      # 免费
                "output": 0.0,     # 免费
                "description": "DeepSeek Chat (免费)"
            },
            "moonshot/kimi-k2.5": {
                "input": 0.003,    # 0.3分/千token
                "output": 0.012,   # 1.2分/千token
                "description": "Kimi K2.5 (较贵)"
            }
        }
        
        # 今日日志文件
        today = datetime.now().strftime("%Y-%m-%d")
        self.daily_log = self.log_dir / f"cost_{today}.json"
        
        # 初始化日志文件
        if not self.daily_log.exists():
            self._init_daily_log()
    
    def _init_daily_log(self):
        """初始化每日日志"""
        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_cost": 0.0,
            "total_tokens": 0,
            "sessions": [],
            "model_breakdown": {
                model: {"cost": 0.0, "tokens": 0, "sessions": 0}
                for model in self.cost_rates.keys()
            }
        }
        self._save_log(data)
    
    def _load_log(self):
        """加载日志文件"""
        if self.daily_log.exists():
            with open(self.daily_log, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._init_daily_log()
    
    def _save_log(self, data):
        """保存日志文件"""
        with open(self.daily_log, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def log_session(self, model, task_type, input_tokens, output_tokens, notes=""):
        """
        记录一次会话使用
        
        Args:
            model: 模型名称
            task_type: 任务类型
            input_tokens: 输入token数
            output_tokens: 输出token数
            notes: 备注
        """
        # 计算成本
        rate = self.cost_rates.get(model, self.cost_rates["deepseek/deepseek-chat"])
        input_cost = (input_tokens / 1000) * rate["input"]
        output_cost = (output_tokens / 1000) * rate["output"]
        total_cost = input_cost + output_cost
        total_tokens = input_tokens + output_tokens
        
        # 创建会话记录
        session = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "task_type": task_type,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost": round(input_cost, 4),
            "output_cost": round(output_cost, 4),
            "total_cost": round(total_cost, 4),
            "total_tokens": total_tokens,
            "notes": notes
        }
        
        # 更新日志
        data = self._load_log()
        data["sessions"].append(session)
        data["total_cost"] = round(data["total_cost"] + total_cost, 4)
        data["total_tokens"] += total_tokens
        
        # 更新模型分类统计
        if model in data["model_breakdown"]:
            breakdown = data["model_breakdown"][model]
            breakdown["cost"] = round(breakdown["cost"] + total_cost, 4)
            breakdown["tokens"] += total_tokens
            breakdown["sessions"] += 1
        
        self._save_log(data)
        
        return session
    
    def get_daily_summary(self):
        """获取今日汇总"""
        data = self._load_log()
        
        summary = {
            "date": data["date"],
            "total_cost": data["total_cost"],
            "total_tokens": data["total_tokens"],
            "session_count": len(data["sessions"]),
            "model_breakdown": data["model_breakdown"],
            "cost_per_session": round(data["total_cost"] / len(data["sessions"]), 4) if data["sessions"] else 0
        }
        
        return summary
    
    def generate_report(self):
        """生成文本报告"""
        summary = self.get_daily_summary()
        
        report = []
        report.append("=" * 60)
        report.append(f"AI 模型消费统计报告 - {summary['date']}")
        report.append("=" * 60)
        report.append("")
        
        # 总体统计
        report.append("📊 总体统计")
        report.append(f"  总成本: ¥{summary['total_cost']:.4f}")
        report.append(f"  总Token数: {summary['total_tokens']:,}")
        report.append(f"  会话次数: {summary['session_count']}")
        report.append(f"  平均成本/会话: ¥{summary['cost_per_session']:.4f}")
        report.append("")
        
        # 模型分类
        report.append("🤖 模型分类统计")
        for model, stats in summary["model_breakdown"].items():
            if stats["sessions"] > 0:
                model_name = self.cost_rates[model]["description"]
                report.append(f"  {model_name}:")
                report.append(f"    成本: ¥{stats['cost']:.4f}")
                report.append(f"    Token数: {stats['tokens']:,}")
                report.append(f"    会话数: {stats['sessions']}")
        report.append("")
        
        # 成本建议
        report.append("💡 成本优化建议")
        total_cost = summary["total_cost"]
        
        if total_cost == 0:
            report.append("  ✅ 今日无成本消耗，继续保持！")
        elif total_cost < 0.1:
            report.append("  ✅ 成本控制良好 (< ¥0.1)")
        elif total_cost < 1.0:
            report.append("  ⚠️  成本适中 (< ¥1.0)，注意监控")
        else:
            report.append("  🔴 成本较高 (> ¥1.0)，建议优化")
        
        # 模型使用建议
        kimi_cost = summary["model_breakdown"].get("moonshot/kimi-k2.5", {}).get("cost", 0)
        if kimi_cost > 0.5:
            report.append("  💰 Kimi 使用较多，建议更多使用 DeepSeek")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)

# 使用示例
if __name__ == "__main__":
    tracker = CostTracker()
    
    # 示例：记录一次使用
    session = tracker.log_session(
        model="deepseek/deepseek-chat",
        task_type="代码开发",
        input_tokens=500,
        output_tokens=300,
        notes="PaperMC 巡查脚本开发"
    )
    
    # 生成报告
    print(tracker.generate_report())