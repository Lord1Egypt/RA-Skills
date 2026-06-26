#!/usr/bin/env python3
"""
IHSG Session Data Extractor v6 - Tavily Edition
================================================
A comprehensive data extraction tool for IHSG session summaries using Tavily API.

Data Sources:
- Yahoo Finance: IHSG index data (WORKING)
- Tavily Search: Top 10 net buy/sell, Foreign Flow, YTD data
- Tavily Extract: Detailed content from financial news sites

Usage:
  python3 ihsg_session_extractor.py [morning|closing] --output json
  python3 ihsg_session_extractor.py [morning|closing] --format
  python3 ihsg_session_extractor.py --tavily-search "top net buy sell Indonesia"

Environment Variables:
  TAVILY_API_KEY - Your Tavily API key (get from https://app.tavily.com)
"""

import os
import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import argparse
from datetime import datetime
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict, field
from enum import Enum

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    print("Warning: tavily-python not installed. Install with: pip install tavily-python")


class Session(Enum):
    MORNING = "morning"
    CLOSING = "closing"


@dataclass
class IHSGData:
    current: float = 0.0
    previous_close: float = 0.0
    change: float = 0.0
    change_percent: float = 0.0
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    volume: int = 0
    value: float = 0.0
    timestamp: str = ""


@dataclass
class StockFlow:
    code: str = ""
    name: str = ""
    net_value: float = 0.0
    net_volume: float = 0.0
    buy_volume: float = 0.0
    sell_volume: float = 0.0
    price_change: float = 0.0
    price_change_percent: float = 0.0


@dataclass
class ForeignFlow:
    foreign_buy: float = 0.0
    foreign_sell: float = 0.0
    net_foreign: float = 0.0
    ytd_net: float = 0.0
    domestic_buy: float = 0.0
    domestic_sell: float = 0.0
    net_domestic: float = 0.0


@dataclass
class SessionData:
    session: str = "closing"
    date: str = ""
    timestamp: str = ""
    ihsg: Optional[IHSGData] = None
    top_buy: List[StockFlow] = field(default_factory=list)
    top_sell: List[StockFlow] = field(default_factory=list)
    foreign_flow: Optional[ForeignFlow] = None
    needs_web_search: Dict[str, bool] = field(default_factory=dict)
    web_search_queries: List[str] = field(default_factory=list)


