#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
TokenTracker - OpenClaw Token 消耗监控工具
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any

# 默认配置
DEFAULT_CONFIG = {
    "daily_threshold": 10.0,
    "weekly_threshold": 50.0,
    "alert_percent": 0.95,
    "time_zone": "Asia/Shanghai",
    "models_to_track": ["minimax-portal/MiniMax-M2.5", "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
    "model_price_list": {
        "minimax-portal/MiniMax-M2.5": {"token_in_price": 0.01, "token_out_price": 0.01},
        "gpt-4o": {"token_in_price": 0.03, "token_out_price": 0.06},
        "gpt-4o-mini": {"token_in_price": 0.015, "token_out_price": 0.03},
        "gpt-3.5-turbo": {"token_in_price": 0.002, "token_out_price": 0.004},
        "default": {"token_in_price": 0.01, "token_out_price": 0.01}
    }
}

DEFAULT_PRICE = {"token_in": 0.01, "token_out": 0.01}


class TokenTracker:
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            # 默认数据目录
            self.data_dir = Path.home() / ".openclaw" / "workspace" / "skills" / "token-tracker"
        else:
            self.data_dir = Path(data_dir)
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.data_dir / "config.json"
        self.records_file = self.data_dir / "usage_records.json"
        
        self.config = self._load_config()
        
        # 使用固定的时区偏移（简化处理）
        self.tz_offset = 8  # Asia/Shanghai UTC+8
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        else:
            # 创建默认配置
            self._save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def _load_records(self) -> List[Dict]:
        """加载使用记录"""
        if self.records_file.exists():
            with open(self.records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_records(self, records: List[Dict]):
        """保存使用记录"""
        with open(self.records_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    
    def add_record(self, session_id: str, model: str, token_in: int, token_out: int, cost: float = None):
        """添加一条使用记录"""
        records = self._load_records()
        
        # 计算成本（如果未提供）
        if cost is None:
            cost = self.calculate_cost(model, token_in, token_out)
        
        record = {
            "timestamp": (datetime.now() + timedelta(hours=self.tz_offset)).isoformat(),
            "session_id": session_id,
            "model": model,
            "token_in": token_in,
            "token_out": token_out,
            "cost": round(cost, 6)
        }
        
        records.append(record)
        self._save_records(records)
        return record
    
    def calculate_cost(self, model: str, token_in: int, token_out: int) -> float:
        """计算成本"""
        # 查找模型价格
        price_list = self.config.get("model_price_list", {})
        
        # 尝试精确匹配
        if model in price_list:
            prices = price_list[model]
        else:
            # 尝试模糊匹配
            matched = False
            for key in price_list:
                if key != "default" and key.lower() in model.lower():
                    prices = price_list[key]
                    matched = True
                    break
            
            if not matched:
                prices = price_list.get("default", DEFAULT_PRICE)
        
        token_in_price = prices.get("token_in_price", DEFAULT_PRICE["token_in"])
        token_out_price = prices.get("token_out_price", DEFAULT_PRICE["token_out"])
        
        cost = (token_in / 1_000_000 * token_in_price) + (token_out / 1_000_000 * token_out_price)
        return round(cost, 6)
    
    def get_records_for_period(self, period: str) -> List[Dict]:
        """获取指定时间段的使用记录"""
        records = self._load_records()
        now = datetime.now() + timedelta(hours=self.tz_offset)
        
        if period == "today":
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            # 本周开始（周一）
            days_since_monday = now.weekday()
            start_time = (now - timedelta(days=days_since_monday)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        else:
            return records
        
        filtered = []
        for r in records:
            try:
                record_time = datetime.fromisoformat(r["timestamp"])
                if record_time >= start_time:
                    filtered.append(r)
            except:
                continue
        
        return filtered
    
    def summarize_records(self, records: List[Dict]) -> Dict:
        """汇总记录"""
        if not records:
            return {
                "total_token_in": 0,
                "total_token_out": 0,
                "total_cost": 0.0,
                "by_model": {},
                "peak_hours": []
            }
        
        total_token_in = sum(r.get("token_in", 0) for r in records)
        total_token_out = sum(r.get("token_out", 0) for r in records)
        total_cost = sum(r.get("cost", 0.0) for r in records)
        
        # 按模型统计
        by_model = {}
        hourly_usage = {}
        
        for r in records:
            model = r.get("model", "unknown")
            if model not in by_model:
                by_model[model] = {
                    "token_in": 0,
                    "token_out": 0,
                    "cost": 0.0
                }
            
            by_model[model]["token_in"] += r.get("token_in", 0)
            by_model[model]["token_out"] += r.get("token_out", 0)
            by_model[model]["cost"] += r.get("cost", 0.0)
            
            # 统计高峰时段
            try:
                record_time = datetime.fromisoformat(r["timestamp"])
                hour = record_time.hour
                hourly_usage[hour] = hourly_usage.get(hour, 0) + r.get("cost", 0.0)
            except:
                pass
        
        # 计算高峰时段
        if hourly_usage:
            sorted_hours = sorted(hourly_usage.items(), key=lambda x: x[1], reverse=True)
            peak_hours = [f"{h}:00" for h, _ in sorted_hours[:3]]
        else:
            peak_hours = []
        
        # 四舍五入成本
        for model in by_model:
            by_model[model]["cost"] = round(by_model[model]["cost"], 4)
        
        return {
            "total_token_in": total_token_in,
            "total_token_out": total_token_out,
            "total_cost": round(total_cost, 4),
            "by_model": by_model,
            "peak_hours": peak_hours
        }
    
    def format_report(self, period: str) -> str:
        """格式化报告"""
        records = self.get_records_for_period(period)
        summary = self.summarize_records(records)
        
        if period == "today":
            title = "📊 今日 Token 账单"
        elif period == "week":
            title = "📊 本周 Token 账单"
        else:
            title = "📊 Token 账单"
        
        lines = [title]
        
        # 按模型显示
        for model, stats in summary["by_model"].items():
            in_k = stats["token_in"] / 1000
            out_k = stats["token_out"] / 1000
            lines.append(f"{model} → {in_k:.1f}k in / {out_k:.1f}k out, ${stats['cost']:.4f}")
        
        lines.append(f"总计：${summary['total_cost']:.4f}")
        
        if summary["peak_hours"]:
            lines.append(f"高峰时段：{', '.join(summary['peak_hours'])}")
        
        return "\n".join(lines)
    
    def format_today(self) -> str:
        """格式化今日消耗（简洁版）"""
        records = self.get_records_for_period("today")
        summary = self.summarize_records(records)
        
        lines = ["📊 今日 Token 消耗：" ]
        
        for model, stats in summary["by_model"].items():
            in_k = stats["token_in"] / 1000
            out_k = stats["token_out"] / 1000
            lines.append(f"{model} → {in_k:.1f}k in / {out_k:.1f}k out")
        
        lines.append(f"总计：${summary['total_cost']:.4f}")
        
        return "\n".join(lines)
    
    def check_threshold(self) -> tuple[bool, str]:
        """检查是否超过阈值"""
        records = self.get_records_for_period("today")
        summary = self.summarize_records(records)
        
        daily_threshold = self.config.get("daily_threshold", 10.0)
        alert_percent = self.config.get("alert_percent", 0.95)
        
        current_cost = summary["total_cost"]
        threshold = daily_threshold * alert_percent
        
        if current_cost >= threshold:
            lines = [f"⚠️ 警告：Token 消耗即将超标"]
            for model, stats in summary["by_model"].items():
                lines.append(f"{model} → ${stats['cost']:.2f} / ${daily_threshold:.2f}")
            lines.append(f"总计：${current_cost:.2f} / ${daily_threshold:.2f}")
            return True, "\n".join(lines)
        
        return False, ""
    
    def get_threshold(self) -> Dict:
        """获取阈值信息"""
        return {
            "daily": self.config.get("daily_threshold", 10.0),
            "weekly": self.config.get("weekly_threshold", 50.0),
            "alert_percent": self.config.get("alert_percent", 0.95)
        }


def main():
    parser = argparse.ArgumentParser(description="TokenTracker - Token 消耗监控")
    parser.add_argument("command", choices=["today", "week", "threshold", "check-threshold", "report", "add"], 
                        help="命令")
    parser.add_argument("period", nargs="?", choices=["today", "week"], help="时间段 (report 命令使用)")
    parser.add_argument("--session-id", default="agent:main:main", help="Session ID")
    parser.add_argument("--model", default="minimax-portal/MiniMax-M2.5", help="模型名称")
    parser.add_argument("--token-in", type=int, default=0, help="输入 token 数")
    parser.add_argument("--token-out", type=int, default=0, help="输出 token 数")
    parser.add_argument("--cost", type=float, help="成本（可选，自动计算）")
    
    args = parser.parse_args()
    
    tracker = TokenTracker()
    
    if args.command == "add":
        # 添加记录
        record = tracker.add_record(
            args.session_id,
            args.model,
            args.token_in,
            args.token_out,
            args.cost
        )
        print(f"已添加记录: {json.dumps(record, ensure_ascii=False, indent=2)}")
    
    elif args.command == "today":
        # 今日消耗
        print(tracker.format_today())
    
    elif args.command == "week":
        # 本周消耗
        print(tracker.format_report("week"))
    
    elif args.command == "threshold":
        # 显示阈值
        th = tracker.get_threshold()
        print(f"每日阈值: ${th['daily']:.2f}")
        print(f"每周阈值: ${th['weekly']:.2f}")
        print(f"警报百分比: {th['alert_percent']*100:.0f}%")
    
    elif args.command == "check-threshold":
        # 检查阈值
        exceeded, message = tracker.check_threshold()
        if exceeded:
            print(message)
        else:
            print("✅ 未超过阈值")
    
    elif args.command == "report":
        # 完整报告
        if not args.period:
            print("请指定 period: today 或 week")
            sys.exit(1)
        print(tracker.format_report(args.period))


if __name__ == "__main__":
    main()
