"""Display-only input health; never changes frozen trading decisions."""


def input_health(now, market, ptb, price, sigma, clock, books, signal):
    reasons = []
    current = bool(market and market['start'] * 1000 <= now < market['end'] * 1000)
    if not current:
        reasons.append('当前 15 分钟市场未取得或已过期')
    if not clock or clock.get('age_ms', 120001) > 120000:
        reasons.append('校时数据超过 120 秒未更新')
    elif clock.get('residual_bound_ms', float('inf')) >= 50:
        reasons.append('校时误差未满足原 50 ms 门槛')
    if not price or not 0 <= now - price['source_ms'] <= 2000:
        reasons.append('币安逐笔缺失或超过原 2 秒门槛')
    if not current or not ptb or ptb['start'] != market['start']:
        reasons.append('本窗口官方待击败价缺失')
    if sigma is None:
        reasons.append('连续分钟波动率未就绪')
    if set(books) != {'Up', 'Down'} or not all(
            b.valid and b.bids and b.asks and 0 <= now - b.source_ms <= 2000
            for b in books.values()):
        reasons.append('双边盘口缺失、不同步或超过原 2 秒门槛')
    signal_current = bool(current and signal and signal['start'] == market['start'])
    if not signal_current:
        reasons.append('本窗口锁定 K14 尚未取得')
    return {'status': 'DEGRADED' if reasons else 'READY', 'reasons': reasons,
            'current_market': current, 'current_signal': signal_current,
            'meaning': '输入健康检查；READY 不代表通过挂价/风控，更不代表成交'}
