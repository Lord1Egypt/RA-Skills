"""
Qdrant 向量数据库集成模块
用于同步 Memory-Plus 记忆到 Qdrant
"""

import json
import logging
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class QdrantIntegration:
    """Qdrant 向量数据库集成"""
    
    def __init__(self, host: str = "localhost", port: int = 6333):
        """
        初始化 Qdrant 集成
        
        Args:
            host: Qdrant 主机地址
            port: Qdrant 端口
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.collection_name = "mem0_memories_restored"
        
        # 测试连接
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """测试 Qdrant 连接"""
        try:
            response = requests.get(f"{self.base_url}/collections", timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ Qdrant 连接成功: {self.base_url}")
                return True
            else:
                logger.error(f"❌ Qdrant 连接失败: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Qdrant 连接异常: {e}")
            return False
    
    def get_collection_info(self) -> Dict[str, Any]:
        """获取集合信息"""
        try:
            url = f"{self.base_url}/collections/{self.collection_name}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.warning(f"集合不存在: {self.collection_name}")
                return {"error": "collection_not_found"}
            else:
                logger.error(f"获取集合信息失败: {response.status_code}")
                return {"error": f"status_{response.status_code}"}
        except Exception as e:
            logger.error(f"获取集合信息异常: {e}")
            return {"error": str(e)}
    
    def create_collection(self, vector_size: int = 1024) -> bool:
        """创建集合（如果不存在）"""
        try:
            # 检查集合是否存在
            info = self.get_collection_info()
            if "error" not in info or info["error"] != "collection_not_found":
                logger.info(f"集合已存在: {self.collection_name}")
                return True
            
            # 创建集合
            url = f"{self.base_url}/collections/{self.collection_name}"
            payload = {
                "vectors": {
                    "size": vector_size,
                    "distance": "Cosine"
                }
            }
            
            response = requests.put(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ 创建集合成功: {self.collection_name}")
                return True
            else:
                logger.error(f"❌ 创建集合失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 创建集合异常: {e}")
            return False
    
    def upsert_points(self, points: List[Dict[str, Any]]) -> bool:
        """
        插入或更新点
        
        Args:
            points: 点列表，每个点包含 id 和 vector
            
        Returns:
            是否成功
        """
        try:
            url = f"{self.base_url}/collections/{self.collection_name}/points"
            payload = {
                "points": points
            }
            
            response = requests.put(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"✅ 插入 {len(points)} 个点成功")
                return True
            else:
                logger.error(f"❌ 插入点失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 插入点异常: {e}")
            return False
    
    def search_similar(self, vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        搜索相似向量
        
        Args:
            vector: 查询向量
            limit: 返回结果数量
            
        Returns:
            相似点列表
        """
        try:
            url = f"{self.base_url}/collections/{self.collection_name}/points/search"
            payload = {
                "vector": vector,
                "limit": limit,
                "with_payload": True
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("result", [])
            else:
                logger.error(f"搜索失败: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"搜索异常: {e}")
            return []
    
    def get_point_count(self) -> int:
        """获取集合中的点数"""
        try:
            info = self.get_collection_info()
            if "error" in info:
                return 0
            return info.get("result", {}).get("vectors_count", 0)
        except Exception as e:
            logger.error(f"获取点数失败: {e}")
            return 0
    
    def sync_from_mem0(self, mem0_db_path: str) -> Dict[str, Any]:
        """
        从 Mem0 数据库同步到 Qdrant
        
        Args:
            mem0_db_path: Mem0 SQLite 数据库路径
            
        Returns:
            同步结果统计
        """
        import sqlite3
        
        stats = {
            "total_mem0_records": 0,
            "successful_sync": 0,
            "failed_sync": 0,
            "start_time": datetime.now().isoformat(),
            "end_time": None
        }
        
        try:
            # 连接 Mem0 数据库
            conn = sqlite3.connect(mem0_db_path)
            cursor = conn.cursor()
            
            # 获取所有向量记录
            cursor.execute("SELECT id, vector, metadata FROM vectors")
            records = cursor.fetchall()
            
            stats["total_mem0_records"] = len(records)
            logger.info(f"从 Mem0 读取 {len(records)} 条记录")
            
            # 准备 Qdrant 点
            points = []
            for record_id, vector_blob, metadata_blob in records:
                try:
                    # 解析向量（假设是 JSON 格式）
                    vector = json.loads(vector_blob) if vector_blob else []
                    
                    # 解析元数据
                    metadata = json.loads(metadata_blob) if metadata_blob else {}
                    
                    # 创建点
                    point = {
                        "id": record_id,
                        "vector": vector,
                        "payload": metadata
                    }
                    
                    points.append(point)
                    stats["successful_sync"] += 1
                    
                except Exception as e:
                    logger.error(f"解析记录 {record_id} 失败: {e}")
                    stats["failed_sync"] += 1
            
            # 批量插入到 Qdrant
            if points:
                batch_size = 100
                for i in range(0, len(points), batch_size):
                    batch = points[i:i+batch_size]
                    if self.upsert_points(batch):
                        logger.info(f"同步批次 {i//batch_size + 1}: {len(batch)} 条")
                    else:
                        logger.error(f"批次 {i//batch_size + 1} 同步失败")
                        stats["failed_sync"] += len(batch)
            
            conn.close()
            
        except Exception as e:
            logger.error(f"同步 Mem0 数据失败: {e}")
            stats["failed_sync"] = stats["total_mem0_records"]
        
        stats["end_time"] = datetime.now().isoformat()
        return stats
    
    def export_to_json(self, output_path: str) -> bool:
        """
        导出 Qdrant 数据到 JSON 文件
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            是否成功
        """
        try:
            # 获取所有点
            url = f"{self.base_url}/collections/{self.collection_name}/points"
            payload = {
                "limit": 10000,  # 最大限制
                "with_payload": True,
                "with_vector": True
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                points = data.get("result", {}).get("points", [])
                
                # 保存到文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(points, f, indent=2, ensure_ascii=False)
                
                logger.info(f"✅ 导出 {len(points)} 个点到 {output_path}")
                return True
            else:
                logger.error(f"❌ 导出失败: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 导出异常: {e}")
            return False

# 全局 Qdrant 集成实例
qdrant_integration = QdrantIntegration()

if __name__ == "__main__":
    # 测试 Qdrant 集成
    print("🧪 测试 Qdrant 集成...")
    
    # 测试连接
    if qdrant_integration._test_connection():
        print("✅ Qdrant 连接成功")
        
        # 获取集合信息
        info = qdrant_integration.get_collection_info()
        if "error" in info and info["error"] == "collection_not_found":
            print("ℹ️  集合不存在，创建新集合...")
            if qdrant_integration.create_collection():
                print("✅ 集合创建成功")
        else:
            print(f"✅ 集合已存在，点数: {qdrant_integration.get_point_count()}")
        
        # 测试搜索（使用零向量）
        test_vector = [0.0] * 1024
        results = qdrant_integration.search_similar(test_vector, limit=3)
        print(f"✅ 搜索测试成功，返回 {len(results)} 个结果")
        
    else:
        print("❌ Qdrant 连接失败")
