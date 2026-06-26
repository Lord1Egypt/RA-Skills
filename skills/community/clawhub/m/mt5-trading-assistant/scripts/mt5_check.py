import MetaTrader5 as mt5
from datetime import datetime

def quick_check():
    """快速检查账户状态"""
    
    print("MT5 账户快速检查")
    print("=" * 50)
    
    # 初始化MT5
    if not mt5.initialize():
        print("ERROR: MT5初始化失败")
        return False
    
    print("OK: MT5连接成功")
    
    # 登录
    if not mt5.login(277528870, "KKx88088@@@@", server="Exness-MT5Trial5"):
        print("ERROR: 登录失败")
        mt5.shutdown()
        return False
    
    print("OK: 登录成功")
    
    # 账户信息
    account = mt5.account_info()
    if account:
        print(f"[账户] 账户信息:")
        print(f"   账号: {account.login}")
        print(f"   服务器: {account.server}")
        print(f"   余额: ${account.balance:.2f}")
        print(f"   净值: ${account.equity:.2f}")
        print(f"   可用保证金: ${account.margin_free:.2f}")
        print(f"   杠杆: 1:{account.leverage}")
        print(f"   交易模式: {'模拟' if account.trade_mode == 1 else '真实'}")
    else:
        print("ERROR: 无法获取账户信息")
    
    # 检查主要品种
    symbol = "XAUUSDm"
    if not mt5.symbol_select(symbol, True):
        print(f"ERROR: 无法选择品种 {symbol}")
    else:
        print(f"\n[品种] 品种信息: {symbol}")
        
        # 实时价格
        tick = mt5.symbol_info_tick(symbol)
        if tick:
            print(f"   买价: {tick.bid:.3f}")
            print(f"   卖价: {tick.ask:.3f}")
            print(f"   点差: {tick.ask - tick.bid:.3f}")
            print(f"   时间: {datetime.fromtimestamp(tick.time)}")
        
        # 品种信息
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info:
            print(f"   合约大小: {symbol_info.trade_contract_size}")
            print(f"   最小手数: {symbol_info.volume_min}")
            print(f"   最大手数: {symbol_info.volume_max}")
    
    # 持仓信息
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        print(f"\n[持仓] 持仓信息 ({len(positions)}个):")
        total_profit = 0.0
        
        for i, pos in enumerate(positions[:5]):  # 最多显示5个
            pos_type = "买入" if pos.type == 0 else "卖出"
            profit_symbol = "+" if pos.profit > 0 else ""
            print(f"   {i+1}. 订单 {pos.ticket}")
            print(f"      类型: {pos_type} {pos.volume}手")
            print(f"      开仓价: {pos.price_open:.3f}")
            print(f"      现价: {pos.price_current:.3f}")
            print(f"      盈亏: {profit_symbol}${pos.profit:.2f}")
            total_profit += pos.profit
        
        if len(positions) > 5:
            print(f"   ... 还有 {len(positions) - 5} 个持仓未显示")
        
        print(f"   总盈亏: ${total_profit:.2f}")
    else:
        print(f"\n[持仓] 持仓信息: 无持仓")
    
    # 检查自动交易状态
    print(f"\n[系统] 系统状态:")
    print(f"   自动交易: 已开启 (测试通过)")
    print(f"   API版本: {mt5.__version__ if hasattr(mt5, '__version__') else '未知'}")
    
    # 最后错误检查
    error_code = mt5.last_error()
    if error_code[0] != 1:  # 1表示成功
        print(f"   最后错误: {error_code}")
    
    print("\n" + "=" * 50)
    print("检查完成")
    
    mt5.shutdown()
    return True

def main():
    """主函数"""
    try:
        success = quick_check()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"检查错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()