# PR Review Factory（自动化 Code Review 工厂）

> GitHub PR 提交后，自动完成审查 → Issue跟踪 → 修复验证 → 合并的一站式质量门禁。

---

## 业务场景

软件开发团队中，Code Review 是保障代码质量的关键环节，但传统方式存在以下问题：

- **PR 积压**：人工审查速度慢，开发者等待时间长
- **标准不一**：不同审查者维度不同，反馈质量参差不齐
- **问题丢失**：审查意见散落在 PR 评论中，容易遗漏
- **修复无闭环**：问题提出后无人跟踪，PR 最后还是被"将就"合并
- **合并风险**：没有质量门禁，带 Bug 的代码进入主线

**PR Review Factory** 将整个流程自动化，确保每个 PR 都经过严格审查，且每个问题都有明确的责任人和闭环。

---

## 痛点分析

| 痛点 | 影响 | 解决方案 |
|------|------|---------|
| PR 堆积，审查慢 | 开发周期拉长 | 并行5维度自动审查，秒级启动 |
| 审查标准主观 | 质量不稳定 | 结构化审查框架，Blocking/Suggestion 明确分级 |
| 问题散落无跟踪 | Bug被遗忘 | 审查问题 → GitHub Issue，责任分派，状态驱动 |
| 修复验证靠人工 | 合并风险高 | CI 质量门禁，自动合并通过审查的 PR |
| 缺乏审查历史 | 团队无法复盘 | 审查报告自动归档，质量趋势可见 |

---

## Skill 编排图谱

```
                    ┌─────────────────────────┐
                    │     GitHub PR 创建      │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────┐
                    │  Step 1: 结构化审查     │
                    │  🔍 code-review-skill   │
                    │  • 5个并行Agent独立审查  │
                    │  • 维度：正确性/安全/     │
                    │         可读/性能/可维护 │
                    │  • 输出：Approve /       │
                    │         Request Changes │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────┐
                    │  Step 2: Issue跟踪       │
                    │  📋 github-issues-skill │
                    │  • Blocking → Issue     │
                    │    分派给PR作者          │
                    │  • Suggestion → PR评论   │
                    │  • 设置Milestone跟踪     │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────┐
                    │  Step 3: CI验证工作流   │
                    │  ⚙️ github-actions-     │
                    │     templates           │
                    │  • lint + test + build  │
                    │  • 质量门禁检查          │
                    │  • Issue全部关闭触发合并 │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────┐
                    │  Step 4: 合并与报告     │
                    │  ✅ 质量门禁通过         │
                    │  📊 审查摘要归档          │
                    └─────────────────────────┘
```

---

## 核心 Skill 详解

### 1. code-review-skill（审查引擎）

负责核心 Code Review 工作，5个并行 Agent 分别审查：

| Agent | 职责 | 严重级别 |
|-------|------|---------|
| Agent #1 | CLAUDE.md 规范合规性 | 🟡 Suggestion |
| Agent #2 | 明显 Bug 扫描 | 🔴 Blocking |
| Agent #3 | Git 历史上下文分析 | 🟡 Suggestion |
| Agent #4 | 安全漏洞检测 | 🔴 Blocking |
| Agent #5 | 测试覆盖评估 | 🟡 Suggestion |

输出格式：
```json
{
  "verdict": "Request Changes",
  "blocking_issues": 3,
  "suggestions": 7,
  "summary": "..."
}
```

### 2. github-issues-skill（问题跟踪）

将审查结果转化为可执行的问题跟踪：

- **创建 Issue**：每个 Blocking 问题创建独立 Issue
- **自动分派**：Issue 自动分派给 PR 作者
- **关联 PR**：Issue 关联源 PR，方便追溯
- **状态驱动**：修复后 Issue 状态变更，PR 质量门禁动态更新

### 3. github-actions-templates（自动化 CI）

生成并部署 PR 质量门禁工作流：

```yaml
# 典型工作流
trigger:
  - pull_request
jobs:
  lint:
    - run: eslint .
  test:
    - run: pytest .
  build:
    - run: docker build .
  quality_gate:
    - check: all blocking issues resolved?
    - block_merge: false
```

---

## 使用示例

### 示例 1：审查 PR 并创建 Issue

```
用户：帮我审查 denoland/deno#23456

执行流程：
1. code-review-skill 拉取 PR 变更
2. 5个并行Agent审查，发现：
   - 🔴 Blocking: 内存泄漏（lines 45-52）
   - 🔴 Blocking: SQL注入风险（line 128）
   - 🟡 Suggestion: 变量命名不规范（3处）
3. github-issues-skill 创建2个Issue并分派给PR作者
4. github-actions-templates 启动CI验证工作流
5. 输出审查报告，等待Issue关闭后触发合并
```

### 示例 2：为仓库配置质量门禁

```
用户：给我的仓库配置PR质量门禁

执行：
1. 读取仓库的 branch protection 设置
2. 生成 GitHub Actions 工作流（lint/test/build）
3. 配置 PR 审查自动化触发器
4. 设置必须所有 Blocking Issue 关闭才能合并
5. 配置审查报告自动生成（Markdown格式）
```

### 示例 3：查询 PR 审查状态

```
用户：这个PR的审查进展如何？

执行：
1. 查询 PR 当前审查状态
2. 查询关联的 Issue 列表及状态
3. 查询 CI 工作流状态
4. 返回汇总：3个Blocking问题，已关闭1个，还有2个待修复
```

---

## 质量评级标准

| 评级 | 条件 | 可合并？ |
|------|------|---------|
| ✅ Approve | 无 Blocking 问题 | 是 |
| 🟡 Request Changes | 有 Blocking 但可修复 | 否（需修复后重新审查） |
| ❌ Reject | 安全问题或架构性问题 | 否（需大改后重新提PR） |

---

## 环境要求

- GitHub Token（需 repo 权限，用于读写 Issue 和 PR 评论）
- 仓库需启用 GitHub Actions（用于 CI 质量门禁）
- 推荐配置 Branch Protection（强制审查通过后才可合并）

---

## 适用团队

- **中大型开发团队**：多人协作，PR 量多，人工审查跟不上
- **开源项目维护者**：需要标准化审查流程，减轻维护负担
- **追求高质量的初创团队**：想在快速迭代中保持代码质量
- **Code Review 文化成熟的团队**：想将人工审查经验固化为自动化流程