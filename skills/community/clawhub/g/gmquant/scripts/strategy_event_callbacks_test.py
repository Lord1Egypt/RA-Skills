"""
策略名称：on_execution_report + on_order_status 专项测试
描述：全面测试两个交易事件回调的完整生命周期
  - on_execution_report: 成交回报（每笔成交/部分成交都触发）
  - on_order_status: 委托状态变更（新建→已报→部分成交→已成/已撤/拒单）

测试场景：
  1. 市价买入 → 正常成交（状态流转 + 成交回报）
  2. 市价卖出 → 正常成交
  3. 限价买入 → 可能部分成交或未成交
  4. order_volume / order_target_volume 两种下单方式对比
  5. 资金不足时的拒单（on_order_status 拒绝原因）
  6. 卖出超出持仓 → 预期触发拒绝

生成时间：2026-04-17
"""

import sys, os, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *

# ============================================================
# 配置区
# ============================================================

TEST_SYMBOL = 'SHSE.600519'    # 贵州茅台 — 流动性好
TEST_SYMBOL_2 = 'SZSE.000858'  # 五粮液

FREQUENCY = '1d'

# 回测参数 — 用短周期方便观察事件
BACKTEST_START = '2025-01-06 09:30:00'   # 从2025年初开始
BACKTEST_END   = '2025-03-15 15:30:00'    # 约2个月，覆盖多次调仓
INITIAL_CASH   = 100000
COMMISSION     = 0.00025
SLIPPAGE       = 0.001


# ============================================================
# 全局计数器 — 用于统计各事件触发次数
# ============================================================

