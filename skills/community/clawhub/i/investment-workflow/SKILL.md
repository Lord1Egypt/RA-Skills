---
name: investment-workflow
version: 1.1.0
description: "［何时使用］当用户需要投研分析时；当用户说'分析这个标的'、'现在什么值得买'、'对 XX 行业怎么看'、'这个热点有什么影响'、'开会讨论投资'时触发。场景驱动的投研全流程，覆盖 6 个场景。"
author: 燃冰 & ant
created: 2026-04-24
skill_type: 通用🟡
allowed-tools: [Bash, Read, Write, Exec, WebSearch]
related_skills: [investment-advisory-workflow, fund-analyzer-pro, holding-diagnoser, fund-allocator, ljg-skills]
tags: [投资研究, 场景驱动, 工作流, 市场分析, 行业分析]
---

# investment-workflow: 投资工作流 🎯

## 📋 功能描述

帮助用户**系统化执行投研全流程**。不是一套固定流程，是 6 个用户场景 × 共享 Skill 模块的排列组合。

**适用场景：**
- 买股票 / 投行业 / 扫描推荐 / 行业看法 / 热点分析 / 开会讨论

**边界条件：**
- 不替代深度基本面研究
- 输出为 Markdown 报告，需配合 data_layer / mcp-aktools 获取真实数据
- 场景识别依赖用户输入关键词
- **模糊输入处理**：用户输入过于模糊（如"最近怎么样？"）时，先询问澄清（行业/事件/标的），不强行触发完整工作流

---

## 🔄 6 个核心场景

| 场景 | 触发词 | 调用步骤 | 输出 |
|------|--------|---------|------|
| 买股票 | "我要买股票"、"分析 XX" | data-query → stock-research → decision-integrate | Markdown 决策报告 |
| 投行业 | "我要投行业"、"XX 行业值得投吗" | industry-rank → data-query → multi-view → decision-integrate | Markdown 行业报告 |
| 扫描推荐 | "现在什么值得买？" | market-scan → industry-rank → data-query → decision-integrate | Top 3 标的 + 优先级 |
| 行业看法 | "对 XX 行业怎么看" | industry-rank → deep-think → plain-explain | Markdown 散文 |
| 热点分析 | "这个热点有什么影响" | market-scan → industry-rank → multi-view → plain-explain | Markdown 影响分析 |
| 开会讨论 | "开会讨论" | multi-view → decision-integrate | Markdown 会议纪要 |

详细共享 Skill 说明 → `references/shared-skills.md`
数据层集成说明 → `references/data-layer-integration.md`

---

## 🔄 核心执行流程（6 阶段）

> **原则**：按场景调用 2-4 个阶段，非必须不跑全 6 步。

### 阶段①：场景识别
**动作**：从用户输入提取关键词，匹配 6 个核心场景之一。
**输出**：场景名称 + 触发步骤列表。
**降级**：若输入模糊（如"最近怎么样？"），先询问澄清，不强行触发。

### 阶段②：数据查询（market-scan / data-query / industry-rank）
**动作**：调用 data_layer / mcp-aktools 获取实时数据。
**指令**：
- 优先调用 `data_layer`（带缓存）。
- 失败时降级到本地缓存或明确告知"数据获取失败"。
- 标注数据来源与时间：`[数据：指标 | 来源：数据源 | 时间：时间]`。

### 阶段③：深度分析（stock-research / multi-view / deep-think）
**动作**：执行降秩分析、追本分析或多视角验证。
**指令**：
- 必须保留推演链（表象→机理→原理→公理）。
- 附 ASCII 关系图辅助理解。
- **合规转化**：若用户请求"帮我买 XX"或"推荐代码"，**不直接拒绝**，转化为"交易成本分析"或"筛选方法论"投教内容。

### 阶段④：逻辑验证（decision-checklist / mental-models）
**动作**：使用芒格思维模型/检查清单验证分析逻辑。
**输出**：逻辑漏洞清单 + 修正建议。

