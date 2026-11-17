<div align="center">

<h1 style="border-bottom: none">
  <b><a href="https://tourmind.com/skills">Hotel Booking AI</a></b><br />
  <strong>你的个人 AI 酒店搜索与预订助手</strong>
</h1>

<a href="https://auth.journione.ai/">
  <img alt="Hotel Booking AI——通过 AI Agent 搜索、比价并预订酒店" src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/hero/tourmind-booking-skills.png" style="width: 100%" />
</a>

<br />

<p align="center">
  找到更合适的住宿，比较实时价格，放心完成预订。
</p>

<br />

<div align="center">
  <a href="https://tourmind.com/skills">产品页面</a> |
  <span>在线演示</span> |
  <a href="https://tourmind.com">公司官网</a>
</div>

<br />

[![ClawHub 下载量](https://img.shields.io/badge/ClawHub_downloads-1.6k-F97316)](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
[![Skill 版本](https://img.shields.io/badge/Skill_version-1.0.8-2563EB)](SKILL.md)
[![许可证](https://img.shields.io/github/license/tourmind-com/Hotel-Booking-AI)](LICENSE)

</div>

<br />

<div align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.es.md">Español</a>
</div>

<br />

把你的 AI Agent 变成个人酒店预订助手。Hotel Booking AI 可搜索全球酒店资源，比较主流 OTA 与酒店供应商的实时房价，展示图片和取消政策，核验最终价格，并在同一次对话中协助完成预订、支付、取消和订单查询。

搜索酒店、查看酒店和房型详情、查询实时价格及核验库存均为公开能力——只有准备下单时才需要登录。

## 演示

### 1. 搜索有实时库存的酒店

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/search-en.gif" alt="Hotel Booking AI 实时酒店搜索演示" width="720" />
  </a>
</div>

### 2. 比较房型、图片和价格

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/detail-en.gif" alt="Hotel Booking AI 房型与价格比较演示" width="720" />
  </a>
</div>

### 3. 重新验价并安全支付

<div align="center">
  <a href="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif">
    <img src="https://skilloss.tourmind.com/skills/tourmind-booking/v1/demo/pay-en.gif" alt="Hotel Booking AI 预订与支付演示" width="720" />
  </a>
</div>

## 在一次对话中规划并预订住宿

- 按城市、酒店、地标、车站、地址、滑雪场或其他兴趣点搜索，不凭空编造坐标。
- 比较最多 20 家候选酒店，并从匹配实时房型的结果中选出最佳 5 家。
- 查看真实的每晚价格和入住总价，以及酒店与房型图片、床型、餐食、税费、取消政策和库存状态。
- 按预算、距离、星级、早餐、设施、房型或免费取消等实际需求筛选。
- 获取有数据依据的匹配理由，而不是泛泛的酒店推荐。
- 确认预订前，重新核验所选房型的准确价格和库存。
- 在同一次对话中创建预订，通过 Stripe、微信支付或支付宝付款，查询订单或取消符合条件的预订。

## 支持的 AI 客户端

| 客户端 | 使用方式 |
|---|---|
| OpenClaw | 从 ClawHub 直接安装，或将本仓库克隆到个人 Skills 目录 |
| WorkBuddy | 将本仓库安装或导入为用户 Skill |
| OpenAI Codex | 通过 Skills 界面或当前版本支持的本地 Skills 目录安装 |
| Claude Code | 作为个人 Skill 安装到 `~/.claude/skills` |
| 兼容 Agent Skills 的客户端 | 客户端能够加载根目录 `SKILL.md` 并发起 HTTPS `POST` 请求时可用 |
| 支持 MCP 的 AI 客户端 | 使用配套的 [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |

## 1 分钟安装

### 方式一：通过 ClawHub 安装

```bash
openclaw skills install @tourmind/hotel-booking-ai
openclaw gateway restart
```

### 方式二：从 GitHub 导入

在 AI 客户端的 Skills 界面中安装或导入以下仓库：

```text
https://github.com/tourmind-com/Hotel-Booking-AI.git
```

如果客户端从本地目录加载 Skill，请将仓库克隆到个人 Skills 目录：

```bash
CLIENT_SKILLS_DIR="<你的客户端 Skills 目录>"
mkdir -p "$CLIENT_SKILLS_DIR"
git clone https://github.com/tourmind-com/Hotel-Booking-AI.git "$CLIENT_SKILLS_DIR/hotel-booking-ai"
```

常见的个人 Skill 目录：

| 客户端 | 目录 |
|---|---|
| OpenClaw | `~/.openclaw/skills` |
| WorkBuddy | `~/.workbuddy/skills` |
| OpenAI Codex | 使用 Skills 界面或当前 Codex 版本支持的本地目录 |
| Claude Code | `~/.claude/skills` |

重新加载 Skills 或重启 AI 客户端，然后直接提出酒店需求即可。无需运行本地 MCP 服务；Hotel Booking AI 会通过 HTTPS 直接调用 TourMind API。

## 先搜索，准备预订时再登录

无需 `user_key` 即可搜索酒店、查看酒店与房型详情、比较实时价格并核验库存。

准备创建、查询、取消或支付订单时：

1. 使用 Google 登录 [auth.journione.ai](https://auth.journione.ai)。
2. 复制 `user_key`，并保存为已安装 `hotel-booking-ai` 目录下的 `user_key.txt`。开始订单操作时，AI Agent 也会引导你完成此步骤。
3. 在 macOS 或 Linux 上限制该文件的访问权限：

   ```bash
   chmod 600 user_key.txt
   ```

不要提交 `user_key.txt`。该文件已被 `.gitignore` 排除，应只保存在你的设备上。

## 示例提示词

```text
我和家人一共四人，计划在 2027 年 4 月 3 日至 4 月 7 日去东京。请找一间靠近车站、方便前往东京迪士尼、含早餐、可免费取消且总价不超过 120,000 日元的客房。比较 5 家最合适且有实时库存的酒店，展示图片、房型、床型、每晚价格、入住总价、交通取舍和取消截止时间。暂时不要预订。
```

```text
查看第 2 家酒店目前可订的房型，包括房间图片、床型、餐食、取消政策、每晚价格、入住总价以及是否可立即确认。推荐性价比最高的方案，但先等我选择。
```

```text
选择含早餐的大床房。重新核验准确价格、库存、税费、取消政策以及酒店现场可能收取的费用。展示最终预订摘要，并在创建订单或发起支付前等待我明确确认。
```

## Hotel Booking AI 的工作流程

```text
目的地、日期和住客信息
  → 解析城市、酒店或兴趣点
  → 搜索最多 20 家候选酒店
  → 查询匹配的实时房型
  → 排序并展示最佳 5 家已验证酒店
  → 展示酒店详情、房型图片和当前报价
  → 重新核验所选房型的价格与库存
  → 仅在用户明确确认后创建预订
  → 按需支付、查询或取消订单
```

初次酒店搜索中的价格仅用于筛选候选项。用于对比的价格来自匹配的实时房型，最终预订则使用库存核验接口返回的最新价格。

## 隐私、预订与支付

- 公开的酒店搜索和实时房价比较无需登录。
- 订单操作使用本地 `user_key.txt` 中的 `user_key`；请勿将其放入提示词、截图、日志、URL、Git 提交或 Issue。
- Hotel Booking AI 仅在即将创建已确认预订时要求住客法定全名和联系邮箱，不收集电话号码。
- 预订、取消和支付均为需要明确确认的操作；Agent 必须先展示相关信息并等待确认。
- TourMind 房价包含税费。少数目的地可能要求酒店在入住时另收城市税或旅游税；接口返回的强制费用会单独展示。
- 选择 Stripe 时会增加 3.5% 的支付处理费，同时支持微信支付和支付宝。
- 只读酒店结果链接仅能展示酒店和房型信息，不能预订、支付、取消或访问账户与财务页面。

## 选择合适的 TourMind 接入方式

| 用户类型 | 接入方式 | 鉴权模式 | 产品与仓库 |
|---|---|---|---|
| 消费者 / ToC | HTTP 直连 Skill | 搜索与验价公开；仅订单操作需要 `user_key` | **[Hotel-booking-ai](https://github.com/tourmind-com/Hotel-Booking-AI)** |
| 企业 / ToB | HTTP 直连 Skill | 每次 API 调用均需要 Skill Token | [Tourmind-booking-skill](https://github.com/tourmind-com/Tourmind-Booking-Skills) |
| 消费者 / ToC | MCP + 配套 Skill | 公开 MCP 连接；仅订单操作需要 `user_key` | [Hotel Booking AI MCP](https://github.com/tourmind-com/Hotel-Booking-AI-MCP) |
| 企业 / ToB | MCP + 配套 Skill | 使用 Bearer 鉴权的 MCP 连接 | [TourMind Booking MCP](https://github.com/tourmind-com/Tourmind-Booking-MCP) |

## API 与支持

**API 基础地址：** `https://api.tourmind.com`

| 接口 | 用途 | 是否需要登录 |
|---|---|---|
| `POST /skill/toc/check_skill_update` | 检查 Skill 更新 | 否 |
| `POST /skill/toc/search_location` | 解析地区、兴趣点或酒店 | 否 |
| `POST /skill/toc/search_hotels` | 搜索候选酒店 | 否 |
| `POST /skill/toc/get_hotel_detail` | 获取酒店详情和图片 | 否 |
| `POST /skill/toc/query_room_rates` | 获取实时房型和价格 | 否 |
| `POST /skill/toc/check_room_availability` | 重新核验所选价格和库存 | 否 |
| `POST /skill/toc/create_booking` | 确认后创建预订 | 是 |
| `POST /skill/toc/query_booking` | 查询订单 | 是 |
| `POST /skill/toc/cancel_booking` | 确认后取消符合条件的订单 | 是 |
| `POST /skill/toc/pay_order` | 确认后发起支付 | 是 |

- 请求字段、响应契约、排序、图片、税费及预订规则：[references/parameter_guide.md](references/parameter_guide.md)
- 从 ClawHub 安装：[Hotel Booking AI](https://clawhub.ai/tourmind/skills/hotel-booking-ai)
- GitHub 支持：[提交 Issue](https://github.com/tourmind-com/Hotel-Booking-AI/issues)
- TourMind 客服：`+86-755 3665 4666`
- 酒店业务支持：`hotel@tourmind.com`
- AI 产品合作：`ai@tourmind.com`

## 开源许可

[MIT](LICENSE) © 2026 TourMind
