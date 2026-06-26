# @huo15/wechat-service

<hr>

<p align="center">
  <strong>打破信息孤岛，用一套系统驱动企业增长</strong><br>
  <strong>加速企业用户向全场景人工智能机器人转变</strong>
</p>

<table align="center" border="1" cellpadding="6">
  <tr><td>🏫 教学机构</td><td>逸寻智库</td></tr>
  <tr><td>👨‍🏫 讲师</td><td>Job</td></tr>
  <tr><td>📧 联系方式</td><td>support@huo15.com</td></tr>
  <tr><td>💬 QQ群</td><td>1093992108</td></tr>
  <tr><td>📺 配套视频</td><td>B站视频：<a href="https://space.bilibili.com/400418085">https://space.bilibili.com/400418085</a></td></tr>
</table>

<p align="center">
  <a href="https://www.npmjs.com/package/@huo15/wechat-service"><img src="https://img.shields.io/npm/v/@huo15/wechat-service?style=flat-square&logo=npm&color=blue" alt="npm" /></a>
  <a href="https://clawhub.ai/skills/huo15-openclaw-wechat-service"><img src="https://img.shields.io/badge/ClawHub-published-orange?style=flat-square" alt="ClawHub" /></a>
  <img src="https://img.shields.io/badge/OpenClaw-2026.3.23%2B-green?style=flat-square" alt="OpenClaw" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/Status-v2.3.x%20Stable-success?style=flat-square" alt="Stable" />
</p>

<hr>

## 📖 正文内容

> **OpenClaw 微信服务号（公众号）渠道插件**：把微信公众号变成你的 AI 协作入口。
> 一粉一会话隔离 · 12 个 agent tool · 覆盖 60+ 个微信公众平台官方 API · 多账号矩阵路由 · 知识库双写

```
@huo15/wechat-service v2.3.3
└─ 12 个 agent tool / 60+ 个 WeChat MP API / 架构按 @huo15/wecom 同构
```

### ✨ 能力总览

| 维度 | 说明 |
|------|------|
| **🚀 一粉一会话**（v2.3.0+ 默认开启） | 动态 Agent 派生：每个 openid 自动一个独立 agent + 独立 session / 记忆；管理员名单可旁路 |
| **📨 消息全栈** | 客服消息（10 类）/ 模板消息（CRUD + 公模板库）/ 一次性 + **长期订阅通知** |
| **📰 内容发布** | 素材管理 + 草稿箱 + `freepublish` 流水线 + 群发（按标签/openid，预览，撤回） |
| **🔐 网页授权** | OAuth2.0 全流程（snsapi_base / snsapi_userinfo） + JS-SDK 签名 |
| **📊 数据分析** | datacube 17 项指标（用户增减、图文阅读分享、消息分析、接口调用） |
| **🤖 智能开放** | OCR 7 类（身份证/银行卡/驾驶证/行驶证/营业执照/车牌/通用） + 图像处理 3 项 |
| **🎫 卡券精简** | create / get / batchget / delete / consume / decrypt encrypt_code |
| **🧠 多账号矩阵** | `accounts.<id>` 隔离 webhook 路径、access_token、agent 路由 |
| **🛡️ 权限控制**（v2.1.0+） | `permissionMode=admin-only` / `role-based`（5 级角色） + AI 对话护栏（v2.2.0） |
| **💾 知识库双写** | 本地 markdown（Karpathy 风格）+ Odoo `knowledge.article` 同步；同时支持 `~/.openclaw/kb/shared/wiki/` 共享 KB 跨 agent 检索 |
| **🤖 内置 persona 预设**（v2.3.0+） | 开箱即用 system instructions：`it-support` 通用 IT 客服 / `huo15-customer` 火一五·逸寻智库专属客服（含 6 产品 4 服务转化路径） |
| **🪄 菜单事件短路**（v2.3.0+） | CLICK / VIEW / scancode_* / pic_* 等 8 类菜单事件默认不入 agent（粉丝不被骚扰），仅 `routing.events.<key>` 显式配置时走 |
| **✍️ Markdown 自动降级**（v2.3.0+） | LLM 输出的 `**bold**` `# 标题` `- list` `[txt](url)` 自动转成微信 text 友好排版（公众号 text 不渲染原生 markdown）。下沉到 `sendCustomerServiceMessage` 底层，5 条 outbound 路径全覆盖（v2.3.1） |
| **🔁 自动回复**（v2.2.0+ / v2.3.3 强化） | 关注欢迎语 `welcomeText` + 关键词触发 `keywords`（**v2.3.3 新增 glob 通配** `*xx*` / `prefix*` / `*suffix`）+ 业务时间 `businessHours` |

---

### 📦 安装

```bash
# 通过 OpenClaw 安装（推荐）
/install @huo15/wechat-service

# 或直接 npm
npm install @huo15/wechat-service
```

### 🚀 初始化

**方式 A — 交互式向导（推荐）**

```
/setup wechat-service
```

