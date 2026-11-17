"""核心修复回归测试

覆盖历轮排查修复的全部缺陷点，防止回归：
- 未定义名称/重复方法覆盖/枚举成员缺失
- 内存降级模式与故障语义区分
- 并发锁
- 预取存储加载、上下文编排警告传播等
"""

import threading

import pytest


# ---------------------------------------------------------------------------
# 加密与密钥派生（曾因静态方法被实例方法覆盖而崩溃）
# ---------------------------------------------------------------------------


def test_key_derivation_static_call():
    from scripts.encryption import KeyManager

    key1, salt = KeyManager.derive_key_from_password("pw")
    assert len(key1) == 32 and len(salt) == 32
    key2, _ = KeyManager.derive_key_from_password("pw", salt)
    assert key1 == key2  # 确定性派生


def test_encrypt_roundtrip():
    from scripts.encryption import DataEncryptor, KeyManager

    km = KeyManager()
    kid, key = km.generate_key()
    km.set_key(kid, key)
    enc = DataEncryptor(key_manager=km)
    token = enc.encrypt("hello memory")
    assert enc.decrypt_to_string(token) == "hello memory"


# ---------------------------------------------------------------------------
# Redis 内存降级模式与故障语义
# ---------------------------------------------------------------------------


def test_degraded_full_features(degraded_redis):
    ad = degraded_redis
    assert ad.is_degraded
    assert ad.set("k1", "v1") and ad.get("k1") == "v1"
    found, val = ad.get_with_status("k1")
    assert (found, val) == (True, "v1")
    assert ad.set("k1", "v2", nx=True) is False  # nx 语义
    ad.hset_multi("h1", {"a": "1", "b": "2"})
    ad.hset("h1", "c", "3")
    assert ad.hget("h1", "b") == "2"
    assert ad.hgetall("h1") == {"a": "1", "b": "2", "c": "3"}
    assert ad.hexists("h1", "a") == 1 and ad.hdel("h1", "a") == 1
    ad.zadd("z1", {"m1": 1.0, "m2": 3.0, "m3": 2.0})
    assert ad.zscore("z1", "m2") == 3.0
    assert ad.zrange_asc("z1", 0, -1) == ["m1", "m3", "m2"]
    assert ad.zrange_desc("z1", 0, -1) == ["m2", "m3", "m1"]
    assert ad.zrange_desc("z1", 0, 0, with_scores=True) == [("m2", 3.0)]
    assert ad.zrange_asc("z1", 0, 1) == ["m1", "m3"]  # 闭区间语义
    assert ad.zremrangebyrank("z1", 0, 0) == 1 and ad.zcard("z1") == 2
    ad.zadd("z1", {"m1": 1.0})
    ad.zincrby("z1", 10, "m1")
    assert ad.zscore("z1", "m1") == 11.0
    assert ad.incr("c1") == 1 and ad.incr("c1", 4) == 5 and ad.decr("c1") == 4
    ad.set("tk", "tv", ttl=1)
    assert ad.ttl("tk") in (0, 1)
    ad.expire("tk", 10)
    assert 0 < ad.ttl("tk") <= 10
    with ad.pipeline() as pipe:
        pipe.set("pk", "pv")
        pipe.execute()
    assert ad.get("pk") == "pv"
    ad.set("scan:a", "1")
    ad.set("scan:b", "2")
    ad.set("other", "x")
    assert ad.delete_pattern("scan:*") == 2
    assert ad.get("other") == "x"


def test_degraded_health_semantics(degraded_redis):
    ad = degraded_redis
    health = ad.get_health()
    assert health["degraded"] is True and health["available"] is False
    assert "degraded_events" in health["stats"] and health["stats"]["degraded_events"] >= 1


def test_fallback_disabled_keeps_original_semantics(degraded_redis):
    from scripts.redis_adapter import RedisConfig, RedisAdapter

    config = RedisConfig(
        host="127.0.0.1", port=6390, socket_connect_timeout=1, socket_timeout=1
    )
    ad = RedisAdapter(config, enable_memory_fallback=False)
    assert not ad.is_degraded
    assert ad.get("x") is None and ad.set("x", "y") is False


def test_memory_client_lru_eviction():
    from scripts.redis_adapter import _MemoryRedisClient

    client = _MemoryRedisClient(3)
    for i in range(5):
        client.set(f"k{i}", str(i))
    assert len(list(client.scan_iter())) == 3