class TavilyIntegration:
    """Tavily API integration for web search and extract"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("TAVILY_API_KEY")
        self.client = None
        if TAVILY_AVAILABLE and self.api_key:
            try:
                self.client = TavilyClient(api_key=self.api_key)
            except Exception as e:
                print(f"Tavily client init error: {e}", file=sys.stderr)
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def search(self, query: str, max_results: int = 10, search_depth: str = "advanced") -> List[Dict]:
        """Perform web search using Tavily"""
        if not self.client:
            print("Tavily client not available", file=sys.stderr)
            return []
        
        try:
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=max_results,
                include_raw_content=True
            )
            return response.get('results', [])
        except Exception as e:
            print(f"Tavily search error: {e}", file=sys.stderr)
            return []
    
    def extract(self, urls: List[str]) -> List[Dict]:
        """Extract content from URLs using Tavily"""
        if not self.client:
            print("Tavily client not available", file=sys.stderr)
            return []
        
        try:
            response = self.client.extract(
                urls=urls,
                extract_depth="advanced"
            )
            return response.get('results', [])
        except Exception as e:
            print(f"Tavily extract error: {e}", file=sys.stderr)
            return []
    
    def search_ihsg_data(self) -> Dict[str, Any]:
        """Search for IHSG market data"""
        queries = [
            "IHSG IDX Composite close today price Indonesia",
            "IHSG index harga penutupan hari ini"
        ]
        
        results = []
        for query in queries:
            results.extend(self.search(query, max_results=5))
        
        return self._parse_ihsg_results(results)
    
    def search_top_net_buy_sell(self, year: int = None) -> Dict[str, List[StockFlow]]:
        """Search for top net buy/sell stocks"""
        year = year or datetime.now().year
        queries = [
            f"top 10 net buy sell saham Indonesia hari ini {year}",
            f"top foreign net buy sell IDX Indonesia today {year}",
            "saham dengan aliran dana asing terbesar hari ini",
            "top net buy sell asing BEI hari ini"
        ]
        
        all_results = []
        for query in queries:
            all_results.extend(self.search(query, max_results=10))
        
        return self._parse_net_buy_sell_results(all_results)
    
    def search_foreign_flow(self, year: int = None) -> Optional[ForeignFlow]:
        """Search for foreign flow data"""
        year = year or datetime.now().year
        queries = [
            f"net foreign flow Bursa Efek Indonesia hari ini miliar {year}",
            f"aliran dana asing BEI hari ini {year}",
            f"foreign buying selling Indonesia stock exchange today billion {year}"
        ]
        
        all_results = []
        for query in queries:
            all_results.extend(self.search(query, max_results=10))
        
        return self._parse_foreign_flow_results(all_results)
    
    def search_ytd_foreign_flow(self, year: int = None) -> float:
        """Search for YTD foreign flow"""
        year = year or datetime.now().year
        queries = [
            f"YTD foreign flow Indonesia stock exchange {year}",
            f"akumulasi dana asing BEI tahun ini {year}",
            f"foreign flow year to date Indonesia {year}"
        ]
        
        all_results = []
        for query in queries:
            all_results.extend(self.search(query, max_results=5))
        
        return self._parse_ytd_results(all_results)
    
    def search_stock_prices(self, codes: List[str]) -> Dict[str, float]:
        """Search for stock price changes"""
        results = {}
        
        for code in codes[:10]:  # Limit to 10 stocks
            query = f"{code} stock price change Indonesia today"
            search_results = self.search(query, max_results=3)
            
            for result in search_results:
                snippet = result.get('snippet', '') or result.get('content', '')
                # Look for price change pattern
                match = re.search(rf'{code}.*?([+-]?[\d,\.]+)\s*%', snippet, re.IGNORECASE)
                if match:
                    try:
                        change = float(match.group(1).replace(',', '.'))
                        results[code] = change
                        break
                    except:
                        pass
        
        return results
    
    def _parse_ihsg_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Parse IHSG search results"""
        data = {}
        
        for result in results:
            snippet = result.get('snippet', '') or result.get('content', '')
            
            # Look for IHSG value
            match = re.search(r'IHSG.*?(\d{1,2}[,.]?\d{3}[,.]?\d{1,2})', snippet, re.IGNORECASE)
            if match:
                value = float(match.group(1).replace(',', ''))
                data['current'] = value
            
            # Look for change percentage
            match = re.search(r'([+-]?[\d,\.]+)\s*%', snippet)
            if match:
                try:
                    data['change_percent'] = float(match.group(1).replace(',', '.'))
                except:
                    pass
        
        return data
    
    def _parse_net_buy_sell_results(self, results: List[Dict]) -> Dict[str, List[StockFlow]]:
        """Parse net buy/sell search results"""
        top_buy = []
        top_sell = []
        seen_buy = set()
        seen_sell = set()
        
        for result in results:
            snippet = result.get('snippet', '') or result.get('content', '')
            
            # Parse net buy patterns
            buy_patterns = [
                r'([A-Z]{2,5})\s*(?:net\s*)?buy[:\s]+([\d,\.]+)\s*([BMK]?)',
                r'buy\s+([A-Z]{2,5})[:\s]+([\d,\.]+)\s*([BMK]?)',
                r'([A-Z]{2,5})\s*net\s*buy\s+([\d,\.]+)\s*([BMK]?)',
            ]
            
            for pattern in buy_patterns:
                matches = re.findall(pattern, snippet, re.IGNORECASE)
                for m in matches:
                    code = m[0].upper()
                    if code in seen_buy or len(code) > 5:
                        continue
                    value = self._parse_value_with_unit(m[1], m[2] if len(m) > 2 else '')
                    if value > 0:
                        top_buy.append(StockFlow(code=code, net_value=value))
                        seen_buy.add(code)
            
            # Parse net sell patterns
            sell_patterns = [
                r'([A-Z]{2,5})\s*(?:net\s*)?sell[:\s]+([\d,\.]+)\s*([BMK]?)',
                r'sell\s+([A-Z]{2,5})[:\s]+([\d,\.]+)\s*([BMK]?)',
                r'([A-Z]{2,5})\s*net\s*sell\s+([\d,\.]+)\s*([BMK]?)',
            ]
            
            for pattern in sell_patterns:
                matches = re.findall(pattern, snippet, re.IGNORECASE)
                for m in matches:
                    code = m[0].upper()
                    if code in seen_sell or len(code) > 5:
                        continue
                    value = self._parse_value_with_unit(m[1], m[2] if len(m) > 2 else '')
                    if value > 0:
                        top_sell.append(StockFlow(code=code, net_value=value))
                        seen_sell.add(code)
        
        # Sort by value
        top_buy.sort(key=lambda x: x.net_value, reverse=True)
        top_sell.sort(key=lambda x: x.net_value, reverse=True)
        
        return {'top_buy': top_buy[:10], 'top_sell': top_sell[:10]}
    
    def _parse_foreign_flow_results(self, results: List[Dict]) -> Optional[ForeignFlow]:
        """Parse foreign flow search results"""
        foreign_buy = 0
        foreign_sell = 0
        net_foreign = 0
        
        for result in results:
            snippet = result.get('snippet', '') or result.get('content', '')
            
            # Look for patterns
            buy_match = re.search(r'[Ff]oreign\s*(?:buy|buying)[:\s]*([\d,\.]+)\s*([BMK]?)', snippet)
            if buy_match:
                foreign_buy = self._parse_value_with_unit(buy_match.group(1), buy_match.group(2))
            
            sell_match = re.search(r'[Ff]oreign\s*(?:sell|selling)[:\s]*([\d,\.]+)\s*([BMK]?)', snippet)
            if sell_match:
                foreign_sell = self._parse_value_with_unit(sell_match.group(1), sell_match.group(2))
            
            net_match = re.search(r'[Nn]et\s*(?:foreign|flow|sell|buy)[:\s]*([+-]?[\d,\.]+)\s*([BMK]?)', snippet)
            if net_match:
                net_foreign = self._parse_value_with_unit(net_match.group(1), net_match.group(2))
        
        if foreign_buy or foreign_sell or net_foreign:
            return ForeignFlow(
                foreign_buy=foreign_buy,
                foreign_sell=foreign_sell,
                net_foreign=net_foreign
            )
        
        return None
    
    def _parse_ytd_results(self, results: List[Dict]) -> float:
        """Parse YTD foreign flow results"""
        for result in results:
            snippet = result.get('snippet', '') or result.get('content', '')
            
            # Look for YTD pattern
            match = re.search(r'[Yy][Tt][Dd][^:]*[:\s]*([+-]?[\d,\.]+)\s*([BMK]?)', snippet)
            if match:
                return self._parse_value_with_unit(match.group(1), match.group(2))
            
            # Look for "akumulasi" pattern
            match = re.search(r'[Aa]kumulasi[^:]*[:\s]*([+-]?[\d,\.]+)\s*([BMK]?)', snippet)
            if match:
                return self._parse_value_with_unit(match.group(1), match.group(2))
        
        return 0.0
    
    def _parse_value_with_unit(self, num_str: str, unit: str) -> float:
        """Parse value with unit multiplier (B/M/K)"""
        try:
            num = float(num_str.replace(',', ''))
            unit = unit.upper()
            multipliers = {'B': 1, 'M': 0.001, 'K': 0.000001}
            return num * multipliers.get(unit, 1)
        except:
            return 0.0


