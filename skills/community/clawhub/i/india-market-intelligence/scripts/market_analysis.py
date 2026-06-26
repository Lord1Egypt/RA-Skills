#!/usr/bin/env python3
# /// script
# dependencies = [
#   "yfinance",
#   "pandas",
#   "rich",
#   "requests",
#   "beautifulsoup4",
#   "feedparser",
#   "numpy"
# ]
# ///

import sys
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich import box
import feedparser
from typing import List, Dict, Tuple
import json

console = Console()

# ============================================================================
# MARKET INDICES CONFIGURATION
# ============================================================================

GLOBAL_INDICES = {
    "US Markets": {
        "GSPC": "S&P 500",
        "DJI": "Dow Jones",
        "IXIC": "NASDAQ",
        "RUT": "Russell 2000",
        "VIX": "VIX (Fear Index)"
    },
    "Indian Markets": {
        "NSEI": "NIFTY 50",
        "NSEBANK": "NIFTY Bank",
        "BSESN": "BSE SENSEX"
    },
    "European Markets": {
        "FTSE": "FTSE 100",
        "GDAXI": "DAX",
        "FCHI": "CAC 40"
    },
    "Asian Markets": {
        "N225": "Nikkei 225",
        "HSI": "Hang Seng",
        "000001.SS": "Shanghai Composite",
        "STI": "Straits Times"
    }
}

COMMODITIES = {
    "GC=F": "Gold",
    "SI=F": "Silver",
    "CL=F": "Crude Oil WTI",
    "BZ=F": "Brent Crude"
}

CURRENCIES = {
    "USDINR=X": "USD/INR",
    "DX-Y.NYB": "Dollar Index",
    "EURUSD=X": "EUR/USD",
    "GBPUSD=X": "GBP/USD"
}

INDIAN_STOCKS = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "HDFCBANK.NS": "HDFC Bank",
    "INFY.NS": "Infosys",
    "ICICIBANK.NS": "ICICI Bank",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "ITC.NS": "ITC Limited",
    "SBIN.NS": "State Bank of India",
    "BHARTIARTL.NS": "Bharti Airtel",
    "KOTAKBANK.NS": "Kotak Mahindra Bank"
}

# RSS News Feeds
NEWS_FEEDS = {
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "Moneycontrol": "https://www.moneycontrol.com/rss/latestnews.xml",
    "Economic Times": "https://economictimes.indiatimes.com/rssfeedstopstories.cms",
    "Bloomberg Markets": "https://www.bloomberg.com/feed/podcast/bloomberg-markets.xml",
}

# ============================================================================
# DATA FETCHING FUNCTIONS
# ============================================================================

def fetch_market_data(symbols: Dict[str, str]) -> pd.DataFrame:
    """Fetch current market data for given symbols."""
    data = []
    for symbol, name in symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.history(period="2d")
            
            if len(info) >= 2:
                current = info['Close'].iloc[-1]
                previous = info['Close'].iloc[-2]
                change = current - previous
                pct_change = (change / previous) * 100
                
                data.append({
                    "Symbol": symbol,
                    "Name": name,
                    "Price": current,
                    "Change": change,
                    "Change%": pct_change,
                    "Volume": info['Volume'].iloc[-1] if 'Volume' in info else 0
                })
        except Exception as e:
            console.print(f"[yellow]Warning: Could not fetch {symbol}: {e}[/yellow]")
    
    return pd.DataFrame(data)


def fetch_historical_data(symbol: str, period: str = "1mo") -> pd.DataFrame:
    """Fetch historical data for a symbol."""
    try:
        ticker = yf.Ticker(symbol)
        return ticker.history(period=period)
    except:
        return pd.DataFrame()


def get_market_news(max_items: int = 10, india_only: bool = False) -> List[Dict]:
    """Fetch latest market news from RSS feeds."""
    news_items = []
    
    feeds_to_check = NEWS_FEEDS.copy()
    if india_only:
        feeds_to_check = {k: v for k, v in NEWS_FEEDS.items() 
                         if k in ["Moneycontrol", "Economic Times"]}
    
    for source, url in feeds_to_check.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:max_items]:
                news_items.append({
                    "source": source,
                    "title": entry.get('title', 'No title'),
                    "link": entry.get('link', ''),
                    "published": entry.get('published', 'Unknown'),
                    "summary": entry.get('summary', '')[:200] + "..."
                })
        except Exception as e:
            console.print(f"[yellow]Could not fetch from {source}: {e}[/yellow]")
    
    return news_items[:max_items]