class EventTracker:
    """追踪所有事件回调的触发情况"""

    def __init__(self):
        self.order_status_events = []   # 所有 on_order_status 事件
        self.execution_events = []      # 所有 on_execution_report 事件
        self.order_counter = 0          # 下单序号
        self.bar_counter = 0            # bar 计数
        self.errors = []                # 错误记录

    def next_order_id(self):
        self.order_counter += 1
        return f'ORD-{self.order_counter:03d}'

    def log_order_status(self, context, order, tag=''):
        """记录 on_order_status 的详细信息"""
        info = {
            'seq': len(self.order_status_events) + 1,
            'tag': tag,
            'time': str(context.now) if hasattr(context, 'now') else 'N/A',
        }

        # 提取 order 对象的所有字段
        if isinstance(order, dict):
            info.update(order)
        else:
            # 尝试作为对象取属性
            for attr in ['cl_ord_id', 'order_id', 'symbol', 'status', 'side',
                         'volume', 'price', 'filled_volume', 'filled_vwap',
                         'created_at', 'rejection_reason', 'reason_msg',
                         'order_type', 'position_effect']:
                try:
                    val = getattr(order, attr, None)
                    if val is not None:
                        info[attr] = val
                except:
                    pass

        self.order_status_events.append(info)

        # 状态文字说明
        status_code = info.get('status', '?')
        status_map = {
            1: '新建(New)',
            2: '已报(Sent)',
            3: '部分成交(PartiallyFilled)',
            4: '已成交(Filled)',
            5: '已撤(Cancelled)',
            6: '未成交(Expired)',     # 限价超时
            7: '拒绝(Rejected)',       # 柜台拒绝
            8: '待撤(Cancelling)',
            9: '未知(Unknown)',
        }
        status_text = status_map.get(status_code, f'未知({status_code})')

        symbol = info.get('symbol', '?')
        side = info.get('side', '?')
        side_text = {1: '买', 2: '卖'}.get(side, str(side))
        vol = info.get('volume', '?')
        filled = info.get('filled_volume', '?')
        price = info.get('price', '?')

        print(f'  📋 [订单状态 #{info["seq"]}] {tag} | {symbol} {side_text}{vol}股 @{price} '
              f'| 状态: {status_text} | 已成: {filled}')

        # 如果是拒绝状态，重点打印原因
        if status_code == 7:
            reason = info.get('rejection_reason', info.get('reason_msg', '未知原因'))
            print(f'      ❌ *** 拒绝原因: {reason} ***')

    def log_execution(self, context, execrpt, tag=''):
        """记录 on_execution_report 的详细信息"""
        info = {
            'seq': len(self.execution_events) + 1,
            'tag': tag,
            'time': str(context.now) if hasattr(context, 'now') else 'N/A',
        }

        if isinstance(execrpt, dict):
            info.update(execrpt)
        else:
            for attr in ['cl_ord_id', 'order_id', 'symbol', 'side', 'volume',
                         'price', 'exec_type', 'exec_id', 'commission',
                         'created_at']:
                try:
                    val = getattr(execrpt, attr, None)
                    if val is not None:
                        info[attr] = val
                except:
                    pass

        self.execution_events.append(info)

        symbol = info.get('symbol', '?')
        side = info.get('side', '?')
        side_text = {1: '买', 2: '卖'}.get(side, str(side))
        vol = info.get('volume', '?')
        price = info.get('price', '?')
        exec_type = info.get('exec_type', '?')

        exec_type_map = {
            'T': 'Trade(成交)',
            'C': 'Cancel(撤单确认)',
        }
        exec_text = exec_type_map.get(str(exec_type), f'{exec_type}')

        commission = info.get('commission', '?')
        print(f'  💰 [成交回报 #{info["seq"]}] {tag} | {symbol} {side_text} '
              f'{vol}股 @ {price}元 | 类型: {exec_text} | 手续费: {commission}')

    def print_summary(self):
        """打印最终汇总"""
        print('\n' + '=' * 70)
        print(f'  📊 事件回调测试汇总报告')
        print('=' * 70)
        print(f'  on_order_status 触发次数: {len(self.order_status_events)}')
        print(f'  on_execution_report 触发次数: {len(self.execution_events)}')
        print(f'  总下单次数: {self.order_counter}')
        print(f'  on_bar 触发次数: {self.bar_counter}')
        print(f'  错误/异常: {len(self.errors)}')

        if self.errors:
            print('\n  ❌ 错误列表:')
            for e in self.errors:
                print(f'      - {e}')

        # 状态分布统计
        if self.order_status_events:
            status_counts = {}
            for ev in self.order_status_events:
                s = ev.get('status', '?')
                status_counts[s] = status_counts.get(s, 0) + 1

            print(f'\n  📋 委托状态分布:')
            status_map = {
                1: '新建', 2: '已报', 3: '部分成交', 4: '已成交',
                5: '已撤', 6: '未成交', 7: '拒绝', 8: '待撤',
            }
            for code, count in sorted(status_counts.items()):
                name = status_map.get(code, f'未知{code}')
                print(f'      状态 {code}({name}): {count}次')


# 全局追踪器实例（在 init 中创建）
tracker = None


# ============================================================
# 策略主逻辑
# ============================================================

def init(context):
    global tracker
    tracker = EventTracker()

    print('=' * 70)
    print('  🔬 on_execution_report + on_order_status 专项测试策略')
    print('=' * 70)
    print(f'  测试标的: {TEST_SYMBOL}, {TEST_SYMBOL_2}')
    print(f'  回测区间: {BACKTEST_START} ~ {BACKTEST_END}')
    print(f'  初始资金: {INITIAL_CASH:,}元')
    print(f'  测试内容:')
    print('    ① 市价买入 (order_volume)')
    print('    ② 市价卖出 (order_target_volume)')
    print('    ③ 限价买单 (可能部分成交/未成交)')
    print('    ④ 超额卖出 (预期被拒)')
    print('    ⑤ 超额买入 (预期因资金不足被拒)')
    print('=' * 70)

    # 订阅行情
    subscribe(symbols=f'{TEST_SYMBOL},{TEST_SYMBOL_2}', frequency=FREQUENCY, count=5)

    # 状态标记
    context.phase = 0           # 当前处于哪个测试阶段
    context.last_phase_date = None  # 上次执行阶段的日子


