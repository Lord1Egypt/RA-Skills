#!/usr/bin/env python3
"""octo-mention merge_mentions 单元测试

运行: python3 tests/test_merge.py
覆盖: 跨群合并、证据去重、置信度计算、证据条数上限、新人追加、bot字段覆盖。
"""
import os, sys, json, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import merge_mentions as mm


def flat_group(gid, members):
    return {"group_id": gid, "members": members}


def member(uid, name, mtype="human", aliases=None):
    return {"uid": uid, "canonical_name": name, "member_type": mtype,
            "aliases": aliases or [], "uncertain_aliases": [], "conflicts": []}


def alias(name, conf, evs, atype="common_call"):
    return {"alias": name, "alias_type": atype, "confidence": conf,
            "evidence_count": len(evs), "evidence": evs, "reason": "t"}


class TestMerge(unittest.TestCase):
    def test_new_person_added(self):
        base = None
        new = flat_group("g1", [member("u1", "张三", aliases=[
            alias("老张", 0.8, [{"time": "t1", "sender": "s", "text": "@张三 老张"}])])])
        out = mm.merge(base, new)
        self.assertIn("u1", out["persons"])
        self.assertEqual(out["persons"]["u1"]["seen_in_groups"], ["g1"])
        self.assertEqual(out["version"], 1)

    def test_cross_group_alias_merge(self):
        base = mm.merge(None, flat_group("g1", [member("u1", "张三", aliases=[
            alias("老张", 0.75, [{"time": "t1", "sender": "a", "text": "@张三 老张"}])])]))
        out = mm.merge(base, flat_group("g2", [member("u1", "张三", aliases=[
            alias("老张", 0.75, [{"time": "t2", "sender": "b", "text": "@张三 老张在?"}])])]))
        p = out["persons"]["u1"]
        self.assertEqual(sorted(p["seen_in_groups"]), ["g1", "g2"])
        al = [a for a in p["aliases"] if a["alias"] == "老张"][0]
        self.assertEqual(al["evidence_count"], 2)            # 跨群证据累加
        self.assertEqual(sorted(al["groups"]), ["g1", "g2"])  # 标两群
        self.assertGreater(al["confidence"], 0.75)            # 置信度上升

    def test_evidence_dedup(self):
        ev = {"time": "t1", "sender": "a", "text": "@张三 老张"}
        base = mm.merge(None, flat_group("g1", [member("u1", "张三", aliases=[alias("老张", 0.8, [ev])])]))
        # 同群同证据再合并一次，不应重复计数
        out = mm.merge(base, flat_group("g1", [member("u1", "张三", aliases=[alias("老张", 0.8, [ev])])]))
        al = out["persons"]["u1"]["aliases"][0]
        self.assertEqual(al["evidence_count"], 1)
        self.assertEqual(len(al["evidence"]), 1)

    def test_evidence_cap(self):
        base = None
        for i in range(8):  # 8 条不同证据
            new = flat_group("g1", [member("u1", "张三", aliases=[
                alias("老张", 0.8, [{"time": f"t{i:02d}", "sender": f"s{i}", "text": f"msg{i}"}])])])
            base = mm.merge(base, new)
        al = base["persons"]["u1"]["aliases"][0]
        self.assertEqual(al["evidence_count"], 8)             # 真实总数不丢
        self.assertLessEqual(len(al["evidence"]), mm.MAX_EVIDENCE)  # 实际只留上限
        # 保留的是最新的
        times = [e["time"] for e in al["evidence"]]
        self.assertIn("t07", times)
        self.assertNotIn("t00", times)

    def test_authoritative_field_override(self):
        base = mm.merge(None, flat_group("g1", [member("b1", "小罗", "bot")]))
        base["persons"]["b1"]["owner"] = "罗伟杰"
        # 新一轮带更新的 owner，应覆盖
        nm = member("b1", "小罗", "bot")
        nm["owner"] = "罗伟杰V2"
        out = mm.merge(base, flat_group("g1", [nm]))
        self.assertEqual(out["persons"]["b1"]["owner"], "罗伟杰V2")

    def test_confidence_capped(self):
        base = None
        for i in range(20):
            base = mm.merge(base, flat_group(f"g{i}", [member("u1", "张三", aliases=[
                alias("老张", 0.8, [{"time": f"t{i}", "sender": f"s{i}", "text": f"m{i}"}])])]))
        al = base["persons"]["u1"]["aliases"][0]
        self.assertLessEqual(al["confidence"], 0.9)  # common_call 封顶 0.9

    def test_previous_names_tracked(self):
        base = mm.merge(None, flat_group("g1", [member("u1", "taylor")]))
        out = mm.merge(base, flat_group("g2", [member("u1", "田哥")]))
        p = out["persons"]["u1"]
        self.assertEqual(p["canonical_name"], "田哥")          # 取最新
        prev = [pn["name"] for pn in p.get("previous_names", [])]
        self.assertIn("taylor", prev)                          # 旧名不丢

    def test_last_evidence_time_set(self):
        out = mm.merge(None, flat_group("g1", [member("u1", "张三", aliases=[
            alias("老张", 0.8, [{"time": "2026-06-01T10:00:00+08:00", "sender": "a", "text": "x"}])])]))
        al = out["persons"]["u1"]["aliases"][0]
        self.assertEqual(al.get("last_evidence_time"), "2026-06-01T10:00:00+08:00")

    # === 纠错功能测试 ===

    def test_locked_alias_not_overridden(self):
        """被锁定的别名不应被自动分析覆盖"""
        base = mm.merge(None, flat_group("g1", [member("u1", "张三", aliases=[
            alias("老张", 0.8, [{"time": "t1", "sender": "a", "text": "x"}])])]))
        # 手动锁定这个别名
        base["persons"]["u1"]["aliases"][0]["locked"] = True
        base["persons"]["u1"]["aliases"][0]["source"] = "manual"
        base["persons"]["u1"]["aliases"][0]["confidence"] = 1.0
        # 自动分析尝试覆盖（confidence 不同）
        out = mm.merge(base, flat_group("g1", [member("u1", "张三", aliases=[
            alias("老张", 0.6, [{"time": "t2", "sender": "b", "text": "y"}])])]))
        al = out["persons"]["u1"]["aliases"][0]
        # 仍然是手动锁定的值——未被覆盖
        self.assertEqual(al["confidence"], 1.0)
        self.assertTrue(al["locked"])

    def test_rejected_alias_not_added(self):
        """被拒绝的别名不应被自动分析重新收录"""
        base = mm.merge(None, flat_group("g1", [member("u1", "张三")]))
        # 添加拒绝词
        base["persons"]["u1"]["rejected_aliases"] = [
            {"alias": "老板", "source": "manual", "rejected_at": "2026-06-01", "reason": "通用称呼"}
        ]
        # 自动分析尝试收录"老板"
        out = mm.merge(base, flat_group("g1", [member("u1", "张三", aliases=[
            alias("老板", 0.7, [{"time": "t1", "sender": "a", "text": "x"}])])]))
        # 不应出现在 aliases 里
        alias_names = [a["alias"] for a in out["persons"]["u1"]["aliases"]]
        self.assertNotIn("老板", alias_names)
        # rejected_aliases 保留
        self.assertEqual(len(out["persons"]["u1"]["rejected_aliases"]), 1)

    def test_manual_alias_overrides_locked(self):
        """手动纠错(source=manual)可以覆盖已锁定的条目"""
        base = mm.merge(None, flat_group("g1", [member("u1", "张三", aliases=[
            alias("老张", 0.8, [{"time": "t1", "sender": "a", "text": "x"}])])]))
        base["persons"]["u1"]["aliases"][0]["locked"] = True
        base["persons"]["u1"]["aliases"][0]["source"] = "manual"
        # 另一次手动纠错（source=manual）应该能覆盖
        new_alias = alias("老张", 0.95, [{"time": "t2", "sender": "b", "text": "y"}])
        new_alias["source"] = "manual"
        out = mm.merge(base, flat_group("g1", [member("u1", "张三", aliases=[new_alias])]))
        al = out["persons"]["u1"]["aliases"][0]
        # manual 可以覆盖 manual
        self.assertGreater(al["confidence"], 0.8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
