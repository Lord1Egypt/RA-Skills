# -*- coding: utf-8 -*-
"""
阶段 1：新闻抓取任务
功能：网络抓取 → 过滤 → 保存到数据库
"""

import os
import sys
import io
from datetime import datetime

# 设置 UTF-8 输出
if not isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

try:
    from .config import DB_PATH
    from .fetcher import fetch_all_news
    from .database import mark_new_flag
except ImportError:
    from config import DB_PATH
    from fetcher import fetch_all_news
    from database import mark_new_flag


def main():
    """阶段 1 主流程"""
    start_time = datetime.now()
    print(f"{'='*60}")
    print(f"新闻抓取任务（阶段 1/3）")
    print(f"开始时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 抓取新闻
    from .config import WEBSITES
    print(f"【任务】抓取 {len(WEBSITES)} 个网站新闻...")
    fetch_start = datetime.now()
    
    new_count = fetch_all_news()
    
    # 标记新抓取的数据
    if new_count > 0:
        mark_new_flag()
    
    fetch_elapsed = (datetime.now() - fetch_start).total_seconds()
    print(f"\nOK 新增新闻：{new_count} 条")
    print(f"OK 耗时：{fetch_elapsed:.1f}秒")
    
    # 完成
    total_elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n{'='*60}")
    print(f"阶段 1 完成！")
    print(f"总耗时：{total_elapsed:.1f}秒")
    print(f"{'='*60}")
    print(f"\n统计：")
    print(f"  新增新闻：{new_count} 条")
    print(f"\nFETCH_DONE")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        import traceback
        print(f"\nERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
