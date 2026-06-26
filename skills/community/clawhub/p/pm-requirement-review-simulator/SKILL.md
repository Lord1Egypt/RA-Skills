---
name: pm-requirement-review-simulator
description: >-
  PRD review stress-test simulator: 5 cross-functional roles challenge your requirements
  across 3 difficulty levels, outputs a scored HTML survival report with radar chart and meeting script.
  Use when PRD review, requirement review simulation, or cross-functional pushback rehearsal,
  or when the user says「评审需求」「模拟评审会」「帮我预演一下」.
---

# PM 需求评审模拟器 · Requirement Review Simulator

> **EN** Five roles stress-test your PRD before the real meeting → survival score + meeting assets.  
> **中文** 五角色预演评审攻防 → 存活率报告 + 会议脚本。

**When / 何时用：** 评审前预演 · 跨部门博弈 · 会议资产准备  
**Not / 不用：** 从零写 PRD · 上线后全面复盘 · 替用户拍板

```text
Review our group-buying feature. Realistic mode.
帮我评审拼团功能，实战模式。
```

结构化输入 → [user_templates.md](references/user_templates.md)

| 档位 | EN | 中文 |
|------|----|------|
| 🟢 | Rookie — gentle | 新手村 |
| 🟡 | Realistic — big-tech | 实战（默认） |
| 🔴 | Hell — hostile | 地狱 |

## 工作流

```text
1) 提交需求  2) 信息采集清单  3) 识别类型 + PRD 来源 + N/A 维度
4) 五角色质疑（按残酷度）  5) 子项打分 → 存活率  6) HTML 报告 + 会议资产
```

### 信息采集清单（第 2 步）

```text
1️⃣ 需求名称  2️⃣ 业务目标  3️⃣ 核心功能  4️⃣ 残酷度  5️⃣ 行业  6️⃣ 公司规模
7️⃣ 技术栈  8️⃣ 约束  9️⃣ 评审角色  🔟 需求类型  1️⃣1️⃣ N/A 维度  1️⃣2️⃣ PRD 来源
```

跳过项保守分 1。

## 五角色 × 五维

| 角色 | 主评维度 |
|------|---------|
| 🛠️ 技术 | 技术友好 |
| 📈 运营 | 运营价值 |
| 🎨 设计 | 运营价值 |
| 👔 老板 | 老板满意 |
| ⚖️ 法务 | 合规安全 |

五维：逻辑自洽（永不 N/A）· 技术友好 · 运营价值 · 老板满意 · 合规安全。公式 → [scoring-engine-deterministic.md](references/scoring-engine-deterministic.md)。

## 输出

按 [report-template-pro.html](references/report-template-pro.html) 生成 HTML；格式锁与自检 → [review-playbook.md](references/review-playbook.md)。

必含：存活率卡 · Go 结论 · 五角色质疑 · 杀手回复 TOP3 · RACI · 会议脚本 · 行动清单 · 免责声明。

## 硬约束

- **信息优先**：禁止编造；缺失→保守分 1；推断须标注；清单追问优于脑补
- **评分**：25 子项逐项；禁止凭感觉；必须有 Go 结论；残酷度确认后不降级
- **优先级**：信息优先 > 评分引擎 > 报告模板 > 角色灵魂
- **合规**：免责声明；专业领域提醒咨询持牌人士

**Rigid**（不可跳过）：
- 25 子项逐项打分 · 存活率公式计算 · Go/Conditional/No Go 结论 · 残酷度确认后不降级 · 杀手回复 TOP3 · RACI · 免责声明

**Flexible**（可按场景调整）：
- 角色话术措辞风格 · 质疑排序 · 会议脚本详略 · 行动清单条目数量

## N/A 维度规则

N/A 维度须在信息采集清单第 11 项确认，不可在评审中途自行降维。确认后该维子项不参与总分计算，公式分母相应减少。

## 验收与失败路径

- **清单追问**：≤3 轮未响应 → 标注缺失信息，跳过项保守分 1 继续
- **残酷度**：确认后不降级；用户明确要求降级须重新确认
- **角色质疑**：每角色≥2 条质疑（地狱模式≥4 条）；信息不足时以保守假设质疑
- **完成标准**：存活率≥70% 为 Conditional Pass；≥85% 为 Pass；<50% 为 Fail
- **失败判定**：核心功能描述完全缺失且用户拒绝补充 → 告知无法有效评审

## 运行时说明

本 skill 无运行时脚本，工作流第 5 步（子项打分→存活率）由 LLM 读取 [scoring-engine-deterministic.md](references/scoring-engine-deterministic.md) 后自行计算执行。本 scoring-engine 为 PM 需求评审模拟器专属评分引擎，与仓库中其他同名文件无关。

## 参考文件

| 文件 | 内容 |
|------|------|
| [references/scoring-engine-deterministic.md](references/scoring-engine-deterministic.md) | 评分引擎 |
| [references/review-playbook.md](references/review-playbook.md) | 角色话术 · 格式锁 |
| [references/report-template-pro.html](references/report-template-pro.html) | HTML 模板 |
| [references/user_templates.md](references/user_templates.md) | 输入模板 |
