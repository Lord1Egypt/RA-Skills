#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户反馈收集器

**功能**：
- 记录每次用户交互
- 收集用户评分（👍/👎）
- 每周分析反馈数据
- 找出改进点

**使用示例**：
```python
from feedback_collector import FeedbackCollector

collector = FeedbackCollector()

# 记录交互
collector.log_interaction(
    user_id="user_001",
    pet_type="songguo",
    question="市场跌了怎么办？",
    response="跌了 3%... 我知道你有点担心...",
    feedback="有帮助",
    helpful=True
)

# 分析反馈
patterns = collector.analyze_feedback(days=7)
print(patterns)
```
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class FeedbackCollector:
    """用户反馈收集器"""
    
    def __init__(self, feedback_dir: str = None):
        if feedback_dir is None:
            feedback_dir = Path(__file__).parent.parent / "data" / "feedback"
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
    
    def log_interaction(self, user_id: str, pet_type: str, 
                       question: str, response: str, 
                       feedback: str = None, helpful: bool = None,
                       metadata: dict = None):
        """
        记录用户交互
        
        Args:
            user_id: 用户 ID
            pet_type: 宠物类型
            question: 用户问题
            response: 宠物回复
            feedback: 用户文字反馈
            helpful: 是否有帮助（True/False）
            metadata: 其他元数据（如大师 ID、数据源等）
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "pet_type": pet_type,
            "question": question,
            "response": response,
            "feedback": feedback,
            "helpful": helpful,
            "metadata": metadata or {}
        }
        
        # 写入日志文件（按日期分文件）
        log_file = self.feedback_dir / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def analyze_feedback(self, days: int = 7) -> Dict:
        """
        分析反馈数据，找出改进点
        
        Args:
            days: 分析最近 N 天
        
        Returns:
            {
                "total_interactions": 150,
                "helpful_rate": 0.85,
                "low_helpful_count": 22,
                "common_questions": [...],
                "pet_performance": {...},
                "improvement_suggestions": [...]
            }
        """
        # 读取最近 N 天的反馈
        feedback_logs = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            log_file = self.feedback_dir / f"{date}.jsonl"
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            feedback_logs.append(json.loads(line))
                        except:
                            continue
        
        if not feedback_logs:
            return {"error": "无反馈数据"}
        
        # 分析模式
        patterns = {
            "total_interactions": len(feedback_logs),
            "helpful_count": 0,
            "not_helpful_count": 0,
            "no_feedback_count": 0,
            "common_questions": [],
            "pet_performance": {},
            "improvement_suggestions": []
        }
        
        # 统计
        question_freq = {}
        
        for log in feedback_logs:
            # 统计有帮助/无帮助
            if log.get('helpful') == True:
                patterns["helpful_count"] += 1
            elif log.get('helpful') == False:
                patterns["not_helpful_count"] += 1
            else:
                patterns["no_feedback_count"] += 1
            
            # 统计常见问题
            q = log.get('question', '')[:50]  # 截断
            question_freq[q] = question_freq.get(q, 0) + 1
            
            # 统计宠物表现
            pet = log.get('pet_type', 'unknown')
            if pet not in patterns["pet_performance"]:
                patterns["pet_performance"][pet] = {"helpful": 0, "not_helpful": 0}
            
            if log.get('helpful') == True:
                patterns["pet_performance"][pet]["helpful"] += 1
            elif log.get('helpful') == False:
                patterns["pet_performance"][pet]["not_helpful"] += 1
        
        # 计算有帮助率
        total_feedback = patterns["helpful_count"] + patterns["not_helpful_count"]
        if total_feedback > 0:
            patterns["helpful_rate"] = patterns["helpful_count"] / total_feedback
        else:
            patterns["helpful_rate"] = None
        
        # 常见问题 Top 10
        patterns["common_questions"] = sorted(
            question_freq.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        # 生成改进建议
        if patterns["helpful_rate"] and patterns["helpful_rate"] < 0.7:
            patterns["improvement_suggestions"].append(
                f"有帮助率较低 ({patterns['helpful_rate']:.1%})，建议优化话术"
            )
        
        # 找出表现最差的宠物
        worst_pet = None
        worst_rate = 1.0
        for pet, stats in patterns["pet_performance"].items():
            total = stats["helpful"] + stats["not_helpful"]
            if total > 0:
                rate = stats["helpful"] / total
                if rate < worst_rate:
                    worst_rate = rate
                    worst_pet = pet
        
        if worst_pet and worst_rate < 0.6:
            patterns["improvement_suggestions"].append(
                f"宠物 {worst_pet} 表现较差 ({worst_rate:.1%})，建议优化人格配置"
            )
        
        return patterns
    
    def get_daily_stats(self, date: str = None) -> Dict:
        """获取单日统计"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        log_file = self.feedback_dir / f"{date}.jsonl"
        if not log_file.exists():
            return {"error": "无数据"}
        
        logs = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    continue
        
        helpful = sum(1 for l in logs if l.get('helpful') == True)
        not_helpful = sum(1 for l in logs if l.get('helpful') == False)
        
        return {
            "date": date,
            "total": len(logs),
            "helpful": helpful,
            "not_helpful": not_helpful,
            "helpful_rate": helpful / (helpful + not_helpful) if (helpful + not_helpful) > 0 else None
        }
    
    def export_report(self, days: int = 7, output_file: str = None) -> str:
        """导出反馈报告"""
        patterns = self.analyze_feedback(days)
        
        report = f"""# 用户反馈报告

**统计周期**: 最近 {days} 天  
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 总体数据

- 总交互次数：{patterns.get('total_interactions', 0)}
- 有帮助率：{(str(round(patterns.get('helpful_rate') * 100, 1)) + "%") if patterns.get('helpful_rate') else 'N/A'}
- 有帮助：{patterns.get('helpful_count', 0)}
- 无帮助：{patterns.get('not_helpful_count', 0)}
- 无反馈：{patterns.get('no_feedback_count', 0)}

---

## 宠物表现

| 宠物 | 有帮助 | 无帮助 | 有帮助率 |
|------|--------|--------|---------|
"""
        
        for pet, stats in patterns.get('pet_performance', {}).items():
            total = stats["helpful"] + stats["not_helpful"]
            rate = stats["helpful"] / total if total > 0 else 0
            report += f"| {pet} | {stats['helpful']} | {stats['not_helpful']} | {rate:.1%} |\n"
        
        report += f"""
---

## 常见问题 Top 10

| 问题 | 次数 |
|------|------|
"""
        
        for q, count in patterns.get('common_questions', []):
            report += f"| {q} | {count} |\n"
        
        report += f"""
---

## 改进建议

"""
        
        for suggestion in patterns.get('improvement_suggestions', []):
            report += f"- {suggestion}\n"
        
        # 写入文件
        if output_file is None:
            output_file = self.feedback_dir / f"report_{datetime.now().strftime('%Y-%m-%d')}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report


# 便捷函数
_default_collector = None

def get_collector() -> FeedbackCollector:
    global _default_collector
    if _default_collector is None:
        _default_collector = FeedbackCollector()
    return _default_collector


if __name__ == '__main__':
    # 测试
    collector = FeedbackCollector()
    
    # 模拟一些数据
    collector.log_interaction(
        user_id="user_001",
        pet_type="songguo",
        question="市场跌了怎么办？",
        response="跌了 3%... 我知道你有点担心...",
        helpful=True
    )
    
    collector.log_interaction(
        user_id="user_002",
        pet_type="songguo",
        question="现在能买茅台吗？",
        response="巴菲特建议...",
        helpful=False,
        feedback="数据不准确"
    )
    
    # 分析
    patterns = collector.analyze_feedback(days=1)
    print(json.dumps(patterns, indent=2, ensure_ascii=False))
