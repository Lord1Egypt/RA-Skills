#!/usr/bin/env python3
"""
MikroTik RouterOS API Client
Based on official documentation: https://help.mikrotik.com/docs/display/ROS/API

Usage:
    from mikrotik_api import RouterOSApi
    
    api = RouterOSApi('192.168.88.1', username='admin', password='')
    api.connect()
    
    # Get system info
    info = api.run_command('/system/resource/print')
    print(info)
    
    # Execute custom command
    interfaces = api.run_command('/interface/print')
    print(interfaces)
    
    api.disconnect()
"""

from .client import RouterOSApi
from .commands import SystemCommands, FirewallCommands, NetworkCommands

__version__ = '2026.03.30'
__author__ = 'drodecker'
__original_author__ = 'Xiage (2944721178)'

__all__ = ['RouterOSApi', 'SystemCommands', 'FirewallCommands', 'NetworkCommands']
