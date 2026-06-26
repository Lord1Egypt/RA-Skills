---
name: price-alert-monitor
version: 1.0.0
description: 商品价格监控工具。监控电商商品价格变化，价格低于阈值时发送通知。适合购物党、羊毛党。
author: 你的名字
triggers:
  - "价格监控"
  - "降价提醒"
  - "价格走势"
  - "购物监控"
  - "亚马逊监控"
---

# Price Alert Monitor 📉

监控商品价格变化，发现底价时通知你！

## 功能

- 🛒 支持监控京东、淘宝、亚马逊等商品
- 📉 记录价格历史，生成走势
- 🔔 价格低于阈值时通知
- 📊 支持多商品同时监控

## 使用方法

### 添加商品监控

```bash
python3 scripts/price_monitor.py add "商品URL"
```

### 查看监控列表

```bash
python3 scripts/price_monitor.py list
```

### 检查价格

```bash
python3 scripts/price_monitor.py check
```

### 设置价格提醒

```bash
python3 scripts/price_monitor.py alert "商品ID" 100
```

## 示例

```bash
# 监控京东商品
python3 scripts/price_monitor.py add "https://item.jd.com/100086924064.html"

# 监控亚马逊商品
python3 scripts/price_monitor.py add "https://www.amazon.com/dp/B09V3KXJPB"

# 设置低于 100 元提醒
python3 scripts/price_monitor.py alert 1 100

# 检查所有商品价格
python3 scripts/price_monitor.py check
```

## 通知设置

需要配置通知方式，支持：
- 打印到终端
- 发送邮件（需要配置 SMTP）
- 发送到 Webhook

```bash
export PRICE_WEBHOOK="your-webhook-url"
```
