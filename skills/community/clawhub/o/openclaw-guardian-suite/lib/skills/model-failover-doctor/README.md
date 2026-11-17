# 🩺 Model Failover Doctor

> *当 AI 说"所有模型都失败了"——它其实是在请求一位医生。*

---

## 你是否遇到过这种情况？

某天，你的 OpenClaw 突然开始报错：

```
All models failed (6): kimi-coding/k2p5: No available channel for model openai/gpt-5.3-codex
```

你看了三遍，感觉哪里不对——`kimi-coding` 明明是个编程模型的 provider，为什么它会去找 `openai/gpt-5.3-codex`？这两个压根就不是一回事。

于是你重启 gateway，重启又重启，甚至清空了 session 状态。有时好了，有时没好，你完全不知道根因在哪里。

**Model Failover Doctor 就是为这种时刻而生的。**

---

## 它能做什么？

这是一个为 OpenClaw 设计的 **模型 Failover 诊断 & 修复工具**。它能在几秒钟内帮你找到 "All models failed" 错误背后真正的根因，并在大多数情况下自动修复它们。

### 五种根因，一网打尽

| 代码 | 病因 | 严重程度 | 能否自动修复 |
|------|------|:--------:|:------------:|
| **MI-1** | `before_agent_start` 无条件返回 `modelOverride`，毒化所有 fallback | 🔴 致命 | ✅ 自动 |
| **MI-2** | 缺少全局死亡模型注册表，不同 session 反复踩同一个坑 | 🟡 警告 | 🖐 手动 |
| **P-1** | `pools.json` 引用了不存在的 provider 前缀 | 🔴 致命 | ✅ 自动 |
| **S-1** | session 没有 `fallbackChain`，runtime fallback 永远无法推进 | 🔴 致命 | ✅ 自动 |
| **S-2** | `fallbackChain` 里含有无效 provider，gateway 路由必然 503 | 🔴 致命 | ✅ 自动 |

---

## 快速上手

### 三条命令，从入门到修复

```bash
# 1. 只看诊断报告，不动任何文件
python3 ~/.openclaw/workspace/skills/model-failover-doctor/model_failover_doctor.py

# 2. 发现问题？预览将要做的修改（安全，不写入）
python3 ~/.openclaw/workspace/skills/model-failover-doctor/model_failover_doctor.py --dry-run

# 3. 确认没问题？一键修复 + 重启 gateway
python3 ~/.openclaw/workspace/skills/model-failover-doctor/model_failover_doctor.py --fix --restart
```

### 健康的输出长什么样？

```
🩺 OpenClaw Model Failover Doctor — 2026-03-05 23:30
────────────────────────────────────────────────
✅ 未发现问题，模型 Failover 配置正常。
   覆盖: MI-1 / MI-2 / P-1 / S-1 / S-2
```

### 有问题时的输出

```
🩺 OpenClaw Model Failover Doctor — 2026-03-05 23:30
────────────────────────────────────────────────
发现 2 个问题  🔴 致命: 1  🟡 警告: 1

🔴 [1] [MI-1] before_agent_start 无条件返回 modelOverride/providerOverride（根因 A）  ✏️ 可自动修复
     问题: Gateway 进行 fallback 时，会将 before_agent_start 返回的
           modelOverride/providerOverride 应用到所有 fallback 尝试，
           导致 kimi-coding、zai、minimax 等 provider 都收到了错误的 model ID。

💊 运行以下命令自动修复 1 个问题:
   python3 model_failover_doctor.py --fix --restart
```

---

## 背后的故事：MI-1 根因解析

最常见的根因是 MI-1，理解它需要一点 Gateway 的工作原理知识。

当 Gateway 发现当前模型失败时，它会按照 `fallbackChain` 的顺序依次尝试每个备用 provider。但在尝试每一个的时候，它都会调用 `before_agent_start` 钩子获取配置——包括 `modelOverride`（你想用哪个 model）。

问题就在这里：如果 `before_agent_start` **无条件地**把 `modelOverride` 写死为某个特定 model ID 并返回，那么 `kimi-coding`、`zai`、`minimax` 这些完全不同的 provider 在尝试时，都会收到同一个错误的 model ID。它们全部失败，Gateway 就报出 `All models failed (6)`——而 6 个 provider 的错误 model ID 完全一样，这就是那种"哪里不对"的感觉的来源。

**修复方案**：把 `modelOverride` 的返回包装在 `lockModel` 条件里。只有当用户明确锁定了模型时，才把 `modelOverride` 传给钩子；正常路由时，让 Gateway 自己根据 provider 决定用哪个 model。

---

## 安全设计

- **所有自动修复操作前，先创建时间戳备份**
- 备份路径：`~/.openclaw/workspace/.lib/.mfd_backups/`
- 支持 `--dry-run` 预览，完全不写入任何文件
- 修复范围明确，只触碰与 failover 相关的三个文件：
  - `message-injector/index.ts`
  - `.lib/pools.json`
  - `.lib/session_model_state.json`

---

## 触发时机（在 Agent 中使用）

在你的 Agent 遇到以下任何一种情况时，触发此工具：

1. 日志出现 `All models failed (N)`，且多个 provider 的错误 model ID 完全相同
2. Agent 重启后第一条消息必然失败，后续消息正常（冷启动 session 无 fallbackChain）
3. 手动编辑 `pools.json` 或 `session_model_state.json` 后，Agent 开始报 503

---

## 安装

```bash
clawhub install model-failover-doctor
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-05 | 初始发布：MI-1/MI-2/P-1/S-1/S-2 五类根因检测，4类自动修复，完整备份机制 |

---

*由 DeepEye 🧿 协同 Claude Code 构建 · OpenClaw 生态*
