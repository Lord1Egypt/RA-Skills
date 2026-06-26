#!/usr/bin/env python3
"""
Polymarket Volume Tracker
Tracks top markets by trading volume in the last 10 minutes
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
import urllib.request
import urllib.error


class SkillPayClient:
    """skillpay.me payment integration"""
    
    def __init__(self, api_key: str, skill_id: str = "ae30e94b-6cf4-444a-b734-f0ad65a50565"):
        self.api_key = api_key
        self.skill_id = skill_id
        self.base_url = "https://skillpay.me"
    
    def check_balance(self, user_id: str) -> float:
        """
        Check user balance
        
        Args:
            user_id: User identifier
        
        Returns:
            Balance in USDT
        """
        url = f"{self.base_url}/api/v1/billing/balance?user_id={user_id}"
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('balance', 0.0)
        except Exception as e:
            print(f"Error checking balance: {e}", file=sys.stderr)
            return 0.0
    
    def charge_user(self, user_id: str, amount: float = 0.001) -> Dict[str, Any]:
        """
        Charge user for skill usage
        
        Args:
            user_id: User identifier
            amount: Amount to charge in USDT (default: 0.001)
        
        Returns:
            Charge result with success status and new balance
        """
        url = f"{self.base_url}/api/v1/billing/charge"
        
        data = {
            "user_id": user_id,
            "skill_id": self.skill_id,
            "amount": amount
        }
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if result.get('success'):
                    return {
                        "success": True,
                        "balance": result.get('balance', 0.0),
                        "transaction_id": result.get('transaction_id')
                    }
                else:
                    # Insufficient balance - return payment URL
                    return {
                        "success": False,
                        "balance": result.get('balance', 0.0),
                        "payment_url": result.get('payment_url'),
                        "error": "Insufficient balance"
                    }
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            return {
                "success": False,
                "error": f"Payment failed: {e.code} - {error_body}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Payment error: {str(e)}"
            }
    
    def get_payment_link(self, user_id: str, amount: float) -> str:
        """
        Generate payment link for user to top up balance
        
        Args:
            user_id: User identifier
            amount: Amount to top up in USDT
        
        Returns:
            Payment URL (BNB Chain USDT)
        """
        url = f"{self.base_url}/api/v1/billing/payment-link"
        
        data = {
            "user_id": user_id,
            "amount": amount
        }
        
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('payment_url', '')
        except Exception as e:
            print(f"Error generating payment link: {e}", file=sys.stderr)
            return ""


class PolymarketClient:
    """Polymarket API client"""
    
    def __init__(self):
        self.base_url = "https://gamma-api.polymarket.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
    
    def get_markets(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch active markets from Polymarket
        
        Args:
            limit: Maximum number of markets to fetch
        
        Returns:
            List of market data
        """
        url = f"{self.base_url}/markets?closed=false&_l={limit}"
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data if isinstance(data, list) else []
        except Exception as e:
            print(f"Error fetching markets: {e}", file=sys.stderr)
            return []
    
    def get_recent_trades(self, market_id: str, minutes: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent trades for a market using CLOB API
        
        Args:
            market_id: Market identifier (conditionId)
            minutes: Time window in minutes
        
        Returns:
            List of recent trades
        """
        url = f"https://clob.polymarket.com/trades?condition_id={market_id}"
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                trades = json.loads(response.read().decode('utf-8'))
                
                if not isinstance(trades, list):
                    return []
                
                # Filter trades within time window
                cutoff_time = datetime.now() - timedelta(minutes=minutes)
                recent_trades = []
                
                for trade in trades:
                    if 'timestamp' in trade:
                        try:
                            trade_time = datetime.fromisoformat(trade['timestamp'].replace('Z', '+00:00').replace('+00:00', ''))
                            if trade_time > cutoff_time:
                                recent_trades.append(trade)
                        except:
                            continue
                
                return recent_trades
        except Exception as e:
            # Silently fail for individual markets
            return []


def calculate_volume_data(trades: List[Dict[str, Any]], market_data: Dict[str, Any] = None) -> Dict[str, float]:
    """
    Calculate volume data from trades or market data
    
    Args:
        trades: List of trade data
        market_data: Market data from gamma API (optional)
    
    Returns:
        Volume breakdown by side (Yes/No)
    """
    # If we have market data with volume, use it directly
    if market_data and 'volume' in market_data:
        total_volume = float(market_data.get('volumeNum', 0))
        # Estimate split based on outcome prices (rough approximation)
        if 'outcomePrices' in market_data:
            prices = market_data['outcomePrices']
            if isinstance(prices, list) and len(prices) == 2:
                yes_price = float(prices[0])
                no_price = float(prices[1])
                price_sum = yes_price + no_price
                if price_sum > 0:
                    return {
                        'yes_volume': total_volume * (yes_price / price_sum),
                        'no_volume': total_volume * (no_price / price_sum),
                        'total_volume': total_volume
                    }
        return {
            'yes_volume': total_volume * 0.5,
            'no_volume': total_volume * 0.5,
            'total_volume': total_volume
        }
    
    # Otherwise calculate from trades
    yes_volume = 0.0
    no_volume = 0.0
    
    for trade in trades:
        side = trade.get('side', '').upper()
        amount = float(trade.get('amount', 0))
        
        if side == 'YES':
            yes_volume += amount
        elif side == 'NO':
            no_volume += amount
    
    return {
        'yes_volume': yes_volume,
        'no_volume': no_volume,
        'total_volume': yes_volume + no_volume
    }


def format_output(markets: List[Dict[str, Any]]) -> str:
    """
    Format market data for display
    
    Args:
        markets: List of market data with volume info
    
    Returns:
        Formatted string output
    """
    output = []
    output.append("=" * 60)
    output.append("Top 10 Polymarket Markets (Last 10 Minutes)")
    output.append("=" * 60)
    output.append("")
    
    for i, market in enumerate(markets, 1):
        output.append(f"{i}. {market['name']}")
        output.append(f"   - Yes Volume: ${market['yes_volume']:,.2f}")
        output.append(f"   - No Volume: ${market['no_volume']:,.2f}")
        
        # Format odds as percentages
        yes_odds = market.get('yes_odds', 0) * 100
        no_odds = market.get('no_odds', 0) * 100
        output.append(f"   - Yes Odds: {yes_odds:.1f}%")
        output.append(f"   - No Odds: {no_odds:.1f}%")
        output.append(f"   - Total Volume: ${market['total_volume']:,.2f}")
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Track top Polymarket markets by volume"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="skillpay.me API key for payment"
    )
    parser.add_argument(
        "--user-id",
        default="default_user",
        help="User identifier for billing (default: default_user)"
    )
    parser.add_argument(
        "--minutes",
        type=int,
        default=10,
        help="Time window in minutes (default: 10)"
    )
    parser.add_argument(
        "--skip-payment",
        action="store_true",
        help="Skip payment (for testing)"
    )
    parser.add_argument(
        "--check-balance",
        action="store_true",
        help="Only check balance without charging"
    )
    
    args = parser.parse_args()
    
    # Initialize SkillPay client
    skillpay = SkillPayClient(args.api_key)
    
    # Check balance only
    if args.check_balance:
        balance = skillpay.check_balance(args.user_id)
        print(f"Current balance: ${balance:.4f} USDT")
        sys.exit(0)
    
    # Process payment
    if not args.skip_payment:
        print(f"Checking balance for user: {args.user_id}", file=sys.stderr)
        balance = skillpay.check_balance(args.user_id)
        
        if balance < 0.001:
            print(f"⚠️  Insufficient balance: ${balance:.4f} USDT", file=sys.stderr)
            print(f"Minimum required: 0.001 USDT", file=sys.stderr)
            
            # Generate payment link
            payment_url = skillpay.get_payment_link(args.user_id, 1.0)
            if payment_url:
                print(f"\n💳 Top up your balance here:", file=sys.stderr)
                print(f"{payment_url}", file=sys.stderr)
            sys.exit(1)
        
        print(f"Charging 0.001 USDT...", file=sys.stderr)
        payment_result = skillpay.charge_user(args.user_id, 0.001)
        
        if not payment_result.get("success"):
            print(f"❌ Payment failed: {payment_result.get('error')}", file=sys.stderr)
            
            if payment_result.get('payment_url'):
                print(f"\n💳 Top up your balance here:", file=sys.stderr)
                print(f"{payment_result['payment_url']}", file=sys.stderr)
            
            sys.exit(1)
        
        print(f"✅ Payment successful. Remaining balance: ${payment_result['balance']:.4f} USDT", file=sys.stderr)
    
    # Fetch market data
    print("Fetching Polymarket data...", file=sys.stderr)
    polymarket = PolymarketClient()
    markets = polymarket.get_markets(limit=100)
    
    if not markets:
        print("No markets found", file=sys.stderr)
        sys.exit(0)
    
    print(f"Found {len(markets)} active markets", file=sys.stderr)
    
    # Process markets - gamma API already has volume data
    market_volumes = []
    
    for market in markets:
        # Get market data
        question = market.get('question', 'Unknown')
        volume_num = float(market.get('volumeNum', 0))
        outcome_prices_raw = market.get('outcomePrices', ['0.5', '0.5'])
        
        # Parse outcome prices (might be string or list)
        if isinstance(outcome_prices_raw, str):
            try:
                outcome_prices = json.loads(outcome_prices_raw)
            except:
                outcome_prices = ['0.5', '0.5']
        else:
            outcome_prices = outcome_prices_raw
        
        if volume_num > 0 and outcome_prices[0] not in ['0', 0, 0.0]:
            yes_price = float(outcome_prices[0]) if len(outcome_prices) > 0 else 0.5
            no_price = float(outcome_prices[1]) if len(outcome_prices) > 1 else 0.5
            
            # Estimate volume split (approximate)
            price_sum = yes_price + no_price
            if price_sum > 0:
                yes_volume = volume_num * (yes_price / price_sum)
                no_volume = volume_num * (no_price / price_sum)
            else:
                yes_volume = volume_num * 0.5
                no_volume = volume_num * 0.5
            
            market_data = {
                'name': question,
                'yes_volume': yes_volume,
                'no_volume': no_volume,
                'total_volume': volume_num,
                'yes_odds': yes_price,
                'no_odds': no_price
            }
            market_volumes.append(market_data)
    
    # Sort by total volume and get top 10
    market_volumes.sort(key=lambda x: x['total_volume'], reverse=True)
    top_markets = market_volumes[:10]
    
    # Output results
    if top_markets:
        print(format_output(top_markets))
    else:
        print("No markets with trading activity in the specified time window", file=sys.stderr)


if __name__ == "__main__":
    main()
