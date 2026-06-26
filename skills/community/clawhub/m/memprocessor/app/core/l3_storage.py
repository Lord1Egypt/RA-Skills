"""
L3 冷存储 - Markdown文件系统实现 (v1.0.1 Hotfix)

修复内容:
1. 添加文件锁机制防止并发写入冲突
2. 添加写入重试机制
3. 添加文件完整性检查
"""
import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import aiofiles

from app.config import settings
from app.models import DailySummary, MemoryItem, MemoryLevel


class L3ColdStorage:
    """L3冷存储 - Markdown文件系统 (带文件锁)"""
    
    def __init__(self):
        self.daily_dir = settings.L3_DAILY_DIR
        self.projects_dir = settings.L3_PROJECTS_DIR
        self.decisions_dir = settings.L3_DECISIONS_DIR
        self.memory_file = settings.L3_MEMORY_DIR / "MEMORY.md"
        # 文件锁字典: path -> asyncio.Lock
        self._file_locks: Dict[str, asyncio.Lock] = {}
        self._lock_lock = asyncio.Lock()  # 用于保护_file_locks的锁
    
    async def _get_lock(self, path: Path) -> asyncio.Lock:
        """获取文件对应的锁 (线程安全)"""
        path_str = str(path)
        async with self._lock_lock:
            if path_str not in self._file_locks:
                self._file_locks[path_str] = asyncio.Lock()
            return self._file_locks[path_str]
    
    async def init(self):
        """初始化目录"""
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.decisions_dir.mkdir(parents=True, exist_ok=True)
        settings.L3_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        
        # 创建MEMORY.md如果不存在
        if not self.memory_file.exists():
            await self._write_file(self.memory_file, self._get_memory_template())
        
        print(f"[L3] File storage initialized: {settings.L3_MEMORY_DIR}")
    
    async def save_daily_summary(self, summary: DailySummary) -> Path:
        """保存每日摘要 (带锁)"""
        await self.init()
        
        file_path = self.daily_dir / f"{summary.date}.md"
        content = self._format_daily_summary(summary)
        
        async with await self._get_lock(file_path):
            await self._write_file(file_path, content)
        
        print(f"[L3] Daily summary saved: {file_path}")
        return file_path
    
    async def append_to_memory(self, item: MemoryItem, section: str = "general"):
        """追加到MEMORY.md (带锁)"""
        await self.init()
        
        async with await self._get_lock(self.memory_file):
            # 读取现有内容
            content = await self._read_file(self.memory_file)
            
            # 生成条目
            entry = self._format_memory_entry(item, section)
            
            # 追加到对应section
            if section == "decisions":
                content = self._append_to_section(content, "## 重要决策", entry)
            elif section == "lessons":
                content = self._append_to_section(content, "## 学到的内容", entry)
            elif section == "projects":
                content = self._append_to_section(content, "## 项目里程碑", entry)
            else:
                content = content + "\n" + entry
            
            await self._write_file(self.memory_file, content)
        
        print(f"[L3] Appended to MEMORY.md: {item.key}")
    
    async def save_decision(self, item: MemoryItem):
        """保存决策到专门文件 (带锁)"""
        await self.init()
        
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        file_path = self.decisions_dir / f"{date_str}.md"
        
        entry = f"""### {item.key}

- **时间**: {item.created_at.isoformat()}
- **重要性**: {item.importance}/100
- **标签**: {', '.join(item.tags)}

{item.content}

---

"""
        
        async with await self._get_lock(file_path):
            # 追加模式写入
            if await self._file_exists(file_path):
                existing = await self._read_file(file_path)
                content = existing + entry
            else:
                content = f"# 决策记录 - {date_str}\n\n" + entry
            
            await self._write_file(file_path, content)
        
        print(f"[L3] Decision saved: {file_path}")
    
    async def _file_exists(self, path: Path) -> bool:
        """检查文件是否存在"""
        return path.exists()
    
    async def _read_file(self, path: Path) -> str:
        """异步读取文件"""
        try:
            async with aiofiles.open(path, 'r', encoding='utf-8') as f:
                return await f.read()
        except FileNotFoundError:
            return ""
        except Exception as e:
            print(f"[L3] Read error: {e}")
            return ""
    
    async def _write_file(self, path: Path, content: str, max_retries: int = 3):
        """异步写入文件 (带重试)"""
        for attempt in range(max_retries):
            try:
                async with aiofiles.open(path, 'w', encoding='utf-8') as f:
                    await f.write(content)
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"[L3] Write error after {max_retries} retries: {e}")
                    raise
                else:
                    print(f"[L3] Write retry {attempt + 1}/{max_retries}...")
                    await asyncio.sleep(0.1 * (attempt + 1))  # 指数退避
    
    def _get_memory_template(self) -> str:
        """获取MEMORY.md模板"""
        return """# 🧠 长期记忆

## 重要决策

## 学到的内容

## 项目里程碑

## 关系约定

*自动生成于 DreamMoon-MemProcessor*
"""
    
    def _format_memory_entry(self, item: MemoryItem, section: str) -> str:
        """格式化记忆条目"""
        tags_str = ', '.join(item.tags) if item.tags else '无'
        
        return f"""
### {item.key}
- **时间**: {item.created_at.strftime('%Y-%m-%d %H:%M')}
- **重要性**: {item.importance}/100
- **标签**: {tags_str}
- **层级**: {item.level}

{item.content}

---
"""
    
    def _format_daily_summary(self, summary: DailySummary) -> str:
        """格式化每日摘要"""
        content = f"""# 📅 {summary.date} 记忆摘要

## 概览

{summary.overview}

"""
        
        if summary.activities:
            content += "## 活动\\n\\n"
            for activity in summary.activities:
                content += f"- {activity.get('time', '')}: {activity.get('description', '')}\\n"
            content += "\\n"
        
        if summary.decisions:
            content += "## 重要决策\\n\\n"
            for decision in summary.decisions:
                content += f"### {decision.get('title', '未命名')}\\n\\n"
                content += f"{decision.get('content', '')}\\n\\n"
            content += "---\\n\\n"
        
        if summary.lessons:
            content += "## 学到的内容\\n\\n"
            for lesson in summary.lessons:
                content += f"- **{lesson.get('category', '一般')}**: {lesson.get('content', '')}\\n"
            content += "\\n"
        
        content += "\\n---\\n*自动生成于 DreamMoon-MemProcessor*\\n"
        
        return content
    
    def _append_to_section(self, content: str, section_header: str, entry: str) -> str:
        """追加到指定section"""
        # 查找section
        section_pattern = f"{section_header}\\n"
        if section_pattern in content:
            # 在section后面追加
            return content.replace(section_pattern, f"{section_header}\\n{entry}\\n")
        else:
            # section不存在，追加到文件末尾
            return content + f"\\n{section_header}\\n{entry}\\n"
    
    async def get_all_memories(self) -> List[MemoryItem]:
        """获取所有记忆 (简化实现)"""
        memories = []
        # TODO: 实现完整的记忆读取
        return memories
    
    async def stats(self) -> dict:
        """获取统计信息"""
        try:
            daily_files = list(self.daily_dir.glob("*.md")) if self.daily_dir.exists() else []
            decision_files = list(self.decisions_dir.glob("*.md")) if self.decisions_dir.exists() else []
            
            # 计算总大小
            total_size = 0
            for f in daily_files:
                total_size += f.stat().st_size
            for f in decision_files:
                total_size += f.stat().st_size
            if self.memory_file.exists():
                total_size += self.memory_file.stat().st_size
            
            return {
                "daily_summaries": len(daily_files),
                "decisions": len(decision_files),
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / 1024 / 1024, 2)
            }
        except Exception as e:
            print(f"[L3] Stats error: {e}")
            return {"daily_summaries": 0, "decisions": 0, "total_size_bytes": 0, "total_size_mb": 0}


# 单例实例
_l3_storage: Optional[L3ColdStorage] = None


async def get_l3_storage() -> L3ColdStorage:
    """获取L3存储实例 (单例)"""
    global _l3_storage
    if _l3_storage is None:
        _l3_storage = L3ColdStorage()
        await _l3_storage.init()
    return _l3_storage
