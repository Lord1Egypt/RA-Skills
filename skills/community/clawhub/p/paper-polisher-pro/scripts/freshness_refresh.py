#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freshness_refresh — 指纹保鲜流水线（月度执行，防"检测器永远慢一代"）。

由使用者在本地按月执行（或新模型发布当天手动触发）:
  1. 活体采样   各模型通道生成新语料（通道配置 freshness_channels.json, 缺通道则跳过）
  2. 频谱重建   build_spectrum.py (calib 半)
  3. 权重校准   calibrate_v3.py  (calib 半)
  4. 模式重校   pattern_recalibrator.py --apply (calib 半)
  5. 指纹挖掘   fingerprint_miner.py 各家族 (calib 半)
  6. 回归评测   run_eval.py --split test → 与上次结果对比, AUROC 掉 >3pt 告警

部署: 由使用者自行配置系统月度定时任务，本脚本不创建、不修改任何系统调度项。
  新模型当天: python3 freshness_refresh.py --model <family> --corpus <新采样jsonl>

本脚本只做编排, 各步骤独立可重跑; 每步输出记入 freshness_log/<date>.md。
"""
import os, sys, subprocess, time, argparse
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(HERE, "..", "eval", "freshness_log")


def run_step(name, cmd, log):
    log.write("\n## %s\n$ %s\n" % (name, " ".join(cmd)))
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore",
                       cwd=HERE, timeout=1800)
    out = (r.stdout or "") + (r.stderr or "")
    log.write(out[-3000:] + "\n[exit=%d]\n" % r.returncode)
    return r.returncode == 0


EXPECTED_BASELINES = {
    # 已发布基线（绑定 v35 指纹 2631df3d388b；规则档含 :nosup）——漂移检测对账用
    "fused_oldgen": 0.9998, "fused_current": 0.9400,
    "rules_oldgen": 0.8985, "rules_current": 0.7149,
}
_FRESHNESS_INTERVAL_DAYS = 35


def status(json_out=False):
    """v5.4.0: 保鲜状态自检——最近执行记录/最新评测锚点/基线漂移旗标/到期提醒。"""
    import json as _json
    import time as _time
    root = Path(HERE).parent
    res_dir = root / "eval" / "results"
    log_dir = root / "eval" / "freshness_log"

    logs = sorted(log_dir.glob("*.md")) if log_dir.exists() else []
    last_refresh = _time.strftime("%Y-%m-%d", _time.localtime(logs[-1].stat().st_mtime)) if logs else None

    latest_file, latest_mtime = None, 0.0
    for f in res_dir.glob("*.json"):
        if f.name == "score_cache.json":
            continue
        if f.stat().st_mtime > latest_mtime:
            latest_file, latest_mtime = f, f.stat().st_mtime
    latest_eval = f"{latest_file.name} ({_time.strftime('%Y-%m-%d', _time.localtime(latest_mtime))})" if latest_file else None

    drift = []
    _pairs = [("v35ctl_oldgen.json", "fused_oldgen"), ("v35ctl_gen2026.json", "fused_current"),
              ("v480_rules_oldgen.json", "rules_oldgen"), ("v480_rules_gen2026.json", "rules_current")]
    for fname, key in _pairs:
        fp = res_dir / fname
        try:
            got = _json.load(open(fp, encoding="utf-8")).get("auroc")
            if got is not None and abs(float(got) - EXPECTED_BASELINES[key]) > 1e-6:
                drift.append(f"{fname}: {got} != 已发布 {EXPECTED_BASELINES[key]}")
        except Exception:
            pass

    due = (last_refresh is None) or (
        (_time.time() - _time.mktime(_time.strptime(last_refresh, "%Y-%m-%d"))) / 86400 > _FRESHNESS_INTERVAL_DAYS)
    out = {
        "status": "freshness",
        "last_refresh": last_refresh,
        "latest_eval_record": latest_eval,
        "baseline_drift": drift,
        "baselines_expected": EXPECTED_BASELINES,
        "due_for_refresh": due,
        "interval_days": _FRESHNESS_INTERVAL_DAYS,
        "note": ("保鲜=月度 freshness_refresh.py 全流程（作者侧执行）；本状态不对账则罢，"
                 "对账以 eval/results 指纹绑定结果与已发布基线逐位比对。"),
    }
    if json_out:
        print(_json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print("── 指纹保鲜状态 ──")
        print(f"最近保鲜执行: {last_refresh or '无记录（保鲜流水线作者侧月度执行，本包不含执行痕迹）'}")
        print(f"最新评测记录: {latest_eval or '无'}")
        print(f"已发布基线漂移: {'✗ ' + '; '.join(drift) if drift else '✓ 无（四路基线逐位一致）'}")
        print(f"到期提醒: {'建议执行月度保鲜（>=%d 天未执行）' % _FRESHNESS_INTERVAL_DAYS if due else '未到期'}")
        print(out["note"])
    return 0 if not drift else 1


def main():
    ap = argparse.ArgumentParser()
    if "--status" in sys.argv:
        return status(json_out="--json" in sys.argv)
    ap.add_argument("--corpus", default=os.path.join(
        "pp_corpus", "eval_zh.jsonl"),
        help="基础语料(大语料jsonl)")
    ap.add_argument("--model", default=None, help="新模型名(触发单家族挖掘)")
    ap.add_argument("--skip-miner", action="store_true")
    a = ap.parse_args()

    os.makedirs(LOG_DIR, exist_ok=True)
    today = time.strftime("%Y%m%d")
    log = open(os.path.join(LOG_DIR, today + ".md"), "w", encoding="utf-8")
    log.write("# 指纹保鲜运行 %s\n" % time.strftime("%Y-%m-%d %H:%M"))
    py = sys.executable
    ok = True
    ok &= run_step("频谱重建", [py, "build_spectrum.py", "--corpus", a.corpus, "--apply"], log)
    ok &= run_step("权重校准", [py, "calibrate_v3.py", "--corpus", a.corpus, "--apply"], log)
    ok &= run_step("模式重校", [py, "pattern_recalibrator.py", "--corpus", a.corpus, "--apply"], log)
    if a.model:
        ok &= run_step("指纹挖掘:" + a.model,
                       [py, "fingerprint_miner.py", "--corpus", a.corpus,
                        "--model", a.model, "--apply"], log)
    elif not a.skip_miner:
        import json
        reg_p = os.path.join(HERE, "..", "references", "model_fingerprints.json")
        try:
            fams = list(json.load(open(reg_p, encoding="utf-8"))["families"].keys())
        except Exception:
            fams = []
        for fam in fams:
            run_step("指纹挖掘:" + fam,
                     [py, "fingerprint_miner.py", "--corpus", a.corpus,
                      "--model", fam, "--apply"], log)
    # 回归(留出半)
    ev = os.path.join(HERE, "..", "eval", "run_eval.py")
    r = subprocess.run([py, ev, "--corpus", a.corpus, "--split", "test",
                        "--tag", "freshness_" + today],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    log.write("\n## 回归评测\n" + (r.stdout or "")[-3000:])
    log.write("\n---\n状态: %s\n" % ("✅ 全部成功" if ok else "⚠️ 有步骤失败, 见上文"))
    log.close()
    print("日志: %s" % os.path.join(LOG_DIR, today + ".md"))
    print("提醒: 对比 eval/results/ 下最新两次 freshness_*.json 的 AUROC, 掉幅>3pt 需人工介入。")


if __name__ == "__main__":
    main()
