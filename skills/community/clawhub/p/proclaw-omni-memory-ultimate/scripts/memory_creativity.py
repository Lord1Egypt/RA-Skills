#!/usr/bin/env python3
"""
记忆创造性系统
基于记忆组合产生新洞察和创新

核心理念:
- 创造力 = 旧元素的新组合
- 通过记忆的碰撞、融合、重组产生新想法
- 类比思维、模式识别、概念整合

功能:
- 记忆组合创新
- 类比推理
- 模式发现
- 概念融合
- 洞察生成
"""

import json
import math
import os
import random
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CreativityType(Enum):
    """创造性类型"""
    COMBINATION = "combination"      # 组合创新
    ANALOGY = "analogy"             # 类比推理
    PATTERN = "pattern"             # 模式发现
    FUSION = "fusion"               # 概念融合
    INSIGHT = "insight"             # 洞察生成
    SYNTHESIS = "synthesis"         # 综合创新


@dataclass
class CreativeIdea:
    """创造性想法"""
    id: str
    type: CreativityType
    source_cells: List[str]
    description: str
    novelty_score: float           # 新颖度
    relevance_score: float         # 相关性
    utility_score: float           # 实用性
    confidence: float              # 置信度
    created_time: str
    metadata: Dict = field(default_factory=dict)


