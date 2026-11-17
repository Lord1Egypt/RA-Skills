---
name: opc-board
description: >-
  OPC Board — 5 advisors stress-test your solo idea across 5 dimensions (logic, deliverability, growth, viability, risk), output a scored feasibility report with Go/No-Go decision.
  Use when evaluating a one-person company, side project, solo venture, or open-source project feasibility,
  or when the user says "这个一人项目靠谱吗", "这个想法靠谱吗", "is this idea viable",
  "can I build this alone", "一个人能做出来吗", "值不值得做", "这个开源项目靠谱吗".
---

# 一人董事会 · OPC Board

> **EN** Five advisors stress-test your solo idea → scored feasibility report + Go / No Go.  
> **中文** 五位顾问五维压测 → 带评分可行性报告 + Go / No Go。

**When / 何时用：** indie SaaS · open source · side project · 独立开发 / 开源 / 副业  
**Not / 不用：** 从零写方案 · 上线后全面复盘 · 替用户拍板

```text
Review my AI weekly newsletter SaaS idea
帮我评审一下我做的 AI 周报 SaaS
```

Say「用示例跑一下」/ "run with an example" for a demo input.

## 可直接触发的说法

以下口语输入都应触发本技能，不要求用户先写成商业计划：

- 这个想法靠谱吗？帮我拍砖。
- 一个人能不能做出这个产品？
- 我想做一个 XX 副业，值不值得投入？
- 帮我判断这个开源项目有没有长期维护价值。
- 我有个 SaaS 点子，帮我用五个顾问压测一下。
- 这个项目适合盈利、开源，还是只当实验？
- 帮我给这个 idea 一个 Go / No Go 结论。

## 最小可用输入

**最低可启动**：一句想法 + 项目目标（盈利/开源/实验三选一，缺失时先预填“实验”并询问确认）。

**推荐输入**：想法名称、目标用户、核心场景、项目目标、商业模式或可持续策略、冷启动渠道、技术栈、个人资源、输出格式、约束条件。

**可兼容输入**：

- 只有一句话：先提炼定位、用户、目标和核心假设，再输出采集清单。
- 只有产品名：不足以评分，先追问一句“它解决谁的什么问题”。
- 用户说“直接生成”：只跳过业务信息追问，用保守假设继续，缺失项按 1 分处理并标注 evidence；**不视为跳过输出格式确认**。
- 非盈利/开源项目：商业可持续维度按开源/社区维护替代子项评分，不直接判 0。

## 工作流

```text
1) 用户提交想法
2) 输出信息采集清单（确认或"跳过"）
3) 识别项目目标 + 需求类型 + N/A 维度
4) 五顾问逐个质疑
5) 子项打分 → 权重归一化 → 综合分
6) 生成报告 + OPC 决策卡
```

### 信息采集清单（第 2 步）

预填已有信息；缺失标「待补充」；可说「跳过，直接生成」（跳过项保守分 1）。

```text
1️⃣ 产品/想法名称  2️⃣ 核心定位  3️⃣ 项目目标（💰盈利/🌐开源/🧪实验）
4️⃣ 目标用户  5️⃣ 商业模式或可持续策略  6️⃣ 冷启动渠道
7️⃣ 技术栈  8️⃣ 资源现实  9️⃣ 约束条件  🔟 报告格式（📊HTML / 📝Markdown）
```

**采集交互（优先使用可操作表单）**：

- **必须复用** [assets/intake-form.html](assets/intake-form.html)，不得临时重写表单 UI。
- 通过 `prefill` URL 参数注入 URI 编码 JSON；推断值不得冒充确认值，输出格式保持未选。
- 宿主支持时内嵌，否则复制资产并用浏览器打开；提交后读取回传或用户粘贴的结构化参数。回传统一使用 `{schema_version:"1.0", skill, action, data}`；优先 `window.codex.submitForm`，兼容 `window.openai.sendFollowUpMessage`，最后复制 JSON。
- 仅当 HTML 无法使用时退回文本清单；格式未确认不得生成，用户明确委托默认时使用 HTML。

