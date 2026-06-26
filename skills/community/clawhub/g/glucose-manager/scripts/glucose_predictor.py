"""
Blood Glucose Predictor
Provides predictions and trend analysis for blood glucose data
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import statistics


class BloodGlucosePredictor:
    """Predicts blood glucose trends and patterns"""
    
    def __init__(self, data_manager):
        """
        Initialize the predictor
        
        Args:
            data_manager: BloodGlucoseDataManager instance
        """
        self.data_manager = data_manager
    
    def predict_next_hours(
        self,
        hours: int = 4,
        context: str = None
    ) -> Dict:
        """
        Predict blood glucose for the next few hours
        
        Args:
            hours: Number of hours to predict (1-8)
            context: Current context ('before_meal', 'after_meal', etc.)
        
        Returns:
            Prediction with confidence intervals
        """
        # Get recent data
        recent_records = self.data_manager.get_glucose_records(limit=20)
        
        if len(recent_records) < 3:
            return {
                "prediction": None,
                "confidence": "low",
                "message": "需要至少3条记录才能进行预测"
            }
        
        # Simple trend-based prediction
        recent_values = [r["value"] for r in recent_records[:5]]
        trend = self._calculate_trend(recent_values)
        
        # Get user's typical patterns
        patterns = self._analyze_patterns()
        
        # Current glucose
        current_glucose = recent_records[0]["value"]
        
        # Predict based on context and time
        predictions = []
        for hour in range(1, hours + 1):
            predicted_value = current_glucose + (trend * hour)
            
            # Adjust based on typical patterns
            hour_of_day = (datetime.now() + timedelta(hours=hour)).hour
            if hour_of_day in patterns["hourly_patterns"]:
                adjustment = patterns["hourly_patterns"][hour_of_day] - statistics.mean(recent_values)
                predicted_value += adjustment * 0.3
            
            # Add confidence interval
            confidence_range = self._calculate_confidence_range(recent_values, hour)
            
            predictions.append({
                "hours_ahead": hour,
                "predicted_value": round(predicted_value, 1),
                "confidence_range": {
                    "min": round(predicted_value - confidence_range, 1),
                    "max": round(predicted_value + confidence_range, 1)
                }
            })
        
        # Determine overall risk
        risk_level = self._assess_risk(predictions)
        
        return {
            "current_glucose": current_glucose,
            "trend": trend,
            "predictions": predictions,
            "risk_level": risk_level,
            "confidence": self._get_confidence_level(len(recent_records)),
            "recommendations": self._generate_prediction_recommendations(predictions, context)
        }
    
    def predict_post_meal_peak(
        self,
        current_glucose: float,
        meal_carbs: float,
        meal_type: str = "regular"
    ) -> Dict:
        """
        Predict post-meal blood glucose peak
        
        Args:
            current_glucose: Current blood glucose level (mmol/L)
            meal_carbs: Estimated carbohydrates in meal (grams)
            meal_type: 'breakfast', 'lunch', 'dinner', 'snack'
        
        Returns:
            Prediction of peak glucose and timing
        """
        # Typical glucose response factors
        # These are simplified estimates - real predictions would need more data
        carb_to_glucose_factor = 0.056  # mmol/L per gram of carbs (simplified)
        
        # Time to peak varies by meal
        peak_times = {
            "breakfast": 90,  # minutes
            "lunch": 75,
            "dinner": 90,
            "snack": 60,
            "regular": 75
        }
        
        # Peak glucose calculation (simplified)
        # In reality, this depends on many factors: insulin sensitivity, GI of foods, etc.
        expected_increase = meal_carbs * carb_to_glucose_factor
        
        # Adjust for individual patterns
        patterns = self._analyze_patterns()
        if patterns["avg_post_meal_increase"]:
            # Use historical average if available
            historical_factor = patterns["avg_post_meal_increase"] / (30 * carb_to_glucose_factor)
            expected_increase = expected_increase * historical_factor
        
        predicted_peak = current_glucose + expected_increase
        time_to_peak = peak_times.get(meal_type, peak_times["regular"])
        
        return {
            "current_glucose": current_glucose,
            "predicted_peak": round(predicted_peak, 1),
            "expected_increase": round(expected_increase, 1),
            "time_to_peak_minutes": time_to_peak,
            "peak_time": (datetime.now() + timedelta(minutes=time_to_peak)).isoformat(),
            "risk_assessment": self._assess_peak_risk(predicted_peak)
        }
    
    def identify_risk_periods(self, days: int = 14) -> Dict:
        """
        Identify periods with high risk of hypo/hyperglycemia
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Risk periods and patterns
        """
        records = self.data_manager.get_glucose_records(
            start_date=(datetime.now() - timedelta(days=days)).isoformat()
        )
        
        if not records:
            return {
                "message": "数据不足,无法识别风险时段"
            }
        
        target_range = self.data_manager.get_user_profile()["target_range"]
        
        # Analyze by time of day
        hourly_data = {}
        for record in records:
            hour = datetime.fromisoformat(record["timestamp"]).hour
            if hour not in hourly_data:
                hourly_data[hour] = []
            hourly_data[hour].append(record["value"])
        
        # Identify risk periods
        hypo_risk_hours = []
        hyper_risk_hours = []
        
        for hour, values in hourly_data.items():
            avg = statistics.mean(values)
            below_range = sum(1 for v in values if v < target_range["min"])
            above_range = sum(1 for v in values if v > target_range["max"])
            
            if below_range / len(values) > 0.3:  # More than 30% below range
                hypo_risk_hours.append({
                    "hour": hour,
                    "average": round(avg, 1),
                    "low_percentage": round(below_range / len(values) * 100, 1)
                })
            
            if above_range / len(values) > 0.3:  # More than 30% above range
                hyper_risk_hours.append({
                    "hour": hour,
                    "average": round(avg, 1),
                    "high_percentage": round(above_range / len(values) * 100, 1)
                })
        
        return {
            "hypoglycemia_risk_periods": sorted(hypo_risk_hours, key=lambda x: x["hour"]),
            "hyperglycemia_risk_periods": sorted(hyper_risk_hours, key=lambda x: x["hour"]),
            "target_range": target_range,
            "analysis_period_days": days,
            "total_records_analyzed": len(records)
        }
    
    def analyze_trends(self, days: int = 30) -> Dict:
        """
        Analyze long-term trends in blood glucose
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Trend analysis results
        """
        records = self.data_manager.get_glucose_records(
            start_date=(datetime.now() - timedelta(days=days)).isoformat()
        )
        
        if len(records) < 7:
            return {
                "message": "需要至少7条记录才能进行趋势分析"
            }
        
        # Group by day
        daily_data = {}
        for record in records:
            date = datetime.fromisoformat(record["timestamp"]).date().isoformat()
            if date not in daily_data:
                daily_data[date] = []
            daily_data[date].append(record["value"])
        
        # Calculate daily averages
        daily_averages = []
        for date in sorted(daily_data.keys()):
            daily_averages.append({
                "date": date,
                "average": statistics.mean(daily_data[date]),
                "readings": len(daily_data[date])
            })
        
        # Calculate overall trend
        if len(daily_averages) >= 3:
            recent_avg = statistics.mean([d["average"] for d in daily_averages[-7:]])
            earlier_avg = statistics.mean([d["average"] for d in daily_averages[:7]])
            trend_direction = "上升" if recent_avg > earlier_avg else "下降" if recent_avg < earlier_avg else "稳定"
            trend_change = abs(recent_avg - earlier_avg)
        else:
            trend_direction = "数据不足"
            trend_change = 0
            recent_avg = 0
            earlier_avg = 0
        
        # Time in range
        target_range = self.data_manager.get_user_profile()["target_range"]
        all_values = [r["value"] for r in records]
        in_range = sum(1 for v in all_values if target_range["min"] <= v <= target_range["max"])
        time_in_range = (in_range / len(all_values)) * 100
        
        return {
            "trend_direction": trend_direction,
            "trend_change": round(trend_change, 2),
            "average_glucose": round(statistics.mean(all_values), 1),
            "time_in_range_percentage": round(time_in_range, 1),
            "daily_averages": daily_averages,
            "analysis_period_days": days,
            "total_readings": len(records)
        }
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend from recent values"""
        if len(values) < 2:
            return 0
        
        # Simple linear regression
        n = len(values)
        x = list(range(n))
        y = values
        
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0
        
        slope = numerator / denominator
        return slope
    
    def _calculate_confidence_range(self, recent_values: List[float], hours_ahead: int) -> float:
        """Calculate confidence range for prediction"""
        # Simplified: wider range for further predictions
        base_range = statistics.stdev(recent_values) if len(recent_values) > 1 else 1.0
        return base_range * (1 + hours_ahead * 0.2)
    
    def _analyze_patterns(self) -> Dict:
        """Analyze historical patterns"""
        records = self.data_manager.get_glucose_records(limit=100)
        
        patterns = {
            "hourly_patterns": {},
            "avg_post_meal_increase": None
        }
        
        if not records:
            return patterns
        
        # Analyze by hour
        hourly = {}
        for record in records:
            hour = datetime.fromisoformat(record["timestamp"]).hour
            if hour not in hourly:
                hourly[hour] = []
            hourly[hour].append(record["value"])
        
        patterns["hourly_patterns"] = {
            hour: statistics.mean(values) for hour, values in hourly.items()
        }
        
        # Analyze post-meal increases
        meal_contexts = [r for r in records if r.get("meal_context") == "after_meal"]
        if meal_contexts:
            # Simplified: would need before/after pairs for accurate calculation
            patterns["avg_post_meal_increase"] = statistics.mean(
                [r["value"] for r in meal_contexts]
            )
        
        return patterns
    
    def _assess_risk(self, predictions: List[Dict]) -> str:
        """Assess overall risk level"""
        target_range = self.data_manager.get_user_profile()["target_range"]
        
        for pred in predictions:
            if pred["predicted_value"] < target_range["min"] - 1:
                return "低血糖风险"
            if pred["predicted_value"] > target_range["max"] + 3:
                return "高血糖风险"
        
        return "正常范围"
    
    def _assess_peak_risk(self, predicted_peak: float) -> str:
        """Assess risk for predicted peak"""
        target_range = self.data_manager.get_user_profile()["target_range"]
        
        if predicted_peak < target_range["min"]:
            return "过低"
        elif predicted_peak > 10.0:
            return "显著升高"
        elif predicted_peak > target_range["max"]:
            return "偏高"
        else:
            return "正常"
    
    def _get_confidence_level(self, num_records: int) -> str:
        """Get confidence level based on data quantity"""
        if num_records >= 50:
            return "高"
        elif num_records >= 20:
            return "中"
        elif num_records >= 5:
            return "低"
        else:
            return "很低"
    
    def _generate_prediction_recommendations(
        self,
        predictions: List[Dict],
        context: str
    ) -> List[str]:
        """Generate recommendations based on predictions"""
        recommendations = []
        target_range = self.data_manager.get_user_profile()["target_range"]
        
        for pred in predictions:
            if pred["predicted_value"] < target_range["min"]:
                recommendations.append(
                    f"{pred['hours_ahead']}小时后可能出现低血糖({pred['predicted_value']} mmol/L),建议适当补充碳水化合物"
                )
                break
            elif pred["predicted_value"] > target_range["max"] + 3:
                recommendations.append(
                    f"{pred['hours_ahead']}小时后血糖可能偏高({pred['predicted_value']} mmol/L),建议增加运动或调整饮食"
                )
        
        if not recommendations:
            recommendations.append("预测血糖在目标范围内,继续保持良好习惯")
        
        return recommendations


if __name__ == '__main__':
    # Test the predictor
    from data_manager import BloodGlucoseDataManager
    
    manager = BloodGlucoseDataManager()
    predictor = BloodGlucosePredictor(manager)
    
    # Test prediction
    print("=== 预测未来4小时血糖 ===")
    result = predictor.predict_next_hours(hours=4)
    print(json.dumps(result, indent=2, ensure_ascii=False))
