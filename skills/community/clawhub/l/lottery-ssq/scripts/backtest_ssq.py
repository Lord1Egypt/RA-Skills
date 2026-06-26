#!/usr/bin/env python3
"""
双色球基础回测脚本
用历史开奖数据测试当前选号规则的表现
"""
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / 'config.json'
DATA_PATH = ROOT / 'data' / 'ssq_history.csv'
BACKTEST_DIR = ROOT / 'backtests'


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


def backtest_simple(history, config, window=50):
    """
    简单回测：用前 window 期数据训练，预测下一期
    滑动窗口遍历所有可用期数
    """
    results = []
    for i in range(window, len(history)):
        train_data = history[:i]
        actual = history[i]
        picks = generate_picks(train_data, config)
        match = evaluate_picks(picks, actual['reds'], actual['blue'])
        results.append({
            'draw_id': actual['draw_id'],
            'draw_date': actual['draw_date'],
            'actual_reds': actual['reds'],
            'actual_blue': actual['blue'],
            'best_match': match,
        })
    return results


def generate_picks(history, config):
    """基于历史数据生成 5 注号码（2 主推 +3 备选）"""
    import random
    from collections import Counter

    red_omit = omission_map(history, 33)
    blue_omit = omission_map(history, 16)
    hot_reds, warm_reds, cold_reds, red_freq = hot_warm_cold(history, 33, recent=20, blue=False)
    hot_blues, warm_blues, cold_blues, blue_freq = hot_warm_cold(history, 16, recent=20, blue=True)
    red_omit = omission_map(history, 33)
    blue_omit = omission_map(history, 16)
    red_meta = (hot_reds, warm_reds, cold_reds, red_freq, red_omit)
    blue_meta = (hot_blues, warm_blues, cold_blues, blue_freq, blue_omit)

    pool_size = config['generation']['candidate_pool_size']
    candidates = []
    seen = set()

    while len(candidates) < pool_size:
        reds = tuple(sorted(random.sample(range(1, 34), 6)))
        blue = random.randint(1, 16)
        key = (reds, blue)
        if key in seen:
            continue
        seen.add(key)
        score = score_candidate(list(reds), blue, history, config, red_meta, blue_meta)
        candidates.append({
            'reds': list(reds),
            'blue': blue,
            'score': score,
        })

    candidates.sort(key=lambda x: x['score'], reverse=True)
    main = candidates[:config['generation']['output_main']]
    backup = candidates[config['generation']['output_main']:config['generation']['output_main'] + config['generation']['output_backup']]
    return main + backup


def score_candidate(reds, blue, history, config, red_meta, blue_meta):
    from collections import Counter
    reds = sorted(reds)
    generation = config['generation']
    weights = generation['strategy_weights']
    score = 100.0

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

    groups = consecutive_groups(reds)
    if groups > generation['max_consecutive_groups']:
        score *= weights['consecutive_penalty']

    if history:
        last_reds = set(history[-1]['reds'])
        repeat_count = len(last_reds & set(reds))
        if repeat_count in generation['allow_repeat_from_last_draw']:
            score *= 1.02
        else:
            score *= 0.9

    hot_reds, warm_reds, cold_reds, red_freq, red_omit = red_meta
    hot_blues, warm_blues, cold_blues, blue_freq, blue_omit = blue_meta

    for n in reds:
        if n in hot_reds:
            score *= weights['hot']
        elif n in warm_reds:
            score *= weights['warm']
        else:
            score *= weights['cold']
        if red_omit[n] >= 8:
            score *= weights['omission']

    if blue in hot_blues:
        score *= 1.02
    elif blue in warm_blues:
        score *= 1.05
    else:
        score *= 1.03
    if blue_omit[blue] >= 8:
        score *= 1.05

    return round(score, 4)


def odd_even_split(nums):
    odd = sum(1 for n in nums if n % 2 == 1)
    return [odd, len(nums) - odd]


