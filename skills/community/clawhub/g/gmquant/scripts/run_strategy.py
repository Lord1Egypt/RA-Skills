"""
掘金量化策略运行器 v2.3
用法：
  python run_strategy.py --strategy my_strategy.py --strategy-id my_ma_strategy --mode backtest --token YOUR_TOKEN
  python run_strategy.py --strategy my_strategy.py --mode live --token YOUR_TOKEN  # 仿真/实盘

设计：通过 subprocess 启动策略文件自身，避免在 run_strategy 内部 import gm
策略文件自身的 __main__ 入口负责调用 run()

v2.2 新增：
  --strategy-id 参数：回测结果会持久化到掘金终端，用户可在终端网页查看绩效分析图表

v2.3 新增：
  --account-id 参数：live 模式下指定仿真/实盘账户 ID（默认 e402bd7b-2e5f-11f1-ae79-00163e022aa6）
"""

import sys
import os
import io
import subprocess
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def main():
    parser = argparse.ArgumentParser(description='掘金量化策略运行器 v2.3')
    parser.add_argument('--strategy', '-s', required=True,
                        help='策略 .py 文件路径（绝对或相对路径）')
    parser.add_argument('--strategy-id', '-i', default='',
                        help='策略ID（填完后回测结果持久化到掘金终端，可在终端网页查看绩效分析图表）')
    parser.add_argument('--account-id', '-a', default='',
                        help='仿真/实盘账户ID(live模式使用)')
    parser.add_argument('--mode', '-m', default='backtest',
                        choices=['backtest', 'live'],
                        help='运行模式: backtest(回测) / live(实盘仿真)，默认 backtest')
    parser.add_argument('--token', '-t', default='',
                        help='掘金 Token')
    parser.add_argument('--start', default='',
                        help='回测开始时间 (2024-01-01 09:30:00)')
    parser.add_argument('--end', default='',
                        help='回测结束时间 (2025-12-31 15:30:00)')
    parser.add_argument('--cash', type=float, default=0,
                        help='初始资金（0=使用策略内默认）')

    args = parser.parse_args()

    # ---- 验证文件 ----
    strategy_path = os.path.abspath(args.strategy)
    if not os.path.exists(strategy_path):
        print(f'[ERROR] 策略文件不存在: {strategy_path}')
        sys.exit(1)

    mode = args.mode.upper()
    account_id = args.account_id or 'e402bd7b-2e5f-11f1-ae79-00163e022aa6'
    print('=' * 60)
    print('  掘金量化策略运行器 v2.3')
    print('=' * 60)
    print(f'  策略   : {strategy_path}')
    print(f'  模式   : {mode}')
    if mode == 'LIVE':
        print(f'  账户ID : {account_id}')
    print(f'  Token  : {(args.token[:8]+"...") if len(args.token)>12 else args.token or "(未设置)"}')
    if args.strategy_id:
        print(f'  策略ID : {args.strategy_id}  ← 终端可查看绩效分析')
    else:
        print(f'  策略ID : (未设置)  ← 提示: 填写 --strategy-id 可在终端查看绩效图表')
    if args.start:
        print(f'  开始   : {args.start}')
    if args.end:
        print(f'  结束   : {args.end}')
    if args.cash > 0:
        print(f'  资金   : {args.cash:,.0f}')
    print('=' * 60 + '\n')

    # ---- 构建子进程命令 ----
    cmd = [sys.executable, strategy_path]

    # 通过环境变量传递参数给策略文件的 __main__
    env = os.environ.copy()
    env['GM_RUN_MODE'] = args.mode
    env['GM_TOKEN'] = args.token
    if args.strategy_id:
        env['GM_STRATEGY_ID'] = args.strategy_id
    env['GM_ACCOUNT_ID'] = account_id
    if args.start:
        env['GM_BACKTEST_START'] = args.start
    if args.end:
        env['GM_BACKTEST_END'] = args.end
    if args.cash > 0:
        env['GM_INITIAL_CASH'] = str(args.cash)

    # 切换工作目录到策略所在目录
    cwd = os.path.dirname(strategy_path)

    # ---- 执行策略 ----
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            check=False,
            capture_output=False,  # 直接输出到控制台
        )
        exit_code = proc.returncode
    except KeyboardInterrupt:
        print('\n[INFO] 用户中断')
        exit_code = 130
    except Exception as e:
        print(f'[FATAL] 运行异常: {e}')
        exit_code = 1

    print('\n' + '=' * 60)
    print(f'  策略执行完成 (exit code={exit_code})')
    print('=' * 60)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
