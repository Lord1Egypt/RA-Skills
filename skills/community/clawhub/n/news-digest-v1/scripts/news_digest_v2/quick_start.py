# -*- coding: utf-8 -*-
"""
快速启动脚本
功能：一键完成 初始化 + 抓取 + 生成摘要
运行：python scripts/news_digest_v2/quick_start.py
"""

import os
import sys
import io

# 设置 UTF-8 输出
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from news_digest_v2.init_db import main as init_db_main
from news_digest_v2.run_all_stages import main as run_all_stages_main


def main():
    print()
    print('#' * 60)
    print('#  新闻摘要 - 快速启动')
    print('#' * 60)
    print()
    
    # 第 1 步：初始化数据库
    print('>>> 第 1 步：初始化数据库')
    try:
        init_db_main()
    except SystemExit as e:
        if e.code != 0:
            print('  数据库初始化失败，请检查错误信息')
            return 1
    print()
    
    # 第 2 步：运行摘要流程
    print('>>> 第 2 步：抓取新闻并生成摘要')
    print('    (这可能需要 3-5 分钟，请耐心等待...)')
    print()
    
    try:
        result = run_all_stages_main()
    except Exception as e:
        print(f'\n  ERROR: 摘要生成失败: {e}')
        return 1
    
    if result != 0:
        print('\n  摘要生成未成功完成，请检查错误信息')
        return 1
    
    # 完成
    print()
    print('#' * 60)
    print('#  全部完成！')
    print('#' * 60)
    print()
    print('  输出文件：')
    print('    - 桌面：新闻摘要_YYYYMMDD_HHMMSS.txt')
    print('    - 工作区：.news-digest-out.md')
    print()
    print('  提示：你可以随时单独运行：')
    print('    python scripts/news_digest_v2/run_all_stages.py')
    print()
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('\n\n  已取消')
        sys.exit(0)
