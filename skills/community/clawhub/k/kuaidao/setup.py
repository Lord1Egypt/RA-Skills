#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快导(KD) - 短视频脚本批量生成与管理
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_path = Path(__file__).parent / "SKILL.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="kd",
    version="1.0.0",
    description="快导(KD) - 短视频脚本批量生成与管理",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="User",
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=[
        "openpyxl>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kd=kd:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
