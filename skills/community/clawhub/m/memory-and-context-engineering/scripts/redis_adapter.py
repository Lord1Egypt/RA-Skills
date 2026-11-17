# Agent Memory System
# Copyright (C) 2024 kiwifruit
#
# This file is part of Agent Memory System.
#
# Agent Memory System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agent Memory System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agent Memory System.  If not, see <https://www.gnu.org/licenses/>.


"""
Agent Memory System - Redis 适配器

=== 依赖与环境声明 ===
- 运行环境：Python >=3.9
- 直接依赖:
  * redis: >=4.5.0
    - 用途：Redis 客户端连接与操作
  * pydantic: >=2.0.0
    - 用途：配置模型验证
- 标准配置文件:
  ```text
  # requirements.txt
  redis>=4.5.0
  pydantic>=2.0.0
  ```
=== 声明结束 ===

安全提醒：生产环境请使用 Redis 密码认证，并考虑 TLS 加密
"""

from __future__ import annotations

import fnmatch
import threading
import time
from collections import OrderedDict
from contextlib import contextmanager
from typing import Any, Callable

from pydantic import BaseModel, Field

from .logging_config import get_logger

logger = get_logger(__name__)

# 延迟导入 redis，支持无 Redis 环境运行
try:
    import redis
    from redis import Redis
    from redis.exceptions import RedisError, ConnectionError as RedisConnectionError
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    Redis = None  # type: ignore
    RedisError = Exception  # type: ignore
    RedisConnectionError = Exception  # type: ignore


# ============================================================================
# 配置模型
# ============================================================================


class RedisConfig(BaseModel):
    """
    Redis 连接配置（安全增强版）

    支持单机模式，集群模式可后续扩展。

    安全特性：
    - 密码认证（生产环境必须）
    - SSL/TLS 加密连接（可选，推荐）
    - 连接池限制（防止资源耗尽）
    - 敏感数据加密存储（可选）

    使用示例：
    ```python
    config = RedisConfig(
        host="localhost",
        port=6379,
        password="your_password",  # 生产环境必须
        db=0,
        enable_ssl=True,          # 推荐开启
        encrypt_sensitive_data=True,  # 敏感数据加密
    )
    adapter = RedisAdapter(config)
    ```
    """

    host: str = Field(default="localhost", description="Redis 主机地址")
    port: int = Field(default=6379, description="Redis 端口")
    password: str | None = Field(default=None, description="Redis 密码（生产环境必须设置）")
    db: int = Field(default=0, description="Redis 数据库编号")

    # 安全配置
    enable_ssl: bool = Field(default=False, description="启用 SSL/TLS 加密连接")
    ssl_cert_reqs: str = Field(default="required", description="SSL 证书要求 (none, optional, required)")
    ssl_ca_certs: str | None = Field(default=None, description="CA 证书文件路径")
    ssl_keyfile: str | None = Field(default=None, description="SSL 密钥文件路径")
    ssl_certfile: str | None = Field(default=None, description="SSL 证书文件路径")

    # 连接池配置
    max_connections: int = Field(default=10, description="最大连接数")
    socket_timeout: float = Field(default=5.0, description="Socket 超时（秒）")
    socket_connect_timeout: float = Field(default=5.0, description="连接超时（秒）")
    retry_on_timeout: bool = Field(default=True, description="超时是否重试")
    retry_on_error: int = Field(default=3, description="错误重试次数")

    # 敏感数据加密配置
    encrypt_sensitive_data: bool = Field(default=False, description="是否加密敏感数据")
    encryption_key: str | None = Field(default=None, description="数据加密密钥（32字节，base64编码）")

    # 健康检查配置
    health_check_interval: int = Field(default=30, description="健康检查间隔（秒）")

    # Key 前缀
    key_prefix: str = Field(default="memory", description="所有 Key 的前缀")

    def model_post_init(self, __context) -> None:
        """配置后处理"""
        # 安全警告
        if not self.password:
            import warnings
            warnings.warn(
                "WARNING: Redis password not set! "
                "Set password for production environments.",
                UserWarning
            )
        
        # SSL 验证警告
        if self.enable_ssl and self.ssl_cert_reqs == "none":
            import warnings
            warnings.warn(
                "WARNING: SSL enabled but certificate verification disabled!",
                UserWarning
            )
        
        # 加密密钥验证
        if self.encrypt_sensitive_data and not self.encryption_key:
            import warnings
            warnings.warn(
                "WARNING: Encryption enabled but no key provided! "
                "Sensitive data will not be encrypted.",
                UserWarning
            )


