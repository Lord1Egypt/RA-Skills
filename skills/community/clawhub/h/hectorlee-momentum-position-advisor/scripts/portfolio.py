"""
持仓文件管理 V1.0
读取/写入持仓JSON文件，计算盈亏
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime

DEFAULT_PORTFOLIO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'positions.json')


def load_portfolio(filepath: str = None) -> dict:
    """加载持仓文件"""
    path = filepath or DEFAULT_PORTFOLIO_PATH
    if not os.path.exists(path):
        return {'positions': []}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_portfolio(portfolio: dict, filepath: str = None):
    """保存持仓文件"""
    path = filepath or DEFAULT_PORTFOLIO_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)


def get_positions(filepath: str = None) -> List[dict]:
    """获取持仓列表"""
    portfolio = load_portfolio(filepath)
    return portfolio.get('positions', [])


def add_position(code: str, name: str = '', cost: float = 0, 
                 buy_date: str = '', notes: str = '', filepath: str = None):
    """添加持仓"""
    portfolio = load_portfolio(filepath)
    
    # 检查是否已存在
    for pos in portfolio.get('positions', []):
        if pos['code'] == code:
            pos['cost'] = cost
            pos['name'] = name
            pos['notes'] = notes
            save_portfolio(portfolio, filepath)
            return
    
    portfolio.setdefault('positions', []).append({
        'code': code,
        'name': name,
        'cost': cost,
        'buy_date': buy_date,
        'notes': notes,
    })
    save_portfolio(portfolio, filepath)


def remove_position(code: str, filepath: str = None):
    """删除持仓"""
    portfolio = load_portfolio(filepath)
    portfolio['positions'] = [p for p in portfolio.get('positions', []) if p['code'] != code]
    save_portfolio(portfolio, filepath)


def calc_pnl(cost: float, current_price: float) -> float:
    """计算盈亏百分比"""
    if cost <= 0:
        return 0
    return (current_price - cost) / cost * 100
