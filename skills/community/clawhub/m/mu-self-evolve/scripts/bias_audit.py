#!/usr/bin/env python3
"""
Bias Audit — 评委偏差审计

Usage:
  python3 bias_audit.py

Purpose:
  构造已知属性的合成条目，运行淘汰逻辑，验证淘汰机制是否正常工作。
  如果"已知应被淘汰"的条目没有被识别 → 淘汰阈值需要校准。

This uses defect injection testing: inject entries with known expected
outcomes to verify the eviction logic handles each correctly.
Without this test, silent failures can delete valuable memories undetected.

Does NOT modify real files. Uses a temporary file for testing.
"""

import os
import sys
import tempfile
import math
from datetime import date, timedelta

# Import the eviction logic
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from eviction_score import calculate_effective_score, ARCHIVE_THRESHOLD, MIN_AGE_DAYS

def create_test_entries():
    """Create synthetic test entries with known properties."""
    today = date.today()

    # Test Case 1: High VFM, recent, high recurrence → MUST KEEP
    entry_keep = {
        'id': 'TEST-KEEP-001',
        'vfm': 85,
        'last_seen': today - timedelta(days=3),  # Very recent
        'recurrence': 5,
        'expected_archive': False,
        'description': '高频使用+最近活跃 → 必须保留',
    }

    # Test Case 2: Low VFM, old, single occurrence → MUST ARCHIVE
    entry_archive = {
        'id': 'TEST-ARCHIVE-001',
        'vfm': 20,
        'last_seen': today - timedelta(days=45),  # Old
        'recurrence': 1,
        'expected_archive': True,
        'description': '低分+老旧+仅1次 → 必须归档',
    }

    # Test Case 3: Medium VFM, very old, but high recurrence → SHOULD KEEP (recurrence override)
    entry_override = {
        'id': 'TEST-OVERRIDE-001',
        'vfm': 30,
        'last_seen': today - timedelta(days=60),  # Very old
        'recurrence': 4,
        'expected_archive': False,
        'description': '低分但高复现(4次) → 应保留(复现覆盖规则)',
    }

    # Test Case 4: Resolved, old → MUST ARCHIVE
    entry_resolved = {
        'id': 'TEST-RESOLVED-001',
        'vfm': 60,
        'last_seen': today - timedelta(days=35),  # Over 30 days
        'recurrence': 2,
        'status': 'resolved',
        'expected_archive': True,
        'description': '已解决+超30天 → 必须归档',
    }

    # Test Case 5: Low VFM, borderline age (just over MIN_AGE) → SHOULD ARCHIVE
    entry_borderline = {
        'id': 'TEST-BORDER-001',
        'vfm': 15,
        'last_seen': today - timedelta(days=20),  # Over MIN_AGE_DAYS
        'recurrence': 1,
        'expected_archive': True,
        'description': '极低分+超过14天 → 应归档',
    }

    return [entry_keep, entry_archive, entry_override, entry_resolved, entry_borderline]

def simulate_eviction(entry):
    """Simulate the eviction decision for a single entry."""
    today = date.today()
    vfm = entry['vfm']
    last_seen = entry['last_seen']
    recurrence = entry.get('recurrence', 1)
    status = entry.get('status', 'pending')

    effective, age_days, decay = calculate_effective_score(vfm, last_seen, today)

    should_archive = False
    # 1. Promoted → always archive
    if status in ['promoted']:
        should_archive = True
    # 2. Resolved + old → archive
    elif status in ['resolved', 'fixed'] and age_days > 30:
        should_archive = True
    # 3. Recurrence override: high recurrence (≥2) → KEEP (must be before low-score)
    elif recurrence >= 2:
        should_archive = False
    # 4. Single occurrence + old → dormant
    elif recurrence == 1 and age_days > MIN_AGE_DAYS:
        should_archive = True
    # 5. Low effective score + old enough → archive
    elif effective < ARCHIVE_THRESHOLD and age_days > MIN_AGE_DAYS:
        should_archive = True

    return should_archive, effective, age_days

def run_audit():
    """Main audit logic."""
    test_entries = create_test_entries()

    print(f"{'='*70}")
    print(f"Bias Audit Report — 评委偏差审计")
    print(f"{'='*70}")
    print(f"")
    print(f"📋 测试目的: 验证淘汰机制是否能正确识别应被归档的条目")
    print(f"   缺陷注入测试: 验证淘汰逻辑不会误删应保留的条目")
    print(f"")

    passed = 0
    failed = 0

    print(f"{'测试ID':<22} {'期望':>6} {'实际':>6} {'有效分':>7} {'天数':>5} {'结果'}")
    print(f"{'─'*70}")

    for entry in test_entries:
        expected = entry['expected_archive']
        actual, effective, age_days = simulate_eviction(entry)

        if actual == expected:
            result = "✅ PASS"
            passed += 1
        else:
            result = "❌ FAIL"
            failed += 1

        exp_str = "归档" if expected else "保留"
        act_str = "归档" if actual else "保留"

        print(f"{entry['id']:<22} {exp_str:>6} {act_str:>6} {effective:>7.1f} {age_days:>5} {result}")
        print(f"  └ {entry['description']}")

    print(f"{'─'*70}")
    print(f"")
    print(f"📊 通过: {passed}/{len(test_entries)} | 失败: {failed}/{len(test_entries)}")

    if failed > 0:
        print(f"")
        print(f"⚠️  审计未通过！")
        print(f"   淘汰机制存在偏差，以下情况需要校准:")
        for entry in test_entries:
            actual, _, _ = simulate_eviction(entry)
            if actual != entry['expected_archive']:
                print(f"   - {entry['id']}: 期望{'归档' if entry['expected_archive'] else '保留'}，实际{'归档' if actual else '保留'}")
                print(f"     原因: {entry['description']}")
        print(f"")
        print(f"   建议调整:")
        print(f"   - ARCHIVE_THRESHOLD (当前: {ARCHIVE_THRESHOLD})")
        print(f"   - MIN_AGE_DAYS (当前: {MIN_AGE_DAYS})")
        print(f"   - 或检查 recurrence override 逻辑")
    else:
        print(f"")
        print(f"✅ 审计通过！淘汰机制工作正常。")

    print(f"{'='*70}")

if __name__ == '__main__':
    run_audit()