class MemoryCreativity:
    """
    记忆创造性系统
    
    通过记忆的组合、类比、融合产生创新
    """
    
    def __init__(self, storage_path: str = "./memory/creativity"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # 创意库
        self.ideas: Dict[str, CreativeIdea] = {}
        
        # 组合规则
        self.combination_rules = self._init_combination_rules()
        
        # 类比模板
        self.analogy_templates = self._init_analogy_templates()
        
        # 统计
        self.stats = {
            'total_ideas': 0,
            'by_type': {t.value: 0 for t in CreativityType},
            'avg_novelty': 0,
            'avg_relevance': 0,
            'avg_utility': 0
        }
        
        self._load_state()
    
    def _init_combination_rules(self) -> List[Dict]:
        """初始化组合规则"""
        return [
            {
                'name': 'problem_solution',
                'pattern': {'problem': True, 'solution': True},
                'template': '发现问题和解决方案的关联：{problem} → {solution}',
                'utility_weight': 0.8
            },
            {
                'name': 'context_action',
                'pattern': {'context': True, 'action': True},
                'template': '在{context}情境下，建议采取{action}',
                'utility_weight': 0.7
            },
            {
                'name': 'preference_recommendation',
                'pattern': {'preference': True, 'resource': True},
                'template': '基于偏好{preference}，推荐{resource}',
                'utility_weight': 0.75
            },
            {
                'name': 'skill_project',
                'pattern': {'skill': True, 'project': True},
                'template': '技能{skill}可应用于项目{project}',
                'utility_weight': 0.85
            },
            {
                'name': 'pattern_extension',
                'pattern': {'pattern': True, 'extension': True},
                'template': '模式{pattern}可扩展到{extension}',
                'utility_weight': 0.6
            }
        ]
    
    def _init_analogy_templates(self) -> List[Dict]:
        """初始化类比模板"""
        return [
            {
                'name': 'domain_transfer',
                'template': '从{source_domain}到{target_domain}：{concept}的迁移应用',
                'conditions': {'different_domains': True, 'similar_structure': True}
            },
            {
                'name': 'structural_analogy',
                'template': '{source}的结构关系可类比到{target}',
                'conditions': {'structural_similarity': 0.6}
            },
            {
                'name': 'functional_analogy',
                'template': '{source}的功能可迁移到{target}',
                'conditions': {'functional_similarity': 0.6}
            }
        ]
    
    def combine(self, cells: Dict[str, Dict], 
                cell_ids: List[str] = None,
                max_combinations: int = 10) -> List[CreativeIdea]:
        """
        记忆组合创新
        
        Args:
            cells: 细胞数据
            cell_ids: 指定组合的细胞（可选）
            max_combinations: 最大组合数
        
        Returns:
            创造性想法列表
        """
        ideas = []
        
        # 选择候选细胞
        candidates = cell_ids if cell_ids else list(cells.keys())[:20]
        
        # 生成所有两两组合
        from itertools import combinations
        pairs = list(combinations(candidates, 2))
        random.shuffle(pairs)
        
        for cell1_id, cell2_id in pairs[:max_combinations * 2]:
            if cell1_id not in cells or cell2_id not in cells:
                continue
            
            cell1 = cells[cell1_id]
            cell2 = cells[cell2_id]
            
            # 尝试各种组合规则
            for rule in self.combination_rules:
                idea = self._try_combination_rule(
                    cell1_id, cell1, cell2_id, cell2, rule
                )
                if idea:
                    ideas.append(idea)
                    if len(ideas) >= max_combinations:
                        break
            
            if len(ideas) >= max_combinations:
                break
        
        return ideas
    
    def _try_combination_rule(self, cell1_id: str, cell1: Dict,
                              cell2_id: str, cell2: Dict,
                              rule: Dict) -> Optional[CreativeIdea]:
        """尝试应用组合规则"""
        # 检查类型匹配
        type1 = cell1.get('type', 'unknown')
        type2 = cell2.get('type', 'unknown')
        
        pattern = rule['pattern']
        
        # 简化的类型匹配
        matched = False
        problem_cell = None
        solution_cell = None
        
        if 'problem' in pattern and 'solution' in pattern:
            if type1 in ['problem', 'issue'] or type2 in ['problem', 'issue']:
                matched = True
                if type1 in ['problem', 'issue']:
                    problem_cell = cell1
                    solution_cell = cell2
                else:
                    problem_cell = cell2
                    solution_cell = cell1
        
        elif 'context' in pattern and 'action' in pattern:
            if type1 != type2:
                matched = True
        
        elif 'preference' in pattern and 'resource' in pattern:
            if type1 == 'user' or type2 == 'user':
                matched = True
        
        elif 'skill' in pattern and 'project' in pattern:
            if type1 != type2:
                matched = True
        
        else:
            # 默认：检查关键词重叠
            keywords1 = set(cell1.get('keywords', []))
            keywords2 = set(cell2.get('keywords', []))
            if keywords1 & keywords2:
                matched = True
        
        if not matched:
            return None
        
        # 计算分数
        novelty = self._calculate_novelty(cell1, cell2)
        relevance = self._calculate_relevance(cell1, cell2)
        utility = rule.get('utility_weight', 0.5) * relevance
        
        # 生成描述
        description = rule['template'].format(
            problem=cell1.get('content', '')[:50],
            solution=cell2.get('content', '')[:50],
            context=cell1.get('content', '')[:30],
            action=cell2.get('content', '')[:30],
            preference=cell1.get('content', '')[:30],
            resource=cell2.get('content', '')[:30],
            skill=cell1.get('content', '')[:30],
            project=cell2.get('content', '')[:30],
            pattern=cell1.get('content', '')[:30],
            extension=cell2.get('content', '')[:30]
        )
        
        idea_id = f"idea_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return CreativeIdea(
            id=idea_id,
            type=CreativityType.COMBINATION,
            source_cells=[cell1_id, cell2_id],
            description=description,
            novelty_score=novelty,
            relevance_score=relevance,
            utility_score=utility,
            confidence=(novelty + relevance + utility) / 3,
            created_time=datetime.now().isoformat(),
            metadata={'rule': rule['name']}
        )
    
    def analogy(self, cells: Dict[str, Dict],
                source_domain: str = None,
                target_domain: str = None,
                max_analogies: int = 5) -> List[CreativeIdea]:
        """
        类比推理
        
        从源领域向目标领域迁移知识
        """
        ideas = []
        
        # 按领域分组
        domains = {}
        for cell_id, cell in cells.items():
            domain = cell.get('domain', 'general')
            if domain not in domains:
                domains[domain] = []
            domains[domain].append((cell_id, cell))
        
        # 如果没有指定领域，自动检测
        if not source_domain or not target_domain:
            domain_list = list(domains.keys())
            if len(domain_list) >= 2:
                source_domain = domain_list[0]
                target_domain = domain_list[1]
        
        if source_domain not in domains or target_domain not in domains:
            return ideas
        
        source_cells = domains[source_domain]
        target_cells = domains[target_domain]
        
        # 寻找相似结构
        for template in self.analogy_templates:
            for s_id, s_cell in source_cells[:5]:
                for t_id, t_cell in target_cells[:5]:
                    # 计算结构相似度
                    structural_sim = self._calculate_structural_similarity(s_cell, t_cell)
                    
                    if structural_sim >= 0.5:
                        idea = self._create_analogy_idea(
                            s_id, s_cell, t_id, t_cell,
                            template, structural_sim
                        )
                        if idea:
                            ideas.append(idea)
                            
                            if len(ideas) >= max_analogies:
                                return ideas
        
        return ideas
    
    def _calculate_structural_similarity(self, cell1: Dict, cell2: Dict) -> float:
        """计算结构相似度"""
        # 关键词重叠
        k1 = set(cell1.get('keywords', []))
        k2 = set(cell2.get('keywords', []))
        keyword_sim = len(k1 & k2) / max(1, len(k1 | k2))
        
        # 类型匹配
        type_match = 1.0 if cell1.get('type') == cell2.get('type') else 0.3
        
        # 能量相近度
        e1 = cell1.get('energy', 1.0)
        e2 = cell2.get('energy', 1.0)
        energy_sim = 1 - abs(e1 - e2)
        
        return (keyword_sim * 0.5 + type_match * 0.3 + energy_sim * 0.2)
    
    def _create_analogy_idea(self, s_id: str, s_cell: Dict,
                            t_id: str, t_cell: Dict,
                            template: Dict, similarity: float) -> Optional[CreativeIdea]:
        """创建类比想法"""
        description = template['template'].format(
            source_domain=s_cell.get('domain', 'unknown'),
            target_domain=t_cell.get('domain', 'unknown'),
            concept=s_cell.get('content', '')[:30],
            source=s_cell.get('content', '')[:30],
            target=t_cell.get('content', '')[:30]
        )
        
        idea_id = f"idea_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return CreativeIdea(
            id=idea_id,
            type=CreativityType.ANALOGY,
            source_cells=[s_id, t_id],
            description=description,
            novelty_score=similarity * 0.8,  # 类比新颖度
            relevance_score=similarity,
            utility_score=similarity * 0.7,
            confidence=similarity * 0.9,
            created_time=datetime.now().isoformat(),
            metadata={'template': template['name']}
        )
    
    def discover_patterns(self, cells: Dict[str, Dict],
                          min_occurrences: int = 3) -> List[CreativeIdea]:
        """
        模式发现
        
        从记忆中发现重复模式
        """
        ideas = []
        
        # 收集所有关键词模式
        pattern_occurrences = {}
        
        for cell_id, cell in cells.items():
            keywords = tuple(sorted(cell.get('keywords', [])))
            if keywords:
                if keywords not in pattern_occurrences:
                    pattern_occurrences[keywords] = []
                pattern_occurrences[keywords].append((cell_id, cell))
        
        # 识别频繁模式
        for pattern, occurrences in pattern_occurrences.items():
            if len(occurrences) >= min_occurrences:
                idea = self._create_pattern_idea(pattern, occurrences)
                if idea:
                    ideas.append(idea)
        
        return ideas
    
    def _create_pattern_idea(self, pattern: Tuple[str, ...],
                            occurrences: List[Tuple[str, Dict]]) -> CreativeIdea:
        """创建模式想法"""
        cell_ids = [occ[0] for occ in occurrences]
        samples = [occ[1].get('content', '')[:50] for occ in occurrences[:3]]
        
        description = f"发现重复模式 [{', '.join(pattern)}]：出现{len(occurrences)}次。示例：{'; '.join(samples)}"
        
        idea_id = f"idea_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return CreativeIdea(
            id=idea_id,
            type=CreativityType.PATTERN,
            source_cells=cell_ids,
            description=description,
            novelty_score=0.3,  # 已有模式，新颖度低
            relevance_score=len(occurrences) / 10,  # 频繁度高
            utility_score=len(occurrences) / 10 * 0.8,
            confidence=min(1.0, len(occurrences) / 5),
            created_time=datetime.now().isoformat(),
            metadata={'pattern': list(pattern), 'occurrence_count': len(occurrences)}
        )
    
    def synthesize(self, cells: Dict[str, Dict],
                   topic: str = None,
                   max_synthesis: int = 3) -> List[CreativeIdea]:
        """
        综合创新
        
        将多个相关记忆综合成新的整体
        """
        ideas = []
        
        # 按主题聚类
        clusters = {}
        for cell_id, cell in cells.items():
            # 提取主题（简化的：使用第一个关键词）
            keywords = cell.get('keywords', [])
            if keywords:
                theme = keywords[0]
                if theme not in clusters:
                    clusters[theme] = []
                clusters[theme].append((cell_id, cell))
        
        # 对每个聚类进行综合
        for theme, cluster_items in clusters.items():
            if topic and theme != topic:
                continue
            
            if len(cluster_items) >= 3:
                idea = self._synthesize_cluster(theme, cluster_items)
                if idea:
                    ideas.append(idea)
                    
                    if len(ideas) >= max_synthesis:
                        break
        
        return ideas
    
    def _synthesize_cluster(self, theme: str,
                           cluster_items: List[Tuple[str, Dict]]) -> CreativeIdea:
        """综合聚类"""
        cell_ids = [item[0] for item in cluster_items]
        contents = [item[1].get('content', '') for item in cluster_items]
        
        # 生成综合描述
        description = f"关于「{theme}」的综合洞察：整合了{len(cluster_items)}条相关记忆。"
        description += f"核心内容：{'; '.join(contents[:3])}..."
        
        # 计算综合分数
        avg_importance = sum(item[1].get('importance', 0.5) for item in cluster_items) / len(cluster_items)
        avg_energy = sum(item[1].get('energy', 1.0) for item in cluster_items) / len(cluster_items)
        
        idea_id = f"idea_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return CreativeIdea(
            id=idea_id,
            type=CreativityType.SYNTHESIS,
            source_cells=cell_ids,
            description=description,
            novelty_score=0.6,  # 综合创新中等新颖
            relevance_score=avg_importance,
            utility_score=avg_importance * 0.9,
            confidence=avg_energy,
            created_time=datetime.now().isoformat(),
            metadata={'theme': theme, 'item_count': len(cluster_items)}
        )
    
    def _calculate_novelty(self, cell1: Dict, cell2: Dict) -> float:
        """计算新颖度"""
        # 不同类型组合更具新颖性
        type_novelty = 0.8 if cell1.get('type') != cell2.get('type') else 0.4
        
        # 不同领域组合更具新颖性
        domain_novelty = 0.9 if cell1.get('domain') != cell2.get('domain') else 0.5
        
        # 关键词差异
        k1 = set(cell1.get('keywords', []))
        k2 = set(cell2.get('keywords', []))
        keyword_diff = 1 - (len(k1 & k2) / max(1, len(k1 | k2)))
        
        return (type_novelty + domain_novelty + keyword_diff) / 3
    
    def _calculate_relevance(self, cell1: Dict, cell2: Dict) -> float:
        """计算相关性"""
        # 关键词重叠
        k1 = set(cell1.get('keywords', []))
        k2 = set(cell2.get('keywords', []))
        keyword_overlap = len(k1 & k2) / max(1, min(len(k1), len(k2)))
        
        # 能量相近度
        e1 = cell1.get('energy', 1.0)
        e2 = cell2.get('energy', 1.0)
        energy_proximity = 1 - min(1, abs(e1 - e2))
        
        return (keyword_overlap * 0.7 + energy_proximity * 0.3)
    
    def save_idea(self, idea: CreativeIdea) -> None:
        """保存想法"""
        self.ideas[idea.id] = idea
        
        # 更新统计
        self.stats['total_ideas'] += 1
        self.stats['by_type'][idea.type.value] += 1
        
        # 更新平均值
        n = self.stats['total_ideas']
        self.stats['avg_novelty'] = (self.stats['avg_novelty'] * (n-1) + idea.novelty_score) / n
        self.stats['avg_relevance'] = (self.stats['avg_relevance'] * (n-1) + idea.relevance_score) / n
        self.stats['avg_utility'] = (self.stats['avg_utility'] * (n-1) + idea.utility_score) / n
        
        self._save_state()
    
    def get_best_ideas(self, limit: int = 10, 
                       by_utility: bool = True) -> List[CreativeIdea]:
        """获取最佳想法"""
        ideas = list(self.ideas.values())
        
        if by_utility:
            ideas.sort(key=lambda x: x.utility_score, reverse=True)
        else:
            ideas.sort(key=lambda x: x.confidence, reverse=True)
        
        return ideas[:limit]
    
    def get_ideas_by_type(self, idea_type: CreativityType) -> List[CreativeIdea]:
        """按类型获取想法"""
        return [idea for idea in self.ideas.values() if idea.type == idea_type]
    
    def get_report(self) -> Dict:
        """获取报告"""
        return {
            'total_ideas': self.stats['total_ideas'],
            'by_type': self.stats['by_type'],
            'averages': {
                'novelty': round(self.stats['avg_novelty'], 3),
                'relevance': round(self.stats['avg_relevance'], 3),
                'utility': round(self.stats['avg_utility'], 3)
            }
        }
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.storage_path, 'creativity_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                self.stats = data.get('stats', self.stats)
            except Exception:
                pass
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.storage_path, 'creativity_state.json')
        
        data = {
            'stats': self.stats
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)