# ============================================================================
# Key 命名工具
# ============================================================================


class RedisKeyBuilder:
    """
    Redis Key 命名工具

    命名规范：
    - 前缀: {key_prefix}
    - 格式: {prefix}:{type}:{user_id}:{item_id}
    - 示例: memory:short:user123:item456

    使用示例：
    ```python
    builder = RedisKeyBuilder("memory")

    # 短期记忆
    key = builder.short_term("user123", "item456")
    # → "memory:short:user123:item456"

    # 热度排序
    key = builder.heat_index("user123")
    # → "memory:heat:user123"

    # Token 计数
    key = builder.token_counter("session789")
    # → "memory:token:session789"
    ```
    """

    def __init__(self, prefix: str = "memory") -> None:
        """
        初始化 Key 构建器

        Args:
            prefix: Key 前缀
        """
        self._prefix = prefix

    def _build(self, *parts: str) -> str:
        """构建完整 Key"""
        return ":".join([self._prefix] + list(parts))

    # -----------------------------------------------------------------------
    # 短期记忆相关
    # -----------------------------------------------------------------------

    def short_term(self, user_id: str, item_id: str) -> str:
        """短期记忆项 Key"""
        return self._build("short", user_id, item_id)

    def short_term_list(self, user_id: str) -> str:
        """短期记忆列表 Key（用于存储所有 item_id）"""
        return self._build("short", user_id, "list")

    # -----------------------------------------------------------------------
    # 热度管理相关
    # -----------------------------------------------------------------------

    def heat_index(self, user_id: str) -> str:
        """热度排序 Key（Sorted Set）"""
        return self._build("heat", user_id)

    # -----------------------------------------------------------------------
    # Token 预算相关
    # -----------------------------------------------------------------------

    def token_counter(self, session_id: str) -> str:
        """Token 计数器 Key"""
        return self._build("token", session_id)

    def token_budget(self, session_id: str) -> str:
        """Token 预算配置 Key"""
        return self._build("token", session_id, "budget")

    # -----------------------------------------------------------------------
    # 长期记忆相关
    # -----------------------------------------------------------------------

    def long_term_profile(self, user_id: str) -> str:
        """用户画像 Key"""
        return self._build("long", "profile", user_id)

    def long_term_procedural(self, user_id: str) -> str:
        """程序性记忆 Key"""
        return self._build("long", "procedural", user_id)

    def long_term_reflection(self, user_id: str) -> str:
        """反思记忆列表 Key"""
        return self._build("long", "reflection", user_id)

    # -----------------------------------------------------------------------
    # 检索缓存相关
    # -----------------------------------------------------------------------

    def retrieval_cache(self, query_hash: str) -> str:
        """检索结果缓存 Key"""
        return self._build("cache", "retrieval", query_hash)

    # -----------------------------------------------------------------------
    # 状态相关
    # -----------------------------------------------------------------------

    def state_checkpoint(self, user_id: str, checkpoint_id: str) -> str:
        """状态检查点 Key"""
        return self._build("state", user_id, checkpoint_id)

    def state_current(self, user_id: str) -> str:
        """当前状态 Key"""
        return self._build("state", user_id, "current")


# ============================================================================
# 内存降级客户端（Redis 不可用时的进程内透明兜底实现）
# ============================================================================


class _MemoryPipeline:
    """内存客户端的 Pipeline 实现：缓冲命令，execute 时统一应用"""

    def __init__(self, client: "_MemoryRedisClient") -> None:
        self._client = client
        self._ops: list[tuple[str, tuple, dict]] = []

    def __getattr__(self, name: str):
        def _queue(*args, **kwargs):
            self._ops.append((name, args, kwargs))
            return self

        return _queue

    def reset(self) -> None:
        self._ops.clear()

    def execute(self) -> list:
        results: list = []
        for name, args, kwargs in self._ops:
            try:
                results.append(getattr(self._client, name)(*args, **kwargs))
            except Exception:
                results.append(None)
        self._ops.clear()
        return results


