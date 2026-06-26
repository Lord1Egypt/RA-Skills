---
name: ke-json-processor
description: 科特船长 - JSON 处理工具，格式化/验证/提取/转换 JSON 数据
version: 1.0.0
metadata: {"openclaw": {"emoji": "📋", "requires": {"bins": ["jq"]}, "install": [{"id": "jq-brew", "kind": "brew", "formula": "jq", "bins": ["jq"], "label": "Install jq (brew)"}, {"id": "jq-apt", "kind": "apt", "package": "jq", "bins": ["jq"], "label": "Install jq (apt)"}]}}
---

# JSON Processor - JSON 处理工具

## 功能说明

快速格式化、验证、提取和转换 JSON 数据。

## 使用场景

- 格式化杂乱的 JSON
- 验证 JSON 语法
- 提取特定字段
- JSON 转 CSV/表格
- API 响应处理

## 使用方法

```bash
# 格式化 JSON
clawhub run ke-json-processor --action format --input '{"name":"test","value":123}'

# 验证 JSON
clawhub run ke-json-processor --action validate --input '{"invalid":}'

# 提取字段
clawhub run ke-json-processor --action extract --field "name" --input '{"name":"test","value":123}'

# JSON 转表格
clawhub run ke-json-processor --action to-table --input '[{"name":"A","value":1},{"name":"B","value":2}]'
```

## 打赏支持

觉得有用？请我喝杯咖啡～
微信/支付宝：私信获取

## 定制服务

需要定制 JSON 处理逻辑？私聊报价 ¥200 起
