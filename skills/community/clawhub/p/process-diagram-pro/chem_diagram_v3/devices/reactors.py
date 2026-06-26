# -*- coding: utf-8 -*-
"""
反应器 - Reactors
=================

固定床反应器等设备绘制
"""

from matplotlib.patches import FancyBboxPatch
from ..core.colors import EQUIPMENT_COLORS, get_temp_color


class Reactor:
    """
    固定床反应器
    
    绘制带催化剂床层符号的反应器
    
    Args:
        x, y: 设备中心坐标
        tag: 位号（如 'R-01'）
        name: 名称（如 '固定床反应器'）
        temp: 操作温度（°C）
        pressure: 操作压力（MPa）
        catalyst: 催化剂信息
        width: 宽度（默认1.5）
        height: 高度（默认2.2）
    """
    
    def __init__(self, x, y, tag, name='', temp=None, pressure=None,
                 catalyst='', width=1.5, height=2.2):
        self.x = x
        self.y = y
        self.tag = tag
        self.name = name
        self.temp = temp
        self.pressure = pressure
        self.catalyst = catalyst
        self.width = width
        self.height = height
        
    def draw(self, ax):
        """绘制反应器"""
        colors = EQUIPMENT_COLORS['reactor']
        
        # 根据温度设置颜色
        facecolor = get_temp_color(self.temp) if self.temp else colors['facecolor']
        
        x, y = self.x - self.width/2, self.y - self.height/2
        cx = self.x
        
        # 主体
        rect = FancyBboxPatch((x, y), self.width, self.height,
                               boxstyle="round,pad=0.05",
                               facecolor=facecolor,
                               edgecolor=colors['edgecolor'],
                               linewidth=2,
                               zorder=3)
        ax.add_patch(rect)
        
        # 催化剂床层（斜线阴影）
        bed = FancyBboxPatch((cx - self.width*0.32, y + self.height*0.25),
                            self.width * 0.64, self.height * 0.5,
                            boxstyle="round,pad=0.02",
                            facecolor=colors['catalyst_bed'],
                            edgecolor='#E57373',
                            linewidth=1,
                            zorder=4)
        ax.add_patch(bed)
        
        # 催化剂床层文字
        ax.text(cx, y + self.height * 0.5,
               'CATALYST\nBED',
               ha='center', va='center',
               fontsize=6, color='#B71C1C',
               fontweight='bold', zorder=5)
        
        # 位号
        ax.text(cx, y + self.height * 0.88,
               self.tag, ha='center', va='center',
               fontsize=9, fontweight='bold',
               color=colors['label_color'], zorder=5)
        
        # 名称
        if self.name:
            ax.text(cx, y + self.height * 0.12,
                   self.name, ha='center', va='center',
                   fontsize=7, color='#424242', zorder=5)
        
        # 温度/压力标注
        if self.temp or self.pressure:
            params = []
            if self.temp:
                params.append(f'T={self.temp}°C')
            if self.pressure:
                params.append(f'P={self.pressure}MPa')
            param_text = '\n'.join(params)
            ax.text(x + self.width + 0.1, y + self.height * 0.75,
                   param_text, ha='left', va='center',
                   fontsize=6, color=colors['label_color'], zorder=5)
        
        # 催化剂备注
        if self.catalyst:
            ax.text(cx, y - 0.2,
                   f'Cat: {self.catalyst}', ha='center', va='top',
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
