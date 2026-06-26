---
name: openclaw-version-bug-hunter
slug: openclaw-version-bug-hunter
version: 2.1.1
description: Query version-specific GitHub bug reports with quality assessment markers; agent combines output with user config for contextual upgrade evaluation.
---

# OpenClaw Version Bug Hunter

**作者**: Initiated by Neo Shi and executed by 银月  
**许可证**: MIT

---

## 👋 使用教程（人类友好）

**你不需要记任何命令，直接用自然语言和你的 Agent 说话就行。**

安装技能后，直接对你的 Agent 说：

| 你想说的 | Agent 会做的 |
|----------|-------------|
| "帮我看看 2026.5.6 有没有什么 bug" | 自动跑脚本，输出分类报告 |
| "获取最新版本的稳定性报告" | 先查当前版本，再跑报告 |
| "升级前帮我查下 2026.5.7 的坑" | 跑报告 + 结合你的配置做升级评估 |
| "2026.5.6 和 2026.5.5 哪个更稳？" | 对比两个版本的 bug 报告 |

**就这么简单。** 不需要记脚本路径，不需要拼命令行，Agent 会搞定一切。

**前置要求**：GitHub CLI (`gh`) 必须已安装并认证。检查方法：
```bash
gh --version && gh auth status
```

---

## 🚀 命令行快速开始

如果你想直接调用脚本：

```bash
# 查询特定版本的 bug 报告
~/.openclaw/workspace/skills/openclaw-version-bug-hunter/scripts/bug-hunt.sh 2026.4.9
```

## 功能

此技能封装了 GitHub CLI (`gh`)，自动搜索并分类 OpenClaw 官方仓库中与特定版本相关的 issue 报告。

**设计原则：脚本提供数据，Agent 做 contextual 评估。** 脚本不做简单的阈值判断（因为 OpenClaw 永远有 actionable issue），Agent 应结合主人的实际配置（渠道/插件/运行时/Node版本/部署方式）判断哪些 bug 真正影响当前环境。

### 输出内容

1. **🔴 Critical / 严重问题** - 导致崩溃、数据丢失、系统不稳定的 bug
2. **🟠 Regression / 回归问题** - 之前版本正常，当前版本失效的功能
3. **🟡 General Bugs / 一般问题** - 其他 bug 报告
4. **📋 质量评估** - 每个 issue 的可行动性/重复/模糊度自动标记
5. **📊 统计信息** - 未解决/已解决 issues 数量 + 质量分布
6. **✅ 修复状态** - 已合并的修复 PR 列表

### 质量评估标记（内置，零 LLM 依赖）

| 标记 | 含义 | 判定逻辑 |
|------|------|----------|
| ✅ actionable | 有足够信息可调查 | 复现步骤 + 错误信息 + 环境/代码引用 ≥ 4 分 |
| ⚡ partial | 部分信息 | 有错误消息但缺少复现步骤，2-3 分 |
| ❓ needs info | 缺少关键信息 | 无复现步骤、无错误堆栈、无环境信息 |
| ⚠️ vague | 描述过于模糊 | 正文 < 50 字或缺乏技术关键词 |
| 🔁 dup of #N | 疑似重复 | 标题与同批次 issue 高度相似 |

### 严重程度判定规则

详细规则见 `references/severity-rules.md`（按需加载）。

**快速参考**：
- **Critical**: 崩溃、数据丢失、安全漏洞、无限循环
- **Regression**: 标记为 `regression` 标签的 issue
- **General**: 标记为 `bug` 但非 critical/regression

## 使用场景

### 升级前避坑

```bash
# 在升级到 v2026.4.9 之前
bug-hunt.sh 2026.4.9
```

