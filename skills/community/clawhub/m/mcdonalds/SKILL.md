---
name: mcdonalds
description: 麦当劳中国 MCP 服务集成，支持优惠券、点餐、外卖、积分商城等功能。当用户提到麦当劳、McDonald's、麦乐送、麦麦省、麦当劳优惠券、麦当劳积分、麦当劳点餐时触发此技能。
---

# 麦当劳点餐技能

通过 MCP 协议连接麦当劳中国服务，实现点餐、领券、积分兑换等功能。

## MCP 配置

- **Server**: `https://mcp.mcd.cn`
- **Token**: 环境变量 `MCD_MCP_TOKEN`
- **协议**: JSON-RPC 2.0 over HTTP

## 获取 MCP Token

1. 用个人麦当劳账号登录 https://open.mcd.cn/mcp
2. 点击页面右上角「控制台」获取 Token
3. 配置环境变量：

```bash
export MCD_MCP_TOKEN="你的token"
```

详细说明：https://open.mcd.cn/mcp

## 快速开始

使用脚本调用 MCP 工具：

```bash
python3 scripts/mcp_call.py <工具名> '[参数JSON]'
```

## 常用场景

### 查看可领优惠券
```bash
python3 scripts/mcp_call.py available-coupons
```

### 自动领券
```bash
python3 scripts/mcp_call.py auto-bind-coupons
```

### 查询积分
```bash
python3 scripts/mcp_call.py query-my-account
```

### 查询配送地址
```bash
python3 scripts/mcp_call.py delivery-query-addresses
```

## 点外卖流程

1. **获取配送地址** → `delivery-query-addresses`
2. **选择地址** → 获取 `storeCode`、`beCode`、`addressId`
3. **查看菜单** → `query-meals`
4. **计算价格** → `calculate-price`
5. **确认下单** → `create-order`

## 积分兑换流程

1. **查看积分** → `query-my-account`
2. **浏览商品** → `mall-points-products`
3. **查看详情** → `mall-product-detail`
4. **兑换商品** → `mall-create-order`

## 价格单位

所有金额单位为**分**，需要除以 100 得到元。

## 详细工具参考

完整工具列表和参数说明见 [references/tools.md](references/tools.md)。
