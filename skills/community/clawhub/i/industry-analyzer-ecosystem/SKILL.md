---
name: ecosystem-mapper
description: "Map the supply chain ecosystem of a given industry — identify upstream/midstream/downstream/horizontal-support positions and representative companies at each. Use when user asks for '生态图谱', '供应链分析', 'industry ecosystem map', '产业图谱', '行业生态', '产业链'. Outputs markdown with 4-生态位 breakdown + Mermaid diagram. Part of the industry-analyzer plugin (6-Skill 流水线第 2 环)."
---

# 生态图谱分析器 (Ecosystem Mapper)

Map the supply chain ecosystem of a given industry — identify upstream / midstream / downstream / horizontal-support positions and representative companies at each.

## When to Use

- 用户明确要求"分析 {行业} 生态图谱 / 产业链 / 供应链"
- 行业分析流水线第 2 环（由 行业分析成章官 调度）
- 独立召唤：用户给出 `output/{slug}/session.json`，单独跑

## Input

- **必填**：`output/{industry-slug}/session.json`
  - 读取 `industry` / `scope` / `time_window`
- **可选**：用户可指定要重点分析的子环节

## Output

- **文件**：`output/{industry-slug}/02-ecosystem.md`
- **格式**：Markdown，含 4 生态位详解 + 1 个 Mermaid 图

### 4 生态位（标准框架）

| 生态位 | 含义 | 典型内容 |
|---|---|---|
| **上游** | 原材料 / 核心组件 / 设备 | 原料供应、关键零部件、生产设备 |
| **中游** | 核心环节 / 加工制造 / 平台 | 主机制造、平台运营、核心加工 |
| **下游** | 应用 / 客户 / 渠道 | 终端产品、分销渠道、最终用户 |
| **横向支持** | 技术 / 服务 / 监管 | 金融、物流、IT、合规、咨询 |

### 必含要素（每个生态位）

| 要素 | 说明 |
|---|---|
| 环节名 | 该生态位的子环节（如"上游 → 原料"） |
| 代表公司 | ≥3 家，含中英文名 |
| 核心壁垒 | 进入门槛 / 护城河 |
| 关键指标 | 行业关心的核心数字（毛利率、产能、市占率等） |

### 必含元素

- **1 个 Mermaid 图**：覆盖 4 生态位 + 关键公司，结构清晰
- 文字描述：每个生态位 200-400 字

## Workflow

1. **读 session.json**
2. **web_search 行业生态结构**：组合搜索
   - `"{行业} 产业链 结构"`
   - `"{行业} 上游 中游 下游"`
   - `"{行业} 供应链 分析"`
   - `"{industry} value chain analysis"`
   - `"{行业} 生态 头部公司"`
3. **识别 4 生态位**：上游 / 中游 / 下游 / 横向支持
4. **每生态位找 ≥3 家公司**：用 webfetch 验证
5. **提炼核心壁垒 + 关键指标**
6. **生成 Mermaid 图**（flowchart / graph 语法）
7. **写 `02-ecosystem.md`**
8. **更新 session.json**

### 输出模板与 Mermaid 示例

参见 `references/ecosystem-positions.md`

## stop_condition

- `02-ecosystem.md` 存在
- 4 生态位齐全
- 每个生态位 ≥3 家公司
- 含 1 个可渲染的 Mermaid 图
- session.json `status.ecosystem` = `done`

## style

- 结构化、可视化优先、突出关键瓶颈
- 文字简洁（每个公司一句话定位）
- 壁垒和指标要给具体数字或定性描述
- 找不到 → 标"该生态位公开信息有限，给出 1-2 个线索"

## 更新 session.json

- 改 `status.ecosystem` = `done` / `failed`
- 改 `updated_at`
- 在 `data_sources` 追加

## Standalone Mode

同 Skill 1，未提供 session.json 时自动生成最小版本。

## 错误处理

- 行业太新 / 太冷门 → 用 AI 通用知识搭骨架 + 标"未找到具体公司，参考线索：..."
- Mermaid 语法错误 → 改用纯文字层级图
- 公司清单不足 3 家 → 显式说明该环节集中度

## 参考

- 行业分析器总 spec：`~/Downloads/周报生成器/行业分析器/docs/superpowers/specs/2026-06-07-industry-analyzer-design.md` §5.2
- 模板：`references/ecosystem-positions.md`
