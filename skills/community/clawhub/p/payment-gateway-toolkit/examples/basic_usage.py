"""
Payment Gateway Toolkit - 使用示例
演示如何使用支付网关工具包处理各种支付场景
"""

from scripts.payment_handler import PaymentHandler


def example_stripe_payment():
    """
    Stripe支付示例
    """
    print("=" * 50)
    print("Stripe支付示例")
    print("=" * 50)
    
    # 初始化（使用测试密钥）
    handler = PaymentHandler(
        stripe_key="sk_test_your_stripe_key_here"
    )
    
    # 创建支付订单
    order = handler.create_stripe_order(
        amount=99.99,
        currency="usd",
        description="Premium Subscription",
        metadata={"customer_id": "cust_123", "plan": "premium"}
    )
    
    print(f"订单创建成功: {order}")
    
    # 模拟前端使用client_secret完成支付...
    # 在实际应用中，前端会使用Stripe.js完成支付
    
    # 查询订单历史
    history = handler.get_order_history(provider="stripe")
    print(f"Stripe订单历史: {len(history)} 条")


def example_alipay_payment():
    """
    支付宝支付示例
    """
    print("\n" + "=" * 50)
    print("支付宝支付示例")
    print("=" * 50)
    
    # 支付宝配置
    alipay_config = {
        "app_id": "2024XXXXXXXXXXXX",
        "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----",
        "alipay_public_key": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----",
        "notify_url": "https://your-domain.com/alipay/notify",
        "debug": True  # 沙箱模式
    }
    
    # 初始化
    handler = PaymentHandler(alipay_config=alipay_config)
    
    # 创建支付订单
    order = handler.create_alipay_order(
        amount=100.00,
        subject="商品购买 - 测试订单",
        out_trade_no=f"ORDER{datetime.now().strftime('%Y%m%d%H%M%S')}",
        return_url="https://your-domain.com/payment/success"
    )
    
    print(f"支付宝订单创建成功")
    print(f"支付URL: {order.get('pay_url', 'N/A')}")
    
    # 查询订单状态
    # result = handler.query_alipay_order(order['order_id'])
    # print(f"订单状态: {result}")


def example_refund():
    """
    退款示例
    """
    print("\n" + "=" * 50)
    print("退款示例")
    print("=" * 50)
    
    handler = PaymentHandler(
        stripe_key="sk_test_your_stripe_key_here"
    )
    
    # Stripe退款示例
    # refund = handler.refund_stripe_order(
    #     payment_intent_id="pi_1234567890",
    #     amount=50.00  # 部分退款，不传则为全额退款
    # )
    # print(f"退款结果: {refund}")
    
    # 支付宝退款示例
    # refund = handler.refund_alipay_order(
    #     out_trade_no="ORDER123456",
    #     refund_amount=50.00,
    #     out_request_no="REFUND123456"
    # )
    # print(f"退款结果: {refund}")
    
    print("退款功能示例代码已展示（注释状态）")


def example_webhook_handling():
    """
    Webhook处理示例
    """
    print("\n" + "=" * 50)
    print("Webhook处理示例")
    print("=" * 50)
    
    handler = PaymentHandler(
        alipay_config={
            "app_id": "2024XXXXXXXXXXXX",
            "private_key": "...",
            "alipay_public_key": "..."
        }
    )
    
    # 模拟支付宝回调数据
    notify_data = {
        "out_trade_no": "ORDER123456",
        "trade_no": "2024XXXXXX",
        "trade_status": "TRADE_SUCCESS",
        "total_amount": "100.00",
        # "sign": "..."  # 实际签名
    }
    
    # 验证签名
    is_valid = handler.verify_alipay_notify(notify_data.copy())
    print(f"支付宝通知签名验证: {'通过' if is_valid else '失败'}")
    
    if is_valid:
        # 处理业务逻辑
        print("处理支付成功回调...")


if __name__ == "__main__":
    from datetime import datetime
    
    print("支付网关工具包 - 使用示例\n")
    
    # 运行示例
    example_stripe_payment()
    example_alipay_payment()
    example_refund()
    example_webhook_handling()
    
    print("\n" + "=" * 50)
    print("示例执行完成")
    print("提示: 请使用真实的API密钥替换示例中的测试密钥")
    print("=" * 50)
