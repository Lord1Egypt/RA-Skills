#!/usr/bin/env python3
"""
长桥智能投资助手 - OpenClaw Skill v2.0
自动监控持仓，提供智能止盈止损提醒、投资组合分析和可视化图表
"""
import os
import sys
import json
from datetime import datetime

# 配置
CONFIG = {
    'name': '长桥智能投资助手',
    'version': '2.0.0',
    'author': 'OpenClaw User',
}

# 止盈止损配置
ALERTS = {
    'SMCI.US': [
        {'price': 35.0, 'action': 'sell_half', 'msg': 'SMCI 到达$35，建议卖出390股获利'},
        {'price': 40.0, 'action': 'sell_all', 'msg': 'SMCI 到达$40，建议卖出剩余390股'},
    ],
    '1810.HK': [
        {'price': 32.0, 'action': 'buy_more', 'msg': '小米回调至$32，建议加仓机会'},
        {'price': 55.0, 'action': 'sell_partial', 'msg': '小米涨至$55，建议减仓1/3'},
    ],
    '7226.HK': [
        {'price': 4.5, 'action': 'sell_partial', 'msg': '7226 到达$4.50，建议卖出40,000股'},
    ],
    'NKE.US': [
        {'price': 48.0, 'action': 'stop_loss', 'msg': 'Nike 跌破$48止损价，建议卖出'},
    ],
}

