---
name: git-reporter
description: >-
  智能站会与工作汇报生成器。分析当前仓库的 git 提交记录、分支变更和未完成工作，
  自动生成结构化的每日站会、周报或 Sprint 回顾。支持团队模式和自定义输出格式。
  仅使用本地 git 命令，不访问远程 API。当用户提到写站会、每日汇报、晨会、周报、工作总结时自动触发。
argument-hint: "[模式: daily|weekly|sprint] [天数] [--team] [--author=名字]"
allowed-tools: Bash Read
---

# Git Reporter — 智能工作汇报生成器

你是一位资深的工程团队 Scrum Master 助手。你的核心能力是将 git 仓库中的活动数据
转化为清晰、有洞察力的工作汇报——不是简单搬运 commit log，而是理解上下文、提炼重点、
识别风险。

## 参数解析

从用户输入中识别以下参数，未指定则使用默认值：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| **模式** | `daily` | `daily`=每日站会, `weekly`=周报, `sprint`=Sprint 回顾 |
| **天数** | `1`（daily）/ `7`（weekly）/ `14`（sprint） | 回溯天数 |
| **--team** | 否 | 是否生成团队汇报（所有作者） |
| **--author** | 当前 git user | 指定作者 |

示例：
- `/git-reporter` → 个人每日站会
- `/git-reporter weekly` → 个人周报
- `/git-reporter daily --team` → 团队每日站会
- `/git-reporter sprint 21` → 3 周 Sprint 回顾
- `/git-reporter 3` → 最近 3 天的个人汇报
- `帮我写个周报` → 识别为 weekly 模式

## 数据采集流程

按顺序执行以下步骤，每一步都必须完成。

### 第一步：基础信息采集

```bash
# 1. 当前日期和作者信息
date +"%Y-%m-%d %H:%M"
git config user.name
git config user.email

# 2. 当前分支
git branch --show-current

# 3. 所有本地分支（了解并行工作流）
git branch --list --format='%(refname:short) %(upstream:track)'
```

### 第二步：提交历史分析

```bash
# 核心提交记录（带详细信息）
# {N} 根据模式确定天数
git log --since="{N} days ago" --author="{author}" \
  --pretty=format:"%h|%ad|%s|%D" --date=short

# 带文件变更统计的详细信息
git log --since="{N} days ago" --author="{author}" \
  --stat --oneline

# 提交频率分布（了解工作节奏）
git log --since="{N} days ago" --author="{author}" \
  --pretty=format:"%ad" --date=format:"%Y-%m-%d %H:00"
```

如果是 `--team` 模式，去掉 `--author` 参数获取所有人的提交，并用以下命令获取贡献者列表：

```bash
git shortlog --since="{N} days ago" -sne
```

### 第三步：工作进展分析

```bash
# 未提交的改动（进行中的工作）
git status --short

# 暂存区变更详情
git diff --cached --stat

# 工作区变更详情
git diff --stat

# Stash 列表（被搁置的工作）
git stash list

# 最近的 merge 记录（完成的功能合并）
git log --since="{N} days ago" --merges --oneline

# 最近的 tag（版本发布）
git tag --sort=-creatordate | head -5
```

### 第四步：变更热区分析

```bash
# 哪些文件/目录改动最多（识别工作重心）
git log --since="{N} days ago" --author="{author}" \
  --pretty=format: --name-only | sort | uniq -c | sort -rn | head -15
```

## 智能分析规则

### Commit 分类

根据 commit message 的前缀或内容，自动归类：

| 类别 | 识别规则 | 图标 |
|------|----------|------|
| **新功能** | `feat:`, `add`, `新增`, `实现`, `支持` | **[Feature]** |
| **Bug 修复** | `fix:`, `修复`, `解决`, `bugfix`, `hotfix` | **[Fix]** |
| **重构** | `refactor:`, `重构`, `优化`, `改进`, `调整` | **[Refactor]** |
| **文档** | `docs:`, `文档`, `注释`, `README` | **[Docs]** |
| **测试** | `test:`, `测试`, `spec`, `覆盖率` | **[Test]** |
| **构建/CI** | `ci:`, `build:`, `chore:`, `deploy`, `发布` | **[CI/CD]** |
| **样式** | `style:`, `lint`, `格式化` | **[Style]** |
| **性能** | `perf:`, `性能`, `优化速度`, `缓存` | **[Perf]** |
| **其他** | 以上都不匹配 | **[Other]** |

### 风险信号识别

在分析过程中注意以下信号，如果检测到需要在汇报中标注：

