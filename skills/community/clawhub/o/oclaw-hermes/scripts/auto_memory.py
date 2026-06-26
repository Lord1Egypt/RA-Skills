#!/usr/bin/env python3
"""
自动记忆系统 v2.0
智能监听、自动提取、主动整合

核心功能：
1. Skill调用自动记录
2. 会话内容实时提取
3. 重要记忆自动整合
4. 智能检索推荐
"""

import sys
sys.path.insert(0, 'C:\\Users\\wry08\\.openclaw\\skills\\oclaw-hermes\\scripts')

from mflow_v2 import MFlowEngineV2, MemoryEntry
from datetime import datetime
import hashlib
import json
import re
from typing import List, Dict, Optional

class AutoMemorySystem:
    """自动记忆系统"""
    
    def __init__(self):
        self.engine = MFlowEngineV2()
        self.session_id = None
        self.session_buffer = []
    
    def start_session(self, session_id: str = None):
        """开始新会话"""
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_buffer = []
        print(f"[AUTO-MEMORY] 会话开始: {self.session_id}")
    
    def record_skill_call(self, skill_name: str, input_data: str, output_data: str, 
                         success: bool = True, duration_ms: int = 0):
        """
        记录Skill调用
        
        Args:
            skill_name: Skill名称
            input_data: 输入内容摘要
            output_data: 输出内容摘要
            success: 是否成功
            duration_ms: 执行时长
        """
        # 提取关键信息
        entry = MemoryEntry(
            id=hashlib.md5(f"skill_{skill_name}_{datetime.now()}".encode()).hexdigest()[:16],
            layer="skill",
            content=f"""Skill调用记录
名称: {skill_name}
输入: {input_data[:200]}
输出: {output_data[:200]}
结果: {'成功' if success else '失败'}
耗时: {duration_ms}ms
会话: {self.session_id}""",
            source="auto_skill_tracker",
            timestamp=datetime.now(),
            importance=7.0 if success else 5.0,
            metadata={
                "skill_name": skill_name,
                "success": success,
                "duration_ms": duration_ms,
                "session_id": self.session_id
            },
            entities=[skill_name, "skill_call"],
            relations=[{
                "source": skill_name,
                "target": self.session_id,
                "type": "used_in",
                "strength": 1.0
            }]
        )
        
        self.engine.store(entry)
        
        # 添加到会话缓冲区
        self.session_buffer.append({
            "type": "skill_call",
            "skill": skill_name,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"[AUTO-MEMORY] 记录Skill调用: {skill_name}")
    
    def record_user_intent(self, user_message: str, detected_intent: str, 
                          confidence: float = 0.8):
        """记录用户意图"""
        entry = MemoryEntry(
            id=hashlib.md5(f"intent_{datetime.now()}".encode()).hexdigest()[:16],
            layer="instant",
            content=f"""用户意图识别
消息: {user_message[:300]}
意图: {detected_intent}
置信度: {confidence}
会话: {self.session_id}""",
            source="intent_detector",
            timestamp=datetime.now(),
            importance=6.0,
            metadata={
                "intent": detected_intent,
                "confidence": confidence,
                "session_id": self.session_id
            }
        )
        
        self.engine.store(entry)
    
    def extract_and_store_facts(self, content: str, fact_type: str = "general"):
        """
        从内容中提取事实并存储
        
        Args:
            content: 原始内容
            fact_type: 事实类型 (general, research, code, expert)
        """
        # 提取关键实体
        entities = self._extract_entities(content)
        
        # 确定记忆层
        layer_map = {
            "general": "short",
            "research": "long",
            "code": "skill",
            "expert": "expert"
        }
        layer = layer_map.get(fact_type, "short")
        
        # 确定重要性
        importance_map = {
            "general": 5.0,
            "research": 8.0,
            "code": 6.0,
            "expert": 9.0
        }
        importance = importance_map.get(fact_type, 5.0)
        
        entry = MemoryEntry(
            id=hashlib.md5(f"fact_{content[:50]}_{datetime.now()}".encode()).hexdigest()[:16],
            layer=layer,
            content=f"""提取事实 [{fact_type}]
{content[:1000]}

来源会话: {self.session_id}
提取时间: {datetime.now().isoformat()}""",
            source=f"auto_extractor_{fact_type}",
            timestamp=datetime.now(),
            importance=importance,
            metadata={
                "fact_type": fact_type,
                "session_id": self.session_id,
                "entity_count": len(entities)
            },
            entities=entities[:10]  # 最多10个实体
        )
        
        self.engine.store(entry)
        print(f"[AUTO-MEMORY] 提取并存储 {fact_type} 类型事实，实体: {len(entities)}个")
        
        return entities
    
    def _extract_entities(self, text: str) -> List[str]:
        """简单实体提取（生产环境应使用NER模型）"""
        entities = []
        
        # 提取引号内容
        quotes = re.findall(r'["""']([^"""']+)["""']', text)
        entities.extend(quotes)
        
        # 提取可能的专业术语（大写字母组合）
        terms = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)+\b', text)
        entities.extend(terms)
        
        # 提取关键词（基于常见模式）
        keywords = [
            "Skill", "Agent", "Memory", "Research", "调解", "工程", "造价",
            "招标", "合同", "项目管理", "DeerFlow", "Hermes", "OpenClaw"
        ]
        for kw in keywords:
            if kw in text:
                entities.append(kw)
        
        return list(set(entities))[:20]  # 去重并限制数量
    
    def get_relevant_context(self, query: str, max_items: int = 3) -> List[Dict]:
        """
        获取与查询相关的上下文记忆
        
        Args:
            query: 当前查询
            max_items: 最大返回数量
            
        Returns:
            相关记忆列表
        """
        results = self.engine.retrieve(query, top_k=max_items)
        
        # 过滤低分结果
        filtered = [r for r in results if r.get("score", 0) > 0.3]
        
        return filtered
    
    def suggest_skills(self, user_message: str) -> List[str]:
        """
        基于用户消息推荐相关Skills
        
        Args:
            user_message: 用户输入
            
        Returns:
            推荐的Skill名称列表
        """
        # 关键词映射
        skill_keywords = {
            "cn-construction-mediation": ["调解", "纠纷", "争议", "仲裁"],
            "cn-tendering-agent": ["招标", "投标", "采购", "评标"],
            "cn-cost-control": ["造价", "成本", "预算", "估算"],
            "cn-project-management": ["项目管理", "进度", "工期", "PM"],
            "china-cost-estimation": ["造价指标", "估算", "投资"],
            "wittgenstein-master": ["哲学", "逻辑", "语言", "思维"],
            "dlh365-expert-system": ["专家", "蒸馏", "大师", "思维"],
            "oclaw-hermes": ["hermes", "deerflow", "记忆", "桥接"]
        }
        
        suggestions = []
        for skill, keywords in skill_keywords.items():
            for kw in keywords:
                if kw in user_message.lower():
                    suggestions.append(skill)
                    break
        
        return suggestions[:5]
    
    def end_session(self, summary: str = None):
        """结束会话，进行整合"""
        if not self.session_id:
            return
        
        # 提取会话摘要
        if summary:
            self.extract_and_store_facts(summary, "general")
        
        # 存储会话元数据
        entry = MemoryEntry(
            id=hashlib.md5(f"session_end_{self.session_id}".encode()).hexdigest()[:16],
            layer="short",
            content=f"""会话结束
会话ID: {self.session_id}
记录数: {len(self.session_buffer)}
结束时间: {datetime.now().isoformat()}
摘要: {summary or '无'}""",
            source="session_manager",
            timestamp=datetime.now(),
            importance=5.0,
            metadata={
                "session_id": self.session_id,
                "record_count": len(self.session_buffer),
                "buffer": self.session_buffer
            }
        )
        
        self.engine.store(entry)
        
        # 触发记忆整合
        consolidation = self.engine.consolidate_memories("short")
        
        print(f"[AUTO-MEMORY] 会话结束: {self.session_id}")
        print(f"[AUTO-MEMORY] 整合结果: {consolidation}")
        
        self.session_id = None
        self.session_buffer = []
    
    def get_memory_report(self) -> Dict:
        """生成记忆系统报告"""
        stats = self.engine.get_stats()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "buffer_size": len(self.session_buffer),
            "memory_stats": stats,
            "status": "active"
        }

