#!/usr/bin/env python3
"""
记忆去重工具 - 基于 SHA-256 内容哈希

功能：
1. 计算记忆内容的哈希值
2. 检查是否已索引（避免重复）
3. 只索引新增/修改的内容

使用：
python3 memory-dedup.py ./memory/
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from datetime import datetime

INDEX_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / ".index.json"

def compute_hash(content: str) -> str:
    """计算内容的 SHA-256 哈希"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def load_index() -> dict:
    """加载索引文件"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"chunks": {}, "files": {}, "last_updated": None}

def save_index(index: dict):
    """保存索引文件"""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

def chunk_memory(content: str, max_chunk_size: int = 500) -> list:
    """
    将记忆内容分块（按段落）
    
    规则：
    - 按空行分割段落
    - 每个 chunk 不超过 max_chunk_size 字符
    - 保留标题层级
    """
    chunks = []
    paragraphs = content.split('\n\n')
    
    current_chunk = []
    current_size = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        para_size = len(para)
        
        # 如果单个段落就超过限制，强制分割
        if para_size > max_chunk_size:
            # 先保存当前 chunk
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # 按行分割长段落
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
        
        # 如果加上这个段落会超限，先保存当前 chunk
        elif current_size + para_size > max_chunk_size:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_size = para_size
        else:
            current_chunk.append(para)
            current_size += para_size
    
    # 保存最后一个 chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def scan_memory_dir(memory_dir: Path) -> dict:
    """扫描记忆目录，返回文件列表和哈希"""
    files = {}
    
    for md_file in memory_dir.glob("*.md"):
        # 跳过索引文件
        if md_file.name.startswith('.'):
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        files[str(md_file)] = {
            "path": str(md_file),
            "hash": compute_hash(content),
            "size": len(content),
            "modified": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
        }
    
    return files

def find_new_or_changed(memory_dir: str) -> list:
    """
    找出新增或修改的文件
    
    返回：需要重新索引的文件列表
    """
    memory_path = Path(memory_dir)
    index = load_index()
    current_files = scan_memory_dir(memory_path)
    
    files_to_index = []
    
    for file_path, file_info in current_files.items():
        # 新文件
        if file_path not in index["files"]:
            files_to_index.append(file_path)
            print(f"🆕 新文件：{file_path}")
        # 文件有变化
        elif index["files"][file_path]["hash"] != file_info["hash"]:
            files_to_index.append(file_path)
            print(f"🔄 已修改：{file_path}")
        else:
            print(f"✅ 无变化：{file_path}")
    
    # 检查已删除的文件
    deleted_files = []
    for file_path in index["files"]:
        if file_path not in current_files:
            deleted_files.append(file_path)
            print(f"❌ 已删除：{file_path}")
    
    return files_to_index, deleted_files

def index_file(file_path: str, index: dict) -> dict:
    """索引单个文件，返回更新后的索引"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    file_hash = compute_hash(content)
    chunks = chunk_memory(content)
    
    new_chunks = 0
    for i, chunk in enumerate(chunks):
        chunk_hash = compute_hash(chunk)
        
        # 如果 chunk 已存在，跳过
        if chunk_hash in index["chunks"]:
            continue
        
        # 新增 chunk
        index["chunks"][chunk_hash] = {
            "content": chunk,
            "source": file_path,
            "chunk_index": i,
            "total_chunks": len(chunks),
            "indexed_at": datetime.now().isoformat()
        }
        new_chunks += 1
    
    # 更新文件记录
    index["files"][file_path] = {
        "hash": file_hash,
        "chunks": len(chunks),
        "indexed_at": datetime.now().isoformat()
    }
    
    index["last_updated"] = datetime.now().isoformat()
    
    return index, new_chunks

def remove_deleted_files(deleted_files: list, index: dict) -> dict:
    """从索引中移除已删除文件的 chunk"""
    removed_chunks = 0
    
    for file_path in deleted_files:
        # 找到这个文件的所有 chunk
        chunks_to_remove = []
        for chunk_hash, chunk_info in index["chunks"].items():
            if chunk_info["source"] == file_path:
                chunks_to_remove.append(chunk_hash)
        
        # 删除 chunk
        for chunk_hash in chunks_to_remove:
            del index["chunks"][chunk_hash]
            removed_chunks += 1
        
        # 删除文件记录
        if file_path in index["files"]:
            del index["files"][file_path]
    
    index["last_updated"] = datetime.now().isoformat()
    
    return index, removed_chunks

def show_stats(index: dict):
    """显示索引统计信息"""
    print("\n" + "=" * 50)
    print("📊 记忆索引统计")
    print("=" * 50)
    
    # 文件统计
    total_files = len(index["files"])
    total_chunks = len(index["chunks"])
    
    # 按文件统计 chunk 数
    chunks_per_file = {}
    for chunk_hash, chunk_info in index["chunks"].items():
        source = chunk_info["source"]
        chunks_per_file[source] = chunks_per_file.get(source, 0) + 1
    
    # 总内容大小
    total_size = sum(chunk_info.get("size", len(chunk_info["content"])) 
                     for chunk_info in index["chunks"].values())
    
    print(f"📁 文件数：{total_files}")
    print(f"📄 Chunk 总数：{total_chunks}")
    print(f"💾 估计总大小：{total_size / 1024:.2f} KB")
    
    if chunks_per_file:
        print(f"\n📋 文件详情（按 chunk 数排序）:")
        print("-" * 50)
        for file_path, count in sorted(chunks_per_file.items(), key=lambda x: -x[1])[:10]:
            filename = Path(file_path).name
            print(f"   {filename}: {count} chunks")
    
    if index.get("last_updated"):
        print(f"\n🕐 最后更新：{index['last_updated']}")
    
    print("=" * 50)

