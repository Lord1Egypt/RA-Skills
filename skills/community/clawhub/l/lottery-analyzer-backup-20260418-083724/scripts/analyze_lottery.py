#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
彩票分析系统 - 飞书专用版
支持双色球/大乐透
飞书兼容：无特殊字符，纯文本格式

包含功能：
1. 基础统计分析
2. 遗漏分析
3. 走势分析
4. 智能推荐（6种策略）
5. 杀号推荐
6. 胆拖推荐
7. 历史回测
8. 趋势数据生成
9. 完整报告导出
10. 自动保存预测记录
11. 预测历史查询
12. 自动兑奖
13. 中奖统计
"""

import json
import argparse
import sys
import os
import math
import random
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# 设置 Windows 控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 尝试导入pandas
try:
    import pandas as pd
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "请先安装依赖: pip install pandas openpyxl"
    }, ensure_ascii=False))
    sys.exit(1)

# ==================== 配置 ====================

DEFAULT_DATA_PATH = Path(__file__).parent.parent / "data" / "ssq_standard.csv"
REPORTS_DIR = Path(__file__).parent.parent / "reports"
PREDICTIONS_DIR = Path(__file__).parent.parent / "predictions"

# 确保目录存在
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)


class LotteryAnalyzer:
    """彩票分析器 - 完整增强版"""
    
    def __init__(self, lottery_type: str = 'ssq'):
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
            self.name = "双色球"
            self.red_max = 33
            self.blue_max = 16
        elif self.lottery_type == 'dlt':
            self.red_range = range(1, 36)
            self.blue_range = range(1, 13)
            self.red_count = 5
            self.blue_count = 2
            self.name = "大乐透"
            self.red_max = 35
            self.blue_max = 12
        else:
            raise ValueError(f"不支持的彩票类型: {lottery_type}")
        
        self.data = None
        self.analysis_results = {}
        self.miss_stats = {}
        self.trend_data = {}
        self.all_red_numbers = []
        self.all_blue_numbers = []
        self.red_freq = Counter()
        self.blue_freq = Counter()
        self.draw_sums = []
    
    def load_data(self, filepath: str) -> Tuple[bool, str]:
        """加载开奖数据文件"""
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return False, f"数据文件不存在：{filepath}"
            
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
            df = None
            for enc in encodings:
                try:
                    df = pd.read_csv(filepath, encoding=enc)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                return False, "无法识别文件编码，请确保文件为UTF-8或GBK格式"
            
            self.data = df
            
            expected_cols = ['期号', '红1', '红2', '红3', '红4', '红5', '红6', '蓝']
            if len(self.data.columns) >= 8:
                self.data.columns = expected_cols[:len(self.data.columns)]
            else:
                return False, f"数据列数不足，需要至少8列，实际{len(self.data.columns)}列"
            
            for col in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
            self.data = self.data.dropna().astype(int)
            
            if len(self.data) == 0:
                return False, "数据文件为空"
            
            self.data = self.data.sort_values('期号', ascending=False).reset_index(drop=True)
            
            self._calculate_missing()
            
            return True, f"数据加载成功，共 {len(self.data)} 期"
        except Exception as e:
            return False, f"数据加载失败: {str(e)}"
    
    def _calculate_missing(self):
        """计算号码遗漏期数"""
        if self.data is None:
            return
        
        red_cols = self._get_red_columns()
        
        red_missing = {num: 0 for num in self.red_range}
        red_missing_history = []
        
        for idx, row in self.data.iterrows():
            current_reds = set(row[red_cols].tolist())
            for num in self.red_range:
                if num in current_reds:
                    red_missing[num] = 0
                else:
                    red_missing[num] += 1
            red_missing_history.append(red_missing.copy())
        
        blue_missing = {num: 0 for num in self.blue_range}
        blue_missing_history = []
        
        for idx, row in self.data.iterrows():
            current_blues = self._get_current_blues(row)
            
            for num in self.blue_range:
                if num in current_blues:
                    blue_missing[num] = 0
                else:
                    blue_missing[num] += 1
            blue_missing_history.append(blue_missing.copy())
        
        self.miss_stats = {
            'red_current': red_missing,
            'red_history': red_missing_history,
            'blue_current': blue_missing,
            'blue_history': blue_missing_history
        }
    
    def _get_current_blues(self, row) -> set:
        """获取当前行的蓝球"""
        if self.lottery_type == 'ssq':
            return {row['蓝']}
        else:
            blues = set()
            if '后1' in row:
                blues.add(row['后1'])
            if '后2' in row:
                blues.add(row['后2'])
            return blues
    
    def _get_red_columns(self) -> List[str]:
        if self.lottery_type == 'ssq':
            return ['红1', '红2', '红3', '红4', '红5', '红6']
        else:
            return ['前1', '前2', '前3', '前4', '前5']
    
    def _get_blue_columns(self) -> List[str]:
        if self.lottery_type == 'ssq':
            return ['蓝']
        else:
            return ['后1', '后2']
    
    def extract_numbers(self, period_count: Optional[int] = None) -> Tuple[bool, str]:
        """提取号码数据"""
        if self.data is None:
            return False, "请先加载数据"
        
        red_cols = self._get_red_columns()
        blue_cols = self._get_blue_columns()
        
        if period_count:
            data_subset = self.data.head(period_count)
        else:
            data_subset = self.data
        
        self.all_red_numbers = []
        for _, row in data_subset[red_cols].iterrows():
            self.all_red_numbers.extend(row.tolist())
        self.red_freq = Counter(self.all_red_numbers)
        
        self.all_blue_numbers = []
        if self.lottery_type == 'ssq':
            self.all_blue_numbers = data_subset['蓝'].tolist()
        else:
            for _, row in data_subset[blue_cols].iterrows():
                self.all_blue_numbers.extend([row[blue_cols[0]], row[blue_cols[1]]])
        self.blue_freq = Counter(self.all_blue_numbers)
        
        self.draw_sums = [row[red_cols].sum() for _, row in data_subset.iterrows()]
        
        return True, f"成功提取{len(data_subset)}期数据"
    
    def analyze_missing(self) -> Dict:
        """遗漏分析"""
        if not self.miss_stats:
            self._calculate_missing()
        
        red_missing_sorted = sorted(
            self.miss_stats['red_current'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        top_missing_reds = red_missing_sorted[:10]
        
        blue_missing_sorted = sorted(
            self.miss_stats['blue_current'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        top_missing_blues = blue_missing_sorted[:5]
        
        total_periods = len(self.data)
        red_rebound = []
        for num, miss in top_missing_reds[:5]:
            prob = min(0.8, miss / total_periods * 2) if total_periods > 0 else 0.5
            red_rebound.append({
                'number': num,
                'miss': miss,
                'rebound_prob': round(prob * 100, 1)
            })
        
        avg_missing_red = 0
        avg_missing_blue = 0
        if self.miss_stats['red_current']:
            avg_missing_red = sum(self.miss_stats['red_current'].values()) / len(self.miss_stats['red_current'])
        if self.miss_stats['blue_current']:
            avg_missing_blue = sum(self.miss_stats['blue_current'].values()) / len(self.miss_stats['blue_current'])
        
        return {
            'red_top_missing': [[n, m] for n, m in top_missing_reds],
            'blue_top_missing': [[n, m] for n, m in top_missing_blues],
            'red_rebound_candidates': red_rebound,
            'avg_missing_red': round(avg_missing_red, 1),
            'avg_missing_blue': round(avg_missing_blue, 1)
        }
    
    def analyze_patterns(self, recent_count: int = 10) -> Tuple[List, Dict]:
        """分析近期走势模式"""
        if self.data is None:
            return [], {}
        
        red_cols = self._get_red_columns()
        recent_data = self.data.head(recent_count)
        
        patterns = []
        for _, row in recent_data.iterrows():
            reds = sorted(row[red_cols].tolist())
            
            consecutive = sum(1 for i in range(len(reds)-1) if reds[i+1] - reds[i] == 1)
            odd_count = sum(1 for n in reds if n % 2 == 1)
            odd_even = f"{odd_count}:{len(reds)-odd_count}"
            
            big_threshold = 17 if self.lottery_type == 'ssq' else 18
            big_count = sum(1 for n in reds if n >= big_threshold)
            big_small = f"{big_count}:{len(reds)-big_count}"
            
            sum_val = sum(reds)
            
            if self.lottery_type == 'ssq':
                zone1 = len([n for n in reds if 1 <= n <= 11])
                zone2 = len([n for n in reds if 12 <= n <= 22])
                zone3 = len([n for n in reds if 23 <= n <= 33])
                zone_ratio = f"{zone1}:{zone2}:{zone3}"
            else:
                zone1 = len([n for n in reds if 1 <= n <= 12])
                zone2 = len([n for n in reds if 13 <= n <= 24])
                zone3 = len([n for n in reds if 25 <= n <= 35])
                zone_ratio = f"{zone1}:{zone2}:{zone3}"
            
            patterns.append({
                'consecutive': consecutive,
                'odd_even': odd_even,
                'big_small': big_small,
                'sum': sum_val,
                'zone_ratio': zone_ratio
            })
        
        trend = {
            'consecutive_trend': [p['consecutive'] for p in patterns],
            'odd_even_trend': [p['odd_even'] for p in patterns],
            'sum_trend': [p['sum'] for p in patterns]
        }
        
        return patterns, trend
    
    def generate_statistics(self) -> Dict:
        """生成统计数据"""
        if not hasattr(self, 'red_freq') or not self.red_freq:
            self.extract_numbers()
        
        red_all = list(range(1, self.red_max + 1))
        blue_all = list(range(1, self.blue_max + 1))
        
        hot_reds_list = [n for n, _ in self.red_freq.most_common(15)]
        cold_reds_list = sorted([n for n in red_all if n not in hot_reds_list])
        hot_blues_list = [n for n, _ in self.blue_freq.most_common(5)] if self.blue_freq else []
        cold_blues_list = sorted([n for n in blue_all if n not in hot_blues_list])
        
        red_freq_dict = dict(self.red_freq.most_common())
        blue_freq_dict = dict(self.blue_freq.most_common()) if self.blue_freq else {}
        
        avg_number = 0
        median_val = 0
        stdev_red = 0
        if self.all_red_numbers:
            avg_number = sum(self.all_red_numbers) / len(self.all_red_numbers)
            sorted_reds = sorted(self.all_red_numbers)
            median_val = sorted_reds[len(sorted_reds)//2]
            if len(self.all_red_numbers) > 1:
                stdev_red = (sum((x - avg_number) ** 2 for x in self.all_red_numbers) / (len(self.all_red_numbers) - 1)) ** 0.5
        
        avg_sum = 0
        min_sum = 0
        max_sum = 0
        stdev_sum = 0
        if self.draw_sums:
            avg_sum = sum(self.draw_sums) / len(self.draw_sums)
            min_sum = min(self.draw_sums)
            max_sum = max(self.draw_sums)
            if len(self.draw_sums) > 1:
                stdev_sum = (sum((x - avg_sum) ** 2 for x in self.draw_sums) / (len(self.draw_sums) - 1)) ** 0.5
        
        sum_ranges = {
            '80以下': len([s for s in self.draw_sums if s < 80]),
            '80-100': len([s for s in self.draw_sums if 80 <= s < 100]),
            '100-120': len([s for s in self.draw_sums if 100 <= s < 120]),
            '120以上': len([s for s in self.draw_sums if s >= 120])
        }
        
        # 获取最新期号
        latest_issue = None
        if self.data is not None and len(self.data) > 0:
            try:
                latest_issue = int(self.data.iloc[0]['期号'])
            except:
                latest_issue = None
        
        stats = {
            'red': {
                'hot_numbers': hot_reds_list,
                'cold_numbers': cold_reds_list,
                'frequency': red_freq_dict,
                'max_red': self.red_max,
                'avg_number': round(avg_number, 2),
                'median': round(median_val, 2),
                'stdev': round(stdev_red, 2)
            },
            'blue': {
                'hot_numbers': hot_blues_list,
                'cold_numbers': cold_blues_list,
                'frequency': blue_freq_dict,
                'max_blue': self.blue_max
            },
            'sum': {
                'avg': round(avg_sum, 2),
                'min': int(min_sum),
                'max': int(max_sum),
                'stdev': round(stdev_sum, 2),
                'ranges': sum_ranges
            },
            'periods': int(len(self.data)),
            'latest_issue': latest_issue
        }
        
        return stats
    
    def recommend_numbers(self, strategy: str = 'balanced', include_dantuo: bool = False) -> Dict:
        """增强版推荐"""
        period_count = len(self.data) if self.data is not None else 50
        if period_count == 0:
            period_count = 50
        
        self.extract_numbers(period_count)
        patterns, trend = self.analyze_patterns(10)
        stats = self.generate_statistics()
        missing = self.analyze_missing()
        
        hot_reds = stats['red']['hot_numbers']
        cold_reds = stats['red']['cold_numbers']
        hot_blues = stats['blue']['hot_numbers']
        cold_blues = stats['blue']['cold_numbers']
        
        rebound_reds = [item['number'] for item in missing['red_rebound_candidates'][:5]]
        
        if strategy == 'balanced':
            reds = hot_reds[:4] + cold_reds[:3] + rebound_reds[:1]
            reds = list(set(reds))[:7]
            if hot_blues and cold_blues:
                blues = [hot_blues[0], cold_blues[0]]
            else:
                blues = hot_blues[:2] if hot_blues else [1, 2]
        
        elif strategy == 'hot':
            reds = hot_reds[:7]
            blues = hot_blues[:2] if hot_blues else [1, 2]
        
        elif strategy == 'cold':
            reds = cold_reds[:7]
            blues = cold_blues[:2] if cold_blues else [1, 2]
        
        elif strategy == 'missing_rebound':
            reds = rebound_reds[:5] + hot_reds[:2]
            reds = list(set(reds))[:7]
            missing_blues = [item[0] for item in missing['blue_top_missing'][:2]]
            blues = missing_blues if missing_blues else [1, 2]
        
        elif strategy == 'consecutive':
            recent_consecutive = trend['consecutive_trend'][-3:] if trend['consecutive_trend'] else [0]
            if sum(recent_consecutive) > 0:
                base = random.randint(1, self.red_max - 10)
                reds = list(range(base, base + 7))
                reds = [r for r in reds if r <= self.red_max]
            else:
                reds = hot_reds[:7]
            blues = hot_blues[:2] if hot_blues else [1, 2]
        
        elif strategy == 'segment':
            if self.lottery_type == 'ssq':
                segments = [(1, 11), (12, 22), (23, 33)]
            else:
                segments = [(1, 12), (13, 24), (25, 35)]
            
            reds = []
            for start, end in segments:
                segment_nums = [n for n in hot_reds if start <= n <= end]
                reds.extend(segment_nums[:2] if len(segment_nums) >= 2 else segment_nums)
            reds = sorted(list(set(reds)))[:7]
            blues = hot_blues[:2] if hot_blues else [1, 2]
        
        else:
            reds = hot_reds[:4] + cold_reds[:3]
            reds = sorted(list(set(reds)))[:7]
            blues = hot_blues[:2] if hot_blues else [1, 2]
        
        reds = sorted(list(set(reds)))[:7]
        if len(reds) < 6:
            need = 6 - len(reds)
            candidates = [n for n in hot_reds if n not in reds]
            reds.extend(candidates[:need])
            reds = sorted(list(set(reds)))
        
        blues = sorted(list(set(blues)))[:2]
        if len(blues) < 1:
            blues = [1]
        
        sum_val = sum(reds[:6]) if len(reds) >= 6 else sum(reds)
        odd_count = sum(1 for n in reds[:6] if n % 2 == 1) if len(reds) >= 6 else sum(1 for n in reds if n % 2 == 1)
        consecutive_pairs = 0
        if len(reds) >= 2:
            sorted_reds = sorted(reds[:6]) if len(reds) >= 6 else sorted(reds)
            consecutive_pairs = sum(1 for i in range(len(sorted_reds)-1) if sorted_reds[i+1] - sorted_reds[i] == 1)
        
        recommendation = {
            'strategy': strategy,
            'lottery_type': self.name,
            'red_balls': reds[:6] if len(reds) >= 6 else reds,
            'blue_balls': blues[:self.blue_count] if self.blue_count == 1 else blues,
            'stats': {
                'sum': sum_val,
                'odd_even': f"{odd_count}:{6-odd_count}",
                'consecutive_pairs': consecutive_pairs,
                'sum_vs_avg': f"{sum_val - stats['sum']['avg']:+.0f}"
            }
        }
        
        if include_dantuo and len(reds) >= 7:
            freq_mean = 0
            if stats['red']['frequency']:
                freq_mean = sum(stats['red']['frequency'].values()) / len(stats['red']['frequency'])
            dan_reds = [r for r in reds if stats['red']['frequency'].get(r, 0) > freq_mean][:2]
            if len(dan_reds) < 2 and len(reds) >= 2:
                dan_reds = reds[:2]
            tuo_reds = [r for r in reds if r not in dan_reds]
            recommendation['dantuo'] = {
                'dan_reds': dan_reds,
                'tuo_reds': tuo_reds[:8],
                'dan_blues': blues[:1] if blues else []
            }
        
        return recommendation
    
    def generate_multiple_recommendations(self, count: int = 6, include_dantuo: bool = False) -> List[Dict]:
        """生成多组推荐"""
        strategies = ['balanced', 'hot', 'cold', 'missing_rebound', 'consecutive', 'segment']
        recommendations = []
        
        strategy_names = {
            'balanced': '均衡策略',
            'hot': '热号策略',
            'cold': '冷号策略',
            'missing_rebound': '遗漏回补',
            'consecutive': '连号防守',
            'segment': '区间覆盖'
        }
        
        for i in range(min(count, len(strategies))):
            rec = self.recommend_numbers(strategy=strategies[i], include_dantuo=include_dantuo)
            rec['group'] = i + 1
            rec['strategy_name'] = strategy_names.get(strategies[i], strategies[i])
            recommendations.append(rec)
        
        return recommendations
    
    def generate_kill_numbers(self) -> Dict:
        """生成杀号"""
        if not hasattr(self, 'red_freq'):
            self.extract_numbers()
        
        stats = self.generate_statistics()
        missing = self.analyze_missing()
        
        kill_reds = []
        kill_blues = []
        
        recent_reds = self.all_red_numbers[:60] if self.all_red_numbers else []
        recent_red_freq = Counter(recent_reds)
        for num, freq in recent_red_freq.items():
            if freq >= 3:
                kill_reds.append(num)
        
        avg_miss = missing['avg_missing_red']
        for num, miss in missing['red_top_missing']:
            if miss > avg_miss * 3:
                kill_reds.append(num)
        
        red_cols = self._get_red_columns()
        if len(self.data) > 0:
            last_reds = self.data.iloc[0][red_cols].tolist()
            kill_reds.extend(last_reds)
        
        if len(self.data) > 0:
            if self.lottery_type == 'ssq':
                last_blue = self.data.iloc[0]['蓝']
                kill_blues.append(last_blue)
            else:
                if '后1' in self.data.columns:
                    kill_blues.append(self.data.iloc[0]['后1'])
                if '后2' in self.data.columns:
                    kill_blues.append(self.data.iloc[0]['后2'])
        
        recent_blues = self.all_blue_numbers[:20] if self.all_blue_numbers else []
        recent_blue_freq = Counter(recent_blues)
        for num, freq in recent_blue_freq.items():
            if freq >= 2:
                kill_blues.append(num)
        
        kill_reds = sorted(list(set(kill_reds)))[:10]
        kill_blues = sorted(list(set(kill_blues)))[:5]
        
        return {
            'kill_reds': kill_reds,
            'kill_blues': kill_blues,
            'reason': '过热（近期出现>=3次）、遗漏过大（>平均3倍）、上期号码'
        }
    
    def backtest(self, test_count: int = 10) -> Dict:
        """历史回测"""
        if len(self.data) < test_count + 10:
            return {
                'success': False,
                'error': f"数据不足，需要至少{test_count + 10}期，当前{len(self.data)}期"
            }
        
        results = []
        
        for i in range(test_count):
            train_data = self.data.iloc[i+10:].copy()
            
            if len(train_data) < 10:
                continue
            
            original_data = self.data
            self.data = train_data
            
            self._calculate_missing()
            self.extract_numbers()
            
            rec = self.recommend_numbers(strategy='balanced')
            
            actual_row = original_data.iloc[i]
            red_cols = self._get_red_columns()
            actual_reds = set(actual_row[red_cols].tolist())
            
            if self.lottery_type == 'ssq':
                actual_blues = {actual_row['蓝']}
            else:
                actual_blues = set()
                if '后1' in actual_row:
                    actual_blues.add(actual_row['后1'])
                if '后2' in actual_row:
                    actual_blues.add(actual_row['后2'])
            
            pred_reds = set(rec['red_balls'])
            red_hits = len(pred_reds & actual_reds)
            blue_hits = len(set(rec['blue_balls']) & actual_blues)
            
            results.append({
                'period': int(actual_row['期号']) if '期号' in actual_row else i+1,
                'red_hits': red_hits,
                'blue_hits': blue_hits,
                'red_accuracy': f"{red_hits}/{len(rec['red_balls'])}",
                'total_hits': red_hits + blue_hits
            })
        
        self.data = original_data
        self._calculate_missing()
        self.extract_numbers()
        
        if results:
            avg_red_hits = sum(r['red_hits'] for r in results) / len(results)
            avg_blue_hits = sum(r['blue_hits'] for r in results) / len(results)
            hit_rate = len([r for r in results if r['red_hits'] >= 3]) / len(results) * 100
        else:
            avg_red_hits = avg_blue_hits = hit_rate = 0
        
        return {
            'success': True,
            'test_count': len(results),
            'avg_red_hits': round(avg_red_hits, 2),
            'avg_blue_hits': round(avg_blue_hits, 2),
            'hit_rate_3plus': f"{hit_rate:.1f}%",
            'details': results
        }
    
    def generate_trend_chart_data(self, recent_count: int = 50) -> Dict:
        """生成趋势图数据"""
        if self.data is None:
            return None
        
        red_cols = self._get_red_columns()
        periods = self.data['期号'].tolist()[:recent_count]
        
        red_trend = {}
        for num in self.red_range:
            appears = []
            for idx in range(min(recent_count, len(self.data))):
                row = self.data.iloc[idx]
                reds = row[red_cols].tolist()
                appears.append(1 if num in reds else 0)
            red_trend[str(num)] = appears
        
        sum_trend = []
        for idx in range(min(recent_count, len(self.data))):
            row = self.data.iloc[idx]
            sum_trend.append(int(row[red_cols].sum()))
        
        odd_trend = []
        for idx in range(min(recent_count, len(self.data))):
            row = self.data.iloc[idx]
            reds = row[red_cols].tolist()
            odd_count = sum(1 for n in reds if n % 2 == 1)
            odd_trend.append(odd_count)
        
        return {
            'periods': periods,
            'red_trend': red_trend,
            'sum_trend': sum_trend,
            'odd_trend': odd_trend
        }
    
    def export_report(self, filename: Optional[str] = None) -> str:
        """导出完整分析报告"""
        if filename is None:
            filename = str(REPORTS_DIR / f"lottery_report_{self.lottery_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        self.extract_numbers()
        stats = self.generate_statistics()
        missing = self.analyze_missing()
        patterns, trend = self.analyze_patterns(10)
        kill_numbers = self.generate_kill_numbers()
        recommendations = self.generate_multiple_recommendations(6, include_dantuo=True)
        backtest = self.backtest(test_count=10)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'lottery_type': self.name,
            'total_periods': len(self.data),
            'latest_issue': stats.get('latest_issue'),
            'statistics': stats,
            'missing_analysis': missing,
            'recent_patterns': patterns[:10],
            'trend_summary': {
                'consecutive_trend': trend.get('consecutive_trend', [])[-10:],
                'sum_trend': trend.get('sum_trend', [])[-10:]
            },
            'kill_numbers': kill_numbers,
            'recommendations': recommendations,
            'backtest': backtest if backtest.get('success') else None
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return filename
    
    # ==================== 新增功能 ====================
    
    def save_prediction_record(self, issue: str, recommendations: List[Dict], 
                                kill_numbers: Dict, metadata: Dict = None) -> str:
        """保存预测记录到文件"""
        record = {
            "issue": issue,
            "lottery_type": self.name,
            "timestamp": datetime.now().isoformat(),
            "recommendations": recommendations,
            "kill_numbers": kill_numbers,
            "metadata": metadata or {}
        }
        
        filename = PREDICTIONS_DIR / f"prediction_{issue}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        
        # 同时保存一个最新的副本
        latest_file = PREDICTIONS_DIR / f"latest_prediction_{self.lottery_type}.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        
        return str(filename)
    
    def list_prediction_history(self, limit: int = 20) -> List[Dict]:
        """列出所有预测记录"""
        predictions = []
        for file in PREDICTIONS_DIR.glob("prediction_*.json"):
            if "latest_prediction" in file.name:
                continue
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    predictions.append({
                        "file": file.name,
                        "issue": data.get("issue", "未知"),
                        "timestamp": data.get("timestamp", ""),
                        "lottery_type": data.get("lottery_type", ""),
                        "recommendations_count": len(data.get("recommendations", []))
                    })
            except:
                continue
        
        predictions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return predictions[:limit]
    
    def load_prediction_record(self, issue: str) -> Optional[Dict]:
        """加载指定期号的预测记录"""
        for file in PREDICTIONS_DIR.glob(f"prediction_{issue}_*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                continue
        
        latest_file = PREDICTIONS_DIR / f"latest_prediction_{self.lottery_type}.json"
        if latest_file.exists():
            try:
                with open(latest_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get("issue") == issue:
                        return data
            except:
                pass
        
        return None
    
    def check_winning(self, issue: str, actual_reds: List[int], actual_blue: int) -> Dict:
        """检查指定期号的预测是否中奖"""
        prediction = self.load_prediction_record(issue)
        if not prediction:
            return {
                "success": False,
                "error": f"未找到期号 {issue} 的预测记录，请先进行预测"
            }
        
        recommendations = prediction.get("recommendations", [])
        results = []
        
        for rec in recommendations:
            pred_reds = set(rec.get("red_balls", []))
            pred_blues = set(rec.get("blue_balls", []))
            actual_reds_set = set(actual_reds)
            actual_blue_set = {actual_blue} if isinstance(actual_blue, int) else set(actual_blue)
            
            red_matches = len(pred_reds & actual_reds_set)
            blue_match = len(pred_blues & actual_blue_set)
            
            prize_level = self._get_prize_level(red_matches, blue_match)
            
            results.append({
                "group": rec.get("group", 0),
                "strategy": rec.get("strategy_name", rec.get("strategy", "")),
                "predicted_reds": list(pred_reds),
                "predicted_blues": list(pred_blues),
                "red_matches": red_matches,
                "blue_matches": blue_match,
                "prize_level": prize_level,
                "is_winning": prize_level != "未中奖"
            })
        
        winning_groups = [r for r in results if r["is_winning"]]
        
        return {
            "success": True,
            "issue": issue,
            "lottery_type": prediction.get("lottery_type", self.name),
            "prediction_time": prediction.get("timestamp", ""),
            "actual_reds": actual_reds,
            "actual_blue": actual_blue,
            "results": results,
            "summary": {
                "total_groups": len(results),
                "winning_groups": len(winning_groups),
                "best_red_hits": max([r["red_matches"] for r in results]) if results else 0,
                "best_blue_hits": max([r["blue_matches"] for r in results]) if results else 0
            }
        }
    
    def get_winning_statistics(self) -> Dict:
        """获取中奖统计数据"""
        stats = {
            "total_predictions": 0,
            "total_checked": 0,
            "winning_predictions": 0,
            "prize_distribution": {
                "一等奖": 0,
                "二等奖": 0,
                "三等奖": 0,
                "四等奖": 0,
                "五等奖": 0,
                "六等奖": 0
            },
            "average_red_hits": 0,
            "average_blue_hits": 0,
            "details": []
        }
        
        for file in PREDICTIONS_DIR.glob("prediction_*_result.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    result = json.load(f)
                    if result.get("success"):
                        stats["total_checked"] += 1
                        summary = result.get("summary", {})
                        stats["total_predictions"] += summary.get("total_groups", 0)
                        stats["winning_predictions"] += summary.get("winning_groups", 0)
                        
                        for r in result.get("results", []):
                            prize = r.get("prize_level", "")
                            if prize in stats["prize_distribution"]:
                                stats["prize_distribution"][prize] += 1
                        
                        stats["details"].append({
                            "issue": result.get("issue"),
                            "winning_groups": summary.get("winning_groups", 0),
                            "best_red_hits": summary.get("best_red_hits", 0)
                        })
            except:
                continue
        
        if stats["total_predictions"] > 0:
            stats["win_rate"] = f"{stats['winning_predictions'] / stats['total_predictions'] * 100:.1f}%"
        else:
            stats["win_rate"] = "0%"
        
        return stats
    
    def save_winning_result(self, issue: str, check_result: Dict) -> str:
        """保存兑奖结果"""
        filename = PREDICTIONS_DIR / f"prediction_{issue}_result.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(check_result, f, ensure_ascii=False, indent=2)
        return str(filename)
    
    def _get_prize_level(self, red_matches: int, blue_matches: int) -> str:
        """判断中奖等级"""
        if self.lottery_type == 'ssq':
            if red_matches == 6 and blue_matches >= 1:
                return "一等奖"
            elif red_matches == 6:
                return "二等奖"
            elif red_matches == 5 and blue_matches >= 1:
                return "三等奖"
            elif red_matches == 5 or (red_matches == 4 and blue_matches >= 1):
                return "四等奖"
            elif red_matches == 4 or (red_matches == 3 and blue_matches >= 1):
                return "五等奖"
            elif (red_matches == 2 and blue_matches >= 1) or (red_matches == 1 and blue_matches >= 1) or (red_matches == 0 and blue_matches >= 1):
                return "六等奖"
            else:
                return "未中奖"
        else:
            if red_matches == 5 and blue_matches >= 2:
                return "一等奖"
            elif red_matches == 5 and blue_matches >= 1:
                return "二等奖"
            elif red_matches == 5:
                return "三等奖"
            elif red_matches == 4 and blue_matches >= 2:
                return "四等奖"
            elif red_matches == 4 or (red_matches == 3 and blue_matches >= 2):
                return "五等奖"
            elif (red_matches == 3 and blue_matches >= 1) or (red_matches == 2 and blue_matches >= 2) or (red_matches == 1 and blue_matches >= 2) or (red_matches == 0 and blue_matches >= 2):
                return "六等奖"
            else:
                return "未中奖"


# ==================== 飞书专用输出函数 ====================

def print_report_feishu(analyzer: LotteryAnalyzer, recommendations: List[Dict], 
                         kill_numbers: Dict, missing_analysis: Dict):
    """飞书专用打印格式化报告（纯文本，无特殊字符）"""
    stats = analyzer.generate_statistics()
    
    total_periods = stats['periods']
    latest_issue = stats.get('latest_issue', '未知')
    
    # 分隔线
    line = '-' * 50
    
    output = []
    output.append("")
    output.append(line)
    output.append(f"双色球分析报告")
    output.append(line)
    output.append("")
    output.append(f"[基础统计] (共 {total_periods} 期，最新期号：{latest_issue})")
    output.append(f"  红球平均和值: {stats['sum']['avg']:.1f}")
    output.append(f"  和值范围: {stats['sum']['min']} - {stats['sum']['max']}")
    output.append(f"  热红球 TOP10: {stats['red']['hot_numbers'][:10]}")
    output.append(f"  冷红球 TOP10: {stats['red']['cold_numbers'][:10]}")
    output.append(f"  热蓝球 TOP5: {stats['blue']['hot_numbers']}")
    output.append("")
    output.append(f"[遗漏分析]")
    output.append(f"  平均遗漏（红球）: {missing_analysis['avg_missing_red']:.1f}期")
    output.append(f"  平均遗漏（蓝球）: {missing_analysis['avg_missing_blue']:.1f}期")
    rebound_nums = [item['number'] for item in missing_analysis['red_rebound_candidates'][:5]]
    output.append(f"  遗漏回补候选: {rebound_nums}")
    output.append("")
    output.append(f"[杀号推荐]")
    output.append(f"  杀红球: {kill_numbers['kill_reds']}")
    output.append(f"  杀蓝球: {kill_numbers['kill_blues']}")
    output.append("")
    output.append(f"[推荐方案]")
    
    for rec in recommendations[:5]:
        reds = ' '.join(f'{n:02d}' for n in rec['red_balls'])
        blues = ' '.join(f'{n:02d}' for n in rec['blue_balls'])
        output.append(f"")
        output.append(f"  第{rec['group']}组 - {rec['strategy_name']}")
        output.append(f"    红球: {reds}")
        output.append(f"    蓝球: {blues}")
        output.append(f"    和值: {rec['stats']['sum']} | 奇偶: {rec['stats']['odd_even']}")
    
    output.append("")
    output.append(line)
    output.append("温馨提示：彩票有风险，购彩需谨慎")
    output.append(line)
    
    # 输出
    for line in output:
        print(line)


def print_check_result_feishu(check_result: Dict):
    """飞书专用打印兑奖结果"""
    line = '-' * 50
    
    output = []
    output.append("")
    output.append(line)
    output.append(f"兑奖结果 - {check_result['issue']}期")
    output.append(line)
    output.append("")
    output.append(f"实际开奖号码:")
    output.append(f"  红球: {' '.join(f'{n:02d}' for n in check_result['actual_reds'])}")
    output.append(f"  蓝球: {check_result['actual_blue']:02d}")
    output.append("")
    output.append(f"预测结果对比:")
    
    for r in check_result['results']:
        status = "[中奖]" if r['is_winning'] else "[未中]"
        output.append(f"")
        output.append(f"  {status} 第{r['group']}组 - {r['strategy']}")
        output.append(f"    预测红球: {' '.join(f'{n:02d}' for n in r['predicted_reds'])}")
        output.append(f"    预测蓝球: {' '.join(f'{n:02d}' for n in r['predicted_blues'])}")
        output.append(f"    命中: 红球{r['red_matches']}个, 蓝球{r['blue_matches']}个")
        output.append(f"    奖级: {r['prize_level']}")
    
    output.append("")
    output.append(f"[统计汇总]")
    output.append(f"  总注数: {check_result['summary']['total_groups']}")
    output.append(f"  中奖注数: {check_result['summary']['winning_groups']}")
    output.append(f"  最高红球命中: {check_result['summary']['best_red_hits']}个")
    
    output.append("")
    output.append(line)
    
    for line in output:
        print(line)


def print_history_feishu(history: List[Dict]):
    """飞书专用打印预测历史"""
    line = '-' * 50
    
    output = []
    output.append("")
    output.append(line)
    output.append(f"预测历史记录")
    output.append(line)
    
    if not history:
        output.append("")
        output.append("暂无预测记录，请先进行预测")
    else:
        output.append("")
        for i, h in enumerate(history, 1):
            timestamp = h.get('timestamp', '')[:16] if h.get('timestamp') else ''
            output.append(f"  {i}. {h['issue']}期 - {timestamp} - {h['recommendations_count']}注")
    
    output.append("")
    output.append(line)
    
    for line in output:
        print(line)


def print_winning_stats_feishu(stats: Dict):
    """飞书专用打印中奖统计"""
    line = '-' * 50
    
    output = []
    output.append("")
    output.append(line)
    output.append(f"中奖统计报告")
    output.append(line)
    output.append("")
    output.append(f"[整体统计]")
    output.append(f"  总预测期数: {stats['total_checked']}")
    output.append(f"  总预测注数: {stats['total_predictions']}")
    output.append(f"  中奖注数: {stats['winning_predictions']}")
    output.append(f"  中奖率: {stats['win_rate']}")
    output.append("")
    output.append(f"[奖级分布]")
    for prize, count in stats['prize_distribution'].items():
        if count > 0:
            output.append(f"  {prize}: {count}注")
    
    if stats['details']:
        output.append("")
        output.append(f"[近期中奖记录]")
        for d in stats['details'][:10]:
            output.append(f"  {d['issue']}期: 中{d['winning_groups']}注, 最高红球{d['best_red_hits']}个")
    
    output.append("")
    output.append(line)
    
    for line in output:
        print(line)


def main():
    """主函数 - ClawHub Skill 入口"""
    parser = argparse.ArgumentParser(description="彩票分析系统")
    parser.add_argument("--issue", type=str, required=True, help="期号（预测的目标期号）")
    parser.add_argument("--lottery", type=str, default="ssq", help="彩种（ssq/dlt）")
    parser.add_argument("--data", type=str, help="数据文件路径")
    parser.add_argument("--output", type=str, default="json", help="输出格式（json/text）")
    parser.add_argument("--backtest", action="store_true", help="执行历史回测")
    parser.add_argument("--export", action="store_true", help="导出完整报告")
    parser.add_argument("--dantuo", action="store_true", help="包含胆拖推荐")
    
    # 新增参数
    parser.add_argument("--history", action="store_true", help="查看预测历史")
    parser.add_argument("--check", type=str, help="兑奖：提供实际开奖号码，格式：红球1,红球2,...,蓝球")
    parser.add_argument("--stats", action="store_true", help="查看中奖统计")
    parser.add_argument("--no-save", action="store_true", help="不保存预测记录")
    
    args = parser.parse_args()
    
    # 查看历史记录（不需要加载数据）
    if args.history:
        temp_analyzer = LotteryAnalyzer(args.lottery)
        history = temp_analyzer.list_prediction_history()
        print_history_feishu(history)
        return
    
    # 查看中奖统计（不需要加载数据）
    if args.stats:
        temp_analyzer = LotteryAnalyzer(args.lottery)
        stats = temp_analyzer.get_winning_statistics()
        print_winning_stats_feishu(stats)
        return
    
    # 确定数据文件路径
    if args.data:
        data_path = args.data
    else:
        data_path = str(DEFAULT_DATA_PATH)
    
    # 创建分析器
    try:
        analyzer = LotteryAnalyzer(args.lottery)
    except ValueError as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        return
    
    # 兑奖模式
    if args.check:
        actual_parts = [int(x) for x in args.check.split(',')]
        actual_blue = actual_parts[-1]
        actual_reds = actual_parts[:-1]
        
        check_result = analyzer.check_winning(args.issue, actual_reds, actual_blue)
        
        if args.output == "json":
            print(json.dumps(check_result, ensure_ascii=False, indent=2))
        else:
            if check_result.get("success"):
                print_check_result_feishu(check_result)
                analyzer.save_winning_result(args.issue, check_result)
            else:
                print(f"错误: {check_result.get('error', '兑奖失败')}")
        return
    
    # 加载数据
    success, msg = analyzer.load_data(data_path)
    if not success:
        print(json.dumps({"success": False, "error": msg}, ensure_ascii=False))
        return
    
    # 提取数据
    analyzer.extract_numbers()
    
    # 执行分析
    missing_analysis = analyzer.analyze_missing()
    kill_numbers = analyzer.generate_kill_numbers()
    recommendations = analyzer.generate_multiple_recommendations(6, include_dantuo=args.dantuo)
    
    # 保存预测记录（除非指定不保存）
    saved_file = None
    if not args.no_save:
        saved_file = analyzer.save_prediction_record(args.issue, recommendations, kill_numbers, {
            "dantuo": args.dantuo,
            "backtest": args.backtest,
            "export": args.export
        })
    
    # 执行回测（如果需要）
    backtest_result = None
    if args.backtest:
        backtest_result = analyzer.backtest(test_count=10)
    
    # 导出报告（如果需要）
    report_file = None
    if args.export:
        report_file = analyzer.export_report()
    
    # 获取最新期号
    latest_issue = analyzer.data.iloc[0]['期号'] if len(analyzer.data) > 0 else None
    
    # 构建输出
    stats = analyzer.generate_statistics()
    
    output = {
        "success": True,
        "version": "2.0.0",
        "issue": args.issue,
        "latest_issue": int(latest_issue) if latest_issue else None,
        "total_periods": len(analyzer.data),
        "statistics": stats,
        "missing_analysis": missing_analysis,
        "kill_numbers": kill_numbers,
        "recommendations": recommendations
    }
    
    if backtest_result:
        output["backtest"] = backtest_result
    
    if report_file:
        output["report_file"] = report_file
    
    if saved_file:
        output["saved_to"] = saved_file
    
    # 输出
    if args.output == "json":
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 使用飞书专用格式输出
        print_report_feishu(analyzer, recommendations, kill_numbers, missing_analysis)
        
        if saved_file:
            print(f"\n[成功] 预测记录已保存: {saved_file}")
        
        if args.backtest and backtest_result and backtest_result.get('success'):
            print(f"\n[回测结果]")
            print(f"  测试期数: {backtest_result['test_count']}")
            print(f"  平均红球命中: {backtest_result['avg_red_hits']}个")
            print(f"  平均蓝球命中: {backtest_result['avg_blue_hits']}个")
            print(f"  红球>=3个命中率: {backtest_result['hit_rate_3plus']}")
        
        if args.export:
            print(f"\n[成功] 完整报告已导出: {report_file}")


if __name__ == "__main__":
    main()