from errors import TradeCliError


def success_response(command, config, result, raw):
    return {
        "ok": True,
        "command": command,
        "environment": config.env,
        "mode": "read-only" if config.read_only else "read-write",
        "human_summary": result.get("human_summary"),
        "data": result.get("data"),
        "debug": {
            "endpoint": raw.get("endpoint"),
            "trace_id": raw.get("trace_id"),
        },
    }


def error_response(command, error):
    if isinstance(error, TradeCliError):
        return {
            "ok": False,
            "command": command,
            "error_type": error.__class__.__name__,
            "message": error.message,
            "hint": error.hint,
            "endpoint": error.endpoint,
            "http_status": error.http_status,
            "biz_code": error.biz_code,
            "trace_id": error.trace_id,
            "retryable": error.retryable,
        }

    return {
        "ok": False,
        "command": command,
        "error_type": error.__class__.__name__,
        "message": str(error),
        "hint": "发生未预期错误，请查看日志并补充结构化错误处理",
        "retryable": False,
    }


def summarize_today_orders(raw):
    data = raw.get("response", {})
    orders = data.get("data", []) if isinstance(data, dict) else []
    return {
        "human_summary": f"查询到今日订单 {len(orders)} 笔。",
        "data": {
            "count": len(orders),
            "items": orders[:20],
        },
    }


def summarize_today_deals(raw):
    data = raw.get("response", {})
    deals = data.get("data", []) if isinstance(data, dict) else []
    return {
        "human_summary": f"查询到今日成交 {len(deals)} 笔。",
        "data": {
            "count": len(deals),
            "items": deals[:20],
        },
    }


def summarize_history_deals(raw):
    data = raw.get("response", {})
    deals = data.get("data", []) if isinstance(data, dict) else []
    return {
        "human_summary": f"查询到历史成交 {len(deals)} 笔。",
        "data": {
            "count": len(deals),
            "items": deals[:20],
        },
    }


def summarize_today_unfinished_orders(raw):
    data = raw.get("response", {})
    items = data.get("data", []) if isinstance(data, dict) else []
    return {
        "human_summary": f"查询到当日未完成订单 {len(items)} 笔。",
        "data": {
            "count": len(items),
            "items": items[:20],
        },
    }


def summarize_finished_orders(raw):
    data = raw.get("response", {})
    items = data.get("data", []) if isinstance(data, dict) else []
    return {
        "human_summary": f"查询到已完成订单 {len(items)} 笔。",
        "data": {
            "count": len(items),
            "items": items[:20],
        },
    }


def summarize_order_detail(raw):
    data = raw.get("response", {})
    return {
        "human_summary": "已获取订单详情。",
        "data": data.get("data", data),
    }


def summarize_fee_estimate(raw, symbol, side, price, qty):
    data = raw.get("response", {})
    return {
        "human_summary": f"已获取 {symbol} {side} {qty} 股/份、价格 {price} 的费用预估。",
        "data": {
            "symbol": symbol,
            "side": side,
            "price": price,
            "qty": qty,
            "result": data.get("data", data),
        },
    }


def summarize_stock_amount(raw, symbol):
    data = raw.get("response", {})
    return {
        "human_summary": f"已获取 {symbol} 的可买可卖数量。",
        "data": {
            "symbol": symbol,
            "result": data.get("data", data),
        },
    }


def summarize_order_fee_detail(raw):
    data = raw.get("response", {})
    return {
        "human_summary": "已获取订单费用详情。",
        "data": data.get("data", data),
    }


def multi_currency_asset_note() -> str:
    return "涉及多种计价货币时，不直接跨币种加总；默认按币种分别展示，未做汇率换算。"


def summarize_max_enable_buy_amt(raw, symbol, order_type):
    data = raw.get("response", {})
    return {
        "human_summary": f"已获取 {symbol} 在 {order_type} 委托属性下的最大可买数量。",
        "data": {
            "symbol": symbol,
            "order_type": order_type,
            "result": data.get("data", data),
        },
    }
