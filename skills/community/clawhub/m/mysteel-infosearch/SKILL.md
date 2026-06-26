---
name: Mysteel_InfoSearch
description: 大宗商品行业资讯查询技能。用于查询钢铁、有色、能源化工等行业的动态新闻、市场快讯、政策变化、企业消息、价格异动分析、供需事件等资讯信息。当用户需要：(1) 了解行业最新动态和新闻；(2) 查询政策法规变化；(3) 获取企业生产经营消息；(4) 分析价格异动原因；(5) 跟踪供需事件；(6) 进行市场跟踪和研究支持时触发此技能。
dependency:
  python:
    - 内置模块 (urllib, json, sys, argparse, pathlib)
---

# Mysteel Info Search

大宗商品行业资讯查询技能，面向钢铁、有色、能源化工、炉料及相关产业链客户，提供行业资讯的智能检索、筛选与聚合服务。

## Quick Start

使用 `scripts/search.py` 脚本查询资讯内容：

```bash
python scripts/search.py "<查询文本>"
```

**读取API密钥**
- 检查`references/api_key.md`文件是否存在
- 如果存在，读取其中的api_key
- 如果文件不存在，提示用户输入API密钥，并将用户输入的密钥保存到`references/api_key.md`文件中

示例：
```bash
python scripts/search.py "钢铁行业最新动态"
python scripts/search.py "铜价异动原因"
python scripts/search.py "房地产政策对钢材需求的影响"
```

脚本参数：
- `--raw`: 输出原始JSON响应

## Query Capabilities

### 1. 行业动态查询
- 钢铁、有色、能源化工行业新闻
- 市场快讯与突发事件报道
- 产业链上下游动态追踪

### 2. 政策法规追踪
- 国家宏观政策解读
- 行业监管政策变化
- 环保、贸易政策影响分析

### 3. 企业消息监控
- 生产经营动态
- 兼并重组信息
- 重大项目进展

### 4. 价格异动分析
- 价格波动原因解读
- 市场情绪分析
- 影响因素梳理

### 5. 供需事件跟踪
- 产能变化信息
- 库存变动情况
- 进出口事件追踪

## Intelligent Features

### 语义理解
- 自动识别关注对象与查询意图
- 行业语义理解与匹配
- 多维度关联分析

### 智能检索
- 海量资讯智能筛选
- 重点信息提炼
- 分类汇总展示

### 业务场景支持
- 日常盯市跟踪
- 市场研究支持
- 客户服务辅助
- 业务决策参考

## API Reference

详细API文档参见 [api_reference.md](references/api_reference.md)。

## Best Practices

1. **精准表达**：描述具体的行业、品种或事件类型，提高检索精准度
2. **时间范围**：可指定时间范围获取特定时期的资讯
3. **持续跟踪**：定期查询关注主题，建立行业认知

## Output Format

查询结果包含：
- **资讯标题与摘要**
- **来源与发布时间**
- **相关实体标签**
- **情感倾向判断**
- **关联数据链接**