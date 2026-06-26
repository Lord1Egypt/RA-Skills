---
name: github-pr-manager
description: GitHub PR 全流程管家。用于自动化管理 Pull Request 的整个生命周期：初始化跟踪、检查 CI 状态、处理 Review 意见、修复 DCO/代码问题、回复评论，直到 PR 合入 main。当用户需要持续跟进 PR 状态、处理 reviewer 反馈、自动化 GitHub 操作时触发此 skill。
---

# GitHub PR 全流程管家

这个 skill 让你可以像有一个专职 PR 助理一样，自动处理从提交到合入的所有事务。

## 核心能力

### 1. PR 初始化与跟踪

当用户提交新 PR 或要求跟踪已有 PR 时：

```
步骤：
1. 确认仓库名和 PR 号
2. 使用 gh CLI 或浏览器获取 PR 当前状态
3. 创建 memory/pr-tracking.md 记录初始状态
4. 设置 cron 定时检查（默认每 2 小时）
5. 告知用户当前状态和阻塞项
```

### 2. CI 状态监控

自动检查并报告：
- DCO 签名状态
- GitHub Actions 检查
- 测试覆盖
- 代码质量检查

**DCO 失败自动修复**：
```bash
cd <repo-path>
git commit --amend --signoff --no-edit
git push --force-with-lease origin <branch>
```

### 3. Review 意见处理

当检测到新的 review 时：

```
步骤：
1. 使用 gh api 获取所有 review 评论
2. 分类整理：必须修复 / 建议修改 / 讨论
3. 对每个必须修复项：
   - 如果是代码问题 → 定位并修复
   - 如果是流程问题 → 执行（如回复 issue、assign 等）
   - 如果是问题讨论 → 准备回复
4. 提交修复并回复 reviewer
```

### 4. 评论自动回复

常见场景的自动回复模板：

| 场景 | 回复模板 |
|------|----------|
| 已修复问题 | "@reviewer Fixed in commit `<hash>`. Thanks for the review!" |
| 需要澄清 | "@reviewer Could you elaborate on ...? I want to make sure I understand correctly." |
| 已处理 issue assign | "@maintainer Done! I've replied to issue #XXX. Please assign it to me." |
| CI 已修复 | "DCO fixed and CI is now passing. Ready for another review!" |

### 5. 直到合入的完整跟踪

自动检测并通知：
- ✅ Review 通过
- ✅ 所有 CI 通过
- ✅ 冲突解决
- ✅ PR 合入 main
- ❌ Review 拒绝 / 需要重大修改

## 必要配置

### GitHub CLI 设置

确保 gh CLI 已安装并登录：
```bash
# Windows
winget install --id GitHub.cli

# 登录（使用用户的 token）
echo "<token>" | gh auth login --with-token
```

### Token 权限

需要以下权限的 GitHub Personal Access Token：
- `repo` - 访问仓库代码
- `workflow` - 访问 Actions
- `read:org` - 读取组织信息

## 工作流

### 场景 1：新 PR 提交后

```
用户：帮我提交这个 fix 到 vllm-omni
Agent：
  1. Fork 目标仓库（如需要）
  2. Clone 到 workspace
  3. 创建分支、提交代码
  4. Push 到用户 fork
  5. 创建 PR
  6. 设置跟踪任务
  7. 报告 PR 链接和初始状态
```

### 场景 2：Review 来了

```
Agent（cron 检查）：
  1. 发现新 review
  2. 分析 review 内容
  3. 判断是否需要代码修改
  4. 执行修复或准备回复
  5. 提交修复并回复 reviewer
  6. 通知用户处理结果
```

### 场景 3：直到合入

```
Agent（持续跟踪）：
  1. 每 2 小时检查 PR 状态
  2. 状态变化时立即通知用户
  3. 自动处理力所能及的问题
  4. 需要人工决策时请示用户
  5. PR 合入后发送庆祝消息
```

## 参考资料

- [references/workflow.md](references/workflow.md) - 完整工作流指南
- [references/templates.md](references/templates.md) - 常用回复模板

## 与用户的交互原则

1. **主动汇报关键节点** - Review 通过、CI 失败、PR 合入等
2. **请示后再执行重大操作** - 如大幅重构代码、关闭 PR 等
3. **保持记录** - 所有操作记录在 memory/pr-tracking.md
4. **安全优先** - Token 不存储在消息中，使用本地配置文件
