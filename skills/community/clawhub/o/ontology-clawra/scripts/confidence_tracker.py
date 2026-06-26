#!/usr/bin/env python3
"""
ontology-clawra 置信度追踪模块
记录推理结果的置信度，根据用户反馈自动调整
"""

import json
import os
from datetime import datetime
from collections import defaultdict

MEMORY_DIR = os.path.expanduser("~/.openclaw/skills/ontology-clawra/memory")
CONFIDENCE_FILE = os.path.join(MEMORY_DIR, "confidence_tracker.jsonl")
REASONING_FILE = os.path.join(MEMORY_DIR, "reasoning.jsonl")


class ConfidenceTracker:
    """置信度追踪器"""
    
    # 置信度等级
    LEVELS = {
        "CONFIRMED": {"weight": 1.0, "color": "🟢", "desc": "已验证"},
        "ASSUMED": {"weight": 0.6, "color": "🟡", "desc": "假设"},
        "SPECULATIVE": {"weight": 0.3, "color": "🔴", "desc": "推测"},
        "UNKNOWN": {"weight": 0.0, "color": "⚪", "desc": "未知"}
    }
    
    def __init__(self):
        self.reasonings = []
        self.load()
    
    def load(self):
        """加载历史记录"""
        if os.path.exists(CONFIDENCE_FILE):
            with open(CONFIDENCE_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        self.reasonings.append(json.loads(line))
                    except:
                        pass
    
    def save(self):
        """保存记录"""
        os.makedirs(MEMORY_DIR, exist_ok=True)
        with open(CONFIDENCE_FILE, 'w', encoding='utf-8') as f:
            for r in self.reasonings:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
    
    def add_reasoning(self, query, confidence, source, details=None):
        """记录推理"""
        entry = {
            "query": query,
            "confidence": confidence,
            "source": source,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        self.reasonings.append(entry)
        self.save()
        return entry
    
    def user_correction(self, query, old_confidence, new_confidence, reason=None):
        """记录用户纠正"""
        entry = {
            "type": "correction",
            "query": query,
            "old_confidence": old_confidence,
            "new_confidence": new_confidence,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
        self.reasonings.append(entry)
        self.save()
        
        # 自动更新置信度
        self._auto_adjust(query, old_confidence, new_confidence)
        
        return entry
    
    def _auto_adjust(self, query, old, new):
        """根据纠正自动调整类似查询的置信度"""
        # 简化的自动调整逻辑
        # 实际生产中可以使用更复杂的相似度匹配
        pass
    
    def get_confidence(self, query):
        """获取查询的置信度"""
        for r in reversed(self.reasonings):
            if r.get("query") == query:
                return r.get("confidence")
        return "UNKNOWN"
    
    def get_statistics(self):
        """获取置信度统计"""
        stats = defaultdict(int)
        for r in self.reasonings:
            conf = r.get("confidence", "UNKNOWN")
            if conf in stats:
                stats[conf] += 1
            else:
                stats[conf] = 1
        
        total = sum(stats.values())
        result = {}
        for conf, count in stats.items():
            result[conf] = {
                "count": count,
                "percentage": round(count / total * 100, 1) if total > 0 else 0
            }
        
        return {
            "total": total,
            "by_confidence": result
        }
    
    def get_low_confidence_queries(self, threshold=0.5):
        """获取低置信度查询列表"""
        low_confidence = []
        for r in self.reasonings:
            conf = r.get("confidence")
            if conf in self.LEVELS:
                if self.LEVELS[conf]["weight"] < threshold:
                    low_confidence.append(r)
        return low_confidence
    
    def suggest_improvements(self):
        """根据统计给出改进建议"""
        stats = self.get_statistics()
        suggestions = []
        
        by_conf = stats.get("by_confidence", {})
        
        # 检查低置信度比例
        low_count = sum([
            by_conf.get("SPECULATIVE", {}).get("count", 0),
            by_conf.get("UNKNOWN", {}).get("count", 0)
        ])
        total = stats.get("total", 0)
        
        if total > 0 and low_count / total > 0.3:
            suggestions.append({
                "type": "confidence",
                "priority": "high",
                "message": f"低置信度推理占比 {round(low_count/total*100)}%，建议增加本体数据或与用户确认"
            })
        
        # 检查ASSUMED是否过多
        assumed_count = by_conf.get("ASSUMED", {}).get("count", 0)
        if total > 0 and assumed_count / total > 0.4:
            suggestions.append({
                "type": "assumption",
                "priority": "medium",
                "message": f"假设性推理占比 {round(assumed_count/total*100)}%，建议与用户确认更多细节"
            })
        
        return suggestions


def label_result(content, confidence):
    """标注结果置信度"""
    level_info = ConfidenceTracker.LEVELS.get(confidence, ConfidenceTracker.LEVELS["UNKNOWN"])
    return f"{level_info['color']} [{confidence}] {content}"


def declare_source(content, confidence, source=None):
    """声明数据来源"""
    level_info = ConfidenceTracker.LEVELS.get(confidence, ConfidenceTracker.LEVELS["UNKNOWN"])
    source_info = f" (来源: {source})" if source else ""
    return f"{level_info['color']} {level_info['desc']}{source_info}: {content}"


def main():
    """测试"""
    print("=" * 50)
    print("置信度追踪测试")
    print("=" * 50)
    
    tracker = ConfidenceTracker()
    
    # 记录一些推理
    print("\n📝 记录推理:")
    tracker.add_reasoning("调压箱选型", "ASSUMED", "典型场景计算", {"n": 100})
    tracker.add_reasoning("100户用气量", "SPECULATIVE", "估算", {"method": "经验"})
    tracker.add_reasoning("用户是AI创业者", "CONFIRMED", "用户输入", {})
    
    # 统计
    print("\n📊 置信度统计:")
    stats = tracker.get_statistics()
    print(f"  总推理数: {stats['total']}")
    for conf, info in stats['by_confidence'].items():
        print(f"  {conf}: {info['count']} ({info['percentage']}%)")
    
    # 低置信度查询
    print("\n⚠️ 低置信度查询:")
    low = tracker.get_low_confidence_queries()
    for q in low:
        print(f"  • {q['query']}: {q['confidence']}")
    
    # 改进建议
    print("\n💡 改进建议:")
    suggestions = tracker.suggest_improvements()
    for s in suggestions:
        print(f"  [{s['priority']}] {s['message']}")
    
    # 测试标注
    print("\n" + "=" * 50)
    print("标注示例:")
    print(label_result("RTZ-50/25 调压箱", "ASSUMED"))
    print(declare_source("用户确认无供暖", "CONFIRMED", "用户输入"))
    print(declare_source("估算用气量", "SPECULATIVE"))


if __name__ == "__main__":
    main()