def demo_creativity():
    """演示创造性系统"""
    print("=" * 60)
    print("记忆创造性系统演示")
    print("=" * 60)
    
    creativity = MemoryCreativity()
    
    # 模拟细胞数据
    cells = {
        'cell_001': {
            'content': '用户偏好Python后端开发',
            'keywords': ['python', '后端', '用户偏好'],
            'type': 'user',
            'domain': 'programming',
            'importance': 0.8,
            'energy': 1.0
        },
        'cell_002': {
            'content': '项目需要实现RESTful API',
            'keywords': ['api', 'restful', '项目需求'],
            'type': 'project',
            'domain': 'programming',
            'importance': 0.9,
            'energy': 0.9
        },
        'cell_003': {
            'content': 'FastAPI框架适合快速开发API',
            'keywords': ['fastapi', 'api', '框架'],
            'type': 'knowledge',
            'domain': 'programming',
            'importance': 0.7,
            'energy': 0.8
        },
        'cell_004': {
            'content': '数据库性能问题需要优化',
            'keywords': ['数据库', '性能', '问题'],
            'type': 'problem',
            'domain': 'programming',
            'importance': 0.85,
            'energy': 1.2
        },
        'cell_005': {
            'content': '索引优化可以提升查询速度',
            'keywords': ['索引', '性能', '优化'],
            'type': 'solution',
            'domain': 'programming',
            'importance': 0.75,
            'energy': 0.7
        }
    }
    
    # 1. 组合创新
    print("\n1. 组合创新测试...")
    ideas = creativity.combine(cells, max_combinations=5)
    print(f"生成 {len(ideas)} 个组合想法")
    for idea in ideas[:3]:
        print(f"  [{idea.type.value}] {idea.description[:60]}...")
        print(f"    新颖度:{idea.novelty_score:.2f} 相关性:{idea.relevance_score:.2f} 实用性:{idea.utility_score:.2f}")
        creativity.save_idea(idea)
    
    # 2. 模式发现
    print("\n2. 模式发现测试...")
    patterns = creativity.discover_patterns(cells, min_occurrences=2)
    print(f"发现 {len(patterns)} 个模式")
    for pattern in patterns[:2]:
        print(f"  {pattern.description[:80]}...")
    
    # 3. 综合创新
    print("\n3. 综合创新测试...")
    synthesis = creativity.synthesize(cells, max_synthesis=3)
    print(f"生成 {len(synthesis)} 个综合洞察")
    for s in synthesis[:2]:
        print(f"  {s.description[:80]}...")
    
    # 4. 获取最佳想法
    print("\n4. 最佳想法（按实用性）...")
    best = creativity.get_best_ideas(limit=3)
    for idea in best:
        print(f"  [{idea.type.value}] {idea.description[:60]}...")
        print(f"    综合评分:{idea.confidence:.2f}")
    
    # 5. 报告
    print("\n5. 创造性报告:")
    report = creativity.get_report()
    print(f"  总想法数: {report['total_ideas']}")
    print(f"  平均新颖度: {report['averages']['novelty']}")
    print(f"  平均相关性: {report['averages']['relevance']}")
    print(f"  平均实用性: {report['averages']['utility']}")


if __name__ == "__main__":
    demo_creativity()
