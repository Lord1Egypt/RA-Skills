# Bottle Drift for OpenClaw

一个面向 OpenClaw 节点的互动式“漂流瓶” Skill。用户写下赠言，把它随机投递给**当前在线且已订阅漂流瓶频道**的节点；收件人可在网页控制台内直接回信，也可以通过专属链接回信；发送人会在自己的控制台或收件箱 API 中看到回信。

## 这次完善设计的关键结论

### 1) 不是只给脚本，而是给完整交互面
单纯命令行版只能验证链路，但不适合“漂流瓶”这种社交玩法。  
所以这版把 relay 升级成了**自带网页控制台**的服务，统一承载：

- 上线 / 心跳
- 发送漂流瓶
- 查看在线订阅者
- 查看收到的漂流瓶
- 直接回信
- 查看自己发出后的回信状态

### 2) 保留“特定链接回传”，但不把它当成唯一入口
你最初提出“收到的朋友也可以通过特定链接回传”，这个设计是对的，因为它门槛低、兼容性高。  
这版的做法是：

- **网页控制台**负责日常操作
- **专属 `reply_url`** 负责嵌入会话、消息卡片、外部页面

这样既满足原始需求，也补足了可视化操作体验。

### 3) 默认单次回信，更贴近“漂流瓶”语义
一个漂流瓶更像一次偶遇和一次回应，而不是无限聊天线程。  
因此当前默认策略是：**每次投递只允许回 1 次**。  
这能显著减少刷屏、重复提交和恶意灌水；如果你以后想扩成多轮对话，可以把 `replies.delivery_id UNIQUE` 放开。

## 当前架构

```text
浏览器控制台 / CLI
        │
        ▼
  Bottle Drift Relay (HTTP)
        │
        ├─ Presence: 在线心跳
        ├─ Send: 随机投递
        ├─ Inbox: 收件箱 / 发件箱 / 回信箱
        ├─ Reply URL: /r/{token}
        └─ SQLite: 持久化用户、瓶子、投递、回信
```

## 目录结构

```text
openclaw-bottle-drift-skill/
├─ SKILL.md
├─ README.md
├─ SELF_CHECK.md
├─ BUNDLE_MANIFEST.md
├─ scripts/
│  ├─ bottle_drift.py
│  └─ relay_server.py
├─ resources/
│  ├─ dashboard.html
│  ├─ dashboard.js
│  ├─ reply_page.html
│  └─ message_schema.json
├─ examples/
│  ├─ demo-session.md
│  └─ sample-bottle.json
└─ tests/
   └─ smoke-test.md
```

## 功能清单

- 内置网页控制台
- 在线用户心跳与在线状态判断
- 随机投递给当前在线订阅者
- 为每次投递生成独立 `reply_url`
- 控制台内直接回信
- 发件箱 / 收件箱 / 回信箱查询
- 过期时间、基础词过滤、频率限制
- 默认单次回信
- 可选回调 URL（若你的节点具备可访问的 webhook）

## 安装要求

- Python 3.10+
- 无第三方依赖
- 出站 HTTP 访问 relay
- 若要跨机器访问，请确保 relay 监听地址和反向代理正确配置
- 若需公网 `reply_url`，请使用 `--public-base-url` 指定外部可访问地址

## 快速开始

### 1) 启动 relay
```bash
python3 scripts/relay_server.py --host 127.0.0.1 --port 8765
```

启动后会输出：

```json
{
  "ok": true,
  "service": "bottle-drift-relay",
  "dashboard_url": "http://127.0.0.1:8765/"
}
```

### 2) 打开网页控制台
在浏览器访问：

```text
http://127.0.0.1:8765/
```

然后：

- 填写 `user_id`
- 填写展示昵称
- 选择是否接收新的漂流瓶
- 点击“保存并上线”

### 3) 发送漂流瓶
在“发送漂流瓶”面板填写赠言、投递人数、有效期后点击“扔出漂流瓶”。

### 4) 收件人回信
收件人有两种方式回信：

- 在控制台的“收到的漂流瓶”卡片里直接回信
- 打开该条漂流瓶的专属 `reply_url` 回信

### 5) 发件人查看回信
发件人在“收到的回信”与“我发出的漂流瓶”两块面板里看到回传结果。

## CLI 仍可用

### 心跳
```bash
python3 scripts/bottle_drift.py heartbeat --relay http://127.0.0.1:8765 --user-id alice --name "Alice"
```

### 发送
```bash
python3 scripts/bottle_drift.py send   --relay http://127.0.0.1:8765   --user-id alice   --name "Alice"   --message "愿你今天也有好心情。"
```

### 查看控制台地址
```bash
python3 scripts/bottle_drift.py dashboard --relay http://127.0.0.1:8765
```

### 查看收件箱
```bash
python3 scripts/bottle_drift.py inbox --relay http://127.0.0.1:8765 --user-id alice
```

## 输入输出示例

### `send` 输出示例
```json
{
  "ok": true,
  "bottle_id": "btl_82ab0fd7f1a90456",
  "deliveries": [
    {
      "delivery_id": "dly_9f07d96a8536fe6a",
      "recipient_id": "bob",
      "recipient_name": "Bob",
      "reply_token": "rpl_0f3bbef1f518c6a30d432c11",
      "reply_url": "http://127.0.0.1:8765/r/rpl_0f3bbef1f518c6a30d432c11"
    }
  ]
}
```

### `inbox` 输出示例
```json
{
  "ok": true,
  "user_id": "alice",
  "received_bottles": [],
  "sent_bottles": [
    {
      "bottle_id": "btl_82ab0fd7f1a90456",
      "reply_count": 1,
      "deliveries": [
        {
          "recipient_id": "bob",
          "recipient_name": "Bob",
          "has_reply": true
        }
      ]
    }
  ],
  "replies_received": [
    {
      "replier_name": "Bob",
      "reply_text": "也祝你今天顺利。"
    }
  ]
}
```

## 常见问题

### 为什么不直接“向所有在线 OpenClaw 用户群发”？
因为这取决于 OpenClaw 是否提供全局在线目录、统一身份、消息投递和深链回调等官方能力。  
在没有确认这些能力稳定可用之前，默认做“已订阅频道的在线用户随机投递”更稳妥，也更容易控制骚扰和滥用。

### 为什么网页里还要填 `user_id`？
当前版本没有接入统一登录系统，所以需要一个稳定标识来区分发件人和收件人。  
这个 ID 只做本系统内的逻辑键，不要求是真实名字。

### 为什么默认只能回 1 次？
因为这更符合漂流瓶“回传”的语义，也更利于控频。  
若你未来想扩成多轮对话，可在数据库约束和 UI 上放开。

### 能否接入真正的 OpenClaw 深链或官方消息？
可以。  
这版已经把投递层和展示层分开了。你后续只要替换 relay 的用户发现与消息投递部分，就能保留当前网页控制台和数据结构。

## 风险提示

- 当前网页身份保存在浏览器 localStorage，不适合作为强身份认证
- 公开部署时建议接 HTTPS、反向代理、IP 限流与更成熟的内容审核
- `reply_url` 具备一次回信能力，应视为敏感链接，不应任意公开扩散
- 当前过滤器仅为基础版，生产环境建议接专门审核服务

## 后续建议的增强方向

1. 接 OpenClaw 官方在线目录 / 消息接口
2. 增加黑名单、静音、举报
3. 增加节日主题瓶、匿名瓶、配对瓶
4. 增加审核后台与统计面板
5. 增加 WebSocket / SSE 实时更新
