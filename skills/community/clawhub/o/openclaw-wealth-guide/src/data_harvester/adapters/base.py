"""
适配器基类模块
定义所有数据源适配器的通用接口
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime

from ..config import SourceConfig
from ..exceptions import AdapterError, FetchError

logger = logging.getLogger(__name__)


class SourceAdapter(ABC):
    """数据源适配器基类"""
    
    def __init__(self, config: SourceConfig):
        """
        初始化适配器
        
        Args:
            config: 数据源配置
        """
        self.config = config
        self.name = config.name
        self.type = config.type
        self.enabled = config.enabled
        
        # 统计信息
        self.fetch_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_fetch_time = 0.0
        self.last_fetch_time: Optional[datetime] = None
        
        logger.debug(f"初始化适配器: {self.name} ({self.type})")
    
    def fetch(self, **kwargs) -> Any:
        """
        获取数据（包装方法，包含错误处理和统计）
        
        Args:
            **kwargs: 传递给实际fetch方法的参数
            
        Returns:
            获取的数据
            
        Raises:
            FetchError: 获取数据失败
        """
        if not self.enabled:
            raise AdapterError(f"适配器已禁用: {self.name}")
        
        start_time = time.time()
        self.fetch_count += 1
        self.last_fetch_time = datetime.now()
        
        try:
            logger.info(f"开始获取数据: {self.name}")
            
            # 合并配置参数和传递的参数
            fetch_kwargs = self._prepare_fetch_kwargs(kwargs)
            
            # 执行实际的数据获取
            data = self._fetch_impl(**fetch_kwargs)
            
            # 验证返回数据
            if data is None:
                raise FetchError(f"适配器返回空数据: {self.name}")
                
            # 统计成功
            end_time = time.time()
            fetch_time = end_time - start_time
            self.total_fetch_time += fetch_time
            self.success_count += 1
            
            logger.info(
                f"数据获取成功: {self.name}, "
                f"数据大小: {self._get_data_size(data)}, "
                f"耗时: {fetch_time:.2f}s"
            )
            
            return data
            
        except Exception as e:
            # 统计失败
            end_time = time.time()
            fetch_time = end_time - start_time
            self.total_fetch_time += fetch_time
            self.error_count += 1
            
            error_msg = f"数据获取失败 {self.name}: {e}"
            logger.error(error_msg, exc_info=True)
            
            # 如果配置了重试，记录但不抛出异常
            if self.config.retry_count > 0:
                logger.warning(f"将进行重试: {self.name}")
                raise FetchError(error_msg) from e
            else:
                raise FetchError(error_msg) from e
    
    @abstractmethod
    def _fetch_impl(self, **kwargs) -> Any:
        """
        实际的数据获取实现（子类必须实现）
        
        Args:
            **kwargs: 获取参数
            
        Returns:
            获取的数据
        """
        pass
    
    def _prepare_fetch_kwargs(self, user_kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        准备获取参数，合并配置和用户参数
        
        Args:
            user_kwargs: 用户传递的参数
            
        Returns:
            合并后的参数
        """
        # 基础参数
        kwargs = {}
        
        # 添加类型特定的配置参数
        if self.type == "web" and self.config.url:
            kwargs["url"] = self.config.url
            if self.config.headers:
                kwargs["headers"] = self.config.headers
            if self.config.params:
                kwargs["params"] = self.config.params
        
        elif self.type == "api" and self.config.url:
            kwargs["url"] = self.config.url
            if self.config.headers:
                kwargs["headers"] = self.config.headers
            if self.config.params:
                kwargs["params"] = self.config.params
        
        elif self.type == "file" and self.config.path:
            kwargs["path"] = self.config.path
        
        elif self.type == "database" and self.config.connection_string:
            kwargs["connection_string"] = self.config.connection_string
            if self.config.query:
                kwargs["query"] = self.config.query
        
        # 添加认证信息
        if self.config.auth:
            kwargs["auth"] = self.config.auth
        
        # 添加提取规则
        if self.config.extract_rules:
            kwargs["extract_rules"] = self.config.extract_rules
        
        # 添加超时设置
        kwargs["timeout"] = self.config.timeout
        
        # 用户参数覆盖配置参数
        kwargs.update(user_kwargs)
        
        return kwargs
    
    def _get_data_size(self, data: Any) -> str:
        """获取数据大小的可读字符串"""
        if data is None:
            return "0 bytes"
        
        if isinstance(data, (list, tuple)):
            return f"{len(data)} items"
        elif isinstance(data, dict):
            return f"{len(data)} keys"
        elif isinstance(data, (str, bytes)):
            return f"{len(data)} chars"
        else:
            return "1 item"
    
    def get_stats(self) -> Dict[str, Any]:
        """获取适配器统计信息"""
        avg_time = 0
        if self.fetch_count > 0:
            avg_time = self.total_fetch_time / self.fetch_count
        
        success_rate = 0
        if self.fetch_count > 0:
            success_rate = (self.success_count / self.fetch_count) * 100
        
        return {
            "name": self.name,
            "type": self.type,
            "enabled": self.enabled,
            "fetch_count": self.fetch_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": f"{success_rate:.1f}%",
            "total_fetch_time": f"{self.total_fetch_time:.2f}s",
            "average_fetch_time": f"{avg_time:.2f}s",
            "last_fetch_time": self.last_fetch_time.isoformat() if self.last_fetch_time else None,
            "config": {
                "timeout": self.config.timeout,
                "retry_count": self.config.retry_count
            }
        }
    
    def validate(self) -> bool:
        """
        验证适配器配置
        
        Returns:
            bool: 配置是否有效
        """
        try:
            # 基本验证
            if not self.name:
                logger.error("适配器名称不能为空")
                return False
            
            if not self.enabled:
                logger.warning(f"适配器已禁用: {self.name}")
                return True  # 禁用的适配器仍然认为是有效的
            
            # 类型特定验证
            if self.type == "web" and not self.config.url:
                logger.error(f"Web适配器必须配置URL: {self.name}")
                return False
            
            if self.type == "api" and not self.config.url:
                logger.error(f"API适配器必须配置URL: {self.name}")
                return False
            
            if self.type == "file" and not self.config.path:
                logger.error(f"文件适配器必须配置路径: {self.name}")
                return False
            
            if self.type == "database" and not self.config.connection_string:
                logger.error(f"数据库适配器必须配置连接字符串: {self.name}")
                return False
            
            logger.debug(f"适配器验证通过: {self.name}")
            return True
            
        except Exception as e:
            logger.error(f"适配器验证失败 {self.name}: {e}")
            return False
    
    def close(self) -> None:
        """关闭适配器，释放资源"""
        logger.debug(f"关闭适配器: {self.name}")


