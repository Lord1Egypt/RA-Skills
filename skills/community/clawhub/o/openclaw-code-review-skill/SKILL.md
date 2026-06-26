---
name: Code Review
description: 对 Pull Request 或代码 Diff 进行结构化审查，使用多 Agent 并行审查 + 置信度评分过滤误报。触发：/code-review、审查 PR、代码审查
---

# Code Review Skill

对 Pull Request 进行结构化代码审查，模拟 Claude Code `/code-review` 插件的工作流。多 Agent 并行从不同角度审查，置信度 ≥80 的问题才输出，过滤误报。

## 适用场景

- PR 合并前需要审查
- 本地 Diff 需要评审
- 审查自己写完的代码
- Code Review 流程规范建立

---

## 工作流程（7步）

### 第1步：确认审查对象

**优先级顺序：**
1. 如果用户提供了 PR 链接 → 直接使用
2. 如果用户在代码仓库中 → 用 `gh pr list --author @me --state open` 查找自己开的 PR
3. 如果用户提供了 Diff 内容 → 直接审查 Diff
4. 其他情况 → 询问用户提供

**跳过检查**（发现以下情况直接终止）：
- PR 已关闭 → 跳过
- PR 是 Draft → 跳过
- PR 是自动化创建的trivial变更 → 跳过
- Claude 已经审查过此 PR → 跳过（检查 `gh pr view <PR> --comments`）

> 注意：Claude 生成的 PR 仍需审查

---

### 第2步：收集上下文

并行执行：

**A. 获取 PR 详情**
```bash
gh pr view <PR> --json title,body,files,additions,deletions,changedFiles,author,createdAt
```

**B. 查找仓库中的 CLAUDE.md**
```bash
# 根目录
gh api repos/:owner/:repo/contents/CLAUDE.md --jq '.content' 2>/dev/null

# 子目录（与变更文件同目录的）
# 用变更文件路径推断需要的 CLAUDE.md
```

**C. 获取变更文件列表**
```bash
gh pr diff <PR>
```

---

### 第3步：总结 PR 变更

用一句话总结：
- 这个 PR 改了什么（功能/修复/重构）
- 涉及多少文件、+多少行/-多少行
- 作者的目的是什么（从 PR 描述推断）

格式：
```
📋 PR 概览
- 标题：xxx
- 作者：xxx
- 变更范围：x 个文件，+x 行/-x 行
- 摘要：xxx
```

---

### 第4步：启动并行审查（3个 Agent）

使用 `sessions_spawn` 工具并行启动 3 个独立审查 Agent：

#### Agent 1：CLAUDE.md 合规检查（Sonnet）
**Prompt：**
```
你是代码审查专家，负责检查此 PR 是否违反了项目 CLAUDE.md 中的规范。

背景：
- PR 标题：<title>
- PR 描述：<description>
- 项目规范在 CLAUDE.md 中列出

任务：
1. 阅读 PR 变更的文件内容和 CLAUDE.md 规范
2. 检查变更是否违反了 CLAUDE.md 中的任何明确规则
3. 只标记**明确违反**的规则（你能引用 CLAUDE.md 中的具体文字）

置信度评分（0-100）：
- 0：误报，规范未要求
- 25：可能是问题，但不确定
- 50：确实违反，但影响较小
- 75：明确违反，影响较大
- 100：完全确定，直接影响功能

只报告置信度 ≥75 的问题。

输出格式：
问题列表，每条包含：
- 置信度
- 违反的规则（引用原文）
- 违反的文件和行号
- 简要说明
```

