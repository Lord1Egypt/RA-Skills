---
name: insight-challenge
slug: yumingtao-insight-challenge
displayName: Insight Challenge
version: 1.7.1
summary: 对代码质量发现进行对抗性审查，用源代码锚定的反向证据产出结构化结论。
license: MIT
tags:
  - 代码审查
  - 开发工具
  - 质量分析
disable-model-invocation: true
description: >
  对代码质量发现进行对抗性审查：用反向证据挑战发现、对照源代码验证主张、产出结构化结论。适用于代码审查、质量分析、架构评估中的发现验证。触发词："审查发现"、"挑战发现"、"insight-challenge"、"challenge finding"。
allowed-tools: Read(*), Glob(*), Grep(*), Bash(*)
session-mode: none
---

# 洞察挑战

对代码质量发现进行对抗性审查：用反向证据挑战发现、对照源代码验证主张、产出结构化结论。

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│  Insight Challenge (SKILL.md) — Adversarial Review          │
│  → Parse finding → Read source → Challenge → Verdict        │
└─────────────────────────────────────────────────────────────┘
                           │
    ┌──────────┬───────────┼───────────┬──────────┐
    ↓          ↓           ↓           ↓          │
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐      │
│Phase 1 │ │Phase 2 │ │Phase 3 │ │Phase 4 │      │
│ Parse  │ │ Source │ │Challenge│ │Verdict │      │
│Finding │ │ Review │ │Analysis │ │Report  │      │
└───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘      │
    │          │          │          │             │
 finding    source     counter-   structured      │
 parsed     code       evidence   verdict         │
