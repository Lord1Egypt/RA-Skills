---
name: mcd-mcp
description: 麦当劳MCP接口自动化工具，支持自动领券、查询门店库存、计算最优优惠组合、一键下单，解决麦当劳优惠券手动领取麻烦、库存查询不便的问题。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl", "jq"] },
      },
  }
---

# 麦当劳MCP自动化工具

🍟 麦当劳接口自动化工具，自动领券、查库存、算优惠、一键下单。

## 功能特性
✅ 每日自动领取当日可用优惠券  
✅ 查询附近任意门店的产品库存  
✅ 自动计算最优优惠组合，最大化省钱  
✅ 支持一键下单到店取餐  
✅ 多账号管理，全家共用  
✅ 优惠券过期提醒，不浪费任何优惠

## 环境要求
- curl (默认系统自带)
- jq (JSON解析工具，`brew install jq` 或 `apt install jq` 安装)

## 快速开始
### 1. 获取Token
打开麦当劳App，抓包获取请求头中的`MCD_TOKEN`，或使用登录接口获取。

### 2. 配置Token
```bash
export MCD_TOKEN="你的MCD_TOKEN"
```

### 3. 常用命令
```bash
# 领取今日优惠券
./mcd-cli.sh coupon:receive

# 查询附近门店库存
./mcd-cli.sh store:stock --city "北京" --keyword "麦辣鸡腿堡"

# 计算最优优惠组合
./mcd-cli.sh order:calculate --items "麦辣鸡腿堡,薯条,可乐"

# 一键下单
./mcd-cli.sh order:place --store-id "12345" --items "麦辣鸡腿堡,薯条,可乐"
```

## 配置说明
| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| MCD_TOKEN | 麦当劳接口Token | 必填 |
| MCD_CITY | 默认城市 | 自动定位 |
| MCD_STORE_ID | 默认门店ID | 自动选择最近门店 |
| MCD_NOTIFY_URL | 优惠提醒通知地址 | 无 |

## 避坑指南（实战总结）
1. **接口地址正确格式**：✅ 正确：POST到 `https://mcp.mcd.cn/`（根地址），使用JSON-RPC 2.0协议调用；❌ 错误：不要调用`/v1/xxx`这类RESTful路径，会返回404
2. **调用方式正确格式**：所有业务接口都通过 `tools/call` 方法调用，参数为工具名称和参数，不要直接调用业务路径
3. **商品编码必查**：下单前必须先调用 `query-meals` 获取真实商品编码和对应名称，禁止凭记忆猜编码，避免下错单
4. **优惠券ID必查**：优惠券ID从 `query-my-coupons` 或 `query-store-coupons` 获取，禁止直接填优惠券名称，会导致优惠无法使用
5. **下单前置检查**：创建订单前必须先调用 `calculate-price` 确认价格、商品、优惠是否正确，再提交订单
6. **Token有效期**：用户账号Token有效期为24小时~7天，无需频繁刷新，返回401再重新获取
7. **调用频率**：接口调用间隔至少2秒，单日调用不超过200次，避免风控
8. **风控处理**：如果被限制访问，等待24小时自动解封，或更换账号
9. **库存查询**：部分三四线城市门店不支持库存查询，自动降级为仅显示优惠券

## 定时任务配置
每天早上8点自动领取优惠券：
```cron
0 8 * * * export MCD_TOKEN="你的Token" && /path/to/mcd-cli.sh coupon:receive
```

## 项目地址
GitHub: https://github.com/yourname/mcd-mcp
文档: https://docs.example.com/mcd-mcp