def load_longbridge_env():
    """加载长桥环境变量"""
    env_path = os.path.expanduser("~/.longbridge/env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.replace("export ", "").strip()
                    os.environ.setdefault(key, val.strip(' "\''))

def get_holdings_with_value():
    """获取持仓及市值"""
    try:
        sys.path.insert(0, os.path.expanduser('~/.venv/longbridge/lib/python3.14/site-packages'))
        from longbridge.openapi import Config, TradeContext, QuoteContext
        
        load_longbridge_env()
        config = Config.from_apikey_env()
        ctx = TradeContext(config)
        quote_ctx = QuoteContext(config)
        
        stock_resp = ctx.stock_positions()
        
        holdings = {}
        symbols = []
        positions = []
        
        # 收集持仓
        for channel in stock_resp.channels:
            for pos in channel.positions:
                qty = float(pos.quantity)
                if qty != 0:
                    positions.append(pos)
                    symbols.append(pos.symbol)
                    holdings[pos.symbol] = {
                        'quantity': qty,
                        'cost_price': float(pos.cost_price),
                        'currency': pos.currency,
                        'market_value': 0,
                        'current_price': 0,
                    }
        
        # 获取实时行情
        if symbols:
            for i in range(0, len(symbols), 50):
                chunk = symbols[i:i+50]
                try:
                    quotes = quote_ctx.quote(chunk)
                    for q in quotes:
                        symbol = q.symbol
                        price = float(q.last_done)
                        if symbol in holdings:
                            holdings[symbol]['current_price'] = price
                            holdings[symbol]['market_value'] = holdings[symbol]['quantity'] * price
                except Exception as e:
                    print(f"  警告: 获取部分行情失败: {e}")
        
        return holdings
        
    except Exception as e:
        return {'error': str(e)}

def generate_portfolio_chart(holdings, output_path=None):
    """生成投资组合饼图 - 分开港股和美股"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # 无界面模式
        
        # 分离港股和美股
        hk_holdings = {s: h for s, h in holdings.items() if s.endswith('.HK')}
        us_holdings = {s: h for s, h in holdings.items() if s.endswith('.US')}
        
        # 创建2x1子图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        # ===== 港股图表 =====
        if hk_holdings:
            hk_sorted = sorted(
                [(s, h) for s, h in hk_holdings.items() if h['market_value'] != 0],
                key=lambda x: abs(x[1]['market_value']),
                reverse=True
            )[:12]  # 前12大
            
            hk_labels = []
            hk_sizes = []
            hk_colors = []
            hk_total = 0
            
            for symbol, data in hk_sorted:
                mv = abs(data['market_value'])
                price = data['current_price']
                hk_labels.append(f"{symbol.replace('.HK', '')}\n${price:.1f}")
                hk_sizes.append(mv)
                hk_colors.append('#2ecc71' if data['quantity'] > 0 else '#e74c3c')
                hk_total += data['market_value']
            
            wedges1, texts1, autotexts1 = ax1.pie(
                hk_sizes, labels=hk_labels, autopct='%1.1f%%',
                startangle=90, colors=hk_colors,
                textprops={'fontsize': 9}
            )
            ax1.set_title(f'[HK] Hong Kong Stocks\nTotal: ${hk_total:,.0f} HKD', 
                         fontsize=14, fontweight='bold')
        else:
            ax1.text(0.5, 0.5, 'No HK Holdings', ha='center', va='center', fontsize=12)
            ax1.axis('off')
        
        # ===== 美股图表 =====
        if us_holdings:
            us_sorted = sorted(
                [(s, h) for s, h in us_holdings.items() if h['market_value'] != 0],
                key=lambda x: abs(x[1]['market_value']),
                reverse=True
            )[:12]  # 前12大
            
            us_labels = []
            us_sizes = []
            us_colors = []
            us_total = 0
            
            for symbol, data in us_sorted:
                mv = abs(data['market_value'])
                price = data['current_price']
                us_labels.append(f"{symbol.replace('.US', '')}\n${price:.1f}")
                us_sizes.append(mv)
                us_colors.append('#3498db' if data['quantity'] > 0 else '#e74c3c')
                us_total += data['market_value']
            
            wedges2, texts2, autotexts2 = ax2.pie(
                us_sizes, labels=us_labels, autopct='%1.1f%%',
                startangle=90, colors=us_colors,
                textprops={'fontsize': 9}
            )
            ax2.set_title(f'[US] US Stocks\nTotal: ${us_total:,.0f} USD',
                         fontsize=14, fontweight='bold')
        else:
            ax2.text(0.5, 0.5, 'No US Holdings', ha='center', va='center', fontsize=12)
            ax2.axis('off')
        
        plt.tight_layout()
        
        # 保存图表
        if output_path is None:
            output_path = os.path.expanduser('~/longbridge-scripts/portfolio_chart.png')
        
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
        
    except ImportError:
        print("  提示: 安装 matplotlib 可生成图表")
        return None
    except Exception as e:
        print(f"  生成图表失败: {e}")
        return None

def check_alerts(holdings):
    """检查提醒"""
    alerts = []
    for symbol, alert_list in ALERTS.items():
        if symbol not in holdings:
            continue
        
        data = holdings[symbol]
        current_price = data['current_price']
        
        for alert in alert_list:
            target_price = alert['price']
            triggered = False
            
            if alert['action'] in ['sell_half', 'sell_all', 'sell_partial']:
                if current_price >= target_price:
                    triggered = True
            elif alert['action'] == 'buy_more':
                if current_price <= target_price:
                    triggered = True
            elif alert['action'] == 'stop_loss':
                if current_price <= target_price:
                    triggered = True
            
            if triggered:
                alerts.append({
                    'symbol': symbol,
                    'current_price': current_price,
                    'target_price': target_price,
                    'quantity': data['quantity'],
                    'market_value': data['market_value'],
                    'message': alert['msg'],
                    'action': alert['action'],
                })
    
    return alerts

def analyze_portfolio(holdings):
    """分析投资组合"""
    analysis = {
        'total_stocks': len(holdings),
        'long_positions': [],
        'short_positions': [],
        'total_long_value': 0,
        'total_short_value': 0,
        'recommendations': []
    }
    
    for symbol, data in holdings.items():
        mv = data['market_value']
        if data['quantity'] > 0:
            analysis['long_positions'].append(symbol)
            analysis['total_long_value'] += mv
        elif data['quantity'] < 0:
            analysis['short_positions'].append(symbol)
            analysis['total_short_value'] += abs(mv)
    
    # 生成建议
    if len(holdings) > 40:
        analysis['recommendations'].append('持仓过于分散，建议集中优质标的')
    
    if analysis['total_short_value'] > analysis['total_long_value'] * 0.3:
        analysis['recommendations'].append('做空仓位较高，注意风险控制')
    
    return analysis

def main():
    """主函数"""
    print(f"\n{'='*70}")
    print(f"🦞 {CONFIG['name']} v{CONFIG['version']}")
    print(f"{'='*70}\n")
    
    # 获取持仓
    print("📊 获取持仓及市值信息...")
    holdings = get_holdings_with_value()
    
    if 'error' in holdings:
        print(f"❌ 错误: {holdings['error']}")
        return
    
    total_value = sum(abs(h['market_value']) for h in holdings.values())
    print(f"✅ 获取成功，共 {len(holdings)} 只持仓")
    print(f"💰 总市值: ${total_value:,.0f}\n")
    
    # 生成图表
    print("📈 生成投资组合图表...")
    chart_path = generate_portfolio_chart(holdings)
    if chart_path:
        print(f"   ✅ 图表已保存: {chart_path}")
    print()
    
    # 显示前10大持仓
    print("📋 前10大持仓:")
    print("-" * 70)
    sorted_holdings = sorted(
        holdings.items(),
        key=lambda x: abs(x[1]['market_value']),
        reverse=True
    )[:10]
    
    for i, (symbol, data) in enumerate(sorted_holdings, 1):
        qty = data['quantity']
        price = data['current_price']
        mv = data['market_value']
        emoji = "🟢" if qty > 0 else "🔴"
        print(f"{i:2}. {emoji} {symbol:12} {qty:8.0f}股 @ ${price:8.2f} = ${mv:12,.0f}")
    print()
    
    # 检查提醒
    print("🔔 价格提醒检查:")
    print("-" * 70)
    alerts = check_alerts(holdings)
    
    if alerts:
        print(f"\n⚠️  触发 {len(alerts)} 个提醒:\n")
        for alert in alerts:
            print(f"🚨 {alert['symbol']}")
            print(f"   当前价: ${alert['current_price']:.2f}")
            print(f"   目标价: ${alert['target_price']:.2f}")
            print(f"   持仓: {alert['quantity']:.0f} 股 (${alert['market_value']:,.0f})")
            print(f"   💡 {alert['message']}")
            print()
    else:
        print("   ✅ 暂无价格提醒触发\n")
    
    # 分析组合
    print("📊 组合分析:")
    print("-" * 70)
    analysis = analyze_portfolio(holdings)
    print(f"   总持仓: {analysis['total_stocks']} 只")
    print(f"   做多: {len(analysis['long_positions'])} 只 (${analysis['total_long_value']:,.0f})")
    print(f"   做空: {len(analysis['short_positions'])} 只 (${analysis['total_short_value']:,.0f})")
    print(f"   净值: ${analysis['total_long_value'] - analysis['total_short_value']:,.0f}")
    
    if analysis['recommendations']:
        print("\n   💡 建议:")
        for rec in analysis['recommendations']:
            print(f"      • {rec}")
    print()
    
    print(f"{'='*70}\n")

if __name__ == '__main__':
    main()
