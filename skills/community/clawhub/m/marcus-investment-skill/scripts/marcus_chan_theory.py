#!/usr/bin/env python3
"""
Marcus Trading Agent - 缠论分析模块
功能：缠论技术形态识别（笔、线段、中枢、背驰、买卖点）
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Fractal:
    """分型"""
    type: str  # top/bottom (顶/底)
    index: int  # K 线索引
    price: float  # 分型价格
    date: str  # 日期
    confirmed: bool  # 是否确认

@dataclass
class Stroke:
    """笔"""
    direction: str  # up/down (上/下)
    start_index: int
    end_index: int
    start_price: float
    end_price: float
    start_date: str
    end_date: str
    height: float  # 笔的高度
    confirmed: bool

@dataclass
class Segment:
    """线段"""
    direction: str  # up/down
    start_index: int
    end_index: int
    start_price: float
    end_price: float
    start_date: str
    end_date: str
    strokes_count: int  # 包含的笔数
    confirmed: bool

@dataclass
class Zhongshu:
    """中枢"""
    level: int  # 中枢级别 (1/2/3...)
    start_index: int
    end_index: int
    start_date: str
    end_date: str
    high: float  # 中枢上沿 (ZG)
    low: float  # 中枢下沿 (ZD)
    entries: List[int]  # 进入中枢的笔索引
    exits: List[int]  # 离开中枢的笔索引
    status: str  # forming/confirmed/destroyed

@dataclass
class Beichi:
    """背驰"""
    type: str  # bullish/bearish (底背驰/顶背驰)
    level: str  # trend/segment/stroke (趋势/线段/笔)
    price_high: float  # 价格高点
    price_low: float  # 价格低点
    indicator_high: float  # 指标高点 (MACD)
    indicator_low: float  # 指标低点
    divergence: float  # 背驰程度
    confirmed: bool
    date: str

@dataclass
class TradingPoint:
    """买卖点"""
    type: str  # buy1/buy2/buy3/sell1/sell2/sell3
    name: str  # 第一类买点/第二类买点...
    index: int
    price: float
    date: str
    confidence: float  # 0-1
    description: str

class ChanTheoryAnalyzer:
    """缠论分析器"""
    
    def __init__(self, data: pd.DataFrame):
        """
        初始化缠论分析器
        
        Args:
            data: 包含 OHLC 数据的 DataFrame，列名：['日期', '开盘', '最高', '最低', '收盘']
        """
        self.data = data.copy()
        self.data = self.data.reset_index(drop=True)
        
        # 分析结果
        self.fractals: List[Fractal] = []
        self.strokes: List[Stroke] = []
        self.segments: List[Segment] = []
        self.zhongshus: List[Zhongshu] = []
        self.beichis: List[Beichi] = []
        self.trading_points: List[TradingPoint] = []
        
        # MACD 数据（用于背驰判断）
        self.macd_data = None
        
    def detect_fractals(self) -> List[Fractal]:
        """
        检测分型（顶分型和底分型）
        
        顶分型：中间 K 线高点最高，且左右两根 K 线高点都低于它
        底分型：中间 K 线低点最低，且左右两根 K 线低点都高于它
        """
        print("\n【检测分型】")
        self.fractals = []
        
        for i in range(2, len(self.data) - 2):
            row_prev = self.data.iloc[i-1]
            row_curr = self.data.iloc[i]
            row_next = self.data.iloc[i+1]
            
            # 顶分型检测
            if (row_curr['最高'] > row_prev['最高'] and 
                row_curr['最高'] > row_next['最高'] and
                row_curr['最高'] >= row_prev.get('最高', row_prev['最高']) and
                row_curr['最高'] >= row_next.get('最高', row_next['最高'])):
                
                # 确认：需要后续 K 线不破顶
                confirmed = i < len(self.data) - 3 and self.data.iloc[i+2]['最高'] < row_curr['最高']
                
                fractal = Fractal(
                    type='top',
                    index=i,
                    price=row_curr['最高'],
                    date=str(row_curr['日期']),
                    confirmed=confirmed
                )
                self.fractals.append(fractal)
            
            # 底分型检测
            elif (row_curr['最低'] < row_prev['最低'] and 
                  row_curr['最低'] < row_next['最低'] and
                  row_curr['最低'] <= row_prev.get('最低', row_prev['最低']) and
                  row_curr['最低'] <= row_next.get('最低', row_next['最低'])):
                
                confirmed = i < len(self.data) - 3 and self.data.iloc[i+2]['最低'] > row_curr['最低']
                
                fractal = Fractal(
                    type='bottom',
                    index=i,
                    price=row_curr['最低'],
                    date=str(row_curr['日期']),
                    confirmed=confirmed
                )
                self.fractals.append(fractal)
        
        print(f"  检测到 {len(self.fractals)} 个分型")
        print(f"    顶分型：{sum(1 for f in self.fractals if f.type == 'top')}")
        print(f"    底分型：{sum(1 for f in self.fractals if f.type == 'bottom')}")
        
        return self.fractals
    
    def detect_strokes(self, min_height: float = 0.03) -> List[Stroke]:
        """
        检测笔（连接相邻的顶分型和底分型）
        
        笔的规则：
        1. 顶分型和底分型交替出现
        2. 顶底之间至少有 1 根独立 K 线
        3. 笔的高度超过最小阈值
        """
        print("\n【检测笔】")
        self.strokes = []
        
        if len(self.fractals) < 2:
            print("  分型数量不足，无法检测笔")
            return self.strokes
        
        # 按索引排序分型
        sorted_fractals = sorted(self.fractals, key=lambda f: f.index)
        
        # 过滤相邻同类型分型（只保留极值）
        filtered = []
        for i, fractal in enumerate(sorted_fractals):
            if not filtered:
                filtered.append(fractal)
            else:
                last = filtered[-1]
                # 同类型分型，保留极值更大的
                if last.type == fractal.type:
                    if fractal.type == 'top' and fractal.price > last.price:
                        filtered[-1] = fractal
                    elif fractal.type == 'bottom' and fractal.price < last.price:
                        filtered[-1] = fractal
                else:
                    # 不同类型，检查间隔
                    if fractal.index - last.index >= 3:  # 至少间隔 3 根 K 线
                        filtered.append(fractal)
                    elif fractal.type == 'top' and fractal.price > last.price:
                        filtered[-1] = fractal
                    elif fractal.type == 'bottom' and fractal.price < last.price:
                        filtered[-1] = fractal
        
        # 构建笔
        for i in range(len(filtered) - 1):
            start_f = filtered[i]
            end_f = filtered[i + 1]
            
            # 顶底必须交替
            if (start_f.type == 'top' and end_f.type == 'bottom') or \
               (start_f.type == 'bottom' and end_f.type == 'top'):
                
                direction = 'down' if start_f.type == 'top' else 'up'
                height = abs(end_f.price - start_f.price) / start_f.price
                
                # 检查最小高度
                if height >= min_height:
                    stroke = Stroke(
                        direction=direction,
                        start_index=start_f.index,
                        end_index=end_f.index,
                        start_price=start_f.price,
                        end_price=end_f.price,
                        start_date=start_f.date,
                        end_date=end_f.date,
                        height=height,
                        confirmed=end_f.confirmed
                    )
                    self.strokes.append(stroke)
        
        print(f"  检测到 {len(self.strokes)} 笔")
        print(f"    上笔：{sum(1 for s in self.strokes if s.direction == 'up')}")
        print(f"    下笔：{sum(1 for s in self.strokes if s.direction == 'down')}")
        
        return self.strokes
    
    def detect_segments(self) -> List[Segment]:
        """
        检测线段（至少由三笔组成）
        
        线段规则：
        1. 至少由三笔组成
        2. 连续三笔有重叠部分
        3. 线段方向由第一笔决定
        """
        print("\n【检测线段】")
        self.segments = []
        
        if len(self.strokes) < 3:
            print("  笔数量不足，无法检测线段")
            return self.segments
        
        i = 0
        while i < len(self.strokes) - 2:
            # 尝试构建线段
            segment_strokes = [self.strokes[i]]
            direction = self.strokes[i].direction
            
            j = i + 1
            while j < len(self.strokes):
                stroke = self.strokes[j]
                
                # 检查方向是否交替
                expected_direction = 'down' if direction == 'up' else 'up'
                if stroke.direction != expected_direction:
                    j += 1
                    continue
                
                segment_strokes.append(stroke)
                
                # 至少 3 笔可以构成线段
                if len(segment_strokes) >= 3:
                    # 检查是否有重叠
                    if self._check_strokes_overlap(segment_strokes):
                        last_stroke = segment_strokes[-1]
                        segment = Segment(
                            direction=direction,
                            start_index=segment_strokes[0].start_index,
                            end_index=last_stroke.end_index,
                            start_price=segment_strokes[0].start_price,
                            end_price=last_stroke.end_price,
                            start_date=segment_strokes[0].start_date,
                            end_date=last_stroke.end_date,
                            strokes_count=len(segment_strokes),
                            confirmed=last_stroke.confirmed
                        )
                        self.segments.append(segment)
                        
                        # 移动到下一线段
                        i = j
                        break
                
                j += 1
            
            if j >= len(self.strokes):
                i += 1
        
        print(f"  检测到 {len(self.segments)} 条线段")
        
        return self.segments
    
    def _check_strokes_overlap(self, strokes: List[Stroke]) -> bool:
        """检查多笔是否有重叠部分"""
        if len(strokes) < 3:
            return False
        
        # 取第 1 笔和第 3 笔的重叠
        stroke1 = strokes[0]
        stroke3 = strokes[2]
        
        high1 = max(stroke1.start_price, stroke1.end_price)
        low1 = min(stroke1.start_price, stroke1.end_price)
        high3 = max(stroke3.start_price, stroke3.end_price)
        low3 = min(stroke3.start_price, stroke3.end_price)
        
        # 检查是否有重叠
        return not (high1 < low3 or high3 < low1)
    
    def detect_zhongshus(self) -> List[Zhongshu]:
        """
        检测中枢
        
        中枢规则：
        1. 至少由三个连续次级别走势（笔或线段）重叠部分构成
        2. 中枢有方向（进入段方向）
        3. 中枢有区间 [ZD, ZG]
        """
        print("\n【检测中枢】")
        self.zhongshus = []
        
        if len(self.strokes) < 3:
            print("  笔数量不足，无法检测中枢")
            return self.zhongshus
        
        i = 0
        while i < len(self.strokes) - 2:
            # 尝试构建中枢
            for j in range(i + 2, min(i + 8, len(self.strokes))):  # 最多检查 8 笔
                candidate_strokes = self.strokes[i:j+1]
                
                # 检查是否有 3 笔重叠
                if len(candidate_strokes) >= 3:
                    zhongshu = self._try_build_zhongshu(candidate_strokes)
                    if zhongshu:
                        self.zhongshus.append(zhongshu)
                        i = j + 1
                        break
            else:
                i += 1
        
        print(f"  检测到 {len(self.zhongshus)} 个中枢")
        
        return self.zhongshus
    
    def _try_build_zhongshu(self, strokes: List[Stroke]) -> Optional[Zhongshu]:
        """尝试构建中枢"""
        if len(strokes) < 3:
            return None
        
        # 计算重叠区间
        overlaps = []
        for stroke in strokes:
            high = max(stroke.start_price, stroke.end_price)
            low = min(stroke.start_price, stroke.end_price)
            overlaps.append((low, high))
        
        # 找三个连续笔的重叠
        for i in range(len(overlaps) - 2):
            o1, o2, o3 = overlaps[i], overlaps[i+1], overlaps[i+2]
            
            # 计算重叠区间
            zg = min(o1[1], o2[1], o3[1])  # 中枢上沿
            zd = max(o1[0], o2[0], o3[0])  # 中枢下沿
            
            if zg > zd:  # 有效重叠
                return Zhongshu(
                    level=1,
                    start_index=strokes[i].start_index,
                    end_index=strokes[i+2].end_index,
                    start_date=strokes[i].start_date,
                    end_date=strokes[i+2].end_date,
                    high=zg,
                    low=zd,
                    entries=[i],
                    exits=[i+2],
                    status='confirmed'
                )
        
        return None
    
    def detect_beichis(self) -> List[Beichi]:
        """
        检测背驰（价格新高/低但 MACD 不新高/低）
        """
        print("\n【检测背驰】")
        self.beichis = []
        
        # 计算 MACD
        self._calculate_macd()
        
        if len(self.strokes) < 4:
            print("  笔数量不足，无法检测背驰")
            return self.beichis
        
        # 检测趋势背驰
        for i in range(len(self.strokes) - 3):
            stroke1 = self.strokes[i]
            stroke2 = self.strokes[i + 2]  # 同向笔
            
            if stroke1.direction == stroke2.direction:
                # 检查价格是否创新高/低
                if stroke1.direction == 'up':
                    # 上涨笔，检查是否顶背驰
                    if stroke2.end_price > stroke1.end_price:
                        # 检查 MACD 是否背驰
                        macd_divergence = self._check_macdivergence(
                            stroke1.start_index, stroke1.end_index,
                            stroke2.start_index, stroke2.end_index,
                            'bearish'
                        )
                        if macd_divergence:
                            beichi = Beichi(
                                type='bearish',
                                level='stroke',
                                price_high=stroke2.end_price,
                                price_low=stroke1.end_price,
                                indicator_high=macd_divergence[1],
                                indicator_low=macd_divergence[0],
                                divergence=macd_divergence[2],
                                confirmed=True,
                                date=str(self.data.iloc[stroke2.end_index]['日期'])
                            )
                            self.beichis.append(beichi)
                
                elif stroke1.direction == 'down':
                    # 下跌笔，检查是否底背驰
                    if stroke2.end_price < stroke1.end_price:
                        macd_divergence = self._check_macdivergence(
                            stroke1.start_index, stroke1.end_index,
                            stroke2.start_index, stroke2.end_index,
                            'bullish'
                        )
                        if macd_divergence:
                            beichi = Beichi(
                                type='bullish',
                                level='stroke',
                                price_high=stroke1.end_price,
                                price_low=stroke2.end_price,
                                indicator_high=macd_divergence[0],
                                indicator_low=macd_divergence[1],
                                divergence=macd_divergence[2],
                                confirmed=True,
                                date=str(self.data.iloc[stroke2.end_index]['日期'])
                            )
                            self.beichis.append(beichi)
        
        print(f"  检测到 {len(self.beichis)} 个背驰")
        print(f"    底背驰：{sum(1 for b in self.beichis if b.type == 'bullish')}")
        print(f"    顶背驰：{sum(1 for b in self.beichis if b.type == 'bearish')}")
        
        return self.beichis
    
    def _calculate_macd(self):
        """计算 MACD 指标"""
        if self.macd_data is not None:
            return
        
        data = self.data.copy()
        
        # 计算 EMA
        exp1 = data['收盘'].ewm(span=12, adjust=False).mean()
        exp2 = data['收盘'].ewm(span=26, adjust=False).mean()
        
        # DIF
        dif = exp1 - exp2
        
        # DEA
        dea = dif.ewm(span=9, adjust=False).mean()
        
        # MACD 柱
        macd = (dif - dea) * 2
        
        self.macd_data = pd.DataFrame({
            'DIF': dif,
            'DEA': dea,
            'MACD': macd
        })
    
    def _check_macdivergence(self, start1: int, end1: int, start2: int, end2: int, 
                             divergence_type: str) -> Optional[Tuple[float, float, float]]:
        """
        检查 MACD 背驰
        
        Returns:
            (indicator1, indicator2, divergence_degree) 或 None
        """
        if self.macd_data is None:
            return None
        
        # 计算两段内的 MACD 面积或峰值
        macd1 = self.macd_data.iloc[start1:end1+1]['MACD']
        macd2 = self.macd_data.iloc[start2:end2+1]['MACD']
        
        if divergence_type == 'bearish':
            # 顶背驰：价格新高，MACD 面积/峰值下降
            area1 = macd1[macd1 > 0].sum() if len(macd1[macd1 > 0]) > 0 else 0
            area2 = macd2[macd2 > 0].sum() if len(macd2[macd2 > 0]) > 0 else 0
            
            if area1 > 0 and area2 < area1 * 0.8:  # MACD 面积下降 20% 以上
                divergence = (area1 - area2) / area1
                return (area1, area2, divergence)
        
        elif divergence_type == 'bullish':
            # 底背驰：价格新低，MACD 面积/峰值上升
            area1 = abs(macd1[macd1 < 0].sum()) if len(macd1[macd1 < 0]) > 0 else 0
            area2 = abs(macd2[macd2 < 0].sum()) if len(macd2[macd2 < 0]) > 0 else 0
            
            if area1 > 0 and area2 < area1 * 0.8:
                divergence = (area1 - area2) / area1
                return (area1, area2, divergence)
        
        return None
    
    def detect_trading_points(self) -> List[TradingPoint]:
        """
        检测三类买卖点
        
        第一类买点：趋势底背驰后
        第二类买点：回踩不破前低
        第三类买点：突破中枢后回踩不破中枢上沿
        
        第一类卖点：趋势顶背驰后
        第二类卖点：反弹不破前高
        第三类卖点：跌破中枢后回抽不破中枢下沿
        """
        print("\n【检测买卖点】")
        self.trading_points = []
        
        # 基于背驰检测第一类买卖点
        for beichi in self.beichis:
            if beichi.type == 'bullish':
                # 底背驰 -> 第一类买点
                point = TradingPoint(
                    type='buy1',
                    name='第一类买点',
                    index=self.data[self.data['日期'] == beichi.date].index[0] if beichi.date in self.data['日期'].values else -1,
                    price=beichi.price_low,
                    date=beichi.date,
                    confidence=0.7 + beichi.divergence * 0.3,
                    description=f'趋势底背驰，背驰程度 {beichi.divergence:.2%}'
                )
                self.trading_points.append(point)
            
            elif beichi.type == 'bearish':
                # 顶背驰 -> 第一类卖点
                point = TradingPoint(
                    type='sell1',
                    name='第一类卖点',
                    index=self.data[self.data['日期'] == beichi.date].index[0] if beichi.date in self.data['日期'].values else -1,
                    price=beichi.price_high,
                    date=beichi.date,
                    confidence=0.7 + beichi.divergence * 0.3,
                    description=f'趋势顶背驰，背驰程度 {beichi.divergence:.2%}'
                )
                self.trading_points.append(point)
        
        # 基于中枢检测第三类买卖点
        for zhongshu in self.zhongshus:
            # 检查中枢后的走势
            pass  # 简化实现
        
        print(f"  检测到 {len(self.trading_points)} 个买卖点")
        
        return self.trading_points
    
    def analyze(self) -> Dict:
        """
        完整缠论分析流程
        
        Returns:
            分析结果字典
        """
        print("\n" + "="*50)
        print("【缠论分析开始】")
        print("="*50)
        
        # 依次执行分析步骤
        self.detect_fractals()
        self.detect_strokes()
        self.detect_segments()
        self.detect_zhongshus()
        self.detect_beichis()
        self.detect_trading_points()
        
        # 生成分析摘要
        summary = self._generate_summary()
        
        print("\n" + "="*50)
        print("【缠论分析完成】")
        print("="*50)
        
        return summary
    
    def _generate_summary(self) -> Dict:
        """生成分析摘要"""
        # 当前状态
        latest_price = self.data.iloc[-1]['收盘']
        latest_date = self.data.iloc[-1]['日期']
        
        # 最近的中枢
        latest_zhongshu = self.zhongshus[-1] if self.zhongshus else None
        
        # 最近的背驰
        latest_beichi = self.beichis[-1] if self.beichis else None
        
        # 最近的买卖点
        latest_point = self.trading_points[-1] if self.trading_points else None
        
        # 当前趋势
        current_trend = 'up' if len(self.strokes) > 0 and self.strokes[-1].direction == 'up' else 'down'
        
        summary = {
            'stock_code': self.data.get('股票代码', ['Unknown'])[0] if '股票代码' in self.data.columns else 'Unknown',
            'analysis_date': str(latest_date),
            'latest_price': float(latest_price),
            'current_trend': current_trend,
            'fractals_count': len(self.fractals),
            'strokes_count': len(self.strokes),
            'segments_count': len(self.segments),
            'zhongshus_count': len(self.zhongshus),
            'beichis_count': len(self.beichis),
            'trading_points_count': len(self.trading_points),
            'latest_zhongshu': asdict(latest_zhongshu) if latest_zhongshu else None,
            'latest_beichi': asdict(latest_beichi) if latest_beichi else None,
            'latest_trading_point': asdict(latest_point) if latest_point else None,
            'recommendation': self._generate_recommendation(current_trend, latest_beichi, latest_point, latest_zhongshu)
        }
        
        return summary
    
    def _generate_recommendation(self, trend: str, beichi: Optional[Beichi], 
                                  point: Optional[TradingPoint],
                                  zhongshu: Optional[Zhongshu]) -> Dict:
        """生成操作建议"""
        recommendation = {
            'action': 'HOLD',
            'confidence': 0.5,
            'reason': '',
            'key_levels': []
        }
        
        # 基于买卖点
        if point:
            if point.type in ['buy1', 'buy2', 'buy3']:
                recommendation['action'] = 'BUY'
                recommendation['confidence'] = point.confidence
                recommendation['reason'] = f'缠论{point.name}：{point.description}'
            elif point.type in ['sell1', 'sell2', 'sell3']:
                recommendation['action'] = 'SELL'
                recommendation['confidence'] = point.confidence
                recommendation['reason'] = f'缠论{point.name}：{point.description}'
        
        # 基于背驰
        if beichi and not point:
            if beichi.type == 'bullish':
                recommendation['action'] = 'BUY'
                recommendation['confidence'] = 0.6 + beichi.divergence * 0.4
                recommendation['reason'] = f'底背驰信号，背驰程度 {beichi.divergence:.2%}'
            elif beichi.type == 'bearish':
                recommendation['action'] = 'SELL'
                recommendation['confidence'] = 0.6 + beichi.divergence * 0.4
                recommendation['reason'] = f'顶背驰信号，背驰程度 {beichi.divergence:.2%}'
        
        # 基于中枢位置
        if zhongshu:
            latest_price = self.data.iloc[-1]['收盘']
            if latest_price > zhongshu.high * 1.05:
                recommendation['key_levels'].append(f'中枢上沿：{zhongshu.high:.2f}')
                recommendation['reason'] += ' 价格在中枢上方运行'
            elif latest_price < zhongshu.low * 0.95:
                recommendation['key_levels'].append(f'中枢下沿：{zhongshu.low:.2f}')
                recommendation['reason'] += ' 价格在中枢下方运行'
            else:
                recommendation['key_levels'].append(f'中枢区间：[{zhongshu.low:.2f}, {zhongshu.high:.2f}]')
                recommendation['reason'] += ' 价格在中枢内震荡'
        
        # 默认理由
        if not recommendation['reason']:
            recommendation['reason'] = f'当前趋势：{trend}，无明确买卖点'
        
        return recommendation


def main():
    """测试缠论分析模块"""
    import akshare as ak
    
    # 获取测试数据
    stock_code = "301308"  # 江波龙
    print(f"获取 {stock_code} 数据...")
    
    data = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date="20250101",
        adjust="qfq"
    )
    
    # 重命名列
    data = data.rename(columns={
        '日期': '日期',
        '开盘': '开盘',
        '收盘': '收盘',
        '最高': '最高',
        '最低': '最低',
        '成交量': '成交量',
        '成交额': '成交额'
    })
    
    # 创建分析器
    analyzer = ChanTheoryAnalyzer(data)
    
    # 执行分析
    result = analyzer.analyze()
    
    # 打印结果
    print("\n" + "="*50)
    print("【缠论分析结果】")
    print("="*50)
    print(f"股票：{result.get('stock_code', 'Unknown')}")
    print(f"分析日期：{result.get('analysis_date', 'Unknown')}")
    print(f"最新价：{result.get('latest_price', 0):.2f}")
    print(f"当前趋势：{result.get('current_trend', 'Unknown')}")
    print(f"\n分型：{result.get('fractals_count', 0)}")
    print(f"笔：{result.get('strokes_count', 0)}")
    print(f"线段：{result.get('segments_count', 0)}")
    print(f"中枢：{result.get('zhongshus_count', 0)}")
    print(f"背驰：{result.get('beichis_count', 0)}")
    print(f"买卖点：{result.get('trading_points_count', 0)}")
    
    rec = result.get('recommendation', {})
    print(f"\n【操作建议】")
    print(f"  动作：{rec.get('action', 'HOLD')}")
    print(f"  置信度：{rec.get('confidence', 0):.2%}")
    print(f"  理由：{rec.get('reason', '')}")
    if rec.get('key_levels'):
        print(f"  关键位：{rec.get('key_levels')}")


if __name__ == "__main__":
    main()
