# OpenClaw Code Review Skill

> 将 Claude Code 官方 `/code-review` 插件的工作流，移植为 OpenClaw 可用的 Skill。多个 Agent 并行审查 + 置信度评分过滤误报，让 Code Review 更高效。

---

## ✨ 功能特性

- **多 Agent 并行审查** — 3 个独立 Agent 从不同角度同时审查（CLAUDE.md 合规、Bug 检测、Git 历史）
- **置信度评分** — 每个问题 0-100 评分，只报告 ≥80 分的高置信度问题
- **自动过滤误报** — lint 问题、pre-existing 问题、吹毛求疵的 nitpick 全部过滤
- **GitHub 集成** — 支持 PR 链接直接审查，支持 `--comment` 发布审查结果为 PR 评论
- **本地 Diff 审查** — 没有 PR 也可以审查任意代码变更

---

## 📋 工作流程

```
第1步：确认审查对象       → PR链接 / 本地PR / Diff内容
第2步：收集上下文         → PR详情 + CLAUDE.md + 变更文件
第3步：总结PR变更         → 一句话概括变更范围
第4步：并行3路审查         → 合规 + Bug + 历史
第5步：置信度验证         → 排除 <80 分的误报
第6步：输出结构化报告     → 🔴高风险 / 🟡中风险 / ✅通过
第7步：（可选）发布评论    → gh pr comment
```

---

## 🚀 快速开始

### 前置要求

- OpenClaw 已安装运行
- GitHub CLI (`gh`) 已安装并登录

```bash
# 登录 GitHub CLI（如未登录）
gh auth login
```

### 安装

将 `code-review/` 目录复制到 OpenClaw 的 skills 目录：

```bash
cp -r code-review ~/.openclaw/workspace/skills/
```

### 使用

在 OpenClaw 对话中直接说：

```bash
# 审查指定 PR
/code-review https://github.com/owner/repo/pull/123

# 审查 + 发布 GitHub PR 评论
/code-review https://github.com/owner/repo/pull/123 --comment

# 在当前仓库查找自己最新的 Open PR 并审查
/code-review
```

---

## 📖 详细用法

### 方式一：直接粘贴 PR 链接

```
/code-review https://github.com/owner/repo/pull/123
```

### 方式二：描述需求

```
帮我 review 这个 PR：
https://github.com/owner/repo/pull/123

审查完成后发布评论。
```

### 方式三：本地 Diff

如果你有本地 Diff 内容，直接粘贴并说：

```
帮我 review 以下 Diff：
<粘贴 diff 内容>
```

---

## 🔍 审查报告示例

```
## 🔍 Code Review

**PR**：feat: 添加用户认证模块
**作者**：@john
**变更**：8 个文件，+423 行 / -12 行

---

### 发现的问题

#### 🔴 高风险（需修复）
1. **[Bug]** 登录失败后 Token 未清除
   - 文件：`src/auth.ts`
   - 位置：第 67-72 行
   - 原因：finally 块缺失，攻击者可利用残留 Token
   - 置信度：94

#### 🟡 中风险（建议处理）
2. **[合规]** 违反 CLAUDE.md 规范：错误需有统一格式
   - 文件：`src/api/users.ts`
   - 位置：第 23-28 行
   - 引用规范：「所有 API 错误必须使用 ApiError 类」
   - 置信度：82

---

### ✅ 通过检查
- 安全性：未见注入漏洞
- 编译检查：通过
- 测试覆盖：变更区域有测试

---
审查完成。如需发布评论请说「发布评论」。
```

---

## 🔧 3 路并行审查机制

| Agent | 模型 | 职责 |
|-------|------|------|
| **合规检查** | Sonnet | 验证是否违反 CLAUDE.md 规范，引用原文 |
| **Bug 检测** | Opus | 扫描逻辑错误、安全隐患、编译失败问题 |
| **历史分析** | Sonnet | Git blame + log 分析，查找冲突和上下文 |

---

## 📊 置信度评分标准

| 分数 | 含义 | 是否报告 |
|------|------|---------|
| 0-49 | 可能是误报 | ❌ 不报告 |
| 50-74 | 真实问题但影响小 | ❌ 不报告 |
| 75-79 | 明确问题，影响较大 | ❌ 不报告 |
| **80-100** | **高置信度** | ✅ **报告** |

**只有 ≥80 分的问题才会出现在最终报告中。**

---

## 🚫 内置过滤（不会报告）

- ❌ PR 之前就存在的问题
- ❌ 看起来像 Bug 但实际正确的代码
- ❌ 吹毛求疵的 nitpick
- ❌ Linter 会自动捕获的问题
- ❌ 笼统的代码质量问题（除非 CLAUDE.md 明确要求）
- ❌ 通过 lint ignore 注释显式忽略的问题

---

## 🏗️ 项目结构

```
openclaw-code-review-skill/
├── README.md              # 本文件
├── SKILL.md               # Skill 定义（OpenClaw 自动加载）
└── README_SOURCE.md       # Claude Code 原插件 README
```

---

## 📦 依赖

| 依赖 | 说明 |
|------|------|
| **OpenClaw** | 框架运行环境 |
| **gh (GitHub CLI)** | PR 数据获取 + 评论发布 |
| **CLAUDE.md** | 可选，有则进行合规检查 |

---

## 🔗 相关项目

- [claw-code](https://github.com/ultraworkers/claw-code) — Rust 实现的 Claude Code CLI
- [OpenClaw](https://github.com/openclaw/openclaw) — 本 Skill 运行的框架
- [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) — Claude Code 社区插件集合

---

## 📄 License

MIT

---

> 💡 **提示**：维护清晰的 `CLAUDE.md` 规范文件，Code Review 的合规检查会更准确！
