#!/usr/bin/env python3
"""
Polymarket BTC 5分钟套利机器人
自动交易 BTC 涨跌预测市场
"""
import asyncio
import sys
import os
import time
import json
import logging
import requests
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - polymarket_btc_5m - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

# Config
POLYMARKET_PRIVATE_KEY = os.getenv('POLYMARKET_PRIVATE_KEY', '')
POLYMARKET_API_KEY = os.getenv('POLYMARKET_API_KEY', '')
SKILLPAY_API_KEY = os.getenv('SKILLPAY_API_KEY', 'sk_b2fe0f003da084ef5549b42c3c55869e3c0f67ea274d6376764c273fd833c76a')
SKILL_ID = 'c9eb1217-19a6-4bb7-92a1-b3b8bd938d93'

# API endpoints
GAMMA_API = "https://gamma-api.polymarket.com"
CLOB_API = "https://clob.polymarket.com"
SKILLPAY_API_URL = "https://skillpay.me"

# Trading params
MIN_LIQUIDITY = 1000  # 最小流动性
MIN_ORDER_SIZE = 5    # 最小订单量
MAX_SPREAD = 0.05     # 最大价差
CHARGE_PER_CALL = 0.001  # 每次调用扣费 (USDT)


def check_skillpay_payment(user_id: str = None) -> bool:
    """
    基于官方 SkillPay 示例检查用户支付
    https://skillpay.me
    """
    if not SKILLPAY_API_KEY:
        logger.warning("⚠️ 未配置 SKILLPAY_API_KEY，跳过支付检查")
        return True
    
    if not user_id:
        return True
    
    try:
        import requests
        
        headers = {
            'X-API-Key': SKILLPAY_API_KEY,
            'Content-Type': 'application/json'
        }
        
        # 尝试扣费
        resp = requests.post(
            f'{SKILLPAY_API_URL}/api/v1/billing/charge',
            json={
                'user_id': user_id,
                'skill_id': SKILL_ID,
                'amount': CHARGE_PER_CALL
            },
            headers=headers,
            timeout=10
        )
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('success'):
                logger.info(f"✅ 用户 {user_id} 已支付，余额: {data.get('balance')} USDT")
                return True
            else:
                logger.warning(f"⚠️ 用户 {user_id} 需要支付: {data.get('payment_url')}")
                return False
        elif resp.status_code == 402:
            logger.warning(f"⚠️ 用户 {user_id} 支付失败")
            return False
        else:
            logger.warning(f"⚠️ 支付检查失败: {resp.status_code}")
            return True
            
    except Exception as e:
        logger.warning(f"⚠️ 支付检查异常: {e}")
        return True


