"""
OKX 量化定时调度服务
基于 APScheduler 在后台按计划自动执行数据获取和指标计算。
- 周一至周五：每 1 小时触发一次
- 周六、周日：每 6 小时触发一次
支持多周期同时监控。
"""

import argparse
import logging
import signal
import sys
import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

# 同级目录引入指标计算核心
from calculator import process_data

# ========== 日志配置 ==========

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("okx-scheduler")


# ========== 任务逻辑 ==========

def job_fetch_and_calculate(inst_id: str, bars: list, limit: int, profile: str):
    """
    定时任务的实际执行体：获取数据并计算指标。
    """
    logger.info(f"▶ 定时任务触发 — 标的: {inst_id}, 周期: {bars}, Profile: {profile}")
    try:
        results = process_data(
            inst_id=inst_id,
            bars=bars,
            limit=limit,
            profile=profile,
            output_json=False,  # 后台调度使用人类可读格式输出到终端/日志
        )
        # 统计成功/失败
        success = sum(1 for r in results if "error" not in r)
        failed = len(results) - success
        logger.info(f"✔ 任务完成 — 成功: {success}, 失败: {failed}")
    except Exception as e:
        logger.error(f"✘ 任务执行过程异常: {e}")


# ========== APScheduler 事件监听 ==========

def job_listener(event):
    """监听调度器的任务执行事件，记录异常。"""
    if event.exception:
        logger.error(f"调度器捕获到异常任务: {event.job_id}, 错误: {event.exception}")


# ========== 主程序 ==========

def main():
    parser = argparse.ArgumentParser(
        description="OKX 量化定时调度器 — 按固定周期自动拉取数据并计算技术指标",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用示例:
  # 监控 BTC-USDT 的 1小时线（实盘环境）
  python scheduler.py --instId BTC-USDT --bar 1H --profile live

  # 同时监控 1H/4H/1D 三个周期（模拟盘）
  python scheduler.py --instId BTC-USDT --bar 1H 4H 1D --profile demo
""",
    )
    parser.add_argument("--instId", type=str, required=True,
                        help="交易标的, 例: BTC-USDT, ETH-USDT-SWAP")
    parser.add_argument("--bar", type=str, nargs="+", default=["1H"],
                        help="时间周期，可指定多个，例: 1H 4H 1D")
    parser.add_argument("--limit", type=int, default=100,
                        help="每个周期获取数据条数（最大 300）")
    parser.add_argument("--profile", type=str, default="live",
                        choices=["live", "demo"],
                        help="运行环境: live (实盘) / demo (模拟盘)")

    args = parser.parse_args()
    inst_id = args.instId
    bars = args.bar
    limit = args.limit
    profile = args.profile

    logger.info("=" * 60)
    logger.info(f"OKX 量化调度服务启动")
    logger.info(f"  标的: {inst_id}")
    logger.info(f"  周期: {', '.join(bars)}")
    logger.info(f"  Profile: {profile}")
    logger.info(f"  平日 (周一~周五): 每 1 小时触发")
    logger.info(f"  周末 (周六~周日): 每 6 小时触发")
    logger.info("=" * 60)

    # 首次启动时立即执行一次，验证数据通路
    logger.info("执行首次数据验证...")
    job_fetch_and_calculate(inst_id, bars, limit, profile)

    # 初始化调度器
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    scheduler.add_listener(job_listener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)

    # 定时任务共用参数
    job_args = [inst_id, bars, limit, profile]

    # 周一至周五：每 1 小时（整点）触发
    scheduler.add_job(
        func=job_fetch_and_calculate,
        trigger="cron",
        day_of_week="mon-fri",
        hour="*",
        minute=0,
        args=job_args,
        id="weekday_hourly",
        name=f"平日每小时监控 {inst_id}",
        replace_existing=True,
        misfire_grace_time=300,  # 允许 5 分钟的 misfire 容忍
    )

    # 周六、周日：每 6 小时触发 (0, 6, 12, 18 点)
    scheduler.add_job(
        func=job_fetch_and_calculate,
        trigger="cron",
        day_of_week="sat,sun",
        hour="0,6,12,18",
        minute=0,
        args=job_args,
        id="weekend_6hourly",
        name=f"周末6小时监控 {inst_id}",
        replace_existing=True,
        misfire_grace_time=300,
    )

    scheduler.start()
    logger.info("调度服务已就绪。按 Ctrl+C 退出。")

    # 优雅退出处理
    def shutdown_handler(signum, frame):
        logger.info("收到退出信号，正在关闭调度器...")
        scheduler.shutdown(wait=False)
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # 主线程保持存活
    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("调度器已关闭。")
        scheduler.shutdown(wait=False)


if __name__ == "__main__":
    main()
