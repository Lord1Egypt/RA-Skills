import MetaTrader5 as mt5
import time
from datetime import datetime

def close_all_positions(symbol="XAUUSDm", magic_numbers=None):
    """平仓所有指定品种的持仓"""
    
    # 初始化MT5
    if not mt5.initialize():
        print("ERROR: MT5初始化失败")
        return False
    
    # 登录
    if not mt5.login(277528870, "KKx88088@@@@", server="Exness-MT5Trial5"):
        print("ERROR: 登录失败")
        mt5.shutdown()
        return False
    
    # 获取所有持仓
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        print(f"ℹ️  {symbol} 无持仓")
        mt5.shutdown()
        return True
    
    print(f"找到 {len(positions)} 个 {symbol} 持仓")
    
    total_profit = 0.0
    closed_count = 0
    
    # 遍历所有持仓
    for pos in positions:
        # 如果指定了magic numbers，只关闭匹配的订单
        if magic_numbers and pos.magic not in magic_numbers:
            print(f"跳过订单 {pos.ticket} (magic: {pos.magic})")
            continue
        
        # 确定平仓类型
        close_type = mt5.ORDER_TYPE_BUY if pos.type == 1 else mt5.ORDER_TYPE_SELL
        
        # 获取当前价格
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            print(f"ERROR: 无法获取 {symbol} 价格，跳过订单 {pos.ticket}")
            continue
        
        close_price = tick.ask if close_type == mt5.ORDER_TYPE_BUY else tick.bid
        
        print(f"平仓订单 {pos.ticket}:")
        print(f"  类型: {'买入' if pos.type == 0 else '卖出'}")
        print(f"  手数: {pos.volume}")
        print(f"  开仓价: {pos.price_open:.3f}")
        print(f"  现价: {pos.price_current:.3f}")
        print(f"  平仓价: {close_price:.3f}")
        print(f"  当前盈亏: ${pos.profit:.2f}")
        
        # 构建平仓请求
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": pos.volume,
            "type": close_type,
            "position": pos.ticket,
            "price": close_price,
            "deviation": 20,
            "magic": pos.magic,
            "comment": f"批量平仓",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK
        }
        
        # 发送平仓请求
        result = mt5.order_send(close_request)
        
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"✅ 平仓成功")
            print(f"  成交价: {result.price:.3f}")
            total_profit += pos.profit
            closed_count += 1
        else:
            print(f"❌ 平仓失败")
            print(f"  错误: {result.comment}")
        
        # 短暂等待，避免请求过快
        time.sleep(0.5)
    
    # 显示总结
    print(f"\n📊 平仓总结:")
    print(f"  平仓数量: {closed_count}/{len(positions)}")
    print(f"  总盈亏: ${total_profit:.2f}")
    
    # 获取账户最新状态
    account = mt5.account_info()
    if account:
        print(f"  账户余额: ${account.balance:.2f}")
        print(f"  账户净值: ${account.equity:.2f}")
    
    mt5.shutdown()
    return True

def close_by_magic(symbol="XAUUSDm", magic_numbers=[100001, 100002]):
    """平仓特定magic number的订单"""
    print(f"平仓 {symbol} 中 magic={magic_numbers} 的订单")
    return close_all_positions(symbol, magic_numbers)

def close_specific_ticket(ticket_id):
    """平仓特定订单号的持仓"""
    
    # 初始化MT5
    if not mt5.initialize():
        print("ERROR: MT5初始化失败")
        return False
    
    # 登录
    if not mt5.login(277528870, "KKx88088@@@@", server="Exness-MT5Trial5"):
        print("ERROR: 登录失败")
        mt5.shutdown()
        return False
    
    # 获取特定持仓
    positions = mt5.positions_get(ticket=ticket_id)
    if not positions:
        print(f"未找到订单 {ticket_id}")
        mt5.shutdown()
        return False
    
    pos = positions[0]
    symbol = pos.symbol
    
    print(f"平仓订单 {ticket_id}:")
    print(f"  品种: {symbol}")
    print(f"  类型: {'买入' if pos.type == 0 else '卖出'}")
    print(f"  手数: {pos.volume}")
    print(f"  开仓价: {pos.price_open:.3f}")
    print(f"  现价: {pos.price_current:.3f}")
    print(f"  当前盈亏: ${pos.profit:.2f}")
    
    # 确定平仓类型
    close_type = mt5.ORDER_TYPE_BUY if pos.type == 1 else mt5.ORDER_TYPE_SELL
    
    # 获取当前价格
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print(f"ERROR: 无法获取 {symbol} 价格")
        mt5.shutdown()
        return False
    
    close_price = tick.ask if close_type == mt5.ORDER_TYPE_BUY else tick.bid
    
    # 构建平仓请求
    close_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": pos.volume,
        "type": close_type,
        "position": ticket_id,
        "price": close_price,
        "deviation": 20,
        "magic": pos.magic,
        "comment": f"指定平仓",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK
    }
    
    # 发送平仓请求
    result = mt5.order_send(close_request)
    
    if result.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"✅ 平仓成功")
        print(f"  成交价: {result.price:.3f}")
        print(f"  最终盈亏: ${pos.profit:.2f}")
        success = True
    else:
        print(f"❌ 平仓失败")
        print(f"  错误: {result.comment}")
        success = False
    
    mt5.shutdown()
    return success

def main():
    """主函数，处理命令行参数"""
    import sys
    
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("用法:")
        print("  python mt5_close_all.py all              # 平仓所有XAUUSDm持仓")
        print("  python mt5_close_all.py magic            # 平仓脚本创建的订单")
        print("  python mt5_close_all.py <订单号>         # 平仓特定订单")
        print("  python mt5_close_all.py                  # 平仓脚本创建的订单(默认)")
        return
    
    command = sys.argv[1]
    
    try:
        if command == "all":
            # 平仓所有持仓
            success = close_all_positions()
        elif command == "magic":
            # 平仓脚本创建的订单
            success = close_by_magic()
        elif command.isdigit():
            # 平仓特定订单
            ticket_id = int(command)
            success = close_specific_ticket(ticket_id)
        else:
            print(f"未知命令: {command}")
            success = False
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"执行错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()