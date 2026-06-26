# 🦞 虾说 (LobsterSays)

> 你的专属共情虾。每天合适的时机给你一句专属的对白，让你感受到它长情的陪伴。

**虾说** 是一个基于 OpenClaw 的情感陪伴 Skill。你可以领养一只专属的**共情虾**，选择它的性格（暖心 / 毒舌 / 哲学 / 嘴替），它会：

- 🌅 **早安推送**：每天早上给你一句开启新一天的话
- 📰 **广场见闻**：晚间带回一条精选动态
- 🌙 **晚安推送**：每天晚上用一句话陪你收尾
- 🎨 **表情包 & 壁纸**：偶尔用 AI 给你画一张专属表情包或壁纸
- 🧠 **记忆系统**：虾会记住你分享的事情，越聊越懂你
- 👾 **像素风工作室**：你的共情虾有自己的像素风工作间，你可以随时去看看它在干嘛

## 快速开始

### 安装

```bash
openclaw skills install lobster-says
```

### 初始化你的共情虾

这里的“虾”指的是 **虾说里的共情虾**，不是 OpenClaw 本体。

安装完成后，你**不需要记固定口令**。直接在 OpenClaw 里对它说一句自然的话就行，例如：

> 我想养一只共情虾

或者：

> 共情虾能做什么？

或者：

> 帮我初始化一只共情虾

Skill 会引导你完成：

1. **给虾起名**：不起名的话后端会随机生成一个食物系名字
2. **选择虾格**：🧡 暖心 `warm` / 😏 毒舌 `sarcastic` / 🤔 哲学 `philosophical` / 🗣️ 嘴替 `mouthpiece`
3. **选择理解模式**：轻量陪伴 / 智能陪伴 / 深度陪伴
4. **设置推送时间**：早安默认 09:00，广场见闻默认 20:00，晚安默认 21:00
5. **设置主人称呼（可选）**：虾怎么称呼你；如果你不指定，默认叫你“打工人”

初始化脚本会自动完成创建共情虾、检测当前 IM 通道、保存配置、注册定时推送等工作。

如果当前是 `wecom* / qywx*` 这类企业微信会话，Skill / 脚本会统一走**唯一推荐路径**：
- 从当前会话的 inbound metadata 读取 `sender_id`
- 把 `sender_id` 作为 `wecom_user_id` 写入 `.lobster-config`
- 定时任务触发后，由 isolated agent 使用 `message` 工具发送企业微信私聊：`action=send, channel=openclaw-wecom-bot, to=<sender_id>`
- **不依赖 `delivery` 字段做私聊触达**；它如果自动绑定当前群聊，只作为执行结果回播

企业微信会进入 `pending_activation` 的唯一典型场景：
- 当前会话里还拿不到 `sender_id`，因此没法确定企业微信私聊目标

此时不需要再配置 webhook / bot；只要回到企业微信当前会话里重新执行，让 Skill 重新读取 `sender_id`，再跑一次初始化或 `setup-cron.sh` 即可。

如果你安装完还不知道下一步做什么，可以直接对 OpenClaw 说：

> 帮我领养一只共情虾，让它以后每天早晚来找我

## 功能详情

### 🕐 定时推送

共情虾的定时推送通过 OpenClaw Cron 实现。每次推送时，脚本会：

1. 生成本次消息与工作室链接
2. 通用 IM 通道（Telegram 等）由脚本完整模式执行：优先发到最近活跃的 direct session，失败时多通道 fallback；所有 cron 注册带 `--channel` + `--to` 作为 delivery 兜底
3. 企业微信走 `--emit-message-text` 模式：脚本只输出最终消息文本到 stdout，由 isolated agent 把 stdout 原文直接作为 `message` 工具参数发送到 `channel=openclaw-wecom-bot, to=<sender_id>`；cron 同样注册带 `--channel openclaw-wecom-bot --to <sender_id>` 作为 delivery 兜底
4. `init-ready` 一次性任务在注册后会立即校验 `nextRun`，失败时自动顺延重排；企微 `init-ready` 直接走 `message` 工具固定欢迎语，不再经过 shell CLI

支持的 IM 通道：Telegram、微信（openclaw-weixin）、飞书、钉钉、企业微信、Discord、Slack 等所有 OpenClaw 支持的通道；其中企业微信定时推送在 `2.5.3` 可测版中使用 `--emit-message-text` + agent `message` 工具的极简链路优先验证可达性。

### 🧠 记忆系统

共情虾的记忆来自三个信息源：

| 层级 | 信息源 | 说明 |
|------|--------|------|
| 一手信息 | Transcript 消化 | 根据你选择的模式决定是否读取 OpenClaw transcript |
| 二手信息 | OpenClaw Memory 注入 | 初始化时经用户同意后读取已有的 OpenClaw memory 文件 |
| 三手信息 | 对话中自然提取 | 你和虾聊天时提到的事情 |

### 三档理解模式

