"""Pure conditional route comparison. No account mutation, receipts or orders.

All amounts describe a hypothetical confirmed first leg, never an actual fill.
Uses only displayed depth; missing deeper levels remain unknown.
"""
from decimal import ROUND_CEILING
from pm_predict.domain.money import D, ZERO, dec, fee


def ceil_tick(value, tick):
    return (value / tick).to_integral_value(rounding=ROUND_CEILING) * tick


def sweep(levels, quantity, *, buy, cap=None):
    normalized = [(dec(p), dec(q)) for p, q in levels]
    if any(not ZERO < p < 1 or q <= 0 for p, q in normalized):
        raise ValueError('invalid depth')
    if len({p for p, _ in normalized}) != len(normalized):
        raise ValueError('duplicate depth price')
    normalized.sort(reverse=not buy)
    left, gross, fees, worst = quantity, ZERO, ZERO, None
    for p, size in normalized:
        if cap is not None and p > cap:
            continue
        take = min(left, size)
        gross += take * p
        fees += fee(take, p)
        left -= take
        worst = p
        if left == 0:
            break
    return {'complete': left == 0, 'gross': gross, 'fee': fees,
            'worst': worst, 'visible_qty': quantity - left, 'missing_qty': left}


def compare_routes(snapshot, side, quantity, entry_price, plan):
    """Condition: first leg fully confirmed at its limit, fee zero; no other fills.

    Conservative limit-price bounds supplement displayed VWAP estimates. They
    bound this calculation, not unknown fees/latency/actual exchange execution.
    """
    q, basis = dec(quantity), dec(entry_price)
    # Actual fees can make a confirmed position's basis >= $1. Such a position
    # cannot exit at break-even; do not crash or pretend its basis is cheaper.
    if side not in ('Up', 'Down') or not ZERO < q <= dec(plan['max_shares']) or not ZERO < basis:
        raise ValueError('invalid assumed position')
    market = snapshot['market']
    tick, minimum = dec(market['tick']), dec(market['min_qty'])
    if tick <= 0 or tick >= 1 or minimum <= 0:
        raise ValueError('invalid market increments')
    opposite = 'Down' if side == 'Up' else 'Up'
    books = snapshot['books']
    own, other = books[side], books[opposite]
    cost = q * basis
    age = snapshot['now_ms'] / 1000 - market['start']
    size_ok = q >= minimum and q % D('.01') == 0
    sell = sweep(own['bids'], q, buy=False)
    pair = sweep(other['asks'], q, buy=True, cap=dec(plan['buy_cap']))
    account = snapshot.get('paper', {}).get('account', {})
    cash = max(ZERO, dec(account.get('cash', '0')) - dec(account.get('reserved', '0')))

    sell_reasons = []
    pair_reasons = []
    if not size_ok:
        sell_reasons.append('不足最小委托量或份额精度不符，不能加仓凑数')
        pair_reasons.append('不足最小委托量或份额精度不符')
    sell_net = sell_bound = None
    if sell['complete']:
        sell_net = sell['gross'] - sell['fee'] - cost
        sell_bound = q * sell['worst'] - fee(q, sell['worst']) - cost
        if sell_bound < 0:
            sell_reasons.append('按最差可见卖价扣费后不能保本')
        if sell['worst'] % tick:
            sell_reasons.append('当前价位与市场 tick 不一致')
    else:
        sell_reasons.append('展示的前 10 档不足；更深盘口未知')

    pair_net = pair_bound = None
    if pair['complete']:
        allowance = q * dec(plan['merge_allowance_per_share'])
        pair_net = q - cost - pair['gross'] - pair['fee'] - allowance
        extra_bound = q * pair['worst'] + fee(q, pair['worst']) + allowance
        pair_bound = q - cost - extra_bound
        if cost + extra_bound > q * dec(plan['pair_cap']):
            pair_reasons.append('最差含费配对成本超过原 0.95 上限')
        if extra_bound > cash:
            pair_reasons.append('原账户可用预算不足；不会另开账户或释放未知预留')
        if pair['worst'] % tick:
            pair_reasons.append('当前价位与市场 tick 不一致')
    else:
        pair_reasons.append('0.50 买价上限内可见深度不足；更深盘口未知')
    if age >= plan['no_buy_age_seconds']:
        pair_reasons.append('已到第 14 分钟，原规则禁止新增买入')
    if age >= plan['window_seconds']:
        sell_reasons.append('窗口已结束，不能沿用旧盘口判断退出')

    # A passive sell is only a price proposal, never queue position or a fill.
    best_bid = max((dec(p) for p, _ in own['bids']), default=ZERO)
    maker_price = ceil_tick(max(basis, best_bid + tick), tick)
    maker_price = maker_price if maker_price < 1 and size_ok and age < 900 else None
    sell_ok = not sell_reasons
    pair_ok = not pair_reasons
    if sell_ok and (not pair_ok or sell_bound >= pair_bound):
        recommendation = 'SELL'
    elif pair_ok:
        recommendation = 'PAIR'
    else:
        recommendation = 'WAIT'
    return {
        'recommendation': recommendation,
        'quantity': str(q), 'side': side, 'assumed_entry_price': str(basis),
        'assumed_cost': str(cost), 'max_directional_loss_if_zero': str(cost),
        'sell': {'eligible': sell_ok, 'reasons': sell_reasons, 'net_estimate': sell_net,
                 'net_at_limit': sell_bound, 'visible_qty': sell['visible_qty'],
                 'missing_qty': sell['missing_qty'], 'fee_estimate': sell['fee'],
                 'limit_price': sell['worst'], 'maker_ask_proposal': maker_price},
        'pair': {'eligible': pair_ok, 'reasons': pair_reasons, 'net_estimate': pair_net,
                 'net_at_limit': pair_bound, 'visible_qty': pair['visible_qty'],
                 'missing_qty': pair['missing_qty'], 'fee_estimate': pair['fee'],
                 'limit_price': pair['worst']},
        'wait': {'pair_seconds_left': max(0, int(840 - age)),
                 'window_seconds_left': max(0, int(900 - age)),
                 'risk_deadline_reached': age >= 840,
                 'note': '等待期间可能亏损；第14分钟只继续比较卖出，期末未退持仓按未知结算处理。没有自动亏损卖出授权参数。'},
        'execution_allowed': False, 'actual_fill': None, 'actual_profit': None,
        'assumption': '仅假设此首腿意图全成、入场 Maker 费为0；不是确认持仓，不生成任何成交或盈亏。',
    }


