#!/usr/bin/env python3
"""
OpenClaw 记忆系统专家
THE MEMORY EXPERT - 专业的记忆系统配置与优化

作者：ProClaw
网站：www.ProClaw.top
联系方式：wechat:Mr-zifang

功能：
1. 记忆类型详解（Basic/Vector/Graph）
2. 向量数据库配置（Chroma/Qdrant/Milvus）
3. 知识图谱配置（NetworkX/Neo4j）
4. 记忆策略优化
5. 跨会话记忆管理
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


# =============================================================================
# 记忆类型定义
# =============================================================================

class MemoryType(Enum):
    """记忆类型"""
    BASIC = "basic"           # 基础对话历史
    VECTOR = "vector"         # 向量记忆
    GRAPH = "graph"           # 知识图谱
    HYBRID = "hybrid"          # 混合记忆


class MemoryProvider(Enum):
    """记忆提供者"""
    # 向量数据库
    CHROMA = "chroma"
    QDRANT = "qdrant"
    MILVUS = "milvus"
    PINECONE = "pinecone"
    
    # 图数据库
    NETWORKX = "networkx"
    NEO4J = "neo4j"
    
    # 混合
    REDIS = "redis"
    ELASTICSEARCH = "elasticsearch"


# =============================================================================
# 记忆配置模板
# =============================================================================

class MemoryTemplates:
    """记忆配置模板库"""

    @staticmethod
    def basic_memory(
        max_history: int = 100,
        summary_enabled: bool = True,
        summary_threshold: int = 50
    ) -> Dict:
        """
        基础记忆配置
        
        适用场景：
        - 对话历史存储
        - 简单上下文管理
        - 轻量级应用
        """
        return {
            "type": "basic",
            "config": {
                "max_history": max_history,
                "summary_enabled": summary_enabled,
                "summary_threshold": summary_threshold,
                "summary_prompt": "请简要总结以下对话的要点：\n{{content}}",
                "compression_ratio": 0.5,
                "keep_recent": 10
            }
        }

    @staticmethod
    def vector_memory(
        provider: str = "chroma",
        persist_directory: str = "~/.openclaw/chroma",
        collection_name: str = "openclaw_memory",
        embedding_model: str = "text-embedding-3-small"
    ) -> Dict:
        """
        向量记忆配置
        
        适用场景：
        - 语义检索
        - 相似度搜索
        - RAG 应用
        """
        return {
            "type": "vector",
            "provider": provider,
            "config": {
                "persist_directory": persist_directory,
                "collection_name": collection_name,
                "embedding_model": embedding_model,
                "embedding_dimension": 1536,
                "metadata": {
                    "enabled": True,
                    "fields": ["source", "timestamp", "tags"]
                }
            }
        }

    @staticmethod
    def chroma_config(
        persist_directory: str = "~/.openclaw/chroma",
        collection_name: str = "memory",
        embedding_model: str = "text-embedding-3-small"
    ) -> Dict:
        """Chroma 向量数据库配置"""
        return {
            "type": "vector",
            "provider": "chroma",
            "config": {
                "persist_directory": persist_directory,
                "collection": {
                    "name": collection_name,
                    "metadata": {"hnsw:space": "cosine"}
                },
                "embedding": {
                    "model": embedding_model,
                    "dimension": 1536
                },
                "hnsw": {
                    "construction_timeout": 60,
                    "search_timeout": 30,
                    "ef_construction": 100,
                    "ef_search": 100,
                    "M": 16
                }
            }
        }

    @staticmethod
    def qdrant_config(
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "memory",
        vector_size: int = 1536
    ) -> Dict:
        """Qdrant 向量数据库配置"""
        return {
            "type": "vector",
            "provider": "qdrant",
            "config": {
                "url": f"http://{host}:{port}",
                "collection": {
                    "name": collection_name,
                    "vector_size": vector_size,
                    "distance": "Cosine"
                },
                "hnsw": {
                    "m": 16,
                    "ef_construct": 100,
                    "full_scan_threshold": 10000
                },
                "optimizers": {
                    "indexing_threshold": 20000,
                    "memmap_threshold": 50000
                }
            }
        }

    @staticmethod
    def graph_memory(
        provider: str = "networkx",
        persist_file: str = "~/.openclaw/knowledge_graph.gpickle",
        max_nodes: int = 10000
    ) -> Dict:
        """
        知识图谱记忆配置
        
        适用场景：
        - 实体关系管理
        - 复杂推理
        - 知识结构化
        """
        return {
            "type": "graph",
            "provider": provider,
            "config": {
                "persist_file": persist_file,
                "max_nodes": max_nodes,
                "node_types": ["entity", "concept", "event"],
                "edge_types": ["relates", "causes", "implies"],
                "inference": {
                    "enabled": True,
                    "max_depth": 3,
                    "pathfinding": "dijkstra"
                }
            }
        }

    @staticmethod
    def neo4j_config(
        uri: str = "bolt://localhost:7687",
        username: str = "neo4j",
        password: str = "",
        database: str = "neo4j"
    ) -> Dict:
        """Neo4j 图数据库配置"""
        return {
            "type": "graph",
            "provider": "neo4j",
            "config": {
                "uri": uri,
                "auth": {
                    "username": username,
                    "password": password
                },
                "database": database,
                "connection_pool": {
                    "max_size": 50,
                    "connection_timeout": 30
                }
            }
        }

    @staticmethod
    def hybrid_memory(
        short_term_config: Dict = None,
        long_term_config: Dict = None
    ) -> Dict:
        """
        混合记忆配置
        
        结合短期记忆和长期记忆
        """
        return {
            "type": "hybrid",
            "config": {
                "short_term": short_term_config or {
                    "type": "basic",
                    "max_history": 50
                },
                "long_term": long_term_config or {
                    "type": "vector",
                    "provider": "chroma"
                },
                "transfer": {
                    "enabled": True,
                    "strategy": "importance",  # importance / frequency / recency
                    "threshold": 0.7
                }
            }
        }


# =============================================================================
# 记忆策略
# =============================================================================

class MemoryStrategy:
    """记忆策略库"""

    @staticmethod
    def importance_based_retention() -> Dict:
        """
        基于重要性的记忆保留策略
        
        保留高价值信息，自动遗忘低价值信息
        """
        return {
            "strategy": "importance",
            "config": {
                "scoring": {
                    "method": "llm",
                    "prompt": "评估以下信息的重要性（0-1）：\n{{content}}"
                },
                "retention": {
                    "high_importance": {"keep_forever": True},
                    "medium_importance": {"keep_days": 30},
                    "low_importance": {"keep_days": 7}
                }
            }
        }

    @staticmethod
    def time_based_retention() -> Dict:
        """
        基于时间的记忆保留策略
        
        按时间自动清理记忆
        """
        return {
            "strategy": "time",
            "config": {
                "retention": {
                    "recent": {"keep_minutes": 60, "detail": "full"},
                    "short_term": {"keep_days": 7, "detail": "summary"},
                    "medium_term": {"keep_days": 30, "detail": "compressed"},
                    "long_term": {"keep_days": 365, "detail": "key_points"}
                },
                "cleanup": {
                    "schedule": "daily",
                    "time": "02:00"
                }
            }
        }

    @staticmethod
    def frequency_based_retention() -> Dict:
        """
        基于频率的记忆保留策略
        
        频繁访问的信息保留，不常访问的遗忘
        """
        return {
            "strategy": "frequency",
            "config": {
                "tracking": {
                    "read_count": True,
                    "write_count": True,
                    "last_access": True
                },
                "retention": {
                    "hot": {"access_count": ">10", "keep_forever": True},
                    "warm": {"access_count": "3-10", "keep_days": 30},
                    "cold": {"access_count": "<3", "keep_days": 7}
                }
            }
        }

    @staticmethod
    def semantic_deduplication() -> Dict:
        """
        语义去重策略
        
        自动合并语义相似的信息
        """
        return {
            "strategy": "deduplication",
            "config": {
                "enabled": True,
                "similarity_threshold": 0.95,
                "merge_strategy": "newest",  # newest / most_complete / manual
                "preserve_metadata": True,
                "track_original": True
            }
        }


# =============================================================================
# 跨会话记忆管理
# =============================================================================

class CrossSessionMemory:
    """跨会话记忆管理"""

    @staticmethod
    def user_profile_template() -> Dict:
        """用户画像记忆模板"""
        return {
            "type": "user_profile",
            "fields": {
                "preferences": {
                    "language": "string",
                    "timezone": "string",
                    "communication_style": "string",
                    "topics_of_interest": ["string"]
                },
                "background": {
                    "profession": "string",
                    "expertise": ["string"],
                    "goals": ["string"]
                },
                "interaction_history": {
                    "total_sessions": "integer",
                    "last_active": "datetime",
                    "average_session_length": "integer"
                }
            }
        }

    @staticmethod
    def context_continuity_template() -> Dict:
        """上下文连续性模板"""
        return {
            "type": "context_continuity",
            "config": {
                "enabled": True,
                "carry_forward": {
                    "summary": True,
                    "key_decisions": True,
                    "pending_tasks": True,
                    "unresolved_questions": True
                },
                "look_back": {
                    "sessions": 3,
                    "include_summaries": True
                }
            }
        }


# =============================================================================
# 记忆专家系统
# =============================================================================

class MemoryExpert:
    """
    记忆系统专家
    
    提供专业级的记忆系统配置和优化服务
    """

    def __init__(self):
        self.templates = MemoryTemplates()
        self.strategies = MemoryStrategy()

    def create_memory_config(
        self,
        memory_type: str = "basic",
        **kwargs
    ) -> Dict:
        """
        创建记忆配置
        
        Args:
            memory_type: 记忆类型 (basic/vector/graph/hybrid)
        """
        creators = {
            "basic": self.templates.basic_memory,
            "vector": self.templates.vector_memory,
            "graph": self.templates.graph_memory,
            "hybrid": self.templates.hybrid_memory
        }
        
        creator = creators.get(memory_type)
        if not creator:
            raise ValueError(f"Unknown memory type: {memory_type}")
        
        return creator(**kwargs)

    def create_vector_config(
        self,
        provider: str = "chroma",
        **kwargs
    ) -> Dict:
        """
        创建向量数据库配置
        """
        creators = {
            "chroma": self.templates.chroma_config,
            "qdrant": self.templates.qdrant_config
        }
        
        creator = creators.get(provider)
        if not creator:
            raise ValueError(f"Unknown vector provider: {provider}")
        
        return creator(**kwargs)

    def select_retention_strategy(
        self,
        use_case: str = "general"
    ) -> Dict:
        """
        选择记忆保留策略
        
        Args:
            use_case: 使用场景 (general/important/frequent)
        """
        selectors = {
            "general": self.strategies.time_based_retention,
            "important": self.strategies.importance_based_retention,
            "frequent": self.strategies.frequency_based_retention
        }
        
        return selectors.get(use_case, self.strategies.time_based_retention)()

    def optimize_memory_config(
        self,
        current_config: Dict,
        use_pattern: str = "conversational"
    ) -> Dict:
        """
        优化记忆配置
        
        Args:
            current_config: 当前配置
            use_pattern: 使用模式 (conversational/rag/agentic)
        """
        optimizations = {
            "conversational": {
                "suggestions": [
                    "增加 summary_threshold 以减少 token 消耗",
                    "启用重要性评分以保留关键信息",
                    "设置合理的 max_history 防止上下文溢出"
                ],
                "config_override": {
                    "summary_threshold": 30,
                    "max_history": 100
                }
            },
            "rag": {
                "suggestions": [
                    "使用向量记忆提升检索精度",
                    "配置合适的 top_k 和 score_threshold",
                    "启用混合记忆结合向量和图谱"
                ],
                "config_override": {
                    "embedding_dimension": 1536,
                    "top_k": 5,
                    "score_threshold": 0.7
                }
            },
            "agentic": {
                "suggestions": [
                    "启用知识图谱以支持复杂推理",
                    "配置跨会话上下文连续性",
                    "使用混合记忆结合短期和长期"
                ],
                "config_override": {
                    "context_continuity": True,
                    "graph_inference": True
                }
            }
        }
        
        opt = optimizations.get(use_pattern, optimizations["conversational"])
        
        # 合并配置
        optimized = current_config.copy()
        optimized.update(opt.get("config_override", {}))
        
        return {
            "original": current_config,
            "optimized": optimized,
            "suggestions": opt["suggestions"]
        }

    def validate_memory_config(self, config: Dict) -> Tuple[bool, List[str]]:
        """
        验证记忆配置
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        if "type" not in config:
            errors.append("缺少 type 字段")
        
        memory_type = config.get("type")
        
        # 类型特定验证
        if memory_type == "vector":
            if "config" not in config:
                errors.append("向量记忆缺少 config 字段")
            else:
                cfg = config["config"]
                if "persist_directory" not in cfg and "url" not in cfg:
                    errors.append("向量记忆缺少持久化配置")
        
        elif memory_type == "graph":
            if "provider" not in config:
                errors.append("图谱记忆缺少 provider 字段")
            elif config["provider"] == "neo4j":
                if "config" in config:
                    auth = config["config"].get("auth", {})
                    if not auth.get("password"):
                        errors.append("Neo4j 缺少密码配置")
        
        return len(errors) == 0, errors


