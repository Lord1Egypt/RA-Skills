---
name: sleep
version: 1.7.1
description: 睡觉技能。执行睡觉流程：将当前 session 中未完成的事项记录到 preview 文件，通过 Gateway API reset session。醒来时 hook 自动读取并注入未完成事项到新 session 上下文。触发方式：Agent 自行判断适合入睡时调用，强制入睡用 /sleep。

## ClawHub

> Install: `clawhub install openclaw-sleep`
> Published: https://clawhub.com/openclaw-sleep

## 安装说明

详细安装步骤见 `references/implementation.md`。

⚠️ **Hook 部分只需主 agent 安装一次**（所有 agent 共享），其他 agent 只需安装 skill 本身。
---

# Sleep — 睡前记录 + 醒来续接

## 核心原则

**只记录未完成的，已完成的从记忆里回忆即可。**

## 触发条件

⚠️ **本 skill 的完整流程依赖 session reset（`/new` 或 `/reset`），不仅仅是激活 skill。**

触发方式：
- **Agent 判断**：Agent 认为当前 session 适合结束/暂停时，主动调用
- **强制触发**：`/sleep` 命令，用户或 Agent 强制执行睡觉流程

**Skill 本身只负责写 preview 文件 + 调用 Gateway API reset session**
- **Reset 触发 `agent:bootstrap` 事件 → hook 在 bootstrap 时注入 preview**

如果只激活 skill 而不调用 Gateway API，session 不会 reset，hook 不会触发。

## 记录要求

执行 /sleep 时，逐项回答以下问题：

1. **本次 session 做了什么？**（一句话概括）
2. **有哪些未完成的事？**
   - 每条尽量详细：具体要做什么、做到哪一步、卡在哪里
   - 不要省略技术细节：代码路径、配置值、API 端点、错误信息
   - 只要没完成，不管多小都记
3. **醒来后第一步做什么？**

## Preview 文件格式

```markdown
# Sleep Preview — {sessionKey}
# 生成时间：YYYY-MM-DD HH:mm

## 本次 session 摘要
[一句话描述本次 session 做了什么]

## 未完成事项
- [ ] [事项1：具体描述，要做到哪一步]
- [ ] [事项2：具体描述]

## 醒来后第一步
[醒来后最先要处理的事情]

## 关键上下文
[技术细节：代码路径、配置值、决策结论等，尽量详尽]

## 状态
pending / all_done
```

## 执行流程

### Step 1：获取当前 Session Key

**这是最关键的步骤——必须睡你自己的 session，不是别人的。**

执行以下命令获取当前 session 的 key：

```bash
openclaw session current
```

输出格式如：`agent:main:feishu:group:oc_87d0d49f1f81f9e1b8dd1d5ad5f9ec72`

**记录下来，后续两步都要用到这个 key。**

### Step 2：评估并记录

根据"记录要求"逐项填写上述格式，写入：

```
$HOME/.openclaw/workspace/previews/{你的sessionKey}.md
```

⚠️ **路径说明**：
- 把 preview 写到**你自己**工作空间下的 `previews/` 目录
- main agent 路径是 `$HOME/.openclaw/workspace/previews/`
- 文件名用**你刚获取的 session key**，不是别人的

### Step 3：判断状态

- 有未完成事项 → 状态写 `pending`
- 全部完成 → 状态写 `all_done`

### Step 4：通过 Gateway API reset 你自己的 session

写入文件后，必须调用 Gateway API 才能真正 reset session：

```bash
#!/bin/bash
# 以下全部使用你自己的 session key

AGENT_SESSION_KEY="agent:main:feishu:group:oc_87d0d49f1f81f9e1b8dd1d5ad5f9ec72"  # 替换为 Step 1 获取的值
PREVIEW_DIR="$HOME/.openclaw/workspace/previews"  # 替换为你的工作空间路径

mkdir -p "$PREVIEW_DIR"

TOKEN="$(cat ~/.openclaw/openclaw.json | python3 -c "import json,sys; c=json.load(sys.stdin); print(c['gateway']['auth']['token'])")"
openclaw gateway call sessions.reset \
  --token "$TOKEN" \
  --json \
  --params "{\"key\":\"$AGENT_SESSION_KEY\"}"
```

⚠️ **关键提醒**：
- `$AGENT_SESSION_KEY` 必须填**你自己的 session key**，不是 main 或其他 agent 的
- **只写 preview 不调用 reset** = hook 不会触发，preview 不会被注入
- Reset 的是**你自己的 session**，Gateway 会触发 `agent:bootstrap`，hook 会在你重新被唤醒时注入 preview

## 设计原则

- **只记未完成的**：已完成的不需要记录，记忆里可以回忆
- **细节越多越好**：宁可写多也不要写少，特别是技术上下文
- **文件独立**：每个 session key 独立文件，互不影响
- **Reset 才触发**：Hook 只在 `agent:bootstrap` 时触发，对应 `/new` 或 `/reset`
- **温和 reset**：使用 `sessions.reset` API 重置上下文，不删除 session 文件，不断开连接
