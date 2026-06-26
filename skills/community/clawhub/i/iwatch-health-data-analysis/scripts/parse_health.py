#!/usr/bin/env python3
"""
Apple Health XML 流式解析器 v2.0
从 export.zip 中提取关键健康指标 → chart_data.json
支持 1-2GB 大文件，512KB 分块流式读取，不全量加载内存。
自动识别 HRV 数据来源，分段标注设备名称。

用法:
    python3 parse_health.py export.zip [output.json]
"""

import zipfile
import re
import json
import sys
import statistics
from collections import defaultdict
from pathlib import Path

# ── 目标指标 ──────────────────────────────────────────────────────────────
TARGET_TYPES = {
    'HKQuantityTypeIdentifierHeartRate',
    'HKQuantityTypeIdentifierHeartRateVariabilitySDNN',
    'HKQuantityTypeIdentifierRestingHeartRate',
    'HKQuantityTypeIdentifierWalkingHeartRateAverage',
    'HKQuantityTypeIdentifierStepCount',
    'HKQuantityTypeIdentifierActiveEnergyBurned',
    'HKQuantityTypeIdentifierBasalEnergyBurned',
    'HKCategoryTypeIdentifierSleepAnalysis',
    'HKQuantityTypeIdentifierVO2Max',
    'HKQuantityTypeIdentifierRespiratoryRate',
    'HKQuantityTypeIdentifierOxygenSaturation',
    'HKQuantityTypeIdentifierBodyMass',
    'HKQuantityTypeIdentifierBodyFatPercentage',
    'HKQuantityTypeIdentifierBloodPressureSystolic',
    'HKQuantityTypeIdentifierBloodPressureDiastolic',
    'HKQuantityTypeIdentifierDistanceWalkingRunning',
    'HKQuantityTypeIdentifierAppleExerciseTime',
    'HKQuantityTypeIdentifierAppleStandTime',
    'HKQuantityTypeIdentifierFlightsClimbed',
}

RECORD_RE = re.compile(r'<Record\s+([^>]+?)/?>', re.DOTALL)
ATTR_RE   = re.compile(r'(\w+)="([^"]*)"')


def parse_zip(zip_path: str) -> dict:
    """流式解析，返回原始 {type: [(date, value, source_name)]}"""
    raw = defaultdict(list)
    count = 0

    with zipfile.ZipFile(zip_path) as zf:
        xml_name = next(
            (n for n in zf.namelist() if n.endswith('export.xml')), None
        )
        if not xml_name:
            raise FileNotFoundError("未找到 export.xml，请确认上传的是 Apple Health 导出的 export.zip")

        with zf.open(xml_name) as f:
            buf = ''
            while True:
                chunk = f.read(512 * 1024).decode('utf-8', errors='replace')
                if not chunk:
                    break
                buf += chunk
                for m in RECORD_RE.finditer(buf):
                    attrs = dict(ATTR_RE.findall(m.group(1)))
                    rtype = attrs.get('type', '')
                    if rtype in TARGET_TYPES:
                        date = attrs.get('startDate', attrs.get('creationDate', ''))[:10]
                        value = attrs.get('value', '')
                        source = attrs.get('sourceName', 'unknown')
                        raw[rtype].append((date, value, source))
                        count += 1
                last = buf.rfind('<Record')
                buf = buf[last:] if last >= 0 else ''

    print(f"[INFO] 解析完成，共 {count:,} 条记录", file=sys.stderr)
    return raw


