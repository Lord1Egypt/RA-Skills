#!/usr/bin/env python3
"""
12 号滚滚 - 学习统计可视化
生成学习统计报告和图表
"""

import os
import re
from datetime import datetime
from pathlib import Path
from collections import Counter

class LearningStats:
    def __init__(self, workspace="/home/admin/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.learnings_dir = self.workspace / ".learnings"
        
    def analyze(self):
        """分析学习记录"""
        stats = {
            'total': 0,
            'pending': 0,
            'resolved': 0,
            'promoted': 0,
            'by_priority': Counter(),
            'by_area': Counter(),
            'by_source': Counter(),
            'patterns': Counter(),
            'recent': []
        }
        
        # 读取所有学习文件
        learning_files = list(self.learnings_dir.glob("*.md"))
        
        for lf in learning_files:
            if lf.name in ['README.md', 'LEARNING-TEMPLATE.md']:
                continue
                
            with open(lf, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统计状态
            stats['total'] += len(re.findall(r'^### \[(LRN|ERR|FEAT)-', content, re.MULTILINE))
            stats['pending'] += len(re.findall(r'\*\*Status\*\*: pending', content))
            stats['resolved'] += len(re.findall(r'\*\*Status\*\*: resolved', content))
            stats['promoted'] += len(re.findall(r'\*\*Status\*\*: promoted', content))
            
            # 统计优先级
            priorities = re.findall(r'\*\*Priority\*\*: (\w+)', content)
            stats['by_priority'].update(priorities)
            
            # 统计领域
            areas = re.findall(r'\*\*Area\*\*: (\w+)', content)
            stats['by_area'].update(areas)
            
            # 统计来源
            sources = re.findall(r'- Source: (\w+)', content)
            stats['by_source'].update(sources)
            
            # 统计模式
            patterns = re.findall(r'- Pattern-Key: (.+)', content)
            stats['patterns'].update(patterns)
        
        return stats
    
    def print_report(self, stats):
        """打印统计报告"""
        print("=" * 60)
        print("📊 滚滚学习统计报告")
        print("=" * 60)
        print()
        
        # 总体统计
        print("📈 总体统计")
        print("-" * 40)
        print(f"  总学习记录：{stats['total']} 条")
        print(f"  🔴 Pending:   {stats['pending']} 条")
        print(f"  🟢 Resolved:  {stats['resolved']} 条")
        print(f"  ✅ Promoted:  {stats['promoted']} 条")
        
        if stats['total'] > 0:
            promotion_rate = (stats['promoted'] / stats['total']) * 100
            print(f"  📊 推广率：    {promotion_rate:.1f}%")
        print()
        
        # 优先级分布
        print("🎯 优先级分布")
        print("-" * 40)
        for priority, count in sorted(stats['by_priority'].items(), key=lambda x: x[1], reverse=True):
            emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(priority, '⚪')
            bar = '█' * count
            print(f"  {emoji} {priority:8s}: {count:2d} {bar}")
        print()
        
        # 领域分布
        print("📁 领域分布")
        print("-" * 40)
        for area, count in sorted(stats['by_area'].items(), key=lambda x: x[1], reverse=True)[:10]:
            bar = '█' * count
            print(f"  {area:15s}: {count:2d} {bar}")
        print()
        
        # 来源分布
        print("📍 来源分布")
        print("-" * 40)
        for source, count in sorted(stats['by_source'].items(), key=lambda x: x[1], reverse=True)[:10]:
            bar = '█' * count
            print(f"  {source:15s}: {count:2d} {bar}")
        print()
        
        # Recurring Patterns
        print("🔄 Recurring Patterns (出现 >= 2 次)")
        print("-" * 40)
        recurring = [(k, v) for k, v in stats['patterns'].items() if v >= 2]
        if recurring:
            for pattern, count in sorted(recurring, key=lambda x: x[1], reverse=True):
                warning = '⚠️' if count >= 3 else 'ℹ️'
                print(f"  {warning} {pattern:30s}: {count} 次")
        else:
            print("  ✅ 未发现重复模式")
        print()
        
        # 建议
        print("💡 建议")
        print("-" * 40)
        if stats['pending'] > 5:
            print(f"  ⚠️  有 {stats['pending']} 条 pending 学习，建议尽快处理")
        if stats['promoted'] < stats['total'] * 0.3:
            print(f"  ⚠️  推广率偏低 ({stats['promoted']}/{stats['total']}), 建议推广更多学习")
        for pattern, count in recurring:
            if count >= 3:
                print(f"  ⚠️  Pattern '{pattern}' 出现 {count} 次，需要系统解决")
        if stats['pending'] <= 5 and stats['promoted'] >= stats['total'] * 0.3 and not recurring:
            print("  ✅ 学习系统运行良好！")
        print()
        
        print("=" * 60)
        print(f"报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("12 号滚滚管理 🌪️")
        print("=" * 60)
    
    def save_report(self, stats):
        """保存报告到文件"""
        report_file = self.learnings_dir / f"LEARNING-STATS-{datetime.now().strftime('%Y%m%d')}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 📊 滚滚学习统计报告\n\n")
            f.write(f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## 总体统计\n\n")
            f.write(f"- 总学习记录：{stats['total']} 条\n")
            f.write(f"- Pending: {stats['pending']} 条\n")
            f.write(f"- Resolved: {stats['resolved']} 条\n")
            f.write(f"- Promoted: {stats['promoted']} 条\n")
            if stats['total'] > 0:
                promotion_rate = (stats['promoted'] / stats['total']) * 100
                f.write(f"- 推广率：{promotion_rate:.1f}%\n")
            f.write("\n---\n\n")
            
            f.write("## 优先级分布\n\n")
            for priority, count in sorted(stats['by_priority'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {priority}: {count} 条\n")
            f.write("\n---\n\n")
            
            f.write("## Recurring Patterns\n\n")
            recurring = [(k, v) for k, v in stats['patterns'].items() if v >= 2]
            if recurring:
                for pattern, count in sorted(recurring, key=lambda x: x[1], reverse=True):
                    f.write(f"- {pattern}: {count} 次\n")
            else:
                f.write("未发现重复模式\n")
            f.write("\n---\n\n")
            
            f.write("**12 号滚滚管理** 🌪️\n")
        
        print(f"📄 报告已保存到：{report_file}")


def main():
    stats_generator = LearningStats()
    stats = stats_generator.analyze()
    stats_generator.print_report(stats)
    stats_generator.save_report(stats)


if __name__ == "__main__":
    main()
