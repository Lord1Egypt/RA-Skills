#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球预测技能 V3.6
核心预测程序

功能：
1. 读取历史数据
2. 计算各维度评分
3. 生成红球和蓝球推荐
4. 输出 5 组推荐组合

作者：成哥写作模型团队
版本：V3.6
创建时间：2026-03-29
"""

import sqlite3
import os
from collections import Counter
import statistics
import math
import random
from datetime import datetime

# 数据库路径
DB_PATH = os.path.expanduser('~/.openclaw/workspace/projects/caipiao/data/caipiao.db')

# V3.6 权重配置
WEIGHTS = {
    'freq_max': 18,
    'miss_max': 22,
    'repeat_max': 15,
    'recent10_max': 15,
    'recent30_max': 10,
    'consecutive_max': 8,
    'same_tail_max': 7,
    'pair_max': 5,
    'fluctuation': 0.01  # 金手指波动 ±1%
}

def connect_db():
    """连接数据库"""
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库不存在：{DB_PATH}")
        return None
    conn = sqlite3.connect(DB_PATH)
    return conn

def get_data(conn, limit=None):
    """获取历史数据"""
    cursor = conn.cursor()
    if limit:
        cursor.execute("SELECT red1, red2, red3, red4, red5, red6, blue FROM ssq ORDER BY issue DESC LIMIT ?", (limit,))
    else:
        cursor.execute("SELECT red1, red2, red3, red4, red5, red6, blue FROM ssq ORDER BY issue")
    return cursor.fetchall()

def calc_ac(numbers):
    """计算 AC 值（数字复杂度）"""
    diffs = set()
    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            diffs.add(abs(numbers[i] - numbers[j]))
    return len(diffs) - len(numbers) + 1

def calculate_red_scores(all_rows, recent_10, recent_30, last_reds, red_miss, red_counter, tail_counts, pair_numbers, consecutive_bonus):
    """计算红球综合评分"""
    red_scores = {}
    
    # 金手指波动因子
    random.seed(datetime.now().timestamp())
    fluctuation = {
        'freq': random.uniform(1 - WEIGHTS['fluctuation'], 1 + WEIGHTS['fluctuation']),
        'miss': random.uniform(1 - WEIGHTS['fluctuation'], 1 + WEIGHTS['fluctuation']),
        'repeat': random.uniform(1 - WEIGHTS['fluctuation'], 1 + WEIGHTS['fluctuation']),
        'recent10': random.uniform(1 - WEIGHTS['fluctuation'], 1 + WEIGHTS['fluctuation']),
        'recent30': random.uniform(1 - WEIGHTS['fluctuation'], 1 + WEIGHTS['fluctuation']),
        'consecutive': random.uniform(1 - WEIGHTS['fluctuation'], 1 + WEIGHTS['fluctuation']),
        'same_tail': random.uniform(1 - WEIGHTS['fluctuation'], 1 + WEIGHTS['fluctuation']),
        'pair': random.uniform(1 - WEIGHTS['fluctuation'], 1 + WEIGHTS['fluctuation']),
    }
    
    # 计算频率统计
    all_reds_flat = []
    for row in all_rows:
        all_reds_flat.extend(row[:6])
    red_counter_full = Counter(all_reds_flat)
    freq_mean = statistics.mean(list(red_counter_full.values()))
    freq_std = statistics.stdev(list(red_counter_full.values())) if len(red_counter_full) > 1 else 1
    
    # 计算遗漏统计
    miss_mean = statistics.mean(list(red_miss.values()))
    
    for num in range(1, 34):
        score = 0
        
        # 1. 历史频率（正态分布）- 18 分
        freq = red_counter_full[num]
        if freq_std > 0:
            z_score = (freq - freq_mean) / freq_std
            freq_score = (1 / (1 + math.exp(-z_score))) * WEIGHTS['freq_max']
        else:
            freq_score = WEIGHTS['freq_max'] / 2
        score += min(freq_score * fluctuation['freq'], WEIGHTS['freq_max'])
        
        # 2. 遗漏动态 - 22 分
        miss = red_miss.get(num, 0)
        miss_ratio = miss / miss_mean if miss_mean > 0 else 1
        miss_score = min(miss_ratio * 11, WEIGHTS['miss_max'])
        score += min(miss_score * fluctuation['miss'], WEIGHTS['miss_max'])
        
        # 3. 重复号 - 15 分
        repeat_score = WEIGHTS['repeat_max'] if num in last_reds else 0
        score += min(repeat_score * fluctuation['repeat'], WEIGHTS['repeat_max'])
        
        # 4. 近期热度（近 10 期）- 15 分
        recent_10_count = sum(1 for row in recent_10 if num in row[:6])
        recent10_score = (recent_10_count / 10) * WEIGHTS['recent10_max']
        score += min(recent10_score * fluctuation['recent10'], WEIGHTS['recent10_max'])
        
        # 5. 近期趋势（近 30 期）- 10 分
        recent_30_count = sum(1 for row in recent_30 if num in row[:6])
        recent30_score = (recent_30_count / 30) * WEIGHTS['recent30_max']
        score += min(recent30_score * fluctuation['recent30'], WEIGHTS['recent30_max'])
        
        # 6. 连号预测 - 8 分
        consec_score = consecutive_bonus.get(num, 0)
        score += min(consec_score * fluctuation['consecutive'], WEIGHTS['consecutive_max'])
        
        # 7. 同尾预测 - 7 分
        tail = num % 10
        same_tail_score = (5 + tail_counts.get(tail, 0)) if tail in tail_counts else 2
        score += min(same_tail_score * fluctuation['same_tail'], WEIGHTS['same_tail_max'])
        
        # 8. 2 码组合 - 5 分
        pair_score = WEIGHTS['pair_max'] if num in pair_numbers else 2
        score += min(pair_score * fluctuation['pair'], WEIGHTS['pair_max'])
        
        red_scores[num] = min(score, 100)
    
    return red_scores

def calculate_blue_scores(all_blues, blue_miss):
    """计算蓝球综合评分"""
    blue_scores = {}
    blue_counter = Counter(all_blues)
    recent_100_blues = all_blues[-100:] if len(all_blues) >= 100 else all_blues
    recent_100_counter = Counter(recent_100_blues)
    blue_miss_mean = statistics.mean(list(blue_miss.values()))
    
    last_blue = all_blues[-1] if all_blues else 7
    
    for num in range(1, 17):
        score = 0
        
        # 1. 历史热度（40 分）
        hist_count = blue_counter[num]
        max_hist = max(blue_counter.values())
        score += (hist_count / max_hist) * 40
        
        # 2. 近期热度（30 分）
        recent_count = recent_100_counter.get(num, 0)
        max_recent = max(recent_100_counter.values()) if recent_100_counter else 1
        score += (recent_count / max_recent) * 30
        
        # 3. 遗漏回补（20 分）
        miss = blue_miss.get(num, 0)
        if miss > blue_miss_mean * 1.5:
            score += 20
        elif miss > blue_miss_mean:
            score += 15
        else:
            score += 10
        
        # 4. 连号/同尾（10 分）
        if abs(num - last_blue) == 1:
            score += 5
        if num == last_blue or abs(num - last_blue) == 10:
            score += 5
        
        blue_scores[num] = min(score, 100)
    
    return blue_scores

def generate_combos(red_scores, blue_scores, last_reds, top_n=18):
    """生成 5 组推荐组合"""
    sorted_reds = sorted(red_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    sorted_blues = sorted(blue_scores.items(), key=lambda x: x[1], reverse=True)[:4]
    top_12 = [num for num, score in sorted_reds]
    
    combos = []
    combo_names = ["TOP6 直选", "重号优先", "连号防守", "冷热搭配", "均衡型"]
    
    # 组合 1：TOP6 直选
    combo1 = sorted([num for num, score in sorted_reds[:6]])
    combos.append((combo1, combo_names[0]))
    
    # 组合 2：重号优先
    repeat_candidates = [num for num in last_reds if num in top_12][:2]
    combo2 = sorted(repeat_candidates + [num for num, score in sorted_reds if num not in repeat_candidates][:4])
    combos.append((combo2, combo_names[1]))
    
    # 组合 3：连号防守
    consec_candidates = [num for num in top_12 if any(abs(num - last) == 1 for last in last_reds)][:2]
    combo3 = sorted(consec_candidates + [num for num, score in sorted_reds[:8] if num not in consec_candidates][:4])
    combos.append((combo3, combo_names[2]))
    
    # 组合 4：冷热搭配
    hot_reds = [num for num, score in sorted_reds if score >= 45][:3]
    remaining = [num for num, score in sorted_reds if num not in hot_reds]
    combo4 = sorted(hot_reds + remaining[:3])[:6]
    combos.append((combo4, combo_names[3]))
    
    # 组合 5：均衡型
    combo5 = sorted([sorted_reds[i][0] for i in [0, 3, 5, 7, 9, 11]])
    combos.append((combo5, combo_names[4]))
    
    return combos, sorted_blues

def print_report(last_row, red_scores, blue_scores, combos, sorted_blues, red_miss, blue_miss):
    """打印预测报告"""
    last_reds = list(last_row[:6])
    last_blue = last_row[6]
    last_sum = sum(last_reds)
    last_span = max(last_reds) - min(last_reds)
    
    print("=" * 80)
    print("🎰 双色球预测技能 V3.6")
    print("=" * 80)
    print()
    
    print("=" * 80)
    print("📊 一、上期开奖回顾")
    print("=" * 80)
    print(f"【红球】 {' '.join([f'{n:02d}' for n in last_reds])}")
    print(f"【蓝球】 {last_blue:02d}")
    print(f"【和值】 {last_sum}（历史平均 100.9，差值{last_sum-100.9:+.1f}）")
    print(f"【跨度】 {last_span}（历史平均 24.1，差值{last_span-24.1:+.1f}）")
    print(f"【大小比】 {sum(1 for n in last_reds if n<=16)}:{6-sum(1 for n in last_reds if n<=16)}（历史 49:51）")
    print(f"【奇偶比】 {sum(1 for n in last_reds if n%2==1)}:{sum(1 for n in last_reds if n%2==0)}（历史 51:49）")
    print(f"【AC 值】 {calc_ac(last_reds)}（历史平均 6.8）")
    print()
    
    print("=" * 80)
    print("📊 二、遗漏分析")
    print("=" * 80)
    miss_mean = statistics.mean(list(red_miss.values()))
    print(f"【遗漏统计】")
    print(f"  平均遗漏：{miss_mean:.1f}期")
    max_miss_num = max(red_miss.items(), key=lambda x: x[1])
    print(f"  最大遗漏：{max_miss_num[0]:02d}号（{max_miss_num[1]}期）")
    print()
    
    hot_reds = [num for num, miss in red_miss.items() if miss <= 4]
    cold_reds = [num for num, miss in red_miss.items() if miss > 8]
    print(f"【热号 TOP10】（遗漏 0-4 期）")
    hot_sorted = sorted(hot_reds, key=lambda x: red_miss[x])[:10]
    for num in hot_sorted:
        print(f"  {num:02d}号 - 遗漏{red_miss[num]}期", end="  ")
    print("\n")
    
    print(f"【冷号 TOP5】（遗漏>8 期）")
    cold_sorted = sorted(cold_reds, key=lambda x: red_miss[x], reverse=True)[:5]
    for num in cold_sorted:
        print(f"  {num:02d}号 - 遗漏{red_miss[num]}期", end="  ")
    print("\n")
    
    blue_miss_mean = statistics.mean(list(blue_miss.values()))
    print(f"【蓝球遗漏】")
    print(f"  平均遗漏：{blue_miss_mean:.1f}期")
    top3 = sorted(blue_miss.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"  当前遗漏 TOP3：{', '.join([f'{k:02d}号 ({v}期)' for k,v in top3])}")
    print()
    
    print("=" * 80)
    print("💡 三、红球推荐 12 码")
    print("=" * 80)
    sorted_reds = sorted(red_scores.items(), key=lambda x: x[1], reverse=True)[:12]
    for i, (num, score) in enumerate(sorted_reds, 1):
        marks = []
        if num in last_reds:
            marks.append("重")
        if any(abs(num - last) == 1 for last in last_reds):
            marks.append("连")
        if any(num == last - 1 or num == last + 1 for last in last_reds):
            marks.append("边")
        mark_str = " ".join(marks) if marks else ""
        print(f"  {i:2d}. {num:02d}号 - {score:5.1f}分  {mark_str}")
    print()
    
    print("=" * 80)
    print("💡 四、蓝球推荐 4 码")
    print("=" * 80)
    for i, (num, score) in enumerate(sorted_blues, 1):
        print(f"  {i}. {num:02d}号 - {score:.1f}分")
    print()
    
    print("=" * 80)
    print("💡 五、5 组推荐组合")
    print("=" * 80)
    for i, (combo, name) in enumerate(combos, 1):
        zone1 = len([n for n in combo if 1 <= n <= 11])
        zone2 = len([n for n in combo if 12 <= n <= 22])
        zone3 = len([n for n in combo if 23 <= n <= 33])
        small = len([n for n in combo if n <= 16])
        odd = len([n for n in combo if n % 2 == 1])
        sum_val = sum(combo)
        ac_val = calc_ac(combo)
        repeat_count = len([n for n in combo if n in last_reds])
        
        print(f"\n【组合{i}】{name}")
        print(f"  红球：{', '.join([f'{n:02d}' for n in combo])}")
        print(f"  蓝球：{sorted_blues[0][0]:02d} {sorted_blues[1][0]:02d}")
        print(f"  区间比：{zone1}:{zone2}:{zone3}")
        print(f"  大小比：{small}:{6-small}")
        print(f"  奇偶比：{odd}:{6-odd}")
        print(f"  和值：{sum_val}")
        print(f"  AC 值：{ac_val}")
        print(f"  重号：{repeat_count}个")
    print()
    
    print("=" * 80)
    print("⚠️  预测仅供娱乐参考，请理性购彩！")
    print("=" * 80)

def main():
    """主函数"""
    print("正在连接数据库...")
    conn = connect_db()
    if not conn:
        return
    
    print("正在加载历史数据...")
    all_rows = get_data(conn)
    recent_10 = get_data(conn, 10)
    recent_30 = get_data(conn, 30)
    all_blues = [row[6] for row in all_rows]
    
    if not all_rows:
        print("❌ 无历史数据")
        return
    
    last_row = all_rows[-1]
    last_reds = list(last_row[:6])
    
    print("正在计算遗漏...")
    # 计算红球遗漏
    red_miss = {}
    for num in range(1, 34):
        for i in range(len(all_rows) - 1, -1, -1):
            if num in all_rows[i][:6]:
                red_miss[num] = len(all_rows) - 1 - i
                break
    
    # 计算蓝球遗漏
    blue_miss = {}
    for num in range(1, 17):
        for i in range(len(all_blues) - 1, -1, -1):
            if all_blues[i] == num:
                blue_miss[num] = len(all_blues) - 1 - i
                break
    
    print("正在分析尾数...")
    # 尾数统计
    tail_counts = Counter()
    for num in all_rows[-1][:6]:
        tail_counts[num % 10] += 1
    
    print("正在分析连号...")
    # 连号加成
    consecutive_bonus = {}
    for num in last_reds:
        if num - 1 >= 1:
            consecutive_bonus[num - 1] = consecutive_bonus.get(num - 1, 0) + 5
        if num + 1 <= 33:
            consecutive_bonus[num + 1] = consecutive_bonus.get(num + 1, 0) + 5
    
    print("正在分析 2 码组合...")
    # 2 码组合
    pair_counter = Counter()
    for row in all_rows:
        for i in range(len(row[:6])):
            for j in range(i+1, len(row[:6])):
                pair = tuple(sorted([row[i], row[j]]))
                pair_counter[pair] += 1
    top_pairs = pair_counter.most_common(20)
    pair_numbers = set()
    for pair, count in top_pairs:
        pair_numbers.add(pair[0])
        pair_numbers.add(pair[1])
    
    print("正在计算红球评分...")
    red_scores = calculate_red_scores(
        all_rows, recent_10, recent_30, last_reds,
        red_miss, Counter(), tail_counts, pair_numbers, consecutive_bonus
    )
    
    print("正在计算蓝球评分...")
    blue_scores = calculate_blue_scores(all_blues, blue_miss)
    
    print("正在生成推荐组合...")
    combos, sorted_blues = generate_combos(red_scores, blue_scores, last_reds)
    
    print()
    print_report(last_row, red_scores, blue_scores, combos, sorted_blues, red_miss, blue_miss)
    
    conn.close()

if __name__ == '__main__':
    main()
