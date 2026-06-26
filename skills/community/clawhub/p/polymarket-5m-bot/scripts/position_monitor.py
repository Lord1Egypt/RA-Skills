#!/usr/bin/env python3
"""
持仓止盈监控 - 5分钟市场专用
在市场关闭前的80-100秒窗口内监控价格，达到+15%即止盈
"""
import json
import os
import subprocess
import time
from datetime import datetime, timezone
import requests

POSITIONS_FILE = "/root/.openclaw/workspace/polymarket-arb-bot/logs/positions.jsonl"
PROFIT_THRESHOLD = 0.15  # 15% 止盈

# Telegram 通知配置
TELEGRAM_BOT_TOKEN = "8315083265:AAGM_rUxfOzmnTDYd6v2n6n-kEArK37tKKk"
TELEGRAM_CHAT_ID = "1609325006"

def send_telegram(text):
    """发送 Telegram 通知"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except:
        pass

def get_open_positions():
    """获取未关闭的持仓"""
    positions = []
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            for line in f:
                if line.strip():
                    try:
                        pos = json.loads(line)
                        if isinstance(pos, dict) and not pos.get("closed", False):
                            positions.append(pos)
                    except:
                        pass
    return positions

def get_market_price(token_id):
    """获取当前市场中间价"""
    try:
        resp = requests.get(
            f"https://clob.polymarket.com/midpoint?token_id={token_id}",
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            mid = data.get("mid")
            if mid:
                return float(mid)
    except:
        pass
    return None

def get_best_bid(token_id):
    """获取最佳买价（用于卖出）"""
    try:
        resp = requests.get(
            f"https://clob.polymarket.com/price?token_id={token_id}&side=sell",
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict):
                price = data.get("price")
                if price:
                    return float(price)
    except:
        pass
    return None

def sell_position(token_id, size, price):
    """卖出持仓"""
    price = round(price, 2)
    cmd = [
        "polymarket", "clob", "create-order",
        "--signature-type", "gnosis-safe",
        "--token", token_id,
        "--side", "sell",
        "--price", str(price),
        "--size", str(size)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return False, str(e)

def close_position(position, exit_price):
    """标记持仓为已关闭"""
    position["closed"] = True
    position["exit_price"] = exit_price
    position["exit_time"] = datetime.now(timezone.utc).isoformat()
    
    all_positions = []
    if os.path.exists(POSITIONS_FILE):
        with open(POSITIONS_FILE, "r") as f:
            for line in f:
                if line.strip():
                    try:
                        pos = json.loads(line)
                        if isinstance(pos, dict):
                            if pos.get("token_id") == position["token_id"] and pos.get("entry_time") == position["entry_time"]:
                                all_positions.append(position)
                            else:
                                all_positions.append(pos)
                    except:
                        pass
    
    with open(POSITIONS_FILE, "w") as f:
        for pos in all_positions:
            f.write(json.dumps(pos) + "\n")

def check_market_closed(slug):
    """检查市场是否已关闭"""
    try:
        resp = requests.get(
            f"https://gamma-api.polymarket.com/events?slug={slug}",
            timeout=5
        )
        if resp.status_code == 200:
            events = resp.json()
            if isinstance(events, list) and len(events) > 0:
                event = events[0]
                if isinstance(event, dict):
                    markets = event.get("markets")
                    if isinstance(markets, list) and len(markets) > 0:
                        market = markets[0]
                        if isinstance(market, dict):
                            return market.get("closed", False)
    except:
        pass
    return False

def monitor():
    """主监控循环"""
    print("🔍 止盈监控启动（阈值: +15%）...")
    
    while True:
        try:
            positions = get_open_positions()
            
            if not positions:
                time.sleep(3)
                continue
            
            for pos in positions:
                token_id = pos["token_id"]
                entry_price = pos["entry_price"]
                size = pos["size"]
                slug = pos.get("slug", "unknown")
                coin = "BTC" if "btc" in slug else "ETH"
                
                # 先检查市场是否已关闭
                if check_market_closed(slug):
                    print(f"  ⏳ {slug} 市场已关闭")
                    close_position(pos, entry_price)
                    continue
                
                # 获取当前价格
                current_price = get_market_price(token_id)
                if current_price is None:
                    continue
                
                # 计算利润率
                profit_rate = (current_price - entry_price) / entry_price if entry_price > 0 else 0
                
                print(f"  📈 {coin} | 买入: ${entry_price:.2f} → 当前: ${current_price:.2f} | {profit_rate*100:+.1f}%")
                
                # 止盈检查
                if profit_rate >= PROFIT_THRESHOLD:
                    print(f"  ✅ 达到止盈条件 ({profit_rate*100:.1f}% >= {PROFIT_THRESHOLD*100:.0f}%)！")
                    
                    best_bid = get_best_bid(token_id)
                    sell_price = best_bid if best_bid else round(current_price * 0.99, 2)
                    
                    success, output = sell_position(token_id, size, sell_price)
                    
                    if success:
                        profit = (sell_price - entry_price) * size
                        print(f"  🎉 止盈成功！利润: ${profit:.2f}")
                        close_position(pos, sell_price)
                        
                        msg = (
                            f"🎉 <b>止盈成功！</b>\n\n"
                            f"📊 市场: {coin}\n"
                            f"📈 买入: ${entry_price:.2f} → 卖出: ${sell_price:.2f}\n"
                            f"💰 利润: ${profit:.2f} ({profit_rate*100:.1f}%)\n"
                            f"📦 数量: {size} 份"
                        )
                        send_telegram(msg)
                    else:
                        print(f"  ❌ 卖出失败: {output[:80]}")
        
        except Exception as e:
            print(f"❌ 监控错误: {e}")
        
        time.sleep(3)  # 3秒扫描一次（窗口只有80-100秒）

if __name__ == "__main__":
    monitor()