def search_chunks(query: str, index: dict, top_k: int = 10):
    """基于关键词搜索 chunk"""
    print(f"\n🔍 搜索：'{query}'")
    print("=" * 50)
    
    query_lower = query.lower()
    results = []
    
    for chunk_hash, chunk_info in index["chunks"].items():
        content = chunk_info["content"]
        if query_lower in content.lower():
            # 计算匹配度（简单关键词匹配）
            score = content.lower().count(query_lower)
            results.append({
                "content": content[:200] + "..." if len(content) > 200 else content,
                "source": chunk_info["source"],
                "score": score
            })
    
    if not results:
        print("❌ 未找到匹配结果")
        return
    
    # 按匹配度排序
    results.sort(key=lambda x: -x["score"])
    
    print(f"✅ 找到 {len(results)} 个匹配结果 (显示前 {top_k} 个)")
    print("-" * 50)
    
    for i, result in enumerate(results[:top_k], 1):
        filename = Path(result["source"]).name
        print(f"\n{i}. 📄 {filename} (匹配度：{result['score']})")
        print(f"   内容：{result['content']}")
    
    print("=" * 50)

def clean_index(index: dict, dry_run: bool = False):
    """清理过期 chunk（超过 30 天的已删除文件 chunk）"""
    print("\n🗑️  清理过期 chunk...")
    print("=" * 50)
    
    now = datetime.now()
    cleaned_chunks = 0
    orphan_chunks = []
    
    # 找出所有文件的来源
    all_sources = set(index["files"].keys())
    
    # 找出孤立 chunk（来源文件已不存在）
    for chunk_hash, chunk_info in list(index["chunks"].items()):
        source = chunk_info["source"]
        if source not in all_sources:
            orphan_chunks.append(chunk_hash)
    
    if not orphan_chunks:
        print("✅ 没有孤立 chunk，无需清理")
        return index, 0
    
    print(f"发现 {len(orphan_chunks)} 个孤立 chunk")
    
    if dry_run:
        print("🔍 干跑模式：不实际删除")
        for chunk_hash in orphan_chunks[:10]:
            chunk_info = index["chunks"][chunk_hash]
            print(f"   将删除：{Path(chunk_info['source']).name}")
    else:
        # 删除孤立 chunk
        for chunk_hash in orphan_chunks:
            del index["chunks"][chunk_hash]
            cleaned_chunks += 1
        
        index["last_updated"] = now.isoformat()
        print(f"✅ 已清理 {cleaned_chunks} 个孤立 chunk")
    
    print("=" * 50)
    return index, cleaned_chunks

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="记忆去重工具")
    parser.add_argument("memory_dir", nargs="?", default="./memory/",
                       help="记忆目录路径")
    parser.add_argument("--stats", action="store_true",
                       help="显示索引统计信息")
    parser.add_argument("--search", type=str, metavar="QUERY",
                       help="搜索记忆内容")
    parser.add_argument("--clean", action="store_true",
                       help="清理过期 chunk")
    parser.add_argument("--dry-run", action="store_true",
                       help="干跑模式（不实际修改）")
    
    args = parser.parse_args()
    
    # 单独的命令：stats
    if args.stats:
        index = load_index()
        show_stats(index)
        return
    
    # 单独的命令：search
    if args.search:
        index = load_index()
        search_chunks(args.search, index)
        return
    
    # 单独的命令：clean
    if args.clean:
        index = load_index()
        clean_index(index, dry_run=args.dry_run)
        if not args.dry_run:
            save_index(index)
        return
    
    # 默认：索引模式
    memory_dir = args.memory_dir
    
    if not Path(memory_dir).exists():
        print(f"错误：目录不存在 {memory_dir}")
        sys.exit(1)
    
    print(f"🔍 扫描记忆目录：{memory_dir}")
    print("-" * 50)
    
    # 找出新增或修改的文件
    files_to_index, deleted_files = find_new_or_changed(memory_dir)
    
    if not files_to_index and not deleted_files:
        print("\n✅ 所有文件都是最新的，无需索引")
        return
    
    print("\n" + "=" * 50)
    print(f"📊 统计：{len(files_to_index)} 个文件需要索引，{len(deleted_files)} 个文件已删除")
    print("=" * 50)
    
    # 加载索引
    index = load_index()
    
    # 索引新文件
    total_new_chunks = 0
    for file_path in files_to_index:
        print(f"\n📝 索引：{file_path}")
        index, new_chunks = index_file(file_path, index)
        total_new_chunks += new_chunks
        print(f"   + 新增 {new_chunks} 个 chunk")
    
    # 移除已删除文件的 chunk
    if deleted_files:
        print(f"\n🗑️  清理已删除文件...")
        index, removed_chunks = remove_deleted_files(deleted_files, index)
        print(f"   - 移除 {removed_chunks} 个 chunk")
    
    # 保存索引
    save_index(index)
    
    print("\n" + "=" * 50)
    print(f"✅ 索引完成！")
    print(f"   - 新增 chunk: {total_new_chunks}")
    print(f"   - 总 chunk 数：{len(index['chunks'])}")
    print(f"   - 索引文件：{INDEX_FILE}")
    print("=" * 50)

if __name__ == "__main__":
    main()
