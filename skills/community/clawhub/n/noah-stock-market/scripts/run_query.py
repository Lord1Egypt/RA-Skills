#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict

from quote_client import NoahQuoteClient
from normalize_symbol import normalize_symbol
from protocol_enums import ensure_enum, ensure_enum_varname, normalize_sort_dir
from summarize_market import (
    summarize_basicinfo,
    summarize_broker_queue,
    summarize_capital_flow,
    summarize_financial,
    summarize_intraday,
    summarize_ipo_list,
    summarize_kline,
    summarize_market_state,
    summarize_rank,
    summarize_shareholder_inc_red_hold,
    summarize_snapshot,
    summarize_ticker,
    summarize_trading_days,
    summarize_us_analysis,
    summarize_wealth_balance_list,
    summarize_wealth_cash_total_asset,
    summarize_wealth_fixed_income,
    summarize_wealth_private_contract_asset_list,
    summarize_wealth_total_asset,
)
from format_market_text import (
    format_basicinfo,
    format_broker_queue,
    format_capital_flow,
    format_financial,
    format_intraday,
    format_ipo_list,
    format_kline,
    format_market_state,
    format_rank,
    format_shareholder_inc_red_hold,
    format_snapshot,
    format_ticker,
    format_trading_days,
    format_us_analysis,
    format_wealth_balance_list,
    format_wealth_cash_total_asset,
    format_wealth_fixed_income,
    format_wealth_private_contract_asset_list,
    format_wealth_total_asset,
)


def build_params(intent: str, symbol: str, **kwargs) -> Dict[str, Any]:
    if intent == 'snapshot':
        return {'code_list': symbol}
    if intent == 'market_state':
        if kwargs.get('global_state') in ('1', 'true', 'yes'):
            return {}
        return {'code_list': symbol}
    if intent == 'global_state':
        return {}
    if intent == 'intraday':
        return {'code': symbol}
    if intent == 'ticker':
        return {'code': symbol, 'num': int(kwargs.get('num', 10))}
    if intent == 'broker_queue':
        return {'code': symbol}
    if intent == 'kline':
        ktype = ensure_enum('KLType', kwargs.get('ktype', 'K_DAY'))
        autype = ensure_enum('AuType', kwargs.get('autype', 'NONE'))
        if kwargs.get('from') and kwargs.get('to'):
            return {
                'code': symbol,
                'from': kwargs.get('from'),
                'to': kwargs.get('to'),
                'ktype': ktype,
                'autype': autype,
            }
        return {
            'code': symbol,
            'num': int(kwargs.get('num', 5)),
            'ktype': ktype,
            'autype': autype,
        }
    if intent == 'capital_flow':
        return {'stock_code': symbol, 'num': int(kwargs.get('num', 5))}
    if intent == 'basicinfo':
        return {'market': symbol.split('-')[0], 'code_list': symbol}
    if intent == 'trading_days':
        return {
            'market': kwargs.get('market', symbol.split('-')[0] if '-' in symbol else symbol),
            'start': kwargs.get('start'),
            'end': kwargs.get('end'),
        }
    if intent == 'us_analysis':
        return {'stock_code': symbol}
    if intent == 'rank':
        ascend = str(kwargs.get('ascend', 'false')).lower() in ('1', 'true', 'yes', 'y')
        return {
            'market_codes': ensure_enum('Markets', kwargs.get('market_codes') or kwargs.get('market') or symbol),
            'rank_field': ensure_enum('QuoteSortField', kwargs.get('rank_field', 'raisePercent')),
            'ascend': ascend,
            'page': int(kwargs.get('page', 1)),
            'page_size': int(kwargs.get('page_size', 10)),
        }
    if intent == 'ipo_list':
        return {
            'market': ensure_enum('Market', kwargs.get('market') or symbol),
        }
    if intent == 'financial_hk':
        return {
            'stock_code': symbol,
            'type_code': ensure_enum_varname('DateTypeConvertUtil', kwargs.get('type_code', 'DT4')),
            'year': int(kwargs.get('year')),
        }
    if intent == 'financial_us':
        return {
            'stock_code': symbol,
            'type_code': ensure_enum_varname('DateTypeConvertUtil', kwargs.get('type_code', 'DT4')),
            'year': int(kwargs.get('year')),
        }
    if intent == 'shareholder_inc_red_hold':
        return {
            'current_page': int(kwargs.get('current_page', kwargs.get('page', 1))),
            'page_size': int(kwargs.get('page_size', 10)),
            'market': ensure_enum('Markets', kwargs.get('market') or symbol),
            'shareholder': ensure_enum_varname('ShareholderRedHoldEnum', kwargs.get('shareholder', 'EVENT_DATE')),
            'order_code': ensure_enum('SortDir', kwargs.get('order_code', 'DESCEND')),
        }
    if intent == 'shareholder_inc_red_hold_by_ucode':
        return {
            'current_page': int(kwargs.get('current_page', kwargs.get('page', 1))),
            'page_size': int(kwargs.get('page_size', 10)),
            'stock_code': symbol,
            'shareholder': ensure_enum_varname('ShareholderRedHoldEnum', kwargs.get('shareholder', 'EVENT_DATE')),
            'order_code': ensure_enum('SortDir', kwargs.get('order_code', 'DESCEND')),
        }
    if intent == 'wealth_balance_list':
        return {}
    if intent == 'wealth_cash_total_asset':
        return {}
    if intent == 'wealth_fixed_income':
        payload = {}
        if kwargs.get('productStatus') or kwargs.get('product_status'):
            payload['productStatus'] = kwargs.get('productStatus') or kwargs.get('product_status')
        if kwargs.get('productTypeList') or kwargs.get('product_type_list'):
            raw = kwargs.get('productTypeList') or kwargs.get('product_type_list')
            payload['productTypeList'] = [x.strip() for x in raw.split(',') if x.strip()]
        if kwargs.get('toCcy') or kwargs.get('to_ccy'):
            payload['toCcy'] = kwargs.get('toCcy') or kwargs.get('to_ccy')
        for k in ['showCcyListItem','showCcyTotalAsset','showTotalAsset','showTotalTransactionCount']:
            raw = kwargs.get(k) or kwargs.get(k.lower())
            if raw is not None:
                payload[k] = str(raw).lower() in ('1','true','yes','y')
        return payload
    if intent == 'wealth_private_contract_asset_list':
        payload = {
            'toCurrency': kwargs.get('toCurrency') or kwargs.get('to_currency') or 'USD',
            'queryType': kwargs.get('queryType') or kwargs.get('query_type'),
            'isPaging': str(kwargs.get('isPaging', kwargs.get('is_paging', 'true'))).lower() in ('1','true','yes','y'),
        }
        raw_status = kwargs.get('positionStatus') or kwargs.get('position_status')
        if raw_status:
            payload['positionStatus'] = [x.strip() for x in raw_status.split(',') if x.strip()]
        return payload
    if intent == 'wealth_total_asset':
        return {'toCurrency': kwargs.get('toCurrency') or kwargs.get('to_currency') or 'USD'}
    raise ValueError(f'unsupported intent: {intent}')


