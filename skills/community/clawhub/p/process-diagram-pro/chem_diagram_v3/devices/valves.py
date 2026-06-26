# -*- coding: utf-8 -*-
"""
阀门 - Valves
=============

调节阀、ESD阀、安全阀等设备绘制

增强版本：
- 使用 matplotlib marker 作为辅助标记
- 支持多种阀门符号风格
- 更灵活的样式配置
"""

from matplotlib.patches import Circle, Polygon as MplPolygon, FancyArrowPatch
from matplotlib.lines import Line2D
from ..core.colors import VALVE_COLORS


class Valve:
    """
    阀门基类
    
    Args:
        x, y: 阀门中心坐标
        tag: 位号（如 'TV-101'）
        valve_type: 阀门类型
        size: 尺寸
    """
    
    def __init__(self, x, y, tag='', valve_type='control', size=0.25):
        self.x = x
        self.y = y
        self.tag = tag
        self.valve_type = valve_type
        self.size = size
        
    def draw(self, ax):
        """绘制阀门（由子类实现具体形状）"""
        pass
        
    def get_connection_points(self):
        """获取连接点"""
        return {
            'left': (self.x - self.size/2, self.y),
            'right': (self.x + self.size/2, self.y),
            'top': (self.x, self.y + self.size/2),
            'bottom': (self.x, self.y - self.size/2),
        }


class ControlValve(Valve):
    """
    调节阀（气动）
    
    绘制风筝形符号 + 弹簧线
    
    Args:
        x, y: 阀门中心坐标
        tag: 位号（如 'TV-101'）
        size: 尺寸
    """
    
    def __init__(self, x, y, tag='', size=0.25):
        super().__init__(x, y, tag, 'control', size)
        
    def draw(self, ax):
        """绘制调节阀"""
        colors = VALVE_COLORS['control']
        s = self.size
        
        # 风筝形阀体
        kv = MplPolygon([[self.x, self.y - s*0.5],
                         [self.x + s*0.5, self.y],
                         [self.x, self.y + s*0.5],
                         [self.x - s*0.5, self.y]],
                        closed=True,
                        facecolor=colors['facecolor'],
                        edgecolor=colors['edgecolor'],
                        linewidth=1.5,
                        zorder=5)
        ax.add_patch(kv)
        
        # 弹簧线（上方）- 使用虚线风格
        ax.plot([self.x, self.x], [self.y + s*0.5, self.y + s*0.7],
               color='#455A64', linewidth=1.2, linestyle='--', zorder=4)
        ax.plot([self.x - s*0.15, self.x + s*0.15], 
               [self.y + s*0.7, self.y + s*0.7],
               color='#455A64', linewidth=1.2, zorder=4)
        
        # 添加菱形标记点（辅助识别）
        ax.scatter([self.x], [self.y], marker='D', s=20, 
                  color=colors['edgecolor'], zorder=6)
        
        # 标签
        if self.tag:
            ax.text(self.x, self.y - s*0.75,
                   self.tag, ha='center', va='top',
                   fontsize=7, fontweight='bold',
                   color=colors['label_color'], zorder=6)


class ESDValve(Valve):
    """
    ESD紧急切断阀
    
    绘制五边形符号（红色）
    
    Args:
        x, y: 阀门中心坐标
        tag: 位号（如 'XV-101'）
        size: 尺寸
    """
    
    def __init__(self, x, y, tag='', size=0.25):
        super().__init__(x, y, tag, 'esd', size)
        
    def draw(self, ax):
        """绘制ESD阀"""
        colors = VALVE_COLORS['esd']
        s = self.size
        
        # 五边形
        pent = MplPolygon([[self.x, self.y + s*0.5],
                          [self.x + s*0.4, self.y + s*0.2],
                          [self.x + s*0.4, self.y - s*0.4],
                          [self.x - s*0.4, self.y - s*0.4],
                          [self.x - s*0.4, self.y + s*0.2]],
                         closed=True,
                         facecolor=colors['facecolor'],
                         edgecolor=colors['edgecolor'],
                         linewidth=2,
                         zorder=5)
        ax.add_patch(pent)
        
        # 添加红色边框强调
        ax.add_patch(Circle((self.x, self.y), s*0.15,
                           facecolor=colors['edgecolor'],
                           edgecolor=colors['edgecolor'],
                           linewidth=1,
                           zorder=6))
        
        # 标签
        if self.tag:
            ax.text(self.x, self.y - s*0.65,
                   self.tag, ha='center', va='top',
                   fontsize=7, fontweight='bold',
                   color=colors['label_color'], zorder=6)


