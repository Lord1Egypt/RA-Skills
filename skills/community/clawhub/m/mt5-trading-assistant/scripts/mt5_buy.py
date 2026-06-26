#!/usr/bin/env python3
"""
MT5 Buy Order Script

NOTE: This script contains hardcoded account information for demonstration.
      For production use, modify the configuration below or use config.py import.

Configuration options:
1. Direct modification: Edit the values in this script
2. Config file: Create config.py and import it
3. Environment variables: Use os.getenv() for sensitive data
"""

import MetaTrader5 as mt5
import sys
import time
from datetime import datetime

# ============================================================================
# CONFIGURATION - MODIFY THESE VALUES FOR YOUR ACCOUNT
# ============================================================================

# MT5 Account Configuration
ACCOUNT_CONFIG = {
    "login": 277528870,                     # CHANGE: Your MT5 account number
    "password": "KKx88088@@@@",             # CHANGE: Your MT5 account password
    "server": "Exness-MT5Trial5",          # CHANGE: Your MT5 server
    "symbol": "XAUUSDm",                    # CHANGE: Trading symbol (Exness gold)
    "deviation": 20,                        # Price deviation in points
    "magic": 100001,                        # Order magic number identifier
    "comment_prefix": "MT5-Buy",            # Order comment prefix
}

# Alternative: Import from config file (uncomment if using config.py)
# try:
#     from config import MT5_CONFIG
#     ACCOUNT_CONFIG.update(MT5_CONFIG)
# except ImportError:
#     print("NOTE: config.py not found, using hardcoded configuration")
#     print("      Create config.py or modify values above")

# ============================================================================

def buy_order(volume=0.01, price=None, sl=None, tp=None):
    """执行买入订单"""
    config = ACCOUNT_CONFIG
    symbol = config["symbol"]
    
    # 初始化MT5
    if not mt5.initialize():
        print("ERROR: MT5初始化失败")
        print("      Ensure MT5 desktop client is running")
        return False
    
    # 登录
    if not mt5.login(config["login"], config["password"], server=config["server"]):
        print("ERROR: 登录失败")
        print(f"      Account: {config['login']}")
        print(f"      Server: {config['server']}")
        print("      Check account credentials and server name")
        mt5.shutdown()
        return False
    
    # 选择品种
    if not mt5.symbol_select(symbol, True):
        print(f"ERROR: 无法选择品种 {symbol}")
        print("      Verify symbol exists in MT5 client")
        mt5.shutdown()
        return False
    
    # 获取当前价格
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print("ERROR: 无法获取实时价格")
        mt5.shutdown()
        return False
    
    # 使用指定价格或市价
    if price is None or price <= 0:
        price = tick.ask  # 买入使用卖价
    
    print(f"买入 {symbol} {volume}手")
    print(f"当前卖价: {tick.ask:.3f}")
    print(f"使用价格: {price:.3f}")
    
    if sl:
        print(f"止损: {sl:.3f}")
    if tp:
        print(f"止盈: {tp:.3f}")
    
    # 构建订单请求
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "deviation": config.get("deviation", 20),
        "magic": config.get("magic", 100001),
        "comment": f"{config.get('comment_prefix', 'MT5')}-Buy {volume}",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    
    # 添加止损止盈
    if sl:
        request["sl"] = sl
    if tp:
        request["tp"] = tp
    
    # 发送订单
    result = mt5.order_send(request)
    
    # 检查结果
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"✅ 买入成功!")
        print(f"   订单号: {result.order}")
        print(f"   成交价: {result.price:.3f}")
        print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 等待订单成交并获取详细信息
        time.sleep(1)
        positions = mt5.positions_get(ticket=result.order)
        if positions:
            pos = positions[0]
            print(f"   持仓信息:")
            print(f"     开仓价: {pos.price_open:.3f}")
            print(f"     现价: {pos.price_current:.3f}")
            print(f"     盈亏: ${pos.profit:.2f}")
    else:
        print(f"❌ 买入失败")
        print(f"   错误码: {result.retcode}")
        print(f"   描述: {result.comment}")
    
    # 关闭连接
    mt5.shutdown()
    return result.retcode == mt5.TRADE_RETCODE_DONE

def main():
    """主函数，处理命令行参数"""
    if len(sys.argv) < 2:
        print("用法: python mt5_buy.py <手数> [价格] [止损] [止盈]")
        print("示例:")
        print("  python mt5_buy.py 0.01                  # 市价买入0.01手")
        print("  python mt5_buy.py 0.05 5040.00         # 指定价格5040.00买入")
        print("  python mt5_buy.py 0.03 0 5030 5050    # 市价买入，设置止损止盈")
        print("  python mt5_buy.py 0.02 5045 5035 5060 # 指定价格，设置止损止盈")
        return
    
    try:
        # 解析参数
        volume = float(sys.argv[1])
        
        price = None
        if len(sys.argv) > 2:
            price_arg = float(sys.argv[2])
            if price_arg > 0:
                price = price_arg
        
        sl = None
        if len(sys.argv) > 3:
            sl_arg = float(sys.argv[3])
            if sl_arg > 0:
                sl = sl_arg
        
        tp = None
        if len(sys.argv) > 4:
            tp_arg = float(sys.argv[4])
            if tp_arg > 0:
                tp = tp_arg
        
        # 执行买入
        success = buy_order(volume, price, sl, tp)
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except ValueError as e:
        print(f"参数错误: {e}")
        print("请确保参数为数字格式")
        sys.exit(1)
    except Exception as e:
        print(f"执行错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()