def run(intent: str, raw_symbol: str, **kwargs) -> Dict[str, Any]:
    if raw_symbol in {'HK', 'US', 'CN', 'ALL'}:
        symbol = raw_symbol
    else:
        symbol = normalize_symbol(raw_symbol) or raw_symbol
    client = NoahQuoteClient()
    supported = {'snapshot', 'market_state', 'global_state', 'intraday', 'ticker', 'broker_queue', 'kline', 'capital_flow', 'basicinfo', 'trading_days', 'us_analysis', 'rank', 'ipo_list', 'financial_hk', 'financial_us', 'shareholder_inc_red_hold', 'shareholder_inc_red_hold_by_ucode', 'wealth_balance_list', 'wealth_cash_total_asset', 'wealth_fixed_income', 'wealth_private_contract_asset_list', 'wealth_total_asset'}
    if intent not in supported:
        return {'ok': False, 'message': f'unsupported intent: {intent}', 'symbol': symbol}

    path_map = {
        'snapshot': '/quotes/get_market_snapshot',
        'market_state': '/infos/get_market_state',
        'global_state': '/quote/get_global_state',
        'intraday': '/quotes/get_rt_data',
        'ticker': '/quotes/get_rt_ticker',
        'broker_queue': '/quotes/get_broker_queue',
        'kline': '/quotes/get_cur_kline_date' if kwargs.get('from') and kwargs.get('to') else '/quotes/get_cur_kline',
        'capital_flow': '/infos/get_capital_flow',
        'basicinfo': '/quote/get_stock_basicinfo',
        'trading_days': '/quote/request_trading_days',
        'us_analysis': '/infos/get_us_analysis',
        'rank': '/rank/get_stock_rank',
        'ipo_list': '/quote/get_ipo_list',
        'financial_hk': '/infos/get_finance_hk_infos',
        'financial_us': '/infos/get_finance_us_infos',
        'shareholder_inc_red_hold': '/infos/shareholder_inc_red_hold',
        'shareholder_inc_red_hold_by_ucode': '/infos/shareholder_inc_red_hold_by_ucode',
        'wealth_balance_list': '/wealth/balance_list',
        'wealth_cash_total_asset': '/wealth/cash_total_asset',
        'wealth_fixed_income': '/wealth/fixed_income',
        'wealth_private_contract_asset_list': '/wealth/query_private_contract_asset_list',
        'wealth_total_asset': '/wealth/total_asset',
    }

    params = build_params(intent, symbol, **kwargs)
    if intent in {'wealth_fixed_income', 'wealth_private_contract_asset_list'}:
        result = client.post(path_map[intent], params)
    else:
        result = client.get(path_map[intent], params)
    out = {
        'ok': result['ok'],
        'http_status': result['http_status'],
        'message': result.get('message'),
        'symbol': symbol,
        'intent': intent,
        'params': params,
    }

    if not result['ok']:
        msg = result.get('message') or '未知错误'
        status = result.get('http_status')
        if status == 404:
            human = '当前环境下，该标的或该查询参数暂不可用（接口返回 404）。'
        elif status in (401, 403):
            human = '鉴权失败或权限不足，请检查本地 token 配置。'
        elif msg == '生产环境暂不支持':
            human = '这个能力接口已定义，但当前环境暂不支持。'
        else:
            human = f'查询失败：{msg}'
        out['text'] = human
        out['error_hint'] = human
        return out

    data = result.get('data')
    if intent == 'snapshot' and isinstance(data, list) and data:
        summary = summarize_snapshot(data[0])
        out['summary'] = summary
        out['text'] = format_snapshot(summary)
    elif intent in ('market_state', 'global_state') and isinstance(data, list):
        summary = summarize_market_state(data)
        out['summary'] = summary
        out['text'] = format_market_state(summary)
    elif intent == 'intraday' and isinstance(data, list):
        detail = str(kwargs.get('detail', 'false')).lower() in ('1', 'true', 'yes', 'y')
        summary = summarize_intraday(data, detail=detail)
        out['summary'] = summary
        out['text'] = format_intraday(summary, detail=detail)
    elif intent == 'ticker' and isinstance(data, list):
        detail = str(kwargs.get('detail', 'false')).lower() in ('1', 'true', 'yes', 'y')
        summary = summarize_ticker(data, detail=detail)
        out['summary'] = summary
        out['text'] = format_ticker(summary, detail=detail)
    elif intent == 'broker_queue' and isinstance(data, dict):
        summary = summarize_broker_queue(data)
        out['summary'] = summary
        out['text'] = format_broker_queue(summary)
    elif intent == 'kline' and isinstance(data, list):
        detail = str(kwargs.get('detail', 'false')).lower() in ('1', 'true', 'yes', 'y')
        summary = summarize_kline(data, detail=detail)
        out['summary'] = summary
        out['text'] = format_kline(summary, detail=detail)
    elif intent == 'capital_flow' and isinstance(data, list):
        detail = str(kwargs.get('detail', 'false')).lower() in ('1', 'true', 'yes', 'y')
        summary = summarize_capital_flow(data, detail=detail)
        out['summary'] = summary
        out['text'] = format_capital_flow(summary, detail=detail)
    elif intent == 'basicinfo' and isinstance(data, list):
        summary = summarize_basicinfo(data)
        out['summary'] = summary
        out['text'] = format_basicinfo(summary)
    elif intent == 'trading_days' and isinstance(data, list):
        summary = summarize_trading_days(data)
        out['summary'] = summary
        out['text'] = format_trading_days(summary)
    elif intent == 'us_analysis' and isinstance(data, dict):
        summary = summarize_us_analysis(data)
        out['summary'] = summary
        out['text'] = format_us_analysis(summary)
    elif intent == 'rank' and isinstance(data, list):
        summary = summarize_rank(data, rank_field=params.get('rank_field'), ascend=params.get('ascend'))
        out['summary'] = summary
        out['text'] = format_rank(summary)
    elif intent == 'ipo_list' and isinstance(data, list):
        summary = summarize_ipo_list(data)
        out['summary'] = summary
        out['text'] = format_ipo_list(summary)
    elif intent == 'financial_hk' and isinstance(data, dict):
        summary = summarize_financial(data, market='HK')
        out['summary'] = summary
        out['text'] = format_financial(summary)
    elif intent == 'financial_us' and isinstance(data, dict):
        summary = summarize_financial(data, market='US')
        out['summary'] = summary
        out['text'] = format_financial(summary)
    elif intent in ('shareholder_inc_red_hold', 'shareholder_inc_red_hold_by_ucode') and isinstance(data, list):
        summary = summarize_shareholder_inc_red_hold(data)
        out['summary'] = summary
        out['text'] = format_shareholder_inc_red_hold(summary)
    elif intent == 'wealth_balance_list':
        summary = summarize_wealth_balance_list(data)
        out['summary'] = summary
        out['text'] = format_wealth_balance_list(summary)
    elif intent == 'wealth_cash_total_asset':
        summary = summarize_wealth_cash_total_asset(data)
        out['summary'] = summary
        out['text'] = format_wealth_cash_total_asset(summary)
    elif intent == 'wealth_fixed_income':
        summary = summarize_wealth_fixed_income(data)
        out['summary'] = summary
        out['text'] = format_wealth_fixed_income(summary)
    elif intent == 'wealth_private_contract_asset_list':
        summary = summarize_wealth_private_contract_asset_list(data)
        out['summary'] = summary
        out['text'] = format_wealth_private_contract_asset_list(summary)
    elif intent == 'wealth_total_asset':
        summary = summarize_wealth_total_asset(data)
        out['summary'] = summary
        out['text'] = format_wealth_total_asset(summary)
    else:
        out['text'] = '查询成功，但当前没有可展示的数据。'
    return out


def parse_kwargs(argv) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {}
    for item in argv:
        if '=' in item:
            k, v = item.split('=', 1)
            kwargs[k] = v
    return kwargs


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: run_query.py <intent> <symbol> [key=value ...]', file=sys.stderr)
        sys.exit(2)
    kwargs = parse_kwargs(sys.argv[3:])
    result = run(sys.argv[1], sys.argv[2], **kwargs)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