```

## 核心设计原则

1. **默认对抗**: 假设发现可能有误，优先寻找反向证据
2. **源代码锚定**: 所有主张必须对照实际代码验证，而非假设
3. **结构化输出**: 结论遵循固定 schema 供下游消费
4. **公正挑战**: 若证据支持发现则确认，不制造怀疑
5. **透明推理**: 展示证据链和推理过程

## 发现输入格式

发现可以 JSON 或结构化文本形式提供。字段要求：

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | JSON 输入必填；内联输入由技能生成 | 发现标识符 |
| `title` 或 `claim` | 是（任一） | 发现标题或可验证主张 |
| `file` 或内联证据 | 是（任一） | 源文件引用，或直接给出的证据文本 |
| `severity` | 否 | 原始严重度 |
| `line` | 否 | 行号 |
| `description` / `evidence` / `suggestion` / `design_ref` | 否 | 补充说明与设计引用 |

缺少必填字段时按 IC-E05 列出缺失项请求补充，不基于猜测执行。

```json
{
  "id": "HIGH-01",
  "title": "知识边类型 resolves/documents 未在 types.ts 声明",
  "severity": "high",
  "file": "src/graph/kg/db/types.ts",
  "line": 58,
  "description": "issue-extractor 使用 'resolves' 边类型...",
  "evidence": "types.ts KnowledgeEdgeKind: defines, constrains...",
  "suggestion": "补齐缺失的边类型声明",
  "design_ref": "Gap 2 — 12 CodeEdgeKind + 9 KnowledgeEdgeKind"
}
```

或结构化文本：
```
HIGH-01: 知识边类型 resolves/documents 未在 types.ts 声明
Severity: high
File: src/graph/kg/db/types.ts:58
Claim: issue-extractor 使用 'resolves' 边类型但未在类型系统中声明
Evidence: types.ts KnowledgeEdgeKind 列表中缺少 'resolves'
```

## 执行流程

按四个阶段依次执行：解析发现 → 源代码审查 → 挑战分析 → 结论报告。

### 阶段 1：解析发现

1. 提取发现 ID、标题、严重度、文件引用和主张。
2. 识别所有可验证的断言：
   - 文件存在性主张
   - 代码结构主张（类型、函数、变量）
   - 行为主张（用法模式、依赖）
   - 设计符合性主张
3. 创建验证清单。

### 阶段 2：源代码审查

1. 读取指定行的引用文件。
2. 使用 Grep/Glob 搜索相关代码。
3. 记录代码的实际状态：
   - 实际存在哪些类型/函数
   - 实际声明了哪些值
   - 实际实现是什么样
4. 将主张与现实对比。

### 阶段 3：挑战分析

对发现中的每个主张：

1. **寻找确认证据**：源代码是否支持该主张？
2. **寻找反证**：源代码是否反驳该主张？
3. **检查误读**：该主张是否基于过时代码或误解？
4. **验证设计引用**：引用的设计文档是否准确？

挑战策略：
- **直接矛盾**：源代码明确显示相反
- **上下文缺失**：发现遗漏了会改变解释的相关上下文
- **过时引用**：发现引用了已更新的代码
- **计数错误**：数字主张（缺少 N 个类型）不正确
- **范围错误**：发现应用了错误范围（如混淆边类型与语言类型）

### 阶段 4：结论报告

产出结构化输出：

```json
{
  "finding_id": "HIGH-01",
  "challenge_result": "overturned|weakened|confirmed",
  "confidence": 95,
  "reasoning": "Detailed explanation of why the finding was challenged or confirmed",
  "counter_evidence": [
    "Source file line 64: 'resolves' IS declared in KnowledgeEdgeKind",
    "Design doc specifies 20 edge types, not 28"
  ],
  "supporting_evidence": [],
  "adjusted_severity": "none|critical|high|medium|low",
  "recommendation": "Dismiss this finding; the claimed gap does not exist"
}
```

产出结论后，运行校验器自检（输入形式：JSON 文件、stdin 管道、markdown 报告提取；JSON 内容可为单条结论、批量 verdicts 对象或顶层数组，用法见 README.md）：

```bash
node scripts/validate-verdict.mjs <verdict.json>   # 或 report.md，或 - 从 stdin 读
```

未通过时按报错修复结论后重新校验（见 IC-E06）。

## 结论定义

| 结论 | 含义 | 适用场景 |
|------|------|----------|
| **overturned** | 发现事实错误 | 源代码直接反驳主张 |
| **weakened** | 发现部分正确但被夸大 | 部分证据支持，但严重度或范围有误 |
| **confirmed** | 发现准确 | 源代码支持所有主张 |

## 挑战模式

### 模式 1：类型声明检查
```
Claim: "Type X is not declared"
Challenge: Read the type file → check if X exists in type union/enum
Counter: "Line N shows X IS declared in the type definition"
```

### 模式 2：设计引用验证
```
Claim: "Design requires N items, implementation has M"
Challenge: Read design doc → verify the claimed requirement
Counter: "Design doc actually specifies K items, not N"
```

### 模式 3：用法验证
```
Claim: "Code uses type X but X is not defined"
Challenge: Check both usage site AND definition site
Counter: "X is defined at line N in file Y"
```

### 模式 4：范围混淆
```
Claim: "Missing 7 edge types (total should be 28)"
Challenge: Check what the "28" actually refers to
Counter: "The 28 refers to language types, not edge types; edge types are 21"
```

## 输出格式

默认输出为 markdown 报告，**内嵌完整 JSON 结论块**——人可直接阅读，机器可解析结论；仅当调用方显式要求纯 JSON 时才省略 markdown 包装：

````markdown
## Challenge Report: <finding_id>

**Verdict**: <overturned|weakened|confirmed>
**Confidence**: <0-100>%
**Adjusted Severity**: <none|critical|high|medium|low>

### Original Finding
<finding summary>

### Counter-Evidence
- <evidence point 1>
- <evidence point 2>

### Supporting Evidence
- <evidence point 1> (if any)

### Reasoning
<detailed explanation>

### Recommendation
<action recommendation>

```json
{
  "finding_id": "<finding_id>",
  "challenge_result": "<overturned|weakened|confirmed>",
  "confidence": <0-100>,
  "reasoning": "<detailed explanation>",
  "counter_evidence": ["<evidence point>", "..."],
  "supporting_evidence": ["<evidence point>", "..."],
  "adjusted_severity": "<none|critical|high|medium|low>",
  "recommendation": "<action recommendation>"
}
```
````

## 错误处理

| 错误码 | 场景 | 处理与恢复 |
|--------|------|-----------|
| IC-E01 | 引用文件不存在 | 报告文件缺失；结论 = weakened（可能已过时） |
| IC-E02 | 行号超出范围 | 改用 Grep 按主张内容搜索重定位；调整行引用 |
| IC-E03 | 设计文档未找到 | 跳过设计验证；在报告中注明 |
| IC-E04 | 证据模糊 | 呈现双方观点；置信度降至 70 以下并说明 |
| IC-E05 | 输入缺必填字段 | 列出缺失项请求补充；不基于猜测执行 |
| IC-E06 | 结论未通过校验器 | 按校验报错修复结论后重新校验 |
| — | 批量多个发现 | 逐个独立处理；产出每个发现的结论 |

## 稳定性保证

- **幂等**：结论只由源代码证据决定——同一发现对照同一代码库，两次挑战产出相同结论。
- **读取重试**：Read 读取失败时改用 Grep 内容搜索一次；仍失败按 IC-E01 降级，不反复重试。
- **上下文上限**：追查调用链最多扩展 2 层；继续收集证据而置信度不再上升时停止扩展。
- **批量隔离**：批量挑战中单条发现失败不阻断其余发现，各自独立产出结论。

## 使用示例

### 单个发现挑战
```
Invoke the insight-challenge skill with:
{"id":"HIGH-01","title":"...","file":"src/types.ts","line":58,...}
```

### 批量挑战
```
Invoke the insight-challenge skill with: findings.json
```

### 内联挑战
```
Challenge this finding:
Claim: Function X is not exported
File: src/utils.ts:45
Evidence: grep shows no export keyword
```

## 相关技能

- **team-adversarial-swarm**：多智能体对抗分析
- **team-quality-assurance**：带问题发现的 QA 流水线
- **codify-to-knowhow**：沉淀已验证知识

## 范围与限制

本技能用于**对照源代码对代码质量发现进行对抗性审查**。**不适用**于：

- 纯安全审计或漏洞扫描任务本身（使用专用安全审查工具）；安全扫描产出的**具体发现**仍可作为输入做对抗性验证。
- 没有具体发现可挑战的完整 MR/PR 通用代码审查。
- 无法对照可访问的源代码、设计文档或运行时证据验证的发现——此时输出 `weakened` 并注明证据不可用。
- 无可验证事实主张的纯风格或偏好类发现。

## 常见问题

**Q: 源文件不存在怎么办？**
A: 输出 `weakened` 并降低置信度。注明文件缺失为原因；不要猜测发现是错的。

**Q: 多个发现互相矛盾怎么办？**
A: 逐个独立挑战。若一个发现的证据推翻另一个，在 `reasoning` 字段中注明冲突。

**Q: 可以不读源代码就确认发现吗？**
A: 不行。始终对照源代码验证。若源代码不可访问，降低置信度并说明。

**Q: `confidence` 如何决定？**
A: 90–100 = 源代码直接证明结论；70–89 = 证据充分但有小缺口；低于 70 = 证据部分或模糊。绝不编造置信度——用收集到的证据证明。