向导收集：AppID / AppSecret / 服务器 Token / EncodingAESKey / 加密模式 / 原始 ID / 账号名。完成后会回显 webhook URL 和公众号后台需要填的字段。

**方式 B — CLI 非交互式（v2.0.0+，适合 CI / Docker）**

```bash
export WECHAT_SERVICE_APP_ID="wx1234567890"
export WECHAT_SERVICE_APP_SECRET="xxx"
export WECHAT_SERVICE_ENCODING_AES_KEY="x_x_43_chars_x"

openclaw channels add --channel wechat-service --name "我的公众号" --token "MY_TOKEN"
```

非 default 账号用 `WECHAT_SERVICE_<UPPER_ACCOUNTID>_APP_ID` 这种带 accountId 前缀的 env：

```bash
export WECHAT_SERVICE_SHOP_A_APP_ID="wx_shop_a"
openclaw channels add --channel wechat-service --account shop-a
```

### 🔌 Webhook URL

主路径：

```
https://你的域名/plugins/wechat-service/{accountId}
```

兼容路径：`/wechat-service/{accountId}`。填到「微信公众平台 → 基本配置 / 开发者中心 → 服务器配置 → URL」，Token / EncodingAESKey 与配置保持一致即可。保存时公众平台发的 `GET echostr` 校验，插件自动响应（明文 + 安全模式都支持）。

---

### ⚙️ 配置 Schema

```yaml
channels:
  wechat-service:
    enabled: true
    defaultAccount: default

    # ① 多账号矩阵
    accounts:
      default:
        enabled: true
        name: 我的公众号
        appId: wx1234567890abcdef
        appSecret: ${WECHAT_SERVICE_APP_SECRET}
        token: ${WECHAT_SERVICE_TOKEN}
        encodingAESKey: ${WECHAT_SERVICE_AES_KEY}
        encryptMode: safe              # plain | compatible | safe
        originalId: gh_xxxxxxxxxx       # 可选
        replyMode: async                # async（默认）/ passive
        replyPlaceholderText: "收到，正在为你处理..."   # async 模式占位
        welcomeText: 欢迎关注！

        # ② 静态事件路由
        routing:
          defaultAgent: wechat-agent
          events:
            subscribe: onboarding-agent
            CLICK: menu-agent
            TEMPLATESENDJOBFINISH: webhook-agent

        # ③ 知识库双写
        knowledgeSync:
          enabled: true
          localPath: ~/knowledge/huo15
          odoo:
            url: https://huo15.com
            db: huo15
            username: bot@huo15.com
            password: ${ODOO_PASSWORD}
            articleParentId: 123        # 可选

    # ④ 🆕 v0.2.0 动态 Agent 派生（与 @huo15/wecom 同构）
    dynamicAgents:
      enabled: true                     # v2.3.0 起默认 true（每位粉丝独立 agent）
      dmCreateAgent: true               # 每个 openid 一个 agent
      groupEnabled: false               # 公众号无群聊；保留是为了与 wecom schema 对齐
      adminUsers:                       # 管理员 openid：旁路动态路由 + admin-only 模式可执行写操作
        - oABC123xyz
      # 🆕 v2.1.0 权限控制
      permissionMode: open              # "open"（默认）/ "admin-only" / "role-based"
      # 🆕 v2.3.0 默认 persona preset（动态 agent 的 system instructions）
      defaultInstructionsPreset: huo15-customer   # 'it-support' / 'huo15-customer' / 'none'

    # ⑤ 🆕 v2.2.0 自动回复（关注欢迎语 / 关键词触发 / 业务时间）—— 详见下方独立章节
    autoReply:
      welcomeText: "欢迎关注！..."
      keywords:
        "你好": "你好呀 👋"
        "*Odoo*": "聊 Odoo 找对人了..."   # v2.3.3 glob 通配
      businessHours:
        timezone: Asia/Shanghai
        schedule:
          - { days: [1,2,3,4,5], start: "09:00", end: "18:00" }

    network:
      egressProxyUrl: ''
      timeoutMs: 15000
```

**Agent ID 命名**（动态 Agent）：`wechat-service-{accountId}-dm-{sanitized_openid}`，例：`wechat-service-default-dm-oabc123xyz`。

---

### 🔗 顶层 `bindings`（**必须配！**）

> ⚠️ **不配 binding，agent 跑完后回复消息会被静默丢弃**（OpenClaw 找不到 channel→agent 的反向路由）。这是最常踩的坑。

`bindings` 在 OpenClaw 顶层（不在 `channels.wechat-service` 里），把 channel + accountId 映射到 agent：

```jsonc
// ~/.openclaw/openclaw.json 顶层
{
  "bindings": [
    {
      "agentId": "main",
      "match": { "channel": "wechat-service", "accountId": "default" }
    }
  ]
}
```

**多账号 / 多渠道场景**：每个 `<channel>:<accountId>` 都要单独一条 binding：

