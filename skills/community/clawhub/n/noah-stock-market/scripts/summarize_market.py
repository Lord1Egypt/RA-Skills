#!/usr/bin/env python3
from typing import Any, Dict, List, Optional


QUOTE_SORT_FIELD_LABELS = {
    'CHANGE_RATE': '涨跌幅',
    'CHANGE_VAL': '涨跌额',
    'CUR_PRICE': '最新价',
    'OPEN_PRICE': '今开',
    'HIGH_PRICE': '最高价',
    'LOW_PRICE': '最低价',
    'LAST_CLOSE': '昨收',
    'VOLUME': '成交量',
    'TURNOVER': '成交额',
    'TURNOVER_RATE': '换手率',
    'AMPLITUDE': '振幅',
    'VOLUME_RATIO': '量比',
    'PE_TTM_RATIO': '市盈率(TTM)',
    'PB_RATIO': '市净率',
    'TOTAL_MARKET_VAL': '总市值',
    'CIRC_MARKET_VAL': '流通市值',
    'lastPrice': '最新价',
    'raisePercent': '涨跌幅',
    'raise': '涨跌额',
    'exchange': '换手率',
    'raiseSpeed': '涨速',
    'mainNetInflow': '主力净流入',
    'totalTradeVol': '成交量',
    'totalTurnover': '成交额',
    'volumeRatio': '量比',
    'entrustRatio': '委比',
    'amplitude': '振幅',
    'highPrice': '最高价',
    'lowPrice': '最低价',
    'openPrice': '今开',
    'preClose': '昨收',
    'peDynamic': '动态市盈率',
    'peRatio': '市盈率TTM',
    'circulationValue': '流通市值',
    'marketValue': '总市值',
    'roe': 'ROE',
    'raisePercentOneYear': '近一年涨幅',
    'raisePercent1m': '近一月涨幅',
    'raisePercentYtd': '年初至今涨幅',
    'assetSize': '资产规模',
    'shareIssued': '已发行份额',
}


MARKET_STATE_MAP = {
    'AUCTION': '盘前竞价',
    'WAITING_OPEN': '等待开盘',
    'MORNING': '早盘交易中',
    'REST': '午间休市',
    'AFTERNOON': '午盘交易中',
    'CLOSED': '已收盘',
    'PRE_MARKET_BEGIN': '美股盘前交易中',
    'PRE_MARKET_END': '美股盘前结束',
    'AFTER_HOURS_BEGIN': '美股盘后交易中',
    'AFTER_HOURS_END': '美股盘后结束',
    'OVERNIGHT': '夜盘交易中',
    'HK_CAS': '港股盘后竞价',
}


def normalize_symbol(code: Optional[str]) -> Optional[str]:
    if not code:
        return code
    if code.startswith('HK-') or code.startswith('US-'):
        return code
    if code.isdigit() and len(code) == 5:
        return f'HK-{code}'
    if code.replace('.', '').replace('-', '').isalnum() and not code.isdigit():
        return f'US-{code.replace("US-", "").replace("US.", "")}' if not code.startswith('US') else code.replace('US.', 'US-')
    return code


def _pct(last_price, prev_close):
    try:
        if prev_close in (None, 0):
            return None
        return (float(last_price) - float(prev_close)) / float(prev_close) * 100
    except Exception:
        return None


def _delta(last_price, prev_close):
    try:
        if last_price is None or prev_close is None:
            return None
        return float(last_price) - float(prev_close)
    except Exception:
        return None


def summarize_snapshot(item: Dict[str, Any]) -> Dict[str, Any]:
    last_price = item.get('last_price')
    prev_close = item.get('prev_close_price')
    pct = _pct(last_price, prev_close)
    delta = _delta(last_price, prev_close)
    return {
        'symbol': normalize_symbol(item.get('code')),
        'name': item.get('name'),
        'last_price': last_price,
        'change_value': round(delta, 2) if delta is not None else None,
        'change_pct': round(pct, 2) if pct is not None else None,
        'open_price': item.get('open_price'),
        'high_price': item.get('high_price'),
        'low_price': item.get('low_price'),
        'volume': item.get('volume'),
        'turnover': item.get('turnover'),
        'update_time': item.get('data_time') or item.get('update_time'),
        'suspension': item.get('suspension'),
    }


