# -*- coding: utf-8 -*-
"""
管道模块 - Pipelines
==================

管道，流向箭头、信号线绘制

增强版本：
- 改进信号线样式（灰色虚线，符合行业标准）
- 支持多种管道类型
- 更灵活的箭头样式
"""

import numpy as np
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
from ..core.colors import PIPELINE_COLORS


class Pipe:
    """
    管道
    
    绘制带箭头和标注的物料管道
    
    Args:
        start: 起点坐标 (x, y)
        end: 终点坐标 (x, y)
        label: 物料标注
        color: 颜色
        linewidth: 线宽
        arrow: 是否带箭头
        pipe_type: 管道类型 ('process', 'hydrogen', 'steam', 'cooling', 'gas')
    """
    
    def __init__(self, start, end, label='', color=None, 
                 linewidth=2.0, arrow=True, pipe_type='process'):
        self.start = start
        self.end = end
        self.label = label
        self.pipe_type = pipe_type
        self.color = color or PIPELINE_COLORS.get(pipe_type, PIPELINE_COLORS['process'])['color']
        self.linewidth = linewidth or PIPELINE_COLORS.get(pipe_type, PIPELINE_COLORS['process']).get('linewidth', 2.0)
        self.arrow = arrow
        
    def draw(self, ax):
        """绘制管道"""
        x1, y1 = self.start
        x2, y2 = self.end
        
        if self.arrow:
            # 带箭头的管道（使用更专业的箭头样式）
            ax.annotate('',
                      xy=(x2, y2), xytext=(x1, y1),
                      arrowprops=dict(
                          arrowstyle='->',
                          color=self.color,
                          lw=self.linewidth,
                          mutation_scale=15,  # 箭头大小
                          connectionstyle='arc3,rad=0'
                      ),
                      zorder=2)
        else:
            # 直线管道
            ax.plot([x1, x2], [y1, y2],
                  color=self.color,
                  linewidth=self.linewidth,
                  solid_capstyle='round',
                  zorder=2)
                  
        # 物料标注
        if self.label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # 计算标注偏移（避免遮挡管道）
            dx, dy = x2 - x1, y2 - y1
            length = np.sqrt(dx**2 + dy**2)
            if length > 0:
                # 垂直于管道的方向偏移
                offset_x = -dy / length * 0.2
                offset_y = dx / length * 0.2
            else:
                offset_x, offset_y = 0, 0.2
            
            # 标注框
            ax.text(mid_x + offset_x, mid_y + offset_y,
                   self.label,
                   ha='center', va='bottom',
                   fontsize=7, color=self.color,
                   fontweight='bold',
                   bbox=dict(
                       boxstyle='round,pad=0.15',
                       facecolor='white',
                       edgecolor=self.color,
                       linewidth=0.8,
                       alpha=0.95
                   ),
                   zorder=8)


class FlowArrow:
    """
    物流流向箭头
    
    带物料信息和参数的流向箭头
    
    Args:
        start: 起点
        end: 终点
        label: 物料名称
        temp: 温度
        pressure: 压力
        flow_rate: 流量
    """
    
    def __init__(self, start, end, label='', temp=None, 
                 pressure=None, flow_rate=None):
        self.start = start
        self.end = end
        self.label = label
        self.temp = temp
        self.pressure = pressure
        self.flow_rate = flow_rate
        
    def draw(self, ax):
        """绘制流向箭头"""
        x1, y1 = self.start
        x2, y2 = self.end
        
        # 计算方向并稍微缩短以便箭头清晰
        dx, dy = x2 - x1, y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        if length > 0:
            # 缩短5%避免箭头和设备重叠
            x2_s, y2_s = x1 + dx * 0.95, y1 + dy * 0.95
        else:
            x2_s, y2_s = x2, y2
        
        # 箭头（使用标准化工蓝色）
        ax.annotate('',
                  xy=(x2_s, y2_s), xytext=(x1, y1),
                  arrowprops=dict(
                      arrowstyle='->',
                      color='#1565C0',
                      lw=2,
                      mutation_scale=18,
                      connectionstyle='arc3,rad=0'
                  ),
                  zorder=2)
        
        # 标注信息
        if self.label or self.temp or self.pressure:
            mid_x = (x1 + x2_s) / 2
            mid_y = (y1 + y2_s) / 2
            
            # 构建标注文字
            lines = []
            if self.label:
                lines.append(self.label)
            if self.temp:
                lines.append(f'{self.temp}°C')
            if self.pressure:
                lines.append(f'{self.pressure}MPa')
            if self.flow_rate:
                lines.append(self.flow_rate)
            
            text = '\n'.join(lines)
            
            ax.text(mid_x, mid_y + 0.18,
                   text,
                   ha='center', va='bottom',
                   fontsize=7, color='#1565C0',
                   fontweight='bold',
                   bbox=dict(
                       boxstyle='round,pad=0.15',
                       facecolor='white',
                       edgecolor='#1565C0',
                       linewidth=1,
                       alpha=0.95
                   ),
                   zorder=8)


