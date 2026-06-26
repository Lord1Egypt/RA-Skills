#!/usr/bin/env python3
"""
Cost Watchdog Visualizer
Generates cost reports, charts, and breakdowns for API spending.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from io_utils import write_json_atomic, read_json

# Default data directory for cost tracking
DATA_DIR = Path.home() / ".cost-watchdog"
DATA_DIR.mkdir(exist_ok=True)


class CostTracker:
    """Track and visualize API costs across sessions."""
    
    def __init__(self):
        self.data_file = DATA_DIR / "cost-data.json"
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        return read_json(
            self.data_file,
            default={
                "sessions": [],
                "tasks": [],
                "providers": {},
                "budgets": [],
                "alerts": [],
            },
        )

    def _save_data(self):
        write_json_atomic(self.data_file, self.data)
    
    def add_session(self, session_id: str, model: str, tokens_in: int, 
                    tokens_out: int, cost: float, duration_seconds: int = 0):
        """Record a new session's cost data."""
        session = {
            "id": session_id,
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "tokens_total": tokens_in + tokens_out,
            "cost": cost,
            "duration_seconds": duration_seconds
        }
        self.data["sessions"].append(session)
        self._update_provider_stats(model, cost)
        self._save_data()
        return session
    
    def add_task(self, task_name: str, cost: float, tokens: int, 
                 provider: str, model: str, status: str = "completed"):
        """Record a task's cost data."""
        task = {
            "name": task_name,
            "timestamp": datetime.now().isoformat(),
            "cost": cost,
            "tokens": tokens,
            "provider": provider,
            "model": model,
            "status": status
        }
        self.data["tasks"].append(task)
        self._save_data()
        return task
    
    def _update_provider_stats(self, model: str, cost: float):
        """Update provider statistics."""
        provider = model.split('/')[0] if '/' in model else model
        if provider not in self.data["providers"]:
            self.data["providers"][provider] = {
                "total_cost": 0.0,
                "total_tokens": 0,
                "sessions": 0
            }
        self.data["providers"][provider]["total_cost"] += cost
        self.data["providers"][provider]["sessions"] += 1
    
    def set_budget(self, amount: float, duration: str = "session"):
        """Set a budget limit."""
        budget = {
            "amount": amount,
            "duration": duration,
            "set_at": datetime.now().isoformat()
        }
        self.data["budgets"].append(budget)
        self._save_data()
    
    def get_daily_summary(self, date: Optional[datetime] = None) -> dict:
        """Get cost summary for a specific day."""
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%Y-%m-%d")
        daily_sessions = [
            s for s in self.data["sessions"]
            if s["timestamp"].startswith(date_str)
        ]
        
        total_cost = sum(s["cost"] for s in daily_sessions)
        total_tokens = sum(s["tokens_total"] for s in daily_sessions)
        
        return {
            "date": date_str,
            "sessions": len(daily_sessions),
            "total_cost": round(total_cost, 4),
            "total_tokens": total_tokens,
            "avg_cost_per_session": round(total_cost / max(len(daily_sessions), 1), 4)
        }
    
    def get_weekly_summary(self, days: int = 7) -> dict:
        """Get cost summary for the last N days."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        daily_summaries = []
        for i in range(days):
            day = start_date + timedelta(days=i)
            daily_summaries.append(self.get_daily_summary(day))
        
        total_cost = sum(d["total_cost"] for d in daily_summaries)
        total_sessions = sum(d["sessions"] for d in daily_summaries)
        
        return {
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "days": days,
            "total_cost": round(total_cost, 4),
            "total_sessions": total_sessions,
            "daily_avg_cost": round(total_cost / days, 4),
            "daily_summaries": daily_summaries
        }
    
    def get_provider_breakdown(self) -> dict:
        """Get cost breakdown by provider."""
        return self.data["providers"]
    
    def get_task_breakdown(self, limit: int = 10) -> list:
        """Get top N most expensive tasks."""
        sorted_tasks = sorted(
            self.data["tasks"],
            key=lambda x: x["cost"],
            reverse=True
        )
        return sorted_tasks[:limit]
    
    def generate_ascii_chart(self, data: list, width: int = 50) -> str:
        """Generate ASCII bar chart for cost data."""
        if not data:
            return "No data available"
        
        max_value = max(d["cost"] for d in data)
        lines = []
        
        for d in data[:10]:  # Top 10
            bar_length = int((d["cost"] / max_value) * width) if max_value > 0 else 0
            bar = "█" * bar_length
            lines.append(f"{d['name'][:20]:<20} {bar} ${d['cost']:.4f}")
        
        return "\n".join(lines)
    
    def generate_report(self, period: str = "daily") -> str:
        """Generate a text-based cost report."""
        if period == "daily":
            summary = self.get_daily_summary()
            title = f"Daily Cost Report - {summary['date']}"
        elif period == "weekly":
            summary = self.get_weekly_summary()
            title = f"Weekly Cost Report - {summary['period']}"
        else:
            return "Invalid period. Use 'daily' or 'weekly'."
        
        report = []
        report.append("=" * 60)
        report.append(f"📊 {title}")
        report.append("=" * 60)
        report.append("")
        report.append(f"💰 Total Cost: ${summary['total_cost']:.4f}")
        report.append(f"📝 Total Sessions: {summary.get('sessions', summary.get('total_sessions', 0))}")
        report.append(f"🔢 Total Tokens: {summary.get('total_tokens', 0):,}")
        
        if 'daily_avg_cost' in summary:
            report.append(f"📈 Daily Average: ${summary['daily_avg_cost']:.4f}")
        
        report.append("")
        report.append("-" * 60)
        report.append("🏆 Top 5 Most Expensive Tasks:")
        report.append("-" * 60)
        
        top_tasks = self.get_task_breakdown(5)
        for i, task in enumerate(top_tasks, 1):
            report.append(f"{i}. {task['name'][:30]:<30} ${task['cost']:.4f}")
        
        report.append("")
        report.append("-" * 60)
        report.append("📊 Provider Breakdown:")
        report.append("-" * 60)
        
        providers = self.get_provider_breakdown()
        for provider, stats in sorted(providers.items(), key=lambda x: x[1]["total_cost"], reverse=True):
            report.append(f"  {provider:<15} ${stats['total_cost']:.4f} ({stats['sessions']} sessions)")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """CLI interface for cost visualization."""
    tracker = CostTracker()
    
    import sys
    if len(sys.argv) < 2:
        print("Usage: cost-visualizer.py [command]")
        print("Commands:")
        print("  daily     - Show daily cost report")
        print("  weekly    - Show weekly cost report")
        print("  tasks     - Show top expensive tasks")
        print("  providers - Show provider breakdown")
        print("  chart     - Show ASCII chart of costs")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "daily":
        print(tracker.generate_report("daily"))
    elif command == "weekly":
        print(tracker.generate_report("weekly"))
    elif command == "tasks":
        tasks = tracker.get_task_breakdown(10)
        print("\n🏆 Top 10 Most Expensive Tasks:\n")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task['name']:<30} ${task['cost']:.4f} ({task['model']})")
    elif command == "providers":
        providers = tracker.get_provider_breakdown()
        print("\n📊 Provider Breakdown:\n")
        for provider, stats in sorted(providers.items(), key=lambda x: x[1]["total_cost"], reverse=True):
            print(f"  {provider:<15} ${stats['total_cost']:.4f} ({stats['sessions']} sessions)")
    elif command == "chart":
        tasks = tracker.get_task_breakdown(10)
        print("\n📊 Cost Chart:\n")
        print(tracker.generate_ascii_chart(tasks))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
