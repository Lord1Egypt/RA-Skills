---
name: mx_data
description: 基于东方财富权威数据库及实时行情数据的金融数据查询 Skill，支持行情、财务、关系与经营类信息的自然语言查询，避免模型使用过时或不准确的金融数据。
---

# 妙想金融数据 Skill (mx_data)

## Overview
此 Skill 通过妙想（Meixiang）金融数据接口，为用户提供实时、权威的金融数据查询能力，覆盖三大类信息：
1. **行情类** – 股票、行业、板块、指数、基金、债券的实时行情、主力资金流向、估值等。
2. **财务类** – 上市公司及非上市公司的基本信息、财务指标、高管信息、主营业务、股东结构、融资情况等。
3. **关系与经营类** – 股票、非上市公司、股东及高管之间的关联关系，以及企业经营相关数据。

## Prerequisites
1. 在 **妙想 Skills** 页面获取 API key。
2. 将 API key 写入环境变量 `MX_APIKEY`：
   ```bash
   export MX_APIKEY="your_api_key_here"
   ```
3. 本地需安装 `curl`（macOS 默认已装）。

## Usage Steps
1. **构造请求** – 根据业务需求准备 JSON payload，最基本的字段为 `toolQuery`（查询关键词），如
   ```json
   {"toolQuery": "东方财富最新价"}
   ```
2. **发送 POST 请求**：
   ```bash
   curl -X POST \
     --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/query' \
     --header 'Content-Type: application/json' \
     --header "apikey:${MX_APIKEY}" \
     --data '{"toolQuery": "<YOUR_QUERY>"}'
   ```
3. **解析响应** – 关键返回字段（仅展示需向下游暴露的核心内容）：
   - `data.questionId` – 本次查询的唯一标识。
   - `data.dataTableDTOList` – 标准化的证券指标数据列表，每个元素对应 **1 个证券 + 1 个指标**，包含 `code`、`entityName`、`title`、`table`（指标值）、`nameMap`（列名映射） 等。
   - `data.entityTagDTOList` – 本次查询涉及的证券主体信息（代码、市场、证券类型、全名等），用于去重展示。
   - `data.condition` – 本次查询的条件描述（关键词、时间范围等）。
4. **返回给用户** – 将 `title`、关键指标值、关联证券（`entityTagDTO`）以可读表格或简要文字形式呈现。必要时可将完整 JSON 保存到工作目录（`mx_data_result.json`）。

## Example
**用户查询**："东方财富最新价"

**命令**：
```bash
curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/query' \
  --header 'Content-Type: application/json' \
  --header 'apikey:${MX_APIKEY}' \
  --data '{"toolQuery": "东方财富最新价"}'
```

**返回（示例）**：
```json
{
  "status":0,
  "message":"ok",
  "data":{
    "questionId":"Q20260314-001",
    "dataTableDTOList":[{
      "code":"300059.SZ",
      "entityName":"东方财富 (300059.SZ)",
      "title":"最新价",
      "table":{"f2":[22.45]},
      "nameMap":{"f2":"最新价"},
      "indicatorOrder":["f2"]
    }],
    "entityTagDTOList":[{
      "secuCode":"300059",
      "marketChar":"SZ",
      "entityTypeName":"A股",
      "fullName":"东方财富",
      "entityId":"ent_300059",
      "className":"沪深A股"
    }]
  }
}
```

**向用户展示**：
- **证券**：东方财富 (300059.SZ)
- **最新价**：22.45 元
- **查询 ID**：Q20260314-001

## Data Size Warning
查询涉及大范围、长时间序列或大量证券时，返回数据量可能非常大，导致上下文超限或性能下降。建议在 `toolQuery` 中加入 **具体筛选条件**（如具体股票代码、时间范围）或使用分页参数（若接口支持）。

## When Not to Use
- 非金融/非财务相关查询。
- 需要主观分析或意见建议的场景（本 Skill 只返回原始数据）。

## References
- Meixiang API 文档（内部）。
- 示例查询表格列映射说明（`nameMap`）。
