#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压力位支撑位识别系统 - 新思路
基于波峰波谷识别 + 显著过滤 + 聚类
特点：
1. 不用20日窗口法
2. 沿日K线搜索明显波峰波谷
3. 日K线默认120天
4. 波峰：最高价高于前后N根K线最高价
5. 波谷：最低价低于前后N根K线最低价
6. 显著过滤：波峰比前一个高5%以上，波谷比前一个低5%以上
7. 聚合：价格相近（差值<2%）归为一组
8. 强度=触及次数
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class SupportResistanceAnalyzer:
    """压力位支撑位分析器 - 新思路版本"""
    
    def __init__(self, days: int = 120, n: int = 5, 
                 significant_threshold: float = 0.05, 
                 cluster_tolerance: float = 0.02):
        """
        初始化分析器
        
        Args:
            days: K线天数，默认120天
            n: 波峰波谷前后N根K线比较，默认5
            significant_threshold: 显著阈值(5%)，波峰需比前一波峰高5%以上
            cluster_tolerance: 聚类容差(2%)，价格差小于2%归为一组
        """
        self.days = days
        self.n = n
        self.significant_threshold = significant_threshold
        self.cluster_tolerance = cluster_tolerance
        
        self.data = None
        self.peaks = []  # 波峰
        self.valleys = []  # 波谷
        self.significant_peaks = []  # 显著波峰
        self.significant_valleys = []  # 显著波谷
        self.supports = []  # 支撑位
        self.resistances = []  # 压力位
        
    def fetch_data(self, symbol: str, days: int = None) -> pd.DataFrame:
        """获取K线数据"""
        if days is None:
            days = self.days
            
        print(f"📊 正在获取 {symbol} 最近{days}天数据...")
        
        # 计算日期范围，多取一些数据确保足够
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days * 1.5)
        
        if symbol.startswith('sh') or symbol.startswith('sz'):
            # 指数
            df = ak.stock_zh_index_daily(symbol=symbol)
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        else:
            # 个股
            df = ak.stock_zh_a_hist(symbol=symbol, period='daily', 
                                   start_date=start_date.strftime('%Y%m%d'), 
                                   end_date=end_date.strftime('%Y%m%d'))
            
        # 统一列名
        df.columns = [c.lower() for c in df.columns]
        if '日期' in df.columns:
            df.rename(columns={'日期': 'date', '开盘': 'open', '收盘': 'close', 
                              '最高': 'high', '最低': 'low', '成交量': 'volume',
                              '成交额': 'amount'}, inplace=True)
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        # 只取最后days条数据
        df = df.tail(days).reset_index(drop=True)
        
        print(f"✅ 获取到 {len(df)} 条数据，从 {df.iloc[0]['date'].strftime('%Y-%m-%d')} 到 {df.iloc[-1]['date'].strftime('%Y-%m-%d')}")
        self.data = df
        return df
    
    def find_peaks(self, n: int = None) -> List[Dict]:
        """
        识别波峰：最高价高于前后N根K线的最高价
        
        Args:
            n: 前后比较的K线数量
            
        Returns:
            波峰列表
        """
        if n is None:
            n = self.n
            
        df = self.data
        peaks = []
        
        # 需要前后n根K线，所以从n开始到len-n结束
        for i in range(n, len(df) - n):
            current_high = df.iloc[i]['high']
            
            # 获取前后n根K线的最高价
            prev_n_highs = df.iloc[i-n:i]['high'].values
            next_n_highs = df.iloc[i+1:i+n+1]['high'].values
            
            # 如果当前K线最高价高于前后所有K线的最高价，则是波峰
            if current_high > np.max(prev_n_highs) and current_high > np.max(next_n_highs):
                peaks.append({
                    'date': df.iloc[i]['date'],
                    'price': current_high,
                    'index': i
                })
        
        self.peaks = peaks
        print(f"🔍 识别到 {len(peaks)} 个波峰")
        return peaks
    
    def find_valleys(self, n: int = None) -> List[Dict]:
        """
        识别波谷：最低价低于前后N根K线的最低价
        
        Args:
            n: 前后比较的K线数量
            
        Returns:
            波谷列表
        """
        if n is None:
            n = self.n
            
        df = self.data
        valleys = []
        
        for i in range(n, len(df) - n):
            current_low = df.iloc[i]['low']
            
            # 获取前后n根K线的最低价
            prev_n_lows = df.iloc[i-n:i]['low'].values
            next_n_lows = df.iloc[i+1:i+n+1]['low'].values
            
            # 如果当前K线最低价低于前后所有K线的最低价，则是波谷
            if current_low < np.min(prev_n_lows) and current_low < np.min(next_n_lows):
                valleys.append({
                    'date': df.iloc[i]['date'],
                    'price': current_low,
                    'index': i
                })
        
        self.valleys = valleys
        print(f"🔍 识别到 {len(valleys)} 个波谷")
        return valleys
    
    def filter_significant_peaks(self, threshold: float = None) -> List[Dict]:
        """
        显著波峰过滤：当前高点比前一个波峰高5%以上
        
        Args:
            threshold: 显著阈值，默认5%
            
        Returns:
            显著波峰列表
        """
        if threshold is None:
            threshold = self.significant_threshold
            
        if not self.peaks:
            return []
        
        significant_peaks = []
        
        for i, peak in enumerate(self.peaks):
            if i == 0:
                # 第一个波峰默认保留
                significant_peaks.append(peak)
            else:
                # 与前一个波峰比较
                prev_peak = self.peaks[i-1]
                price_change = (peak['price'] - prev_peak['price']) / prev_peak['price']
                
                # 如果比前一波峰高5%以上，或者是回调后再次上涨
                if price_change >= threshold:
                    significant_peaks.append(peak)
                # 如果比前一波峰低，但可能是调整后的支撑
                elif price_change >= -threshold:
                    # 保留接近的波峰（可能是双顶等形态）
                    if len(significant_peaks) > 0:
                        last_sig = significant_peaks[-1]
                        if (peak['price'] - last_sig['price']) / last_sig['price'] >= -threshold * 0.5:
                            significant_peaks.append(peak)
        
        self.significant_peaks = significant_peaks
        print(f"⭐ 显著波峰: {len(significant_peaks)} 个")
        return significant_peaks
    
    def filter_significant_valleys(self, threshold: float = None) -> List[Dict]:
        """
        显著波谷过滤：当前低点比前一个波谷低5%以上
        
        Args:
            threshold: 显著阈值，默认5%
            
        Returns:
            显著波谷列表
        """
        if threshold is None:
            threshold = self.significant_threshold
            
        if not self.valleys:
            return []
        
        significant_valleys = []
        
        for i, valley in enumerate(self.valleys):
            if i == 0:
                # 第一个波谷默认保留
                significant_valleys.append(valley)
            else:
                # 与前一个波谷比较
                prev_valley = self.valleys[i-1]
                price_change = (valley['price'] - prev_valley['price']) / prev_valley['price']
                
                # 如果比前一波谷低5%以上（下跌）
                if price_change <= -threshold:
                    significant_valleys.append(valley)
                # 如果比前一波谷高，但可能是反弹后的回调
                elif price_change <= threshold:
                    if len(significant_valleys) > 0:
                        last_sig = significant_valleys[-1]
                        if (valley['price'] - last_sig['price']) / last_sig['price'] <= threshold * 0.5:
                            significant_valleys.append(valley)
        
        self.significant_valleys = significant_valleys
        print(f"⭐ 显著波谷: {len(significant_valleys)} 个")
        return significant_valleys
    
    def cluster_levels(self, levels: List[Dict], tolerance: float = None) -> List[Dict]:
        """
        聚类生成支撑/压力位
        价格相近（差值<2%）的归为一组
        
        Args:
            levels: 波峰或波谷列表
            tolerance: 聚类容差，默认2%
            
        Returns:
            支撑位或压力位列表
        """
        if tolerance is None:
            tolerance = self.cluster_tolerance
            
        if not levels:
            return []
        
        # 按价格排序
        sorted_levels = sorted(levels, key=lambda x: x['price'])
        clusters = []
        current_cluster = [sorted_levels[0]]
        
        for i in range(1, len(sorted_levels)):
            prev_price = current_cluster[-1]['price']
            curr_price = sorted_levels[i]['price']
            
            # 价格差小于tolerance，归入同一组
            if abs(curr_price - prev_price) / prev_price <= tolerance:
                current_cluster.append(sorted_levels[i])
            else:
                clusters.append(current_cluster)
                current_cluster = [sorted_levels[i]]
        
        # 最后一个cluster
        clusters.append(current_cluster)
        
        # 合并为支撑/压力位
        result = []
        for cluster in clusters:
            prices = [c['price'] for c in cluster]
            avg_price = np.mean(prices)
            touches = [c['date'] for c in cluster]
            
            result.append({
                'price': round(avg_price, 2),
                'strength': len(cluster),  # 触及次数 = 聚合的波峰/波谷数量
                'touches': touches,
                'max_price': round(max(prices), 2),
                'min_price': round(min(prices), 2),
                'valid': len(cluster) >= 1  # 只要有聚合就算有效
            })
        
        return sorted(result, key=lambda x: x['price'], reverse=True)
    
    def generate_levels(self):
        """生成支撑位和压力位"""
        # 波峰 -> 压力位
        self.resistances = self.cluster_levels(self.significant_peaks)
        # 波谷 -> 支撑位
        self.supports = self.cluster_levels(self.significant_valleys)
        
        print(f"📍 聚类得到 {len(self.resistances)} 个压力位, {len(self.supports)} 个支撑位")
        return self.resistances, self.supports
    
    def analyze_current_position(self) -> Dict:
        """分析当前位置"""
        if self.data is None or len(self.data) == 0:
            return {}
            
        df = self.data
        latest = df.iloc[-1]
        current_price = latest['close']
        
        result = {
            'current_price': current_price,
            'nearest_resistance': None,
            'nearest_support': None,
            'distance_to_resistance': None,
            'distance_to_support': None
        }
        
        # 找最近的压力位
        for res in self.resistances:
            if res['price'] > current_price:
                distance = (res['price'] - current_price) / current_price * 100
                result['nearest_resistance'] = res['price']
                result['distance_to_resistance'] = round(distance, 2)
                break
        
        # 找最近的支撑位
        for sup in reversed(self.supports):
            if sup['price'] < current_price:
                distance = (current_price - sup['price']) / sup['price'] * 100
                result['nearest_support'] = sup['price']
                result['distance_to_support'] = round(distance, 2)
                break
        
        return result
    
    def run_full_analysis(self, symbol: str, days: int = None) -> Dict:
        """运行完整分析"""
        if days is None:
            days = self.days
            
        # 1. 获取数据
        self.fetch_data(symbol, days)
        
        # 2. 识别波峰波谷
        self.find_peaks()
        self.find_valleys()
        
        # 3. 显著过滤
        self.filter_significant_peaks()
        self.filter_significant_valleys()
        
        # 4. 生成支撑压力位
        self.generate_levels()
        
        # 5. 当前位置分析
        position = self.analyze_current_position()
        
        return {
            'symbol': symbol,
            'days': days,
            'n': self.n,
            'data': self.data,
            'peaks': self.peaks,
            'valleys': self.valleys,
            'significant_peaks': self.significant_peaks,
            'significant_valleys': self.significant_valleys,
            'resistances': self.resistances,
            'supports': self.supports,
            'position': position
        }
    
    def visualize(self, symbol: str = None, save_path: str = None):
        """可视化"""
        if self.data is None:
            raise ValueError("请先运行分析")
            
        df = self.data
        
        fig, ax = plt.subplots(figsize=(16, 9))
        
        # 绘制K线
        for idx, row in df.iterrows():
            color = 'red' if row['close'] >= row['open'] else 'green'
            ax.plot([idx, idx], [row['low'], row['high']], color=color, linewidth=0.8)
            width = 0.6
            ax.fill_between([idx-width/2, idx+width/2], row['open'], row['close'], 
                           facecolor=color, alpha=0.3)
        
        # 绘制所有波峰
        for peak in self.peaks:
            ax.scatter(peak['index'], peak['price'], marker='^', color='orange', s=30, alpha=0.5)
        
        # 绘制显著波峰
        for peak in self.significant_peaks:
            ax.scatter(peak['index'], peak['price'], marker='^', color='red', s=80, zorder=5)
        
        # 绘制所有波谷
        for valley in self.valleys:
            ax.scatter(valley['index'], valley['price'], marker='v', color='lightgreen', s=30, alpha=0.5)
        
        # 绘制显著波谷
        for valley in self.significant_valleys:
            ax.scatter(valley['index'], valley['price'], marker='v', color='green', s=80, zorder=5)
        
        # 绘制压力位
        for res in self.resistances:
            ax.axhline(y=res['price'], color='red', linestyle='--', linewidth=1.5, alpha=0.7)
            ax.text(len(df)-1, res['price'], f"压力:{res['price']}({res['strength']}次)", 
                   va='center', ha='right', fontsize=9, color='red')
        
        # 绘制支撑位
        for sup in self.supports:
            ax.axhline(y=sup['price'], color='green', linestyle='--', linewidth=1.5, alpha=0.7)
            ax.text(len(df)-1, sup['price'], f"支撑:{sup['price']}({sup['strength']}次)", 
                   va='center', ha='right', fontsize=9, color='green')
        
        # 设置标题
        title = f"{symbol or '股票'} 压力位支撑位分析 (新思路)"
        if len(self.data) > 0:
            latest = df.iloc[-1]
            title += f" | 现价:{latest['close']:.2f}"
        ax.set_title(title, fontsize=14)
        
        ax.set_xlabel('交易日')
        ax.set_ylabel('价格')
        ax.set_xlim(0, len(df))
        
        # X轴日期标签
        tick_positions = np.linspace(0, len(df)-1, min(10, len(df))).astype(int)
        tick_labels = [df.iloc[i]['date'].strftime('%Y-%m-%d') for i in tick_positions]
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=45)
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"📊 图表已保存: {save_path}")
        
        plt.show()
        
        return fig


