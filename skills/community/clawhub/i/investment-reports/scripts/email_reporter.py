#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Investage Email Reporter v2
增強版每日投資報告
"""

import subprocess
import yfinance as yf
from datetime import datetime
from typing import List, Dict, Any
import psycopg2

RECIPIENTS = ["george@precaster.com.tw", "ching@precaster.com.tw"]
GOG_ACCOUNT = "george@precaster.com.tw"


def get_market_indices() -> Dict:
    """取得大盤指數"""
    indices = {}
    tickers = {
        '^GSPC': 'S&P 500',
        '^IXIC': 'Nasdaq',
        '^DJI': 'Dow Jones',
        '^VIX': 'VIX'
    }
    
    for symbol, name in tickers.items():
        try:
            data = yf.Ticker(symbol).history(period='2d')
            if len(data) >= 2:
                current = float(data['Close'].iloc[-1])
                prev = float(data['Close'].iloc[-2])
                change = (current - prev) / prev * 100
                indices[name] = {
                    'price': current,
                    'change': change,
                    'symbol': symbol
                }
        except:
            indices[name] = {'price': 0, 'change': 0, 'symbol': symbol}
    
    return indices


def get_watchlist() -> List[Dict]:
    """取得追蹤清單報價"""
    conn = psycopg2.connect(host='localhost', database='investage', user='george')
    cur = conn.cursor()
    
    cur.execute("SELECT ticker, reason FROM watchlist WHERE status = 'WATCHING' ORDER BY ticker")
    watchlist = [{'ticker': r[0], 'reason': r[1]} for r in cur.fetchall()]
    conn.close()
    
    result = []
    for w in watchlist:
        try:
            data = yf.Ticker(w['ticker']).history(period='5d')
            if len(data) >= 2:
                current = float(data['Close'].iloc[-1])
                prev = float(data['Close'].iloc[-2])
                change = (current - prev) / prev * 100
                
                # 取得分析師評級
                info = yf.Ticker(w['ticker']).info
                recommendation = info.get('recommendationKey', 'unknown')
                
                result.append({
                    'ticker': w['ticker'],
                    'price': current,
                    'change': change,
                    'reason': w['reason'],
                    'recommendation': recommendation
                })
        except Exception as e:
            result.append({
                'ticker': w['ticker'],
                'price': 0,
                'change': 0,
                'reason': w['reason'],
                'recommendation': 'unknown'
            })
    
    return result


def get_volume_analysis(ticker: str) -> Dict:
    """取得成交量分析"""
    try:
        data = yf.Ticker(ticker).history(period='30d')
        if len(data) >= 5:
            volumes = data['Volume'].tolist()
            avg_volume = sum(volumes[:-1]) / len(volumes[:-1])  # 不含今天
            
            recent_volumes = volumes[-3:]  # 近3日
            recent_avg = sum(recent_volumes) / len(recent_volumes)
            
            above_avg = recent_avg > avg_volume
            
            # 計算變化趨勢
            if len(recent_volumes) >= 3:
                trend = '↗️' if recent_volumes[-1] > recent_volumes[-2] > recent_volumes[-3] else \
                        '↘️' if recent_volumes[-1] < recent_volumes[-2] < recent_volumes[-3] else \
                        '→'
            else:
                trend = '→'
            
            return {
                'avg_volume': avg_volume,
                'recent_volume': recent_avg,
                'above_avg': above_avg,
                'trend': trend,
                'pct_of_avg': (recent_avg / avg_volume * 100) if avg_volume > 0 else 100
            }
    except:
        pass
    
    return {'avg_volume': 0, 'recent_volume': 0, 'above_avg': False, 'trend': '→', 'pct_of_avg': 100}


class EmailReporter:
    """Email 發送器 - 使用 gog"""
    
    def send_email(self, to_emails: List[str], subject: str, html_content: str) -> bool:
        """使用 gog 發送 Email"""
        try:
            cmd = [
                'gog', 'gmail', 'send',
                '--to', ','.join(to_emails),
                '--subject', subject,
                '--body-html', html_content,
                '--account', GOG_ACCOUNT
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ Email 已發送到: {', '.join(to_emails)}")
                return True
            else:
                print(f"❌ Email 發送失敗: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Email 發送失敗: {e}")
            return False


def generate_html_report(portfolio_data: Dict, holdings_data: List[Dict],
                        market_indices: Dict, watchlist_data: List[Dict],
                        market_summary: str = "") -> str:
    """生成 HTML 報告 v2"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # === 大盤指數 ===
    indices_html = ""
    for name, data in market_indices.items():
        if data['price'] > 0:
            change = data['change']
            color = '#22c55e' if change > 0 else '#ef4444' if change < 0 else '#6b7280'
            emoji = '📈' if change > 0 else '📉' if change < 0 else '➡️'
            indices_html += f"""
                <div class="index-item">
                    <span class="index-name">{name}</span>
                    <span class="index-price">${data['price']:,.2f}</span>
                    <span class="index-change" style="color: {color};">{emoji} {change:+.2f}%</span>
                </div>
            """
    
    # === 持股總覽 ===
    total_value = portfolio_data.get('total_value', 0)
    cash = portfolio_data.get('cash', 0)
    stock_value = total_value - cash
    change_pct = portfolio_data.get('change_pct', 0)
    change_amount = portfolio_data.get('change_amount', 0)
    prev_value = portfolio_data.get('prev_total_value', 0)
    
    if change_pct > 0:
        change_color = '#22c55e'
        change_emoji = '📈'
    elif change_pct < 0:
        change_color = '#ef4444'
        change_emoji = '📉'
    else:
        change_color = '#6b7280'
        change_emoji = '➡️'
    
    # === 持股明細 ===
    # 分開持股和現金
    stock_holdings = [h for h in holdings_data if h.get('ticker') != 'CASH']
    cash_data = next((h for h in holdings_data if h.get('ticker') == 'CASH'), None)
    
    holdings_html = ""
    total_pnl = 0
    total_cost = 0
    
    for h in stock_holdings:
        ticker = h.get('ticker', '')
        change = h.get('change_pct', 0)
        value = h.get('current_value', 0)
        pnl = h.get('unrealized_pnl', 0)
        shares = h.get('shares', 0)
        avg_cost = h.get('cost', 0)
        current_price = h.get('current_price', 0)
        recommendation = h.get('recommendation', 'hold')
        
        total_pnl += pnl
        total_cost += avg_cost * shares
        
        # 燈號
        if recommendation == 'buy':
            signal = '🟢'
        elif recommendation == 'sell':
            signal = '🔴'
        else:
            signal = '🔵'
        
        # 漲跌顏色
        if change > 0:
            h_color = '#22c55e'
        elif change < 0:
            h_color = '#ef4444'
        else:
            h_color = '#6b7280'
        
        # 損益顏色
        pnl_color = '#22c55e' if pnl > 0 else '#ef4444'
        
        # 成交量分析
        vol = h.get('volume_analysis', {})
        vol_indicator = ""
        if vol.get('above_avg'):
            vol_indicator = f"<span class='vol-indicator' title='成交量 {vol.get('pct_of_avg', 0):.0f}% of avg'>{vol.get('trend', '→')}*</span>"
        else:
            vol_indicator = f"<span class='vol-normal'>{vol.get('trend', '→')}</span>"
        
        holdings_html += f"""
        <tr>
            <td><strong>{signal} {ticker}</strong></td>
            <td>{shares:,.0f}</td>
            <td>${current_price:.2f}</td>
            <td>${avg_cost:.2f}</td>
            <td>${value:,.2f}</td>
            <td style="color: {h_color};">{change:+.2f}% {vol_indicator}</td>
            <td style="color: {pnl_color};">${pnl:>+10,.2f}</td>
            <td style="color: {pnl_color};">{pnl/(avg_cost*shares)*100:+.1f}%</td>
        </tr>
        """
    
    # 持股合計
    holdings_html += f"""
    <tr style="background: #f3f4f6; font-weight: bold;">
        <td>📊 持股合計</td>
        <td></td>
        <td></td>
        <td></td>
        <td>${stock_value:,.2f}</td>
        <td></td>
        <td style="color: {'#22c55e' if total_pnl > 0 else '#ef4444'};">${total_pnl:>+10,.2f}</td>
        <td style="color: {'#22c55e' if total_pnl > 0 else '#ef4444'};">{total_pnl/total_cost*100:+.1f}%</td>
    </tr>
    """
    
    # 現金 (在最下方，佔市值欄位)
    if cash_data:
        cash_value = cash_data.get('current_value', 0)
        holdings_html += f"""
        <tr style="background: #fef3c7;">
            <td><strong>💵 現金</strong></td>
            <td></td>
            <td></td>
            <td></td>
            <td>${cash_value:,.2f}</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        """
    
    # === 當日信號 ===
    buy_signals = portfolio_data.get('buy_signals', [])
    sell_signals = portfolio_data.get('sell_signals', [])
    
    buy_html = ""
    if buy_signals:
        buy_html = " <span style='color:#22c55e;'>" + " </span> <span style='color:#22c55e;'>".join([f"🟢 {s}" for s in buy_signals]) + "</span>"
    else:
        buy_html = "無"
    
    sell_html = ""
    if sell_signals:
        sell_html = " <span style='color:#ef4444;'>" + " </span> <span style='color:#ef4444;'>".join([f"🔴 {s}" for s in sell_signals]) + "</span>"
    else:
        sell_html = "無"
    
    # === 追蹤清單 ===
    watchlist_html = ""
    for w in watchlist_data:
        w_change = w.get('change', 0)
        w_color = '#22c55e' if w_change > 0 else '#ef4444' if w_change < 0 else '#6b7280'
        w_emoji = '📈' if w_change > 0 else '📉' if w_change < 0 else '➡️'
        
        rec = w.get('recommendation', 'unknown')
        if rec == 'buy':
            rec_emoji = '🟢'
        elif rec == 'sell':
            rec_emoji = '🔴'
        else:
            rec_emoji = '🔵'
        
        watchlist_html += f"""
        <tr>
            <td><strong>{rec_emoji} {w['ticker']}</strong></td>
            <td>${w.get('price', 0):.2f}</td>
            <td style="color: {w_color};">{w_emoji} {w_change:+.2f}%</td>
            <td>{w.get('reason', '')}</td>
        </tr>
        """
    
    # === 市場結語 ===
    market_summary_html = market_summary if market_summary else "<p>市場分析資料讀取中...</p>"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Investage 每日報告 - {today}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #fafafa; }}
            h1 {{ color: #1f2937; border-bottom: 3px solid #3b82f6; padding-bottom: 10px; }}
            h2 {{ color: #374151; margin-top: 30px; border-left: 4px solid #3b82f6; padding-left: 10px; }}
            h3 {{ color: #4b5563; margin-top: 20px; }}
            
            .market-indices {{ background: linear-gradient(135deg, #1f2937, #374151); padding: 20px; border-radius: 12px; margin: 20px 0; }}
            .index-item {{ display: inline-block; margin: 10px 25px 10px 0; }}
            .index-name {{ color: #9ca3af; font-size: 12px; display: block; }}
            .index-price {{ color: white; font-size: 18px; font-weight: bold; display: block; }}
            .index-change {{ font-size: 14px; display: block; }}
            
            .summary {{ background: white; padding: 25px; border-radius: 12px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .metric {{ display: inline-block; margin: 15px 30px 15px 0; }}
            .metric-label {{ color: #6b7280; font-size: 13px; text-transform: uppercase; }}
            .metric-value {{ font-size: 28px; font-weight: bold; color: #1f2937; }}
            .metric-small {{ font-size: 16px; color: #6b7280; }}
            
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; background: white; border-radius: 8px; overflow: hidden; }}
            th {{ background: #3b82f6; color: white; padding: 12px 10px; text-align: left; font-weight: 600; }}
            td {{ padding: 12px 10px; border-bottom: 1px solid #e5e7eb; }}
            tr:hover {{ background: #f9fafb; }}
            tr:last-child td {{ border-bottom: none; }}
            
            .vol-indicator {{ color: #f59e0b; font-weight: bold; }}
            .vol-normal {{ color: #9ca3af; }}
            
            .buy-signal {{ background: #dcfce7; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #22c55e; }}
            .sell-signal {{ background: #fee2e2; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #ef4444; }}
            
            .watchlist {{ background: white; padding: 20px; border-radius: 8px; margin: 15px 0; }}
            
            .market-summary {{ background: linear-gradient(135deg, #fef3c7, #fde68a); padding: 25px; border-radius: 12px; margin: 20px 0; }}
            .market-summary h2 {{ border-left-color: #f59e0b; }}
            
            .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #e5e7eb; color: #6b7280; font-size: 12px; text-align: center; }}
            
            .legend {{ background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 15px 0; font-size: 13px; }}
            .legend-item {{ display: inline-block; margin: 5px 15px 5px 0; }}
        </style>
    </head>
    <body>
        <h1>📊 Investage 每日投資報告</h1>
        <p style="color: #6b7280;">{today} | 美股收盤後自動更新</p>
        
        <!-- 大盤概況 -->
        <h2>🌐 大盤概況</h2>
        <div class="market-indices">
            {indices_html}
        </div>
        
        <!-- 持股總覽 -->
        <h2>💼 持股總覽</h2>
        <div class="summary">
            <div class="metric">
                <div class="metric-label">總資產</div>
                <div class="metric-value">${total_value:,.2f}</div>
            </div>
            <div class="metric">
                <div class="metric-label">持股價值</div>
                <div class="metric-value">${stock_value:,.2f}</div>
            </div>
            <div class="metric">
                <div class="metric-label">現金</div>
                <div class="metric-value">${cash:,.2f}</div>
            </div>
            <div class="metric">
                <div class="metric-label">今日變化</div>
                <div class="metric-value" style="color: {change_color};">{change_emoji} {change_pct:+.2f}%</div>
                <div class="metric-small">${change_amount:+,.2f}</div>
            </div>
            <div class="metric">
                <div class="metric-label">昨日總值</div>
                <div class="metric-value" style="color: #6b7280;">${prev_value:,.2f}</div>
            </div>
        </div>
        
        <!-- 圖例 -->
        <div class="legend">
            <span class="legend-item">🟢 Buy 買入</span>
            <span class="legend-item">🔵 Hold 持有</span>
            <span class="legend-item">🔴 Sell 賣出</span>
            <span class="legend-item">→* 放量</span>
        </div>
        
        <!-- 持股明細 -->
        <h2>📈 持股明細</h2>
        <table>
            <thead>
                <tr>
                    <th>股票</th>
                    <th>股數</th>
                    <th>現價</th>
                    <th>成本</th>
                    <th>市值</th>
                    <th>今日漲跌</th>
                    <th>未實現損益</th>
                    <th>報酬率</th>
                </tr>
            </thead>
            <tbody>
                {holdings_html}
            </tbody>
        </table>
        
        <!-- 當日信號 -->
        <h2>🎯 當日信號</h2>
        <div class="buy-signal">
            <strong>🟢 買入信號：</strong> {buy_html}
        </div>
        <div class="sell-signal">
            <strong>🔴 賣出信號：</strong> {sell_html}
        </div>
        
        <!-- 追蹤標的 -->
        <h2>👀 追蹤標的</h2>
        <div class="watchlist">
            <table>
                <thead>
                    <tr>
                        <th>股票</th>
                        <th>現價</th>
                        <th>漲跌</th>
                        <th>備註</th>
                    </tr>
                </thead>
                <tbody>
                    {watchlist_html}
                </tbody>
            </table>
        </div>
        
        <!-- 市場結語 -->
        <h2>📝 本日市場結語</h2>
        <div class="market-summary">
            {market_summary_html}
        </div>
        
        <div class="footer">
            <p>此報告由 <strong>Investage</strong> 自動生成 | 數據來源：Yahoo Finance</p>
            <p>⚠️ 本報告不構成投資建議，投資有風險，請謹慎評估</p>
        </div>
    </body>
    </html>
    """
    return html


def generate_market_summary(market_indices: Dict, watchlist: List[Dict]) -> str:
    """生成市場結語"""
    summary_parts = []
    
    # 三大指數分析
    sp500 = market_indices.get('S&P 500', {}).get('change', 0)
    nasdaq = market_indices.get('Nasdaq', {}).get('change', 0)
    dow = market_indices.get('Dow Jones', {}).get('change', 0)
    vix = market_indices.get('VIX', {}).get('price', 0)
    
    if sp500 > 0.5:
        summary_parts.append(f"美股三大指數全數上漲，S&P 500 表現強勁 ({sp500:+.2f}%)")
    elif sp500 < -0.5:
        summary_parts.append(f"美股三大指數全數下跌，S&P 500 回調明顯 ({sp500:+.2f}%)")
    else:
        summary_parts.append(f"美股主要指數漲跌互現，S&P 500 變化不大 ({sp500:+.2f}%)")
    
    # VIX 風險情緒
    if vix > 25:
        summary_parts.append(f"VIX 升至 {vix:.1f}，市場避險情緒升溫")
    elif vix < 15:
        summary_parts.append(f"VIX 維持低檔 {vix:.1f}，市場風險偏好樂觀")
    else:
        summary_parts.append(f"VIX 為 {vix:.1f}，市場情緒中性")
    
    # 追蹤標的表現
    if watchlist:
        winners = [w['ticker'] for w in watchlist if w.get('change', 0) > 2]
        losers = [w['ticker'] for w in watchlist if w.get('change', 0) < -2]
        
        if winners:
            summary_parts.append(f"追蹤標的中 {', '.join(winners)} 表現突出")
        if losers:
            summary_parts.append(f"追蹤標的中 {', '.join(losers)} 回調較大")
    
    summary_html = "<ul>"
    for part in summary_parts:
        summary_html += f"<li>{part}</li>"
    summary_html += "</ul>"
    
    return summary_html


def main():
    """主程式"""
    import sys
    
    # 取得持股資料
    conn = psycopg2.connect(host='localhost', database='investage', user='george')
    cur = conn.cursor()
    
    cur.execute("""
        SELECT h.ticker, h.shares, h.avg_cost, s.company_name
        FROM holdings h
        JOIN stocks s ON h.ticker = s.ticker
        ORDER BY h.ticker
    """)
    holdings = cur.fetchall()
    
    portfolio = {
        'holdings': [],
        'total_value': 0,
        'cash': 0,
        'prev_total_value': 0,
        'change_pct': 0,
        'change_amount': 0,
        'buy_signals': [],
        'sell_signals': []
    }
    
    for ticker, shares, avg_cost, company in holdings:
        if ticker == 'CASH':
            cash = float(shares)
            portfolio['cash'] = cash
            portfolio['total_value'] += cash
            portfolio['prev_total_value'] += cash
            portfolio['holdings'].append({
                'ticker': 'CASH',
                'shares': cash,
                'current_price': 1.0,
                'cost': 1.0,
                'current_value': cash,
                'prev_value': cash,
                'unrealized_pnl': 0,
                'change_pct': 0,
                'recommendation': 'hold',
                'volume_analysis': {}
            })
            continue
            
        try:
            shares = float(shares)
            avg_cost = float(avg_cost)
            
            data = yf.Ticker(ticker).history(period='5d')
            
            if len(data) >= 2:
                current_price = float(data['Close'].iloc[-1])
                prev_price = float(data['Close'].iloc[-2])
                change_pct = (current_price - prev_price) / prev_price * 100
            elif len(data) == 1:
                current_price = float(data['Close'].iloc[-1])
                prev_price = current_price
                change_pct = 0
            else:
                current_price = avg_cost  # 用成本價
                prev_price = avg_cost
                change_pct = 0
            
            current_value = shares * current_price
            prev_value = shares * prev_price
            pnl = current_value - (avg_cost * shares)
            
            # 取得推薦
            try:
                info = yf.Ticker(ticker).info
                recommendation = info.get('recommendationKey', 'hold')
            except:
                recommendation = 'hold'
            
            # 成交量分析
            vol_analysis = get_volume_analysis(ticker)
            
            portfolio['holdings'].append({
                'ticker': ticker,
                'shares': shares,
                'current_price': current_price,
                'cost': avg_cost,
                'current_value': current_value,
                'prev_value': prev_value,
                'unrealized_pnl': pnl,
                'change_pct': change_pct,
                'recommendation': recommendation,
                'volume_analysis': vol_analysis
            })
            
            portfolio['total_value'] += current_value
            portfolio['prev_total_value'] += prev_value
        except Exception as e:
            print(f"{ticker}: Error - {e}")
    
    # 計算變化
    if portfolio['prev_total_value'] > 0:
        portfolio['change_pct'] = (
            (portfolio['total_value'] - portfolio['prev_total_value']) / 
            portfolio['prev_total_value'] * 100
        )
        portfolio['change_amount'] = portfolio['total_value'] - portfolio['prev_total_value']
    
    conn.close()
    
    # 取得大盤指數
    print("取得大盤資料...")
    market_indices = get_market_indices()
    
    # 取得追蹤清單
    print("取得追蹤標的...")
    watchlist_data = get_watchlist()
    
    # 生成市場結語
    market_summary = generate_market_summary(market_indices, watchlist_data)
    
    # 生成報告
    html = generate_html_report(portfolio, portfolio['holdings'], 
                               market_indices, watchlist_data, market_summary)
    
    # 發送
    reporter = EmailReporter()
    subject = f"📊 Investage 每日報告 - {datetime.now().strftime('%Y-%m-%d')}"
    result = reporter.send_email(['george@precaster.com.tw', 'ching@precaster.com.tw'], subject, html)
    
    print(f"\n總值: ${portfolio['total_value']:,.2f}")
    print(f"變化: {portfolio['change_pct']:+.2f}% (${portfolio['change_amount']:+,.2f})")
    
    return result


if __name__ == "__main__":
    main()
