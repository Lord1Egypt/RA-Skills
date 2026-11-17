"""KingDoc 配额管理器

v3.9.0 新增：API 配额与限流管理，保护测试与生产环境。

三件套：
1. SQLite 按天计数（对接测试环境 500 次/天限制）
2. 令牌桶限速（默认 5 req/s）
3. 429 指数退避 + 批量任务自动降并发削峰

附加能力：
- 配额看板展示剩余量与建议执行时段
- 硬件自适应（批量任务并发 ≤ hardware.py workers）
- 零第三方依赖（sqlite3 标准库）
- 零密钥可用（本地模式）
"""
from __future__ import annotations

import json
import math
import os
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


# 默认配置
DEFAULT_MAX_REQUESTS_PER_DAY = 500  # 测试环境限制
DEFAULT_TOKEN_BUCKET_RATE = 5.0    # 每秒 5 个请求
DEFAULT_TOKEN_BUCKET_BURST = 10    # 突发最多 10 个
DEFAULT_MAX_BACKOFF_RETRIES = 5    # 最大退避次数
DEFAULT_BACKOFF_BASE = 1.0         # 退避基数（秒）
DEFAULT_BACKOFF_MAX = 60.0         # 最大退避时间（秒）

# 配额阈值告警（v4.3.0 新增）：用量越级经 webhook 三通道推送
QUOTA_ALERT_THRESHOLDS = [
    ("warning", 0.80),   # 80% 警告
    ("critical", 0.95),  # 95% 严重
]
QUOTA_ALERT_EVENT_TYPE = "quota_alert"


class TokenBucket:
    """令牌桶限速器

    经典令牌桶算法：
    - 桶内令牌以固定速率生成
    - 每次请求消耗一个令牌
    - 桶满时令牌丢弃
    - 桶空时等待令牌生成
    """

    def __init__(self, rate: float = DEFAULT_TOKEN_BUCKET_RATE,
                 burst: int = DEFAULT_TOKEN_BUCKET_BURST):
        self.rate = rate
        self.burst = burst
        self.tokens = float(burst)
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.rate
        self.tokens = min(self.burst, self.tokens + new_tokens)
        self.last_refill = now

    def consume(self, tokens: int = 1, timeout: float = 30.0) -> Tuple[bool, float]:
        """尝试消耗令牌

        Args:
            tokens: 需要消耗的令牌数
            timeout: 最大等待时间（秒）

        Returns:
            (success, wait_time)
        """
        deadline = time.monotonic() + timeout
        while True:
            with self._lock:
                self._refill()
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return True, 0.0
                # 计算需要等待的时间
                wait = (tokens - self.tokens) / self.rate
            if time.monotonic() + wait > deadline:
                return False, wait
            time.sleep(min(wait, 0.1))

    def get_status(self) -> Dict:
        with self._lock:
            self._refill()
            return {
                "tokens": round(self.tokens, 2),
                "rate": self.rate,
                "burst": self.burst,
                "utilization": round(1.0 - self.tokens / self.burst, 2),
            }


