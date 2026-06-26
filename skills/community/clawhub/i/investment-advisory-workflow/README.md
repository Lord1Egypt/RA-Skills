# investment-advisory-workflow: 投资顾问工作流

场景驱动的投顾全流程。融合林奇/卡尼曼/芒格/马利克 四位专家思想，覆盖 5 个用户场景。

## 快速开始

```
/投资顾问 最近消费怎么看？
/投资顾问 帮我看看持仓
/投资顾问 100 万怎么配置？
/投资顾问 大跌了怎么办？
```

## 场景

| 场景 | 触发词 | 步骤 | 输出 |
|------|--------|------|------|
| 市场解读 | "最近 XX 怎么看？" | market-scan → industry-rank → plain-explain → ljg-card | Markdown + PNG 卡片 |
| 事件分析 | "这个事件有什么用？" | market-scan → industry-rank → multi-view → plain-explain → decision-integrate | Markdown 影响分析 + 操作建议 |
| 持仓诊断 | "帮我看看持仓" | data-query → holding-diagnoser → decision-checklist → fund-allocator → report-generator | Markdown 诊断报告 + 调仓建议 |
| 资产配置 | "100 万怎么配置？" | decision-checklist → fund-allocator → ljg-roundtable → IPS 模板 → report-generator | Markdown 配置方案 + IPS |
| 行为纠偏 | "大跌了怎么办？" | market-scan → companion-script → ljg-relationship → problem-mapper → plain-explain | Markdown 纠偏方案 + 话术 |

## 四专家思维框架

| 专家 | 视角 | 核心能力 | 对应 Skill |
|------|------|---------|-----------|
| 林奇 | 洞察发掘 | 生活化触达/故事驱动/持续观察 | ljg-learn, ljg-plain, ljg-rank, fund-analyzer |
| 卡尼曼 | 行为纠偏 | 认知偏误画像/负面叙事/选择架构 | decision-checklist, companion-script, ljg-relationship |
| 芒格 | 逆向检查 | 双轨分析/安全边际/失败预演 | ljg-think, ljg-roundtable, mental-models, problem-mapper |
| 马利克 | 系统管理 | 目标约束/多方案/反馈回路 | fund-allocator, report-generator, task-state-tracker |

## 数据层

- **data_layer v2.2.0**：统一数据层，akshare + fund_eastmoney provider
- **mcp-aktools**：零 API Key，AKShare 数据源
- **qieman-mcp**：且慢 MCP，持仓穿透/业绩归因/策略详情

## 共享 Skill

| Skill | 用途 | 复用场景 |
|-------|------|---------|
| `market-scan` | 市场扫描 | 1, 2 |
| `industry-rank` | 行业降秩 | 1, 2, 5 |
| `stock-research` | 股票研究 | 1, 2, 3 |
| `data-query` | 数据查询 | 1, 2, 3 |
| `multi-view` | 多视角讨论 | 2, 3, 5 |
| `decision-integrate` | 决策整合 | 1, 2, 3 |
| `plain-explain` | 白话说 | 1, 5, 6 |
| `deep-think` | 追本分析 | 2, 3, 5 |
| `companion-script` | 安抚话术 | 5, 6 |
| `holding-diagnoser` | 持仓诊断 | 3, 5 |
| `fund-analyzer-pro` | 基金深度分析 | 3, 5 |
| `fund-allocator` | 资产配置 | 2, 3 |
| `decision-checklist` | 检查清单 | 2, 3 |
| `report-generator` | 报告生成 | 3, 5, 6 |
| `content-compliance` | 合规审查 | 4 |

## 示例

### 场景 1：市场解读

```
用户：最近消费怎么看？
助手：[场景 1：市场解读]
     [market-scan → 市场快照]
     [industry-rank → 降秩分析]
     [plain-explain → 白话说]
     [ljg-card → 可视化卡片]
     [输出 Markdown + PNG]
```

### 场景 2：事件分析

```
用户：央行降准有什么用？
助手：[场景 2：事件分析]
     [market-scan → 当前状态]
     [industry-rank → 分析影响行业]
     [multi-view → 多视角验证]
     [plain-explain → 口语化影响评估]
     [decision-integrate → 是否需要调仓]
     [输出 Markdown 影响分析 + 操作建议]
```

### 场景 3：持仓诊断

```
用户：帮我看看持仓
助手：[场景 3：持仓诊断]
     [data-query → 持仓数据查询]
     [holding-diagnoser → 5 层诊断]
     [decision-checklist → 偏误诊断]
     [fund-allocator → 优化建议]
     [report-generator → 诊断报告]
     [输出 Markdown 诊断报告 + 调仓建议]
```

### 场景 4：资产配置

```
用户：100 万怎么配置？
助手：[场景 4：资产配置]
     [decision-checklist → 风险容忍度评估]
     [fund-allocator → 资产配置框架]
     [ljg-roundtable → 多视角验证]
     [IPS 模板 → 投资政策说明书]
     [report-generator → 配置报告]
     [输出 Markdown 配置方案 + IPS]
```

### 场景 5：行为纠偏

```
用户：大跌了怎么办？
助手：[场景 5：行为纠偏]
     [market-scan → 实时数据]
     [companion-script → 安抚话术]
     [ljg-relationship → 行为模式识别]
     [problem-mapper → 纠偏策略]
     [plain-explain → 白话说]
     [输出 Markdown 纠偏方案 + 话术]
```

---

*版本：v1.0.0 | 2026-04-24*
