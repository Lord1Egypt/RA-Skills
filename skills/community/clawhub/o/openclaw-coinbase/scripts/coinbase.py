# Klara's Coinbase API Helper
# Uses Coinbase App API (CDP) with JWT authentication

import jwt
from cryptography.hazmat.primitives import serialization
import time
import secrets
import json
import os

# Configuration
API_KEY_FILE = os.path.join(os.path.dirname(__file__), '.coinbase-api-key')
API_SECRET_FILE = os.path.join(os.path.dirname(__file__), '.coinbase-api-secret')
BASE_URL = "api.coinbase.com"

def _load_credentials():
    """Load API credentials from files"""
    with open(API_KEY_FILE, 'r') as f:
        api_key = f.read().strip()
    with open(API_SECRET_FILE, 'r') as f:
        api_secret = f.read().strip()
    return api_key, api_secret

def _build_jwt(uri, api_key, api_secret):
    """Build JWT token for authentication"""
    private_key_bytes = api_secret.encode('utf-8')
    private_key = serialization.load_pem_private_key(private_key_bytes, password=None)
    jwt_payload = {
        'sub': api_key,
        'iss': "cdp",
        'nbf': int(time.time()),
        'exp': int(time.time()) + 120,
        'uri': uri,
    }
    jwt_token = jwt.encode(
        jwt_payload,
        private_key,
        algorithm='ES256',
        headers={'kid': api_key, 'nonce': secrets.token_hex()},
    )
    return jwt_token

def _make_request(method, path, body=None):
    """Make authenticated request to Coinbase API"""
    api_key, api_secret = _load_credentials()
    uri = f"{method} {BASE_URL}{path}"
    jwt_token = _build_jwt(uri, api_key, api_secret)
    
    import urllib.request
    
    url = f"https://{BASE_URL}{path}"
    if method == "GET":
        req = urllib.request.Request(url)
    else:
        req = urllib.request.Request(url, data=body.encode() if body else None, method=method)
    
    req.add_header('Authorization', f'Bearer {jwt_token}')
    req.add_header('Content-Type', 'application/json')
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def get_accounts():
    """Get all accounts"""
    return _make_request("GET", "/api/v3/brokerage/accounts")

def get_account(currency):
    """Get specific account by currency"""
    accounts = get_accounts()
    for account in accounts.get('accounts', []):
        if account['currency'] == currency:
            return account
    return None

def get_balance(currency):
    """Get balance for a specific currency"""
    account = get_account(currency)
    if account:
        return account['available_balance']['value']
    return None

def get_euro_balance():
    """Get EUR balance"""
    return get_balance('EUR')

def get_btc_balance():
    """Get BTC balance"""
    return get_balance('BTC')

def get_all_balances():
    """Get all account balances"""
    accounts = get_accounts()
    balances = {}
    for account in accounts.get('accounts', []):
        balances[account['currency']] = account['available_balance']['value']
    return balances

def get_products():
    """Get available trading products"""
    return _make_request("GET", "/api/v3/brokerage/products")

def get_product(product_id):
    """Get specific product details"""
    return _make_request("GET", f"/api/v3/brokerage/products/{product_id}")

def get_product_book(product_id):
    """Get order book for a product"""
    return _make_request("GET", f"/api/v3/brokerage/products/{product_id}/ticker")

def get_eur_products():
    """Get all EUR trading pairs"""
    products = get_products()
    eur_products = []
    for p in products.get('products', []):
        if 'EUR' in p.get('product_id', ''):
            eur_products.append(p)
    return eur_products

def create_order(product_id, side, size, price=None, order_type="MARKET"):
    """Create an order
    
    Args:
        product_id: Trading pair (e.g., 'BTC-EUR')
        side: 'BUY' or 'SELL'
        size: Amount to trade (in base currency, e.g., BTC amount)
        price: Limit price (optional, for LIMIT orders)
        order_type: 'MARKET' or 'LIMIT'
    """
    import time
    import secrets
    
    client_order_id = f"klara-{int(time.time())}-{secrets.token_hex(4)}"
    
    if order_type == "MARKET":
        # Use IOC (Immediate or Cancel) market order
        order_config = {
            "market_market_ioc": {
                "base_size": str(size)
            }
        }
    else:
        # Limit order (GTC - Good Till Cancel)
        order_config = {
            "limit_limit_gtc": {
                "base_size": str(size),
                "limit_price": str(price) if price else None
            }
        }
    
    body = {
        "client_order_id": client_order_id,
        "product_id": product_id,
        "side": side.upper(),
        "order_configuration": order_config
    }
    
    return _make_request("POST", "/api/v3/brokerage/orders", json.dumps(body))

def get_orders():
    """Get all orders"""
    return _make_request("GET", "/api/v3/brokerage/orders/historical/batch")

def get_fills(product_id=None):
    """Get recent fills (trades)"""
    path = "/api/v3/brokerage/orders/historical/fills"
    if product_id:
        path += f"?product_id={product_id}"
    return _make_request("GET", path)

if __name__ == "__main__":
    # Test
    print("Accounts:", get_accounts())