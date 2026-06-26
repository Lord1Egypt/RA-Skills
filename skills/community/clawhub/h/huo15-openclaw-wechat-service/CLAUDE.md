# @huo15/wechat-service — 火一五·微信服务号插件

OpenClaw 渠道插件，接入微信服务号（公众号），实现消息收发、菜单管理、客服/模板/订阅消息、素材/图文发布、标签群发、JS-SDK、多账号多 Agent 隔离与知识库双写。

## 架构

```
index.ts                     # 插件入口：注册 channel / webhook 路由 / agent tools
src/
├── channel.ts               # ChannelPlugin 装配（config/outbound/gateway/status）
├── types.ts                 # 所有类型定义（WechatServiceConfig / ResolvedAccount / DynamicAgents 等）
├── runtime.ts               # 运行时模块 re-export
├── monitor.ts               # 公共入口 re-export
├── dynamic-agent.ts         # 动态 Agent 派生（一粉一会话）
├── outbound.ts              # 主动消息下发
├── access-token.ts          # Access Token 管理与自动刷新
├── http-client.ts           # HTTP 客户端（含重试/代理）
├── crypto.ts                # 微信加解密（SHA1/AES）
├── auto-reply.ts            # 自动回复：关键词匹配 / 业务时间 / 欢迎语模板
├── config/
│   ├── accounts.ts          # 账号解析（多账号矩阵）
│   ├── derived-paths.ts     # Webhook 路径推导
│   └── index.ts
├── app/
│   ├── account-runtime.ts   # 账号状态机类
│   └── index.ts
├── shared/
│   ├── authorization.ts     # 权限控制（open / admin-only / role-based）
│   ├── roles.ts             # 角色权限系统（resolveUserRole / checkRoleAuthorization）
│   ├── guard.ts             # AI 对话护栏（角色感知 system prompt 生成）
│   ├── xml-parser.ts        # XML 解析与被动回复构造
│   └── *.test.ts            # 对应测试文件
├── runtime/
│   └── dispatcher.ts        # 消息分发：inbound → agent → 客服回复
├── transport/webhook/
│   ├── handler.ts           # HTTP webhook 入口（GET 校验 / POST 接收）
│   ├── normalize.ts         # XML → UnifiedInboundEvent
│   ├── registry.ts          # Webhook 目标注册表
│   └── common.ts            # 通用 HTTP 工具
├── api/                     # 微信公众平台 API 封装（20+ 个）
│   ├── customer-service.ts  # 客服消息 (text/image/voice/video/news/mpnews/menu/miniprogram)
│   ├── template-message.ts  # 模板消息 CRUD + 公模板库
│   ├── subscribe-message.ts # 长期订阅通知
│   ├── menu.ts              # 自定义菜单（基础 + 个性化）
│   ├── material.ts          # 临时/永久素材
│   ├── draft.ts             # 草稿箱 + freepublish
│   ├── user.ts              # 用户信息/标签/黑名单
│   ├── user-tag.ts          # 用户标签管理
│   ├── mass-send.ts         # 群发（按标签/openid/预览/撤回）
│   ├── oauth.ts             # 网页授权 OAuth2.0
│   ├── jssdk.ts             # JS-SDK 签名
│   ├── qrcode.ts            # 带参二维码
│   ├── analytics.ts         # 数据统计（datacube 17 项指标）
│   ├── intelligent.ts       # 智能开放（OCR 7 类 + 图像处理 3 项）
│   ├── card.ts              # 卡券精简（6 个 actions）
│   └── *.test.ts
├── tools/                   # Agent Tool 注册（12 个 tool / 60+ actions）
│   ├── index.ts             # registerWechatServiceTools()
│   ├── shared.ts            # 公共：resolveToolAccount / assertAuthorized / buildToolResult
│   ├── menu-tool.ts         # wechat_service_menu
│   ├── message-tool.ts      # wechat_service_message（25 actions）
│   ├── material-tool.ts     # wechat_service_material
│   ├── article-tool.ts      # wechat_service_article
│   ├── user-tool.ts         # wechat_service_user
│   ├── qrcode-tool.ts       # wechat_service_qrcode
│   ├── mass-send-tool.ts    # wechat_service_mass_send
│   ├── jssdk-tool.ts        # wechat_service_jssdk
│   ├── oauth-tool.ts        # wechat_service_oauth
│   ├── analytics-tool.ts    # wechat_service_analytics
│   ├── intelligent-tool.ts  # wechat_service_intelligent
│   └── card-tool.ts         # wechat_service_card
└── knowledge/               # 知识库双写（本地 MD + Odoo）
    ├── index.ts
    ├── local-sync.ts
    └── odoo-sync.ts
```

