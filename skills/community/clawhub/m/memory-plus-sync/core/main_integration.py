"""
Memory-Plus 主集成模块
整合所有功能：三代理验证 + Mem0 + Qdrant
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# 导入各个模块
from core.config_manager import config_manager
from core.triple_agent_processor_updated import TripleAgentProcessor
from core.qdrant_integration import qdrant_integration
from core.memory_dedup import MemoryDeduplicator as MemoryDedup
from core.mem0_integration import Mem0Integration

logger = logging.getLogger(__name__)

class MemoryPlusIntegration:
    """Memory-Plus 主集成类"""
    
    def __init__(self):
        """初始化 Memory-Plus 集成"""
        self.config = config_manager
        self.triple_agent = TripleAgentProcessor()
        self.qdrant = qdrant_integration
        self.dedup = MemoryDedup()
        self.mem0 = Mem0Integration()
        
        # 状态跟踪
        self.stats = {
            "total_processed": 0,
            "validated": 0,
            "stored": 0,
            "duplicates_removed": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat()
        }
        
        logger.info("✅ Memory-Plus 集成初始化完成")
    
    async def process_and_store_memory(self, memory_content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        处理并存储记忆（完整流程）
        
        Args:
            memory_content: 记忆内容
            metadata: 附加元数据
            
        Returns:
            处理结果
        """
        result = {
            "success": False,
            "memory_id": None,
            "validation_result": None,
            "storage_result": None,
            "errors": []
        }
        
        try:
            # 1. 去重检查
            dedup_result = self.dedup.check_duplicate(memory_content)
            if dedup_result.is_duplicate:
                result["duplicate"] = True
                result["message"] = "记忆内容重复，跳过存储"
                self.stats["duplicates_removed"] += 1
                return result
            
            # 2. 三代理验证
            logger.info("🔍 开始三代理验证...")
            validation_results = await self.triple_agent.process_memory_async(memory_content)
            result["validation_result"] = validation_results
            
            # 3. 聚合验证结果
            final_decision = self._aggregate_validation(validation_results)
            result["final_decision"] = final_decision
            
            if not final_decision.get("should_store", False):
                result["message"] = "验证未通过，不存储"
                return result
            
            # 4. 准备存储数据
            storage_data = {
                "content": memory_content,
                "metadata": metadata or {},
                "validation_scores": final_decision.get("scores", {}),
                "category": final_decision.get("category", "other"),
                "importance": final_decision.get("importance", 5),
                "timestamp": datetime.now().isoformat()
            }
            
            # 5. 存储到 Mem0
            logger.info("💾 存储到 Mem0...")
            mem0_result = self.mem0.store_memory(storage_data)
            if mem0_result.get("success"):
                result["memory_id"] = mem0_result.get("memory_id")
                result["mem0_result"] = mem0_result
            else:
                result["errors"].append(f"Mem0 存储失败: {mem0_result.get('error')}")
            
            # 6. 同步到 Qdrant（如果 Mem0 存储成功）
            if result["memory_id"]:
                logger.info("🔄 同步到 Qdrant...")
                qdrant_result = self._sync_to_qdrant(storage_data, result["memory_id"])
                result["qdrant_result"] = qdrant_result
            
            # 7. 更新统计
            self.stats["total_processed"] += 1
            self.stats["validated"] += 1
            if result["memory_id"]:
                self.stats["stored"] += 1
            
            result["success"] = True
            result["message"] = "记忆处理并存储成功"
            
        except Exception as e:
            logger.error(f"处理记忆失败: {e}")
            result["errors"].append(str(e))
            self.stats["errors"] += 1
        
        return result
    
    def _aggregate_validation(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """聚合三代理验证结果"""
        aggregated = {
            "should_store": False,
            "scores": {},
            "category": "other",
            "importance": 5,
            "confidence": 0.0
        }
        
        try:
            # 提取各代理的推荐
            recommendations = []
            scores = {}
            
            for agent_name, response in validation_results.items():
                if response.success and response.response_data:
                    data = response.response_data
                    
                    # 收集推荐
                    if "recommendation" in data:
                        rec = data["recommendation"]
                        if "存储" in rec or "通过" in rec:
                            recommendations.append(True)
                        elif "拒绝" in rec:
                            recommendations.append(False)
                        else:
                            recommendations.append(True)  # 默认通过
                    
                    # 收集分数
                    for key, value in data.items():
                        if "score" in key.lower():
                            scores[f"{agent_name}_{key}"] = value
                    
                    # 收集分类和重要性
                    if "memory_type" in data:
                        aggregated["category"] = data["memory_type"]
                    if "importance_score" in data:
                        aggregated["importance"] = data["importance_score"]
            
            # 计算最终决策
            if recommendations:
                # 简单多数投票
                true_count = sum(1 for r in recommendations if r)
                false_count = len(recommendations) - true_count
                
                aggregated["should_store"] = true_count >= false_count
                aggregated["confidence"] = true_count / len(recommendations) if recommendations else 0.0
            
            aggregated["scores"] = scores
            
        except Exception as e:
            logger.error(f"聚合验证结果失败: {e}")
            aggregated["should_store"] = True  # 失败时默认存储
            aggregated["confidence"] = 0.5
        
        return aggregated
    
    def _sync_to_qdrant(self, storage_data: Dict[str, Any], memory_id: str) -> Dict[str, Any]:
        """同步到 Qdrant"""
        try:
            # 这里应该生成向量并存储到 Qdrant
            # 目前先返回模拟结果
            return {
                "success": True,
                "message": "Qdrant 同步成功（模拟）",
                "point_id": f"qdrant_{memory_id}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Qdrant 同步失败: {str(e)}"
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.stats.copy()
        stats["current_time"] = datetime.now().isoformat()
        stats["uptime_seconds"] = (datetime.now() - datetime.fromisoformat(stats["start_time"])).total_seconds()
        return stats
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            "total_processed": 0,
            "validated": 0,
            "stored": 0,
            "duplicates_removed": 0,
            "errors": 0,
            "start_time": datetime.now().isoformat()
        }
        logger.info("📊 统计已重置")

# 全局 Memory-Plus 集成实例
memory_plus_integration = MemoryPlusIntegration()

if __name__ == "__main__":
    # 测试 Memory-Plus 集成
    print("🧪 测试 Memory-Plus 集成...")
    
    # 创建集成实例
    mpi = MemoryPlusIntegration()
    
    # 测试处理记忆
    test_memory = "Memory-Plus 集成测试完成，所有功能正常。"
    
    async def test():
        result = await mpi.process_and_store_memory(test_memory, {"test": True})
        print(f"处理结果: {result['success']} - {result.get('message', '')}")
        
        if result.get('validation_result'):
            print("验证结果:")
            for agent, response in result['validation_result'].items():
                print(f"  {agent}: {response.success} - {response.response_data.get('recommendation', 'N/A')}")
        
        # 显示统计
        stats = mpi.get_stats()
        print(f"\n统计信息:")
        for key, value in stats.items():
            if key not in ["start_time", "current_time"]:
                print(f"  {key}: {value}")
    
    asyncio.run(test())