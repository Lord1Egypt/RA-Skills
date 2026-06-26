#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持仓汇总 - 命令行输出版本

用于定时任务执行（如 cron），无持仓时自动退出。

依赖: mt4_client.py, summary_utils.py
"""
import sys
import os
import logging

# 动态路径，无需硬编码
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mt4_client import MT4Client
from summary_utils import build_position_summary

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("position_summary")


def main():
    logger.info("开始获取持仓数据...")
    c = MT4Client()

    try:
        r = c.get_positions()
    except Exception as e:
        logger.exception("获取持仓失败")
        sys.exit(1)

    summary, count, total_pl = build_position_summary(r)

    if count == 0:
        print(summary)
        logger.info("当前空仓，任务结束。")
        # 不自动取消 cron 任务 —— 调度器应自行决策
        return

    print(summary)
    logger.info("持仓汇总已输出（共 %d 单，总盈亏 $%.2f）", count, total_pl)


if __name__ == "__main__":
    main()