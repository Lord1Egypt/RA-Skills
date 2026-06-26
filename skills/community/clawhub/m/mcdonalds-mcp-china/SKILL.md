---
name: mcd-mcp
description: 麦当劳 MCP 点餐技能。通过麦当劳官方 MCP 服务查询门店、餐品、优惠券，完成外送/到店/团餐点餐与积分兑换。Use when users want to order McDonald's food, check menus, use coupons, or redeem points in mainland China.
license: MIT
metadata:
  author: openclaw
  version: "1.0"
  tags:
    - mcdonalds
    - mcp
    - food-ordering
    - delivery
    - china
---

# 麦当劳 MCP 点餐技能 (mcd-mcp)

通过麦当劳中国 MCP 接口，实现麦乐送/到店取餐/团餐点餐、优惠券查询、积分兑换等功能。

---

## 1. 前置条件：获取 MCP Token

**必须先让用户提供 MCP Token。** 用户需自行前往 [https://open.mcd.cn/mcp](https://open.mcd.cn/mcp) 申请：

1. 点右上角「登录」，用手机号验证登录
2. 登录后右上角变成「控制台」，点击进入
3. 点击「激活」按钮，同意服务协议
4. 复制生成的 MCP Token

⚠️ **MCP Token 代表麦当劳会员身份，严禁分享给他人。**

---

## 2. 配置 MCP Server 到 OpenClaw

获取到 Token 后，使用以下命令配置：

```bash
openclaw mcp set mcd-mcp \
  --transport streamable-http \
  --url https://mcp.mcd.cn \
  --header "Authorization" "Bearer YOUR_MCP_TOKEN"
```

**注意：** `YOUR_MCP_TOKEN` 需要替换为用户提供的实际 Token。

> 如果 `openclaw mcp set` 命令不可用，也可以直接编辑 `~/.openclaw/openclaw.json`，在根对象添加 `mcp.servers` 配置：
> ```json
> {
>   "mcp": {
>     "servers": {
>       "mcd-mcp": {
>         "url": "https://mcp.mcd.cn",
>         "transport": "streamable-http",
>         "headers": {
>           "Authorization": "Bearer YOUR_MCP_TOKEN"
>         }
>       }
>     }
>   }
> }
> ```

配置完成后，可以通过 MCP 协议调用 McDonald's 的所有工具。

---

## 3. MCP 工具清单

| 工具名 | 中文名 | 用途 |
|--------|--------|------|
| `list-nutrition-foods` | 餐品营养信息列表 | 查热量、营养成分 |
| `delivery-query-addresses` | 获取配送地址列表 | 查已有外送地址 |
| `delivery-create-address` | 新增配送地址 | 创建新外送地址 |
| `query-nearby-stores` | 查询附近门店 | 搜附近麦当劳 |
| `query-store-coupons` | 查询门店可用券 | 查当前门店可用优惠券 |
| `query-meals` | 查询门店可售餐品 | 查看菜单 |
| `query-meal-detail` | 查询餐品详情 | 查看套餐内容 |
| `calculate-price` | 价格计算 | 计算总价 |
| `create-order` | 创建订单 | 下单 |
| `query-order` | 查询订单 | 查订单状态 |
| `campaign-calendar` | 活动日历 | 查当月活动 |
| `available-coupons` | 麦麦省券列表 | 查可领取的券 |
| `auto-bind-coupons` | 一键领券 | 自动领取所有可用券 |
| `query-my-coupons` | 我的优惠券 | 查我已领取的券 |
| `query-my-account` | 积分查询 | 查积分余额 |
| `mall-points-products` | 积分兑换商品 | 查可兑换商品 |
| `mall-product-detail` | 积分商品详情 | 查具体商品信息 |
| `mall-create-order` | 积分兑换下单 | 用积分兑换商品 |

---

## 4. 点餐流程（完整工作流）

### 4.1 麦乐送（外送）点餐

```
1. 问用户想吃什么、送到哪里
2. 调用 delivery-query-addresses(beType=2) 获取已存地址列表
   → 如果没有地址，调用 delivery-create-address 新建
   → 从返回值获取 addressId、storeCode、beCode
3. 调用 query-meals(storeCode, beCode, orderType=2) 查看门店菜单
   → 向用户展示餐品，让其选择
4. 调用 query-store-coupons(storeCode, beCode, orderType=2) 查看可用券
   → 问用户是否要用券
5. 调用 calculate-price() 计算价格，让用户确认
   ⚠️ 参数字段为 items（数组），不是 productList/products！
6. 用户确认后，调用 create-order() 创建订单
7. 返回支付链接给用户完成支付
```

### 4.2 到店取餐

```
1. 问用户想去哪家店
2. 调用 query-nearby-stores(searchType=2, beType=1, city=..., keyword=...) 找附近门店
   → 获取 storeCode
3. 调用 query-meals(storeCode, beCode=null, orderType=1) 查看菜单
4. 调用 query-store-coupons(storeCode, beCode=null, orderType=1) 查看可用券
5. 计算价格并确认
6. 创建订单并获取取餐码
```

### 4.3 积分兑换

```
1. 调用 query-my-account 查用户积分
2. 调用 mall-points-products 查可兑换商品
3. 调用 mall-product-detail 查看具体商品详情
4. 用户确认后调用 mall-create-order 兑换
```

### 4.4 团餐

```
与麦乐送相同，但 beType=6
```

---

## 5. ⚠️ 踩坑记录与解决方案

### 5.1 `calculate-price` 和 `create-order` 参数格式（2026-04-01）

**问题**：调用时一直报 `"缺少参数"` 或 `"参数缺失"`。

**原因**：`items` 参数必须是 **JSON 对象数组**（不能是字符串），且需与 `storeCode`、`beCode`、`addressId` 一起作为顶层参数传入。

**正确格式**（传 JSON）：

```javascript
// 调用 MCP 工具时，args 必须是完整 JSON 对象
{
  "storeCode": "1450555",
  "beCode": "145055502",
  "addressId": "1036946320159843531343293876",
  "items": [
    { "productCode": "9900013722", "quantity": 1 }
  ]
}
```

**踩坑的错误写法**（均会报错）：

```javascript
// ❌ items 被当成字符串
{ "addressId": "xxx", "items": "..." }

// ❌ 用了 productList 而非 items
{ "addressId": "xxx", "productList": [...] }

// ❌ 用了 products 而非 items
{ "addressId": "xxx", "products": [...] }

// ❌ 缺少 storeCode/beCode
{ "addressId": "xxx", "items": [...] }

// ❌ items 是字符串数组而非对象数组
{ "addressId": "xxx", "items": ["9900013722"] }
```

### 5.2 `query-meal-detail` 对某些商品码返回错误（2026-04-01）

**问题**：查询 `521533`（泷情蜜意麦旋风单个）时返回 `"未匹配到商品"`。

**原因**：部分促销/限时商品（尤其是买一送一类套餐码如 `9900013722`）可能不在标准餐品详情库中。

**规避**：优先使用 `query-meals` 获取商品名和价格，不依赖 `query-meal-detail`。买一送一商品直接用套餐码下单即可。

### 5.3 支付链接变为扫码支付（2026-04-01）

**问题**：`create-order` 返回的 `payH5Url` 从网页收银台变成了 `https://m.mcd.cn/mcp/scanToPay?orderId=xxx` 扫码支付页。

**原因**：麦当劳 MCP 端更新了支付流程，不再提供 H5 网页收银台。

**应对方案**：
- 手机上直接打开链接 → 可能自动调起微信/支付宝支付
- 在麦当劳 App「我的订单」中找到待支付订单，直接支付
- 暂无办法恢复网页收银台，接受现状

### 5.4 `items` vs `productCode` 直传（2026-04-01）

**发现**：`create-order` 的 schema 声明 `items?: string[]`，但实际需要传 JSON 对象数组 `[{"productCode":"xxx","quantity":1}]`。直接传 `productCode=xxx&quantity=1` 会报参数缺失。**必须传完整 JSON 对象数组。**

### 5.5 MCP 版本兼容性（2026-04-01）

- MCP Server 当前仅支持 MCP **Version 2025-06-18** 及之前的版本
- 每个 Token 每分钟最多允许 600 次请求，超过限制会返回 429 错误码
- 确保 MCP Client 支持 Streamable HTTP 协议

---

## 6. 注意事项

- MCP Token 代表麦当劳会员身份，**严禁分享**
- 服务面向 **中国大陆地区**（不含港澳台）
- 下单时需先 `calculate-price` 计算价格并让用户确认
- **多个商品兑换需分别下单**，等前一个订单完成后再下新的
- 门店信息（storeCode/beCode）必须从 `delivery-query-addresses` 或 `query-nearby-stores` 返回值获取，不可凭空生成
- 参考文档：https://open.mcd.cn/mcp/doc
- MCP 地址：https://mcp.mcd.cn

---

## 7. 错误码速查

| code | 原因 | 处理 |
|:----:|:----:|:-----|
| 401 | Token 无效/过期/未提供 | 检查 Token 配置 |
| 429 | 超过 600 次/分钟限流 | 降低请求频率 |