```jsonc
"bindings": [
  { "agentId": "main",          "match": { "channel": "wecom",          "accountId": "default" } },
  { "agentId": "main",          "match": { "channel": "wechat-service", "accountId": "default" } },
  { "agentId": "shopa-agent",   "match": { "channel": "wechat-service", "accountId": "shop-a"  } },
  { "agentId": "support-agent", "match": { "channel": "wechat-service", "accountId": "support" } }
]
```

`agentId: "main"` 是 OpenClaw 默认 agent，不需要在 `agents.list` 显式注册。其他自定义 agent 要先注册：

```jsonc
"agents": {
  "list": [
    { "id": "main" },
    { "id": "shopa-agent" },
    { "id": "support-agent" }
  ]
}
```

---

### 📨 回复模式详解（`replyMode` + `replyPlaceholderText`）

公众号 webhook 协议要求 **5 秒内**返回响应，但 LLM 通常要 5–30 秒才能产出回复。Plugin 提供两种模式应对：

#### 模式 A：`async`（**默认，推荐**）

```yaml
accounts:
  default:
    replyMode: async                                # 默认值
    replyPlaceholderText: "收到，正在为你处理..."     # 默认值
```

行为：
1. webhook 收到消息 → **立即** 返回**被动回复 XML 含 placeholder 文本** → 粉丝立刻看到 "收到，正在为你处理..."
2. 后台异步跑 agent → agent 产出回复 → 通过**客服消息接口**（`customservice/send`）push 第二条给粉丝
3. 粉丝在微信里看到两条消息：先是 placeholder（瞬间到达），然后是 agent 真回复（几秒后）

**自定义 placeholder**：

```yaml
replyPlaceholderText: "🤖 AI 助手收到啦~ 正在思考中，请稍候 5-10 秒"
```

**关掉 placeholder（回到 v2.1.0 之前的行为）**：

```yaml
replyPlaceholderText: ""    # 空字符串 → 不发占位，立即返 success
```

#### 模式 B：`passive`（5 秒内必须出结果，否则降级）

```yaml
replyMode: passive
```

行为：5 秒内如果 agent 已经产出 text，则把整段回复打包成被动回复 XML 直接返回（粉丝只看到一条消息，无延迟）；超时则**降级到 async 模式**（同上）。

适合：纯模板回复 / 关键词路由 / 缓存命中 等**确定能 5 秒内完成**的场景。LLM 推理建议留在 `async`。

#### Event 类回调不会发 placeholder

关注/扫码/菜单点击等 `event` 类回调始终返回 `"success"`，避免微信侧把被动回复 XML 当事件确认从而触发额外重发。日志区分：

```
acked(placeholder)  ← user message + async + 占位生效
acked(success)      ← event 类回调 / passive 模式 / 占位关闭
```

---

### ⏰ 客服消息「48 小时窗口」硬性约束

微信平台规则（不是 plugin 限制）：

- 粉丝**主动**给公众号发完消息后，公众号有 **48 小时**窗口可以用 `customservice/send` 主动回复
- 超过 48 小时**禁用**客服消息接口（`errcode: 45015`）；想发就要走**模板消息**或**订阅消息**（且粉丝事先订阅过）
- 关注事件 / 扫码事件 / 点击菜单 也开 48h 窗口

实务建议：
- agent **回复**走 `async` 模式 + 客服消息（48h 内绝对够用）
- **主动通知**（超 48h、或粉丝从未交互）必须用模板消息（`wechat_service_message send_template`）或长期订阅通知（`send_subscribe`）

---

### 🛠️ Agent Tools（12 个）

| Tool | 主要 action |
|------|-------------|
| `wechat_service_menu` | create / get / delete / create_conditional / delete_conditional / try_match |
| `wechat_service_message` | 客服消息（10 类）+ 模板消息 CRUD + **公模板库** + 一次性订阅 + **长期订阅通知**（共 25 个 actions） |
| `wechat_service_material` | 临时/永久素材上传、图文素材、列表、删除 |
| `wechat_service_article` | 草稿箱 CRUD + freepublish 发布流水线（含 describePublishStatus） |
| `wechat_service_user` | 用户信息 / 粉丝列表 / 标签 CRUD / 黑名单 / 备注 |
| `wechat_service_qrcode` | create（temp_id/temp_str/perm_id/perm_str）+ gen_shortkey + fetch_shortkey |
| `wechat_service_mass_send` | 按标签 / openid 列表 / 预览群发 + 速度控制 + 撤回 |
| `wechat_service_jssdk` | sign（JS-SDK config）/ get_ticket / invalidate_ticket |
| **`wechat_service_oauth`** 🆕 v0.4.0 | build_authorize_url / code_to_token / refresh_token / userinfo / validate |
| **`wechat_service_analytics`** 🆕 v0.4.0 | list_metrics + query metric:`<name>` —— 17 项 datacube 指标 |
| **`wechat_service_intelligent`** 🆕 v1.0.0 | list_visions + run vision:`<name>` —— OCR 7 类 + 图像 3 项 |
| **`wechat_service_card`** 🆕 v1.0.0 | create / get / batchget / delete / consume / decrypt（卡券精简） |

