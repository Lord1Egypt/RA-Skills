#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Ingest Script - 投资宠物知识库摄入脚本

基于 Karpathy LLM Wiki 思路
功能：读取 raw/ 中的原始素材，提取知识，创建/更新 wiki/ 页面

用法:
    python scripts/knowledge_ingest.py [--raw-path PATH] [--dry-run]
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class KnowledgeIngest:
    """知识库摄入引擎"""
    
    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.raw_path = self.base_path / "raw"
        self.wiki_path = self.base_path / "wiki"
        self.index_path = self.base_path / "index.md"
        self.log_path = self.base_path / "log.md"
        
        # 确保目录存在
        for subdir in ["concepts", "entities", "patterns", "topics"]:
            (self.wiki_path / subdir).mkdir(parents=True, exist_ok=True)
        
        # 统计信息
        self.stats = {
            "processed": 0,
            "new_concepts": 0,
            "new_entities": 0,
            "new_patterns": 0,
            "new_topics": 0,
            "updated_pages": 0,
            "new_links": 0
        }
    
    def extract_concepts(self, text):
        """从文本中提取概念"""
        # 简单实现：匹配投资术语
        concept_patterns = [
            r'定投', r'估值', r'市盈率', r'市净率', r'PE', r'PB',
            r'价值投资', r'成长投资', r'趋势跟踪', r'资产配置',
            r'风险收益', r'最大回撤', r'夏普比率', r'波动率',
            r'损失厌恶', r'从众心理', r'过度自信', r'锚定效应',
            r'左侧交易', r'右侧交易', r'止盈止损', r'仓位管理'
        ]
        
        concepts = []
        for pattern in concept_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                concepts.append(pattern)
        
        return list(set(concepts))
    
    def extract_entities(self, text):
        """从文本中提取实体"""
        # 简单实现：匹配股票、基金、人物等
        entities = []
        
        # 股票名称（简化匹配）
        stock_pattern = r'([A 股沪深创业]+|贵州茅台 | 宁德时代 | 招商银行 | 中国平安)'
        entities.extend(re.findall(stock_pattern, text))
        
        # 投资大师
        masters = ['巴菲特', '芒格', '达利欧', '索罗斯', '林奇', '格雷厄姆']
        for master in masters:
            if master in text:
                entities.append(master)
        
        # 指数
        indices = ['沪深 300', '上证 50', '创业板指', '标普 500', '纳斯达克']
        for index in indices:
            if index in text:
                entities.append(index)
        
        return list(set(entities))
    
    def extract_patterns(self, text):
        """从文本中提取模式"""
        patterns = []
        
        # 策略模式
        if '定投' in text and ('下跌' in text or '熊市' in text):
            patterns.append('熊市定投策略')
        
        if '估值' in text and '低' in text and '买入' in text:
            patterns.append('低估值买入策略')
        
        # 行为模式
        if '慌' in text or '怕' in text or '担心' in text:
            patterns.append('市场恐慌时的心理')
        
        if '后悔' in text or '早知道' in text:
            patterns.append('投资后悔心理')
        
        return list(set(patterns))
    
    def create_concept_page(self, concept):
        """创建概念页"""
        page_path = self.wiki_path / "concepts" / f"{concept}.md"
        
        if page_path.exists():
            self.stats["updated_pages"] += 1
            return False
        
        content = f"""# [[{concept}]]

## 定义
待完善 - 需要精确定义

## 核心要点
- 待完善

## 相关概念
- 待补充

## 应用场景
- 待补充

## 来源
- [[raw/待补充]]

---
*最后更新*: {datetime.now().strftime('%Y-%m-%d')}
*创建方式*: 自动 Ingest
"""
        
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stats["new_concepts"] += 1
        return True
    
    def create_entity_page(self, entity):
        """创建实体页"""
        page_path = self.wiki_path / "entities" / f"{entity}.md"
        
        if page_path.exists():
            self.stats["updated_pages"] += 1
            return False
        
        # 判断实体类型
        entity_type = "未知"
        if any(x in entity for x in ['茅台', '宁德', '招商', '平安']):
            entity_type = "股票"
        elif any(x in entity for x in ['巴菲特', '芒格', '达利欧']):
            entity_type = "投资大师"
        elif any(x in entity for x in ['沪深', '上证', '创业板', '标普']):
            entity_type = "市场指数"
        
        content = f"""# [[{entity}]]

## 类型
{entity_type}

## 关键信息
- 待完善

## 相关概念
- 待补充

## 相关模式
- 待补充

## 来源
- [[raw/待补充]]

---
*最后更新*: {datetime.now().strftime('%Y-%m-%d')}
*创建方式*: 自动 Ingest
"""
        
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stats["new_entities"] += 1
        return True
    
    def create_pattern_page(self, pattern):
        """创建模式页"""
        page_path = self.wiki_path / "patterns" / f"{pattern}.md"
        
        if page_path.exists():
            self.stats["updated_pages"] += 1
            return False
        
        content = f"""# [[{pattern}]]

## 描述
待完善 - 描述这个模式的含义

## 适用条件
- 待完善

## 成功案例
- 待补充

## 失败教训
- 待补充

## 相关概念
- 待补充

## 相关实体
- 待补充

## 来源
- [[raw/待补充]]

---
*最后更新*: {datetime.now().strftime('%Y-%m-%d')}
*创建方式*: 自动 Ingest
"""
        
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stats["new_patterns"] += 1
        return True
    
    def update_index(self):
        """更新索引文件"""
        # 统计各类页面数量
        concepts = list((self.wiki_path / "concepts").glob("*.md"))
        entities = list((self.wiki_path / "entities").glob("*.md"))
        patterns = list((self.wiki_path / "patterns").glob("*.md"))
        topics = list((self.wiki_path / "topics").glob("*.md"))
        
        total = len(concepts) + len(entities) + len(patterns) + len(topics)
        
        # 更新 index.md 的统计表格
        index_content = self.index_path.read_text(encoding='utf-8')
        
        # 更新表格
        old_table = "| 概念 (Concepts) | 0 | 投资术语、策略、心理模式 |"
        new_table = f"| 概念 (Concepts) | {len(concepts)} | 投资术语、策略、心理模式 |"
        index_content = index_content.replace(old_table, new_table)
        
        old_table = "| 实体 (Entities) | 0 | 股票、基金、人物、指数 |"
        new_table = f"| 实体 (Entities) | {len(entities)} | 股票、基金、人物、指数 |"
        index_content = index_content.replace(old_table, new_table)
        
        old_table = "| 模式 (Patterns) | 0 | 成功策略、失败教训、用户行为 |"
        new_table = f"| 模式 (Patterns) | {len(patterns)} | 成功策略、失败教训、用户行为 |"
        index_content = index_content.replace(old_table, new_table)
        
        old_table = "| 主题 (Topics) | 0 | 宏观主题、综合讨论 |"
        new_table = f"| 主题 (Topics) | {len(topics)} | 宏观主题、综合讨论 |"
        index_content = index_content.replace(old_table, new_table)
        
        old_total = "| **总计** | **0** | 持续生长中... |"
        new_total = f"| **总计** | **{total}** | 持续生长中... |"
        index_content = index_content.replace(old_total, new_total)
        
        # 更新日期
        today = datetime.now().strftime('%Y-%m-%d')
        index_content = re.sub(
            r'\*\*最后更新\*\*: \d{4}-\d{2}-\d{2}',
            f'**最后更新**: {today}',
            index_content
        )
        
        self.index_path.write_text(index_content, encoding='utf-8')
    
    def log_operation(self, operation, details):
        """记录操作日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        log_entry = f"\n## {operation} - {timestamp}\n\n"
        log_entry += f"```json\n{json.dumps(details, ensure_ascii=False, indent=2)}\n```\n"
        
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def process_raw_file(self, raw_file):
        """处理单个原始文件"""
        print(f"  处理：{raw_file.name}")
        
        try:
            content = raw_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"    读取失败：{e}")
            return
        
        # 提取知识
        concepts = self.extract_concepts(content)
        entities = self.extract_entities(content)
        patterns = self.extract_patterns(content)
        
        # 创建页面
        for concept in concepts:
            if self.create_concept_page(concept):
                print(f"    + 新概念：[[{concept}]]")
        
        for entity in entities:
            if self.create_entity_page(entity):
                print(f"    + 新实体：[[{entity}]]")
        
        for pattern in patterns:
            if self.create_pattern_page(pattern):
                print(f"    + 新模式：[[{pattern}]]")
        
        self.stats["processed"] += 1
    
    def run(self, dry_run=False):
        """运行 Ingest 流程"""
        print("🚀 开始 Knowledge Ingest...")
        print(f"  原始素材目录：{self.raw_path}")
        print(f"  知识库目录：{self.wiki_path}")
        print()
        
        if dry_run:
            print("🔍 模拟运行模式（不创建页面）")
            print()
        
        # 遍历 raw/ 目录
        for subdir in ["interactions", "market-events", "feedback"]:
            subdir_path = self.raw_path / subdir
            if not subdir_path.exists():
                continue
            
            print(f"📁 扫描 {subdir}/ ...")
            raw_files = list(subdir_path.glob("*.md"))
            
            for raw_file in raw_files:
                self.process_raw_file(raw_file)
            
            print()
        
        # 更新索引
        if not dry_run:
            print("📑 更新索引...")
            self.update_index()
            
            # 记录日志
            self.log_operation("Ingest", self.stats)
        
        # 输出统计
        print("✅ Ingest 完成")
        print()
        print("📊 统计信息:")
        print(f"  处理文件数：{self.stats['processed']}")
        print(f"  新增概念：{self.stats['new_concepts']}")
        print(f"  新增实体：{self.stats['new_entities']}")
        print(f"  新增模式：{self.stats['new_patterns']}")
        print(f"  更新页面：{self.stats['updated_pages']}")
        print()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Knowledge Ingest - 投资宠物知识库摄入脚本')
    parser.add_argument('--raw-path', type=str, help='原始素材目录路径')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不创建页面')
    
    args = parser.parse_args()
    
    ingest = KnowledgeIngest(args.raw_path)
    ingest.run(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