def get_ticker_news(symbol: str, max_items: int = 5) -> List[Dict]:
    """Get news for a specific ticker using yfinance."""
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news
        
        news_items = []
        for item in news[:max_items]:
            news_items.append({
                "title": item.get('title', 'No title'),
                "publisher": item.get('publisher', 'Unknown'),
                "link": item.get('link', ''),
                "published": datetime.fromtimestamp(item.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M')
            })
        return news_items
    except:
        return []


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def calculate_market_sentiment(indices_df: pd.DataFrame) -> str:
    """Calculate overall market sentiment based on major indices."""
    if indices_df.empty:
        return "NEUTRAL"
    
    avg_change = indices_df['Change%'].mean()
    
    if avg_change > 1:
        return "BULLISH"
    elif avg_change < -1:
        return "BEARISH"
    else:
        return "NEUTRAL"


def analyze_indian_market(nifty_symbol: str = "^NSEI", sensex_symbol: str = "^BSESN") -> Dict:
    """Detailed analysis of Indian market."""
    analysis = {}
    
    # Fetch NIFTY and SENSEX data
    nifty_data = fetch_historical_data(nifty_symbol, "5d")
    sensex_data = fetch_historical_data(sensex_symbol, "5d")
    
    if not nifty_data.empty:
        nifty_current = nifty_data['Close'].iloc[-1]
        nifty_prev = nifty_data['Close'].iloc[-2]
        nifty_change = ((nifty_current - nifty_prev) / nifty_prev) * 100
        
        analysis['nifty'] = {
            'current': nifty_current,
            'change_pct': nifty_change,
            'high_5d': nifty_data['High'].max(),
            'low_5d': nifty_data['Low'].min(),
            'volume': nifty_data['Volume'].iloc[-1]
        }
    
    if not sensex_data.empty:
        sensex_current = sensex_data['Close'].iloc[-1]
        sensex_prev = sensex_data['Close'].iloc[-2]
        sensex_change = ((sensex_current - sensex_prev) / sensex_prev) * 100
        
        analysis['sensex'] = {
            'current': sensex_current,
            'change_pct': sensex_change,
            'high_5d': sensex_data['High'].max(),
            'low_5d': sensex_data['Low'].min(),
            'volume': sensex_data['Volume'].iloc[-1]
        }
    
    # Fetch top Indian stocks
    stocks_df = fetch_market_data(INDIAN_STOCKS)
    if not stocks_df.empty:
        analysis['top_gainers'] = stocks_df.nlargest(3, 'Change%')[['Name', 'Change%']].to_dict('records')
        analysis['top_losers'] = stocks_df.nsmallest(3, 'Change%')[['Name', 'Change%']].to_dict('records')
    
    return analysis


def analyze_global_correlations(indices_data: pd.DataFrame) -> Dict:
    """Analyze correlations between major markets."""
    correlations = {}
    
    if not indices_data.empty:
        # Simple correlation analysis based on direction
        us_indices = indices_data[indices_data['Symbol'].isin(['^GSPC', '^DJI', '^IXIC'])]
        indian_indices = indices_data[indices_data['Symbol'].isin(['^NSEI', '^BSESN'])]
        
        if not us_indices.empty:
            us_avg_change = us_indices['Change%'].mean()
            correlations['us_market_direction'] = 'UP' if us_avg_change > 0 else 'DOWN'
            correlations['us_avg_change'] = us_avg_change
        
        if not indian_indices.empty:
            india_avg_change = indian_indices['Change%'].mean()
            correlations['india_market_direction'] = 'UP' if india_avg_change > 0 else 'DOWN'
            correlations['india_avg_change'] = india_avg_change
    
    return correlations


def generate_market_outlook(all_data: Dict) -> str:
    """Generate AI-powered market outlook."""
    outlook = []
    
    # Global sentiment
    if 'global_sentiment' in all_data:
        sentiment = all_data['global_sentiment']
        outlook.append(f"Global Market Sentiment: {sentiment}")
        
        if sentiment == "BULLISH":
            outlook.append("• Markets are showing positive momentum across major indices")
        elif sentiment == "BEARISH":
            outlook.append("• Markets are experiencing selling pressure")
        else:
            outlook.append("• Markets are consolidating with mixed signals")
    
    # Indian market specific
    if 'indian_analysis' in all_data:
        india = all_data['indian_analysis']
        if 'nifty' in india:
            change = india['nifty']['change_pct']
            if change > 0.5:
                outlook.append(f"• Indian markets are positive with NIFTY up {change:.2f}%")
            elif change < -0.5:
                outlook.append(f"• Indian markets are under pressure with NIFTY down {change:.2f}%")
            else:
                outlook.append(f"• Indian markets are range-bound with NIFTY {change:+.2f}%")
    
    # Commodities impact
    if 'commodities' in all_data and not all_data['commodities'].empty:
        gold_data = all_data['commodities'][all_data['commodities']['Symbol'] == 'GC=F']
        oil_data = all_data['commodities'][all_data['commodities']['Symbol'] == 'CL=F']
        
        if not gold_data.empty:
            gold_change = gold_data.iloc[0]['Change%']
            if abs(gold_change) > 1:
                direction = "rising" if gold_change > 0 else "falling"
                outlook.append(f"• Gold is {direction} {abs(gold_change):.2f}%, indicating {'risk-off' if gold_change > 0 else 'risk-on'} sentiment")
        
        if not oil_data.empty:
            oil_change = oil_data.iloc[0]['Change%']
            if abs(oil_change) > 2:
                direction = "surging" if oil_change > 2 else "declining"
                outlook.append(f"• Crude oil {direction} {abs(oil_change):.2f}%, may impact inflation expectations")
    
    # Currency impact
    if 'currencies' in all_data and not all_data['currencies'].empty:
        usdinr_data = all_data['currencies'][all_data['currencies']['Symbol'] == 'USDINR=X']
        if not usdinr_data.empty:
            inr_change = usdinr_data.iloc[0]['Change%']
            if abs(inr_change) > 0.3:
                direction = "weakening" if inr_change > 0 else "strengthening"
                outlook.append(f"• Rupee {direction} against Dollar, {inr_change:+.2f}%")
    
    return "\n".join(outlook) if outlook else "Insufficient data for market outlook"


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_market_table(df: pd.DataFrame, title: str):
    """Display market data in a formatted table."""
    if df.empty:
        console.print(f"[yellow]No data available for {title}[/yellow]")
        return
    
    table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan", width=25)
    table.add_column("Symbol", style="dim", width=15)
    table.add_column("Price", justify="right", style="white")
    table.add_column("Change", justify="right")
    table.add_column("Change %", justify="right")
    
    for _, row in df.iterrows():
        change_color = "green" if row['Change'] >= 0 else "red"
        change_symbol = "+" if row['Change'] >= 0 else ""
        
        table.add_row(
            row['Name'],
            row['Symbol'],
            f"{row['Price']:.2f}",
            f"[{change_color}]{change_symbol}{row['Change']:.2f}[/{change_color}]",
            f"[{change_color}]{change_symbol}{row['Change%']:.2f}%[/{change_color}]"
        )
    
    console.print(table)
    console.print()


def display_news(news_items: List[Dict], title: str = "Market News"):
    """Display news items in a formatted panel."""
    if not news_items:
        console.print(f"[yellow]No news available[/yellow]")
        return
    
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", expand=False))
    
    for i, item in enumerate(news_items, 1):
        source = item.get('source', item.get('publisher', 'Unknown'))
        title = item['title']
        link = item.get('link', '')
        published = item.get('published', '')
        
        console.print(f"\n[bold]{i}. {title}[/bold]")
        console.print(f"[dim]Source: {source} | {published}[/dim]")
        if link:
            console.print(f"[blue underline]{link}[/blue underline]")
    
    console.print()


def display_indian_analysis(analysis: Dict):
    """Display detailed Indian market analysis."""
    console.print(Panel("[bold cyan]Indian Market Analysis[/bold cyan]", expand=False))
    
    if 'nifty' in analysis:
        nifty = analysis['nifty']
        change_color = "green" if nifty['change_pct'] >= 0 else "red"
        console.print(f"\n[bold]NIFTY 50:[/bold]")
        console.print(f"  Current: {nifty['current']:.2f}")
        console.print(f"  Change: [{change_color}]{nifty['change_pct']:+.2f}%[/{change_color}]")
        console.print(f"  5-Day High: {nifty['high_5d']:.2f}")
        console.print(f"  5-Day Low: {nifty['low_5d']:.2f}")
    
    if 'sensex' in analysis:
        sensex = analysis['sensex']
        change_color = "green" if sensex['change_pct'] >= 0 else "red"
        console.print(f"\n[bold]BSE SENSEX:[/bold]")
        console.print(f"  Current: {sensex['current']:.2f}")
        console.print(f"  Change: [{change_color}]{sensex['change_pct']:+.2f}%[/{change_color}]")
        console.print(f"  5-Day High: {sensex['high_5d']:.2f}")
        console.print(f"  5-Day Low: {sensex['low_5d']:.2f}")
    
    if 'top_gainers' in analysis:
        console.print(f"\n[bold green]Top Gainers:[/bold green]")
        for stock in analysis['top_gainers']:
            console.print(f"  • {stock['Name']}: [green]+{stock['Change%']:.2f}%[/green]")
    
    if 'top_losers' in analysis:
        console.print(f"\n[bold red]Top Losers:[/bold red]")
        for stock in analysis['top_losers']:
            console.print(f"  • {stock['Name']}: [red]{stock['Change%']:.2f}%[/red]")
    
    console.print()


# ============================================================================
# COMMAND HANDLERS
# ============================================================================

def cmd_overview():
    """Display global market overview."""
    console.print("\n[bold cyan]🌍 GLOBAL MARKET OVERVIEW[/bold cyan]\n")
    
    # Fetch all market data
    all_indices = {}
    for region, indices in GLOBAL_INDICES.items():
        all_indices.update(indices)
    
    indices_df = fetch_market_data(all_indices)
    commodities_df = fetch_market_data(COMMODITIES)
    currencies_df = fetch_market_data(CURRENCIES)
    
    # Display by region
    for region, indices in GLOBAL_INDICES.items():
        region_df = indices_df[indices_df['Symbol'].isin(indices.keys())]
        if not region_df.empty:
            display_market_table(region_df, f"📊 {region}")
    
    # Display commodities and currencies
    display_market_table(commodities_df, "💰 Commodities")
    display_market_table(currencies_df, "💱 Currencies")
    
    # Market sentiment
    sentiment = calculate_market_sentiment(indices_df)
    sentiment_color = "green" if sentiment == "BULLISH" else "red" if sentiment == "BEARISH" else "yellow"
    console.print(Panel(
        f"[bold {sentiment_color}]Market Sentiment: {sentiment}[/bold {sentiment_color}]",
        title="Overall Sentiment",
        expand=False
    ))


def cmd_india():
    """Display Indian market analysis."""
    console.print("\n[bold cyan]🇮🇳 INDIAN MARKET ANALYSIS[/bold cyan]\n")
    
    analysis = analyze_indian_market()
    display_indian_analysis(analysis)
    
    # Fetch and display Indian market news
    news = get_market_news(max_items=5, india_only=True)
    display_news(news, "📰 Indian Market News")


def cmd_news(india_only: bool = False, geopolitical: bool = False, ticker: str = None):
    """Display market news."""
    console.print("\n[bold cyan]📰 MARKET NEWS[/bold cyan]\n")
    
    if ticker:
        news = get_ticker_news(ticker, max_items=10)
        display_news(news, f"News for {ticker}")
    else:
        news = get_market_news(max_items=15, india_only=india_only)
        
        if geopolitical:
            # Filter for geopolitical keywords
            geo_keywords = ['fed', 'election', 'war', 'trade', 'tariff', 'sanctions', 
                           'central bank', 'rbi', 'ecb', 'boj', 'conflict', 'treaty']
            news = [n for n in news if any(kw in n['title'].lower() for kw in geo_keywords)]
            display_news(news, "🌐 Geopolitical News Affecting Markets")
        else:
            display_news(news, "Market News")


def cmd_geopolitical():
    """Display geopolitical events and their market impact."""
    console.print("\n[bold cyan]🌐 GEOPOLITICAL EVENTS MONITOR[/bold cyan]\n")
    
    console.print(Panel(
        "[bold]Tracking geopolitical events that may impact markets:[/bold]\n\n"
        "• Central Bank Policy Decisions (Fed, ECB, RBI, BoJ)\n"
        "• Major Elections & Political Changes\n"
        "• Trade Wars & Tariff Announcements\n"
        "• Regional Conflicts & Tensions\n"
        "• Economic Sanctions\n"
        "• International Treaties & Agreements",
        title="Event Categories",
        expand=False
    ))
    
    # Fetch geopolitical news
    cmd_news(geopolitical=True)
    
    # Display VIX (fear index)
    vix_df = fetch_market_data({"^VIX": "VIX (Fear Index)"})
    if not vix_df.empty:
        vix_level = vix_df.iloc[0]['Price']
        if vix_level < 15:
            risk = "[green]LOW[/green]"
            desc = "Markets are calm"
        elif vix_level < 25:
            risk = "[yellow]MODERATE[/yellow]"
            desc = "Some uncertainty in markets"
        else:
            risk = "[red]HIGH[/red]"
            desc = "Significant market fear/uncertainty"
        
        console.print(Panel(
            f"[bold]Current VIX Level: {vix_level:.2f}[/bold]\n"
            f"Risk Level: {risk}\n"
            f"Interpretation: {desc}",
            title="Market Fear Gauge",
            expand=False
        ))


def cmd_report(region: str = "global"):
    """Generate comprehensive market intelligence report."""
    console.print("\n[bold cyan]📊 COMPREHENSIVE MARKET INTELLIGENCE REPORT[/bold cyan]")
    console.print(f"[dim]Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n")
    
    # Gather all data
    all_data = {}
    
    # 1. Global indices
    all_indices = {}
    for reg, indices in GLOBAL_INDICES.items():
        all_indices.update(indices)
    indices_df = fetch_market_data(all_indices)
    all_data['indices'] = indices_df
    
    # 2. Commodities and currencies
    all_data['commodities'] = fetch_market_data(COMMODITIES)
    all_data['currencies'] = fetch_market_data(CURRENCIES)
    
    # 3. Market sentiment
    all_data['global_sentiment'] = calculate_market_sentiment(indices_df)
    
    # 4. Indian market analysis
    all_data['indian_analysis'] = analyze_indian_market()
    
    # Display report sections
    if region in ["global", "all"]:
        cmd_overview()
    
    if region in ["india", "global", "all"]:
        console.print("\n" + "="*80 + "\n")
        display_indian_analysis(all_data['indian_analysis'])
    
    # Market outlook
    console.print("="*80 + "\n")
    outlook = generate_market_outlook(all_data)
    console.print(Panel(outlook, title="[bold]Market Outlook & Analysis[/bold]", expand=False))
    
    # Latest news
    console.print("\n" + "="*80 + "\n")
    news = get_market_news(max_items=10)
    display_news(news, "📰 Top Market Headlines")
    
    # Recommendations
    console.print(Panel(
        "[bold]Key Takeaways:[/bold]\n\n"
        "1. Monitor global market sentiment and correlations\n"
        "2. Watch for geopolitical events that may cause volatility\n"
        "3. Track sector rotation and FII/DII activity in Indian markets\n"
        "4. Stay informed on central bank policy decisions\n"
        "5. Diversify across asset classes based on risk appetite\n\n"
        "[dim]⚠️  This is for informational purposes only, not financial advice.[/dim]",
        title="Trading Considerations",
        expand=False,
        border_style="yellow"
    ))


def cmd_sectors(india: bool = False):
    """Analyze sector performance."""
    console.print("\n[bold cyan]📈 SECTOR ANALYSIS[/bold cyan]\n")
    
    if india:
        # Indian sector indices
        sectors = {
            "^CNXIT": "IT",
            "^CNXBANK": "Banking",
            "^CNXPHARMA": "Pharma",
            "^CNXAUTO": "Auto",
            "^CNXFMCG": "FMCG",
            "^CNXMETAL": "Metals",
            "^CNXENERGY": "Energy",
            "^CNXREALTY": "Realty"
        }
        sector_df = fetch_market_data(sectors)
        display_market_table(sector_df, "Indian Sector Performance")
    else:
        console.print("[yellow]Global sector analysis - Feature coming soon![/yellow]")
        console.print("Tip: Use --india flag for Indian sector analysis")


def cmd_intermarket():
    """Analyze intermarket relationships."""
    console.print("\n[bold cyan]🔗 INTERMARKET ANALYSIS[/bold cyan]\n")
    
    # Fetch key assets
    assets = {
        "^GSPC": "S&P 500",
        "GC=F": "Gold",
        "^TNX": "10Y Treasury Yield",
        "DX-Y.NYB": "Dollar Index",
        "CL=F": "Crude Oil"
    }
    
    assets_df = fetch_market_data(assets)
    display_market_table(assets_df, "Key Asset Classes")
    
    console.print(Panel(
        "[bold]Intermarket Relationships:[/bold]\n\n"
        "• Stocks vs Bonds: Typically inverse correlation\n"
        "• Dollar vs Commodities: Strong dollar = weaker commodities\n"
        "• Gold vs Stocks: Risk-off asset, rises when stocks fall\n"
        "• Oil vs Inflation: Rising oil increases inflation expectations\n"
        "• VIX vs Stocks: Inverse (fear rises when stocks fall)",
        title="Market Correlations",
        expand=False
    ))


# ============================================================================
# ADVANCED ANALYTICS FUNCTIONS
# ============================================================================

def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    """Calculate RSI (Relative Strength Index)."""
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 50.0
    except:
        return 50.0


def calculate_volatility(prices: pd.Series, period: int = 20) -> float:
    """Calculate volatility (standard deviation of returns)."""
    try:
        returns = prices.pct_change()
        volatility = returns.rolling(window=period).std().iloc[-1] * 100
        return volatility if not pd.isna(volatility) else 0.0
    except:
        return 0.0


def calculate_momentum(prices: pd.Series, period: int = 10) -> float:
    """Calculate momentum indicator."""
    try:
        if len(prices) < period:
            return 0.0
        momentum = ((prices.iloc[-1] / prices.iloc[-period]) - 1) * 100
        return momentum
    except:
        return 0.0


def calculate_trend_strength(df: pd.DataFrame) -> Dict:
    """Calculate trend strength using multiple indicators."""
    try:
        close = df['Close']
        
        # Moving averages
        ma5 = close.rolling(window=5).mean().iloc[-1]
        ma20 = close.rolling(window=20).mean().iloc[-1]
        ma50 = close.rolling(window=50).mean().iloc[-1] if len(close) >= 50 else ma20
        current = close.iloc[-1]
        
        # Trend determination
        if current > ma5 > ma20:
            trend = "STRONG UPTREND"
            trend_score = 8
        elif current > ma5 and current > ma20:
            trend = "UPTREND"
            trend_score = 6
        elif current < ma5 < ma20:
            trend = "STRONG DOWNTREND"
            trend_score = 2
        elif current < ma5 and current < ma20:
            trend = "DOWNTREND"
            trend_score = 4
        else:
            trend = "SIDEWAYS"
            trend_score = 5
        
        return {
            'trend': trend,
            'score': trend_score,
            'ma5': ma5,
            'ma20': ma20,
            'ma50': ma50,
            'current': current
        }
    except:
        return {'trend': 'UNKNOWN', 'score': 5}


def calculate_market_probability(indices_data: pd.DataFrame, historical_data: Dict) -> Dict:
    """Calculate probability of market direction based on current conditions."""
    try:
        probabilities = {}
        
        # Calculate based on current momentum and volatility
        for symbol in ['^NSEI', '^BSESN', '^GSPC']:
            if symbol in historical_data:
                df = historical_data[symbol]
                if len(df) > 20:
                    # RSI analysis
                    rsi = calculate_rsi(df['Close'])
                    
                    # Momentum
                    momentum = calculate_momentum(df['Close'])
                    
                    # Volatility
                    volatility = calculate_volatility(df['Close'])
                    
                    # Calculate probability
                    bullish_prob = 50.0  # Base probability
                    
                    # Adjust based on RSI
                    if rsi < 30:
                        bullish_prob += 20  # Oversold
                    elif rsi > 70:
                        bullish_prob -= 20  # Overbought
                    elif 40 < rsi < 60:
                        bullish_prob += 5  # Neutral
                    
                    # Adjust based on momentum
                    if momentum > 2:
                        bullish_prob += 10
                    elif momentum < -2:
                        bullish_prob -= 10
                    
                    # Adjust based on volatility
                    if volatility > 3:
                        bullish_prob -= 5  # High volatility = more risk
                    
                    # Clamp between 0 and 100
                    bullish_prob = max(0, min(100, bullish_prob))
                    
                    probabilities[symbol] = {
                        'bullish': bullish_prob,
                        'bearish': 100 - bullish_prob,
                        'rsi': rsi,
                        'momentum': momentum,
                        'volatility': volatility
                    }
        
        return probabilities
    except Exception as e:
        return {}


def calculate_risk_score(all_data: Dict) -> Dict:
    """Calculate comprehensive risk score based on multiple factors."""
    risk_factors = []
    risk_score = 5  # Base score (1-10, where 10 is highest risk)
    
    try:
        # VIX analysis
        if 'indices' in all_data and not all_data['indices'].empty:
            vix_data = all_data['indices'][all_data['indices']['Symbol'] == '^VIX']
            if not vix_data.empty:
                vix_level = vix_data.iloc[0]['Price']
                if vix_level > 30:
                    risk_score += 3
                    risk_factors.append(f"VIX extremely high ({vix_level:.1f})")
                elif vix_level > 25:
                    risk_score += 2
                    risk_factors.append(f"VIX elevated ({vix_level:.1f})")
                elif vix_level > 20:
                    risk_score += 1
                    risk_factors.append(f"VIX moderately high ({vix_level:.1f})")
                else:
                    risk_score -= 1
                    risk_factors.append(f"VIX low ({vix_level:.1f}) - calm market")
        
        # Market decline analysis
        if 'indices' in all_data and not all_data['indices'].empty:
            major_indices = all_data['indices'][all_data['indices']['Symbol'].isin(['^GSPC', '^NSEI', '^DJI'])]
            declining = (major_indices['Change%'] < -1.5).sum()
            if declining >= 2:
                risk_score += 2
                risk_factors.append(f"{declining} major indices down >1.5%")
        
        # Currency stress
        if 'currencies' in all_data and not all_data['currencies'].empty:
            usdinr = all_data['currencies'][all_data['currencies']['Symbol'] == 'USDINR=X']
            if not usdinr.empty and abs(usdinr.iloc[0]['Change%']) > 0.5:
                risk_score += 1
                risk_factors.append(f"INR volatility ({usdinr.iloc[0]['Change%']:+.2f}%)")
        
        # Commodity stress
        if 'commodities' in all_data and not all_data['commodities'].empty:
            oil = all_data['commodities'][all_data['commodities']['Symbol'] == 'CL=F']
            if not oil.empty and oil.iloc[0]['Change%'] > 3:
                risk_score += 1
                risk_factors.append(f"Oil spiking ({oil.iloc[0]['Change%']:+.1f}%)")
        
        # Cap risk score
        risk_score = min(10, max(1, risk_score))
        
        # Determine risk level
        if risk_score >= 8:
            risk_level = "VERY HIGH"
            risk_color = "red"
        elif risk_score >= 6:
            risk_level = "HIGH"
            risk_color = "yellow"
        elif risk_score >= 4:
            risk_level = "MODERATE"
            risk_color = "yellow"
        else:
            risk_level = "LOW"
            risk_color = "green"
        
        return {
            'score': risk_score,
            'level': risk_level,
            'color': risk_color,
            'factors': risk_factors
        }
    except:
        return {
            'score': 5,
            'level': 'MODERATE',
            'color': 'yellow',
            'factors': ['Unable to calculate detailed risk']
        }


def generate_ascii_chart(prices: List[float], width: int = 50, height: int = 10) -> str:
    """Generate ASCII chart for price movement."""
    try:
        if not prices or len(prices) < 2:
            return "Insufficient data"
        
        # Normalize prices
        min_price = min(prices)
        max_price = max(prices)
        price_range = max_price - min_price
        
        if price_range == 0:
            return "No price movement"
        
        # Create chart
        chart_lines = []
        for i in range(height, 0, -1):
            threshold = min_price + (price_range * i / height)
            line = ""
            for price in prices[-width:]:
                if price >= threshold:
                    line += "█"
                else:
                    line += " "
            chart_lines.append(line)
        
        return "\n".join(chart_lines)
    except:
        return "Chart unavailable"


def display_probability_analysis(probabilities: Dict):
    """Display probability analysis with visual indicators."""
    if not probabilities:
        console.print("[yellow]Probability analysis unavailable[/yellow]")
        return
    
    console.print(Panel("[bold]📊 PROBABILITY ANALYSIS[/bold]", expand=False))
    
    for symbol, data in probabilities.items():
        name = GLOBAL_INDICES.get("Indian Markets", {}).get(symbol, 
               GLOBAL_INDICES.get("US Markets", {}).get(symbol, symbol))
        
        bullish_prob = data['bullish']
        bearish_prob = data['bearish']
        
        # Create visual bar
        bar_length = 40
        bullish_bars = int(bullish_prob / 100 * bar_length)
        bearish_bars = bar_length - bullish_bars
        
        bar = f"[green]{'█' * bullish_bars}[/green][red]{'█' * bearish_bars}[/red]"
        
        # Determine signal
        if bullish_prob > 65:
            signal = "[bold green]BULLISH SIGNAL ↗[/bold green]"
        elif bullish_prob > 55:
            signal = "[green]Slightly Bullish ↗[/green]"
        elif bullish_prob > 45:
            signal = "[yellow]NEUTRAL ↔[/yellow]"
        elif bullish_prob > 35:
            signal = "[red]Slightly Bearish ↘[/red]"
        else:
            signal = "[bold red]BEARISH SIGNAL ↘[/bold red]"
        
        console.print(f"\n[bold cyan]{name}[/bold cyan]")
        console.print(f"  {bar}")
        console.print(f"  Bullish: {bullish_prob:.1f}% | Bearish: {bearish_prob:.1f}%")
        console.print(f"  Signal: {signal}")
        console.print(f"  RSI: {data['rsi']:.1f} | Momentum: {data['momentum']:+.2f}% | Volatility: {data['volatility']:.2f}%")


def display_risk_dashboard(risk_data: Dict):
    """Display comprehensive risk dashboard."""
    console.print(Panel("[bold]⚠️  RISK ASSESSMENT DASHBOARD[/bold]", expand=False))
    
    score = risk_data['score']
    level = risk_data['level']
    color = risk_data['color']
    factors = risk_data['factors']
    
    # Risk gauge visualization
    gauge = ""
    for i in range(1, 11):
        if i <= score:
            if i <= 3:
                gauge += "[green]█[/green]"
            elif i <= 6:
                gauge += "[yellow]█[/yellow]"
            else:
                gauge += "[red]█[/red]"
        else:
            gauge += "░"
    
    console.print(f"\n[bold]Risk Level: [{color}]{level}[/{color}][/bold]")
    console.print(f"Risk Score: {gauge} {score}/10")
    
    console.print(f"\n[bold]Risk Factors:[/bold]")
    if factors:
        for factor in factors:
            console.print(f"  • {factor}")
    else:
        console.print("  • No major risk factors identified")
    
    # Trading recommendations based on risk
    console.print(f"\n[bold]Trading Recommendations:[/bold]")
    if score >= 8:
        console.print("  🔴 HIGH RISK: Consider defensive positions, reduce leverage")
        console.print("  🔴 Move to cash or safe havens (Gold, bonds)")
        console.print("  🔴 Avoid new long positions")
    elif score >= 6:
        console.print("  🟡 ELEVATED RISK: Reduce position sizes, tighten stops")
        console.print("  🟡 Hedging recommended")
        console.print("  🟡 Be selective with new positions")
    elif score >= 4:
        console.print("  🟡 MODERATE RISK: Normal trading with caution")
        console.print("  🟡 Maintain risk management discipline")
        console.print("  🟡 Diversification important")
    else:
        console.print("  🟢 LOW RISK: Favorable for aggressive positions")
        console.print("  🟢 Good environment for swing trades")
        console.print("  🟢 Consider increasing exposure")
    
    console.print()


def cmd_watchlist(symbols: List[str]):
    """Monitor custom watchlist."""
    console.print("\n[bold cyan]👁️  WATCHLIST MONITOR[/bold cyan]\n")
    
    symbols_dict = {s: s for s in symbols}
    watchlist_df = fetch_market_data(symbols_dict)
    display_market_table(watchlist_df, "Your Watchlist")


def cmd_all():
    """Execute all commands for comprehensive market intelligence with advanced analytics."""
    console.print("\n[bold magenta]" + "="*80 + "[/bold magenta]")
    console.print("[bold magenta]🌟 COMPLETE MARKET INTELLIGENCE - ALL DATA 🌟[/bold magenta]")
    console.print("[bold magenta]" + "="*80 + "[/bold magenta]")
    console.print(f"[dim]Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n")
    
    try:
        # Fetch historical data for advanced analytics
        console.print("[dim]Fetching historical data for advanced analysis...[/dim]\n")
        historical_data = {}
        for symbol in ['^NSEI', '^BSESN', '^GSPC', '^DJI', '^IXIC']:
            try:
                historical_data[symbol] = fetch_historical_data(symbol, "3mo")
            except:
                pass
        
        # 1. Global Market Overview
        console.print("\n[bold yellow]" + "―"*80 + "[/bold yellow]")
        console.print("[bold yellow]📊 SECTION 1: GLOBAL MARKET OVERVIEW[/bold yellow]")
        console.print("[bold yellow]" + "―"*80 + "[/bold yellow]\n")
        cmd_overview()
        
        # 2. Indian Market Deep Dive with Charts
        console.print("\n[bold yellow]" + "―"*80 + "[/bold yellow]")
        console.print("[bold yellow]🇮🇳 SECTION 2: INDIAN MARKET ANALYSIS[/bold yellow]")
        console.print("[bold yellow]" + "―"*80 + "[/bold yellow]\n")
        cmd_india()
        
        # Display NIFTY trend chart
        if '^NSEI' in historical_data and not historical_data['^NSEI'].empty:
            nifty_df = historical_data['^NSEI']
            prices = nifty_df['Close'].tolist()[-30:]  # Last 30 days
            console.print("\n[bold cyan]NIFTY 50 - 30 Day Price Movement:[/bold cyan]")
            chart = generate_ascii_chart(prices, width=60, height=8)
            console.print(f"[dim]{chart}[/dim]")
            console.print(f"[dim]Range: {min(prices):.2f} - {max(prices):.2f}[/dim]\n")
            
            # Trend strength
            trend_data = calculate_trend_strength(nifty_df)
            trend_color = "green" if "UP" in trend_data['trend'] else "red" if "DOWN" in trend_data['trend'] else "yellow"
            console.print(f"[{trend_color}]Trend: {trend_data['trend']} (Score: {trend_data['score']}/10)[/{trend_color}]")
            console.print(f"Current: {trend_data['current']:.2f} | MA5: {trend_data['ma5']:.2f} | MA20: {trend_data['ma20']:.2f}\n")
        
        # 3. ADVANCED ANALYTICS: Probability Analysis
        console.print("\n[bold yellow]" + "―"*80 + "[/bold yellow]")
        console.print("[bold yellow]🎯 SECTION 3: PROBABILITY & TECHNICAL ANALYSIS[/bold yellow]")
        console.print("[bold yellow]" + "―"*80 + "[/bold yellow]\n")
        
        probabilities = calculate_market_probability(None, historical_data)
        display_probability_analysis(probabilities)
        
        # Technical indicators table
        console.print("\n")
        tech_table = Table(title="Technical Indicators Summary", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        tech_table.add_column("Index", style="cyan", width=15)
        tech_table.add_column("RSI", justify="right", width=10)
        tech_table.add_column("Signal", width=20)
        tech_table.add_column("Momentum", justify="right", width=12)
        tech_table.add_column("Volatility", justify="right", width=12)
        
        for symbol, data in probabilities.items():
            name = "NIFTY 50" if symbol == "^NSEI" else "SENSEX" if symbol == "^BSESN" else "S&P 500"
            rsi = data['rsi']
            
            # RSI signal
            if rsi < 30:
                rsi_signal = "[green]Oversold (Buy)[/green]"
            elif rsi > 70:
                rsi_signal = "[red]Overbought (Sell)[/red]"
            else:
                rsi_signal = "[yellow]Neutral[/yellow]"
            
            # Momentum color
            momentum = data['momentum']
            mom_color = "green" if momentum > 0 else "red"
            
            tech_table.add_row(
                name,
                f"{rsi:.1f}",
                rsi_signal,
                f"[{mom_color}]{momentum:+.2f}%[/{mom_color}]",
                f"{data['volatility']:.2f}%"
            )
        
        console.print(tech_table)
        console.print()
        
        # 4. RISK ASSESSMENT DASHBOARD
        console.print("\n[bold yellow]" + "―"*80 + "[/bold yellow]")
        console.print("[bold yellow]⚠️  SECTION 4: RISK ASSESSMENT[/bold yellow]")
        console.print("[bold yellow]" + "―"*80 + "[/bold yellow]\n")
        
        # Collect data for risk calculation
        all_data = {}
        all_indices = {}
        for reg, indices in GLOBAL_INDICES.items():
            all_indices.update(indices)
        all_data['indices'] = fetch_market_data(all_indices)
        all_data['commodities'] = fetch_market_data(COMMODITIES)
        all_data['currencies'] = fetch_market_data(CURRENCIES)
        
        risk_data = calculate_risk_score(all_data)
        display_risk_dashboard(risk_data)
        
        # 5. Sector Analysis
        console.print("\n[bold yellow]" + "―"*80 + "[/bold yellow]")
        console.print("[bold yellow]📈 SECTION 5: SECTOR PERFORMANCE[/bold yellow]")
        console.print("[bold yellow]" + "―"*80 + "[/bold yellow]\n")
        cmd_sectors(india=True)
        
        # 6. Intermarket Relationships
        console.print("\n[bold yellow]" + "―"*80 + "[/bold yellow]")
        console.print("[bold yellow]🔗 SECTION 6: INTERMARKET ANALYSIS[/bold yellow]")
        console.print("[bold yellow]" + "―"*80 + "[/bold yellow]\n")
        cmd_intermarket()
        
        # 7. Geopolitical Events
        console.print("\n[bold yellow]" + "―"*80 + "[/bold yellow]")
        console.print("[bold yellow]🌐 SECTION 7: GEOPOLITICAL EVENTS & VIX[/bold yellow]")
        console.print("[bold yellow]" + "―"*80 + "[/bold yellow]\n")
        cmd_geopolitical()
        
        # 8. Latest News (Indian + Global)
        console.print("\n[bold yellow]" + "―"*80 + "[/bold yellow]")
        console.print("[bold yellow]📰 SECTION 8: MARKET NEWS[/bold yellow]")
        console.print("[bold yellow]" + "―"*80 + "[/bold yellow]\n")
        
        console.print("[bold cyan]Indian Market News:[/bold cyan]")
        news_india = get_market_news(max_items=5, india_only=True)
        display_news(news_india, "Top Indian Headlines")
        
        console.print("\n[bold cyan]Global Market News:[/bold cyan]")
        news_global = get_market_news(max_items=5, india_only=False)
        display_news(news_global, "Top Global Headlines")
        
        # 9. COMPREHENSIVE OUTLOOK & DECISION SUPPORT
        console.print("\n[bold yellow]" + "―"*80 + "[/bold yellow]")
        console.print("[bold yellow]💡 SECTION 9: MARKET OUTLOOK & DECISIONS[/bold yellow]")
        console.print("[bold yellow]" + "―"*80 + "[/bold yellow]\n")
        
        all_data['global_sentiment'] = calculate_market_sentiment(all_data['indices'])
        all_data['indian_analysis'] = analyze_indian_market()
        
        outlook = generate_market_outlook(all_data)
        console.print(Panel(outlook, title="[bold]Market Outlook & Analysis[/bold]", expand=False))
        
        # Trading Decision Matrix
        console.print("\n")
        decision_matrix = Table(title="📋 Trading Decision Matrix", box=box.DOUBLE, show_header=True, header_style="bold magenta")
        decision_matrix.add_column("Factor", style="cyan", width=25)
        decision_matrix.add_column("Status", width=30)
        decision_matrix.add_column("Action", style="yellow", width=20)
        
        # Market sentiment
        sentiment = all_data['global_sentiment']
        sentiment_color = "green" if sentiment == "BULLISH" else "red" if sentiment == "BEARISH" else "yellow"
        sentiment_action = "BUY" if sentiment == "BULLISH" else "SELL" if sentiment == "BEARISH" else "HOLD"
        decision_matrix.add_row(
            "Global Sentiment",
            f"[{sentiment_color}]{sentiment}[/{sentiment_color}]",
            sentiment_action
        )
        
        # Risk level
        risk_action = "REDUCE" if risk_data['score'] >= 7 else "HEDGE" if risk_data['score'] >= 5 else "EXPAND"
        decision_matrix.add_row(
            "Risk Level",
            f"[{risk_data['color']}]{risk_data['level']} ({risk_data['score']}/10)[/{risk_data['color']}]",
            risk_action
        )
        
        # NIFTY probability
        if '^NSEI' in probabilities:
            nifty_prob = probabilities['^NSEI']['bullish']
            prob_color = "green" if nifty_prob > 60 else "red" if nifty_prob < 40 else "yellow"
            prob_action = "LONG" if nifty_prob > 60 else "SHORT" if nifty_prob < 40 else "NEUTRAL"
            decision_matrix.add_row(
                "NIFTY Probability",
                f"[{prob_color}]{nifty_prob:.1f}% Bullish[/{prob_color}]",
                prob_action
            )
        
        # Volatility
        if '^NSEI' in probabilities:
            vol = probabilities['^NSEI']['volatility']
            vol_color = "red" if vol > 2.5 else "yellow" if vol > 1.5 else "green"
            vol_action = "REDUCE SIZE" if vol > 2.5 else "NORMAL SIZE" if vol > 1.5 else "AGGRESSIVE"
            decision_matrix.add_row(
                "Volatility",
                f"[{vol_color}]{vol:.2f}%[/{vol_color}]",
                vol_action
            )
        
        console.print(decision_matrix)
        console.print()
        
        # Strategic Recommendations
        console.print(Panel(
            "[bold]🎯 STRATEGIC RECOMMENDATIONS:[/bold]\n\n"
            "[bold underline]Immediate Actions:[/bold underline]\n"
            "1. ✅ Review your portfolio allocation based on risk score\n"
            "2. ✅ Set stop-losses based on current volatility levels\n"
            "3. ✅ Check probability scores before opening new positions\n"
            "4. ✅ Monitor geopolitical events for sudden changes\n\n"
            "[bold underline]Trading Guidelines:[/bold underline]\n"
            "• Use technical indicators (RSI, Momentum) for entry/exit\n"
            "• Adjust position sizes based on risk assessment\n"
            "• Follow trend strength for swing trades\n"
            "• Watch intermarket correlations for confirmation\n\n"
            "[bold underline]Risk Management:[/bold underline]\n"
            "• Position Size: Inversely proportional to risk score\n"
            "• Stop Loss: 1.5x current volatility from entry\n"
            "• Profit Target: 2-3x risk (1:2 or 1:3 ratio)\n"
            "• Max Portfolio Risk: < 2% per trade\n\n"
            "[dim]⚠️  This is for informational purposes only, not financial advice.\n"
            "Always consult qualified financial advisors before making investment decisions.[/dim]",
            title="Decision Support",
            expand=False,
            border_style="green"
        ))
        
        # Final Summary
        console.print("\n[bold magenta]" + "="*80 + "[/bold magenta]")
        console.print("[bold magenta]✨ COMPLETE ANALYSIS FINISHED ✨[/bold magenta]")
        console.print("[bold magenta]" +"="*80 + "[/bold magenta]\n")
        
        console.print(Panel(
            f"[bold]Report Summary:[/bold]\n\n"
            f"📊 Sections Analyzed: 9\n"
            f"🎯 Probability Models: {len(probabilities)}\n"
            f"⚠️  Risk Score: {risk_data['score']}/10 ({risk_data['level']})\n"
            f"📈 Market Sentiment: {sentiment}\n"
            f"🔔 Risk Factors: {len(risk_data['factors'])}\n"
            f"📰 News Items: {len(news_india) + len(news_global)}\n\n"
            f"[dim]Tip: Run 'all' command daily for updated intelligence![/dim]",
            title="Report Statistics",
            expand=False,
            border_style="cyan"
        ))
        console.print()
        
    except Exception as e:
        console.print(f"[red]Error in comprehensive analysis: {e}[/red]")
        import traceback
        traceback.print_exc()
        raise


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    if len(sys.argv) < 2:
        console.print("[red]Usage: market_analysis.py <command> [options][/red]")
        console.print("\nCommands:")
        console.print("  all               - ⭐ ALL data (super command)")
        console.print("  overview          - Global market overview")
        console.print("  india             - Indian market analysis")
        console.print("  news              - Market news")
        console.print("  geopolitical      - Geopolitical events")
        console.print("  report            - Comprehensive report")
        console.print("  sectors           - Sector analysis")
        console.print("  intermarket       - Intermarket analysis")
        console.print("  watchlist <symbols> - Monitor custom symbols")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "all":
            cmd_all()
        
        elif command == "overview":
            cmd_overview()
        
        elif command == "india":
            cmd_india()
        
        elif command == "news":
            india_only = "--india" in sys.argv
            geopolitical = "--geopolitical" in sys.argv
            ticker = None
            if "--ticker" in sys.argv:
                ticker_idx = sys.argv.index("--ticker") + 1
                if ticker_idx < len(sys.argv):
                    ticker = sys.argv[ticker_idx]
            cmd_news(india_only, geopolitical, ticker)
        
        elif command == "geopolitical":
            cmd_geopolitical()
        
        elif command == "report":
            region = "global"
            if "--region" in sys.argv:
                region_idx = sys.argv.index("--region") + 1
                if region_idx < len(sys.argv):
                    region = sys.argv[region_idx]
            cmd_report(region)
        
        elif command == "sectors":
            india = "--india" in sys.argv
            cmd_sectors(india)
        
        elif command == "intermarket":
            cmd_intermarket()
        
        elif command == "watchlist":
            symbols = sys.argv[2:]
            if not symbols:
                console.print("[red]Error: Please provide at least one symbol[/red]")
                sys.exit(1)
            cmd_watchlist(symbols)
        
        else:
            console.print(f"[red]Unknown command: {command}[/red]")
            sys.exit(1)
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