所有 tool 都支持 `accountId` 参数；不传时使用当前 agent 绑定的账号或 `defaultAccount`。未配置账号会直接返回结构化错误（`isError=true`）。

---

### 🎯 v0.2 → v2.3 演进路线（已落地）

```
v0.1.0  初始版本（消息/菜单/素材/草稿/用户/标签/二维码/JS-SDK/群发）
v0.2.0  ✅ Phase 0   动态 Agent 框架（模仿 @huo15/wecom）
v0.3.0  ✅ Phase 1   通知能力补全（模板消息 CRUD + 长期订阅通知）
v0.4.0  ✅ Phase 2   网页授权 OAuth + 数据统计 datacube
v1.0.0  ✅ Phase 3   智能开放 OCR/图像 + 卡券精简版
v1.0.1  🩹 Bugfix    channel id / config key kebab-case 对齐
v2.0.0  🏗️ 架构升级  src/ 按 @huo15/wecom 同构 + account-runtime + setup.applyAccountConfig
v2.1.0  🛡️ 权限层    permissionMode=admin-only：写操作仅 main agent / adminUsers
v2.1.1  🩹 UX        async 模式立即返 placeholder 占位回复
v2.2.0  🎭 角色权限  permissionMode=role-based + AI 对话护栏 + 自动回复（welcomeText + keywords + businessHours）
v2.2.4  🪪 manifest  注册 contracts.tools 适配 OpenClaw 2026.5.x loader 契约
v2.3.0  🎉 客服化    菜单事件短路（CLICK/VIEW 默认不入 agent）+ markdown 自动降级 + 动态 agent 默认开启 + 内置 it-support persona preset
v2.3.1  🛠️ Hotfix    markdown 渲染下沉到 sendCustomerServiceMessage 底层（5 条 outbound 路径全覆盖）+ 表格降级 + 幂等保护
v2.3.2  💼 行业 preset  新增 huo15-customer persona（火一五·逸寻智库公众号专属：6 产品 4 服务 + 课程库 + 留资转化路径）+ 6 份共享 KB md
v2.3.3  🔁 关键词通配  matchKeyword 支持 glob `*xx*` / `prefix*` / `*suffix`（大小写不敏感）+ README 自动回复实战章节  ← 当前 latest
```

详细变更见 [`CHANGELOG.md`](./CHANGELOG.md)。

---

### 🔁 自动回复实战（v2.2.0+ / v2.3.3 强化）

`autoReply` 是 "AI agent 之前的一道快速通道"——命中关键词 / 业务时间 / subscribe 事件时直接发固定文本，**不调 LLM 省 token**。适合：高频问候、留资引导、产品索引、联系方式速查。

#### 1) `welcomeText`：关注后欢迎语

```yaml
channels:
  wechat-service:
    autoReply:
      welcomeText: |
        欢迎来到「逸寻智库」👋  我是火一五（Huo15）的 AI 客服。

        我能帮你：
        • 介绍公司 6 大产品（辉火云企业套件/管家、XR-IoT、机器视觉、镜像世界、逸寻智库）
        • 答 IT 技术问题（Odoo / AI / 前端 / 鸿蒙 / Web3 / 视觉 AI）
        • 答工商管理问题（ERP / 中国本地化 / 数字化转型 / 合规）
        • 推荐学习课程：https://chatai.huo15.com/slides

        试试发：「Odoo」「AI」「价格」「演示」「课程」「联系」给我。

        📺 B 站「逸寻智库」UID 400418085 也有免费视频。
```

支持变量：
- `{{nickname}}` → 粉丝昵称（如能拿到）
- `{{date}}` → 当前日期 `YYYY-MM-DD`

#### 2) `keywords`：关键词命中回复（v2.3.3 起支持 glob 通配）

匹配优先级：**先 exact 全扫一遍未命中再扫通配**——这样运营可以「精确短句走快回复 + 通配模糊兜底」。

| 配置 key 写法 | 匹配模式 | 命中示例 |
|------|------|------|
| `"你好"` | exact 完全匹配（旧版语义） | "你好" ✓；"你好吗" ✗ |
| `"*Odoo*"` | contains 包含（**大小写不敏感**） | "Odoo 怎么学"、"ODOO" 都 ✓ |
| `"价格*"` | prefix 前缀 | "价格多少" ✓；"问下价格" ✗ |
| `"*多少钱"` | suffix 后缀 | "Odoo 实施多少钱" ✓ |

实战配置（逸寻智库公众号 43 组）：

