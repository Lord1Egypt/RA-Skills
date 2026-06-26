# investment-workflow: 投资工作流

场景驱动的投研全流程。覆盖 6 个场景，8 个共享 Skill 模块。

## 快速开始

```
/投资研究 分析消费 ETF 是否值得投？
```

## 场景

| 场景 | 触发词 | 步骤 |
|------|--------|------|
| 买股票 | "我要买股票"、"分析 XX 股票" | data-query → stock-research → decision-integrate |
| 投行业 | "我要投行业"、"XX 行业值得投吗" | industry-rank → data-query → multi-view → decision-integrate |
| 扫描推荐 | "现在什么值得买？" | market-scan → industry-rank → data-query → decision-integrate |
| 行业看法 | "对 XX 行业怎么看" | industry-rank → deep-think → plain-explain |
| 热点分析 | "这个热点有什么影响" | market-scan → industry-rank → multi-view → plain-explain |
| 开会讨论 | "开会讨论" | multi-view → decision-integrate |

## 共享 Skill

| Skill | 用途 | 复用场景 |
|-------|------|---------|
| `market-scan` | 市场扫描 | 3、5 |
| `industry-rank` | 行业降秩 | 2、4、5 |
| `stock-research` | 股票研究 | 1 |
| `data-query` | 数据查询 | 1、2、3 |
| `multi-view` | 多视角讨论 | 2、5、6 |
| `decision-integrate` | 决策整合 | 1、2、3 |
| `plain-explain` | 白话说 | 4、5 |
| `deep-think` | 追本分析 | 1、2、4 |

## 数据层

- **mcp-aktools**：零 API Key，AKShare 数据源
- **data_layer v2.2.0**：统一数据层，akshare provider

## 报告规范

- 输出格式：Markdown
- 推理过程：每个结论必须保留推演链
- 数据论证：所有数据必须标注来源和时间
- 结构：5 个部分（降秩分析 → 追本分析 → 秩序判定 → 圆桌讨论 → 决策）

## 示例

### 买股票

```
用户：分析贵州茅台是否值得买？
助手：[场景 1：买股票]
     [data-query → 获取行情数据]
     [stock-research → 生成投资报告]
     [decision-integrate → 整合决策]
     [输出 Markdown 报告]
```

### 投行业

```
用户：消费行业值得投吗？
助手：[场景 2：投行业]
     [industry-rank → 降秩分析]
     [data-query → 查消费 ETF 数据]
     [multi-view → 圆桌讨论]
     [decision-integrate → 整合决策]
     [输出 Markdown 报告]
```

### 扫描推荐

```
用户：现在什么值得买？
助手：[场景 3：扫描推荐]
     [market-scan → 市场扫描]
     [industry-rank → 降秩分析]
     [data-query → 数据验证]
     [decision-integrate → 排序推荐]
     [输出 Top 3 标的]
```

---

*版本：v1.0.0 | 2026-04-24*
