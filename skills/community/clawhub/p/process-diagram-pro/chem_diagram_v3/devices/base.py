# -*- coding: utf-8 -*-
"""
设备基类 - Device Base Class
===========================

所有设备对象的基类

Classes:
    Device: 抽象基类
"""

from abc import ABC, abstractmethod


class Device(ABC):
    """
    设备基类
    
    所有设备（储罐、反应器、换热器等）都继承此类
    
    Attributes:
        x, y: 设备中心坐标
        tag: 设备位号（如 'R-01'）
        name: 设备名称（如 '固定床反应器'）
        size: 设备尺寸 (width, height)
    """
    
    def __init__(self, x, y, tag, name=''):
        """
        初始化设备
        
        Args:
            x, y: 设备中心坐标
            tag: 设备位号
            name: 设备名称
        """
        self.x = x
        self.y = y
        self.tag = tag
        self.name = name
        
    @abstractmethod
    def draw(self, ax):
        """
        在 matplotlib Axes 上绘制设备
        
        Args:
            ax: matplotlib Axes 对象
        """
        pass
        
    def get_connection_points(self):
        """
        获取设备连接点
        
        Returns:
            dict: {
                'left': (x, y),
                'right': (x, y),
                'top': (x, y),
                'bottom': (x, y)
            }
        """
        return {
            'left': (self.x - self.size[0]/2, self.y),
            'right': (self.x + self.size[0]/2, self.y),
            'top': (self.x, self.y + self.size[1]/2),
            'bottom': (self.x, self.y - self.size[1]/2),
        }
        
    def get_input_point(self, direction='left'):
        """
        获取输入连接点
        
        Args:
            direction: 方向 ('left', 'top', 'bottom')
        
        Returns:
            tuple: (x, y)
        """
        points = self.get_connection_points()
        return points.get(direction, points['left'])
        
    def get_output_point(self, direction='right'):
        """
        获取输出连接点
        
        Args:
            direction: 方向 ('right', 'top', 'bottom')
        
        Returns:
            tuple: (x, y)
        """
        points = self.get_connection_points()
        return points.get(direction, points['right'])