```yaml
channels:
  wechat-service:
    autoReply:
      keywords:
        # === 高频问候（exact）===
        "你好":   "你好呀 👋 我是「逸寻智库」AI 客服..."
        "您好":   "您好 👋 ..."
        "hi":     "Hi！..."
        "在吗":   "在的 👋 我是 AI 客服，7×24 在线..."
        "你是谁": "我是「逸寻智库」AI 客服..."

        # === 联系方式（exact，秒回）===
        "联系":   "📞 18554898815 / postmaster@huo15.com / QQ 群 1093992108"
        "客服":   "我就是 AI 客服 👋 转人工：18554898815"
        "电话":   "18554898815（同微信）"
        "微信":   "加微信 18554898815..."

        # === 课程 / 学习（exact）===
        "课程":   "📚 https://chatai.huo15.com/slides\n热门课程：Odoo19 实施..."
        "学习":   "想学什么？回复 Odoo / Android / AI..."
        "B站":    "https://space.bilibili.com/400418085"
        "视频":   "B 站「逸寻智库」https://space.bilibili.com/400418085"

        # === 产品引流（exact，列清单）===
        "产品":   "火一五 6 大产品：1. 辉火云企业套件 2. 辉火云管家 3. XR-IoT 4. 机器视觉质检 5. 镜像世界 Web3.0 6. 逸寻智库"
        "服务":   "火一五 4 大服务：Odoo 实施 / OpenClaw 增强 / 安全架构 / 高校 XR"
        "ERP":    "ERP 推荐：辉火云企业套件（Odoo 10~19）..."
        "AI":     "AI 推荐：辉火云管家 + OpenClaw 增强服务..."
        "XR":     "XR 推荐：XR-IoT 平台 + 高校 XR 定制..."

        # === 留资（exact）===
        "演示":   "🎬 留下姓名+公司+联系方式+想看哪款，运营 24h 内回访"
        "报价":   "报价按需求评估，请留信息，运营给方案..."
        "?":      "我能聊 IT / 管理 / 产品 / 课程。试试发「Odoo」「AI」「演示」给我"

        # === 通配兜底（v2.3.3+，contains）===
        "*多少钱*": "具体报价按需求评估，请留：姓名+公司+联系方式+行业+产品..."
        "*价格*":   "具体价格按方案定，公众号不直接报价..."
        "*Odoo*":   "聊 Odoo 找对人了 ✨  火一五 10 年 Odoo 经验..."
        "*怎么学*": "学习路径：先看 B 站免费片段 → 再来逸寻智库系统学..."
        "*合作*":   "想合作？欢迎 🤝  请说说你公司的方向 / 痛点..."
```

**经验法则**：
- exact 关键词 ≤ 20 组：高频问候 / 一句问出来的标准化问题（"联系"、"产品"、"课程"）
- 通配关键词 ≤ 10 组：模糊兜底（"*Odoo*"、"*价格*"、"*怎么学*"）
- 其他全部留给 LLM agent + 知识库（共享 KB / 模型记忆）

#### 3) `businessHours`：业务时间提示

```yaml
autoReply:
  businessHours:
    timezone: Asia/Shanghai
    schedule:
      - { days: [1,2,3,4,5], start: "09:00", end: "18:00" }
    # offHoursMessage 留空 = 非工作时间也走 LLM（推荐：AI 客服 7×24 在线）
    # offHoursMessage: "您现在咨询的是非工作时间..."  ← 配上 = 非工作时间短路 LLM 只发这句
```

`days` 用 ISO 周几（0=周日 ~ 6=周六）。**配了 `offHoursMessage` 会短路 LLM**——非工作时间所有 text 消息只发这句话，不调 agent。客服场景一般留空让 AI 7×24 答。

#### 自动回复执行顺序

```
inbound text
  ├─ subscribe 事件 → welcomeText（如配）
  ├─ keywords 命中（exact 优先）→ 直接发 reply，不调 LLM
  ├─ businessHours.offHoursMessage（如配且非工作时间）→ 直接发，不调 LLM
  └─ 都未命中 → 走 dispatcher → agent（含 huo15-customer persona + 共享 KB）
```

---

### 🤖 内置 Persona Preset + 共享 KB（v2.3.0+）

动态 agent 派生时自动注入"开箱即用"的 system instructions。不写 prompt 也能直接当客服用。

#### 内置 preset

| preset 名 | 适合场景 | 内容速览 |
|------|------|------|
| `it-support`（默认） | 通用 IT 学习陪伴客服（开源 / 教学 / 个人公众号） | Python / 前端 / Odoo / AI / DevOps 全栈白名单 + 不答清单 + 回答结构 |
| `huo15-customer` | 火一五·逸寻智库 公众号专属 | 6 大产品 + 4 大服务介绍 + 课程库 / B 站 链接 + 留资转化 4 步路径 + IT / 工商管理 白名单 |
| `"none"` / `"off"` | 不注入 persona | 走 OpenClaw 默认 agent 行为，自己写 instructions |

切换：

```yaml
channels:
  wechat-service:
    dynamicAgents:
      enabled: true
      defaultInstructionsPreset: huo15-customer   # ← 切到逸寻智库客服
```

#### 共享 KB（跨 agent 检索）

在 `~/.openclaw/kb/shared/wiki/*.md` 下的 markdown 会被 OpenClaw 自动索引成 `corpus="kb"`，**所有动态 agent 都能搜到**——不需要每个 agent 复制一份私有 KB。

