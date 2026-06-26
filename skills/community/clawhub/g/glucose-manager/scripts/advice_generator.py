#!/usr/bin/env python3
"""
健康建议生成脚本
Health Advice Generator

功能：
- 饮食建议
- 运动建议
- 用药建议
- 就医建议
- 综合建议
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# 默认数据文件路径
DEFAULT_DATA_PATH = Path.home() / ".workbuddy" / "glucose_data.json"


class AdviceGenerator:
    """健康建议生成器"""
    
    def __init__(self, data_path: Optional[Path] = None):
        """
        初始化建议生成器
        
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
    
    def get_recent_glucose(self, hours: int = 24) -> List[Dict]:
        """获取最近的血糖记录"""
        records = self.data.get("records", [])
        start_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        return [r for r in records if r["timestamp"] >= start_time]
    
    def generate_diet_advice(
        self,
        current_glucose: Optional[float] = None,
        meal_type: str = "lunch",
        target_carbs: Optional[float] = None
    ) -> Dict:
        """
        生成饮食建议
        
        Args:
            current_glucose: 当前血糖值（mmol/L），如果为None则使用最近记录
            meal_type: 餐类型 (breakfast/lunch/dinner/snack)
            target_carbs: 目标碳水摄入量（克）
        
        Returns:
            饮食建议
        """
        # 获取当前血糖
        if current_glucose is None:
            recent = self.get_recent_glucose(6)
            if recent:
                current_glucose = recent[-1]["glucose_value"]
            else:
                current_glucose = 7.0  # 默认值
        
        advice = {
            "success": True,
            "current_glucose": current_glucose,
            "meal_type": meal_type,
            "glucose_status": self._assess_glucose_status(current_glucose),
            "recommendations": [],
            "carb_recommendation": {},
            "food_suggestions": [],
            "warnings": []
        }
        
        # 根据血糖状态给出建议
        if current_glucose < 3.9:
            # 低血糖
            advice["glucose_status"] = "低血糖"
            advice["recommendations"].append("⚠️ 当前血糖偏低，立即补充15-20克快速吸收的碳水化合物")
            advice["food_suggestions"] = [
                "葡萄糖片 3-4片",
                "果汁 150ml",
                "蜂蜜或糖水 1-2汤匙",
                "糖果 4-5颗"
            ]
            advice["warnings"].append("15分钟后复测血糖，如仍低于4.0 mmol/L，再次补充碳水")
        
        elif current_glucose < 5.0:
            # 偏低
            advice["recommendations"].append("血糖略低，建议先补充少量碳水再进餐")
            advice["carb_recommendation"] = {
                "suggested_intake": "45-60克" if meal_type != "snack" else "15-20克",
                "note": "餐前可先吃少量饼干或水果"
            }
        
        elif current_glucose <= 7.0:
            # 正常
            advice["recommendations"].append("血糖在正常范围，可以正常进餐")
            advice["carb_recommendation"] = {
                "suggested_intake": "45-60克" if meal_type != "snack" else "15-25克",
                "note": "选择低GI食物有助于维持血糖稳定"
            }
            advice["food_suggestions"] = self._get_normal_glucose_foods(meal_type)
        
        elif current_glucose <= 10.0:
            # 偏高
            advice["recommendations"].append("血糖略高，建议控制碳水摄入，选择低GI食物")
            advice["carb_recommendation"] = {
                "suggested_intake": "30-45克" if meal_type != "snack" else "10-15克",
                "note": "避免精制碳水和高糖食物"
            }
            advice["food_suggestions"] = self._get_high_glucose_foods(meal_type)
        
        else:
            # 高血糖
            advice["recommendations"].append("⚠️ 血糖较高，建议严格控制碳水摄入")
            advice["carb_recommendation"] = {
                "suggested_intake": "20-30克" if meal_type != "snack" else "避免零食",
                "note": "如果血糖>13.9 mmol/L且有不适症状，建议就医"
            }
            advice["food_suggestions"] = [
                "大量非淀粉类蔬菜（绿叶菜、西兰花、黄瓜等）",
                "优质蛋白质（鸡胸肉、鱼肉、豆腐、鸡蛋）",
                "少量健康脂肪（橄榄油、坚果）"
            ]
            if current_glucose > 13.9:
                advice["warnings"].append("⚠️ 血糖显著升高，如持续高血糖应咨询医生")
        
        # 添加通用的健康饮食建议
        advice["general_tips"] = [
            "每餐包含蔬菜、蛋白质和适量碳水",
            "选择全谷物代替精制谷物",
            "避免含糖饮料",
            "细嚼慢咽，控制进餐速度",
            "定时定量进餐"
        ]
        
        return advice
    
    def _assess_glucose_status(self, glucose: float) -> str:
        """评估血糖状态"""
        if glucose < 3.9:
            return "低血糖"
        elif glucose < 5.0:
            return "偏低"
        elif glucose <= 7.0:
            return "正常"
        elif glucose <= 10.0:
            return "偏高"
        else:
            return "高血糖"
    
    def _get_normal_glucose_foods(self, meal_type: str) -> List[str]:
        """获取正常血糖时的食物建议"""
        foods = {
            "breakfast": [
                "燕麦粥 + 水煮蛋 + 牛奶",
                "全麦面包 + 牛油果 + 煎蛋",
                "杂粮粥 + 蔬菜 + 豆腐"
            ],
            "lunch": [
                "糙米饭 + 清炒蔬菜 + 瘦肉/鱼",
                "全麦面条 + 蔬菜 + 豆腐/蛋",
                "荞麦饭 + 时蔬 + 鸡胸肉"
            ],
            "dinner": [
                "杂粮饭（减量）+ 大量蔬菜 + 清淡蛋白质",
                "蔬菜沙拉 + 烤鱼/鸡胸肉",
                "清汤 + 少量主食 + 蔬菜"
            ],
            "snack": [
                "一小把坚果（10-15颗）",
                "希腊酸奶 + 少量莓果",
                "一小块水果（苹果、梨）",
                "全麦饼干 2-3片"
            ]
        }
        return foods.get(meal_type, foods["lunch"])
    
    def _get_high_glucose_foods(self, meal_type: str) -> List[str]:
        """获取高血糖时的食物建议"""
        return [
            "大量绿叶蔬菜（菠菜、生菜、芹菜）",
            "十字花科蔬菜（西兰花、花菜、卷心菜）",
            "优质蛋白质（鸡胸肉、鱼肉、豆腐、鸡蛋）",
            "健康脂肪（橄榄油、少量坚果）",
            "低碳水蔬菜（黄瓜、西红柿、茄子）"
        ]
    
    def generate_exercise_advice(
        self,
        current_glucose: Optional[float] = None,
        exercise_type: Optional[str] = None
    ) -> Dict:
        """
        生成运动建议
        
        Args:
            current_glucose: 当前血糖值
            exercise_type: 计划的运动类型
        
        Returns:
            运动建议
        """
        # 获取当前血糖
        if current_glucose is None:
            recent = self.get_recent_glucose(3)
            if recent:
                current_glucose = recent[-1]["glucose_value"]
            else:
                current_glucose = 7.0
        
        advice = {
            "success": True,
            "current_glucose": current_glucose,
            "glucose_status": self._assess_glucose_status(current_glucose),
            "exercise_recommendation": {},
            "precautions": [],
            "timing_suggestion": ""
        }
        
        if current_glucose < 4.0:
            # 低血糖风险
            advice["exercise_recommendation"] = {
                "status": "不建议运动",
                "reason": "血糖过低，应先补充碳水",
                "alternative": "休息并补充15-20克碳水，15分钟后复测"
            }
            advice["precautions"] = [
                "⚠️ 低血糖时运动危险",
                "先治疗低血糖，血糖恢复后再考虑运动"
            ]
        
        elif current_glucose < 5.6:
            # 稍低但可运动
            advice["exercise_recommendation"] = {
                "status": "轻度运动",
                "suggested_activities": ["散步", "轻度瑜伽", "太极"],
                "duration": "20-30分钟",
                "intensity": "低强度"
            }
            advice["precautions"] = [
                "运动前吃少量碳水（如半片饼干或一小块水果）",
                "随身携带糖果或葡萄糖片",
                "运动中出现头晕、心慌立即停止"
            ]
        
        elif current_glucose <= 10.0:
            # 适合运动
            advice["exercise_recommendation"] = {
                "status": "适合运动",
                "suggested_activities": [
                    "快走/慢跑 30-45分钟",
                    "游泳 30分钟",
                    "骑自行车 30-45分钟",
                    "有氧操/健身操 30分钟",
                    "羽毛球、乒乓球等"
                ],
                "duration": "30-45分钟",
                "intensity": "中等强度"
            }
            advice["timing_suggestion"] = "餐后1-2小时是运动的最佳时机"
            advice["precautions"] = [
                "运动前热身，运动后拉伸",
                "补充足够水分",
                "运动时携带血糖仪和糖果"
            ]
        
        elif current_glucose <= 13.9:
            # 可运动但有风险
            advice["exercise_recommendation"] = {
                "status": "轻度运动",
                "suggested_activities": ["散步", "轻度家务"],
                "duration": "15-20分钟",
                "intensity": "低强度"
            }
            advice["precautions"] = [
                "血糖较高时避免剧烈运动",
                "运动有助于降低血糖",
                "注意监测血糖变化"
            ]
        
        else:
            # 高血糖，需谨慎
            advice["exercise_recommendation"] = {
                "status": "暂缓运动",
                "reason": "血糖显著升高，建议先降低血糖",
                "alternative": "咨询医生，调整治疗方案"
            }
            advice["precautions"] = [
                "⚠️ 血糖过高时运动可能导致血糖进一步升高",
                "如伴有酮症，绝对禁止运动",
                "建议就医检查"
            ]
        
        # 最佳运动时段建议
        advice["best_time"] = {
            "recommendation": "餐后1-2小时",
            "reason": "此时血糖较高，运动有助于降低血糖峰值",
            "avoid": "空腹或餐前运动（可能引起低血糖）"
        }
        
        return advice
    
    def generate_medication_advice(
        self,
        medication_name: Optional[str] = None,
        current_glucose: Optional[float] = None
    ) -> Dict:
        """
        生成用药建议
        
        Args:
            medication_name: 药物名称
            current_glucose: 当前血糖
        
        Returns:
            用药建议
        """
        # 获取当前血糖
        if current_glucose is None:
            recent = self.get_recent_glucose(6)
            if recent:
                current_glucose = recent[-1]["glucose_value"]
            else:
                current_glucose = 7.0
        
        advice = {
            "success": True,
            "disclaimer": "以下建议仅供参考，不替代医生处方，具体用药请遵医嘱",
            "current_glucose": current_glucose,
            "general_reminders": [],
            "timing_advice": {},
            "warnings": []
        }
        
        # 通用用药提醒
        advice["general_reminders"] = [
            "按时按量服药，不要自行调整剂量",
            "了解药物的作用机制和可能的副作用",
            "记录服药时间和剂量",
            "定期复诊，让医生了解血糖控制情况"
        ]
        
        # 根据药物类型给出建议
        common_medications = {
            "二甲双胍": {
                "timing": "随餐或餐后服用，减少胃肠道不适",
                "notes": ["可能导致体重下降", "需要定期检查肾功能"]
            },
            "格列美脲": {
                "timing": "早餐前服用",
                "notes": ["可能引起低血糖", "需要规律进餐"]
            },
            "胰岛素": {
                "timing": "根据类型：速效餐前即刻，短效餐前30分钟",
                "notes": ["注意轮换注射部位", "监测血糖，防止低血糖"]
            },
            "阿卡波糖": {
                "timing": "与第一口主食同服",
                "notes": ["减少碳水消化吸收", "可能引起腹胀"]
            }
        }
        
        if medication_name and medication_name in common_medications:
            med_info = common_medications[medication_name]
            advice["specific_medication"] = {
                "name": medication_name,
                "timing": med_info["timing"],
                "notes": med_info["notes"]
            }
        
        # 根据血糖水平给出用药相关建议
        if current_glucose < 4.0:
            advice["warnings"].append("⚠️ 低血糖 - 如使用胰岛素或促泌剂，可能需要调整剂量")
        elif current_glucose > 13.9:
            advice["warnings"].append("⚠️ 血糖显著升高 - 建议咨询医生是否需要调整治疗方案")
        
        return advice
    
    def generate_medical_advice(self, days: int = 30) -> Dict:
        """
        生成就医建议
        
        Args:
            days: 分析最近多少天的数据
        
        Returns:
            就医建议
        """
        records = self.data.get("records", [])
        
        # 筛选最近N天的记录
        start_time = (datetime.now() - timedelta(days=days)).isoformat()
        recent_records = [r for r in records if r["timestamp"] >= start_time]
        
        advice = {
            "success": True,
            "analysis_period": f"最近 {days} 天",
            "data_available": len(recent_records) > 0,
            "reasons_to_see_doctor": [],
            "urgency": "routine",
            "recommended_actions": []
        }
        
        if not recent_records:
            advice["recommended_actions"].append("建议开始规律监测血糖并记录数据")
            return advice
        
        values = [r["glucose_value"] for r in recent_records]
        
        # 检查各种需要就医的情况
        
        # 1. 持续高血糖
        high_glucose_events = [v for v in values if v > 13.9]
        if len(high_glucose_events) >= 3:
            advice["reasons_to_see_doctor"].append({
                "reason": "持续高血糖",
                "detail": f"有 {len(high_glucose_events)} 次血糖超过 13.9 mmol/L",
                "urgency": "high"
            })
        
        # 2. 频繁低血糖
        low_glucose_events = [v for v in values if v < 3.9]
        if len(low_glucose_events) >= 3:
            advice["reasons_to_see_doctor"].append({
                "reason": "频繁低血糖",
                "detail": f"有 {len(low_glucose_events)} 次血糖低于 3.9 mmol/L",
                "urgency": "high"
            })
        
        # 3. 血糖波动大
        if len(values) > 5:
            import statistics
            std_dev = statistics.stdev(values)
            if std_dev > 3.0:
                advice["reasons_to_see_doctor"].append({
                    "reason": "血糖波动大",
                    "detail": f"血糖标准差 {round(std_dev, 2)} mmol/L，波动较大",
                    "urgency": "medium"
                })
        
        # 4. 平均血糖偏高
        avg_glucose = sum(values) / len(values)
        if avg_glucose > 10.0:
            advice["reasons_to_see_doctor"].append({
                "reason": "平均血糖偏高",
                "detail": f"平均血糖 {round(avg_glucose, 1)} mmol/L",
                "urgency": "medium"
            })
        
        # 5. 目标范围内时间过低
        in_range = [v for v in values if 4.4 <= v <= 10.0]
        time_in_range = len(in_range) / len(values) * 100
        if time_in_range < 50:
            advice["reasons_to_see_doctor"].append({
                "reason": "血糖控制不佳",
                "detail": f"目标范围内时间仅 {round(time_in_range, 1)}%",
                "urgency": "medium"
            })
        
        # 确定紧急程度
        urgency_levels = [r.get("urgency", "low") for r in advice["reasons_to_see_doctor"]]
        if "high" in urgency_levels:
            advice["urgency"] = "urgent"
            advice["recommended_actions"] = [
                "⚠️ 建议尽快就医",
                "带上血糖记录和当前用药清单",
                "如有不适症状（口渴、多尿、疲劳、视力模糊），立即就医"
            ]
        elif "medium" in urgency_levels:
            advice["urgency"] = "soon"
            advice["recommended_actions"] = [
                "建议近期预约医生复诊",
                "准备血糖记录和分析报告",
                "考虑是否需要调整治疗方案"
            ]
        else:
            advice["urgency"] = "routine"
            advice["recommended_actions"] = [
                "继续规律监测血糖",
                "定期复诊（建议每3-6个月）",
                "保持健康生活方式"
            ]
        
        # 通用建议
        advice["general_recommendations"] = [
            "定期检测HbA1c（糖化血红蛋白）",
            "定期检查眼底、肾功能、神经系统",
            "保持血压、血脂在正常范围",
            "足部护理，预防糖尿病足"
        ]
        
        return advice
    
    def generate_comprehensive_advice(
        self,
        current_glucose: Optional[float] = None,
        context: str = "general"
    ) -> Dict:
        """
        生成综合建议
        
        Args:
            current_glucose: 当前血糖
            context: 上下文 (general/pre_meal/post_meal/before_exercise)
        
        Returns:
            综合建议
        """
        # 获取当前血糖
        if current_glucose is None:
            recent = self.get_recent_glucose(6)
            if recent:
                current_glucose = recent[-1]["glucose_value"]
            else:
                current_glucose = None
        
        advice = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "current_glucose": current_glucose,
            "glucose_status": self._assess_glucose_status(current_glucose) if current_glucose else "未知",
            "context": context,
            "advice_sections": {}
        }
        
        # 根据上下文生成针对性建议
        if context == "pre_meal":
            advice["advice_sections"]["diet"] = self.generate_diet_advice(current_glucose)
            advice["summary"] = "餐前血糖检查，根据血糖调整本餐饮食"
        
        elif context == "post_meal":
            advice["advice_sections"]["diet"] = self.generate_diet_advice(current_glucose)
            advice["summary"] = "餐后血糖检查，评估本餐饮食是否合适"
        
        elif context == "before_exercise":
            advice["advice_sections"]["exercise"] = self.generate_exercise_advice(current_glucose)
            advice["summary"] = "运动前血糖检查，评估是否适合运动"
        
        else:
            # 通用情况
            advice["advice_sections"]["diet"] = self.generate_diet_advice(current_glucose)
            advice["advice_sections"]["exercise"] = self.generate_exercise_advice(current_glucose)
            advice["advice_sections"]["medical"] = self.generate_medical_advice()
            
            # 综合总结
            if current_glucose:
                if current_glucose < 4.0:
                    advice["summary"] = "⚠️ 血糖偏低，请立即补充碳水并休息"
                elif current_glucose <= 7.0:
                    advice["summary"] = "✅ 血糖正常，继续保持健康生活方式"
                elif current_glucose <= 10.0:
                    advice["summary"] = "血糖略高，注意控制饮食，适当运动"
                else:
                    advice["summary"] = "⚠️ 血糖偏高，控制碳水摄入，如持续高血糖请就医"
            else:
                advice["summary"] = "建议测量血糖以获取个性化建议"
        
        return advice


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python advice_generator.py diet [glucose] [meal_type]")
        print("  python advice_generator.py exercise [glucose]")
        print("  python advice_generator.py medication [med_name]")
        print("  python advice_generator.py medical [days]")
        print("  python advice_generator.py comprehensive [glucose]")
        return
    
    generator = AdviceGenerator()
    command = sys.argv[1]
    
    if command == "diet":
        glucose = float(sys.argv[2]) if len(sys.argv) > 2 else None
        meal_type = sys.argv[3] if len(sys.argv) > 3 else "lunch"
        result = generator.generate_diet_advice(glucose, meal_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "exercise":
        glucose = float(sys.argv[2]) if len(sys.argv) > 2 else None
        result = generator.generate_exercise_advice(glucose)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "medication":
        med_name = sys.argv[2] if len(sys.argv) > 2 else None
        result = generator.generate_medication_advice(med_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "medical":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        result = generator.generate_medical_advice(days)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif command == "comprehensive":
        glucose = float(sys.argv[2]) if len(sys.argv) > 2 else None
        result = generator.generate_comprehensive_advice(glucose)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
