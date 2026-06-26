import time
import json
import os
from longbridge.openapi import Config, TradeContext, OrderType, OrderSide, TimeInForceType
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# 配置路径
HISTORY_FILE = "/home/admin/.openclaw/skills/my_stock_longbridge_skill/order_history.json"

# API 凭证 (应使用安全 vault)
APP_KEY = "1ab56e0d711bf492491a795fd088170f"
APP_SECRET = "6f9285faff4b8aec2e6de8fc4fdb67f0f08426c7ba9a92fc9b041f9151b9f111"
ACCESS_TOKEN = "m_eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5YWRiMGIxYTdlNzYxNzEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJsb25nYnJpZGdlIiwic3ViIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzgxMDE5Njc3LCJpYXQiOjE3NzMyNDM2NzksImFrIjoiMWFiNTZlMGQ3MTFiZjQ5MjQ5MWE3OTVmZDA4ODE3MGYiLCJhYWlkIjoyMDUzMjY1MCwiYWMiOiJsYl9wYXBlcnRyYWRpbmciLCJtaWQiOjE2MTg0MzksInNpZCI6ImJmSDV6SUNpL0Rwc3ViK050T1I3akE9PSIsImJsIjozLCJ1bCI6MCwiaWsiOiJsYl9wYXBlcnRyYWRpbmdfMjA1MzI2NTAifQ.OG-mJZpPtEMy-j_6bBnh8rrw_i_VVOuu1XsuAY4yDGcpjXTEFDKe_l-OH853hc5JDmfQFRDb1SBc5bB_Gj4zsPFKtpHqP0Ogyuj7vwvtk6iwVmm4ubAImYhx8HaRwMsowglEaUm0jwQrI1yLmyw2yI3nPJQ43Ai_fvFIJifN907LOk7nrhNxyTOo6EKRE29qfBu4w6EeE9b0vK7Gq25nTwQ2N5xprZSplZkNTUg2t1QdlFXVgrjvWP44JFkYegEJgg8EGFKfx_CaYGFgRO8z1GwM9GilhIHj9d7YLBn3WRhdO22_rsH46YcXOhpIXxwlUNQSdf3fqyhglG_rd6Vveg3GvPEKfSPpxjUadAqKth61d13bjRMX3LAgaeR4oM7tV1tep6MH5r5w1pNMOjX51Ac8p6Z0-fLFDJ45qRmk3RFoR6NjgTXB-E5NBfC36WNJKgSzerUeQE3KbO8ob-McY1jymQ4yfCuv4BSEM0NJrTEdYsKDDhsvfQ15DGQP2VCm5Myg6YRt9rG0OvSLsTdXD73OtGyU-0lBJdrPs9eTIcp_Ldp2cREea-SOQiNcsOQ-nNhI2PCulsgtgsfws77strdwgNb6QyEXVQRsU4LGcKHEdNeAmKzi6yAnNBrBAGOevgudk8yHae3l79LmZoxwPDTc6PyFOuFazMadMDjGA-c"

def get_trade_context():
    config = Config.from_apikey(app_key=APP_KEY, app_secret=APP_SECRET, access_token=ACCESS_TOKEN)
    return TradeContext(config)

def is_duplicate_order(symbol, side, quantity, price=None):
    if not os.path.exists(HISTORY_FILE):
        return False
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    
    now = time.time()
    # 检查 60 秒内是否有相同订单
    for entry in history:
        if (entry["symbol"] == symbol and entry["side"] == str(side) and 
            entry["quantity"] == quantity and entry.get("price") == price and (now - entry["time"] < 60)):
            return True
    return False

def save_order(symbol, side, quantity, price=None):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    
    history.append({"symbol": symbol, "side": str(side), "quantity": quantity, "price": price, "time": time.time()})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_order_with_retry(trade, symbol, side, quantity, order_type=OrderType.MO, price=None):
    kwargs = {
        "symbol": symbol,
        "order_type": order_type,
        "side": side,
        "submitted_quantity": quantity,
        "time_in_force": TimeInForceType.Day
    }
    if order_type == OrderType.LO and price is not None:
        kwargs["submitted_price"] = price
        
    return trade.submit_order(**kwargs)

def has_pending_order(trade, symbol, side, quantity, price=None):
    orders = trade.today_orders()
    for order in orders:
        if order.symbol == symbol and str(order.side) == str(side) and order.quantity == quantity:
            if order.status in ["Submitted", "Pending"]:
                return True
    return False

def manage_order(action, symbol=None, quantity=None, order_id=None, side=None, force=False, order_type=OrderType.MO, price=None):
    if action == "sell" or action == "buy":
        if not force and is_duplicate_order(symbol, str(side), quantity, price):
            print("DUPLICATE_CONFIRMATION_REQUIRED")
            return
        
        trade = get_trade_context()
        if has_pending_order(trade, symbol, side, quantity, price):
            print("SERVER_SIDE_DUPLICATE_DETECTED: 存在同向待成交订单")
            return

        kwargs = {
            "symbol": symbol,
            "order_type": order_type,
            "side": side,
            "submitted_quantity": quantity,
            "time_in_force": TimeInForceType.Day
        }
        if order_type == OrderType.LO and price is not None:
            kwargs["submitted_price"] = price

        resp = trade.submit_order(**kwargs)
        oid = resp.order_id
        save_order(symbol, str(side), quantity, price)
        time.sleep(2)
        detail = trade.order_detail(order_id=oid)
        
        order_type_str = "限价单" if order_type == OrderType.LO else "市价单"
        price_str = f" @ {price}" if price else ""
        print(f"[{symbol}] {order_type_str}提交成功, ID: {oid}, 状态: {detail.status}, 委托量: {quantity}{price_str}")

