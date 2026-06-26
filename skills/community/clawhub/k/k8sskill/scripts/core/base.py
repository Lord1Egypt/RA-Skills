"""
文件功能：K8sSkill核心基础模块
主要类/函数：
    - Severity - 问题严重程度枚举
    - Failure - 故障详情数据类
    - AnalysisResult - 分析结果数据类
    - AnalyzerError - 分析器错误基类
    - BaseAnalyzer - 分析器抽象基类
    - ResourceCache - 资源缓存管理器
作者：chenzc
创建时间：2026-04-03
最后修改：2026-04-03

LEARNING: 抽象基类设计模式，统一分析器接口
IMPORTANT: 所有具体分析器必须继承BaseAnalyzer
NOTE: 使用模板方法模式定义分析流程
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import re
import os
import logging
import time
from datetime import datetime
from functools import wraps
from collections import OrderedDict

# 配置日志
logger = logging.getLogger(__name__)

# ============== 性能配置 ==============
PERF_CONFIG = {
    "page_size": 100,
    "cache_ttl": 300,
    "request_timeout": 30,
    "max_concurrent": 5,
    "retry_count": 3,
    "retry_delay": 1,
    "max_iterations": 1000,
    "max_items": 50000,
}

# 尝试导入kubernetes客户端
try:
    from kubernetes import client, config
    from kubernetes.client.exceptions import ApiException
    K8S_AVAILABLE = True
except ImportError:
    K8S_AVAILABLE = False
    logger.warning("kubernetes库未安装，分析功能不可用")


# ============== 自定义错误类型 ==============

class AnalyzerError(Exception):
    """
    分析器错误基类
    
    所有分析器相关错误的父类
    
    使用示例：
    >>> raise AnalyzerError("无法连接Kubernetes集群")
    """
    pass


class K8sConnectionError(AnalyzerError):
    """Kubernetes连接错误"""
    pass


class ResourceNotFoundError(AnalyzerError):
    """资源未找到错误"""
    pass


class AnalysisFailedError(AnalyzerError):
    """分析过程失败错误"""
    pass


# ============== 性能优化工具 ==============

class ResourceCache:
    """
    资源缓存管理器
    
    功能：
    - 缓存K8s资源查询结果
    - 自动过期清理
    - 内存占用控制
    
    使用示例：
    >>> cache = ResourceCache()
    >>> cache.set("pods:default", pod_list, ttl=300)
    >>> pods = cache.get("pods:default")
    
    LEARNING: 使用TTL缓存避免重复API调用
    IMPORTANT: 缓存时间不宜过长，K8s资源状态变化快
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = None):
        """
        初始化缓存
        
        参数说明：
        - max_size: [int] 最大缓存条目数
        - default_ttl: [int] 默认过期时间(秒)
        """
        self._cache: OrderedDict = OrderedDict()
        self._max_size = max_size
        self._default_ttl = default_ttl or PERF_CONFIG["cache_ttl"]
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        参数说明：
        - key: [str] 缓存键
        
        返回说明：
        - [Optional[Any]] 缓存值，过期或不存在返回None
        """
        if key not in self._cache:
            return None
        
        value, expire_time = self._cache[key]
        
        if time.time() > expire_time:
            del self._cache[key]
            return None
        
        self._cache.move_to_end(key)
        return value
    
    def set(self, key: str, value: Any, ttl: int = None):
        """
        设置缓存值
        
        参数说明：
        - key: [str] 缓存键
        - value: [Any] 缓存值
        - ttl: [int] 过期时间(秒)
        """
        if key in self._cache:
            self._cache.move_to_end(key)
        
        if len(self._cache) >= self._max_size:
            self._cleanup()
        
        expire_time = time.time() + (ttl or self._default_ttl)
        self._cache[key] = (value, expire_time)
    
    def _cleanup(self):
        """清理过期缓存和最久未使用的条目"""
        now = time.time()
        expired = [k for k, (_, exp) in self._cache.items() if now > exp]
        
        for key in expired:
            del self._cache[key]
        
        while len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()


# 全局缓存实例
_global_cache = ResourceCache()


# ============== 工具函数 ==============

def get_kubeconfig_path() -> Optional[str]:
    """
    获取kubeconfig路径
    
    按优先级查找：
    1. KUBECONFIG环境变量
    2. 默认位置 ~/.kube/config
    3. 项目自带配置 config/k8s-Test-admin.conf
    
    返回说明：
    - [Optional[str]] kubeconfig路径，如果未找到返回None
    """
    # 1. 检查环境变量
    kubeconfig_env = os.environ.get('KUBECONFIG')
    if kubeconfig_env and os.path.exists(kubeconfig_env):
        return kubeconfig_env
    
    # 2. 检查默认位置
    home = os.path.expanduser('~')
    default_config = os.path.join(home, '.kube', 'config')
    if os.path.exists(default_config):
        return default_config
    
    # 3. 检查项目自带配置
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_config = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'config', 'k8s-Test-admin.conf')
    if os.path.exists(project_config):
        return project_config
    
    return None


def verify_k8s_connection() -> tuple:
    """
    验证Kubernetes连接是否正常
    
    功能：
    - 检查kubeconfig是否存在
    - 尝试连接集群
    - 返回友好的状态信息
    
    返回说明：
    - [tuple] (success: bool, message: str)
    
    使用示例：
    >>> success, msg = verify_k8s_connection()
    >>> print(msg)
    """
    if not K8S_AVAILABLE:
        return False, "[X] kubernetes库未安装，请运行: pip install kubernetes"
    
    kubeconfig_path = get_kubeconfig_path()
    if not kubeconfig_path:
        return False, "[X] 未找到kubeconfig文件\n   请检查以下位置:\n   1. KUBECONFIG环境变量\n   2. ~/.kube/config\n   3. skill/config/k8s-Test-admin.conf"
    
    try:
        config.load_kube_config(config_file=kubeconfig_path)
        v1 = client.CoreV1Api()
        v1.list_namespace(limit=1, _request_timeout=5)
        return True, f"[OK] 连接成功\n   kubeconfig: {kubeconfig_path}"
    except Exception as e:
        error_msg = str(e)
        if "Unauthorized" in error_msg or "401" in error_msg:
            return False, "[X] 认证失败：kubeconfig中的token或证书已过期"
        elif "Forbidden" in error_msg or "403" in error_msg:
            return False, "[X] 权限不足：当前用户缺少读取集群权限"
        elif "connection refused" in error_msg.lower():
            return False, "[X] 连接失败：无法连接到Kubernetes API Server"
        else:
            return False, f"[X] 连接失败: {e}"


# ============== 数据模型 ==============

class Severity(Enum):
    """
    问题严重程度分级
    
    对应业界标准的错误分类逻辑
    """
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Failure:
    """
    故障详情数据类
    
    参数说明：
    - text: [str] 故障描述文本
    - severity: [Severity] 严重程度
    - reason: [str] 故障原因分类
    - suggestion: [str] 修复建议
    
    示例：
    >>> failure = Failure(
    ...     text="Container crashed with OOMKilled",
    ...     severity=Severity.CRITICAL,
    ...     reason="OOMKilled",
    ...     suggestion="增加内存限制"
    ... )
    """
    text: str
    severity: Severity = Severity.WARNING
    reason: str = ""
    suggestion: str = ""


@dataclass
class AnalysisResult:
    """
    分析结果数据类
    
    参数说明：
    - kind: [str] 资源类型 (Pod/Deployment/Service等)
    - name: [str] 资源名称
    - namespace: [str] 命名空间
    - failures: [List[Failure]] 发现的故障列表
    - details: [Dict[str, Any]] 额外详情信息
    - parent_object: [str] 父级资源（如Deployment拥有Pod）
    
    示例：
    >>> result = AnalysisResult(
    ...     kind="Pod",
    ...     name="api-server-xxx",
    ...     namespace="default",
    ...     failures=[failure1, failure2]
    ... )
    """
    kind: str
    name: str
    namespace: str
    failures: List[Failure] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    parent_object: str = ""
    
    @property
    def has_issues(self) -> bool:
        """检查是否存在问题"""
        return len(self.failures) > 0
    
    @property
    def critical_count(self) -> int:
        """统计Critical级别问题数量"""
        return sum(1 for f in self.failures if f.severity == Severity.CRITICAL)


# ============== 抽象基类 ==============

class BaseAnalyzer(ABC):
    """
    分析器抽象基类
    
    所有具体分析器的父类，定义统一接口和公共方法。
    使用模板方法模式，子类只需实现特定的抽象方法。
    
    使用示例：
    >>> class MyAnalyzer(BaseAnalyzer):
    ...     @property
    ...     def resource_kind(self) -> str:
    ...         return "MyResource"
    ...     
    ...     def _list_resources(self, namespace: str, label_selector: str):
    ...         # 实现资源列表获取
    ...         pass
    ...     
    ...     def _analyze_resource(self, resource) -> List[Failure]:
    ...         # 实现单个资源分析
    ...         pass
    
    LEARNING: 模板方法模式统一分析流程
    IMPORTANT: 子类必须实现所有抽象方法
    """
    
    def __init__(self, k8s_client=None, use_cache: bool = True):
        """
        初始化分析器
        
        参数说明：
        - k8s_client: [Optional[Any]] Kubernetes客户端实例
        - use_cache: [bool] 是否启用缓存，默认启用
        """
        self.client = k8s_client
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._use_cache = use_cache
        self._cache = _global_cache if use_cache else None
        self._timeout = PERF_CONFIG["request_timeout"]
        
        if self.client is None and K8S_AVAILABLE:
            self._init_k8s_client()
    
    def _init_k8s_client(self):
        """初始化Kubernetes客户端"""
        try:
            kubeconfig_path = get_kubeconfig_path()
            if kubeconfig_path:
                config.load_kube_config(config_file=kubeconfig_path)
                self.client = client
                self._logger.info(f"成功加载kubeconfig: {kubeconfig_path}")
            else:
                self._logger.warning("未找到kubeconfig文件")
                self.client = None
        except Exception as e:
            self._logger.error(f"加载kubeconfig失败: {e}")
            self.client = None
    
    @property
    @abstractmethod
    def resource_kind(self) -> str:
        """
        资源类型标识
        
        返回说明：
        - [str] 资源类型名称，如 "Pod", "Deployment" 等
        """
        pass
    
    @property
    def analyzer_name(self) -> str:
        """
        分析器名称
        
        返回说明：
        - [str] 分析器名称，默认使用类名小写
        """
        return self.__class__.__name__.lower().replace("analyzer", "")
    
    def analyze(self, namespace: str = "", label_selector: str = "") -> List[AnalysisResult]:
        """
        执行分析（模板方法）
        
        分析流程：
        1. 检查K8s客户端可用性
        2. 获取资源列表
        3. 逐个分析资源
        4. 返回分析结果
        
        参数说明：
        - namespace: [str] 目标命名空间，空字符串表示所有命名空间
        - label_selector: [str] 标签选择器，用于过滤资源
        
        返回说明：
        - [List[AnalysisResult]] 分析结果列表
        """
        if not K8S_AVAILABLE or self.client is None:
            self._logger.warning("Kubernetes客户端不可用，跳过分析")
            return []
        
        try:
            return self._do_analyze(namespace, label_selector)
        except Exception as e:
            self._logger.error(f"分析过程出错: {e}", exc_info=True)
            return []
    
    @abstractmethod
    def _do_analyze(self, namespace: str, label_selector: str) -> List[AnalysisResult]:
        """
        执行具体分析的抽象方法
        
        参数说明：
        - namespace: [str] 命名空间
        - label_selector: [str] 标签选择器
        
        返回说明：
        - [List[AnalysisResult]] 分析结果列表
        
        NOTE: 子类必须实现此方法
        """
        pass
    
    def _create_result(self, resource: Any, failures: List[Failure], **extra_details) -> AnalysisResult:
        """
        创建分析结果对象
        
        参数说明：
        - resource: [Any] K8s资源对象
        - failures: [List[Failure]] 故障列表
        - **extra_details: 额外详情信息
        
        返回说明：
        - [AnalysisResult] 分析结果对象
        """
        metadata = getattr(resource, 'metadata', None)
        return AnalysisResult(
            kind=self.resource_kind,
            name=getattr(metadata, 'name', 'unknown') if metadata else 'unknown',
            namespace=getattr(metadata, 'namespace', '') if metadata else '',
            failures=failures,
            details=extra_details
        )
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """
        获取缓存数据
        
        参数说明：
        - key: [str] 缓存键
        
        返回说明：
        - [Optional[Any]] 缓存数据
        """
        if self._cache:
            return self._cache.get(key)
        return None
    
    def _set_cached(self, key: str, value: Any, ttl: int = None):
        """
        设置缓存数据
        
        参数说明：
        - key: [str] 缓存键
        - value: [Any] 缓存数据
        - ttl: [int] 过期时间(秒)
        """
        if self._cache:
            self._cache.set(key, value, ttl)
    
    def _list_resources_paginated(
        self,
        list_func: Callable,
        cache_key: str,
        namespace: str = "",
        label_selector: str = "",
        limit: int = None
    ) -> List[Any]:
        """
        分页获取资源列表
        
        参数说明：
        - list_func: [Callable] 列表获取函数
        - cache_key: [str] 缓存键前缀
        - namespace: [str] 命名空间
        - label_selector: [str] 标签选择器
        - limit: [int] 最大返回数量，None表示不限制
        
        返回说明：
        - [List[Any]] 资源列表
        
        LEARNING: 分页获取避免内存溢出
        IMPORTANT: 大集群必须使用分页
        """
        limit = limit or PERF_CONFIG["page_size"]
        full_cache_key = f"{cache_key}:{namespace}:{label_selector}"
        
        cached = self._get_cached(full_cache_key)
        if cached is not None:
            self._logger.debug(f"使用缓存数据: {full_cache_key}")
            return cached
        
        all_items = []
        continue_token = None
        total_count = 0
        iteration = 0
        max_iterations = PERF_CONFIG["max_iterations"]
        
        while iteration < max_iterations:
            iteration += 1
            try:
                if continue_token:
                    response = list_func(
                        limit=limit,
                        _continue=continue_token,
                        label_selector=label_selector if label_selector else None,
                        _request_timeout=self._timeout
                    )
                else:
                    response = list_func(
                        limit=limit,
                        label_selector=label_selector if label_selector else None,
                        _request_timeout=self._timeout
                    )
                
                items = response.items if hasattr(response, 'items') else response
                if not isinstance(items, list):
                    items = [items] if items else []
                
                all_items.extend(items)
                total_count += len(items)
                
                if total_count >= PERF_CONFIG["max_items"]:
                    self._logger.warning(f"资源数量达到上限 {PERF_CONFIG['max_items']}")
                    break
                
                continue_token = getattr(getattr(response, 'metadata', None), '_continue', None)
                
                if not continue_token:
                    break
                    
            except Exception as e:
                self._logger.error(f"分页获取资源失败: {e}", exc_info=True)
                break
        
        if iteration >= max_iterations:
            self._logger.warning(f"分页迭代达到上限 {max_iterations}")
        
        self._set_cached(full_cache_key, all_items)
        self._logger.info(f"获取 {total_count} 个资源: {cache_key}")
        
        return all_items
