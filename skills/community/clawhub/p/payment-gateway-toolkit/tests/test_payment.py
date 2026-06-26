"""
Payment Gateway Toolkit - 单元测试
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from scripts.payment_handler import PaymentHandler


class TestPaymentHandler:
    """测试支付处理器"""
    
    @pytest.fixture
    def stripe_handler(self):
        """创建Stripe处理器fixture"""
        return PaymentHandler(stripe_key="sk_test_fake_key")
    
    @pytest.fixture
    def alipay_handler(self):
        """创建支付宝处理器fixture"""
        config = {
            "app_id": "test_app_id",
            "private_key": "-----BEGIN RSA PRIVATE KEY-----\ntest\n-----END RSA PRIVATE KEY-----",
            "alipay_public_key": "-----BEGIN PUBLIC KEY-----\ntest\n-----END PUBLIC KEY-----",
            "debug": True
        }
        return PaymentHandler(alipay_config=config)
    
    def test_init_without_config(self):
        """测试空配置初始化"""
        handler = PaymentHandler()
        assert handler.stripe_enabled is False
        assert handler.alipay_enabled is False
    
    def test_init_with_stripe(self, stripe_handler):
        """测试Stripe配置初始化"""
        assert stripe_handler.stripe_enabled is True
        assert stripe_handler.alipay_enabled is False
    
    def test_init_with_alipay(self, alipay_handler):
        """测试支付宝配置初始化"""
        assert alipay_handler.stripe_enabled is False
        assert alipay_handler.alipay_enabled is True
    
    @patch('scripts.payment_handler.stripe.PaymentIntent.create')
    def test_create_stripe_order_success(self, mock_create, stripe_handler):
        """测试创建Stripe订单成功"""
        # 模拟Stripe响应
        mock_intent = Mock()
        mock_intent.id = "pi_test_123"
        mock_intent.client_secret = "pi_test_secret"
        mock_intent.status = "requires_payment_method"
        mock_create.return_value = mock_intent
        
        result = stripe_handler.create_stripe_order(
            amount=99.99,
            currency="usd",
            description="Test"
        )
        
        assert result["provider"] == "stripe"
        assert result["order_id"] == "pi_test_123"
        assert result["amount"] == 99.99
        assert result["currency"] == "usd"
        assert "error" not in result
    
    @patch('scripts.payment_handler.stripe.PaymentIntent.create')
    def test_create_stripe_order_error(self, mock_create, stripe_handler):
        """测试创建Stripe订单失败"""
        from stripe.error import CardError
        mock_create.side_effect = CardError(
            message="Card declined",
            code="card_declined",
            param="",
            http_status=402
        )
        
        result = stripe_handler.create_stripe_order(amount=99.99)
        
        assert "error" in result
        assert result["provider"] == "stripe"
    
    @patch('scripts.payment_handler.AliPay')
    def test_create_alipay_order(self, mock_alipay_class, alipay_handler):
        """测试创建支付宝订单"""
        mock_alipay = Mock()
        mock_alipay.api_alipay_trade_page_pay.return_value = "order_string_test"
        mock_alipay_class.return_value = mock_alipay
        
        # 重新初始化handler以使用mock
        config = {
            "app_id": "test_app_id",
            "private_key": "test_key",
            "alipay_public_key": "test_pubkey",
            "debug": True
        }
        handler = PaymentHandler(alipay_config=config)
        
        result = handler.create_alipay_order(
            amount=100.00,
            subject="Test Subject",
            out_trade_no="ORDER123"
        )
        
        assert result["provider"] == "alipay"
        assert result["order_id"] == "ORDER123"
        assert result["amount"] == 100.00
        assert result["status"] == "created"
    
    def test_stripe_not_initialized_error(self):
        """测试未初始化Stripe时报错"""
        handler = PaymentHandler()
        with pytest.raises(ValueError, match="Stripe not initialized"):
            handler.create_stripe_order(amount=99.99)
    
    def test_alipay_not_initialized_error(self):
        """测试未初始化支付宝时报错"""
        handler = PaymentHandler()
        with pytest.raises(ValueError, match="Alipay not initialized"):
            handler.create_alipay_order(amount=100.00, subject="Test", out_trade_no="123")
    
    @patch('scripts.payment_handler.stripe.Refund.create')
    def test_refund_stripe_order(self, mock_refund, stripe_handler):
        """测试Stripe退款"""
        mock_refund_obj = Mock()
        mock_refund_obj.id = "re_test_123"
        mock_refund_obj.amount = 5000
        mock_refund_obj.status = "succeeded"
        mock_refund.return_value = mock_refund_obj
        
        result = stripe_handler.refund_stripe_order(
            payment_intent_id="pi_test_123",
            amount=50.00
        )
        
        assert result["success"] is True
        assert result["refund_id"] == "re_test_123"
        assert result["amount"] == 50.00
    
    def test_get_order_history_empty(self, stripe_handler):
        """测试获取空订单历史"""
        history = stripe_handler.get_order_history()
        assert history == []
    
    def test_get_order_history_filtered(self, stripe_handler):
        """测试筛选订单历史"""
        # 手动添加测试订单
        stripe_handler.order_history = [
            {"provider": "stripe", "order_id": "1"},
            {"provider": "alipay", "order_id": "2"},
            {"provider": "stripe", "order_id": "3"}
        ]
        
        stripe_orders = stripe_handler.get_order_history(provider="stripe")
        assert len(stripe_orders) == 2
        
        alipay_orders = stripe_handler.get_order_history(provider="alipay")
        assert len(alipay_orders) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
