# opphub-skill v3.1 · OpenClaw runtime · channel-renderer 渲染层架构

> "原始内容归原始内容, 你得 写一个 飞书 card 的渲染层 当然未来也有其他通道需要特定的渲染"

> **含义**: runtime 渲染层是 OpenClaw 平台活, **不在 opphub skill v3.1 范围**
> **本文状态**: 独立存档, 等 OpenClaw runtime 团队接

---

## 0. 文档归属

| 项 | 归属 |
|---|---|
| **本档**(运行时渲染层) | OpenClaw runtime 团队 |
| opphub skill v3.1 doc | skill 层 (我开干的范围) |
| opphub-server schema v3.1 | server 层 (单独存档) |

---


> "原始内容归原始内容, 你得 写一个 飞书 card 的渲染层 当然未来也有其他通道需要特定的渲染"


> "只到 skill 开放完, 没开发完, 不会会话"

**含义**:
- skill 层只发 "IntentMessage 原始内容"(channel-agnostic)
- skill 层不拼飞书 card / Block Kit / InlineKeyboard
- runtime 渲染层是 OpenClaw 平台活, **不在 opphub skill v3.1 范围**
- server schema (`OpcKnowledgeEntry` 表) 也是单独一条线

---


| # | 任务 | 改动层 | 工时 | 依赖 |
|---|---|---|---|---|
| N10 | Skill 改造: 5 个 bin 都改用 `bot.skillApi.askInteractive/askFreeText/send`, 删硬编码飞书 JSON | Skill | 3h | 无 |
| N11 | SKILL.md frontmatter: `requires.tools` 加 `minimax__web_search / web_fetch / minimax__understand_image / pdf / memory_search / wiki_search` | Skill | 0.5h | 无 |
| N12 | OpenClaw runtime 新 API: `skillApi.send/askInteractive/askFreeText/getChannel` + 类型定义 + 8 个 Renderer (FeishuCard / FeishuGroup / WeixinText / SlackBlock / DiscordEmbed / TelegramInline / CliInquirer / WebForm) + FallbackText | Runtime | 8h | 无 (这是 OpenClaw runtime 改造, 不是 skill 改造) |
| N13 | E2E 多 channel 测试: 飞书 DM / 飞书群 / 微信 iLink / CLI 各跑一遍偶合配置 + 偶合画像 6 步 | 全链路 | 2h | N10 N12 |
| **N10-N13 合计** | | | **13.5h ≈ 1.7 天** | |

**总工时** v3.1: 19.5h (skill 6 步) + 13.5h (renderer) + 1h (server schema N4-N5) + 1h (server API N5) = **约 35h ≈ 4.5 天**


---



### 关键分工

```
┌─────────────────────────────────────────────────────┐
│  Skill / Plugin 层                                  │
│  发 "原始内容" (IntentMessage, channel-agnostic)   │
│  - prompt / options / actions / inputHint / links   │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  OpenClaw runtime · Content Renderer 层 ★ 这里 ★    │
│  每个 channel 一个 renderer:                         │
│  · FeishuCardRenderer   (interactive card + actions) │
│  · FeishuGroupRenderer  (同上,群 channel)            │
│  · WeixinRenderer       (文本 + emoji 协议)          │
│  · SlackRenderer        (Block Kit)                  │
│  · DiscordRenderer      (Embed + Components)         │
│  · TelegramRenderer     (InlineKeyboard)             │
│  · CliRenderer          (inquirer.select / confirm)  │
│  · WebRenderer          (HTML form, 走 opphub-web)   │
│  · FallbackTextRenderer (纯文本兜底)                │
└──────────────────┬──────────────────────────────────┘
                   ↓
                Channel (IM / CLI / Web)
```

### Skill / Plugin API (IntentMessage 原始内容)

