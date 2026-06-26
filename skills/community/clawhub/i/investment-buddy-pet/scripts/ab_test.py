#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A/B 测试框架

**功能**：
- 管理话术变体
- 分配用户到不同变体
- 追踪变体表现
- 自动选择最佳变体

**使用示例**：
```python
from ab_test import ABTestFramework

ab = ABTestFramework()

# 获取变体（自动分配）
template = ab.get_variant("greeting_morning", "user_001")
print(template)  # "早上好！今天也是存坚果的一天！☀️"

# 追踪表现
ab.track_performance("greeting_morning", 0, is_helpful=True)

# 获取最佳变体
best_idx = ab.get_best_variant("greeting_morning")
print(f"最佳变体：{best_idx}")
```
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class ABTestFramework:
    """A/B 测试框架"""
    
    def __init__(self, variants_file: str = None):
        if variants_file is None:
            variants_file = Path(__file__).parent.parent / "data" / "ab_variants.json"
        self.variants_file = Path(variants_file)
        self.variants_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载或初始化变体
        self.variants = self._load_variants()
        
        # 表现追踪数据
        self.performance_file = Path(__file__).parent.parent / "data" / "ab_performance.jsonl"
        self.performance_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_variants(self) -> Dict:
        """加载变体配置"""
        if self.variants_file.exists():
            with open(self.variants_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认变体
        return {
            "greeting_morning": [
                "早上好！今天也是存坚果的一天！☀️",  # A
                "早安！新的一天，新的机会！🌰",  # B
                "早上好！一起变富的一天开始了！☀️"  # C
            ],
            "greeting_night": [
                "晚安~ 今天又积累了不少经验值呢！",  # A
                "晚安，慢慢变富。",  # B
            ],
            "market_up": [
                "今天涨了 {percent}%！我们的坚持见效啦！🎉",  # A
                "市场不错，涨了{percent}%。继续持有。",  # B
            ],
            "market_down_comfort": [
                "跌了 {percent}%... 我知道你有点担心。但历史上每次都涨回来了！",  # A
                "市场波动正常。坚持定投，时间会奖励耐心。",  # B
                "跌了{percent}%。历史数据：跌幅>3% 后 3 个月内涨回概率 91.6%。",  # C
            ],
            "sip_reminder": [
                "定投日到了！记得打卡哦~ 我已经准备好存坚果啦！🌰",  # A
                "定投日。继续积累。",  # B
            ]
        }
    
    def _save_variants(self):
        """保存变体配置"""
        with open(self.variants_file, 'w', encoding='utf-8') as f:
            json.dump(self.variants, f, ensure_ascii=False, indent=2)
    
    def get_variant(self, template_name: str, user_id: str) -> str:
        """
        根据用户 ID 分配变体
        
        使用哈希确保同一用户始终看到同一变体
        
        Args:
            template_name: 模板名称
            user_id: 用户 ID
        
        Returns:
            变体文本
        """
        if template_name not in self.variants:
            return None
        
        variants = self.variants[template_name]
        if not variants:
            return None
        
        # 使用用户 ID 的哈希值分配
        variant_idx = hash(user_id) % len(variants)
        return variants[variant_idx]
    
    def get_variant_index(self, template_name: str, user_id: str) -> int:
        """获取变体索引"""
        if template_name not in self.variants:
            return 0
        
        variants = self.variants[template_name]
        return hash(user_id) % len(variants)
    
    def track_performance(self, template_name: str, variant_idx: int, 
                         is_helpful: bool, metadata: dict = None):
        """
        追踪变体表现
        
        Args:
            template_name: 模板名称
            variant_idx: 变体索引
            is_helpful: 是否有帮助
            metadata: 其他元数据
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "template": template_name,
            "variant_idx": variant_idx,
            "is_helpful": is_helpful,
            "metadata": metadata or {}
        }
        
        with open(self.performance_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_best_variant(self, template_name: str, min_samples: int = 10) -> int:
        """
        获取表现最好的变体
        
        Args:
            template_name: 模板名称
            min_samples: 最小样本数
        
        Returns:
            最佳变体索引
        """
        if template_name not in self.variants:
            return 0
        
        # 读取表现数据
        performance_data = []
        if self.performance_file.exists():
            with open(self.performance_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log = json.loads(line)
                        if log['template'] == template_name:
                            performance_data.append(log)
                    except:
                        continue
        
        if len(performance_data) < min_samples:
            return 0  # 样本不足，返回默认
        
        # 统计每个变体的表现
        variant_stats = {}
        for log in performance_data:
            idx = log['variant_idx']
            if idx not in variant_stats:
                variant_stats[idx] = {"helpful": 0, "total": 0}
            
            variant_stats[idx]["total"] += 1
            if log['is_helpful']:
                variant_stats[idx]["helpful"] += 1
        
        # 计算有帮助率
        best_idx = 0
        best_rate = 0
        
        for idx, stats in variant_stats.items():
            if stats["total"] >= min_samples:
                rate = stats["helpful"] / stats["total"]
                if rate > best_rate:
                    best_rate = rate
                    best_idx = idx
        
        return best_idx
    
    def add_variant(self, template_name: str, variant_text: str):
        """添加新变体"""
        if template_name not in self.variants:
            self.variants[template_name] = []
        
        self.variants[template_name].append(variant_text)
        self._save_variants()
    
    def remove_variant(self, template_name: str, variant_idx: int):
        """移除变体"""
        if template_name in self.variants:
            if 0 <= variant_idx < len(self.variants[template_name]):
                del self.variants[template_name][variant_idx]
                self._save_variants()
    
    def get_stats(self, template_name: str) -> Dict:
        """获取模板统计"""
        if template_name not in self.variants:
            return {"error": "模板不存在"}
        
        # 读取表现数据
        performance_data = []
        if self.performance_file.exists():
            with open(self.performance_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log = json.loads(line)
                        if log['template'] == template_name:
                            performance_data.append(log)
                    except:
                        continue
        
        # 统计
        variant_stats = {}
        for log in performance_data:
            idx = log['variant_idx']
            if idx not in variant_stats:
                variant_stats[idx] = {"helpful": 0, "total": 0}
            
            variant_stats[idx]["total"] += 1
            if log['is_helpful']:
                variant_stats[idx]["helpful"] += 1
        
        return {
            "template": template_name,
            "variants_count": len(self.variants[template_name]),
            "total_samples": len(performance_data),
            "variant_stats": variant_stats
        }
    
    def export_report(self) -> str:
        """导出 A/B 测试报告"""
        report = "# A/B 测试报告\n\n"
        
        for template_name in self.variants:
            stats = self.get_stats(template_name)
            
            report += f"## {template_name}\n\n"
            report += f"- 变体数量：{stats.get('variants_count', 0)}\n"
            report += f"- 总样本数：{stats.get('total_samples', 0)}\n\n"
            
            variant_stats = stats.get('variant_stats', {})
            if variant_stats:
                report += "| 变体 | 样本数 | 有帮助 | 有帮助率 |\n"
                report += "|------|--------|--------|----------|\n"
                
                for idx, s in variant_stats.items():
                    rate = s["helpful"] / s["total"] if s["total"] > 0 else 0
                    report += f"| {idx} | {s['total']} | {s['helpful']} | {rate:.1%} |\n"
                
                best_idx = self.get_best_variant(template_name)
                report += f"\n**最佳变体**: {best_idx}\n\n"
            
            report += "---\n\n"
        
        return report


# 便捷函数
_default_ab = None

def get_ab_framework() -> ABTestFramework:
    global _default_ab
    if _default_ab is None:
        _default_ab = ABTestFramework()
    return _default_ab


if __name__ == '__main__':
    # 测试
    ab = ABTestFramework()
    
    # 获取变体
    for i in range(5):
        user_id = f"user_{i}"
        template = ab.get_variant("greeting_morning", user_id)
        print(f"{user_id}: {template}")
    
    # 追踪表现
    ab.track_performance("greeting_morning", 0, is_helpful=True)
    ab.track_performance("greeting_morning", 0, is_helpful=True)
    ab.track_performance("greeting_morning", 1, is_helpful=False)
    
    # 获取最佳变体
    best_idx = ab.get_best_variant("greeting_morning")
    print(f"\n最佳变体：{best_idx}")
    
    # 导出报告
    report = ab.export_report()
    print("\n" + report)