按身份追加：开发者→MVP/技术栈；创作者→粉丝/复购；咨询师→交付物/报价。行业增量：电商 · B2B SaaS · 金融科技（合规一票否决）。

## 五顾问 × 五维

| 顾问 | 主评 | 兼评 |
|---|---|---|
| 🛠️ 技术 | 独立可交付 | 逻辑自洽 |
| 📈 增长 | 增长可行 | 逻辑自洽 |
| 🎨 体验 | 增长可行 | 独立可交付 |
| 💰 商业 | 商业可持续 | 逻辑自洽 |
| ⚖️ 风险 | 风险可控 | 逻辑自洽 |

五维：逻辑自洽 · 独立可交付 · 增长可行 · 商业可持续 · 风险可控。每维 5 子项（0/1/2），公式见 [scoring-engine-deterministic.md](references/scoring-engine-deterministic.md)。工具：MoSCoW · North Star · CJM · Lean Canvas · Pre-Mortem。

## 输出

| 格式 | 模板 |
|------|------|
| HTML 专业版 | [report-template-pro.html](references/report-template-pro.html) |
| Markdown 快速版 | [report-template-markdown.md](references/report-template-markdown.md) |
| 顾问人设/话术 | [soul.md](references/soul.md) |

按采集表确认的格式与对应模板生成；格式已明确时不重复询问。

必含：评分卡 · Go/Conditional/No Go · 五顾问质疑 · Pre-Mortem · MoSCoW · OPC 决策卡 · 行动清单 · 免责声明。

## 硬约束

- **信息优先**：禁止编造；缺失→保守分 1 + evidence；推断须标注；清单追问优于脑补
- **评分**：25 子项逐项打分；禁止凭感觉；必须有 Go 结论 + OPC 决策卡
- **文风**：去 AI 化；具名、具数、具动作
- **优先级**：信息优先 > 评分引擎 > 报告模板 > 顾问灵魂
- **合规**：免责声明；法律/金融/医疗仅风险提示，不替代表达合规方案

**Rigid**（不可跳过）：
- 25 子项逐项打分 · 公式计算综合分 · Go/Conditional/No Go 结论 · OPC 决策卡 · Pre-Mortem · 免责声明 · 信息采集清单先行

**Flexible**（可按场景调整）：
- 顾问人设话术风格 · 追问深度与轮次 · MoSCoW 条目数量 · 报告格式（HTML/Markdown）

## 验收与失败路径

- **清单追问**：≤3 轮未响应 → 标注缺失信息，跳过项保守分 1 继续
- **只有一句想法**：可启动，但必须列出 ≤3 条关键假设，并在评分 evidence 中标注
- **只有产品名**：不能直接评分；先追问目标用户和核心问题，用户拒绝补充才失败
- **非商业目标**：不得强行按盈利项目扣死分；按开源/实验规则重算商业可持续维度
- **合规敏感**：金融/医疗/法律等场景必须让风险顾问优先质疑，必要时触发 No Go
- **顾问质疑**：每维≥3 条质疑；信息不足时给出假设并保守打分
- **完成标准**：报告含所有 Rigid 项 + 综合分公式校验通过
- **失败判定**：用户提供信息不足以判断任何一维（如仅提供名称无其他信息且拒绝补充）→ 告知无法出具有效评分

## 运行时说明

本 skill 无运行时脚本，工作流第 5 步（子项打分→权重归一化→综合分）由 LLM 读取 [scoring-engine-deterministic.md](references/scoring-engine-deterministic.md) 后自行计算执行。本 scoring-engine 为 OPC Board 专属评分引擎，与仓库中其他同名文件无关。

## 参考文件

| 文件 | 内容 |
|------|------|
| [references/scoring-engine-deterministic.md](references/scoring-engine-deterministic.md) | 评分引擎 |
| [references/report-template-markdown.md](references/report-template-markdown.md) | Markdown 报告模板 |
| [references/report-template-pro.html](references/report-template-pro.html) | HTML 专业报告模板 |
| [references/soul.md](references/soul.md) | 五顾问人设与话术 |
| [assets/intake-form.html](assets/intake-form.html) | 跨 Agent 可复用采集表 UI |
