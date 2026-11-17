"""
搜索结果缓存与历史记录（F1-1）
==============================
V1.2 新增

问题背景：
    V1.1 没有任何缓存，同一关键词重复搜索会再次向所有引擎发起真实请求，
    既浪费流量，也增加被引擎限流的概率，且无法回看此前搜过什么。

设计要点：
    - SQLite 单文件存储，跨进程共享，与更新检查缓存分离互不影响
    - 缓存键包含 查询词 + 引擎组合 + 隐私模式 + 结果数，避免串味
    - TTL 默认 1 小时，可配置；--no-cache 可绕过
    - 容量上限默认 50MB，超限按最近最少使用淘汰（死规则 10：不拖累设备）
    - 历史记录与缓存分表，清空缓存不影响历史
    - 任何异常均静默降级为"无缓存"，绝不影响搜索主流程
"""

import hashlib
import json
import os
import sqlite3
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence

sys.dont_write_bytecode = True

DEFAULT_CACHE_PATH = os.path.expanduser("~/.workbuddy/output/.privacy-search-cache.db")
DEFAULT_TTL_SECONDS = 3600          # 1 小时
DEFAULT_MAX_SIZE_MB = 50            # 容量上限
DEFAULT_HISTORY_LIMIT = 500         # 历史保留条数


# ============================================================
# 缓存键
# ============================================================

