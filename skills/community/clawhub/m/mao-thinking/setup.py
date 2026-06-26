#!/usr/bin/env python3
"""
毛泽东思想实践工具包安装配置
Mao Zedong Thought Practice Toolkit Setup
"""

from setuptools import setup, find_packages
import os

# 读取README
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="mao-thinking",
    version="1.0.0",
    description="毛泽东思想实践工具包 - 基于毛泽东选集核心思想的方法论工具集",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mao Thought AI Team",
    author_email="contact@maothinking.ai",
    url="https://github.com/your-repo/mao-thinking",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mao-think=mao_thinking.main:main",
            "mao-analyze=mao_thinking.analyzer:main",
            "mao-situate=mao_thinking.situator:main",
            "mao-decide=mao_thinking.decider:main",
            "mao-summary=mao_thinking.summary:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Office/Business",
    ],
    keywords="mao zedong thought philosophy decision making analysis",
    project_urls={
        "Bug Reports": "https://github.com/your-repo/mao-thinking/issues",
        "Source": "https://github.com/your-repo/mao-thinking",
    },
)