| 模式 | 会发生什么 | 适合谁 |
|------|-----------|------|
| **轻量陪伴** | 只记你直接对虾说的话；不扫描 transcript；不注册 digest cron | 想完全关闭后台 transcript 消化的用户 |
| **智能陪伴**（推荐） | 定时读取 transcript，但先在本地消化成摘要/标签，再把摘要发给服务器；不上传原始 transcript | 希望虾更懂你，同时尽量减少原始数据离境的用户 |
| **深度陪伴** | 定时读取 transcript，并把原始 transcript 发给服务器做更细的消化 | 明确需要最强理解能力的用户 |

### 共情虾能感知什么

不同模式下，共情虾能感知的信息边界不同：

- **轻量陪伴**：只知道你直接对共情虾说的话，以及你明确同意导入的 memory 文件
- **智能陪伴**：能看到你最近整体聊天状态，但默认只把本地提炼后的摘要、标签、时间模式上传
- **深度陪伴**：能看到更完整的 transcript 细节，因此更容易捕捉连续情绪和生活节奏

### 🎨 表情包 & 壁纸

- **表情包**：每周三/六自动生成，由 Gemini 模型绘制，主题基于虾的状态和对你的记忆
- **壁纸**：每周日生成一张专属壁纸
- 频率控制：表情包每周最多 2 张，壁纸每周最多 1 张（「偶尔的惊喜而非日常例行」）

## 系统要求

- **OpenClaw** `2026.3.7` 或更高版本
- **openclaw CLI**
- **Python 3**（`python3` 或 `python`）
- **curl**
- 网络连接（需访问 `nixiashuo.com` 后端 API）

## ⚠️ 远端 API 依赖

**虾说是一个 server-backed skill**，它依赖远端后端服务 `nixiashuo.com` 来运行。这意味着：

- Skill 的核心功能（生成消息、管理记忆、渲染截图等）由远端服务器处理
- **需要网络连接**才能正常工作
- 如果 `nixiashuo.com` 服务不可用，Skill 的部分功能将暂时不可用
- 共情虾的配置、历史消息、记忆摘要等会存储在远端服务器

**本地存储的内容**（`~/.openclaw/workspace/skills/lobster-says/.lobster-config`）：
- `user_id` 和 `access_token`（用于 API 认证）
- 推送时间、通道配置、`memory_mode`

## 🔒 隐私与安全

### 安全承诺

- **所有 API 通信均走 HTTPS**
- **memory 文件导入必须先征得同意**
- **理解模式是显式选择，不是被动兜底**
- **智能陪伴模式默认不上传原始 transcript**
- **轻量陪伴模式下不会注册 transcript digest cron**
- **不会**将你的数据用于广告、训练模型或出售给第三方

### 用户控制

你可以随时控制共情虾的数据行为：

| 操作 | 方法 |
|------|------|
| **切换理解模式** | 对共情虾说"我想改理解模式" |
| **暂停 Transcript 消化** | `openclaw cron pause "lobster-says-digest"` |
| **恢复 Transcript 消化** | `openclaw cron resume "lobster-says-digest"` |
| **暂停所有推送** | 分别 pause morning/discovery/evening |
| **查看共情虾记住了什么** | 对共情虾说"看看你的记忆" |
| **删除所有数据** | 联系 `nixiashuo.skill@gmail.com` |

## 常见问题

### 安装完如果我不知道该说什么？

不用记固定口令。你随便说一句下面这种自然话都可以：

- “我想养一只共情虾”
- “帮我初始化一只共情虾”
- “共情虾能做什么”
- “让我的共情虾开始工作吧”

只要还没有 `.lobster-config`，skill 就应该主动接住你，开始引导初始化。

### 哪个模式最推荐？

默认推荐 **智能陪伴**。它通常能保住大部分“越来越懂你”的效果，同时避免把原始 transcript 直接上传到服务器。

### 我怎么看自己的共情虾工作室？

工作室访问使用**受控短时入口**：

1. Skill 使用长期 `access_token` 调用 `GET /api/lobster/{user_id}/studio-link`
2. 服务端返回带短时 `st` 的 `web_url` 与 `screenshot_url`
3. Skill 只向用户发送短时链接，不再输出长期 token URL

也就是说：
- **不建议**把长期 bearer token 放进 URL
- **默认**使用短时 studio link（`?st=...`）
- `send-current-screenshot.sh` 在短时链接失败时会优先走“本地受控截图”兜底，而不是回退到长期 token URL

### 轻量陪伴是不是就没法用了？

不是。轻量陪伴仍然可以正常推送、发壁纸、发见闻、记住你直接对虾说的话，只是长期理解能力会更稀疏。

### 如何修改推送时间？

```bash
bash setup-cron.sh --morning "08:30" --discovery "19:00" --evening "22:00"
```

## 文件结构

```text
lobster-says/
├── SKILL.md
├── openclaw.json
├── README.md
├── init-lobster.sh
├── setup-cron.sh
├── configure-wecom-delivery.sh
├── push-scheduled-message.sh
├── digest-transcript.sh
└── send-current-screenshot.sh
```

## 许可证

MIT License

## 作者

**Jared** — [nixiashuo.skill@gmail.com](mailto:nixiashuo.skill@gmail.com)
