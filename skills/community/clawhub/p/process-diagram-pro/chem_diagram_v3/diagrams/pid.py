# -*- coding: utf-8 -*-
"""
P&ID图生成器
============

管道仪表流程图生成器

增强版本：
- 支持更多阀门类型（手动阀、止回阀）
- 改进信号线样式（灰色虚线）
- 支持管道弯头连接
"""

from ..core.canvas import ChemicalCanvas
from ..devices import (
    Tank, Reactor, HeatExchanger, Separator,
    ControlValve, ESDValve, SafetyValve, HandValve, CheckValve,
    Instrument, TIC, PIC, FIC, TE, PE, FE, PSH, PSL, AE
)
from ..pipelines import Pipe, SignalLine, PipeElbow


class PIDGenerator:
    """
    P&ID管道仪表流程图生成器
    
    支持：
    - 设备绘制
    - 阀门组
    - 控制回路
    - ESD联锁
    - 信号线连接
    
    Usage:
        generator = PIDGenerator()
        generator.set_title("顺酐加氢制丁二酸酐 P&ID")
        generator.add_equipment(...)
        generator.add_valve({'type': 'esd', 'x': 3, 'y': 3, 'tag': 'XV-101'})
        generator.add_instrument({'type': 'TIC', 'x': 5, 'y': 5, 'tag': 'TIC-101'})
        generator.add_signal({'from': 'TE-101', 'to': 'TIC-101'})
        generator.render().save('pid.png')
    """
    
    def __init__(self, figsize=(18, 10), dpi=150):
        self.canvas = ChemicalCanvas(figsize=figsize, dpi=dpi)
        self.devices_map = {}  # tag -> device
        self.valves_map = {}
        self.instruments_map = {}
        
    def set_title(self, title, subtitle=''):
        """设置标题"""
        self.canvas.set_title(title, subtitle)
        return self
        
    def add_equipment(self, eq):
        """添加设备"""
        eq_type = eq.get('type', 'tank')
        tag = eq.get('tag', '')
        
        if eq_type == 'tank':
            device = Tank(
                x=eq['x'], y=eq['y'],
                tag=tag, name=eq.get('name', ''),
                note=eq.get('note', '')
            )
        elif eq_type == 'reactor':
            device = Reactor(
                x=eq['x'], y=eq['y'],
                tag=tag, name=eq.get('name', ''),
                temp=eq.get('temp'),
                pressure=eq.get('pressure'),
                catalyst=eq.get('catalyst', '')
            )
        elif eq_type == 'heat_exchanger':
            device = HeatExchanger(
                x=eq['x'], y=eq['y'],
                tag=tag, name=eq.get('name', ''),
                note=eq.get('note', '')
            )
        elif eq_type == 'separator':
            device = Separator(
                x=eq['x'], y=eq['y'],
                tag=tag, name=eq.get('name', ''),
                note=eq.get('note', '')
            )
        else:
            raise ValueError(f"Unknown equipment type: {eq_type}")
            
        self.canvas.add_device(device)
        self.devices_map[tag] = device
        return self
        
    def add_valve(self, valve):
        """
        添加阀门
        
        Args:
            valve: {
                'type': 'control' | 'esd' | 'safety' | 'hand' | 'check',
                'x': 3, 'y': 3,
                'tag': 'XV-101'
            }
        """
        v_type = valve.get('type', 'control')
        tag = valve.get('tag', '')
        
        if v_type == 'control':
            v = ControlValve(
                x=valve['x'], y=valve['y'],
                tag=tag
            )
        elif v_type == 'esd':
            v = ESDValve(
                x=valve['x'], y=valve['y'],
                tag=tag
            )
        elif v_type == 'safety':
            v = SafetyValve(
                x=valve['x'], y=valve['y'],
                tag=tag
            )
        elif v_type == 'hand':
            v = HandValve(
                x=valve['x'], y=valve['y'],
                tag=tag
            )
        elif v_type == 'check':
            v = CheckValve(
                x=valve['x'], y=valve['y'],
                tag=tag
            )
        else:
            v = ControlValve(
                x=valve['x'], y=valve['y'],
                tag=tag
            )
            
        v.draw(self.canvas.ax)
        if tag:
            self.valves_map[tag] = v
        return self
        
    def add_instrument(self, inst):
        """
        添加仪表
        
        Args:
            inst: {
                'type': 'TIC' | 'PIC' | 'FIC' | 'TE' | 'PE' | 'FE',
                'x': 5, 'y': 5,
                'tag': 'TIC-101'
            }
        """
        i_type = inst.get('type', 'default')
        tag = inst.get('tag', '')
        
        # 根据类型创建仪表
        if i_type == 'TIC':
            i = TIC(x=inst['x'], y=inst['y'], tag=tag)
        elif i_type == 'PIC':
            i = PIC(x=inst['x'], y=inst['y'], tag=tag)
        elif i_type == 'FIC':
            i = FIC(x=inst['x'], y=inst['y'], tag=tag)
        elif i_type == 'TE':
            i = TE(x=inst['x'], y=inst['y'], tag=tag)
        elif i_type == 'PE':
            i = PE(x=inst['x'], y=inst['y'], tag=tag)
        elif i_type == 'FE':
            i = FE(x=inst['x'], y=inst['y'], tag=tag)
        elif i_type == 'PSH':
            i = PSH(x=inst['x'], y=inst['y'], tag=tag)
        elif i_type == 'PSL':
            i = PSL(x=inst['x'], y=inst['y'], tag=tag)
        elif i_type == 'AE':
            i = AE(x=inst['x'], y=inst['y'], tag=tag)
        else:
            i = Instrument(x=inst['x'], y=inst['y'], tag=tag, inst_type=i_type)
            
        i.draw(self.canvas.ax)
        if tag:
            self.instruments_map[tag] = i
        return self
        
    def add_pipe(self, start, end, label='', color=None):
        """添加管道"""
        pipe = Pipe(start=start, end=end, label=label, color=color)
        pipe.draw(self.canvas.ax)
        return self
        
    def add_signal(self, signal):
        """
        添加信号线
        
        Args:
            signal: {
                'from': 'TE-101',  # 或设备tag
                'to': 'TIC-101',
                'type': 'TE→TIC'
            }
        """
        # 查找起点
        start_point = None
        from_tag = signal.get('from', '')
        
        if from_tag in self.instruments_map:
            inst = self.instruments_map[from_tag]
            pts = inst.get_connection_points()
            start_point = pts.get('bottom', pts.get('left', pts.get('right', pts.get('top', (inst.x, inst.y)))))
        elif from_tag in self.devices_map:
            dev = self.devices_map[from_tag]
            pts = dev.get_connection_points()
            start_point = pts.get('top', pts.get('left', pts.get('right', pts.get('bottom', (dev.x, dev.y)))))
            
        # 查找终点
        end_point = None
        to_tag = signal.get('to', '')
        
        if to_tag in self.instruments_map:
            inst = self.instruments_map[to_tag]
            pts = inst.get_connection_points()
            end_point = pts.get('top', pts.get('left', pts.get('right', pts.get('bottom', (inst.x, inst.y)))))
        elif to_tag in self.devices_map:
            dev = self.devices_map[to_tag]
            pts = dev.get_connection_points()
            end_point = pts.get('bottom', pts.get('left', pts.get('right', pts.get('top', (dev.x, dev.y)))))
            
        if start_point and end_point:
            sl = SignalLine(start=start_point, end=end_point)
            sl.draw(self.canvas.ax)
            
        return self
        
    def add_esd_box(self, x, y, conditions):
        """
        添加ESD标注框
        
        Args:
            x, y: 位置
            conditions: ['T>170°C', 'P>5.5MPa']
        """
        text_lines = ['ESD触发条件:']
        text_lines.extend(conditions)
        text = '\n'.join(text_lines)
        
        self.canvas.add_box(x-0.5, y-0.5, 2.5, 1.5,
                           facecolor='#FFEBEE',
                           edgecolor='#C62828',
                           linewidth=1.5,
                           alpha=0.9)
        self.canvas.add_text(x+0.5, y+0.3, text,
                           fontsize=7,
                           color='#C62828')
        return self
        
    def add_legend(self, items, location='lower right'):
        """添加图例"""
        self.canvas.add_legend(items, location=location)
        return self
        
    def render(self):
        """渲染并返回canvas"""
        return self.canvas
        
    def save(self, path):
        """保存图片"""
        return self.canvas.save(path)


# ===================== 便捷函数 =====================

def draw_pid(title, equipments, valves, instruments, signals, 
            output='pid_output.png'):
    """
    快速绘制P&ID图
    
    Args:
        title: 图表标题
        equipments: 设备列表
        valves: 阀门列表
        instruments: 仪表列表
        signals: 信号线列表
        output: 输出路径
    
    Returns:
        PIDGenerator实例
    """
    generator = PIDGenerator()
    generator.set_title(title)
    
    for eq in equipments:
        generator.add_equipment(eq)
        
    for valve in valves:
        generator.add_valve(valve)
        
    for inst in instruments:
        generator.add_instrument(inst)
        
    for signal in signals:
        generator.add_signal(signal)
        
    generator.save(output)
    return generator