def summarize_market_state(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for x in items:
        code = x.get('code')
        market = x.get('market')
        symbol = normalize_symbol(code) if code else market
        state = x.get('market_state')
        out.append({
            'symbol': symbol,
            'name': x.get('stock_name') or x.get('name') or market,
            'market_state': state,
            'market_state_text': MARKET_STATE_MAP.get(state, state),
            'trade_session': x.get('trade_session'),
        })
    return out


def summarize_kline(items: List[Dict[str, Any]], detail: bool = False) -> Dict[str, Any]:
    if not items:
        return {'count': 0, 'latest': None, 'highest': None, 'lowest': None, 'items': []}
    normalized_items = []
    closes = []
    for x in items:
        row = dict(x)
        row['code'] = normalize_symbol(row.get('code') or row.get('uniqueCode'))
        row['time_key'] = row.get('time_key') or row.get('tradeDateTime')
        row['open'] = row.get('open', row.get('openPrice'))
        row['high'] = row.get('high', row.get('highPrice'))
        row['low'] = row.get('low', row.get('lowPrice'))
        row['close'] = row.get('close', row.get('closePrice'))
        row['volume'] = row.get('volume', row.get('tradeVol'))
        row['turnover'] = row.get('turnover', row.get('turnover'))
        closes.append(row.get('close')) if row.get('close') is not None else None
        normalized_items.append(row)
    latest = normalized_items[-1]
    result = {
        'count': len(normalized_items),
        'latest': latest,
        'highest': max(closes) if closes else None,
        'lowest': min(closes) if closes else None,
        'symbol': latest.get('code'),
        'name': latest.get('name'),
    }
    result['items'] = normalized_items if detail else []
    return result


def summarize_intraday(items: List[Dict[str, Any]], detail: bool = False) -> Dict[str, Any]:
    if not items:
        return {'count': 0, 'latest': None, 'items': []}
    normalized_items = []
    for x in items:
        row = dict(x)
        row['code'] = normalize_symbol(row.get('code'))
        normalized_items.append(row)
    latest = normalized_items[-1]
    result = {
        'count': len(normalized_items),
        'latest': latest,
        'avg_price': latest.get('avg_price'),
        'last_close': latest.get('last_close'),
        'volume': latest.get('volume'),
        'turnover': latest.get('turnover'),
    }
    result['items'] = normalized_items if detail else []
    return result


def summarize_orderbook(item: Dict[str, Any]) -> Dict[str, Any]:
    bid = (item.get('bid') or [])
    ask = (item.get('ask') or [])
    best_bid = bid[0] if bid else None
    best_ask = ask[0] if ask else None
    return {
        'symbol': normalize_symbol(item.get('code')),
        'name': item.get('name'),
        'best_bid': best_bid,
        'best_ask': best_ask,
        'bid_levels': len(bid),
        'ask_levels': len(ask),
        'recv_time_bid': item.get('svr_recv_time_bid'),
        'recv_time_ask': item.get('svr_recv_time_ask'),
    }


def summarize_ticker(items: List[Dict[str, Any]], detail: bool = False) -> Dict[str, Any]:
    if not items:
        return {'count': 0, 'latest': None, 'items': []}
    normalized = []
    for x in items:
        row = dict(x)
        row['code'] = normalize_symbol(row.get('code'))
        normalized.append(row)
    latest = normalized[0]
    result = {'count': len(normalized), 'latest': latest}
    result['items'] = normalized if detail else normalized[:10]
    return result


def summarize_broker_queue(item: Dict[str, Any]) -> Dict[str, Any]:
    bid = item.get('bid_frame_table') or []
    ask = item.get('ask_frame_table') or []
    symbol = None
    name = None
    sample = bid[0] if bid else (ask[0] if ask else {})
    if sample:
        symbol = normalize_symbol(sample.get('code'))
        name = sample.get('name')
    return {
        'symbol': symbol,
        'name': name,
        'bid_count': len(bid),
        'ask_count': len(ask),
        'bid_items': bid[:10],
        'ask_items': ask[:10],
    }


def summarize_trading_days(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    trading = [x for x in items if x.get('is_trading_day')]
    closed = [x for x in items if not x.get('is_trading_day')]
    return {
        'count': len(items),
        'trading_days': len(trading),
        'non_trading_days': len(closed),
        'first': items[0] if items else None,
        'last': items[-1] if items else None,
        'items': items[:31],
    }


def summarize_us_analysis(item: Dict[str, Any]) -> Dict[str, Any]:
    target = item.get('targetPricePrediction') or {}
    rating = item.get('recommendedByUSStockAnalysts') or {}
    return {
        'target_price': {
            'high': target.get('high'),
            'mean': target.get('mean'),
            'low': target.get('low'),
            'last_price': target.get('lastPrice'),
            'num_estimates': target.get('numOfEstimates'),
        },
        'rating': {
            'average_rating': rating.get('averageRating'),
            'average_rating_data': rating.get('averageRatingData'),
            'analyst_count': rating.get('numberOfAnalystsOneWeekAgo'),
            'one_week_ago': rating.get('oneWeekAgo') or {},
            'one_month_ago': rating.get('oneMonthAgo') or {},
            'two_month_ago': rating.get('twoMonthAgo') or {},
            'three_month_ago': rating.get('threeMonthAgo') or {},
        },
    }


def summarize_capital_flow(items: List[Dict[str, Any]], detail: bool = False) -> Dict[str, Any]:
    if not items:
        return {'count': 0, 'latest': None, 'items': []}

    def _is_zero_row(x: Dict[str, Any]) -> bool:
        vals = [x.get('in_flow'), x.get('super_in_flow'), x.get('big_in_flow'), x.get('mid_in_flow'), x.get('sml_in_flow')]
        cleaned = [0 if v is None else float(v) for v in vals]
        return all(v == 0 for v in cleaned)

    trimmed = list(items)
    while trimmed and _is_zero_row(trimmed[-1]):
        trimmed.pop()

    effective = trimmed if trimmed else items
    latest = effective[-1]
    result = {
        'count': len(effective),
        'raw_count': len(items),
        'latest': {
            'in_flow': latest.get('in_flow'),
            'main_in_flow': latest.get('main_in_flow'),
            'super_in_flow': latest.get('super_in_flow'),
            'big_in_flow': latest.get('big_in_flow'),
            'mid_in_flow': latest.get('mid_in_flow'),
            'sml_in_flow': latest.get('sml_in_flow'),
            'time': latest.get('capital_flow_item_time'),
            'last_valid_time': latest.get('last_valid_time'),
        },
        'has_trimmed_zero_tail': len(effective) != len(items),
    }
    if detail:
        result['items'] = [
            {
                'in_flow': x.get('in_flow'),
                'super_in_flow': x.get('super_in_flow'),
                'big_in_flow': x.get('big_in_flow'),
                'mid_in_flow': x.get('mid_in_flow'),
                'sml_in_flow': x.get('sml_in_flow'),
                'time': x.get('capital_flow_item_time'),
                'last_valid_time': x.get('last_valid_time'),
            }
            for x in effective
        ]
    else:
        result['items'] = []
    return result


def summarize_basicinfo(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for x in items:
        out.append({
            'symbol': normalize_symbol(x.get('code')),
            'name': x.get('name'),
            'lot_size': x.get('lot_size'),
            'listing_date': x.get('listing_date'),
            'stock_id': x.get('stock_id'),
            'delisting': x.get('delisting'),
        })
    return out


def summarize_plate_list(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            'code': x.get('code'),
            'plate_name': x.get('plate_name'),
            'plate_id': x.get('plate_id'),
        }
        for x in items
    ]


def summarize_plate_stock(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        'count': len(items),
        'items': [
            {
                'symbol': normalize_symbol(x.get('code')),
                'stock_name': x.get('stock_name'),
                'lot_size': x.get('lot_size'),
                'list_time': x.get('list_time'),
            }
            for x in items[:10]
        ],
    }


def summarize_option_expirations(items: List[Dict[str, Any]]) -> List[str]:
    return [x.get('expiration_date') for x in items if x.get('expiration_date')]


def summarize_option_chain(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        'count': len(items),
        'items': [
            {
                'code': x.get('code'),
                'name': x.get('name'),
                'stock_owner': normalize_symbol(x.get('stock_owner')),
                'strike_time': x.get('strike_time'),
                'strike_price': x.get('strike_price'),
                'option_type': x.get('option_type'),
            }
            for x in items[:10]
        ],
    }


def summarize_rank(items: List[Dict[str, Any]], rank_field: Optional[str] = None, ascend: Optional[bool] = None) -> Dict[str, Any]:
    normalized = []
    for x in items:
        symbol = normalize_symbol(x.get('code') or x.get('stock_code') or x.get('uniqueCode'))
        normalized.append({
            'symbol': symbol,
            'name': x.get('name') or x.get('stock_name') or x.get('targetName'),
            'last_price': x.get('last_price') or x.get('cur_price') or x.get('price') or x.get('lastPrice'),
            'change_pct': x.get('change_rate') or x.get('change_pct') or x.get('raisePercent'),
            'change_value': x.get('change_val') or x.get('change_value') or x.get('raise'),
            'volume': x.get('volume') or x.get('totalTradeVol'),
            'turnover': x.get('turnover') or x.get('totalTurnover'),
            'raw': x,
        })
    return {
        'count': len(normalized),
        'rank_field': rank_field,
        'rank_field_label': QUOTE_SORT_FIELD_LABELS.get(rank_field or '', rank_field),
        'ascend': ascend,
        'items': normalized[:20],
    }


def summarize_ipo_list(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    normalized = []
    for x in items:
        normalized.append({
            'symbol': normalize_symbol(x.get('code') or x.get('stock_code')),
            'name': x.get('name') or x.get('stock_name'),
            'market': x.get('market'),
            'listing_date': x.get('listing_date') or x.get('list_time') or x.get('ipo_date'),
            'issue_price': x.get('issue_price') or x.get('price'),
            'lot_size': x.get('lot_size'),
            'raw': x,
        })
    return {
        'count': len(normalized),
        'items': normalized[:20],
    }


def summarize_financial(summary: Dict[str, Any], market: str) -> Dict[str, Any]:
    if market == 'HK':
        indicators = (summary or {}).get('hkStockFinancialIndicatorResp') or []
        latest = indicators[0] if indicators else {}
        return {
            'market': 'HK',
            'latest': latest,
            'eps': latest.get('basicEps'),
            'bps': latest.get('netAssetPs'),
            'roe': latest.get('roeWeighted'),
            'gross_margin': latest.get('grossIncomeRatio'),
            'net_margin': latest.get('netProfitRatio'),
            'debt_ratio': latest.get('debtAssetsRatio'),
            'revenue_growth_yoy': latest.get('operatingRevenueGr1y'),
            'net_profit_growth_yoy': latest.get('netProfitGr1y'),
            'report_end': latest.get('endDate') or latest.get('fiscalYear'),
            'raw': summary,
        }
    main = (summary or {}).get('usMainFinancialInfoResp') or {}
    return {
        'market': 'US',
        'latest': main,
        'eps': main.get('epsBasic') or main.get('eps'),
        'bps': main.get('netAssetValuePerShare'),
        'operating_cashflow_per_share': main.get('netOperatingCashFlowPerShare'),
        'operating_income_per_share': main.get('operatingIncomePerShare'),
        'dividend_per_share': main.get('dividendPerShare'),
        'yoy_growth_in_basic_eps': main.get('yoyGrowthInBasicEps'),
        'report_end': main.get('endDate'),
        'currency': main.get('reportingCurrency') or main.get('priceCurrency'),
        'raw': summary,
    }


def summarize_shareholder_inc_red_hold(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    normalized = []
    for x in items:
        normalized.append({
            'holder_name': x.get('name'),
            'event_date': x.get('transDate'),
            'shares_traded': x.get('adjSharesTraded'),
            'changed_amount': x.get('changedAmount'),
            'hold_before': x.get('holdSumBefEvent'),
            'hold_after': x.get('holdSumAfEvent'),
            'quantity_ratio': x.get('variableQuantityRatio'),
            'symbol': normalize_symbol(x.get('uniqueCode')),
            'sec_name': x.get('secName'),
            'exchange_code': x.get('exgCode'),
            'raw': x,
        })
    return {
        'count': len(normalized),
        'items': normalized[:20],
    }



def summarize_wealth_balance_list(data: Any) -> Dict[str, Any]:
    x = data if isinstance(data, dict) else {}
    items = x.get('cashBalanceList') or []
    normalized = []
    for item in items:
        normalized.append({
            'currency': item.get('currency'),
            'cash_balance_amount': item.get('cashBalanceAmount'),
            'balance_amount': item.get('balanceAmount'),
            'cash_frozen_amount': item.get('cashFrozenAmount'),
            'last_modified_date': item.get('lastModifiedDate'),
            'raw': item,
        })
    return {
        'group_no': x.get('groupNo'),
        'total_cash_balance_amount': x.get('totalCrashBalanceAmount'),
        'count': len(normalized),
        'items': normalized[:20],
        'raw': x,
    }



def summarize_wealth_cash_total_asset(data: Any) -> Dict[str, Any]:
    x = data if isinstance(data, dict) else {}
    profit_items = x.get('profit') or []
    normalized = []
    for item in profit_items:
        normalized.append({
            'currency': item.get('currency'),
            'total_asset': item.get('totalAsset'),
            'day_profit': item.get('dayProfit'),
            'total_asset_profit': item.get('totalAssetProfit'),
            'total_confirming_amount': item.get('totalConfirmingAmount'),
            'total_freeze_amount': item.get('totalFreezeAmount'),
            'total_transaction_count': item.get('totalTransactionCount'),
            'raw': item,
        })
    return {'count': len(normalized), 'items': normalized[:20], 'raw': x}


def summarize_wealth_fixed_income(data: Any) -> Dict[str, Any]:
    x = data if isinstance(data, dict) else {}
    total = x.get('totalDto') or {}
    groups = x.get('productTypeCurrencyList') or []
    return {
        'currency': total.get('currency'),
        'total_asset': total.get('totalAsset'),
        'total_confirming_amount': total.get('totalConfirmingAmount'),
        'total_holding_profit': total.get('totalHoldingProfit'),
        'total_profit': total.get('totalProfit'),
        'total_transaction_count': total.get('totalTransactionCount'),
        'group_count': len(groups),
        'groups': groups[:10],
        'raw': x,
    }


def summarize_wealth_private_contract_asset_list(data: Any) -> Dict[str, Any]:
    x = data if isinstance(data, dict) else {}
    contracts = ((x.get('contractAssetItemList') or {}).get('r')) or []
    normalized = []
    for item in contracts:
        normalized.append({
            'contract_code': item.get('contractCode'),
            'product_name': item.get('contractNameCn') or item.get('contractNameEn'),
            'asset_class_desc': item.get('assetClassDesc') or item.get('assetClassDescEn'),
            'currency': item.get('currency'),
            'asset': item.get('asset'),
            'confirmed_asset': item.get('confirmedAsset'),
            'input_amount': item.get('inputAmount'),
            'output_amount': item.get('outputAmount'),
            'invested_amount': item.get('investedAmount'),
            'fee': item.get('fee'),
            'float_profit': item.get('floatProfit'),
            'ineffective_amount': item.get('ineffectiveAmount'),
            'is_close': item.get('isClose'),
            'raw': item,
        })
    return {
        'currency': x.get('currency'),
        'total_asset': x.get('totalAsset'),
        'total_confirmed_asset': x.get('totalConfirmedAsset'),
        'total_input_amount': x.get('totalInputAmount'),
        'total_output_amount': x.get('totalOutputAmount'),
        'total_float_profit': x.get('totalFloatProfit'),
        'total_ineffective_amount': x.get('totalIneffectiveAmount'),
        'total_contract_count': x.get('totalContractCount'),
        'count': len(normalized),
        'items': normalized[:20],
        'raw': x,
    }


def summarize_wealth_total_asset(data: Any) -> Dict[str, Any]:
    x = data if isinstance(data, dict) else {}
    total = x.get('totalAsset') or {}
    hold = x.get('holdShareList') or {}
    return {
        'currency': hold.get('currency') or total.get('currency'),
        'total_asset': total.get('totalAsset'),
        'cash_asset': total.get('cashAsset'),
        'fund_asset': total.get('fundAsset'),
        'private_asset': total.get('privateAsset'),
        'bank_deposit_asset': total.get('bankDepositAsset'),
        'note_asset': total.get('noteAsset'),
        'hold_total_holding_amount': hold.get('totalHoldingAmount'),
        'hold_total_holding_profit': hold.get('totalHoldingProfit'),
        'hold_total_confirming_amount': hold.get('totalConfirmingAmount'),
        'hold_total_freeze_amount': hold.get('totalFreezeAmount'),
        'hold_total_invested_amount': hold.get('totalInvestedAmount'),
        'raw': x,
    }


