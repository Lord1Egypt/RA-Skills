# -*- coding: utf-8 -*-
"""
简单内存缓存实现
"""
import time
from typing import Any, Optional
from collections import OrderedDict


class SimpleCache:
    """LRU 缓存实现"""
    
    def __init__(self, max_size: int = 100, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: OrderedDict = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if time.time() - entry["timestamp"] > self.ttl_seconds:
            # 缓存过期，删除
            del self._cache[key]
            return None
        
        # 移到最后（最近使用）
        self._cache.move_to_end(key)
        return entry["value"]
    
    def set(self, key: str, value: Any) -> None:
        """设置缓存值"""
        if key in self._cache:
            # 更新现有条目
            self._cache[key] = {
                "value": value,
                "timestamp": time.time(),
            }
            self._cache.move_to_end(key)
        else:
            # 添加新条目
            if len(self._cache) >= self.max_size:
                # 删除最旧的条目
                self._cache.popitem(last=False)
            self._cache[key] = {
                "value": value,
                "timestamp": time.time(),
            }
    
    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()
    
    def size(self) -> int:
        """获取缓存大小"""
        return len(self._cache)