# 便捷函数
def auto_record_skill(skill_name: str, **kwargs):
    """便捷函数：记录Skill调用"""
    system = AutoMemorySystem()
    system.record_skill_call(skill_name, **kwargs)

def auto_extract_facts(content: str, fact_type: str = "general"):
    """便捷函数：提取事实"""
    system = AutoMemorySystem()
    return system.extract_and_store_facts(content, fact_type)

def get_context_for_query(query: str) -> List[Dict]:
    """便捷函数：获取相关上下文"""
    system = AutoMemorySystem()
    return system.get_relevant_context(query)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="自动记忆系统")
    parser.add_argument("command", choices=[
        "start", "record_skill", "record_intent", "extract", 
        "context", "suggest", "end", "report"
    ])
    parser.add_argument("--session-id", help="会话ID")
    parser.add_argument("--skill-name", help="Skill名称")
    parser.add_argument("--input", help="输入内容")
    parser.add_argument("--output", help="输出内容")
    parser.add_argument("--content", help="内容")
    parser.add_argument("--query", help="查询")
    parser.add_argument("--intent", help="意图")
    parser.add_argument("--type", default="general", help="事实类型")
    
    args = parser.parse_args()
    
    system = AutoMemorySystem()
    
    if args.command == "start":
        system.start_session(args.session_id)
    
    elif args.command == "record_skill":
        system.record_skill_call(
            args.skill_name,
            args.input or "",
            args.output or ""
        )
    
    elif args.command == "record_intent":
        system.record_user_intent(args.content, args.intent)
    
    elif args.command == "extract":
        entities = system.extract_and_store_facts(args.content, args.type)
        print(json.dumps({"entities": entities}, ensure_ascii=False))
    
    elif args.command == "context":
        context = system.get_relevant_context(args.query)
        print(json.dumps(context, ensure_ascii=False, indent=2))
    
    elif args.command == "suggest":
        skills = system.suggest_skills(args.query)
        print(json.dumps({"suggested_skills": skills}, ensure_ascii=False))
    
    elif args.command == "end":
        system.end_session(args.content)
    
    elif args.command == "report":
        report = system.get_memory_report()
        print(json.dumps(report, ensure_ascii=False, indent=2))