class SignalLine:
    """
    信号线（虚线）
    
    仪表到控制器的信号连接
    
    增强版本：使用灰色虚线（行业标准），而非紫色
    """
    
    # 行业标准信号线颜色
    DEFAULT_COLOR = '#757575'  # 灰色
    HIGHLIGHT_COLOR = '#424242'  # 深灰
    
    def __init__(self, start, end, line_type='analog', color=None):
        self.start = start
        self.end = end
        self.line_type = line_type
        self.color = color or self.DEFAULT_COLOR
        
    def draw(self, ax):
        """绘制信号线 - 灰色虚线"""
        x1, y1 = self.start
        x2, y2 = self.end
        
        # 灰色虚线（行业标准）
        ax.plot([x1, x2], [y1, y2],
              color=self.color,
              linewidth=1.2,
              linestyle='--',  # 虚线
              dashes=[5, 3],  # 5点线，3点间隔
              zorder=2)
        
        # 信号方向标记（小三角形）
        dx, dy = x2 - x1, y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        if length > 0:
            # 在中点添加方向标记
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # 计算垂直方向
            perp_x = -dy / length * 0.08
            perp_y = dx / length * 0.08
            
            ax.scatter([mid_x + perp_x], [mid_y + perp_y], 
                      marker='<', s=20, 
                      color=self.color, zorder=3)


class PipeElbow:
    """
    管道弯头
    
    带拐角的管道连接线
    
    Args:
        start: 起点
        middle: 拐点
        end: 终点
        label: 标注
    """
    
    def __init__(self, start, middle, end, label='', color=None, pipe_type='process'):
        self.start = start
        self.middle = middle
        self.end = end
        self.label = label
        self.color = color or PIPELINE_COLORS.get(pipe_type, PIPELINE_COLORS['process'])['color']
        self.pipe_type = pipe_type
        
    def draw(self, ax):
        """绘制弯管"""
        x1, y1 = self.start
        x2, y2 = self.middle
        x3, y3 = self.end
        
        color = self.color
        linewidth = PIPELINE_COLORS.get(self.pipe_type, PIPELINE_COLORS['process']).get('linewidth', 2.0)
        
        # 第一段（水平或垂直）
        ax.plot([x1, x2], [y1, y2],
              color=color, linewidth=linewidth, zorder=2)
        
        # 第二段
        ax.plot([x2, x3], [y2, y3],
              color=color, linewidth=linewidth, zorder=2)
        
        # 箭头（在终点）
        ax.annotate('',
                  xy=(x3, y3), xytext=(x3 - 0.1 * np.sign(x3 - x2), y3),
                  arrowprops=dict(
                      arrowstyle='->',
                      color=color,
                      lw=linewidth,
                      mutation_scale=12
                  ),
                  zorder=3)
        
        # 标注（在拐点）
        if self.label:
            ax.text(x2, y2 + 0.15,
                   self.label,
                   ha='center', va='bottom',
                   fontsize=6, color=color,
                   fontweight='bold',
                   bbox=dict(
                       boxstyle='round,pad=0.1',
                       facecolor='white',
                       edgecolor=color,
                       linewidth=0.5,
                       alpha=0.9
                   ),
                   zorder=8)
