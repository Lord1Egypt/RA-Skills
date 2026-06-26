"""
股票自动监控脚本 - 每小时检查一次
监控列表：山子高科、隆基绿能等
通知方式：保存到日志文件
"""

import requests
import json
import time
from datetime import datetime
import os

# 监控的股票列表
STOCKS_TO_MONITOR = [
    {'code': 'sz000981', 'name': '山子高科', 'target_low': 4.05, 'target_high': 4.18},
    {'code': 'sh601012', 'name': '隆基绿能', 'target_low': 18.5, 'target_high': 19.5},
]

def get_stock_quote(code):
    """腾讯财经API获取行情"""
    url = f"https://qt.gtimg.cn/q={code}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            content = response.text
            if 'v_' in content:
                data = content.split('~')
                return {
                    'name': data[1],
                    'price': float(data[3]),
                    'change_pct': float(data[32]),
                    'high': float(data[33]),
                    'low': float(data[34]),
                    'volume': int(data[6]),
                }
    except Exception as e:
        print(f"Error: {e}")
    return None

def check_alerts(stock_info, targets):
    """检查是否触发警报"""
    alerts = []
    price = stock_info['price']
    
    if price <= targets['target_low']:
        alerts.append(f"ALERT: 价格触及低吸位 {targets['target_low']}")
    
    if price >= targets['target_high']:
        alerts.append(f"ALERT: 价格触及高抛位 {targets['target_high']}")
    
    if abs(stock_info['change_pct']) > 5:
        alerts.append(f"WARN: 涨跌幅超过5% ({stock_info['change_pct']:+.2f}%)")
    
    return alerts

def monitor_once():
    """执行一次监控"""
    log_lines = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    log_lines.append(f"\n{'='*60}")
    log_lines.append(f"监控时间: {timestamp}")
    log_lines.append(f"{'='*60}")
    
    for stock in STOCKS_TO_MONITOR:
        print(f"检查 {stock['name']} ({stock['code']})...")
        info = get_stock_quote(stock['code'])
        
        if info:
            line = f"{stock['name']}: {info['price']:.2f} ({info['change_pct']:+.2f}%) H:{info['high']:.2f} L:{info['low']:.2f}"
            log_lines.append(line)
            print(f"  {line}")
            
            # 检查警报
            alerts = check_alerts(info, stock)
            for alert in alerts:
                log_lines.append(f"  >> {alert}")
                print(f"  >> {alert}")
        else:
            log_lines.append(f"{stock['name']}: 获取失败")
            print(f"  获取失败")
    
    # 保存到日志文件
    log_dir = r"I:\OpenClawWorkspace\stocks\监控日志"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"stock_monitor_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write('\n'.join(log_lines) + '\n')
    
    print(f"\n日志已保存: {log_file}")
    return log_lines

def main():
    """主循环 - 每小时检查一次"""
    print("股票监控系统启动")
    print(f"监控列表: {[s['name'] for s in STOCKS_TO_MONITOR]}")
    print(f"检查间隔: 60分钟")
    print("按 Ctrl+C 停止\n")
    
    try:
        while True:
            monitor_once()
            
            # 等待60分钟
            print(f"\n下次检查: 60分钟后...")
            time.sleep(3600)
            
    except KeyboardInterrupt:
        print("\n\n监控系统已停止")

if __name__ == '__main__':
    # 先执行一次
    monitor_once()
    
    # 如果要持续监控，取消下面注释
    # main()
