# -*- coding: utf-8 -*-
"""
仪表 - Instruments
==================

温度/压力/流量/分析仪表绘制

增强版本：
- 使用 matplotlib 标准标记（+、x、s 等）
- 支持多种仪表类型
- 更符合化工行业标准
"""

from matplotlib.patches import Circle, Rectangle
from matplotlib.lines import Line2D
from ..core.colors import INSTRUMENT_COLORS


class Instrument:
    """
    仪表基类（圆形+符号）
    
    Args:
        x, y: 仪表中心坐标
        tag: 位号（如 'TIC-101'）
        inst_type: 仪表类型
        size: 尺寸
    """
    
    # 仪表类型对应的符号（显示在圆内）
    TYPE_SYMBOLS = {
        'TI': 'TI',
        'TE': 'TE', 
        'TIC': 'TIC',
        'TICL': 'TIC',  # 带本地显示
        'PI': 'PI',
        'PE': 'PE',
        'PIC': 'PIC',
        'FI': 'FI',
        'FE': 'FE',
        'FIC': 'FIC',
        'PT': 'PT',
        'PS': 'PS',
        'PSH': 'PSH',
        'PSL': 'PSL',
        'AE': 'AE',
        'AI': 'AI',
        'default': 'IN',
    }
    
    def __init__(self, x, y, tag='', inst_type='default', size=0.25):
        self.x = x
        self.y = y
        self.tag = tag
        self.inst_type = inst_type
        self.size = size
        
    def draw(self, ax):
        """绘制仪表"""
        colors = INSTRUMENT_COLORS['default']
        
        # 圆形仪表（双圆环）
        circle = Circle((self.x, self.y), self.size/2,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=2,
                      zorder=6)
        ax.add_patch(circle)
        
        # 内圈
        inner_circle = Circle((self.x, self.y), self.size/4,
                            facecolor='white',
                            edgecolor=colors['edgecolor'],
                            linewidth=1,
                            zorder=7)
        ax.add_patch(inner_circle)
        
        # 仪表符号（+ 标记用于测量）
        ax.scatter([self.x], [self.y], marker='+', s=50,
                  color=colors['edgecolor'], zorder=8, linewidth=1.5)
        
        # 位号标签（在下方）
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.12,
                   self.tag, ha='center', va='top',
                   fontsize=7, fontweight='bold',
                   color=colors['label_color'], zorder=7)
                   
    def get_connection_points(self):
        """获取连接点"""
        return {
            'top': (self.x, self.y + self.size/2),
            'bottom': (self.x, self.y - self.size/2),
            'left': (self.x - self.size/2, self.y),
            'right': (self.x + self.size/2, self.y),
        }


# ===================== 便捷子类 =====================

class TIC(Instrument):
    """温度指示控制器"""
    def __init__(self, x, y, tag='TIC-101', size=0.28):
        super().__init__(x, y, tag, 'TIC', size)
        
    def draw(self, ax):
        """绘制TIC - 使用T标记"""
        colors = INSTRUMENT_COLORS.get('temperature', INSTRUMENT_COLORS['default'])
        
        # 圆形仪表
        circle = Circle((self.x, self.y), self.size/2,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=2,
                      zorder=6)
        ax.add_patch(circle)
        
        # T 标记
        ax.text(self.x, self.y,
               'T', ha='center', va='center',
               fontsize=10, fontweight='bold',
               color=colors['label_color'], zorder=7)
        
        # 位号标签
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.12,
                   self.tag, ha='center', va='top',
                   fontsize=7, fontweight='bold',
                   color=colors['label_color'], zorder=7)


class PIC(Instrument):
    """压力指示控制器"""
    def __init__(self, x, y, tag='PIC-101', size=0.28):
        super().__init__(x, y, tag, 'PIC', size)
        
    def draw(self, ax):
        """绘制PIC - 使用P标记"""
        colors = INSTRUMENT_COLORS.get('pressure', INSTRUMENT_COLORS['default'])
        
        circle = Circle((self.x, self.y), self.size/2,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=2,
                      zorder=6)
        ax.add_patch(circle)
        
        # P 标记
        ax.text(self.x, self.y,
               'P', ha='center', va='center',
               fontsize=10, fontweight='bold',
               color=colors['label_color'], zorder=7)
        
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.12,
                   self.tag, ha='center', va='top',
                   fontsize=7, fontweight='bold',
                   color=colors['label_color'], zorder=7)


class FIC(Instrument):
    """流量指示控制器"""
    def __init__(self, x, y, tag='FIC-101', size=0.28):
        super().__init__(x, y, tag, 'FIC', size)
        
    def draw(self, ax):
        """绘制FIC - 使用F标记"""
        colors = INSTRUMENT_COLORS.get('flow', INSTRUMENT_COLORS['default'])
        
        circle = Circle((self.x, self.y), self.size/2,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=2,
                      zorder=6)
        ax.add_patch(circle)
        
        # F 标记
        ax.text(self.x, self.y,
               'F', ha='center', va='center',
               fontsize=10, fontweight='bold',
               color=colors['label_color'], zorder=7)
        
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.12,
                   self.tag, ha='center', va='top',
                   fontsize=7, fontweight='bold',
                   color=colors['label_color'], zorder=7)


