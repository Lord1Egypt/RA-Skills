#!/usr/bin/env python3
"""
ASIN诊所Pro版 - Level 2
ASIN Clinic Pro

基于免费版5维评分，增加：
- benchmark: ASIN对标分析
- gantt: 修复优先级甘特图
- weekly-report: 周报模板生成
- trend: 历史趋势对比

Author: Miaoji Studio Pro
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class DiagnosisResult:
    """诊断结果"""
    asin: str
    overall_score: float
    dimensions: Dict[str, float]
    issues: List[Dict]
    priority_fixes: List[Dict]


@dataclass
class BenchmarkResult:
    """对标结果"""
    asin: str
    vs_competitors: List[Dict]
    gap_analysis: Dict[str, Any]
    opportunities: List[str]


class AsinClinicPro:
    """ASIN诊所Pro版"""
    
    DIMENSION_WEIGHTS = {
        "合规度": 0.20,
        "广告度": 0.25,
        "评论度": 0.20,
        "视觉度": 0.15,
        "内容度": 0.20
    }
    
    def __init__(self):
        self.current_diagnosis: Optional[DiagnosisResult] = None
        self.history_data: List[Dict] = []
    
    def diagnose(self, asin: str, data: Dict) -> DiagnosisResult:
        """
        诊断ASIN
        
        Args:
            asin: ASIN
            data: 诊断数据
        
        Returns:
            诊断结果
        """
        dimensions = {}
        issues = []
        
        # 五维诊断
        for dim, weight in self.DIMENSION_WEIGHTS.items():
            dim_data = data.get(dim, {})
            score = dim_data.get("score", 50)
            dimensions[dim] = score
            
            # 发现问题
            if score < 70:
                issue = {
                    "dimension": dim,
                    "score": score,
                    "severity": "high" if score < 50 else "medium",
                    "description": f"{dim}得分{score}分，需要优化",
                    "suggestions": self._get_dim_suggestions(dim, score)
                }
                issues.append(issue)
        
        # 计算综合分
        overall = sum(dimensions.values()) / len(dimensions)
        
        # 生成修复优先级
        priority_fixes = self._generate_priority_fixes(issues)
        
        self.current_diagnosis = DiagnosisResult(
            asin=asin,
            overall_score=round(overall, 1),
            dimensions=dimensions,
            issues=issues,
            priority_fixes=priority_fixes
        )
        
        # 保存历史
        self.history_data.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "score": overall,
            "dimensions": dimensions
        })
        
        return self.current_diagnosis
    
    def _get_dim_suggestions(self, dim: str, score: float) -> List[str]:
        """获取维度建议"""
        suggestions = {
            "合规度": ["检查关键词是否违规", "优化产品描述合规性", "确认品类要求"],
            "广告度": ["优化关键词策略", "调整竞价", "检查广告结构"],
            "评论度": ["申请Vine计划", "优化产品品质", "主动评价请求"],
            "视觉度": ["提升主图质量", "增加场景图", "优化信息图"],
            "内容度": ["完善A+内容", "优化要点展示", "丰富FAQ"]
        }
        return suggestions.get(dim, ["进行全面优化"])[:3]
    
    def _generate_priority_fixes(self, issues: List[Dict]) -> List[Dict]:
        """生成优先级修复计划"""
        # 按严重程度和分数排序
        sorted_issues = sorted(issues, key=lambda x: (0 if x["severity"] == "high" else 1, x["score"]))
        
        fixes = []
        for i, issue in enumerate(sorted_issues, 1):
            fixes.append({
                "rank": i,
                "dimension": issue["dimension"],
                "action": self._get_fix_action(issue["dimension"]),
                "timeline": self._get_fix_timeline(issue["score"]),
                "expected_improvement": f"+{15 - i*3}分"
            })
        
        return fixes[:5]
    
    def _get_fix_action(self, dim: str) -> str:
        """获取修复动作"""
        actions = {
            "合规度": "合规自查并修复",
            "广告度": "优化广告投放策略",
            "评论度": "提升评论数量和质量",
            "视觉度": "优化产品图片",
            "内容度": "完善A+和描述"
        }
        return actions.get(dim, "综合优化")
    
    def _get_fix_timeline(self, score: float) -> str:
        """获取修复时间线"""
        if score < 40:
            return "2-4周"
        elif score < 60:
            return "1-2周"
        else:
            return "3-7天"
    
    def benchmark(self, asin: str, competitors: List[str] = None) -> BenchmarkResult:
        """
        ASIN对标分析
        
        Args:
            asin: 目标ASIN
            competitors: 同行ASIN列表
        
        Returns:
            对标结果
        """
        if not self.current_diagnosis:
            return None
        
        if competitors is None:
            competitors = [f"COMP-{i}" for i in range(1, 4)]
        
        # 模拟同行数据
        vs_competitors = []
        for comp in competitors:
            comp_scores = {
                "合规度": self.current_diagnosis.dimensions.get("合规度", 50) + 5,
                "广告度": self.current_diagnosis.dimensions.get("广告度", 50) - 10,
                "评论度": self.current_diagnosis.dimensions.get("评论度", 50) + 15,
                "视觉度": self.current_diagnosis.dimensions.get("视觉度", 50) + 8,
                "内容度": self.current_diagnosis.dimensions.get("内容度", 50) - 5
            }
            
            vs_competitors.append({
                "asin": comp,
                "scores": comp_scores,
                "overall": sum(comp_scores.values()) / len(comp_scores)
            })
        
        # 差距分析
        gap_analysis = self._analyze_gap(self.current_diagnosis.dimensions, vs_competitors)
        
        # 机会识别
        opportunities = [
            "广告策略优化空间大",
            "内容质量可进一步提升",
            "评论数量优势明显"
        ]
        
        return BenchmarkResult(
            asin=asin,
            vs_competitors=vs_competitors,
            gap_analysis=gap_analysis,
            opportunities=opportunities
        )
    
    def _analyze_gap(self, target: Dict, competitors: List[Dict]) -> Dict:
        """分析差距"""
        gaps = {}
        
        for dim in target.keys():
            target_score = target[dim]
            comp_avg = sum(c["scores"].get(dim, 50) for c in competitors) / len(competitors)
            
            gaps[dim] = {
                "target": target_score,
                "competitor_avg": round(comp_avg, 1),
                "gap": round(target_score - comp_avg, 1),
                "status": "ahead" if target_score > comp_avg else "behind" if target_score < comp_avg else "equal"
            }
        
        return gaps
    
    def generate_gantt(self, fixes: List[Dict] = None) -> List[Dict]:
        """
        生成修复优先级甘特图
        
        Args:
            fixes: 修复计划
        
        Returns:
            甘特图数据
        """
        if fixes is None and self.current_diagnosis:
            fixes = self.current_diagnosis.priority_fixes
        
        if not fixes:
            return []
        
        gantt = []
        start_date = datetime.now()
        
        for i, fix in enumerate(fixes):
            duration_days = {
                "2-4周": 21,
                "1-2周": 10,
                "3-7天": 5
            }.get(fix.get("timeline", "1-2周"), 7)
            
            gantt.append({
                "task_id": f"T{i+1}",
                "dimension": fix["dimension"],
                "action": fix["action"],
                "start_date": (start_date + timedelta(days=i*3)).strftime("%Y-%m-%d"),
                "end_date": (start_date + timedelta(days=i*3 + duration_days)).strftime("%Y-%m-%d"),
                "duration_days": duration_days,
                "priority": fix["rank"],
                "progress": 0
            })
        
        return gantt
    
    def generate_weekly_report(self) -> Dict:
        """生成周报模板"""
        if not self.current_diagnosis:
            return {}
        
        diagnosis = self.current_diagnosis
        
        # 计算本周变化
        weekly_change = 0
        if len(self.history_data) >= 2:
            weekly_change = self.history_data[-1]["score"] - self.history_data[-2]["score"]
        
        report = {
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "period": f"第{datetime.now().isocalendar()[1]}周",
            "summary": {
                "asin": diagnosis.asin,
                "overall_score": diagnosis.overall_score,
                "weekly_change": round(weekly_change, 1),
                "score_status": "提升" if weekly_change > 0 else "下降" if weekly_change < 0 else "持平"
            },
            "dimensions": [
                {
                    "name": dim,
                    "score": score,
                    "change": self._get_dimension_change(dim)
                }
                for dim, score in diagnosis.dimensions.items()
            ],
            "issues_summary": {
                "total": len(diagnosis.issues),
                "high_priority": len([i for i in diagnosis.issues if i["severity"] == "high"]),
                "medium_priority": len([i for i in diagnosis.issues if i["severity"] == "medium"])
            },
            "action_items": [
                {
                    "item": f"优化{fix['dimension']}",
                    "action": fix["action"],
                    "timeline": fix["timeline"],
                    "expected": fix["expected_improvement"]
                }
                for fix in diagnosis.priority_fixes[:3]
            ],
            "next_week_plan": [
                "继续关注核心指标",
                "执行优先级最高的修复计划",
                "对比同行数据调整策略"
            ]
        }
        
        return report
    
    def _get_dimension_change(self, dim: str) -> float:
        """获取维度变化"""
        if len(self.history_data) >= 2:
            current = self.history_data[-1]["dimensions"].get(dim, 50)
            previous = self.history_data[-2]["dimensions"].get(dim, 50)
            return round(current - previous, 1)
        return 0
    
    def analyze_trend(self) -> Dict:
        """分析历史趋势"""
        if len(self.history_data) < 2:
            return {"message": "历史数据不足，需要至少2次诊断记录"}
        
        # 整理趋势数据
        trend = {
            "dates": [h["date"] for h in self.history_data],
            "scores": [h["score"] for h in self.history_data],
            "dimensions_trend": {}
        }
        
        # 各维度趋势
        for dim in self.DIMENSION_WEIGHTS.keys():
            trend["dimensions_trend"][dim] = {
                "values": [h["dimensions"].get(dim, 50) for h in self.history_data],
                "change": round(trend["scores"][-1] - self.history_data[0]["dimensions"].get(dim, 50), 1) if self.history_data else 0
            }
        
        # 计算整体趋势
        first_score = self.history_data[0]["score"]
        last_score = self.history_data[-1]["score"]
        trend["overall_change"] = round(last_score - first_score, 1)
        trend["trend_direction"] = "上升" if last_score > first_score else "下降" if last_score < first_score else "持平"
        
        return trend


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python asin-clinic-pro.py <command> [args]")
        print("命令:")
        print("  benchmark      - ASIN对标分析")
        print("  gantt         - 修复甘特图")
        print("  weekly-report - 周报生成")
        print("  trend         - 历史趋势")
        return
    
    command = sys.argv[1]
    clinic = AsinClinicPro()
    
    # 示例诊断数据
    sample_data = {
        "合规度": {"score": 75},
        "广告度": {"score": 55},
        "评论度": {"score": 82},
        "视觉度": {"score": 68},
        "内容度": {"score": 70}
    }
    
    clinic.diagnose("B08N5WRWNW", sample_data)
    
    if command == "benchmark":
        result = clinic.benchmark("B08N5WRWNW", ["COMP-001", "COMP-002", "COMP-003"])
        
        print("=" * 60)
        print("ASIN对标分析")
        print("=" * 60)
        
        print(f"\n目标ASIN: {result.asin}")
        print(f"综合得分: {clinic.current_diagnosis.overall_score}分\n")
        
        print("【与同行对比】")
        for comp in result.vs_competitors:
            print(f"\n  {comp['asin']} (综合: {comp['overall']:.1f}分)")
            for dim, score in comp["scores"].items():
                diff = clinic.current_diagnosis.dimensions[dim] - score
                sign = "+" if diff > 0 else ""
                print(f"    {dim}: {score}分 ({sign}{diff})")
        
        print("\n【差距分析】")
        for dim, gap in result.gap_analysis.items():
            status_icon = "↑" if gap["status"] == "ahead" else "↓" if gap["status"] == "behind" else "="
            print(f"  {status_icon} {dim}: {gap['status']} (差距: {gap['gap']:+})")
    
    elif command == "gantt":
        gantt = clinic.generate_gantt()
        
        print("=" * 60)
        print("修复优先级甘特图")
        print("=" * 60)
        
        for task in gantt:
            bar_len = task["duration_days"] // 3
            bar = "█" * bar_len + "░" * (7 - bar_len)
            print(f"\n  {task['task_id']} {task['dimension']}")
            print(f"     时间: {task['start_date']} ~ {task['end_date']} ({task['duration_days']}天)")
            print(f"     进度: [{bar}] {task['progress']}%")
    
    elif command == "weekly-report":
        report = clinic.generate_weekly_report()
        
        print("=" * 60)
        print(f"运营周报 - {report['period']}")
        print("=" * 60)
        
        summary = report["summary"]
        print(f"\nASIN: {summary['asin']}")
        print(f"综合评分: {summary['overall_score']}分 ({summary['weekly_change']:+})")
        
        print("\n【各维度】")
        for dim in report["dimensions"]:
            print(f"  {dim['name']}: {dim['score']}分 ({dim['change']:+})")
        
        print("\n【问题汇总】")
        issues = report["issues_summary"]
        print(f"  总计: {issues['total']}项")
        print(f"  高优先级: {issues['high_priority']}项")
        print(f"  中优先级: {issues['medium_priority']}项")
        
        print("\n【下周计划】")
        for item in report["next_week_plan"]:
            print(f"  • {item}")
    
    elif command == "trend":
        # 添加一些历史数据
        clinic.history_data.append({
            "date": "2024-01-01",
            "score": 65,
            "dimensions": {"合规度": 70, "广告度": 50, "评论度": 75, "视觉度": 60, "内容度": 65}
        })
        clinic.history_data.append({
            "date": "2024-01-08",
            "score": 68,
            "dimensions": {"合规度": 72, "广告度": 52, "评论度": 78, "视觉度": 65, "内容度": 68}
        })
        
        trend = clinic.analyze_trend()
        
        print("=" * 60)
        print("历史趋势分析")
        print("=" * 60)
        
        print(f"\n整体趋势: {trend['trend_direction']} ({trend['overall_change']:+})")
        
        print("\n【评分变化】")
        for i, date in enumerate(trend["dates"]):
            print(f"  {date}: {trend['scores'][i]}分")
        
        print("\n【各维度变化】")
        for dim, data in trend["dimensions_trend"].items():
            change = data["change"]
            print(f"  {dim}: {change:+}")
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
