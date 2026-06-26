#!/usr/bin/env python3
"""
血糖分析与预测脚本
Blood Glucose Analyzer and Predictor

功能：
- 趋势分析
- 血糖预测
- 风险评估
- 统计报告
- HbA1c 估算
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import statistics

# 默认数据文件路径
DEFAULT_DATA_PATH = Path.home() / ".workbuddy" / "glucose_data.json"


class GlucoseAnalyzer:
    """血糖分析器"""
    
    def __init__(self, data_path: Optional[Path] = None):
        """
        初始化分析器
        
        Args:
            data_path: 数据文件路径
        """
        self.data_path = data_path or DEFAULT_DATA_PATH
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载数据文件"""
        if not self.data_path.exists():
            return {"records": [], "user_profile": {}}
        
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"records": [], "user_profile": {}}
    
    def get_records(self, days: Optional[int] = None) -> List[Dict]:
        """获取记录"""
        records = self.data.get("records", [])
        
        if days:
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            records = [r for r in records if r["timestamp"] >= start_date]
        
        return sorted(records, key=lambda x: x["timestamp"])
    
    def analyze_trends(self, period: str = "short") -> Dict:
        """
        分析血糖趋势
        
        Args:
            period: 分析周期 (short/medium/long)
                short: 7天
                medium: 30天
                long: 90天
        
        Returns:
            趋势分析结果
        """
        period_days = {
            "short": 7,
            "medium": 30,
            "long": 90
        }
        
        days = period_days.get(period, 7)
        records = self.get_records(days)
        
        if len(records) < 3:
            return {
                "success": False,
                "message": f"数据不足，至少需要3条记录（当前{len(records)}条）"
            }
        
        # 按时间排序
        values = [r["glucose_value"] for r in records]
        timestamps = [datetime.fromisoformat(r["timestamp"]) for r in records]
        
        # 计算趋势
        trend_direction = self._calculate_trend_direction(values)
        
        # 按时段分析
        time_period_analysis = self._analyze_by_time_period(records)
        
        # 移动平均
        moving_avg = self._calculate_moving_average(values, window=min(5, len(values)))
        
        # 波动分析
        volatility = self._calculate_volatility(values)
        
        return {
            "success": True,
            "period": period,
            "days": days,
            "total_records": len(records),
            "trend_direction": trend_direction,  # "increasing" / "decreasing" / "stable"
            "avg_glucose": round(statistics.mean(values), 1),
            "latest_glucose": values[-1],
            "time_period_analysis": time_period_analysis,
            "moving_average": moving_avg,
            "volatility": volatility,
            "change_rate": self._calculate_change_rate(values, timestamps)
        }
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """计算趋势方向"""
        if len(values) < 3:
            return "stable"
        
        # 简单线性趋势判断
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        diff = second_avg - first_avg
        
        if diff > 0.5:
            return "increasing"
        elif diff < -0.5:
            return "decreasing"
        else:
            return "stable"
    
    def _analyze_by_time_period(self, records: List[Dict]) -> Dict:
        """按时段分析"""
        periods = defaultdict(list)
        
        for record in records:
            r_type = record.get("measurement_type", "random")
            periods[r_type].append(record["glucose_value"])
        
        result = {}
        for period_name, values in periods.items():
            if values:
                result[period_name] = {
                    "count": len(values),
                    "avg": round(statistics.mean(values), 1),
                    "min": min(values),
                    "max": max(values)
                }
        
        return result
    
    def _calculate_moving_average(self, values: List[float], window: int = 5) -> List[float]:
        """计算移动平均"""
        if len(values) < window:
            return [round(statistics.mean(values), 1)]
        
        moving_avg = []
        for i in range(len(values) - window + 1):
            window_values = values[i:i+window]
            moving_avg.append(round(statistics.mean(window_values), 1))
        
        return moving_avg
    
    def _calculate_volatility(self, values: List[float]) -> float:
        """计算波动性（标准差）"""
        if len(values) < 2:
            return 0.0
        
        return round(statistics.stdev(values), 2)
    
    def _calculate_change_rate(self, values: List[float], timestamps: List[datetime]) -> float:
        """计算变化率（mmol/L/天）"""
        if len(values) < 2:
            return 0.0
        
        # 简单线性回归
        first_value = values[0]
        last_value = values[-1]
        first_time = timestamps[0]
        last_time = timestamps[-1]
        
        days_diff = (last_time - first_time).total_seconds() / 86400
        
        if days_diff == 0:
            return 0.0
        
        return round((last_value - first_value) / days_diff, 2)
    
    def predict_glucose(self, hours_ahead: int = 3) -> Dict:
        """
        预测未来血糖
        
        Args:
            hours_ahead: 预测未来多少小时
        
        Returns:
            预测结果
        """
        # 获取最近的记录
        recent_records = self.get_records(days=3)
        
        if len(recent_records) < 3:
            return {
                "success": False,
                "message": "数据不足，至少需要3条最近记录才能预测"
            }
        
        # 最近24小时的记录
        now = datetime.now()
        last_24h_records = [
            r for r in recent_records
            if (now - datetime.fromisoformat(r["timestamp"])).total_seconds() <= 86400
        ]
        
        if len(last_24h_records) < 2:
            last_24h_records = recent_records[-5:]  # 取最近5条
        
        values = [r["glucose_value"] for r in last_24h_records]
        timestamps = [datetime.fromisoformat(r["timestamp"]) for r in last_24h_records]
        
        # 当前血糖
        current_glucose = values[-1]
        
        # 计算平均变化率
        if len(values) >= 2:
            # 计算每小时平均变化
            hourly_changes = []
            for i in range(1, len(values)):
                time_diff = (timestamps[i] - timestamps[i-1]).total_seconds() / 3600
                if time_diff > 0:
                    glucose_change = values[i] - values[i-1]
                    hourly_rate = glucose_change / time_diff
                    hourly_changes.append(hourly_rate)
            
            if hourly_changes:
                avg_hourly_rate = statistics.mean(hourly_changes)
            else:
                avg_hourly_rate = 0
        else:
            avg_hourly_rate = 0
        
        # 预测
        predicted_change = avg_hourly_rate * hours_ahead
        predicted_glucose = current_glucose + predicted_change
        
        # 考虑时段规律调整
        current_hour = now.hour
        time_adjustment = self._get_time_adjustment(current_hour, hours_ahead)
        predicted_glucose += time_adjustment
        
        # 限制预测范围（合理范围内）
        predicted_glucose = max(3.0, min(15.0, predicted_glucose))
        
        # 预测置信度
        confidence = self._calculate_prediction_confidence(len(last_24h_records), hours_ahead)
        
        return {
            "success": True,
            "current_glucose": current_glucose,
            "predicted_glucose": round(predicted_glucose, 1),
            "hours_ahead": hours_ahead,
            "prediction_time": (now + timedelta(hours=hours_ahead)).isoformat(),
            "trend": "上升" if avg_hourly_rate > 0.1 else ("下降" if avg_hourly_rate < -0.1 else "稳定"),
            "confidence": confidence,
            "factors": {
                "average_hourly_change": round(avg_hourly_rate, 2),
                "time_adjustment": round(time_adjustment, 1),
                "recent_values_count": len(last_24h_records)
            }
        }
    
    def _get_time_adjustment(self, current_hour: int, hours_ahead: int) -> float:
        """获取时段调整因子"""
        # 根据时段规律调整预测
        # 默认假设：
        # - 夜间（0-6点）血糖相对稳定或略降
        # - 早晨（6-9点）可能升高（黎明现象）
        # - 餐后（早餐后约9-10点，午餐后约13-14点，晚餐后约19-20点）可能升高
        
        future_hour = (current_hour + hours_ahead) % 24
        
        # 黎明现象时段
        if 5 <= future_hour <= 8:
            return 0.5  # 预期上升
        # 深夜
        elif 0 <= future_hour <= 5:
            return -0.3  # 预期略降
        else:
            return 0.0
    
    def _calculate_prediction_confidence(self, data_points: int, hours_ahead: int) -> str:
        """计算预测置信度"""
        # 数据点越多、预测时间越短，置信度越高
        if data_points >= 5 and hours_ahead <= 3:
            return "高"
        elif data_points >= 3 and hours_ahead <= 6:
            return "中等"
        else:
            return "低"
    
    def predict_post_meal_peak(self, pre_meal_glucose: float, carbs_g: float) -> Dict:
        """
        预测餐后血糖峰值
        
        Args:
            pre_meal_glucose: 餐前血糖 (mmol/L)
            carbs_g: 碳水化合物摄入量 (克)
        
        Returns:
            预测结果
        """
        # 简化模型：每10克碳水约升高血糖 1.5-2.5 mmol/L
        # 个体差异大，这里使用中等估算值
        glucose_rise_per_10g_carbs = 2.0
        
        # 计算预期血糖上升
        expected_rise = (carbs_g / 10) * glucose_rise_per_10g_carbs
        
        # 考虑餐前血糖水平调整
        if pre_meal_glucose > 10:
            # 高血糖时，上升幅度可能更大
            expected_rise *= 1.2
        elif pre_meal_glucose < 5:
            # 低血糖时，上升幅度可能较小（身体会优先补充）
            expected_rise *= 0.9
        
        peak_glucose = pre_meal_glucose + expected_rise
        
        # 峰值时间（通常餐后1-2小时）
        peak_time_minutes = 60 + int(carbs_g / 20) * 15  # 碳水越多，峰值越晚
        
        return {
            "success": True,
            "pre_meal_glucose": pre_meal_glucose,
            "carbs_g": carbs_g,
            "predicted_peak": round(peak_glucose, 1),
            "expected_rise": round(expected_rise, 1),
            "peak_time_minutes": peak_time_minutes,
            "peak_time_str": f"餐后约 {peak_time_minutes // 60} 小时 {peak_time_minutes % 60} 分钟",
            "risk_level": self._assess_peak_risk(peak_glucose)
        }
    
    def _assess_peak_risk(self, peak_glucose: float) -> str:
        """评估峰值风险"""
        if peak_glucose > 13.9:
            return "高风险"
        elif peak_glucose > 11.1:
            return "中等风险"
        elif peak_glucose > 10.0:
            return "轻度风险"
        else:
            return "正常"
    
    def assess_risks(self, days: int = 30) -> Dict:
        """
        评估血糖风险
        
        Args:
            days: 评估最近多少天
        
        Returns:
            风险评估结果
        """
        records = self.get_records(days)
        
        if not records:
            return {
                "success": False,
                "message": "无数据"
            }
        
        values = [r["glucose_value"] for r in records]
        
        # 统计低血糖事件
        hypoglycemia_events = [v for v in values if v < 3.9]
        hypoglycemia_count = len(hypoglycemia_events)
        
        # 统计高血糖事件
        hyperglycemia_events = [v for v in values if v > 11.1]
        hyperglycemia_count = len(hyperglycemia_events)
        
        # 严重高血糖事件
        severe_hyper_events = [v for v in values if v > 13.9]
        
        # 目标范围内时间
        in_range = [v for v in values if 4.4 <= v <= 10.0]
        time_in_range = round(len(in_range) / len(values) * 100, 1)
        
        # 识别风险时段
        risk_periods = self._identify_risk_periods(records)
        
        # 总体风险评分
        risk_score = self._calculate_overall_risk(
            hypoglycemia_count,
            hyperglycemia_count,
            len(severe_hyper_events),
            time_in_range,
            len(values)
        )
        
        return {
            "success": True,
            "period_days": days,
            "total_readings": len(values),
            "hypoglycemia": {
                "count": hypoglycemia_count,
                "percentage": round(hypoglycemia_count / len(values) * 100, 1),
                "min_value": min(hypoglycemia_events) if hypoglycemia_events else None,
                "risk": "高" if hypoglycemia_count >= 3 else ("中" if hypoglycemia_count >= 1 else "低")
            },
            "hyperglycemia": {
                "count": hyperglycemia_count,
                "percentage": round(hyperglycemia_count / len(values) * 100, 1),
                "max_value": max(hyperglycemia_events) if hyperglycemia_events else None,
                "severe_count": len(severe_hyper_events),
                "risk": "高" if hyperglycemia_count >= 5 else ("中" if hyperglycemia_count >= 2 else "低")
            },
            "time_in_range": time_in_range,
            "risk_periods": risk_periods,
            "overall_risk_score": risk_score,
            "overall_risk_level": self._risk_score_to_level(risk_score)
        }
    
    def _identify_risk_periods(self, records: List[Dict]) -> List[Dict]:
        """识别风险时段"""
        # 按小时统计
        hour_stats = defaultdict(list)
        
        for record in records:
            hour = datetime.fromisoformat(record["timestamp"]).hour
            hour_stats[hour].append(record["glucose_value"])
        
        risk_periods = []
        
        for hour, values in hour_stats.items():
            avg = statistics.mean(values)
            
            # 检查是否为风险时段
            if avg < 5.0:
                risk_periods.append({
                    "hour": hour,
                    "time_range": f"{hour}:00-{hour+1}:00",
                    "avg_glucose": round(avg, 1),
                    "risk_type": "低血糖风险",
                    "readings_count": len(values)
                })
            elif avg > 10.0:
                risk_periods.append({
                    "hour": hour,
                    "time_range": f"{hour}:00-{hour+1}:00",
                    "avg_glucose": round(avg, 1),
                    "risk_type": "高血糖风险",
                    "readings_count": len(values)
                })
        
        return sorted(risk_periods, key=lambda x: x["avg_glucose"], reverse=True)
    
    def _calculate_overall_risk(
        self,
        hypo_count: int,
        hyper_count: int,
        severe_hyper_count: int,
        time_in_range: float,
        total_readings: int
    ) -> float:
        """计算总体风险评分（0-100，越高越危险）"""
        score = 0
        
        # 低血糖贡献
        score += hypo_count * 10
        
        # 高血糖贡献
        score += hyper_count * 5
        score += severe_hyper_count * 10
        
        # 时间范围内贡献
        if time_in_range < 50:
            score += 20
        elif time_in_range < 70:
            score += 10
        
        # 限制最大值
        return min(100, score)
    
    def _risk_score_to_level(self, score: float) -> str:
        """将风险评分转换为等级"""
        if score >= 60:
            return "高风险"
        elif score >= 30:
            return "中等风险"
        else:
            return "低风险"
    
    def generate_statistics(self, days: int = 30) -> Dict:
        """
        生成血糖统计报告
        
        Args:
            days: 统计最近多少天
        
        Returns:
            统计报告
        """
        records = self.get_records(days)
        
        if not records:
            return {
                "success": False,
                "message": "无数据"
            }
        
        values = [r["glucose_value"] for r in records]
        
        # 基础统计
        stats = {
            "success": True,
            "period": f"最近 {days} 天",
            "total_readings": len(records),
            "basic_stats": {
                "average": round(statistics.mean(values), 1),
                "median": round(statistics.median(values), 1),
                "min": min(values),
                "max": max(values),
                "std_dev": round(statistics.stdev(values), 2) if len(values) > 1 else 0,
                "range": round(max(values) - min(values), 1)
            }
        }
        
        # 按测量类型统计
        type_stats = defaultdict(list)
        for record in records:
            m_type = record.get("measurement_type", "random")
            type_stats[m_type].append(record["glucose_value"])
        
        stats["by_measurement_type"] = {}
        for m_type, vals in type_stats.items():
            stats["by_measurement_type"][m_type] = {
                "count": len(vals),
                "average": round(statistics.mean(vals), 1),
                "min": min(vals),
                "max": max(vals)
            }
        
        # 按日期统计
        daily_stats = defaultdict(list)
        for record in records:
            date = datetime.fromisoformat(record["timestamp"]).strftime("%Y-%m-%d")
            daily_stats[date].append(record["glucose_value"])
        
        stats["daily_summary"] = {}
        for date, vals in sorted(daily_stats.items(), reverse=True)[:7]:  # 最近7天
            stats["daily_summary"][date] = {
                "readings": len(vals),
                "average": round(statistics.mean(vals), 1)
            }
        
        # 目标范围分析
        target_min = self.data.get("user_profile", {}).get("target_range", {}).get("fasting_min", 4.4)
        target_max = self.data.get("user_profile", {}).get("target_range", {}).get("post_meal_max", 10.0)
        
        in_range = [v for v in values if target_min <= v <= target_max]
        below_range = [v for v in values if v < target_min]
        above_range = [v for v in values if v > target_max]
        
        stats["target_range_analysis"] = {
            "target_range": f"{target_min}-{target_max} mmol/L",
            "in_range": {
                "count": len(in_range),
                "percentage": round(len(in_range) / len(values) * 100, 1)
            },
            "below_range": {
                "count": len(below_range),
                "percentage": round(len(below_range) / len(values) * 100, 1)
            },
            "above_range": {
                "count": len(above_range),
                "percentage": round(len(above_range) / len(values) * 100, 1)
            }
        }
        
        return stats
    
    def estimate_hba1c(self) -> Dict:
        """
        估算糖化血红蛋白 (HbA1c)
        
        基于最近2-3个月的平均血糖估算
        
        Returns:
            HbA1c 估算结果
        """
        # 获取最近90天的数据
        records = self.get_records(days=90)
        
        if len(records) < 10:
            return {
                "success": False,
                "message": "数据不足，至少需要10条记录才能估算HbA1c"
            }
        
        values = [r["glucose_value"] for r in records]
        avg_glucose = statistics.mean(values)
        
        # 使用 ADAG 公式估算
        # HbA1c (%) = (Average Glucose (mmol/L) + 2.59) / 1.59
        estimated_hba1c = (avg_glucose + 2.59) / 1.59
        
        # 评估
        if estimated_hba1c < 7.0:
            assessment = "理想范围，血糖控制良好"
            status = "good"
        elif estimated_hba1c < 7.5:
            assessment = "可接受范围，建议继续努力改善"
            status = "acceptable"
        elif estimated_hba1c < 8.0:
            assessment = "需要改善，建议咨询医生调整治疗方案"
            status = "needs_improvement"
        else:
            assessment = "控制不佳，强烈建议就医评估"
            status = "poor"
        
        return {
            "success": True,
            "estimated_hba1c": round(estimated_hba1c, 1),
            "unit": "%",
            "avg_glucose_used": round(avg_glucose, 1),
            "records_count": len(records),
            "period_days": min(90, (datetime.fromisoformat(records[-1]["timestamp"]) - 
                                    datetime.fromisoformat(records[0]["timestamp"])).days),
            "assessment": assessment,
            "status": status,
            "note": "这是基于平均血糖的估算值，实际HbA1c需通过血液检测获得"
        }


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python glucose_analyzer.py trends [short/medium/long]")
        print("  python glucose_analyzer.py predict [hours]")
        print("  python glucose_analyzer.py risks [days]")
        print("  python glucose_analyzer.py stats [days]")
        print("  python glucose_analyzer.py hba1c")
        return
    
    analyzer = GlucoseAnalyzer()
    command = sys.argv[1]
    
    if command == "trends":
        period = sys.argv[2] if len(sys.argv) > 2 else "short"
        result = analyzer.analyze_trends(period)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "predict":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        result = analyzer.predict_glucose(hours)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "risks":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        result = analyzer.assess_risks(days)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "stats":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        result = analyzer.generate_statistics(days)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "hba1c":
        result = analyzer.estimate_hba1c()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
