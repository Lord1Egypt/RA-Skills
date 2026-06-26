---
name: glance-watch
description: 智能盯盘插件，用于监控A股、港股、比特币等金融市场行情并在条件触发时发送提醒。当用户要求盯盘、监控价格、设置提醒时自动触发，例如"帮我盯着比特币"、监控某只股票、涨跌幅提醒等。
---

# Glance Watch 智能盯盘

## 快速开始

1. **环境变量**（已在系统配置）:
   - `OPENCLAW_WS_TOKEN`（由网页申请得到）

2. **安装插件包**：
   - `npm install -g openclaw-glance-plugin`

3. **用户请求盯盘时**，解析用户需求提取：
   - `productCode`: 产品代码
   - `productType`: 市场类型 (stock/index/hk_stock/crypto)
   - `condition`: 条件表达式
   - `variables`: 变量值

4. **创建监控脚本**并运行（bridge 地址固定为 `ws://glanceup-pre.100credit.cn`）

## 调用判定规则（给 OpenClaw 大模型）

只有在用户明确表达以下意图时调用插件：
- “帮我盯盘/监控/提醒”
- “涨到/跌到某个价格提醒我”
- “达到某个涨跌幅提醒我”

调用前必须确认：
- `productCode`（标的代码）
- `productType`（`stock/index/hk_stock/crypto`）
- `condition`（规则表达式）
- `variables`（阈值变量）

缺任一项时先追问，不要猜测阈值。

## 渠道参数填写

`openclaw` 渠道必传，`email` / `call` 可选。如用户没明确说明使用邮件(email)、电话/外呼(call) 通知提醒，则只需要传入`openclaw` 渠道。

### email 参数（emailConfig）
- `to_address`：收件人邮箱（必填）
- `template_id`：邮件模板 ID（必填，默认为4，不需要修改）
- `template_params`：模板变量（可选）

示例：
```javascript
emailConfig: {
  to_address: 'demo@example.com',
  template_id: 4,
  template_params: {
    title: '监控提醒',
    product_name: '比特币'
  }
}
```

### call 参数（callConfig）
- `phone`：手机号（必填）
- `customer_name`：客户名称（可选）
- `condition`：外呼内容（可选，默认用触发消息，如不需要自定义可使用默认消息）

示例：
```javascript
callConfig: {
  phone: '13800138000',
  customer_name: 'Demo',
  condition: '比特币价格突破阈值'
}
```

## 支持的市场

| 市场 | productType | 示例 | 说明 |
|------|-------------|------|------|
| A股个股 | stock | 000001 | 每3秒行情 |
| A股指数 | index | 000300 | 每3秒行情 |
| 港股 | hk_stock | 00700 | 延迟15分钟 |
| 加密货币 | crypto | BTCUSDT | 每10秒行情 |

意图映射建议：
- 用户提到“指数/沪深300/上证” -> `index`
- 用户提到“港股” -> `hk_stock`
- 用户提到“比特币/BTC” -> `crypto`
- 其余股票默认先按 `stock` 处理并在必要时追问确认

详细产品代码见 [references/markets.md](references/markets.md)

## 使用示例

### 比特币监控
```javascript
// 条件: 价格 >= 73000 且涨幅 >= 1%
condition: 'price >= threshold and change_percent >= cp_threshold'
variables: { threshold: 73000, cp_threshold: 0.01, product_name: 'Bitcoin' }
// 注意: crypto 不支持 turnover_rate
```

### A股监控
```javascript
// 条件: 价格 >= 12.5 且换手率 >= 1%
condition: 'price >= threshold and turnover_rate >= tr_threshold'
variables: { threshold: 12.5, tr_threshold: 0.01, product_name: '平安银行' }
```

### 港股监控
```javascript
// 条件: 价格 >= 420
condition: 'price >= threshold'
variables: { threshold: 420, product_name: '腾讯控股' }
```

## 触发后操作

当监控触发时:
1. 解析 `market_data` 获取价格、涨跌幅等信息
2. 发送提醒到用户当前对话的渠道（群聊/私聊）
3. `openclaw` 渠道必传，`email/call` 可按需附加
4. 根据触发消息构建友好的提醒文案

如果创建失败（`watch.create.result.success=false`）：
- 明确返回失败原因给用户
- 引导用户补充或修正参数后再次创建

## 相关资源

- 脚本: [scripts/watch-monitor.js](scripts/watch-monitor.js)
- 市场参考: [references/markets.md](references/markets.md)