## 关键设计模式

### 1. 消息生命周期

```
微信服务器 POST /plugins/wechat-service/{accountId}
  → handler.ts: 验签 → 解密 → 解析 XML → 立即 200 "success"
  → auto-reply 检查（关键词/业务时间）
  → normalize.ts: XML → UnifiedInboundEvent
  → dispatcher.ts: 路由解析 → 动态 Agent 派生 → dispatchReply
  → LLM agent 回复 → sendCustomerServiceMessage → 微信服务器
```

### 2. 工具调用模式

每个 tool 的 execute() 遵循统一模板：
```ts
// 1. 解析账号
const { account, tokenHandle } = resolveToolAccount({ ctx, apiConfig, explicitAccountId });
// 2. 权限检查
const denied = assertAuthorized({ ctx, apiConfig, toolName, action, accountId });
if (denied) return denied;
// 3. switch(action) 调度 → 调用 api/ 层 → buildToolResult / buildErrorResult
```

### 3. 权限系统（三种模式）

| 模式 | 说明 | 配置字段 |
|------|------|----------|
| `open`（默认） | 所有 agent 全权限 | — |
| `admin-only` | 读放行，写仅 main/adminUsers | `adminUsers` |
| `role-based`（v2.2.0） | 按角色细粒度控制 | `roles` + `rolePermissions` + `defaultRole` |

**role-based 决策流程**：
1. `resolveUserRole(openid)` → 角色名
2. `getRolePermissions(role)` → 白名单（用户配置 > 内置默认）
3. `checkRoleAuthorization()` → 白名单匹配

内置角色：`superadmin` / `admin`（全权限）、`editor`（内容管理）、`operator`（客服运营）、`customer`（最小权限）。

### 4. AI 对话护栏

在 role-based 模式下：
- **Agent 创建时**：`resolveAgentInstructions()` 生成角色感知的 system instructions，写入 `agents.list[].instructions`
- **消息分发时**：`injectGuardToEnvelope()` 将护栏 prompt 拼接到消息信封中
- customer 角色的 agent 会在 system prompt 中被告知"只能回答常见问题，管理操作需礼貌拒绝"

### 5. 配置 key 约束

- **Config section key MUST be** `"wechat-service"` (kebab)，与 channel id 对齐
- Legacy key `"wechatService"` (camelCase) 仅用于读取旧配置时的回退（with console.warn）
- 常量：`CONFIG_SECTION_KEY = "wechat-service"` / `LEGACY_CONFIG_SECTION_KEY = "wechatService"`

## 命名规范

- 所有文件/导入使用 kebab-case 文件名
- Agent ID 格式：`wechat-service-{accountId}-dm-{sanitized_openid}`
- Session target 格式：`wechat-service:{accountId}:user:{openid}`
- Tool 名称使用 snake_case 前缀：`wechat_service_*`

## 测试规范

- 使用 vitest，148+ 用例
- 测试文件与源文件同目录，命名为 `*.test.ts`
- 不 mock 数据库或外部 API 调用单元测试，但使用 fake config / runtime 测试逻辑
- 关键不变量在测试文件顶部注释说明

## 注意事项

- 客服消息有 48 小时窗口限制
- 模板消息/订阅消息有独立的 API 端点，不与客服消息混用
- 群发消息每天有限额（服务号每月 4 次）
- `encryptMode: "safe"` 需要 `encodingAESKey`（43 位）
- webhook 路径 `/plugins/wechat-service/{accountId}` 和 `/wechat-service/{accountId}` 都注册了
- 公众号没有群聊，`groupEnabled` 保留仅为了与 @huo15/wecom schema 对齐
