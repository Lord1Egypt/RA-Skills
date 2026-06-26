#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Reasoner - 日常习惯健康小工具 (v2.0)
安全声明: 本工具仅供参考，不提供医疗建议或诊断。健康问题请咨询专业医师。
"""
import json
import logging
import sys
import argparse
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import warnings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("HealthReasoner")

# ==================== 数据模型 ====================
@dataclass
class UserHealthProfile:
    """用户健康档案（带校验）"""
    age: int
    gender: str  # 'male' or 'female'
    sleep_hours: float
    sleep_quality: str  # 'good','fair','poor'
    diet_type: str  # 'balanced','high_fat','high_sugar','high_salt','vegetarian'
    exercise_frequency: str  # 'daily','weekly','rarely','sedentary'
    stress_level: str  # 'low','moderate','high'
    smoking_status: str = 'never'  # 'never','past','current'
    alcohol_use: str = 'none'  # 'none','light','moderate','heavy'
    symptoms: List[str] = None
    medical_history: List[str] = None

    def __post_init__(self):
        if not (0 <= self.age <= 120):
            raise ValueError("年龄必须在0-120之间")
        if self.gender not in ('male', 'female'):
            raise ValueError("性别必须为 male/female")
        if not (0 <= self.sleep_hours <= 24):
            raise ValueError("睡眠时长应为0-24小时")
        if self.sleep_quality not in ('good','fair','poor'):
            raise ValueError("睡眠质量须为 good/fair/poor")
        if self.diet_type not in ('balanced','high_fat','high_sugar','high_salt','vegetarian'):
            raise ValueError("饮食类型无效")
        if self.exercise_frequency not in ('daily','weekly','rarely','sedentary'):
            raise ValueError("运动频率无效")
        if self.stress_level not in ('low','moderate','high'):
            raise ValueError("压力等级无效")
        if self.smoking_status not in ('never','past','current'):
            raise ValueError("吸烟状态无效")
        if self.alcohol_use not in ('none','light','moderate','heavy'):
            raise ValueError("酒精摄入无效")
        if self.symptoms is None:
            self.symptoms = []
        if self.medical_history is None:
            self.medical_history = []


@dataclass
class LifestyleAssessment:
    """生活习惯综合评估（非医疗诊断）"""
    score: float
    risk_level: str  # 'low' | 'medium' | 'high'
    suggestions: List[Dict[str, Any]]
    risk_factors: List[str]
    details: Dict[str, float]
    timestamp: str = ""


# ==================== 规则引擎 ====================
class HealthReasoner:
    """日常习惯健康小工具 — 基于生活方式的评分引擎（非医疗用途）"""

    def __init__(self, history_file: Optional[str] = None):
        self.history = []
        self.history_file = history_file
        if history_file and Path(history_file).exists():
            try:
                with open(history_file, 'r') as f:
                    self.history = json.load(f)
                logger.info(f"从 {history_file} 加载了 {len(self.history)} 条历史记录")
            except Exception as e:
                logger.warning(f"历史记录加载失败: {e}")

    # ─── 睡眠评分 ───
    def _calc_sleep_score(self, p: UserHealthProfile) -> float:
        score = 60.0
        # 理想睡眠 7-9 小时
        if 7 <= p.sleep_hours <= 9:
            score = 100
        elif 6 <= p.sleep_hours < 7:
            score = 70
        elif 5 <= p.sleep_hours < 6:
            score = 50
        elif p.sleep_hours < 5:
            score = 30
        elif p.sleep_hours > 9:
            score = 60  # 过多睡眠也扣分
        # 质量调整
        if p.sleep_quality == 'good':
            score = min(100, score + 10)
        elif p.sleep_quality == 'poor':
            score = max(0, score - 15)
        return max(0, min(100, score))

    # ─── 饮食评分 ───
    def _calc_diet_score(self, p: UserHealthProfile) -> float:
        scores = {
            'balanced': 100, 'vegetarian': 85,
            'high_fat': 40, 'high_sugar': 35, 'high_salt': 40
        }
        return scores.get(p.diet_type, 50)

    # ─── 运动评分 ───
    def _calc_exercise_score(self, p: UserHealthProfile) -> float:
        scores = {
            'daily': 100, 'weekly': 65,
            'rarely': 30, 'sedentary': 10
        }
        return scores.get(p.exercise_frequency, 50)

    # ─── 压力评分 ───
    def _calc_stress_score(self, p: UserHealthProfile) -> float:
        scores = {'low': 100, 'moderate': 60, 'high': 25}
        return scores.get(p.stress_level, 50)

    # ─── 烟酒评分 ───
    def _calc_substance_score(self, p: UserHealthProfile) -> float:
        score = 100
        if p.smoking_status == 'current':
            score -= 40
        elif p.smoking_status == 'past':
            score -= 10  # 戒烟有负面影响但不大
        if p.alcohol_use == 'heavy':
            score -= 30
        elif p.alcohol_use == 'moderate':
            score -= 15
        elif p.alcohol_use == 'light':
            score -= 5
        return max(0, score)

    # ─── 风险因素识别 ───
    def _assess_risks(self, p: UserHealthProfile) -> List[str]:
        risks = []
        if p.sleep_hours < 6:
            risks.append("睡眠不足(<6小时)")
        if p.sleep_quality == 'poor':
            risks.append("睡眠质量差")
        if p.diet_type in ('high_fat', 'high_sugar', 'high_salt'):
            risks.append("饮食习惯不健康")
        if p.exercise_frequency in ('rarely', 'sedentary'):
            risks.append("缺乏运动")
        if p.stress_level == 'high':
            risks.append("高压力")
        if p.smoking_status == 'current':
            risks.append("吸烟")
        if p.alcohol_use in ('moderate', 'heavy'):
            risks.append("饮酒过多")
        if p.age >= 60 and p.exercise_frequency == 'sedentary':
            risks.append("高龄+久坐")
        return risks

    # ─── 生成改善建议 ───
    def _generate_suggestions(self, p: UserHealthProfile, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        suggestions = []
        priority = 1

        if scores['sleep'] < 60:
            if p.sleep_hours < 7:
                suggestions.append({
                    "priority": priority, "category": "sleep",
                    "message": "尝试将晚间睡眠调整至7-9小时"
                })
                priority += 1
            if p.sleep_quality == 'poor':
                suggestions.append({
                    "priority": priority, "category": "sleep",
                    "message": "改善睡眠环境：保持黑暗安静，睡前1小时不使用电子设备"
                })
                priority += 1

        if scores['diet'] < 60:
            suggestions.append({
                "priority": priority, "category": "diet",
                "message": "尝试增加蔬菜水果比例，减少高脂/高糖/高盐食物"
            })
            priority += 1

        if scores['exercise'] < 60:
            if p.exercise_frequency == 'sedentary':
                suggestions.append({
                    "priority": priority, "category": "exercise",
                    "message": "每坐45分钟起身活动5分钟，逐步建立运动习惯"
                })
            else:
                suggestions.append({
                    "priority": priority, "category": "exercise",
                    "message": "将运动频率提升至每周3-5次"
                })
            priority += 1

        if scores['stress'] < 60:
            suggestions.append({
                "priority": priority, "category": "stress",
                "message": "每天安排5-10分钟深呼吸或正念练习"
            })
            priority += 1

        if p.smoking_status == 'current':
            suggestions.append({
                "priority": priority, "category": "substance",
                "message": "考虑制定戒烟计划，可咨询社区健康服务中心"
            })
            priority += 1

        if p.alcohol_use == 'heavy':
            suggestions.append({
                "priority": priority, "category": "substance",
                "message": "建议减少酒精摄入量，男性每日不超过25g(约2标准杯)"
            })
            priority += 1

        return suggestions

    def assess(self, p: UserHealthProfile) -> LifestyleAssessment:
        """评估生活习惯并返回评分建议"""
        scores = {
            'sleep': self._calc_sleep_score(p),
            'diet': self._calc_diet_score(p),
            'exercise': self._calc_exercise_score(p),
            'stress': self._calc_stress_score(p),
            'substance': self._calc_substance_score(p),
        }

        # 综合评分 (加权)
        weights = {'sleep': 0.25, 'diet': 0.20, 'exercise': 0.25, 'stress': 0.20, 'substance': 0.10}
        total = sum(scores[k] * weights[k] for k in weights)

        # 风险等级
        risk_factors = self._assess_risks(p)
        if len(risk_factors) >= 4:
            risk_level = 'high'
        elif len(risk_factors) >= 2:
            risk_level = 'medium'
        else:
            risk_level = 'low'

        # 建议
        suggestions = self._generate_suggestions(p, scores)
        suggestions.sort(key=lambda x: x['priority'])

        result = LifestyleAssessment(
            score=round(total, 1),
            risk_level=risk_level,
            suggestions=suggestions[:5],  # 最多5条
            risk_factors=risk_factors,
            details=scores,
            timestamp=datetime.now().isoformat()
        )

        # 保存历史（可选）
        self._save_to_history(p, result)

        return result

    def _save_to_history(self, p: UserHealthProfile, r: LifestyleAssessment):
        """保存历史记录（仅当指定了 history_file 时）"""
        if not self.history_file:
            return
        entry = {
            "timestamp": r.timestamp,
            "score": r.score,
            "risk_level": r.risk_level,
            "details": r.details,
        }
        self.history.append(entry)
        # 只保留最近100条
        if len(self.history) > 100:
            self.history = self.history[-100:]
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"历史记录写入失败: {e}")

    def batch_assess(self, profiles: List[dict]) -> List[dict]:
        """批量评估多个健康档案"""
        results = []
        for data in profiles:
            try:
                p = UserHealthProfile(**data)
                r = self.assess(p)
                results.append(asdict(r))
            except Exception as e:
                results.append({"error": str(e)})
        return results

    def trend_analysis(self, history: List[dict] = None) -> dict:
        """从历史记录生成趋势报告"""
        records = history or self.history
        if len(records) < 2:
            return {"score_trend": "insufficient_data"}
        recent = records[-7:]
        scores = [r.get('score', 0) for r in recent]
        avg_first = sum(scores[:len(scores)//2]) / max(len(scores)//2, 1)
        avg_last = sum(scores[len(scores)//2:]) / max(len(scores) - len(scores)//2, 1)
        diff = avg_last - avg_first
        if diff > 5:
            trend = "improving"
        elif diff < -5:
            trend = "declining"
        else:
            trend = "stable"
        return {
            "score_trend": trend,
            "avg_score": round(sum(scores) / len(scores), 1),
            "latest_score": scores[-1],
            "days_tracked": len(records),
        }


# ==================== CLI 接口 ====================
def interactive_cli():
    """交互式命令行输入"""
    print("=== 日常习惯健康小工具 ===")
    print("(本工具仅供参考，不提供医疗建议)\n")
    try:
        p = UserHealthProfile(
            age=int(input("年龄: ")),
            gender=input("性别 (male/female): ").strip().lower(),
            sleep_hours=float(input("每日睡眠时长(小时): ")),
            sleep_quality=input("睡眠质量 (good/fair/poor): ").strip().lower(),
            diet_type=input("饮食类型 (balanced/high_fat/high_sugar/high_salt/vegetarian): ").strip().lower(),
            exercise_frequency=input("运动频率 (daily/weekly/rarely/sedentary): ").strip().lower(),
            stress_level=input("压力等级 (low/moderate/high): ").strip().lower(),
            smoking_status=input("吸烟状态 (never/past/current): ").strip().lower() or 'never',
            alcohol_use=input("酒精摄入 (none/light/moderate/heavy): ").strip().lower() or 'none',
        )
    except Exception as e:
        print(f"输入错误: {e}")
        sys.exit(1)

    hr = HealthReasoner()
    result = hr.assess(p)
    print(f"\n综合评分: {result.score}/100")
    print(f"风险等级: {result.risk_level}")
    print("建议:")
    for s in result.suggestions:
        print(f"  [{s['priority']}] {s['category']}: {s['message']}")


def json_input_cli(json_path: str, output_format: str = 'text'):
    """从 JSON 文件输入并输出结果"""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)

    hr = HealthReasoner()
    try:
        p = UserHealthProfile(**data)
        result = asdict(hr.assess(p))
        if output_format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"综合评分: {result['score']}/100")
            print(f"风险等级: {result['risk_level']}")
            for s in result['suggestions']:
                print(f"  [{s['priority']}] {s['category']}: {s['message']}")
    except Exception as e:
        print(f"评估出错: {e}")
        sys.exit(1)


def run_tests():
    """简单功能测试"""
    print("运行自检...")
    test_cases = [
        {"age": 45, "gender": "female", "sleep_hours": 5.5, "sleep_quality": "poor",
         "diet_type": "high_sugar", "exercise_frequency": "rarely",
         "stress_level": "high", "smoking_status": "never", "alcohol_use": "light",
         "symptoms": ["fatigue", "headache"]},
        {"age": 28, "gender": "male", "sleep_hours": 7.5, "sleep_quality": "good",
         "diet_type": "balanced", "exercise_frequency": "daily",
         "stress_level": "low", "smoking_status": "never", "alcohol_use": "none"},
        {"age": 60, "gender": "male", "sleep_hours": 6, "sleep_quality": "fair",
         "diet_type": "high_salt", "exercise_frequency": "sedentary",
         "stress_level": "moderate", "smoking_status": "current", "alcohol_use": "moderate"},
    ]
    hr = HealthReasoner()
    for i, data in enumerate(test_cases):
        p = UserHealthProfile(**data)
        r = hr.assess(p)
        print(f"自检 {i+1}: 评分={r.score}, 风险={r.risk_level}, 建议={len(r.suggestions)}条")
    print("自检完成")


def main():
    parser = argparse.ArgumentParser(description="日常习惯健康小工具")
    parser.add_argument('--cli', action='store_true', help='交互模式')
    parser.add_argument('--input', type=str, help='JSON 文件路径')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--test', action='store_true', help='运行自检')
    parser.add_argument('--history', type=str, help='历史记录文件路径（可选）')
    args = parser.parse_args()

    if args.test:
        run_tests()
    elif args.cli:
        interactive_cli()
    elif args.input:
        json_input_cli(args.input, args.format)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
