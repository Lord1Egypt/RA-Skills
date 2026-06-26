#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压力位支撑位识别系统
基于波峰波谷分析和成交量验证
"""

import akshare as ak
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class SupportResistanceAnalyzer:
    """压力位支撑位分析器"""
    
    def __init__(self, window: int = 20, min_amplitude: float = 0.05, 
                 volume_ma: int = 20, volume_threshold: float = 1.5):
        """
        初始化分析器
        
        Args:
            window: 波峰波谷识别窗口
            min_amplitude: 最小幅度阈值(5%)
            volume_ma: 成交量均量周期
            volume_threshold: 放量阈值系数
        """
        self.window = window
        self.min_amplitude = min_amplitude
        self.volume_ma = volume_ma
        self.volume_threshold = volume_threshold
        self.data = None
        self.peaks = []  # 波峰
        self.valleys = []  # 波谷
        self.supports = []  # 支撑位
        self.resistances = []  # 压力位
        
    def fetch_data(self, symbol: str, start_date: str, end_date: str = None) -> pd.DataFrame:
        """获取K线数据"""
        if end_date is None:
            end_date = datetime.now().strftime('%Y%m%d')
            
        print(f"📊 正在获取 {symbol} 数据...")
        
        # 转换日期字符串为datetime
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        if symbol.startswith('sh') or symbol.startswith('sz'):
            # 指数
            df = ak.stock_zh_index_daily(symbol=symbol)
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
        else:
            # 个股
            df = ak.stock_zh_a_hist_tx(symbol=symbol, period='daily', 
                                   start_date=start_date, end_date=end_date)
            df['日期'] = pd.to_datetime(df['日期'])
            
        # 统一列名
        df.columns = [c.lower() for c in df.columns]
        if '日期' in df.columns:
            df.rename(columns={'日期': 'date', '开盘': 'open', '收盘': 'close', 
                              '最高': 'high', '最低': 'low', '成交量': 'volume',
                              '成交额': 'amount', '振幅': 'amplitude',
                              '涨跌幅': 'pct_change'}, inplace=True)
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        print(f"✅ 获取到 {len(df)} 条数据")
        self.data = df
        return df
    
    def find_peaks_and_valleys(self) -> Tuple[List[Dict], List[Dict]]:
        """识别波峰和波谷 - 使用scipy信号处理"""
        try:
            from scipy.signal import argrelextrema
            df = self.data.copy()
            
            # 使用收盘价找极值
            close = df['close'].values
            
            # 找波峰 (order=5 表示前后5个点比较)
            peak_indices = argrelextrema(close, np.greater, order=5)[0]
            # 找波谷
            valley_indices = argrelextrema(close, np.less, order=5)[0]
            
            peaks = []
            valleys = []
            
            # 处理波峰
            for idx in peak_indices:
                if idx > 0 and idx < len(df) - 1:
                    prev_close = df.iloc[idx-1]['close']
                    curr_high = df.iloc[idx]['high']
                    amplitude = (curr_high - prev_close) / prev_close
                    
                    if amplitude >= self.min_amplitude * 0.5:  # 放宽条件
                        peaks.append({
                            'date': df.iloc[idx]['date'],
                            'price': curr_high,
                            'amplitude': amplitude,
                            'index': idx
                        })
            
            # 处理波谷
            for idx in valley_indices:
                if idx > 0 and idx < len(df) - 1:
                    prev_close = df.iloc[idx-1]['close']
                    curr_low = df.iloc[idx]['low']
                    amplitude = (prev_close - curr_low) / prev_close
                    
                    if amplitude >= self.min_amplitude * 0.5:
                        valleys.append({
                            'date': df.iloc[idx]['date'],
                            'price': curr_low,
                            'amplitude': amplitude,
                            'index': idx
                        })
            
            self.peaks = peaks
            self.valleys = valleys
            
            print(f"🔍 识别到 {len(peaks)} 个波峰, {len(valleys)} 个波谷")
            return peaks, valleys
            
        except ImportError:
            # 如果没有scipy，使用简化版
            print("⚠️ scipy未安装，使用简化算法")
            return self._simple_find_peaks_valleys()
    
    def _simple_find_peaks_valleys(self) -> Tuple[List[Dict], List[Dict]]:
        """简化版波峰波谷识别"""
        df = self.data.copy()
        
        peaks = []
        valleys = []
        
        # 计算n日高点/低点
        n = 10  # 简化窗口
        
        for i in range(n, len(df) - n):
            current = df.iloc[i]
            window = df.iloc[i-n:i+n+1]
            
            # 波峰: 前后n日内最高
            if current['high'] == window['high'].max():
                prev = df.iloc[i-1]['close']
                amp = (current['high'] - prev) / prev
                if amp >= 0.01:
                    peaks.append({
                        'date': current['date'],
                        'price': current['high'],
                        'amplitude': amp,
                        'index': i
                    })
            
            # 波谷: 前后n日内最低
            if current['low'] == window['low'].min():
                prev = df.iloc[i-1]['close']
                amp = (prev - current['low']) / prev
                if amp >= 0.01:
                    valleys.append({
                        'date': current['date'],
                        'price': current['low'],
                        'amplitude': amp,
                        'index': i
                    })
        
        self.peaks = peaks
        self.valleys = valleys
        
        print(f"🔍 识别到 {len(peaks)} 个波峰, {len(valleys)} 个波谷")
        return peaks, valleys
    
    def cluster_levels(self, peaks: List[Dict], valleys: List[Dict], 
                      tolerance: float = 0.02) -> Tuple[List[Dict], List[Dict]]:
        """
        聚类生成支撑位和压力位
        
        Args:
            tolerance: 价格容差(2%)
        """
        def cluster(levels: List[Dict]) -> List[Dict]:
            if not levels:
                return []
            
            # 按价格排序
            sorted_levels = sorted(levels, key=lambda x: x['price'])
            clusters = []
            current_cluster = [sorted_levels[0]]
            
            for i in range(1, len(sorted_levels)):
                prev_price = current_cluster[-1]['price']
                curr_price = sorted_levels[i]['price']
                
                if abs(curr_price - prev_price) / prev_price <= tolerance:
                    current_cluster.append(sorted_levels[i])
                else:
                    clusters.append(current_cluster)
                    current_cluster = [sorted_levels[i]]
            
            clusters.append(current_cluster)
            
            # 合并为支撑/压力位
            result = []
            for cluster in clusters:
                prices = [c['price'] for c in cluster]
                avg_price = np.mean(prices)
                touches = [c['date'] for c in cluster]
                
                result.append({
                    'price': round(avg_price, 2),
                    'strength': len(cluster),
                    'touches': touches,
                    'valid': len(cluster) >= 2  # 至少触及2次
                })
            
            return sorted(result, key=lambda x: x['price'], reverse=True)
        
        # 波峰 -> 压力位
        self.resistances = cluster(peaks)
        # 波谷 -> 支撑位
        self.supports = cluster(valleys)
        
        print(f"📍 聚类得到 {len(self.resistances)} 个压力位, {len(self.supports)} 个支撑位")
        return self.resistances, self.supports
    
    def analyze_volume(self) -> Dict:
        """分析成交量状态"""
        if self.data is None:
            raise ValueError("请先调用 fetch_data 获取数据")
            
        df = self.data
        
        # 计算20日均量
        df['volume_ma'] = df['volume'].rolling(window=self.volume_ma).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        # 最新成交量状态
        latest = df.iloc[-1]
        volume_ratio = latest['volume_ratio']
        
        result = {
            'latest_volume': int(latest['volume']),
            'volume_ma': int(latest['volume_ma']),
            'volume_ratio': round(volume_ratio, 2),
            'is_volume_up': volume_ratio > self.volume_threshold,
            'is_volume_down': volume_ratio < 0.5
        }
        
        return result
    
    def detect_breakout(self) -> Dict:
        """检测突破信号"""
        if self.data is None or not self.resistances:
            return {}
            
        df = self.data
        latest = df.iloc[-1]
        
        current_price = latest['close']
        volume_ratio = latest['volume_ratio']
        
        # 检测是否接近压力位
        for res in self.resistances:
            if res['valid']:
                price = res['price']
                diff_pct = (current_price - price) / price * 100
                
                if -3 <= diff_pct <= 3:  # 3%以内
                    is_bullish = latest['close'] > latest['open']
                    
                    if diff_pct >= 0:  # 突破压力位
                        if volume_ratio > self.volume_threshold:
                            signal = '有效突破'
                        else:
                            signal = '假突破可能'
                    else:  # 接近压力位
                        signal = '蓄势待发'
                    
                    return {
                        'type': 'resistance',
                        'level': price,
                        'current_price': current_price,
                        'diff_pct': round(diff_pct, 2),
                        'volume_ratio': round(volume_ratio, 2),
                        'signal': signal,
                        'is_bullish': is_bullish
                    }
        
        # 检测是否接近支撑位
        for sup in self.supports:
            if sup['valid']:
                price = sup['price']
                diff_pct = (current_price - price) / price * 100
                
                if -3 <= diff_pct <= 3:
                    is_bullish = latest['close'] > latest['open']
                    
                    if diff_pct <= 0:  # 跌破支撑位
                        if volume_ratio > self.volume_threshold:
                            signal = '有效跌破'
                        else:
                            signal = '诱空可能'
                    else:  # 获得支撑
                        signal = '获得支撑'
                    
                    return {
                        'type': 'support',
                        'level': price,
                        'current_price': current_price,
                        'diff_pct': round(diff_pct, 2),
                        'volume_ratio': round(volume_ratio, 2),
                        'signal': signal,
                        'is_bullish': is_bullish
                    }
        
        return {}
    
    def run_full_analysis(self, symbol: str, days: int = 250) -> Dict:
        """运行完整分析"""
        # 计算日期
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days*1.5)
        
        # 获取数据
        self.fetch_data(symbol, start_date.strftime('%Y%m%d'))
        
        # 识别波峰波谷
        self.find_peaks_and_valleys()
        
        # 聚类生成支撑压力位
        self.cluster_levels(self.peaks, self.valleys)
        
        # 成交量分析
        volume_info = self.analyze_volume()
        
        # 突破检测
        breakout = self.detect_breakout()
        
        return {
            'symbol': symbol,
            'data': self.data,
            'peaks': self.peaks,
            'valleys': self.valleys,
            'supports': self.supports,
            'resistances': self.resistances,
            'volume': volume_info,
            'breakout': breakout
        }
    
    def visualize(self, symbol: str = None, save_path: str = None):
        """可视化"""
        if self.data is None:
            raise ValueError("请先运行分析")
            
        df = self.data
        
        fig, ax = plt.subplots(figsize=(16, 9))
        
        # 绘制K线 - 优化配色
        up_color = '#E74C3C'    # 上涨红色
        down_color = '#27AE60'  # 下跌绿色
        for idx, row in df.iterrows():
            color = up_color if row['close'] >= row['open'] else down_color
            ax.plot([idx, idx], [row['low'], row['high']], color=color, linewidth=0.8)
            width = 0.6
            ax.plot([idx-width/2, idx+width/2], [row['open'], row['open']], color=color, linewidth=0.8)
            ax.plot([idx-width/2, idx+width/2], [row['close'], row['close']], color=color, linewidth=0.8)
            ax.fill_between([idx-width/2, idx+width/2], row['open'], row['close'], 
                           facecolor=color, alpha=0.4)
        
        # 绘制压力位 - 线宽1.5
        for res in self.resistances:
            if res['valid']:
                ax.axhline(y=res['price'], color='#C0392B', linestyle='--', linewidth=1.5, alpha=0.8)
                ax.text(len(df)-1, res['price'], f"压力:{res['price']}({res['strength']}次)", 
                       va='center', ha='right', fontsize=9, color='#C0392B', fontweight='bold')
        
        # 绘制支撑位 - 线宽1.5
        for sup in self.supports:
            if sup['valid']:
                ax.axhline(y=sup['price'], color='#16A085', linestyle='--', linewidth=1.5, alpha=0.8)
                ax.text(len(df)-1, sup['price'], f"支撑:{sup['price']}({sup['strength']}次)", 
                       va='center', ha='right', fontsize=9, color='#16A085', fontweight='bold')
        
        # 标记波峰波谷 - 优化配色
        for peak in self.peaks[:10]:  # 只标记前10个
            ax.scatter(peak['index'], peak['price'], marker='^', color='#E74C3C', s=60, zorder=5, edgecolors='white', linewidths=0.5)
        for valley in self.valleys[:10]:
            ax.scatter(valley['index'], valley['price'], marker='v', color='#27AE60', s=60, zorder=5, edgecolors='white', linewidths=0.5)
        
        # 设置标题 - 优化配色
        title = f"{symbol or '股票'} 压力位支撑位分析"
        if self.resistances and self.supports:
            latest = df.iloc[-1]
            title += f" | 现价:{latest['close']:.2f}"
        ax.set_title(title, fontsize=14, fontweight='bold', color='#2C3E50')
        
        ax.set_xlabel('交易日', fontsize=11, color='#2C3E50')
        ax.set_ylabel('价格', fontsize=11, color='#2C3E50')
        ax.set_xlim(0, len(df))
        
        # X轴日期标签 - 设置fontstyle='normal'
        tick_positions = np.linspace(0, len(df)-1, min(10, len(df))).astype(int)
        tick_labels = [df.iloc[i]['date'].strftime('%Y-%m-%d') for i in tick_positions]
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=45, fontstyle='normal', fontsize=9)
        
        ax.grid(True, alpha=0.3, color='#BDC3C7')
        ax.set_facecolor('#FAFAFA')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"📊 图表已保存: {save_path}")
        
        plt.show()
        
        return fig


def print_analysis_result(result: Dict):
    """打印分析结果"""
    print("\n" + "="*60)
    print(f"📈 {result['symbol']} 压力位支撑位分析结果")
    print("="*60)
    
    # 压力位
    print("\n🔴 压力位:")
    if result['resistances']:
        for i, res in enumerate(result['resistances'][:5], 1):
            status = "✅有效" if res['valid'] else "❌无效"
            print(f"   {i}. 价格:{res['price']} | 触及:{res['strength']}次 | {status}")
    else:
        print("   无有效压力位")
    
    # 支撑位
    print("\n🟢 支撑位:")
    if result['supports']:
        for i, sup in enumerate(result['supports'][:5], 1):
            status = "✅有效" if sup['valid'] else "❌无效"
            print(f"   {i}. 价格:{sup['price']} | 触及:{sup['strength']}次 | {status}")
    else:
        print("   无有效支撑位")
    
    # 成交量
    vol = result['volume']
    print(f"\n📊 成交量状态:")
    print(f"   现量:{vol['latest_volume']:,} | 均量:{vol['volume_ma']:,} | 量比:{vol['volume_ratio']}")
    
    # 突破信号
    breakout = result['breakout']
    if breakout:
        print(f"\n🎯 突破信号:")
        print(f"   类型:{breakout['type']} | 价位:{breakout['level']}")
        print(f"   现价:{breakout['current_price']:.2f} | 偏离:{breakout['diff_pct']}%")
        print(f"   信号:{breakout['signal']}")
    
    print("\n" + "="*60)


# 测试函数
def test_shanghai_index():
    """测试上证指数"""
    print("\n" + "🌟"*20)
    print("测试: 上证指数 (sh000001)")
    print("🌟"*20 + "\n")
    
    # 降低阈值到2%，更容易识别波峰波谷
    analyzer = SupportResistanceAnalyzer(window=15, min_amplitude=0.02)
    result = analyzer.run_full_analysis('sh000001', days=250)
    print_analysis_result(result)
    
    # 可视化
    analyzer.visualize('上证指数', 'sh000001_sr.png')
    
    return result


def test_stock():
    """测试个股"""
    print("\n" + "🌟"*20)
    print("测试: 贵州茅台 (600519)")
    print("🌟"*20 + "\n")
    
    analyzer = SupportResistanceAnalyzer(window=15, min_amplitude=0.02)
    result = analyzer.run_full_analysis('600519', days=250)
    print_analysis_result(result)
    
    # 可视化
    analyzer.visualize('贵州茅台', '600519_sr.png')
    
    return result


if __name__ == '__main__':
    # 测试上证指数
    test_shanghai_index()