def print_analysis_result(result: Dict):
    """打印分析结果"""
    print("\n" + "="*60)
    print(f"📈 {result['symbol']} 压力位支撑位分析结果 (新思路)")
    print(f"📊 数据范围: {result['days']}天 | N={result['n']}")
    print("="*60)
    
    # 压力位
    print("\n🔴 压力位 (由显著波峰聚合):")
    if result['resistances']:
        for i, res in enumerate(result['resistances'][:5], 1):
            print(f"   {i}. 价格:{res['price']} | 触及:{res['strength']}次 | 区间:{res['min_price']}-{res['max_price']}")
    else:
        print("   无压力位")
    
    # 支撑位
    print("\n🟢 支撑位 (由显著波谷聚合):")
    if result['supports']:
        for i, sup in enumerate(result['supports'][:5], 1):
            print(f"   {i}. 价格:{sup['price']} | 触及:{sup['strength']}次 | 区间:{sup['min_price']}-{sup['max_price']}")
    else:
        print("   无支撑位")
    
    # 当前位置
    pos = result['position']
    print(f"\n📍 当前位置分析:")
    print(f"   现价: {pos['current_price']:.2f}")
    if pos['nearest_resistance']:
        print(f"   最近压力位: {pos['nearest_resistance']:.2f} (距{pos['distance_to_resistance']:.1f}%)")
    if pos['nearest_support']:
        print(f"   最近支撑位: {pos['nearest_support']:.2f} (距{pos['distance_to_support']:.1f}%)")
    
    print("\n" + "="*60)


# 测试函数
def test_shanghai_index():
    """测试上证指数"""
    print("\n" + "🌟"*20)
    print("测试: 上证指数 (sh000001)")
    print("🌟"*20 + "\n")
    
    # 新思路参数
    analyzer = SupportResistanceAnalyzer(days=120, n=5, significant_threshold=0.05)
    result = analyzer.run_full_analysis('sh000001')
    print_analysis_result(result)
    
    # 可视化
    analyzer.visualize('上证指数', 'sh000001_sr_new.png')
    
    return result


def test_stock(stock_code: str = '600519', name: str = '贵州茅台'):
    """测试个股"""
    print("\n" + "🌟"*20)
    print(f"测试: {name} ({stock_code})")
    print("🌟"*20 + "\n")
    
    # 新思路参数
    analyzer = SupportResistanceAnalyzer(days=120, n=5, significant_threshold=0.05)
    result = analyzer.run_full_analysis(stock_code)
    print_analysis_result(result)
    
    # 可视化
    analyzer.visualize(name, f'{stock_code}_sr_new.png')
    
    return result


if __name__ == '__main__':
    # 测试上证指数
    test_shanghai_index()
    
    # 测试个股
    # test_stock('600519', '贵州茅台')
    # test_stock('000858', '五粮液')
