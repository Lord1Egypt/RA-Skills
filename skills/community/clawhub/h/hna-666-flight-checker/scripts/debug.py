#!/usr/bin/env python3
"""
调试模块 - 统一控制日志输出
"""

import sys
import time

# 全局调试开关
DEBUG = True  # 设为 False 可关闭所有调试输出


def log(msg: str, level: str = "INFO"):
    """统一日志输出"""
    if not DEBUG:
        return
    
    # 获取调用者信息
    frame = sys._getframe(1)
    filename = frame.f_code.co_filename.split('/')[-1]
    lineno = frame.f_lineno
    
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] [{filename}:{lineno}] [{level}] {msg}")


def info(msg: str):
    """信息日志"""
    log(msg, "INFO")


def debug(msg: str):
    """调试日志"""
    log(msg, "DEBUG")


def error(msg: str):
    """错误日志"""
    log(msg, "ERROR")


def set_debug(enabled: bool):
    """设置调试开关"""
    global DEBUG
    DEBUG = enabled
    info(f"调试模式已{'开启' if enabled else '关闭'}")


# 方便在脚本中直接调用
if __name__ == "__main__":
    # 测试
    set_debug(True)
    info("这是一条信息")
    debug("这是一条调试")
    error("这是一条错误")
