#!/usr/bin/env python3
"""
记忆备份与恢复系统
确保记忆数据的持久性和可恢复性

功能:
- 完整快照备份
- 增量备份
- 定期自动备份
- 灾难恢复
- 版本管理
"""

import json
import os
import shutil
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import threading
import fcntl


class BackupType(Enum):
    """备份类型"""
    FULL = "full"           # 完整备份
    INCREMENTAL = "incremental"  # 增量备份
    SNAPSHOT = "snapshot"   # 快照


@dataclass
class BackupMetadata:
    """备份元数据"""
    id: str
    type: BackupType
    timestamp: str
    size_bytes: int
    cell_count: int
    checksum: str
    description: str
    parent_id: Optional[str] = None  # 增量备份的父ID
    files: List[str] = field(default_factory=list)


class MemoryBackup:
    """
    记忆备份系统
    
    支持完整备份、增量备份和快速恢复
    """
    
    def __init__(self, memory_path: str = "./memory",
                 backup_path: str = "./memory/backups"):
        self.memory_path = memory_path
        self.backup_path = backup_path
        os.makedirs(backup_path, exist_ok=True)
        
        # 备份索引
        self.backups: Dict[str, BackupMetadata] = {}
        
        # 锁
        self._lock = threading.Lock()
        
        # 配置
        self.max_backups = 20
        self.auto_backup_interval = 3600  # 秒
        
        # 统计
        self.stats = {
            'total_backups': 0,
            'total_restores': 0,
            'total_size': 0,
            'last_backup': None,
            'last_restore': None
        }
        
        self._load_index()
    
    def create_full_backup(self, description: str = "") -> BackupMetadata:
        """创建完整备份"""
        with self._lock:
            backup_id = self._generate_backup_id()
            backup_dir = os.path.join(self.backup_path, backup_id)
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().isoformat()
            files = []
            total_size = 0
            cell_count = 0
            
            # 复制所有记忆文件
            for root, dirs, filenames in os.walk(self.memory_path):
                # 跳过备份目录
                if 'backups' in root:
                    continue
                
                for filename in filenames:
                    src_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(src_path, self.memory_path)
                    dst_path = os.path.join(backup_dir, rel_path)
                    
                    # 创建目标目录
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    
                    # 复制文件
                    shutil.copy2(src_path, dst_path)
                    
                    # 计算大小
                    size = os.path.getsize(dst_path)
                    total_size += size
                    files.append(rel_path)
                    
                    # 统计细胞数量
                    if filename.endswith('.json') and 'cell' in filename:
                        try:
                            with open(dst_path, 'r') as f:
                                data = json.load(f)
                                if isinstance(data, dict):
                                    cell_count += 1
                                elif isinstance(data, list):
                                    cell_count += len(data)
                        except:
                            pass
            
            # 计算校验和
            checksum = self._calculate_checksum(backup_dir)
            
            # 创建元数据
            metadata = BackupMetadata(
                id=backup_id,
                type=BackupType.FULL,
                timestamp=timestamp,
                size_bytes=total_size,
                cell_count=cell_count,
                checksum=checksum,
                description=description or f"完整备份 {timestamp}",
                files=files
            )
            
            # 保存元数据
            self._save_backup_metadata(backup_dir, metadata)
            
            # 更新索引
            self.backups[backup_id] = metadata
            
            # 更新统计
            self.stats['total_backups'] += 1
            self.stats['total_size'] += total_size
            self.stats['last_backup'] = timestamp
            
            # 清理旧备份
            self._cleanup_old_backups()
            
            self._save_index()
            return metadata
    
    def create_incremental_backup(self, description: str = "") -> Optional[BackupMetadata]:
        """创建增量备份"""
        with self._lock:
            # 找到最近的完整备份作为父
            parent = self._find_latest_full_backup()
            if not parent:
                # 没有完整备份，创建一个
                return self.create_full_backup(description)
            
            backup_id = self._generate_backup_id()
            backup_dir = os.path.join(self.backup_path, backup_id)
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().isoformat()
            files = []
            total_size = 0
            cell_count = 0
            
            # 获取父备份时间
            parent_time = datetime.fromisoformat(parent.timestamp).timestamp()
            
            # 只复制修改过的文件
            for root, dirs, filenames in os.walk(self.memory_path):
                if 'backups' in root:
                    continue
                
                for filename in filenames:
                    src_path = os.path.join(root, filename)
                    
                    # 检查修改时间
                    mtime = os.path.getmtime(src_path)
                    if mtime < parent_time:
                        continue
                    
                    rel_path = os.path.relpath(src_path, self.memory_path)
                    dst_path = os.path.join(backup_dir, rel_path)
                    
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    
                    size = os.path.getsize(dst_path)
                    total_size += size
                    files.append(rel_path)
            
            if not files:
                # 没有变化，删除空备份目录
                shutil.rmtree(backup_dir)
                return None
            
            checksum = self._calculate_checksum(backup_dir)
            
            metadata = BackupMetadata(
                id=backup_id,
                type=BackupType.INCREMENTAL,
                timestamp=timestamp,
                size_bytes=total_size,
                cell_count=cell_count,
                checksum=checksum,
                description=description or f"增量备份 {timestamp}",
                parent_id=parent.id,
                files=files
            )
            
            self._save_backup_metadata(backup_dir, metadata)
            self.backups[backup_id] = metadata
            
            self.stats['total_backups'] += 1
            self.stats['total_size'] += total_size
            self.stats['last_backup'] = timestamp
            
            self._cleanup_old_backups()
            self._save_index()
            return metadata
    
    def create_snapshot(self, name: str, description: str = "") -> BackupMetadata:
        """创建命名快照（不会被自动清理）"""
        with self._lock:
            backup_id = f"snapshot_{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            backup_dir = os.path.join(self.backup_path, backup_id)
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().isoformat()
            files = []
            total_size = 0
            cell_count = 0
            
            for root, dirs, filenames in os.walk(self.memory_path):
                if 'backups' in root:
                    continue
                
                for filename in filenames:
                    src_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(src_path, self.memory_path)
                    dst_path = os.path.join(backup_dir, rel_path)
                    
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    
                    size = os.path.getsize(dst_path)
                    total_size += size
                    files.append(rel_path)
            
            checksum = self._calculate_checksum(backup_dir)
            
            metadata = BackupMetadata(
                id=backup_id,
                type=BackupType.SNAPSHOT,
                timestamp=timestamp,
                size_bytes=total_size,
                cell_count=cell_count,
                checksum=checksum,
                description=description or f"快照 {name}"
            )
            
            self._save_backup_metadata(backup_dir, metadata)
            self.backups[backup_id] = metadata
            
            self.stats['total_backups'] += 1
            self.stats['total_size'] += total_size
            self.stats['last_backup'] = timestamp
            
            self._save_index()
            return metadata
    
    def restore(self, backup_id: str, target_path: str = None) -> bool:
        """恢复备份"""
        with self._lock:
            if backup_id not in self.backups:
                return False
            
            metadata = self.backups[backup_id]
            backup_dir = os.path.join(self.backup_path, backup_id)
            
            if not os.path.exists(backup_dir):
                return False
            
            # 验证校验和
            current_checksum = self._calculate_checksum(backup_dir)
            if current_checksum != metadata.checksum:
                print(f"警告: 校验和不匹配，备份可能已损坏")
            
            target = target_path or self.memory_path
            
            # 如果是增量备份，需要先恢复父备份
            if metadata.type == BackupType.INCREMENTAL and metadata.parent_id:
                # 先恢复父备份到临时目录
                temp_dir = os.path.join(self.backup_path, "_temp_restore")
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                
                # 递归恢复所有依赖
                self._restore_chain(metadata, temp_dir)
                
                # 复制到目标
                if os.path.exists(target):
                    # 备份当前数据
                    current_backup = os.path.join(self.backup_path, "_pre_restore")
                    if os.path.exists(current_backup):
                        shutil.rmtree(current_backup)
                    shutil.move(target, current_backup)
                
                shutil.move(temp_dir, target)
            else:
                # 完整备份或快照，直接恢复
                if os.path.exists(target):
                    current_backup = os.path.join(self.backup_path, "_pre_restore")
                    if os.path.exists(current_backup):
                        shutil.rmtree(current_backup)
                    shutil.move(target, current_backup)
                
                shutil.copytree(backup_dir, target)
            
            self.stats['total_restores'] += 1
            self.stats['last_restore'] = datetime.now().isoformat()
            self._save_index()
            
            return True
    
    def _restore_chain(self, metadata: BackupMetadata, target_dir: str) -> None:
        """递归恢复备份链"""
        if metadata.parent_id and metadata.parent_id in self.backups:
            parent = self.backups[metadata.parent_id]
            self._restore_chain(parent, target_dir)
        
        # 应用当前备份
        backup_dir = os.path.join(self.backup_path, metadata.id)
        if os.path.exists(backup_dir):
            for root, dirs, filenames in os.walk(backup_dir):
                for filename in filenames:
                    src_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(src_path, backup_dir)
                    dst_path = os.path.join(target_dir, rel_path)
                    
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    shutil.copy2(src_path, dst_path)
    
    def list_backups(self) -> List[BackupMetadata]:
        """列出所有备份"""
        return sorted(self.backups.values(), key=lambda x: x.timestamp, reverse=True)
    
    def get_backup(self, backup_id: str) -> Optional[BackupMetadata]:
        """获取备份信息"""
        return self.backups.get(backup_id)
    
    def delete_backup(self, backup_id: str) -> bool:
        """删除备份"""
        with self._lock:
            if backup_id not in self.backups:
                return False
            
            metadata = self.backups[backup_id]
            
            # 快照不能删除（除非强制）
            if metadata.type == BackupType.SNAPSHOT:
                return False
            
            # 检查是否有增量备份依赖此备份
            for bid, bm in self.backups.items():
                if bm.parent_id == backup_id:
                    return False
            
            # 删除文件
            backup_dir = os.path.join(self.backup_path, backup_id)
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
            
            del self.backups[backup_id]
            self._save_index()
            
            return True
    
    def _generate_backup_id(self) -> str:
        """生成备份ID"""
        return f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"
    
    def _calculate_checksum(self, directory: str) -> str:
        """计算目录校验和"""
        hasher = hashlib.sha256()
        
        for root, dirs, filenames in sorted(os.walk(directory)):
            for filename in sorted(filenames):
                filepath = os.path.join(root, filename)
                with open(filepath, 'rb') as f:
                    hasher.update(filepath.encode())
                    hasher.update(f.read())
        
        return hasher.hexdigest()[:16]
    
    def _find_latest_full_backup(self) -> Optional[BackupMetadata]:
        """找到最近的完整备份"""
        full_backups = [b for b in self.backups.values() 
                       if b.type == BackupType.FULL]
        if full_backups:
            return max(full_backups, key=lambda x: x.timestamp)
        return None
    
    def _save_backup_metadata(self, backup_dir: str, metadata: BackupMetadata) -> None:
        """保存备份元数据"""
        meta_path = os.path.join(backup_dir, "backup_metadata.json")
        with open(meta_path, 'w') as f:
            json.dump({
                'id': metadata.id,
                'type': metadata.type.value,
                'timestamp': metadata.timestamp,
                'size_bytes': metadata.size_bytes,
                'cell_count': metadata.cell_count,
                'checksum': metadata.checksum,
                'description': metadata.description,
                'parent_id': metadata.parent_id,
                'files': metadata.files
            }, f, indent=2)
    
    def _cleanup_old_backups(self) -> None:
        """清理旧备份"""
        # 不清理快照
        regular_backups = [b for b in self.backups.values() 
                         if b.type != BackupType.SNAPSHOT]
        
        if len(regular_backups) <= self.max_backups:
            return
        
        # 按时间排序
        regular_backups.sort(key=lambda x: x.timestamp)
        
        # 删除最旧的备份（确保没有依赖）
        while len(regular_backups) > self.max_backups:
            oldest = regular_backups[0]
            
            # 检查依赖
            has_dependents = any(
                b.parent_id == oldest.id for b in self.backups.values()
            )
            
            if not has_dependents:
                self.delete_backup(oldest.id)
                regular_backups.pop(0)
            else:
                # 跳过有依赖的备份
                regular_backups.pop(0)
    
    def _load_index(self) -> None:
        """加载备份索引"""
        index_file = os.path.join(self.backup_path, 'backup_index.json')
        if os.path.exists(index_file):
            try:
                with open(index_file, 'r') as f:
                    data = json.load(f)
                
                self.stats = data.get('stats', self.stats)
                
                for bid, bm in data.get('backups', {}).items():
                    self.backups[bid] = BackupMetadata(
                        id=bm['id'],
                        type=BackupType(bm['type']),
                        timestamp=bm['timestamp'],
                        size_bytes=bm['size_bytes'],
                        cell_count=bm['cell_count'],
                        checksum=bm['checksum'],
                        description=bm['description'],
                        parent_id=bm.get('parent_id'),
                        files=bm.get('files', [])
                    )
            except Exception as e:
                print(f"加载备份索引失败: {e}")
    
    def _save_index(self) -> None:
        """保存备份索引"""
        index_file = os.path.join(self.backup_path, 'backup_index.json')
        
        data = {
            'stats': self.stats,
            'backups': {
                bid: {
                    'id': bm.id,
                    'type': bm.type.value,
                    'timestamp': bm.timestamp,
                    'size_bytes': bm.size_bytes,
                    'cell_count': bm.cell_count,
                    'checksum': bm.checksum,
                    'description': bm.description,
                    'parent_id': bm.parent_id,
                    'files': bm.files
                }
                for bid, bm in self.backups.items()
            }
        }
        
        with open(index_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_report(self) -> Dict:
        """获取报告"""
        return {
            'stats': self.stats,
            'backup_count': len(self.backups),
            'backup_types': {
                t.value: len([b for b in self.backups.values() if b.type == t])
                for t in BackupType
            },
            'total_size_human': self._format_size(self.stats['total_size']),
            'latest_backup': self.stats['last_backup']
        }
    
    def _format_size(self, size: int) -> str:
        """格式化大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"


def demo_backup():
    """演示备份系统"""
    print("=" * 60)
    print("记忆备份系统演示")
    print("=" * 60)
    
    backup = MemoryBackup()
    
    # 创建完整备份
    print("\n创建完整备份...")
    metadata = backup.create_full_backup("初始完整备份")
    print(f"备份ID: {metadata.id}")
    print(f"大小: {backup._format_size(metadata.size_bytes)}")
    print(f"细胞数: {metadata.cell_count}")
    
    # 创建快照
    print("\n创建快照...")
    snapshot = backup.create_snapshot("v1.0", "版本1.0快照")
    print(f"快照ID: {snapshot.id}")
    
    # 创建增量备份
    print("\n创建增量备份...")
    incremental = backup.create_incremental_backup("日常增量备份")
    if incremental:
        print(f"增量备份ID: {incremental.id}")
        print(f"变更文件数: {len(incremental.files)}")
    else:
        print("无变更，跳过增量备份")
    
    # 列出备份
    print("\n备份列表:")
    for bm in backup.list_backups()[:5]:
        print(f"  [{bm.type.value}] {bm.id}: {bm.description}")
    
    # 报告
    print("\n备份报告:")
    report = backup.get_report()
    for k, v in report.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    demo_backup()
