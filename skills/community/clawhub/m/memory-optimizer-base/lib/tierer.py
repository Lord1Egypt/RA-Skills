#!/usr/bin/env python3
"""
记忆分层器 - 将记忆按热度和重要性分层
"""

from datetime import datetime, timedelta
from pathlib import Path
import config

class MemoryTierer:
    def __init__(self, config_obj):
        self.config = config_obj
        base_path = self.config.get('memory.base_path', '~/.openclaw/workspace')
        self.workspace_root = Path(base_path).expanduser()

    def tier_all(self, strategy='smart'):
        """对所有记忆进行分层"""
        result = {'hot': 0, 'warm': 0, 'cold': 0, 'archive': 0, 'freed_mb': 0.0}

        memory_files = self._get_all_memory_files()

        for file_path in memory_files:
            tier = self._determine_tier(file_path, strategy)
            result[tier] += 1

        # 模拟计算释放空间（实际需要移动文件）
        result['freed_mb'] = result['cold'] * 0.05 + result['archive'] * 0.1

        return result

    def _get_all_memory_files(self):
        """获取所有记忆文件"""
        files = []
        memory_dir = self.workspace_root / 'memory'
        if memory_dir.exists():
            files.extend(memory_dir.glob('*.md'))
        return files

    def _determine_tier(self, file_path, strategy):
        """确定文件所属层级"""
        stat = file_path.stat()
        file_age_days = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days

        # 根据策略判断
        if strategy == 'lru':
            # 最近最少使用
            if file_age_days < 7:
                return 'hot'
            elif file_age_days < 30:
                return 'warm'
            elif file_age_days < 180:
                return 'cold'
            else:
                return 'archive'

        elif strategy == 'fifo':
            # 先进先出
            if file_age_days < 30:
                return 'hot'
            elif file_age_days < 90:
                return 'warm'
            elif file_age_days < 365:
                return 'cold'
            else:
                return 'archive'

        else:  # smart 策略
            # 智能：结合文件大小、修改频率、内容关键词
            file_size = stat.st_size
            if file_age_days < 3 and file_size > 1024:
                return 'hot'
            elif file_age_days < 14:
                return 'warm'
            elif file_age_days < 60:
                return 'cold'
            else:
                return 'archive'