# =============================================================================
# 主函数
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw 记忆系统专家 v5.0"
    )

    # 创建配置
    parser.add_argument("--create", choices=["basic", "vector", "graph", "hybrid"],
                       help="创建记忆配置")
    parser.add_argument("--provider", choices=["chroma", "qdrant", "neo4j", "networkx"],
                       help="数据库提供者")
    parser.add_argument("--output", "-o", help="输出文件路径")

    # 策略选择
    parser.add_argument("--strategy", choices=["importance", "time", "frequency", "dedup"],
                       help="选择保留策略")

    # 优化
    parser.add_argument("--optimize", action="store_true", help="优化配置")
    parser.add_argument("--use-pattern", choices=["conversational", "rag", "agentic"],
                       default="conversational", help="使用模式")
    parser.add_argument("--config-file", help="配置文件路径")

    # 验证
    parser.add_argument("--validate", help="验证配置文件")

    args = parser.parse_args()

    expert = MemoryExpert()

    if args.create:
        config = expert.create_memory_config(
            memory_type=args.create,
            provider=args.provider or "chroma"
        )
        output = json.dumps(config, indent=2, ensure_ascii=False)
        
        if args.output:
            Path(args.output).write_text(output)
            print(f"配置已保存: {args.output}")
        else:
            print(output)

    elif args.strategy:
        strategy = expert.select_retention_strategy(args.strategy)
        print(json.dumps(strategy, indent=2, ensure_ascii=False))

    elif args.optimize and args.config_file:
        with open(args.config_file) as f:
            config = json.load(f)
        
        result = expert.optimize_memory_config(
            config,
            use_pattern=args.use_pattern
        )
        
        print("优化建议:")
        for suggestion in result["suggestions"]:
            print(f"  - {suggestion}")
        print("\n优化后配置:")
        print(json.dumps(result["optimized"], indent=2, ensure_ascii=False))

    elif args.validate:
        with open(args.validate) as f:
            config = json.load(f)
        
        is_valid, errors = expert.validate_memory_config(config)
        
        if is_valid:
            print("配置验证通过")
        else:
            print("配置验证失败:")
            for error in errors:
                print(f"  - {error}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
