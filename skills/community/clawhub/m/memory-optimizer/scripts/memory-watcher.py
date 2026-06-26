#!/usr/bin/env python3
"""
记忆文件监听器 - 自动索引变化的文件

功能：
1. 监听记忆目录的文件变化
2. 文件修改后自动索引（防抖 1500ms）
3. 文件删除后自动清理对应 chunk

使用：
python3 memory-watcher.py ./memory/
"""

import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from threading import Timer

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("❌ 缺少依赖：watchdog")
    print("安装：pip3 install watchdog")
    sys.exit(1)

INDEX_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / ".index.json"

class MemoryIndexer:
    """记忆索引管理器"""
    
    def __init__(self, index_file: Path):
        self.index_file = index_file
        self.index = self.load_index()
    
    def load_index(self) -> dict:
        """加载索引文件"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"chunks": {}, "files": {}, "last_updated": None}
    
    def save_index(self):
        """保存索引文件"""
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)
    
    def compute_hash(self, content: str) -> str:
        """计算内容的 SHA-256 哈希"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def chunk_memory(self, content: str, max_chunk_size: int = 500) -> list:
        """将记忆内容分块（按段落）"""
        chunks = []
        paragraphs = content.split('\n\n')
        
        current_chunk = []
        current_size = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_size = len(para)
            
            if para_size > max_chunk_size:
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = []
                    current_size = 0
                
                lines = para.split('\n')
                temp_chunk = []
                temp_size = 0
                
                for line in lines:
                    line_size = len(line)
                    if temp_size + line_size > max_chunk_size:
                        if temp_chunk:
                            chunks.append('\n'.join(temp_chunk))
                            temp_chunk = []
                            temp_size = 0
                        temp_chunk.append(line)
                        temp_size = line_size
                    else:
                        temp_chunk.append(line)
                        temp_size += line_size
                
                if temp_chunk:
                    chunks.append('\n'.join(temp_chunk))
            
            elif current_size + para_size > max_chunk_size:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_size = para_size
            else:
                current_chunk.append(para)
                current_size += para_size
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
    
    def index_file(self, file_path: str) -> int:
        """索引单个文件，返回新增 chunk 数"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"   ⚠️  读取失败：{e}")
            return 0
        
        file_hash = self.compute_hash(content)
        chunks = self.chunk_memory(content)
        
        new_chunks = 0
        for i, chunk in enumerate(chunks):
            chunk_hash = self.compute_hash(chunk)
            
            if chunk_hash in self.index["chunks"]:
                continue
            
            self.index["chunks"][chunk_hash] = {
                "content": chunk,
                "source": file_path,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "indexed_at": datetime.now().isoformat()
            }
            new_chunks += 1
        
        self.index["files"][file_path] = {
            "hash": file_hash,
            "chunks": len(chunks),
            "indexed_at": datetime.now().isoformat()
        }
        
        self.index["last_updated"] = datetime.now().isoformat()
        self.save_index()
        
        return new_chunks
    
    def remove_file(self, file_path: str) -> int:
        """移除文件的索引，返回删除的 chunk 数"""
        chunks_to_remove = []
        for chunk_hash, chunk_info in self.index["chunks"].items():
            if chunk_info["source"] == file_path:
                chunks_to_remove.append(chunk_hash)
        
        for chunk_hash in chunks_to_remove:
            del self.index["chunks"][chunk_hash]
        
        if file_path in self.index["files"]:
            del self.index["files"][file_path]
        
        self.index["last_updated"] = datetime.now().isoformat()
        self.save_index()
        
        return len(chunks_to_remove)


class MemoryFileHandler(FileSystemEventHandler):
    """记忆文件变化处理器"""
    
    def __init__(self, indexer: MemoryIndexer, debounce_ms: int = 1500):
        self.indexer = indexer
        self.debounce_ms = debounce_ms / 1000.0
        self.timers = {}
    
    def _debounce(self, file_path: str, callback):
        """防抖处理"""
        if file_path in self.timers:
            self.timers[file_path].cancel()
        
        timer = Timer(self.debounce_ms, callback, args=[file_path])
        timer.daemon = True
        timer.start()
        self.timers[file_path] = timer
    
    def on_modified(self, event):
        """文件修改事件"""
        if event.is_directory:
            return
        
        if not event.src_path.endswith('.md'):
            return
        
        if event.src_path.endswith('.index.json'):
            return
        
        def process(file_path):
            print(f"\n📝 检测到修改：{file_path}")
            new_chunks = self.indexer.index_file(file_path)
            print(f"   + 新增 {new_chunks} 个 chunk")
            print(f"   💾 索引已保存")
        
        self._debounce(event.src_path, process)
    
    def on_created(self, event):
        """文件创建事件"""
        if event.is_directory:
            return
        
        if not event.src_path.endswith('.md'):
            return
        
        def process(file_path):
            print(f"\n🆕 检测到新文件：{file_path}")
            new_chunks = self.indexer.index_file(file_path)
            print(f"   + 新增 {new_chunks} 个 chunk")
            print(f"   💾 索引已保存")
        
        self._debounce(event.src_path, process)
    
    def on_deleted(self, event):
        """文件删除事件"""
        if event.is_directory:
            return
        
        if not event.src_path.endswith('.md'):
            return
        
        def process(file_path):
            print(f"\n🗑️  检测到删除：{file_path}")
            removed = self.indexer.remove_file(file_path)
            print(f"   - 移除 {removed} 个 chunk")
            print(f"   💾 索引已保存")
        
        self._debounce(event.src_path, process)


def main():
    if len(sys.argv) < 2:
        print("用法：python3 memory-watcher.py <memory_dir> [debounce_ms]")
        print("示例：python3 memory-watcher.py ./memory/ 1500")
        sys.exit(1)
    
    memory_dir = sys.argv[1]
    debounce_ms = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    
    memory_path = Path(memory_dir)
    
    if not memory_path.exists():
        print(f"❌ 错误：目录不存在 {memory_dir}")
        sys.exit(1)
    
    print(f"👁️  开始监听：{memory_dir}")
    print(f"⏱️  防抖时间：{debounce_ms}ms")
    print(f"📁 监听目录：{memory_path.absolute()}")
    print("-" * 50)
    print(f"💡 按 Ctrl+C 停止监听")
    print("=" * 50)
    
    # 初始化索引器
    indexer = MemoryIndexer(INDEX_FILE)
    
    # 先索引现有文件
    print("\n📋 初始化索引现有文件...")
    for md_file in memory_path.glob("*.md"):
        if md_file.name.startswith('.'):
            continue
        chunks = indexer.index_file(str(md_file))
        print(f"   ✓ {md_file.name} ({chunks} chunks)")
    
    print(f"\n✅ 初始索引完成，共 {len(indexer.index['chunks'])} 个 chunk")
    print("=" * 50)
    
    # 设置监听器
    event_handler = MemoryFileHandler(indexer, debounce_ms)
    observer = Observer()
    observer.schedule(event_handler, str(memory_path), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 停止监听...")
        observer.stop()
        observer.join()
        print("✅ 已退出")


if __name__ == "__main__":
    main()
