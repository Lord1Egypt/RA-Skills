from trade_client import NoahTradeClient
from format_portfolio_text import format_account_info, format_positions, format_sec_asset, format_capital_flow

DETAIL_LIMIT = 10


class NoahPortfolioClient(NoahTradeClient):
    def get_account_info(self):
        return self._get('/trade/get_account_info', {})

    def get_positions(self, market):
        params = {'market': market}
        return self._get('/trade/get_positions', params)

    def get_sec_asset(self):
        return self._get('/trade/get_sec_asset', {})

    def get_sec_capital_flow(self, **kwargs):
        params = {}
        for k in ['start_date', 'end_date', 'business_type', 'fund_direction', 'page', 'page_size', 'last_id', 'record_last_id', 'trade_code', 'unique_code']:
            if kwargs.get(k) not in (None, ''):
                params[k] = kwargs[k]
        return self._get('/trade/get_sec_capital_flow', params)


def summarize_account_info(item):
    return item or {}


def summarize_positions(items):
    shown = items[:DETAIL_LIMIT]
    return {'count': len(items), 'items': shown, 'truncated': len(items) > DETAIL_LIMIT}


def summarize_sec_asset(items):
    return {'count': len(items), 'items': items[:DETAIL_LIMIT], 'truncated': len(items) > DETAIL_LIMIT}


def summarize_capital_flow(data):
    records = (data or {}).get('records') or []
    return {'count': len(records), 'items': records[:DETAIL_LIMIT], 'truncated': len(records) > DETAIL_LIMIT, 'last_update_time': (data or {}).get('last_update_time')}


def portfolio_text(intent, summary):
    if intent == 'account-info':
        return format_account_info(summary)
    if intent == 'positions':
        return format_positions(summary)
    if intent == 'sec-asset':
        return format_sec_asset(summary)
    if intent == 'sec-capital-flow':
        return format_capital_flow(summary)
    return ''
