# -*- coding: utf-8 -*-
"""
换热器/分离器 - Heat Exchangers & Separators
===========================================
"""

from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np
from ..core.colors import EQUIPMENT_COLORS


class HeatExchanger:
    """
    换热器/预热器/冷凝器
    
    绘制带波浪线符号的换热设备
    
    Args:
        x, y: 设备中心坐标
        tag: 位号（如 'E-101'）
        name: 名称（如 '预热器'）
        heat_type: 类型 ('heater', 'preheater', 'condenser')
        note: 备注
        width: 宽度（默认1.0）
        height: 高度（默认1.6）
    """
    
    def __init__(self, x, y, tag, name='', heat_type='preheater', 
                 note='', width=1.0, height=1.6):
        self.x = x
        self.y = y
        self.tag = tag
        self.name = name
        self.heat_type = heat_type
        self.note = note
        self.width = width
        self.height = height
        
    def draw(self, ax):
        """绘制换热器"""
        colors = EQUIPMENT_COLORS['heat_exchanger']
        x, y = self.x - self.width/2, self.y - self.height/2
        cx, cy = self.x, self.y
        
        # 主体
        rect = FancyBboxPatch((x, y), self.width, self.height,
                               boxstyle="round,pad=0.05",
                               facecolor=colors['facecolor'],
                               edgecolor=colors['edgecolor'],
                               linewidth=1.5,
                               zorder=3)
        ax.add_patch(rect)
        
        # 波浪线符号
        wave_x = np.linspace(x + self.width*0.15, x + self.width*0.85, 50)
        wave_y1 = cy + self.height * 0.08 * np.sin(np.linspace(0, 4*np.pi, 50))
        wave_y2 = cy - self.height * 0.08 * np.sin(np.linspace(0, 4*np.pi, 50))
        
        ax.plot(wave_x, wave_y1, color=colors['edgecolor'], linewidth=1.5, zorder=5)
        ax.plot(wave_x, wave_y2, color=colors['edgecolor'], linewidth=1.5, zorder=5)
        
        # 位号
        ax.text(cx, y + self.height * 0.82,
               self.tag, ha='center', va='center',
               fontsize=9, fontweight='bold',
               color=colors['label_color'], zorder=5)
        
        # 名称
        if self.name:
            ax.text(cx, y + self.height * 0.15,
                   self.name, ha='center', va='center',
                   fontsize=7, color='#424242', zorder=5)
        
        # 备注
        if self.note:
            ax.text(cx, y - 0.2,
                   self.note, ha='center', va='top',
                   fontsize=6, color='#757575',
                   style='italic', zorder=5)
                   
    def get_connection_points(self):
        """获取连接点"""
        return {
            'left': (self.x - self.width/2, self.y),
            'right': (self.x + self.width/2, self.y),
            'top': (self.x, self.y + self.height/2),
            'bottom': (self.x, self.y - self.height/2),
        }


class Separator:
    """
    气液分离器/罐
    
    绘制带视镜的分离设备
    
    Args:
        x, y: 设备中心坐标
        tag: 位号（如 'V-01'）
        name: 名称（如 '气液分离器'）
        note: 备注
        width: 宽度（默认1.0）
        height: 高度（默认1.6）
    """
    
    def __init__(self, x, y, tag, name='', note='', width=1.0, height=1.6):
        self.x = x
        self.y = y
        self.tag = tag
        self.name = name
        self.note = note
        self.width = width
        self.height = height
        
    def draw(self, ax):
        """绘制分离器"""
        colors = EQUIPMENT_COLORS['separator']
        x, y = self.x - self.width/2, self.y - self.height/2
        cx, cy = self.x, self.y
        
        # 主体
        rect = FancyBboxPatch((x, y), self.width, self.height,
                               boxstyle="round,pad=0.05",
                               facecolor=colors['facecolor'],
                               edgecolor=colors['edgecolor'],
                               linewidth=1.5,
                               zorder=3)
        ax.add_patch(rect)
        
        # 视镜（中间斜线）
        ax.plot([x + 0.1, x + self.width - 0.1],
               [cy + self.height * 0.15, cy - self.height * 0.15],
               color='#4CAF50', linewidth=1.2,
               linestyle='--', zorder=4)
        
        # 位号
        ax.text(cx, y + self.height * 0.80,
               self.tag, ha='center', va='center',
               fontsize=9, fontweight='bold',
               color=colors['label_color'], zorder=5)
        
        # 名称
        if self.name:
            ax.text(cx, y + self.height * 0.15,
                   self.name, ha='center', va='center',
                   fontsize=7, color='#424242', zorder=5)
        
        # 备注
        if self.note:
            ax.text(cx, y - 0.2,
                   self.note, ha='center', va='top',
                   fontsize=6, color='#757575',
                   style='italic', zorder=5)
                   
    def get_connection_points(self):
        """获取连接点"""
        return {
            'left': (self.x - self.width/2, self.y),
            'right': (self.x + self.width/2, self.y),
            'top': (self.x, self.y + self.height/2),
            'bottom': (self.x, self.y - self.height/2),
        }
