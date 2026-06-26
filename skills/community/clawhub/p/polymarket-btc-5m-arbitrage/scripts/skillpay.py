#!/usr/bin/env python3
"""
SkillPay Billing Client
官方接入代码 Python 版本
https://skillpay.me
"""
import os
import requests
from typing import Dict, Optional

# SkillPay 配置
BILLING_API_URL = os.getenv('SKILLPAY_API_URL', 'https://skillpay.me')
BILLING_API_KEY = os.getenv('SKILLPAY_API_KEY', 'sk_b2fe0f003da084ef5549b42c3c55869e3c0f67ea274d6376764c273fd833c76a')
SKILL_ID = 'c9eb1217-19a6-4bb7-92a1-b3b8bd938d93'


class SkillPayClient:
    """SkillPay 计费客户端"""
    
    def __init__(self, api_key: str = None, skill_id: str = None):
        self.api_key = api_key or BILLING_API_KEY
        self.skill_id = skill_id or SKILL_ID
        self.api_url = BILLING_API_URL
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def check_balance(self, user_id: str) -> float:
        """
        ① Check balance / 查余额
        Returns: USDT amount
        """
        try:
            resp = self.session.get(
                f'{self.api_url}/api/v1/billing/balance',
                params={'user_id': user_id},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                return float(data.get('balance', 0))
            return 0
        except Exception as e:
            print(f"Balance check error: {e}")
            return 0
    
    def charge_user(self, user_id: str, amount: float = 0.001) -> Dict:
        """
        ② Charge per call / 每次调用扣费
        
        Returns:
            {"ok": True, "balance": xxx} - 扣费成功
            {"ok": False, "balance": xxx, "payment_url": "..."} - 余额不足
        """
        try:
            resp = self.session.post(
                f'{self.api_url}/api/v1/billing/charge',
                json={
                    'user_id': user_id,
                    'skill_id': self.skill_id,
                    'amount': amount
                },
                timeout=30
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    return {
                        'ok': True,
                        'balance': float(data.get('balance', 0))
                    }
                else:
                    # 余额不足
                    return {
                        'ok': False,
                        'balance': float(data.get('balance', 0)),
                        'payment_url': data.get('payment_url', '')
                    }
            elif resp.status_code == 402:
                # 支付失败
                data = resp.json()
                return {
                    'ok': False,
                    'balance': 0,
                    'payment_url': data.get('payment_url', f'{self.api_url}/pay/{user_id}')
                }
            else:
                return {
                    'ok': False,
                    'error': f'API Error: {resp.status_code}'
                }
                
        except Exception as e:
            return {
                'ok': False,
                'error': str(e)
            }
    
    def get_payment_link(self, user_id: str, amount: float = 10) -> str:
        """
        ③ Generate payment link / 生成充值链接
        """
        try:
            resp = self.session.post(
                f'{self.api_url}/api/v1/billing/payment-link',
                json={
                    'user_id': user_id,
                    'amount': amount
                },
                timeout=30
            )
            
            if resp.status_code == 200:
                data = resp.json()
                return data.get('payment_url', '')
            return ''
        except Exception as e:
            print(f"Payment link error: {e}")
            return ''


def handle_request(user_id: str, skill_logic_func, amount: float = 0.001) -> Dict:
    """
    完整的请求处理函数
    
    Args:
        user_id: 用户ID
        skill_logic_func: 技能逻辑函数 (无参数)
        amount: 每次调用费用 (USDT)
    
    Returns:
        {"success": True, ...} - 执行成功
        {"success": False, "paymentUrl": "..."} - 需要支付
    """
    client = SkillPayClient()
    result = client.charge_user(user_id, amount)
    
    if result.get('ok'):
        # ✅ 执行技能逻辑
        try:
            skill_result = skill_logic_func()
            return {
                'success': True,
                'balance': result['balance'],
                'result': skill_result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    else:
        # ❌ 余额不足，返回支付链接
        return {
            'success': False,
            'payment_url': result.get('payment_url', ''),
            'balance': result.get('balance', 0)
        }


# 示例用法
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python skillpay.py <user_id>")
        sys.exit(1)
    
    user_id = sys.argv[1]
    client = SkillPayClient()
    
    # 示例：检查余额
    balance = client.check_balance(user_id)
    print(f"User {user_id} balance: {balance} USDT")
    
    # 示例：扣费
    result = client.charge_user(user_id)
    print(f"Charge result: {result}")
