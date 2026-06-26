#!/usr/bin/env python3
"""
双色球选号系统 v2
改进点：
- 动态冷热周期（10/20/30 期加权）
- AC 值、极距、尾数和形态筛选
- 蓝球细化（分区 + 奇偶 + 遗漏）
- 多策略支持（稳健/均衡/激进）
- 近期走势动态加权
"""
import csv
import json
import random
from collections import Counter
from datetime import datetime
from pathlib import Path
from itertools import combinations

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / 'config.json'
DATA_PATH = ROOT / 'data' / 'ssq_history.csv'
OUTPUT_DIR = ROOT / 'outputs'


def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_history():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    parsed = []
    for row in rows:
        try:
            reds = sorted([int(row[f'red_{i}']) for i in range(1, 7)])
            blue = int(row['blue_1'])
            parsed.append({
                'draw_id': row['draw_id'],
                'draw_date': row['draw_date'],
                'reds': reds,
                'blue': blue,
            })
        except Exception:
            continue
    return parsed


def zone_of(n):
    if 1 <= n <= 11:
        return 1
    if 12 <= n <= 22:
        return 2
    return 3


def blue_zone_of(n):
    if 1 <= n <= 8:
        return 1
    return 2


def odd_even_split(nums):
    odd = sum(1 for n in nums if n % 2 == 1)
    return [odd, len(nums) - odd]


def zone_split(nums):
    c = Counter(zone_of(n) for n in nums)
    return [c[1], c[2], c[3]]


def consecutive_groups(nums):
    groups = 0
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1] + 1:
            if i == 1 or nums[i - 1] != nums[i - 2] + 1:
                groups += 1
    return groups


def calc_span(nums):
    return max(nums) - min(nums)


def calc_tail_sum(nums):
    return sum(n % 10 for n in nums)


def calc_ac_value(nums):
    """AC 值 = 不同差值个数 - (红球数 - 1)"""
    diffs = set()
    for a, b in combinations(nums, 2):
        diffs.add(abs(a - b))
    return len(diffs) - 5


def omission_map(history, max_num):
    result = {n: 999 for n in range(1, max_num + 1)}
    for idx, draw in enumerate(reversed(history), start=1):
        current = set(draw['reds']) if max_num == 33 else {draw['blue']}
        for n in list(result.keys()):
            if result[n] == 999 and n in current:
                result[n] = idx - 1
    for n, v in result.items():
        if v == 999:
            result[n] = len(history)
    return result


