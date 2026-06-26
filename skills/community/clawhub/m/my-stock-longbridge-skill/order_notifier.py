import sys
import time
import subprocess
from stock_manager import get_trade_context
import longbridge.openapi as openapi

# 目标用户和机器人账号
ACCOUNT_ID = "bot_jiucai"
TARGET_USER = "01436648354824173434"

def send_dingtalk_msg(content):
    cmd = [
        "openclaw", "message", "send",
        "--account", ACCOUNT_ID,
        "--target", TARGET_USER,
        "--message", content
    ]
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"Failed to send message: {e}")

def on_order_changed(event: openapi.PushOrderChanged):
    status_str = str(event.status)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {event.symbol} -> {status_str}", flush=True)
    
    # 过滤状态，只推送关键状态
    if "Filled" in status_str or "Rejected" in status_str or "Canceled" in status_str:
        side_str = str(event.side).replace("OrderSide.", "")
        status_clean = status_str.replace("OrderStatus.", "")
        
        msg = f"🔔 **订单状态变更通知**\n\n"
        msg += f"- **标的**: {event.symbol}\n"
        msg += f"- **方向**: {side_str}\n"
        msg += f"- **状态**: {status_clean}\n"
        msg += f"- **委托量**: {event.submitted_quantity}\n"
        
        if "Filled" in status_clean:
            msg += f"- **成交量**: {event.executed_quantity}\n"
            msg += f"- **成交均价**: ${event.executed_price}\n"
        elif "Rejected" in status_clean:
            msg += f"- **失败原因**: {event.msg}\n"
            
        send_dingtalk_msg(msg)

def main():
    print("Starting Longbridge Order Notifier daemon...", flush=True)
    trade = get_trade_context()
    trade.set_on_order_changed(on_order_changed)
    trade.subscribe([openapi.TopicType.Private])
    
    print("Subscribed to Private Topic. Waiting for events...", flush=True)
    # 阻塞主线程，保持监听
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