def to_float(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def monthly_mean(records, start='2010-01-01', source_filter=None):
    """按月聚合均值，可按 source_filter 过滤设备"""
    by_month = defaultdict(list)
    for d, v, src in records:
        val = to_float(v)
        if val is None or d < start:
            continue
        if source_filter and source_filter not in src:
            continue
        by_month[d[:7]].append(val)
    return {m: round(statistics.mean(vs), 2) for m, vs in sorted(by_month.items())}


def daily_sum_monthly_mean(records, start='2010-01-01'):
    """每日求和 → 月度均值（处理多设备重复记录）"""
    daily = defaultdict(float)
    for d, v, _src in records:
        val = to_float(v)
        if val and d >= start:
            daily[d] += val
    by_month = defaultdict(list)
    for d, v in daily.items():
        by_month[d[:7]].append(v)
    return {m: round(statistics.mean(vs)) for m, vs in sorted(by_month.items())}


def detect_hrv_sources(records):
    """
    检测 HRV 数据源，按设备分段。
    返回 {source_name: {'earliest': date, 'latest': date, 'count': n, 'mean': v}}
    """
    by_src = defaultdict(list)
    for d, v, src in records:
        val = to_float(v)
        if val:
            by_src[src].append((d, val))

    result = {}
    for src, items in by_src.items():
        dates = [d for d, _ in items]
        vals  = [v for _, v in items]
        result[src] = {
            'earliest': min(dates),
            'latest':   max(dates),
            'count':    len(items),
            'mean':     round(statistics.mean(vals), 1),
        }
    return result


def build_chart_data(raw: dict) -> dict:
    """将原始记录聚合为图表数据"""

    # HRV：检测设备，主设备 = 数据量最多的那个
    hrv_raw = raw.get('HKQuantityTypeIdentifierHeartRateVariabilitySDNN', [])
    hrv_sources = detect_hrv_sources(hrv_raw)
    if hrv_sources:
        primary_src = max(hrv_sources, key=lambda s: hrv_sources[s]['count'])
    else:
        primary_src = None

    hrv_primary = monthly_mean(hrv_raw, source_filter=primary_src) if primary_src else {}
    hrv_all     = monthly_mean(hrv_raw)  # 包含所有设备（早期稀疏值）

    rhr   = monthly_mean(raw.get('HKQuantityTypeIdentifierRestingHeartRate', []))
    vo2   = monthly_mean(raw.get('HKQuantityTypeIdentifierVO2Max', []))
    spo2  = {m: round(v * 100, 1)
             for m, v in monthly_mean(raw.get('HKQuantityTypeIdentifierOxygenSaturation', [])).items()}
    rr    = monthly_mean(raw.get('HKQuantityTypeIdentifierRespiratoryRate', []))

    steps  = daily_sum_monthly_mean(raw.get('HKQuantityTypeIdentifierStepCount', []))
    ae     = daily_sum_monthly_mean(raw.get('HKQuantityTypeIdentifierActiveEnergyBurned', []))
    bme    = daily_sum_monthly_mean(raw.get('HKQuantityTypeIdentifierBasalEnergyBurned', []))
    dist   = daily_sum_monthly_mean(raw.get('HKQuantityTypeIdentifierDistanceWalkingRunning', []))

    # 体重：原始 lb 值，由 generate_report 按用户设置换算
    bw_raw = monthly_mean(raw.get('HKQuantityTypeIdentifierBodyMass', []))
    bf     = monthly_mean(raw.get('HKQuantityTypeIdentifierBodyFatPercentage', []))

    # 血压
    sbp = monthly_mean(raw.get('HKQuantityTypeIdentifierBloodPressureSystolic', []))
    dbp = monthly_mean(raw.get('HKQuantityTypeIdentifierBloodPressureDiastolic', []))

    # 睡眠
    sleep_monthly = defaultdict(lambda: defaultdict(int))
    for d, v, _src in raw.get('HKCategoryTypeIdentifierSleepAnalysis', []):
        sleep_monthly[d[:7]][v] += 1

    # 合并所有月份
    all_months = sorted(set(
        list(rhr) + list(hrv_primary) + list(vo2) +
        list(steps) + list(sleep_monthly) + list(spo2)
    ))

    result = {}
    for m in all_months:
        sm = sleep_monthly.get(m, {})
        result[m] = {
            # 心血管
            'rhr':           rhr.get(m),
            'hrv':           hrv_primary.get(m),   # 主设备 HRV
            'hrv_all':       hrv_all.get(m),        # 包含早期稀疏值（供参考）
            'vo2':           vo2.get(m),
            # 呼吸
            'spo2':          spo2.get(m),
            'resp_rate':     rr.get(m),
            # 血压
            'sbp':           sbp.get(m),
            'dbp':           dbp.get(m),
            # 活动
            'steps':         steps.get(m),
            'active_kcal':   ae.get(m),
            'basal_kcal':    bme.get(m),
            'distance_km':   round(dist[m] / 1000, 2) if dist.get(m) else None,
            # 体成分（原始单位，待 generate_report 换算）
            'weight_raw':    bw_raw.get(m),
            'body_fat_pct':  round(bf[m], 3) if bf.get(m) else None,
            # 睡眠
            'sleep_deep':    sm.get('HKCategoryValueSleepAnalysisAsleepDeep', 0),
            'sleep_rem':     sm.get('HKCategoryValueSleepAnalysisAsleepREM', 0),
            'sleep_core':    sm.get('HKCategoryValueSleepAnalysisAsleepCore', 0),
            'sleep_awake':   sm.get('HKCategoryValueSleepAnalysisAwake', 0),
            'sleep_inbed':   sm.get('HKCategoryValueSleepAnalysisInBed', 0),
        }

    # 元数据
    meta = {
        'generated_at':  __import__('datetime').datetime.now().isoformat(),
        'months':        len(result),
        'date_range':    [min(result), max(result)] if result else [],
        'hrv_sources':   hrv_sources,
        'hrv_primary_source': primary_src,
    }

    return {'meta': meta, 'data': result}


if __name__ == '__main__':
    zip_path = sys.argv[1] if len(sys.argv) > 1 else 'export.zip'
    out_path = sys.argv[2] if len(sys.argv) > 2 else '/tmp/chart_data.json'

    raw = parse_zip(zip_path)
    output = build_chart_data(raw)
    Path(out_path).write_text(json.dumps(output, ensure_ascii=False, indent=2))

    meta = output['meta']
    print(f"[INFO] 输出 → {out_path}", file=sys.stderr)
    print(f"[INFO] {meta['months']} 个月，{meta['date_range'][0]} → {meta['date_range'][1]}", file=sys.stderr)
    if meta['hrv_sources']:
        print(f"[INFO] HRV 数据源：", file=sys.stderr)
        for src, info in meta['hrv_sources'].items():
            flag = ' ← 主设备' if src == meta['hrv_primary_source'] else ''
            print(f"       [{src}] {info['earliest']}→{info['latest']} n={info['count']} 均值={info['mean']}ms{flag}", file=sys.stderr)