火一五开箱即用 6 份共享 KB（配合 `huo15-customer` preset 用）：

```
~/.openclaw/kb/shared/wiki/
├── huo15-公司概览.md           # 基本信息 / Mission / 客户画像 / 联系方式
├── huo15-6大产品.md            # 6 大产品定位 / 适合谁 / 推荐路径表
├── huo15-4大服务.md            # 4 大服务交付内容 / 周期 / 价格沟通流程
├── huo15-IT技术知识范畴.md      # IT 领域白名单 + 不答清单
├── huo15-工商管理知识范畴.md    # ERP / 中国本地化 / 数字化转型 / 合规
└── huo15-逸寻智库课程库.md      # 5 门课程详情 + B 站 + 学习路径
```

维护：直接编辑 md 文件即可，OpenClaw 自动重新索引，**不需要发版**。

#### 自定义 instructions

如果内置 preset 不够用，覆盖单个 agent 的 `instructions` 字段（OpenClaw 标准做法）：

```jsonc
"agents": {
  "list": [
    { "id": "main" },
    {
      "id": "wechat-service-default-dm-oABC123",
      "instructions": "你是 ACME 公司的 AI 客服...自定义 prompt"
    }
  ]
}
```

或者新增 4 份 persona md 到 `templates/personas/<your-preset>/{soul,identity,user,agents}.md` 作为运维参考资产，再在 PR 加进 `BUILT_IN_PERSONAS` 注册表（参考 [`src/shared/personas/it-support.ts`](src/shared/personas/it-support.ts)）。

---

### 🛡️ 权限模型（v2.1.0+）

公众号的 12 个 agent tool 共 80+ 个 action，按副作用分两类：

| 类别 | 例子 | admin-only 模式下谁能调 |
|------|------|-------------------------|
| **read（读）** | `list_templates` / `get_info` / OCR / OAuth flow / `analytics.query` | 所有 agent（主 agent 和粉丝的动态 agent 都可） |
| **write（写）** | `send_text`（给任意 openid）/ `mass_send.*` / `menu.create` / `card.create` / `article.publish` / 模板&订阅消息发送 | **仅** main agent / `adminUsers` 列表 / OpenClaw owner |

**重点：粉丝跟公众号的"自然对话"不受影响** —— agent 收到入向消息后的回复走 `dispatcher` 直接调客服消息接口，**不经 tool**。`admin-only` 模式只 block 粉丝在自己的动态 agent 里**主动调 tool 越权**的场景（譬如试图用 `wechat_service_message.send_text` 给别人发消息）。

```yaml
# 启用方法（推荐生产配置）
channels:
  wechat-service:
    dynamicAgents:
      enabled: true
      adminUsers: [oABC_admin1, oXYZ_admin2]
      permissionMode: admin-only
```

被拒绝时 tool 返回结构化错误：

```json
{
  "ok": false,
  "isError": true,
  "action": "send_text",
  "permissionMode": "admin-only",
  "agentId": "wechat-service-default-dm-onormal",
  "requesterSenderId": "oNORMAL",
  "error": "[wechat-service] action \"wechat_service_message.send_text\" 是 admin/write 操作..."
}
```

---

### 📐 多 Agent 路由

`routing.events` 允许把不同事件类型路由到不同 agent：

- `subscribe` / `unsubscribe` — 关注 / 取消关注
- `CLICK` / `VIEW` — 菜单点击 / 跳转
- `SCAN` — 带参二维码扫描
- `LOCATION` / `location_select` — 位置上报
- `TEMPLATESENDJOBFINISH` / `MASSSENDJOBFINISH` — 模板 / 群发回调

未命中的事件走 `routing.defaultAgent`。设置 `failClosedOnDefaultRoute: true` 时，默认 agent 未配置会拒绝消息。

**动态 Agent 优先级**：当 `dynamicAgents.enabled=true` 时，路由先走静态 `routing.events`，再被动态 agent 覆盖（除非 senderId 在 `adminUsers` 里）。

---

### 💾 知识库双写

启用 `knowledgeSync.enabled` 后，每条入站消息 + agent 回复会同时写入：

1. **本地 markdown**：`{localPath}/wechat-service/{accountId}/{openid}/{YYYY-MM-DD}.md`
   一天一个文件，首次写入带 YAML frontmatter，后续追加 `## HH:mm:ss` 段落。
2. **Odoo `knowledge.article`**：按 title `[wechat-service] {name} · {openid} · {date}` 去重；存在则 `write` 追加 body，不存在则 `create`（可选 `articleParentId`）。

两路独立 best-effort：任一失败不影响另一路，也不会 throw 到消息处理链。

---

### 🔒 加密模式与签名

- `plain` — 仅测试用，webhook 明文 XML
- `compatible` — 同时接受明文和加密；推荐只在迁移期使用
- `safe`（**推荐**）— 强制加密。插件用 `encodingAESKey` + `appId` 解密 `Encrypt` 字段并校验 `msg_signature`

