#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

HERE = Path(__file__).resolve().parent
GO = HERE / "go_stargazing.py"

BANNED_TOKENS = [
    "decision_rank_score",
    "usable_hours",
    "trip_score",
    "direct_stage2_threshold",
    "cloud_stability=",
]

REAL_WEATHER_SMOKE_DEFAULTS = {
    "single_disputed_models",
    "single_province_refine",
}

SCENARIOS = [
    {
        "name": "single_province_refine",
        "description": "单省细化：不应像换答案，需带参考信息",
        "command": [
            sys.executable,
            str(GO),
            "--mode", "stargazing",
            "--target-datetime", "2026-04-01T22:00:00",
            "--boxes-json", '[{"province":"西藏","min_lat":27.2,"max_lat":30.8,"min_lng":86.0,"max_lng":91.8}]',
            "--compare-models", "ecmwf_ifs", "gfs_global",
            "--top-n", "2",
        ],
        "checks": [
            ("has_reference_note", "error"),
            ("has_refinement_note", "error"),
            ("no_banned_tokens_in_standard", "error"),
            ("no_double_period_in_concise", "warn"),
            ("concise_not_too_long", "warn"),
            ("standard_not_overlapping_lines", "warn"),
        ],
    },
    {
        "name": "trip_far_line",
        "description": "多天远线：不能冒充主方案，需带参考信息",
        "command": [
            sys.executable,
            str(GO),
            "--mode", "stargazing",
            "--scope-preset", "national",
            "--trip-start-date", "2026-04-01",
            "--trip-days", "3",
            "--target-datetime", "2026-04-01T22:00:00",
            "--trip-top-n", "1",
        ],
        "checks": [
            ("trip_plan_label_present", "error"),
            ("trip_far_line_honest", "error"),
            ("has_reference_note", "error"),
            ("no_banned_tokens_in_standard", "error"),
            ("standard_not_overlapping_lines", "warn"),
        ],
    },
    {
        "name": "single_national_basic",
        "description": "单天全国：摘要应带参考信息，不应出现参数味",
        "command": [
            sys.executable,
            str(GO),
            "--mode", "stargazing",
            "--scope-preset", "national",
            "--target-datetime", "2026-04-01T22:00:00",
            "--top-n", "2",
        ],
        "checks": [
            ("has_reference_note", "error"),
            ("no_banned_tokens_in_standard", "error"),
            ("no_double_period_in_concise", "warn"),
            ("concise_not_too_long", "warn"),
        ],
    },
    {
        "name": "single_disputed_models",
        "description": "模型分歧明显：要老实说先观察，别装成稳结论",
        "command": [
            sys.executable,
            str(GO),
            "--real-weather",
            "--mode", "stargazing",
            "--target-datetime", "2026-04-01T22:00:00",
            "--boxes-json", '[{"province":"西藏","min_lat":27.2,"max_lat":30.8,"min_lng":86.0,"max_lng":91.8}]',
            "--compare-models", "ecmwf_ifs", "gfs_global", "icon_global",
            "--top-n", "3",
        ],
        "checks": [
            ("has_reference_note", "error"),
            ("disputed_models_honest", "error"),
            ("no_banned_tokens_in_standard", "error"),
            ("standard_not_overlapping_lines", "warn"),
        ],
    },
    {
        "name": "trip_has_plan_label",
        "description": "多天路线：至少要把方案类型说清楚",
        "command": [
            sys.executable,
            str(GO),
            "--mode", "stargazing",
            "--scope-preset", "national",
            "--trip-start-date", "2026-04-04",
            "--trip-days", "3",
            "--target-datetime", "2026-04-04T22:00:00",
            "--trip-top-n", "1",
        ],
        "checks": [
            ("trip_plan_label_present", "error"),
            ("trip_summary_mentions_plan_type", "warn"),
            ("has_reference_note", "error"),
            ("standard_not_overlapping_lines", "warn"),
        ],
    },
    {
        "name": "single_model_basic",
        "description": "单模型（无对比）：输出应正常，不应出现多模型相关字段报错",
        "command": [
            sys.executable,
            str(GO),
            "--mode", "stargazing",
            "--scope-preset", "national",
            "--target-datetime", "2026-04-01T22:00:00",
            "--model", "ecmwf_ifs",
            "--top-n", "2",
        ],
        "checks": [
            ("has_reference_note", "error"),
            ("no_banned_tokens_in_standard", "error"),
            ("no_double_period_in_concise", "warn"),
        ],
    },
    {
        "name": "2day_trip",
        "description": "2天trip：天数偏少时的方案标签与路线表达",
        "command": [
            sys.executable,
            str(GO),
            "--mode", "stargazing",
            "--scope-preset", "national",
            "--trip-start-date", "2026-04-01",
            "--trip-days", "2",
            "--target-datetime", "2026-04-01T22:00:00",
            "--trip-top-n", "1",
        ],
        "checks": [
            ("trip_plan_label_present", "error"),
            ("has_reference_note", "error"),
        ],
    },
]


