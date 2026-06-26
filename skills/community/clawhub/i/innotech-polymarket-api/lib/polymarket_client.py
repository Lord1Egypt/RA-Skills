#!/usr/bin/env python3
"""
Polymarket API Client - Reusable client for Polymarket CLOB API

Provides:
- CLOB API client initialization
- Market order placement (FOK)
- Wallet balance queries
- Market info fetching
- Automatic API credential derivation from private key

Installation:
    pip install py-clob-client

Usage:
    from lib.polymarket_client import PolymarketClient
    
    client = PolymarketClient(
        private_key="0x...",
        wallet_address="0x...",
        signature_type=0
    )
    await client.init_client()
    
    # Place market order
    await client.place_market_order(
        asset_id="123...",
        side="BUY",
        amount=10.0,
        price=0.50
    )
"""

import asyncio
import time
import math
from typing import Dict, Optional, Any
import aiohttp

# Try to import Polymarket SDK
try:
    from py_clob_client.client import ClobClient
    from py_clob_client.clob_types import OrderArgs, OrderType
    PY_CLOB_CLIENT_AVAILABLE = True
except ImportError:
    PY_CLOB_CLIENT_AVAILABLE = False


class PolymarketClient:
    """
    Client for Polymarket CLOB API (real trading)

    Uses official Polymarket SDK (py-clob-client) for:
    - Automatic API credential derivation from private key
    - Order placement and management
    - Wallet balance queries

    See: https://docs.polymarket.com/api-reference/authentication
    """

    def __init__(self, private_key: str, wallet_address: str, signature_type: int = 0):
        """
        Initialize Polymarket client

        Args:
            private_key: Wallet private key (0x...)
            wallet_address: Wallet address (funder address)
            signature_type: 0=EOA, 1=POLY_PROXY, 2=GNOSIS_SAFE
        """
        if not PY_CLOB_CLIENT_AVAILABLE:
            raise ImportError("py-clob-client is required for real trading. Install with: pip install py-clob-client")

        self.private_key = private_key
        self.wallet_address = wallet_address
        self.signature_type = signature_type
        self.client: Optional[ClobClient] = None
        self.api_creds: Optional[Dict] = None
        
        # Cached parameters (for fast order placement)
        self.tick_sizes: Dict[str, float] = {}
        self.neg_risks: Dict[str, bool] = {}
        
        # Nonce counter for unique order IDs
        self.nonce_counter = 0

    async def init_client(self):
        """
        Initialize CLOB client and derive API credentials

        According to Polymarket docs:
        - L1 auth uses private key to derive L2 API credentials
        """
        loop = asyncio.get_event_loop()
        
        # Create client in thread (SDK is sync)
        def create_client():
            client = ClobClient(
                host="https://clob.polymarket.com",
                key=self.private_key,
                chain_id=137,  # Polygon mainnet
                signature_type=self.signature_type
            )
            # Derive API credentials from private key
            creds = client.derive_api_key()
            return client, creds
        
        self.client, self.api_creds = await loop.run_in_executor(None, create_client)

    async def get_tick_size(self, asset_id: str) -> float:
        """
        Get tick size for an asset (with caching)
        
        Args:
            asset_id: Token ID
            
        Returns:
            Tick size (minimum price increment)
        """
        if asset_id in self.tick_sizes:
            return self.tick_sizes[asset_id]
        
        loop = asyncio.get_event_loop()
        
        def fetch():
            return self.client.get_tick_size(asset_id)
        
        tick_size = await loop.run_in_executor(None, fetch)
        self.tick_sizes[asset_id] = float(tick_size)
        return self.tick_sizes[asset_id]

    async def get_neg_risk(self, asset_id: str) -> bool:
        """
        Get negative risk status for an asset (with caching)
        
        Args:
            asset_id: Token ID
            
        Returns:
            True if negative risk market
        """
        if asset_id in self.neg_risks:
            return self.neg_risks[asset_id]
        
        loop = asyncio.get_event_loop()
        
        def fetch():
            return self.client.get_neg_risk(asset_id)
        
        neg_risk = await loop.run_in_executor(None, fetch)
        self.neg_risks[asset_id] = bool(neg_risk)
        return self.neg_risks[asset_id]

    async def place_market_order(
        self,
        asset_id: str,
        side: str,
        amount: float,
        price: float,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Place a FOK (Fill-Or-Kill) market order
        
        Args:
            asset_id: Token ID to trade
            side: "BUY" or "SELL"
            amount: Amount in USD
            price: Price (slippage protection, can be 0 for immediate fill)
            dry_run: If True, simulate order without placing
            
        Returns:
            Dict with order details or error
        """
        if dry_run:
            return {
                'status': 'dry_run',
                'asset_id': asset_id,
                'side': side,
                'amount': amount,
                'price': price
            }
        
        # Generate unique nonce
        self.nonce_counter += 1
        nonce = str(int(time.time() * 1000000) + self.nonce_counter)
        
        loop = asyncio.get_event_loop()
        
        def place_order():
            # Create order using SDK
            order_args = OrderArgs(
                token_id=asset_id,
                price=price,
                size=amount,
                side=side,
                nonce=nonce,
                expiration=0,  # GTC (Good-Til-Canceled)
            )
            
            # Post order
            resp = self.client.post_order(order_args, OrderType.FOK)
            return resp
        
        try:
            result = await loop.run_in_executor(None, place_order)
            return {
                'status': 'success',
                'order': result,
                'asset_id': asset_id,
                'side': side,
                'amount': amount,
                'price': price
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'asset_id': asset_id,
                'side': side,
                'amount': amount,
                'price': price
            }

    async def get_balance(self) -> Dict[str, Any]:
        """
        Get wallet balance
        
        Returns:
            Dict with balance info
        """
        loop = asyncio.get_event_loop()
        
        def fetch():
            return self.client.get_balance()
        
        try:
            balance = await loop.run_in_executor(None, fetch)
            return {
                'status': 'success',
                'balance': balance
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    @staticmethod
    async def get_market_info(slug: str) -> Optional[Dict]:
        """
        Get market info from Gamma API
        
        Args:
            slug: Market slug (e.g., "btc-updown-5m-1234567890")
            
        Returns:
            Market data dict or None
        """
        async with aiohttp.ClientSession() as session:
            url = "https://gamma-api.polymarket.com/markets"
            params = {"slug": slug}
            
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data:
                        return data[0]
            return None

    @staticmethod
    async def get_all_markets(active_only: bool = True, limit: int = 100) -> list:
        """
        Get all markets from Gamma API
        
        Args:
            active_only: If True, only return active markets
            limit: Maximum number of markets to return
            
        Returns:
            List of market data dicts
        """
        async with aiohttp.ClientSession() as session:
            url = "https://gamma-api.polymarket.com/markets"
            params = {
                "limit": limit
            }
            if active_only:
                params["active"] = "true"
            
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    return await resp.json()
            return []
