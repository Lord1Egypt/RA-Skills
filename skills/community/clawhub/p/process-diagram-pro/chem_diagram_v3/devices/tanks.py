# -*- coding: utf-8 -*-
"""
储罐 - Tanks
=============

储罐/原料罐设备绘制
"""

from matplotlib.patches import FancyBboxPatch
from ..core.colors import EQUIPMENT_COLORS


class Tank:
    """
    储罐/原料罐
    
    绘制带夹套条纹的圆柱形储罐
    
    Args:
        x, y: 设备中心坐标
        tag: 位号（如 'T-101'）
        name: 名称（如 '顺酐原料罐'）
        width: 宽度（默认1.2）
        height: 高度（默认2.2）
        note: 备注（如 'T: RT~60°C'）
    """
    
    size = (1.2, 2.2)  # 默认尺寸
    
    def __init__(self, x, y, tag, name='', width=1.2, height=2.2, note=''):
        self.x = x
        self.y = y
        self.tag = tag
        self.name = name
        self.width = width
        self.height = height
        self.note = note
        
    def draw(self, ax):
        """绘制储罐"""
        colors = EQUIPMENT_COLORS['tank']
        x, y = self.x - self.width/2, self.y - self.height/2
        
        # 主体
        rect = FancyBboxPatch((x, y), self.width, self.height,
                               boxstyle="round,pad=0.02",
                               facecolor=colors['facecolor'],
                               edgecolor=colors['edgecolor'],
                               linewidth=1.5,
                               zorder=3)
        ax.add_patch(rect)
        
        # 夹套条纹
        for i in range(3):
            stripe_y = y + self.height * (0.25 + i * 0.2)
            ax.plot([x + 0.05, x + self.width - 0.05], 
                   [stripe_y, stripe_y],
                   color='#BBDEFB', linewidth=0.8, zorder=4)
        
        # 位号
        ax.text(self.x, y + self.height * 0.62,
               self.tag, ha='center', va='center',
               fontsize=9, fontweight='bold', 
               color=colors['label_color'], zorder=5)
        
        # 名称（第二行）
        if self.name:
            # 处理中英文混合名称
            ax.text(self.x, y + self.height * 0.38,
                   self.name, ha='center', va='center',
                   fontsize=7, color='#424242', zorder=5)
        
        # 备注
        if self.note:
            ax.text(self.x, y - 0.2,
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
