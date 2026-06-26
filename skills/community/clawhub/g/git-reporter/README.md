# Git Reporter

> 智能站会与工作汇报生成器 — 一个 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) Skill

分析当前仓库的 git 提交记录、分支状态和未完成工作，一键生成专业的站会汇报、周报或 Sprint 回顾。

不是简单搬运 `git log`，而是理解上下文、提炼重点、识别风险。

> **注意：** 本 Skill 仅使用本地 git 命令（`git log`、`git status`、`git diff` 等），不调用任何远程 API（如 GitHub/GitLab API），不需要网络访问或额外凭证。

## Features

- **三种汇报模式** — Daily 站会 / Weekly 周报 / Sprint 回顾，覆盖日常所有汇报场景
- **智能 Commit 分类** — 自动识别 feat / fix / refactor / test / docs 等类型并归类
- **变更热区分析** — 告诉你这段时间的代码改动集中在哪些模块
- **风险信号检测** — 自动标注 revert、hotfix、大规模变更、长时间未提交等异常
- **团队模式** — 基于本地仓库的提交记录，生成全团队的工作概览和贡献统计
- **多语言自适应** — 根据 commit message 语言自动切换输出语言

## Install

通过 ClawHub 安装：

```bash
claude install clawhub:maximum2974/git-reporter
```

或通过 GitHub 安装：

```bash
claude install github:maximum2974/git-reporter
```

## Quick Start

```bash
# 最简单的用法：生成今天的站会
/git-reporter

# 指定回溯天数
/git-reporter 3

# 生成周报
/git-reporter weekly

# Sprint 回顾（默认14天）
/git-reporter sprint

# 团队每日站会
/git-reporter daily --team

# 指定作者
/git-reporter --author=john
```

也支持自然语言触发：

```
帮我写今天的站会
生成一下本周的周报
整理一下这个 sprint 的工作
团队这周都做了什么？
```

## Usage

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| 模式 | `daily` / `weekly` / `sprint` | `daily` | 汇报模式 |
| 天数 | 数字 | 1 / 7 / 14（按模式） | 回溯天数 |
| `--team` | flag | 否 | 生成团队汇报（基于本地已有的提交记录） |
| `--author` | string | `git config user.name` | 指定作者 |

### 模式对比

| 特性 | Daily | Weekly | Sprint |
|------|-------|--------|--------|
| 默认天数 | 1 | 7 | 14 |
| 工作项详情 | 逐条列出 | 分类汇总 | 按模块分组 |
| 变更热区 | 不显示 | 显示 | 显示 |
| 贡献者统计 | 仅 team 模式 | 仅 team 模式 | 默认显示 |
| Key Metrics | 基础 | 中等 | 详细 |
| 回顾信号 | 不显示 | 不显示 | 显示 |

## Examples

### Daily Standup

```
## Daily Standup — 2026-04-04

> 专注于支付模块的核心开发，修复了一个关键的并发问题

### Done（昨日完成）
- **[Feature]** 实现用户订单列表的分页加载和无限滚动
- **[Fix]** 修复登录页 token 刷新时的竞态条件（影响约 2% 用户）
- **[Test]** 补充支付回调接口的集成测试（覆盖率 78% → 90%）

### In Progress（进行中）
- 支付宝回调签名验证（`src/payment/alipay.ts` 有未提交改动）
- 分支 `feat/payment-webhook` 上有 3 个暂存改动

### Blocked（阻碍事项）
- 暂无

---
*5 commits | branch: feat/payment-integration | files changed: 12*
```

### Weekly Report

```
## Weekly Report — 2026-03-28 ~ 2026-04-04

> 本周重心在支付系统集成，完成了微信/支付宝双通道对接，同时修复了 3 个线上问题

### Highlights（本周亮点）
- 完成微信支付和支付宝双通道的完整对接
- 修复了影响 2% 用户的 token 竞态条件
- 测试覆盖率从 65% 提升至 90%

### Breakdown（工作分类）

| 类别 | 数量 | 主要内容 |
|------|------|----------|
| Feature | 8 | 支付通道对接、订单分页 |
| Fix | 3 | token 竞态、金额精度、超时处理 |
| Refactor | 2 | 支付回调统一抽象层 |
| Test | 5 | 支付集成测试、E2E |
| Docs | 1 | API 文档更新 |

### Change Heatmap（变更热区）
- `src/payment/` — 23 次变更（本周主战场）
- `tests/payment/` — 15 次变更
- `src/auth/` — 5 次变更

### Carry Over（延续到下周）
- 支付对账系统的定时任务开发

---
*19 commits across 5 days | 34 files changed | +1,247 -389*
```

## How It Works

```
用户输入
  │
  ▼
┌──────────────────┐
│  参数解析         │ ← 识别模式、天数、作者
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  本地 Git 数据采集 │ ← git log / status / diff / stash / branch
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  智能分析         │ ← Commit 分类 / 热区分析 / 风险检测
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  汇报生成         │ ← 按模式选择模板，填充数据
└──────────────────┘
```

**分析维度：**

1. **Commit 分类** — 根据 message 前缀和关键字自动归类为 Feature / Fix / Refactor / Test / Docs / CI 等
2. **变更热区** — 统计文件修改频率，识别本周/本 Sprint 的工作重心
3. **风险信号** — 检测 revert、hotfix、WIP、大规模变更等需要关注的事项
4. **进度推断** — 结合未提交改动、分支名和 stash 推断当前进行中的工作

## Data & Privacy

本 Skill 运行时会读取以下本地 git 数据：

- `git config user.name` / `user.email`（当前用户信息）
- `git log`（提交历史和 commit message）
- `git status` / `git diff`（未提交的改动）
- `git stash list`（暂存的工作）
- `git branch`（本地分支列表）

**不会访问任何远程服务。** 所有数据处理在本地完成。如果你的仓库包含敏感信息（如 commit message 中有密钥），请注意这些信息会被 Skill 读取。

## Skill Structure

```
git-reporter/
├── SKILL.md          # Skill 定义（核心 prompt + 工作流 + 输出模板）
├── README.md         # 文档（你正在看的这个）
├── LICENSE           # MIT 许可证
└── examples/
    ├── daily.md      # Daily 模式示例输出
    ├── weekly.md     # Weekly 模式示例输出
    └── sprint.md     # Sprint 模式示例输出
```

## FAQ

**Q: 这个 Skill 会访问 GitHub / GitLab API 吗？**
A: 不会。它只使用本地 git 命令，不需要网络访问或 API token。如果需要 PR 状态等远程信息，请结合 `gh` CLI 工具单独查询。

**Q: 支持 monorepo 吗？**
A: 支持。它会分析当前目录下的 git 仓库，monorepo 中可以在子目录运行来聚焦特定模块。

**Q: 如果我在多个分支上工作呢？**
A: Skill 会读取所有本地分支信息，并在汇报中体现跨分支的工作。

**Q: commit message 写得很随意怎么办？**
A: Skill 会尽力从 message + 文件变更路径推断工作内容，但更规范的 commit message 会带来更好的汇报质量。

**Q: 团队模式需要什么权限？**
A: 只需要本地仓库有团队成员的提交记录（即已 pull/fetch），不需要额外权限。

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- Git 仓库（非 shallow clone 效果最佳）

## License

MIT
