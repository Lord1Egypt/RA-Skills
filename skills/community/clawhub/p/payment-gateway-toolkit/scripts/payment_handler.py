"""
Payment Gateway Handler - 支付网关处理器
支持 Stripe、支付宝等多渠道支付
"""

import stripe
from alipay import AliPay
from typing import Dict, Optional, Any
import requests
import json
from datetime import datetime


class PaymentHandler:
    """
    支付处理器主类
    集成多种支付渠道的统一处理接口
    """
    
    def __init__(self, 
                 stripe_key: Optional[str] = None,
                 alipay_config: Optional[Dict] = None):
        """
        初始化支付处理器
        
        Args:
            stripe_key: Stripe API密钥
            alipay_config: 支付宝配置字典
        """
        self.stripe_key = stripe_key
        self.alipay_config = alipay_config
        self.order_history = []
        
        # 初始化Stripe
        if stripe_key:
            stripe.api_key = stripe_key
            self.stripe_enabled = True
        else:
            self.stripe_enabled = False
            
        # 初始化支付宝
        if alipay_config:
            self.alipay = AliPay(
                appid=alipay_config.get("app_id"),
                app_notify_url=alipay_config.get("notify_url", ""),
                app_private_key_string=alipay_config.get("private_key"),
                alipay_public_key_string=alipay_config.get("alipay_public_key"),
                sign_type="RSA2",
                debug=alipay_config.get("debug", False)
            )
            self.alipay_enabled = True
        else:
            self.alipay_enabled = False
    
    def create_stripe_order(self, 
                           amount: float, 
                           currency: str = "usd",
                           description: str = "",
                           metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        创建Stripe支付订单
        
        Args:
            amount: 金额
            currency: 货币代码 (默认usd)
            description: 订单描述
            metadata: 附加元数据
            
        Returns:
            订单信息字典
        """
        if not self.stripe_enabled:
            raise ValueError("Stripe not initialized. Please provide stripe_key.")
        
        try:
            # 创建PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Stripe使用最小货币单位
                currency=currency.lower(),
                description=description,
                metadata=metadata or {}
            )
            
            order_info = {
                "provider": "stripe",
                "order_id": intent.id,
                "client_secret": intent.client_secret,
                "amount": amount,
                "currency": currency,
                "status": intent.status,
                "created_at": datetime.now().isoformat(),
                "description": description
            }
            
            self.order_history.append(order_info)
            return order_info
            
        except stripe.error.StripeError as e:
            return {
                "error": True,
                "message": str(e),
                "provider": "stripe"
            }
    
    def create_alipay_order(self,
                         amount: float,
                         subject: str,
                         out_trade_no: str,
                         return_url: Optional[str] = None) -> Dict[str, Any]:
        """
        创建支付宝电脑网站支付订单
        
        Args:
            amount: 金额
            subject: 订单标题
            out_trade_no: 商户订单号
            return_url: 支付完成后跳转地址
            
        Returns:
            订单信息字典
        """
        if not self.alipay_enabled:
            raise ValueError("Alipay not initialized. Please provide alipay_config.")
        
        try:
            # 创建支付订单
            order_string = self.alipay.api_alipay_trade_page_pay(
                out_trade_no=out_trade_no,
                total_amount=str(amount),
                subject=subject,
                return_url=return_url,
                notify_url=self.alipay_config.get("notify_url")
            )
            
            # 构建完整支付URL
            gateway = "https://openapi.alipay.com/gateway.do?"
            if self.alipay_config.get("debug", False):
                gateway = "https://openapi.alipaydev.com/gateway.do?"
            
            pay_url = gateway + order_string
            
            order_info = {
                "provider": "alipay",
                "order_id": out_trade_no,
                "pay_url": pay_url,
                "amount": amount,
                "subject": subject,
                "status": "created",
                "created_at": datetime.now().isoformat()
            }
            
            self.order_history.append(order_info)
            return order_info
            
        except Exception as e:
            return {
                "error": True,
                "message": str(e),
                "provider": "alipay"
            }
    
    def query_alipay_order(self, out_trade_no: str) -> Dict[str, Any]:
        """
        查询支付宝订单状态
        
        Args:
            out_trade_no: 商户订单号
            
        Returns:
            订单状态信息
        """
        if not self.alipay_enabled:
            raise ValueError("Alipay not initialized.")
        
        try:
            result = self.alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
            return {
                "success": True,
                "order_id": out_trade_no,
                "trade_status": result.get("trade_status", "unknown"),
                "total_amount": result.get("total_amount"),
                "buyer_logon_id": result.get("buyer_logon_id"),
                "raw_response": result
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }
    
    def refund_stripe_order(self, payment_intent_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        """
        发起Stripe退款
        
        Args:
            payment_intent_id: 支付意图ID
            amount: 退款金额，不传则全额退款
            
        Returns:
            退款结果
        """
        if not self.stripe_enabled:
            raise ValueError("Stripe not initialized.")
        
        try:
            refund_data = {"payment_intent": payment_intent_id}
            if amount:
                refund_data["amount"] = int(amount * 100)
            
            refund = stripe.Refund.create(**refund_data)
            
            return {
                "success": True,
                "refund_id": refund.id,
                "amount": refund.amount / 100,
                "status": refund.status,
                "created_at": datetime.now().isoformat()
            }
        except stripe.error.StripeError as e:
            return {
                "error": True,
                "message": str(e)
            }
    
    def refund_alipay_order(self, out_trade_no: str, refund_amount: float, out_request_no: str) -> Dict[str, Any]:
        """
        发起支付宝退款
        
        Args:
            out_trade_no: 商户订单号
            refund_amount: 退款金额
            out_request_no: 退款请求号
            
        Returns:
            退款结果
        """
        if not self.alipay_enabled:
            raise ValueError("Alipay not initialized.")
        
        try:
            result = self.alipay.api_alipay_trade_refund(
                out_trade_no=out_trade_no,
                refund_amount=str(refund_amount),
                out_request_no=out_request_no
            )
            
            return {
                "success": result.get("code") == "10000",
                "order_id": out_trade_no,
                "refund_amount": refund_amount,
                "refund_request_no": out_request_no,
                "raw_response": result
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }
    
    def verify_alipay_notify(self, data: Dict[str, str]) -> bool:
        """
        验证支付宝异步通知签名
        
        Args:
            data: 支付宝回调数据
            
        Returns:
            签名是否有效
        """
        if not self.alipay_enabled:
            return False
        
        signature = data.pop("sign", None)
        return self.alipay.verify(data, signature)
    
    def get_order_history(self, provider: Optional[str] = None) -> list:
        """
        获取订单历史
        
        Args:
            provider: 筛选特定支付渠道 (stripe/alipay)
            
        Returns:
            订单列表
        """
        if provider:
            return [o for o in self.order_history if o.get("provider") == provider]
        return self.order_history.copy()