输出示例：
```
### 🔴 Critical / 严重问题
- #64745: macOS 2026.4.8 app causes infinite self-replication... [✅ actionable]
- #64812: Same replication loop issue... [🔁 dup of #64745]
- #65003: It crashes lol [⚠️ vague]

### 🟠 Regression / 回归问题
- #64552: Severe Performance Regression - 30-60 Second Delay... [✅ actionable]
- #64636: Version 2026.4.9 ignore the system environment proxy... [⚡ partial]

### 📋 质量评估
- 总 issue 数: 25
- ✅ actionable: 8
- ⚡ partial: 5
- ❓ needs info: 7
- ⚠️ vague: 3
- 🔁 duplicate: 2

### 📊 统计信息
- 未解决 issues: 25
- 已解决 issues: 8

---
💡 升级评估：请结合你的实际配置（渠道/插件/运行时/Node版本/部署方式）
```

### 比较两个版本

```bash
# 比较 v2026.4.8 和 v2026.4.9
bug-hunt.sh 2026.4.8
bug-hunt.sh 2026.4.9
```

### 检查当前版本的已知问题

```bash
# 先用 openclaw status 查看当前版本
openclaw status | grep "app"

# 然后查询该版本的 bug
bug-hunt.sh 2026.4.8
```

## 依赖

- **GitHub CLI** (`gh`) - 必须已安装并认证
- **Bash** - 脚本运行环境

### 检查依赖

```bash
# 检查 gh 是否安装
gh --version

# 检查是否已认证
gh auth status
```

## 输出解读

脚本只提供**结构化数据**，不做简单的阈值判断。OpenClaw 是活跃项目，永远有 actionable issue，关键是**哪些影响你的实际配置**。

### Agent 评估指南

当主人要求升级评估时，Agent 应结合以下维度做 contextual 判断：

| 配置维度 | 排查方向 |
|---|---|
| 使用的渠道 | 只关注对应渠道的 bug（飞书/Discord/微信等） |
| 启用的插件 | 关注相关插件的 bug（active-memory、codex 等） |
| 运行时 | Pi/Codex embedded — 关注对应 runtime 的 regression |
| Node 版本 | 关注特定 Node 版本的兼容性问题 |
| 部署方式 | 本机/容器 — 忽略无关部署的问题 |
| 当前版本 | 判断是否有新 regression 需要热修复 |

**评估结论格式**：
```
🟢 可以升级 — 与你的配置相关的 actionable issue 为 0
🟡 谨慎升级 — 发现 X 个影响你配置的问题：
   - #N: 简述（影响你的 Y 功能）
🔴 暂缓升级 — 发现 Critical regression 影响核心功能：
   - #N: 简述
```

## 高级用法

### 搜索特定标签

```bash
# 只搜索 regression
gh issue list --repo openclaw/openclaw --label regression --search "2026.4.9"

# 只搜索 Critical
gh issue list --repo openclaw/openclaw --label Critical --search "2026.4.9"
```

### 查看 issue 详情

```bash
gh issue view 64552 --comments
```

### 导出为 Markdown

```bash
bug-hunt.sh 2026.4.9 > bug-report-2026.4.9.md
```

## 限制

1. **需要 gh CLI 认证** - 未认证用户无法访问 GitHub API
2. **API 速率限制** - 未认证用户每小时 60 次请求，认证后 5000 次
3. **搜索精度** - 依赖 GitHub 搜索算法，可能遗漏未明确提及版本号的 issue

## 故障排查

### 问题：`gh: command not found`

**解决**：安装 GitHub CLI
```bash
# macOS
brew install gh

# 验证
gh --version
```

### 问题：`gh: not authenticated`

**解决**：认证 GitHub
```bash
gh auth login
```

### 问题：搜索结果太少

**原因**：issue 标题/正文未明确提及版本号

**解决**：手动搜索关键词
```bash
gh issue list --repo openclaw/openclaw --label bug --search "v2026.4.9 OR 2026.4.9 OR 2026.4.8"
```

## 相关文件

- `scripts/bug-hunt.sh` - 核心搜索脚本
- `references/severity-rules.md` - 严重程度判定规则（详细版）

## 发布渠道

- **ClawHub**: `clawhub install openclaw-version-bug-hunter`
- **GitHub**: https://github.com/Suidge/openclaw-version-bug-hunter

---

*银月注：此技能专为 OpenClaw 用户设计，帮助大家在升级前避开已知坑点～🌙*
