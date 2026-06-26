"""
L1 热存储 - 内存字典实现 (v1.0.1 Hotfix)

修复内容:
1. 添加内存上限强制执行 - LRU淘汰机制
2. 添加条目数量限制
3. 添加内存使用统计
"""
import time
from typing import Optional, Dict, Any
from app.models import MemoryItem, MemoryLevel


class L1HotStorage:
    """L1热存储 - 纯内存实现 (带LRU淘汰)"""
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = 100 * 1024 * 1024  # 100MB (修正: 原来是100KB太小)
        self.max_entries = 10000  # 最多10000条
        self.ttl = 3600  # 1小时
        self.access_count = 0  # 访问计数用于LRU
    
    async def init(self):
        """初始化 (无需操作)"""
        print(f"[L1] Memory cache initialized (max: {self.max_size / 1024 / 1024:.0f}MB, max entries: {self.max_entries})")
    
    def _get_memory_usage(self) -> int:
        """计算当前内存使用"""
        return sum(len(item["data"]) for item in self.cache.values())
    
    def _evict_if_needed(self, required_space: int = 0):
        """
        LRU淘汰 - 当内存不足时删除最旧的条目
        
        策略:
        1. 首先删除过期条目(TTL)
        2. 如果还不够，删除最少访问的条目(LRU)
        """
        current_size = self._get_memory_usage()
        target_size = self.max_size - required_space
        
        # 检查是否需要淘汰
        if current_size + required_space <= self.max_size and len(self.cache) < self.max_entries:
            return
        
        print(f"[L1] Memory limit reached ({current_size / 1024 / 1024:.1f}MB, {len(self.cache)} entries), starting eviction...")
        
        # 第一步: 删除过期条目
        now = time.time()
        expired_keys = [
            key for key, item in self.cache.items()
            if now - item.get("timestamp", 0) > self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            print(f"[L1] Evicted {len(expired_keys)} expired entries")
        
        # 检查是否还需要继续淘汰
        current_size = self._get_memory_usage()
        if current_size + required_space <= self.max_size and len(self.cache) < self.max_entries:
            return
        
        # 第二步: LRU淘汰 - 删除访问次数最少的20%条目
        entries_to_remove = max(
            int(len(self.cache) * 0.2),  # 20%
            len(self.cache) - self.max_entries + 1  # 或者超过数量限制的部分
        )
        
        # 按访问次数排序，删除最少的
        sorted_items = sorted(
            self.cache.items(),
            key=lambda x: (x[1].get("access_count", 0), x[1].get("timestamp", 0))
        )
        
        removed_count = 0
        for i in range(min(entries_to_remove, len(sorted_items))):
            del self.cache[sorted_items[i][0]]
            removed_count += 1
            
            # 检查是否足够
            current_size = self._get_memory_usage()
            if current_size + required_space <= self.max_size and len(self.cache) < self.max_entries:
                break
        
        print(f"[L1] LRU eviction: removed {removed_count} entries")
    
    async def get(self, key: str) -> Optional[MemoryItem]:
        """获取记忆"""
        cache_key = f"memory:{key}"
        item = self.cache.get(cache_key)
        if not item:
            return None
        
        # 检查TTL
        if time.time() - item.get("timestamp", 0) > self.ttl:
            del self.cache[cache_key]
            return None
        
        # 更新访问计数
        item["access_count"] = item.get("access_count", 0) + 1
        
        import pickle
        try:
            item_dict = pickle.loads(item["data"])
            return MemoryItem(**item_dict)
        except Exception:
            return None
    
    async def set(self, key: str, item: MemoryItem) -> bool:
        """存储记忆 (带LRU淘汰)"""
        import pickle
        try:
            data = pickle.dumps(item.model_dump())
            
            # 检查是否需要淘汰
            self._evict_if_needed(len(data))
            
            self.cache[f"memory:{key}"] = {
                "data": data,
                "timestamp": time.time(),
                "access_count": 0
            }
            return True
        except Exception as e:
            print(f"[L1] Set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """删除记忆"""
        cache_key = f"memory:{key}"
        if cache_key in self.cache:
            del self.cache[cache_key]
            return True
        return False
    
    async def exists(self, key: str) -> bool:
        """检查是否存在"""
        return f"memory:{key}" in self.cache
    
    async def keys(self, pattern: str = "*") -> list:
        """获取所有key"""
        return [k.replace("memory:", "") for k in self.cache.keys()]
    
    async def stats(self) -> dict:
        """获取统计信息"""
        size = self._get_memory_usage()
        return {
            "entries": len(self.cache),
            "size_bytes": size,
            "size_mb": round(size / 1024 / 1024, 2),
            "max_size_mb": self.max_size / 1024 / 1024,
            "usage_percent": round((size / self.max_size) * 100, 1),
            "max_entries": self.max_entries
        }
    
    async def close(self):
        """关闭 (无需操作)"""
        pass


# 单例实例
_l1_storage: Optional[L1HotStorage] = None


async def get_l1_storage() -> L1HotStorage:
    """获取L1存储实例 (单例)"""
    global _l1_storage
    if _l1_storage is None:
        _l1_storage = L1HotStorage()
        await _l1_storage.init()
    return _l1_storage
