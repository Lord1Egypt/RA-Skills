# -*- coding: utf-8 -*-
"""
阶段 2：新闻处理任务
功能：去重检测 → 关键词标记
（摘要输出移至阶段 3，LLM 总结后执行）
"""

import os
import sys
import io
from datetime import datetime, timedelta

# 设置 UTF-8 输出
if not isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

try:
    from .config import DB_PATH, SIMILARITY_THRESHOLD
    from .database import mark_duplicates, update_keywords_for_new
except ImportError:
    from config import DB_PATH, SIMILARITY_THRESHOLD
    from database import mark_duplicates, update_keywords_for_new


def main():
    """阶段 2 主流程"""
    start_time = datetime.now()
    print(f"{'='*60}")
    print(f"新闻处理任务（阶段 2/3）")
    print(f"开始时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 步骤 1：去重检测
    print("【任务 1】数据库去重（相似度检测）...")
    dup_start = datetime.now()
    
    dup_count = mark_duplicates(threshold=SIMILARITY_THRESHOLD)
    
    dup_elapsed = (datetime.now() - dup_start).total_seconds()
    print(f"OK 标记重复：{dup_count} 条")
    print(f"OK 耗时：{dup_elapsed:.1f}秒\n")
    
    # 步骤 2：关键词标记
    print("【任务 2】关键词标记（基于系统关键词表）...")
    kw_start = datetime.now()
    
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - 
                 timedelta(days=1)).strftime('%Y-%m-%d')
    
    kw_count = update_keywords_for_new(date_from=yesterday, max_keywords=5)
    
    kw_elapsed = (datetime.now() - kw_start).total_seconds()
    print(f"OK 更新关键词：{kw_count} 条")
    print(f"OK 耗时：{kw_elapsed:.1f}秒\n")
    
    # 完成
    total_elapsed = (datetime.now() - start_time).total_seconds()
    print(f"{'='*60}")
    print(f"阶段 2 完成！")
    print(f"总耗时：{total_elapsed:.1f}秒")
    print(f"{'='*60}")
    print(f"\n统计：")
    print(f"  标记重复：{dup_count} 条")
    print(f"  更新关键词：{kw_count} 条")
    print(f"\nPROCESS_DONE")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        import traceback
        print(f"\nERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