def hot_warm_cold_dynamic(history, max_num, config, blue=False):
    """动态冷热：10/20/30 期加权"""
    hot_period = config['generation'].get('hot_period', 10)
    warm_period = config['generation'].get('warm_period', 20)
    cold_period = config['generation'].get('cold_period', 30)

    hot_pool = []
    warm_pool = []
    cold_pool = []

    for draw in history[-hot_period:]:
        if blue:
            hot_pool.append(draw['blue'])
        else:
            hot_pool.extend(draw['reds'])

    for draw in history[-warm_period:-hot_period] if len(history) > hot_period else []:
        if blue:
            warm_pool.append(draw['blue'])
        else:
            warm_pool.extend(draw['reds'])

    for draw in history[-cold_period:-warm_period] if len(history) > warm_period else []:
        if blue:
            cold_pool.append(draw['blue'])
        else:
            cold_pool.extend(draw['reds'])

    hot_freq = Counter(hot_pool)
    warm_freq = Counter(warm_pool)
    cold_freq = Counter(cold_pool)

    # 综合频率 = 近期×3 + 中期×2 + 远期×1
    combined_freq = {}
    all_nums = set(hot_freq.keys()) | set(warm_freq.keys()) | set(cold_freq.keys())
    for n in all_nums:
        combined_freq[n] = hot_freq.get(n, 0) * 3 + warm_freq.get(n, 0) * 2 + cold_freq.get(n, 0)

    # 补全未出现的号码
    for n in range(1, max_num + 1):
        if n not in combined_freq:
            combined_freq[n] = 0

    ranked = sorted(range(1, max_num + 1), key=lambda x: (-combined_freq.get(x, 0), x))
    hot = set(ranked[: max(1, max_num // 3)])
    cold = set(ranked[-max(1, max_num // 3):])
    warm = set(range(1, max_num + 1)) - hot - cold

    return hot, warm, cold, combined_freq


def get_recent_trends(history, window=10):
    """分析近期走势"""
    if len(history) < window:
        return {'prefer_consecutive': False, 'prefer_repeat': False, 'avg_repeat': 1.5}

    recent = history[-window:]
    consecutive_counts = []
    repeat_counts = []

    for i, draw in enumerate(recent):
        groups = consecutive_groups(draw['reds'])
        consecutive_counts.append(groups)
        if i > 0:
            repeat = len(set(draw['reds']) & set(recent[i-1]['reds']))
            repeat_counts.append(repeat)

    avg_consecutive = sum(consecutive_counts) / len(consecutive_counts)
    avg_repeat = sum(repeat_counts) / len(repeat_counts) if repeat_counts else 1.5

    return {
        'prefer_consecutive': avg_consecutive > 1.0,
        'prefer_repeat': avg_repeat > 1.5,
        'avg_repeat': avg_repeat,
    }


def score_candidate_v2(reds, blue, history, config, red_meta, blue_meta, trends):
    """v2 评分：加入 AC 值、极距、尾数、动态权重"""
    reds = sorted(reds)
    generation = config['generation']
    strategy_name = generation.get('default_strategy', 'balanced')
    weights = generation['strategies'].get(strategy_name, generation['strategies']['balanced'])

    score = 100.0

    # === 结构评分 ===
    oe = odd_even_split(reds)
    if oe in generation['preferred_odd_even']:
        score *= weights['balance']
    else:
        score *= 0.92

    zs = zone_split(reds)
    if zs in generation['preferred_zone_splits']:
        score *= weights['balance']
    elif min(zs) == 0:
        score *= 0.88

    red_sum = sum(reds)
    low, high = generation['sum_range']
    if low <= red_sum <= high:
        score *= 1.08
    else:
        score *= 0.9

    # 连号 - 根据近期走势动态调整
    groups = consecutive_groups(reds)
    max_groups = generation.get('max_consecutive_groups', 2)
    if groups > max_groups:
        score *= weights['consecutive_penalty']
    elif trends.get('prefer_consecutive') and groups >= 1:
        score *= 1.05

    # 重号 - 根据近期走势
    if history:
        last_reds = set(history[-1]['reds'])
        repeat_count = len(last_reds & set(reds))
        avg_repeat = trends.get('avg_repeat', 1.5)
        if abs(repeat_count - avg_repeat) <= 0.5:
            score *= 1.05
        elif repeat_count in generation['allow_repeat_from_last_draw']:
            score *= 1.02
        else:
            score *= 0.9

    # === 形态评分 ===
    span = calc_span(reds)
    span_min = generation.get('span_min', 18)
    span_max = generation.get('span_max', 30)
    if span_min <= span <= span_max:
        score *= 1.05
    else:
        score *= 0.95

    ac = calc_ac_value(reds)
    ac_min = generation.get('ac_min', 4)
    ac_max = generation.get('ac_max', 10)
    if ac_min <= ac <= ac_max:
        score *= 1.05
    else:
        score *= 0.95

    tail_sum = calc_tail_sum(reds)
    tail_range = generation.get('tail_sum_range', [10, 25])
    if tail_range[0] <= tail_sum <= tail_range[1]:
        score *= 1.03

    # === 冷热遗漏评分 ===
    hot_reds, warm_reds, cold_reds, red_freq, red_omit = red_meta
    hot_blues, warm_blues, cold_blues, blue_freq, blue_omit = blue_meta

    for n in reds:
        if n in hot_reds:
            score *= weights['hot']
        elif n in warm_reds:
            score *= weights['warm']
        else:
            score *= weights['cold']

        omit_thresh = generation.get('omission_threshold', 10)
        if red_omit[n] >= omit_thresh:
            score *= weights['omission']

    # 蓝球细化评分
    blue_zone = blue_zone_of(blue)
    blue_odd = blue % 2
    blue_omit_val = blue_omit.get(blue, 0)

    if blue in hot_blues:
        score *= 1.03
    elif blue in warm_blues:
        score *= 1.06
    else:
        score *= 1.02

    if blue_omit_val >= omit_thresh:
        score *= 1.08

    # 蓝球分区偏好
    if blue_zone == 1:
        score *= 1.02
    else:
        score *= 1.01

    # 蓝球奇偶
    if blue_odd == 1:
        score *= 1.01

    return round(score, 4)


def generate_candidates_v2(config, history):
    """v2 生成：扩大候选池，加入形态筛选"""
    red_omit = omission_map(history, 33)
    blue_omit = omission_map(history, 16)
    hot_reds, warm_reds, cold_reds, red_freq = hot_warm_cold_dynamic(history, 33, config, blue=False)
    hot_blues, warm_blues, cold_blues, blue_freq = hot_warm_cold_dynamic(history, 16, config, blue=True)
    red_meta = (hot_reds, warm_reds, cold_reds, red_freq, red_omit)
    blue_meta = (hot_blues, warm_blues, cold_blues, blue_freq, blue_omit)
    trends = get_recent_trends(history, window=10)

    pool_size = config['generation']['candidate_pool_size']
    candidates = []
    seen = set()

    ac_min = config['generation'].get('ac_min', 4)
    ac_max = config['generation'].get('ac_max', 10)
    span_min = config['generation'].get('span_min', 18)
    span_max = config['generation'].get('span_max', 30)

    while len(candidates) < pool_size:
        reds = tuple(sorted(random.sample(range(1, 34), 6)))
        blue = random.randint(1, 16)
        key = (reds, blue)
        if key in seen:
            continue
        seen.add(key)

        # 预筛选：形态阈值
        span = calc_span(list(reds))
        ac = calc_ac_value(list(reds))
        if not (span_min <= span <= span_max):
            continue
        if not (ac_min <= ac <= ac_max):
            continue

        score = score_candidate_v2(list(reds), blue, history, config, red_meta, blue_meta, trends)
        candidates.append({
            'reds': list(reds),
            'blue': blue,
            'score': score,
            'odd_even': odd_even_split(list(reds)),
            'zone_split': zone_split(list(reds)),
            'sum': sum(reds),
            'consecutive_groups': consecutive_groups(list(reds)),
            'span': span,
            'ac': ac,
            'tail_sum': calc_tail_sum(list(reds)),
        })

    candidates.sort(key=lambda x: x['score'], reverse=True)
    return candidates


def save_output(candidates, config):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    out = {
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'lottery': config['name'],
        'main': candidates[:config['generation']['output_main']],
        'backup': candidates[config['generation']['output_main']:config['generation']['output_main'] + config['generation']['output_backup']]
    }
    path = OUTPUT_DIR / f'ssq-picks-{ts}.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return path, out


def fmt_pick_v2(p):
    reds = ' '.join(f'{n:02d}' for n in p['reds'])
    blue = f"{p['blue']:02d}"
    return (f"红球：{reds} | 蓝球：{blue} | 评分：{p['score']} | "
            f"奇偶：{p['odd_even'][0]}:{p['odd_even'][1]} | 分区：{p['zone_split']} | "
            f"和值：{p['sum']} | 极距：{p['span']} | AC：{p['ac']}")


def main():
    config = load_config()
    history = load_history()
    candidates = generate_candidates_v2(config, history)
    path, out = save_output(candidates, config)

    print('双色球选号完成 (v2)')
    print(f'策略：{config["generation"].get("default_strategy", "balanced")}')
    print(f'候选池：{config["generation"]["candidate_pool_size"]} 注')
    print(f'输出文件：{path}')
    print('\n主推:')
    for p in out['main']:
        print('-', fmt_pick_v2(p))
    print('\n备选:')
    for p in out['backup']:
        print('-', fmt_pick_v2(p))


if __name__ == '__main__':
    main()
