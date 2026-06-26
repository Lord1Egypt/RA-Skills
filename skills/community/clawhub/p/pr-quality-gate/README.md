# PR Quality Gate - PR 质量门禁工作流

## 业务场景

**痛点：** 团队代码 Review 依赖人工，效率低、易遗漏、问题追踪散落各处。合并前 Review 流于形式，导致线上 Bug、代码债务累积。

**场景：** 代码提交后到合并前，系统性检查 PR 质量维度，自动创建 Issue 追踪未解决问题，AI 辅助修复，最终给出合并建议。

## 痛点分析

| 痛点 | 影响 |
|------|------|
| Review 维度不统一 | 有人看逻辑，有人看风格，质量参差不齐 |
| 问题发现后无追踪 | PR 评论的问题随着时间被遗忘，无人跟进 |
| 高严重度问题被忽视 | 压力下 Medium/High 问题被直接合入 main |
| 重复问题反复出现 | 同样的问题在多个 PR 中出现，没有系统性解决 |

## Skill 编排图谱

```
用户发起 PR Review 请求
         │
         ▼
┌─────────────────────┐
│   code-review       │  ← 读取 PR diff + gh pr diff
│   结构化质量分析      │    输出多维度评分 + 问题列表
└────────┬────────────┘
         │
         ├─▶ 发现问题 ──▶ ┌──────────────────┐
         │                │  github-issues    │
         │                │  创建 Issue + 关联 │
         │                │  PR + 设置标签     │
         │                └──────────────────┘
         │
         ▼
┌─────────────────────┐
│ 高严重度(High)问题?  │
└────────┬────────────┘
      Yes│                 ┌──────────────────┐
         ├───▶ 触发 ──────▶│  kimi-cli        │
         │                │  AI 修复建议生成   │
         │                └──────────────────┘
         │                      │
      No │◀────────────────────┘
         │
         ▼
┌─────────────────────┐
│  github             │
│  输出 Review 报告    │  ──▶ gh pr comment / status
│  给出合并建议        │
└─────────────────────┘
```

## 协作的 Skill

| Skill | 职责 |
|-------|------|
| **code-review** | 核心结构化代码审查，多维度评分，问题定位 |
| **github-issues** | 自动创建 Issue，自动关联 PR，设置标签/负责人 |
| **kimi-cli** | High 严重度问题触发 AI 修复建议（通过 PTY 交互） |
| **github** | PR 状态更新、评论、最终合并决策 |

## 使用示例

### 场景 1：Review 指定 PR

```
用户：帮我 review github.com/cli/cli/pull/8723

系统激活 pr-quality-gate：
1. code-review 拉取 PR diff，分析 5 个质量维度
2. 发现 3 个问题：1 High + 2 Medium
3. github-issues 为每个问题创建 Issue 并关联 PR
4. High 问题触发 kimi-cli 生成修复代码
5. 输出完整 Review 报告 + 关联 Issue 链接
```

### 场景 2：PR 质量 Gate 检查

```
用户：这个 PR 可以合并吗？

系统：
1. code-review 再次执行快速复检
2. 检查关联 Issue 是否全部 Close
3. 输出 Gate 状态：
   ✅ Gate Passed — 所有 High 问题已解决，可合并
   ⚠️ Gate Blocked — Issue #124 未关闭，阻止合并
```

### 场景 3：批量检查未解决问题

```
用户：检查一下这个仓库所有 open 的 PR 有哪些阻塞问题

系统：
1. github 列出所有 open PR
2. 逐个执行 code-review 快速扫描
3. github-issues 检查关联 Issue 状态
4. 汇总输出：《PR 质量阻塞报告》
```