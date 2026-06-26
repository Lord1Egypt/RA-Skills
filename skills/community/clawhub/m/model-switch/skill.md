---
name: model-switch
description: OpenClaw 一键切换AI模型技能。懒人触发词：切到xxx、当前模型、模型问题、添加/移除模型、模型对比/列表。解决"切换模型后为什么总是失败"的痛点。
---

# model-switch — OpenClaw 一键切换 AI 模型

> 🎯 **一句话搞定模型切换 + 动态添加 + 诊断对比**
>
> ⚠️ 本技能仅适用于 [OpenClaw](https://github.com/openclaw/openclaw) 用户
>
> **触发词（懒人版）：**
> - `切到 gpt-4o` / `切到 deepseek` — 直接切换
> - `当前模型` — 查看当前模型
> - `模型问题` — 诊断配置问题
> - `添加模型` / `移除模型`
> - `模型对比` / `模型列表`
>
> **执行流程：** 当你说"切到 xxx"时，会自动执行全部 5 步切换，包括在当前会话调用 `session_status(model="xxx")`，**无需手动操作**。

---

## 🚀 为什么需要这个技能

切换模型不是改一个地方就完事——**必须同时改 4 个地方**，缺一不可：

| 层级 | 位置 | 作用 | 不改的后果 |
|------|------|------|-----------|
| ① 运行态 | 当前会话 `session_status(model=...)` | 立即生效 | 当前会话不切换 |
| ② 配置 | `openclaw.json → agents.list[agent].model` | 新会话默认值 | 重启后回退 |
| ③ 兜底 | `openclaw.json → agents.defaults.model.primary` | 所有 Agent 的兜底 | 未配置 Agent 用旧模型 |
| ④ 认证 | `agents/<agent>/agent/auth-profiles.json` | **API key 必须匹配 provider** | Gateway 自动回退 → "Something went wrong" |

> ⚠️ **这是"Something went wrong"的根本原因**：只改了模型名，但 auth-profiles 里还是旧 provider 的 key。

---

## 📋 命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `switch <agent> <model>` | 切换单个 Agent 模型 | `switch main openai/gpt-4o` |
| `switch ALL <model>` | 批量切换所有 Agent | `switch ALL deepseek/deepseek-v4-flash` |
| `add <provider> <model>` | 添加新模型到白名单 | `add openai gpt-5` |
| `remove <provider> <model>` | 从白名单移除 | `remove minimax MiniMax-M2.7-highspeed` |
| `list` | 列出所有可用模型 | `list` |
| `list-providers` | 列出 provider 及 API key 状态 | `list-providers` |
| `compare` | 模型能力/成本对比 | `compare` |
| `diagnose` | 诊断当前配置问题 | `diagnose` |
| `show` | 显示当前会话模型 | `show` |
| `reset` | 清除 override，回退默认 | `reset` |
| `add-key <provider>` | 从环境变量添加 provider key | `add-key anthropic` |

---

## 🔧 核心功能详解

### 1. 切换模型（4 层同步）

```bash
bash model-switcher.sh switch main openai/gpt-4o
```

**自动执行 5 步：**

1. **白名单检查** — 模型不在列表则自动添加
2. **API key 验证** — 检查 provider 的 key 是否完整（环境变量 + config）
3. **auth-profiles 更新** — 为所有相关 Agent 添加/更新 provider 认证
4. **openclaw.json 更新** — 修改 agents.list 和 defaults
5. **输出下一步** — 告知需要在会话中执行 `session_status(model=...)`

### 2. 动态添加任意模型（核心增强）

**不再局限于预置的 6 个模型！** 支持添加任何 provider/model：

```bash
# 添加 OpenAI GPT-5
bash model-switcher.sh add openai gpt-5

# 添加 Anthropic Claude
bash model-switcher.sh add anthropic claude-3-7-sonnet

# 添加 Groq 极速推理
bash model-switcher.sh add groq llama-3-3-70b

# 添加本地 Ollama 模型
bash model-switcher.sh add ollama qwen2-5-72b
```

**添加后自动检查：**
- ✅ provider 是否在 `models.providers` 中配置
- ✅ API key 环境变量是否设置
- ⚠️ 如果 provider 未配置，给出明确修复指引

### 3. 添加 Provider API Key

当环境变量已设置但 config 中未配置时：

```bash
bash model-switcher.sh add-key anthropic
```

自动完成：
- 将环境变量值写入 `models.providers.anthropic.apiKey`
- 更新所有 Agent 的 `auth-profiles.json`

### 4. 模型对比

```bash
bash model-switcher.sh compare
```

输出所有可用模型的 Tier/成本/速度/推理能力/用途对比表。

### 5. 配置诊断

```bash
bash model-switcher.sh diagnose
```

检查：
- ✅ 默认模型是否在白名单
- ✅ 每个 Agent 的模型是否在白名单
- ✅ 每个 Provider 的 API key 是否完整
- ✅ 每个 Agent 的 auth-profile 是否匹配当前模型

### 6. 模型对比参考表（内置）

| 模型 | Tier | 成本 | 速度 | 推理 | 用途 |
|------|------|------|------|------|------|
| `sensenova-6.7-flash-lite` | L4 | 极低 | 快 | 弱 | 日常调度、闲聊 |
| `sensenova-u1-fast` | L4 | 最低 | 最快 | 弱 | 自动化、规则匹配 |
| `deepseek-v4-flash` | L2 | 低 | 中 | 中 | 后端开发、批量处理 |
| `deepseek-v4-pro` | L1 | 中 | 慢 | 强 | 复杂推理、代码审查 |
| `MiniMax-M2.7-highspeed` | L3 | 低 | 快 | 中 | 创意内容、文案 |
| `mimo-v2.5-pro` | L1 | 中 | 中 | 强 | 深度分析、战略 |
| `gpt-4o` | L1 | 高 | 中 | 强 | 通用最强 |
| `gpt-4o-mini` | L3 | 低 | 快 | 中 | 轻量任务 |
| `gpt-5` | L1 | 高 | 中 | 极强 | 最复杂推理 |
| `claude-3-7-sonnet` | L1 | 高 | 慢 | 极强 | 代码、推理 |
| `claude-3-5-haiku` | L3 | 低 | 快 | 中 | 快速响应 |
| `gemini-2-5-pro` | L1 | 高 | 中 | 强 | 多模态、长上下文 |
| `gemini-2-5-flash` | L2 | 中 | 快 | 中 | 性价比平衡 |
| `llama-3-3-70b (Groq)` | L2 | 极低 | 极快 | 中 | 极速推理 |
| `llama3 (Ollama)` | L2 | 免费 | 取决于硬件 | 中 | 本地离线 |
| `qwen2-5-72b (Ollama)` | L2 | 免费 | 取决于硬件 | 强 | 本地中文 |

> 📝 **自定义扩展**：编辑 `model_switcher.py` 中的 `MODEL_PROFILE` 字典即可添加/修改模型参考信息。

---

## 🔄 与 Matt Pocock Skills 体系集成

本技能属于 **Infrastructure（基础设施）** 分类，与 Matt Pocock 体系的对应关系：

| Matt Pocock Skill | 本技能对应 | 关系 |
|-------------------|-----------|------|
| `/grill-me` | — | 需求对齐（不同维度） |
| `/tdd` | — | 测试驱动（不同维度） |
| `/diagnose` | `diagnose` 子命令 | **直接集成** — 模型配置诊断 |
| `setup-matt-pocock-skills` | `add-key` + `add` | **互补** — 环境配置 |

**集成建议：**
- 将 `model-switcher` 作为 Matt Pocock Skills 的 **Infrastructure 扩展包**
- 在 `grill-me` 流程中增加"当前模型是否适合此任务"的检查
- 在 `tdd` 流程中根据模型能力自动调整测试策略

---

## ⚠️ 常见错误 & 修复

### "Something went wrong while processing your request"

**根因**: 模型/provider/auth 三者不匹配。

```bash
# 1. 诊断问题
bash model-switcher.sh diagnose

# 2. 根据输出修复
# - 白名单缺失 → add
# - API key 缺失 → add-key
# - auth-profile 缺失 → switch 会自动修复
```

### 切换后还是旧模型

```bash
# 清除 model override
bash model-switcher.sh reset
# 然后在会话中执行: session_status(model="default")
```

### 子 Agent 切换不生效

子 Agent 的飞书会话有自己的 `agents.list[agentId].model`，需要单独切换：

```bash
bash model-switcher.sh switch backbase deepseek/deepseek-v4-flash
bash model-switcher.sh switch strategy deepseek/deepseek-v4-pro
```

### 添加新 provider 后无法使用

```bash
# 1. 添加模型到白名单
bash model-switcher.sh add anthropic claude-3-7-sonnet

# 2. 确保环境变量已设置
export ANTHROPIC_API_KEY="sk-..."

# 3. 将 key 添加到 config
bash model-switcher.sh add-key anthropic

# 4. 切换使用
bash model-switcher.sh switch main anthropic/claude-3-7-sonnet
```

---

## 📦 文件结构

```
model-switcher/
├── SKILL.md              # 本文件 — 技能文档
├── model_switcher.py     # 核心 Python 实现（支持 10+ 子命令）
├── model-switcher.sh     # Shell 入口（兼容旧用法）
└── switch.sh             # 旧版 Shell 脚本（保留兼容）
```

---

## 🎯 设计哲学

> **"切换模型应该像换衣服一样简单，而不是像修电路一样复杂。"**

1. **零知识门槛** — 用户只需说"切换到 GPT-5"，其余全部自动
2. **防御性设计** — 每一步都验证，发现问题立即给出修复指引
3. **可扩展性** — 支持任意 provider/model，不局限于预置列表
4. **透明化** — diagnose 命令让配置问题一目了然
5. **兼容性** — 保留旧版 switch.sh，平滑升级

---

## 🚀 发布计划

1. ✅ v3 增强版完成（动态添加 + 子命令 + 诊断对比）
2. ⏳ 集成到 Matt Pocock Skills 体系
3. ⏳ 发布到 ClawHub 和 GitHub
4. ⏳ 编写多语言文档（中英文）
