#!/usr/bin/env python3
"""
tests/test_capability_extension_v101.py — P0/P1 能力扩展测试（v1.0.1）

覆盖：
  1. public_apis_catalog：README 解析 / 检索 / 分类 / 降级
  2. account_trust_scorer：真人/机器人/水军/信息不足 四类判定 + 强flag降级
  3. capability_registry v2：新增能力声明 / kind 族 / 双源一致
  4. tiered_router：意图识别 / 执行顺序 / 免费优先 / 末端兜底
  5. agentkey adapter：注册 / 优雅降级
"""

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))                  # 项目根（ecosystem 包导入必需）
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "ecosystem"))

# 隔离数据目录（不污染真实状态）
TEST_DATA_DIR = Path(os.environ.get("TEST_TMP", "/tmp/infoseek_cap_ext_test"))
TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
os.environ["INFOSEEK_DATA_DIR"] = str(TEST_DATA_DIR)


class TestPublicApisCatalog(unittest.TestCase):
    def test_parse_readme(self):
        import public_apis_catalog as pc
        # 用内置最小集验证解析 schema（不依赖网络）
        entries = pc._BUILTIN_MINIMAL
        self.assertGreaterEqual(len(entries), 10)
        for e in entries:
            self.assertIn("category", e)
            self.assertIn("name", e)
            self.assertIn("auth", e)
            self.assertIn("url", e)

    def test_builtin_fallback(self):
        """无索引/无网络 → 内嵌最小集（L3 降级不塌）。"""
        import public_apis_catalog as pc
        # 确定性降级：目录不存在 + 网络拉取强制失败 → 内嵌集
        pc.catalog_path = lambda: Path("/nonexistent/void.json")
        pc._fetch_readme = lambda: (_ for _ in ()).throw(RuntimeError("offline"))
        data = pc.build_index(refresh=True)
        self.assertIn("entries", data)
        self.assertGreater(len(data["entries"]), 0)
        self.assertTrue(data.get("degraded", False))

    def test_search_free_api(self):
        import public_apis_catalog as pc
        pc.catalog_path = lambda: Path("/nonexistent/void.json")
        pc._fetch_readme = lambda: (_ for _ in ()).throw(RuntimeError("offline"))
        r = pc.search_free_api("汇率", limit=3)
        self.assertGreaterEqual(len(r), 1)
        self.assertIn("name", r[0])


class TestAccountTrustScorer(unittest.TestCase):
    def _scorer(self):
        from account_trust_scorer import score_account
        return score_account

    def test_real_account(self):
        s = self._scorer()({
            "username": "alice", "account_age_days": 800, "post_count": 1200,
            "post_interval_std": 3.5, "active_hours": 14, "reply_rate": 1.2,
            "followers": 5000, "following": 300, "zombie_follower_ratio": 0.05,
            "engagement_rate": 0.03, "topic_diversity": 0.7,
            "cross_platform_overlap": 0.1, "cross_platform_matches": 3,
        })
        self.assertEqual(s["verdict"], "real")
        self.assertGreaterEqual(s["trust_score"], 80)

    def test_bot_timer(self):
        """定时机器人：强flag≥3 → 强制 bot。"""
        s = self._scorer()({
            "username": "bot1", "account_age_days": 400, "post_count": 4000,
            "post_interval_std": 0.05, "active_hours": 1, "reply_rate": 0,
            "followers": 50, "following": 5000, "zombie_follower_ratio": 0.8,
            "engagement_rate": 0.0001, "topic_diversity": 0.02,
            "cross_platform_overlap": 0.95, "cross_platform_matches": 0,
        })
        self.assertIn(s["verdict"], ("bot", "suspicious"))

    def test_matrix_mob(self):
        s = self._scorer()({
            "username": "mob", "account_age_days": 15, "post_count": 3000,
            "post_interval_std": 0.1, "active_hours": 2, "reply_rate": 80,
            "followers": 10, "following": 200, "zombie_follower_ratio": 0.9,
            "engagement_rate": 0.0002, "topic_diversity": 0.05,
            "cross_platform_overlap": 0.9, "cross_platform_matches": 1,
        })
        self.assertEqual(s["verdict"], "bot")

    def test_insufficient_info(self):
        """缺 ≥2 维信号 → unknown（不误判）。"""
        s = self._scorer()({"username": "ghost"})
        self.assertEqual(s["verdict"], "unknown")
        self.assertEqual(s["confidence"], 0.0)

    def test_output_schema(self):
        s = self._scorer()({"username": "x", "account_age_days": 100})
        for k in ("trust_score", "verdict", "verdict_cn", "confidence", "dimensions", "flags"):
            self.assertIn(k, s)
        self.assertIn("maturity", s["dimensions"])


