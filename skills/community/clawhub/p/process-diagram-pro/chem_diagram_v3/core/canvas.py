# -*- coding: utf-8 -*-
"""
画布核心 - ChemicalCanvas
========================

核心画布类，管理所有绘图元素

Features:
    - matplotlib + PIL 混合引擎
    - 中文字幕渲染（无乱码）
    - 元素管理（设备、管道、信号线）
    - 坐标转换
    - 导出PNG/SVG

Usage:
    canvas = ChemicalCanvas(figsize=(16, 8))
    canvas.add_device(reactor)
    canvas.add_pipe(pipe)
    canvas.add_signal(signal)
    canvas.save('output.png')
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import warnings
warnings.filterwarnings('ignore')

# 字体加载
from ..fonts.loader import get_font, get_text_bbox, draw_centered_text

# 颜色
from .colors import COLORS


class ChemicalCanvas:
    """
    化工图纸绘制画布
    
    Attributes:
        figsize: 画布尺寸（英寸）
        dpi: 分辨率
        devices: 设备列表
        pipes: 管道列表
        signals: 信号线列表
        annotations: 标注列表
    """
    
    def __init__(self, figsize=(16, 10), dpi=150):
        """
        初始化画布
        
        Args:
            figsize: 画布尺寸 (width, height) 单位英寸
            dpi: 分辨率
        """
        self.figsize = figsize
        self.dpi = dpi
        
        # 创建 matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi)
        self.fig.set_size_inches(figsize)
        
        # 设置坐标范围
        self.ax.set_xlim(0, figsize[0])
        self.ax.set_ylim(0, figsize[1])
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        # 背景色
        self.fig.patch.set_facecolor(COLORS['misc']['background'])
        
        # 元素存储
        self.devices = []
        self.pipes = []
        self.signals = []
        self.annotations = []
        
        # PIL层（延迟初始化）
        self.pil_img = None
        self.pil_draw = None
        self.font = None
        self.font_size = int(dpi * 0.18)
        self.font_size_small = int(dpi * 0.12)
        
    # ===================== 设备管理 =====================
    
    def add_device(self, device):
        """
        添加设备到画布
        
        Args:
            device: Device 对象
        """
        self.devices.append(device)
        device.draw(self.ax)
        
    def get_device(self, tag):
        """
        根据标签获取设备
        
        Args:
            tag: 设备标签，如 'R-01'
        
        Returns:
            Device 对象或 None
        """
        for dev in self.devices:
            if dev.tag == tag:
                return dev
        return None
        
    # ===================== 管道管理 =====================
    
    def add_pipe(self, pipe):
        """
        添加管道
        
        Args:
            pipe: Pipe 对象
        """
        self.pipes.append(pipe)
        pipe.draw(self.ax)
        
    # ===================== 信号线管理 =====================
    
    def add_signal(self, signal):
        """
        添加信号线
        
        Args:
            signal: SignalLine 对象
        """
        self.signals.append(signal)
        signal.draw(self.ax)
        
    # ===================== 标注管理 =====================
    
    def add_text(self, x, y, text, fontsize=None, color='#000000', 
                 align='center', bold=False):
        """
        添加文字标注
        
        Args:
            x, y: 位置
            text: 文字内容
            fontsize: 字号
            color: 颜色
            align: 对齐方式 ('center', 'left', 'right')
            bold: 是否加粗
        """
        self.annotations.append({
            'type': 'text',
            'x': x, 'y': y,
            'text': text,
            'fontsize': fontsize or self.font_size,
            'color': color,
            'align': align,
            'bold': bold,
        })
        
    def add_box(self, x, y, width, height, **kwargs):
        """
        添加矩形框
        
        Args:
            x, y: 左下角位置
            width, height: 宽高
            **kwargs: 其他参数 (facecolor, edgecolor, alpha等)
        """
        rect = FancyBboxPatch((x, y), width, height,
                              boxstyle="round,pad=0.02",
                              **kwargs)
        self.ax.add_patch(rect)
        
    def add_legend(self, items, location='lower right', **kwargs):
        """
        添加图例
        
        Args:
            items: 图例项列表，每项为 (颜色, 描述)
            location: 位置
        """
        patches = []
        for color, label in items:
            if isinstance(color, dict):
                patch = mpatches.Patch(**color, label=label)
            else:
                patch = mpatches.Patch(facecolor=color, edgecolor='#BDBDBD', label=label)
            patches.append(patch)
        
        self.ax.legend(handles=patches, loc=location.replace('_', ' '), 
                      fontsize=self.font_size_small, **kwargs)
        
    # ===================== 标题 =====================
    
    def set_title(self, title, subtitle='', **kwargs):
        """
        设置图纸标题
        
        Args:
            title: 主标题
            subtitle: 副标题（可选）
        """
        default_kwargs = {
            'fontsize': int(14 * self.dpi / 100),
            'fontweight': 'bold',
            'color': '#1A237E',
            'ha': 'center',
            'va': 'center',
        }
        default_kwargs.update(kwargs)
        
        # 主标题
        title_y = self.figsize[1] - 0.5
        self.ax.text(self.figsize[0] / 2, title_y, title, **default_kwargs)
        
        # 副标题
        if subtitle:
            subtitle_y = title_y - 0.45
            self.ax.text(self.figsize[0] / 2, subtitle_y, subtitle,
                        fontsize=int(9 * self.dpi / 100),
                        color='#5C6BC0',
                        style='italic',
                        ha='center', va='center')
        
    # ===================== 坐标转换 =====================
    
    def to_pixel(self, x_data, y_data):
        """
        数据坐标转像素坐标
        
        Args:
            x_data, y_data: 数据坐标（matplotlib坐标系）
        
        Returns:
            tuple: (x_px, y_px) 像素坐标
        """
        x_px = int(x_data * self.dpi)
        y_px = int((self.figsize[1] - y_data) * self.dpi)
        return x_px, y_px
    
    # ===================== 渲染与导出 =====================
    
    def _render_to_pil(self):
        """将 matplotlib 图形渲染到 PIL Image（延迟渲染）"""
        if self.pil_img is not None:
            return
            
        # matplotlib buffer 转 numpy
        self.fig.canvas.draw()
        buf = np.asarray(self.fig.canvas.buffer_rgba())
        
        # numpy 转 PIL Image
        self.pil_img = Image.fromarray(buf, 'RGBA')
        self.pil_draw = ImageDraw.Draw(self.pil_img)
        
        # 加载字体
        self.font = get_font(size=self.font_size)
        self.font_small = get_font(size=self.font_size_small)
        
        # 关闭 matplotlib figure（释放内存）
        plt.close(self.fig)
        
    def _draw_annotations(self):
        """在 PIL 层绘制标注"""
        if not self.annotations:
            return
            
        for ann in self.annotations:
            px, py = self.to_pixel(ann['x'], ann['y'])
            font = get_font(size=ann.get('fontsize', self.font_size))
            fill = self._hex_to_rgba(ann.get('color', '#000000'))
            
            if ann['align'] == 'center':
                draw_centered_text(self.pil_draw, (px, py), ann['text'], font, fill)
            else:
                self.pil_draw.text((px, py), ann['text'], fill=fill, font=font)
                
    def _hex_to_rgba(self, hex_color):
        """HEX颜色转RGBA"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b, 255)
        
    def save(self, output_path, format=None, dpi=None, **kwargs):
        """
        保存图片
        
        Args:
            output_path: 输出路径
            format: 格式 (png, svg, pdf)
            dpi: 分辨率
            **kwargs: 其他参数
        """
        # 延迟渲染
        self._render_to_pil()
        
        # 绘制标注
        self._draw_annotations()
        
        # 保存
        if format is None:
            format = os.path.splitext(output_path)[1].lstrip('.').lower() or 'png'
        
        save_kwargs = {
            'quality': 95 if format == 'jpeg' else None,
        }
        save_kwargs.update(kwargs)
        
        self.pil_img.save(output_path, format=format.upper(), **save_kwargs)
        print(f"[ChemicalCanvas] ✅ 图片已保存: {output_path}")
        
    def show(self):
        """
        显示图片（仅在交互环境有效）
        """
        self._render_to_pil()
        self.pil_img.show()
        
    # ===================== 上下文管理器 =====================
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        pass
        
    # ===================== 便捷方法 =====================
    
    def draw_arrow(self, x1, y1, x2, y2, color=None, lw=2, style='->'):
        """
        绘制箭头
        
        Args:
            x1, y1: 起点
            x2, y2: 终点
            color: 颜色
            lw: 线宽
            style: 箭头样式
        """
        if color is None:
            color = COLORS['misc']['arrow']
            
        self.ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle=style, color=color, lw=lw))
                        
    def draw_line(self, x1, y1, x2, y2, color=None, lw=2, linestyle='-'):
        """
        绘制直线
        
        Args:
            x1, y1: 起点
            x2, y2: 终点
            color: 颜色
            lw: 线宽
            linestyle: 线型
        """
        if color is None:
            color = COLORS['pipeline']['process']['color']
            
        self.ax.plot([x1, x2], [y1, y2], 
                    color=color, linewidth=lw, linestyle=linestyle)
                    
    def draw_dashed_line(self, x1, y1, x2, y2, color=None, lw=1):
        """
        绘制虚线
        
        Args:
            x1, y1: 起点
            x2, y2: 终点
            color: 颜色
            lw: 线宽
        """
        if color is None:
            color = COLORS['pipeline']['signal']['color']
            
        self.draw_line(x1, y1, x2, y2, color=color, lw=lw, linestyle='--')