#### Agent 2：Bug 和逻辑错误检查（Opus）
**Prompt：**
```
你是资深代码审查专家，负责在此 PR 变更中发现明显的 Bug 和逻辑错误。

背景：
- PR 标题：<title>
- PR 描述：<description>

任务：
只检查 Diff 本身，不要引入 Diff 之外的上下文。

**标记标准（高信号问题）：**
- 会导致编译失败或运行时 panic 的错误（类型错误、缺少 import、引用错误）
- 无论输入如何都会产生错误结果的逻辑错误
- 安全隐患（注入、泄露、硬编码凭证）

**不标记：**
- 代码风格问题
- 依赖特定输入才能触发的问题
- 主观改进建议
- Linter 会捕获的问题
- PR 之前就存在的问题

置信度评分（0-100）：
只报告置信度 ≥80 的问题。

输出格式：
问题列表，每条包含：
- 置信度
- 问题类型（bug/security/logic）
- 文件和行号
- 简要说明
- 预期行为 vs 实际行为
```

#### Agent 3：Git 历史上下文分析（Sonnet）
**Prompt：**
```
你是代码审查专家，负责通过 Git 历史为此 PR 提供上下文。

背景：
- PR 标题：<title>
- PR 描述：<description>
- 变更的文件：<files>

任务：
1. 对变更的关键文件运行 `git blame` 和 `git log`
2. 检查：
   - 是否有文件最近被大规模重构过，这次 PR 是否与之冲突
   - 变更是否绕过了已有的测试或保护措施
   - 是否有相关的历史 issue 或 PR 上下文
3. 提供有价值的上下文，帮助理解此次变更的风险

只报告高置信度（≥75）的风险点。

输出格式：
风险点列表，每条包含：
- 置信度
- 历史上下文
- 潜在风险
- 相关文件
```

---

### 第5步：置信度验证

对 Agent 2（Bug检查）发现的每个问题，启动一个子 Agent 验证：
- 重新阅读相关代码
- 确认问题确实存在
- 排除误报

**过滤掉置信度 <80 的问题。**

---

### 第6步：输出审查结果

**Chat 输出格式：**

```
## 🔍 Code Review

**PR**：<title>
**作者**：<author>
**变更**：<x> 个文件，+<x> 行 / -<x> 行

---

### 发现的问题（按严重程度排序）

#### 🔴 高风险（需修复）
1. **[Bug]** <问题描述>
   - 文件：`src/foo.ts`
   - 位置：第 23-27 行
   - 原因：<简要说明>
   - 置信度：92

#### 🟡 中风险（建议处理）
...

---

### ✅ 通过检查
- CLAUDE.md 合规性：通过
- 安全性：未见明显漏洞
- 测试覆盖：变更区域有测试

---

### 📝 总体评价
<一句话总结>

---
审查完成。如需将此审查发布为 GitHub PR 评论，请说「发布评论」。
```

---

### 第7步：（可选）发布 GitHub PR 评论

如果用户说「发布评论」：

**使用 `gh pr comment`：**
```bash
gh pr comment <PR> --body "## 🔍 Code Review

发现 <N> 个问题..."

# 如需逐行评论用：
gh pr comment <PR> --body "**文件：src/foo.ts#L23-27**
<Brief issue description>"
```

---

## 误报过滤器（内置，不报告以下情况）

- PR 之前就存在的问题
- 看起来是 Bug 但实际是正确的代码
- 吹毛求疵的 nitpick
- Linter 会自动捕获的问题
- 笼统的代码质量问题（除非 CLAUDE.md 明确要求）
- 通过 lint ignore 注释显式忽略的问题

---

## 命令

| 输入 | 行为 |
|------|------|
| `/code-review <PR-URL>` | 审查指定 PR |
| `/code-review --comment` | 审查 + 发布 GitHub 评论 |
| `/code-review` | 在当前仓库查找自己最新的 Open PR |
| `帮我 review 这个 diff` | 审查提供的 Diff 内容 |

---

## 注意事项

- **先问清楚再动手**：如果 PR 信息不足（缺少描述、变更范围不明确），先问用户
- **只报告高置信度问题**：宁可漏报，不要误报
- **引用具体规则**：CLAUDE.md 问题必须引用原文
- **GitHub CLI 优先**：用 `gh` 而非 Web Fetch
- **链接格式**：GitHub 链接必须用完整 SHA：`https://github.com/owner/repo/blob/<full-sha>/path#Ln`
