#!/usr/bin/env python3
"""
MikroTik RouterOS API Client
基于官方文档：https://help.mikrotik.com/docs/display/ROS/API

用法:
    from mikrotik_api import MikroTikAPI
    
    api = MikroTikAPI('192.168.1.1', username='admin', password='')
    api.connect()
    
    # 获取系统信息
    info = api.get_system_resource()
    print(info)
    
    # 执行自定义命令
    interfaces = api.run_command('/interface/print')
    print(interfaces)
    
    api.disconnect()
"""

from .client import MikroTikAPI
from .commands import SystemCommands, FirewallCommands, NetworkCommands

__version__ = '1.0.0'
__author__ = '虾哥'

__all__ = ['MikroTikAPI', 'SystemCommands', 'FirewallCommands', 'NetworkCommands']
