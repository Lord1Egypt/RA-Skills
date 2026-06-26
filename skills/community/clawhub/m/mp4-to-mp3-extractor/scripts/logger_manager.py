#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: MP4-To-MP3-Extractor
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: 这段代码定义了一个名为 LoggerManager 的类，专门用于自动化配置和管理日志系统。
它通过封装 Python 的 logging 模块，为项目提供了一个既能输出到控制台，又能自动按天滚动保存的日志工具。
智能目录管理：利用 pathlib 自动检查并创建日志目录（LOG_DIR），防止因文件夹不存在而报错。
1、双通道输出：
    1、控制台 (Stdout)：方便开发者在运行程序时实时查看状态。
    2、文件 (File)：持久化记录运行日志，便于后续排查问题。
2、自动滚动备份：使用了 TimedRotatingFileHandler，设置每 1天 滚动一次日志文件，并保留最近 3天 的记录，有效防止日志文件无限增大占用硬盘空间。
3、防止日志重复：通过 if not logger.handlers 判断，确保在多次调用初始化方法时，不会重复绑定处理器（Handler），避免出现一行日志被打印多次的情况。
"""

import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from config import LOG_DIR

class LoggerManager:
    @staticmethod
    def setup_logger(logger_name: str = "log", log_filename: str = "skill_execution.log"):
        """
        初始化并配置日志记录器
        :param log_dir: 日志保存目录 (Path 对象)
        :param logger_name: logger 的名称
        :param log_filename: 日志文件的名称
        """
        # 确保日志目录存在 (parents=True 确保父级目录也会被创建)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / log_filename
        
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        
        # 避免在多次调用时重复添加 handler 导致日志重复输出
        if not logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            
            # 文件输出 Handler
            file_handler = TimedRotatingFileHandler(
                log_file, when="D", interval=1, backupCount=3, encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            # 控制台输出 Handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger