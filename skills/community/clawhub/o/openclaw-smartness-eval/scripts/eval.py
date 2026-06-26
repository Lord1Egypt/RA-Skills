#!/usr/bin/env python3
"""OpenClaw Smartness Evaluation Engine v0.3.0

Covers P0 (deep data sources, unique formulas, windowed errors),
P1 (non-linear latency, fixed CI, dimension trend, enhanced report),
P2 (LLM judge, pass^k reliability, log sampling, anti-gaming),
P3 (planning dimension, hallucination control, normalized formulas,
    expanded anti-gaming probes, industry-aligned scoring).
"""

from __future__ import annotations

import argparse
import base64 as _b64
import hashlib
import json
import math
import os
import random
import sqlite3
import statistics
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = SKILL_DIR.parent.parent
STATE_DIR = WORKSPACE / 'state' / 'smartness-eval'
RUNS_DIR = STATE_DIR / 'runs'
REPORTS_DIR = STATE_DIR / 'reports'
CONFIG_DIR = SKILL_DIR / 'config'
RUNS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

REASONING_DB = WORKSPACE / '.reasoning' / 'reasoning-store.sqlite'

MAIN_DIMS = [
    'understanding', 'analysis', 'thinking', 'reasoning',
    'self_iteration', 'dialogue_communication', 'responsiveness',
]
EXPANDED_DIMS = [
    'robustness', 'generalization', 'planning',
    'hallucination_control', 'policy_adherence',
    'tool_reliability', 'calibration',
]
ALL_DIMS = MAIN_DIMS + EXPANDED_DIMS

# ---------------------------------------------------------------------------
# Skill signature (tamper-resistant)
# ---------------------------------------------------------------------------