class _MemoryRedisClient:
    """Redis 命令的进程内模拟实现。

    与 redis.Redis(decode_responses=True) 的命令子集对齐，仅覆盖本项目
    实际使用的命令。当 Redis 不可用时作为透明兜底，保证记忆系统继续运行。
    内置 LRU 容量上限、TTL 过期与线程安全。
    """

    def __init__(self, max_entries: int = 10000) -> None:
        self._lock = threading.RLock()
        self._max_entries = max(1, max_entries)
        # key -> (type, payload, expire_at)；type: str | hash | zset
        self._store: OrderedDict[str, tuple[str, Any, float | None]] = OrderedDict()

    # ---- 内部工具 ---------------------------------------------------------

    @staticmethod
    def _now() -> float:
        return time.time()

    def _alive(self, key: str):
        """返回仍存活的 entry，过期则清除；不存在返回 None"""
        entry = self._store.get(key)
        if entry is None:
            return None
        _, _, expire_at = entry
        if expire_at is not None and expire_at <= self._now():
            self._store.pop(key)
            return None
        self._store.move_to_end(key)
        return entry

    def _evict_if_needed(self) -> None:
        while len(self._store) > self._max_entries:
            self._store.popitem(last=False)

    # ---- 连接类 -----------------------------------------------------------

    def ping(self) -> bool:
        return True

    def close(self) -> None:
        return None

    # ---- String -----------------------------------------------------------

    def get(self, key: str) -> str | None:
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'str':
                return None
            return entry[1]

    def get_status(self, key: str) -> tuple[bool, str | None]:
        """精确区分"存在"与"不存在"（String 场景返回 (found, value)）"""
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'str':
                return False, None
            return True, entry[1]

    def set(
        self,
        key: str,
        value: str,
        ex: int | None = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        with self._lock:
            entry = self._alive(key)
            exists = entry is not None and entry[0] == 'str'
            if nx and exists:
                return False
            if xx and not exists:
                return False
            expire_at = (self._now() + ex) if ex else (entry[2] if entry else None)
            self._store[key] = ('str', value, expire_at)
            self._evict_if_needed()
            return True

    def delete(self, *keys: str) -> int:
        with self._lock:
            removed = 0
            for key in keys:
                if self._store.pop(key, None) is not None:
                    removed += 1
            return removed

    def exists(self, key: str) -> int:
        with self._lock:
            return 1 if self._alive(key) is not None else 0

    def expire(self, key: str, ttl: int) -> int:
        with self._lock:
            entry = self._alive(key)
            if entry is None:
                return 0
            self._store[key] = (entry[0], entry[1], self._now() + ttl)
            return 1

    def ttl(self, key: str) -> int:
        with self._lock:
            entry = self._alive(key)
            if entry is None:
                return -2
            _, _, expire_at = entry
            if expire_at is None:
                return -1
            return int(expire_at - self._now())

    # ---- Hash ---------------------------------------------------------------

    def hset(self, key, field=None, value=None, mapping=None):
        with self._lock:
            entry = self._alive(key)
            data = dict(entry[1]) if entry is not None and entry[0] == 'hash' else {}
            added = 0
            if mapping:
                for f, v in mapping.items():
                    if f not in data:
                        added += 1
                    data[f] = v
            if field is not None:
                if field not in data:
                    added += 1
                data[field] = value
            self._store[key] = ('hash', data, entry[2] if entry else None)
            self._evict_if_needed()
            return added

    def hget(self, key, field):
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'hash':
                return None
            return entry[1].get(field)

    def hgetall(self, key):
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'hash':
                return {}
            return dict(entry[1])

    def hdel(self, key, *fields):
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'hash':
                return 0
            data = entry[1]
            removed = 0
            for f in fields:
                if f in data:
                    del data[f]
                    removed += 1
            if removed and not data:
                self._store.pop(key)
            return removed

    def hexists(self, key, field):
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'hash':
                return 0
            return 1 if field in entry[1] else 0

    # ---- Sorted Set -----------------------------------------------------------

    def zadd(self, key, mapping):
        with self._lock:
            entry = self._alive(key)
            data = dict(entry[1]) if entry is not None and entry[0] == 'zset' else {}
            added = 0
            for member, score in mapping.items():
                if member not in data:
                    added += 1
                data[member] = float(score)
            self._store[key] = ('zset', data, entry[2] if entry else None)
            self._evict_if_needed()
            return added

    def zincrby(self, key, amount, member):
        with self._lock:
            entry = self._alive(key)
            data = dict(entry[1]) if entry is not None and entry[0] == 'zset' else {}
            new_score = float(data.get(member, 0.0)) + float(amount)
            data[member] = new_score
            self._store[key] = ('zset', data, entry[2] if entry else None)
            self._evict_if_needed()
            return new_score

    def zscore(self, key, member):
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'zset':
                return None
            return entry[1].get(member)

    def zrange(self, key, start, end, desc=False, withscores=False):
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'zset':
                return []
            items = sorted(entry[1].items(), key=lambda kv: kv[1], reverse=desc)
            # Redis 闭区间语义 [start, end]，负索引从 -1 起；转换为 Python 切片
            n = len(items)
            s = start if start >= 0 else max(n + start, 0)
            e = end + 1 if end >= 0 else n + end + 1
            sliced = items[s:e]
            if withscores:
                return [(m, sc) for m, sc in sliced]
            return [m for m, _ in sliced]

    def zrem(self, key, *members):
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'zset':
                return 0
            data = entry[1]
            removed = 0
            for m in members:
                if m in data:
                    del data[m]
                    removed += 1
            if removed and not data:
                self._store.pop(key)
            return removed

    def zremrangebyrank(self, key, start, end):
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'zset':
                return 0
            items = sorted(entry[1].items(), key=lambda kv: kv[1])
            n = len(items)
            s = start if start >= 0 else max(n + start, 0)
            e = end + 1 if end >= 0 else n + end + 1
            removed = 0
            data = entry[1]
            for m, _ in items[s:e]:
                if m in data:
                    del data[m]
                    removed += 1
            if removed and not data:
                self._store.pop(key)
            return removed

    def zcard(self, key):
        with self._lock:
            entry = self._alive(key)
            if entry is None or entry[0] != 'zset':
                return 0
            return len(entry[1])

    # ---- Counter -----------------------------------------------------------

    def incrby(self, key, amount=1):
        with self._lock:
            entry = self._alive(key)
            current = 0
            if entry is not None and entry[0] == 'str':
                try:
                    current = int(entry[1])
                except (TypeError, ValueError):
                    current = 0
            new_val = current + int(amount)
            self._store[key] = ('str', str(new_val), entry[2] if entry else None)
            self._evict_if_needed()
            return new_val

    def decrby(self, key, amount=1):
        return self.incrby(key, -int(amount))

    # ---- Scan -----------------------------------------------------------

    def scan_iter(self, match=None):
        with self._lock:
            keys = [k for k in list(self._store.keys()) if self._alive(k) is not None]
        if match:
            for k in keys:
                if fnmatch.fnmatch(k, match):
                    yield k
        else:
            for k in keys:
                yield k

    # ---- Pipeline / 回写 -----------------------------------------------------------

    def pipeline(self):
        return _MemoryPipeline(self)

    def flush_to(self, real_client, max_entries: int | None = None) -> int:
        """尽力将内存兜底数据回写到真实 Redis（恢复时调用），返回成功条数"""
        flushed = 0
        with self._lock:
            entries = list(self._store.items())
        for key, (typ, payload, expire_at) in entries:
            try:
                if typ == 'str':
                    real_client.set(key, payload)
                elif typ == 'hash':
                    if payload:
                        real_client.hset(key, mapping=dict(payload))
                elif typ == 'zset':
                    if payload:
                        real_client.zadd(key, {m: float(s) for m, s in payload.items()})
                if expire_at is not None:
                    real_client.expire(key, max(1, int(expire_at - self._now())))
                flushed += 1
                if max_entries is not None and flushed >= max_entries:
                    break
            except Exception:
                continue
        with self._lock:
            self._store.clear()
        return flushed


# ============================================================================
# Redis 适配器
# ============================================================================


class RedisAdapter:
    """
    Redis 适配器

    提供 Redis 连接管理和基础操作封装。

    特性：
    - 连接池管理
    - 健康检查
    - 断线重连
    - 操作重试
    - Key 命名工具集成

    使用示例：
    ```python
    from scripts.redis_adapter import RedisConfig, RedisAdapter

    # 初始化
    config = RedisConfig(host="localhost", port=6379)
    adapter = RedisAdapter(config)

    # 检查连接
    if adapter.is_available():
        # 基础操作
        adapter.set("test_key", "test_value", ttl=60)
        value = adapter.get("test_key")

        # Hash 操作
        adapter.hset("hash_key", "field1", "value1")
        data = adapter.hgetall("hash_key")

        # Sorted Set 操作
        adapter.zadd("sorted_key", {"member1": 100, "member2": 50})
        top_items = adapter.zrange_desc("sorted_key", 0, 9)

    # 上下文管理器
    with adapter.pipeline() as pipe:
        pipe.set("key1", "value1")
        pipe.set("key2", "value2")
        pipe.execute()
    ```
    """

    def __init__(
        self,
        config: RedisConfig,
        enable_memory_fallback: bool = True,
        memory_max_entries: int = 10000,
    ) -> None:
        """
        初始化 Redis 适配器

        Args:
            config: Redis 配置
            enable_memory_fallback: Redis 不可用时是否启用进程内内存兜底
            memory_max_entries: 内存兜底最大条目数（LRU 淘汰）
        """
        self._config = config
        self._client: Redis | None = None
        self._key_builder = RedisKeyBuilder(config.key_prefix)
        self._last_health_check: float = 0.0
        self._is_available = False

        # 并发安全：保护 client 引用切换与健康检查状态
        self._conn_lock = threading.RLock()

        # 内存降级（Redis 不可用时的透明兜底）
        self._fallback_enabled = enable_memory_fallback
        self._mem_client = _MemoryRedisClient(memory_max_entries)
        self._degraded = False
        self._last_recover_attempt: float = 0.0
        self._degraded_events = 0
        self.last_error: str | None = None
        self.stats: dict[str, int] = {
            'degraded_events': 0,
            'failed_ops': 0,
            'recoveries': 0,
        }

        # 尝试初始化连接；失败且启用兜底时直接进入降级模式
        if REDIS_AVAILABLE:
            if not self._connect():
                self._enter_degraded()
        else:
            self._is_available = False
            if self._fallback_enabled:
                self._enter_degraded()

    # -----------------------------------------------------------------------
    # 连接管理
    # -----------------------------------------------------------------------

    def _connect(self) -> bool:
        """
        建立 Redis 连接（内部方法，安全增强版）

        Returns:
            是否连接成功
        """
        if not REDIS_AVAILABLE:
            return False

        try:
            # 构建 Redis 连接参数
            redis_params = {
                'host': self._config.host,
                'port': self._config.port,
                'db': self._config.db,
                'max_connections': self._config.max_connections,
                'socket_timeout': self._config.socket_timeout,
                'socket_connect_timeout': self._config.socket_connect_timeout,
                'retry_on_timeout': self._config.retry_on_timeout,
                'decode_responses': True,
            }

            # 安全增强：密码认证
            if self._config.password:
                redis_params['password'] = self._config.password

            # 安全增强：SSL/TLS 加密
            if self._config.enable_ssl:
                ssl_config = {
                    'ssl': True,
                    'ssl_cert_reqs': self._config.ssl_cert_reqs,
                }
                if self._config.ssl_ca_certs:
                    ssl_config['ssl_ca_certs'] = self._config.ssl_ca_certs
                if self._config.ssl_keyfile:
                    ssl_config['ssl_keyfile'] = self._config.ssl_keyfile
                if self._config.ssl_certfile:
                    ssl_config['ssl_certfile'] = self._config.ssl_certfile
                redis_params.update(ssl_config)

            self._client = Redis(**redis_params)

            # 测试连接
            self._client.ping()
            self._is_available = True

            # 此前处于内存降级：尽力回写兜底数据后恢复正常
            if self._degraded:
                self._exit_degraded()
            return True

        except (RedisError, OSError) as e:
            self._client = None
            self._is_available = False
            self.last_error = str(e)
            return False

    def _ensure_connection(self) -> bool:
        """
        确保连接可用（内部方法）

        Redis 可用时返回 True；Redis 不可用但启用内存兜底时，切换到
        进程内内存客户端并返回 True（降级模式）；仅当既不可用且未启用
        兜底时返回 False。
        """
        with self._conn_lock:
            # 降级模式：按固定间隔尝试恢复真实连接
            if self._degraded:
                now = time.time()
                if now - self._last_recover_attempt > max(
                    self._config.health_check_interval, 5.0
                ):
                    self._last_recover_attempt = now
                    self._client = None
                    if self._connect():
                        return True  # _connect 内部已回写兜底数据并恢复
                    self._client = self._mem_client  # 恢复失败，继续内存兜底
                return True

            if self._client is None:
                if self._connect():
                    return True
                return self._enter_degraded()

            # 健康检查
            now = time.time()
            if now - self._last_health_check > self._config.health_check_interval:
                if not self._health_check():
                    # 健康检查失败：先尝试重连；仍失败则进入降级
                    if self._connect():
                        return True
                    return self._enter_degraded()

            return True

    def _enter_degraded(self) -> bool:
        """Redis 不可用时切换到进程内内存兜底（内部方法）"""
        if not self._fallback_enabled:
            self.last_error = self.last_error or 'redis_unavailable'
            return False
        self._degraded = True
        self._client = self._mem_client
        self._degraded_events += 1
        self.stats['degraded_events'] += 1
        if self._degraded_events == 1:
            logger.warning('Redis 不可用，已切换到进程内内存兜底模式')
        elif self._degraded_events % 50 == 0:
            logger.warning(
                '内存兜底模式持续运行: 累计降级事件 %d 次', self._degraded_events
            )
        return True

    def _exit_degraded(self) -> None:
        """Redis 恢复：尽力回写内存兜底数据，切回真实客户端（内部方法）"""
        self._degraded = False
        self._last_health_check = time.time()
        self._last_recover_attempt = time.time()
        self.stats['recoveries'] += 1
        mem_client = self._mem_client
        real_client = self._client
        if real_client is not None:
            try:
                flushed = mem_client.flush_to(real_client)
                if flushed:
                    logger.info('Redis 已恢复，回写内存兜底数据 %d 条', flushed)
            except Exception as exc:
                logger.warning('内存兜底数据回写失败: %s', exc)

    @property
    def is_degraded(self) -> bool:
        """当前是否处于内存兜底降级模式"""
        return self._degraded

    def get_health(self) -> dict:
        """
        返回连接健康快照（只读，不触发重连；供调用方区分"不存在"与"故障"）

        Returns:
            包含 available/degraded/last_error/stats 的字典
        """
        return {
            'available': bool(
                self._client is not None and not self._degraded and self._is_available
            ),
            'degraded': self._degraded,
            'last_error': self.last_error,
            'stats': dict(self.stats),
        }

    def get_with_status(self, key: str) -> tuple[bool, str | None]:
        """
        读取 String 值，并区分"不存在"与"存储故障"

        Returns:
            (found, value)
            - 正常模式: found=True 表示 key 存在，False 表示确实不存在
            - 降级模式: 结果来自内存兜底，结合 is_degraded 判断来源
            - 完全不可用: (False, None)，last_error 与 stats 已记录
        """
        if not self._ensure_connection() or self._client is None:
            self.stats['failed_ops'] += 1
            self.last_error = self.last_error or 'redis_unavailable'
            return False, None
        try:
            if self._degraded:
                return self._mem_client.get_status(key)
            value = self._client.get(key)
            return (value is not None), value
        except (RedisError, OSError) as e:
            self.last_error = str(e)
            self.stats['failed_ops'] += 1
            return False, None

    def _health_check(self) -> bool:
        """
        健康检查（内部方法）

        Returns:
            健康状态
        """
        if self._client is None:
            return False

        try:
            self._client.ping()
            self._last_health_check = time.time()
            self._is_available = True
            return True
        except (RedisError, OSError):
            self._is_available = False
            return False

    def is_available(self) -> bool:
        """
        检查 Redis 是否可用

        Returns:
            是否可用
        """
        return self._ensure_connection()

    def close(self) -> None:
        """关闭连接"""
        if self._client is not None:
            try:
                self._client.close()
            except RedisError:
                pass
            finally:
                self._client = None
                self._is_available = False

    # -----------------------------------------------------------------------
    # Key 构建器
    # -----------------------------------------------------------------------

    @property
    def keys(self) -> RedisKeyBuilder:
        """获取 Key 构建器"""
        return self._key_builder

    # -----------------------------------------------------------------------
    # 基础操作
    # -----------------------------------------------------------------------

    def get(self, key: str) -> str | None:
        """
        获取值

        Args:
            key: Key

        Returns:
            值，不存在返回 None
        """
        if not self._ensure_connection() or self._client is None:
            return None

        try:
            return self._client.get(key)
        except RedisError:
            return None

    def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        """
        设置值

        Args:
            key: Key
            value: 值
            ttl: 过期时间（秒）
            nx: 仅当 Key 不存在时设置
            xx: 仅当 Key 存在时设置

        Returns:
            是否成功
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            result = self._client.set(key, value, ex=ttl, nx=nx, xx=xx)
            return result is not False
        except RedisError:
            return False

    def delete(self, key: str) -> bool:
        """
        删除 Key

        Args:
            key: Key

        Returns:
            是否成功
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            self._client.delete(key)
            return True
        except RedisError:
            return False

    def exists(self, key: str) -> bool:
        """
        检查 Key 是否存在

        Args:
            key: Key

        Returns:
            是否存在
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            return self._client.exists(key) > 0
        except RedisError:
            return False

    def expire(self, key: str, ttl: int) -> bool:
        """
        设置过期时间

        Args:
            key: Key
            ttl: 过期时间（秒）

        Returns:
            是否成功
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            return self._client.expire(key, ttl)
        except RedisError:
            return False

    def ttl(self, key: str) -> int:
        """
        获取剩余过期时间

        Args:
            key: Key

        Returns:
            剩余秒数，-1 表示永不过期，-2 表示不存在
        """
        if not self._ensure_connection() or self._client is None:
            return -2

        try:
            return self._client.ttl(key)
        except RedisError:
            return -2

    # -----------------------------------------------------------------------
    # Hash 操作
    # -----------------------------------------------------------------------

    def hset(self, key: str, field: str, value: str) -> bool:
        """
        设置 Hash 字段

        Args:
            key: Key
            field: 字段名
            value: 值

        Returns:
            是否成功
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            self._client.hset(key, field, value)
            return True
        except RedisError:
            return False

    def hset_multi(self, key: str, mapping: dict[str, str]) -> bool:
        """
        批量设置 Hash 字段

        Args:
            key: Key
            mapping: 字段-值映射

        Returns:
            是否成功
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            self._client.hset(key, mapping=mapping)
            return True
        except RedisError:
            return False

    def hget(self, key: str, field: str) -> str | None:
        """
        获取 Hash 字段值

        Args:
            key: Key
            field: 字段名

        Returns:
            值，不存在返回 None
        """
        if not self._ensure_connection() or self._client is None:
            return None

        try:
            return self._client.hget(key, field)
        except RedisError:
            return None

    def hgetall(self, key: str) -> dict[str, str]:
        """
        获取 Hash 所有字段

        Args:
            key: Key

        Returns:
            字段-值映射
        """
        if not self._ensure_connection() or self._client is None:
            return {}

        try:
            result = self._client.hgetall(key)
            return result if result else {}
        except RedisError:
            return {}

    def hdel(self, key: str, field: str) -> bool:
        """
        删除 Hash 字段

        Args:
            key: Key
            field: 字段名

        Returns:
            是否成功
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            self._client.hdel(key, field)
            return True
        except RedisError:
            return False

    def hexists(self, key: str, field: str) -> bool:
        """
        检查 Hash 字段是否存在

        Args:
            key: Key
            field: 字段名

        Returns:
            是否存在
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            return self._client.hexists(key, field)
        except RedisError:
            return False

    # -----------------------------------------------------------------------
    # Sorted Set 操作
    # -----------------------------------------------------------------------

    def zadd(self, key: str, mapping: dict[str, float]) -> bool:
        """
        添加 Sorted Set 成员

        Args:
            key: Key
            mapping: 成员-分数映射

        Returns:
            是否成功
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            self._client.zadd(key, mapping)
            return True
        except RedisError:
            return False

    def zincrby(self, key: str, amount: float, member: str) -> float | None:
        """
        增加 Sorted Set 成员分数

        Args:
            key: Key
            amount: 增量
            member: 成员

        Returns:
            新分数，失败返回 None
        """
        if not self._ensure_connection() or self._client is None:
            return None

        try:
            return self._client.zincrby(key, amount, member)
        except RedisError:
            return None

    def zscore(self, key: str, member: str) -> float | None:
        """
        获取 Sorted Set 成员分数

        Args:
            key: Key
            member: 成员

        Returns:
            分数，不存在返回 None
        """
        if not self._ensure_connection() or self._client is None:
            return None

        try:
            return self._client.zscore(key, member)
        except RedisError:
            return None

    def zrange_desc(
        self,
        key: str,
        start: int = 0,
        end: int = -1,
        with_scores: bool = False,
    ) -> list[str] | list[tuple[str, float]]:
        """
        按分数降序获取 Sorted Set 成员

        Args:
            key: Key
            start: 起始位置
            end: 结束位置
            with_scores: 是否返回分数

        Returns:
            成员列表，或 (成员, 分数) 列表
        """
        if not self._ensure_connection() or self._client is None:
            return []

        try:
            result = self._client.zrange(
                key, start, end, desc=True, withscores=with_scores
            )
            return result if result else []
        except RedisError:
            return []

    def zrange_asc(
        self,
        key: str,
        start: int = 0,
        end: int = -1,
        with_scores: bool = False,
    ) -> list[str] | list[tuple[str, float]]:
        """
        按分数升序获取 Sorted Set 成员

        Args:
            key: Key
            start: 起始位置
            end: 结束位置
            with_scores: 是否返回分数

        Returns:
            成员列表，或 (成员, 分数) 列表
        """
        if not self._ensure_connection() or self._client is None:
            return []

        try:
            result = self._client.zrange(
                key, start, end, desc=False, withscores=with_scores
            )
            return result if result else []
        except RedisError:
            return []

    def zrem(self, key: str, member: str) -> bool:
        """
        删除 Sorted Set 成员

        Args:
            key: Key
            member: 成员

        Returns:
            是否成功
        """
        if not self._ensure_connection() or self._client is None:
            return False

        try:
            self._client.zrem(key, member)
            return True
        except RedisError:
            return False

    def zremrangebyrank(self, key: str, start: int, end: int) -> int:
        """
        按排名范围删除 Sorted Set 成员

        Args:
            key: Key
            start: 起始排名
            end: 结束排名

        Returns:
            删除的数量
        """
        if not self._ensure_connection() or self._client is None:
            return 0

        try:
            return self._client.zremrangebyrank(key, start, end)
        except RedisError:
            return 0

    def zcard(self, key: str) -> int:
        """
        获取 Sorted Set 成员数量

        Args:
            key: Key

        Returns:
            成员数量
        """
        if not self._ensure_connection() or self._client is None:
            return 0

        try:
            return self._client.zcard(key)
        except RedisError:
            return 0

    # -----------------------------------------------------------------------
    # 计数器操作
    # -----------------------------------------------------------------------

    def incr(self, key: str, amount: int = 1) -> int | None:
        """
        增加计数器

        Args:
            key: Key
            amount: 增量

        Returns:
            新值，失败返回 None
        """
        if not self._ensure_connection() or self._client is None:
            return None

        try:
            return self._client.incrby(key, amount)
        except RedisError:
            return None

    def decr(self, key: str, amount: int = 1) -> int | None:
        """
        减少计数器

        Args:
            key: Key
            amount: 减量

        Returns:
            新值，失败返回 None
        """
        if not self._ensure_connection() or self._client is None:
            return None

        try:
            return self._client.decrby(key, amount)
        except RedisError:
            return None

    # -----------------------------------------------------------------------
    # Pipeline
    # -----------------------------------------------------------------------

    @contextmanager
    def pipeline(self):
        """
        获取 Pipeline 上下文管理器

        使用示例：
        ```python
        with adapter.pipeline() as pipe:
            pipe.set("key1", "value1")
            pipe.set("key2", "value2")
            pipe.execute()
        ```
        """
        if not self._ensure_connection() or self._client is None:
            yield None
            return

        pipe = self._client.pipeline()
        try:
            yield pipe
        finally:
            try:
                pipe.reset()
            except RedisError:
                pass

    # -----------------------------------------------------------------------
    # 批量操作
    # -----------------------------------------------------------------------

    def delete_pattern(self, pattern: str) -> int:
        """
        按模式删除 Key

        注意：生产环境慎用，SCAN 可能阻塞

        Args:
            pattern: Key 模式（如 "memory:short:user123:*"）

        Returns:
            删除的数量
        """
        if not self._ensure_connection() or self._client is None:
            return 0

        try:
            keys = []
            for key in self._client.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                return self._client.delete(*keys)
            return 0
        except RedisError:
            return 0


# ============================================================================
# 工厂函数
# ============================================================================


def create_redis_adapter(
    host: str = "localhost",
    port: int = 6379,
    password: str | None = None,
    db: int = 0,
    key_prefix: str = "memory",
) -> RedisAdapter:
    """
    创建 Redis 适配器

    Args:
        host: Redis 主机地址
        port: Redis 端口
        password: Redis 密码
        db: Redis 数据库编号
        key_prefix: Key 前缀

    Returns:
        RedisAdapter 实例
    """
    config = RedisConfig(
        host=host,
        port=port,
        password=password,
        db=db,
        key_prefix=key_prefix,
    )
    return RedisAdapter(config)


# ============================================================================
# 导出
# ============================================================================

__all__ = [
    "REDIS_AVAILABLE",
    "RedisConfig",
    "RedisKeyBuilder",
    "RedisAdapter",
    "create_redis_adapter",
]