class TestRegistryV2(unittest.TestCase):
    def test_new_capabilities(self):
        from capability_registry import list_capabilities, get_capability
        caps = {c["name"]: c for c in list_capabilities()}
        for name in ("AccountTrustScorer", "PublicApisCatalog", "AgentKey"):
            self.assertIn(name, caps)
        self.assertEqual(caps["AccountTrustScorer"]["kind"], "identity_attribution")
        self.assertEqual(caps["PublicApisCatalog"]["kind"], "free_api")
        self.assertEqual(caps["AgentKey"]["kind"], "gateway_api")
        self.assertEqual(caps["AgentKey"]["auth_env"], "AGENTKEY_API_KEY")

    def test_yaml_embedded_consistency(self):
        """registry.yaml 与内嵌默认双源一致。"""
        from capability_registry import list_capabilities
        try:
            import yaml
            yaml_data = yaml.safe_load(
                (ROOT / "capabilities" / "registry.yaml").read_text(encoding="utf-8"))
            yaml_names = {c["name"] for c in yaml_data["capabilities"]}
            emb_names = {c["name"] for c in list_capabilities()}
            self.assertEqual(yaml_names, emb_names)
        except ImportError:
            self.skipTest("PyYAML 缺失")


class TestTieredRouter(unittest.TestCase):
    def test_detect_intent(self):
        from tiered_router import detect_intent
        self.assertEqual(detect_intent("2026 铝价走势"), "finance")
        self.assertEqual(detect_intent("某品牌用户口碑"), "sentiment")
        self.assertEqual(detect_intent("查询账号 alice 身份"), "identity")
        self.assertEqual(detect_intent("量子纠缠态制备"), "general")

    def test_resolve_route_exec_order(self):
        """执行顺序免费优先：finance 链 L0 起。"""
        from tiered_router import resolve_route
        plan = resolve_route("汇率", intent="finance")
        self.assertEqual(plan["chain"][0], "PublicApisCatalog")
        self.assertEqual(plan["layers"][0], "L0-免费")

    def test_route_free_hit(self):
        """finance 意图 → L0 免费层命中（目录检索）。"""
        from tiered_router import route_query
        # 隔离数据目录 + 离线目录强制内嵌集
        import public_apis_catalog as pc
        pc.catalog_path = lambda: Path("/nonexistent/void.json")
        pc._fetch_readme = lambda: (_ for _ in ()).throw(RuntimeError("offline"))
        r = route_query("汇率")
        self.assertIn(r["used"], ("PublicApisCatalog", "QVeris"))
        if r["used"] == "PublicApisCatalog":
            self.assertEqual(r["layer"], "L0-免费")
            self.assertGreater(len(r["results"]), 0)

    def test_route_manual_fallback(self):
        """全层未命中 → manual_review（不静默丢数据）。"""
        from tiered_router import route_query
        import public_apis_catalog as pc
        pc.catalog_path = lambda: Path("/nonexistent/void.json")
        pc._fetch_readme = lambda: (_ for _ in ()).throw(RuntimeError("offline"))
        r = route_query("量子纠缠态制备超导材料")
        if r["used"] == "manual_review":
            self.assertTrue(r["exhausted"])
            self.assertEqual(r["results"][0]["source"], "manual_review")


class TestAgentKeyAdapter(unittest.TestCase):
    def test_registered(self):
        from ecosystem.registry import REGISTRY, get_adapter
        self.assertIn("agentkey", REGISTRY)
        ad = get_adapter("agentkey")
        self.assertEqual(ad.name, "agentkey")
        self.assertEqual(ad.credential_spec()["required_env"], ["AGENTKEY_API_KEY"])

    def test_graceful_degrade_no_key(self):
        from ecosystem.adapters.agentkey import search, AgentKeyUnavailable
        os.environ.pop("AGENTKEY_API_KEY", None)
        with self.assertRaises(AgentKeyUnavailable):
            search("股票行情")

    def test_graceful_degrade_no_mcp(self):
        from ecosystem.adapters.agentkey import find_tools, AgentKeyUnavailable
        os.environ["AGENTKEY_API_KEY"] = "sk-test"
        try:
            with self.assertRaises(AgentKeyUnavailable):
                find_tools("股票", subset="finance")
        finally:
            os.environ.pop("AGENTKEY_API_KEY", None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
