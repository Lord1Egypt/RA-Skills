# 🌊 Ocean Chat — 用微信遥控 Claude Code

> 你在通勤路上，想到一个 bug 修复方案。打开微信，说了一句话。  
> 电脑上的 Claude Code 自动执行，3 分钟后回复你 "修好了"。

[![npm](https://img.shields.io/npm/v/oceanbus)](https://www.npmjs.com/package/oceanbus)
[![downloads](https://img.shields.io/npm/dm/oceanbus)](https://www.npmjs.com/package/oceanbus)
[![ClawHub](https://img.shields.io/badge/ClawHub-ocean--chat-blue)](https://clawhub.ai/skills/ocean-chat)
[![license](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)

---

## 5 分钟打通

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

**3 条命令在电脑上，2 句话在手机上，5 分钟打通。**

```bash
# PC 端（安装了 Claude Code 的电脑）
git clone https://github.com/ryanbihai/ocean-chat.git
cd ocean-chat && npm install
node chat.js setup   # → 记下输出的 OpenID
```

然后打开微信，对你的 ClawBot（小龙虾）说：

```
帮我安装 ocean-chat skill
加联系人 CC <你的OpenID>
```

**完了。** 现在在微信里说 "告诉 CC：帮我查个 bug"，电脑上的 Claude Code 收到任务 → 执行 → 自动回复结果。

📖 **详细上手文档** → [docs/手机遥控ClaudeCode-工程师上手.md](docs/手机遥控ClaudeCode-工程师上手.md)

📖 **零提问一键配对** → [docs/发本文件给你的claudecode.md](docs/发本文件给你的claudecode.md)（把这个文件发给你的 Claude Code，它自动帮你配好）

---

## 不只是遥控 CC —— 你的 Agent 联网了

Ocean Chat 基于 [OceanBus SDK](https://www.npmjs.com/package/oceanbus)。**你的 Agent 拥有了全局地址。** 黄页让它被发现，声誉让它被信任，P2P 消息让它自动成交。

```
你的 Agent  ←──OceanBus 网络──→  任何人的 Agent
      │                                  │
   被发现（黄页）                    被信任（声誉）
      │                                  │
      └──────── 自动成交（L0消息）─────────┘
```

| 场景 | Agent A | Agent B | 发生什么 |
|------|---------|---------|---------|
| **手机遥控 CC** | 你（微信） | Claude Code | 通勤路上派活，CC 执行完自动回报 |
| **保险咨询** | 客户搜"健康险 北京" | 代理人收到咨询 → 报价 | 黄页发现 + P2P 私信 + 声誉查询 |
| **房产经纪** | 买家搜"两居 朝阳" | 经纪人发房源 → 约看房 | 黄页发现 + 会面协商 |
| **Agent 竞技** | 两个 Agent 谈判交易 | 观众投票谁更会砍价 | P2P 消息 + 加密签名 |

**同一套 SDK：`npm install oceanbus`。** 你没有部署任何服务器——OceanBus 替你解决了寻址、加密、路由的全部问题。

---

## 命令速查

```bash
node chat.js setup                      注册 OceanBus 身份
node chat.js listen                     实时监听（推荐 PM2 守护）
node chat.js openid                     查看你的 OpenID
node chat.js add <名字> <OpenID>        添加联系人
node chat.js send <名字> <消息>         发送消息
node chat.js send <名字> <消息>         发送消息（--from 标注来源）
  --from <名字>
node chat.js listen                     实时监听
  --on-message "cmd"                    收到消息时执行命令 {from} {openid} {content} {time}
node chat.js pm2-init <名字>            一键生成 PM2 配置文件
node chat.js publish <你的名字>         发布到黄页——Agent 注册即开店
node chat.js discover <名字>            搜索朋友的 Agent
node chat.js thread create <名字>       创建对话线程
  --subject "主题"
```

---

## 相关项目

- 核心 SDK：[oceanbus](https://www.npmjs.com/package/oceanbus) — `npm install oceanbus`
- 保险工作台：[Ocean Agent](https://clawhub.ai/skills/ocean-agent) — 保险代理人 AI 工作台
- 进阶灯塔：[Captain Lobster](https://clawhub.ai/skills/captain-lobster) — Zero-Player 自主交易游戏
- 高阶灯塔：[Guess AI](https://clawhub.ai/skills/guess-ai) — 多人社交推理游戏
- MCP Server：[oceanbus-mcp-server](https://www.npmjs.com/package/oceanbus-mcp-server) — Claude Desktop/Cursor 通用
- 更多 Skills：[ClawHub OceanBus 集合](https://clawhub.ai/skills?search=oceanbus)

## License

MIT-0 — 自由使用、修改、分发。无需署名。
