---
name: mcdonalds-mcp
description: 麦当劳MCP服务集成，支持点餐、优惠券、麦麦商城、积分兑换等功能。需要用户先在 https://open.mcd.cn 申请MCP Token。
---

# 麦当劳MCP集成

使用麦当劳MCP平台API进行点餐、查优惠券、积分兑换等操作。

## 前置要求

用户需要在 https://open.mcd.cn 申请MCP Token：
1. 登录/手机号验证
2. 点击"控制台" → 激活MCP Token
3. 获取 Token 和接入地址 `https://mcp.mcd.cn`

## 配置

在调用接口时需要用户提供：
- MCP Token
- （可选）指定功能模块

## 可用功能

### 点餐相关
- 查询门店可售卖的餐品列表
- 查询餐品详情
- 查询用户可配送地址
- 新增配送地址
- 查询门店可用优惠券
- 商品价格计算
- 创建外送订单
- 查询订单详情

### 优惠券
- 麦麦省券列表查询
- 一键领券
- 我的优惠券查询

### 麦麦商城
- 查询我的积分
- 积分兑换商品列表
- 积分兑换商品详情
- 积分兑换下单

### 其他
- 活动日历查询
- 当前时间查询

## 接口调用方式

由于OpenClaw不直接支持MCP协议，通过HTTP API调用：

```
POST https://mcp.mcd.cn
Headers:
  Authorization: Bearer YOUR_TOKEN
  Content-Type: application/json
```

具体接口格式需要参考MCP协议文档，或使用支持MCP协议的客户端（如Cherry Studio、Cursor）。

## 注意事项

- 每个Token每分钟最多600次请求
- MCP Server仅支持2025-06-18及之前版本
- 请妥善保管Token避免泄露
