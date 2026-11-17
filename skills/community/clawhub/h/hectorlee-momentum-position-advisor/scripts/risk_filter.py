"""
风险前置过滤 V1.0
ST/退市/一字板/连板检查
标记风险但不中断评估
"""

from typing import Dict, List, Optional

def check_st(name: str) -> dict:
    """ST/*ST检查"""
    is_st = 'ST' in name.upper()
    return {
        'flag': 'ST',
        'triggered': is_st,
        'level': 'critical' if is_st else 'none',
        'detail': f'{name} 含ST标记' if is_st else ''
    }

def check_delist_risk(name: str, kline: List[dict]) -> dict:
    """退市风险检查（简化版：名称 + K线异常）"""
    flags = []
    if any(kw in name for kw in ['退', '已退']):
        flags.append('名称含退市标记')
    
    # 连续多日无交易
    if kline and len(kline) < 15:
        flags.append(f'K线仅{len(kline)}根，疑似新上市或停牌')
    
    return {
        'flag': '退市风险',
        'triggered': len(flags) > 0,
        'level': 'critical' if len(flags) > 0 else 'none',
        'detail': '; '.join(flags) if flags else ''
    }

def check_one_word_board(kline: List[dict], params: dict = None) -> dict:
    """一字板检查：放量日 high==low 且涨停"""
    p = params or {}
    
    for i in range(max(0, len(kline)-20), len(kline)):
        k = kline[i]
        if k['high'] == k['low']:
            if i > 0:
                prev = kline[i-1]
                chg = (k['close'] - prev['close']) / prev['close'] * 100
                if chg > 9:
                    return {
                        'flag': '一字板',
                        'triggered': True,
                        'level': 'high',
                        'detail': f'{k["date"]} 一字涨停，无法买入'
                    }
    
    return {'flag': '一字板', 'triggered': False, 'level': 'none', 'detail': ''}

def check_consecutive_limit(kline: List[dict], params: dict = None) -> dict:
    """连板股检查：放量日前连续≥2日涨停"""
    p = params or {}
    
    for i in range(max(0, len(kline)-20), len(kline)-1):
        # 检查是否连续2日涨停
        if i < 1:
            continue
        chg1 = (kline[i]['close'] - kline[i-1]['close']) / kline[i-1]['close'] * 100
        chg2 = (kline[i-1]['close'] - kline[i-2]['close']) / kline[i-2]['close'] * 100 if i >= 2 else 0
        if chg1 > 9.5 and chg2 > 9.5:
            return {
                'flag': '连板股',
                'triggered': True,
                'level': 'high',
                'detail': f'{kline[i-1]["date"]}~{kline[i]["date"]} 连续涨停，T+1无法参与'
            }
    
    return {'flag': '连板股', 'triggered': False, 'level': 'none', 'detail': ''}

def run_risk_checks(name: str, kline: List[dict], turnover: float = None, params: dict = None) -> dict:
    """
    运行所有风险检查，返回风险报告。
    不中断评估，仅标记。
    """
    checks = [
        check_st(name),
        check_delist_risk(name, kline),
        check_one_word_board(kline, params),
        check_consecutive_limit(kline, params),
    ]
    
    triggered = [c for c in checks if c['triggered']]
    critical = [c for c in triggered if c['level'] == 'critical']
    
    return {
        'all_checks': checks,
        'triggered': triggered,
        'has_critical': len(critical) > 0,
        'risk_level': 'critical' if critical else ('high' if triggered else 'low'),
    }
