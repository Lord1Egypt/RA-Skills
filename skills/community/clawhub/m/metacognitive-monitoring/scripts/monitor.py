#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
metacognitive-monitoring —— 元认知监控（可本地实跑，零依赖）

读取「认知状态」(confidence / uncertainty / novelty / scope_match / necessity)，
输出元决策：PROCEED / DEGRADE / SEEK_HELP / DEFER，并对"高置信+高不确定"触发
过置信校准告警(OVERCONFIDENT)。同时提供简化 ECE 校准误差度量。

用法:
  python monitor.py --selftest
  python monitor.py --json '{"confidence":0.9,"uncertainty":0.2,"novelty":0.3,"scope_match":0.8,"necessity":0.7}'
  python monitor.py --calibrate '[[0.9,true],[0.6,false],[0.8,true],[0.3,false]]'
"""
import argparse
import json
import math
import sys

# 经验阈值（可被校准数据回灌后调参）
T_OVERCONF_CONF = 0.8   # 自信过高
T_OVERCONF_UNC = 0.6    # 不确定性同时过高 -> 矛盾
T_SEEK_UNC = 0.7        # 不确定性过高 -> 求助
T_SEEK_SCOPE = 0.3      # 能力不匹配 -> 求助
T_DEGRADE_UNC = 0.45    # 中等不确定 -> 降级(加验证)
T_DEGRADE_SCOPE = 0.6   # 中等不匹配 -> 降级
T_DEFER_NEC = 0.2       # 价值过低 -> 暂缓

VERDICTS = ("PROCEED", "DEGRADE", "SEEK_HELP", "DEFER", "OVERCONFIDENT")


def decide(state):
    """根据认知状态返回元决策字典。state 字段缺省按中性 0.5 处理。"""
    confidence = float(state.get("confidence", 0.5))
    uncertainty = float(state.get("uncertainty", 0.5))
    novelty = float(state.get("novelty", 0.5))
    scope_match = float(state.get("scope_match", 0.5))
    necessity = float(state.get("necessity", 0.5))

    # 1) 过置信：自信高但依据薄弱 -> 强制求助 + 校准失败标记
    if confidence > T_OVERCONF_CONF and uncertainty > T_OVERCONF_UNC:
        return {
            "verdict": "OVERCONFIDENT",
            "action": "SEEK_HELP",
            "calibration_failure": True,
            "reason": "confidence>%.2f 且 uncertainty>%.2f：自信与依据矛盾，疑似幻觉式过度自信"
                      % (T_OVERCONF_CONF, T_OVERCONF_UNC),
            "confidence": confidence, "uncertainty": uncertainty,
            "scope_match": scope_match, "novelty": novelty, "necessity": necessity,
        }

    # 2) 暂缓：价值过低 -> 直接跳过（最廉价的元决策，优先于"求助/降级"以省资源）
    if necessity < T_DEFER_NEC:
        return {
            "verdict": "DEFER",
            "action": "DEFER",
            "calibration_failure": False,
            "reason": "necessity<%.2f：任务价值过低，建议暂缓/跳过（除非用户显式要求）" % T_DEFER_NEC,
            "confidence": confidence, "uncertainty": uncertainty,
            "scope_match": scope_match, "novelty": novelty, "necessity": necessity,
        }

    # 3) 求助：不确定性过高或能力不匹配
    if uncertainty >= T_SEEK_UNC or scope_match < T_SEEK_SCOPE:
        return {
            "verdict": "SEEK_HELP",
            "action": "SEEK_HELP",
            "calibration_failure": False,
            "reason": "uncertainty>=%.2f 或 scope_match<%.2f：超出可靠边界，需澄清/检索/升级"
                      % (T_SEEK_UNC, T_SEEK_SCOPE),
            "confidence": confidence, "uncertainty": uncertainty,
            "scope_match": scope_match, "novelty": novelty, "necessity": necessity,
        }

    # 4) 降级：中等不确定 / 中等不匹配 -> 加验证、走保守方案
    if uncertainty >= T_DEGRADE_UNC or scope_match < T_DEGRADE_SCOPE:
        return {
            "verdict": "DEGRADE",
            "action": "DEGRADE",
            "calibration_failure": False,
            "reason": "uncertainty>=%.2f 或 scope_match<%.2f：可用，但须加 reason-verify 自验证、走保守路径"
                      % (T_DEGRADE_UNC, T_DEGRADE_SCOPE),
            "confidence": confidence, "uncertainty": uncertainty,
            "scope_match": scope_match, "novelty": novelty, "necessity": necessity,
        }

    # 5) 继续
    return {
        "verdict": "PROCEED",
        "action": "PROCEED",
        "calibration_failure": False,
        "reason": "认知状态健康，正常推进",
        "confidence": confidence, "uncertainty": uncertainty,
        "scope_match": scope_match, "novelty": novelty, "necessity": necessity,
    }


def calibration_error(samples):
    """简化 ECE：把自信度分 10 个桶，对比桶内平均自信与平均正确率，加权绝对差。
    samples: list of [confidence(float), actual_correct(bool)]。"""
    if not samples:
        return 0.0
    buckets = [[] for _ in range(10)]
    for conf, correct in samples:
        conf = max(0.0, min(1.0, float(conf)))
        b = min(9, int(conf * 10))
        buckets[b].append((conf, 1.0 if correct else 0.0))
    ece = 0.0
    total = len(samples)
    for b in buckets:
        if not b:
            continue
        n = len(b)
        avg_conf = sum(c for c, _ in b) / n
        avg_acc = sum(a for _, a in b) / n
        ece += n / total * abs(avg_conf - avg_acc)
    return round(ece, 4)


def run_selftest():
    cases = [
        # (state, 期望 verdict)
        ({"confidence": 0.9, "uncertainty": 0.1, "novelty": 0.3, "scope_match": 0.9, "necessity": 0.8}, "PROCEED"),
        ({"confidence": 0.6, "uncertainty": 0.5, "novelty": 0.4, "scope_match": 0.7, "necessity": 0.6}, "DEGRADE"),
        ({"confidence": 0.5, "uncertainty": 0.8, "novelty": 0.5, "scope_match": 0.5, "necessity": 0.7}, "SEEK_HELP"),
        ({"confidence": 0.7, "uncertainty": 0.3, "novelty": 0.5, "scope_match": 0.2, "necessity": 0.7}, "SEEK_HELP"),
        # 过置信：自信高但依据薄弱 -> OVERCONFIDENT + 强制求助
        ({"confidence": 0.95, "uncertainty": 0.75, "novelty": 0.5, "scope_match": 0.5, "necessity": 0.7}, "OVERCONFIDENT"),
        ({"confidence": 0.9, "uncertainty": 0.2, "novelty": 0.5, "scope_match": 0.5, "necessity": 0.1}, "DEFER"),
    ]
    passed = 0
    for state, expected in cases:
        out = decide(state)
        assert out["verdict"] == expected, (
            "FAIL: %s -> got %s, expected %s" % (state, out["verdict"], expected)
        )
        if expected == "OVERCONFIDENT":
            assert out["calibration_failure"] is True and out["action"] == "SEEK_HELP"
        passed += 1

    # 校准误差：构造"完美校准"样本（正确率按置信度概率生成）-> ECE 应很小
    import random as _r
    _r.seed(0)
    cal = [[c, _r.random() < c] for c in [_r.random() for _ in range(300)]]
    assert calibration_error(cal) < 0.08, "well-calibrated ECE should be small, got %s" % calibration_error(cal)
    # 构造"严重过置信"样本（一律高自信但正确率仅 ~0.55）-> ECE 应明显偏大
    mis = [[max(0.7, _r.random()), _r.random() < 0.55] for _ in range(300)]
    assert calibration_error(mis) > 0.1, "overconfident ECE should be high, got %s" % calibration_error(mis)
    passed += 1
    print("✅ selftest PASSED (%d checks)" % passed)
    return True


def main():
    ap = argparse.ArgumentParser(description="元认知监控")
    ap.add_argument("--json", help="认知状态 JSON")
    ap.add_argument("--calibrate", help="校准样本 JSON: [[conf, correct], ...]")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        run_selftest(); return
    if args.json:
        print(json.dumps(decide(json.loads(args.json)), ensure_ascii=False, indent=2))
        return
    if args.calibrate:
        samples = json.loads(args.calibrate)
        print("calibration_error(ECE) =", calibration_error(samples))
        return
    print("用法: monitor.py --selftest | --json '{...}' | --calibrate '[[c,ok],...]'")


if __name__ == "__main__":
    main()
