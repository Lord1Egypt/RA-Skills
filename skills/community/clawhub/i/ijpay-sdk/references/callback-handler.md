# 支付回调高级处理指南

## 回调设计核心原则

1. **幂等性**：同一通知多次处理，结果必须一致
2. **快速响应**：接收到回调后立即返回 SUCCESS，再异步处理业务
3. **日志完整**：记录每次回调的原始报文、解析结果、处理结果
4. **异常隔离**：业务处理异常不应导致返回 FAIL（已处理的通知除外）

## 幂等处理方案

### 方案A：数据库唯一约束 + 状态机

```sql
-- 订单表添加支付流水号唯一索引
ALTER TABLE orders ADD UNIQUE (transaction_id);

-- 订单状态机
-- 0:待支付  →  1:已支付  →  2:已完成  →  3:已退款
```

```java
@Transactional
public boolean markPaidIfAbsent(String orderId, String transactionId) {
    Order order = orderMapper.selectByOrderId(orderId);
    if (order == null) {
        log.warn("订单不存在: {}", orderId);
        return false;
    }
    if (order.getStatus() >= 1) {
        log.info("订单 {} 已处理，跳过（幂等）", orderId);
        return true; // 已处理，返回true表示"已知"
    }
    orderMapper.updateStatus(orderId, 1, transactionId);
    return true;
}
```

### 方案B：Redis 分布式锁 + 防重表

```java
public boolean processCallback(String transactionId, Runnable business) {
    String lockKey = "pay:callback:" + transactionId;
    String lock = redisTemplate.opsForValue().get(lockKey);
    if ("processed".equals(lock)) {
        return true; // 已处理
    }
    Boolean acquired = redisTemplate.opsForValue()
        .setIfAbsent(lockKey, "processing", 30, TimeUnit.SECONDS);
    if (!Boolean.TRUE.equals(acquired)) {
        return false; // 并发中
    }
    try {
        business.run();
        redisTemplate.opsForValue().set(lockKey, "processed", 7, TimeUnit.DAYS);
        return true;
    } finally {
        redisTemplate.delete(lockKey);
    }
}
```

## 异步处理模式（推荐）

```java
@PostMapping("/ali-callback")
public String aliCallback(HttpServletRequest request) {
    String rawBody = StreamUtils.readToString(request.getInputStream());
    log.info("支付宝回调原始报文: {}", rawBody);

    // 1. 快速验签并返回
    if (!AliPaySignature.checksum(request.getParameterMap(), alipayPublicKey, "UTF-8")) {
        return "fail";
    }

    // 2. 立即返回 SUCCESS（支付宝要求3秒内响应）
    new Thread(() -> processPayment(request)).start();
    return "success";
}

private void processPayment(HttpServletRequest request) {
    try {
        String orderId = request.getParameter("out_trade_no");
        String tradeStatus = request.getParameter("trade_status");
        String amount = request.getParameter("total_amount");

        if ("TRADE_SUCCESS".equals(tradeStatus) || "TRADE_FINISHED".equals(tradeStatus)) {
            paymentService.settle(orderId, new BigDecimal(amount), tradeStatus);
        }
    } catch (Exception e) {
        log.error("异步处理支付异常", e);
        // 记录到补偿队列，稍后重试
       补偿队列.add(request.getParameter("out_trade_no"));
    }
}
```

## 补偿队列（Failover）

```java
// 定时任务扫描未处理的支付通知
@Scheduled(fixedDelay = 60000)
public void retryUnprocessedPayments() {
    List<String> failedOrders = paymentMapper.selectFailedOrders();
    for (String orderId : failedOrders) {
        try {
            // 1. 查询支付宝/微信订单状态
            OrderStatus status = queryOrderStatus(orderId);
            // 2. 根据实际状态更新本地订单
            if (status == PAID) {
                orderService.markPaid(orderId, status.getTransactionId());
                log.info("补偿成功：订单 {} 已标记为已支付", orderId);
            }
        } catch (Exception e) {
            log.error("补偿失败：订单 {}", orderId, e);
        }
    }
}
```

## 回调安全 Checklist

- [ ] 支付宝：验签 `AlipaySignature.checksum()`
- [ ] 微信：验证签名 `WxPayApiKit.verifyNotify()`
- [ ] 回调URL必须 HTTPS（微信强制要求）
- [ ] 回调IP白名单（微信允许配置）
- [ ] 敏感字段加密存储
- [ ] 回调记录落库（order_sync_log）
- [ ] 回调超时时间：≤3秒必须返回