```ts
interface IntentMessage {
  prompt: string;                    // 主文案 ("选默认推送通道")
  options?: Array<{                  // 选项 (pickOne 场景)
    id: string;                      // 选中时回传 (feishu:pm)
    label: string;                   // 显示 ("feishu:pm ⭐")
    hint?: string;                    // 副文案 ("pm bot")
    isDefault?: boolean;
  }>;
  actions?: Array<{                  // 按钮
    id: string;                      // 唯一 action id
    label: string;                   // 按钮文字 ("确认" / "🚀 一键装 plugin")
    style?: 'primary' | 'default' | 'danger';
    payload?: Record<string, any>;   // action 回调带的元数据
  }>;
  inputHint?: string;                // 自由文本输入
  links?: Array<{                    // 链接按钮 (install 引导)
    text: string;
    url: string;
  }>;
  markdown?: string;                 // 富文本 (lark_md / mrkdwn / html)
  header?: {
    title: string;
    color?: 'blue' | 'orange' | 'red' | 'green';
  };
  metadata?: Record<string, any>;
}
```

### 8 个 Renderer 渲染示例

| channel | askInteractive / askFreeText 渲染 |
|---|---|
| 飞书 DM / 群 | interactive card · actions + button + url link |
| 微信 iLink | 文本 + emoji + "回复按钮序号" + 文本链接 |
| Slack | Block Kit · actions block + button + url |
| Discord | Embed + Components (buttons + link) |
| Telegram | InlineKeyboard + URL 按钮 |
| CLI / tty | inquirer.select / confirm / input |
| web (opphub-web) | HTML form (走 /admin/devices/:opcId) |
| FallbackText | 纯文本兜底 (不识别的 channel) |

### OpenClaw runtime skillApi 新增 API

```ts
declare global {
  interface SkillApi {
    /** 单向通知 (无操作) */
    send(intent: IntentMessage): Promise<void>;

    /** 交互意图 - 等用户回复 (pickOne / actions) */
    askInteractive(intent: IntentMessage & {
      options?: Option[];
      actions?: Action[];
    }): Promise<UserReply>;

    /** 自由文本输入 */
    askFreeText(intent: IntentMessage & {
      inputHint: string;
    }): Promise<string>;

    /** 当前 channel hint */
    getChannel(): {
      type: 'feishu' | 'weixin' | 'slack' | 'discord' | 'telegram' | 'cli' | 'web';
      account?: string;
      supportsCards: boolean;
      supportsInlineActions: boolean;
      supportsFreeText: boolean;
    };
  }
}
```

### Skill ↔ Plugin ↔ Runtime 三者边界 (钉死)

| 层 | 谁做 | 不做 |
|---|---|---|
| Skill (per-invocation) | 发 "IntentMessage 原始内容" + 调 plugin CLI | ❌ 不拼飞书 card JSON / Block Kit / InlineKeyboard |
| Plugin (常驻) | 执行 spawn CLI + WS 通讯 + 直读 JSON | ❌ 不接 channel context (没 channelType) |
| OpenClaw runtime ★ | 把 IntentMessage 转译成 channel 原生渲染 | 不解析业务意图 |
| Channel | 飞书 OpenAPI / 微信 iLink / Slack / Discord / Telegram / tty / web | — |


- ✅ skill 必须调 `bot.skillApi.askInteractive(...)` / `askFreeText(...)` / `send(...)`
- ❌ skill **永远不写** 硬编码 飞书 card JSON (不是 skill 的活)
- ❌ skill **永远不写** `feishu_mcp_create_card(...)` 这种飞书 OpenAPI 直调
- ❌ skill **永远不** 自己 `bot.sendMessage(一段 ad-hoc JSON)`
- ✅ OpenClaw runtime 8 个 renderer, 未来加 channel 加 renderer 就行 (renderer 由 runtime/插件编写者实现)
- ❌ skill / plugin **不在 tty** 跑 inquirer (runtime CliRenderer 才跑)
- ✅ CliRenderer 是 runtime 内置 (SSH/headless fallback)

### Plugin CLI 保留 (再钉一遍)

- ❌ plugin **不接** skill 的 IntentMessage (没 channel context)
- ❌ plugin CLI 的 inquirer 姿势 **保留** (SSH/headless 用户绕过 skill 直接跑 plugin CLI)

