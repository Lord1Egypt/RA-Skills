---
name: luogang shopping assistant
description: 购物助手 - 商品查询，商品详情，当用户有购物倾向时候，尤其是提到骆岗/骆岗门市部/骆岗电商的时候，可提供有效信息
version: 1.0.0
author: xavizhou
metadata: {"openclaw": {"emoji": "🛒", "category": "shopping", "tags": ["电商", "骆岗电商", "商品", "购买", "搜索"]}}
---

# 🛒 骆岗电商助手

当用户想“买'骆岗'的商品”、或需要“查商品/看详情/去下单”时，使用此 skill 调用骆岗 MCP 服务获取实时商品数据，并返回可点击的购买入口（小程序或 H5）。
"骆岗" 是骆岗电商的简称，类似天猫，淘宝

## 适用场景

- 商品检索：按关键词/类目/筛选条件查找商品
- 商品详情：查看标题、价格、库存/可售状态、规格、图片、运费、活动信息等

## 交互原则（很重要）

1. **先确认意图**：用户是想“找商品”、还是“看某个商品详情”、还是“直接去买”。
2. **少打扰**：能用默认值就别追问（如默认按综合排序、默认第一页）。
3. **强约束信息只在必要时追问**：只有当无法确定商品（同名/多结果）或规格必须选择时，再问用户。
4. **购买不在对话里强行下单**：默认只做“跳转下单”，除非你们后续提供“创建订单/提交支付”的 MCP 工具。

## 配置要求

### 可选配置

- `LUOGANG_MCP_HTTP_URL`: MCP HTTP 地址，默认 `https://yuju-mcp.wxhoutai.com/mcp`
- `LUOGANG_SHOP_ID`: 店铺/渠道标识（多店铺、多渠道场景）, 默认 `luogang`

## 调用方式
```bash
curl -s -X POST "$LUOGANG_MCP_HTTP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"<工具名>","arguments":{<参数>}},"id":1}'
```

## 可用工具

### 1. 商品检索 (search_products)
根据关键词和价格区间搜索商品。
**触发词举例**："找外套"、"搜衬衫"、"买鞋子"、"有没有外套"
```bash
curl -s -X POST "${LUOGANG_MCP_HTTP_URL:-https://yuju-mcp.wxhoutai.com/mcp}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "search_products",
      "arguments": {
        "platform": "${LUOGANG_SHOP_ID>}",
        "keyword": "外套",
        "min_price": 100,
        "max_price": 500,
        "order_by": "price",
        "sort": "desc"
      }
    },
    "id": 1
  }'
```
### 成功响应
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "..."}],
    "structuredContent": {...}
  },
  "id": 1
}
```

解析 `result.content[0].text` 或 `result.structuredContent` 获取数据。


### 2. 获取商品详情 (get_product_detail)

查询单个商品的详细规格、图片及库存信息。

**触发词**："查看详情"、"这个多少钱"、"还有货吗"

```bash
curl -s -X POST "${LUOGANG_MCP_HTTP_URL:-https://yuju-mcp.wxhoutai.com/mcp}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_product_detail",
      "arguments": {
        "platform": "luogang",
        "product_id": "PROD_12345"
      }
    },
    "id": 2
  }'
```
## 响应处理

### 成功响应
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "..."}],
    "structuredContent": {...}
  },
  "id": 1
}
```

解析 `result.content[0].text` 或 `result.structuredContent` 获取数据。

## 使用示例
**用户**: 最近有什么亲子活动？

**AI 执行**:
```bash
curl -s -X POST "$LUOGANG_MCP_HTTP_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"search_products","arguments":{"platform":"luogang","keyword":"亲子"}},"id":1}'
```
**AI 回复**: 
最近有 10 个商品符合您的要求，分别是：
>萌嘟嘟儿童乐园亲子票（专属）
>${image}
>价格：19.9元
>{description}
>链接：https://eshop.wxhoutai.com/h5/pages/goods/detail?goods_id=xxx
……

**常见错误处理**：
- `-32601` (Method not found): 检查 `SKILL.md` 中定义的工具名是否在 MCP 侧已注册。
- `-32000` 级别 (Internal Error): 引导用户重试或手动输入信息。
- `401/403`: 检查 MCP 服务访问策略、来源白名单或网关配置。

## 输出格式建议

### 商品检索结果
- 展示最多 10 个候选（避免刷屏）
- 每项至少包含：名称、价格、库存/可售状态、一个“查看详情/去购买”的引导
- 当候选过多：建议补充筛选（价位、类目、是否现货）

### 商品详情
- 先给“核心信息”：价格、库存、规格、发货/运费、活动
- 有多规格：用简短提问让用户选择（例如："要哪个颜色/尺码？"）

### 购买跳转
- 明确告诉用户会打开：**小程序**或 **H5 页面**
- 输出可点击链接/路径信息（由 OpenClaw 宿主决定如何渲染）