def make_cache_key(
    query: str,
    engines: Sequence[str],
    privacy_mode: str,
    num: int,
) -> str:
    """
    生成缓存键

    引擎顺序不影响结果集合，故排序后参与计算，
    使 "baidu,bing" 与 "bing,baidu" 命中同一条缓存。
    """
    raw = "|".join([
        (query or "").strip().lower(),
        ",".join(sorted(e.strip().lower() for e in engines if e)),
        (privacy_mode or "normal").lower(),
        str(num),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


# ============================================================
# 缓存实现
# ============================================================

@dataclass
class CacheStats:
    """缓存统计信息"""
    entries: int = 0
    size_bytes: int = 0
    history_count: int = 0

    @property
    def size_mb(self) -> float:
        return round(self.size_bytes / (1024 * 1024), 2)


class SearchCache:
    """
    搜索结果缓存

    所有方法在异常时静默失败，保证缓存故障不会中断搜索。

    TTL 语义：
        ttl > 0   缓存该秒数后过期
        ttl <= 0  视为不缓存（等同于 enabled=false）
    早期实现把 0 当作「永不过期」，与用户直觉相反——把有效期设为 0
    却得到永久缓存，容易导致隐私数据长期滞留，因此改为不缓存。
    """

    def __init__(
        self,
        db_path: str = DEFAULT_CACHE_PATH,
        ttl: int = DEFAULT_TTL_SECONDS,
        max_size_mb: int = DEFAULT_MAX_SIZE_MB,
        enabled: bool = True,
    ):
        self.db_path = db_path
        self.ttl = max(0, ttl)
        self.max_size_mb = max(1, max_size_mb)
        # ttl 为 0 等同于关闭缓存
        self.enabled = bool(enabled) and self.ttl > 0
        self._available = False
        if self.enabled:
            self._init_db()

    def close(self) -> None:
        """
        释放缓存资源

        当前实现为每次操作独立连接、用完即关，故此处无需真正关闭连接。
        保留该方法是为了让调用方（含测试）可以显式表达生命周期结束，
        日后若改为长连接池也不必修改调用侧。
        """
        self._available = False

    # ---------- 基础设施 ----------

    def _connect(self) -> Optional[sqlite3.Connection]:
        """
        建立连接，任何失败都返回 None

        除 sqlite3.Error 外还需拦截 ValueError 与 OSError：
        路径含空字符等非法内容时 sqlite3.connect 抛的是 ValueError，
        缓存属于可选加速功能，绝不能因此中断搜索主流程。
        """
        try:
            conn = sqlite3.connect(self.db_path, timeout=5)
            conn.row_factory = sqlite3.Row
            return conn
        except (sqlite3.Error, ValueError, OSError):
            return None

    def _init_db(self) -> None:
        """建库建表，失败则关闭缓存功能"""
        try:
            parent = os.path.dirname(self.db_path)
            if parent:
                os.makedirs(parent, exist_ok=True)
        except (OSError, ValueError):
            # ValueError 对应路径含空字符等非法形式
            self._available = False
            return

        conn = self._connect()
        if conn is None:
            self._available = False
            return

        try:
            with conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS search_cache (
                        key         TEXT PRIMARY KEY,
                        query       TEXT NOT NULL,
                        engines     TEXT NOT NULL,
                        privacy     TEXT NOT NULL,
                        payload     TEXT NOT NULL,
                        created_at  REAL NOT NULL,
                        accessed_at REAL NOT NULL,
                        hits        INTEGER DEFAULT 0
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS search_history (
                        id          INTEGER PRIMARY KEY AUTOINCREMENT,
                        query       TEXT NOT NULL,
                        engines     TEXT NOT NULL,
                        privacy     TEXT NOT NULL,
                        result_count INTEGER DEFAULT 0,
                        elapsed     REAL DEFAULT 0,
                        created_at  REAL NOT NULL
                    )
                """)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS engine_stats (
                        engine      TEXT PRIMARY KEY,
                        success     INTEGER DEFAULT 0,
                        failure     INTEGER DEFAULT 0,
                        last_used   REAL DEFAULT 0
                    )
                """)
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_cache_accessed ON search_cache(accessed_at)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_history_created ON search_history(created_at)"
                )
            self._available = True
        except sqlite3.Error:
            self._available = False
        finally:
            conn.close()

    @property
    def available(self) -> bool:
        """缓存是否可用"""
        return self.enabled and self._available

    # ---------- 读写 ----------

    def get(self, key: str) -> Optional[List[Dict[str, Any]]]:
        """
        读取缓存

        Returns:
            结果列表；未命中或已过期返回 None
        """
        if not self.available:
            return None

        conn = self._connect()
        if conn is None:
            return None

        try:
            row = conn.execute(
                "SELECT payload, created_at FROM search_cache WHERE key = ?", (key,)
            ).fetchone()
            if not row:
                return None

            # 过期判定
            if self.ttl > 0 and (time.time() - row["created_at"]) > self.ttl:
                with conn:
                    conn.execute("DELETE FROM search_cache WHERE key = ?", (key,))
                return None

            with conn:
                conn.execute(
                    "UPDATE search_cache SET accessed_at = ?, hits = hits + 1 WHERE key = ?",
                    (time.time(), key),
                )
            return json.loads(row["payload"])
        except (sqlite3.Error, ValueError, TypeError):
            return None
        finally:
            conn.close()

    def set(
        self,
        key: str,
        query: str,
        engines: Sequence[str],
        privacy_mode: str,
        results: List[Dict[str, Any]],
    ) -> bool:
        """写入缓存，返回是否成功"""
        if not self.available:
            return False

        conn = self._connect()
        if conn is None:
            return False

        try:
            now = time.time()
            with conn:
                conn.execute(
                    """INSERT OR REPLACE INTO search_cache
                       (key, query, engines, privacy, payload, created_at, accessed_at, hits)
                       VALUES (?, ?, ?, ?, ?, ?, ?, 0)""",
                    (
                        key,
                        query,
                        ",".join(engines),
                        privacy_mode,
                        json.dumps(results, ensure_ascii=False),
                        now,
                        now,
                    ),
                )
            self._enforce_size_limit()
            return True
        except (sqlite3.Error, TypeError, ValueError):
            return False
        finally:
            conn.close()

    # ---------- 容量控制 ----------

    def _enforce_size_limit(self) -> None:
        """
        容量超限时按最近最少访问淘汰

        每次淘汰约四分之一条目，避免频繁触发。
        """
        try:
            if not os.path.exists(self.db_path):
                return
            size_mb = os.path.getsize(self.db_path) / (1024 * 1024)
            if size_mb <= self.max_size_mb:
                return
        except OSError:
            return

        conn = self._connect()
        if conn is None:
            return
        try:
            total = conn.execute("SELECT COUNT(*) AS c FROM search_cache").fetchone()["c"]
            if total <= 1:
                return
            evict = max(1, total // 4)
            with conn:
                conn.execute(
                    """DELETE FROM search_cache WHERE key IN (
                           SELECT key FROM search_cache ORDER BY accessed_at ASC LIMIT ?
                       )""",
                    (evict,),
                )
            # VACUUM 不能在事务内执行，必须等上面的 with 块提交后单独运行，
            # 否则整个淘汰操作会因 OperationalError 回滚，容量上限形同虚设
            self._vacuum(conn)
        except sqlite3.Error:
            pass
        finally:
            conn.close()

    @staticmethod
    def _vacuum(conn: sqlite3.Connection) -> None:
        """在事务之外执行 VACUUM，失败不影响已提交的删除"""
        try:
            conn.isolation_level = None      # 切换为自动提交
            conn.execute("VACUUM")
        except sqlite3.Error:
            pass
        finally:
            conn.isolation_level = ""        # 还原默认事务行为

    def purge_expired(self) -> int:
        """清理过期条目，返回清理数量"""
        if not self.available or self.ttl <= 0:
            return 0
        conn = self._connect()
        if conn is None:
            return 0
        try:
            cutoff = time.time() - self.ttl
            with conn:
                cur = conn.execute("DELETE FROM search_cache WHERE created_at < ?", (cutoff,))
                return cur.rowcount or 0
        except sqlite3.Error:
            return 0
        finally:
            conn.close()

    def clear(self) -> bool:
        """清空全部缓存（不影响历史记录）"""
        if not self.available:
            return False
        conn = self._connect()
        if conn is None:
            return False
        try:
            with conn:
                conn.execute("DELETE FROM search_cache")
            # VACUUM 须在事务外执行，此前写在 with 块内导致整个清空被回滚，
            # --clear-cache 表面返回失败且缓存实际未被清除
            self._vacuum(conn)
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()

    # ---------- 历史记录 ----------

    def add_history(
        self,
        query: str,
        engines: Sequence[str],
        privacy_mode: str,
        result_count: int,
        elapsed: float,
    ) -> bool:
        """记录一次搜索，并按上限裁剪旧记录"""
        if not self.available:
            return False
        conn = self._connect()
        if conn is None:
            return False
        try:
            with conn:
                conn.execute(
                    """INSERT INTO search_history
                       (query, engines, privacy, result_count, elapsed, created_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (query, ",".join(engines), privacy_mode, result_count, elapsed, time.time()),
                )
                conn.execute(
                    """DELETE FROM search_history WHERE id NOT IN (
                           SELECT id FROM search_history ORDER BY created_at DESC LIMIT ?
                       )""",
                    (DEFAULT_HISTORY_LIMIT,),
                )
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()

    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """读取最近的搜索历史"""
        if not self.available:
            return []
        conn = self._connect()
        if conn is None:
            return []
        try:
            rows = conn.execute(
                """SELECT query, engines, privacy, result_count, elapsed, created_at
                   FROM search_history ORDER BY created_at DESC LIMIT ?""",
                (max(1, limit),),
            ).fetchall()
            return [
                {
                    "query": r["query"],
                    "engines": r["engines"],
                    "privacy": r["privacy"],
                    "result_count": r["result_count"],
                    "elapsed": round(r["elapsed"], 2),
                    "time": datetime.fromtimestamp(r["created_at"]).strftime("%Y-%m-%d %H:%M:%S"),
                }
                for r in rows
            ]
        except (sqlite3.Error, ValueError, OSError):
            return []
        finally:
            conn.close()

    def clear_history(self) -> bool:
        """清空搜索历史"""
        if not self.available:
            return False
        conn = self._connect()
        if conn is None:
            return False
        try:
            with conn:
                conn.execute("DELETE FROM search_history")
            return True
        except sqlite3.Error:
            return False
        finally:
            conn.close()

    # ---------- 引擎统计（降级策略动态化） ----------

    def record_engine_result(self, engine: str, success: bool) -> None:
        """
        记录引擎成功/失败次数，用于动态降级选择

        幂等：引擎不存在时自动初始化
        """
        if not self.available:
            return
        conn = self._connect()
        if conn is None:
            return
        try:
            col = "success" if success else "failure"
            with conn:
                conn.execute(
                    f"""INSERT INTO engine_stats (engine, {col}, last_used)
                       VALUES (?, 1, ?)
                       ON CONFLICT(engine) DO UPDATE SET
                           {col} = {col} + 1,
                           last_used = excluded.last_used""",
                    (engine, time.time()),
                )
        except sqlite3.Error:
            pass
        finally:
            conn.close()

    def get_engine_success_rate(self, engine: str) -> float:
        """
        获取引擎成功率（0.0~1.0）

        从未使用时返回 0.5（中性值），避免新引擎被低估或高估
        """
        if not self.available:
            return 0.5
        conn = self._connect()
        if conn is None:
            return 0.5
        try:
            row = conn.execute(
                "SELECT success, failure FROM engine_stats WHERE engine = ?",
                (engine,),
            ).fetchone()
            if not row:
                return 0.5
            total = (row["success"] or 0) + (row["failure"] or 0)
            if total == 0:
                return 0.5
            return (row["success"] or 0) / total
        except sqlite3.Error:
            return 0.5
        finally:
            conn.close()

    def rank_engines_by_success(self, engines: Sequence[str]) -> List[str]:
        """
        按成功率降序排列引擎列表

        成功率相同时保持原始顺序，稳定排序
        """
        return sorted(
            engines,
            key=lambda e: self.get_engine_success_rate(e),
            reverse=True,
        )

    def stats(self) -> CacheStats:
        """获取缓存统计"""
        st = CacheStats()
        if not self.available:
            return st
        conn = self._connect()
        if conn is None:
            return st
        try:
            st.entries = conn.execute("SELECT COUNT(*) AS c FROM search_cache").fetchone()["c"]
            st.history_count = conn.execute("SELECT COUNT(*) AS c FROM search_history").fetchone()["c"]
            st.size_bytes = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        except (sqlite3.Error, OSError):
            pass
        finally:
            conn.close()
        return st


def build_cache_from_config(config: Dict[str, Any]) -> SearchCache:
    """
    依据配置构造缓存实例

    配置示例：
        cache:
          enabled: true
          ttl_seconds: 3600
          max_size_mb: 50
    """
    cfg = (config or {}).get("cache", {}) or {}
    return SearchCache(
        db_path=os.path.expanduser(cfg.get("path", DEFAULT_CACHE_PATH)),
        ttl=int(cfg.get("ttl_seconds", DEFAULT_TTL_SECONDS)),
        max_size_mb=int(cfg.get("max_size_mb", DEFAULT_MAX_SIZE_MB)),
        enabled=bool(cfg.get("enabled", True)),
    )