def on_bar(context, bars):
    """
    每个 bar 触发一次，按日期分阶段执行不同测试
    Phase 0: 市价买入（第1个bar）
    Phase 1: 再买一笔 + 限价单测试（第3个bar）
    Phase 2: 部分卖出（第5个bar）
    Phase 3: 全部清仓（第7个bar）
    Phase 4: 尝试超额卖出（第9个bar，预期被拒）
    Phase 5: 尝试超额买入（第11个bar，预期资金不足被拒）
    """
    global tracker
    tracker.bar_counter += 1
    bar_num = tracker.bar_counter

    if bars:
        bar0 = bars[0]
        current_dt = None
        if isinstance(bar0, dict):
            current_dt = bar0.get('datetime') or bar0.get('bob')
        else:
            current_dt = getattr(bar0, 'datetime', None) or getattr(bar0, 'bob', None)

        date_str = str(current_dt)[:10] if current_dt else f'bar-{bar_num}'
    else:
        date_str = f'bar-{bar_num}'

    # ---- 根据不同的 bar 执行不同的测试 ----

    # === Phase 0: 市价买入 ===
    if bar_num == 1:
        print(f'\n{"─"*70}')
        print(f'  🧪 Phase 0 [Bar#{bar_num} {date_str}]: 市价买入 {TEST_SYMBOL}')
        print(f'{"─"*70}')

        try:
            oid = tracker.next_order_id()
            # 用市价单买入约 50% 资金
            cash = get_cash()
            buy_amount = cash.available * 0.5
            price_data = history_n(symbol=TEST_SYMBOL, frequency='1d', count=1,
                                   fields='close', adjust=ADJUST_PREV, df=True)
            if price_data is not None and len(price_data) > 0:
                price = price_data['close'].iloc[0]
                volume = int(buy_amount / price / 100) * 100
                volume = max(volume, 100)

                print(f'  可用资金: {cash.available:,.0f}元, 计划买入: {volume}股 @{price:.2f}元')
                order_volume(symbol=TEST_SYMBOL, volume=volume,
                             side=OrderSide_Buy, order_type=OrderType_Market,
                             position_effect=PositionEffect_Open, price=0)
                oid = tracker.next_order_id()
                print(f'  ✅ 已发送市价买入委托: cl_ord_id={oid}')
            else:
                print(f'  ⚠️ 无法获取价格，跳过')
        except Exception as e:
            print(f'  ❌ Phase 0 异常: {e}')
            tracker.errors.append(f'Phase 0: {e}')

    # === Phase 1: 第二笔买入 + 限价单测试 ===
    elif bar_num == 3:
        print(f'\n{"─"*70}')
        print(f'  🧪 Phase 1 [Bar#{bar_num} {date_str}]: 第二笔买入 + 限价单测试')
        print(f'{"─"*70}')

        try:
            # 1a: 再用 order_target_volume 买入一点
            cash = get_cash()
            if cash.available > 5000:
                oid_a = tracker.next_order_id()
                order_target_volume(symbol=TEST_SYMBOL_2, volume=200,
                                    position_side=PositionSide_Long,
                                    order_type=OrderType_Market)
                print(f'  ✅ 1a. order_target_volume 买入 {TEST_SYMBOL_2} 200股, id={oid_a}')

            # 1b: 发一个远低于市场价的限价买单（预期不会成交或部分成交）
            oid_b = tracker.next_order_id()
            # 获取当前价格，设一个很低的价格
            price_data = history_n(symbol=TEST_SYMBOL, frequency='1d', count=1,
                                   fields='close', adjust=ADJUST_PREV, df=True)
            if price_data is not None and len(price_data) > 0:
                curr_price = price_data['close'].iloc[0]
                limit_price = round(curr_price * 0.5, 2)  # 半价买入，基本不可能成交
                print(f'  📝 1b. 发送限价买单: {TEST_SYMBOL} 100股 @ {limit_price}元 '
                      f'(现价约 {curr_price:.2f}元), id={oid_b}')
                order_volume(symbol=TEST_SYMBOL, volume=100,
                             side=OrderSide_Buy, order_type=OrderType_Limit,
                             position_effect=PositionEffect_Open, price=limit_price)

        except Exception as e:
            print(f'  ❌ Phase 1 异常: {e}')
            tracker.errors.append(f'Phase 1: {e}')

    # === Phase 2: 部分卖出 ===
    elif bar_num == 5:
        print(f'\n{"─"*70}')
        print(f'  🧪 Phase 2 [Bar#{bar_num} {date_str}]: 部分卖出 {TEST_SYMBOL}')
        print(f'{"─"*70}')

        try:
            positions = get_position()
            pos_vol = 0
            if positions:
                for p in positions:
                    sym = p.get('symbol') if isinstance(p, dict) else (p.symbol if hasattr(p, 'symbol') else '')
                    if sym == TEST_SYMBOL:
                        pos_vol = p.get('volume', 0) if isinstance(p, dict) else (getattr(p, 'volume', 0))

            if pos_vol >= 200:
                sell_vol = pos_vol // 2  # 卖出一半
                oid = tracker.next_order_id()
                order_volume(symbol=TEST_SYMBOL, volume=sell_vol,
                             side=OrderSide_Sell, order_type=OrderType_Market,
                             position_effect=PositionEffect_Close, price=0)
                print(f'  ✅ 卖出 {sell_vol}股 (持仓{pos_vol}股的一半), id={oid}')
            elif pos_vol > 0:
                sell_vol = min(pos_vol, 100)
                oid = tracker.next_order_id()
                order_volume(symbol=TEST_SYMBOL, volume=sell_vol,
                             side=OrderSide_Sell, order_type=OrderType_Market,
                             position_effect=PositionEffect_Close, price=0)
                print(f'  ✅ 卖出全部 {sell_vol}股, id={oid}')
            else:
                print(f'  ⚠️ 无持仓可卖，跳过')
                tracker.errors.append(f'Phase 2: 无持仓可卖')

        except Exception as e:
            print(f'  ❌ Phase 2 异常: {e}')
            tracker.errors.append(f'Phase 2: {e}')

    # === Phase 3: 清仓剩余 ===
    elif bar_num == 7:
        print(f'\n{"─"*70}')
        print(f'  🧪 Phase 3 [Bar#{bar_num} {date_str}]: 全部平仓 (order_target_volume→0)')
        print(f'{"─"*70}')

        try:
            oid = tracker.next_order_id()
            order_target_volume(symbol=TEST_SYMBOL, volume=0,
                                position_side=PositionSide_Long,
                                order_type=OrderType_Market)
            print(f'  ✅ 清仓 {TEST_SYMBOL}, id={oid}')

            oid2 = tracker.next_order_id()
            order_target_volume(symbol=TEST_SYMBOL_2, volume=0,
                                position_side=PositionSide_Long,
                                order_type=OrderType_Market)
            print(f'  ✅ 清仓 {TEST_SYMBOL_2}, id={oid2}')

        except Exception as e:
            print(f'  ❌ Phase 3 异常: {e}')
            tracker.errors.append(f'Phase 3: {e}')

    # === Phase 4: 尝试超额卖出（预期被拒）===
    elif bar_num == 9:
        print(f'\n{"─"*70}')
        print(f'  🧪 Phase 4 [Bar#{bar_num} {date_str}]: 超额卖出测试 (预期触发拒绝)')
        print(f'{"─"*70}')

        try:
            oid = tracker.next_order_id()
            # 尝试卖出 99999 股（肯定没有这么多持仓）
            order_volume(symbol=TEST_SYMBOL, volume=99999,
                         side=OrderSide_Sell, order_type=OrderType_Market,
                         position_effect=PositionEffect_Close, price=0)
            print(f'  📤 已发送超额卖出请求: {TEST_SYMBOL} 99999股, id={oid}')
            print(f'     → 预期 on_order_status 会收到 Rejected 状态')

        except Exception as e:
            print(f'  ❌ Phase 4 异常 (可能在下单时直接抛异常): {e}')
            tracker.errors.append(f'Phase 4: {e}')

    # === Phase 5: 尝试超额买入（预期资金不足被拒）===
    elif bar_num == 11:
        print(f'\n{"─"*70}')
        print(f'  🧪 Phase 5 [Bar#{bar_num} {date_str}]: 超额买入测试 (预期资金不足)')
        print(f'{"─"*70}')

        try:
            cash = get_cash()
            oid = tracker.next_order_id()
            # 尝试买入远超可用资金的量
            order_value(symbol=TEST_SYMBOL, value=cash.nav * 100,
                        side=OrderSide_Buy, order_type=OrderType_Market,
                        position_effect=PositionEffect_Open, price=0)
            print(f'  📤 已发送超额买入请求: {TEST_SYMBOL} 金额={cash.nav*100:,.0f}元 (可用{cash.available:,.0f}), id={oid}')
            print(f'     → 预期 on_order_status 会收到 Rejected 状态')

        except Exception as e:
            print(f'  ❌ Phase 5 异常 (可能在下单时直接抛异常): {e}')
            tracker.errors.append(f'Phase 5: {e}')


