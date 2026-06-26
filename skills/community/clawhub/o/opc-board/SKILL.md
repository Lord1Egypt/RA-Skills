---
name: opc-board
description: >-
  OPC Board — 5 advisors stress-test your solo idea across 5 dimensions (logic, deliverability, growth, viability, risk), output a scored feasibility report with Go/No-Go decision.
  Use when evaluating a one-person company, side project, solo venture, or open-source project feasibility,
  or when the user says "帮我评审一下", "这个想法靠谱吗", "is this idea viable",
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
7️⃣ 技术栈  8️⃣ 资源现实  9️⃣ 约束条件  🔟 报告格式（📝Markdown / 📊HTML）
```

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
| Markdown（默认） | [report-template-markdown.md](references/report-template-markdown.md) |
| HTML 专业版 | [report-template-pro.html](references/report-template-pro.html) |
| 顾问人设/话术 | [soul.md](references/soul.md) |

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
- 顾问人设话术风格 · 追问深度与轮次 · MoSCoW 条目数量 · 报告格式（Markdown/HTML）

## 验收与失败路径

- **清单追问**：≤3 轮未响应 → 标注缺失信息，跳过项保守分 1 继续
- **顾问质疑**：每维≥3 条质疑；信息不足时给出假设并保守打分
- **完成标准**：报告含所有 Rigid 项 + 综合分公式校验通过
- **失败判定**：用户提供信息不足以判断任何一维（如仅提供名称无其他信息且拒绝补充）→ 告知无法出具有效评分

## 运行时说明

本 skill 无运行时脚本，工作流第 5 步（子项打分→权重归一化→综合分）由 LLM 读取 [scoring-engine-deterministic.md](references/scoring-engine-deterministic.md) 后自行计算执行。本 scoring-engine 为 OPC Board 专属评分引擎，与仓库中其他同名文件无关。
