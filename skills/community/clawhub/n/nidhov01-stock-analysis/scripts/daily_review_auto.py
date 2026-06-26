#!/usr/bin/env python3
"""
每日股市复盘 - 自动定时任务版本
支持：定时运行、飞书通知、数据保存
"""

import requests
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 工作区路径
WORKSPACE = Path('/root/.openclaw/workspace')
SCRIPTS_DIR = WORKSPACE / 'skills/stock-analysis/scripts'

def get_index_price(code):
    """获取指数价格（腾讯数据源）"""
    try:
        url = f"http://qt.gtimg.cn/q={code}"
        response = requests.get(url, timeout=3)
        response.encoding = 'gbk'
        
        if response.status_code == 200 and '=' in response.text:
            parts = response.text.split('"')[1].split('~')
            if len(parts) >= 50:
                return {
                    'price': float(parts[3]),
                    'change_pct': float(parts[32]),
                    'change_amt': float(parts[4]),
                }
    except:
        pass
    return None

def get_market_indices():
    """获取大盘指数"""
    indices = {
        '上证指数': 'sh000001',
        '深证成指': 'sz399001',
        '创业板指': 'sz399006',
        '沪深 300': 'sh000300',
    }
    
    results = {}
    for name, code in indices.items():
        data = get_index_price(code)
        if data:
            results[name] = data
    
    return results

def get_stock_price(symbol):
    """获取个股价格"""
    try:
        market = 'sh' if symbol.startswith('6') else 'sz'
        url = f"http://qt.gtimg.cn/q={market}{symbol}"
        response = requests.get(url, timeout=3)
        response.encoding = 'gbk'
        
        if response.status_code == 200 and '=' in response.text:
            parts = response.text.split('"')[1].split('~')
            if len(parts) >= 50:
                return {
                    'name': parts[1],
                    'price': float(parts[3]),
                    'change_pct': float(parts[32]),
                    'volume': float(parts[6]),
                    'high': float(parts[33]),
                    'low': float(parts[34]),
                }
    except:
        pass
    return None

def load_holdings():
    """加载持仓数据"""
    holdings_file = WORKSPACE / '投资组合记录.json'
    if holdings_file.exists():
        with open(holdings_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('投资组合', [])
    return []

def generate_daily_report():
    """生成每日复盘报告"""
    report = []
    report.append("="*60)
    report.append("  📊 每日股市复盘")
    report.append("="*60)
    report.append(f"\n日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # 1. 大盘指数
    report.append("📈 大盘指数：")
    report.append("-"*50)
    indices = get_market_indices()
    for name, data in indices.items():
        status = "📈" if data['change_pct'] > 0 else "📉" if data['change_pct'] < 0 else "➖"
        report.append(f"{name}: {data['price']:.2f} ({data['change_pct']:+.2f}%) {status}")
    
    report.append("\n")
    
    # 2. 持仓股跟踪
    report.append("💼 持仓股跟踪：")
    report.append("-"*50)
    holdings = load_holdings()
    
    total_profit = 0
    for h in holdings:
        if h.get('当前状态') != '持仓':
            continue
        
        symbol = h.get('股票代码', '')
        name = h.get('股票名称', '')
        cost = h.get('买入价格', 0)
        shares = h.get('持仓数量', 0)
        
        data = get_stock_price(symbol)
        if data:
            current_price = data['price']
            profit = (current_price - cost) * shares
            profit_pct = (current_price - cost) / cost * 100
            total_profit += profit
            
            status = "📈" if profit > 0 else "📉" if profit < 0 else "➖"
            report.append(f"{name} ({symbol}):")
            report.append(f"  现价：¥{current_price:.2f} ({data['change_pct']:+.2f}%)")
            report.append(f"  成本：¥{cost:.2f} | 盈亏：¥{profit:.2f} ({profit_pct:+.2f}%) {status}")
            
            # 条件单状态
            if '条件单设置' in h and h['条件单设置'].get('状态') == '已激活':
                target = h['条件单设置'].get('止盈价', 0)
                stop = h['条件单设置'].get('止损价', 0)
                dist_profit = ((target - current_price) / current_price * 100)
                dist_loss = ((current_price - stop) / current_price * 100)
                report.append(f"  止盈：¥{target:.2f} (+{dist_profit:.1f}%) | 止损：¥{stop:.2f} (-{dist_loss:.1f}%)")
        else:
            report.append(f"{name} ({symbol}): 数据获取失败 ❌")
        
        report.append("")
    
    # 3. 总结
    report.append("="*60)
    report.append("📌 今日总结：")
    report.append("-"*50)
    
    if indices:
        sh = indices.get('上证指数', {})
        if sh.get('change_pct', 0) > 0:
            report.append(f"大盘：📈 上涨 {sh.get('change_pct', 0):.2f}%")
        else:
            report.append(f"大盘：📉 下跌 {abs(sh.get('change_pct', 0)):.2f}%")
    
    report.append(f"持仓盈亏：{'📈' if total_profit > 0 else '📉' if total_profit < 0 else '➖'} ¥{total_profit:.2f}")
    report.append("")
    report.append("="*60)
    
    return "\n".join(report)

def save_report(report_text):
    """保存复盘报告到文件"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    report_file = WORKSPACE / f'每日复盘_{date_str}.md'
    
    # 转换为 Markdown 格式
    md_content = f"# 📊 每日股市复盘\n\n**日期：** {date_str}\n\n"
    md_content += "```\n" + report_text + "\n```"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return report_file

def send_feishu_notification(report_text):
    """发送飞书通知"""
    import json
    
    # 提取关键信息
    lines = report_text.split('\n')
    summary = []
    
    for line in lines:
        if '上证指数' in line:
            summary.append(line.strip())
        elif '深证成指' in line:
            summary.append(line.strip())
        elif '创业板指' in line:
            summary.append(line.strip())
        elif '持仓盈亏' in line:
            summary.append(line.strip())
        elif '祥龙电业' in line and '现价' in line:
            summary.append(line.strip())
    
    # 构建消息内容
    message_text = "📊 每日股市复盘\n\n"
    message_text += "\n".join(summary[:6])
    message_text += "\n\n查看详细报告：/root/.openclaw/workspace/每日复盘_*.md"
    
    print(f"\n📱 准备发送飞书通知...")
    print(f"消息内容：\n{message_text}\n")
    
    # 保存到待发送文件
    pending_file = WORKSPACE / 'feishu_pending_message.json'
    message_json = {
        "msg_type": "text",
        "content": {
            "text": message_text
        }
    }
    
    with open(pending_file, 'w', encoding='utf-8') as f:
        json.dump(message_json, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 通知已准备就绪：{pending_file}")
    print(f"📩 将发送到飞书：ou_f1a29f8d231d21d113acbea658fc45fe")

def main():
    """主函数"""
    print("🚀 开始生成每日复盘报告...\n")
    
    try:
        # 生成报告
        report = generate_daily_report()
        
        # 显示报告
        print(report)
        
        # 保存报告
        report_file = save_report(report)
        print(f"\n✅ 报告已保存：{report_file}")
        
        # 发送飞书通知
        send_feishu_notification(report)
        
        print("\n✨ 每日复盘完成！")
        return 0
        
    except Exception as e:
        print(f"\n❌ 生成报告失败：{e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
