> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

# SKILL.md 外移附录（入口文档瘦身用）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

> **用途**：承载从 `SKILL.md` 外移的**长表格与平台参数**，使入口文档保持在**本技能适用**的体积上限内。
> **来源**：技能审计（2026-09-13）A1 —— `SKILL.md` 11,335 字符，超过当时套用的 10,000 字符基准，故外移瘦身（该基准的**适用范围订正**见下）。
> ⚠️ **上限口径订正（消除适用范围泛化，2026-09-14）**：10,000 **字符**上限**只适用于 autonomous proposal 的 `SKILL.md`**（官方 `docs/tools/skill-workshop/reference.md`「Autonomous proposal `SKILL.md` | 10,000 characters」；`docs/tools/skill-workshop/configuration.md`）。**通用上限是 `skills.workshop.maxSkillBytes`（默认 40,000 字节，区间 1024-200000，硬顶 200,000）**（官方 `docs/tools/skills-config.md`；`docs/tools/skill-workshop/reference.md`）。**本技能走 direct maintenance**（agent 直接维护 Workshop 目录），官方明写「**direct maintenance does not use proposal limits**」（`docs/tools/skill-workshop/configuration.md`）—— 故 **10,000 字符不是本技能的上限**；「继续瘦身」应按**可读性与 token 预算**取舍，而非套用 proposal 棘轮基准。
> **约束**：本文件内容与 `SKILL.md` 为**派生关系**；冲突时以本文件为准（`SKILL.md` 只留指针）。

---

## 一、spawn 参数约定（主控 spawn 子代理时必用）

> 平台参数，**非 frontmatter 键**——官方 skill frontmatter 无该键且拒顶层未知键。

| 参数 | 取值 | 说明 |
|---|---|---|
| `expectsCompletionMessage` | `true` | 需完成事件回传 |
| `context` | `"isolated"` | 叶子 worker（不带父上下文）|
| `cleanup` | `"keep"` | 保留子会话供调试（平台默认即 keep）|
| `cwd` | **绝对路径** `<workspace>/run/<项目名>/` | **必须绝对路径**，禁相对拼接|
| `runTimeoutSeconds` | **按角色**（见 `SKILL.md` 硬卡阈值表）| 平台**机械**超时，与硬卡阈值同源 |
| `visible` | T5 / T7 → `true`；其余 → 默认（hidden）| 关键路径 dashboard 可见；并行检索员不刷屏 |
| `taskName` | **ASCII**：匹配 `[a-z][a-z0-9_-]*` | **平台强制**（v2.18.1 反哺 FB-03）：中文 / 大写 / 空格 / 点号一律被拒（实测 `T1-文献检索` 被平台打回）；建议形态 `t1-lit-scout`。派发硬验证须含字符集自检 |

---

## 二、主控必读文档清单（🔴 必读全文 / 🟠 分片必读）

> **完整分层清单真源 = [`00-主控-扩展职责.md`](../../agents/00-主控-扩展职责.md)「主控必读文档清单」段**。本表只留 🔴 / 🟠，🟡 按需分片项见真源。
> **表内路径均以仓库根为基准。**

| 层 | 文档 | 标记 |
|----|------|------|
| 0 | `references/agents/00-主控-coordinator.md`（核心职责全貌）| 🔴 |
| 1 | `SKILL.md`（入口）| 🔴 |
| 1 | `references/pipeline-readme.md`（入口）| 🔴 |
| 1 | `references/_shared/真源/glossary-full.md`（入口）| 🔴 |
| 2 | `references/_shared/真源/phase-order/` 目录（流程顺序与阻断关系**唯一真源**，含 `index.yaml` + 27 节点切片；`phase-order.yaml` 为装配视图）| 🔴 |
| 2 | `references/_shared/真源/M-Gate-核心.md`（M-Form/M-Exist/M-Integrity 伪代码段**逐段必读**；「分片」只为省 token，**不表示跳读**）| 🟠 |

---

## 三、License

**MIT License** — Copyright (c) 2026 左运来 (zuoyunlai)。完整文本见 [`LICENSE`](../../../LICENSE)；允许商业使用、修改、分发，需保留版权声明。受 MIT License 约束。

---

## 四、Phase 0 必走步骤 完整条文

1. 读 `references/pipeline-readme.md`（启动清单 / 模型配置 / 派发话术索引）+ [`glossary-full.md`](glossary-full.md)
2. **目标语言确认**：只确认**产出语言**（中文 / English / 中英混 / 其他，写入任务简报「目标语言」字段，**不设默认**）；**明确不收集使用者身份 / 国籍 / 语种背景**
3. **spawn 前必读对应派发话术**（`references/dispatch/` 11 个文件，spawn 哪角色读哪文件，勿凭记忆复制）。**含「能力自检」**：主控核验自身工具面是否超限；子代理 spawn 后首步自检回报 —— **工具面超限 = 警告级**（记录 + 披露 + 照样开工，**≠ 调用许可**）；**实际调用越权工具 = 阻断级**（停止 + 回报 `capability_excess`）。见 [`permissions.md`](../../permissions.md)「能力自检」
4. **审计前必读 G 体系**：`references/agents/07-审计-auditor.md`（G0-G18 必查项 + M 门算法）
5. **文件修改安全流程**：**禁止 `替换 -i`**（静默清空）——用 `edit` 精确 oldText 匹配；改前 `read` 后另存备份（`write` 到 `drafts/archive/`，语义等价 `复制`），改后验证
6. **硬卡阈值表**（左＝硬卡墙钟；右＝平台机械超时 `runTimeoutSeconds`，**同源不另立数**）：T1-T3 10 分钟/**600s** · T4 12 分钟/**720s** · T5 15 分钟/**900s** · T6 15 分钟/**900s** · T7 12 分钟/**720s** · T9 10 分钟/**600s** · G14 8 分钟/**480s** · **spawn watchdog 8 分钟**（spawn 后无产物兜底）

---

## 五、单源指针表低频行（SKILL.md 入口只留高频）

| 需要什么 | 去哪读 |
|---|---|
| 安全须知 / 外部服务声明 / 隐私与外发 | [`external-services.md`](external-services.md) |
| 字数分层 / 字数判定（单一口径：仅正文） | [`字数判定表.md`](字数判定表.md) |
| M 门算法（🟠 分片：伪代码必读 / 附录按需）| [`M-Gate-核心.md`](M-Gate-核心.md) + [附录](M-Gate-Algorithm-appendix.md) |
| 交付边界 / F1-F9 失败模式 / 阶段闸门 | [`deliverables.md`](../../deliverables.md) |
| 模型 5 档候选池 + 运行手册 | [`模型候选池.md`](模型候选池.md)（唯一真源；`model-assignment.md` 已降级为指针页） / [`pipeline-readme.md`](../../pipeline-readme.md) |