def run_json(command: List[str]) -> Dict[str, Any]:
    proc = subprocess.run(command, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"command failed ({proc.returncode}): {' '.join(command)}\nSTDERR:\n{proc.stderr[-1200:]}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid json output: {exc}\nSTDOUT tail:\n{proc.stdout[-1200:]}") from exc


def get_decision_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("decision_summary") or {}


def check_has_reference_note(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    note = ds.get("reference_note") or ""
    ok = "本轮参考信息：" in note and "没直接查" in note
    return ok, "reference_note 已带出本轮参考信息" if ok else "reference_note 缺失或不完整"


def check_has_refinement_note(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    note = ds.get("refinement_note") or ""
    ok = ("大方向先看" in note) and ("继续收窄" in note or "继续细看" in note)
    return ok, "细化说明保持了同一锚点" if ok else "细化说明可能像换答案，缺少“大方向先看/继续收窄”口径"


def check_no_banned_tokens_in_standard(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    text = json.dumps(ds.get("reply_drafts") or {}, ensure_ascii=False)
    hit = [token for token in BANNED_TOKENS if token in text]
    ok = not hit
    return ok, "未发现参数味过重的红线词" if ok else f"发现不该直接给用户的内部词：{', '.join(hit)}"


def check_no_double_period_in_concise(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    concise = ((ds.get("reply_drafts") or {}).get("concise") or "")
    ok = "。。" not in concise
    return ok, "concise 没有双句号毛刺" if ok else "concise 出现双句号"


def check_concise_not_too_long(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    concise = ((ds.get("reply_drafts") or {}).get("concise") or "")
    length = len(concise)
    ok = length <= 140
    return ok, f"concise 长度正常（{length}）" if ok else f"concise 偏长（{length}），建议继续压缩"


def check_standard_not_overlapping_lines(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    standard = ((ds.get("reply_drafts") or {}).get("standard") or "")
    lines = [line.strip() for line in standard.splitlines() if line.strip()]
    norm = []
    for line in lines:
        base = line
        if "：" in line:
            base = line.split("：", 1)[1].strip()
        norm.append(base)
    overlap = False
    for i in range(len(norm)):
        for j in range(i + 1, len(norm)):
            a, b = norm[i], norm[j]
            if not a or not b:
                continue
            if a == b or a in b or b in a:
                overlap = True
                break
        if overlap:
            break
    return (not overlap), "standard 各行信息分工正常" if not overlap else "standard 里有重复味较重的行，建议继续去重"


def check_trip_plan_label_present(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    plan_label = ds.get("plan_label")
    ok = plan_label in {"主方案", "备选方案", "远线方案"}
    return ok, f"trip plan_label={plan_label}" if ok else "trip plan_label 缺失或不在允许集合"


def check_trip_far_line_honest(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    plan_label = ds.get("plan_label")
    one_line = ds.get("one_line") or ""
    if plan_label != "远线方案":
        return True, f"当前不是远线方案（plan_label={plan_label}），无需检查该红线"
    ok = ("没有特别顺的连续主线" in one_line) and ("远线方案" in one_line)
    return ok, "远线方案没有冒充主方案" if ok else "远线方案文案不够诚实，可能冒充主线"


def check_disputed_models_honest(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    level = ds.get("model_stability_level")
    text = (ds.get("reply_drafts") or {}).get("standard") or ""
    if level != "unstable":
        return True, f"当前不是明显分歧场景（model_stability_level={level}），无需强制检查“先观察”口径"
    ok = ("先观察" in text) or ("不建议太早拍板" in text)
    return ok, "模型分歧场景已经老实提示先观察/别太早拍板" if ok else "模型分歧场景文案不够诚实，缺少“先观察/别太早拍板”口径"


def check_trip_summary_mentions_plan_type(payload: Dict[str, Any]) -> Tuple[bool, str]:
    ds = get_decision_summary(payload)
    plan_label = ds.get("plan_label")
    one_line = ds.get("one_line") or ""
    if plan_label == "主方案":
        ok = ("主线" in one_line) or ("主方案" in one_line)
    elif plan_label == "备选方案":
        ok = ("备选" in one_line)
    elif plan_label == "远线方案":
        ok = ("远线方案" in one_line)
    else:
        ok = False
    return ok, f"one_line 已把方案类型说清楚（{plan_label}）" if ok else f"one_line 没有把方案类型说清楚（{plan_label}）"


CHECKERS = {
    "has_reference_note": check_has_reference_note,
    "has_refinement_note": check_has_refinement_note,
    "no_banned_tokens_in_standard": check_no_banned_tokens_in_standard,
    "no_double_period_in_concise": check_no_double_period_in_concise,
    "concise_not_too_long": check_concise_not_too_long,
    "standard_not_overlapping_lines": check_standard_not_overlapping_lines,
    "trip_plan_label_present": check_trip_plan_label_present,
    "trip_far_line_honest": check_trip_far_line_honest,
    "disputed_models_honest": check_disputed_models_honest,
    "trip_summary_mentions_plan_type": check_trip_summary_mentions_plan_type,
}


def maybe_enable_real_weather(command: List[str], enabled: bool) -> List[str]:
    if not enabled:
        return command
    if "--real-weather" in command:
        return command
    if len(command) >= 2:
        return command[:2] + ["--real-weather"] + command[2:]
    return command + ["--real-weather"]


def run_scenario(scenario: Dict[str, Any], use_real_weather: bool) -> Dict[str, Any]:
    command = maybe_enable_real_weather(list(scenario["command"]), use_real_weather)
    payload = run_json(command)
    results = []
    pass_count = 0
    warn_count = 0
    error_count = 0
    for check_name, severity in scenario["checks"]:
        ok, message = CHECKERS[check_name](payload)
        results.append({"check": check_name, "severity": severity, "ok": ok, "message": message})
        if ok:
            pass_count += 1
        elif severity == "warn":
            warn_count += 1
        else:
            error_count += 1
    return {
        "name": scenario["name"],
        "description": scenario["description"],
        "passed": pass_count,
        "warnings": warn_count,
        "errors": error_count,
        "results": results,
        "decision_summary": payload.get("decision_summary") or {},
    }


def print_report(report: List[Dict[str, Any]]) -> int:
    total_warn = 0
    total_err = 0
    for item in report:
        status = "PASS" if item["errors"] == 0 and item["warnings"] == 0 else ("WARN" if item["errors"] == 0 else "FAIL")
        print(f"[{status}] {item['name']} — {item['description']}")
        for row in item["results"]:
            if row["ok"]:
                tag = "PASS"
            elif row["severity"] == "warn":
                tag = "WARN"
            else:
                tag = "FAIL"
            print(f"  - {tag}: {row['message']}")
        ds = item.get("decision_summary") or {}
        if ds.get("one_line"):
            print(f"  - one_line: {ds['one_line']}")
        total_warn += item["warnings"]
        total_err += item["errors"]
        print()
    print(f"Summary: {len(report)} scenarios, total failures = {total_err}, total warnings = {total_warn}")
    return 0 if total_err == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Lightweight reply regression checker for go-stargazing")
    parser.add_argument("--real-weather", action="store_true", help="Run scenarios with real weather instead of mock mode where applicable")
    parser.add_argument("--real-weather-smoke", action="store_true", help="Run only the default small subset of real-weather smoke scenarios")
    parser.add_argument("--scenario", action="append", help="Run only selected scenario name(s)")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    scenarios = SCENARIOS
    if args.real_weather_smoke:
        scenarios = [s for s in scenarios if s["name"] in REAL_WEATHER_SMOKE_DEFAULTS]

    if args.scenario:
        wanted = set(args.scenario)
        scenarios = [s for s in scenarios if s["name"] in wanted]
        missing = wanted - {s["name"] for s in scenarios}
        if missing:
            raise SystemExit(f"Unknown scenario(s): {', '.join(sorted(missing))}")

    use_real_weather = args.real_weather or args.real_weather_smoke
    report = [run_scenario(s, use_real_weather=use_real_weather) for s in scenarios]
    has_errors = any(item["errors"] > 0 for item in report)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise SystemExit(1 if has_errors else 0)
    raise SystemExit(print_report(report))


if __name__ == "__main__":
    main()
