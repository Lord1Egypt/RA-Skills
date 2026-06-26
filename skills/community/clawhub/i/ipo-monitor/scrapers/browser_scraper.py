#!/usr/bin/env python3
"""
浏览器Scraper基类 - 使用OpenClaw browser工具抓取数据
"""
import json
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime


class BrowserScraper(ABC):
    """使用浏览器抓取数据的基类"""
    
    def __init__(self, config, exchange: str):
        self.config = config
        self.exchange = exchange
        self.logger = logging.getLogger(self.__class__.__name__)
        self.browser = None
        self.tab_id = None
        
        # 失败计数（用于告警）
        self._failure_count = 0
        self._last_failure_time = None
        self._alert_callback = None
    
    @property
    @abstractmethod
    def url(self) -> str:
        """返回抓取URL"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """返回交易所名称"""
        pass
    
    def set_alert_callback(self, callback):
        """设置告警回调"""
        self._alert_callback = callback
    
    def _trigger_alert(self, error_msg: str):
        """触发告警"""
        from datetime import datetime
        self._failure_count += 1
        current_time = datetime.now()
        
        if self.config.alert_enabled:
            threshold = self.config.alert_failure_threshold
            cooldown = self.config.alert_cooldown_seconds
            
            # 检查是否在冷却期内
            if self._last_failure_time:
                elapsed = (current_time - self._last_failure_time).total_seconds()
                if elapsed >= cooldown:
                    # 冷却期过了，重置计数（清零并更新冷却时间点）
                    self._failure_count = 0
                    self._last_failure_time = current_time
                    return  # 冷却期重置后必须return，避免重复触发告警
            
            # 触发告警
            if self._failure_count >= threshold:
                self.logger.error(
                    f"🚨 告警触发: {self.exchange} 连续失败 {self._failure_count} 次 - {error_msg}"
                )
                
                if self._alert_callback:
                    try:
                        self._alert_callback(self.exchange, error_msg, self._failure_count)
                    except Exception as e:
                        self.logger.error(f"告警回调执行失败: {e}")
                
                # 触发告警后更新告警时间和重置计数
                self._last_failure_time = current_time
                self._failure_count = 0
                return
        
        self._last_failure_time = current_time
    
    def _reset_failure_count(self):
        """重置失败计数"""
        if self._failure_count > 0:
            self.logger.info(f"{self.exchange} 恢复成功，重置失败计数")
        self._failure_count = 0
        self._last_failure_time = None
    
    def fetch(self, browser) -> List[Dict]:
        """使用浏览器抓取数据
        
        Args:
            browser: OpenClaw浏览器实例
            
        Returns:
            IPO数据列表
        """
        try:
            # 打开页面
            result = browser.action(
                action="open",
                url=self.url
            )
            tab_id = result.get("targetId")
            
            # 等待页面加载
            browser.action(
                action="snapshot",
                targetId=tab_id,
                loadState="networkidle"
            )
            
            # 获取快照
            snapshot = browser.action(
                action="snapshot",
                targetId=tab_id
            )
            
            # 解析数据
            data = self.parse(snapshot)
            
            # 成功，重置计数
            self._reset_failure_count()
            
            return data
            
        except Exception as e:
            self.logger.exception(f"{self.name} 抓取失败: {e}")
            self._trigger_alert(f"Browser error: {e}")
            return []
    
    @abstractmethod
    def parse(self, snapshot: Dict) -> List[Dict]:
        """解析浏览器快照
        
        Args:
            snapshot: browser.snapshot()返回的数据
            
        Returns:
            IPO数据列表
        """
        pass


# 导出
__all__ = ['BrowserScraper']
