#!/usr/bin/env python3
"""
Eviction Score Calculator — 基于评分+衰减的淘汰推荐

Usage:
  python3 eviction_score.py <file-path>
  python3 eviction_score.py ~/.claude_code/memory/.learnings/LEARNINGS.md
  python3 eviction_score.py ~/.claude_code/memory/.learnings/ERRORS.md

Reads:
  LEARNINGS.md or ERRORS.md

Algorithm:
  effective_score = vfm_score * 0.5 ^ (days_since_last_seen / 30)
  - Half-life: 30 days (对标 CrewAI)
  - Retrieval hit resets decay (Last-Seen updated by agent)
  - Entries with effective_score < threshold AND age > 14 days → recommend archival

Output:
  按effective_score排序的条目列表，标注是否建议归档
"""

import sys
import os
import re
import math
from datetime import datetime, date

DEFAULT_VFM = 50  # Default VFM score if not recorded
ARCHIVE_THRESHOLD = 25  # Below this effective_score → recommend archive
MIN_AGE_DAYS = 14  # Must be older than this to be eligible for archive
HALF_LIFE_DAYS = 30  # Half-life for decay calculation

def parse_entries(filepath):
    """Parse a markdown file into individual entries."""
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    entries = []
    blocks = re.split(r'^---\s*$', content, flags=re.MULTILINE)
    for block in blocks:
        block = block.strip()
        if block.startswith('## ['):
            entries.append(block)
    return entries

def extract_field(entry, field_name):
    """Extract a field value from an entry block."""
    pattern = rf'\*?\*?{re.escape(field_name)}\*?\*?\s*[:：]\s*(.+)'
    match = re.search(pattern, entry)
    if match:
        return match.group(1).strip()
    return None

def extract_id(entry):
    """Extract the entry ID from the header."""
    match = re.match(r'##\s*\[([A-Z]+-\d{8}-\d+)\]', entry)
    return match.group(1) if match else "UNKNOWN"

def extract_status(entry):
    """Extract entry status."""
    status = extract_field(entry, '状态')
    if status:
        status = re.sub(r'\*+', '', status).strip().lower()
    return status or 'unknown'

def extract_recurrence(entry):
    """Extract recurrence count."""
    rc = extract_field(entry, 'Recurrence-Count')
    if rc:
        match = re.search(r'\d+', rc)
        if match:
            return int(match.group())
    return 1

def extract_last_seen(entry):
    """Extract Last-Seen date."""
    ls = extract_field(entry, 'Last-Seen')
    if not ls:
        ls = extract_field(entry, '记录时间')
    if ls:
        match = re.search(r'(\d{4}-\d{2}-\d{2})', ls)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d').date()
            except ValueError:
                pass
    # Fallback: try to extract from ID (LRN-YYYYMMDD-XXX)
    match = re.search(r'(\d{4})(\d{2})(\d{2})', entry)
    if match:
        try:
            return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            pass
    return date.today()  # If no date found, assume today (don't penalize)

def extract_vfm(entry):
    """Extract VFM score if recorded."""
    vfm = extract_field(entry, 'VFM')
    if vfm:
        match = re.search(r'\d+', vfm)
        if match:
            return int(match.group())
    # Estimate VFM from recurrence
    rc = extract_recurrence(entry)
    return min(rc * 15, 80)  # Rough estimate: more recurrence = higher value

def calculate_effective_score(vfm, last_seen, today=None):
    """Calculate effective score with time decay."""
    if today is None:
        today = date.today()
    days_since = (today - last_seen).days
    if days_since < 0:
        days_since = 0
    decay = math.pow(0.5, days_since / HALF_LIFE_DAYS)
    effective = vfm * decay
    return effective, days_since, decay

