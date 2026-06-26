#!/usr/bin/env python3
"""
Memory Sync Enhanced 与 OpenClaw 原生记忆系统集成脚本

功能：
1. 同步记忆文件到共现图
2. 增强记忆搜索（语义 + 共现）
3. 记录记忆访问共现
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path

# 添加技能脚本路径
sys.path.append('/root/.openclaw/workspace/skills/memory-sync-enhanced/scripts')

try:
    from integration.adapter.co_occurrence_adapter import CoOccurrenceAdapter
except ImportError:
    print("警告：无法导入 co_occurrence_adapter.py")
    print("请确保适配器文件存在：/root/.openclaw/workspace/integration/adapter/co_occurrence_adapter.py")
    sys.exit(1)

# 语义向量适配器（可选）
try:
    from integration.adapter.semantic_vector_adapter import SemanticVectorAdapter
    SEMANTIC_VECTOR_AVAILABLE = True
except ImportError:
    print("警告：无法导入 semantic_vector_adapter.py，语义向量功能将不可用")
    SEMANTIC_VECTOR_AVAILABLE = False
    SemanticVectorAdapter = None

class MemoryIntegration:
    def __init__(self):
        self.workspace = Path(os.environ.get('OPENCLAW_WORKSPACE', '/root/.openclaw/workspace'))
        self.memory_dir = self.workspace / 'memory'
        self.tracker = CoOccurrenceAdapter()

        # 语义向量适配器（可选）
        if SEMANTIC_VECTOR_AVAILABLE and SemanticVectorAdapter is not None:
            try:
                self.vector_store = SemanticVectorAdapter()
                print("语义向量适配器初始化成功")
            except Exception as e:
                print(f"语义向量适配器初始化失败: {e}")
                self.vector_store = None
        else:
            self.vector_store = None

        # 增量同步配置
        self.config_file = self.workspace / 'integration' / 'memory_sync_config.json'
        self.sync_state = self._load_sync_state()

    def _load_sync_state(self):
        """加载同步状态"""
        if not self.config_file.exists():
            return {
                'last_sync': None,
                'file_hashes': {}
            }
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {
                'last_sync': None,
                'file_hashes': {}
            }

    def _save_sync_state(self):
        """保存同步状态"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.sync_state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存同步状态失败: {e}")

    def generate_memory_id(self, file_path, content, line_start=0):
        """生成记忆的唯一ID"""
        # 使用文件路径和内容哈希生成ID
        hash_input = f"{file_path}:{line_start}:{content[:100]}"
        return f"mem_{hashlib.md5(hash_input.encode()).hexdigest()[:10]}"

    def get_all_memory_files(self):
        """获取所有记忆文件路径"""
        files = []
        memory_file = self.workspace / 'MEMORY.md'
        if memory_file.exists():
            files.append(memory_file)
        if self.memory_dir.exists():
            files.extend(sorted(self.memory_dir.glob('*.md')))
        return files

    def parse_single_file(self, file_path):
        """解析单个记忆文件"""
        memories = []
        print(f"解析 {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#') and len(line.strip()) > 10:
                    mem_id = self.generate_memory_id(str(file_path), line, i)
                    memory = {
                        'id': mem_id,
                        'content': line.strip(),
                        'file': str(file_path),
                        'line': i,
                        'type': 'ltm' if file_path.name == 'MEMORY.md' else 'stm'
                    }
                    if file_path.name != 'MEMORY.md':
                        memory['date'] = file_path.stem
                    memories.append(memory)
        return memories

    def parse_memory_files(self):
        """解析所有记忆文件，提取记忆片段"""
        memories = []
        for file_path in self.get_all_memory_files():
            memories.extend(self.parse_single_file(file_path))
        return memories

    def _update_co_occurrence(self, memories):
        """更新共现图（内部方法）"""
        # 按文件分组，记录同一文件内记忆的共现
        file_groups = {}
        for mem in memories:
            file = mem['file']
            if file not in file_groups:
                file_groups[file] = []
            file_groups[file].append(mem['id'])

        # 记录同一文件内记忆的共现（它们具有上下文关联）
        for file, mem_ids in file_groups.items():
            if len(mem_ids) > 1:
                print(f"记录文件 {file} 内 {len(mem_ids)} 个记忆的共现")
                self.tracker.record_co_occurrence(mem_ids, f"file_context:{file}")

        # 还可以按日期分组记录共现
        date_groups = {}
        for mem in memories:
            if 'date' in mem:
                date = mem['date']
                if date not in date_groups:
                    date_groups[date] = []
                date_groups[date].append(mem['id'])

        for date, mem_ids in date_groups.items():
            if len(mem_ids) > 1:
                print(f"记录日期 {date} 内 {len(mem_ids)} 个记忆的共现")
                self.tracker.record_co_occurrence(mem_ids, f"date_context:{date}")

        return len(memories)

    def sync_to_cooccurrence(self, incremental=True):
        """同步记忆到共现图（支持增量同步）"""
        if not incremental or self.sync_state['last_sync'] is None:
            # 全量同步
            memories = self.parse_memory_files()
            print(f"全量同步: 找到 {len(memories)} 个记忆片段")
            count = self._update_co_occurrence(memories)
            # 更新同步状态（记录所有文件的哈希）
            self._update_sync_state_full()
            return count
        else:
            # 增量同步：检测文件变更
            changed_files = []
            current_hashes = {}
            for file_path in self.get_all_memory_files():
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                except Exception:
                    continue
                current_hashes[str(file_path)] = file_hash
                old_hash = self.sync_state['file_hashes'].get(str(file_path))
                if old_hash != file_hash:
                    changed_files.append(file_path)

            if not changed_files:
                print("增量同步: 没有检测到文件变更")
                # 仍然更新哈希，以防文件被删除
                self.sync_state['file_hashes'] = current_hashes
                self.sync_state['last_sync'] = datetime.now().astimezone().isoformat()
                self._save_sync_state()
                return 0

            print(f"增量同步: 检测到 {len(changed_files)} 个文件变更")
            memories = []
            for file_path in changed_files:
                memories.extend(self.parse_single_file(file_path))

            if memories:
                count = self._update_co_occurrence(memories)
                # 更新同步状态
                self.sync_state['file_hashes'] = current_hashes
                self.sync_state['last_sync'] = datetime.now().astimezone().isoformat()
                self._save_sync_state()
                print(f"增量同步: 处理了 {count} 个新记忆片段")
                return count
            else:
                print("增量同步: 没有提取到新记忆片段")
                self.sync_state['file_hashes'] = current_hashes
                self.sync_state['last_sync'] = datetime.now().astimezone().isoformat()
                self._save_sync_state()
                return 0

    def _update_sync_state_full(self):
        """全量同步后更新状态"""
        current_hashes = {}
        for file_path in self.get_all_memory_files():
            try:
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
            except Exception:
                continue
            current_hashes[str(file_path)] = file_hash

        self.sync_state['file_hashes'] = current_hashes
        self.sync_state['last_sync'] = datetime.now().astimezone().isoformat()
        self._save_sync_state()
        print(f"已更新同步状态: {len(current_hashes)} 个文件")

    def enhance_search(self, query, search_results):
        """
        增强搜索结果

        Args:
            query: 搜索查询
            search_results: 原生记忆搜索结果列表，每个元素包含 'content', 'path', 'lines' 等

        Returns:
            增强后的结果列表
        """
        if not search_results:
            return []

        # 提取记忆ID
        mem_ids = []
        for result in search_results:
            # 从结果生成ID
            content = result.get('content', '') or result.get('text', '')
            path = result.get('path', '')
            lines = result.get('lines', (0, 0))

            if content and path:
                mem_id = self.generate_memory_id(path, content, lines[0])
                mem_ids.append(mem_id)
                result['memory_id'] = mem_id

        # 记录这次搜索中所有结果的共现
        if len(mem_ids) > 1:
            self.tracker.record_co_occurrence(mem_ids, f"search:{query[:50]}")

        # 为每个结果计算共现增强分数
        for result in search_results:
            if 'memory_id' in result:
                mem_id = result['memory_id']
                # 获取与其他结果的共现分数
                related_ids = [id for id in mem_ids if id != mem_id]
                co_score = self.tracker.get_co_occurrence_score(mem_id, related_ids)

                # 增强原始分数（如果有的话）
                original_score = result.get('score', 0.5)
                enhanced_score = original_score * (1.0 + co_score * 0.3)  # 最多增强30%
                result['enhanced_score'] = enhanced_score
                result['co_occurrence_score'] = co_score

        # 按增强分数排序
        search_results.sort(key=lambda x: x.get('enhanced_score', 0), reverse=True)

        return search_results

    def get_stats(self):
        """获取集成统计"""
        try:
            stats = self.tracker.get_stats()
            if 'engine_stats' in stats:
                tracker_stats = stats['engine_stats']
            else:
                tracker_stats = stats
        except Exception as e:
            print(f"警告：获取共现图统计失败: {e}")
            tracker_stats = {}

        # 语义向量统计（如果可用）
        vector_stats = {}
        if self.vector_store is not None:
            try:
                vector_stats = self.vector_store.get_stats()
            except Exception as e:
                print(f"警告：获取语义向量统计失败: {e}")

        # 记忆文件统计
        memory_files = []
        if (self.workspace / 'MEMORY.md').exists():
            memory_files.append('MEMORY.md')
        
        if self.memory_dir.exists():
            memory_files.extend([f.name for f in self.memory_dir.glob('*.md')])
        
        return {
            'memory_files': len(memory_files),
            'co_occurrence_stats': tracker_stats,
            'semantic_vector_stats': vector_stats,
            'workspace': str(self.workspace)
        }
    
    def semantic_search(self, query: str, limit: int = 10) -> list:
        """语义向量搜索"""
        if self.vector_store is None:
            print("警告：语义向量适配器不可用，无法执行语义搜索")
            return []
        
        try:
            results = self.vector_store.search(query, limit)
            # 转换为统一格式
            formatted = []
            for r in results:
                formatted.append({
                    'content': f"语义匹配: {r.get('memory_id', 'unknown')}",
                    'score': r.get('score', 0.0),
                    'type': 'semantic',
                    'metadata': r,
                    'memory_id': r.get('memory_id')
                })
            return formatted
        except Exception as e:
            print(f"语义向量搜索失败: {e}")
            return []
    
    def enhance_search_with_vectors(self, query: str, search_results: list, vector_weight: float = 0.3) -> list:
        """使用语义向量增强搜索结果（可选）"""
        if self.vector_store is None or not search_results:
            return search_results
        
        # 获取语义向量搜索结果
        vector_results = self.semantic_search(query, len(search_results) * 2)
        if not vector_results:
            return search_results
        
        # 为每个原始结果计算语义相似度
        for result in search_results:
            # 提取文本内容
            content = result.get('content', '') or result.get('text', '')
            if not content:
                continue
            
            # 寻找最相似的向量结果
            best_vector_score = 0.0
            for vec_result in vector_results:
                # 简单相似度匹配（实际应使用向量相似度）
                # 这里简化：使用向量结果的分数作为参考
                vec_score = vec_result['score']
                if vec_score > best_vector_score:
                    best_vector_score = vec_score
            
            # 增强原始分数
            original_score = result.get('score', 0.5)
            enhanced_score = original_score * (1.0 + best_vector_score * vector_weight)
            result['semantic_boost'] = best_vector_score
            result['enhanced_score'] = enhanced_score
        
        # 重新排序
        search_results.sort(key=lambda x: x.get('enhanced_score', 0), reverse=True)
        return search_results


if __name__ == "__main__":
    print("=== Memory Sync Enhanced 集成脚本 ===")
    print(f"工作空间: /root/.openclaw/workspace")
    print()

    integration = MemoryIntegration()

    # 同步记忆
    print("1. 同步记忆到共现图...")
    count = integration.sync_to_cooccurrence()
    print(f"   同步完成: {count} 个记忆片段")

    # 显示统计
    print("\n2. 系统统计:")
    stats = integration.get_stats()
    print(f"   记忆文件: {stats['memory_files']} 个")
    print(f"   共现边: {stats['co_occurrence_stats']['total_edges']} 条")
    print(f"   唯一记忆: {stats['co_occurrence_stats']['unique_memories']} 个")
    print(f"   平均权重: {stats['co_occurrence_stats']['avg_weight']}")

    # 测试增强搜索（模拟）
    print("\n3. 测试增强搜索...")
    test_results = [
        {'content': 'ClawHub API 已配置完成', 'path': 'memory/2026-03-13.md', 'lines': (1, 5), 'score': 0.8},
        {'content': 'Context Window 检查完成', 'path': 'memory/2026-03-13.md', 'lines': (10, 15), 'score': 0.7},
        {'content': 'Memory Sync Enhanced 安装', 'path': 'memory/2026-03-13.md', 'lines': (20, 25), 'score': 0.9}
    ]

    enhanced = integration.enhance_search("记忆配置", test_results)
    print(f"   增强 {len(enhanced)} 个结果")
    for i, result in enumerate(enhanced[:3]):
        print(f"   {i+1}. {result['content'][:50]}... (原分: {result.get('score', 0):.2f}, 增强: {result.get('enhanced_score', 0):.2f})")

    print("\n=== 集成脚本完成 ===")