def on_tick(context, tick):
    pass


# ============================================================
# 核心测试回调 — 这是本次测试的重点！！！
# ============================================================

def on_execution_report(context, execrpt):
    """
    成交回报事件 — 每当有成交发生时触发（包括部分成交）
    这是最关键的事件之一，用于实时跟踪实际成交
    """
    global tracker
    if tracker is None:
        return

    tracker.log_execution(context, execrpt)


def on_order_status(context, order):
    """
    委托状态变更事件 — 订单生命周期中的每个状态变化都会触发
    包括：
      新建(1) → 已报(2) → 部分成交(3) → 已成交(4)
                              ↘ 已撤(5) / 未成交(6) / 拒绝(7)
    特别重要的是 status==7（拒绝）时会包含 rejection_reason
    """
    global tracker
    if tracker is None:
        return

    # 用当前阶段做 tag
    tag = f'Phase{(tracker.bar_counter - 1) // 2}'
    tracker.log_order_status(context, order, tag=tag)


def on_backtest_finished(context, indicator):
    """回测结束时打印完整的汇总报告"""
    global tracker
    if tracker is None:
        return

    tracker.print_summary()

    print(f'\n  📈 绩效指标:')
    if indicator:
        for key in ['pnl_ratio', 'pnl_ratio_annual', 'sharp_ratio',
                     'max_drawdown', 'win_ratio', 'open_count', 'close_count']:
            val = indicator.get(key) if isinstance(indicator, dict) else getattr(indicator, key, None)
            if val is not None:
                label = {'pnl_ratio': '累计收益率', 'pnl_ratio_annual': '年化收益率',
                         'sharp_ratio': '夏普比率', 'max_drawdown': '最大回撤',
                         'win_ratio': '胜率', 'open_count': '开仓次数',
                         'close_count': '平仓次数'}.get(key, key)
                if isinstance(val, float):
                    print(f'      {label}: {val:.4f}')
                else:
                    print(f'      {label}: {val}')


