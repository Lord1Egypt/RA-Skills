# model-switch — 模型切换与管理工具

> 🎯 **一键热切换模型 + 动态添加任意模型 + 完整诊断对比**
>
> 解决 AI 编程中最大的痛点之一：**切换模型后为什么总是失败？**

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

## 📋 快速开始

```bash
# 查看帮助
bash model-switch.sh

# 切换模型
bash model-switch.sh switch main openai/gpt-4o

# 添加新模型
bash model-switch.sh add anthropic claude-3-7-sonnet

# 查看可用模型
bash model-switch.sh list

# 模型对比
bash model-switch.sh compare

# 诊断配置问题
bash model-switch.sh diagnose
```

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

## 🔧 核心功能

### 1. 切换模型（4 层同步）

```bash
bash model-switch.sh switch main openai/gpt-4o
```

**自动执行 5 步：**

1. **白名单检查** — 模型不在列表则自动添加
2. **API key 验证** — 检查 provider 的 key 是否完整
3. **auth-profiles 更新** — 为所有相关 Agent 添加/更新 provider 认证
4. **openclaw.json 更新** — 修改 agents.list 和 defaults
5. **输出下一步** — 告知需要在会话中执行 `session_status(model=...)`

### 2. 动态添加任意模型

**不再局限于预置模型！** 支持添加任何 provider/model：

```bash
bash model-switch.sh add openai gpt-5
bash model-switch.sh add anthropic claude-3-7-sonnet
bash model-switch.sh add groq llama-3-3-70b
bash model-switch.sh add ollama qwen2-5-72b
```

### 3. 模型对比

```bash
bash model-switch.sh compare
```

输出所有可用模型的 Tier/成本/速度/推理能力/用途对比表。

### 4. 配置诊断

```bash
bash model-switch.sh diagnose
```

检查默认模型、Agent 模型、Provider API key、auth-profile 完整性。

---

## 📦 文件结构

```
model-switch/
├── README.md              # 本文件
├── SKILL.md               # 技能文档（含 Matt Pocock 集成）
├── model_switcher.py      # 核心 Python 实现
├── model-switch.sh      # Shell 入口
└── switch.sh              # 旧版兼容脚本
```

---

## 🔄 与 Matt Pocock Skills 体系集成

本技能属于 **Infrastructure（基础设施）** 分类，补充 Matt Pocock 体系缺少的基础设施运维能力。

详见：[INFRASTRUCTURE.md](../INFRASTRUCTURE.md)

---

## 🎯 设计哲学

> **"切换模型应该像换衣服一样简单，而不是像修电路一样复杂。"**

1. **零知识门槛** — 用户只需说"切换到 GPT-5"，其余全部自动
2. **防御性设计** — 每一步都验证，发现问题立即给出修复指引
3. **可扩展性** — 支持任意 provider/model，不局限于预置列表
4. **透明化** — diagnose 命令让配置问题一目了然
5. **安全性** — 不打印任何真实 API key

---

## 📜 许可证

MIT License

---

## 🙏 致谢

- [Matt Pocock Skills](https://github.com/mattpocock/skills) — 启发 Infrastructure 扩展包的设计
- [OpenClaw](https://github.com/openclaw/openclaw) — 多模型支持架构
