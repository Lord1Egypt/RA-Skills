#!/usr/bin/env python3
# -*- coding: utf-8, -*-

"""
Skill Name: MP4-To-MP3-Extractor
Author: 王岷瑞/https://github.com/wangminrui2022
License: Apache License
Description: 这段代码是一个典型的 Python 项目路径管理模块。
它利用 pathlib 库实现了一套自动化的路径解析方案，旨在解决硬编码（Hardcoding）路径带来的跨平台兼容性差和维护困难等问题。
这段代码的核心逻辑是**“以当前文件为基准，向上溯源寻找根目录”**。
这种方式能确保无论项目被部署在哪个文件夹下，只要目录结构保持不变，代码都能准确找到对应的资源。
"""

from pathlib import Path

_BASE_PATH = Path(__file__).resolve()

class ProjectPaths:
    """
    统一路径管理
    ProjectPaths 类将项目中常用的核心目录进行了静态封装：
    | 路径变量 | 指向位置 | 用途 |
    | :--- | :--- | :--- |
    | VENV_DIR | 根目录/venv | 虚拟环境目录 |
    | DATA_DIR | 根目录/data | 数据文件存放处 |
    | LOG_DIR | 根目录/logs | 日志记录输出目录 |
    | MODEL_DIR | 根目录/models | AI模型权重等资源目录 |    
    """
    SCRIPT_PATH = _BASE_PATH
    SKILL_ROOT = _BASE_PATH.parent.parent
    VENV_DIR = _BASE_PATH.parent.parent.parent / "venv" #venv虚拟环境目录在skills/venv通用目录
    DATA_DIR = SKILL_ROOT / "data"
    LOG_DIR = SKILL_ROOT / "logs"
    MODEL_DIR = SKILL_ROOT / "models"      # 模型下载目录

    @classmethod
    def get_subpath(cls, *parts):
        """
        动态获取基于根目录的子路径
        用法: ProjectPaths.get_subpath("data", "raw", "test.txt")
        """
        path = cls.SKILL_ROOT.joinpath(*parts)
        # 自动创建不存在的目录（可选）
        # path.parent.mkdir(parents=True, exist_ok=True)
        return path

# 也可以直接导出变量，方便外部 import
SCRIPT_PATH = ProjectPaths.SCRIPT_PATH
SKILL_ROOT = ProjectPaths.SKILL_ROOT
VENV_DIR = ProjectPaths.VENV_DIR
DATA_DIR = ProjectPaths.DATA_DIR
LOG_DIR = ProjectPaths.LOG_DIR
MODEL_DIR = ProjectPaths.MODEL_DIR