def evaluate_snapshot(snapshot, plan, *, source_age_ms=0):
    market = snapshot.get('market') or {}
    paper = snapshot.get('paper') or {}
    signal = paper.get('signal') or {}
    now = snapshot.get('now_ms', 0)
    result = {'market': market.get('slug'), 'signal_side': signal.get('side'),
              'source_run_id': snapshot.get('run_id'), 'source_now_ms': now,
              'state': 'WAIT_ENTRY', 'message': '等待本窗口通过原条件的首腿意图。',
              'routes': None, 'issues': [], 'execution_allowed': False,
              'actual_fill': None, 'actual_profit': None}
    issues = result['issues']
    if snapshot.get('status') != 'RUNNING' or not snapshot.get('process_alive'):
        issues.append('采集进程未运行')
    if not 0 <= source_age_ms <= 2000:
        issues.append('本地 API 快照或读取耗时超过 2 秒')
    if not market or not market.get('start', float('inf')) * 1000 <= now < market.get('end', 0) * 1000:
        issues.append('当前15分钟市场不匹配或已结束')
    if signal.get('start') != market.get('start'):
        issues.append('K14 信号不属于当前窗口')
    if not (market.get('rules_verified') and market.get('fees_verified') and market.get('accepting')) or market.get('closed'):
        issues.append('市场规则、费用或交易状态未通过原检查')
    clock = snapshot.get('clock') or {}
    if clock.get('age_ms', float('inf')) + max(0, source_age_ms) > 120000:
        issues.append('校时锚点过期')
    if clock.get('residual_bound_ms', float('inf')) >= 50:
        issues.append('校时误差未低于原 50 ms 门槛')
    if snapshot.get('health', {}).get('status') != 'READY':
        issues.extend(snapshot.get('health', {}).get('reasons') or ['原输入健康检查未通过'])
    for side in ('Up', 'Down'):
        book = snapshot.get('books', {}).get(side) or {}
        if not book.get('valid') or not book.get('bids') or not book.get('asks') or not 0 <= book.get('age_ms', float('inf')) + max(0, source_age_ms) <= 2000:
            issues.append(side + ' 盘口无效、缺失或超过原2秒门槛')
    if snapshot.get('storage', {}).get('error'):
        issues.append('原始采集写入异常')
    orders = [o for o in paper.get('orders', []) if o.get('market') == market.get('slug')]
    if not orders:
        result['message'] = '当前 K14 没有信号，继续监视。' if signal.get('side') is None else '已有 K14 方向，但尚无通过原条件的首腿意图。'
    elif len(orders) != 1 or orders[0].get('side') != signal.get('side'):
        issues.append('多张意图或方向不符；无法确定首腿成本与持仓，不能相加假设全成')
    else:
        order = orders[0]
        result['order_id'] = order['id']
        result['state'] = 'FILL_UNKNOWN'
        result['message'] = '首腿成交未知；以下仅是假设全成后的退出比较，不能据此发出第二笔订单。'
        if not issues:
            try:
                result['routes'] = compare_routes(snapshot, order['side'], order['qty'], order['price'], plan)
            except (ValueError, KeyError, TypeError, ArithmeticError) as ex:
                issues.append('输入格式异常：' + str(ex))
    if issues:
        result['state'] = 'INPUT_UNKNOWN'
        result['message'] = '输入未通过原门槛；保留未知，等待数据恢复。'
        result['routes'] = None
    result['issues'] = list(dict.fromkeys(issues))
    result['recovery_blocked'] = snapshot.get('recovery_blocked', False)
    return result
