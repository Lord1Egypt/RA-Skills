#!/usr/bin/env python3
"""Get vital signs trends and averages."""
import json
import os
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

HEALTH_DIR = os.path.expanduser("~/.openclaw/workspace/memory/health")
VITALS_FILE = os.path.join(HEALTH_DIR, "vitals.json")

def load_vitals():
    if not os.path.exists(VITALS_FILE):
        return {"vitals": {}, "targets": {}}
    with open(VITALS_FILE, 'r') as f:
        return json.load(f)

def get_readings_in_period(readings, days=7):
    """Get readings from last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    return [r for r in readings if datetime.fromisoformat(r['timestamp']) > cutoff]

def analyze_bp(readings):
    """Analyze blood pressure readings."""
    if not readings:
        return None
    
    systolics = [r['systolic'] for r in readings]
    diastolics = [r['diastolic'] for r in readings]
    
    return {
        'avg_systolic': round(sum(systolics) / len(systolics)),
        'avg_diastolic': round(sum(diastolics) / len(diastolics)),
        'min_sys': min(systolics),
        'max_sys': max(systolics),
        'min_dia': min(diastolics),
        'max_dia': max(diastolics),
        'count': len(readings)
    }

def analyze_glucose(readings):
    """Analyze glucose readings."""
    if not readings:
        return None
    
    values = [r['value'] for r in readings]
    fasting = [r['value'] for r in readings if r.get('context') == 'fasting']
    
    result = {
        'avg': round(sum(values) / len(values), 1),
        'min': min(values),
        'max': max(values),
        'count': len(readings)
    }
    
    if fasting:
        result['avg_fasting'] = round(sum(fasting) / len(fasting), 1)
    
    return result

def analyze_weight(readings):
    """Analyze weight readings."""
    if not readings:
        return None
    
    values = [r['value'] for r in readings]
    
    return {
        'latest': values[-1],
        'start': values[0],
        'change': round(values[-1] - values[0], 1),
        'avg': round(sum(values) / len(values), 1),
        'count': len(readings)
    }

def main():
    parser = argparse.ArgumentParser(description='Get vital signs trends')
    parser.add_argument('--type', choices=['bp', 'glucose', 'weight', 'all'],
                        default='all', help='Vital type to analyze')
    parser.add_argument('--period', choices=['week', 'month'],
                        default='week', help='Time period')
    parser.add_argument('--chart', action='store_true',
                        help='Show simple ASCII chart')
    
    args = parser.parse_args()
    
    days = 7 if args.period == 'week' else 30
    
    data = load_vitals()
    vitals = data.get('vitals', {})
    targets = data.get('targets', {})
    
    print(f"\nVITAL SIGNS TREND REPORT")
    print(f"Period: Last {days} days")
    print("=" * 50)
    
    if args.type in ['bp', 'all']:
        bp_readings = get_readings_in_period(vitals.get('bp', []), days)
        if bp_readings:
            analysis = analyze_bp(bp_readings)
            print(f"\n📊 BLOOD PRESSURE")
            print(f"   Average: {analysis['avg_systolic']}/{analysis['avg_diastolic']} mmHg")
            print(f"   Range: {analysis['min_sys']}-{analysis['max_sys']}/{analysis['min_dia']}-{analysis['max_dia']}")
            print(f"   Readings: {analysis['count']}")
            
            bp_target = targets.get('bp', {})
            if bp_target:
                sys_max = bp_target.get('systolic_max', 130)
                dia_max = bp_target.get('diastolic_max', 85)
                above = sum(1 for r in bp_readings 
                          if r['systolic'] > sys_max or r['diastolic'] > dia_max)
                print(f"   Above target (<{sys_max}/{dia_max}): {above} readings")
        else:
            print(f"\n📊 BLOOD PRESSURE: No readings in last {days} days")
    
    if args.type in ['glucose', 'all']:
        glucose_readings = get_readings_in_period(vitals.get('glucose', []), days)
        if glucose_readings:
            analysis = analyze_glucose(glucose_readings)
            print(f"\n📊 BLOOD GLUCOSE")
            print(f"   Average: {analysis['avg']} mg/dL")
            if 'avg_fasting' in analysis:
                print(f"   Avg fasting: {analysis['avg_fasting']} mg/dL")
            print(f"   Range: {analysis['min']}-{analysis['max']}")
            print(f"   Readings: {analysis['count']}")
        else:
            print(f"\n📊 BLOOD GLUCOSE: No readings in last {days} days")
    
    if args.type in ['weight', 'all']:
        weight_readings = get_readings_in_period(vitals.get('weight', []), days)
        if weight_readings:
            analysis = analyze_weight(weight_readings)
            unit = weight_readings[0].get('unit', 'lbs')
            print(f"\n📊 WEIGHT")
            print(f"   Latest: {analysis['latest']} {unit}")
            print(f"   Start of period: {analysis['start']} {unit}")
            change_str = f"+{analysis['change']}" if analysis['change'] > 0 else str(analysis['change'])
            print(f"   Change: {change_str} {unit}")
            print(f"   Readings: {analysis['count']}")
        else:
            print(f"\n📊 WEIGHT: No readings in last {days} days")
    
    print("\n" + "=" * 50)
    print("💡 Discuss trends with your doctor at your next appointment.")

if __name__ == '__main__':
    main()
