#!/usr/bin/env python3
import json
import sys

sys.path.append('noah-agent-skills/noah-stock-market/scripts')
from quote_client import NoahQuoteClient
from summarize_market import (
    summarize_basicinfo,
    summarize_capital_flow,
    summarize_intraday,
    summarize_kline,
    summarize_market_state,
    summarize_option_chain,
    summarize_option_expirations,
    summarize_orderbook,
    summarize_plate_list,
    summarize_plate_stock,
    summarize_snapshot,
)


def main():
    client = NoahQuoteClient()
    results = {}

    snapshot = client.get('/quotes/get_market_snapshot', {'code_list': 'HK-00700'})
    results['snapshot'] = {
        'ok': snapshot['ok'],
        'http_status': snapshot['http_status'],
        'message': snapshot.get('message'),
    }
    if isinstance(snapshot.get('data'), list) and snapshot['data']:
        results['snapshot']['summary'] = summarize_snapshot(snapshot['data'][0])

    market_state = client.get('/infos/get_market_state', {'code_list': 'HK-00700'})
    results['market_state'] = {
        'ok': market_state['ok'],
        'http_status': market_state['http_status'],
        'message': market_state.get('message'),
    }
    if isinstance(market_state.get('data'), list) and market_state['data']:
        results['market_state']['summary'] = summarize_market_state(market_state['data'])[:1]

    kline = client.get('/quotes/get_cur_kline', {'code': 'HK-00700', 'num': 5, 'ktype': 'K_DAY', 'autype': 'NONE'})
    results['kline'] = {
        'ok': kline['ok'],
        'http_status': kline['http_status'],
        'message': kline.get('message'),
    }
    if isinstance(kline.get('data'), list):
        results['kline']['summary'] = summarize_kline(kline['data'])

    intraday = client.get('/quotes/get_rt_data', {'code': 'HK-00700'})
    results['intraday'] = {
        'ok': intraday['ok'],
        'http_status': intraday['http_status'],
        'message': intraday.get('message'),
    }
    if isinstance(intraday.get('data'), list):
        results['intraday']['summary'] = summarize_intraday(intraday['data'])

    orderbook = client.get('/quotes/get_order_book', {'code': 'HK-00700', 'num': 5})
    results['orderbook'] = {
        'ok': orderbook['ok'],
        'http_status': orderbook['http_status'],
        'message': orderbook.get('message'),
    }
    if isinstance(orderbook.get('data'), dict):
        results['orderbook']['summary'] = summarize_orderbook(orderbook['data'])

    capital_flow = client.get('/infos/get_capital_flow', {'stock_code': 'HK-00700', 'num': 5})
    results['capital_flow'] = {
        'ok': capital_flow['ok'],
        'http_status': capital_flow['http_status'],
        'message': capital_flow.get('message'),
    }
    if isinstance(capital_flow.get('data'), list):
        results['capital_flow']['summary'] = summarize_capital_flow(capital_flow['data'])

    basicinfo = client.get('/quote/get_stock_basicinfo', {'market': 'HK', 'code_list': 'HK-00700'})
    results['basicinfo'] = {
        'ok': basicinfo['ok'],
        'http_status': basicinfo['http_status'],
        'message': basicinfo.get('message'),
    }
    if isinstance(basicinfo.get('data'), list):
        results['basicinfo']['summary'] = summarize_basicinfo(basicinfo['data'])[:3]

    plate_list = client.get('/quote/get_plate_list', {'market': 'HK', 'plate_class': 'INDUSTRY'})
    results['plate_list'] = {
        'ok': plate_list['ok'],
        'http_status': plate_list['http_status'],
        'message': plate_list.get('message'),
    }
    if isinstance(plate_list.get('data'), list):
        results['plate_list']['summary'] = summarize_plate_list(plate_list['data'])[:5]
        if plate_list['data']:
            first_plate_code = plate_list['data'][0].get('code')
            plate_stock = client.get('/quote/get_plate_stock', {'plate_code': first_plate_code, 'market': 'HK', 'page': 1, 'pageSize': 10})
            results['plate_stock'] = {
                'ok': plate_stock['ok'],
                'http_status': plate_stock['http_status'],
                'message': plate_stock.get('message'),
            }
            if isinstance(plate_stock.get('data'), list):
                results['plate_stock']['summary'] = summarize_plate_stock(plate_stock['data'])

    option_exp = client.get('/derivatives/get_option_expiration_date', {'code': 'HK-00700'})
    results['option_expiration'] = {
        'ok': option_exp['ok'],
        'http_status': option_exp['http_status'],
        'message': option_exp.get('message'),
    }
    if isinstance(option_exp.get('data'), list):
        results['option_expiration']['summary'] = summarize_option_expirations(option_exp['data'])[:10]

    option_chain = client.get('/derivatives/get_option_chain', {'code': 'US-AAPL', 'option_type': 'CALL'})
    results['option_chain'] = {
        'ok': option_chain['ok'],
        'http_status': option_chain['http_status'],
        'message': option_chain.get('message'),
    }
    if isinstance(option_chain.get('data'), list):
        results['option_chain']['summary'] = summarize_option_chain(option_chain['data'])

    print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