### 阶段⑤：决策整合（decision-integrate）⭐ 核心
**动作**：综合所有分析，给出明确建议。
**指令**：
- **必须输出**：`买入 / 卖出 / 持有 / 观望` 之一。
- **必须标注**：置信度（高/中/低）及理由。
- 若数据不足，明确说明"因 XX 数据缺失，置信度低"。
- **禁止**：只罗列数据表格，不给结论。

### 阶段⑥：多形式输出（调用表达层）⭐ 核心
**动作**：将决策报告传递给 `expression-layer` 进行格式化。
**指令**：
- 调用 `expression-layer`，传入 `content` + `intent`（plain/writes/card/wechat）。
- **禁止**：直接输出原始 Markdown，必须经表达层路由。
- 输出形式：Markdown 报告 / PNG 卡片 / HTML 演讲 / 公众号推文。

---

## ⚠️ 常见错误

**错误 1：线性执行所有阶段**
```
问题：
• 用户只问"XX 怎么看"，却跑完 5 个阶段
• 输出冗长，用户找不到重点

解决：
✓ 严格按场景定义调用 2-4 个共享 Skill
✓ 输出聚焦场景核心问题
```

**错误 2：忽略数据层降级**
```
问题：
• mcp-aktools 或 data_layer 调用失败
• 报告数据为空或报错

解决：
✓ 优先调用 data_layer（带缓存）
✓ 失败时降级到本地缓存或明确告知"数据获取失败"
✓ 标注数据来源与时间
```

**错误 3：推理过程缺失**
```
问题：
• 直接给结论，用户不知道"怎么想到的"
• 缺乏降秩/追本/验证过程

解决：
✓ 每个结论必须保留推演链
✓ 使用 [数据：指标 | 来源：数据源 | 时间：时间] 格式
✓ 附 ASCII 关系图辅助理解
```

**错误 4：数据罗列无结论**
```
问题：
• 阶段③只输出数据表格，阶段⑤未给出明确建议
• 用户得不到 actionable 的建议

解决：
✓ 阶段⑤必须综合数据给出"买/卖/持有"建议及置信度
✓ 使用 decision-integrate 共享 Skill 整合所有分析
```

**错误 5：合规拦截过度**
```
问题：
• 遇到模糊或交易指令，直接拒绝
• 未提供替代方案（如"扫描当前强势板块"）

解决：
✓ 执行"合规转化"协议：拒绝 -> 转化为分析/投教
✓ 例："无法直接交易" → "分析交易成本/时机"
```

**错误 6：表达层未调用**
```
问题：
• 阶段⑥未调用 expression-layer
• 输出格式不统一（有时表格，有时纯文本）

解决：
✓ 阶段⑥必须调用 expression-layer，传入 content + intent
✓ 让表达层统一路由至 Markdown/PNG/HTML
```

---

## 🧪 使用示例

**输入：**
```
分析消费 ETF 是否值得投？
```

**预期输出：**
- 识别场景：投行业
- 调用：industry-rank → data-query → multi-view → decision-integrate
- 输出：Markdown 报告（含降秩分析、数据验证、圆桌讨论、决策建议）

**输入：**
```
现在什么值得买？
```

**预期输出：**
- 识别场景：扫描推荐
- 调用：market-scan → industry-rank → data-query → decision-integrate
- 输出：Top 3 标的 + 优先级 + 逻辑

---

## 🔧 故障排查

| 问题 | 检查项 |
|------|--------|
| 不触发 | description 是否包含触发词？用户输入是否匹配场景？ |
| 数据为空 | data_layer 是否安装？mcp-aktools 是否运行？缓存是否过期？ |
| 输出过长 | 是否跨场景调用？检查场景定义，只调用必要步骤 |
| 推理缺失 | 是否跳过降秩/追本步骤？检查共享 Skill 执行顺序 |

---

## 🔗 相关资源

- 共享 Skill 文档：`references/shared-skills.md`
- 数据层集成：`references/data-layer-integration.md`
- 报告模板：`templates/report-template.md`
- 表达层路由：`../expression-layer/SKILL.md`
- 标准参考：`docs/SKILL-STANDARD-v3.md`
