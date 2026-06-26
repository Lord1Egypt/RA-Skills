#!/usr/bin/env python3
"""
Metacognition - 元认知能力
让Agent"知道自己知道什么"和"知道自己不知道什么"
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from collections import defaultdict, Counter

# 路径配置
WORKSPACE_ROOT = os.getcwd()
MEMORY_DIR = os.path.join(WORKSPACE_ROOT, "memory")
MEMORY_INDEX_PATH = os.path.join(WORKSPACE_ROOT, "MEMORY.md")
SESSION_STATE_PATH = os.path.join(WORKSPACE_ROOT, "SESSION-STATE.md")
METACOG_PATH = os.path.join(MEMORY_DIR, "metacognition.json")


class Metacognition:
    """元认知系统"""
    
    def __init__(self):
        self.knowledge_domains: Dict[str, Dict] = {}
        self.coverage_stats: Dict[str, Any] = {}
        self.gaps: List[Dict] = []
        self.confidence_scores: Dict[str, float] = {}
        
        self._load_state()
    
    def _load_state(self):
        """加载元认知状态"""
        if os.path.exists(METACOG_PATH):
            try:
                with open(METACOG_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.knowledge_domains = data.get('domains', {})
                    self.coverage_stats = data.get('coverage', {})
                    self.gaps = data.get('gaps', [])
                    self.confidence_scores = data.get('confidence', {})
            except Exception:
                pass
    
    def _save_state(self):
        """保存元认知状态"""
        os.makedirs(os.path.dirname(METACOG_PATH), exist_ok=True)
        with open(METACOG_PATH, 'w', encoding='utf-8') as f:
            json.dump({
                'domains': self.knowledge_domains,
                'coverage': self.coverage_stats,
                'gaps': self.gaps,
                'confidence': self.confidence_scores,
                'updated_at': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    
    def analyze_coverage(self, memories: List[Dict]) -> Dict[str, Any]:
        """
        分析记忆覆盖率
        
        Args:
            memories: 记忆列表 [{id, type, content, keywords, ...}]
        
        Returns:
            覆盖率报告
        """
        # 按类型统计
        type_counts = Counter(m.get('type', 'unknown') for m in memories)
        
        # 按领域统计（基于关键词聚类）
        domain_keywords = defaultdict(Counter)
        for m in memories:
            for kw in m.get('keywords', []):
                # 简单的领域分类
                domain = self._classify_domain(kw)
                domain_keywords[domain][kw] += 1
        
        # 计算覆盖率
        total_memories = len(memories)
        coverage = {
            'total_memories': total_memories,
            'by_type': dict(type_counts),
            'by_domain': {k: dict(v.most_common(10)) for k, v in domain_keywords.items()},
            'domain_count': len(domain_keywords),
            'avg_per_domain': total_memories / len(domain_keywords) if domain_keywords else 0,
            'coverage_score': self._calculate_coverage_score(type_counts, domain_keywords)
        }
        
        self.coverage_stats = coverage
        return coverage
    
    def _classify_domain(self, keyword: str) -> str:
        """将关键词分类到领域"""
        domain_keywords = {
            'technology': ['react', 'python', 'api', 'code', 'database', 'server', 'frontend', 'backend'],
            'preference': ['like', 'prefer', 'want', 'style', 'format', '简洁', '详细'],
            'project': ['project', 'task', 'feature', 'release', 'version', 'deadline'],
            'user': ['user', 'name', 'role', 'team', 'company', '工作', '角色'],
            'knowledge': ['learn', 'know', 'understand', 'concept', 'theory', '知识']
        }
        
        kw_lower = keyword.lower()
        for domain, keywords in domain_keywords.items():
            if any(k in kw_lower for k in keywords):
                return domain
        
        return 'general'
    
    def _calculate_coverage_score(self, type_counts: Counter, 
                                   domain_keywords: Dict) -> float:
        """
        计算覆盖率分数
        
        理想状态：
        - 四种类型都有记忆
        - 覆盖多个领域
        - 分布均匀
        """
        # 类型覆盖 (0-0.4)
        expected_types = {'user', 'feedback', 'project', 'reference'}
        type_coverage = len(expected_types & set(type_counts.keys())) / 4
        type_score = type_coverage * 0.4
        
        # 领域覆盖 (0-0.3)
        domain_count = len(domain_keywords)
        domain_score = min(domain_count / 10, 1.0) * 0.3
        
        # 均匀度 (0-0.3)
        if type_counts:
            values = list(type_counts.values())
            avg = sum(values) / len(values)
            variance = sum((v - avg) ** 2 for v in values) / len(values)
            uniformity = 1 / (1 + variance ** 0.5)
            uniformity_score = uniformity * 0.3
        else:
            uniformity_score = 0
        
        return round(type_score + domain_score + uniformity_score, 3)
    
    def identify_gaps(self, memories: List[Dict], 
                      recent_queries: List[str] = None) -> List[Dict]:
        """
        识别知识缺口
        
        Args:
            memories: 当前记忆
            recent_queries: 最近的查询列表
        
        Returns:
            缺口列表
        """
        gaps = []
        
        # 1. 类型缺口
        expected_types = {'user', 'feedback', 'project', 'reference'}
        existing_types = set(m.get('type', 'unknown') for m in memories)
        missing_types = expected_types - existing_types
        
        for t in missing_types:
            gaps.append({
                'type': 'missing_type',
                'domain': t,
                'severity': 'high',
                'suggestion': f"缺少{t}类型的记忆，建议主动收集",
                'created_at': datetime.now().isoformat()
            })
        
        # 2. 领域缺口（基于最近查询）
        if recent_queries:
            for query in recent_queries:
                domain = self._classify_domain(query)
                # 检查该领域是否有足够记忆
                domain_memories = [m for m in memories 
                                   if any(self._classify_domain(kw) == domain 
                                          for kw in m.get('keywords', []))]
                
                if len(domain_memories) < 3:
                    gaps.append({
                        'type': 'weak_domain',
                        'domain': domain,
                        'severity': 'medium',
                        'suggestion': f"关于'{domain}'的记忆较少，可能需要补充",
                        'query_hint': query,
                        'created_at': datetime.now().isoformat()
                    })
        
        # 3. 时效性缺口（太久未更新）
        cutoff = datetime.now() - timedelta(days=30)
        for m in memories:
            created_at = m.get('created_at')
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at)
                    if dt < cutoff:
                        gaps.append({
                            'type': 'stale_memory',
                            'memory_id': m.get('id'),
                            'domain': m.get('type'),
                            'severity': 'low',
                            'suggestion': f"记忆 '{m.get('id')}' 已超过30天未更新，可能需要验证",
                            'created_at': datetime.now().isoformat()
                        })
                except Exception:
                    pass
        
        self.gaps = gaps
        return gaps
    
    def calculate_confidence(self, query: str, 
                            relevant_memories: List[Dict]) -> float:
        """
        计算回答置信度
        
        Args:
            query: 查询
            relevant_memories: 相关记忆
        
        Returns:
            置信度 (0-1)
        """
        if not relevant_memories:
            return 0.0
        
        # 因素1: 记忆数量
        count_factor = min(len(relevant_memories) / 5, 1.0) * 0.3
        
        # 因素2: 相关性分数
        if relevant_memories:
            avg_score = sum(m.get('score', 0.5) for m in relevant_memories) / len(relevant_memories)
            score_factor = avg_score * 0.3
        else:
            score_factor = 0
        
        # 因素3: 记忆类型覆盖
        types = set(m.get('type', 'unknown') for m in relevant_memories)
        type_factor = len(types) / 4 * 0.2
        
        # 因素4: 时效性
        now = datetime.now()
        fresh_count = 0
        for m in relevant_memories:
            created_at = m.get('created_at')
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at)
                    if (now - dt).days < 7:
                        fresh_count += 1
                except Exception:
                    pass
        
        fresh_factor = fresh_count / len(relevant_memories) * 0.2 if relevant_memories else 0
        
        confidence = count_factor + score_factor + type_factor + fresh_factor
        return round(confidence, 3)
    
    def generate_questions(self, gaps: List[Dict] = None) -> List[Dict]:
        """
        生成主动提问
        
        Args:
            gaps: 知识缺口列表
        
        Returns:
            提问列表
        """
        if gaps is None:
            gaps = self.gaps
        
        questions = []
        
        for gap in gaps:
            if gap['type'] == 'missing_type':
                domain = gap['domain']
                question_templates = {
                    'user': {
                        'question': "能告诉我更多关于你的工作背景吗？比如你的角色、常用的技术栈？",
                        'reason': "了解你的背景可以让我提供更贴合的建议",
                        'priority': 1
                    },
                    'feedback': {
                        'question': "对于我的回复风格，你有什么偏好吗？比如详细程度、格式等？",
                        'reason': "了解你的偏好可以让我的回复更符合你的期望",
                        'priority': 2
                    },
                    'project': {
                        'question': "能介绍一下你当前项目的背景吗？比如目标、技术选型等？",
                        'reason': "了解项目背景可以让我更好地理解你的需求",
                        'priority': 3
                    },
                    'reference': {
                        'question': "项目中重要的文档或资源存放在哪里？",
                        'reason': "记录资源位置可以方便后续查找",
                        'priority': 4
                    }
                }
                
                if domain in question_templates:
                    q = question_templates[domain].copy()
                    q['gap_id'] = gap.get('domain')
                    questions.append(q)
            
            elif gap['type'] == 'weak_domain':
                domain = gap['domain']
                questions.append({
                    'question': f"关于{domain}方面，有什么重要的信息我应该知道的吗？",
                    'reason': f"当前关于{domain}的记忆较少",
                    'priority': 5,
                    'gap_id': gap.get('domain')
                })
        
        # 按优先级排序
        questions.sort(key=lambda x: x['priority'])
        return questions[:3]  # 最多返回3个问题
    
    def should_ask(self, context: Dict) -> Tuple[bool, str]:
        """
        判断是否应该主动提问
        
        Args:
            context: 当前上下文
        
        Returns:
            (是否提问, 提问内容)
        """
        # 检查覆盖率
        coverage_score = self.coverage_stats.get('coverage_score', 0)
        
        # 覆盖率太低，需要主动收集
        if coverage_score < 0.3:
            questions = self.generate_questions()
            if questions:
                return True, questions[0]['question']
        
        # 检查最近的缺口
        recent_gaps = [g for g in self.gaps if g['severity'] == 'high']
        if recent_gaps:
            questions = self.generate_questions(recent_gaps)
            if questions:
                return True, questions[0]['question']
        
        return False, ""
    
    def get_meta_report(self) -> Dict[str, Any]:
        """
        获取元认知报告
        
        Returns:
            完整的元认知状态报告
        """
        return {
            'coverage': self.coverage_stats,
            'gaps_count': len(self.gaps),
            'gaps_by_severity': Counter(g['severity'] for g in self.gaps),
            'top_gaps': sorted(self.gaps, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x['severity'], 3))[:5],
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        coverage = self.coverage_stats.get('coverage_score', 0)
        if coverage < 0.3:
            recommendations.append("覆盖率较低，建议主动收集用户画像、项目背景等基础信息")
        elif coverage < 0.6:
            recommendations.append("覆盖率中等，建议补充薄弱领域的记忆")
        
        high_gaps = [g for g in self.gaps if g['severity'] == 'high']
        if high_gaps:
            recommendations.append(f"存在{len(high_gaps)}个高优先级缺口，建议优先处理")
        
        stale_count = len([g for g in self.gaps if g['type'] == 'stale_memory'])
        if stale_count > 5:
            recommendations.append(f"{stale_count}条记忆超过30天未更新，建议验证时效性")
        
        return recommendations
    
    def save(self):
        """保存状态"""
        self._save_state()


def main():
    parser = argparse.ArgumentParser(description="Metacognition System")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # analyze命令
    analyze_parser = subparsers.add_parser("analyze", help="分析覆盖率")
    analyze_parser.add_argument("--memories", type=str, help="记忆JSON文件路径")
    
    # gaps命令
    gaps_parser = subparsers.add_parser("gaps", help="识别知识缺口")
    gaps_parser.add_argument("--memories", type=str, help="记忆JSON文件路径")
    
    # questions命令
    subparsers.add_parser("questions", help="生成主动提问")
    
    # confidence命令
    conf_parser = subparsers.add_parser("confidence", help="计算置信度")
    conf_parser.add_argument("--query", required=True, help="查询")
    conf_parser.add_argument("--memories", type=str, help="记忆JSON文件路径")
    
    # report命令
    subparsers.add_parser("report", help="获取元认知报告")
    
    # should_ask命令
    subparsers.add_parser("should_ask", help="判断是否应该提问")
    
    args = parser.parse_args()
    meta = Metacognition()
    
    # 模拟记忆数据（实际应从向量库加载）
    sample_memories = [
        {'id': 'm1', 'type': 'user', 'content': '用户是开发者', 'keywords': ['developer', 'python'], 'created_at': datetime.now().isoformat()},
        {'id': 'm2', 'type': 'project', 'content': '项目使用React', 'keywords': ['react', 'frontend'], 'created_at': datetime.now().isoformat()},
    ]
    
    if args.command == "analyze":
        coverage = meta.analyze_coverage(sample_memories)
        meta.save()
        print(json.dumps(coverage, ensure_ascii=False, indent=2))
        
    elif args.command == "gaps":
        gaps = meta.identify_gaps(sample_memories)
        meta.save()
        print(json.dumps(gaps, ensure_ascii=False, indent=2))
        
    elif args.command == "questions":
        questions = meta.generate_questions()
        print(json.dumps(questions, ensure_ascii=False, indent=2))
        
    elif args.command == "confidence":
        confidence = meta.calculate_confidence(args.query, sample_memories)
        print(f"Confidence: {confidence}")
        
    elif args.command == "report":
        report = meta.get_meta_report()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    elif args.command == "should_ask":
        should, question = meta.should_ask({})
        if should:
            print(f"[ASK] {question}")
        else:
            print("[NO] No need to ask")


if __name__ == "__main__":
    main()