class TE(Instrument):
    """温度传感器"""
    def __init__(self, x, y, tag='TE-101', size=0.22):
        super().__init__(x, y, tag, 'TE', size)
        
    def draw(self, ax):
        """绘制TE - 圆形带T"""
        colors = INSTRUMENT_COLORS.get('temperature', INSTRUMENT_COLORS['default'])
        
        # 圆形
        circle = Circle((self.x, self.y), self.size/2,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=1.5,
                      zorder=6)
        ax.add_patch(circle)
        
        # T 符号
        ax.text(self.x, self.y,
               'T', ha='center', va='center',
               fontsize=8, fontweight='bold',
               color=colors['label_color'], zorder=7)
        
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.1,
                   self.tag, ha='center', va='top',
                   fontsize=6, color=colors['label_color'], zorder=7)


class PE(Instrument):
    """压力传感器"""
    def __init__(self, x, y, tag='PE-101', size=0.22):
        super().__init__(x, y, tag, 'PE', size)
        
    def draw(self, ax):
        """绘制PE - 圆形带P"""
        colors = INSTRUMENT_COLORS.get('pressure', INSTRUMENT_COLORS['default'])
        
        circle = Circle((self.x, self.y), self.size/2,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=1.5,
                      zorder=6)
        ax.add_patch(circle)
        
        ax.text(self.x, self.y,
               'P', ha='center', va='center',
               fontsize=8, fontweight='bold',
               color=colors['label_color'], zorder=7)
        
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.1,
                   self.tag, ha='center', va='top',
                   fontsize=6, color=colors['label_color'], zorder=7)


class FE(Instrument):
    """流量元件"""
    def __init__(self, x, y, tag='FE-101', size=0.22):
        super().__init__(x, y, tag, 'FE', size)
        
    def draw(self, ax):
        """绘制FE - 圆形带F"""
        colors = INSTRUMENT_COLORS.get('flow', INSTRUMENT_COLORS['default'])
        
        circle = Circle((self.x, self.y), self.size/2,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=1.5,
                      zorder=6)
        ax.add_patch(circle)
        
        ax.text(self.x, self.y,
               'F', ha='center', va='center',
               fontsize=8, fontweight='bold',
               color=colors['label_color'], zorder=7)
        
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.1,
                   self.tag, ha='center', va='top',
                   fontsize=6, color=colors['label_color'], zorder=7)


class PSH(Instrument):
    """压力开关（高报）"""
    def __init__(self, x, y, tag='PSH-101', size=0.22):
        super().__init__(x, y, tag, 'PSH', size)
        
    def draw(self, ax):
        """绘制PSH - 三角形高报标记"""
        colors = INSTRUMENT_COLORS.get('pressure', INSTRUMENT_COLORS['default'])
        
        circle = Circle((self.x, self.y), self.size/2,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=1.5,
                      zorder=6)
        ax.add_patch(circle)
        
        # 上三角标记（表示高报）
        ax.scatter([self.x], [self.y + self.size*0.15], marker='^', s=40,
                  color=colors['edgecolor'], zorder=7)
        
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.1,
                   self.tag, ha='center', va='top',
                   fontsize=6, color=colors['label_color'], zorder=7)


class PSL(Instrument):
    """压力开关（低报）"""
    def __init__(self, x, y, tag='PSL-101', size=0.22):
        super().__init__(x, y, tag, 'PSL', size)
        
    def draw(self, ax):
        """绘制PSL - 三角形低报标记"""
        colors = INSTRUMENT_COLORS.get('pressure', INSTRUMENT_COLORS['default'])
        
        circle = Circle((self.x, self.y), self.size/2,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=1.5,
                      zorder=6)
        ax.add_patch(circle)
        
        # 下三角标记（表示低报）
        ax.scatter([self.x], [self.y - self.size*0.15], marker='v', s=40,
                  color=colors['edgecolor'], zorder=7)
        
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.1,
                   self.tag, ha='center', va='top',
                   fontsize=6, color=colors['label_color'], zorder=7)


class AE(Instrument):
    """在线分析仪"""
    def __init__(self, x, y, tag='AE-101', size=0.30):
        super().__init__(x, y, tag, 'AE', size)
        
    def draw(self, ax):
        """绘制AE - 六边形分析标记"""
        colors = INSTRUMENT_COLORS.get('analysis', INSTRUMENT_COLORS['default'])
        
        # 六边形
        angles = np.linspace(0, 2*np.pi, 7)[:-1]
        hex_x = self.x + self.size/2 * np.cos(angles)
        hex_y = self.y + self.size/2 * np.sin(angles)
        
        from matplotlib.patches import Polygon as MplPolygon
        hex_pts = np.column_stack([hex_x, hex_y])
        hex_patch = MplPolygon(hex_pts, closed=True,
                               facecolor=colors['facecolor'],
                               edgecolor=colors['edgecolor'],
                               linewidth=1.5,
                               zorder=6)
        ax.add_patch(hex_patch)
        
        # A 标记
        ax.text(self.x, self.y,
               'A', ha='center', va='center',
               fontsize=9, fontweight='bold',
               color=colors['label_color'], zorder=7)
        
        if self.tag:
            ax.text(self.x, self.y - self.size/2 - 0.12,
                   self.tag, ha='center', va='top',
                   fontsize=6, color=colors['label_color'], zorder=7)


# 导入numpy用于AE仪表的六边形计算
import numpy as np