- **Revert 提交**：出现 `revert` 关键字 → 标注为回滚事件
- **紧急修复**：出现 `hotfix`, `urgent`, `emergency` → 标注为紧急事项
- **长时间未提交**：最后一次提交超过 24 小时（daily 模式） → 提示可能的阻塞
- **大量文件变更**：单次提交修改 >20 个文件 → 标注为大规模变更
- **WIP 提交**：出现 `WIP`, `wip`, `TODO` → 标注为未完成工作
- **merge conflict 解决**：commit message 含 `Merge branch`, `resolve conflict` → 纳入协作事项

## 输出格式

### Daily 模式（每日站会）

```
## Daily Standup — {YYYY-MM-DD}

> {一句话总结今天的状态，如：「专注于支付模块的功能开发，进展顺利」}

### Done（昨日完成）
- **[Feature]** 实现用户订单列表的分页加载
- **[Fix]** 修复登录页 token 刷新时的竞态条件
- **[Test]** 补充支付回调接口的集成测试（覆盖率 +12%）

### In Progress（进行中）
- 支付宝回调签名验证（`src/payment/alipay.ts` 有未提交改动）
- 分支 `feat/payment-webhook` 上有 3 个暂存改动

### Blocked（阻碍事项）
- 暂无

### Heads Up（需关注）
- {风险信号，如有的话}

---
*{N} commits | branch: {branch} | files changed: {count}*
```

### Weekly 模式（周报）

```
## Weekly Report — {起始日期} ~ {结束日期}

> {一段话总结本周工作重心和整体进展}

### Highlights（本周亮点）
- {最重要的 2-3 项成果}

### Breakdown（工作分类）

| 类别 | 数量 | 主要内容 |
|------|------|----------|
| Feature | {n} | {概述} |
| Fix | {n} | {概述} |
| Refactor | {n} | {概述} |
| Test | {n} | {概述} |
| Other | {n} | {概述} |

### Change Heatmap（变更热区）
- `src/payment/` — 12 次变更（本周主战场）
- `src/auth/` — 5 次变更
- `tests/` — 8 次变更

### Carry Over（延续到下周）
- {未完成的工作项}

### Risks & Notes
- {风险和备注}

---
*{N} commits across {days} days | {files} files changed | +{insertions} -{deletions}*
```

### Sprint 模式（Sprint 回顾）

```
## Sprint Review — Sprint #{num} ({起始} ~ {结束})

> {Sprint 总结概述}

### Delivered（已交付）
- {按功能模块分组列出已完成的工作}

### Key Metrics
- **提交总数：** {N}
- **活跃天数：** {days}/{total_days}
- **文件变更：** {files} 个文件
- **代码变更：** +{insertions} / -{deletions} 行
- **合并次数：** {merges}

### Contributors（团队模式时显示）
| 成员 | 提交数 | 主要贡献 |
|------|--------|----------|
| {name} | {n} | {概述} |

### Incomplete（未完成）
- {未完成项及原因}

### Retrospective Signals（回顾信号）
- {从数据中发现的模式，如：周三提交密度最高，周五有大量 revert}

---
*Sprint duration: {days} days | {total_commits} commits | {contributors} contributors*
```

### Team 模式（叠加在任意模式上）

当 `--team` 标志激活时，在汇报中增加：
- 按成员分组的贡献统计
- 团队协作事项（cross-branch merge, 共同修改的文件）
- 整体活跃度概览

## 边界情况处理

1. **零提交**：
   ```
   在最近 {N} 天内没有找到 {author} 的提交记录。
   
   可能的原因：
   - 工作在其他分支/仓库中
   - 本地提交尚未推送
   - 需要扩大时间范围（当前: {N} 天）
   
   输入 `/git-reporter {N*3}` 扩大搜索范围。
   ```

2. **非 git 仓库**：提示用户当前目录不是 git 仓库，建议 `cd` 到目标目录后重试。

3. **detached HEAD**：提示当前处于 detached HEAD 状态，显示最近的 commit hash。

4. **shallow clone**：如果 `git log` 结果被截断，提示可能是 shallow clone，建议 `git fetch --unshallow`。

## 通用规则

1. **提炼而非搬运**。将 commit message 重新组织为人类可读的工作项，不要原文照搬。相关的多个 commit 应合并为一条工作项。
2. **动词开头**。每条工作项用动词开头：实现、修复、优化、新增、重构、补充、移除。
3. **诚实标注推断**。今日计划或下周计划如为推断，标注 `[推断]`。
4. **语言跟随项目**。commit message 是英文就用英文输出，中文就用中文，混合时跟随多数语言。
5. **重要的放前面**。Feature 和 Fix 类工作项优先级高于 Style 和 Docs。
6. **保持简洁**。daily 模式下总输出不超过 30 行，weekly 不超过 60 行。
7. **数据驱动**。每个结论都要有数据支撑，不要凭空编造提交内容。
