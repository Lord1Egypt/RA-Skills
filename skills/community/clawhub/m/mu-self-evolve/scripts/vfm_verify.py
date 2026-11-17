#!/usr/bin/env python3
"""
VFM Verification Script — 验证经验规则的实际效果

Usage:
  python3 vfm_verify.py <pattern-key>
  python3 vfm_verify.py mcp.token_expired

Reads:
  OpenClaw: ~/.openclaw/workspace/.learnings/LEARNINGS.md
  Claude Code:   ~/.claude_code/memory/.learnings/LEARNINGS.md (自动降级)

Output:
  结构化报告：复现次数、跨任务验证、解决率、置信度评分

This script provides DETERMINISTIC verification to complement LLM's VFM scoring.
LLM proposes the rule → this script verifies it with actual data.
"""

import sys
import os
import re
from datetime import datetime, date

# 自动检测环境：OpenClaw 优先，Claude Code 降级
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from env_detect import get_paths

_paths = get_paths()
LEARNINGS_PATH = _paths['learnings_md']
ERRORS_PATH = _paths['errors_md']
_ENV = _paths['env']

def parse_entries(filepath):
    """Parse a markdown file into individual entries."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Entries are separated by --- and start with ## [
    entries = []
    blocks = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    for block in blocks:
        block = block.strip()
        if block.startswith('## ['):
            entries.append(block)
    return entries

def extract_field(entry, field_name):
    """Extract a field value from an entry block."""
    # Match **field_name**: value  or  - field_name: value
    pattern = rf'\*?\*?{re.escape(field_name)}\*?\*?\s*[:：]\s*(.+)'
    match = re.search(pattern, entry)
    if match:
        return match.group(1).strip()
    return None

def extract_id(entry):
    """Extract the entry ID from the header."""
    match = re.match(r'##\s*\[([A-Z]+-\d{8}-\d+)\]', entry)
    if match:
        return match.group(1)
    return "UNKNOWN"

def extract_related_files(entry):
    """Extract related file paths to determine cross-task scope."""
    related = extract_field(entry, '相关文件')
    if not related:
        related = extract_field(entry, '相关文件'.upper())
    if related:
        # Split by comma, return unique paths
        files = [f.strip() for f in related.split(',')]
        return list(set(files))
    return []

def extract_status(entry):
    """Extract entry status."""
    status = extract_field(entry, '状态')
    if status:
        # Normalize: remove markdown bold
        status = re.sub(r'\*+', '', status).strip()
    return status or 'unknown'

def extract_recurrence(entry):
    """Extract recurrence count."""
    rc = extract_field(entry, 'Recurrence-Count')
    if rc:
        # Extract number
        match = re.search(r'\d+', rc)
        if match:
            return int(match.group())
    return 1

def extract_last_seen(entry):
    """Extract Last-Seen date."""
    ls = extract_field(entry, 'Last-Seen')
    if ls:
        # Try to parse date (YYYY-MM-DD)
        match = re.search(r'(\d{4}-\d{2}-\d{2})', ls)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d').date()
            except ValueError:
                pass
    return None

def extract_where(entry):
    """Extract WHERE field (which pipeline stage)."""
    return extract_field(entry, 'WHERE') or '未标注'

def extract_why(entry):
    """Extract WHY field (root cause type)."""
    return extract_field(entry, 'WHY') or '未标注'

def verify_pattern(pattern_key):
    """Main verification logic."""
    learnings = parse_entries(LEARNINGS_PATH)
    errors = parse_entries(ERRORS_PATH)
    all_entries = learnings + errors

    # Find matching entries by Pattern-Key
    matching = []
    for entry in all_entries:
        pk = extract_field(entry, 'Pattern-Key')
        if pk and pattern_key.lower() in pk.lower():
            matching.append(entry)

    if not matching:
        print(f"⚠️  未找到 Pattern-Key 匹配 '{pattern_key}' 的条目")
        print(f"   LEARNINGS.md 条目数: {len(learnings)}")
        print(f"   ERRORS.md 条目数: {len(errors)}")
        print(f"   建议：检查 Pattern-Key 拼写，或该模式尚未被记录")
        return

    # Collect verification metrics
    total_occurrences = len(matching)
    recurrence_counts = [extract_recurrence(e) for e in matching]
    max_recurrence = max(recurrence_counts) if recurrence_counts else 0

    # Cross-task check: collect all unique related files
    all_files = set()
    for e in matching:
        files = extract_related_files(e)
        all_files.update(files)
    cross_task_count = len(all_files)

    # Resolution check: how many entries are resolved?
    statuses = [extract_status(e) for e in matching]
    resolved_count = sum(1 for s in statuses if s.lower() in ['resolved', 'fixed', '已修复'])
    pending_count = sum(1 for s in statuses if s.lower() in ['pending', 'active', 'open'])

    # WHERE×WHY pathology distribution
    where_set = set()
    why_set = set()
    for e in matching:
        where_set.add(extract_where(e))
        why_set.add(extract_why(e))

    # Calculate confidence score (0-100)
    # Factor 1: Recurrence (max 30 pts) — more occurrences = higher confidence
    rec_score = min(max_recurrence * 10, 30)
    # Factor 2: Cross-task (max 30 pts) — spanning more tasks = less likely overfitting
    cross_score = min(cross_task_count * 10, 30)
    # Factor 3: Resolution rate (max 25 pts) — resolved entries prove the rule works
    if total_occurrences > 0:
        resolution_rate = resolved_count / total_occurrences
    else:
        resolution_rate = 0
    res_score = int(resolution_rate * 25)
    # Factor 4: Pathology concentration (max 15 pts) — same WHERE×WHY = stronger pattern
    if len(where_set) == 1 and len(why_set) == 1:
        path_score = 15  # All same pathology
    elif len(where_set) <= 2 and len(why_set) <= 2:
        path_score = 10
    else:
        path_score = 5

    confidence = rec_score + cross_score + res_score + path_score

    # Determine recommendation
    if confidence >= 70:
        recommendation = "✅ 建议提升 — 数据支撑充分"
    elif confidence >= 40:
        recommendation = "🟡 观察中 — 部分指标达标，建议继续积累"
    else:
        recommendation = "🔴 暂不提升 — 数据不足，继续观察"

    # Print report
    print(f"{'='*60}")
    print(f"VFM Verification Report — Pattern-Key: {pattern_key}")
    print(f"{'='*60}")
    print(f"")
    print(f"📊 匹配条目数: {total_occurrences}")
    print(f"📈 最大复现次数: {max_recurrence}")
    print(f"🔗 跨任务数(不同文件): {cross_task_count}")
    print(f"✅ 已解决: {resolved_count} / ⏳ 待处理: {pending_count}")
    print(f"")
    print(f"📍 WHERE (环节): {', '.join(where_set)}")
    print(f"❓ WHY (根因): {', '.join(why_set)}")
    print(f"")
    print(f"{'─'*40}")
    print(f"置信度评分 (0-100):")
    print(f"  复现因子 (max 30): {rec_score}")
    print(f"  跨任务因子 (max 30): {cross_score}")
    print(f"  解决率因子 (max 25): {res_score}")
    print(f"  病理集中因子 (max 15): {path_score}")
    print(f"  ─────────────────────")
    print(f"  总分: {confidence}/100")
    print(f"{'─'*40}")
    print(f"")
    print(f"🎯 建议: {recommendation}")
    print(f"")
    print(f"{'='*60}")

    # List matching entries
    print(f"\n关联条目:")
    for e in matching:
        eid = extract_id(e)
        status = extract_status(e)
        where = extract_where(e)
        why = extract_why(e)
        print(f"  [{eid}] status={status} WHERE={where} WHY={why}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 vfm_verify.py <pattern-key>")
        print("Example: python3 vfm_verify.py mcp.token_expired")
        sys.exit(1)
    verify_pattern(sys.argv[1])
