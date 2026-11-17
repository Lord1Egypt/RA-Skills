#!/usr/bin/env python3
"""engine_lifecycle.py — Infoseek 搜索引擎全生命周期管理（v1.0.1 评估升级 P0/P1/P2/P3）

上轮「搜索引擎全生命周期评估」结论：搜索链为「静态配置 + 静态配额保护 + 超时降级」，
三维动态管理缺失 —— 新鲜度/免费额度/能力范围。本模块补齐引擎层动态管理：

- **健康状态机 (P0)**：连续失败计数 → 临时降权/禁用；错误类型分类
  （timeout / network / quota / forbidden / parse / unknown）
- **配额动态追踪 (P1)**：解析 429 / quota_exceeded / 401 / 403，
  标记额度耗尽 + 推算重置时刻；reserve_pool 自动剔除耗尽引擎
- **能力感知路由 (P2)**：get_active() 基于健康 + 配额筛选可用引擎，
  search_v3 选层时跳过被禁用/降权引擎
- **新鲜度动态管理 (P3)**：
  - P3.1 配额重置自动恢复：到重置时刻自动清零 quota_exhausted 标志（避免 status 永久陈旧
    + 修复「日/时额度引擎被误用『下月1日』估算而白白禁用 30 天」的 bug）；支持 monthly/daily/
    hourly/fixed 重置模式（INFOSEEK_ENGINE_QUOTA_RESET）
  - P3.2 上下线/存活恢复：auth_broken 在启用自动恢复（INFOSEEK_ENGINE_AUTH_RECOVER_SECONDS>0）
    且冷却期满后自动清零；访问前经 reconcile() 自愈（不主动打网络，靠后续 success 自然恢复）
  - P3.3 API 漂移检测：成功响应抽取 response_signature，连续 N 次不一致置 api_changed 告警
    （不影响禁用判定，默认关闭 INFOSEEK_ENGINE_API_DRIFT）
  - P3.4 新鲜度 TTL/对账/CLI：状态过期 TTL、reconcile_all()、engine-reconcile / engine-probe 子命令

零依赖（仅 stdlib），状态持久化到 engine_state.json（复用 INFOSEEK_DATA_DIR）。
单机/单进程内聚合；跨进程共享同一 JSON 文件（粗粒度最终一致，足够本 skill 场景）。
"""

import calendar
import hashlib
import json
import os
import threading
import time
from pathlib import Path

# ── 错误分类常量 ──
ERR_NONE = "none"
ERR_TIMEOUT = "timeout"
ERR_NETWORK = "network"
ERR_QUOTA = "quota"        # 429 / quota_exceeded / rate limit
ERR_FORBIDDEN = "forbidden"  # 401 / 403 / auth 失效
ERR_PARSE = "parse"        # 404 / 响应解析失败
ERR_UNKNOWN = "unknown"

# ── 可调阈值（env 覆盖）──
_FAIL_THRESHOLD = int(os.environ.get("INFOSEEK_ENGINE_FAIL_THRESHOLD", "3"))
_DISABLE_SECONDS = int(os.environ.get("INFOSEEK_ENGINE_DISABLE_SECONDS", "600"))
# 配额耗尽默认禁用时长（覆盖到下月 1 日 00:00 UTC，或 Retry-After）
_AUTH_BROKEN_STICKY = os.environ.get("INFOSEEK_ENGINE_AUTH_STICKY", "1") == "1"
# P3.1 配额重置模式：monthly(默认,下月1日UTC) / daily(次日0点本地) / hourly(整点) / fixed:<ISO>
_QUOTA_RESET_MODE = os.environ.get("INFOSEEK_ENGINE_QUOTA_RESET", "monthly").lower()
# P3.2 认证自动恢复冷却（秒）；0=禁用（保持 sticky 语义，需手动 engine-reset）
_AUTH_RECOVER_SECONDS = int(os.environ.get("INFOSEEK_ENGINE_AUTH_RECOVER_SECONDS", "0"))
# P3.3 API 漂移检测（默认关闭）
_API_DRIFT = os.environ.get("INFOSEEK_ENGINE_API_DRIFT", "0") == "1"
_API_DRIFT_N = int(os.environ.get("INFOSEEK_ENGINE_API_DRIFT_N", "3"))
# P3.4 状态新鲜度 TTL（秒）：状态距上次对账超过此值视为过期（reconcile 时强制重新评估）
_FRESHNESS_TTL = int(os.environ.get("INFOSEEK_ENGINE_FRESHNESS_TTL", "86400"))


def _state_path() -> Path:
    base = Path(os.environ.get("INFOSEEK_DATA_DIR", Path.home() / ".infoseek"))
    base.mkdir(parents=True, exist_ok=True)
    return base / "engine_state.json"


