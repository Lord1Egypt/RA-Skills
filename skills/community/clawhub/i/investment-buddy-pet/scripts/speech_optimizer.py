#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
话术自动优化器

**功能**：
- 基于反馈数据自动优化话术
- 使用 LLM 生成新话术变体
- A/B 测试新旧话术
- 自动切换到表现更好的话术

**使用示例**：
```python
from speech_optimizer import SpeechOptimizer

optimizer = SpeechOptimizer()

# 优化话术
optimizer.optimize_template("greeting_morning", "songguo")

# 获取优化建议
suggestions = optimizer.get_optimization_suggestions("market_down_comfort")
print(suggestions)
```
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from feedback_collector import FeedbackCollector
from ab_test import ABTestFramework


class SpeechOptimizer:
    """话术自动优化器"""
    
    def __init__(self):
        self.feedback_collector = FeedbackCollector()
        self.ab_test = ABTestFramework()
        self.optimization_log = Path(__file__).parent.parent / "data" / "optimization_log.jsonl"
        self.optimization_log.parent.mkdir(parents=True, exist_ok=True)
    
    def optimize_template(self, template_name: str, pet_type: str = None) -> Dict:
        """
        自动优化话术模板
        
        Args:
            template_name: 模板名称
            pet_type: 宠物类型（可选）
        
        Returns:
            {
                "status": "success",
                "old_variants": [...],
                "new_variants": [...],
                "ab_test_started": True
            }
        """
        # 1. 收集反馈数据
        patterns = self.feedback_collector.analyze_feedback(days=7)
        
        # 2. 找出低评分的话术
        pet_stats = patterns.get("pet_performance", {})
        if pet_type and pet_type in pet_stats:
            stats = pet_stats[pet_type]
            total = stats["helpful"] + stats["not_helpful"]
            if total > 0:
                helpful_rate = stats["helpful"] / total
                if helpful_rate >= 0.7:
                    return {"status": "no_need", "reason": f"有帮助率{helpful_rate:.1%}，无需优化"}
        
        # 3. 获取当前话术
        current_variants = self.ab_test.variants.get(template_name, [])
        if not current_variants:
            return {"status": "error", "reason": "模板不存在"}
        
        # 4. 生成新话术（使用 LLM）
        new_variants = self._generate_new_variants(template_name, pet_type, patterns)
        
        # 5. 添加新变体
        for variant in new_variants:
            self.ab_test.add_variant(template_name, variant)
        
        # 6. 记录优化日志
        self._log_optimization(template_name, pet_type, current_variants, new_variants)
        
        return {
            "status": "success",
            "old_variants": current_variants,
            "new_variants": new_variants,
            "ab_test_started": True
        }
    
    def _generate_new_variants(self, template_name: str, pet_type: str, patterns: Dict) -> List[str]:
        """
        生成新话术变体
        
        实际实现：调用 LLM 生成
        简化实现：基于规则生成
        """
        # 从反馈中找出问题
        common_questions = patterns.get("common_questions", [])
        
        # 基于模板类型生成新话术
        if template_name == "greeting_morning":
            return [
                "早上好！又是积累财富的一天！☀️",
                "早安！今天的你比昨天更懂投资！🌰"
            ]
        elif template_name == "market_down_comfort":
            return [
                "市场调整正常。坚持纪律，长期必胜。",
                "跌了{percent}%。别担心，这是积累便宜筹码的机会！"
            ]
        elif template_name == "sip_reminder":
            return [
                "定投日！积少成多，慢慢变富。",
                "今天是定投日，打卡成功！🎉"
            ]
        
        return []
    
    def _log_optimization(self, template_name: str, pet_type: str, 
                         old_variants: List[str], new_variants: List[str]):
        """记录优化日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "template": template_name,
            "pet_type": pet_type,
            "old_variants": old_variants,
            "new_variants": new_variants,
            "status": "ab_test_started"
        }
        
        with open(self.optimization_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_optimization_suggestions(self, template_name: str) -> List[str]:
        """
        获取优化建议
        
        Returns:
            ["建议 1", "建议 2", ...]
        """
        patterns = self.feedback_collector.analyze_feedback(days=7)
        suggestions = []
        
        # 分析有帮助率
        helpful_rate = patterns.get("helpful_rate")
        if helpful_rate and helpful_rate < 0.7:
            suggestions.append(f"总体有帮助率较低 ({helpful_rate:.1%})，建议全面优化话术")
        
        # 分析宠物表现
        pet_stats = patterns.get("pet_performance", {})
        for pet, stats in pet_stats.items():
            total = stats["helpful"] + stats["not_helpful"]
            if total > 0:
                rate = stats["helpful"] / total
                if rate < 0.6:
                    suggestions.append(f"宠物{pet}表现较差 ({rate:.1%})，建议优化该宠物的话术")
        
        # 分析常见问题
        common_questions = patterns.get("common_questions", [])
        if common_questions:
            suggestions.append(f"用户常问：{common_questions[0][0]}，建议添加相关话术")
        
        return suggestions
    
    def auto_switch_best_variant(self, template_name: str) -> bool:
        """
        自动切换到最佳变体
        
        Returns:
            是否切换成功
        """
        best_idx = self.ab_test.get_best_variant(template_name, min_samples=10)
        
        if best_idx == 0:
            return False  # 无需切换
        
        # 将最佳变体移到第一位
        variants = self.ab_test.variants.get(template_name, [])
        if len(variants) > best_idx:
            best_variant = variants[best_idx]
            variants.pop(best_idx)
            variants.insert(0, best_variant)
            self.ab_test.variants[template_name] = variants
            self.ab_test._save_variants()
            
            return True
        
        return False


if __name__ == '__main__':
    # 测试
    optimizer = SpeechOptimizer()
    
    # 获取优化建议
    suggestions = optimizer.get_optimization_suggestions("greeting_morning")
    print("优化建议:")
    for s in suggestions:
        print(f"- {s}")
    
    # 优化话术
    result = optimizer.optimize_template("greeting_morning", "songguo")
    print(f"\n优化结果：{result}")
