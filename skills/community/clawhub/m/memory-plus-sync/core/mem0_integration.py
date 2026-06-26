"""
Mem0 存储集成模块

将三代理验证后的记忆存储到 Mem0 数据库
"""

import json
import sqlite3
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from .triple_agent_processor import TripleAgentProcessor, AgentResponse
from .vote_aggregator import VoteAggregator, AggregatedResult
from .llm_arbiter import LLMArbiter, ArbitrationResult


@dataclass
class MemoryRecord:
    """记忆记录"""
    id: Optional[int]
    content: str
    user_id: str
    memory_type: str
    importance: str
    tags: List[str]
    metadata: Dict[str, Any]
    validation_results: Dict[str, Any]
    created_at: str
    updated_at: str


class Mem0Integration:
    """Mem0 存储集成"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        初始化 Mem0 集成
        
        Args:
            db_path: SQLite 数据库路径，默认使用 ~/.openclaw/memory/main.sqlite
        """
        if db_path is None:
            db_path = str(Path.home() / ".openclaw" / "memory" / "main.sqlite")
        
        self.db_path = db_path
        self.triple_processor = TripleAgentProcessor(use_kimi=True)
        self.vote_aggregator = VoteAggregator()
        self.arbiter = LLMArbiter(use_kimi=True)
        
        # 确保数据库存在
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建记忆表 (如果不存在)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS validated_memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id TEXT NOT NULL,
            memory_type TEXT,
            importance TEXT,
            tags TEXT,
            metadata TEXT,
            validation_results TEXT,
            arbitration_result TEXT,
            final_decision TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)
        
        # 创建索引
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_id ON validated_memories(user_id)
        """)
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_memory_type ON validated_memories(memory_type)
        """)
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_created_at ON validated_memories(created_at)
        """)
        
        conn.commit()
        conn.close()
    
    def process_and_store(
        self,
        memory_content: str,
        user_id: str = "default",
        force_store: bool = False
    ) -> Dict[str, Any]:
        """
        处理并存储记忆
        
        Args:
            memory_content: 记忆内容
            user_id: 用户 ID
            force_store: 是否强制存储 (跳过验证)
        
        Returns:
            处理结果字典
        """
        result = {
            "success": False,
            "memory_id": None,
            "decision": None,
            "validation": None,
            "arbitration": None,
            "latency_ms": 0,
            "error": None
        }
        
        start_time = time.time()
        
        try:
            if force_store:
                # 强制存储，跳过验证
                memory_id = self._store_memory(
                    content=memory_content,
                    user_id=user_id,
                    validation_results={"forced": True},
                    final_decision="FORCE_STORE"
                )
                result["success"] = True
                result["memory_id"] = memory_id
                result["decision"] = "FORCE_STORE"
                result["latency_ms"] = (time.time() - start_time) * 1000
                return result
            
            # 1. 三代理并行验证
            print("📊 步骤 1/3: 三代理并行验证...")
            responses = self.triple_processor.process_memory_sync(memory_content)
            
            # 2. 投票聚合
            print("📊 步骤 2/3: 投票聚合...")
            aggregated_result = self.vote_aggregator.aggregate(responses)
            
            result["validation"] = {
                "vote_result": aggregated_result.vote_result.value,
                "vote_counts": aggregated_result.vote_counts,
                "confidence": aggregated_result.confidence,
                "needs_arbitration": aggregated_result.needs_arbitration,
                "reasoning": aggregated_result.reasoning
            }
            
            # 3. 如果需要仲裁，调用仲裁模型
            final_decision = aggregated_result.final_decision
            arbitration_result = None
            
            if aggregated_result.needs_arbitration:
                print("📊 步骤 3/3: 启动仲裁...")
                arbitration_result = self.arbiter.arbitrate(memory_content, aggregated_result)
                final_decision = arbitration_result.final_decision
                
                result["arbitration"] = {
                    "decision": arbitration_result.final_decision,
                    "confidence": arbitration_result.confidence,
                    "reasoning": arbitration_result.reasoning,
                    "model_used": arbitration_result.model_used
                }
            else:
                print("📊 步骤 3/3: 无需仲裁")
            
            result["decision"] = final_decision
            
            # 4. 根据最终决定存储
            if final_decision in ["STORE", "APPROVE", "MERGE"]:
                # 提取验证结果
                validation_data = {}
                for agent_name, response in responses.items():
                    if response.success:
                        validation_data[agent_name] = response.response_data
                
                memory_id = self._store_memory(
                    content=memory_content,
                    user_id=user_id,
                    validation_results=validation_data,
                    arbitration_result=asdict(arbitration_result) if arbitration_result else None,
                    final_decision=final_decision
                )
                
                result["success"] = True
                result["memory_id"] = memory_id
                print(f"✅ 记忆已存储，ID: {memory_id}")
            
            elif final_decision == "REJECT":
                print("❌ 记忆被拒绝存储")
                result["success"] = False
                result["decision"] = "REJECT"
            
            else:  # REVIEW
                print("⚠️  记忆需要人工审核")
                result["success"] = False
                result["decision"] = "REVIEW"
            
            result["latency_ms"] = (time.time() - start_time) * 1000
            
        except Exception as e:
            result["error"] = str(e)
            result["latency_ms"] = (time.time() - start_time) * 1000
            import traceback
            print(f"❌ 处理失败：{e}")
            print(traceback.format_exc())
        
        return result
    
    def _store_memory(
        self,
        content: str,
        user_id: str,
        validation_results: Dict,
        arbitration_result: Optional[Dict] = None,
        final_decision: str = "STORE"
    ) -> int:
        """
        将记忆存储到数据库
        
        Returns:
            记忆 ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 从验证结果中提取元数据
        memory_type = "UNKNOWN"
        importance = "NORMAL"
        tags = []
        
        if "scorer" in validation_results:
            scorer_data = validation_results["scorer"]
            memory_type = scorer_data.get("memory_type", "UNKNOWN")
            importance = scorer_data.get("importance", "NORMAL")
            tags = scorer_data.get("suggested_tags", [])
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
        INSERT INTO validated_memories 
        (content, user_id, memory_type, importance, tags, metadata, 
         validation_results, arbitration_result, final_decision, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            content,
            user_id,
            memory_type,
            importance,
            json.dumps(tags, ensure_ascii=False),
            json.dumps({}, ensure_ascii=False),
            json.dumps(validation_results, ensure_ascii=False),
            json.dumps(arbitration_result, ensure_ascii=False) if arbitration_result else None,
            final_decision,
            now,
            now
        ))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return memory_id
    
    def get_memory(self, memory_id: int) -> Optional[MemoryRecord]:
        """获取单条记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, content, user_id, memory_type, importance, tags, metadata,
               validation_results, created_at, updated_at
        FROM validated_memories
        WHERE id = ?
        """, (memory_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return MemoryRecord(
                id=row[0],
                content=row[1],
                user_id=row[2],
                memory_type=row[3],
                importance=row[4],
                tags=json.loads(row[5]) if row[5] else [],
                metadata=json.loads(row[6]) if row[6] else {},
                validation_results=json.loads(row[7]) if row[7] else {},
                created_at=row[8],
                updated_at=row[9]
            )
        
        return None
    
    def search_memories(self, query: str, user_id: Optional[str] = None, limit: int = 10) -> List[MemoryRecord]:
        """搜索记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("""
            SELECT id, content, user_id, memory_type, importance, tags, metadata,
                   validation_results, created_at, updated_at
            FROM validated_memories
            WHERE user_id = ? AND content LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
            """, (user_id, f"%{query}%", limit))
        else:
            cursor.execute("""
            SELECT id, content, user_id, memory_type, importance, tags, metadata,
                   validation_results, created_at, updated_at
            FROM validated_memories
            WHERE content LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
            """, (f"%{query}%", limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in rows:
            memories.append(MemoryRecord(
                id=row[0],
                content=row[1],
                user_id=row[2],
                memory_type=row[3],
                importance=row[4],
                tags=json.loads(row[5]) if row[5] else [],
                metadata=json.loads(row[6]) if row[6] else {},
                validation_results=json.loads(row[7]) if row[7] else {},
                created_at=row[8],
                updated_at=row[9]
            ))
        
        return memories


if __name__ == "__main__":
    # 测试 Mem0 集成
    print("=== Mem0 集成测试 ===\n")
    
    mem0 = Mem0Integration()
    
    test_memory = f"""
    2026-04-03 {time.strftime('%H:%M')} 测试记忆存储功能。
    这是一条用于测试三代理验证模块的记忆内容。
    包含一些关键信息：项目=Memory-Plus, 优先级=P2, 状态=开发中
    """
    
    result = mem0.process_and_store(
        memory_content=test_memory,
        user_id="test_user",
        force_store=False
    )
    
    print(f"\n处理结果:")
    print(f"  成功：{result['success']}")
    print(f"  决定：{result['decision']}")
    print(f"  记忆 ID: {result['memory_id']}")
    print(f"  耗时：{result['latency_ms']:.0f}ms")
    
    if result.get("validation"):
        print(f"\n验证结果:")
        print(f"  投票：{result['validation']['vote_counts']}")
        print(f"  置信度：{result['validation']['confidence']:.2f}")
        print(f"  需要仲裁：{result['validation']['needs_arbitration']}")
    
    if result.get("arbitration"):
        print(f"\n仲裁结果:")
        print(f"  决定：{result['arbitration']['decision']}")
        print(f"  模型：{result['arbitration']['model_used']}")
    
    if result.get("error"):
        print(f"\n错误：{result['error']}")
    
    print("\n=== 测试完成 ===")
