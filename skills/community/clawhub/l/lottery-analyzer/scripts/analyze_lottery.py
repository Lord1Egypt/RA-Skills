#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球/大乐透彩票分析脚本
支持趋势分析、智能推荐、复式生成
"""

import pandas as pd
import json
import random
from collections import Counter
from itertools import combinations
import statistics
import sys

class LotteryAnalyzer:
    def __init__(self, lottery_type='ssq'):
        """
        初始化分析器
        lottery_type: 'ssq' (双色球) 或 'dlt' (大乐透)
        """
        self.lottery_type = lottery_type.lower()

        if self.lottery_type == 'ssq':
            self.red_range = range(1, 34)
            self.blue_range = range(1, 17)
            self.red_count = 6
            self.blue_count = 1
        elif self.lottery_type == 'dlt':
            self.red_range = range(1, 36)
            self.blue_range = range(1, 13)
            self.red_count = 5
            self.blue_count = 2
        else:
            raise ValueError(f"不支持的彩票类型: {lottery_type}")

        self.data = None
        self.analysis_results = {}

    def load_data(self, filepath, has_header=True):
        """加载开奖数据文件 (Excel或CSV)"""
        try:
            if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
                if has_header:
                    self.data = pd.read_excel(filepath, skiprows=1)
                else:
                    self.data = pd.read_excel(filepath)
            elif filepath.endswith('.csv'):
                self.data = pd.read_csv(filepath)
            else:
                raise ValueError("不支持的文件格式，请使用Excel或CSV")

            # 标准化列名
            if self.lottery_type == 'ssq':
                self.data.columns = ['期号', '红1', '红2', '红3', '红4', '红5', '红6', '蓝']
            else:  # dlt
                self.data.columns = ['期号', '前1', '前2', '前3', '前4', '前5', '后1', '后2']

            # 转换并清理数据
            for col in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
            self.data = self.data.dropna().astype(int)

            return True, "数据加载成功"
        except Exception as e:
            return False, f"数据加载失败: {str(e)}"

    def _get_red_columns(self):
        """获取红球/前区列名"""
        if self.lottery_type == 'ssq':
            return ['红1', '红2', '红3', '红4', '红5', '红6']
        else:
            return ['前1', '前2', '前3', '前4', '前5']

    def _get_blue_columns(self):
        """获取蓝球/后区列名"""
        if self.lottery_type == 'ssq':
            return ['蓝']
        else:
            return ['后1', '后2']

    def extract_numbers(self, period_count=None):
        """
        提取号码数据
        period_count: 提取最近N期数据，None表示全部
        """
        if self.data is None:
            return False, "请先加载数据"

        red_cols = self._get_red_columns()
        blue_cols = self._get_blue_columns()

        if period_count:
            data_subset = self.data.head(period_count)
        else:
            data_subset = self.data

        # 提取红球/前区
        self.all_red_numbers = [num for _, row in data_subset[red_cols].iterrows() for num in row.tolist()]
        self.red_freq = Counter(self.all_red_numbers)

        # 提取蓝球/后区
        if self.lottery_type == 'ssq':
            self.all_blue_numbers = data_subset['蓝'].tolist()
        else:
            all_blues = []
            for _, row in data_subset[blue_cols].iterrows():
                all_blues.extend([int(row[blue_cols[0]]), int(row[blue_cols[1]])])
            self.all_blue_numbers = all_blues

        self.blue_freq = Counter(self.all_blue_numbers)

        # 计算和值
        self.draw_sums = [row[red_cols].sum() for _, row in data_subset.iterrows()]

        return True, f"成功提取{len(data_subset)}期数据"

    def analyze_patterns(self, recent_count=10):
        """分析近期走势模式"""
        if self.data is None:
            return False, "请先加载数据"

        red_cols = self._get_red_columns()
        recent_data = self.data.head(recent_count)

        patterns = []
        for _, row in recent_data.iterrows():
            reds = sorted(row[red_cols].tolist())

            # 连号对数
            consecutive = sum(1 for i in range(len(reds)-1) if reds[i+1] - reds[i] == 1)

            # 奇偶比例
            odd_count = sum(1 for n in reds if n % 2 == 1)
            odd_even = f"{odd_count}:{len(reds)-odd_count}"

            # 大小比例
            big_threshold = 17 if self.lottery_type == 'ssq' else 18
            big_count = sum(1 for n in reds if n >= big_threshold)
            big_small = f"{big_count}:{len(reds)-big_count}"

            # 和值区间
            sum_val = sum(reds)
            sum_range_base = (sum_val // 20) * 20 + 1
            sum_range = f"{sum_range_base}-{sum_range_base+19}"

            patterns.append({
                'consecutive': consecutive,
                'odd_even': odd_even,
                'big_small': big_small,
                'sum': sum_val,
                'sum_range': sum_range
            })

        return patterns

    def generate_statistics(self):
        """生成统计数据"""
        if not hasattr(self, 'red_freq'):
            return None

        # 获取热号列表
        hot_reds_list = [n for n, _ in self.red_freq.most_common(15)]
        hot_blues_list = [n for n, _ in self.blue_freq.most_common(5)]

        # 计算红球范围
        red_max = 33 if self.lottery_type == 'ssq' else 35
        red_all = list(range(1, red_max + 1))

        # 计算蓝球范围
        blue_max = 16 if self.lottery_type == 'ssq' else 12
        blue_all = list(range(1, blue_max + 1))

        # 生成冷号列表
        cold_reds_list = sorted([n for n in red_all if n not in hot_reds_list])
        cold_blues_list = sorted([n for n in blue_all if n not in hot_blues_list])

        # 计算统计数据并转换为Python原生类型
        avg_number = statistics.mean(self.all_red_numbers)
        median_val = statistics.median(self.all_red_numbers)
        stdev_red = statistics.stdev(self.all_red_numbers) if len(self.all_red_numbers) > 1 else 0

        avg_sum = statistics.mean(self.draw_sums)
        min_sum = min(self.draw_sums)
        max_sum = max(self.draw_sums)
        stdev_sum = statistics.stdev(self.draw_sums) if len(self.draw_sums) > 1 else 0

        stats = {
            'red': {
                'hot_numbers': hot_reds_list,
                'cold_numbers': cold_reds_list,
                'max_red': red_max,
                'avg_number': float(avg_number),
                'median': float(median_val),
                'stdev': float(stdev_red)
            },
            'blue': {
                'hot_numbers': hot_blues_list,
                'cold_numbers': cold_blues_list,
                'max_blue': blue_max
            },
            'sum': {
                'avg': float(avg_sum),
                'min': float(min_sum),
                'max': float(max_sum),
                'stdev': float(stdev_sum)
            },
            'periods': int(len(self.data))
        }

        return stats

    def recommend_numbers(self, strategy='balanced', format_type='simple'):
        """
        推荐号码
        strategy: 'balanced' (均衡), 'hot' (热号), 'cold' (冷号),
                  'consecutive' (连号), 'segment' (区间)
        format_type: 'simple' (单注), '7+2' (复式), '6+2' (复式)
        """
        period_count = len(self.data) if self.data is not None else 50
        if period_count == 0:
            period_count = 50

        # 获取最近数据统计
        self.extract_numbers(period_count)
        patterns = self.analyze_patterns(10)
        stats = self.generate_statistics()

        hot_reds = stats['red']['hot_numbers']
        cold_reds = stats['red']['cold_numbers']
        hot_blues = stats['blue']['hot_numbers']
        cold_blues = stats['blue']['cold_numbers']

        # 根据策略生成号码
        if strategy == 'balanced':
            # 均衡策略：热冷混合
            reds = hot_reds[:5] + cold_reds[:2]
            if len(hot_blues) > 0 and len(cold_blues) > 0:
                blues = [hot_blues[0], cold_blues[0]]
            else:
                blues = hot_blues[:2]

        elif strategy == 'hot':
            # 热号策略
            reds = hot_reds[:self.red_count + 1]  # 多选一个用于复式
            blues = hot_blues[:2]

        elif strategy == 'cold':
            # 冷号策略
            reds = cold_reds[:self.red_count + 1]
            blues = cold_blues[:2]

        elif strategy == 'consecutive':
            # 连号策略
            base = random.randint(1, max(self.red_range) - 10)
            reds = list(range(base, base + 7))
            if len(hot_blues) > 1:
                blues = [hot_blues[0], hot_blues[1]]
            else:
                blues = [1, 2]

        elif strategy == 'segment':
            # 区间策略：覆盖多个区间
            if self.lottery_type == 'ssq':
                segments = [1, 12, 23]
            else:
                segments = [1, 13, 25]

            reds_part1 = [segments[0] + i for i in range(3)]
            reds_part2 = [segments[1] + i for i in range(2)]
            reds_part3 = [segments[2] + i for i in range(2)]
            reds = reds_part1 + reds_part2 + reds_part3

            if hot_blues:
                blues = [random.choice(hot_blues)]
            else:
                blues = [1]

            if cold_blues:
                blues.append(random.choice(cold_blues))
            else:
                blues.append(10)

        else:
            # 默认均衡策略
            reds = hot_reds[:5] + cold_reds[:2]
            if len(hot_blues) > 0 and len(cold_blues) > 0:
                blues = [hot_blues[0], cold_blues[0]]
            else:
                blues = hot_blues[:2]

        # 调整数量
        reds = sorted(list(set(reds)))[:7]  # 最多7个
        blues = sorted(list(set(blues)))[:2]  # 最多2个

        # 生成推荐结果
        recommendation = {
            'strategy': strategy,
            'lottery_type': '双色球' if self.lottery_type == 'ssq' else '大乐透',
            'red_balls': reds,
            'blue_balls': blues,
            'stats': {
                'sum': sum(reds),
                'odd_even': f"{sum(1 for n in reds if n % 2 == 1)}:{len(reds)-sum(1 for n in reds if n % 2 == 1)}",
                'consecutive_pairs': sum(1 for i in range(len(reds)-1) if abs(reds[i+1] - reds[i]) == 1)
            }
        }

        return recommendation

    def generate_multiple_recommendations(self, count=5, format_type='7+2'):
        """生成多组推荐"""
        strategies = ['balanced', 'hot', 'cold', 'consecutive', 'segment']
        recommendations = []

        for i in range(min(count, len(strategies))):
            rec = self.recommend_numbers(strategy=strategies[i], format_type=format_type)
            rec['group'] = i + 1
            recommendations.append(rec)

        return recommendations

    def save_results(self, filename):
        """保存分析结果到JSON"""
        if not self.analysis_results:
            return False, "没有可保存的结果"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)

        return True, f"结果已保存到 {filename}"


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("用法: python analyze_lottery.py <彩票类型> <数据文件> [格式]")
        print("彩票类型: ssq (双色球) 或 dlt (大乐透)")
        print("格式: simple (单注) 或 7+2 (复式)")
        return

    lottery_type = sys.argv[1]
    data_file = sys.argv[2]
    format_type = sys.argv[3] if len(sys.argv) > 3 else '7+2'

    analyzer = LotteryAnalyzer(lottery_type)

    # 加载数据
    success, msg = analyzer.load_data(data_file)
    if not success:
        print(f"❌ {msg}")
        return

    print(f"✅ {msg}")

    # 提取数据并分析
    analyzer.extract_numbers(50)

    # 生成统计
    stats = analyzer.generate_statistics()
    print(f"\n📊 统计信息 ({len(analyzer.data)}期数据):")
    print(f"  平均和值: {stats['sum']['avg']:.1f}")
    print(f"  和值范围: {stats['sum']['min']} - {stats['sum']['max']}")
    print(f"  热红球(前10): {stats['red']['hot_numbers'][:10]}")
    print(f"  冷红球(前10): {stats['red']['cold_numbers'][:10]}")

    # 生成推荐
    recommendations = analyzer.generate_multiple_recommendations(5, format_type)

    print(f"\n🎯 推荐方案 ({format_type}格式):")
    for rec in recommendations:
        print(f"\n第{rec['group']}组 - {rec['strategy']}")
        print(f"  红球: {' '.join(f'{n:02d}' for n in rec['red_balls'])}")
        print(f"  蓝球: {' '.join(f'{n:02d}' for n in rec['blue_balls'])}")
        print(f"  和值: {rec['stats']['sum']} | 奇偶: {rec['stats']['odd_even']}")

    # 保存结果
    output_file = f'/home/admin/worktemp/lottery_{lottery_type}_analysis.json'
    analyzer.analysis_results = {
        'lottery_type': lottery_type,
        'statistics': stats,
        'recommendations': recommendations
    }
    analyzer.save_results(output_file)
    print(f"\n✅ 完整分析已保存到 {output_file}")


if __name__ == '__main__':
    main()
