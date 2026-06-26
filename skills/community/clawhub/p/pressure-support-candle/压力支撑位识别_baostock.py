#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压力位支撑位识别系统（Baostock版）
基于波峰波谷分析和成交量验证
修复：AKShare换用Baostock
"""

import baostock as bs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体（使用系统自带的中文字体）
import matplotlib.font_manager as fm

# 尝试多个中文字体
font_paths = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',
    '/usr/share/fonts/truetype/arphic/uming.ttc',
]

FONT_PROP = None
for fp in font_paths:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
        FONT_PROP = fm.FontProperties(fname=fp)
        plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
        break

# 如果没找到中文字体，使用默认
if FONT_PROP is None:
    FONT_PROP = fm.FontProperties()

plt.rcParams['axes.unicode_minus'] = False

# ========== 配色方案（与股票分红记录技能统一）==========
BG = '#1A1A2E'  # 深蓝黑背景

COLORS = {
    'up': '#FF6B6B',        # 珊瑚红 - 上涨
    'down': '#4ECDC4',     # 青绿色 - 下跌
    'support': '#4ECDC4',  # 青绿色 - 支撑位
    'resistance': '#FF6B6B', # 珊瑚红 - 压力位
    'text': '#FFFFFF',      # 白色文字
    'grid': '#3D3D5C',     # 网格线
    'spine': '#5C5C7A',    # 边框
    'volume_up': '#FF6B6B',   # 上涨成交量
    'volume_down': '#4ECDC4', # 下跌成交量
}


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
        self.symbol = None
        self.peaks = []  # 波峰
        self.valleys = []  # 波谷
        self.supports = []  # 支撑位
        self.resistances = []  # 压力位
        
    def fetch_data(self, symbol: str, start_date: str, end_date: str = None) -> pd.DataFrame:
        """获取K线数据（使用Baostock）"""
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        print(f"📊 正在获取 {symbol} 数据...")
        
        # 转换日期
        start_dt = start_date.replace('/', '-')
        end_dt = end_date.replace('/', '-')
        
        # 转换symbol格式：600989 -> sh.600989
        symbol = str(symbol).strip()
        if not symbol.startswith('sh.') and not symbol.startswith('sz.') and not symbol.startswith('bj.'):
            if symbol.startswith('6'):
                symbol = 'sh.' + symbol
            elif symbol.startswith('0') or symbol.startswith('3'):
                symbol = 'sz.' + symbol
            elif symbol.startswith('8') or symbol.startswith('4'):
                symbol = 'bj.' + symbol
        
        print(f"查询代码: {symbol}")
        
        # Baostock查询
        bs.login()
        rs = bs.query_history_k_data_plus(
            symbol,
            'date,code,open,high,low,close,volume,amount',
            start_date=start_dt,
            end_date=end_dt,
            frequency='d',
            adjustflag='3'  # 不复权
        )
        
        # 转换为DataFrame
        data_list = []
        while (rs.error_code == '0') and rs.next():
            data_list.append(rs.get_row_data())
        
        df = pd.DataFrame(data_list, columns=rs.fields)
        
        if df.empty:
            print(f"❌ 未获取到数据")
            return df
        
        # 统一列名
        df.rename(columns={
            'date': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'amount': 'amount'
        }, inplace=True)
        
        # 转换类型
        for col in ['open', 'high', 'low', 'close', 'volume', 'amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        self.data = df
        self.symbol = symbol
        print(f"✅ 获取到 {len(df)} 条数据")
        
        return df
    
    def find_peaks_and_valleys(self):
        """识别波峰和波谷 - 只识别振幅>=15%的大波段，取波段最高点/最低点"""
        if self.data is None or len(self.data) < 10:
            print("⚠️ 数据不足，无法识别波峰波谷")
            return
        
        prices = self.data['close'].values
        dates = self.data['date'].values
        volumes = self.data['volume'].values
        
        self.peaks = []
        self.valleys = []
        
        # 动态计算波段振幅阈值：根据近20日波动率
        # 波动率 = 日收益率标准差，波动大则振幅阈值高
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns)
        
        # 波段振幅阈值 = max(15%, 波动率 * 3)
        wave_min_amplitude = max(0.15, volatility * 3)
        
        print(f"波动率: {volatility*100:.2f}%, 波段振幅阈值: {wave_min_amplitude*100:.1f}%")
        
        # 找到所有局部极值点
        all_extremes = []  # (index, type, price, date, volume)
        
        for i in range(2, len(prices) - 2):
            # 波峰
            if prices[i] > prices[i-1] and prices[i] > prices[i-2] and \
               prices[i] > prices[i+1] and prices[i] > prices[i+2]:
                all_extremes.append((i, 'peak', prices[i], dates[i], volumes[i]))
            # 波谷
            elif prices[i] < prices[i-1] and prices[i] < prices[i-2] and \
                 prices[i] < prices[i+1] and prices[i] < prices[i+2]:
                all_extremes.append((i, 'valley', prices[i], dates[i], volumes[i]))
        
        if len(all_extremes) < 2:
            print("⚠️ 未识别到足够的波峰波谷")
            return
        
        # 按日期排序
        all_extremes.sort(key=lambda x: x[0])
        
        # 简化：只取振幅>=9%的连续极值对，然后取范围内最高/最低点
        # 这样每个大波段只有一对极值点
        
        used_indices = set()
        
        for i in range(len(all_extremes) - 1):
            if i in used_indices or i+1 in used_indices:
                continue
            
            idx1, type1, price1, date1, vol1 = all_extremes[i]
            idx2, type2, price2, date2, vol2 = all_extremes[i+1]
            
            if type1 == type2:
                continue
            
            # 计算振幅
            if type1 == 'peak' and type2 == 'valley':
                amplitude = (price1 - price2) / price1
            elif type1 == 'valley' and type2 == 'peak':
                amplitude = (price2 - price1) / price1
            else:
                continue
            
            # 振幅>=9%才是大波段
            if amplitude >= wave_min_amplitude:
                # 在这个范围内找最高点和最低点
                start_idx = min(idx1, idx2)
                end_idx = max(idx1, idx2)
                
                segment_prices = prices[start_idx:end_idx+1]
                segment_indices = list(range(start_idx, end_idx+1))
                
                max_price = float(max(segment_prices))
                min_price = float(min(segment_prices))
                max_idx = segment_indices[int(np.argmax(segment_prices))]
                min_idx = segment_indices[int(np.argmin(segment_prices))]
                
                # 添加波峰
                vol = volumes[max_idx]
                vol_ma = np.mean(volumes[max(0,max_idx-5):min(len(volumes),max_idx+5)])
                self.peaks.append({
                    'date': dates[max_idx],
                    'price': prices[max_idx],
                    'volume': vol,
                    'volume_ratio': vol / vol_ma if vol_ma > 0 else 0
                })
                
                # 添加波谷
                vol = volumes[min_idx]
                vol_ma = np.mean(volumes[max(0,min_idx-5):min(len(volumes),min_idx+5)])
                self.valleys.append({
                    'date': dates[min_idx],
                    'price': prices[min_idx],
                    'volume': vol,
                    'volume_ratio': vol / vol_ma if vol_ma > 0 else 0
                })
                
                used_indices.add(i)
                used_indices.add(i+1)
        
        # 按日期排序
        self.peaks.sort(key=lambda x: x['date'])
        self.valleys.sort(key=lambda x: x['date'])
        
        print(f"🔍 识别到 {len(self.peaks)} 个波峰，{len(self.valleys)} 个波谷")
        
        print(f"🔍 识别到 {len(self.peaks)} 个波峰，{len(self.valleys)} 个波谷")
    
    def _get_volume_at_price(self, target_date):
        """获取指定日期附近的成交量（取±2天的平均）"""
        try:
            dates = self.data['date']
            idx = None
            for i, d in enumerate(dates):
                if d >= target_date:
                    idx = i
                    break
            if idx is None:
                idx = len(dates) - 1
            # 取前后2天的平均成交量
            start_idx = max(0, idx - 2)
            end_idx = min(len(self.data), idx + 3)
            vol = self.data['volume'].iloc[start_idx:end_idx].mean()
            return vol
        except:
            return 0
    
    def find_support_resistance(self, tolerance: float = None):
        """
        识别支撑位和压力位
        1. 支撑压力交换：跌破支撑后变压力，突破压力后变支撑
        2. 相近合并：价格相近的合并
        """
        # 动态计算合并容差：根据当前股价水平
        # 股价越高，相近的绝对值差异越大
        if tolerance is None:
            current_price = self.data['close'].iloc[-1]
            # 容差 = min(6%, 绝对值/当前股价 * 1.2)
            abs_tolerance = current_price * 0.05  # 5%绝对值
            tolerance = min(0.06, abs_tolerance / current_price * 1.2)
        
        print(f"支撑压力合并容差: {tolerance*100:.1f}%")
        
        # ========== 1. 成交密集区分析 ==========
        volumes = self.data['volume'].values
        prices = self.data['close'].values
        dates = self.data['date'].values
        
        # 计算成交量均线
        vol_ma = np.mean(volumes[-20:])  # 近20日均量
        
        # 找到成交量密集区（高于均量1.5倍）
        volume_clusters = []
        for i in range(len(volumes)):
            if volumes[i] > vol_ma * 1.5:
                volume_clusters.append({'price': prices[i], 'date': dates[i], 'volume': volumes[i]})
        
        # 将成交密集区按价格聚类
        if volume_clusters:
            volume_clusters.sort(key=lambda x: x['price'])
            
            # 合并相近的成交密集区
            merged_vol = []
            current_group = [volume_clusters[0]]
            
            for i in range(1, len(volume_clusters)):
                prev_price = current_group[-1]['price']
                curr_price = volume_clusters[i]['price']
                diff_ratio = abs(curr_price - prev_price) / prev_price
                
                if diff_ratio <= tolerance:
                    current_group.append(volume_clusters[i])
                else:
                    merged_vol.append(current_group)
                    current_group = [volume_clusters[i]]
            
            merged_vol.append(current_group)
            
            # 成交密集区的中心价格
            vol_price_levels = []
            for group in merged_vol:
                avg_price = np.mean([p['price'] for p in group])
                total_vol = sum([p['volume'] for p in group])
                latest_date = max([p['date'] for p in group])
                vol_price_levels.append({
                    'price': avg_price,
                    'volume': total_vol,
                    'date': latest_date
                })
            
            print(f"📊 找到 {len(vol_price_levels)} 个成交密集区")
        
        if not self.peaks or not self.valleys:
            self.find_peaks_and_valleys()
        
        if not self.peaks and not self.valleys:
            print("⚠️ 未识别到波峰波谷")
            return
        
        # 获取当前（最新）股价
        current_price = self.data['close'].iloc[-1]
        current_date = self.data['date'].iloc[-1]
        
        print(f"当前股价: {current_price} ({current_date})")
        
        # 收集所有波峰波谷的价格和成交量，按日期排序（从旧到新）
        all_levels = []  # (price, date, type, volume)
        
        for peak in self.peaks:
            all_levels.append((peak['price'], peak['date'], 'peak', peak.get('volume', 0)))
        for valley in self.valleys:
            all_levels.append((valley['price'], valley['date'], 'valley', valley.get('volume', 0)))
        
        all_levels.sort(key=lambda x: x[1])
        
        # 支撑压力动态判断逻辑：
        # 1. 先判断每个价位是否曾被跌破或突破
        # 2. 确认突破：突破后需要在压力位上方稳定（涨幅>3%并稳定N天）
        # 3. 如果只是在压力位附近来回震荡，不能转变为支撑
        
        CONFIRM_BREAKOUT = 0.03  # 突破确认幅度3%
        STABLE_DAYS = 5  # 稳定天数（突破后需在上方稳定5天以上）
        
        supports = []  # 有效支撑位
        resistances = []  # 有效压力位
        
        for price, date, ptype, vol in all_levels:
            # 检查在这个价位之后是否被突破/跌破
            after_data = self.data[self.data['date'] > date]
            
            if len(after_data) > 0:
                max_price = after_data['close'].max()
                min_price = after_data['close'].min()
                latest_price = after_data['close'].iloc[-1]
                
                # 计算突破后在上方稳定的天数
                days_above = 0
                for i in range(len(after_data)):
                    if after_data['close'].iloc[i] > price * (1 + CONFIRM_BREAKOUT):
                        days_above += 1
                
                # 判断是否曾被跌破或突破过
                was_broken_down = min_price < price * (1 - CONFIRM_BREAKOUT)
                was_broken_up = max_price > price * (1 + CONFIRM_BREAKOUT)
                
                # 判断当前是否在价位上方稳定（超过3天）
                currently_stable = days_above >= STABLE_DAYS
                
                # 根据当前股价位置和是否有效突破决定
                if current_price > price:
                    # 当前在价位上方
                    if was_broken_up and currently_stable:
                        # 有效突破后稳定在上方3天以上，是支撑
                        # 获取volume
                        vol = self._get_volume_at_price(date)
                        supports.append({'price': price, 'date': date, 'volume': vol if vol > 0 else self._get_volume_at_price(date)})
                    elif not was_broken_up:
                        # 没有效突破，是压力
                        # 获取volume
                        vol = self._get_volume_at_price(date)
                        resistances.append({'price': price, 'date': date, 'volume': vol if vol > 0 else self._get_volume_at_price(date)})
                    else:
                        # 突破后不稳定，是压力
                        # 找到对应日期的成交量
                        vol = self._get_volume_at_price(date)
                        resistances.append({'price': price, 'date': date, 'volume': vol if vol > 0 else self._get_volume_at_price(date)})
                else:
                    # 当前在价位下方
                    if was_broken_down:
                        # 曾跌破过，是压力
                        vol = self._get_volume_at_price(date)
                        resistances.append({'price': price, 'date': date, 'volume': vol if vol > 0 else self._get_volume_at_price(date)})
                    else:
                        # 没有跌破，是支撑
                        vol = self._get_volume_at_price(date)
                        supports.append({'price': price, 'date': date, 'volume': vol if vol > 0 else self._get_volume_at_price(date)})
            else:
                # 没有后续数据，按当前位置
                vol = self._get_volume_at_price(date)
                if current_price > price:
                    supports.append({'price': price, 'date': date, 'volume': vol})
                else:
                    resistances.append({'price': price, 'date': date, 'volume': vol})
        
        final_supports = supports
        final_resistances = resistances
        
        
        
        # 相近价格合并（容差5%）
        def merge_prices(price_list, tolerance=0.05):
            """合并相近的价格"""
            if not price_list:
                return []
            
            price_list.sort(key=lambda x: x['price'])
            
            merged = []
            current_group = [price_list[0]]
            
            for i in range(1, len(price_list)):
                prev_price = current_group[-1]['price']
                curr_price = price_list[i]['price']
                diff_ratio = abs(curr_price - prev_price) / prev_price
                
                if diff_ratio <= tolerance:
                    current_group.append(price_list[i])
                else:
                    merged.append(current_group)
                    current_group = [price_list[i]]
            
            merged.append(current_group)
            
            result = []
            for group in merged:
                avg_price = np.mean([p['price'] for p in group])
                count = len(group)
                latest_date = max([p['date'] for p in group])
                # 累加成交量
                total_volume = sum([p.get('volume', 0) for p in group])
                result.append({'price': avg_price, 'count': count, 'date': latest_date, 'volume': total_volume})
            
            return result
        
        # 合并支撑位和压力位
        merged_supports = merge_prices(final_supports, tolerance)
        merged_resistances = merge_prices(final_resistances, tolerance)
        
        
        # 跨列表合并：支撑和压力如果很接近，也合并
        # 将支撑和压力合并到一起，然后重新分类
        all_merged = []
        for s in merged_supports:
            all_merged.append({'price': s['price'], 'count': s['count'], 'date': s['date'], 'category': 'support', 'volume': s.get('volume', 0)})
        for r in merged_resistances:
            all_merged.append({'price': r['price'], 'count': r['count'], 'date': r['date'], 'category': 'resistance', 'volume': r.get('volume', 0)})
        
        # 再次合并（这次是支撑和压力一起合并）
        if len(all_merged) > 1:
            all_merged.sort(key=lambda x: x['price'])
            final_all = []
            current_group = [all_merged[0]]
            
            for i in range(1, len(all_merged)):
                prev_price = current_group[-1]['price']
                curr_price = all_merged[i]['price']
                diff_ratio = abs(curr_price - prev_price) / prev_price
                
                if diff_ratio <= tolerance:  # 5%以内合并
                    current_group.append(all_merged[i])
                else:
                    final_all.append(current_group)
                    current_group = [all_merged[i]]
            
            final_all.append(current_group)
            
            # 重新分类为支撑或压力
            new_supports = []
            new_resistances = []
            
            for group in final_all:
                avg_price = np.mean([p['price'] for p in group])
                count = len(group)
                latest_date = max([p['date'] for p in group])
                
                # 多数决定类型
                support_count = sum(1 for p in group if p['category'] == 'support')
                resistance_count = sum(1 for p in group if p['category'] == 'resistance')
                
                # 累加成交量
                total_volume = sum([p.get('volume', 0) for p in group])
                
                if support_count >= resistance_count:
                    new_supports.append({'price': avg_price, 'count': count, 'type': '支撑', 'volume': total_volume})
                else:
                    new_resistances.append({'price': avg_price, 'count': count, 'type': '压力', 'volume': total_volume})
            
            merged_supports = new_supports
            merged_resistances = new_resistances
        
        # ========== 2. 成交密集区作为参考（暂不加为独立支撑压力）==========
        # 只保留波峰波谷的支撑压力，避免混乱
        # if 'vol_price_levels' in dir() and vol_price_levels:
        #     for v in vol_price_levels:
        #         v_price = v['price']
        #         if v_price > current_price:
        #             merged_resistances.append({'price': v_price, 'count': v['volume']/1e6, 'type': 'vol'})
        #         else:
        #             merged_supports.append({'price': v_price, 'count': v['volume']/1e6, 'type': 'vol'})
        
        # 转换为输出格式
        self.supports = [{'price': s['price'], 'count': s['count'], 'type': '支撑', 'volume': s.get('volume', 0)} for s in merged_supports]
        self.resistances = [{'price': r['price'], 'count': r['count'], 'type': '压力', 'volume': r.get('volume', 0)} for r in merged_resistances]
        
        # 按价格排序
        self.supports.sort(key=lambda x: x['price'])
        self.resistances.sort(key=lambda x: x['price'], reverse=True)
        
        print(f"💪 识别到 {len(self.supports)} 个支撑位，{len(self.resistances)} 个压力位")
        
        print(f"💪 识别到 {len(self.supports)} 个支撑位，{len(self.resistances)} 个压力位")
    
    def plot_candlestick(self, title: str = "压力位支撑位分析"):
        """绘制K线图"""
        if self.data is None:
            print("⚠️ 没有数据")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), 
                                        gridspec_kw={'height_ratios': [3, 1]},
                                        facecolor=BG)
        
        # 设置背景色
        ax1.set_facecolor(BG)
        ax2.set_facecolor(BG)
        
        # K线图
        dates = range(len(self.data))
        opens = self.data['open'].values
        closes = self.data['close'].values
        highs = self.data['high'].values
        lows = self.data['low'].values
        
        # 绘制K线（使用珊瑚红/青绿配色）
        for i, (date, o, c, h, l) in enumerate(zip(dates, opens, closes, highs, lows)):
            color = COLORS['up'] if c >= o else COLORS['down']
            ax1.plot([i, i], [l, h], color=color, linewidth=0.8)
            ax1.plot([i-0.3, i+0.3], [o, o], color=color, linewidth=0.8)
            ax1.plot([i-0.3, i+0.3], [c, c], color=color, linewidth=0.8)
            ax1.fill_between([i-0.3, i+0.3], o, c, 
                           color=color, alpha=0.4)
        
        # 计算成交量均线，用于判断强弱
        vol_ma = np.mean(self.data['volume'].values[-20:])
        
        # 标记支撑位（青绿色）- 根据成交量分强弱
        for sup in self.supports[:5]:
            price = sup['price']
            vol = sup.get('volume', 0)
            vol_ratio = vol / vol_ma if vol_ma > 0 and vol > 0 else 0
            
            # 成交量大于均量1.5倍为强支撑
            if vol_ratio > 1.5:
                label = f"强支撑 {price:.2f}"
                linewidth = 2.5
            else:
                label = f"支撑 {price:.2f}"
                linewidth = 1.5
            
            ax1.axhline(y=price, color=COLORS['support'], linestyle='--', 
                      linewidth=linewidth, alpha=0.8)
            ax1.text(len(self.data)-1, price, label, 
                    color=COLORS['support'], fontsize=12, va='top',
                    fontweight='bold', fontproperties=FONT_PROP,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, 
                             edgecolor=COLORS['support'], alpha=0.8))
        
        # 标记压力位（珊瑚红）- 根据成交量分强弱
        for res in self.resistances[:5]:
            price = res['price']
            vol = res.get('volume', 0)
            vol_ratio = vol / vol_ma if vol_ma > 0 and vol > 0 else 0
            
            # 成交量大于均量1.5倍为强压力
            if vol_ratio > 1.5:
                label = f"强压力 {price:.2f}"
                linewidth = 2.5
            else:
                label = f"压力 {price:.2f}"
                linewidth = 1.5
            
            ax1.axhline(y=price, color=COLORS['resistance'], linestyle='--', 
                      linewidth=linewidth, alpha=0.8)
            ax1.text(len(self.data)-1, price, label, 
                    color=COLORS['resistance'], fontsize=12, va='bottom',
                    fontweight='bold', fontproperties=FONT_PROP,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, 
                             edgecolor=COLORS['resistance'], alpha=0.8))
        
        # 设置标题和标签
        ax1.set_title(title, fontsize=20, color=COLORS['text'], fontweight='bold', pad=15, fontproperties=FONT_PROP)
        ax1.set_ylabel('价格', color=COLORS['text'], fontsize=14, fontproperties=FONT_PROP)
        
        # X轴不显示标签（用成交量图的X轴统一显示）
        ax1.set_xticks([])
        
        # Y轴数字用默认字体（不是中文），保持白色
        ax1.tick_params(colors=COLORS['text'], labelsize=12)
        for label in ax1.get_yticklabels():
            label.set_color(COLORS['text'])
            label.set_fontsize(12)
        
        ax1.grid(True, color=COLORS['grid'], alpha=0.3, linestyle='-')
        
        # 美化边框
        for spine in ax1.spines.values():
            spine.set_color(COLORS['spine'])
        for spine in ax2.spines.values():
            spine.set_color(COLORS['spine'])
        
        # 成交量（使用新配色）
        ax2.bar(dates, self.data['volume'].values, 
               color=[COLORS['volume_up'] if c >= o else COLORS['volume_down'] 
                     for o, c in zip(opens, closes)], alpha=0.5)
        ax2.set_ylabel('成交量', color=COLORS['text'], fontsize=14, fontproperties=FONT_PROP)
        ax2.set_xlabel('交易日', color=COLORS['text'], fontsize=14, fontproperties=FONT_PROP)
        
        # 设置X轴日期标签（每20天显示一个）
        tick_positions = list(range(0, len(self.data), max(1, len(self.data)//10)))
        tick_labels = [self.data['date'].iloc[i].strftime('%Y-%m-%d') for i in tick_positions]
        ax2.set_xticks(tick_positions)
        
        # 设置刻度标签使用中文字体
        for label in ax2.get_xticklabels() + ax2.get_yticklabels():
            label.set_fontproperties(FONT_PROP)
            label.set_color(COLORS['text'])
            label.set_fontsize(11)
        
        ax2.set_xticklabels(tick_labels, rotation=30, ha='right')
        
        ax2.grid(True, color=COLORS['grid'], alpha=0.3, linestyle='-')
        
        # 保存到桌面
        output_dir = os.path.expanduser("~/Desktop")
        stock_code = self.symbol.replace('sh.', '').replace('sz.', '').replace('bj.', '')
        filename = f"压力支撑位_{stock_code}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor=BG)
        print(f"📈 图片已保存: {filepath}")
        
        return filepath
    
    def get_summary(self) -> Dict:
        """获取分析摘要"""
        return {
            'data_count': len(self.data) if self.data is not None else 0,
            'peak_count': len(self.peaks),
            'valley_count': len(self.valleys),
            'support_count': len(self.supports),
            'resistance_count': len(self.resistances),
            'supports': self.supports[:5],
            'resistances': self.resistances[:5]
        }


def get_stock_name(symbol: str) -> str:
    """获取股票名称"""
    # 去掉sh.前缀
    code = symbol.replace('sh.', '').replace('sz.', '').replace('bj.', '')
    
    # 常用股票名称字典
    STOCK_NAMES = {
        '600989': '宝丰能源',
        '600987': '航民股份',
        '600519': '贵州茅台',
        '600585': '海螺水泥',
        '000001': '平安银行',
        '600036': '招商银行',
    }
    
    return STOCK_NAMES.get(code, code)

def analyze_stock(symbol: str, start_date: str = None, 
                  end_date: str = None, window: int = 20):
    """分析股票"""
    # 获取股票名称
    stock_name = get_stock_name(symbol)
    
    # 如果未指定start_date，默认获取近120天数据
    if start_date is None:
        from datetime import timedelta
        end_date = datetime.now()
        start_date = (end_date - timedelta(days=120)).strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
    
    # 登录Baostock
    bs.login()
    
    analyzer = SupportResistanceAnalyzer(window=window)
    
    # 获取数据
    df = analyzer.fetch_data(symbol, start_date, end_date)
    
    if df is None or df.empty:
        bs.logout()
        return None
    
    # 分析
    analyzer.find_peaks_and_valleys()
    analyzer.find_support_resistance()
    
    # 绘图
    try:
        analyzer.plot_candlestick(f"{stock_name} ({symbol}) 压力位支撑位分析")
    except Exception as e:
        print(f"绘图失败: {e}")
    
    # 登出
    bs.logout()
    
    return analyzer.get_summary()


if __name__ == '__main__':
    # 测试
    print("="*50)
    print("压力支撑位分析工具 (Baostock版)")
    print("="*50)
    
    # 分析宝丰能源
    result = analyze_stock('600989', '2024-01-01', window=20)
    
    if result:
        print("\n📊 分析结果:")
        print(f"数据量: {result['data_count']}条")
        print(f"波峰: {result['peak_count']}个")
        print(f"波谷: {result['valley_count']}个")
        print(f"\n💪 支撑位:")
        for s in result['supports']:
            print(f"  {s['price']:.2f}元 ({s['count']}次)")
        print(f"\n🔺 压力位:")
        for r in result['resistances']:
            print(f"  {r['price']:.2f}元 ({r['count']}次)")
