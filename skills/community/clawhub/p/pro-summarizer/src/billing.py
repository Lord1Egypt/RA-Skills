import requests
import os

BILLING_API_URL = 'https://skillpay.me'
# 这里暂时使用占位符，用户后续会自己申请并替换真实的 API Key 和 Skill ID
BILLING_API_KEY = os.getenv('SKILLPAY_API_KEY', 'sk_YOUR_KEY_HERE')
SKILL_ID = os.getenv('SKILLPAY_SKILL_ID', 'YOUR_SKILL_ID_HERE')

HEADERS = {'X-API-Key': BILLING_API_KEY, 'Content-Type': 'application/json'}

def check_and_charge(user_id: str) -> dict:
    # 每次调用扣除 0.001 USDT
    resp = requests.post(
        f'{BILLING_API_URL}/api/v1/billing/charge', 
        headers=HEADERS, 
        json={'user_id': user_id, 'skill_id': SKILL_ID, 'amount': 0.001}
    )
    data = resp.json()
    if data.get('success'):
        return {'ok': True, 'balance': data.get('balance')}
    return {'ok': False, 'payment_url': data.get('payment_url')}