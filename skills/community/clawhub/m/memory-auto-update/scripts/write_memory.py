#!/usr/bin/env python3
"""
写入记忆文件 - 将生成的摘要写入记忆文件
"""

import os
from datetime import datetime
from typing import Optional

class MemoryWriter:
    """记忆写入器"""
    
    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = '/root/.openclaw/workspace'
        self.workspace_path = workspace_path
        self.memory_dir = os.path.join(workspace_path, 'memory')
        
        # 确保目录存在
        os.makedirs(self.memory_dir, exist_ok=True)
    
    def get_memory_file_path(self, date: str = None) -> str:
        """
        获取记忆文件路径
        
        Args:
            date: 日期字符串，默认为今天
            
        Returns:
            记忆文件路径
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        return os.path.join(self.memory_dir, f'{date}.md')
    
    def write(self, content: str, date: str = None, append: bool = True) -> bool:
        """
        写入记忆文件
        
        Args:
            content: 要写入的内容
            date: 日期，默认为今天
            append: 是否追加，True=追加，False=覆盖
            
        Returns:
            是否成功
        """
        file_path = self.get_memory_file_path(date)
        
        try:
            mode = 'a' if append else 'w'
            
            # 如果是追加且文件已存在，先加个分隔符
            if append and os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing = f.read()
                if existing and not existing.endswith('\n---\n'):
                    content = '\n---\n' + content
            
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
                if not content.endswith('\n'):
                    f.write('\n')
            
            return True
        except Exception as e:
            print(f"写入记忆文件失败: {e}")
            return False
    
    def exists(self, date: str = None) -> bool:
        """
        检查记忆文件是否存在
        
        Args:
            date: 日期，默认为今天
            
        Returns:
            是否存在
        """
        return os.path.exists(self.get_memory_file_path(date))
    
    def read(self, date: str = None) -> Optional[str]:
        """
        读取记忆文件
        
        Args:
            date: 日期，默认为今天
            
        Returns:
            文件内容，不存在返回 None
        """
        file_path = self.get_memory_file_path(date)
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None

if __name__ == "__main__":
    writer = MemoryWriter()
    
    test_content = """
# 测试记忆

## 今日事项

### 测试事项
- **事件：** 测试写入功能
- **决策：** 使用这个技能
- **待办：** [ ] 测试完成

---

记录时间：测试
"""
    
    print("测试写入记忆文件...")
    success = writer.write(test_content, append=False)
    
    if success:
        print("✅ 写入成功！")
        print(f"文件路径: {writer.get_memory_file_path()}")
        print("\n文件内容:")
        print(writer.read())
    else:
        print("❌ 写入失败")
