"""
支付 API 客户端
"""

import aiohttp
import json
import logging
import time
import hmac
import hashlib
import base64
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class PaymentAPIClient:
    """支付 API 客户端"""
    
    def __init__(self, api_key: str, api_secret: str, api_url: str, timeout: int = 30):
        """
        初始化 API 客户端
        
        参数:
            api_key: API 密钥（用于身份认证）
            api_secret: API 密钥（用于请求签名）
            api_url: API 地址
            timeout: 超时时间(秒)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _ensure_session(self):
        """确保会话已创建"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def _request(self, method: str, endpoint: str,
                      data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        发送 HTTP 请求
        
        参数:
            method: HTTP 方法
            endpoint: API 端点
            data: 请求数据
        
        返回:
            响应数据
        """
        await self._ensure_session()
        
        url = f"{self.api_url}/{endpoint}"
        
        # 生成请求签名
        signature = self._generate_signature(method, endpoint, data)
        timestamp = str(int(time.time()))
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Signature": signature,
            "X-Timestamp": timestamp,
            "Content-Type": "application/json"
        }
        
        try:
            async with self.session.request(
                method, url,
                json=data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                response_data = await response.json()
                
                if response.status == 200:
                    logger.debug(f"API 请求成功: {method} {endpoint}")
                    return response_data
                else:
                    error_msg = response_data.get("error", "未知错误")
                    logger.error(f"API 请求失败: {response.status} - {error_msg}")
                    raise Exception(f"API 错误: {response.status} - {error_msg}")
        
        except aiohttp.ClientError as e:
            logger.error(f"网络错误: {e}")
            raise Exception(f"网络错误: {str(e)}")
    
    def _generate_signature(self, method: str, endpoint: str,
                           data: Dict[str, Any] = None) -> str:
        """
        生成请求签名
        
        参数:
            method: HTTP 方法
            endpoint: API 端点
            data: 请求数据
        
        返回:
            签名字符串
        """
        timestamp = str(int(time.time()))
        message = f"{method}:{endpoint}:{timestamp}"
        
        if data:
            message += f":{json.dumps(data, sort_keys=True)}"
        
        # 使用 HMAC-SHA256 签名（使用 api_secret）
        signature = hmac.new(
            key=self.api_secret.encode(),
            msg=message.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        return signature
    
    async def health_check(self) -> bool:
        """
        健康检查
        
        返回:
            是否健康
        """
        try:
            result = await self._request("GET", "health")
            return result.get("status") == "ok"
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return False
    
    async def create_payment(self, amount: float, currency: str,
                            merchant_id: str, description: str = "") -> Dict[str, Any]:
        """
        创建支付
        
        参数:
            amount: 支付金额
            currency: 货币代码
            merchant_id: 商户 ID
            description: 支付描述
        
        返回:
            支付结果
        """
        payload = {
            "amount": amount,
            "currency": currency,
            "merchant_id": merchant_id,
            "description": description
        }
        
        result = await self._request("POST", "v1/payments", payload)
        
        return {
            "id": result.get("id"),
            "status": result.get("status"),
            "amount": result.get("amount"),
            "currency": result.get("currency"),
            "verification_url": result.get("verification_url"),
            "qr_code": result.get("qr_code"),
            "expires_at": result.get("expires_at")
        }
    
    async def query_payment(self, transaction_id: str) -> Dict[str, Any]:
        """
        查询支付状态
        
        参数:
            transaction_id: 交易 ID
        
        返回:
            支付状态
        """
        result = await self._request("GET", f"v1/payments/{transaction_id}")
        
        return {
            "id": result.get("id"),
            "status": result.get("status"),
            "amount": result.get("amount"),
            "currency": result.get("currency"),
            "created_at": result.get("created_at"),
            "completed_at": result.get("completed_at")
        }
    
    async def refund_payment(self, transaction_id: str,
                            amount: float = None) -> Dict[str, Any]:
        """
        发起退款
        
        参数:
            transaction_id: 原交易 ID
            amount: 退款金额(可选)
        
        返回:
            退款结果
        """
        payload = {}
        if amount is not None:
            payload["amount"] = amount
        
        result = await self._request(
            "POST",
            f"v1/payments/{transaction_id}/refund",
            payload
        )
        
        return {
            "id": result.get("id"),
            "status": result.get("status"),
            "amount": result.get("amount"),
            "currency": result.get("currency"),
            "created_at": result.get("created_at")
        }
    
    async def close(self):
        """关闭连接"""
        if self.session:
            await self.session.close()