class QuotaManager:
    """配额管理器

    统一管理 API 配额、令牌桶限速、429 退避。
    硬件自适应：批量任务并发自动降峰。
    """

    def __init__(self, db_path: str = "", max_requests_per_day: int = DEFAULT_MAX_REQUESTS_PER_DAY,
                 token_rate: float = DEFAULT_TOKEN_BUCKET_RATE,
                 token_burst: int = DEFAULT_TOKEN_BUCKET_BURST):
        # 数据库路径
        if not db_path:
            db_path = str(Path(__file__).resolve().parent.parent.parent / ".kingdoc_quota.db")
        self.db_path = db_path

        # 配额配置
        self.max_requests_per_day = max_requests_per_day

        # 令牌桶
        self.token_bucket = TokenBucket(rate=token_rate, burst=token_burst)

        # 硬件自适应参数
        self._workers = None
        self._batch_chunk = None

        # 初始化数据库
        self._init_db()

    def _init_db(self):
        """初始化 SQLite 数据库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quota_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    hour INTEGER NOT NULL,
                    endpoint TEXT NOT NULL,
                    status TEXT NOT NULL,
                    response_time_ms INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_quota_date_hour
                ON quota_log(date, hour)
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date TEXT PRIMARY KEY,
                    total_requests INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    error_429_count INTEGER DEFAULT 0,
                    error_other_count INTEGER DEFAULT 0,
                    avg_response_time_ms REAL DEFAULT 0.0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quota_alert_dedup (
                    date TEXT NOT NULL,
                    level TEXT NOT NULL,
                    alerted_at TEXT,
                    PRIMARY KEY (date, level)
                )
            """)
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _get_hardware_settings(self) -> Dict:
        """获取硬件自适应参数"""
        if self._workers is not None:
            return {"workers": self._workers, "batch_chunk": self._batch_chunk}
        try:
            from engine.hardware import get_recommended_settings
            settings = get_recommended_settings()
            self._workers = settings.get("workers", 4)
            self._batch_chunk = settings.get("batch_chunk", 200)
        except Exception:
            self._workers = 4
            self._batch_chunk = 200
        return {"workers": self._workers, "batch_chunk": self._batch_chunk}

    def _today(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def _current_hour(self) -> int:
        return datetime.now().hour

    def record_request(self, endpoint: str, status: str,
                       response_time_ms: int = 0) -> Dict:
        """记录一次 API 请求

        Args:
            endpoint: API 端点
            status: success / 429 / error
            response_time_ms: 响应时间（毫秒）

        Returns:
            {"success": bool, "daily_count": int, "remaining": int}
        """
        date = self._today()
        hour = self._current_hour()

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 记录请求日志
            cursor.execute(
                "INSERT INTO quota_log (date, hour, endpoint, status, response_time_ms) VALUES (?, ?, ?, ?, ?)",
                (date, hour, endpoint, status, response_time_ms)
            )

            # 更新日统计
            cursor.execute(
                "INSERT OR IGNORE INTO daily_stats (date, total_requests) VALUES (?, 0)",
                (date,)
            )
            cursor.execute(
                "UPDATE daily_stats SET total_requests = total_requests + 1, updated_at = CURRENT_TIMESTAMP WHERE date = ?",
                (date,)
            )
            if status == "success":
                cursor.execute(
                    "UPDATE daily_stats SET success_count = success_count + 1 WHERE date = ?",
                    (date,)
                )
            elif status == "429":
                cursor.execute(
                    "UPDATE daily_stats SET error_429_count = error_429_count + 1 WHERE date = ?",
                    (date,)
                )
            elif status == "error":
                cursor.execute(
                    "UPDATE daily_stats SET error_other_count = error_other_count + 1 WHERE date = ?",
                    (date,)
                )

            # 计算平均响应时间
            if response_time_ms > 0:
                cursor.execute(
                    "UPDATE daily_stats SET avg_response_time_ms = "
                    "(avg_response_time_ms * (total_requests - 1) + ?) / total_requests "
                    "WHERE date = ?",
                    (response_time_ms, date)
                )

            # 获取当日统计
            cursor.execute(
                "SELECT total_requests FROM daily_stats WHERE date = ?",
                (date,)
            )
            row = cursor.fetchone()
            daily_count = row[0] if row else 0

            conn.commit()
            conn.close()

            return {
                "success": True,
                "daily_count": daily_count,
                "remaining": max(0, self.max_requests_per_day - daily_count),
                "date": date,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "daily_count": 0,
                "remaining": self.max_requests_per_day,
            }

    def check_quota(self) -> Dict:
        """检查当前配额状态

        Returns:
            {
                "date": str,
                "daily_count": int,
                "daily_limit": int,
                "remaining": int,
                "usage_percent": float,
                "status": "ok" | "warning" | "exhausted",
                "suggestion": str
            }
        """
        date = self._today()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT total_requests FROM daily_stats WHERE date = ?",
                (date,)
            )
            row = cursor.fetchone()
            conn.close()

            daily_count = row[0] if row else 0
        except Exception:
            daily_count = 0

        remaining = max(0, self.max_requests_per_day - daily_count)
        usage = daily_count / self.max_requests_per_day if self.max_requests_per_day > 0 else 0

        if usage >= 1.0:
            status = "exhausted"
            suggestion = "配额已用尽，请明天再试或申请提额"
        elif usage >= 0.8:
            status = "warning"
            suggestion = f"配额使用 {usage:.0%}，建议减少批量操作或分批执行"
        else:
            status = "ok"
            suggestion = "配额充足"

        # 阈值告警（v4.3.0）：越 80% / 95% 经 webhook 三通道推送，按天+级去重幂等
        alerts = self._maybe_alert(usage)

        return {
            "date": date,
            "daily_count": daily_count,
            "daily_limit": self.max_requests_per_day,
            "remaining": remaining,
            "usage_percent": round(usage, 3),
            "status": status,
            "suggestion": suggestion,
            "alerts": alerts,
        }

    def _maybe_alert(self, usage: float) -> List[Dict]:
        """用量越阈值时触发 webhook 告警（按天+级别幂等去重）。"""
        sent: List[Dict] = []
        triggered_level = None
        for level, thr in QUOTA_ALERT_THRESHOLDS:
            if usage >= thr:
                triggered_level = level
        if triggered_level is None:
            return sent
        date = self._today()
        if self._already_alerted(date, triggered_level):
            return sent
        try:
            payload = {
                "event_type": QUOTA_ALERT_EVENT_TYPE,
                "table_id": "system",
                "record_id": f"{date}:{triggered_level}",
                "level": triggered_level,
                "usage_percent": round(usage, 3),
                "daily_limit": self.max_requests_per_day,
            }
            from engine import webhook_center
            import hmac as _hmac
            import hashlib as _hl
            body = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
            secret = getattr(webhook_center, "DEFAULT_SIGNING_SECRET", "kingdoc_webhook_secret_v4")
            signature = _hmac.new(secret.encode(), body, _hl.sha256).hexdigest()
            result = webhook_center.process_event(payload, signature=signature)
            ok = result.get("success", False)
            self._mark_alerted(date, triggered_level)
            sent.append({
                "level": triggered_level,
                "usage_percent": round(usage, 3),
                "pushed": ok,
                "status": result.get("status", "n/a"),
            })
        except Exception:
            sent.append({"level": triggered_level, "usage_percent": round(usage, 3),
                         "pushed": False, "status": "error"})
        return sent

    def _already_alerted(self, date: str, level: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        try:
            row = conn.execute(
                "SELECT date FROM quota_alert_dedup WHERE date = ? AND level = ?",
                (date, level),
            ).fetchone()
            return row is not None
        finally:
            conn.close()

    def _mark_alerted(self, date: str, level: str) -> None:
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                "INSERT OR REPLACE INTO quota_alert_dedup (date, level, alerted_at) VALUES (?, ?, ?)",
                (date, level, datetime.now().isoformat()),
            )
            conn.commit()
        finally:
            conn.close()

    def get_hourly_distribution(self, date: str = "") -> Dict:
        """获取按小时分布的请求统计

        Args:
            date: 日期（默认今天）

        Returns:
            {"date": str, "hourly": [{hour, count, ...}], "peak_hour": int}
        """
        if not date:
            date = self._today()

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT hour, COUNT(*) as cnt, "
                "SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success, "
                "SUM(CASE WHEN status = '429' THEN 1 ELSE 0 END) as rate_limited "
                "FROM quota_log WHERE date = ? GROUP BY hour ORDER BY hour",
                (date,)
            )
            rows = cursor.fetchall()
            conn.close()

            hourly = []
            peak_hour = 0
            peak_count = 0
            for row in rows:
                entry = {
                    "hour": row[0],
                    "count": row[1],
                    "success": row[2],
                    "rate_limited": row[3],
                }
                hourly.append(entry)
                if row[1] > peak_count:
                    peak_count = row[1]
                    peak_hour = row[0]

            return {
                "date": date,
                "hourly": hourly,
                "peak_hour": peak_hour,
                "peak_count": peak_count,
            }
        except Exception:
            return {"date": date, "hourly": [], "peak_hour": 0, "peak_count": 0}

    def compute_backoff(self, attempt: int) -> float:
        """计算指数退避时间

        Args:
            attempt: 当前尝试次数（从 0 开始）

        Returns:
            等待时间（秒）
        """
        wait = DEFAULT_BACKOFF_BASE * (2 ** attempt)
        # 加随机抖动，避免惊群
        import random
        jitter = random.uniform(0, wait * 0.1)
        return min(wait + jitter, DEFAULT_BACKOFF_MAX)

    def wait_if_needed(self, timeout: float = 30.0) -> Dict:
        """令牌桶限速等待

        Args:
            timeout: 最大等待时间

        Returns:
            {"waited": bool, "wait_time": float}
        """
        success, wait = self.token_bucket.consume(tokens=1, timeout=timeout)
        return {"waited": not success, "wait_time": round(wait, 3)}

    def get_safe_batch_params(self, total_items: int) -> Dict:
        """计算安全的批量任务参数（硬件自适应削峰）

        Args:
            total_items: 总任务数

        Returns:
            {
                "workers": int,
                "batch_chunk": int,
                "estimated_seconds": float,
                "suggestion": str
            }
        """
        hw = self._get_hardware_settings()
        workers = hw["workers"]
        batch_chunk = hw["batch_chunk"]

        # 考虑令牌桶限速：每秒最多处理 rate 个
        rate = self.token_bucket.rate
        # 实际并发 = min(workers, int(rate))
        effective_workers = max(1, min(workers, int(rate)))

        # 计算预估时间
        batches = math.ceil(total_items / batch_chunk)
        estimated_seconds = batches / effective_workers

        # 削峰建议
        quota = self.check_quota()
        remaining = quota.get("remaining", 0)

        if total_items > remaining:
            suggestion = f"任务数({total_items})超过剩余配额({remaining})，建议分批或明日执行"
        elif total_items > remaining * 0.5:
            suggestion = f"任务数较多，建议分 {batches} 批执行，每批 {batch_chunk} 条"
        else:
            suggestion = f"可一次性执行，预计 {estimated_seconds:.1f} 秒完成"

        return {
            "workers": effective_workers,
            "batch_chunk": batch_chunk,
            "total_items": total_items,
            "batches": batches,
            "estimated_seconds": round(estimated_seconds, 1),
            "remaining_quota": remaining,
            "suggestion": suggestion,
        }

    def get_dashboard(self) -> Dict:
        """获取配额看板数据

        Returns:
            {
                "quota": {...},
                "token_bucket": {...},
                "hardware": {...},
                "hourly": {...},
                "recommendation": str
            }
        """
        quota = self.check_quota()
        token_status = self.token_bucket.get_status()
        hw = self._get_hardware_settings()
        hourly = self.get_hourly_distribution()

        # 生成建议
        if quota["status"] == "exhausted":
            recommendation = "配额已用尽，明日再试"
        elif quota["status"] == "warning":
            recommendation = "配额紧张，建议削峰执行：降低并发、分批处理"
        else:
            recommendation = "配额充足，可正常执行"

        return {
            "quota": quota,
            "token_bucket": token_status,
            "hardware": hw,
            "hourly": hourly,
            "recommendation": recommendation,
        }

    def reset_daily_stats(self, date: str = "") -> Dict:
        """重置指定日期的统计（用于测试或提额后）

        Args:
            date: 日期（默认今天）
        """
        if not date:
            date = self._today()

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM quota_log WHERE date = ?", (date,))
            cursor.execute("DELETE FROM daily_stats WHERE date = ?", (date,))
            conn.commit()
            conn.close()
            return {"success": True, "message": f"已重置 {date} 的配额统计"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def cleanup_old_logs(self, days: int = 30) -> Dict:
        """清理超过指定天数的日志

        Args:
            days: 保留天数
        """
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM quota_log WHERE date < ?", (cutoff,))
            deleted_log = cursor.rowcount
            cursor.execute("DELETE FROM daily_stats WHERE date < ?", (cutoff,))
            deleted_stats = cursor.rowcount
            conn.commit()
            conn.close()
            return {
                "success": True,
                "deleted_log_entries": deleted_log,
                "deleted_daily_stats": deleted_stats,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


def get_quota_manager(db_path: str = "") -> QuotaManager:
    """获取配额管理器实例"""
    return QuotaManager(db_path=db_path)


def check_quota(db_path: str = "") -> Dict:
    """便捷函数：检查配额"""
    mgr = QuotaManager(db_path=db_path)
    return mgr.check_quota()


def get_dashboard(db_path: str = "") -> Dict:
    """便捷函数：获取配额看板"""
    mgr = QuotaManager(db_path=db_path)
    return mgr.get_dashboard()


def get_safe_batch_params(total_items: int, db_path: str = "") -> Dict:
    """便捷函数：获取安全批量参数"""
    mgr = QuotaManager(db_path=db_path)
    return mgr.get_safe_batch_params(total_items)
