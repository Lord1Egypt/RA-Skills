#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hypothesis-driven-inquiry —— 假设驱动探究（溯因推理 Abduction）。

由观测反推成因，按 解释覆盖 × 简约度 排序候选假设，
并为每条假设设计判别性实验（它解释、但最强竞对不解释的观测）。

零依赖、可本地实跑；--selftest 自带夹具断言全链路通过。
"""
import os, sys, argparse, json


def parse_hypo(s):
    """hA|explains=o1,o2|complexity=1 -> dict"""
    name, rest = (s.split("|", 1) + [""])[:2]
    d = {"name": name.strip(), "explains": set(), "complexity": 1}
    for part in rest.split("|"):
        if part.startswith("explains="):
            d["explains"] = set(x.strip() for x in part[len("explains="):].split(",") if x.strip())
        elif part.startswith("complexity="):
            try:
                d["complexity"] = float(part[len("complexity="):])
            except Exception:
                d["complexity"] = 1
    return d


def rank(obs, hypos):
    """score = coverage_ratio × parsimony；稳定排序。"""
    O = set(obs)
    scored = []
    for h in hypos:
        explained = h["explains"] & O
        cov = len(explained) / len(O) if O else 0.0
        parsimony = 1.0 / (1.0 + h["complexity"])
        scored.append({
            "name": h["name"],
            "explains": sorted(explained),
            "coverage_ratio": round(cov, 3),
            "parsimony": round(parsimony, 3),
            "score": round(cov * parsimony, 4),
        })
    scored.sort(key=lambda x: (-x["score"], x["name"]))
    return scored


def discriminate(obs, hypos, ranked):
    """为每条假设找判别性实验：它解释、但其最强竞对（评分最高的其他假设）不解释的观测。

    定义相对"全体竞对并集"更贴合实际：一个假设只要存在一条能把
    它与最强替代方案区分开的观测，就具备可证伪性（crucial experiment）。
    """
    O = set(obs)
    results = []
    for i, r in enumerate(ranked):
        h = next(x for x in hypos if x["name"] == r["name"])
        # 最强竞对 = 其余假设中评分最高者
        best_rival = None
        best_rival_score = -1.0
        for j, r2 in enumerate(ranked):
            if j == i:
                continue
            if r2["score"] > best_rival_score:
                best_rival_score = r2["score"]
                best_rival = next(x for x in hypos if x["name"] == r2["name"])
        rival_explains = (best_rival["explains"] & O) if best_rival else set()
        test = sorted((h["explains"] & O) - rival_explains)
        results.append({
            "name": r["name"],
            "discriminating_test": test,   # 可证伪的判别观测
            "falsifiable": len(test) > 0,
        })
    return results


def conclude(obs, hypos):
    ranked = rank(obs, hypos)
    disc = discriminate(obs, hypos, ranked)
    return {"observations": sorted(set(obs)), "ranked": ranked, "discriminating": disc}


def selftest():
    print("🧪 selftest: 构造溯因夹具 ...")
    obs = ["o1", "o2", "o3", "o4"]
    hypos = [
        parse_hypo("h_A|explains=o1,o2,o3|complexity=1"),   # 覆盖3/4，最简
        parse_hypo("h_B|explains=o2,o3,o4|complexity=1"),   # 覆盖3/4，最简
        parse_hypo("h_C|explains=o1,o4|complexity=3"),      # 覆盖2/4，复杂
    ]
    res = conclude(obs, hypos)
    ranked = res["ranked"]
    # 断言1：评分最高的是 h_A（覆盖0.75×简约0.5=0.375，按名序居首）
    assert ranked[0]["name"] == "h_A", f"top 应为 h_A，实际 {ranked[0]['name']}"
    assert ranked[0]["coverage_ratio"] == 0.75, f"h_A 覆盖应=0.75，实际 {ranked[0]['coverage_ratio']}"
    # 断言2：h_C 覆盖最低（2/4）排末位
    assert ranked[-1]["name"] == "h_C", f"末位应为 h_C，实际 {ranked[-1]['name']}"
    # 断言3：每条假设都存在可证伪的判别性实验（crucial experiment）
    byname = {d["name"]: d for d in res["discriminating"]}
    for nm in ("h_A", "h_B", "h_C"):
        assert byname[nm]["falsifiable"], f"{nm} 应存在判别实验"
    # h_A 相对最强竞对 h_B，独有判别观测 o1
    assert byname["h_A"]["discriminating_test"] == ["o1"], f"h_A 判别观测应=[o1]，实际 {byname['h_A']['discriminating_test']}"
    print(f"  ✓ 评分排序正确（top={ranked[0]['name']}, cov={ranked[0]['coverage_ratio']}）")
    print(f"  ✓ 判别性实验设计正确（3 条假设均有可证伪检验，h_A⟷o1）")
    print("✅ selftest 全链路 PASS")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obs", default="")
    ap.add_argument("--hypo", action="append", default=[], help="hA|explains=o1,o2|complexity=1")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    obs = [x.strip() for x in args.obs.split(",") if x.strip()]
    hypos = [parse_hypo(h) for h in args.hypo]
    if not obs or not hypos:
        print("用法: --obs o1,o2 --hypo 'hA|explains=o1|complexity=1' [--selftest]")
        return None
    res = conclude(obs, hypos)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return res


if __name__ == "__main__":
    main()