def zone_of(n):
    if 1 <= n <= 11:
        return 1
    if 12 <= n <= 22:
        return 2
    return 3


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


def hot_warm_cold(history, max_num, recent=20, blue=False):
    pool = []
    for draw in history[-recent:]:
        if blue:
            pool.append(draw['blue'])
        else:
            pool.extend(draw['reds'])
    freq = Counter(pool)
    ranked = sorted(range(1, max_num + 1), key=lambda x: (-freq[x], x))
    hot = set(ranked[: max(1, max_num // 3)])
    cold = set(ranked[-max(1, max_num // 3):])
    warm = set(range(1, max_num + 1)) - hot - cold
    return hot, warm, cold, freq


def evaluate_picks(picks, actual_reds, actual_blue):
    """评估 5 注号码与当期开奖的匹配情况"""
    best = {'red_matches': 0, 'blue_match': False, 'pick_idx': -1}
    for idx, pick in enumerate(picks):
        red_match = len(set(pick['reds']) & set(actual_reds))
        blue_match = pick['blue'] == actual_blue
        if red_match > best['red_matches'] or (red_match == best['red_matches'] and blue_match and not best['blue_match']):
            best = {'red_matches': red_match, 'blue_match': blue_match, 'pick_idx': idx}
    return best


def save_backtest_results(results, config):
    BACKTEST_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    path = BACKTEST_DIR / f'backtest-{ts}.json'

    summary = {
        'total_draws': len(results),
        'red_3_plus': sum(1 for r in results if r['best_match']['red_matches'] >= 3),
        'red_4_plus': sum(1 for r in results if r['best_match']['red_matches'] >= 4),
        'red_5_plus': sum(1 for r in results if r['best_match']['red_matches'] >= 5),
        'red_6': sum(1 for r in results if r['best_match']['red_matches'] == 6),
        'blue_correct': sum(1 for r in results if r['best_match']['blue_match']),
        'red_3_plus_with_blue': sum(1 for r in results if r['best_match']['red_matches'] >= 3 and r['best_match']['blue_match']),
        'red_4_plus_with_blue': sum(1 for r in results if r['best_match']['red_matches'] >= 4 and r['best_match']['blue_match']),
    }

    out = {
        'generated_at': datetime.now().isoformat(timespec='seconds'),
        'config': {
            'output_main': config['generation']['output_main'],
            'output_backup': config['generation']['output_backup'],
        },
        'summary': summary,
        'details': results,
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    return path, summary


def main():
    config = load_config()
    history = load_history()

    if len(history) < 100:
        print(f'历史数据不足 ({len(history)} 期)，无法回测')
        return

    print(f'开始回测，共 {len(history)} 期数据...')
    results = backtest_simple(history, config, window=50)

    path, summary = save_backtest_results(results, config)

    print('\n===== 回测完成 =====')
    print(f'回测期数：{summary["total_draws"]} 期')
    print(f'红球≥3 匹配：{summary["red_3_plus"]} 期 ({summary["red_3_plus"]/summary["total_draws"]*100:.1f}%)')
    print(f'红球≥4 匹配：{summary["red_4_plus"]} 期 ({summary["red_4_plus"]/summary["total_draws"]*100:.1f}%)')
    print(f'红球≥5 匹配：{summary["red_5_plus"]} 期 ({summary["red_5_plus"]/summary["total_draws"]*100:.2f}%)')
    print(f'红球全中 (6): {summary["red_6"]} 期')
    print(f'蓝球命中：{summary["blue_correct"]} 期 ({summary["blue_correct"]/summary["total_draws"]*100:.1f}%)')
    print(f'红≥3+ 蓝中：{summary["red_3_plus_with_blue"]} 期')
    print(f'红≥4+ 蓝中：{summary["red_4_plus_with_blue"]} 期')
    print(f'详细结果：{path}')


if __name__ == '__main__':
    main()
