from .db import MemoryDB
from .embedding import embedding_model
from datetime import datetime
import re

class MemoryManager:
    def __init__(self):
        self.db = MemoryDB()
        self.config = {
            "auto_extract": True,
            "auto_inject": True,
            "max_memory_results": 8,
            "expire_days": 90
        }
    
    def extract_memories_from_conversation(self, user_message, assistant_reply):
        """从对话中自动提取关键记忆点"""
        if not self.config['auto_extract']:
            return []
        
        memories = []
        
        # 提取事实类信息：用户提到的偏好、信息、项目等
        # 简单规则提取，后续可以用LLM优化
        patterns = [
            # 我喜欢/我偏好/我习惯
            r'我(?:喜欢|偏好|习惯|常用|一般用)(.*?)(?:[。，\n]|$)',
            # 我是/我叫/我在/我有
            r'我(?:是|叫|在|有|做)(.*?)(?:[。，\n]|$)',
            # 记住/记得/别忘了
            r'(?:记住|记得|别忘了)(.*?)(?:[。，\n]|$)',
            # 项目/任务/待办
            r'(?:项目|任务|待办|要做的事)(?:是|有|:|：)(.*?)(?:[。，\n]|$)'
        ]
        
        text = f"{user_message} {assistant_reply}"
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                match = match.strip()
                if len(match) > 5 and len(match) < 200:
                    memories.append({
                        "content": match,
                        "type": "preference" if "喜欢" in pattern or "偏好" in pattern else "fact"
                    })
        
        # 去重
        unique_memories = []
        seen = set()
        for mem in memories:
            if mem['content'] not in seen:
                seen.add(mem['content'])
                unique_memories.append(mem)
        
        # 保存到数据库
        saved_ids = []
        for mem in unique_memories:
            mem_id = self.add_memory(mem['content'], mem['type'], source='conversation')
            saved_ids.append(mem_id)
        
        return saved_ids
    
    def add_memory(self, content, memory_type='fact', source='manual'):
        """手动添加记忆"""
        # 先检查是否有相似记忆，存在则更新
        vector = embedding_model.encode(content)
        similar = self.search_memories(content, top_k=1)
        if similar and similar[0]['similarity'] > 0.9:
            # 更新现有记忆
            self.db.update_memory(similar[0]['id'], content)
            return similar[0]['id']
        
        # 添加新记忆
        mem_id = self.db.add_memory(content, memory_type, source, self.config['expire_days'])
        self.db.add_vector(mem_id, vector)
        return mem_id
    
    def search_memories(self, query, top_k=None):
        """搜索相关记忆"""
        if top_k is None:
            top_k = self.config['max_memory_results']
        
        query_vector = embedding_model.encode(query)
        return self.db.search_similar(query_vector, top_k)
    
    def get_relevant_context(self, query):
        """获取相关上下文，用于注入对话"""
        if not self.config['auto_inject']:
            return ""
        
        memories = self.search_memories(query)
        if not memories:
            return ""
        
        context = "### 相关记忆:\n"
        for i, mem in enumerate(memories, 1):
            context += f"{i}. {mem['content']} (创建时间: {mem['created_at'][:10]})\n"
        
        return context
    
    def list_all_memories(self, limit=100):
        """列出所有记忆"""
        return self.db.list_memories(limit)
    
    def delete_memory(self, memory_id):
        """删除记忆"""
        return self.db.delete_memory(memory_id)
    
    def delete_by_query(self, query):
        """根据关键词删除相关记忆"""
        memories = self.search_memories(query, top_k=10)
        deleted = []
        for mem in memories:
            if mem['similarity'] > 0.8:
                self.db.delete_memory(mem['id'])
                deleted.append(mem)
        return deleted
    
    def close(self):
        self.db.close()

# 全局单例
memory_manager = MemoryManager()