class IHSGExtractor:
    """Extract IHSG data from Yahoo Finance"""
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def get_ihsg_data(self) -> Optional[IHSGData]:
        """Get IHSG index data from Yahoo Finance"""
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EJKSE"
        params = {
            'interval': '1d',
            'range': '2d'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return self._parse_yahoo_response(data)
        except Exception as e:
            print(f"Yahoo Finance error: {e}", file=sys.stderr)
        
        return None
    
    def _parse_yahoo_response(self, data: dict) -> Optional[IHSGData]:
        """Parse IHSG from Yahoo Finance response"""
        try:
            result = data.get('chart', {}).get('result', [])
            if not result:
                return None
            
            meta = result[0].get('meta', {})
            indicators = result[0].get('indicators', {})
            quotes = indicators.get('quote', [])
            
            quote = quotes[0] if quotes else {}
            
            current = float(meta.get('regularMarketPrice', 0))
            chart_prev_close = float(meta.get('chartPreviousClose', 0))
            
            closes = quote.get('close', [])
            opens = quote.get('open', [])
            highs = quote.get('high', [])
            lows = quote.get('low', [])
            volumes = quote.get('volume', [])
            
            latest_close = float(closes[-1]) if closes and closes[-1] else current
            latest_open = float(opens[-1]) if opens and opens[-1] else 0
            latest_high = float(highs[-1]) if highs and highs[-1] else 0
            latest_low = float(lows[-1]) if lows and lows[-1] else 0
            latest_volume = int(volumes[-1]) if volumes and volumes[-1] else 0
            
            prev_close_val = float(closes[-2]) if len(closes) > 1 and closes[-2] else chart_prev_close
            
            change = latest_close - prev_close_val
            change_pct = (change / prev_close_val * 100) if prev_close_val else 0
            
            return IHSGData(
                current=round(latest_close, 2),
                previous_close=round(prev_close_val, 2),
                change=round(change, 2),
                change_percent=round(change_pct, 2),
                open=round(latest_open, 2),
                high=round(latest_high, 2),
                low=round(latest_low, 2),
                volume=latest_volume,
                value=0,
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            print(f"Parse Yahoo error: {e}", file=sys.stderr)
        
        return None


class TopNetScraper:
    """Scrape top net buy/sell from Infovesta (fallback)"""
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Connection': 'keep-alive',
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def get_top_net_from_infovesta(self) -> Dict[str, List[StockFlow]]:
        """Get top net buy and net sell from Infovesta (provides Top 5)"""
        result = {'top_buy': [], 'top_sell': []}
        
        # Get top buy
        buy_url = "https://www.infovesta.com/index/data_info/saham/topbuy"
        try:
            response = self.session.get(buy_url, timeout=15)
            if response.status_code == 200:
                result['top_buy'] = self._parse_infovesta_table(response.text)
        except Exception as e:
            print(f"Infovesta buy error: {e}", file=sys.stderr)
        
        # Get top sell
        sell_url = "https://www.infovesta.com/index/data_info/saham/topsell"
        try:
            response = self.session.get(sell_url, timeout=15)
            if response.status_code == 200:
                result['top_sell'] = self._parse_infovesta_table(response.text)
        except Exception as e:
            print(f"Infovesta sell error: {e}", file=sys.stderr)
        
        return result
    
    def _parse_infovesta_table(self, html: str) -> List[StockFlow]:
        """Parse Infovesta HTML table"""
        stocks = []
        soup = BeautifulSoup(html, 'html.parser')
        
        table = soup.find('table', class_='table')
        if not table:
            return stocks
        
        text = table.get_text(separator='|', strip=True)
        pattern = r'([A-Z]{2,5})\|Buy\|([\d,]+)\|([\d,]+)\|Sell\|([\d,]+)'
        matches = re.findall(pattern, text)
        
        for match in matches:
            code = match[0]
            buy_vol = self._parse_number(match[1])
            net_vol = self._parse_number(match[2])
            sell_vol = self._parse_number(match[3])
            
            if code and len(code) <= 5:
                stocks.append(StockFlow(
                    code=code,
                    buy_volume=buy_vol,
                    sell_volume=sell_vol,
                    net_volume=net_vol,
                    net_value=0,
                    price_change=0
                ))
        
        return stocks
    
    def _parse_number(self, text: str) -> float:
        """Parse number from text"""
        try:
            clean = text.replace(',', '')
            return float(clean) if clean else 0
        except:
            return 0.0


class OutputFormatter:
    """Format output in plain text ASCII format"""
    
    DAYS_ID = {
        'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
        'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
    }
    MONTHS_ID = {
        'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
        'April': 'April', 'May': 'Mei', 'June': 'Juni', 'July': 'Juli',
        'August': 'Agustus', 'September': 'September', 'October': 'Oktober',
        'November': 'November', 'December': 'Desember'
    }
    
    def format_date_id(self) -> str:
        """Format date in Bahasa Indonesia"""
        now = datetime.now()
        day_id = self.DAYS_ID.get(now.strftime('%A'), now.strftime('%A'))
        month_id = self.MONTHS_ID.get(now.strftime('%B'), now.strftime('%B'))
        return f"{day_id}, {now.day} {month_id} {now.year}"
    
    def format_full_output(self, data: SessionData, insights: str = "") -> str:
        """Format complete session report"""
        session_label = "PAGI" if data.session == 'morning' else "CLOSING"
        date_str = self.format_date_id()
        
        ihsg = data.ihsg or IHSGData()
        emoji = '🟢' if ihsg.change >= 0 else '🔴'
        
        output = f"""📊 IHSG {session_label} SUMMARY
{date_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{emoji} IHSG: {ihsg.current:,.2f} ({ihsg.change_percent:+.2f}%)
Open: {ihsg.open:,.2f} | High: {ihsg.high:,.2f} | Low: {ihsg.low:,.2f}
Prev Close: {ihsg.previous_close:,.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 TOP 10 NET BUY (by Value)
"""
        
        output += self._format_stock_table(data.top_buy)
        
        output += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n📉 TOP 10 NET SELL (by Value)\n"
        
        output += self._format_stock_table(data.top_sell)
        
        # Foreign flow
        if data.foreign_flow:
            ff = data.foreign_flow
            flow_emoji = '📈' if ff.net_foreign >= 0 else '📉'
            flow_status = 'INFLOW' if ff.net_foreign >= 0 else 'OUTFLOW'
            
            output += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 FOREIGN vs DOMESTIC FLOW

Foreign:
• Buy:  IDR {ff.foreign_buy:,.1f}B
• Sell: IDR {ff.foreign_sell:,.1f}B
• Net:  IDR {ff.net_foreign:+,.1f}B {flow_emoji} {flow_status}
"""
            if data.session == 'closing':
                if ff.net_domestic != 0:
                    output += f"""
Domestic:
• Net:  IDR {ff.net_domestic:+,.1f}B
"""
                if ff.ytd_net != 0:
                    output += f"""
YTD Foreign: IDR {ff.ytd_net:+,.1f}B
"""
        else:
            output += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 FOREIGN FLOW
⚠ Data tidak tersedia - gunakan Tavily API untuk mencari data
"""
        
        # Insights
        if insights:
            output += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 INSIGHTS {session_label}

{insights}
"""
        
        output += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session: {session_label} | Generated: {datetime.now().strftime('%H:%M')} WIB
Data Source: Tavily API + Yahoo Finance
"""
        
        return output
    
    def _format_stock_table(self, stocks: List[StockFlow]) -> str:
        """Format stock list as ASCII table"""
        output = "┌────┬────────┬────────────┬───────────┬──────────┐\n"
        output += "│ No │ Kode   │ Net Value  │ Net Vol   │ Chg %    │\n"
        output += "├────┼────────┼────────────┼───────────┼──────────┤\n"
        
        if not stocks:
            output += "│ -- │ Data belum tersedia - gunakan Tavily API     │\n"
        else:
            for i, s in enumerate(stocks[:10], 1):
                code = s.code[:6] if s.code else "N/A"
                
                # Format net value
                if s.net_value != 0:
                    nv = s.net_value
                    if abs(nv) >= 1e9:
                        nv_str = f"IDR {nv/1e9:.1f}B"
                    elif abs(nv) >= 1e6:
                        nv_str = f"IDR {nv/1e6:.1f}M"
                    else:
                        nv_str = f"IDR {nv/1e3:.1f}K"
                else:
                    nv_str = "N/A"
                
                # Format net volume
                vol = s.net_volume
                if abs(vol) >= 1e9:
                    vol_str = f"{vol/1e9:.1f}B"
                elif abs(vol) >= 1e6:
                    vol_str = f"{vol/1e6:.1f}M"
                elif abs(vol) >= 1e3:
                    vol_str = f"{vol/1e3:.1f}K"
                else:
                    vol_str = f"{vol:.0f}"
                
                # Format price change
                if s.price_change_percent != 0:
                    chg_str = f"{s.price_change_percent:+.2f}%"
                else:
                    chg_str = "N/A"
                
                output += f"│ {i:2d} │ {code:<6} │ {nv_str:>10} │ {vol_str:>9} │ {chg_str:>8} │\n"
        
        output += "└────┴────────┴────────────┴───────────┴──────────┘\n"
        
        if stocks and len(stocks) < 10:
            output += f"⚠ Hanya {len(stocks)} saham - gunakan Tavily API untuk Top 10\n"
        
        return output


def main():
    parser = argparse.ArgumentParser(description='IHSG Session Data Extractor v6 - Tavily Edition')
    parser.add_argument('session', nargs='?', default='closing', choices=['morning', 'closing'])
    parser.add_argument('--output', choices=['json', 'text'], default='json', help='Output format')
    parser.add_argument('--format', action='store_true', help='Format output as text')
    parser.add_argument('--tavily-search', type=str, help='Test Tavily search with query')
    parser.add_argument('--tavily-api-key', type=str, help='Tavily API key')
    parser.add_argument('--use-tavily', action='store_true', help='Force use Tavily for all data')
    
    args = parser.parse_args()
    
    # Initialize Tavily
    tavily = TavilyIntegration(api_key=args.tavily_api_key)
    if tavily.is_available():
        print("✓ Tavily API connected", file=sys.stderr)
    else:
        print("⚠ Tavily API not available (set TAVILY_API_KEY env var)", file=sys.stderr)
    
    # Test mode: just search
    if args.tavily_search:
        if not tavily.is_available():
            print("Error: Tavily API key required for search", file=sys.stderr)
            sys.exit(1)
        
        results = tavily.search(args.tavily_search, max_results=10)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return
    
    session = Session.MORNING if args.session == 'morning' else Session.CLOSING
    
    # Initialize extractors
    ihsg_extractor = IHSGExtractor()
    infovesta_scraper = TopNetScraper()
    formatter = OutputFormatter()
    
    # Create session data
    data = SessionData(
        session=session.value,
        date=datetime.now().strftime('%Y-%m-%d'),
        timestamp=datetime.now().isoformat()
    )
    
    print(f"Extracting data for {session.value} session...", file=sys.stderr)
    
    # 1. Get IHSG data (always from Yahoo Finance)
    print("  - Fetching IHSG data (Yahoo Finance)...", file=sys.stderr)
    data.ihsg = ihsg_extractor.get_ihsg_data()
    
    # 2. Get top net buy/sell
    if args.use_tavily and tavily.is_available():
        print("  - Fetching top net buy/sell (Tavily)...", file=sys.stderr)
        net_data = tavily.search_top_net_buy_sell()
        data.top_buy = net_data.get('top_buy', [])
        data.top_sell = net_data.get('top_sell', [])
    else:
        print("  - Fetching top net buy/sell (Infovesta)...", file=sys.stderr)
        net_data = infovesta_scraper.get_top_net_from_infovesta()
        data.top_buy = net_data.get('top_buy', [])
        data.top_sell = net_data.get('top_sell', [])
    
    # 3. Get foreign flow
    if tavily.is_available():
        print("  - Fetching foreign flow (Tavily)...", file=sys.stderr)
        data.foreign_flow = tavily.search_foreign_flow()
        
        if session == Session.CLOSING and data.foreign_flow:
            print("  - Fetching YTD foreign flow (Tavily)...", file=sys.stderr)
            data.foreign_flow.ytd_net = tavily.search_ytd_foreign_flow()
    
    # 4. Get stock price changes if we have stocks
    if tavily.is_available() and (data.top_buy or data.top_sell):
        print("  - Fetching stock price changes (Tavily)...", file=sys.stderr)
        codes = [s.code for s in data.top_buy + data.top_sell if s.code]
        price_changes = tavily.search_stock_prices(codes)
        
        for stock in data.top_buy + data.top_sell:
            if stock.code in price_changes:
                stock.price_change_percent = price_changes[stock.code]
    
    # 5. Determine what's missing
    data.needs_web_search = {
        'top_buy': len(data.top_buy) < 10,
        'top_sell': len(data.top_sell) < 10,
        'price_changes': any(s.price_change_percent == 0 for s in data.top_buy + data.top_sell),
        'foreign_flow': data.foreign_flow is None or data.foreign_flow.net_foreign == 0,
        'ytd': session == Session.CLOSING and (not data.foreign_flow or data.foreign_flow.ytd_net == 0)
    }
    
    # 6. Generate search queries for missing data
    year = datetime.now().year
    data.web_search_queries = []
    
    if data.needs_web_search['top_buy'] or data.needs_web_search['top_sell']:
        data.web_search_queries.extend([
            f"top 10 net buy sell saham Indonesia hari ini {year}",
            f"top foreign net buy sell IDX Indonesia today {year}",
        ])
    
    if data.needs_web_search['foreign_flow']:
        data.web_search_queries.extend([
            f"net foreign flow Bursa Efek Indonesia hari ini miliar {year}",
            f"aliran dana asing BEI hari ini {year}",
        ])
    
    if data.needs_web_search['ytd']:
        data.web_search_queries.extend([
            f"YTD foreign flow Indonesia stock exchange {year}",
            f"akumulasi dana asing BEI tahun ini {year}",
        ])
    
    # 7. Output
    if args.format or args.output == 'text':
        print(formatter.format_full_output(data))
    else:
        output_data = {
            'session': data.session,
            'date': data.date,
            'timestamp': data.timestamp,
            'ihsg': asdict(data.ihsg) if data.ihsg else None,
            'top_buy': [asdict(s) for s in data.top_buy],
            'top_sell': [asdict(s) for s in data.top_sell],
            'foreign_flow': asdict(data.foreign_flow) if data.foreign_flow else None,
            'needs_web_search': data.needs_web_search,
            'web_search_queries': data.web_search_queries,
            'tavily_available': tavily.is_available(),
            'instructions': {
                'if_tavily_available': 'Data fetched automatically via Tavily API',
                'if_tavily_unavailable': 'Set TAVILY_API_KEY environment variable',
                'cli_example': f'python3 ihsg_session_extractor.py {session.value} --use-tavily --tavily-api-key tvly-xxx'
            }
        }
        print(json.dumps(output_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
