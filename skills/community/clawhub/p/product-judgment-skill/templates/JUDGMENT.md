# JUDGMENT.md
> Product Judgment Record — 产品需求判决书
> Generated / Updated: {{DATE}}
> **Commit this file. It is the permanent record of why this demand was (or wasn't) built.**
> **Only new evidence (L2+) changes this verdict. Authority, deadlines, and sunk cost do not.**

---

## ⚖️ Verdict / 判决

### **{{VERDICT}}**
> 可选：BUILD / VALIDATE FIRST / DE-SCOPE / REFRAME / KILL

| 维度 | 值 |
|------|-----|
| 证据等级 Evidence Level | {{L0-L4}} |
| 资源投入 Resource Commitment | {{Small / Medium / Large / Very Large}} |
| 需求来源 Demand Source | {{User research / Sales / CEO / Competitor / ...}} |
| 触发频率 Trigger Frequency | {{Daily / Weekly / Monthly / Rarely}} |

---

## 📋 Demand Summary / 需求描述

{{用一段话描述需求，不是PRD，就是"我们想做什么、为什么"}}

**Target User / 目标用户：**
{{不是"用户"，是"在X场景下因为Y原因的Z类型用户"}}

**Trigger Context / 触发场景：**
{{什么时候、在哪里、为什么会触发这个需求}}

---

## ⚡ Strike 1: Disease Diagnosis / 病灶命名

<!-- 从以下病型中选择，可多选 -->
<!-- 竞品焦虑症 / 技术炫技症 / 老板幻觉症 / Demo成瘾症 -->
<!-- 替换成本失明 / 商业闭环断裂 / 低频刚需误判 / 万能入口症 -->
<!-- 指标幻觉症 / 场景错配症 -->

- {{病型1}}
- {{病型2（如有）}}

**真实动机 / Real driver:**
{{这个需求表面上是为了用户，实际上的驱动力是什么}}

---

## 🔍 Strike 2: Assumption Interrogation / 假设审讯

### 用户价值公式 / User Value Equation

| 维度 | 内容 |
|------|------|
| 旧体验 Old Experience | {{用户现在怎么解决}} |
| 新体验 New Experience | {{新方案具体好在哪里，不能只写"更方便"}} |
| 替换成本 Replacement Cost | {{学习成本、迁移成本、信任成本、组织成本、金钱成本}} |
| 净用户价值 Net Value | {{高 / 中 / 低 / 未成立}} |

### 需求成立的关键假设 / Critical Assumptions

需求成立，需要以下假设**全部**为真：

1. {{假设1}}
2. {{假设2}}
3. {{假设3}}
4. {{假设4（如有）}}

| 假设 | 验证状态 | 证据 |
|------|---------|------|
| 假设1 | ✅ 已验证 / ⚠️ 部分验证 / ❌ 未验证 | {{数据来源或"无"}} |
| 假设2 | ✅ / ⚠️ / ❌ | {{}} |
| 假设3 | ✅ / ⚠️ / ❌ | {{}} |

**当前证据等级 / Current Evidence Level:** {{L0-L4}}

---

## 💀 Strike 3: Failure Forecast / 失败预演

如果现在直接开发，以下是大概率发生的事：

**第1个月：** {{...}}

**第2-3个月：** {{...}}

**第4个月：** {{...}}

**第5-6个月：** {{...}}

**根因 / Root cause:** {{一句话，不是"执行问题"，而是需求本身的缺陷}}

---

## 💼 Business Model / 商业价值

**价值捕获机制 / Value Capture:** {{用户爽了，公司通过什么赚钱或获得战略价值}}

**商业闭环是否成立：** {{成立 / 不成立 / 不确定}}

---

## ✅ Recommendation / 建议行动

<!-- 根据判决填写 -->

### 如果是 BUILD：
- [ ] PRD已启动
- [ ] 成功指标已定义
- [ ] 60天验证节点已设置

### 如果是 VALIDATE FIRST：
**验证目标：** {{最需要验证的1-2个假设}}

**验证方案：**
- 最低成本实验：{{...}}
- 样本选择：{{...}}
- 成功标准：{{...}}
- 失败信号：{{...}}
- 时间限制：{{几周内完成}}

**验证后决策规则：** 如果{{指标}}达到{{阈值}}，进入完整PRD；否则{{...}}

### 如果是 KILL：
**终止原因摘要：** {{...}}

**资源重定向建议：** {{这些资源可以更好地用在哪里}}

---

## 🔄 Verdict History / 判决历史

| 日期 | 判决 | 证据等级 | 变更原因 |
|------|------|---------|---------|
| {{DATE}} | {{VERDICT}} | {{L?}} | 初始判决 |

> 判决只因新证据而改变。如需修改，在此表格追加记录，并说明新证据是什么。

---

## 📎 Related Files / 相关文件

- [ ] PRD: `docs/prd-{{feature-name}}.md`
- [ ] User Research: `{{link}}`
- [ ] Validation Results: `{{link}}`
- [ ] Post-launch Review: `{{link}}`

---

*Brutal to the logic. Respectful to the person.*
*Product Judgment Skill — 需求不是因为能被做而存在，而是因为值得被做才存在。*