def run_eviction(filepath):
    """Main eviction scoring logic."""
    entries = parse_entries(filepath)
    if not entries:
        print(f"📭 文件为空或不存在: {filepath}")
        return

    today = date.today()
    results = []

    for entry in entries:
        eid = extract_id(entry)
        status = extract_status(entry)
        vfm = extract_vfm(entry)
        last_seen = extract_last_seen(entry)
        recurrence = extract_recurrence(entry)

        effective, age_days, decay = calculate_effective_score(vfm, last_seen, today)

        # Determine if entry should be archived
        # Skip promoted and resolved entries (handled separately)
        should_archive = False
        reason = ""

        # 1. Promoted entries → always archive (moved to permanent memory)
        if status in ['promoted']:
            should_archive = True
            reason = "已提升(promoted) → 移出至永久记忆"
        # 2. Resolved + old → archive
        elif status in ['resolved', 'fixed', '已修复'] and age_days > 30:
            should_archive = True
            reason = f"已解决且超过30天({age_days}天) → 移至archive"
        # 3. Recurrence override: high recurrence (≥2) → KEEP regardless of score
        #    Must check BEFORE low-score rule, otherwise elif chain skips it
        elif recurrence >= 2:
            should_archive = False
            reason = f"复现{recurrence}次，保留(跨任务复现覆盖低分)"
        # 4. Single occurrence + old → dormant
        elif recurrence == 1 and age_days > MIN_AGE_DAYS:
            should_archive = True
            reason = f"仅出现1次且超过{MIN_AGE_DAYS}天({age_days}天) → 标记dormant"
        # 5. Low effective score + old enough → archive
        elif effective < ARCHIVE_THRESHOLD and age_days > MIN_AGE_DAYS:
            should_archive = True
            reason = f"有效分数{effective:.1f}<{ARCHIVE_THRESHOLD}且超过{MIN_AGE_DAYS}天({age_days}天)"
        else:
            reason = f"保留(分数{effective:.1f}≥{ARCHIVE_THRESHOLD} 或 年龄{age_days}天<{MIN_AGE_DAYS}天)"

        results.append({
            'id': eid,
            'status': status,
            'vfm': vfm,
            'effective': effective,
            'age_days': age_days,
            'decay': decay,
            'recurrence': recurrence,
            'should_archive': should_archive,
            'reason': reason,
        })

    # Sort by effective score (lowest first = most likely to archive)
    results.sort(key=lambda x: x['effective'])

    # Print report
    total = len(results)
    archive_count = sum(1 for r in results if r['should_archive'])
    keep_count = total - archive_count

    print(f"{'='*70}")
    print(f"Eviction Score Report — {os.path.basename(filepath)}")
    print(f"{'='*70}")
    print(f"")
    print(f"📊 总条目: {total} | 保留: {keep_count} | 建议归档: {archive_count}")
    print(f"📐 评分公式: effective = VFM × 0.5^(age/30)")
    print(f"   归档阈值: effective < {ARCHIVE_THRESHOLD} AND age > {MIN_AGE_DAYS}天")
    print(f"   衰减半衰期: {HALF_LIFE_DAYS}天 (被检索命中时Last-Seen重置)")
    print(f"")

    if results:
        print(f"{'ID':<22} {'状态':<10} {'VFM':>5} {'有效分':>7} {'衰减':>6} {'天数':>5} {'复现':>4} {'建议'}")
        print(f"{'─'*70}")
        for r in results:
            archive_flag = "📦归档" if r['should_archive'] else "✅保留"
            print(f"{r['id']:<22} {r['status']:<10} {r['vfm']:>5} {r['effective']:>7.1f} {r['decay']:>6.3f} {r['age_days']:>5} {r['recurrence']:>4} {archive_flag}")

        print(f"")
        print(f"{'─'*70}")
        print(f"归档原因:")
        for r in results:
            if r['should_archive']:
                print(f"  [{r['id']}] {r['reason']}")

    print(f"{'='*70}")

    # Also output file line count for reference
    with open(filepath, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    print(f"\n📄 文件行数: {line_count}")
    if line_count > 500:
        print(f"⚠️  超过500行参考上限，建议执行归档")
    elif line_count > 300:
        print(f"🟡 接近上限(300/500)，关注增长趋势")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # 无参数时自动检测环境并默认处理 LEARNINGS.md
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, SCRIPT_DIR)
        from env_detect import get_paths
        paths = get_paths()
        print(f"环境: {paths['env']} | 自动选择: LEARNINGS.md")
        print(f"路径: {paths['learnings_md']}")
        print(f"如需处理 ERRORS.md: python3 eviction_score.py {paths['errors_md']}")
        print()
        run_eviction(paths['learnings_md'])
    else:
        filepath = os.path.expanduser(sys.argv[1])
        run_eviction(filepath)