def test_memory_client_flush_to_real():
    from scripts.redis_adapter import _MemoryRedisClient

    class FakeReal:
        def __init__(self):
            self.data, self.h, self.z = {}, {}, {}

        def set(self, k, v, ex=None):
            self.data[k] = v

        def hset(self, k, field=None, value=None, mapping=None):
            self.h.setdefault(k, {}).update(mapping or {field: value})

        def zadd(self, k, mapping):
            self.z.setdefault(k, {}).update(mapping)

        def expire(self, k, ttl):
            pass

    real = FakeReal()
    mem = _MemoryRedisClient(100)
    mem.set("s1", "v")
    mem.hset("h2", mapping={"x": "1"})
    mem.zadd("z2", {"m": 1.5})
    flushed = mem.flush_to(real)
    assert flushed == 3
    assert real.data["s1"] == "v"
    assert real.h["h2"] == {"x": "1"}
    assert real.z["z2"] == {"m": 1.5}


# ---------------------------------------------------------------------------
# 并发安全（共享可变状态加锁后无竞态丢失）
# ---------------------------------------------------------------------------


def test_cache_thread_safety():
    from scripts.cache_layer import L1MemoryCache

    cache = L1MemoryCache()

    def worker(i):
        for j in range(100):
            cache.set(f"k{i % 10}", f"v{i}-{j}")
            cache.get(f"k{i % 10}")
            cache.get_stats()

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(cache.cache) <= 10


def test_insight_pool_thread_safety():
    from scripts.insight_module import Insight, InsightPool, InsightPriority, InsightType

    pool = InsightPool()
    members = list(InsightType.__members__)
    added = []
    add_lock = threading.Lock()

    def worker(i):
        for j in range(10):
            ins = Insight(
                insight_id=f"ins-{i}-{j}",
                insight_type=InsightType[members[i % len(members)]],
                title=f"t{i}{j}",
                content=f"insight-{i}-{j}",
                priority=InsightPriority.MEDIUM,
                confidence=0.9,
            )
            if pool.add_insight(ins):
                with add_lock:
                    added.append(ins.insight_id)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(added) == 500  # 500 次并发添加全部成功，无竞态丢失


# ---------------------------------------------------------------------------
# 冲突解决 / 状态差异 / 枚举成员（历轮修复回归）
# ---------------------------------------------------------------------------


def test_resolve_by_recency_picks_highest_relevance():
    import scripts.conflict_resolver as cr
    from scripts.conflict_resolver import ConflictResolver
    from scripts.type_defs import (
        ActivatedMemory,
        ConflictType,
        HeatLevel,
        MemoryConflict,
        MemoryType,
    )

    resolver = ConflictResolver()
    conflict = MemoryConflict(
        conflict_id="c1",
        conflict_type=ConflictType.FACTUAL_CONTRADICTION,
        memory_ids=["a", "b"],
        description="d",
    )
    memories = [
        ActivatedMemory(
            memory_id="a",
            memory_type=MemoryType.SEMANTIC,
            content_summary="x",
            triggered_by=[],
            relevance_score=0.9,
            heat_level=HeatLevel.WARM,
        ),
        ActivatedMemory(
            memory_id="b",
            memory_type=MemoryType.SEMANTIC,
            content_summary="y",
            triggered_by=[],
            relevance_score=0.6,
            heat_level=HeatLevel.WARM,
        ),
    ]
    result = resolver._resolve_by_recency(conflict, memories)
    assert result.winning_memory == "a"  # 选相关度最高者


def test_layer_state_sync_diff():
    from scripts.state_capture import LayerStateSync

    class Bus:
        def __init__(self):
            self.events = []

        def emit(self, event):
            self.events.append(event)

    sync = LayerStateSync(event_bus=Bus())
    diff = sync.compute_state_diff({"a": 1, "b": 2}, {"a": 1, "b": 3, "c": 4})
    assert set(diff.keys()) == {"b", "c"}
    assert diff["b"] == {"old": 2, "new": 3}


def test_enum_members_exist():
    from scripts.knowledge_gap_identifier import FillStrategy
    from scripts.privacy import StoragePolicy
    from scripts.state_capture import StateEventType
    from scripts.memory_forgetting_mechanism import ForgettingTrigger

    assert hasattr(StoragePolicy, "ANONYMIZED")
    assert not hasattr(StoragePolicy, "ANONYMOUS")
    assert hasattr(FillStrategy, "RETRIEVAL")
    assert not hasattr(FillStrategy, "VERIFICATION")
    assert hasattr(ForgettingTrigger, "IRRELEVANCE")
    assert hasattr(StateEventType, "STATE_CHANGE")


# ---------------------------------------------------------------------------
# 预取存储加载（曾为永远返回 None 的占位）
# ---------------------------------------------------------------------------


