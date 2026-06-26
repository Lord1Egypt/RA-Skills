# PAD Mode for OpenClaw

<img width="1536" height="776" alt="PAD Mode" src="https://github.com/user-attachments/assets/097ea4bf-a70b-4579-8246-5a578cf2e3a4" />

**Plan → Act → Deliver** — 一个为 OpenClaw 设计的结构化任务执行 Skill。

[![ClawHub](https://img.shields.io/badge/ClawHub-install%20pad--mode-blue)](https://clawhub.ai/yipxiyi/pad-mode)
[![Version](https://img.shields.io/badge/version-1.1.0-green)](https://clawhub.ai/yipxiyi/pad-mode)
[![License](https://img.shields.io/badge/license-MIT-yellow)](./LICENSE)

[English](./README.md)

---

## 效果对比

**没有 PAD Mode：**
> 用户："把认证模块从 session 改成 JWT"
>
> Agent：*立刻开始改文件，改到一半登录流程坏了，忘了更新测试，主文件改完就说"搞定了"，但中间件还在用 session*

**有 PAD Mode：**
> 用户："把认证模块从 session 改成 JWT"
>
> Agent：创建一个 5 步计划（token 生成、中间件更新、测试更新、迁移脚本、清理），等你确认后逐个执行并更新状态，最后让你验收再归档。

区别在于：**结构化拆解 + 确认门槛 = 可靠执行**。

---

## 核心特性

- 📋 **计划文档** — 每个任务有明确可交付物。"优化代码"变成"通过 Redis 缓存用户接口，将响应时间从 800ms 降到 200ms"
- 🔄 **前台/后台执行** — 复杂计划可转后台（sub-agent），进度实时推送给你
- ✅ **完成门槛** — 计划不会自动关闭，必须你确认验收才算完
- 📦 **并行执行** — 独立任务通过 sub-agent 并行处理
- 🔁 **可恢复** — 中断的计划可以从上次进度继续
- 📝 **变更日志** — 每次修改都记录在计划文档中

## 状态流转

```
🟡 讨论中 → 🔵 已确认 → 🟢 执行中 → ⏳ 待确认 → ✅ 已完成
                                                      ↓
                                    🔧 需要修改 → 回到讨论
```

---

## 安装

### ClawHub（推荐）

```bash
clawhub install pad-mode
```

### 从源码安装

```bash
git clone https://github.com/Yipxiyi/PAD-Mode-for-openclaw.git
cp -r PAD-Mode-for-openclaw ~/.openclaw/workspace/skills/pad-mode/
```

---

## 触发方式

| 方式 | 示例 | 何时触发 |
|------|------|---------|
| 斜杠命令 | `/pad` | 始终触发 |
| 关键词 | "做个计划"、"plan mode"、"帮我规划" | 检测到规划意图 |
| 自动检测 | 3+ 独立任务、多文件修改、架构决策 | 复杂需求自动建议 |

**会触发的场景：**
- ✅ "加个用户认证，要有登录、注册、密码重置、邮箱验证"（4 个任务）
- ✅ "把数据库从 MySQL 迁移到 PostgreSQL"（多步骤、高风险）
- ✅ "重构支付模块，顺便接 Stripe"（多个关注点）

**不会触发的场景：**
- ❌ "修一下 header.js 的拼写错误"（单一简单任务）
- ❌ "这个函数是干嘛的？"（问题是提问，不是任务）

---

## 工作流程

四个阶段，每一步都有执行纪律：

```
  PLAN            DISCUSS         ACT             DELIVER
  拆解            讨论            执行            交付
  ├ 创建计划      ├ 完善范围      ├ 逐个任务      ├ 验收全部
  ├ 拆成任务      ├ 锁定          │ 状态追踪      ├ ✅ 或 🔧
  │              │ 可交付物      ├ 进度推送      └ 归档
  └ 不做调研      └ 最多 4 个问题  └ 前台/后台      │
                                                    │
                                   ◄── 如需修改回到讨论 ──►
```

## ⚠️ 强制规则

PAD Mode 把以下规则当作硬性阻断，不是建议：

| 规则 | 违反后果 |
|------|---------|
| 不得跳过审批（Phase 3） | 立即停止，撤回操作，回到 Phase 3 |
| 计划阶段不做调研 | 丢弃所有调研结果 |
| 必须询问执行模式 | 暂停所有工作，等待用户回复 |
| 必须更新任务状态 | 立即修正计划文档 |
| 不得自动归档 | 等待用户确认 |

---

## 实际案例

**用户请求：** "做一个 Todo App 的 REST API，要 CRUD、用户认证、部署到 Railway"

**生成的计划 (`plans/2026-03-31-todo-api.md`)：**

```markdown
# 📋 Todo REST API

**状态:** 🔵 已确认
**创建:** 2026-03-31 14:00

## 任务拆解
- [x] **T1.1** 初始化 Express + TypeScript 项目
  - 交付物: 项目脚手架，含 tsconfig、package.json、目录结构
  - 依赖: 无
- [x] **T1.2** 实现 CRUD 接口（GET/POST/PUT/DELETE /todos）
  - 交付物: 4 个带验证的可用接口
  - 依赖: T1.1
- [ ] **T2.1** 添加 JWT 认证
  - 交付物: 登录/注册接口 + 认证中间件
  - 依赖: T1.1
- [ ] **T3.1** 编写测试
  - 交付物: 接口测试覆盖率 80%+
  - 依赖: T1.2, T2.1
- [ ] **T4.1** 部署到 Railway
  - 交付物: 线上 URL，健康检查通过
  - 依赖: T3.1
```

---

## 开发背景

灵感来自 **OpenAI Codex** 和 **Anthropic Claude Code** 的结构化计划模式。它们证明了一个事实：**强制 LLM 先计划再执行，能显著提高长任务的成功率。**

PAD Mode 在此基础上增加了：
- **用户确认关卡**（计划审批 + 完成验收）
- **前台/后台执行**选择
- **实时进度追踪**（通过计划文档）
- **Sub-agent 并行**（独立任务同时跑）
- **强制执行规则**（防止 Agent 常见错误）

目标：让 OpenClaw 处理长任务时跟处理短任务一样靠谱。

## License

MIT