def _blank_state() -> dict:
    return {
        "fail_count": 0,
        "last_error": ERR_NONE,
        "last_failure": 0,
        "last_success": 0,
        "quota_exhausted": False,
        "quota_reset_at": 0,
        "auth_broken": False,
        "total_calls": 0,
        "total_failures": 0,
        # ── P3 新鲜度字段 ──
        "last_reconcile": 0,
        "last_probe_at": 0,
        "api_changed": False,
        "api_changed_at": 0,
        "response_signature": "",
        "drift_count": 0,
        "freshness_ttl": 0,
    }


def _quota_reset_epoch(e, mode=None) -> int:
    """推算配额重置时刻（P3.1）。优先级：Retry-After > 模式规则。

    mode: monthly(默认,下月1日UTC) / daily(次日0点本地) / hourly(整点) / fixed:<ISO>
    """
    mode = (mode or _QUOTA_RESET_MODE).lower()
    now = time.time()
    # 1) Retry-After（秒）
    try:
        hdrs = getattr(e, "headers", None)
        if hdrs:
            ra = hdrs.get("Retry-After") if hasattr(hdrs, "get") else None
            if ra and str(ra).isdigit():
                return int(now) + int(ra)
    except Exception:
        pass
    # 2) 模式规则
    if mode == "daily":
        t = time.localtime(now + 86400)
        return int(time.mktime((t.tm_year, t.tm_mon, t.tm_mday, 0, 0, 0, 0, 0, -1)))
    if mode == "hourly":
        t = time.localtime(now)
        return int(time.mktime((t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour + 1, 0, 0, 0, 0, -1)))
    if mode.startswith("fixed:"):
        iso = mode[len("fixed:"):].strip()
        try:
            import datetime as _dt
            return int(_dt.datetime.fromisoformat(iso).timestamp())
        except Exception:
            pass  # 解析失败回退 monthly
    # 3) 默认 monthly：下月 1 日 00:00 UTC
    g = time.gmtime(now)
    if g.tm_mon == 12:
        y, m = g.tm_year + 1, 1
    else:
        y, m = g.tm_year, g.tm_mon + 1
    return calendar.timegm((y, m, 1, 0, 0, 0, 0, 0, 0))


def _response_signature(result) -> str:
    """从成功响应抽取稳定签名（P3.3）：取首个结果项顶层 key 集合的哈希。"""
    if result is None:
        return ""
    items = result if isinstance(result, list) else (
        result.get("results") if isinstance(result, dict) else None)
    if not items:
        return ""
    first = items[0] if isinstance(items, list) else items
    if not isinstance(first, dict):
        return ""
    keys = sorted(first.keys())
    if not keys:
        return ""
    return hashlib.sha256(",".join(keys).encode("utf-8")).hexdigest()[:16]


