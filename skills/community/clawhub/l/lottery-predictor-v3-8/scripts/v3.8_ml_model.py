#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球预测技能 V3.8 - 机器学习增强版（优化）

V3.8 改进：
1. ✅ 随机森林预测红球冷热
2. ✅ Gradient Boosting 预测蓝球
3. ✅ 特征工程优化（15 维特征）
4. ✅ 减少训练数据量（最近 500 期）
5. ✅ 简化模型（只用随机森林）

依赖：
    pip install scikit-learn numpy pandas

作者：小四（CFO）🤖
版本：V3.8
创建时间：2026-03-30
"""

import sqlite3
import os
import numpy as np
from collections import Counter
import statistics
from datetime import datetime

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️  机器学习库未安装，使用规则引擎降级模式")
    print("   安装：pip install scikit-learn numpy pandas")

# 数据库路径
DB_PATH = os.path.expanduser('~/.openclaw/workspace/projects/caipiao/data/caipiao.db')

# V3.8 配置（优化版）
CONFIG = {
    'train_window': 2000,  # 使用更多历史数据
    'n_estimators': 100,       # 随机森林树数量（减少）
    'max_depth': 12,           # 最大深度（减少）
    'random_state': 42,
    'ml_weight': 0.4,         # ML 预测权重（40%）
    'rule_weight': 0.6,       # 规则引擎权重（60%）
}

ZONE1 = range(1, 12)
ZONE2 = range(12, 23)
ZONE3 = range(23, 34)

def connect_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库不存在：{DB_PATH}")
        return None
    conn = sqlite3.connect(DB_PATH)
    return conn

def get_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT issue, red1, red2, red3, red4, red5, red6, blue FROM ssq ORDER BY issue")
    return cursor.fetchall()

def extract_features(all_rows, target_num):
    """
    提取特征用于机器学习（15 维）
    """
    # 基础统计
    recent_10 = sum(1 for row in all_rows[-10:] if target_num in row[1:7])
    recent_30 = sum(1 for row in all_rows[-30:] if target_num in row[1:7])
    recent_50 = sum(1 for row in all_rows[-50:] if target_num in row[1:7])
    
    # 遗漏特征
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
    
    # 重复号
    is_repeat = 1 if target_num in all_rows[-1][1:7] else 0
    
    # 连号
    last_reds = list(all_rows[-1][1:7])
    has_consecutive = 1 if any(abs(target_num - r) == 1 for r in last_reds) else 0
    
    # 同尾号
    target_tail = target_num % 10
    same_tail_count = sum(1 for r in last_reds if r % 10 == target_tail)
    
    # 历史频率
    all_reds_flat = []
    for row in all_rows:
        all_reds_flat.extend(row[1:7])
    total_count = sum(1 for n in all_reds_flat if n == target_num)
    freq = total_count / len(all_rows) if all_rows else 0
    
    # 区间特征
    in_zone1 = 1 if target_num in ZONE1 else 0
    in_zone2 = 1 if target_num in ZONE2 else 0
    in_zone3 = 1 if target_num in ZONE3 else 0
    
    # 形态特征
    is_odd = target_num % 2
    is_big = 1 if target_num > 16 else 0
    is_prime = 1 if target_num in [2,3,5,7,11,13,17,19,23,29,31] else 0
    
    return [
        recent_10, recent_30, recent_50,
        current_miss, avg_miss, max_miss,
        is_repeat, has_consecutive, same_tail_count,
        freq,
        in_zone1, in_zone2, in_zone3,
        is_odd, is_big, is_prime
    ]

def prepare_ml_data(all_rows, window=100):
    """准备机器学习训练数据"""
    X = []
    y = []
    
    for i in range(window, len(all_rows)):
        history = all_rows[i-window:i]
        actual = all_rows[i]
        actual_reds = set(actual[1:7])
        
        for num in range(1, 34):
            features = extract_features(history, num)
            label = 1 if num in actual_reds else 0
            X.append(features)
            y.append(label)
    
    return np.array(X), np.array(y)

def train_ml_models(all_rows):
    """训练机器学习模型（简化版）"""
    if not ML_AVAILABLE:
        return None, None, None
    
    print("   正在准备训练数据...")
    # 只用最近 train_window 期
    train_data = all_rows[-CONFIG['train_window']:]
    X, y = prepare_ml_data(train_data, window=100)
    
    print(f"   训练数据形状：X={X.shape}, y={y.shape}")
    print(f"   正样本比例：{sum(y)/len(y)*100:.1f}%")
    
    # 特征缩放
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 红球模型：随机森林（简化）
    print("   正在训练红球模型（随机森林）...")
    rf = RandomForestClassifier(
        n_estimators=CONFIG['n_estimators'],
        max_depth=CONFIG['max_depth'],
        random_state=CONFIG['random_state'],
        class_weight='balanced',
        n_jobs=-1
    )
    
    rf.fit(X_scaled, y)
    train_score = rf.score(X_scaled, y)
    print(f"   红球模型 - 训练准确率：{train_score:.3f}")
    
    # 蓝球模型：Gradient Boosting
    print("   正在训练蓝球模型（Gradient Boosting）...")
    X_blue = []
    y_blue = []
    for i in range(100, len(train_data)):
        history = train_data[i-100:i]
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
    blue_score = gb.score(X_blue, y_blue)
    print(f"   蓝球模型 - 训练准确率：{blue_score:.3f}")
    
    return rf, gb, scaler

def predict_with_ml(all_rows, red_model, blue_model, scaler):
    """使用 ML 模型预测下一期"""
    if not ML_AVAILABLE or red_model is None:
        return None, None
    
    try:
        # 红球预测
        red_probs = []
        for num in range(1, 34):
            features = extract_features(all_rows, num)
            features_scaled = scaler.transform([features])
            prob = red_model.predict_proba(features_scaled)[0][1]
            red_probs.append((num, prob))
        
        red_probs.sort(key=lambda x: x[1], reverse=True)
        predicted_reds = [num for num, prob in red_probs[:6]]
        
        # 蓝球预测
        all_blues = [row[7] for row in all_rows]
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
            prob = blue_model.predict_proba([features])[0][1]
            blue_probs.append((num, prob))
        
        blue_probs.sort(key=lambda x: x[1], reverse=True)
        predicted_blue = blue_probs[0][0]
        
        return sorted(predicted_reds), predicted_blue
    except Exception as e:
        print(f"⚠️  ML 预测失败：{e}，降级到规则引擎")
        return None, None

def calculate_rule_scores(all_rows, last_reds, red_miss):
    """规则引擎评分（V3.7 逻辑）"""
    red_scores = {}
    
    all_reds_flat = []
    for row in all_rows:
        all_reds_flat.extend(row[1:7])
    red_counter = Counter(all_reds_flat)
    
    miss_mean = statistics.mean(list(red_miss.values()))
    
    for num in range(1, 34):
        score = 0
        
        freq = red_counter[num]
        score += freq * 0.3
        
        miss = red_miss.get(num, 0)
        score += min(miss / miss_mean * 10, 15)
        
        if num in last_reds:
            score += 12
        
        recent_10 = sum(1 for row in all_rows[-10:] if num in row[1:7])
        score += recent_10 * 1.5
        
        red_scores[num] = min(score, 100)
    
    return red_scores

def hybrid_predict(all_rows, red_model, blue_model, scaler):
    """混合预测：ML + 规则引擎集成"""
    # ML 预测
    ml_reds, ml_blue = predict_with_ml(all_rows, red_model, blue_model, scaler)
    
    # 规则引擎预测
    last_reds = list(all_rows[-1][1:7])
    red_miss = {}
    for num in range(1, 34):
        for i in range(len(all_rows) - 1, -1, -1):
            if num in all_rows[i][1:7]:
                red_miss[num] = len(all_rows) - 1 - i
                break
    
    rule_red_scores = calculate_rule_scores(all_rows, last_reds, red_miss)
    sorted_rule_reds = sorted(rule_red_scores.items(), key=lambda x: x[1], reverse=True)[:6]
    rule_reds = [num for num, score in sorted_rule_reds]
    
    # 蓝球规则
    all_blues = [row[7] for row in all_rows]
    blue_counter = Counter(all_blues)
    sorted_blues = sorted(blue_counter.items(), key=lambda x: x[1], reverse=True)
    rule_blue = sorted_blues[0][0]
    
    # 集成（投票）
    if ml_reds:
        ml_set = set(ml_reds)
        rule_set = set(rule_reds)
        
        overlap = ml_set & rule_set
        remaining = [num for num in ml_reds if num not in overlap][:6-len(overlap)]
        final_reds = sorted(list(overlap) + remaining)
        
        if len(final_reds) < 6:
            for num in rule_reds:
                if num not in final_reds:
                    final_reds.append(num)
                if len(final_reds) >= 6:
                    break
        
        final_reds = sorted(final_reds)[:6]
    else:
        final_reds = rule_reds
    
    final_blue = ml_blue if ml_blue else rule_blue
    
    return final_reds, final_blue

def main():
    print("=" * 80)
    print("🎰 双色球预测技能 V3.8（机器学习增强版 - 优化）")
    print("=" * 80)
    print()
    
    print("正在连接数据库...")
    conn = connect_db()
    if not conn:
        return
    
    print("正在加载历史数据...")
    all_rows = get_all_data(conn)
    
    if not all_rows:
        print("❌ 无历史数据")
        return
    
    print(f"✅ 加载完成：共 {len(all_rows)} 期数据")
    print()
    
    if ML_AVAILABLE:
        print("🤖 正在训练机器学习模型...")
        print(f"   使用最近 {CONFIG['train_window']} 期数据训练")
        red_model, blue_model, scaler = train_ml_models(all_rows)
        print()
    else:
        red_model, blue_model, scaler = None, None, None
    
    print("正在生成预测...")
    predicted_reds, predicted_blue = hybrid_predict(all_rows, red_model, blue_model, scaler)
    
    print()
    print("=" * 80)
    print("🔮 V3.8 预测结果")
    print("=" * 80)
    print()
    
    last_row = all_rows[-1]
    last_reds = list(last_row[1:7])
    last_blue = last_row[7]
    
    print(f"上期开奖：{' '.join([f'{n:02d}' for n in last_reds])} + {last_blue:02d}")
    print()
    print(f"【红球推荐】{', '.join([f'{n:02d}' for n in predicted_reds])}")
    print(f"【蓝球推荐】{predicted_blue:02d}")
    print()
    
    if ML_AVAILABLE:
        print("💡 说明：")
        print("  - 使用随机森林预测红球")
        print("  - 使用 Gradient Boosting 预测蓝球")
        print("  - 集成规则引擎提高稳定性")
        print("  - 训练数据：最近 500 期")
    else:
        print("⚠️  降级模式：")
        print("  - 机器学习库未安装")
        print("  - 使用规则引擎预测")
    
    print()
    print("=" * 80)
    print("⚠️  预测仅供娱乐参考，请理性购彩！")
    print("=" * 80)
    
    conn.close()

if __name__ == '__main__':
    main()
