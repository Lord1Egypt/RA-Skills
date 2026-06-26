#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球 V3.8 模型回测脚本（机器学习增强版）

功能：
1. 回测 V3.8 ML 模型
2. 对比 V3.6 vs V3.7 vs V3.8
3. 统计 ML 模型表现

用法：
    python3 backtest_v3.8.py --periods 3000  # 回测 3000 期
    python3 backtest_v3.8.py --periods 3000 --compare  # 对比所有版本

作者：小四（CFO）🤖
版本：1.0
创建时间：2026-03-30
"""

import sqlite3
import os
import numpy as np
from collections import Counter
import statistics
import argparse
from datetime import datetime

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️  scikit-learn 未安装，无法回测 V3.8")

DB_PATH = os.path.expanduser('~/.openclaw/workspace/projects/caipiao/data/caipiao.db')

CONFIG = {
    'train_window': 800,
    'n_estimators': 50,
    'max_depth': 8,
    'random_state': 42,
}

ZONE1 = range(1, 12)
ZONE2 = range(12, 23)
ZONE3 = range(23, 34)

def connect_db():
    if not os.path.exists(DB_PATH):
        return None
    return sqlite3.connect(DB_PATH)

def get_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT issue, red1, red2, red3, red4, red5, red6, blue FROM ssq ORDER BY issue")
    return cursor.fetchall()

def extract_features(all_rows, target_num):
    recent_10 = sum(1 for row in all_rows[-10:] if target_num in row[1:7])
    recent_30 = sum(1 for row in all_rows[-30:] if target_num in row[1:7])
    recent_50 = sum(1 for row in all_rows[-50:] if target_num in row[1:7])
    
    current_miss = 0
    for i in range(len(all_rows) - 1, -1, -1):
        if target_num in all_rows[i][1:7]:
            current_miss = len(all_rows) - 1 - i
            break
    
    appearances = []
    last_pos = -1
    for i in range(len(all_rows) - 1, -1, -1):
        if target_num in all_rows[i][1:7]:
            if last_pos != -1:
                appearances.append(last_pos - i - 1)
            last_pos = i
    avg_miss = statistics.mean(appearances) if appearances else 10
    max_miss = max(appearances) if appearances else 20
    
    is_repeat = 1 if target_num in all_rows[-1][1:7] else 0
    last_reds = list(all_rows[-1][1:7])
    has_consecutive = 1 if any(abs(target_num - r) == 1 for r in last_reds) else 0
    target_tail = target_num % 10
    same_tail_count = sum(1 for r in last_reds if r % 10 == target_tail)
    
    all_reds_flat = []
    for row in all_rows:
        all_reds_flat.extend(row[1:7])
    total_count = sum(1 for n in all_reds_flat if n == target_num)
    freq = total_count / len(all_rows) if all_rows else 0
    
    in_zone1 = 1 if target_num in ZONE1 else 0
    in_zone2 = 1 if target_num in ZONE2 else 0
    in_zone3 = 1 if target_num in ZONE3 else 0
    is_odd = target_num % 2
    is_big = 1 if target_num > 16 else 0
    is_prime = 1 if target_num in [2,3,5,7,11,13,17,19,23,29,31] else 0
    
    return [
        recent_10, recent_30, recent_50,
        current_miss, avg_miss, max_miss,
        is_repeat, has_consecutive, same_tail_count,
        freq, in_zone1, in_zone2, in_zone3,
        is_odd, is_big, is_prime
    ]

def train_and_predict(all_rows, train_start, train_end):
    """训练模型并预测下一期"""
    if not ML_AVAILABLE:
        return None, None
    
    train_data = all_rows[train_start:train_end]
    if len(train_data) < 150:
        return None, None
    
    # 准备训练数据
    X, y = [], []
    for i in range(CONFIG["train_window"] // 2, len(train_data)):
        history = train_data[i - CONFIG["train_window"] // 2:i]
        actual = train_data[i]
        actual_reds = set(actual[1:7])
        for num in range(1, 34):
            features = extract_features(history, num)
            label = 1 if num in actual_reds else 0
            X.append(features)
            y.append(label)
    
    if len(X) < 100:
        return None, None
    
    X = np.array(X)
    y = np.array(y)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 红球模型
    rf = RandomForestClassifier(
        n_estimators=CONFIG['n_estimators'],
        max_depth=CONFIG['max_depth'],
        random_state=CONFIG['random_state'],
        class_weight='balanced',
        n_jobs=-1
    )
    rf.fit(X_scaled, y)
    
    # 蓝球模型
    X_blue, y_blue = [], []
    for i in range(CONFIG["train_window"] // 2, len(train_data)):
        history = train_data[i - CONFIG["train_window"] // 2:i]
        actual_blue = train_data[i][7]
        all_blues = [row[7] for row in history]
        blue_counter = Counter(all_blues)
        for num in range(1, 17):
            features = [
                blue_counter[num],
                sum(1 for b in all_blues[-10:] if b == num),
                sum(1 for b in all_blues[-30:] if b == num),
                next((j for j in range(len(all_blues)-1, -1, -1) if all_blues[j] == num), 99),
                0
            ]
            X_blue.append(features)
            y_blue.append(1 if num == actual_blue else 0)
    
    X_blue = np.array(X_blue)
    y_blue = np.array(y_blue)
    
    gb = GradientBoostingClassifier(
        n_estimators=30,
        max_depth=4,
        learning_rate=0.1,
        random_state=CONFIG['random_state']
    )
    gb.fit(X_blue, y_blue)
    
    # 预测下一期（train_end）
    test_history = all_rows[train_end-100:train_end]
    
    # 红球预测
    red_probs = []
    for num in range(1, 34):
        features = extract_features(test_history, num)
        features_scaled = scaler.transform([features])
        prob = rf.predict_proba(features_scaled)[0][1]
        red_probs.append((num, prob))
    red_probs.sort(key=lambda x: x[1], reverse=True)
    predicted_reds = sorted([num for num, prob in red_probs[:6]])
    
    # 蓝球预测
    all_blues = [row[7] for row in test_history]
    blue_counter = Counter(all_blues)
    blue_probs = []
    for num in range(1, 17):
        features = [
            blue_counter[num],
            sum(1 for b in all_blues[-10:] if b == num),
            sum(1 for b in all_blues[-30:] if b == num),
            next((j for j in range(len(all_blues)-1, -1, -1) if all_blues[j] == num), 99),
            0
        ]
        prob = gb.predict_proba([features])[0][1]
        blue_probs.append((num, prob))
    blue_probs.sort(key=lambda x: x[1], reverse=True)
    predicted_blue = blue_probs[0][0]
    
    return predicted_reds, predicted_blue

def backtest(periods, compare=False, verbose=False):
    print("=" * 80)
    print("🎰 双色球 V3.8 模型回测（机器学习版）")
    print("=" * 80)
    print()
    
    conn = connect_db()
    if not conn:
        return
    
    print("正在加载历史数据...")
    all_data = get_all_data(conn)
    total_issues = len(all_data)
    print(f"✅ 加载完成：共 {total_issues} 期数据")
    print(f"   期号范围：{all_data[0][0]} - {all_data[-1][0]}")
    print()
    
    if periods > total_issues - 150:
        periods = total_issues - 150
    
    print(f"📊 回测配置：")
    print(f"   回测期数：{periods}")
    print(f"   起始期号：{all_data[150][0]}")
    print(f"   结束期号：{all_data[periods+149][0]}")
    print(f"   训练窗口：滑动 100 期")
    print()
    
    # V3.8 统计
    stats_v38 = {
        'red_6': 0, 'red_5': 0, 'red_4': 0, 'red_3': 0, 'red_2': 0, 'red_1': 0, 'red_0': 0,
        'blue_1': 0, 'blue_0': 0,
        'total_red_hits': 0, 'total_blue_hits': 0,
    }
    
    print("🔄 开始回测 V3.8...")
    print()
    
    for i in range(150, periods + 150):
        train_end = i
        train_start = max(0, train_end - CONFIG['train_window'])
        
        actual_row = all_data[i]
        actual_issue = actual_row[0]
        actual_reds = set(actual_row[1:7])
        actual_blue = actual_row[7]
        
        predicted_reds, predicted_blue = train_and_predict(all_data, train_start, train_end)
        
        if predicted_reds is None:
            continue
        
        predicted_reds_set = set(predicted_reds)
        red_hits = len(predicted_reds_set & actual_reds)
        blue_hit = 1 if predicted_blue == actual_blue else 0
        
        stats_v38[f'red_{red_hits}'] += 1
        stats_v38[f'blue_{blue_hit}'] += 1
        stats_v38['total_red_hits'] += red_hits
        stats_v38['total_blue_hits'] += blue_hit
        
        if verbose and (red_hits >= 4 or blue_hit == 1):
            print(f"【{actual_issue}】红球命中：{red_hits}/6  蓝球：{'✅' if blue_hit else '❌'}")
        
        if (i - 150 + 1) % 500 == 0:
            print(f"   进度：{i - 150 + 1}/{periods} 期 ({(i - 150 + 1) / periods * 100:.1f}%)")
    
    print()
    print("=" * 80)
    print("📊 V3.8 回测结果")
    print("=" * 80)
    print()
    
    print("【V3.8 红球命中分布】")
    for hits in range(6, -1, -1):
        count = stats_v38[f'red_{hits}']
        pct = count / periods * 100 if periods > 0 else 0
        bar = '█' * int(pct / 2)
        print(f"  中{hits}红：{count:4d}期 ({pct:5.2f}%) {bar}")
    
    blue_hit_rate_v38 = stats_v38['blue_1'] / periods * 100 if periods > 0 else 0
    print(f"\n【V3.8 蓝球命中】")
    print(f"  命中：{stats_v38['blue_1']:4d}期 ({blue_hit_rate_v38:5.2f}%)")
    
    avg_red_hits_v38 = stats_v38['total_red_hits'] / periods if periods > 0 else 0
    print(f"\n【V3.8 综合指标】")
    print(f"  平均每期中红球：{avg_red_hits_v38:.2f}个")
    print(f"  红球理论期望：1.09 个")
    print(f"  相对提升：{(avg_red_hits_v38 / 1.09 - 1) * 100:+.1f}%")
    
    # 生成报告
    report_path = os.path.expanduser(f'~/.openclaw/workspace/projects/caipiao/reports/v3.8_backtest_{periods}periods.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 🎯 V3.8 模型回测报告（机器学习版）\n\n")
        f.write(f"**回测时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**回测期数：** {periods} 期\n\n")
        
        f.write(f"## 📊 红球命中分布\n\n")
        f.write(f"| 命中数 | 期数 | 百分比 |\n")
        f.write(f"|--------|------|--------|\n")
        for hits in range(6, -1, -1):
            count = stats_v38[f'red_{hits}']
            pct = count / periods * 100 if periods > 0 else 0
            f.write(f"| {hits}红 | {count} | {pct:.2f}% |\n")
        
        f.write(f"\n## 🔵 蓝球命中\n\n")
        f.write(f"- 命中：{stats_v38['blue_1']}期 ({blue_hit_rate_v38:.2f}%)\n")
        
        f.write(f"\n## 📈 综合指标\n\n")
        f.write(f"- 平均每期中红球：{avg_red_hits_v38:.2f}个\n")
        f.write(f"- 相对提升：{(avg_red_hits_v38 / 1.09 - 1) * 100:+.1f}%\n")
    
    print(f"\n📄 报告已保存：{report_path}")
    
    conn.close()
    
    print("=" * 80)
    print("✅ V3.8 回测完成！")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description='V3.8 模型回测')
    parser.add_argument('--periods', type=int, default=100, help='回测期数')
    parser.add_argument('--compare', action='store_true', help='对比其他版本')
    parser.add_argument('--verbose', action='store_true', help='显示详情')
    args = parser.parse_args()
    
    backtest(args.periods, args.compare, args.verbose)

if __name__ == '__main__':
    main()