class SafetyValve(Valve):
    """
    安全阀
    
    绘制半圆形+箭头符号
    
    Args:
        x, y: 阀门中心坐标
        tag: 位号（如 'PSV-101'）
        size: 尺寸
    """
    
    def __init__(self, x, y, tag='', size=0.25):
        super().__init__(x, y, tag, 'safety', size)
        
    def draw(self, ax):
        """绘制安全阀"""
        colors = VALVE_COLORS['safety']
        s = self.size
        
        # 半圆
        circle = Circle((self.x, self.y + s*0.1), s*0.4,
                      facecolor=colors['facecolor'],
                      edgecolor=colors['edgecolor'],
                      linewidth=1.5,
                      zorder=5)
        ax.add_patch(circle)
        
        # 向下箭头（使用三角标记）
        ax.scatter([self.x], [self.y - s*0.3], marker='v', s=50,
                  color=colors['edgecolor'], zorder=6)
        ax.plot([self.x, self.x], [self.y - s*0.1, self.y - s*0.5],
               color=colors['edgecolor'], linewidth=1.5, zorder=4)
        
        # 标签
        if self.tag:
            ax.text(self.x, self.y - s*0.7,
                   self.tag, ha='center', va='top',
                   fontsize=7, fontweight='bold',
                   color=colors['label_color'], zorder=6)


class HandValve(Valve):
    """
    手动阀
    
    绘制菱形符号（手工操作）
    
    Args:
        x, y: 阀门中心坐标
        tag: 位号（如 'HV-101'）
        size: 尺寸
    """
    
    def __init__(self, x, y, tag='', size=0.25):
        super().__init__(x, y, tag, 'hand', size)
        
    def draw(self, ax):
        """绘制手动阀"""
        colors = VALVE_COLORS.get('check', {
            'facecolor': '#FFFFFF',
            'edgecolor': '#455A64',
            'label_color': '#37474F'
        })
        s = self.size
        
        # 菱形
        diamond = MplPolygon([[self.x, self.y + s*0.5],
                              [self.x + s*0.4, self.y],
                              [self.x, self.y - s*0.5],
                              [self.x - s*0.4, self.y]],
                             closed=True,
                             facecolor=colors['facecolor'],
                             edgecolor=colors['edgecolor'],
                             linewidth=1.2,
                             zorder=5)
        ax.add_patch(diamond)
        
        # 手柄线
        ax.plot([self.x, self.x], [self.y, self.y + s*0.7],
               color=colors['edgecolor'], linewidth=1.5, zorder=4)
        
        # 标签
        if self.tag:
            ax.text(self.x, self.y - s*0.7,
                   self.tag, ha='center', va='top',
                   fontsize=6, color=colors['label_color'], zorder=6)


class CheckValve(Valve):
    """
    止回阀
    
    绘制三角形符号（单向流动）
    
    Args:
        x, y: 阀门中心坐标
        tag: 位号（如 'CV-101'）
        size: 尺寸
    """
    
    def __init__(self, x, y, tag='', size=0.25):
        super().__init__(x, y, tag, 'check', size)
        
    def draw(self, ax):
        """绘制止回阀"""
        colors = VALVE_COLORS.get('check', {
            'facecolor': '#E3F2FD',
            'edgecolor': '#1565C0',
            'label_color': '#0D47A1'
        })
        s = self.size
        
        # 三角形（指向流动方向）
        tri = MplPolygon([[self.x - s*0.4, self.y - s*0.3],
                          [self.x + s*0.4, self.y],
                          [self.x - s*0.4, self.y + s*0.3]],
                         closed=True,
                         facecolor=colors['facecolor'],
                         edgecolor=colors['edgecolor'],
                         linewidth=1.2,
                         zorder=5)
        ax.add_patch(tri)
        
        # 箭头表示流向
        ax.annotate('', xy=(self.x + s*0.3, self.y),
                   xytext=(self.x - s*0.2, self.y),
                   arrowprops=dict(arrowstyle='->', 
                                 color=colors['edgecolor'],
                                 lw=1.5))
        
        # 标签
        if self.tag:
            ax.text(self.x, self.y - s*0.6,
                   self.tag, ha='center', va='top',
                   fontsize=6, color=colors['label_color'], zorder=6)