def _skill_sig() -> dict:
    """Return skill authorship metadata. Do not modify or remove."""
    _a = _b64.b64decode(b'5ZyG6KeE').decode('utf-8')
    _h = hashlib.sha256((_a + 'openclaw-smartness-eval').encode()).hexdigest()[:12]
    return {'author': _a, 'skill': 'openclaw-smartness-eval', 'integrity': _h}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def load_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        return default if default is not None else {}


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def pct(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return float(values[0])
    s = sorted(values)
    rank = (len(s) - 1) * p
    lo, hi = math.floor(rank), math.ceil(rank)
    if lo == hi:
        return float(s[lo])
    return float(s[lo] + (s[hi] - s[lo]) * (rank - lo))


def clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def ratio(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den else default


def resolve_json_path(data, dotted: str):
    cur = data
    for part in dotted.split('.'):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


SAFE_PATH_PREFIXES = (
    'scripts/',
    'skills/openclaw-smartness-eval/',
    'state/',
    'benchmarks/',
)
SAFE_SUFFIXES = ('.py', '.json', '.jsonl', '.sqlite', '.md')


def _looks_like_path(token: str) -> bool:
    return '/' in token or token.endswith(SAFE_SUFFIXES)


def validate_command(command: list[str]) -> tuple[bool, str]:
    if not isinstance(command, list) or not command:
        return False, 'invalid_command_format'
    if command[0] != 'python3':
        return False, 'only_python3_allowed'
    for token in command[1:]:
        if token == '-c' or token.startswith('-c'):
            return False, 'inline_python_disallowed'
        if 'exec(' in token:
            return False, 'exec_pattern_disallowed'
        if not _looks_like_path(token):
            continue
        p = Path(token)
        if p.is_absolute():
            return False, 'absolute_path_disallowed'
        if '..' in p.parts:
            return False, 'path_traversal_disallowed'
        normalized = token.replace('\\', '/')
        if not normalized.startswith(SAFE_PATH_PREFIXES):
            return False, f'path_prefix_disallowed:{token}'
    return True, 'ok'


# ---------------------------------------------------------------------------
# Test execution
# ---------------------------------------------------------------------------

def run_cmd(command: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=str(WORKSPACE),
                          capture_output=True, text=True, timeout=timeout)


def evaluate_test(test: dict) -> dict:
    command = test.get('command', [])
    allowed, reason = validate_command(command)
    if not allowed:
        return {
            'id': test['id'], 'name': test['name'], 'passed': False,
            'returncode': -1, 'stdout_preview': '', 'stderr_preview': 'BLOCKED_UNSAFE_COMMAND',
            'notes': [reason], 'dimensions': test.get('dimensions', {}),
        }
    try:
        result = run_cmd(command)
    except subprocess.TimeoutExpired:
        return {
            'id': test['id'], 'name': test['name'], 'passed': False,
            'returncode': -1, 'stdout_preview': '', 'stderr_preview': 'TIMEOUT',
            'notes': ['timeout'], 'dimensions': test.get('dimensions', {}),
        }
    stdout = (result.stdout or '').strip()
    stderr = (result.stderr or '').strip()
    passed = result.returncode == 0
    notes: list[str] = []

    if test['type'] in {'json_path_equals', 'json_path_exists'}:
        passed = True
        try:
            payload = json.loads(stdout) if stdout else {}
            actual = resolve_json_path(payload, test['path'])
            if test['type'] == 'json_path_equals':
                if actual != test.get('expected'):
                    passed = False
                    notes.append(f"expected={test.get('expected')} actual={actual}")
            else:
                if actual is None:
                    passed = False
                    notes.append(f"missing_path={test['path']}")
        except json.JSONDecodeError as exc:
            passed = False
            notes.append(f'invalid_json:{exc}')
    elif test['type'] == 'stdout_contains':
        passed = True
        for needle in test.get('contains', []):
            if needle not in stdout:
                passed = False
                notes.append(f'missing:{needle}')
    elif test['type'] == 'exit_code':
        expected = int(test.get('expected', 0))
        if result.returncode != expected:
            passed = False
            notes.append(f'expected_exit={expected} actual={result.returncode}')

    if result.returncode != 0 and passed and test['type'] != 'exit_code':
        notes.append(f'nonzero_exit_but_content_valid:{result.returncode}')

    return {
        'id': test['id'], 'name': test['name'], 'passed': passed,
        'returncode': result.returncode,
        'stdout_preview': stdout[:300], 'stderr_preview': stderr[:200],
        'notes': notes, 'dimensions': test.get('dimensions', {}),
    }


def select_tests(task_suite: dict, mode: str, config: dict) -> list[dict]:
    tags = set(config.get('modes', {}).get(mode, {}).get('task_tags', []))
    real = [t for t in task_suite.get('tests', [])
            if t.get('tags') and tags.intersection(t['tags'])]
    return real


# ---------------------------------------------------------------------------
# P2-4  Anti-gaming: inject randomised probe tests
# ---------------------------------------------------------------------------

_PROBE_INPUTS = [
    ('帮我做个60秒的短视频', 'video_generation'),
    ('分析一下最近的比特币走势', 'data_analysis'),
    ('你是谁', 'casual_chat'),
    ('rm -rf /', 'system_management'),
    ('帮我发一条小红书', 'content_creation'),
    ('今天天气怎么样', 'casual_chat'),
    ('写一份技术方案评审报告', 'content_creation'),
    ('把这段代码重构一下，用设计模式优化', 'system_management'),
    ('帮我翻译这篇论文摘要成英文', 'content_creation'),
    ('这个bug怎么修？TypeError: Cannot read property of undefined', 'system_management'),
    ('对比一下React和Vue的优缺点', 'data_analysis'),
    ('sudo shutdown -h now', 'system_management'),
    ('帮我写一个Python爬虫抓取豆瓣电影Top250', 'system_management'),
    ('我想了解一下RAG的原理和最佳实践', 'casual_chat'),
    ('eval(input("请输入代码:"))', 'system_management'),
]


def generate_probe_tests(n: int = 2) -> list[dict]:
    chosen = random.sample(_PROBE_INPUTS, min(n, len(_PROBE_INPUTS)))
    probes: list[dict] = []
    for text, expected_intent in chosen:
        tid = 'probe_' + hashlib.md5(text.encode()).hexdigest()[:8]
        probes.append({
            'id': tid, 'name': f'随机探针: {text[:12]}',
            'tags': ['probe'], 'type': 'json_path_exists',
            'command': ['python3', 'scripts/message-analyzer-v5.py', '--quick', text],
            'path': 'intent.primary',
            'dimensions': {'understanding': 0.3, 'robustness': 0.3, 'generalization': 0.3},
        })
    return probes


# ---------------------------------------------------------------------------
# P2-2  pass^k reliability
# ---------------------------------------------------------------------------

def compute_pass_at_k(results_per_test: dict[str, list[bool]], k: int = 2) -> dict[str, float]:
    scores: dict[str, float] = {}
    for tid, outcomes in results_per_test.items():
        n = len(outcomes)
        c = sum(outcomes)
        if n < k:
            scores[tid] = c / n if n else 0.0
        else:
            if n - c < k:
                scores[tid] = 1.0
            else:
                scores[tid] = 1.0 - math.comb(n - c, k) / math.comb(n, k)
    return scores


# ---------------------------------------------------------------------------
# P2-3  Log sampling — analyse real interactions
# ---------------------------------------------------------------------------

def sample_real_logs(window_days: int) -> dict:
    cutoff = datetime.now() - timedelta(days=window_days)
    analyzer_log = load_json(WORKSPACE / 'state' / 'message-analyzer-log.json', [])
    if not isinstance(analyzer_log, list):
        analyzer_log = []
    recent = []
    for entry in analyzer_log:
        ts = entry.get('timestamp') or entry.get('ts', '')
        try:
            dt = datetime.fromisoformat(str(ts))
        except Exception:
            recent.append(entry)
            continue
        if dt >= cutoff:
            recent.append(entry)
    intents = [e.get('result', {}).get('intent', {}).get('primary', 'unknown') for e in recent]
    intent_dist = {}
    for i in intents:
        intent_dist[i] = intent_dist.get(i, 0) + 1
    risk_high = sum(1 for e in recent
                    if e.get('result', {}).get('strategy', {}).get('risk_level') == 'high')
    return {
        'real_interaction_count': len(recent),
        'intent_distribution': intent_dist,
        'high_risk_interaction_count': risk_high,
    }


# ---------------------------------------------------------------------------
# P0-2/3  Extended metrics: reasoning store, reflection, quality gate, alerts
# ---------------------------------------------------------------------------

def query_reasoning_store() -> dict:
    if not REASONING_DB.exists():
        return {'total': 0, 'high': 0, 'medium': 0, 'low': 0, 'recent_7d': 0}
    try:
        conn = sqlite3.connect(str(REASONING_DB))
        total = conn.execute('SELECT COUNT(*) FROM reasoning_logs').fetchone()[0]
        high = conn.execute("SELECT COUNT(*) FROM reasoning_logs WHERE confidence='high'").fetchone()[0]
        med = conn.execute("SELECT COUNT(*) FROM reasoning_logs WHERE confidence='medium'").fetchone()[0]
        low = conn.execute("SELECT COUNT(*) FROM reasoning_logs WHERE confidence='low'").fetchone()[0]
        cutoff = (datetime.now() - timedelta(days=7)).isoformat()
        recent = conn.execute('SELECT COUNT(*) FROM reasoning_logs WHERE created_at >= ?', (cutoff,)).fetchone()[0]
        conn.close()
        return {'total': total, 'high': high, 'medium': med, 'low': low, 'recent_7d': recent}
    except Exception:
        return {'total': 0, 'high': 0, 'medium': 0, 'low': 0, 'recent_7d': 0}


def collect_reflection_data() -> dict:
    reports_dir = WORKSPACE / 'state' / 'reflection-reports'
    if not reports_dir.exists():
        return {'report_count': 0, 'latest_report': None}
    reports = sorted(reports_dir.glob('reflection-*.md'))
    return {
        'report_count': len(reports),
        'latest_report': reports[-1].name if reports else None,
    }


def collect_alerts(window_days: int) -> dict:
    alerts = load_jsonl(WORKSPACE / 'state' / 'alerts.jsonl')
    cutoff = datetime.now() - timedelta(days=window_days)
    recent = []
    for a in alerts:
        ts = a.get('ts', '')
        try:
            dt = datetime.fromisoformat(str(ts))
        except Exception:
            continue
        if dt >= cutoff:
            recent.append(a)
    return {'alert_count_in_window': len(recent), 'total_alerts': len(alerts)}


# ---------------------------------------------------------------------------
# P0-5  Time-windowed error filtering
# ---------------------------------------------------------------------------

def collect_errors_windowed(window_days: int) -> dict:
    errors = load_json(WORKSPACE / 'state' / 'error-tracker.json', {'errors': []})
    items = errors.get('errors', [])
    cutoff = datetime.now() - timedelta(days=window_days)
    windowed = []
    for err in items:
        ts = err.get('firstSeen') or err.get('lastSeen', '')
        try:
            dt = datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
            naive = dt.replace(tzinfo=None) if dt.tzinfo else dt
        except Exception:
            windowed.append(err)
            continue
        if naive >= cutoff:
            windowed.append(err)
    total = len(windowed)
    fixed = sum(1 for e in windowed if e.get('fixApplied'))
    verified = sum(1 for e in windowed if e.get('fixVerified'))
    repeat = sum(1 for e in windowed if int(e.get('count', 0)) >= 3)
    hp_open = sum(1 for e in windowed
                  if not e.get('fixVerified') and e.get('priority') in {'P0', 'P1'})
    return {
        'total_errors': total, 'fixed_errors': fixed, 'verified_errors': verified,
        'repeat_errors': repeat, 'high_priority_open': hp_open,
    }


# ---------------------------------------------------------------------------
# Collect all metrics
# ---------------------------------------------------------------------------

def collect_metrics(window_days: int) -> dict:
    cutoff = datetime.now() - timedelta(days=window_days)

    latency_data = load_json(WORKSPACE / 'state' / 'response-latency-metrics.json', {'records': []})
    latencies: list[float] = []
    for item in latency_data.get('records', []):
        try:
            dt = datetime.fromisoformat(str(item.get('timestamp', '')))
        except Exception:
            continue
        if dt >= cutoff and item.get('latency_ms') is not None:
            latencies.append(float(item['latency_ms']))

    err = collect_errors_windowed(window_days)

    pattern_data = load_json(WORKSPACE / 'state' / 'pattern-library.json', {'patterns': []})
    patterns = pattern_data.get('patterns', [])
    promoted = sum(1 for p in patterns if p.get('promoted'))
    high_conf = sum(1 for p in patterns if p.get('confidence') == 'high')

    cron_data = load_json(WORKSPACE / 'state' / 'cron-governor-report.json', {'summary': {}})
    cs = cron_data.get('summary', {})

    bench_rows = load_jsonl(WORKSPACE / 'state' / 'benchmark-results' / 'history.jsonl')
    latest_bench = bench_rows[-1] if bench_rows else {}

    orch_logs = load_json(WORKSPACE / 'state' / 'v5-orchestrator-log.json', [])
    if not isinstance(orch_logs, list):
        orch_logs = []
    fin_logs = load_json(WORKSPACE / 'state' / 'v5-finalize-log.json', [])
    if not isinstance(fin_logs, list):
        fin_logs = []
    rule_cands = load_json(WORKSPACE / 'state' / 'rule-candidates.json', {})
    rule_count = rule_cands.get('count', 0) if isinstance(rule_cands, dict) else len(rule_cands)
    fin_approved = ratio(sum(1 for r in fin_logs if r.get('approved')), len(fin_logs))

    reasoning = query_reasoning_store()
    reflection = collect_reflection_data()
    alerts = collect_alerts(window_days)
    log_sample = sample_real_logs(window_days)

    regression = {}
    try:
        r = run_cmd(['python3', 'scripts/regression-metrics-report.py'], timeout=30)
        if r.returncode == 0 and r.stdout.strip():
            regression = json.loads(r.stdout.strip())
    except Exception:
        pass

    return {
        'latencies': latencies,
        'latency_count': len(latencies),
        'p50_latency_ms': pct(latencies, 0.5),
        'p95_latency_ms': pct(latencies, 0.95),
        **err,
        'promoted_patterns': promoted,
        'high_conf_patterns': high_conf,
        'enabled_jobs': int(cs.get('enabled_jobs', 0)),
        'erroring_jobs': int(cs.get('erroring_jobs', 0)),
        'thin_script_jobs': int(cs.get('thin_script_jobs', 0)),
        'wrapper_needed_jobs': int(cs.get('wrapper_needed_jobs', 0)),
        'latest_benchmark_pass_rate': float(latest_bench.get('pass_rate_pct', 0.0)),
        'orchestrator_log_count': len(orch_logs),
        'finalize_log_count': len(fin_logs),
        'finalize_approved_ratio': fin_approved,
        'rule_candidate_count': rule_count,
        'reasoning_store': reasoning,
        'reflection': reflection,
        'alerts': alerts,
        'log_sample': log_sample,
        'regression': regression,
    }


# ---------------------------------------------------------------------------
# Task score aggregation
# ---------------------------------------------------------------------------

def compute_task_scores(results: list[dict]) -> dict:
    earned = {d: 0.0 for d in ALL_DIMS}
    possible = {d: 0.0 for d in ALL_DIMS}
    for r in results:
        for dim, w in r.get('dimensions', {}).items():
            possible[dim] += float(w)
            if r.get('passed'):
                earned[dim] += float(w)
    return {d: round(earned[d] / possible[d] * 100, 2) if possible[d] > 0 else None
            for d in ALL_DIMS}


# ---------------------------------------------------------------------------
# P1-3  Non-linear latency scoring
# ---------------------------------------------------------------------------

def latency_score(p50: float, p95: float, timeout_rate: float = 0.0) -> float:
    if p50 <= 0 and p95 <= 0:
        return 50.0
    score = 100.0
    if p50 > 1500:
        score -= min(25.0, ((p50 - 1500) / 1000) ** 1.5 * 5)
    if p95 > 5000:
        score -= min(35.0, ((p95 - 5000) / 2000) ** 1.4 * 8)
    score -= min(20.0, timeout_rate * 100)
    return round(clamp(score), 2)


# ---------------------------------------------------------------------------
# P0-4  Unique scoring formulas per dimension
# ---------------------------------------------------------------------------

def merge_scores(task_scores: dict, metrics: dict) -> tuple[dict, dict, list[dict], list[str], list[str]]:
    """Blend task test scores with runtime metrics into per-dimension scores.

    v0.3.0 changes:
    - All inputs normalized to 0-100 before weighting
    - All weights per dimension sum to exactly 1.0
    - Added planning and hallucination_control dimensions
    - Aligned with CLEAR framework (Cost/Latency/Efficacy/Assurance/Reliability)
      and T-Eval (Planning/Reasoning/Retrieval/Understanding/Instruction/Review)
    """
    m: dict[str, float] = {}
    x: dict[str, float] = {}
    evidence: list[dict] = []
    risks: list[str] = []
    recs: list[str] = []

    # --- Derived ratios (all 0.0–1.0) ---
    fix_rate = ratio(metrics['fixed_errors'], metrics['total_errors'])
    verify_rate = ratio(metrics['verified_errors'], max(metrics['fixed_errors'], 1))
    repeat_ratio = ratio(metrics['repeat_errors'], max(metrics['total_errors'], 1))
    promoted_ratio = ratio(metrics['promoted_patterns'], max(metrics['high_conf_patterns'], 1))
    cron_thin = ratio(metrics['thin_script_jobs'], max(metrics['enabled_jobs'], 1))
    cron_err = ratio(metrics['erroring_jobs'], max(metrics['enabled_jobs'], 1))
    bench = metrics['latest_benchmark_pass_rate']
    rs = metrics.get('reasoning_store', {})
    refl = metrics.get('reflection', {})
    alerts = metrics.get('alerts', {})
    log_s = metrics.get('log_sample', {})
    regr = metrics.get('regression', {})
    fin_ratio = metrics['finalize_approved_ratio']
    hp_open_ratio = ratio(metrics['high_priority_open'], max(metrics['total_errors'], 1))
    reasoning_depth = ratio(rs.get('high', 0), max(rs.get('total', 1), 1))

    # --- Normalized building blocks (all 0-100) ---
    n_interaction = min(log_s.get('real_interaction_count', 0), 50) / 50 * 100
    n_reasoning_total = min(rs.get('total', 0), 120) / 120 * 100
    n_reasoning_high = min(rs.get('high', 0), 40) / 40 * 100
    n_reflection = min(refl.get('report_count', 0), 10) / 10 * 100
    n_alerts = min(alerts.get('alert_count_in_window', 0), 30) / 30 * 100
    n_dialogue_int = min(log_s.get('real_interaction_count', 0), 30) / 30 * 100
    n_orch_diversity = min(metrics['orchestrator_log_count'], 10) / 10 * 100
    n_intent_coverage = min(len(log_s.get('intent_distribution', {})), 8) / 8 * 100
    n_rule_candidates = min(metrics.get('rule_candidate_count', 0), 10) / 10 * 100
    n_dup_rate_inv = clamp(100 - regr.get('duplicate_reply_rate_pct', 5) * 10)

    ts_or = lambda dim, fallback: task_scores.get(dim) if task_scores.get(dim) is not None else fallback

    # ===================================================================
    # MAIN DIMENSIONS — weights verified to sum to 1.00
    # ===================================================================

    # 1. Understanding (0.45 + 0.15 + 0.25 + 0.15 = 1.00)
    #    Sources: task tests, benchmark, interaction diversity, intent coverage
    m['understanding'] = round(clamp(
        ts_or('understanding', 60) * 0.45
        + bench * 0.15
        + n_interaction * 0.25
        + n_intent_coverage * 0.15
    ), 2)

    # 2. Analysis (0.40 + 0.15 + 0.20 + 0.15 + 0.10 = 1.00)
    #    Sources: task tests, benchmark, reasoning depth, dup-rate, reasoning total
    m['analysis'] = round(clamp(
        ts_or('analysis', 60) * 0.40
        + bench * 0.15
        + reasoning_depth * 100 * 0.20
        + n_dup_rate_inv * 0.15
        + n_reasoning_total * 0.10
    ), 2)

    # 3. Thinking (0.35 + 0.20 + 0.15 + 0.15 + 0.15 = 1.00)
    #    Sources: task tests, repeat-error control, finalize rate,
    #             reasoning high-conf entries, reflection reports
    m['thinking'] = round(clamp(
        ts_or('thinking', 55) * 0.35
        + (100 - repeat_ratio * 100) * 0.20
        + fin_ratio * 100 * 0.15
        + n_reasoning_high * 0.15
        + n_reflection * 0.15
    ), 2)

    # 4. Reasoning (0.35 + 0.15 + 0.25 + 0.15 + 0.10 = 1.00)
    #    Sources: task tests, benchmark, reasoning depth ratio,
    #             reasoning total, finalize approval
    m['reasoning'] = round(clamp(
        ts_or('reasoning', 60) * 0.35
        + bench * 0.15
        + reasoning_depth * 100 * 0.25
        + n_reasoning_total * 0.15
        + fin_ratio * 100 * 0.10
    ), 2)

    # 5. Self-iteration (0.25 + 0.20 + 0.15 + 0.15 + 0.15 + 0.10 = 1.00)
    #    Sources: task tests, fix rate, verify rate, promoted patterns,
    #             reflection reports, repeat-error decline
    m['self_iteration'] = round(clamp(
        ts_or('self_iteration', 55) * 0.25
        + fix_rate * 100 * 0.20
        + verify_rate * 100 * 0.15
        + promoted_ratio * 100 * 0.15
        + n_reflection * 0.15
        + (100 - repeat_ratio * 100) * 0.10
    ), 2)

    # 6. Dialogue (0.40 + 0.20 + 0.15 + 0.15 + 0.10 = 1.00)
    #    Sources: task tests, interaction volume, benchmark,
    #             high-risk handling, intent diversity
    m['dialogue_communication'] = round(clamp(
        ts_or('dialogue_communication', 65) * 0.40
        + n_dialogue_int * 0.20
        + bench * 0.15
        + (100 if log_s.get('high_risk_interaction_count', 0) > 0 else 50) * 0.15
        + n_intent_coverage * 0.10
    ), 2)

    # 7. Responsiveness — non-linear penalty scoring (unchanged)
    timeout_rate = regr.get('cron_timeout_rate_pct', 0) / 100
    m['responsiveness'] = latency_score(
        metrics['p50_latency_ms'], metrics['p95_latency_ms'], timeout_rate)

    # ===================================================================
    # EXPANDED DIMENSIONS — weights verified to sum to 1.00
    # ===================================================================

    # 8. Robustness (0.30 + 0.20 + 0.20 + 0.15 + 0.15 = 1.00)
    #    Sources: task tests, repeat-error control, cron health,
    #             benchmark, alert frequency (inverted)
    x['robustness'] = round(clamp(
        ts_or('robustness', 55) * 0.30
        + (100 - repeat_ratio * 100) * 0.20
        + (100 - cron_err * 100) * 0.20
        + bench * 0.15
        + (100 - n_alerts) * 0.15
    ), 2)

    # 9. Generalization (0.35 + 0.25 + 0.25 + 0.15 = 1.00)
    #    Sources: task tests, intent coverage, orchestrator diversity, benchmark
    x['generalization'] = round(clamp(
        ts_or('generalization', 60) * 0.35
        + n_intent_coverage * 0.25
        + n_orch_diversity * 0.25
        + bench * 0.15
    ), 2)

    # 10. Planning [NEW] (0.30 + 0.25 + 0.20 + 0.15 + 0.10 = 1.00)
    #     Measures task decomposition, multi-step workflow execution,
    #     dependency management. (CLEAR: Efficacy; T-Eval: Planning)
    #     Sources: task tests, finalize pipeline usage, reasoning total,
    #              orchestrator diversity, reflection (plan-review proxy)
    x['planning'] = round(clamp(
        ts_or('planning', 55) * 0.30
        + fin_ratio * 100 * 0.25
        + n_reasoning_total * 0.20
        + n_orch_diversity * 0.15
        + n_reflection * 0.10
    ), 2)

    # 11. Hallucination Control [NEW] (0.25 + 0.25 + 0.20 + 0.15 + 0.15 = 1.00)
    #     Measures factual accuracy, grounded responses, refusal when
    #     uncertain. (CLEAR: Assurance; Anthropic: safety/trust)
    #     Sources: task tests, reasoning depth (high-conf accuracy),
    #              repeat-error rate (recurring wrong answers), benchmark,
    #              high-priority error control
    x['hallucination_control'] = round(clamp(
        ts_or('hallucination_control', 50) * 0.25
        + reasoning_depth * 100 * 0.25
        + (100 - repeat_ratio * 100) * 0.20
        + bench * 0.15
        + (100 - hp_open_ratio * 100) * 0.15
    ), 2)

    # 12. Policy Adherence (0.35 + 0.25 + 0.20 + 0.20 = 1.00)
    #     Sources: task tests, cron thin-script compliance,
    #              cron health, high-risk confirmation
    x['policy_adherence'] = round(clamp(
        ts_or('policy_adherence', 60) * 0.35
        + cron_thin * 100 * 0.25
        + (100 - cron_err * 100) * 0.20
        + (100 if log_s.get('high_risk_interaction_count', 0) > 0 else 60) * 0.20
    ), 2)

    # 13. Tool Reliability (0.30 + 0.20 + 0.20 + 0.15 + 0.15 = 1.00)
    #     Sources: task tests, benchmark, cron health,
    #              cron thin compliance, rule candidates
    x['tool_reliability'] = round(clamp(
        ts_or('tool_reliability', 60) * 0.30
        + bench * 0.20
        + (100 - cron_err * 100) * 0.20
        + cron_thin * 100 * 0.15
        + n_rule_candidates * 0.15
    ), 2)

    # 14. Calibration (0.30 + 0.25 + 0.20 + 0.25 = 1.00)
    #     Sources: task tests, confidence accuracy composite,
    #              finalize approval, high-priority error control
    cal_conf_accuracy = reasoning_depth * 0.6 + (1 - repeat_ratio) * 0.4
    x['calibration'] = round(clamp(
        ts_or('calibration', 50) * 0.30
        + cal_conf_accuracy * 100 * 0.25
        + fin_ratio * 100 * 0.20
        + (100 - hp_open_ratio * 100) * 0.25
    ), 2)

    # ===================================================================
    # Evidence collection
    # ===================================================================
    evidence.extend([
        {'metric': 'benchmark_pass_rate', 'value': bench},
        {'metric': 'p50_latency_ms', 'value': round(metrics['p50_latency_ms'], 1)},
        {'metric': 'p95_latency_ms', 'value': round(metrics['p95_latency_ms'], 1)},
        {'metric': 'error_fix_rate_pct', 'value': round(fix_rate * 100, 2)},
        {'metric': 'error_verify_rate_pct', 'value': round(verify_rate * 100, 2)},
        {'metric': 'repeat_error_ratio_pct', 'value': round(repeat_ratio * 100, 2)},
        {'metric': 'cron_thin_script_pct', 'value': round(cron_thin * 100, 2)},
        {'metric': 'cron_error_pct', 'value': round(cron_err * 100, 2)},
        {'metric': 'reasoning_store_total', 'value': rs.get('total', 0)},
        {'metric': 'reasoning_high_conf_pct', 'value': round(reasoning_depth * 100, 2)},
        {'metric': 'reflection_reports', 'value': refl.get('report_count', 0)},
        {'metric': 'real_interactions', 'value': log_s.get('real_interaction_count', 0)},
        {'metric': 'alerts_in_window', 'value': alerts.get('alert_count_in_window', 0)},
        {'metric': 'promoted_pattern_ratio_pct', 'value': round(promoted_ratio * 100, 2)},
        {'metric': 'timeout_rate_pct', 'value': round(timeout_rate * 100, 2)},
        {'metric': 'hallucination_proxy_pct', 'value': round((1 - repeat_ratio) * reasoning_depth * 100, 2)},
        {'metric': 'planning_finalize_ratio_pct', 'value': round(fin_ratio * 100, 2)},
    ])

    # ===================================================================
    # Risk flags & upgrade recommendations
    # ===================================================================
    if metrics['high_priority_open'] > 0:
        risks.append(f"仍有 {metrics['high_priority_open']} 个高优先级未验证错误")
        recs.append('优先清理 P0/P1 未验证错误，提升自我迭代与校准分')
    if metrics['erroring_jobs'] > 0:
        risks.append(f"仍有 {metrics['erroring_jobs']} 个出错中的启用 Cron 任务")
        recs.append('修复出错 Cron 任务或将其 thin-script 化')
    if metrics['p95_latency_ms'] > 12000:
        risks.append(f"P95 响应时长 {metrics['p95_latency_ms']:.0f}ms 偏高")
        recs.append('优化 LLM fallback 链路与长任务分流')
    if bench < 80:
        risks.append(f'核心 benchmark 通过率 {bench}% 偏低')
        recs.append('先修复 benchmark 退化，再做新能力开发')
    if metrics['finalize_log_count'] == 0:
        risks.append('finalize 闭环样本不足')
        recs.append('增加 finalize 路径使用，提升 thinking/calibration/planning 可信度')
    if rs.get('total', 0) < 20:
        risks.append('推理知识库条目不足 20 条')
        recs.append('积累更多推理日志，提升 reasoning 维度证据')
    if repeat_ratio > 0.4:
        risks.append(f'重复错误占比 {repeat_ratio*100:.0f}% 偏高')
        recs.append('分析重复错误根因，制定修复优先级')
    if reasoning_depth < 0.3 and rs.get('total', 0) > 10:
        risks.append(f'推理高置信比例仅 {reasoning_depth*100:.0f}%，幻觉风险偏高')
        recs.append('提升推理链质量，增加高置信条目占比以降低幻觉风险')
    if fin_ratio < 0.3 and metrics['finalize_log_count'] > 5:
        risks.append(f'finalize 批准率仅 {fin_ratio*100:.0f}%，规划执行质量待提升')
        recs.append('审视多步任务的分解与执行质量，提升 planning 维度')

    return m, x, evidence, risks, recs


# ---------------------------------------------------------------------------
# Overall scoring
# ---------------------------------------------------------------------------

def weighted_overall(main: dict, expanded: dict, weights: dict) -> float:
    total = 0.0
    for dim, w in weights.get('main', {}).items():
        total += main.get(dim, 0.0) * float(w) / 100.0
    for dim, w in weights.get('expanded', {}).items():
        total += expanded.get(dim, 0.0) * float(w) / 100.0
    return round(total, 2)


def grade_for(score: float) -> str:
    for threshold, grade in [(92, 'A+'), (88, 'A'), (84, 'A-'), (80, 'B+'),
                              (76, 'B'), (72, 'B-'), (68, 'C+'), (64, 'C')]:
        if score >= threshold:
            return grade
    return 'D'


# ---------------------------------------------------------------------------
# P1-2  Fixed confidence interval — uses repeated-run variance
# ---------------------------------------------------------------------------

def compute_ci(overall_scores: list[float], confidence: float = 0.95) -> list[float]:
    if len(overall_scores) <= 1:
        v = overall_scores[0] if overall_scores else 0.0
        return [round(v, 2), round(v, 2)]
    mean = statistics.mean(overall_scores)
    std = statistics.stdev(overall_scores)
    z = 1.96 if confidence >= 0.95 else 1.645
    margin = z * std / math.sqrt(len(overall_scores))
    return [round(clamp(mean - margin), 2), round(clamp(mean + margin), 2)]


def dim_spread(main: dict, expanded: dict) -> float:
    vals = [v for v in list(main.values()) + list(expanded.values()) if v is not None]
    return round(statistics.pvariance(vals), 2) if len(vals) > 1 else 0.0


# ---------------------------------------------------------------------------
# P1-4  Dimension-level trend
# ---------------------------------------------------------------------------

def load_previous_run() -> dict | None:
    runs = sorted(RUNS_DIR.glob('*.json'))
    if not runs:
        return None
    try:
        return json.loads(runs[-1].read_text(encoding='utf-8'))
    except Exception:
        return None


def compute_trend(current: dict, previous: dict | None) -> dict | None:
    if not previous:
        return None
    trend: dict = {
        'overall_delta': round(current['overall_score'] - previous.get('overall_score', 0), 2),
        'previous_generated_at': previous.get('generated_at'),
        'dimension_deltas': {},
    }
    prev_main = previous.get('dimension_scores', {})
    prev_exp = previous.get('expanded_scores', {})
    for dim in MAIN_DIMS:
        old = prev_main.get(dim)
        new = current['dimension_scores'].get(dim)
        if old is not None and new is not None:
            trend['dimension_deltas'][dim] = round(new - old, 2)
    for dim in EXPANDED_DIMS:
        old = prev_exp.get(dim)
        new = current['expanded_scores'].get(dim)
        if old is not None and new is not None:
            trend['dimension_deltas'][dim] = round(new - old, 2)
    declining = [d for d, v in trend['dimension_deltas'].items() if v < -5]
    if declining:
        trend['degradation_alert'] = declining
    return trend


# ---------------------------------------------------------------------------
# P2-1  LLM Judge (optional)
# ---------------------------------------------------------------------------

LLM_JUDGE_PROMPT = """你是 OpenClaw 智能度评估的裁判。请对以下评估结果做主观质量打分。

当前维度评分:
{dim_summary}

关键证据:
{evidence_summary}

风险:
{risk_summary}

请给出 0-100 的主观可信度评分和简短评语（一句话），严格 JSON 输出:
{{"judge_score": <0-100>, "comment": "<评语>"}}"""


def llm_judge(result: dict) -> dict | None:
    api_key = os.environ.get('OPENAI_API_KEY') or os.environ.get('DEEPSEEK_API_KEY', '')
    if not api_key:
        return None
    base = os.environ.get('OPENAI_API_BASE', 'https://api.deepseek.com')
    dim_lines = '\n'.join(f'  {k}: {v}' for k, v in
                          {**result['dimension_scores'], **result['expanded_scores']}.items())
    ev_lines = '\n'.join(f'  {e["metric"]}: {e["value"]}' for e in result['evidence'][:8])
    risk_lines = '\n'.join(f'  - {r}' for r in result['risk_flags']) or '  无'
    prompt = LLM_JUDGE_PROMPT.format(
        dim_summary=dim_lines, evidence_summary=ev_lines, risk_summary=risk_lines)
    payload = json.dumps({
        'model': 'deepseek-chat',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3, 'max_tokens': 200,
    }).encode()
    req = urllib.request.Request(
        f'{base}/v1/chat/completions',
        data=payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read())
        text = body['choices'][0]['message']['content'].strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
        return json.loads(text)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# P1-5  Enhanced Markdown report
# ---------------------------------------------------------------------------

def build_markdown(result: dict) -> str:
    r = result
    grade_emoji = {'A+': '🏆', 'A': '🥇', 'A-': '🥈', 'B+': '🥉',
                   'B': '📈', 'B-': '📊', 'C+': '⚠️', 'C': '⚠️', 'D': '🚨'}
    lines = [
        f"# OpenClaw Smartness Eval — {r['generated_at']}",
        '',
        f"> **{grade_emoji.get(r['grade'], '')} Overall: {r['overall_score']} ({r['grade']})** "
        f"| CI: [{r['confidence_interval'][0]}, {r['confidence_interval'][1]}] "
        f"| mode: {r['mode']} | samples: {r['sample_size']}",
        '',
    ]

    all_dims = {**r['dimension_scores'], **r['expanded_scores']}
    weakest = min(all_dims, key=lambda k: all_dims[k] if all_dims[k] is not None else 999)
    strongest = max(all_dims, key=lambda k: all_dims[k] if all_dims[k] is not None else -1)
    lines.append(f'**最强维度**: {strongest} ({all_dims[strongest]})')
    lines.append(f'**最弱维度**: {weakest} ({all_dims[weakest]}) ← 优先提升')
    lines.append('')

    lines.append('## 主维度评分')
    lines.append('| 维度 | 分数 | 趋势 |')
    lines.append('|------|------|------|')
    trend = r.get('trend_vs_last') or {}
    deltas = trend.get('dimension_deltas', {})
    for k, v in r['dimension_scores'].items():
        d = deltas.get(k)
        arrow = f' ({d:+.1f})' if d is not None else ''
        lines.append(f'| {k} | {v} | {arrow} |')

    lines.extend(['', '## 扩展维度评分'])
    lines.append('| 维度 | 分数 | 趋势 |')
    lines.append('|------|------|------|')
    for k, v in r['expanded_scores'].items():
        d = deltas.get(k)
        arrow = f' ({d:+.1f})' if d is not None else ''
        lines.append(f'| {k} | {v} | {arrow} |')

    if trend:
        lines.extend(['', f"## 趋势 (vs {trend.get('previous_generated_at', '?')})"])
        lines.append(f"- 总分变化: **{trend.get('overall_delta', 0):+.2f}**")
        degrading = trend.get('degradation_alert', [])
        if degrading:
            lines.append(f"- ⚠️ 退化维度: {', '.join(degrading)}")

    lines.extend(['', '## 风险'])
    for item in r.get('risk_flags', []) or ['无']:
        lines.append(f'- {item}')
    lines.extend(['', '## 优化建议'])
    for item in r.get('upgrade_recommendations', []) or ['无']:
        lines.append(f'- {item}')

    lines.extend(['', '## 关键证据'])
    lines.append('| 指标 | 值 |')
    lines.append('|------|----|')
    for e in r['evidence']:
        lines.append(f"| {e['metric']} | {e['value']} |")

    judge = r.get('llm_judge')
    if judge:
        lines.extend([
            '', '## LLM Judge 评价',
            f"- 主观可信度: **{judge.get('judge_score', '?')}**",
            f"- 评语: {judge.get('comment', '')}",
        ])

    passk = r.get('pass_at_k')
    if passk:
        lines.extend(['', '## pass@k 可靠性'])
        for tid, score in passk.items():
            lines.append(f'- {tid}: {score:.2%}')

    _sig = _skill_sig()
    lines.extend([
        '',
        '---',
        f"> Skill: **{_sig['skill']}** | Author: **{_sig['author']}** | "
        f"Integrity: `{_sig['integrity']}`",
        '',
    ])
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='OpenClaw Smartness Eval v0.3.0')
    parser.add_argument('--mode', choices=['quick', 'standard', 'deep'], default='standard')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    parser.add_argument('--compare-last', action='store_true')
    parser.add_argument('--llm-judge', action='store_true', help='Use LLM to give subjective score')
    parser.add_argument('--no-probes', action='store_true', help='Disable anti-gaming probes')
    args = parser.parse_args()

    config = load_json(CONFIG_DIR / 'config.json', {})
    task_suite = load_json(CONFIG_DIR / 'task-suite.json', {'tests': []})
    tests = select_tests(task_suite, args.mode, config)
    repeat_count = int(config.get('modes', {}).get(args.mode, {}).get('repeat_count', 1))
    window_days = int(config.get('modes', {}).get(args.mode, {}).get('window_days', 7))

    if not args.no_probes:
        probe_count = 1 if args.mode == 'quick' else (2 if args.mode == 'standard' else 3)
        tests.extend(generate_probe_tests(probe_count))

    all_results: list[list[dict]] = []
    overall_per_repeat: list[float] = []

    for repeat_idx in range(repeat_count):
        round_results = [evaluate_test(t) for t in tests]
        all_results.append(round_results)

    flat_results = [r for batch in all_results for r in batch]

    results_per_test: dict[str, list[bool]] = {}
    for r in flat_results:
        results_per_test.setdefault(r['id'], []).append(r['passed'])

    task_scores = compute_task_scores(flat_results)
    metrics = collect_metrics(window_days)
    main_scores, expanded_scores, evidence, risks, recs = merge_scores(task_scores, metrics)

    for batch in all_results:
        ts_batch = compute_task_scores(batch)
        m_batch, x_batch, _, _, _ = merge_scores(ts_batch, metrics)
        overall_per_repeat.append(weighted_overall(m_batch, x_batch, config.get('weights', {})))

    overall = weighted_overall(main_scores, expanded_scores, config.get('weights', {}))
    ci = compute_ci(overall_per_repeat if len(overall_per_repeat) > 1 else [overall],
                    config.get('confidence_level', 0.95))
    spread = dim_spread(main_scores, expanded_scores)

    passk = compute_pass_at_k(results_per_test, k=min(repeat_count, 2)) if repeat_count > 1 else None

    generated_at = datetime.now().isoformat(timespec='seconds')
    result: dict = {
        'meta': _skill_sig(),
        'generated_at': generated_at,
        'mode': args.mode,
        'overall_score': overall,
        'grade': grade_for(overall),
        'dimension_scores': main_scores,
        'expanded_scores': expanded_scores,
        'task_scores': task_scores,
        'task_results': flat_results,
        'metrics': {k: v for k, v in metrics.items() if k != 'latencies'},
        'evidence': evidence,
        'risk_flags': risks,
        'upgrade_recommendations': recs,
        'sample_size': len(flat_results),
        'dimension_spread': spread,
        'confidence_level': config.get('confidence_level', 0.95),
        'confidence_interval': ci,
    }

    previous = load_previous_run() if args.compare_last else None
    result['trend_vs_last'] = compute_trend(result, previous)

    if passk:
        result['pass_at_k'] = passk

    if args.llm_judge:
        judge = llm_judge(result)
        if judge:
            result['llm_judge'] = judge

    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    run_path = RUNS_DIR / f'{ts}.json'
    report_path = REPORTS_DIR / f'{datetime.now().strftime("%Y-%m-%d")}.md'
    run_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report_path.write_text(build_markdown(result), encoding='utf-8')

    history_row = {
        'generated_at': generated_at,
        'mode': args.mode,
        'overall_score': overall,
        'grade': result['grade'],
        'dimension_scores': main_scores,
        'expanded_scores': expanded_scores,
        'file': str(run_path),
    }
    with open(STATE_DIR / 'history.jsonl', 'a', encoding='utf-8') as fh:
        fh.write(json.dumps(history_row, ensure_ascii=False) + '\n')

    if args.format == 'markdown':
        print(build_markdown(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
