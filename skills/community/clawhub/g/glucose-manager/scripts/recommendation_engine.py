"""
Blood Glucose Recommendation Engine
Generates personalized recommendations for blood glucose management
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import statistics


class RecommendationEngine:
    """Generates personalized blood glucose management recommendations"""
    
    def __init__(self, data_manager, predictor):
        """
        Initialize recommendation engine
        
        Args:
            data_manager: BloodGlucoseDataManager instance
            predictor: BloodGlucosePredictor instance
        """
        self.data_manager = data_manager
        self.predictor = predictor
    
    def get_comprehensive_recommendations(self) -> Dict:
        """
        Get comprehensive recommendations based on current status
        
        Returns:
            Dictionary with categorized recommendations
        """
        # Get recent data
        recent_records = self.data_manager.get_glucose_records(limit=10)
        stats = self.data_manager.get_statistics(days=7)
        trends = self.predictor.analyze_trends(days=30)
        risk_periods = self.predictor.identify_risk_periods(days=14)
        
        recommendations = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": self._assess_overall_status(stats, trends),
            "immediate_actions": [],
            "diet_recommendations": [],
            "exercise_recommendations": [],
            "medication_reminders": [],
            "monitoring_suggestions": [],
            "lifestyle_tips": [],
            "warnings": []
        }
        
        if not recent_records:
            recommendations["immediate_actions"].append(
                "开始记录血糖数据以获得个性化建议"
            )
            return recommendations
        
        current_glucose = recent_records[0]["value"]
        target_range = self.data_manager.get_user_profile()["target_range"]
        
        # Immediate actions based on current glucose
        recommendations["immediate_actions"] = self._get_immediate_actions(
            current_glucose, target_range
        )
        
        # Diet recommendations
        recommendations["diet_recommendations"] = self._get_diet_recommendations(
            stats, trends, risk_periods
        )
        
        # Exercise recommendations
        recommendations["exercise_recommendations"] = self._get_exercise_recommendations(
            current_glucose, stats, target_range
        )
        
        # Medication reminders
        recommendations["medication_reminders"] = self._get_medication_reminders()
        
        # Monitoring suggestions
        recommendations["monitoring_suggestions"] = self._get_monitoring_suggestions(
            stats, risk_periods
        )
        
        # Lifestyle tips
        recommendations["lifestyle_tips"] = self._get_lifestyle_tips(trends)
        
        # Warnings
        recommendations["warnings"] = self._get_warnings(stats, trends, risk_periods)
        
        return recommendations
    
    def get_meal_suggestion(self, meal_type: str, current_glucose: float = None) -> Dict:
        """
        Get meal suggestions based on current glucose and time
        
        Args:
            meal_type: 'breakfast', 'lunch', 'dinner', 'snack'
            current_glucose: Current blood glucose level
        
        Returns:
            Meal recommendations
        """
        target_range = self.data_manager.get_user_profile()["target_range"]
        
        # Get recent glucose patterns for this meal time
        recent_records = self.data_manager.get_glucose_records(limit=30)
        meal_hour_ranges = {
            "breakfast": (6, 9),
            "lunch": (11, 14),
            "dinner": (17, 20),
            "snack": None
        }
        
        suggestion = {
            "meal_type": meal_type,
            "carbohydrate_range": self._get_carb_range(current_glucose, meal_type),
            "food_suggestions": [],
            "timing_suggestion": None,
            "pre_meal_glucose_target": None,
            "warnings": []
        }
        
        # Adjust based on current glucose
        if current_glucose:
            if current_glucose > target_range["max"]:
                suggestion["warnings"].append(
                    f"当前血糖偏高({current_glucose} mmol/L),建议减少碳水化合物摄入"
                )
                suggestion["carbohydrate_range"]["max"] -= 15
                
            elif current_glucose < target_range["min"]:
                suggestion["warnings"].append(
                    f"当前血糖偏低({current_glucose} mmol/L),建议先补充少量碳水化合物"
                )
                suggestion["pre_meal_glucose_target"] = "建议先摄入15g速效碳水化合物,等待15分钟后再用餐"
        
        # Meal-specific suggestions
        suggestion["food_suggestions"] = self._get_food_suggestions(
            meal_type, current_glucose, target_range
        )
        
        # Timing suggestion
        if meal_hour_ranges[meal_type]:
            suggestion["timing_suggestion"] = f"建议在{meal_hour_ranges[meal_type][0]}:00-{meal_hour_ranges[meal_type][1]}:00之间用餐"
        
        return suggestion
    
    def get_exercise_suggestion(self, current_glucose: float = None) -> Dict:
        """
        Get exercise suggestions based on current glucose
        
        Args:
            current_glucose: Current blood glucose level
        
        Returns:
            Exercise recommendations
        """
        target_range = self.data_manager.get_user_profile()["target_range"]
        
        suggestion = {
            "suitable": True,
            "exercise_types": [],
            "duration_minutes": None,
            "intensity": None,
            "timing": None,
            "precautions": [],
            "warnings": []
        }
        
        if not current_glucose:
            suggestion["warnings"].append("建议先测量血糖再决定运动计划")
            return suggestion
        
        # Determine exercise suitability
        if current_glucose < 4.0:
            suggestion["suitable"] = False
            suggestion["warnings"].append(
                f"血糖过低({current_glucose} mmol/L),不适合运动。请先补充15-30g碳水化合物"
            )
            suggestion["precautions"].append(
                "等待血糖升至5.0 mmol/L以上再开始运动"
            )
            
        elif current_glucose < 5.0:
            suggestion["suitable"] = True
            suggestion["warnings"].append(
                f"血糖偏低({current_glucose} mmol/L),运动前建议先补充少量碳水化合物"
            )
            suggestion["exercise_types"] = ["散步", "瑜伽", "轻度拉伸"]
            suggestion["duration_minutes"] = 20
            suggestion["intensity"] = "低强度"
            suggestion["precautions"].append("准备含糖零食以备不时之需")
            
        elif current_glucose <= target_range["max"]:
            suggestion["suitable"] = True
            suggestion["exercise_types"] = ["快走", "慢跑", "游泳", "骑车", "健身操"]
            suggestion["duration_minutes"] = 30
            suggestion["intensity"] = "中等强度"
            suggestion["timing"] = "餐后1-2小时是运动的最佳时机"
            
        elif current_glucose <= 15.0:
            suggestion["suitable"] = True
            suggestion["warnings"].append(
                f"血糖偏高({current_glucose} mmol/L),运动有助于降低血糖"
            )
            suggestion["exercise_types"] = ["快走", "慢跑", "游泳", "骑车"]
            suggestion["duration_minutes"] = 30
            suggestion["intensity"] = "中等强度"
            suggestion["precautions"].append("注意补充水分")
            
        else:
            suggestion["suitable"] = False
            suggestion["warnings"].append(
                f"血糖过高({current_glucose} mmol/L),建议先咨询医生"
            )
            suggestion["precautions"].append("检测尿酮体,如阳性则避免运动")
        
        return suggestion
    
    def analyze_and_recommend(self) -> str:
        """
        Generate a comprehensive analysis report with recommendations
        
        Returns:
            Formatted analysis report
        """
        recommendations = self.get_comprehensive_recommendations()
        
        report = []
        report.append("=" * 50)
        report.append("血糖管理分析与建议报告")
        report.append("=" * 50)
        report.append(f"\n生成时间: {recommendations['timestamp']}")
        report.append(f"\n整体状态: {recommendations['overall_status']}")
        
        if recommendations["warnings"]:
            report.append("\n⚠️  警告:")
            for warning in recommendations["warnings"]:
                report.append(f"  • {warning}")
        
        if recommendations["immediate_actions"]:
            report.append("\n🎯 立即行动:")
            for action in recommendations["immediate_actions"]:
                report.append(f"  • {action}")
        
        if recommendations["diet_recommendations"]:
            report.append("\n🍎 饮食建议:")
            for rec in recommendations["diet_recommendations"]:
                report.append(f"  • {rec}")
        
        if recommendations["exercise_recommendations"]:
            report.append("\n🏃 运动建议:")
            for rec in recommendations["exercise_recommendations"]:
                report.append(f"  • {rec}")
        
        if recommendations["medication_reminders"]:
            report.append("\n💊 用药提醒:")
            for reminder in recommendations["medication_reminders"]:
                report.append(f"  • {reminder}")
        
        if recommendations["monitoring_suggestions"]:
            report.append("\n📊 监测建议:")
            for suggestion in recommendations["monitoring_suggestions"]:
                report.append(f"  • {suggestion}")
        
        if recommendations["lifestyle_tips"]:
            report.append("\n💡 生活小贴士:")
            for tip in recommendations["lifestyle_tips"]:
                report.append(f"  • {tip}")
        
        report.append("\n" + "=" * 50)
        
        return "\n".join(report)
    
    def _assess_overall_status(self, stats: Dict, trends: Dict) -> str:
        """Assess overall glucose management status"""
        if stats.get("total_records", 0) == 0:
            return "数据不足"
        
        in_range_pct = stats.get("in_range_percentage", 0)
        
        if in_range_pct >= 70:
            return "控制良好 ✅"
        elif in_range_pct >= 50:
            return "需要改善 ⚠️"
        else:
            return "控制欠佳 ❌"
    
    def _get_immediate_actions(
        self,
        current_glucose: float,
        target_range: Dict
    ) -> List[str]:
        """Get immediate actions based on current glucose"""
        actions = []
        
        if current_glucose < 3.9:
            actions.append("⚠️ 低血糖! 立即补充15-20g速效碳水化合物(如葡萄糖片、果汁)")
            actions.append("15分钟后复测血糖,如仍低于4.0 mmol/L,再次补充碳水化合物")
        elif current_glucose < 4.4:
            actions.append("血糖偏低,建议适当补充碳水化合物")
        elif current_glucose > 13.9:
            actions.append("血糖显著升高,建议检测尿酮体")
            actions.append("如出现恶心、呕吐等症状,请立即就医")
        elif current_glucose > target_range["max"]:
            actions.append("血糖偏高,建议增加运动或调整饮食")
        
        return actions
    
    def _get_diet_recommendations(
        self,
        stats: Dict,
        trends: Dict,
        risk_periods: Dict
    ) -> List[str]:
        """Get diet recommendations"""
        recommendations = []
        
        avg = stats.get("average")
        if avg and avg > 8.0:
            recommendations.append("平均血糖偏高,建议控制碳水化合物摄入,选择低GI食物")
        elif avg and avg < 5.0:
            recommendations.append("平均血糖偏低,建议适当增加餐次,避免长时间空腹")
        
        if trends.get("trend_direction") == "上升":
            recommendations.append("血糖呈上升趋势,建议减少精制碳水化合物,增加膳食纤维")
        
        # Risk period specific
        if risk_periods.get("hyperglycemia_risk_periods"):
            high_risk_hours = risk_periods["hyperglycemia_risk_periods"]
            if high_risk_hours:
                recommendations.append(
                    f"{high_risk_hours[0]['hour']}时段血糖偏高风险较高,建议控制该时段的碳水摄入"
                )
        
        return recommendations
    
    def _get_exercise_recommendations(
        self,
        current_glucose: float,
        stats: Dict,
        target_range: Dict
    ) -> List[str]:
        """Get exercise recommendations"""
        recommendations = []
        
        if stats.get("in_range_percentage", 0) < 60:
            recommendations.append("建议每天进行30分钟中等强度有氧运动,有助于血糖控制")
        
        recommendations.append("餐后1-2小时是运动的最佳时机")
        
        if stats.get("above_range_count", 0) > stats.get("total_records", 0) * 0.3:
            recommendations.append("餐后血糖偏高明显,建议餐后散步15-20分钟")
        
        return recommendations
    
    def _get_medication_reminders(self) -> List[str]:
        """Get medication reminders"""
        reminders = []
        
        # Check recent medication records
        recent_meds = self.data_manager.data.get("medications", [])
        if not recent_meds:
            reminders.append("请记得按时服用降糖药物(如适用)")
        
        return reminders
    
    def _get_monitoring_suggestions(
        self,
        stats: Dict,
        risk_periods: Dict
    ) -> List[str]:
        """Get monitoring suggestions"""
        suggestions = []
        
        total_records = stats.get("total_records", 0)
        if total_records < 14:
            suggestions.append("建议每天至少测量血糖2-4次,建立数据基础")
        elif total_records < 30:
            suggestions.append("建议继续规律监测,包括空腹和餐后血糖")
        
        # Risk period monitoring
        if risk_periods.get("hypoglycemia_risk_periods"):
            suggestions.append(
                "存在低血糖风险时段,建议在这些时段增加监测频率"
            )
        
        suggestions.append("建议每周生成一次血糖趋势报告进行回顾")
        
        return suggestions
    
    def _get_lifestyle_tips(self, trends: Dict) -> List[str]:
        """Get general lifestyle tips"""
        tips = [
            "保持规律作息,避免熬夜",
            "管理压力,学会放松技巧",
            "保持充足睡眠(7-8小时/天)",
            "戒烟限酒有助于血糖控制"
        ]
        
        if trends.get("trend_direction") == "上升":
            tips.append("血糖控制需要更多关注,建议记录饮食日记找出影响因素")
        
        return tips
    
    def _get_warnings(self, stats: Dict, trends: Dict, risk_periods: Dict) -> List[str]:
        """Get warning messages"""
        warnings = []
        
        if stats.get("below_range_count", 0) > 0:
            warnings.append(
                f"过去一周出现{stats['below_range_count']}次低血糖,需特别注意"
            )
        
        if stats.get("above_range_count", 0) > stats.get("total_records", 0) * 0.5:
            warnings.append("高血糖频率较高,建议咨询医生调整治疗方案")
        
        if trends.get("average_glucose", 0) > 10.0:
            warnings.append("平均血糖显著升高,建议尽快就医检查")
        
        return warnings
    
    def _get_carb_range(self, current_glucose: float, meal_type: str) -> Dict:
        """Get recommended carbohydrate range for meal"""
        base_ranges = {
            "breakfast": {"min": 30, "max": 60},
            "lunch": {"min": 45, "max": 75},
            "dinner": {"min": 45, "max": 75},
            "snack": {"min": 15, "max": 30}
        }
        
        return base_ranges.get(meal_type, {"min": 30, "max": 60})
    
    def _get_food_suggestions(
        self,
        meal_type: str,
        current_glucose: float,
        target_range: Dict
    ) -> List[Dict]:
        """Get specific food suggestions"""
        suggestions = {
            "breakfast": [
                {"name": "全麦面包+鸡蛋", "carbs": 30, "gi": "低"},
                {"name": "燕麦粥+坚果", "carbs": 35, "gi": "低"},
                {"name": "杂粮粥+蔬菜", "carbs": 40, "gi": "中"}
            ],
            "lunch": [
                {"name": "糙米饭+蔬菜+瘦肉", "carbs": 50, "gi": "低"},
                {"name": "全麦面条+蔬菜", "carbs": 55, "gi": "中"},
                {"name": "荞麦饭+鱼类", "carbs": 45, "gi": "低"}
            ],
            "dinner": [
                {"name": "杂粮饭+蔬菜+豆制品", "carbs": 45, "gi": "低"},
                {"name": "山药+蔬菜", "carbs": 40, "gi": "低"},
                {"name": "全麦馒头+蔬菜汤", "carbs": 50, "gi": "中"}
            ],
            "snack": [
                {"name": "坚果(一小把)", "carbs": 10, "gi": "低"},
                {"name": "无糖酸奶", "carbs": 15, "gi": "低"},
                {"name": "水果(低糖类)", "carbs": 20, "gi": "低"}
            ]
        }
        
        return suggestions.get(meal_type, [])


if __name__ == '__main__':
    from data_manager import BloodGlucoseDataManager
    from glucose_predictor import BloodGlucosePredictor
    
    manager = BloodGlucoseDataManager()
    predictor = BloodGlucosePredictor(manager)
    engine = RecommendationEngine(manager, predictor)
    
    print(engine.analyze_and_recommend())