### 渲染示例 (每个 channel 一段)

#### 飞书 (FeishuCardRenderer)

```json
{
  "config": { "wide_screen_mode": true },
  "header": { "title": { "tag": "plain_text", "content": "选默认推送通道" }, "template": "blue" },
  "elements": [
    { "tag": "div", "text": { "tag": "lark_md", "content": "本机已配 5 条有效通道" } },
    { "tag": "select_static", "options": [
      { "text": { "tag": "plain_text", "content": "feishu:pm" }, "value": "feishu:pm" }
    ], "value": { "type": "text", "text": "feishu:pm" } },
    { "tag": "action", "actions": [
      { "tag": "button", "text": { "tag": "plain_text", "content": "确认" }, "type": "primary", "value": { "action": "confirm" } },
      { "tag": "button", "text": { "tag": "plain_text", "content": "取消" }, "type": "danger", "value": { "action": "cancel" } }
    ]}
  ]
}
```

#### 微信 iLink (WeixinRenderer · 文本 + emoji)

```
📋 偶合 OppHub · 选默认推送通道

本机已配 5 条有效通道:
  1️⃣ feishu:default       公司主账号
  2️⃣ feishu:dev            dev bot
  3️⃣ ⭐ feishu:pm           pm bot
  4️⃣ feishu:frontend       前端
  5️⃣ openclaw-weixin:eat-im-bot   微信 bot

回复 [数字] 选择通道, 或:
  Y → 用默认 (feishu:pm)
  N → 取消

(消息已加密, 2 分钟有效)
```

#### Telegram (TelegramRenderer · InlineKeyboard)

```json
{
  "text": "📋 *偶合 OppHub · 选默认推送通道*\n\n本机已配 5 条有效通道",
  "reply_markup": {
    "inline_keyboard": [
      [{ "text": "feishu:default", "callback_data": "pick:feishu:default" }],
      [{ "text": "⭐ feishu:pm",   "callback_data": "pick:feishu:pm" }],
      [{ "text": "feishu:dev",     "callback_data": "pick:feishu:dev" }],
      [{ "text": "✅ 确认",        "callback_data": "confirm" }, { "text": "❌ 取消", "callback_data": "cancel" }]
    ]
  }
}
```

#### CLI / tty (CliRenderer · inquirer)

```js
const answer = await inquirer.prompt([{
  type: 'list',
  name: 'choice',
  message: '选默认推送通道',
  choices: [
    { name: 'feishu:default (公司主账号)', value: 'feishu:default' },
    { name: '⭐ feishu:pm (pm bot)', value: 'feishu:pm' },
    ...
  ],
  default: 'feishu:pm',
}]);
```

#### Web (WebRenderer · HTML form, 走 opphub-web)

```html
<form action="/api/user/channels/default" method="PATCH">
  <h2>选默认推送通道</h2>
  <select name="channelType+channelId">
    <option value="feishu:default">feishu:default</option>
    <option value="feishu:pm" selected>feishu:pm</option>
    ...
  </select>
  <button type="submit">确认</button>
  <button type="cancel">取消</button>
</form>
```

### 改造 + 风险

| 风险 | 缓解 |
|---|---|
| skill 误写硬编码飞书 card | SKILL.md 加 lint / require.js static check (CI grep) |
| 现有 plugin CLI 用户绕开 skill | plugin CLI inquirer **完全保留** |
| 微信 iLink 不支持原生 card | WeixinRenderer 走文本 + emoji + 编号协议 (兜底) |
| tty 没 TTY 时 CliRenderer 失败 | FallbackTextRenderer 兜底 (纯文本提一个一次性的"我帮你做") |
| renderer 自己 crash | renderer 异常时自动回退到 FallbackTextRenderer (try/catch 包裹) |

### 关联档

- 设计稿:`workspace/skills/opphub/docs/v3.1-architecture.md` (本节)
- 后续整改:Skill 全部 bin 改用 `bot.skillApi.*` 替代硬编码 JSON

---