def handle_error(context, error_code, error_msg, **kwargs):
    """全局错误处理"""
    global tracker
    print(f'\n  ⚠️ [全局错误] code={error_code}, msg={error_msg}')
    if tracker:
        tracker.errors.append(f'GlobalError[{error_code}]: {error_msg}')


# ============================================================
# 启动入口
# ============================================================
if __name__ == '__main__':
    TOKEN = os.environ.get('GM_TOKEN', '') or ''
    MODE = os.environ.get('GM_RUN_MODE', 'backtest')
    STRATEGY_ID = os.environ.get('GM_STRATEGY_ID', '') or 'event_callback_test_v1'
    START = os.environ.get('GM_BACKTEST_START', BACKTEST_START)
    END = os.environ.get('GM_BACKTEST_END', BACKTEST_END)
    CASH = float(os.environ.get('GM_INITIAL_CASH', str(INITIAL_CASH)))

    mode = MODE_LIVE if MODE.lower() in ('live', 'realtime') else MODE_BACKTEST

    run(
        strategy_id=STRATEGY_ID,
        filename='strategy_event_callbacks_test',
        mode=mode,
        token=TOKEN,
        backtest_start_time=START,
        backtest_end_time=END,
        backtest_initial_cash=CASH,
        backtest_commission_ratio=COMMISSION,
        backtest_slippage_ratio=SLIPPAGE,
        backtest_adjust=ADJUST_PREV,
    )
