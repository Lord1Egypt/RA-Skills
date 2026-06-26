#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心情报告生成器
生成日/周/月情绪报告和趋势分析
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 数据路径
DATA_DIR = Path(os.path.expanduser("~/.openclaw/workspace/data/journal"))
DATA_FILE = DATA_DIR / "entries.json"

# 加载情绪配置
def load_mood_config() -> Dict:
    """加载情绪配置文件"""
    config_path = Path(__file__).parent.parent / "assets" / "moods.json"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "moods": {
                "开心": {"score_range": [7, 9], "emoji": "😊", "color": "#FFD93D"},
                "平静": {"score_range": [5, 7], "emoji": "😌", "color": "#6BCB77"},
                "兴奋": {"score_range": [8, 10], "emoji": "🤩", "color": "#FF6B6B"},
                "焦虑": {"score_range": [3, 5], "emoji": "😰", "color": "#9B59B6"},
                "难过": {"score_range": [2, 4], "emoji": "😢", "color": "#3498DB"},
                "愤怒": {"score_range": [1, 3], "emoji": "😠", "color": "#E74C3C"},
                "疲惫": {"score_range": [3, 5], "emoji": "😴", "color": "#95A5A6"}
            }
        }


class MoodReporter:
    """心情报告生成器"""
    
    def __init__(self):
        self.config = load_mood_config()
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载日记数据"""
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"entries": []}
    
    def _get_entries_in_range(self, start_date: str, end_date: str) -> List[Dict]:
        """获取日期范围内的日记"""
        entries = []
        for e in self.data.get("entries", []):
            if start_date <= e["date"] <= end_date:
                entries.append(e)
        return entries
    
    def _get_date_range(self, period: str, offset: int = 0) -> Tuple[str, str]:
        """获取日期范围"""
        today = datetime.now()
        
        if period == 'day':
            target = today - timedelta(days=offset)
            start = end = target.strftime("%Y-%m-%d")
        
        elif period == 'week':
            monday = today - timedelta(days=today.weekday(), weeks=offset)
            sunday = monday + timedelta(days=6)
            start = monday.strftime("%Y-%m-%d")
            end = sunday.strftime("%Y-%m-%d")
        
        elif period == 'month':
            year = today.year
            month = today.month - offset
            while month <= 0:
                year -= 1
                month += 12
            
            start = f"{year}-{month:02d}-01"
            if month == 12:
                next_month = datetime(year + 1, 1, 1)
            else:
                next_month = datetime(year, month + 1, 1)
            last_day = (next_month - timedelta(days=1)).day
            end = f"{year}-{month:02d}-{last_day}"
        
        else:
            raise ValueError(f"不支持的周期类型: {period}")
        
        return start, end
    
    def _calculate_mood_stats(self, entries: List[Dict]) -> Dict:
        """计算情绪统计数据"""
        if not entries:
            return {
                "avg_score": 0,
                "mood_distribution": {},
                "dominant_mood": "无数据",
                "score_trend": "stable"
            }
        
        # 平均评分
        total_score = sum(e.get("score", 5) for e in entries)
        avg_score = total_score / len(entries)
        
        # 情绪分布
        mood_dist = defaultdict(int)
        for e in entries:
            mood_dist[e["mood"]] += 1
        
        # 主导情绪
        dominant_mood = max(mood_dist.items(), key=lambda x: x[1])[0] if mood_dist else "无数据"
        
        # 评分趋势（如果有多条记录）
        score_trend = "stable"
        if len(entries) >= 2:
            entries_sorted = sorted(entries, key=lambda x: x["date"])
            first_half = entries_sorted[:len(entries_sorted)//2]
            second_half = entries_sorted[len(entries_sorted)//2:]
            
            if first_half and second_half:
                first_avg = sum(e.get("score", 5) for e in first_half) / len(first_half)
                second_avg = sum(e.get("score", 5) for e in second_half) / len(second_half)
                
                if second_avg > first_avg + 0.5:
                    score_trend = "improving"
                elif second_avg < first_avg - 0.5:
                    score_trend = "declining"
        
        return {
            "avg_score": round(avg_score, 1),
            "mood_distribution": dict(mood_dist),
            "dominant_mood": dominant_mood,
            "score_trend": score_trend
        }
    
    def generate_daily_report(self, date: Optional[str] = None) -> Dict:
        """生成日报"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        entries = self._get_entries_in_range(date, date)
        stats = self._calculate_mood_stats(entries)
        
        # 获取情绪emoji
        mood_config = self.config["moods"].get(stats["dominant_mood"], {})
        emoji = mood_config.get("emoji", "📝")
        
        return {
            "type": "daily",
            "date": date,
            "emoji": emoji,
            "entry_count": len(entries),
            **stats,
            "entries": entries
        }
    
    def generate_weekly_report(self, offset: int = 0) -> Dict:
        """生成周报"""
        start, end = self._get_date_range('week', offset)
        entries = self._get_entries_in_range(start, end)
        stats = self._calculate_mood_stats(entries)
        
        # 按天统计
        daily_scores = defaultdict(list)
        for e in entries:
            daily_scores[e["date"]].append(e.get("score", 5))
        
        daily_avg = {date: round(sum(scores)/len(scores), 1) for date, scores in daily_scores.items()}
        
        # 情绪emoji
        mood_config = self.config["moods"].get(stats["dominant_mood"], {})
        emoji = mood_config.get("emoji", "📝")
        
        # 生成建议
        suggestion = self._generate_suggestion(stats)
        
        return {
            "type": "weekly",
            "start_date": start,
            "end_date": end,
            "emoji": emoji,
            "entry_count": len(entries),
            "daily_scores": daily_avg,
            **stats,
            "suggestion": suggestion
        }
    
    def generate_monthly_report(self, offset: int = 0) -> Dict:
        """生成月报"""
        start, end = self._get_date_range('month', offset)
        entries = self._get_entries_in_range(start, end)
        stats = self._calculate_mood_stats(entries)
        
        # 按周统计
        weekly_stats = defaultdict(lambda: {"scores": [], "moods": []})
        for e in entries:
            date = datetime.strptime(e["date"], "%Y-%m-%d")
            week_num = date.isocalendar()[1]
            weekly_stats[f"第{week_num}周"]["scores"].append(e.get("score", 5))
            weekly_stats[f"第{week_num}周"]["moods"].append(e["mood"])
        
        weekly_summary = {}
        for week, data in weekly_stats.items():
            weekly_summary[week] = {
                "avg_score": round(sum(data["scores"]) / len(data["scores"]), 1),
                "dominant_mood": max(set(data["moods"]), key=data["moods"].count) if data["moods"] else "无"
            }
        
        # 情绪emoji
        mood_config = self.config["moods"].get(stats["dominant_mood"], {})
        emoji = mood_config.get("emoji", "📝")
        
        # 生成建议
        suggestion = self._generate_suggestion(stats)
        
        return {
            "type": "monthly",
            "start_date": start,
            "end_date": end,
            "emoji": emoji,
            "entry_count": len(entries),
            "weekly_summary": weekly_summary,
            **stats,
            "suggestion": suggestion
        }
    
    def generate_trend_analysis(self, days: int = 30) -> Dict:
        """生成趋势分析报告"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        entries = self._get_entries_in_range(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        if not entries:
            return {
                "type": "trend",
                "period_days": days,
                "has_data": False,
                "message": "该时间段内没有日记记录"
            }
        
        # 按周分组统计
        weekly_data = defaultdict(lambda: {"scores": [], "moods": []})
        for e in entries:
            date = datetime.strptime(e["date"], "%Y-%m-%d")
            week_key = date.strftime("%Y-W%W")
            weekly_data[week_key]["scores"].append(e.get("score", 5))
            weekly_data[week_key]["moods"].append(e["mood"])
        
        # 计算每周平均
        weekly_scores = {}
        for week, data in weekly_data.items():
            weekly_scores[week] = round(sum(data["scores"]) / len(data["scores"]), 1)
        
        # 趋势判断
        sorted_weeks = sorted(weekly_scores.keys())
        trend = "stable"
        trend_description = "情绪状态保持稳定"
        
        if len(sorted_weeks) >= 2:
            first_score = weekly_scores[sorted_weeks[0]]
            last_score = weekly_scores[sorted_weeks[-1]]
            
            if last_score > first_score + 1:
                trend = "improving"
                trend_description = "情绪状态呈上升趋势，保持积极！"
            elif last_score < first_score - 1:
                trend = "declining"
                trend_description = "情绪状态呈下降趋势，建议关注心理健康"
        
        # 找出情绪波动较大的时期（标准差大于2）
        volatility_periods = []
        for week, data in weekly_data.items():
            if len(data["scores"]) >= 2:
                mean = sum(data["scores"]) / len(data["scores"])
                variance = sum((x - mean) ** 2 for x in data["scores"]) / len(data["scores"])
                std_dev = variance ** 0.5
                if std_dev > 2:
                    volatility_periods.append({
                        "week": week,
                        "volatility": round(std_dev, 2)
                    })
        
        # 生成建议
        suggestion = self._generate_suggestion({
            "avg_score": sum(e.get("score", 5) for e in entries) / len(entries),
            "dominant_mood": max(set(e["mood"] for e in entries), key=lambda x: sum(1 for e in entries if e["mood"] == x)),
            "score_trend": trend
        })
        
        return {
            "type": "trend",
            "period_days": days,
            "has_data": True,
            "entry_count": len(entries),
            "weekly_scores": weekly_scores,
            "trend": trend,
            "trend_description": trend_description,
            "volatility_periods": volatility_periods,
            "suggestion": suggestion
        }
    
    def _generate_suggestion(self, stats: Dict) -> str:
        """根据统计数据生成建议"""
        avg_score = stats.get("avg_score", 5)
        trend = stats.get("score_trend", "stable")
        dominant_mood = stats.get("dominant_mood", "平静")
        
        suggestions = []
        
        # 基于平均评分
        if avg_score >= 8:
            suggestions.append("你的情绪状态非常好！保持这种积极的生活态度。")
        elif avg_score >= 6:
            suggestions.append("你的情绪状态不错，继续保持良好的生活节奏。")
        elif avg_score >= 4:
            suggestions.append("情绪状态一般，可以尝试增加一些让自己开心的活动。")
        else:
            suggestions.append("最近情绪状态偏低，建议多关注自己的心理健康，必要时寻求专业帮助。")
        
        # 基于趋势
        if trend == "improving":
            suggestions.append("情绪呈上升趋势，很棒！")
        elif trend == "declining":
            suggestions.append("情绪有些下滑，试着找些方式调节一下。")
        
        # 基于主导情绪
        if dominant_mood in ["焦虑", "难过", "愤怒"]:
            suggestions.append(f"最近{dominant_mood}情绪较多，试着找出原因并寻求解决方法。")
        elif dominant_mood in ["开心", "兴奋"]:
            suggestions.append("保持这份好心情！")
        
        return " ".join(suggestions)
    
    def format_report(self, report: Dict, format_type: str = "text") -> str:
        """格式化报告为可读文本"""
        if format_type == "json":
            return json.dumps(report, ensure_ascii=False, indent=2)
        
        lines = []
        
        # 标题
        emoji = report.get("emoji", "📝")
        if report["type"] == "daily":
            lines.append(f"{emoji} 心情日报 ({report['date']})")
        elif report["type"] == "weekly":
            lines.append(f"{emoji} 心情周报 ({report['start_date']} ~ {report['end_date']})")
        elif report["type"] == "monthly":
            lines.append(f"{emoji} 心情月报 ({report['start_date'][:7]})")
        elif report["type"] == "trend":
            lines.append(f"📊 情绪趋势分析 (近{report['period_days']}天)")
        
        lines.append("=" * 50)
        
        # 无数据情况
        if report.get("has_data") is False:
            lines.append(f"\n{report.get('message', '暂无数据')}")
            return "\n".join(lines)
        
        # 基本统计
        if "entry_count" in report:
            lines.append(f"📝 日记数量: {report['entry_count']} 篇")
        
        if "avg_score" in report:
            score_emoji = "😊" if report["avg_score"] >= 7 else "😐" if report["avg_score"] >= 5 else "😔"
            lines.append(f"{score_emoji} 平均情绪评分: {report['avg_score']}/10")
        
        if "dominant_mood" in report:
            lines.append(f"🎭 主导情绪: {report['dominant_mood']}")
        
        # 情绪分布
        if "mood_distribution" in report and report["mood_distribution"]:
            lines.append(f"\n📊 情绪分布:")
            for mood, count in sorted(report["mood_distribution"].items(), key=lambda x: x[1], reverse=True):
                mood_config = self.config["moods"].get(mood, {})
                mood_emoji = mood_config.get("emoji", "")
                lines.append(f"   {mood_emoji} {mood}: {count}篇")
        
        # 趋势信息
        if report["type"] == "trend":
            lines.append(f"\n📈 趋势: {report.get('trend_description', '')}")
            
            if report.get("volatility_periods"):
                lines.append(f"\n⚠️ 情绪波动较大的时期:")
                for period in report["volatility_periods"]:
                    lines.append(f"   {period['week']}: 波动指数 {period['volatility']}")
        
        # 每日/每周详情
        if "daily_scores" in report and report["daily_scores"]:
            lines.append(f"\n📅 每日情绪评分:")
            for date, score in sorted(report["daily_scores"].items()):
                lines.append(f"   {date}: {score}/10")
        
        if "weekly_summary" in report and report["weekly_summary"]:
            lines.append(f"\n📅 每周情绪概况:")
            for week, data in sorted(report["weekly_summary"].items()):
                lines.append(f"   {week}: {data['avg_score']}/10 ({data['dominant_mood']})")
        
        # 建议
        if "suggestion" in report:
            lines.append(f"\n💡 建议:")
            lines.append(f"   {report['suggestion']}")
        
        return "\n".join(lines)


def main():
    """命令行入口"""
    reporter = MoodReporter()
    
    if len(sys.argv) < 2:
        print("心情报告生成器 - mood-diary")
        print("用法: python mood-report.py <报告类型> [参数]\n")
        print("报告类型:")
        print("  daily [日期]        - 日报，如: daily 2024-01-15")
        print("  weekly [周偏移]     - 周报，0=本周, 1=上周")
        print("  monthly [月偏移]    - 月报，0=本月, 1=上月")
        print("  trend [天数]        - 趋势分析，默认30天")
        print("")
        sys.exit(0)
    
    command = sys.argv[1]
    
    try:
        if command == "daily":
            date = sys.argv[2] if len(sys.argv) > 2 else None
            report = reporter.generate_daily_report(date)
        
        elif command == "weekly":
            offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            report = reporter.generate_weekly_report(offset)
        
        elif command == "monthly":
            offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            report = reporter.generate_monthly_report(offset)
        
        elif command == "trend":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            report = reporter.generate_trend_analysis(days)
        
        else:
            print(f"❌ 未知报告类型: {command}")
            print("可用类型: daily, weekly, monthly, trend")
            sys.exit(1)
        
        # 输出报告
        format_type = sys.argv[-1] if sys.argv[-1] in ["text", "json"] else "text"
        print(reporter.format_report(report, format_type))
    
    except Exception as e:
        print(f"❌ 生成报告失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
