from urllib.parse import urljoin

import requests

from errors import TradeApiError, TradeBizError


class NoahTradeClient:
    def __init__(self, config):
        self.config = config
        self.base_url = config.base_url.rstrip('/') + '/'
        self.headers = {
            'Authorization': f'Bearer {config.token}',
            'Accept': 'application/json',
        }

    def _normalize_error(self, resp, endpoint, data, trace_id):
        detail = data.get('detail') if isinstance(data, dict) else None
        message = data.get('msg') if isinstance(data, dict) else None
        text = detail or message or str(data)
        raise TradeApiError(
            f"HTTP {resp.status_code}: {text}",
            endpoint=endpoint,
            http_status=resp.status_code,
            trace_id=trace_id,
            hint='交易接口返回 HTTP 错误，请检查请求参数与访问权限',
        )

    def _handle_response(self, resp, endpoint):
        trace_id = resp.headers.get('x-trace-id') or resp.headers.get('traceId')
        try:
            data = resp.json()
        except Exception:
            raise TradeApiError(
                f"HTTP {resp.status_code}: {resp.text[:500]}",
                endpoint=endpoint,
                http_status=resp.status_code,
                trace_id=trace_id,
                hint='接口返回内容不是合法 JSON',
            )

        if resp.status_code >= 400:
            self._normalize_error(resp, endpoint, data, trace_id)

        if isinstance(data, dict):
            success = data.get('success', True)
            biz_code = data.get('code')
            message = data.get('msg') or data.get('message')
            if success is False or biz_code == 0:
                raise TradeBizError(
                    message or 'Trade business error',
                    endpoint=endpoint,
                    biz_code=biz_code,
                    trace_id=trace_id,
                    hint='请检查业务参数、账户状态和 Bearer token 是否匹配',
                )

        return {
            'endpoint': endpoint,
            'trace_id': trace_id,
            'response': data,
        }

    def _get(self, endpoint, params=None):
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        params = params or {}
        try:
            resp = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=self.config.timeout_seconds,
            )
        except requests.RequestException as e:
            raise TradeApiError(
                f"HTTP request failed: {e}",
                endpoint=endpoint,
                hint='请检查网络、Base URL 和交易服务可达性',
                retryable=True,
            )
        return self._handle_response(resp, endpoint)

    def _post(self, endpoint, payload=None):
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        payload = payload or {}
        headers = dict(self.headers)
        headers['Content-Type'] = 'application/json'
        try:
            resp = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.config.timeout_seconds,
            )
        except requests.RequestException as e:
            raise TradeApiError(
                f"HTTP request failed: {e}",
                endpoint=endpoint,
                hint='请检查网络、Base URL 和交易服务可达性',
                retryable=True,
            )
        return self._handle_response(resp, endpoint)

    def get_today_orders(self, market, code=None, page=1, page_size=50):
        params = {'market': market}
        if code:
            params['code'] = code
        if page is not None:
            params['page'] = page
        if page_size is not None:
            params['page_size'] = page_size
        return self._get('/trade/get_order_list', params)

    def get_today_deals(self, code=None):
        params = {}
        if code:
            params['code'] = code
        return self._get('/trade/get_today_deal_list', params)


    def get_history_orders(self, code=None, start_date=None, end_date=None, order_id=None, order_no=None, order_status=None):
        params = {}
        if code:
            params['code'] = code
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        if order_id:
            params['order_id'] = order_id
        if order_no:
            params['order_no'] = order_no
        if order_status:
            params['order_status'] = order_status
        return self._get('/trade/get_history_order_list', params)

    def query_push_data(self, init_date, begin_serial_no, end_serial_no):
        payload = {
            'init_date': init_date,
            'begin_serial_no': str(begin_serial_no),
            'end_serial_no': str(end_serial_no),
        }
        return self._post('/trade/query_push_data', payload)
    def get_history_deals(self, code=None, start_date=None, end_date=None):
        params = {}
        if code:
            params['code'] = code
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        return self._get('/trade/get_history_deal_list', params)

    def get_today_unfinished_orders(self, code=None, order_id=None, order_no=None, order_status=None):
        params = {}
        if code:
            params['code'] = code
        if order_id:
            params['order_id'] = order_id
        if order_no:
            params['order_no'] = order_no
        if order_status:
            params['order_status'] = order_status
        return self._get('/trade/get_today_order_list', params)

    def get_finished_orders(self, code=None, start_date=None, end_date=None, page=None, page_size=None, order_id=None, order_no=None, order_status=None, order_side=None, order_type=None):
        params = {}
        for k, v in {
            'code': code,
            'start_date': start_date,
            'end_date': end_date,
            'page': page,
            'page_size': page_size,
            'order_id': order_id,
            'order_no': order_no,
            'order_status': order_status,
            'order_side': order_side,
            'order_type': order_type,
        }.items():
            if v not in (None, ''):
                params[k] = v
        return self._get('/trade/get_finished_order_list', params)

    def get_order_detail(self, order_id, order_no=None, is_history=None):
        params = {'order_id': order_id}
        if order_no:
            params['order_no'] = order_no
        if is_history is not None:
            params['is_history'] = str(bool(is_history)).lower()
        return self._get('/trade/get_order_detail', params)

    def get_order_fee_detail(self, order_id, order_no=None, is_history=None):
        params = {'order_id': order_id}
        if order_no:
            params['order_no'] = order_no
        if is_history is not None:
            params['is_history'] = str(bool(is_history)).lower()
        return self._get('/trade/get_order_fee_detail', params)

    def max_enable_buy_amt(self, symbol, order_type, entrust_price, session_type=None):
        params = {
            'code': symbol,
            'order_type': order_type,
            'entrust_price': str(entrust_price),
        }
        if session_type is not None:
            params['session_type'] = session_type
        return self._get('/trade/max_enable_buy_amt', params)

    def order_fee_query(self, symbol, side, order_type, qty, price=None):
        payload = {
            'code': symbol,
            'order_side': side,
            'order_type': order_type,
            'quantity': str(qty),
        }
        if price is not None:
            payload['price'] = str(price)
        return self._post('/trade/order_fee_query', payload)

    def get_stock_amount(self, symbol, order_type, session_type=None):
        params = {
            'code': symbol,
            'order_type': order_type,
        }
        if session_type is not None:
            params['session_type'] = session_type
        return self._get('/trade/get_stock_amount', params)