class PolymarketClient:
    """Polymarket API 客户端"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def get_markets(self, slug: str) -> Optional[Dict]:
        """获取市场信息"""
        url = f"{GAMMA_API}/markets"
        params = {'slug': slug}
        
        try:
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data[0] if data else None
        except Exception as e:
            logger.error(f"获取市场失败: {e}")
            return None
    
    def get_order_book(self, token_id: str) -> Dict:
        """获取订单簿"""
        url = f"{CLOB_API}/book"
        params = {'tokenId': token_id}
        
        try:
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"获取订单簿失败: {e}")
            return {'bids': [], 'asks': []}
    
    def get_markets_by_series(self, series_slug: str = "btc-up-or-down-5m") -> List[Dict]:
        """获取系列市场的所有活跃市场"""
        url = f"{GAMMA_API}/markets"
        params = {
            'active': 'true',
            'closed': 'false',
            'limit': 100
        }
        
        try:
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            all_markets = resp.json()
            
            # Filter for BTC 5m markets - check multiple patterns
            btc_markets = []
            for m in all_markets:
                slug = m.get('slug', '').lower()
                question = m.get('question', '').lower()
                series_slug_lower = series_slug.lower()
                
                # Match various patterns
                if ('btc' in slug or 'btc' in question) and ('5m' in slug or '5m' in question or '5 minute' in question):
                    btc_markets.append(m)
                elif 'updown' in slug or 'up-or-down' in slug:
                    btc_markets.append(m)
                    
            return btc_markets
        except Exception as e:
            logger.error(f"获取市场列表失败: {e}")
            return []


def calculate_spread(best_bid: float, best_ask: float) -> float:
    """计算价差"""
    if best_bid == 0:
        return 1.0
    return (best_ask - best_bid) / best_bid


def find_arbitrage_opportunity(order_book: Dict) -> Optional[Dict]:
    """寻找套利机会"""
    bids = order_book.get('bids', [])
    asks = order_book.get('asks', [])
    
    if not bids or not asks:
        return None
    
    best_bid = float(bids[0].get('price', 0))
    best_ask = float(asks[0].get('price', 0))
    spread = calculate_spread(best_bid, best_ask)
    
    # 检查是否有套利机会
    if best_bid + best_ask < 1.0:
        return {
            'type': 'pair_arbitrage',
            'buy_yes': best_bid,
            'sell_no': best_ask,
            'profit': 1.0 - (best_bid + best_ask)
        }
    
    # 检查价差是否足够大
    if spread > MAX_SPREAD:
        return {
            'type': 'wide_spread',
            'best_bid': best_bid,
            'best_ask': best_ask,
            'spread': spread
        }
    
    return None


async def scan_and_trade():
    """扫描市场并交易"""
    # SkillPay 支付检查 (可选)
    if not check_skillpay_payment():
        logger.warning("⚠️ 支付检查未通过，跳过交易")
        return
    
    client = PolymarketClient()
    
    logger.info("🔍 扫描 BTC 5分钟市场...")
    
    markets = client.get_markets_by_series()
    
    if not markets:
        logger.warning("⚠️ 未发现活跃市场")
        return
    
    logger.info(f"📊 发现 {len(markets)} 个 BTC 5分钟市场")
    
    for market in markets[:5]:  # 处理前5个市场
        slug = market.get('slug', '')
        question = market.get('question', '')
        liquidity = float(market.get('liquidity', 0))
        
        logger.info(f"\n📌 {question[:50]}...")
        logger.info(f"   流动性: ${liquidity:,.2f}")
        
        if liquidity < MIN_LIQUIDITY:
            logger.info("   跳过: 流动性不足")
            continue
        
        # 获取订单簿
        clob_token_ids = market.get('clobTokenIds', '[]')
        try:
            token_ids = json.loads(clob_token_ids)
        except:
            token_ids = []
        
        if not token_ids:
            continue
        
        # 分析每个 token
        for i, token_id in enumerate(token_ids[:2]):
            outcome = market.get('outcomes', '["Up", "Down"]')
            try:
                outcomes = json.loads(outcome)
            except:
                outcomes = ['Up', 'Down']
            
            outcome_name = outcomes[i] if i < len(outcomes) else f"Token{i}"
            
            order_book = client.get_order_book(token_id)
            
            if not order_book.get('bids') or not order_book.get('asks'):
                continue
            
            best_bid = float(order_book['bids'][0].get('price', 0))
            best_ask = float(order_book['asks'][0].get('price', 0))
            spread = calculate_spread(best_bid, best_ask)
            
            logger.info(f"   {outcome_name}: Bid ${best_bid:.2f} | Ask ${best_ask:.2f} | 价差 {spread*100:.1f}%")
            
            # 寻找套利机会
            arb = find_arbitrage_opportunity(order_book)
            if arb:
                logger.info(f"   ⚠️ 套利机会: {arb}")


async def main():
    """主函数"""
    logger.info("🚀 Polymarket BTC 5分钟套利机器人启动")
    logger.info(f"📡 API: {GAMMA_API}")
    
    while True:
        try:
            await scan_and_trade()
        except Exception as e:
            logger.error(f"错误: {e}")
        
        await asyncio.sleep(30)  # 每30秒扫描一次


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 机器人已停止")
