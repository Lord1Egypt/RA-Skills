# hello-hitch-skill

让 AI Agent 帮你叫顺风车——从询价到下车，全程对话完成。

**ClawHub**: [hello-hitch-skill](https://clawhub.ai/zhujianjie-kevin/hello-hitch-skill) · **平台**: [哈啰 AI 开放平台](https://aiopen.hellobike.com)

## 30 秒体验

```bash
# 1. 安装
openclaw skill install hello-hitch-skill

# 2. 配置（在 Agent 对话中说）
你: 我的 API Key 是 xxxxxx

# 3. 开始
你: 顺风车从西溪湿地到杭州东站
```

> API Key 在 [哈啰 AI 开放平台](https://aiopen.hellobike.com) 登录后获取。

## 能做什么

```
你: 从西溪湿地到灵隐寺多少钱？        → 询价，展示拼座/独享/特惠多种运力价格
你: 选拼座，等 30 分钟                 → 下单，开始匹配顺路车主
你: 帮我看看有哪些司机                 → 展示附近车主评分、车型、顺路度
你: 邀请王师傅                         → 向指定车主发送邀请
你: 司机到哪了                         → 实时位置 + 预计到达时间
你: 到了                               → 确认到达，完成行程
你: 明天 9 点顺风车去机场              → 预约出行（定时自动发单）
你: 记住我家在文三路 123 号            → 保存地址，下次直接说"回家"
```

## 顺风车特有能力

区别于网约车打车类 Skill，本技能围绕顺风车场景提供以下差异化能力：

| 能力 | 说明 |
|------|------|
| **运力选择** | 拼座、独享、特惠独享等多种运力，支持同时选择多种（如"拼座+独享"同时发单） |
| **邀请车主** | 查看附近顺路车主列表（含评分、车型、顺路度），主动邀请加速匹配 |
| **等待时长** | 自定义愿等时间（1~180 分钟），灵活平衡等待与匹配成功率 |
| **双向确认** | 乘客侧确认上车 / 确认到达，完成履约闭环 |
| **多端跳转** | 生成哈啰 App Deep Link 或微信小程序链接，覆盖不同使用场景 |

## 工具清单

| 工具 | 用途 | 需确认 |
|------|------|--------|
| `maps_textsearch` | 关键词搜索 POI，获取坐标 | |
| `hitch_estimate_price` | 询价，获取运力列表和预估价 | |
| `hitch_create_order` | 创建顺风车订单 | ✓ |
| `hitch_query_order` | 查询订单状态 | |
| `hitch_cancel_order` | 取消订单 | ✓ |
| `hitch_invite_driver_list` | 获取附近顺路车主列表 | |
| `hitch_invite_driver` | 邀请车主接单 | ✓ |
| `hitch_get_driver_location` | 查询司机实时位置 | |
| `hitch_pax_confirm_get_on_car` | 乘客确认上车 | ✓ |
| `hitch_pax_confirm_reach_destination` | 乘客确认到达 | ✓ |
| `hitch_generate_app_link` | 生成 App 跳转链接 | |
| `hitch_generate_wechat_link` | 生成微信小程序链接 | |

## 配置方式

### OpenClaw 安装（推荐）

```bash
openclaw skill install hello-hitch-skill
```

安装后配置 MCP 连接：

```bash
openclaw mcp set hitch-ai-platform '{"url":"https://hellohitchapi.hellobike.com/ai-openplatform/mcp","headers":{"Authorization":"YOUR_API_KEY"},"transport":"streamable-http"}'
openclaw gateway restart
```

### 手动编辑配置文件

编辑 `~/.openclaw/openclaw.json`，在 `mcpServers` 下添加：

```json
{
  "mcpServers": {
    "hitch-ai-platform": {
      "url": "https://hellohitchapi.hellobike.com/ai-openplatform/mcp",
      "headers": {
        "Authorization": "YOUR_API_KEY"
      },
      "transport": "streamable-http"
    }
  }
}
```

编辑后执行 `openclaw gateway restart` 使配置生效。

## 对话示例

### 询价 + 下单

```
用户: 明天下午 3 点从杭州东站到西湖，顺风车多少钱？

Agent: 杭州东站 → 西湖，约 12 公里，以下运力可选：
       1. 拼座 — 约 18 元
       2. 独享 — 约 32 元
       请回复编号选择（可多选如"1 2"，或回复"全选"）

用户: 1 2

Agent: 你愿意等多久？（默认 10 分钟，最长 180 分钟）

用户: 30 分钟

Agent: ✅ 顺风车订单已发出！
       📋 订单号: HB20260409xxxxx
       📍 杭州东站 → 西湖
       🎫 运力: 拼座 + 独享
       💰 预估: 18~32 元
       ⏳ 等待时长: 30 分钟
       正在为您匹配顺路车主...
```

### 邀请车主

```
用户: 帮我看看有哪些司机

Agent: 找到 3 位顺路车主：
       1. 张师傅 ⭐4.9 | 白色本田雅阁 | 顺路 85%
       2. 李师傅 ⭐4.7 | 黑色大众帕萨特 | 顺路 72%
       3. 王师傅 ⭐4.8 | 银色丰田凯美瑞 | 顺路 90%
       要邀请哪位？

用户: 王师傅

Agent: 已向王师傅发送邀请，等待确认中。
```

### 行程跟踪

```
用户: 司机到哪了？

Agent: 王师傅当前距您约 2.3 公里，预计 5 分钟到达上车点。
```

## 项目结构

```
hello-hitch-skill/
├── SKILL.md                       # Agent 执行入口（触发、流程、约束）
├── README.md                      # 本文件
└── references/
    ├── operations.md              # 各场景操作命令详情
    └── api.md                     # 工具签名、参数、返回值、错误码
```

## 服务范围

支持哈啰顺风车运营的所有中国大陆城市。

## 相关链接

- [哈啰 AI 开放平台](https://aiopen.hellobike.com) — 获取 API Key、查看文档
- [ClawHub](https://clawhub.ai/zhujianjie-kevin/hello-hitch-skill) — 安装 Skill
- [API 参考](references/api.md) — 工具签名与参数定义
- [操作手册](references/operations.md) — 各场景执行命令