class WebAdapter(SourceAdapter):
    """Web页面适配器"""
    
    def _fetch_impl(self, **kwargs) -> Any:
        # 实现Web页面数据获取
        # 这里使用requests和beautifulsoup4
        import requests
        from bs4 import BeautifulSoup
        
        url = kwargs.get("url")
        if not url:
            raise ValueError("URL不能为空")
        
        headers = kwargs.get("headers", {})
        params = kwargs.get("params", {})
        timeout = kwargs.get("timeout", 30)
        
        # 发送请求
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        
        # 解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 提取数据
        extract_rules = kwargs.get("extract_rules")
        if extract_rules:
            return self._extract_data(soup, extract_rules)
        else:
            # 默认返回整个HTML
            return str(soup)
    
    def _extract_data(self, soup: BeautifulSoup, extract_rules: Dict[str, Any]) -> Dict[str, Any]:
        """根据提取规则提取数据"""
        result = {}
        
        for key, rule in extract_rules.items():
            if isinstance(rule, dict):
                # 复杂提取规则
                selector = rule.get("selector")
                attr = rule.get("attr")
                regex = rule.get("regex")
                
                if selector:
                    elements = soup.select(selector)
                    if elements:
                        if attr:
                            values = [elem.get(attr) for elem in elements]
                        else:
                            values = [elem.get_text(strip=True) for elem in elements]
                        
                        # 应用正则表达式
                        if regex:
                            import re
                            pattern = re.compile(regex)
                            values = [pattern.search(str(v)).group() if v and pattern.search(str(v)) else v 
                                     for v in values]
                        
                        result[key] = values if len(values) > 1 else values[0] if values else None
            elif isinstance(rule, str):
                # 简单CSS选择器
                elements = soup.select(rule)
                if elements:
                    result[key] = [elem.get_text(strip=True) for elem in elements]
        
        return result