服务器 URL 校验（`GET echostr`）兼容 `signature` + `msg_signature` 两种签名方式。

---

### 📡 公众号后台必做的 6 件事（缺一不可）

登录 https://mp.weixin.qq.com 找管理员账号，按顺序操作：

| # | 后台位置 | 字段 | 注意 |
|---|---------|------|------|
| 1 | 设置与开发 → 基本配置 → 服务器配置 | URL | 填 `https://你的域名/plugins/wechat-service/<accountId>`，accountId 跟 `~/.openclaw/openclaw.json` 一致 |
| 2 | 同上 | Token | 跟 plugin 配置 `accounts.<id>.token` **一字不差**（无空格、大小写敏感） |
| 3 | 同上 | EncodingAESKey | 43 位完整字符串，跟 `accounts.<id>.encodingAESKey` 一致 |
| 4 | 同上 | 加密模式 | 选「**安全模式**」对应 plugin 的 `encryptMode: safe`（推荐） |
| 5 | 设置与开发 → 基本配置 → IP 白名单 | 加入 OpenClaw gateway 的**出口公网 IP** | ⚠️ 不加无法调任何 wechat API（包括 access_token / 客服消息 / 模板消息），报 `errcode: 40164` |
| 6 | 设置与开发 → 接口权限 | 确认开通：客服消息 / 模板消息 / 用户管理 / 素材管理 / 群发接口 / 自定义菜单 / 数据分析 等 | 未认证号 / 个人号 / 订阅号有些接口禁用，需要服务号或已认证 |

**取出口 IP 的方法**：

```bash
# 在 gateway 跑的那台机器上
curl -s ifconfig.me ; echo
```

如果 gateway 跑在本地 mac、用 frpc 反代到公网，**出口 IP 是 mac 这边的公网 IP**（因为 outbound 不走隧道，是 mac 直连 wechat API）。建议把 gateway 部署到固定公网 IP 的 VPS，避免每次 IP 变都要改白名单。

---

### 🧰 故障排查（常见错误对照 + 日志关键字）

#### 错误码速查

| 现象 / 错误码 | 含义 | 排查 |
|--------------|------|------|
| 后台「请求失败，HTTP 返回非 200」 | webhook 不可达 | curl `https://你的域名/plugins/wechat-service/<id>` 看 200/404；查 frpc 隧道；查 gateway 是否在跑 |
| `signature_invalid` | Token 不一致 / 大小写 / 前后空格 | 重新对照 plugin 配置和后台 Token 字段，**完全一致** |
| `route-failure` 但 `signed=true` | 签名算到了但结果不一致 | 同上，Token 校对 |
| `errcode: 40164` | **IP 不在白名单** | 加 mac 出口 IP 到后台白名单（上面第 5 步） |
| `errcode: 45015` | 48 小时窗口已过 | 客服消息超 48h 不能发，改用模板消息 / 订阅消息 |
| `errcode: 45047` | 客服消息超出每日上限 | 等次日重置或降发频 |
| `errcode: 48001` | 接口权限未开通 | 后台「接口权限」页申请相应能力 |
| `errcode: 40001` | access_token 失效 | 不用动，plugin 自动刷新；持续报错检查 AppSecret 是否被重置 |
| `unknown channel id: wechatService` | 老配置 key 不对 | 升级到 v1.0.1+，把 `channels.wechatService` 改成 `channels["wechat-service"]`（kebab-case） |
| `Channel does not support add` | plugin v1.x 没暴露 setup adapter | 升级到 v2.0.0+ |
| `~/.openclaw/openclaw.json.clobbered.<ts>` 不断生成 | 配置 validator 拒收，自动备份 → 还原 last-good | 看 `.clobbered.*` 里写了啥 → 修配置 → 重启 gateway |
| 粉丝发消息没反应 | bindings 缺 wechat-service 反向路由 | 顶层 `bindings` 里加 `{agentId, match:{channel:wechat-service,accountId:...}}` |

#### 日志 grep 模板

```bash
# 实时跟踪 wechat-service 全链路
tail -f /tmp/openclaw-gateway.log | grep -E "wechat-service|customer_service|errcode"

# 看一条消息从 inbound 到 outbound 全流程
grep -E "reqId=<具体id>|wechat-service-outbound" /tmp/openclaw-gateway.log

# 单看 outbound 是否真的发出去
grep "wechat-service-outbound sent" /tmp/openclaw-gateway.log

# 看签名/解密失败
grep -E "signature_invalid|decrypt_failed" /tmp/openclaw-gateway.log

# 看是不是 IP 白名单问题
grep "40164" /tmp/openclaw/openclaw-*.log

# 看配置是否被 clobber
ls -lt ~/.openclaw/openclaw.json.clobbered.* 2>/dev/null | head -3
```

#### 期待看到的成功链路

粉丝发消息后日志按顺序应出现：

```
[wechat-service] inbound(http): reqId=xxx ... method=POST signed=true
[wechat-service] acked(placeholder) reqId=xxx accountId=default msgType=text from=oXXX
[wechat-service] inbound dispatch accountId=default agent=main from=oXXX
[wechat-service-outbound] sent text to openid=oXXX accountId=default (len=NNN)   ← 关键
```