class EngineLifecycle:
    """单引擎生命周期状态机（线程安全，持久化到 engine_state.json）。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._engines: dict = {}
        self._loaded = False

    # ── 持久化 ──
    def _ensure_loaded(self):
        if self._loaded:
            return
        with self._lock:
            if self._loaded:
                return
            try:
                p = _state_path()
                if p.exists():
                    self._engines = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                self._engines = {}
            self._loaded = True

    def _persist(self):
        try:
            p = _state_path()
            p.write_text(json.dumps(self._engines, ensure_ascii=False, indent=2),
                         encoding="utf-8")
        except Exception:
            pass

    # ── 错误分类 ──
    @staticmethod
    def classify(e) -> str:
        if e is None:
            return ERR_UNKNOWN
        code = getattr(e, "code", None)
        msg = str(e).lower()
        if code == 429 or "429" in msg or "quota" in msg or "rate limit" in msg \
                or "too many requests" in msg:
            return ERR_QUOTA
        if code in (401, 403) or "401" in msg or "403" in msg \
                or "unauthorized" in msg or "forbidden" in msg or "api key" in msg \
                or "auth" in msg:
            return ERR_FORBIDDEN
        if code in (404, 410) or "404" in msg or "410" in msg:
            return ERR_PARSE
        if isinstance(e, TimeoutError) or "timed out" in msg or "timeout" in msg:
            return ERR_TIMEOUT
        if "connection" in msg or "urlopen" in msg or "urllib" in msg \
                or "getaddrinfo" in msg or "name or service" in msg \
                or "connection refused" in msg:
            return ERR_NETWORK
        return ERR_UNKNOWN

    # ── 记录 ──
    def record_success(self, name: str, result=None):
        self._ensure_loaded()  # 先加载，保证内存态不被子进程/后续读取冲掉
        with self._lock:
            st = self._engines.setdefault(name, _blank_state())
            was_failing = st["fail_count"] > 0
            st["fail_count"] = 0
            st["last_error"] = ERR_NONE
            st["last_success"] = int(time.time())
            st["total_calls"] += 1
            dirty = was_failing
            # P3.3 API 漂移检测（默认关闭）
            if _API_DRIFT and result is not None:
                sig = _response_signature(result)
                if sig:
                    base = st.get("response_signature")
                    if not base:
                        st["response_signature"] = sig
                        st["drift_count"] = 0
                        dirty = True
                    elif sig != base:
                        st["drift_count"] = st.get("drift_count", 0) + 1
                        if st["drift_count"] >= _API_DRIFT_N:
                            st["api_changed"] = True
                            st["api_changed_at"] = int(time.time())
                            st["response_signature"] = sig  # 稳定到新基线，避免反复触发
                            st["drift_count"] = 0
                        dirty = True
                    else:
                        if st.get("drift_count", 0) != 0:
                            st["drift_count"] = 0
                            dirty = True
            if dirty:
                self._persist()

    def record_failure(self, name: str, e=None):
        etype = self.classify(e) if e else ERR_UNKNOWN
        self._ensure_loaded()  # 先加载，保证内存态不被后续读取冲掉
        with self._lock:
            st = self._engines.setdefault(name, _blank_state())
            st["fail_count"] += 1
            st["last_error"] = etype
            st["last_failure"] = int(time.time())
            st["total_calls"] += 1
            st["total_failures"] += 1
            if etype == ERR_QUOTA:
                st["quota_exhausted"] = True
                st["quota_reset_at"] = _quota_reset_epoch(e)
            if etype == ERR_FORBIDDEN and _AUTH_BROKEN_STICKY:
                st["auth_broken"] = True
            self._persist()

    # ── 新鲜度对账 (P3.1 / P3.2 / P3.4) ──
    def reconcile(self, name: str) -> bool:
        """访问前自愈：到重置时刻清零配额/认证标记。返回是否发生状态变更。"""
        self._ensure_loaded()
        st = self._engines.get(name)
        if not st:
            return False
        now = time.time()
        changed = False
        with self._lock:
            # P3.1 配额重置自动恢复
            if st.get("quota_exhausted"):
                rat = st.get("quota_reset_at", 0)
                if rat and now >= rat:
                    st["quota_exhausted"] = False
                    st["quota_reset_at"] = 0
                    st["last_reconcile"] = int(now)
                    changed = True
            # P3.2 认证自动恢复（需启用 INFOSEEK_ENGINE_AUTH_RECOVER_SECONDS>0）
            if st.get("auth_broken") and _AUTH_RECOVER_SECONDS > 0:
                lf = st.get("last_failure", 0)
                if now - lf >= _AUTH_RECOVER_SECONDS:
                    st["auth_broken"] = False
                    st["last_reconcile"] = int(now)
                    changed = True
            if changed:
                self._persist()
        return changed

    def reconcile_all(self) -> int:
        """全量对账（engine-reconcile CLI）。返回发生变更的引擎数。"""
        self._ensure_loaded()
        changed = 0
        for name in list(self._engines.keys()):
            if self.reconcile(name):
                changed += 1
        return changed

    # ── 查询 ──
    def is_disabled(self, name: str) -> bool:
        self._ensure_loaded()
        st = self._engines.get(name)
        if not st:
            return False
        now = time.time()
        # 1) 连续失败临时禁用
        if st["fail_count"] >= _FAIL_THRESHOLD \
                and now - st["last_failure"] < _DISABLE_SECONDS:
            return True
        # 2) 配额耗尽且未到重置日
        if st.get("quota_exhausted"):
            rat = st.get("quota_reset_at", 0)
            if rat and now < rat:
                return True
            if not rat:  # 无明确重置时刻 → 持续禁用直到手动 reset
                return True
        # 3) 认证损坏（sticky，需手动 reset；或已启用自动恢复则 reconcile 处理）
        if st.get("auth_broken"):
            return True
        return False

    def get_active(self, engines: list) -> list:
        """过滤出可用引擎 [(name, fn), ...]。"""
        return [(n, f) for n, f in engines if not self.is_disabled(n)]

    def status(self) -> dict:
        self._ensure_loaded()
        return {n: dict(s) for n, s in self._engines.items()}

    def probe(self, name: str, fn=None) -> bool:
        """存活探测（engine-probe CLI / 轻量恢复）。fn 提供则实际调用一次。"""
        self._ensure_loaded()
        if fn is not None:
            try:
                fn("", 1)
                self.record_success(name)
                return True
            except Exception as e:
                self.record_failure(name, e)
                return False
        return not self.is_disabled(name)

    def reset(self, name: str = None):
        with self._lock:
            if name:
                self._engines.pop(name, None)
            else:
                self._engines = {}
            self._persist()


_INSTANCE = None


def get_lifecycle() -> EngineLifecycle:
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = EngineLifecycle()
    return _INSTANCE


def reset_instance():
    """测试辅助：丢弃单例（需在设置 INFOSEEK_DATA_DIR 后调用）。"""
    global _INSTANCE
    _INSTANCE = None
