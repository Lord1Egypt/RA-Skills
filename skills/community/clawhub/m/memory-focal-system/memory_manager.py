#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Manager - 焦距记忆系统核心模块

功能：
1. 消息自动分类（4 种焦距模式）
2. 按需加载记忆
3. 自动记忆写入
4. Token 优化

Usage:
    from memory_manager import MemoryManager
    
    manager = MemoryManager()
    context = manager.process_message(user_message)
    
    if manager.should_write_memory(user_message):
        manager.write_memory(user_message, response)
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 添加 memory-focal 到路径
memory_focal_scripts = Path(os.path.expanduser("~/.openclaw/workspace/memory-focal/scripts"))
sys.path.insert(0, str(memory_focal_scripts))

# 导入分类器
from classifier import MessageClassifier


class MemoryManager:
    """焦距记忆管理器"""
    
    def __init__(self, config_path: str = None):
        """初始化"""
        self.workspace_base = Path(os.path.expanduser("~/.openclaw/workspace"))
        self.memory_focal_base = self.workspace_base / "memory-focal"
        
        # 默认配置
        self.config = {
            "enabled": True,
            "auto_classify": True,
            "auto_write": True,
            "load_focal_active": True,
            "token_limit": 8000,
        }
        
        # 加载配置
        if config_path:
            self.load_config(config_path)
        else:
            config_file = self.workspace_base / "skills" / "memory-focal-system" / "config.json"
            if config_file.exists():
                self.load_config(str(config_file))
        
        # 初始化分类器
        self.classifier = MessageClassifier()
        
        # 当前状态
        self.current_category = None
        self.current_config = None
    
    def load_config(self, config_path: str):
        """加载配置"""
        with open(config_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            self.config.update(loaded)
    
    def _count_tokens(self, text: str) -> int:
        """计算 Token 数（中英文友好）"""
        if not text:
            return 0
        
        # 中文字符
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        
        # 英文单词
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        
        # 其他字符
        other_chars = len(text) - chinese_chars - sum(len(w) for w in re.findall(r'\b[a-zA-Z]+\b', text))
        
        # 计算
        tokens = (chinese_chars / 1.5) + (english_words * 1.3) + (other_chars / 2)
        return int(tokens)
    
    def process_message(self, message: str) -> Dict:
        """
        处理用户消息（核心入口）
        
        Returns:
            {
                "category": str,
                "load_focal": list,
                "should_write": bool,
                "token_count": int,
            }
        """
        result = {
            "category": None,
            "load_focal": [],
            "should_write": False,
            "token_count": 0,
        }
        
        if not self.config.get("enabled", True):
            return result
        
        # 1. 分类消息
        if self.config.get("auto_classify", True):
            self.current_category, self.current_config = self.classifier.classify(message)
            result["category"] = self.current_category
            result["should_write"] = self.classifier.should_write_memory(message)
        
        # 2. 加载记忆（仅 memory-focal 系统）
        token_count = 0
        
        if self.current_config.get("load_focal") and self.config.get("load_focal_active", True):
            memories = self._load_focal_active()
            result["load_focal"] = memories
            for mem in memories:
                token_count += self._count_tokens(mem.get("text", ""))
        
        result["token_count"] = int(token_count)
        return result
    
    def _load_focal_active(self) -> List[Dict]:
        """加载 memory-focal 热存储记忆"""
        buffer_path = self.memory_focal_base / "data" / "raw" / "buffer.jsonl"
        
        if not buffer_path.exists():
            return []
        
        memories = []
        try:
            with open(buffer_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        mem = json.loads(line.strip())
                        memories.append(mem)
                    except:
                        continue
        except:
            return []
        
        # 按访问次数排序，取前 20 条
        memories.sort(key=lambda x: x.get("access_count", 0), reverse=True)
        return memories[:20]
    
    def should_write_memory(self, message: str, response: str = None) -> bool:
        """判断是否需要写入"""
        return self.classifier.should_write_memory(message)
    
    def write_memory(self, message: str, response: str = None,
                     mem_type: str = None, tags: List[str] = None) -> Optional[str]:
        """写入新记忆"""
        if not self.config.get("auto_write", True):
            return None
        
        if not self.should_write_memory(message, response):
            return None
        
        # 自动推断类型
        if mem_type is None:
            message_lower = message.lower()
            if any(x in message_lower for x in ["偏好", "喜欢", "讨厌"]):
                mem_type = "preference"
            elif any(x in message_lower for x in ["规则", "禁止", "必须"]):
                mem_type = "rule"
            elif any(x in message_lower for x in ["决定", "决策"]):
                mem_type = "decision"
            else:
                mem_type = "default"
        
        # 自动生成标签
        if tags is None:
            tags = self._auto_generate_tags(message)
        
        # 生成记忆 ID
        index_path = self.memory_focal_base / "data" / "index" / "memory_index.json"
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
            mem_id = f"mem_{index.get('total_memories', 0) + 1:04d}"
        else:
            mem_id = "mem_0001"
        
        # 创建记忆对象
        memory = {
            "id": mem_id,
            "text": message,
            "type": mem_type,
            "tags": tags,
            "timestamp": datetime.now().astimezone().isoformat(),
            "created_at": datetime.now().astimezone().isoformat(),
            "access_count": 0,
            "last_accessed": None,
            "importance": 1.0,
            "layer": "active",
            "priority": 0.0,
        }
        
        # 写入 buffer
        buffer_path = self.memory_focal_base / "data" / "raw" / "buffer.jsonl"
        buffer_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(buffer_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(memory, ensure_ascii=False) + '\n')
        
        # 更新索引
        self._update_index(mem_id, memory)
        
        return mem_id
    
    def _update_index(self, mem_id: str, memory: Dict):
        """更新记忆索引"""
        index_path = self.memory_focal_base / "data" / "index" / "memory_index.json"
        
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {"version": "1.0.0", "total_memories": 0, "memories": []}
        
        index["total_memories"] += 1
        index["memories"].append({
            "id": mem_id,
            "type": memory["type"],
            "tags": memory["tags"],
            "created_at": memory["timestamp"],
            "layer": "active"
        })
        
        index["updated_at"] = datetime.now().astimezone().isoformat()
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        
        # 更新标签索引
        self._update_tag_index(mem_id, memory["tags"])
    
    def _update_tag_index(self, mem_id: str, tags: List[str]):
        """更新标签索引"""
        tag_index_path = self.memory_focal_base / "data" / "index" / "tag_index.json"
        
        if tag_index_path.exists():
            with open(tag_index_path, 'r', encoding='utf-8') as f:
                tag_index = json.load(f)
        else:
            tag_index = {"version": "1.0.0", "tags": {}}
        
        for tag in tags:
            if tag not in tag_index["tags"]:
                tag_index["tags"][tag] = []
            if mem_id not in tag_index["tags"][tag]:
                tag_index["tags"][tag].append(mem_id)
        
        tag_index["updated_at"] = datetime.now().astimezone().isoformat()
        
        with open(tag_index_path, 'w', encoding='utf-8') as f:
            json.dump(tag_index, f, ensure_ascii=False, indent=2)
    
    def _auto_generate_tags(self, message: str) -> List[str]:
        """自动生成标签"""
        tags = []
        message_lower = message.lower()
        
        if any(x in message_lower for x in ["偏好", "喜欢", "讨厌"]):
            tags.append("偏好")
        
        if any(x in message_lower for x in ["规则", "禁止", "必须"]):
            tags.append("规则")
        
        if any(x in message_lower for x in ["作息", "起床", "睡觉"]):
            tags.append("作息")
        
        if any(x in message_lower for x in ["工作", "任务"]):
            tags.append("工作")
        
        if any(x in message_lower for x in ["邮件", "邮箱"]):
            tags.append("工具")
        
        if any(x in message_lower for x in ["记忆", "记住"]):
            tags.append("记忆")
        
        if not tags:
            tags.append("对话")
        
        return tags
    
    def get_stats(self) -> Dict:
        """获取统计"""
        buffer_path = self.memory_focal_base / "data" / "raw" / "buffer.jsonl"
        
        if not buffer_path.exists():
            return {"total": 0}
        
        total = 0
        with open(buffer_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    json.loads(line.strip())
                    total += 1
                except:
                    continue
        
        return {"total": total}


# 测试
if __name__ == "__main__":
    manager = MemoryManager()
    
    test_cases = [
        ("在吗", "简单对话"),
        ("用户偏好早上 8 点起床", "偏好记忆"),
        ("查一下配置", "任务执行"),
        ("记住，以后别用这功能", "否定词"),
        ("新增一条规则", "新信息"),
    ]
    
    print("🧪 Memory Focal System 测试\n")
    for msg, note in test_cases:
        result = manager.process_message(msg)
        should_write = manager.should_write_memory(msg)
        print(f'{note}: {msg}')
        print(f'  分类：{result["category"]}')
        print(f'  Token: {result["token_count"]}')
        print(f'  写入：{should_write}')
        print()
