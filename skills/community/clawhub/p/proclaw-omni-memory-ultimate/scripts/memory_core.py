#!/usr/bin/env python3
"""
Omni-Memory Core - 核心记忆管理器
融合向量存储、流体衰减、自动分类
"""

import os
import sys
import time
import math
import json
import argparse
import hashlib
from datetime import datetime
from typing import Optional, List, Dict, Any

try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False
    print("[WARN] ChromaDB not installed, running in simulation mode.")

# 配置路径
WORKSPACE_ROOT = os.getcwd()
MEMORY_DIR = os.path.join(WORKSPACE_ROOT, "memory")
VECTOR_PATH = os.path.join(MEMORY_DIR, "vectors")
SESSION_STATE_PATH = os.path.join(WORKSPACE_ROOT, "SESSION-STATE.md")
MEMORY_INDEX_PATH = os.path.join(WORKSPACE_ROOT, "MEMORY.md")

# 流体衰减参数
LAMBDA_DECAY = 0.05  # 遗忘速度
ALPHA_BOOST = 0.2    # 强化力度
MIN_SCORE = 0.05     # 最低阈值
DEDUP_THRESHOLD = 0.95  # 去重阈值


class FluidMemory:
    """流体记忆管理器 - 基于艾宾浩斯遗忘曲线"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self._init_chroma()
    
    def _init_chroma(self):
        """初始化ChromaDB"""
        if not HAS_CHROMA:
            return
        
        try:
            os.makedirs(VECTOR_PATH, exist_ok=True)
            self.client = chromadb.PersistentClient(path=VECTOR_PATH)
            self.collection = self.client.get_or_create_collection(
                name="omni_memory",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"[ERROR] ChromaDB初始化失败: {e}")
            self.client = None
            self.collection = None
    
    def _calculate_score(self, similarity: float, created_at: float, access_count: int) -> float:
        """
        流体衰减核心公式
        score = (similarity * decay) + boost
        """
        days_passed = (time.time() - created_at) / 86400
        decay = math.exp(-LAMBDA_DECAY * days_passed)
        boost = ALPHA_BOOST * math.log(1 + access_count)
        return (similarity * decay) + boost
    
    def _generate_id(self, content: str) -> str:
        """生成内容哈希ID"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def store(self, content: str, memory_type: str = "other", 
              importance: float = 0.7) -> Dict[str, Any]:
        """
        存储记忆
        
        Args:
            content: 记忆内容
            memory_type: 记忆类型 (user/feedback/project/reference)
            importance: 重要性 (0.0-1.0)
        
        Returns:
            {"success": bool, "id": str, "duplicate": bool}
        """
        if not self.collection:
            return {"success": False, "error": "ChromaDB not available"}
        
        mem_id = self._generate_id(content)
        now = time.time()
        
        # 去重检查
        try:
            existing = self.collection.query(
                query_texts=[content],
                n_results=1,
                where={"status": "active"}
            )
            if existing['ids'] and existing['distances'][0]:
                if 1 - existing['distances'][0][0] > DEDUP_THRESHOLD:
                    return {"success": True, "id": existing['ids'][0], "duplicate": True}
        except Exception:
            pass
        
        # 存储新记忆
        try:
            self.collection.add(
                documents=[content],
                metadatas=[{
                    "type": memory_type,
                    "importance": importance,
                    "created_at": now,
                    "last_accessed": now,
                    "access_count": 0,
                    "status": "active"
                }],
                ids=[mem_id]
            )
            return {"success": True, "id": mem_id, "duplicate": False}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def recall(self, query: str, limit: int = 5, 
               memory_type: Optional[str] = None,
               min_score: float = MIN_SCORE) -> List[Dict[str, Any]]:
        """
        检索记忆
        
        Args:
            query: 查询内容
            limit: 返回数量
            memory_type: 过滤类型
            min_score: 最低分数阈值
        
        Returns:
            记忆列表，按分数排序
        """
        if not self.collection:
            return []
        
        # 构建过滤条件
        where_filter = {"status": "active"}
        if memory_type:
            where_filter["type"] = memory_type
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=min(limit * 3, 20),  # 多取一些用于过滤
                where=where_filter
            )
        except Exception as e:
            print(f"[ERROR] 检索失败: {e}")
            return []
        
        if not results['ids'] or not results['ids'][0]:
            return []
        
        scored_memories = []
        ids = results['ids'][0]
        docs = results['documents'][0]
        metas = results['metadatas'][0]
        distances = results['distances'][0]
        
        for i in range(len(ids)):
            # 距离转相似度
            similarity = 1 - distances[i]
            
            meta = metas[i]
            created_at = meta.get('created_at', time.time())
            access_count = meta.get('access_count', 0)
            
            # 计算流体分数
            final_score = self._calculate_score(similarity, created_at, access_count)
            
            if final_score >= min_score:
                scored_memories.append({
                    "id": ids[i],
                    "content": docs[i],
                    "score": round(final_score, 4),
                    "type": meta.get('type', 'other'),
                    "importance": meta.get('importance', 0.5),
                    "created_at": created_at,
                    "access_count": access_count
                })
        
        # 排序并限制数量
        scored_memories.sort(key=lambda x: x['score'], reverse=True)
        top_memories = scored_memories[:limit]
        
        # 强化机制：更新top记忆的访问次数
        if top_memories:
            for mem in top_memories[:3]:  # 只强化top3
                try:
                    new_count = mem['access_count'] + 1
                    self.collection.update(
                        ids=[mem['id']],
                        metadatas=[{
                            "type": mem['type'],
                            "importance": mem['importance'],
                            "created_at": mem['created_at'],
                            "last_accessed": time.time(),
                            "access_count": new_count,
                            "status": "active"
                        }]
                    )
                except Exception:
                    pass
        
        return top_memories
    
    def forget(self, keyword: str) -> Dict[str, Any]:
        """
        遗忘记忆（软删除/归档）
        
        Args:
            keyword: 关键词
        
        Returns:
            {"success": bool, "archived": str}
        """
        if not self.collection:
            return {"success": False, "error": "ChromaDB not available"}
        
        try:
            results = self.collection.query(
                query_texts=[keyword],
                n_results=1,
                where={"status": "active"}
            )
            
            if results['ids'] and results['ids'][0]:
                target_id = results['ids'][0][0]
                target_text = results['documents'][0][0]
                current_meta = results['metadatas'][0][0]
                
                # 更新状态为archive
                current_meta['status'] = 'archived'
                self.collection.update(
                    ids=[target_id],
                    metadatas=[current_meta]
                )
                return {"success": True, "archived": target_text}
            else:
                return {"success": False, "error": "未找到相关记忆"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def status(self) -> Dict[str, Any]:
        """获取记忆系统状态"""
        if not self.collection:
            return {"status": "ChromaDB not available"}
        
        try:
            total = self.collection.count()
            
            # 统计各类型数量
            type_counts = {}
            for t in ['user', 'feedback', 'project', 'reference', 'other']:
                try:
                    result = self.collection.get(
                        where={"type": t, "status": "active"}
                    )
                    type_counts[t] = len(result['ids'])
                except Exception:
                    type_counts[t] = 0
            
            return {
                "total_memories": total,
                "active_by_type": type_counts,
                "vector_path": VECTOR_PATH
            }
        except Exception as e:
            return {"status": f"Error: {e}"}


def ensure_session_state():
    """确保SESSION-STATE.md存在"""
    if not os.path.exists(SESSION_STATE_PATH):
        template = """# SESSION-STATE.md — 活跃工作记忆

## Current Task
[None]

## Key Context
[None yet]

## Pending Actions
- [ ] None

## Recent Decisions
[None yet]

---
*Last updated: {timestamp}*
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"))
        with open(SESSION_STATE_PATH, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"[INFO] Created {SESSION_STATE_PATH}")


def ensure_memory_structure():
    """确保记忆目录结构存在"""
    dirs = [
        MEMORY_DIR,
        os.path.join(MEMORY_DIR, "user"),
        os.path.join(MEMORY_DIR, "feedback"),
        os.path.join(MEMORY_DIR, "project"),
        os.path.join(MEMORY_DIR, "reference"),
        os.path.join(MEMORY_DIR, "vectors"),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Omni-Memory Core")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # store命令
    store_parser = subparsers.add_parser("store", help="存储记忆")
    store_parser.add_argument("--content", required=True, help="记忆内容")
    store_parser.add_argument("--type", default="other", 
                              choices=["user", "feedback", "project", "reference", "other"],
                              help="记忆类型")
    store_parser.add_argument("--importance", type=float, default=0.7, help="重要性")
    
    # recall命令
    recall_parser = subparsers.add_parser("recall", help="检索记忆")
    recall_parser.add_argument("--query", required=True, help="查询内容")
    recall_parser.add_argument("--limit", type=int, default=5, help="返回数量")
    recall_parser.add_argument("--type", choices=["user", "feedback", "project", "reference"],
                               help="过滤类型")
    
    # forget命令
    forget_parser = subparsers.add_parser("forget", help="遗忘记忆")
    forget_parser.add_argument("--keyword", required=True, help="关键词")
    
    # status命令
    subparsers.add_parser("status", help="查看状态")
    
    # init命令
    subparsers.add_parser("init", help="初始化记忆系统")
    
    args = parser.parse_args()
    
    memory = FluidMemory()
    
    if args.command == "init":
        ensure_memory_structure()
        ensure_session_state()
        print("[OK] Memory system initialized")
        
    elif args.command == "store":
        result = memory.store(args.content, args.type, args.importance)
        if result.get("success"):
            if result.get("duplicate"):
                print(f"[SKIP] Duplicate memory: {result['id']}")
            else:
                print(f"[OK] Stored memory: {result['id']}")
        else:
            print(f"[ERROR] {result.get('error', 'Unknown error')}")
            
    elif args.command == "recall":
        results = memory.recall(args.query, args.limit, args.type)
        if results:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print("[EMPTY] No relevant memories found")
            
    elif args.command == "forget":
        result = memory.forget(args.keyword)
        if result.get("success"):
            print(f"[ARCHIVED] {result['archived']}")
        else:
            print(f"[ERROR] {result.get('error', 'Unknown error')}")
            
    elif args.command == "status":
        status = memory.status()
        print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
