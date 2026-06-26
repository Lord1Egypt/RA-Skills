#!/usr/bin/env python3
"""
抓取器基类 - 提供超时、重试、反爬等通用能力
增强版：增加异常处理、日志记录和告警回调
"""
import time
import random
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Callable
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ScraperError(Exception):
    """抓取器异常基类"""
    pass


class NetworkError(ScraperError):
    """网络请求异常"""
    pass


class ParseError(ScraperError):
    """解析异常"""
    pass


class BaseScraper(ABC):
    """抓取器基类"""
    
    # 默认请求头
    DEFAULT_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    def __init__(self, config, exchange: str):
        self.config = config
        self.exchange = exchange
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = self._create_session()
        self._current_ua_index = 0
        
        # 失败计数（用于告警）
        self._failure_count = 0
        self._last_failure_time = None
        self._alert_callback: Optional[Callable] = None
    
    def _create_session(self) -> requests.Session:
        """创建带重试机制的Session"""
        session = requests.Session()
        
        # 配置重试策略：指数退避
        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=2,  # 2秒、4秒、6秒
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict:
        """获取带User-Agent的请求头"""
        headers = self.DEFAULT_HEADERS.copy()
        agents = self.config.user_agents
        headers['User-Agent'] = agents[self._current_ua_index % len(agents)]
        return headers
    
    def _rotate_user_agent(self):
        """轮换User-Agent"""
        self._current_ua_index += 1
    
    def set_alert_callback(self, callback: Callable):
        """设置告警回调函数
        
        Args:
            callback: 回调函数，签名为 callback(exchange: str, error: str, failure_count: int)
        """
        self._alert_callback = callback
    
    def _trigger_alert(self, error_msg: str):
        """触发告警"""
        self._failure_count += 1
        current_time = datetime.now()
        
        # 检查是否达到告警阈值
        if self.config.alert_enabled:
            threshold = self.config.alert_failure_threshold
            cooldown = self.config.alert_cooldown_seconds
            
            # 检查是否在冷却期内
            if self._last_failure_time:
                elapsed = (current_time - self._last_failure_time).total_seconds()
                if elapsed >= cooldown:
                    # 冷却期过了，重置计数（清零而不是重置为1）
                    self._failure_count = 0
                else:
                    # 还在冷却期内，不触发告警，只计数
                    if self._failure_count >= threshold:
                        # 已经达到阈值，但在冷却期内，不重复告警
                        self.logger.debug(f"{self.exchange} 在冷却期内，跳过告警")
                        return
            
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
        
        self._last_failure_time = current_time
    
    def _reset_failure_count(self):
        """重置失败计数（成功时调用）"""
        if self._failure_count > 0:
            self.logger.info(f"{self.exchange} 恢复成功，重置失败计数")
        self._failure_count = 0
        self._last_failure_time = None
    
    def fetch_with_retry(self, url: str, timeout: int = None) -> Optional[requests.Response]:
        """
        带重试的请求
        
        Args:
            url: 请求URL
            timeout: 超时时间（秒）
        
        Returns:
            Response对象或None
        """
        if timeout is None:
            timeout = self.config.timeout
        
        max_attempts = self.config.max_retries + 1
        attempt = 0
        last_error = None
        
        while attempt < max_attempts:
            # 随机延迟，反爬
            delay = random.uniform(self.config.min_delay, self.config.max_delay)
            time.sleep(delay)
            
            try:
                response = self.session.get(
                    url,
                    headers=self._get_headers(),
                    timeout=timeout
                )
                
                # 处理反爬
                if response.status_code == 403:
                    self.logger.warning(f"403 Forbidden，尝试更换UA")
                    self._rotate_user_agent()
                    attempt += 1
                    last_error = "403 Forbidden"
                    continue
                
                if response.status_code == 429:
                    # 限流，等待更长时间
                    wait_time = 30 * (attempt + 1)
                    self.logger.warning(f"429 Rate Limited，等待 {wait_time}秒")
                    time.sleep(wait_time)
                    attempt += 1
                    last_error = "429 Rate Limited"
                    continue
                
                response.raise_for_status()
                
                # 成功，重置失败计数
                self._reset_failure_count()
                return response
                
            except requests.exceptions.Timeout as e:
                self.logger.warning(f"请求超时 (尝试 {attempt + 1}/{max_attempts}): {url}")
                attempt += 1
                last_error = f"Timeout: {e}"
                
            except requests.exceptions.HTTPError as e:
                self.logger.warning(f"HTTP错误 (尝试 {attempt + 1}/{max_attempts}): {e}")
                attempt += 1
                last_error = f"HTTP Error: {e}"
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"请求失败 (尝试 {attempt + 1}/{max_attempts}): {e}")
                attempt += 1
                last_error = f"Request Error: {e}"
        
        error_msg = f"重试{max_attempts}次后仍失败: {url}"
        self.logger.error(error_msg)
        
        # 触发告警
        self._trigger_alert(last_error or error_msg)
        
        return None
    
    def safe_fetch(self, url: str, timeout: int = None) -> Optional[requests.Response]:
        """
        安全的抓取方法，包装了异常处理
        
        Args:
            url: 请求URL
            timeout: 超时时间
        
        Returns:
            Response对象或None
        """
        try:
            return self.fetch_with_retry(url, timeout)
        except Exception as e:
            self.logger.exception(f"抓取异常: {url} - {e}")
            self._trigger_alert(f"Exception: {e}")
            return None
    
    @abstractmethod
    def fetch(self) -> List[Dict]:
        """
        抓取数据（子类实现）
        
        Returns:
            IPO数据列表
        """
        pass
    
    def wait_for_load(self, selector: str = None, timeout: int = 10):
        """等待页面加载完成（简化实现）"""
        time.sleep(2)


# 导出
__all__ = ['BaseScraper', 'ScraperError', 'NetworkError', 'ParseError']
