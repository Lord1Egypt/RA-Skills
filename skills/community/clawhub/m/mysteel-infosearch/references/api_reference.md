# API Reference

## Endpoint

```
POST https://mcp.mysteel.com/mcp/info/ai-search/search
```

## Request Headers

| Header       | Value           |
|--------------|-----------------|
| Content-Type | application/json|
| token        | <your api_key>  |

## Request Body

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| source | string | Yes | - | 数据来源模式，固定值 "MyClaw模式" |
| text | string | Yes | - | 用户查询文本 |
| indexSearchEnable | boolean | No | false | 是否启用指标数据搜索（资讯搜索通常设为false） |
| infoSearchEnable | boolean | No | true | 是否启用资讯信息搜索 |
| staticKnowledgeEnable | boolean | No | true | 是否检索静态知识              |

## Request Example

```json
{
  "source": "MyClaw模式",
  "text": "钢铁行业最新政策动态",
  "indexSearchEnable": false,
  "infoSearchEnable": true,
  "staticKnowledgeEnable": true
}
```

## Supported Query Types

### 行业动态
- 钢铁、有色、能源化工等行业新闻
- 市场快讯与突发事件
- 产业链上下游动态

### 政策法规
- 国家宏观政策
- 行业监管政策
- 环保、贸易政策变化

### 企业消息
- 企业生产经营动态
- 兼并重组信息
- 重大项目进展

### 价格异动分析
- 价格波动原因解读
- 市场情绪分析
- 供需事件影响

### 供需事件
- 产能变化
- 库存变动
- 进出口事件

## Response Structure

API返回JSON格式数据，主要包含：

1. **资讯列表**：标题、摘要、来源、发布时间
2. **相关实体**：涉及的品种、企业、地区
3. **情感标签**：利多/利空/中性判断
4. **关联数据**：相关价格数据链接

## cURL Example

```bash
curl --location 'https://mcp.mysteel.com/mcp/info/ai-search/search' \
--header 'Content-Type: application/json' \
--header 'token: <your api_key>' \
--data '{
  "source": "MyClaw模式",
  "text": "钢铁行业限产政策最新消息",
  "indexSearchEnable": false,
  "infoSearchEnable": true,
  "staticKnowledgeEnable": true
}'
```