#!/usr/bin/env python3
"""
Signal Filter - Enhanced screening to reduce false signals
"""

def filter_signal(symbol, analysis):
    """
    Filter signals based on quality criteria
    
    Returns: (passed: bool, reason: str)
    """
    
    # 1. Reject whale-manipulated tokens
    WHALE_TOKENS = ['SHIB', 'DOGE', 'PEPE', 'WIF', 'FLOKI', 'BONK', 'SATS', 'RATS', 'MOTHER', 'AI', 'NEIRO']
    symbol_clean = symbol.replace('USDT', '').replace('BTC', '')
    
    if symbol_clean in WHALE_TOKENS:
        return False, f"REJECT: {symbol} is whale-manipulated token"
    
    # 2. Reject if volume too low
    vol_ratio = analysis.get('vol_ratio', 0)
    if vol_ratio < 2:
        return False, f"REJECT: Volume too low ({vol_ratio}x)"
    
    # 3. Reject if price change < 2%
    price_change = abs(analysis.get('price_change', 0))
    if price_change < 2:
        return False, f"REJECT: Price change too small ({price_change}%)"
    
    # 4. Reject if RSI in extreme zone only (no confirmation)
    rsi = analysis.get('rsi', 50)
    if rsi < 20 or rsi > 80:
        if analysis.get('runner_score', 0) < 4:
            return False, f"REJECT: RSI extreme without confirmation ({rsi})"
    
    # 5. Require minimum score
    score = analysis.get('runner_score', 0)
    if score < 3:
        return False, f"REJECT: Score too low ({score})"
    
    # 6. Require momentum alignment
    change_1h = analysis.get('change_1h', 0)
    
    if change_1h * price_change < 0 and abs(change_1h) > abs(price_change) * 0.3:
        return False, f"REJECT: 1h reversal ({change_1h}%) vs 4h ({price_change}%)"
    
    # 7. Check SL cooldown (30 minutes after SL hit)
    try:
        import time
        now = time.time()
        cooldown = 30 * 60  # 30 minutes
        
        try:
            with open('.recently_closed') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 2 and parts[0] == symbol_clean + 'USDT':
                        ts = int(parts[1])
                        if now - ts < cooldown:
                            age = (cooldown - (now - ts)) / 60
                            return False, f"REJECT: SL cooldown ({age:.0f}m left)"
        except:
            pass
    except:
        pass
    
    return True, "PASSED"

def get_filter_stats():
    """Return filter statistics"""
    return {
        'whale_tokens': 12,
        'min_volume_ratio': 2.0,
        'min_price_change': 2.0,
        'min_score': 3,
        'cooldown_minutes': 30
    }
