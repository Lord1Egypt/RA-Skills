#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享文件夹双向记忆同步系统

设计原则：
1. Hermes 记忆存 Hermes 数据库，OpenClaw 记忆存 OpenClaw 数据库
2. 共享文件夹作为中转站，不交叉存储
3. 避免记忆混乱，保持系统纯净

作者：伊娃 (Eva)
版本：1.0
创建：2026-04-17
"""

import json
import os
import shutil
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SharedFolderSync')

# 路径配置
SHARED_MEMORY_DIR = Path.home() / '.shared-memory'

# Hermes 相关路径
HERMES_TO_OPENCLAW = SHARED_MEMORY_DIR / 'hermes' / 'to_openclaw'
HERMES_FROM_OPENCLAW = SHARED_MEMORY_DIR / 'hermes' / 'from_openclaw'
HERMES_PROCESSED = SHARED_MEMORY_DIR / 'hermes' / 'processed'
HERMES_LOGS = SHARED_MEMORY_DIR / 'hermes' / 'logs'

# OpenClaw 相关路径
OPENCLAW_TO_HERMES = SHARED_MEMORY_DIR / 'openclaw' / 'to_hermes'
OPENCLAW_FROM_HERMES = SHARED_MEMORY_DIR / 'openclaw' / 'from_hermes'
OPENCLAW_PROCESSED = SHARED_MEMORY_DIR / 'openclaw' / 'processed'
OPENCLAW_LOGS = SHARED_MEMORY_DIR / 'openclaw' / 'logs'

# 备份目录
BACKUP_DIR = SHARED_MEMORY_DIR / 'backups'

# 确保所有目录存在
for directory in [
    SHARED_MEMORY_DIR,
    HERMES_TO_OPENCLAW, HERMES_FROM_OPENCLAW, HERMES_PROCESSED, HERMES_LOGS,
    OPENCLAW_TO_HERMES, OPENCLAW_FROM_HERMES, OPENCLAW_PROCESSED, OPENCLAW_LOGS,
    BACKUP_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)

class SharedFolderSync:
    """共享文件夹双向同步核心类"""
    
    def __init__(self):
        self.sync_history = []
        self.last_sync_time = None
        
    def compute_file_hash(self, file_path: Path) -> str:
        """计算文件哈希值"""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def generate_filename(self, prefix: str, memory_type: str) -> str:
        """生成带时间戳的文件名"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{prefix}_{memory_type}_{timestamp}.json"
    
    def log_sync_operation(self, operation: str, source: str, target: str, 
                          files_count: int, status: str):
        """记录同步操作日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'source': source,
            'target': target,
            'files_count': files_count,
            'status': status
        }
        
        self.sync_history.append(log_entry)
        
        # 保存到日志文件
        log_file = HERMES_LOGS / f"sync_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        logger.info(f"{operation}: {source} → {target}, 文件数: {files_count}, 状态: {status}")
    
    def backup_file(self, file_path: Path, backup_type: str):
        """备份文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = BACKUP_DIR / f"{backup_type}_{file_path.name}_{timestamp}.bak"
        
        try:
            shutil.copy2(file_path, backup_file)
            logger.info(f"✅ 文件备份成功: {file_path} → {backup_file}")
            return True
        except Exception as e:
            logger.error(f"❌ 文件备份失败: {e}")
            return False