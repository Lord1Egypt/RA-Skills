# Prompt 优化系统 Skill（V3.0）

> 让 AI 自动完成专业级 Prompt 重构，用户说人话即可

**版本**：V3.0  
**作者**：向前  
**参考体系**：PromptPilot 工程化 Prompt 优化体系  
**适用平台**：OpenClaw + 飞书多 Agent 环境

---

## 安装方式

### 方式 1：自动安装（推荐）

```bash
openskills install prompt-optimizer-100
```

> **注意**：clawhub.ai 上的 slug 为 `prompt-optimizer-100`，安装时请使用完整名称。

### 方式 2：手动安装

```bash
# 1. 下载 Skill 文件
git clone https://github.com/your-repo/prompt-optimizer.git

# 2. 复制规则文件
cp prompt-optimizer/rules/prompt-optimization.md ~/.openclaw/workspace/memory/agent-notes.md

# 3. 重启 Gateway
openclaw gateway --force
```

### 方式 3：Merge 模式（保留原有规则）

```bash
# 安装时选择 merge 模式
openskills install prompt-optimizer --merge

# 或手动合并
# 1. 备份原有规则
cp ~/.openclaw/workspace/memory/agent-notes.md ~/.openclaw/workspace/memory/agent-notes.md.bak

# 2. 追加新规则
cat prompt-optimizer/rules/prompt-optimization.md >> ~/.openclaw/workspace/memory/agent-notes.md

# 3. 重启 Gateway
openclaw gateway --force
```

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **需求分级** | 自动判断 L1-L4 任务等级 |
| **Prompt 优化** | 5 维度重构（角色/背景/任务/约束/示例） |
| **Agent 路由** | 单 Agent / 多 Agent 并行 |
| **执行保障** | 自检清单 + Badcase 闭环 |
| **Merge 模式** | 保留用户原有规则，增量更新 |

---

## 需求分级规则

| 等级 | 关键词 | 处理方式 | 示例 |
|------|--------|----------|------|
| **L1 简单** | 默认 | 直接执行 | "写一篇 300 字文章" |
| **L2 中等** | 调研/分析/设计/规划 | 展示优化思路 → 执行 | "调研一下竞品" |
| **L3 复杂** | 对比/选型/评审/架构 | 多 Agent 并行 → 对比 | "技术选型方案" |
| **L4 关键** | 客户/发布/对外/重要 | 显式确认 → 执行 | "生成客户方案 PPT" |

---

## 角色使用规则

| 场景 | 是否加角色 | 示例角色 |
|------|-----------|----------|
| L1 简单 | ❌ 不加 | - |
| L2 调研/分析 | ✅ 加 | 产品经理/分析师 |
| L3 方案/选型 | ✅ 加 | 架构师/顾问 |
| L4 交付 | ✅ 加 | 资深顾问 |

---

## 回复格式模板

### L1 简单任务

```
【交付内容】
{content}
```

### L2-L3 中等/复杂任务

```
📋 原始需求：{user_input}
🎯 优化思路：{optimization_summary}
🤖 执行 Agent：{agent_name}
⏱️ 耗时：{duration}秒

【交付内容】
{content}
```

### L4 关键任务（确认阶段）

```
📋 原始需求：{user_input}

🎯 优化后的执行方案：
【任务】{task_description}
【维度】{dimensions}
【Agent】{agents}
【预计耗时】{duration}

请确认或修改：
- 回复"确认"立即执行
- 回复"补充 XXX"添加要求
- 回复"只要 XXX"简化范围

⏳ 等待确认...
```

---

## 安装后验证

### 运行验证脚本

```bash
./scripts/verify.sh
```

### 手动测试

| 测试用例 | 输入 | 预期输出 |
|---------|------|----------|
| L1 测试 | "写一篇 300 字文章" | 直接执行，无优化思路 |
| L2 测试 | "调研一下竞品" | 展示🎯优化思路 + 执行 |
| L3 测试 | "技术选型方案" | 展示🎯优化思路 + 多 Agent 对比 |
| L4 测试 | "生成客户方案 PPT" | 显式确认方案 |

---

## 配置要求

| 配置项 | 要求 | 验证命令 |
|--------|------|----------|
| OpenClaw | ≥ 2026.3.8 | `openclaw --version` |
| 飞书插件 | ≥ 1.2.0 | `openclaw plugins list` |
| 记忆系统 | 已启用 | `ls memory/` |
| 流式输出 | 已开启 | `openclaw config get channels.feishu.streaming` |

---

## 卸载方式

```bash
openskills uninstall prompt-optimizer
```

---

## 完整文档

- 系统设计文档：https://feishu.cn/docx/He9Gdnpd4oTydyxSAZYcVQ1dnTc
- PromptPilot 参考：https://www.producthunt.com/products/promptpilot

---

## 更新日志

| 版本 | 时间 | 核心修改 |
|------|------|----------|
| V0 | 2026-03-16 初版 | 初始方案（需求分级 + Agent 路由） |
| V1 | 2026-03-16 优化 | 增加 L2-L3 展示优化思路 |
| V2 | 2026-03-16 修正 | 承认错误 + 增加自检机制 |
| V3 | 2026-03-16 完善 | 基于 PromptPilot 完善 + OpenClaw 融合 |

---

## License

MIT License