def test_prefetch_storage_loader_injection():
    from scripts.prefetch_manager import PrefetchManager

    manager = PrefetchManager()
    store = {"mem:1": "DATA1"}
    assert manager._load_from_storage("mem:1", store.get) == "DATA1"
    assert manager._load_from_storage("missing", store.get) is None
    assert manager._load_from_storage("k") is None  # 未注入时如实降级


# ---------------------------------------------------------------------------
# 懒加载访问模式（曾因未初始化属性丢失首次转移）
# ---------------------------------------------------------------------------


def test_lazy_loader_access_pattern():
    from scripts.context_lazy_loader import ContextLazyLoader

    loader = ContextLazyLoader()
    loader._update_access_pattern("k1")
    loader._update_access_pattern("k2")
    assert loader._access_patterns["k1"] == ["k2"]
    assert loader._last_key == "k2"


# ---------------------------------------------------------------------------
# 上下文编排端到端（借助内存降级模式，无需真实 Redis）
# ---------------------------------------------------------------------------


def test_orchestrator_provider_warning_propagation(degraded_redis):
    from scripts.context_orchestrator import ContextOrchestrator

    orchestrator = ContextOrchestrator(
        redis_adapter=degraded_redis, user_id="u1", session_id="s1"
    )

    def bad_provider():
        raise RuntimeError("boom")
        return []  # pragma: no cover

    orchestrator._providers["bad"] = bad_provider
    result = orchestrator.prepare_context("hello")
    assert result.warnings, "provider 异常应转化为警告而非 NameError"
    assert any("bad" in w for w in result.warnings)


# ---------------------------------------------------------------------------
# 冲突检测->解决->统计 全链路（memory_conflict 模型脱节修复回归）
# ---------------------------------------------------------------------------


def _mk_mem(mid, content, heat="hot", score=0.95):
    from scripts.type_defs import ActivatedMemory, HeatLevel, MemoryType

    return ActivatedMemory(
        memory_id=mid,
        memory_type=MemoryType.SEMANTIC,
        content_summary=content,
        triggered_by=["semantic"],
        relevance_score=score,
        heat_level=HeatLevel[heat.upper()],
    )


def test_conflict_detect_resolve_stats_full_chain():
    from scripts.memory_conflict import MemoryConflictDetector
    from scripts.type_defs import MemoryConflict

    det = MemoryConflictDetector()
    new = _mk_mem("m_new", "甲乙，丙丁，用户是学生")
    old = _mk_mem("m_old", "甲乙，丙丁，用户是学生，否", heat="cold", score=0.8)

    conflicts = det.detect_all_conflicts(new, [old])
    assert conflicts, "事实/时效冲突应被检测到"
    assert all(isinstance(c, MemoryConflict) for c in conflicts)
    assert all(c.memory_ids for c in conflicts), "memory_ids 必填"
    ids = [c.conflict_id for c in conflicts]
    assert len(set(ids)) == len(ids), "同批 conflict_id 不得重复"

    for c in conflicts:
        for mode in (None, "RECENCY", "FREQUENCY", "USER_CONFIRMATION", "SOURCE_TRUST", "CONTEXTUAL"):
            r = det.resolve_conflict(c, mode=mode, memories=[new, old])
            assert r.conflict_id == c.conflict_id
            assert r.resolution_mode is not None

    det.log_conflict(conflicts[0])
    stats = det.get_conflict_stats()
    d = stats.model_dump()
    assert d["total_conflicts"] >= 1
    assert d["by_severity"], "severity 统计应非空"


def test_resolver_all_modes_dispatch_and_trust_clamp():
    from scripts.conflict_resolver import ConflictResolver
    from scripts.type_defs import (
        ConflictType,
        LongTermMemoryContainer,
        MemoryConflict,
        ResolutionMode,
    )

    cr = ConflictResolver()
    conflict = MemoryConflict(
        conflict_id="c9",
        conflict_type=ConflictType.FACTUAL_CONTRADICTION,
        memory_ids=["a", "b"],
        description="d",
    )
    hot_high = _mk_mem("a", "x", heat="hot", score=0.95)  # 0.95+0.2=1.15 必须 clamp 到 1.0
    mems = [hot_high, _mk_mem("b", "y", heat="warm", score=0.6)]
    ltm = LongTermMemoryContainer(user_id="u1")

    for mode in (ResolutionMode.RECENCY, ResolutionMode.FREQUENCY, ResolutionMode.USER_CONFIRMATION,
                 ResolutionMode.SOURCE_TRUST, ResolutionMode.CONTEXTUAL):
        r = cr.resolve(conflict, mems, ltm, mode=mode)
        assert r.resolution_mode == mode, f"{mode} 分支应可达"
        assert 0.0 <= r.confidence <= 1.0, "confidence 必须在 [0,1]"