class ApiAdapter(SourceAdapter):
    """API适配器"""
    
    def _fetch_impl(self, **kwargs) -> Any:
        import requests
        import json
        
        url = kwargs.get("url")
        if not url:
            raise ValueError("URL不能为空")
        
        headers = kwargs.get("headers", {})
        params = kwargs.get("params", {})
        timeout = kwargs.get("timeout", 30)
        
        # 处理认证
        auth = kwargs.get("auth")
        if auth:
            auth_type = auth.get("type")
            if auth_type == "bearer":
                token = auth.get("token")
                if token:
                    headers["Authorization"] = f"Bearer {token}"
            elif auth_type == "basic":
                username = auth.get("username")
                password = auth.get("password")
                if username and password:
                    from requests.auth import HTTPBasicAuth
                    auth_obj = HTTPBasicAuth(username, password)
                    response = requests.get(url, headers=headers, params=params, 
                                          timeout=timeout, auth=auth_obj)
                else:
                    response = requests.get(url, headers=headers, params=params, 
                                          timeout=timeout)
            else:
                response = requests.get(url, headers=headers, params=params, 
                                      timeout=timeout)
        else:
            response = requests.get(url, headers=headers, params=params, 
                                  timeout=timeout)
        
        response.raise_for_status()
        
        # 尝试解析JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            # 如果不是JSON，返回文本
            return response.text


class FileAdapter(SourceAdapter):
    """文件适配器"""
    
    def _fetch_impl(self, **kwargs) -> Any:
        import pandas as pd
        import json
        
        path = kwargs.get("path")
        if not path:
            raise ValueError("文件路径不能为空")
        
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        
        # 根据文件扩展名选择读取方式
        suffix = file_path.suffix.lower()
        
        if suffix == '.csv':
            # 读取CSV
            encoding = kwargs.get("encoding", "utf-8")
            delimiter = kwargs.get("delimiter", ",")
            has_header = kwargs.get("has_header", True)
            
            if has_header:
                return pd.read_csv(file_path, encoding=encoding, delimiter=delimiter).to_dict(orient='records')
            else:
                return pd.read_csv(file_path, encoding=encoding, delimiter=delimiter, header=None).to_dict(orient='records')
        
        elif suffix in ['.xlsx', '.xls']:
            # 读取Excel
            sheet_name = kwargs.get("sheet_name", 0)
            return pd.read_excel(file_path, sheet_name=sheet_name).to_dict(orient='records')
        
        elif suffix == '.json':
            # 读取JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        elif suffix in ['.txt', '.text']:
            # 读取文本文件
            encoding = kwargs.get("encoding", "utf-8")
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        
        else:
            # 尝试使用pandas自动检测
            try:
                return pd.read_csv(file_path).to_dict(orient='records')
            except:
                # 最后尝试二进制读取
                with open(file_path, 'rb') as f:
                    return f.read()


class DatabaseAdapter(SourceAdapter):
    """数据库适配器"""
    
    def _fetch_impl(self, **kwargs) -> Any:
        import sqlalchemy as sa
        from sqlalchemy import text
        
        connection_string = kwargs.get("connection_string")
        query = kwargs.get("query")
        
        if not connection_string:
            raise ValueError("数据库连接字符串不能为空")
        
        if not query:
            raise ValueError("查询语句不能为空")
        
        # 创建数据库引擎
        engine = sa.create_engine(connection_string)
        
        try:
            # 执行查询
            with engine.connect() as connection:
                result = connection.execute(text(query), kwargs.get("params", {}))
                
                # 转换为字典列表
                columns = result.keys()
                rows = [dict(zip(columns, row)) for row in result]
                
                return rows
        finally:
            engine.dispose()
    
    def close(self) -> None:
        """数据库适配器不需要额外关闭操作"""
        pass