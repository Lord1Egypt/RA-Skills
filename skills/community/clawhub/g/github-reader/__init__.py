"""
GitHub Reader Skill v3.2 — 纯 GitHub API 安全版

用法:
  /github-read owner/repo
  https://github.com/owner/repo
  分析 owner/repo

数据源: 仅 GitHub REST API (api.github.com)
第三方服务: 无
"""

# Skill 由 github_reader_v3_secure.py 中的 run() 函数驱动
# 此文件用于包发现和导入

from .github_reader_v3_secure import run, SecureGitHubReaderV3

__version__ = "3.2.0"
