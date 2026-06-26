# -*- coding: utf-8 -*-
"""
PFD图生成器
===========

工艺流程图生成器
"""

from ..core.canvas import ChemicalCanvas
from ..devices import Tank, Reactor, HeatExchanger, Separator
from ..pipelines import Pipe, FlowArrow


class PFDGenerator:
    """
    PFD工艺流程图生成器
    
    简化API，用于快速生成PFD图
    
    Usage:
        generator = PFDGenerator()
        generator.set_title("顺酐加氢制丁二酸酐")
        generator.add_equipment({'type': 'tank', 'x': 1, 'y': 3, 'tag': 'T-101', 'name': '顺酐原料罐'})
        generator.add_flow({'from': 'T-101', 'to': 'E-101', 'label': '顺酐'})
        generator.render().save('pfd.png')
    """
    
    def __init__(self, figsize=(16, 8), dpi=150):
        self.canvas = ChemicalCanvas(figsize=figsize, dpi=dpi)
        self.equipment = []
        self.flows = []
        
    def set_title(self, title, subtitle=''):
        """设置标题"""
        self.canvas.set_title(title, subtitle)
        return self
        
    def add_equipment(self, eq):
        """
        添加设备
        
        Args:
            eq: 设备字典 {
                'type': 'tank' | 'reactor' | 'heat_exchanger' | 'separator',
                'x': 1, 'y': 3,
                'tag': 'T-101',
                'name': '顺酐原料罐',
                'temp': 60,  # 可选
                'pressure': 4,  # 可选
                'note': '备注'  # 可选
            }
        """
        eq_type = eq.get('type', 'tank')
        
        if eq_type == 'tank':
            device = Tank(
                x=eq['x'], y=eq['y'],
                tag=eq.get('tag', ''),
                name=eq.get('name', ''),
                note=eq.get('note', '')
            )
        elif eq_type == 'reactor':
            device = Reactor(
                x=eq['x'], y=eq['y'],
                tag=eq.get('tag', ''),
                name=eq.get('name', ''),
                temp=eq.get('temp'),
                pressure=eq.get('pressure'),
                catalyst=eq.get('catalyst', '')
            )
        elif eq_type == 'heat_exchanger':
            device = HeatExchanger(
                x=eq['x'], y=eq['y'],
                tag=eq.get('tag', ''),
                name=eq.get('name', ''),
                note=eq.get('note', '')
            )
        elif eq_type == 'separator':
            device = Separator(
                x=eq['x'], y=eq['y'],
                tag=eq.get('tag', ''),
                name=eq.get('name', ''),
                note=eq.get('note', '')
            )
        else:
            raise ValueError(f"Unknown equipment type: {eq_type}")
            
        self.canvas.add_device(device)
        self.equipment.append({'tag': eq.get('tag'), 'device': device})
        return self
        
    def add_flow(self, flow):
        """
        添加物流
        
        Args:
            flow: 物流字典 {
                'from': 'T-101',  # 起点设备tag
                'to': 'E-101',  # 终点设备tag
                'label': '顺酐',  # 物料标注
                'temp': 60  # 温度
            }
        """
        self.flows.append(flow)
        
        # 查找设备
        from_dev = self._get_device(flow.get('from'))
        to_dev = self._get_device(flow.get('to'))
        
        if from_dev and to_dev:
            # 从设备右侧到另一设备左侧
            from_points = from_dev.get_connection_points()
            to_points = to_dev.get_connection_points()
            start = from_points.get('right', (from_dev.x, from_dev.y))
            end = to_points.get('left', (to_dev.x, to_dev.y))
            
            pipe = FlowArrow(
                start=start,
                end=end,
                label=flow.get('label', ''),
                temp=flow.get('temp'),
                pressure=flow.get('pressure')
            )
            pipe.draw(self.canvas.ax)
            
        return self
        
    def add_pipe(self, start, end, label='', color=None):
        """
        添加管道（直接指定坐标）
        
        Args:
            start: (x, y)
            end: (x, y)
            label: 标注
            color: 颜色
        """
        pipe = Pipe(start=start, end=end, label=label, color=color)
        pipe.draw(self.canvas.ax)
        return self
        
    def _get_device(self, tag):
        """根据tag获取设备"""
        for eq in self.equipment:
            if eq['tag'] == tag:
                return eq['device']
        return None
        
    def render(self):
        """渲染并返回canvas"""
        return self.canvas
        
    def save(self, path):
        """保存图片"""
        return self.canvas.save(path)


# ===================== 便捷函数 =====================

def draw_pfd(title, equipments, flows, output='pfd_output.png'):
    """
    快速绘制PFD图
    
    Args:
        title: 图表标题
        equipments: 设备列表
        flows: 物流列表
        output: 输出路径
    
    Returns:
        PFDGenerator实例
    """
    generator = PFDGenerator()
    generator.set_title(title)
    
    for eq in equipments:
        generator.add_equipment(eq)
        
    for flow in flows:
        generator.add_flow(flow)
        
    generator.save(output)
    return generator
