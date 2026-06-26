# API Reference

## Endpoint

```
POST https://mcp.mysteel.com/mcp/info/ai-search/search
```

## Request Headers

| Header       | Value            |
|--------------|------------------|
| Content-Type | application/json |
| token        | <your api_key>   |

## Request Body

| Parameter | Type | Required | Default | Description           |
|-----------|------|----------|---------|-----------------------|
| source | string | Yes | - | 数据来源模式，固定值 "MyClaw模式" |
| text | string | Yes | - | 用户查询文本                |
| indexSearchEnable | boolean | No | true | 是否启用指标数据搜索            |
| infoSearchEnable | boolean | No | false | 是否启用资讯信息搜索            |
| staticKnowledgeEnable | boolean | No | true | 是否检索静态知识              |

## Request Example

```json
{
  "source": "MyClaw模式",
  "text": "鸡蛋交割时以褐壳还是粉壳交割？最新收盘价多少",
  "indexSearchEnable": true,
  "infoSearchEnable": false,
  "staticKnowledgeEnable": true
}
```

## Response Structure

响应为JSON格式，包含查询结果数据。

## Supported Query Types

### 期货价格查询
- 最新收盘价、结算价
- 历史价格趋势
- 交割规则

### 现货价格查询
- 实时现货报价
- 区域价格对比
- 企业报价

### 宏观经济数据
- GDP、CPI等宏观指标
- 分国别/地区数据

### 产业链数据
- 供需数据
- 进出口数据
- 库存数据

### 金融市场数据
- 期权价格
- 股票行情
- 债券收益率
- 外汇汇率

## cURL Example

```bash
curl --location 'https://mcp.mysteel.com/mcp/info/ai-search/search' \
--header 'Content-Type: application/json' \
--header 'token: <your api_key>' \
--data '{
  "source": "MyClaw模式",
  "text": "鸡蛋交割时以褐壳还是粉壳交割？最新收盘价多少",
  "indexSearchEnable": true,
  "infoSearchEnable": false,
  "staticKnowledgeEnable": true
}'
```