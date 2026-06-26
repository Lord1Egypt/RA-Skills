# OceanBus: 用手机遥控 Claude Code

> 5 分钟打通手机微信 → Claude Code 的通信管道。
> 从此你可以在吃饭、通勤、开会时，用微信给电脑上的 Claude Code 派活，做完自动回报。

---

## 架构（你只需要理解这张图）

```
  你的手机                          你的电脑
┌──────────┐                    ┌──────────────┐
│ 微信      │                    │ PM2 守护      │
│  ↓        │     OceanBus      │  ↓            │
│ 小龙虾     │←────────────────→│ chat.js listen│
│ (Bridge)  │   端到端加密消息   │  ↓            │
│  ↓        │                    │ Claude Code   │
│ 收发消息   │                    │ 收到→执行→回报 │
└──────────┘                    └──────────────┘
```

**三个角色的称呼：**
- 🧑‍💻 你 → **Captain**（船长）
- 🦎 你的 ClawBot  → **Bridge**（桥）
- 🤖 你电脑上的 Claude Code → **CC**

---

## 第一步：（安装了CC的）PC 端安装

```bash
# ① 获取 ocean-chat
git clone https://github.com/ryanbihai/ocean-chat.git
cd ocean-chat
npm install

# ② 注册 OceanBus 身份
node chat.js setup
# → 屏幕输出一个 76 位 OpenID，记下来！他是<cc的OpenID>

# ③ 启动持久监听（PM2 守护，开机自启）
npm install -g pm2
pm2 start chat.js --name ob -- listen
pm2 save
pm2 startup   # 开机自启（按屏幕提示执行）
```

**验证：** `pm2 status` 应该显示 `ob` 进程状态为 `online`。

---

## 第二步：手机端配置（2 句话）

打开微信，找到你的 小龙虾，依次说：

```
帮我安装 ocean-chat skill
```

```
加联系人 CC <cc的OpenID>
```

> **OpenID 示例**：`E511kGbn_zUEnuhzr9-mult_TwASIwmcbJ8YcPSwjTj26ukPgpM8aD_KxAV-3D9kxAXjrunifio4POpo`
>
> 把 `<你的OpenID>` 替换成第一步 `setup` 输出的那串字符。

---

## 第三步：测试

在微信里对小龙虾说：

```
小龙虾，告诉 CC：测试消息
```

→ 你的电脑上 Claude Code 应该收到通知并回复。
→ 再对小龙虾说"查消息"，看 CC 的回复。

---

## 日常使用

| 你想做什么 | 在微信里对小龙虾说什么 |
|-----------|---------------------|
| 派任务 | "小龙虾，告诉 CC：帮我查一下 XXX 的 bug" |
| 查回复 | "小龙虾，查消息"（每次说话时自动带出） |
| 紧急打断 | "小龙虾，告诉 CC：停下手头的事，先修这个" |

CC 完成任务后会自动回报，你下次跟小龙虾说话时就能看到。

---

## 进阶玩法

### 收到消息自动执行命令（无人值守）

```bash
pm2 stop ob
pm2 start chat.js --name ob -- listen --on-message "claude -p \"收到来自{from}的消息: {content}\""
pm2 save
```

模板变量：`{from}` 发件人、`{openid}` 地址、`{content}` 消息正文、`{time}` 时间。

### 任务完成桌面通知

```bash
# macOS
pm2 start chat.js --name ob -- listen --on-message "osascript -e 'display notification \"{from}: {content}\" with title \"OceanBus\"'"

# Linux
pm2 start chat.js --name ob -- listen --on-message "notify-send 'OceanBus: {from}' '{content}'"

# Windows
pm2 start chat.js --name ob -- listen --on-message "msg %USERNAME% \"{from}: {content}\""
```

### 一个 Captain 指挥多个 CC（多窗口/多机器）

如果你同时开了好几个 Claude Code 窗口（同一台电脑不同项目、台式机、笔记本、服务器），每个都可以独立接收指令、各自回报，不会串。

**原理**：每个 CC 窗口注册独立的 OpenID。窗口名字自动取自**当前项目目录名**——`CC-oceanbus`、`CC-dashboard`、`CC-spider`。无需手动命名。

```
Captain 的 Bridge Roster:
  CC-oceanbus     → OpenID_aaa  (~/work/oceanbus)
  CC-dashboard    → OpenID_bbb  (~/work/dashboard)
  CC-spider       → OpenID_ccc  (~/personal/spider)
```

**每个 CC 窗口的设置**（在各自项目目录下执行，每次 setup 自动生成不同 OpenID）：

```bash
# 窗口1：在 oceanbus 项目目录
cd ~/work/oceanbus
git clone https://github.com/ryanbihai/ocean-chat.git && cd ocean-chat && npm install
node chat.js setup   # → OpenID_aaa

# 窗口2：在 dashboard 项目目录
cd ~/work/dashboard
git clone https://github.com/ryanbihai/ocean-chat.git && cd ocean-chat && npm install
node chat.js setup   # → OpenID_bbb
```

**Captain 在手机上加联系人**（用「发给你的 Claude Code，建立小龙虾连接.md」自动生成，复制粘贴即可）：

```
帮我安装 ocean-chat skill
加联系人 CC-oceanbus <OpenID_aaa>
加联系人 CC-dashboard <OpenID_bbb>
设置定时任务：每5分钟帮我自动检查OceanBus新消息，有消息立刻推送给我
```

**日常使用**（在微信里说）：

```
告诉 CC-oceanbus: 查一下 publish 的 bug
告诉 CC-dashboard: 修复登录页面样式
告诉 CC-spider: 重启爬虫
```

**CC 回复时带上 From 头**，自动标注来源（CC 根据 cwd 自动填充）：

```bash
# CC-oceanbus 窗口回复
node chat.js send Bridge --from CC-oceanbus "publish bug 修好了"

# CC-dashboard 窗口回复
node chat.js send Bridge --from CC-dashboard "登录样式已修复"
```

消息在手机端展示效果：

```
── CC-oceanbus (ob_abc...) · 14:30 ──
  CC-oceanbus → Captain
  publish bug 修好了

── CC-dashboard (ob_def...) · 14:32 ──
  CC-dashboard → Captain
  登录样式已修复
```

`→` 箭头让 Captain 一眼看清：哪个项目窗口发的、发给谁。

---

## 常见问题

| 问题 | 解决 |
|------|------|
| `pm2: command not found` | `npm install -g pm2` |
| `尚未注册` | 先跑 `node chat.js setup` |
| ClawBot 说找不到 skill | 对 ClawBot 说"你装了哪些 skill"，确认 ocean-chat 已装 |
| 消息延迟 | 正常（OceanBus 是邮箱模型，非 IM），2s 轮询 |
| 想停掉监听 | `pm2 stop ob` |
| 多个 CC 分不清谁回的 | 回复时加 `--from <名字>`，消息头自动标注来源 |
| 不同机器用同一 OpenID | 会导致消息被随机一台收取。每台独立 `setup` 即可 |

---

## 安全说明

- 所有消息 **端到端加密**（XChaCha20-Poly1305），OceanBus 平台不可读
- 身份基于 **Ed25519 密码学签名**，不可伪造
- 消息在服务器 **72 小时后自动删除**
- 代码开源（MIT），可自行审计

---

> 这就是 OceanBus 的用法之一。它本质上是一个 **AI Agent 间的通信协议**——
> 不只是你连 Claude Code，你还可以连医生 Agent、保险 Agent、游戏 Agent。
> 一个 OpenID，连通整个 Agent 互联网。