少最后一条 = agent 没产出回复 / outbound 路由错 / 客服消息发送失败。按错误码对照排查。

---

### 🚦 完整最小可用配置（**一键复制粘贴**）

下面这段直接覆盖 `~/.openclaw/openclaw.json` 即可（替换 4 处 `__REPLACE__`）：

```jsonc
{
  "agents": {
    "list": [
      { "id": "main" }
    ]
  },
  "bindings": [
    {
      "agentId": "main",
      "match": { "channel": "wechat-service", "accountId": "default" }
    }
  ],
  "channels": {
    "wechat-service": {
      "enabled": true,
      "defaultAccount": "default",
      "accounts": {
        "default": {
          "enabled": true,
          "name": "我的公众号",
          "appId": "__REPLACE_WX_APP_ID__",
          "appSecret": "__REPLACE_APP_SECRET__",
          "token": "__REPLACE_TOKEN__",
          "encodingAESKey": "__REPLACE_43_CHAR_AES_KEY__",
          "encryptMode": "safe",
          "replyMode": "async",
          "replyPlaceholderText": "收到，正在为你处理..."
        }
      },
      "dynamicAgents": {
        "enabled": true,
        "dmCreateAgent": true,
        "defaultInstructionsPreset": "huo15-customer",
        "adminUsers": []
      },
      "autoReply": {
        "welcomeText": "欢迎来到「逸寻智库」👋  试试发：「Odoo」「AI」「价格」「演示」「课程」「联系」给我。\n📺 B 站 https://space.bilibili.com/400418085 也有免费视频。",
        "keywords": {
          "你好": "你好呀 👋 我是「逸寻智库」AI 客服。",
          "联系": "📞 18554898815 / postmaster@huo15.com / QQ 群 1093992108",
          "课程": "📚 https://chatai.huo15.com/slides",
          "B站": "https://space.bilibili.com/400418085",
          "产品": "火一五 6 大产品：辉火云企业套件 / 辉火云管家 / XR-IoT / 机器视觉质检 / 镜像世界 Web3.0 / 逸寻智库",
          "服务": "火一五 4 大服务：Odoo 实施 / OpenClaw 增强 / 安全架构 / 高校 XR",
          "演示": "🎬 留下姓名+公司+联系方式+想看哪款，运营 24h 内回访",
          "*Odoo*": "聊 Odoo 找对人了 ✨ 火一五 10 年经验、100+ 客户、10~19 全版本",
          "*价格*": "具体价格按方案定，请留信息：18554898815"
        },
        "businessHours": {
          "timezone": "Asia/Shanghai",
          "schedule": [
            { "days": [1,2,3,4,5], "start": "09:00", "end": "18:00" }
          ]
        }
      }
    }
  },
  "plugins": {
    "entries": {
      "wechat-service": { "enabled": true }
    }
  }
}
```

填好 4 个 `__REPLACE__` 字段（来自公众号后台「基本配置」+ AppSecret），然后：

```bash
# 重启 gateway 加载新配置
pkill -9 -x openclaw-gateway && sleep 2
nohup openclaw gateway run --bind loopback --port 18789 --force \
  > /tmp/openclaw-gateway.log 2>&1 &

# 验证
sleep 5
openclaw channels list | grep 微信服务号
# 期待：微信服务号（公众号） default: configured, enabled
```

**生产上线前再加**：`dynamicAgents.enabled: true` + `adminUsers` + `permissionMode: admin-only`（一粉一会话隔离 + 权限控制）。

---

### 🧪 脚本

```bash
npm run typecheck   # tsc --noEmit
npm test            # vitest run（17 个文件 282 个用例）
npm run build       # tsc → dist/
npm run release -- 2.3.3   # 一键串行发版（git tag + npm + ClawHub + 双 remote push）
```

`prepublishOnly` 会自动跑 typecheck + build。`release.sh` 含 11 项预检（工作树干净 / 远端同步 / 三处版本对齐 / pluginApi ranged / 无 child_process 红线 / npm 无幽灵占用 / tag 不冲突等）。

---

### 📚 资源

- **微信公众平台官方文档**：https://developers.weixin.qq.com/doc/service/guide/
- **OpenClaw 文档**：https://docs.openclaw.ai/zh-CN
- **本地知识库**：`~/knowledge/huo15/2026-04-29-wechat-service-v2-wecom-mirror-refactor.md`
- **公司 Odoo 技术知识库**：https://www.huo15.com/odoo/knowledge/

<hr>

**公司名称：** 青岛火一五信息科技有限公司
**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

<hr>

<p align="center">
  <strong>关注逸寻智库公众号，获取更多资讯</strong>
</p>

<hr>

## 📄 License

MIT © 青岛火一五信息科技有限公司（jobzhao / zhaobod1@163.com）

详见 [`LICENSE`](./LICENSE)。
