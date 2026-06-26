# OpenClaw Version Bug Hunter

**OpenClaw 版本 Bug 猎人** — 升级前查询特定版本的已知 bug 和 regression，帮助避坑🔍

![License](https://img.shields.io/github/license/Suidge/openclaw-version-bug-hunter)
![Version](https://img.shields.io/badge/version-2.1.1-blue)

---

## 👋 给人类用户的使用教程

**你不需要记任何命令，直接用自然语言和你的 Agent 说话就行。**

### 第一步：安装技能

在你的 OpenClaw 工作区中安装：

```bash
# 通过 ClawHub 安装
clawhub install openclaw-version-bug-hunter

# 或手动克隆
git clone https://github.com/Suidge/openclaw-version-bug-hunter.git ~/.openclaw/workspace/skills/openclaw-version-bug-hunter
```

### 第二步：直接用

安装完成后，直接对你的 Agent 说：

| 你想说的 | Agent 会做的 |
|----------|-------------|
| "帮我看看 2026.5.6 有没有什么 bug" | 自动跑脚本，输出分类报告 |
| "获取最新版本的稳定性报告" | 先查当前版本，再跑报告 |
| "升级前帮我查下 2026.5.7 的坑" | 跑报告 + 结合你的配置做升级评估 |
| "2026.5.6 和 2026.5.5 哪个更稳？" | 对比两个版本的 bug 报告 |

**就这么简单。** 不需要记脚本路径，不需要拼命令行，Agent 会搞定一切。

### 前置要求

- **GitHub CLI** (`gh`) - 必须已安装并认证
- **Bash** - macOS/Linux 默认自带

```bash
# 检查 gh 是否就绪
gh --version && gh auth status
```

---

## 🌟 功能特性

- 🔍 **版本搜索** - 输入版本号，自动搜索 GitHub issues
- 📊 **分类展示** - 按严重程度分类（Critical / Regression / General）
- 📋 **质量评估** - 每个 issue 自动标记可行动性（✅ actionable / ⚡ partial / ❓ needs info / ⚠️ vague / 🔁 duplicate）
- 📈 **统计信息** - 未解决/已解决 issues 数量
- ✅ **修复状态** - 显示已合并的修复 PR
- 🎨 **彩色输出** - 清晰的视觉层次（TTY 终端）
- 🤖 **Agent 评估** - 脚本提供数据，Agent 结合你的实际配置做升级建议

### v2.1.0 新变化

- 内置质量评估系统（零 LLM 依赖，纯 jq 实现）
- 自动检测重复 issue
- 升级评估改为 Agent contextual 判断，不再使用简单阈值

---

## 📋 输出示例

```bash
$ bug-hunt.sh 2026.5.6

🔍 正在搜索 OpenClaw v2026.5.6 的 bug 报告...

### 🔴 Critical / 严重问题
  无

### 🟠 Regression / 回归问题
- #78962: Upgrade to 2026.5.6 Broke Cloudflare AI Gateway [✅ actionable]
- #78944: 2026.5.6version the running session of the cron job is incorrect [✅ actionable]
- #78601: Gateway liveness watchdog restarting the gateway [✅ actionable]

### 🟡 General Bugs / 一般问题
- #78826: Feishu: groupId incorrectly set to sender open_id [✅ actionable]
- #78949: Feishu Group Chat: Bot mentions receive no response [✅ actionable]
- #78999: 微信插件 fetch failed with Node.js 25.x [✅ actionable]

### 📋 质量评估
- 总 issue 数: 73
- ✅ actionable: 58
- ⚡ partial: 11
- ❓ needs info: 4
- ⚠️ vague: 0
- 🔁 duplicate: 0

### 📊 统计信息
- 未解决 issues: 73
- 已解决 issues: 31

### ✅ 修复状态
已合并的修复 PR: 3

---
💡 升级评估：请结合你的实际配置（渠道/插件/运行时/Node版本/部署方式）
```

---

## 🤖 Agent 评估指南

脚本只提供结构化数据，不做简单的阈值判断。OpenClaw 是活跃项目，永远有 actionable issue，关键是**哪些影响你的实际配置**。

当主人要求升级评估时，Agent 应结合以下维度做 contextual 判断：

| 配置维度 | 排查方向 |
|----------|---------|
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

---

## 🎯 使用场景

### 升级前避坑

直接告诉 Agent：
> "帮我查下 2026.5.7 有没有什么坑"

### 对比两个版本

> "2026.5.6 和 2026.5.5 哪个更稳定？"

### 检查当前版本

> "我当前版本有什么已知问题？"

### 批量监控

可以在 cron 中定期运行，或在心跳巡检中加入版本检查。

---

## 🔧 命令行直接调用

如果你想在终端中直接运行：

```bash
# 直接调用脚本
~/.openclaw/workspace/skills/openclaw-version-bug-hunter/scripts/bug-hunt.sh 2026.5.6

# 添加到 PATH 后可简写
bug-hunt.sh 2026.5.6
```

---

## 📁 项目结构

```
openclaw-version-bug-hunter/
├── README.md                           # 本文件
├── LICENSE                             # MIT 许可证
├── SKILL.md                            # OpenClaw 技能说明（Agent 读取）
├── scripts/
│   └── bug-hunt.sh                     # 核心搜索脚本（质量评估 + 去重）
└── references/
    └── severity-rules.md               # 严重程度判定规则
```

---

## 🛠️ 开发

```bash
# 克隆仓库
git clone https://github.com/Suidge/openclaw-version-bug-hunter.git
cd openclaw-version-bug-hunter

# 测试
chmod +x scripts/bug-hunt.sh
./scripts/bug-hunt.sh 2026.4.9
```

---

## 📄 许可证

MIT License

---

## 👥 作者

**Initiated by Neo Shi and executed by 银月**

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - 强大的 AI 代理框架
- [GitHub CLI](https://cli.github.com/) - 让 GitHub 操作更简单

---

*🌙 银月注：升级前查一查，避坑省心又省力～*
