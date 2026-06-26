#!/usr/bin/env python3
"""
配置加载模块
"""
import os
import yaml
from pathlib import Path
from typing import List, Dict, Any


class Config:
    """配置类"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # 默认当前目录下的config.yaml
            config_path = Path(__file__).parent / "config.yaml"
        
        self.config_path = config_path
        self._config = self._load()
    
    def _load(self) -> Dict:
        """加载配置文件"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    # ==================== 飞书配置 ====================
    
    @property
    def feishu_webhook(self) -> str:
        return self._config.get('feishu', {}).get('webhook', '')
    
    @property
    def feishu_mention_ids(self) -> List[str]:
        return self._config.get('feishu', {}).get('mention_ids', [])
    
    @property
    def feishu_alert_webhook(self) -> str:
        return self._config.get('feishu', {}).get('alert_webhook', '')
    
    # ==================== 告警配置 ====================
    
    @property
    def alert_enabled(self) -> bool:
        return self._config.get('alert', {}).get('enabled', True)
    
    @property
    def alert_failure_threshold(self) -> int:
        return self._config.get('alert', {}).get('failure_threshold', 3)
    
    @property
    def alert_cooldown_seconds(self) -> int:
        return self._config.get('alert', {}).get('cooldown_seconds', 3600)
    
    # ==================== 抓取配置 ====================
    
    @property
    def timeout(self) -> int:
        return self._config.get('scraper', {}).get('timeout', 30)
    
    @property
    def max_retries(self) -> int:
        return self._config.get('scraper', {}).get('max_retries', 3)
    
    @property
    def min_delay(self) -> float:
        return self._config.get('scraper', {}).get('min_delay', 1)
    
    @property
    def max_delay(self) -> float:
        return self._config.get('scraper', {}).get('max_delay', 3)
    
    @property
    def user_agents(self) -> List[str]:
        agents = self._config.get('scraper', {}).get('user_agents', [])
        if not agents:
            return ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"]
        return agents
    
    # ==================== 监控配置 ====================
    
    @property
    def enabled_exchanges(self) -> List[Dict]:
        exchanges = self._config.get('monitor', {}).get('exchanges', [])
        return [ex for ex in exchanges if ex.get('enabled', False)]
    
    @property
    def exchange_urls(self) -> Dict[str, str]:
        """获取所有交易所URL映射"""
        result = {}
        exchanges = self._config.get('monitor', {}).get('exchanges', [])
        for ex in exchanges:
            name = ex.get('name', '')
            url = ex.get('url', '')
            if name and url:
                result[name] = url
        return result
    
    # ==================== 存储配置 ====================
    
    @property
    def db_path(self) -> str:
        return self._config.get('storage', {}).get('db_path', './data/ipo_cache.db')
    
    @property
    def backup_days(self) -> int:
        return self._config.get('storage', {}).get('backup_days', 30)
    
    # ==================== 定时任务配置 ====================
    
    @property
    def scheduler_enabled(self) -> bool:
        return self._config.get('scheduler', {}).get('enabled', True)
    
    @property
    def scheduler_interval_hours(self) -> int:
        return self._config.get('scheduler', {}).get('interval_hours', 1)
    
    @property
    def scheduler_daily_time(self) -> str:
        return self._config.get('scheduler', {}).get('daily_time', '')
    
    # ==================== 日志配置 ====================
    
    @property
    def log_level(self) -> str:
        return self._config.get('logging', {}).get('level', 'INFO')
    
    @property
    def log_file(self) -> str:
        return self._config.get('logging', {}).get('file', './logs/ipo_monitor.log')
    
    @property
    def log_max_bytes(self) -> int:
        return self._config.get('logging', {}).get('max_bytes', 10485760)
    
    @property
    def log_backup_count(self) -> int:
        return self._config.get('logging', {}).get('backup_count', 5)


# 导出
__all__ = ['Config']
