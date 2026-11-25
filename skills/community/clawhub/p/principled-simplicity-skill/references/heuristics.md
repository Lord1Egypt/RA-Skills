# 启发式、反模式、例子、影响来源 / Heuristics, Anti-patterns, Examples, Influences

> **何时加载本文件 / Load this when:** 需要决策的拇指法则、要核对工作有没有踩反模式、需要例子锚定一个不熟的情境、或想看上游思想来源。

---

## 决策启发式 / Decision Heuristics

**1. 三 case 原则 / Three-case rule** —— 三个表面不同但失败原因相同的 case?**不要加三条规则,建一个机制**。

**2. 已有能力优先 / Existing-capability-first** —— 创建新逻辑前,先在代码库、Prompt 库、架构里搜——大多数"缺失"的能力其实已经在某处存在。

**3. Prompt 不是垃圾桶 / Prompt is not a trash bin** —— 不要把不清晰的产品逻辑、业务规则、架构债务塞进更长的 Prompt。(Prompt 本身是主症状时,加载 `references/prompt-decompose.md`。)

**4. 好的抽象会减少分支 / Good abstraction removes branches** —— 如果一个所谓抽象**制造的分支比它消除的还多**,那就不是好抽象。**抽象前后数一数分支数**——数字不下降就拒绝。

**5. Demo 不等于产品 / Demo is not product** —— Demo 跑通一个 case,产品要经得住正例、负例、边界例、回归例。把"在 demo 里能跑"当成起点,不是终点。

**6. 优先深模块 / Prefer deep modules** —— 外部接口简单、内部能力强的深模块,优于暴露许多浅层分支。Ousterhout 的话:深度 > 实现的简洁。

**7. 验证是设计的一部分 / Verification is part of design** —— 机制无法被测试 = 设计还没做完。**没有 eval plan = 设计完成度只有一半**。

**8. 过早抽象也是反模式 / Premature abstraction is also an anti-pattern** —— 不要在第一次出现就抽象。等 ≥2 次共因实例后再提炼。"三 case 原则"是地板,不是天花板。

(对"该不该现在抽象"拿不准时,加载 `references/abstraction-readiness.md` 走 5 维评分。)

---

## 反模式 / Anti-patterns

| 反模式 | 描述 | 反制动作 |
|---|---|---|
| Badcase 补丁成瘾 | 每个失败都变成一条特殊规则 | 修之前先按根因聚类 |
| 关键词路由成瘾 | 工具选择依赖表层词,而非意图与上下文 | 建意图分类器;规则只管可用性/权限 |
| Prompt 膨胀 | 系统 Prompt 变成未解决决策的垃圾桶 | 加载 `references/prompt-decompose.md`,重分配到 memory/skill/code |
| 规则与模型职责混乱 | 规则做语义理解,模型做确定性约束 | 应用 Step 6(显性分配 model/code/eval) |
| 能力重复 | 没有共享模块,相似逻辑散落各处 | 提取;建 capability registry;重构调用点 |
| 没有负例 | 只测 happy path | 给每个 eval 加负例 + 边界例 + 回归例 |
| 架构表演 | 用 agent/skill/runtime/harness 等词,但责任边界不清 | 每个命名组件都要给一行接口规格 |
| 领域锁死的抽象 | "通用"机制只用一个行业/项目解释 | 在纸上把抽象**应用到另一个领域**测试一下 |
| 过早抽象 | 单一 case 就提炼机制 | 等 ≥2 次共因实例 |

---

## 实战例子 / Worked Examples

### 例 1 — 登录失败处理 / Login Failure Handling

**输入 / Input:** 几个用户登录失败。提议修复:给每种错误文案加特殊处理。

**Principled Simplicity 回应 / Response:**

```text
Direct Judgment / 直接判决: mechanism-level solution(不是 case 补丁)。

Problem Reframe / 问题重构: 不是几个孤立的登录失败——这是
认证状态(auth-state)与错误归一化(error-normalization)问题。

抽象路径:
  case      → multiple login failures / 多个登录失败
  pattern   → inconsistent auth states + fragmented provider error messages
  mechanism → unified auth-error normalizer + recovery router
  module    → AuthFailureClassifier
  eval      → 过期 token / 密码错误 / 账号锁定 / 网络超时 /
              SSO 回调失败 / 缺少权限
```

### 例 2 — Agent 工具选择 / Agent Tool Selection

**输入 / Input:** Agent 在该读本地文件时调用了搜索工具。提议修复:加"if user says 'file', use file tool"。

```text
Direct Judgment / 直接判决: mechanism-level——tool-intent arbitration。

Problem Reframe / 问题重构: 不是关键词漏配——本质是
真相源(source-of-truth)在本地文件、连接文档、Web、
记忆、生成内容之间不清。

抽象路径:
  case      → 工具选错
  pattern   → source-of-truth ambiguity / 真相源歧义
  mechanism → source-of-truth classifier + candidate tool ranking + preflight check
  module    → ToolRoutingArbiter
  eval      → 本地文件 / 上传文件 / 连接文档 / 公开网页 /
              私有记忆 / 来源歧义 / 来源不可用
```

### 例 3 — 重复代码分支 / Repeated Code Branches

**输入 / Input:** 五个 badcase 在不同文件里被五个 if/else 分支修了。

```text
Direct Judgment / 直接判决: 补丁扩散风险——选机制前先聚类。

动作: 先按根因聚类五个 case。
如果根因一致,提取一个机制。
验收标准:
  - 散落分支总数下降
  - 覆盖原有五个 case + 新变体
  - 包含负例和边界测试
  - 回归测试防止原五个 case 复发
```

---

## 影响来源(完整版)/ Influences (Full)

| 来源 | 原则 | 对 Principled Simplicity 的启发 |
|---|---|---|
| Karpathy: Software 3.0 | 上下文、Prompt、工具、记忆是**程序的一部分**,不是装饰 | 把重复推理沉淀成可复用的 skill / context / eval |
| Anthropic Skills 设计 | Skill 要**够窄**才能被准确路由,**够深**才能解决一类有意义问题 | 拒绝巨大万能 Prompt |
| Context-first engineering | AI 系统的质量受限于它收到的**上下文质量** | 修复前先重建最小必要上下文 |
| TDD / Verification-first | 没有回归保护的修复**只是临时补丁** | 每个机制必须包含正例、负例、边界例、回归例 |
| Ousterhout: Deep Modules | 好抽象把复杂度藏在简单接口后 | 抽象**增加了**散落分支就拒绝它 |

---

## 最终原则(完整版)/ Final Principle

低级 AI 开发修 case。高级 AI 架构造机制。真正强的 Skill,会把重复机制沉淀成可复用认知资产。

大道至简的最高形态,不是规则更少——而是因为正确抽象已经存在,所以不再需要那么多 **不必要的** 规则。
