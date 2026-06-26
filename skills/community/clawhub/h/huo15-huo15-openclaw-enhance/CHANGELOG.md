# CHANGELOG

本插件语义化版本号与龙虾适配版本解耦：`package.json.version` 为插件自身的发布版本，`openclaw.build.openclawVersion` 为目标龙虾版本。

## 6.7.13 — 2026-05-11（large-file-bridge 兜底死循环修复 + 用户上传后流程引导）

### 触发

用户截图实测 v6.7.12（token URL 已生效）：

```
贾维斯 15:30
上传好了，你试试转成会议纪要发给我
👉 https://keepermac.huo15.com/plugins/enhance-upload/2eaffa5d5569

黄宣榕 15:31
我已经上传好了

贾维斯 15:31
我已经上传好了
👉 https://keepermac.huo15.com/plugins/enhance-upload/2eaffa5d5569   ← 又塞了一遍！
```

用户已经上传完，AI 应该调 `enhance_upload_check({token: "2eaffa5d5569"})` 拿文件，处理"转会议纪要"任务。但 hook 把 LLM 输出**又**强制覆盖成上传链接 → 死循环。

### 根因（两个）

#### 根因 A: `before_agent_reply` 兜底每轮 reply 都 fire

```ts
// v6.7.12 兜底逻辑
const entry = injectedSessions.get(key);
if (!entry) return;       // 只要 inject 过就触发
// body 不含 URL → appendText 上传链接
```

`injectedSessions` 在 session 整个生命周期都保留 entry → 每个后续 reply 都被兜底覆盖。用户的"传完了"那条 reply 也被覆盖 → 永远拿不到处理结果。

#### 根因 B: prompt 没明确"用户上传后该干什么"

LLM 看到 prompt 里说『token 已预备好』但没说『用户上传后必须调 enhance_upload_check 工具』，弱模型不会主动调。

### v6.7.13 改动

#### 1. injectedSessions entry 加 `replyAppendUsed` 标记

```ts
// v6.7.13
Map<string, { token, createdAt, replyAppendUsed: boolean }>
```

`before_prompt_build` 注入时 `replyAppendUsed: false`，`before_agent_reply` fire 一次后**立即** `replyAppendUsed = true` → 后续 reply 不再被覆盖。

```ts
const entry = injectedSessions.get(key);
if (!entry || entry.replyAppendUsed) return;  // ← 关键
// ... appendText logic
entry.replyAppendUsed = true;                  // ← 标记已用
```

#### 2. prompt 加『用户上传后处理流程』强引导

```
# 本次会话已预生成 token (AI 追踪用)

**token = `2eaffa5d5569`** (已写入 ~/.openclaw/upload/manifest.json, 24h 有效)

## 用户上传后的处理流程（关键！LLM 必须严格按此顺序执行）

用户上传文件后会发"传完了" / "上传好了" / "已传完" / 类似确认消息。**此时你必须**：

1. 立即调用 enhance_upload_check({token: "2eaffa5d5569"}) 工具
2. 工具返 {files: [{path, size, name}, ...]} 数组
3. 用 Read 工具读 files[i].path 拿到文件内容
4. 按用户原始任务继续处理（如"转会议纪要" / "分析内容" / "提取信息"）

**严禁的反模式**：
❌ 再次发上传链接（用户已上传，再发链接 = 死循环！）
❌ 反问"你确定上传了吗 / 请截图" / "我没收到"
❌ 跳过 enhance_upload_check 直接 ls 或 grep ~/.openclaw/upload/ 全盘扫
```

### 用户场景验证

| 步骤 | v6.7.12（死循环） | v6.7.13（正常）|
|---|---|---|
| 用户首次发"超过100M无法下载" | hook inject + 兜底给链接 ✓ | 同上 ✓ |
| 用户回"传完了" | hook 又兜底给链接（死循环）❌ | replyAppendUsed=true → 不接管 ✓ |
| LLM 看到"传完了" | （prompt 没教）瞎回 | （prompt 强引导）调 enhance_upload_check({token}) ✓ |
| AI 拿到文件路径 | 拿不到 | files: [{path, size, name}] ✓ |
| AI 处理"转会议纪要" | 永远不进入这步 | Read 路径 → 调 model → 输出纪要 ✓ |

### 红线自查

- ✅ 不修龙虾核心
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ 兜底 hook 一次性消费,不影响后续 reply 自然流转

## 6.7.12 — 2026-05-11（large-file-bridge 自动生成 token URL — 兜底也给 token，AI 追踪零依赖弱模型）

### 触发

用户原话：**「没有后缀 token 啊」**

v6.7.11 兜底虽然给了 `https://keepermac.huo15.com/plugins/enhance/upload` 完整 URL，但 **没 token** → AI 拿不到 `enhance_upload_check({token})` 的输入 → **不能查谁传了什么**。

弱模型（MiniMax M2.7）从来不会主动调 `enhance_upload_link` 工具拿 token，所以 token URL 一直没机会生效。

### 设计取舍

让 `large-file-bridge` **在 hook 内部自动生成 token**，不依赖 LLM 主动调工具：

| 时机 | 动作 |
|---|---|
| `before_prompt_build` 命中 WECOM_LARGE_FILE_ERROR | `randomBytes(6).hex()` 生成 token + mkdir `<uploadRoot>/<token>/files/` + 写 manifest.json |
| 同 session 后续触发 | injectedSessions Map 已存 token，复用 |
| `before_agent_reply` 兜底 | 用 injectedSessions 里那个 token 拼 URL（前后一致） |

manifest.json 跟 `bot-upload-link` **共用 `~/.openclaw/upload/manifest.json`**，所以 LLM 调 `enhance_upload_check({token})` 工具时 bot-upload-link 能读到这条 token，拉清单成功。

### 改动

#### 1. `injectedSessions` Map 升级

```ts
// v6.7.11: Map<string, number>          (只存 timestamp)
// v6.7.12: Map<string, { token: string; createdAt: number }>
```

#### 2. 新增 `createUploadToken()` helper

```ts
const UPLOAD_ROOT = join(homedir(), ".openclaw", "upload");
const MANIFEST_PATH = join(UPLOAD_ROOT, "manifest.json");

function createUploadToken(label, ownerAgent): string | null {
  const token = randomBytes(6).toString("hex");  // 12 hex
  mkdirSync(join(UPLOAD_ROOT, token, "files"), { recursive: true });

  // 读/写 manifest（与 bot-upload-link 共用）
  let manifest = existsSync(MANIFEST_PATH)
    ? JSON.parse(readFileSync(MANIFEST_PATH, "utf-8"))
    : { version: 1, entries: [] };
  manifest.entries.push({
    token, label, ownerAgent,
    createdAt: new Date().toISOString(),
    expireAt: new Date(Date.now() + 24*3600*1000).toISOString(),
    files: [],
  });
  writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2));

  return token;
}

function buildTokenUrl(baseUrl, token): string {
  return `${baseUrl}/plugins/enhance-upload/${token}`;
}
```

#### 3. before_prompt_build 用 token URL

```ts
const token = createUploadToken(`session:${sessionId.slice(0,12)}`, agentId);
const url = token ? buildTokenUrl(baseUrl, token) : resolveUploadUrl();
const text = buildUploadContext(url, token);  // prompt 提示 token 已就绪
injectedSessions.set(key, { token: token ?? "", createdAt: Date.now() });
```

#### 4. before_agent_reply 用同一个 token URL

```ts
const entry = injectedSessions.get(key);
const url = entry.token ? buildTokenUrl(baseUrl, entry.token) : resolveUploadUrl();
// suffix 拼 token URL，前后完全一致
```

#### 5. prompt 增强：告诉 LLM token 已预备好

```
# 已为本次会话预生成 token（AI 可追踪）

token = `abc123def456`（已写入 manifest，24h 有效）。用户上传后,你**必须**调:
  enhance_upload_check({token: "abc123def456"})
拉清单 → 拿到 {path, size, name} 数组 → Read 路径分析文件。

# 严禁的行为
❌ 不要再调 enhance_upload_link 工具生成新 token — token "abc123def456" 已预备好,直接发给用户即可
```

### 用户场景验证

| 步骤 | 之前 (v6.7.11) | 现在 (v6.7.12) |
|---|---|---|
| 用户发"视频/文件超过100M无法下载" | hook 注 prompt + 兜底，URL 是共享 `/plugins/enhance/upload`（无 token，AI 拿不到追踪 key） | hook 注 prompt + 兜底，URL 是 `/plugins/enhance-upload/<token>`（manifest 已写，AI 立刻能用 token） |
| LLM 完全无视 prompt | 兜底 appendText 共享 URL，**AI 不能查谁传了什么** | 兜底 appendText token URL，**AI 调 enhance_upload_check({token}) 查清单成功** |
| 用户上传 → "传完了" | AI 没 token，只能 `ls ~/.openclaw/upload/` 全盘扫（隐私 + 性能差） | AI 调 enhance_upload_check({token: "abc..."}) → 精确返该 token 文件清单 → Read |

### 红线自查

- ✅ 不修龙虾核心
- ✅ 零 child_process / 零新 npm 依赖（randomBytes 是 node stdlib）
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ manifest 跟 bot-upload-link 共用，避免重复实现 token 系统
- ✅ token 生成失败时优雅降级到共享 URL（不阻塞主流程）

## 6.7.11 — 2026-05-11（large-file-bridge 双重 prompt-following 加固 — 针对 MiniMax M2.7 等弱模型）

### 触发

用户报错持续，让我"查本地 agent"。grep `~/.openclaw/agents/` 找到根因：

**agent**: `wecom-default-dm-huangxuanrong`
**model**: `minimax/MiniMax-M2.7`
**session jsonl**: `6b98e16a-...jsonl`

读 jsonl line 6 — **enhance prompt 已完整注入**（含『首选调 enhance_upload_link → 返 /plugins/enhance-upload/<token>』+ 备用 URL 等所有引导）。

但 LLM 后续 messages 显示：

| LLM 动作 | 实际做了什么 |
|---|---|
| 调 `enhance_upload_link`? | ❌ 没有 |
| 给用户 `https://...upload` URL? | ❌ 没有 |
| 改去 `exec grep wecom 源码` | ✅ 做了 3-4 次 |
| 自己发现 `DEFAULT_WECOM_MEDIA_MAX_BYTES = 80MB` | ✅ |
| 反问用户『请把完整错误消息截图发给我』 | ✅ |

**LLM 完全无视 enhance 的硬指令，反向操作**：
- 指令『不要先问诊断问题』 → 反问"请把完整错误消息截图发给我"
- 指令『首选调 enhance_upload_link』 → 不调，自己 grep 源码
- 指令『把 URL 发给用户』 → 没给

这是 **MiniMax M2.7 prompt-following 能力差** + **prompt 措辞不够刺激** 的双重失败。

### 第三层防御也失效

`before_agent_reply` hook 本应兜底强制 appendText 上传 URL：

```ts
// v6.7.10 兜底逻辑
if (
  body.includes("upload") ||      // ← 太宽! LLM 叙述里说"upload 相关问题"也命中
  body.includes("/plugins/enhance") ||
  body.includes("/lanhuo/upload") ||
  body.includes("上传链接") ||      // ← 太宽! LLM 说"插件有上传链接功能"也命中
  body.includes("上传页面")
) return;                          // ← 误判已给链接,不接管
```

LLM 最终回复里**叙述性**提到："克劳德增强包里有一个 `large-file-bridge` 模块专门处理这个场景" + "请你确认 large-file-bridge 模块是否已经在运行" + "上传链接相关问题" — 含 `large-file-bridge` 等字符串触发 `body.includes("upload")` → 误判 → 兜底放行。

### v6.7.11 改动

#### 1. prompt 改命令式硬规则（针对弱模型）

```
【大文件上传 — 强制规则，禁止违反】

# 你的回复必须是下面这一段，一字不改：

文件超过 100MB 无法在企微直接传输，请通过下面这个链接上传（支持 2GB 以内，浏览器拖拽即可）：

${url}

上传完成后告诉我，我来处理。

# 严禁的行为（违反 = 用户卡死）

❌ 不要 exec/grep wecom / openclaw 源码查"limit / maxBytes / MAX_DOCUMENT_BYTES"等
❌ 不要反问用户"请把完整错误消息截图发给我" / "你是哪个场景" / "需要更多信息才能定位"
❌ 不要建议用户 `openclaw config set` 或修改任何配置
❌ 不要叙述性提到 "large-file-bridge 模块" / "增强包 hook" / "插件内置限制"
❌ 不要给 `/plugins/enhance/upload` 这种**裸路径**（缺 https:// 前缀），用户点不开
```

把 LLM 容易"反向操作"的具体路径**逐条列字面值禁止**（参考红线 #11 / Allen 流的"具体反例字面写进 prompt"原则）。

#### 2. before_agent_reply 兜底关键词收紧

```ts
// v6.7.11 新逻辑
const hasRealUrl =
  body.includes(url) ||                                          // 完整匹配当前 url
  /https?:\/\/[^\s)]+\/plugins\/enhance(-upload)?\//.test(body) || // 任何 enhance 上传 URL
  body.includes("enhance_upload_link") ||                        // 调过工具会留下 marker
  body.includes("enhance_upload_check");
if (hasRealUrl) return;
```

只在含**真实可点 URL**（http(s):// 前缀 + /plugins/enhance.../ 路径）或工具名 marker 时跳过。叙述性提及不再误判 → 兜底真正生效 → 强制 appendText 完整上传链接。

### 红线自查

- ✅ 不修龙虾核心
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ 把 LLM 反向操作的具体路径字面写进 prompt（红线 #11 anti-pattern in prompt）

### 通用沉淀

**LLM 给定相同 prompt 会因 model 不同表现差异巨大**。强模型（Claude / GPT）能 follow 一句"必须给链接"硬指令；弱模型（MiniMax M2.7 / DeepSeek-V4-Flash）需要：
1. 命令式硬指令（"必须 / 禁止"，不是描述性）
2. 把具体反例（"不要 exec grep 源码 / 不要反问"）字面写进 prompt
3. 兜底 hook 关键词匹配要"内容驱动"（含真实 URL）而非"语义驱动"（含 "upload" 字面）

## 6.7.10 — 2026-05-11（large-file-bridge 触发放宽 — 不再卡 agentId.startsWith("wecom-")）

### 触发

用户实测 v6.7.9 升级后 LLM 回复（在某个非企微渠道发"视频/文件超过100M无法下载"）：

```
这是 openclaw-media-bridge 的下载限制，文件超过 100MB 会被截断。让我查一下当前的配置：
找到关键信息了。文件大小有几层限制：
- MAX_VIDEO_BYTES : 16 MB
- MAX_DOCUMENT_BYTES : 100 MB ← 这就是你遇到的
- MAX_AUDIO_BYTES : 16 MB
- ...
如果你想让贾维斯能处理更大的文件，可以调高配置：
openclaw config set channels.wecom.mediaMaxMb 200
```

LLM **完全没走 enhance 引导**（没调 `enhance_upload_link`、没给 `/plugins/enhance/upload` URL），反而自己读 source code 调研 `MAX_DOCUMENT_BYTES`。

### 根因

v6.7.0 修 channel 检测 bug 时加了：

```ts
if (!agentId.startsWith("wecom-")) return;
```

但 main agent / terminal / Claude CLI / Claude Desktop / dingtalk / wechat-service 等所有非 wecom 渠道的 agentId **都不以 `wecom-` 开头** → 这些场景 large-file-bridge **彻底不工作**。

但「视频/文件超过 100M，无法下载」**是企微独家错误文本**——只要消息含这句话，就一定是企微大文件场景（即使 LLM 在非 wecom agent 上看到了，比如用户在 Claude CLI 里贴企微截图）。

### v6.7.10 改动

`before_prompt_build` hook：

```ts
// v6.7.10: 触发条件不再卡 agentId
if (detectWecomError && WECOM_LARGE_FILE_ERROR.test(promptText)) {
  reason = "detected-wecom-large-file-error";
  // ↑ 命中即触发，不管 channel/agentId
}
else if (
  proactiveOffer &&
  LARGE_FILE_INTENT.test(promptText) &&
  FILE_UPLOAD_KEYWORDS.test(promptText) &&
  agentId.startsWith("wecom-")     // ← 仅这条仍卡 wecom-
) {
  reason = "detected-large-file-intent";
}
```

`before_agent_reply` hook 同步：删除 `if (!agentId.startsWith("wecom-")) return;`，靠 `injectedSessions.has(key)` 一致性自动联动。

**结果**：用户在任何渠道（企微/terminal/Claude CLI/dingtalk/...）贴企微错误文本 → 100% 命中 enhance 引导。

### 红线自查

- ✅ 不修龙虾核心
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ 主动「要传大文件」泛意图引导仍卡 wecom-（避免 terminal 用户误触发）

## 6.7.9 — 2026-05-11（large-file-bridge baseUrl 解析 hotfix — 修裸路径缺 https:// 前缀）

### 触发

用户截图 LLM 回复给的链接：

```
📎 大文件上传：文件超过 100MB 无法在企微直接传输，请通过以下链接上传：
👉 /plugins/enhance/upload          ← 裸路径！缺 https://keepermac.huo15.com
上传完成后告诉我，我来处理文件。
```

用户根本点不开 — IM 客户端不会把裸路径补成绝对 URL。

### 根因

`large-file-bridge.resolveUploadUrl()` 在 `config.baseUrl` 没填时直接返裸路径：

```ts
// v6.7.8 旧代码
if (base) return `${base}/plugins/enhance/upload`;
return "/plugins/enhance/upload";   // ← 没拼公网前缀
```

跟 bot-share-link / bot-upload-link 比 — 它们都用了 `resolveBaseUrl()` 多源解析链（env > config > shared share/config.json > bridge 检测外网 URL）。**large-file-bridge 是独立写的，从未接入这套**。

### v6.7.9 改动

```ts
function readSharedBaseUrl(): string | undefined {
  const sharePath = join(homedir(), ".openclaw", "share", "config.json");
  if (!existsSync(sharePath)) return undefined;
  const j = JSON.parse(readFileSync(sharePath, "utf-8"));
  return j?.baseUrl?.trim() || undefined;
}

function resolveUploadUrl(): string {
  if (config?.uploadUrl?.trim()) return config.uploadUrl.trim();
  const base = resolveBaseUrlFromBridge({
    configBaseUrl: config?.baseUrl?.trim() || readSharedBaseUrl(),
    envName: "BOT_BASE_URL",
    fallback: "http://localhost:18789",
  });
  return `${base}/plugins/enhance/upload`;   // ← 永远拼前缀
}
```

baseUrl 解析优先级（跟 bot-share-link / bot-upload-link 完全一致）：

1. `env BOT_BASE_URL`
2. `config.largeFileBridge.baseUrl`
3. `~/.openclaw/share/config.json` 的 `baseUrl`（bot-share-link 用户配过的）
4. bridge `detectBaseUrlFromRequest()` 缓存的外网 URL
5. `http://localhost:18789` fallback（最次）

### 现在的 LLM 回复

```
📎 大文件上传：文件超过 100MB 无法在企微直接传输，请通过以下链接上传：
👉 https://keepermac.huo15.com/plugins/enhance/upload      ← 完整公网 URL ✓
上传完成后告诉我，我来处理文件。
```

### 红线自查

- ✅ 不修龙虾核心 / 不动 cc-media-bridge
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ readSharedBaseUrl 只读 ~/.openclaw/share/config.json（用户主动 enhance_share_set_baseurl 写过）

### 用户操作

```bash
openclaw plugins update @huo15/huo15-openclaw-enhance && openclaw restart
# 然后必须 /new 开新会话 — 老 session 的 prompt 是 freeze 的
```

## 6.7.8 — 2026-05-11（统一上传 URL 到 /plugins/enhance/* + 强化 token 化追踪）

### 触发

用户两连发：

1. **问 token 化**：『这里上传他怎么知道我上传了啥呢，应该 agent 给一个带 hash 的比如 .../upload/2efabc00000 才能追踪吧』
2. **改主意 URL 风格**：『默认用 /plugins/enhance/upload，/lanhuo/upload 这个先删除了』

### 改动

#### A. 删 /lanhuo/upload (v6.7.4) 和 /upload (v6.7.7) 两条 alias route

dashboard.ts 整段 `api.registerHttpRoute({ path: "/lanhuo", ... })` 删除。`/upload` route 同样删（被 OpenClaw control UI SPA 截，注册了也用不上）。

理由：
- `/lanhuo/upload` 跟 cc-media-bridge 的 `/lanhuo/*` namespace 撞，职责混乱
- `/upload` 短 URL 走不通（v6.7.7 实测）
- `/plugins/enhance/*` 是 enhance 自己的 namespace，最清晰

#### B. resolveUploadUrl 默认回 /plugins/enhance/upload

```ts
function resolveUploadUrl(): string {
  if (config?.uploadUrl?.trim()) return config.uploadUrl.trim();
  const base = config?.baseUrl?.trim();
  if (base) return `${base}/plugins/enhance/upload`;
  return "/plugins/enhance/upload";
}
```

#### C. prompt 强化：LLM 优先调 enhance_upload_link 拿 token URL

`large-file-bridge` buildUploadContext 改写：

```
首选：调 enhance_upload_link 工具拿 token 化 URL 给用户
  1. 你调 enhance_upload_link({label: "<本次任务简述>"}) → 返
     https://keepermac.huo15.com/plugins/enhance-upload/<12-hex-token>
  2. 把 URL 发给用户："请通过此链接上传：<url>，传完告诉我"
  3. 用户上传完说"传完了" → 你调 enhance_upload_check({token: "..."}) → 拉清单
  4. 拿到文件路径 → Read 工具读文件分析

备用（仅在 enhance_upload_link 不可用时）：共享 URL /plugins/enhance/upload
  无 token，AI 不知道是谁传了什么，仅适合一次性快速上传
```

`cc-bridge-prompt` 严格区分段同步更新。

### 现在 enhance 暴露的两条上传路径

| URL 模式 | 模块 | 特点 |
|---|---|---|
| `/plugins/enhance/upload` | dashboard.ts | 共享，无 token，AI 不能追踪 |
| `/plugins/enhance-upload/<12-hex-token>` | **bot-upload-link.ts (v6.5.2 已实现!)** | token 隔离，AI 通过 enhance_upload_check 查清单 |

bot-upload-link 三个工具（v6.5.2 已有，无需改）：
- `enhance_upload_link({label?, expireHours?})` — 生成 token + 返 URL
- `enhance_upload_check({token})` — 列该 token 已收文件 + 路径
- `enhance_upload_revoke({token})` — 撤销 token

### 用户场景

```
群里 ZhaoBo 转发 200MB 视频 → 企微推「视频/文件超过100M无法下载」纯文本给 bot
LLM 看到 + large-file-bridge prompt 触发 →
  调 enhance_upload_link({label: "视频分析"}) →
  返 https://keepermac.huo15.com/plugins/enhance-upload/ab12cd1234ef
LLM 群里回："企微 100MB 限制，请打开此链接上传：https://...ab12cd1234ef
            传完跟我说一声"
ZhaoBo 浏览器打开 → 拖拽 200MB 视频 → 流式写到 ~/.openclaw/upload/ab12cd1234ef/files/video.mp4
ZhaoBo 群里："传完了"
LLM 调 enhance_upload_check({token: "ab12cd1234ef"}) → 拿到 [{path:"...", size:200MB}]
LLM Read 路径 → 分析视频 → 回结果
```

### 红线自查

- ✅ 不修龙虾核心
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ /plugins/enhance/* namespace 干净（不跟 cc-media-bridge /lanhuo 混淆）

## 6.7.7 — 2026-05-11（/upload 短 URL 走不通 — 退回 /lanhuo/upload）

### 触发

用户实测 v6.7.6 升级后访问 `https://keepermac.huo15.com/upload`，浏览器**自动跳转**到 `https://keepermac.huo15.com/upload/chat?session=main`（OpenClaw control UI 的 chat panel 路径，错误页）。

### 根因

诊断 `curl -i https://keepermac.huo15.com/upload`：

```
HTTP/2 200
content-type: text/html; charset=utf-8
content-length: 2821

<!doctype html>
<title>OpenClaw Control</title>
```

返回的是 **OpenClaw control UI SPA 的 index.html**（2821 bytes），不是 enhance 的 UPLOAD_HTML（应该 5688 bytes）。

进一步本机对比 enhance 在 OpenClaw gateway 注册的几个 route：

| URL | size | 谁返回 |
|---|---|---|
| `/upload` | 2821 | **OpenClaw control UI SPA**（截了！） |
| `/upload/foo` | 2821 | 同上 |
| `/lanhuo/upload` | 6263 | **enhance UPLOAD_HTML** ✓ |
| `/plugins/enhance/upload` | 6263 | **enhance UPLOAD_HTML** ✓ |

**OpenClaw gateway 的 control UI SPA 在 root path 优先级最高**，plugin 注册的 root-level prefix（如 `/upload`）会被 SPA 接管返 index.html。只有 OpenClaw 让给 plugin 的特定 prefix（`/lanhuo/*`、`/plugins/*`）才能被 plugin route 拦截。

v6.7.6 我在 cc-media-bridge 加的 `/upload` handler 也用不上 — 用户 nginx 反代根 `/` 到 OpenClaw gateway (47.104.78.121:18080)，**不是** cc-media-bridge。

### 改动（v6.7.7 = revert v6.7.6 + prompt 更明确）

1. `large-file-bridge.resolveUploadUrl()` **默认回 `/lanhuo/upload`**（从 `/upload` 退回）
2. `large-file-bridge buildUploadContext` prompt 加显式禁止：
   ```
   /upload 短 URL **不可用**！OpenClaw control UI SPA 占了 root path，
   访问 /upload 会跳 /upload/chat?session=main（错的）
   ```
3. `cc-bridge-prompt` 严格区分段同步更新：
   ```
   📊 /lanhuo = 蓝火任务 dashboard
   📎 /lanhuo/upload = 大文件上传专用页面
   ❌ /upload 短 URL 不可用——OpenClaw control UI SPA 占了 root
   ```

`/upload` route 在 `dashboard.ts` 仍注册（无副作用，被 SPA 截了也不报错），万一未来 OpenClaw 让出 root prefix 可立即生效。

### 短 URL 走通的唯一办法（说明）

要让 `https://keepermac.huo15.com/upload` 工作，**唯一可行路径**是把 nginx `/upload` 单独反代到一个不被 OpenClaw control UI 占用的进程：

```nginx
location ^~ /upload {
  proxy_pass http://47.104.78.121:18790;   # cc-media-bridge native /upload (v2.18.10)
  client_max_body_size 2050M;
  proxy_request_buffering off;
  # ...
}
```

但这要求 cc-media-bridge 在远端 18790 端口暴露公网（默认只 bind 127.0.0.1）。

**红线 #2 不复制龙虾原生 + 不修龙虾核心** → enhance 无法让 OpenClaw control UI 把 `/upload` 让给 plugin。所以现实可用 URL：

| URL | 状态 |
|---|---|
| `https://keepermac.huo15.com/lanhuo/upload` | ✅ **推荐** — 当前默认 |
| `https://keepermac.huo15.com/plugins/enhance/upload` | ✅ 等价备用 |
| `https://keepermac.huo15.com/upload` | ❌ 不可用 — OpenClaw SPA 截 |

### 红线自查

- ✅ 不修龙虾核心 / 不动 control UI SPA 优先级
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged

## 6.7.6 — 2026-05-11（上传 URL 简化到最短 /upload）

### 触发

用户原话：『 [https://keepermac.huo15.com/upload](https://keepermac.huo15.com/lanhuo/upload) 能不能换成这个链接』

之前 v6.7.4 改用 `/lanhuo/upload` 是因为想跟 dashboard `/lanhuo` 心智模型对齐。但用户偏向**最短易记 URL**：

| URL | 长度 | 易记度 |
|---|---|---|
| `/upload` | 7 字符 | ⭐⭐⭐⭐⭐ |
| `/lanhuo/upload` | 14 字符 | ⭐⭐⭐ |
| `/plugins/enhance/upload` | 23 字符 | ⭐ |

### 改动

cc-media-bridge v2.18.9 的 `_lanhuo_strip(path)` 函数：
```python
if path.startswith("/lanhuo/"):
    return path[len("/lanhuo"):]
return path     # ← 直接 /upload 不映射，原样 return
```

所以 `path == "/upload"` 已经命中 cc-media-bridge 的 upload handler（**zero 改动 cc-media-bridge**）。

enhance v6.7.6：
1. **`large-file-bridge.resolveUploadUrl`** 默认 `${base}/upload`（从 `${base}/lanhuo/upload` 简化）
2. **`large-file-bridge buildUploadContext`** prompt 文本提示 LLM 用 `/upload` 短 URL
3. **`cc-bridge-prompt`** 严格区分段落：
   ```
   📊 /lanhuo = 蓝火任务 dashboard
   📎 /upload = 大文件上传专用页面（最短最易记）
       备用等价 URL：/lanhuo/upload / /plugins/enhance/upload
   ```

### 等价性保证

三个 URL **完全等价**（cc-media-bridge v2.18.9 已 native 支持，nginx 不用配 location）：

| URL | 路径流转 |
|---|---|
| `/upload` ⭐ | _lanhuo_strip 不映射 → handle_upload |
| `/lanhuo/upload` | _lanhuo_strip 剥成 `/upload` → handle_upload |
| `/plugins/enhance/upload` | enhance dashboard.ts 注册的 OpenClaw gateway route（如果 nginx 反代到 gateway） |

本机 diff 验证：`/upload` 和 `/lanhuo/upload` 返回完全相同的 5688 bytes HTML。

### 用户操作

升级到 v6.7.6 后 LLM 给出的回复将默认推 `/upload` 短 URL：

```
"企微聊天文件上限 100MB，2GB 以内大文件都可以通过下面这个链接上传：
https://keepermac.huo15.com/upload
（流式上传，浏览器拖拽即可，传完告诉我我来处理。）"
```

### 红线自查

- ✅ 不修龙虾核心 / 不动 cc-media-bridge（v2.18.9 已 native 支持）
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ /lanhuo/upload 兼容 alias，老的 prompt cache / few-shot example 仍工作

## 6.7.5 — 2026-05-11（上传支持 2GB 单文件 — 流式写盘不 OOM）

### 触发

用户实测企微大文件场景，说："要 2G 以内都可以"。

但 v6.7.4 的 `handleUpload` 是 v5.x 老实现：

```ts
const chunks: Buffer[] = [];
for await (const chunk of req) chunks.push(Buffer.from(chunk));  // ← 全 buffer 进内存
const parsed = parseMultipart(Buffer.concat(chunks), boundary);   // ← concat 出一个超大 Buffer
```

2GB 文件走这条路径 **100% OOM** —— Node V8 默认 heap ~1.5GB，Buffer.concat 出 2GB 超大 buffer 直接撞 `Cannot allocate Buffer`。

### 改动

#### 1. handleUpload 新增 octet-stream 流式路径

`Content-Type: application/octet-stream` (或非 multipart) 走 `handleStreamingUpload`：

```ts
async function handleStreamingUpload(req, res, contentLengthHint) {
  const safeName = sanitizeUploadFilename(req.headers["x-filename"]);
  const destPath = join(getUploadDir(), `${Date.now()}-${safeName}`);
  let receivedBytes = 0;
  const ws = createWriteStream(destPath);

  return new Promise((resolve) => {
    req.on("data", (chunk) => {
      receivedBytes += chunk.length;
      if (receivedBytes > UPLOAD_MAX_BYTES) {  // 2GB 硬上限
        req.destroy(); ws.destroy(); rmSync(destPath);
        res.writeHead(413); res.end("..."); resolve(true); return;
      }
      // 背压：write 返 false 时暂停 req，等 drain 再 resume
      const canContinue = ws.write(chunk);
      if (!canContinue) {
        req.pause();
        ws.once("drain", () => req.resume());
      }
    });
    req.on("end", () => ws.end(() => { sendJson(res, {...}); resolve(true); }));
    req.on("error", () => { /* abort + cleanup */ });
    ws.on("error", () => { /* abort + cleanup */ });
  });
}
```

- **2GB 硬上限**：`content-length` 头预检 + 边读边累计字节，超过主动 destroy + 删盘
- **背压处理**：`ws.write` 返 `false` 时 `req.pause()`，避免 client 推太快内存堆积
- **错误清理**：req/ws 任一抛错都 cleanup 已写部分文件

#### 2. multipart/form-data 老路径保留但加 100MB 上限

兼容旧 form 上传，但超过 100MB 直接 413 + 提示用 octet-stream：

```ts
if (contentLength > MULTIPART_INMEM_MAX /* 100MB */) {
  res.writeHead(413);
  res.end(JSON.stringify({
    error: "multipart 模式仅支持 <100MB；2GB 以内大文件请改用 application/octet-stream 头",
    hint: "fetch(url, { method: 'POST', body: file, headers: { 'Content-Type': 'application/octet-stream', 'X-Filename': file.name } })",
  }));
}
```

#### 3. UPLOAD_HTML 默认走 octet-stream

```js
xhr.open('POST', location.pathname, true);  // 同源相对路径
xhr.setRequestHeader('Content-Type', 'application/octet-stream');
xhr.setRequestHeader('X-Filename', encodeURIComponent(file.name));
xhr.send(file);  // 直接发 File 对象，浏览器自动流式
```

- `location.pathname` 让同一份 HTML 既能在 `/lanhuo/upload` 跑也能在 `/plugins/enhance/upload` 跑（自动同源相对路径）
- `xhr.send(file)` 直发 File 对象，浏览器原生 stream，**不全 buffer 进 RAM**
- progress 实时更新：`100 MB / 1.5 GB (8.5%)` 这种细粒度显示
- 客户端预检：选 >2GB 文件直接 alert，不发请求

#### 4. large-file-bridge prompt 更新

```
回复模板:
"企微聊天文件上限 100MB，2GB 以内大文件都可以通过下面这个链接上传：
${url}
（流式上传，浏览器拖拽即可，传完告诉我我来处理。）"
```

#### 5. nginx 配置补充

`client_max_body_size 2050M` 让反代不被 nginx 自己截胡（默认 1MB），keepermac.huo15.com 的 server block 都要加：

```nginx
server {
  client_max_body_size 2050M;  # 留 50MB margin

  location /lanhuo/upload {
    proxy_pass http://localhost:18789;
    proxy_request_buffering off;  # ← 关键：让上传也是流式，nginx 不缓存全包
    proxy_read_timeout 600s;       # 慢网传 2GB 可能 >5 分钟
  }
  location /lanhuo {
    proxy_pass http://localhost:18790;
  }
}
```

`proxy_request_buffering off` 让 nginx 把 request body 边收边传给后端 — 否则 nginx 会先缓存 2GB 到磁盘再转发，再被后端流式收一遍，两遍 IO 浪费。

### 红线自查

- ✅ 不修龙虾核心
- ✅ 零 child_process / 零新 npm 依赖（fs.createWriteStream + http 原生 stream）
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ Path traversal sanitizer 仍生效（`sanitizeUploadFilename`）
- ✅ content-length 头预检 + 边读累计双闸门，防恶意大请求

### 用户操作

```bash
# 1. 升级
openclaw plugins update @huo15/huo15-openclaw-enhance && openclaw restart

# 2. nginx 加 client_max_body_size + proxy_request_buffering off
# 编辑 /etc/nginx/sites-enabled/keepermac.huo15.com 加上面那段
sudo nginx -t && sudo nginx -s reload

# 3. 浏览器测试: https://keepermac.huo15.com/lanhuo/upload
# 拖一个 500MB+ 文件，progress 应该实时更新到 100%
```

## 6.7.4 — 2026-05-11（修 LLM 把 /lanhuo 当上传链接 + 同步 v6.7.2/3 + preflight 加固）

### 触发

用户实测 LLM 在企微大文件场景给出的回复：

> 这是企微的文件传输限制（最大 100MB），超过的话：
> 👉 `https://keepermac.huo15.com/lanhuo`
> 通过这个 dashboard 上传大文件，然后把链接发给我处理。

但 `/lanhuo` 是 **cc-media-bridge 的任务 dashboard**，根本不是上传页！LLM 推理混淆了。

用户原话："是不是 `/lanhuo` 后面再加个内容，加个后缀然后写个上传页面比较合适"。

### 根因

`cc-bridge-prompt` 模块给 LLM 注入："用户唯一的可视化入口是 bridge 自带 dashboard：${base}/lanhuo"——LLM 把这条引导泛化用，看到『上传』场景也推 `/lanhuo`。

`large-file-bridge` 给 LLM 注入的是 `${base}/plugins/enhance/upload`（正确的上传页），但 LLM 觉得这个 URL 太长、不像"用户常用入口"，**幻觉**改成 `/lanhuo`。

### v6.7.4 改动

#### 1. `dashboard.ts` 新增 `/lanhuo/upload` 别名

```ts
api.registerHttpRoute({
  path: "/lanhuo",
  match: "prefix",
  handler: async (req, res) => {
    const url = parseUrl(req);
    if (url.pathname === "/lanhuo/upload") {
      if (req.method === "POST") return handleUpload(req, res);
      sendHtml(res, UPLOAD_HTML);  // ← 跟 /plugins/enhance/upload 同一份 HTML
      return true;
    }
    return false;  // 其他 /lanhuo/* 不接管，让 nginx fallback 到 cc-media-bridge
  },
});
```

用户 nginx 加一条规则：

```nginx
location /lanhuo/upload {
  proxy_pass http://localhost:18789;   # OpenClaw gateway
}
location /lanhuo {
  proxy_pass http://localhost:18790;   # cc-media-bridge
}
```

（注意：specific 路径要在前，nginx 才会优先匹配）

#### 2. `large-file-bridge` 默认推 `/lanhuo/upload`

```ts
function resolveUploadUrl(): string {
  if (config?.uploadUrl?.trim()) return config.uploadUrl.trim();
  const base = config?.baseUrl?.trim();
  if (base) return `${base}/lanhuo/upload`;   // v6.7.4: 默认从 /plugins/enhance/upload 改为 /lanhuo/upload
  return "/lanhuo/upload";
}
```

#### 3. prompt 文本明确区分 dashboard / upload

`cc-bridge-prompt`：

```
**严格区分：/lanhuo 跟 /lanhuo/upload 是不同 URL（v6.7.4）**：
📊 /lanhuo = 蓝火任务 dashboard（看 cc-media-task 进度，不是上传文件页面）
📎 /lanhuo/upload = 大文件上传专用页面（企微 >100MB 文件走这里）
**不要混用**：用户问任务 → /lanhuo；用户要上传大文件 → /lanhuo/upload。
```

`large-file-bridge`：

```
⚠️ 严格区分（v6.7.4）：
- 上传专用页面 = ${url}（这是你**必须**给用户的链接）
- /lanhuo = 蓝火任务 dashboard，**不是**上传页！不要把它当上传链接给用户！
```

#### 4. 同步补 v6.7.2 / v6.7.3 改动到 git

之前另一会话只 `npm publish` 了但**没 git commit/push**：v6.7.2 (description 误标) + v6.7.3 (真补 `before_agent_reply` hook)。本期把 v6.7.3 tarball 里的 `large-file-bridge.ts` 拉回本地（含 `before_agent_reply` 强制 appendText 上传链接的兜底逻辑），与 v6.7.4 一起 commit + push。

#### 5. release.sh preflight 新增第 12 项校验

防 v6.7.2 那种"description 提到 `before_agent_reply` 但代码没加"的误发：

```bash
# 抓 description 里的 hook 名 → grep src/ + index.ts 验证 api.on() 真注册
HOOK_NAMES=(before_prompt_build before_model_resolve before_agent_reply ...)
for HK in "${HOOK_NAMES[@]}"; do
  if echo "$DESC" | grep -q "$HK"; then
    grep -qrE "api\.on\(\s*[\"']${HK}[\"']" src/ index.ts || {
      log_err "description 提到 hook \"$HK\" 但源码没注册"
      exit 1
    }
  fi
done
```

### 用户操作

1. 升级：
   ```bash
   openclaw plugins update @huo15/huo15-openclaw-enhance && openclaw restart
   ```

2. nginx 配 `/lanhuo/upload` 优先反代到 OpenClaw gateway：
   ```nginx
   # 在 keepermac.huo15.com 的 server block 里
   location /lanhuo/upload {
     proxy_pass http://localhost:18789;
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     client_max_body_size 100M;   # OpenClaw 自己也允许 100M+
   }
   location /lanhuo {
     proxy_pass http://localhost:18790;  # cc-media-bridge dashboard
   }
   ```

3. 验证：浏览器访问 `https://keepermac.huo15.com/lanhuo/upload` 应该看到带拖拽 dropzone 的上传 HTML 页。

### 红线自查

- ✅ 不修龙虾核心 / 不动 cc-media-bridge
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ `/lanhuo/upload` 别名只接 `/lanhuo/upload` 单路径，其他 `/lanhuo/*` 让出来给 cc-media-bridge

## 6.7.3 — 2026-05-11（large-file-bridge 加 before_agent_reply 强制兜底上传链接）

另一会话独立发布，git 没 push（v6.7.4 一起补回）。

`large-file-bridge` 新增 `before_agent_reply` hook：LLM 输出 final/block 消息时，如果该 session 之前触发过 large-file-bridge prompt 注入但 LLM 回复里**没**含 `upload / /plugins/enhance / 上传链接 / 上传页面` 关键词 → hook 强制 appendText 一段上传链接 suffix 到 LLM 输出末尾。

第三层防御（第 1 层 prompt 引导 / 第 2 层硬性 prompt 模板 / 第 3 层 appendText 兜底）。

## 6.7.2 — 2026-05-11（误发：description 标了 before_agent_reply 但代码忘加）

另一会话独立发布，git 没 push。description 误写"v6.7.2 before_agent_reply 强制插入上传链接"但代码没加 before_agent_reply hook。v6.7.3 立刻补齐。

v6.7.4 release.sh 加 preflight 第 12 项校验防再次出现。

## 6.7.1 — 2026-05-11（large-file-bridge 注入更强制引导文本）

另一会话发布，已 git push。`buildUploadContext` 从软引导改"必读 + 标准回复模板"，让 LLM 直接给上传链接，不再先问诊断问题。

## 6.7.0 — 2026-05-11（large-file-bridge channel 检测改 agentId.startsWith）

另一会话发布，已 git push。修一个 silently-failing bug：之前 `ctx.channel` 在 before_prompt_build 阶段为空 → channel !== "wecom" 总是 true → hook 早 return → large-file-bridge **从未真生效**。改用 `agentId.startsWith("wecom-")` 判断后才激活。

## 6.6.9 — 2026-05-11（config-doctor 加 model-id 大小写校验）

### 触发

用户 v6.6.8 升级后**仍撞**同问题。新截图关键：

```
/clear → ⚠ Something went wrong
/new → ✅ New session started
你好 → ⚠ Something went wrong   ← 新 session 第一条简短消息也撞！
```

**新会话第一条『你好』也撞**——完全跟 ctx 用量、跟 hook 都无关：
- 不是 ctx 满（fresh session）
- 不是 hook 抛（v6.6.8 已系统性 safeHook 包裹全部 28 hook）
- **100% 是 OpenClaw → provider 端的 LLM 调用本身失败**

### 根因（最大嫌疑）

用户截图 cfg：
```json
"agents.defaults.model": {
  "primary": "deepseek/DeepSeek-V4-Pro",        ← 大写驼峰
  "fallbacks": [
    "minimax/MiniMax-M2.7",                      ← 大写驼峰
    "deepseek/DeepSeek-V4-Flash"                 ← 大写驼峰
  ]
}
```

但 **deepseek 后端 API 只认全小写带连字符**：`deepseek-v4-pro` / `deepseek-v4-flash`。v6.6.4 commit 实测就是这条：

```
ERROR: FailoverError: provider rejected the request schema
WARN model_fallback_decision:
  requestedProvider: deepseek
  errPreview: "400 The supported API model names are
    deepseek-v4-pro or deepseek-v4-flash, ..."
```

**整个 fallback 链都因为同样的命名错全部 400** → chain_exhausted → "Something went wrong"。

每次新会话第一次调用都立刻撞 → 用户体感就是『发什么都不行』。

### 改动

`config-doctor.ts` 新增 `checkModelIdRegistration(cfg)`：

```ts
// 1. 收集 cfg.agents.defaults.model.{primary, fallbacks} 全部 fullId
// 2. 每个 fullId split → provider + bareId
// 3. 在 cfg.models.providers[provider].models 找 bareId 完全匹配
// 4a. 找到 → ok
// 4b. case-insensitive 命中 → 错（大小写不一致）+ 给精确 fix
//      "把 'deepseek/DeepSeek-V4-Pro' 改成 'deepseek/deepseek-v4-pro'"
// 4c. 完全不存在 → 错 + 列出已注册的近似 candidates
// 4d. provider 不存在 → 错
```

启动期跑（fire-and-forget），结果走 `notifyQueue` 推到 dashboard + log warn。`enhance_config_doctor` 工具也会返回这些 issue。

### 用户应该立刻看

升级 v6.6.9 后调 `enhance_config_doctor` 工具（在能调通的会话/终端里），或者直接看 dashboard，会显示类似：

```
❌ [model-id-case-mismatch] agents.defaults.model 中 "deepseek/DeepSeek-V4-Pro"
   的 bare id "DeepSeek-V4-Pro" 在 cfg.models.providers.deepseek.models 没找到
   完全匹配（大小写敏感）。实际注册的是 "deepseek-v4-pro"——大小写不一致会导致
   LLM 调用 400 chain_exhausted ("Something went wrong")
   → 修复: 把 agents.defaults.model 里 "deepseek/DeepSeek-V4-Pro" 改成
     "deepseek/deepseek-v4-pro"，或在 cfg.models.providers.deepseek.models
     里把 id 改成 "DeepSeek-V4-Pro"
```

### 红线自查

- ✅ 不修龙虾核心
- ✅ 完全只读 ~/.openclaw/openclaw.json（红线 #1）
- ✅ 不调 child_process（红线 #4） — 修复命令是文字描述给用户/cron-cli 执行
- ✅ tier=1 minimal 也启用

### 用户操作（紧急）

```bash
# 1. 升级
openclaw plugins update @huo15/huo15-openclaw-enhance
openclaw restart

# 2. 查日志看真实错误（最直接）
tail -500 ~/.openclaw/logs/gateway.err.log | grep -iE "ERROR|deepseek|minimax|400|401|chain_exhausted|provider rejected" | tail -30

# 3. 手动看 openclaw.json model id 大小写
python3 -c "import json; cfg=json.load(open('$HOME/.openclaw/openclaw.json')); m=cfg['agents']['defaults']['model']; print('primary:', m.get('primary')); print('fallbacks:', m.get('fallbacks')); print('---registered---'); [print(p+':', [m.get('id') for m in cfg['models']['providers'][p].get('models',[])]) for p in cfg['models']['providers']]"
```

最直接的修法（如果 ID 大小写不对）：

```bash
# 把 model 配置改成跟 providers 注册的完全一致
# 通常 deepseek 应该是全小写：
sed -i.bak 's|"deepseek/DeepSeek-V4-Pro"|"deepseek/deepseek-v4-pro"|g; s|"deepseek/DeepSeek-V4-Flash"|"deepseek/deepseek-v4-flash"|g' ~/.openclaw/openclaw.json
# minimax 可能确实是大写驼峰，先看 providers.minimax.models 实际 id 再改
openclaw restart
```

## 6.6.8 — 2026-05-11（**全模块 hook 系统性防御** — 修反复『Something went wrong』根因）

### 触发

用户 v6.6.5 / 6.6.6 / 6.6.7 升级后**反复**截图同一个错误：

```
⚠ Something went wrong while processing your request.
  Please try again, or use /new to start a fresh session.
```

前三个 hotfix 都没命中：
- v6.6.5 doc sync
- v6.6.6 ctx-watchdog 6 hook safeHook 包裹
- v6.6.7 user-config 优先强切（修硬编码 LONG_CTX_CANDIDATES 设计错误）

### 终极根因

`grep -rn "api\.on(" src/modules/ | wc -l` → **28 个 hook 跨 17 个模块**。

v6.6.6 只把 **ctx-watchdog 的 6 个** safeHook 包了，**剩 22 个 hook 完全裸奔**：

| 文件 | hook 数 |
|---|---|
| `session-lifecycle.ts` | 5 |
| `tool-safety.ts` | 2 |
| `cc-bridge-dispatch-harness.ts` | 2 |
| `workflow-hooks.ts` | 1 |
| `task-planner.ts` | 1 |
| `session-recap.ts` | 1 |
| `session-bridge.ts` | 1 |
| `self-check.ts` | 1 |
| `scheduled-tasks-bridge.ts` | 1 |
| `prompt-enhancer.ts` | 1 |
| `native-memory-surfacer.ts` | 1 |
| `model-router.ts` | 1 |
| `mode-gate.ts` | 1 |
| `large-file-bridge.ts` | 1 |
| `cc-bridge-pre-fetch.ts` | 1 |
| `cc-bridge-keyword-dispatch.ts` | 1 |

任一抛 unhandled exception → OpenClaw 整个请求 fail-fast → 通用错误页。

### v6.6.8 改动

新建 `src/utils/safe-api-wrapper.ts`（~70 行）：

```ts
export function wrapApiForSafeHooks(api: OpenClawPluginApi): OpenClawPluginApi {
  if ((api as any).__enhance_safehook_wrapped__) return api;
  const originalOn = api.on.bind(api);

  const safeOn = ((hookName, handler, opts) => {
    const wrappedHandler = (event, ctx) => {
      try {
        return handler(event, ctx);
      } catch (err) {
        api.logger.error(`[enhance safeHook] ${hookName} 异常已捕获: ${err.message}`);
        // 调试用：stack 第一行
        if (err.stack) {
          const firstFrame = err.stack.split("\n").slice(1, 3).join(" | ");
          api.logger.error(`[enhance safeHook] stack: ${firstFrame}`);
        }
        return undefined;
      }
    };
    return originalOn(hookName, wrappedHandler, opts);
  });

  return new Proxy(api, {
    get(target, prop, receiver) {
      if (prop === "on") return safeOn;
      if (prop === "__enhance_safehook_wrapped__") return true;
      return Reflect.get(target, prop, receiver);
    },
  });
}
```

`index.ts` register 入口：

```ts
register(rawApi) {
  const api = wrapApiForSafeHooks(rawApi);  // 一次性 wrap
  // ... 所有模块都拿 wrapped api
}
```

**效果**：所有 28 个 hook 自动包 try/catch，不用改 17 个模块文件。再有任何 hook 抛——log 一行 stack 信息然后 return undefined，OpenClaw 主流程完全不受影响。

### 怎么定位真正的根因

升级 v6.6.8 后用户再发『麻将观战可行性研究报告，用 word 写一份给我』：

**如果不再撞错** → 某个 hook 在抛被 safeHook catch 了。日志看 `[enhance safeHook] <hookName>` 行就知道是哪个 hook，stack frame 第一行就知道是哪个模块。

**如果还撞错** → 100% 不是 enhance hook 抛了。是 OpenClaw 自己或 provider 端的问题。需要看 `~/.openclaw/logs/gateway.err.log` 实际 ERROR trace。

### 红线自查

- ✅ 不修龙虾核心
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ Proxy wrap 是 transparent：所有其他 api.* 方法（registerTool / registerMemory* / logger / runtime 等）原样透传
- ✅ marker 防重复 wrap：`__enhance_safehook_wrapped__` 标记位避免 hot-reload 时双层 proxy
- ✅ logger 抛也吞掉：避免无限循环

## 6.6.7 — 2026-05-11（强切候选改读用户 openclaw.json，修硬编码 LONG_CTX_CANDIDATES 设计错误）

### 触发

用户截图明确指出：

```
openclaw.json:
  agents.defaults.model.primary = "deepseek/DeepSeek-V4-Pro"
  agents.defaults.model.fallbacks = [
    "minimax/MiniMax-M2.7",
    "deepseek/DeepSeek-V4-Flash"
  ]
```

**用户原话**："你应该看 openclaw.json 里面配置的几个模型，按照这个里面的配置切换"

### 设计错误回溯

v6.5.5 起 ctx-watchdog 强切用的是硬编码 `LONG_CTX_CANDIDATES_DEFAULT`：

```ts
const LONG_CTX_CANDIDATES_DEFAULT = [
  "claude-opus-4.7-1m",   // ← 用户没装 anthropic provider
  "gemini-2.5-pro",        // ← 用户没装 google-ai-studio provider
  "kimi-k2",               // ← 用户没装 moonshot provider
  // ... 全部跟用户实际配置不匹配
];
```

用户实际机器装的是 **deepseek + minimax**，硬编码全部 miss → v6.6.4 的三重过滤把候选筛干净 → 强切静默失败（"FORCE-escalate skipped: no long-ctx model available"）。

这是**根本性的设计错误**：v6.5.5 的"真实切换闭环"实际上**对国内用户从未真正工作过**——只有装了 anthropic/google/moonshot 国际 provider 的用户才会被强切。

### v6.6.7 改动

新增 `readUserAgentModels(cfg)`：

```ts
interface UserModelCandidate {
  fullId: string;       // "deepseek/DeepSeek-V4-Pro"
  bareId: string;       // "DeepSeek-V4-Pro"
  provider: string;     // "deepseek"
  contextWindow: number;
  costInPerM?: number;
  costOutPerM?: number;
}

function readUserAgentModels(cfg: unknown): UserModelCandidate[] {
  // 1. 读 cfg.agents.defaults.model.{primary, fallbacks}（按顺序去重）
  // 2. 每个 fullId split → provider + bareId
  // 3. join cfg.models.providers[<provider>].models[<bareId>] 拿 contextWindow + cost
  // 4. 返完整候选列表
}
```

新增 `pickEscalateTargetFromUserConfig`：
- 过滤：`ctx > current.ctxMax`（严格更大才有意义切）+ 非 banned + 非当前 model
- 排序：默认 ctx 降序（最大优先），preferCheap 时 cost 升序

`before_model_resolve` 优先级：
1. **优先**：`readUserAgentModels(cfg)` → `pickEscalateTargetFromUserConfig` → 返 `{modelOverride, providerOverride}`
2. **兜底**：用户配置完全没读到 → 退回 v6.6.4 硬编码 `LONG_CTX_CANDIDATES_DEFAULT` 路径

`enhance_route_to_long_ctx` 工具同步：
- target 参数支持完整 fullId（如 `"minimax/MiniMax-M2.7"`）
- 自动选时优先用用户配置
- 错误提示返用户配置候选清单

`enhance_ctx_status` 工具新增 `userConfigCandidates` 字段：

```jsonc
{
  "userConfigCandidates": [
    { "fullId": "deepseek/DeepSeek-V4-Pro", "ctxMax": 131072, "costInPerM": 0.14 },
    { "fullId": "minimax/MiniMax-M2.7", "ctxMax": 204800, "costInPerM": 1.0 },
    { "fullId": "deepseek/DeepSeek-V4-Flash", "ctxMax": 131072, "costInPerM": 0.14 }
  ],
  "availableLongCtxModel": "minimax/MiniMax-M2.7",  // ctx 比当前大的首选
  "shouldEscalate": true
}
```

### 用户场景验证

| Step | 之前（v6.6.6）| 现在（v6.6.7）|
|---|---|---|
| 用户 primary 用 deepseek-v4-pro 跑到 95% | 在 LONG_CTX_CANDIDATES 找 kimi-k2 → installedProviders 没 moonshot → 跳过 → 不强切 | 在 user config 找 → minimax-m2.7 ctx 200K > 当前 128K → 强切 `{modelOverride: "minimax/MiniMax-M2.7", providerOverride: "minimax"}` ✓ |
| 当前已是 user config 最大 ctx | 同上不强切 | 同上不强切，banner 提示 /compact |
| 用户没配 fallbacks 也无 model 字段 | 走硬编码 | 走硬编码兜底（兼容旧行为）|

### 红线自查

- ✅ 不修龙虾核心 / 不复制 isContextOverflowError
- ✅ 不抢龙虾 model-fallback
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ 用户没读到配置时退回硬编码（兼容性 fallback）
- ✅ readUserAgentModels 跟 model-router 的 scanAvailableModels 用相似 schema 但读不同字段（model-router 读 cfg.models.providers，我读 cfg.agents.defaults.model.{primary,fallbacks} + join providers）

### 后续

如果 v6.6.7 升级后用户『麻将观战可行性报告』仍撞错 → 一定不是 ctx-watchdog，看 `~/.openclaw/logs/gateway.err.log` ERROR 行确定根因。

## 6.6.6 — 2026-05-11（ctx-watchdog 6 个 hook 全 safeHook 防御包裹）

### 触发

用户实测 v6.6.5 升级后**再次**截图同一个错误：

```
⚠ Something went wrong while processing your request.
  Please try again, or use /new to start a fresh session.
```

请求是简短的『麻将观战系统可行性研究报告，用 word 写一份给我』——不像 ctx 满，也不像跨 provider 强切（v6.6.4 已经 fix 了那个）。

唯一合理解释：**某个 enhance hook 在 edge case 抛 unhandled exception**。OpenClaw 接到 hook throw 后整个请求 fail-fast，UI 显示通用错误页。审计 `context-watchdog.ts` 发现 **7 个 hook handler 0 处 try/catch 包裹**——任何 hook 抛都会撞主流程。

最高嫌疑 `before_model_resolve` (priority=100，最早跑)：
- `api.runtime?.config?.loadConfig?.()` 在某些 OpenClaw runtime 版本可能 throw（SDK 版本差异）
- `readInstalledProviders` 解析 cfg 时如果格式异常会 throw
- `estimatePromptTokens(event)` 在 event 字段 unexpected shape 时 throw

### 改动

新增 `safeHook(hookName, body)` helper（在 registerContextWatchdog 内 closure 捕获 api.logger）：

```ts
const safeHook = <T>(hookName: string, body: () => T | undefined): T | undefined => {
  try {
    return body();
  } catch (err) {
    api.logger.error(
      `[ctx-watchdog] ${hookName} hook 异常已捕获（不影响主流程）: ${(err as Error)?.message ?? err}`,
    );
    return undefined;
  }
};
```

包裹全部 7 处 hook handler：

| Hook | 风险点 |
|---|---|
| `llm_output` | usage 字段 unexpected shape / runId 解析 |
| `llm_input` | event.prompt 非 string / attachments 异常 |
| `subagent_spawned` | event.childSessionKey undefined |
| `subagent_ended` | event.targetSessionKey undefined |
| `after_compaction` | resolveCtxMax/originalModel 解析 |
| `before_prompt_build` | revertSuggestPending / evalThresholdBanner 链式 |
| `before_model_resolve` (priority=100) | **最高风险** — api.runtime / loadConfig / readInstalledProviders / estimatePromptTokens |

`readInstalledProviders(api.runtime?.config?.loadConfig?.())` 单独再 try/catch（防 `api.runtime` 字段不存在或 `loadConfig` 抛 — SDK 版本差异）。

### 红线自查

- ✅ 不修龙虾核心
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ 任何 enhance hook 抛 → log + 返 undefined，不影响 OpenClaw 主流程（"扩展挂了不能拖累主功能"原则）

### 后续

如果 v6.6.6 升级后用户仍撞同样错误 → 一定不是 ctx-watchdog 而是 OpenClaw 内部或其他 enhance 模块。需要用户提供 `~/.openclaw/logs/gateway.err.log` 实际 trace。

## 6.6.5 — 2026-05-11（doc sync — SKILL.md / package.json description 跟版本号对齐）

### 触发

发现 SKILL.md description 字段还停留在 v6.6.2（但 `version: 6.6.4`）——release.sh preflight 只校验 version 数字相等，没校验 description 文本和 version 的语义一致性。

ClawHub manifest 用 SKILL.md description 字段做插件介绍——用户在 ClawHub 浏览插件看到的还是『v6.6.2 runId 去重 + 静音工具』，不知道 v6.6.4 的关键 hotfix（强切 long-ctx 跨 provider 撞 400）。

### 改动

仅 doc sync，无代码改动：

- `SKILL.md` description 同步到 v6.6.5（含 v6.6.3/4/5 hotfix 闭环）
- `package.json` description 同步到 v6.6.5

ClawHub manifest 重新发布后，新用户看到的描述跟实际能力对齐。

## 6.6.4 — 2026-05-11（修跨 provider 强切撞 400 mismatch — long-ctx 选型必带 providerOverride）

### 触发

赵博实测：cfg 改成 `primary=deepseek-v4-flash, fallbacks=[deepseek-v4-pro, minimax/MiniMax-M2.7, ...]` 后，让 BOT 写 word 撞：

```
ERROR: FailoverError: LLM request failed: provider rejected the request schema or tool payload
WARN model_fallback_decision:
  requestedProvider: deepseek
  errPreview: "400 The supported API model names are deepseek-v4-pro or deepseek-v4-flash, 
               but you passed minimax/MiniMax-M2.7."
  finalOutcome: chain_exhausted
```

DeepSeek API 收到 `minimax/MiniMax-M2.7`——OpenClaw 把 fallback model id 整串塞给当前 session 的 provider client，跨 provider 时撞 400。

### 双重根因（enhance 自己的 bug）

| Bug | 位置 | 影响 |
|---|---|---|
| `LONG_CTX_CANDIDATES_DEFAULT` 只有裸 model id（无 provider prefix） | `context-watchdog.ts:96-104` | 强切返 `modelOverride` 时不知道对应 provider |
| 强切 hook 只返 `modelOverride` 不返 `providerOverride` | `context-watchdog.ts:1051` 等 3 处 | OpenClaw 核心拿到 model id 但用旧 session provider 调 → API 拒 400 |
| `pickLongCtxModel` 没过滤"用户已注册 provider" | `context-watchdog.ts:434-444` | 选了 claude/gemini/kimi 这种用户没装的 model → 必失败 |

之前 `pickLongCtxModel` 逐个 prefix 试 ban check（`sidus/${c}` / `minimax/${c}` / `anthropic/${c}` ...）— 暴露了"裸 model id 不知道 provider"的设计 confusion。

### 修法（不修 OpenClaw 核心）

`PluginHookBeforeModelResolveResult` SDK 类型支持 `providerOverride` 字段（`hook-before-agent-start.types.d.ts`），enhance 一直**没用**。本版补上。

1. **新增 `MODEL_TO_PROVIDER_MAP`**（裸 model id → provider）：
   ```ts
   const MODEL_TO_PROVIDER_MAP: Record<string, string> = {
     "claude-opus-4.7-1m": "anthropic",
     "gemini-2.5-pro": "google-ai-studio",
     "kimi-k2": "moonshot",
     "minimax-m2": "minimax",
     "deepseek-v3.2": "deepseek",
     // ...约 20 个常见 long-ctx model
   };
   ```

2. **新增 `readInstalledProviders(cfg)`** — 从 `cfg.agents.defaults.models` keys 推已注册 provider Set。

3. **`pickLongCtxModel` 加 `installedProviders` 参数过滤**：
   ```ts
   const provider = MODEL_TO_PROVIDER_MAP[c];
   if (!provider) return false;  // 未知 provider 的 candidate 跳
   if (installedProviders.size > 0 && !installedProviders.has(provider)) return false;
   ```

4. **强切 hook + `enhance_route_to_long_ctx` tool 同时返 providerOverride**：
   ```ts
   const targetProvider = MODEL_TO_PROVIDER_MAP[target];
   const targetFullId = targetProvider ? `${targetProvider}/${target}` : target;
   return targetProvider
     ? { modelOverride: targetFullId, providerOverride: targetProvider }
     : { modelOverride: target };
   ```

5. **enhance_route_to_long_ctx 显式 target 也校验 provider 已注册**，给错时返 hint 列已装 providers。

### 用户场景（赵博）效果

cfg 当前装 `deepseek + minimax`：

- candidates 过滤：`gemini/claude/kimi` 全去掉（provider 没装），剩 `minimax-m2` (200K) 不算 long-ctx → 返 null
- **不强切**，banner 提示用户 /compact
- 主路径走 cfg.fallbacks `[deepseek-v4-pro]`（同 provider 安全），不撞跨 provider 拼接 bug

### 测试

- `tsc --noEmit` 干净
- 已有 vitest 全跑通

### 不变

- v6.6.3 cc-bridge-prompt 严格触发条件
- v6.6.2 runId 去重 + 静音工具
- v6.6.0 cost-aware + channel 差异化
- v6.5.7 sidus 清理 + subagent 累加
- v6.5.6 ctx-usage-db 持久化
- v6.5.5 真实切换闭环（≥95% 强切）

---

## 6.6.2 — 2026-05-11（上下文守护『runId 去重 + 静音工具』bug fix + UX）

### 触发

v6.6.0 上线后，路线图剩余 P3 / P2 项里挑两个最痛的：

1. **P3-13 龙虾 model-fallback retry 重算 bug**：龙虾 `model-fallback.ts:1011` 检测 ctx overflow 后会触发 retry，retry 时 `llm_output` 同一个 `runId` 会**再 emit 一次**——ctx-watchdog 不去重则 token / cost 累加翻倍，预警提前误触发。
2. **P2-10 用户烦提醒**：70%-85% 阶段 banner 反复出现，长会话用户希望能临时静音，等任务完了再恢复。

### 改动

#### A. P3-13 runId 去重（context-watchdog.ts）

`SessionUsage` 新增字段：

```ts
seenRunIds: Set<string>;  // bounded 20 FIFO, in-memory only
```

`llm_output` 入口：

```ts
const runId = String(event?.runId ?? "").trim();
if (runId) {
  if (s.seenRunIds.has(runId)) {
    // retry 重复 emit — 跳过 (dedup)
    return;
  }
  s.seenRunIds.add(runId);
  if (s.seenRunIds.size > SEEN_RUNIDS_LIMIT) {
    // FIFO eviction（Set 保持插入顺序）
    s.seenRunIds.delete(s.seenRunIds.values().next().value);
  }
}
```

仅内存（不持久化）—— 重启后 retry 风险自动消失，无需 sqlite schema 复杂化。

#### B. P2-10 enhance_ctx_silence 工具

新工具：

```jsonc
enhance_ctx_silence({ minutes: 1-60, reason?: string })
// → 返回 mutedUntilMs / mutedUntilLocal
```

`before_prompt_build` 入口检查：

```ts
if (s.mutedUntilMs && Date.now() < s.mutedUntilMs) return undefined;
if (s.mutedUntilMs && Date.now() >= s.mutedUntilMs) s.mutedUntilMs = undefined;
```

mute 期间所有 banner（revert / threshold / prediction / budget）都跳过。过期自动解除；重启自动解除（仅内存，不持久化，保护用户不错过真正风险）。

`enhance_ctx_status` 工具响应加 `mutedUntilMs` / `seenRunIdsCount` 字段方便排查。

### 红线自查

- ✅ 不修龙虾核心（仅修自己的累加逻辑防 retry）
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ Silence 不持久化 → 重启自动解除，避免静音错过真正风险（红线 #5"诊断不修复"邻位的安全默认）

### 完整路线图状态

v6.5.4 起 16 个完善点已落地 13 个：

| 类 | 完成 | 剩 |
|---|---|---|
| P0 | 3/3 | 0 |
| P1 | 4/4 | 0 |
| P2 | 4/5 | P2-11/12 dashboard 可视化（依赖 dashboard.ts 改造） |
| P3 | 2/4 | P3-15 ctx_growth_rate / P3-16 provider-usage 联动 |

剩余 3 项按需启动。ctx-watchdog 主能力已经『跑完一圈』可以稳定服役。

## 6.6.0 — 2026-05-11（上下文守护『cost-aware + 多模态精算 + channel 差异化』收尾）

### 触发

v6.5.7 后路线图剩 3 个 P1/P2 完善点，本期收尾：

1. **P1-4 cost-aware 切换**：long-ctx 模型贵（opus-1m vs sonnet 5x），不分场景一刀切；需要月度预算感知
2. **P1-6 多模态 token 估算**：固定 1500 token/image 不准——gemini 800 / gpt 1200 / claude 1500，差异 2x
3. **P2-8 channel-aware 阈值差异化**：群聊每条进上下文涨得快，应该比 terminal 更激进；现在所有渠道用 70/85/95% 不合理

### 改动

#### A. P1-4 cost-aware 切换

新增数据：

```ts
const KNOWN_MODEL_COST: Record<string, { in: number; out: number }> = {
  "claude-opus-4.7-1m": { in: 15, out: 75 },  // $/M token
  "claude-sonnet-4.5":  { in: 3,  out: 15 },
  "claude-haiku-4.5":   { in: 1,  out: 5 },
  "gpt-5.4":            { in: 5,  out: 15 },
  "gpt-5.4-mini":       { in: 0.15, out: 0.6 },
  "gemini-2.5-pro":     { in: 1.25, out: 5 },
  "gemini-2.5-flash":   { in: 0.1, out: 0.4 },
  "kimi-k2":            { in: 0.6, out: 2.5 },
  "deepseek-v3.2":      { in: 0.14, out: 0.28 },
  // ... 18 个常见 model
};
```

`SessionUsage.estimatedCostUSD` 字段：

- `llm_output` 时累加 `(input × in + output × out + cacheRead × 0.1 + cacheWrite × 1.25) / 1_000_000`
- sqlite schema v7→v8 ALTER 加 `estimated_cost_usd REAL DEFAULT 0`
- 持久化跨 session（hydrate 时恢复）
- `getMonthlyCostEstimate(agentId?)` 跨 session 月度求和

`monthlyBudgetUSD` 配置（默认 undefined = 不启用）：

- ≥80% 预算 → `evalThresholdBanner` 附加『💰 预算告警』段
- `before_model_resolve` force-escalate 时 `budgetTight = sessionCost > monthlyBudgetUSD × 0.8`
- `pickLongCtxModel({ preferCheap: budgetTight })` → 按 cost.in 升序选最便宜的 long-ctx（kimi-k2 $0.6 vs opus-1m $15）

#### B. P1-6 多模态精算

新增 `KNOWN_MODEL_IMAGE_TOKEN_COST`（按 model 单图 token）：

| Model | Token/Image | 来源 |
|---|---|---|
| Claude-* | 1500 | Anthropic vision 文档实测 |
| GPT-5.4 / Codex / Mini | 1200 | OpenAI high detail |
| Gemini-2.5-pro/flash | 800 | 单图通常 1-3 tile × 258 token |
| GLM-4.6 / Kimi-K2 | 1500 | 智谱/Moonshot 实测 |

`estimatePromptTokens(event, modelId)` 新增 modelId 参数（不传则用 `event.model` / `event.resolvedRef`）；`resolveImageTokens(modelId)` 内部按 model 查表。

`before_model_resolve` / `before_prompt_build` 都传 `s.lastModel` 进 `estimatePromptTokens` 拿精确估算。

#### C. P2-8 channel-aware 阈值差异化

新增内置 `CHANNEL_THRESHOLDS_DEFAULT`：

| Channel | hint/warn/critical | escalate / force |
|---|---|---|
| wecom-group | 60% / 75% / 90% | 65% / 90% |
| wecom-direct | 65% / 80% / 92% | 70% / 92% |
| wechat-service | 65% / 80% / 92% | 70% / 92% |
| dingtalk | 65% / 80% / 92% | 70% / 92% |
| terminal / default | 70% / 85% / 95% | 80% / 95%（全局沿用） |

`ContextWatchdogConfig.thresholdsByChannel`：用户可覆盖任一渠道任一字段（部分覆盖 fallback 全局）。

`resolveChannel(ctx)`：
- 读 `ctx.channelId / originatingChannel`
- `wecom` 进一步按 `agentId` 含 `"group"` 拆 `wecom-group` / `wecom-direct`
- 空/terminal → `default`

`evalThresholdBanner` / `evalPredictionBanner` / `before_model_resolve` 都改用 `resolveThresholds(channel)` 取阈值，每个 session 按其实际 channel 走差异化。

#### D. 工具暴露

`enhance_ctx_status` 新增返回字段：

- `channel`: 当前渠道（"wecom-group" / "terminal" / ...）
- `channelThresholds`: 该渠道的 5 个阈值
- `estimatedCostUSD`: 本会话累计估算成本
- `monthlyBudgetUSD` / `budgetUsedPercent`: 预算占比
- `avgTokensPerTurn`: P2-9 预测式提醒的速率指标

`enhance_ctx_profile` 新增：
- `totalCostUSD`: agent 历史累计
- `monthly30dSessions` / `monthly30dCostUSD` / `monthlyBudgetUsedPercent`: 30 天画像

### 数据库 migration v7→v8

`migrateV7ToV8` 检测 `ctx_usage` 表已存在但缺 `estimated_cost_usd` 列 → ALTER 加上。新装 v6.6.0 用户 CREATE TABLE 时已包含该列。

### 红线自查

- ✅ 不修龙虾核心 / 不复制 isContextOverflowError
- ✅ 不抢龙虾 model-fallback
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ KNOWN_MODEL_COST 是 fallback；openclaw.json 注册的 model 真实价格由 model-router 的 capability 表覆盖（互补）
- ✅ monthlyBudget 仅观察 + 软提示，不强制阻止切换（红线 #5"诊断不修复"）

### 路线图收尾

`v6.5.4` 起的 16 个完善点已落地 11 个核心 P0+P1+部分 P2，ctx-watchdog 从『纸上谈兵』→『真实切换』→『状态持久化』→『subagent + 预测』→『cost-aware + 多模态 + channel 差异化』五个阶段闭环。

剩余 P2/P3（按需启动）：
- P2-10 mute/silence 工具（用户烦提醒时静音 N 分钟）
- P2-11 dashboard 可视化（sessions overview）
- P2-12 跨 session 历史画像（已有数据底子，缺 dashboard 入口）
- P3-13 龙虾 model-fallback 协调（runId 去重，避免 retry 重算）
- P3-15 ctx_growth_rate 指标（latency-tracker schema 扩展）
- P3-16 龙虾 provider-usage 联动（真实 quota snapshot）

## 6.5.7 — 2026-05-11（上下文守护『subagent 累加 + 预测式提醒』+ sidus 清理）

### 触发

v6.5.6 路线图剩 5 个完善点，本期挑两个最痛的 + 顺手清掉另一会话遗留的 sidus 残留：

1. **P1-7 subagent token 累加盲区**：子 agent 调 LLM 的 token 走 child sessionKey，main agent 看 ctx 用量永远是"自己的部分"，但实际后端 ctx 已经被 child 吃掉一截。蓝火派活 / spawn_task 场景下 ctx-watchdog 严重失真。
2. **P2-9 反应式 → 预测式**：当前预警是"已经到 70%才提"，用户被提醒时只剩 30% 余量；应该按速率预测"未来 3 轮可能撞 85%"提前给空间。
3. **sidus hardcoded 清理**（另一会话遗留 WIP）：`model-router.ts` 默认 fallback `"sidus/DeepSeek-V4-Flash"` 不存在（provider 未注册）→ 撞 "Model not allowed"。

### 改动

#### A. P1-7 subagent token 累加（context-watchdog.ts）

新增 hooks `subagent_spawned` / `subagent_ended`：

```ts
const childToParent = new Map<string, string>();

api.on("subagent_spawned", (event, ctx) => {
  const childKey = event?.childSessionKey ?? ctx?.childSessionKey;
  const parentKey = ctx?.requesterSessionKey;
  if (childKey && parentKey) childToParent.set(childKey, parentKey);
});

api.on("subagent_ended", (event, ctx) => {
  const childKey = event?.targetSessionKey ?? ctx?.childSessionKey;
  const parentKey = childToParent.get(childKey) ?? ctx?.requesterSessionKey;
  const child = sessions.get(childKey);
  const parent = sessions.get(parentKey);
  if (parent && child && child.totalTokens > 0) {
    parent.totalTokens += child.totalTokens;
    markDirty(parentKey);
  }
  childToParent.delete(childKey);
});
```

LRU 限制 `MAX_SUBAGENT_LINKS=500` 防内存膨胀。child 的 sessions 行留在 sqlite 作画像（不立即 evict）。

#### B. P2-9 预测式提醒（context-watchdog.ts）

`SessionUsage` 新增 `tokensPerTurnHistory: number[]`（最近 5 轮 token 增量 FIFO）。`llm_output` push 当前 usageDelta。

新增 `evalPredictionBanner(s, event)`：

```ts
const avgPerTurn = sum(history) / history.length;
const turnsToWarn = ceil((warnAt × ctxMax - used) / avgPerTurn);
if (turnsToWarn <= 3 && percent < warnAt && !s.predictionEmittedFor === Math.round(warnAt × 100))
  → 注入"按速率 X 轮内撞 Y%"提示，防抖直到真到阈值
```

`before_prompt_build` 三层优先级：revert hint > threshold banner > prediction banner。

#### C. sidus hardcoded 清理（model-router.ts / model-route-config.ts）

- `routeTask` 默认 fallback：`"sidus/DeepSeek-V4-Flash"` → `"deepseek/deepseek-v4-flash"`（与 OpenClaw 默认对齐）
- `enhance_route_set` tool description 示例从 sidus 改 minimax

### Hook chain（v6.5.7 全景）

| Priority | Module | Hook | Action |
|---|---|---|---|
| 100 | ctx-watchdog | `before_model_resolve` | 事前估算 → ≥95% 强切 long-ctx |
| 默认 | ctx-watchdog | `llm_output` | 累加 usage + push history + markDirty |
| 默认 | ctx-watchdog | `llm_input` | 估算 pendingTokens |
| 默认 | ctx-watchdog | `subagent_spawned` | 记 child→parent 链路 |
| 默认 | ctx-watchdog | `subagent_ended` | child.totalTokens 累加回 parent |
| 默认 | ctx-watchdog | `before_prompt_build` | revert hint > threshold banner > prediction |
| 默认 | ctx-watchdog | `after_compaction` | totalTokens×0.3 + revertSuggest + markDirty |
| 默认 | model-router | `before_model_resolve` | 任务/渠道/quota 路由 |

### 红线自查

- ✅ 不修龙虾核心 / 不复制 isContextOverflowError
- ✅ 不抢龙虾 model-fallback
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged

### 后续路线（v6.6.0 candidates）

剩 3 个 P1/P2 完善点：
- **P1-4 cost-aware 切换**：cost-budget mode 加月度配额联动
- **P1-6 多模态 token 估算**：scan 时记每 model 的 imageTokenCost
- **P2-8 channel-aware 阈值差异化**：群聊 60/75/90 + terminal 70/85/95

## 6.5.6 — 2026-05-11（上下文守护『状态持久化 + 切回原模型』）

### 触发

v6.5.5 上线后路线图剩 11 个完善点，按优先级开干 P0-3 + P1-5：

1. **P0-3 状态内存易丢**：sessions Map 内存 only，OpenClaw 重启清零——长会话跨日续接 (≥75min idle) 桥接进来后 ctx 计数从 0 起算，预警失灵
2. **P1-5 没有"切回原模型"回归路径**：因 ctx 切到 long-ctx 后，/compact 成功 ctx 降下来，应该回原模型省钱（claude-opus-4.7-1m vs sonnet 价差 5x）

### 改动

#### A. P0-3 状态持久化（sqlite ctx_usage 表，schema v6→v7）

新建 `src/utils/ctx-usage-db.ts`（~140 行）：

```sql
CREATE TABLE ctx_usage (
  session_key TEXT PRIMARY KEY,
  agent_id TEXT NOT NULL DEFAULT 'main',
  total_tokens INTEGER NOT NULL DEFAULT 0,
  last_model TEXT,
  last_model_ctx_max INTEGER NOT NULL DEFAULT 128000,
  original_model TEXT,
  last_warned_threshold REAL NOT NULL DEFAULT 0,
  peak_percent REAL NOT NULL DEFAULT 0,
  last_updated_at INTEGER NOT NULL,
  created_at INTEGER NOT NULL
);
```

`ON CONFLICT(session_key) DO UPDATE` 时 `peak_percent = MAX(stored, new)` 单调递增（为 P2-12 agent 画像铺路）。

`context-watchdog.ts` 集成持久化：

- **Lazy hydrate**：首次 `getOrCreate(sessionKey)` 查 sqlite，hit 则恢复 totalTokens / lastModel / originalModel / lastWarnedThreshold / peakPercent
- **节流 flush**：`markDirty(sk)` 标记 + `scheduleFlush()` 10s 后批量 `batchSaveCtxUsage`（事务化）
- **LRU eviction**：内存满（500 session）evict 时**不删 sqlite 行**（保留作画像）
- **process.beforeExit / SIGTERM**：`finalFlush` 兜底同步落盘
- **30 天 TTL 清理**：启动期 `purgeOldCtxUsage(30)`

#### B. P1-5 切回原模型回归路径

`after_compaction` hook 升级：

```ts
if (s.originalModel && s.lastModel !== s.originalModel) {
  const projectedInOriginal = s.totalTokens / resolveCtxMax(s.originalModel);
  if (projectedInOriginal < 0.6) {
    revertSuggestPending.set(sessionKey, s.originalModel);
  }
}
```

`before_prompt_build` 一次性消费 revert hint，抽出 `evalThresholdBanner` 复用 → revert hint 与三阶 banner 可叠加。

#### C. 两个新工具

| 工具 | 触发场景 | 行为 |
|---|---|---|
| `enhance_route_revert_to_original({reason?})` | LLM 看到 revert hint 后调 | 清掉 `originalModel`，让 model-router 接管重选 |
| `enhance_ctx_profile({agentId?})` | 用户/LLM 想看历史画像 | 返 `sessions / avgPeakPercent / maxPeakPercent` |

### 红线自查

- ✅ 不修龙虾核心 / 不复制 isContextOverflowError
- ✅ 不抢龙虾 model-fallback（仅在错误前预防）
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ sqlite 不可用时 graceful degrade

### 后续路线（v6.6.0 candidates）

P1-4 cost-aware / P1-6 多模态 token / P1-7 subagent 累加 / P2-8 channel-aware 阈值 / P2-9 预测式提醒。

## 6.5.5 — 2026-05-11（上下文守护『真实切换』闭环：≥95% 强切 + ≥80% 工具 + 事前估算）

### 触发

v6.5.4 上线后梳理出三个 P0 薄弱点：
1. **预警仅"建议"，没真切**：banner 让 LLM 看到，但 LLM 大概率回复用户『建议你新开会话』把活推回去——没有主动切大 ctx 模型的工具
2. **prompt size 入场预估缺失**：只有 `llm_output` 事后累加，预警永远迟一拍——本轮 prompt 已发出去
3. **long-ctx 推荐没排除 banned**：v6.5.4 推荐 `claude-opus-4.7-1m` 但如果它刚被 latency-tracker ban 了 → LLM 切过去秒报错（P3-14 顺手修）

### 改动

`src/modules/context-watchdog.ts`（v6.5.4 280 行 → v6.5.5 ~480 行）：

#### A. P0-1 真实切换（before_model_resolve + 工具双闸）

新增 `before_model_resolve` hook，**priority=100**（OpenClaw mergeBeforeModelResolve 用 firstDefined：高 priority 先跑，第一个返 modelOverride 的赢）：

```ts
api.on("before_model_resolve", (event, ctx) => {
  // 事前估算本轮 prompt：totalTokens + estimatePromptTokens(event)
  const projected = s.totalTokens + estimatePromptTokens(event);
  const percent = projected / s.lastModelCtxMax;

  // 强切条件：percent ≥ forceEscalateAt (默认 0.95) 且当前 ctx<256K
  if (percent < forceEscalateAt) return undefined;
  if (s.lastModelCtxMax >= 256_000) return undefined;

  const target = pickLongCtxModel(longCtxCandidates, s.lastModel);
  if (!target) return undefined; // 全 banned 时降级到 banner

  if (!s.originalModel) s.originalModel = s.lastModel; // 记原始 model 备切回
  return { modelOverride: target };
}, { priority: 100 });
```

新增 LLM 工具 `enhance_route_to_long_ctx({reason?, target?})`：
- 让 LLM 在看到 ≥80% banner 后主动调（明确入口，不靠 LLM 自己想）
- target 可选；不填按 `longCtxCandidates` 顺序自动选第一个非 banned 且 ctx≥256K 的
- 调完只更新 sessions 状态，**实际切**等下一轮 LLM 调用 hook 接管（避免改本轮）

#### B. P0-2 事前 prompt 估算

新增 `estimatePromptTokens(event)` 函数：
- 文本：4 chars/token（保守=高估，宁可早预警）
- 图片：每张 1500 token
- 视频：每帧 1500 token
- 音频：每秒 100 token

新增 `pendingTokens` 字段到 `SessionUsage`：
- `llm_input` hook 来时设为 estimate（覆盖，因为一轮一次）
- `llm_output` hook 拿到真实 usage 时清零（被真值替代）
- `before_prompt_build` / `before_model_resolve` 用 `totalTokens + pendingTokens` 做阈值评估

效果：v6.5.4 是『**这轮发完才知道炸了**』，v6.5.5 是『**这轮还没发就拦下来切模型**』。

#### C. P3-14 顺手修：long-ctx 选型跳过 banned

新增 `pickLongCtxModel(candidates, currentModel)` 函数：
- 按 `longCtxCandidates` 顺序遍历（默认 8 个：opus-1m / gemini-pro / gemini-flash / kimi-k2 / ...）
- 跳过当前 model（避免切到自己）
- 跳过 `KNOWN_MODEL_CTX_MAX[c] < 256_000` 的（不算 long ctx）
- 跳过 `isModelBanned()` 命中的（含 sidus/minimax/anthropic/openai/google 五个常见 prefix 模糊匹配）

#### D. 配置扩展

```ts
ContextWatchdogConfig {
  // 原 v6.5.4 字段保留
  hintAt?: number;            // 0.70
  warnAt?: number;            // 0.85
  criticalAt?: number;        // 0.95
  escalateToLongCtxAt?: number; // 0.80（仅"建议"阈值）

  // v6.5.5 新增
  forceEscalateAt?: number;    // 0.95（强切阈值）
  longCtxCandidates?: string[]; // 默认 8 个；用户可覆盖
}
```

### Hook chain 协调（与 model-router 不冲突）

| 优先级 | 模块 | 角色 | 决策 |
|---|---|---|---|
| 100 | ctx-watchdog | 事前估算 | percent≥95% & ctx<256K → modelOverride |
| 0 (默认) | model-router | 任务/渠道/quota 路由 | 按 routeTask + selectProvider 返 modelOverride |

OpenClaw `mergeBeforeModelResolve` 用 `firstDefined(prev, next)`：ctx-watchdog 先跑，返 modelOverride 后 model-router 还会跑但 modelOverride 已被高优先级占住。日志可见 `[hooks] before_model_resolve decided by ctx-watchdog (priority=100); skipping remaining handlers`（实际是 mergeBeforeModelResolve 不 skip，但 firstDefined 让结果固定）。

### 用户使用流程对比

```
v6.5.4（纸上谈兵）
  85% banner 注入 → LLM 看到 → LLM 回复用户『建议新开会话』← 推皮球
  95% banner 注入 → LLM 看到 → LLM 调 /compact 或继续报错 ← 没主动切

v6.5.5（真实切换）
  85% banner 注入 → LLM 看到 → LLM 调 enhance_route_to_long_ctx ← 主动切
  95% 系统强切 → ctx-watchdog hook 在 before_model_resolve 直接返 modelOverride ← 绕开 LLM
```

### 红线自查

- ✅ 不修龙虾核心 / 不复制 isContextOverflowError 错误检测
- ✅ 不抢龙虾 model-fallback 决策（仅在错误**前**预防；错误后还是龙虾负责）
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ 跟 model-router 通过 hook priority 协调，不破坏其 cache / circuit-breaker / quota-aware 逻辑

### 后续路线（v6.5.6 / v6.6.0 candidates）

- P0-3：sqlite 持久化 sessions（跨重启不丢）
- P1-5：ctx 降下来后建议切回 `originalModel`（after_compaction 触发）
- P1-4：cost-aware 切换（cost-budget mode 跟 ctx 联动，月度配额）
- P1-7：subagent token 累加回 main agent
- P2-8：channel-aware 阈值差异化（群聊更激进，terminal 宽松）

## 6.5.4 — 2026-05-11（上下文守护：三阶预警 + ≥80% 建议切大 ctx 模型）

### 触发

用户：『上下文快超过了，要及时处理、或者切换模型』。

实测痛点：长会话 + 跨日续接 + 多轮工具调用，token 累计到 180K+ 还没主动 `/compact`，突然撞 200K 上限报错。龙虾原生 `isContextOverflowError` 在 overflow **错误发生后**才走 model-fallback；用户体感是"突然报错"或"突然丢上下文"，没有预警。

### 龙虾原生已有（红线 #2 不复制）

- `isContextOverflowError` / `isLikelyContextOverflowError` 错误检测
- `model-fallback.ts:1011` ctx overflow 触发后做 model fallback
- `/compact` 命令 + `before_compaction` / `after_compaction` hook

### 龙虾原生没有的（本模块补）

新建 `src/modules/context-watchdog.ts`（~280 行）：

| 阶段 | 阈值 | 动作 |
|---|---|---|
| HINT | ≥70% | 友好提示『建议告一段落或主动 /compact』|
| WARN | ≥85% | ⚠️ 强烈建议立即 /compact 或切大 ctx 模型 |
| CRITICAL | ≥95% | 🚨 命令式『立即停止新任务，先总结 + memory_store + /compact』|
| ESCALATE | ≥80% 且当前 model ctx<256K | 附带『切大 ctx 模型』候选清单（claude-opus-4.7-1m / gemini-2.5-pro / kimi-k2）|

**hook 路径**：

1. `llm_output` 拿真实 `usage = { input, output, cacheRead, cacheWrite, total }` 累加到 `Map<sessionKey, SessionUsage>`
2. `before_prompt_build` 评估当前 percent，命中阈值注入 prependContext banner（同 session 同阈值只警告一次防抖）
3. `after_compaction` 自动归零（保留 30% 估计；龙虾不 emit 真实 compact 后 size，保守估）
4. `enhance_ctx_status` tool 让 LLM 主动查（返 `tokensUsed/ctxMax/percent/severity/recommendation/shouldEscalate/longCtxCandidates`）

### 已知 model ctx 上限表

内置 18 个常见 model（Anthropic / OpenAI / Google / 智谱 / DeepSeek / Moonshot / Minimax）；启发式 fallback（`-1m` / `-256k` / `-200k` / `-128k` / `-32k` 后缀解析）；未知 model 默认 128K 保守值。

### 配置

```jsonc
{
  "contextWatchdog": {
    "enabled": true,           // tier=1 minimal 也启用
    "hintAt": 0.70,
    "warnAt": 0.85,
    "criticalAt": 0.95,
    "escalateToLongCtxAt": 0.80,
    "debug": false
  }
}
```

### 红线自查

- ✅ 不修龙虾核心 / 不复制 isContextOverflowError 错误检测（我们做"预防"，龙虾做"善后"）
- ✅ 不抢龙虾的 model-fallback 决策（仅"建议"，由 LLM 或 model-router 自行切）
- ✅ 零 child_process / 零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ tier=1 minimal 也启用——纯观察 + 1 prompt supplement + 3 hook + 1 tool，零侵入

### 与现有 model-router 的关系

不冲突。model-router 处理"任务复杂度 → tier 选择 → quota-aware ban"；ctx-watchdog 处理"用量观察 → 阈值预警 → 切模型建议"。两者都在 hook 链里，互不抢决策——ctx-watchdog 仅提示，最终切模型决策仍由 model-router 或 LLM 主动调用 `enhance_route_set` 完成。

## 6.5.3 — 2026-05-11（manifest contracts.tools — 适配 OpenClaw 2026.5.x loader 契约）

### 触发

5/11 凌晨 OpenClaw 2026.5.x gateway 启动 log 大量 warning：

```
[gateway] [plugins] plugin must declare contracts.tools before registering agent tools
  (plugin=enhance, source=...dist/index.js)
```

每次 register 一个工具就报一条,enhance 48 个工具刷出 48 条 warning。

### 根因

OpenClaw 2026.5.x `dist/loader-B-GXgDrk.js` 在 `registerTool` 加了契约校验：插件必须在 manifest 根级 `contracts.tools[]` 显式声明所有要 register 的 tool 名,否则 register 调用被拒。`dist/tool-contracts-DxWKDI1k.js` 的 `normalizePluginToolContractNames(record.contracts)` 读 `manifest.contracts.tools`。

### 改动

`openclaw.plugin.json` 加根级 `contracts.tools` 数组,从 src/modules/*.ts 实际 register 的 48 个工具自动扫出（按字母序排）：

- bot-share-link (4): enhance_share_file/list/revoke/set_baseurl
- bot-upload-link (3): enhance_upload_check/link/revoke
- chapter-marks (2): enhance_chapter_list / enhance_mark_chapter
- config-doctor (1): enhance_config_doctor
- hook-profiler (1): enhance_hook_doctor
- large-file-bridge (1): enhance_upload_large_file
- memory-integrator (1): enhance_memory_export
- mode-gate (3): enhance_set_mode/current_mode/exit_plan_mode
- model-router (7): enhance_model_route_set/status/disable/mode/ban_status/unban/history
- scheduled-tasks-bridge (3): enhance_loop_register/list/disable
- session-doctor / session-recap / skill-doctor / skill-recommender / skill-installer / spawn-task / statusline / transcript-search / trajectory-archiver (各 1)
- structured-memory (4): enhance_memory_store/search/review/purge
- task-planner / todo-tracker (3): enhance_plan_task / enhance_todo_write/list/update
- tool-safety (3): enhance_safety_rules/log + enhance_retry_status
- workflow-hooks (2): enhance_workflow / enhance_task

### 不影响

- 没改任何代码逻辑,只动 manifest
- 工具注册行为不变,SDK 调用方式不变
- 兼容旧 OpenClaw（2026.4.x 不读 contracts.tools 字段,无副作用）

## 6.5.2 — 2026-05-11（BOT 文件上传桥：用户 → AI 反向兜底，修企微 100MB 上限）

### 触发

5/10 用户实测：群里有人转发 200MB 视频，企微只发系统通知文本『视频/文件超过 100M，无法下载』给 bot——**没附件、没 hook 错误、什么都没**。LLM 看到这段文本但不知该怎么办，直接回了句"没有上下文啊——你要我发哪个 HTML 给我？"

`bot-share-link`（v5.7.22）解决的是**反方向**（AI 发文件 → 用户下载）。这次需要镜像版：用户传文件 → AI 收。

### 改动

新建 `src/modules/bot-upload-link.ts`（~580 行），完全镜像 `bot-share-link` 设计：

| | bot-share-link（已有，v5.7.22）| **bot-upload-link**（新，v6.5.2）|
|---|---|---|
| 方向 | AI → 用户（下载） | 用户 → AI（上传） |
| URL prefix | `/plugins/enhance-share/` | `/plugins/enhance-upload/` |
| HTTP route | GET 服务文件 | GET HTML 上传页 + GET api/list + POST api/upload |
| 落盘 | `~/.openclaw/share/files/<token>-<file>` | `~/.openclaw/upload/<token>/files/<file>` |
| LLM 工具 | `enhance_share_file` | `enhance_upload_link` / `enhance_upload_check` / `enhance_upload_revoke` |
| 单文件上限 | 500 MB | 2 GB |

**关键设计决策**：

- **零新 npm 依赖**：故意不用 multipart——浏览器 `fetch(url, { body: file })` 自带 octet-stream，服务端 `req.pipe(createWriteStream)` 流式写。完整规避 busboy / formidable 等包的 native binding 风险（红线 #4 child_process 邻位的 binary-binding 红线）。
- **共享 baseUrl 配置**：跟 bot-share-link 用同一份 `~/.openclaw/share/config.json`——用户配过一次 share 就同时给 upload URL 用，零额外配置。
- **拖拽上传页**（200 行原生 HTML/JS）：浅色主题 + 多文件 + XHR 进度条 + 深色模式适配。
- **prompt supplement**（~80 token）：把企微 100MB 系统提示文本字面写进去，LLM 看到立即识别该调 enhance_upload_link。

### 与 v6.5.x large-file-bridge 关系

两个模块**互补共存**，不是替代关系：

| | large-file-bridge（v6.5.0）| bot-upload-link（v6.5.2）|
|---|---|---|
| 性质 | hook 触发型 | token 化基建 |
| 触发 | regex 检测错误文本自动注入 prompt | LLM 调工具按需创建 token |
| 上传端点 | 单一 `/plugins/enhance/upload`（无隔离）| `/plugins/enhance-upload/<token>`（per-token 目录）|
| 用途 | "看到错误立即提示链接" | "给具体用户具体场景一个隔离上传位" |
| 启用 | tier=2 默认 enabled | tier=1 默认 enabled |

LLM 流程：先 large-file-bridge hook 注入提示（"用户传文件超 100M 了，调 enhance_upload_link 给链接"），LLM 看到提示后调 `enhance_upload_link` 拿 token URL 发回去。

### 红线自查

- ✅ 不修 openclaw 核心 / 不动 wecom 插件 / 不复制龙虾原生
- ✅ 无 `child_process`、零新 npm 依赖
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ Token 12-hex sanitizer + filename path traversal 防御 + 单文件 2GB 上限
- ✅ 24h TTL + lazy 清理过期 token 目录
- ✅ baseUrl 跟 bot-share-link 完全共享解析逻辑
- ✅ tier=1 minimal 也启用（渠道兜底类，没了它企微 100MB 场景就死结）

### 三个新工具

| 工具 | 参数 | 用途 |
|---|---|---|
| `enhance_upload_link` | `label?`, `expireHours?` | 创建 token + 返回上传 URL |
| `enhance_upload_check` | `token` | 列该 token 已收到文件 + 路径（用户说"传完了"后调） |
| `enhance_upload_revoke` | `token` | 立刻删除整个 token 目录 + manifest 条目（处理完不需要时） |

## 6.5.1 — 2026-05-11（蓝火智能体关键词触发器：完全绕开 LLM 决策）

### 触发

v6.4.x 用 hook 拦工具 + 注 prompt 让 LLM 改用 `cc-media-task`——治不住"@贾维斯 帮我 X"这种用户没说"蓝火"的 case。LLM 决策路径太宽，hook 拦不住所有岔路。

用户决断：**"不行，这样不行。你应该把 cc 封装一个智能体。让我用关键词触发这个智能体。让它去干活。"**

### 改动

新建 `src/modules/cc-bridge-keyword-dispatch.ts`（~220 行）：

- 触发正则 `/^[\s　]*@?(?:蓝火|Lanhuo)[\s　:：,，、]+([^\s].{2,1500})$/is`
- 仅匹配消息开头的"蓝火 X"/"@蓝火 X"，X 至少 3 字
- 命中即 hook 直接 HTTP POST `cc-media-bridge:18790/dispatch`，桥 `spawn cc-media-task` 秒返 `task_id`
- hook 注 `prependContext` 让 LLM 只 echo 结果
- **完全绕开 LLM 决策**：蓝火 = 独立可触发的派活服务，关键词命中即真派活

### 配套（remote 三连击）

- `feat: large-file-bridge`（>100MB 错误检测 + 上传链接引导，commit `ad488719`）
- `fix: dist/index.js path`（编译产物 `../package.json` 兜底，commit `023dcf13`）
- `fix: channel 检测从 ctx 获取`（不依赖缓存，commit `57ae93c3`）

## 6.4.2 — 2026-05-10（session-bridge 修群聊场景失忆：chat_id null fallback + 多字段）

### 触发

5/10 用户实测群聊 `agent:wecom-default-group-wrgzumeqaaqxngzbthjuexh20e57vhew:wecom:default:group:wrgzumeqaaqxngzbthjuexh20e57vhew` 跨夜 8 小时还是失忆——LLM 说"没有上下文啊——你要我发哪个 HTML 给我？"，但用户昨天明明做了 HTML。

数据驱动诊断：

| 检查项 | 结果 |
|---|---|
| enhance 装版 | ✓ v6.4.1（已是 6.x 版本） |
| prior reset 文件 | ✓ `42f0676b-...jsonl.reset.2026-05-09T23-46-18.634Z`（199KB） |
| 当前活跃 session | ✓ 10KB（远 < 200KB freshSessionMaxBytes） |
| idle 阈值 | ✓ 8 小时 ≥ 75min |
| session-bridge 模块加载 | ✓ "已加载 fresh<200KB & idle≥75min..." |
| **当前 jsonl 头部 `chat_id` 字段** | **❌ 不存在** |
| **prior reset jsonl 头部 `chat_id`** | **❌ 不存在** |

→ session-bridge.ts 行 108 严格匹配 `"chat_id"` 字段，OpenClaw 4.29+ wecom 群聊 jsonl 头里**根本没写这字段** → `readChatId() → null` → 行 316 `if (!currentChatId) return undefined` → 直接放弃桥接，**从未注入 prependContext**。

### 改动（纯 enhance 内修复，零 OpenClaw / wecom 侵入）

`src/modules/session-bridge.ts`：

1. **`readChatId` 多字段 fallback**：`chat_id` / `chatid` / `chatId` 三种命名都试；都没有 → 从 `cwd` 字段抽末段路径（`workspace-wecom-default-group-XXX` 等动态 agent workspace 标识跨版本/跨渠道都稳定）作 `cwd:<tail>` 形式 key

2. **`findPriorBridgeSource` 加 mtime 最新 fallback**：`currentChatId === null`（OpenClaw 4.29+ 群聊场景）→ 选最新的 `.jsonl.reset.*`。**这是安全的**因为：
   - sessionsDir 已经 per-agent 隔离（`agents/<agentId>/sessions/`）
   - wecom-default-group-XXX / wecom-direct-XXX / wechat-service-XXX 等动态派生 agent 天然属于同一会话伙伴
   - chat_id 严格匹配仅在 main agent 多渠道共用 sessions 时有意义（这场景没有 .jsonl.reset.* 跨渠道混淆）

3. **主流程**：行 316 `if (!currentChatId) return undefined` 删除——允许 null 进 findPriorBridgeSource，由后者的 fallback 接管

### 设计哲学

**严格匹配条件不该成为唯一失败点**——v5.7.26 加 chat_id 严格匹配是为了"鲁棒性"（怕 sessionKey 大小写归一不一致），但当 chat_id 字段本身在 jsonl 头里**不写出来**时，整个桥接流程跪掉。修法：**降级保底**——chat_id 命中优先（保 v5.7.26 wecom direct 行为），命中失败 fallback 到 per-agent + mtime 最新（足够稳）。

### 红线自查

- ✅ 不修 openclaw 核心 / 不动 wecom 插件 / 不复制龙虾原生
- ✅ 无 `child_process`、零额外 IO
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ chat_id 命中场景行为不变（保留 v5.7.26 优先匹配）
- ✅ 仅 fallback 路径变化，对已工作的 wecom direct 场景零影响

### 验证

用户重启后让 ZhaoBo 在群里发消息：

```bash
# 看 enhance log 里是否有"桥接"实际触发记录（debug 模式开了的话）
grep "session-bridge\|桥接\|prior=" ~/.openclaw/logs/gateway.log | tail -10
```

预期：群聊场景下桥接器现在能命中 mtime 最新的 .jsonl.reset.* → 注入 12KB prependContext + PRIOR_SESSION_CHECKPOINT banner → LLM 能续上昨天对话。

## 6.2.1 — 2026-05-06（memory supplement token 优化：12 行 → 3 行，省 350 token/call）

### 触发

用户反馈："不要拖慢 OpenClaw 速度，也不要增加太多 token 消耗负担"。

精确分析 v6.2.0 token 开销：

| 模块 | 字符数 | token 估算 | 触发频率 | 月度（按 100K 调用） |
|---|---|---|---|---|
| **A. memory supplement**（v6.2.0 加） | ~800 | ~500 token | **每次 LLM 调用** | ~5000 万 token |
| B. PRIOR_SESSION_CHECKPOINT banner | ~700 | ~450 token | reset 后偶发（1-3 次/天） | ~30K-90K token |

A 部分**每次 LLM 调用 +500 token** —— 按 deepseek-v4-pro $1.74/M 估，月度浪费 ~$52。

虽有 prompt cache 缓解（5min TTL，命中后 0.1x 成本），但：
- 不连续会话每次重建 cache
- multi-agent 场景互不复用
- supplement 任何变动让所有 cache 失效

### 改动

`src/modules/memory-integrator.ts:342-373`：12 行 → 3 行精简版

| 维度 | v6.2.0 | v6.2.1 |
|---|---|---|
| 行数 | 12 行 | **3 行** |
| 字符数 | ~800 | **~220** |
| token | ~500 | **~150** |
| 月度成本（100K calls）| ~$52 | **~$16** |
| 引导力度 | ★★★★★ | ★★★ |

**保留**：工具签名 + 5 类枚举 + 判据 + 召回方式

**去掉**：每类的具体场景例子（LLM 训练时本就懂）、importance 范围（让 LLM 自己判断）、anti-pattern 详述（trajectory 里有 LLM 不会重复 store）、章节互补关系（cross-reference 浪费 token）

### 设计哲学

prompt supplement 是**每次 LLM 调用都加的**——成本敏感。设计原则：

1. **保留 LLM 训练里没有的信息**（你的工具名、5 类 schema、判据）
2. **去掉 LLM 训练里已有的常识**（不要 store 临时变量、importance 数值范围这些）
3. **观察后调**：先精简发版，看实测 memories 写入率。如果 ★★★ 引导够用 → 保持；如果 LLM 仍不主动 store → 加回 1-2 行最关键引导（不是恢复全部 12 行）

### 红线自查

- ✅ 不修 openclaw 核心、不复制龙虾原生
- ✅ 无 `child_process`、零额外 IO
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ 完全向后兼容（仅 prompt 文本调整，行为不变）

## 6.2.0 — 2026-05-06（第二天失忆三层守卫第二期：memory store 强引导 + PRIOR_SESSION_CHECKPOINT banner）

### 触发

v6.1.9 修了第二天失忆的前两层（session-bridge 窗口 + surfacer 阈值），但诊断还指出**第三层**问题：

- **enhance SQLite `memories` 表低写入**：5 月以来只 8 条记录 vs 146 章节，**LLM 几乎没主动调过 store 工具**——chapters 是自动 hook 写入的（session_start/end/subagent_*）；memories 是 LLM 主动 store 的。原 prompt supplement 只一句"提供分类记忆"，LLM 知道工具但不知何时该调。
- **session-bridge 注入了但 LLM 不知道是历史**：v5.7.26 + v6.1.9 都塞了 prependContext，但 LLM 不知是"昨天的延续"还是"当下要回应的新内容"——被动用、不主动检索完整 jsonl。

### 改动

#### A. memory-integrator prompt supplement 强化（按 v5.7.27 给 enhance_share_file 同款套路）

`src/modules/memory-integrator.ts:343-373`：

之前 1 行说明 → 升级为 12 行明确引导：
- 工具签名 + corpus 集成解释
- **应主动 store 的 5 类**：`decision` / `project` / `user` / `feedback` / `reference`，每类配具体场景例子 + importance 范围
- **判据**：『下次 reset / 第二天 / 跨会话被问到时是否要重新解释一遍？』是 → store
- **anti-pattern**：纯过程性 tool result / 临时变量 / 含敏感凭据 / 可重新计算的内容 —— 不要 store
- 跟章节标记互补关系：章节是『何时发生』，store 是『是什么、为什么、怎么用』

预期：从 8 条/月 → 几十-上百条/月，构建真正的"长期记忆"。

#### B. session-bridge PRIOR_SESSION_CHECKPOINT banner

`src/modules/session-bridge.ts:buildBridgeText`：

| 维度 | v6.1.9 之前 | v6.2.0 |
|---|---|---|
| 标题 | `【会话桥接 — 上次会话末尾】` | `🔄 PRIOR_SESSION_CHECKPOINT —— 上一段会话的尾段` |
| 明确性 | 隐含"是历史" | **明示**"这是历史延续，不是用户当下的新请求" |
| 完整 jsonl 路径 | 缺（只显前 8 字符 sessionId） | ✓ 完整路径 + 提示需要更多上下文可主动 Read |
| 使用建议 | 缺 | 3 条：① 不主动 echo/复述 ② 需更多上下文 Read 完整文件 ③ 重要决策 store 到分类记忆 |
| 截断提示 | "用 enhance_transcript_search 检索" | + 加"或 Read 完整 jsonl"二选一 |

预期：LLM 看到 PRIOR_SESSION_CHECKPOINT 字面 banner 立即知道"这是历史"——不会困惑、不会主动 echo；需要更多时主动 Read 完整文件（>>> 12KB 的 prependContext）。

### 红线自查

- ✅ 不修 openclaw 核心、不复制龙虾原生
- ✅ 无 `child_process`、零额外 IO（都是 prompt 文本调整）
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ supplement 仅在 `availableTools.has("enhance_memory_store")` 时注入（capability detection），enhance 单装 / 多 agent 场景不破坏

### 设计哲学

第二天失忆的"三层守卫"模型：

1. **session-bridge**（v5.7.26 加 → v6.1.9 扩容到 12KB → v6.2.0 加 banner 明示历史身份）
2. **native-memory-surfacer**（v5.7.10 加 → v6.1.9 松绑到 12 文件）
3. **memory store 行为**（v6.2.0 强引导补完）

三层互补、各司其职：bridge 抢救最近会话尾、surfacer 把 .md 锚点 surface、store 攒长期记忆。**任一层失火都会"第二天失忆"**——v6.2.0 完成全套加固。

## 6.1.9 — 2026-05-06（修第二天失忆：session-bridge 窗口 3x 扩容 + native-memory-surfacer 松绑）

### 触发

用户报「openclaw 第二天失忆问题还是比较严重」。v5.7.26 加过 session-bridge 修过一次，但仍有问题。数据驱动诊断（grep gateway.log + sessions/ + sqlite + .md memory dir）发现：

| 模块 | 状态 | 问题 |
|---|---|---|
| **session-bridge** | ✓ 触发了（5/5 23:51 reset → 5/6 01:05 prependContext 跑了） | 窗口太窄：仅 `tail 8msg / 4000字`——跨夜的项目背景、几小时前的决策全丢 |
| **native-memory-surfacer** | ✓ 在跑 | 阈值过严：默认 `maxFiles=5 + threshold=0.15`，REFERENCE/USER 类权重 0.10/0.15 几乎过不了——37 个 .md 中 **72% 没注入** system prompt |

### 改动

#### A. `src/modules/session-bridge.ts` 默认值 3x 扩容

| 字段 | v6.1.8 | v6.1.9 | 收益 |
|---|---|---|---|
| `tailMessages` | 8 | **20** | 尾部 → 中段都拿到 |
| `maxChars` | 4000 | **12000** | 跨夜 prependContext 4KB → 12KB |
| `priorMaxAgeHours` | 48 | **72** | 跨周末 OK |

实测：v6.1.0 一个 zhaobo session jsonl tail 20msg ≈ 8-10KB 中文，给 12000 字上限留 20-50% buffer 不会截断到信息丢失。

#### B. `src/modules/native-memory-surfacer.ts` 松绑

| 字段 | v6.1.8 | v6.1.9 |
|---|---|---|
| `maxFiles` | 5 | **12** |
| `threshold` | 0.15 | **0.05** |
| `cwdRelevanceBoost`（新增） | — | **0.2**（cwd 匹配 +20% 权重） |
| `ageRecencyBoost`（新增） | hardcoded 0.1 | **0.1**（近 7 天 2x，近 30 天 0.5x） |

`scoreFile()` 函数签名加两个可选 param 默认值；`registerNativeMemorySurfacer` 从 config 读、未配走默认。`TYPE_WEIGHT` 不变（user=0.15 / reference=0.1 仍偏低，但 0.05 阈值能过）。

预期：用户 37 个 .md 中至少 10-12 个被 surface（之前只 5 个），覆盖 USER 偏好 / PROJECT 进度 / REFERENCE 文档全部类型，LLM 第二天找回参考资料的概率从 28% → 80%+。

### 红线自查

- ✅ 不修 openclaw 核心、不复制龙虾原生
- ✅ 无 `child_process`、零额外 IO（都是默认值调整 + 一个 hardcoded 系数变可配）
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ 完全向后兼容：用户已显式配置的 maxFiles/threshold 不受影响

### 设计哲学

**第二天失忆不是单一 bug，是三层守卫都启动了但火力都不够**：

1. session-bridge（v5.7.26 加） → 触发了但 4KB 窗口太小
2. native-memory-surfacer（v5.7.10 加） → 在跑但阈值太严
3. enhance SQLite memory（5 月仅 8 条 memories store） → LLM 行为问题，留 v6.2 加 prompt supplement 引导

v6.1.9 修前两层（最小改动 + 最大 ROI）。第三层（rate limit memories store + reset.jsonl 第一条 prompt 加 PRIOR_SESSION_CHECKPOINT）留 v6.2。

## 6.1.8 — 2026-05-05（bot-share prompt 翻转：按大小分流，渠道本地直发优先）

**触发**：赵博 5/5 群里实测 `@贾维斯 直接发文件给我，不要发下载链接` —— wecom v2.8.23 + v2.8.24 修了群聊主动推送通道 + UI 锁交互后，MEDIA: 渠道本地直发已稳定可靠（5/5 23:42 实测群里直接收到 docx 附件成功）。v6.1.3 当时怀疑 stream 截断把 share_file 设为"任意大小都强制"，现在按用户偏好翻转回 MEDIA: 直发优先。

### 改动

[`src/modules/bot-share-link.ts:856-862`](src/modules/bot-share-link.ts:856) — prompt supplement 6 行重写：

| 旧（v6.1.3）| 新（v6.1.8）|
|---|---|
| 任意大小都强制 `enhance_share_file` | 按大小分流，渠道本地直发优先 |
| 标题：「文件分享（强制规则，无大小阈值）」 | 标题：「文件分享（按大小分流，v6.1.8 — 优先渠道本地直发）」 |
| 小文件没有例外，禁 emit `MEDIA:` 字面量 | 小文件优先 wecom MEDIA: 等渠道本地直发 |
| — | 用户明确说「不要发链接」时强制直发 |
| — | 决策表（图/视频 ≤10MB / 语音 ≤2MB / 文件 ≤20MB → 直发；超阈值 → 链接）|

### 配套上游

`@huo15/wecom@2.8.25`（同日发布）的 `WECOM_BOT_WS_MEDIA_GUIDANCE` 同步翻转。两边 prompt 互补不冲突。

### 红线自查

- ✅ 不修 openclaw 核心
- ✅ 无 `child_process`
- ✅ `compat.pluginApi >=2026.4.24` 仍 ranged
- ✅ 不假设 wecom 装着 — capability detection 按 availableTools 决定（wecom 不装时降级行为不变）

### 设计哲学

GUIDANCE 优先级随**底层能力 + 用户偏好**动态调，不是一次写死：

- v6.1.3：怀疑 stream 截断 → 强制 share_file
- v2.8.23/24（wecom 侧）：群聊主动推送通道 work + UI 锁交互修了 → MEDIA: 重新可靠
- v6.1.8：按用户偏好（群里直接附件 > 链接）翻回直发优先

每次大改路径选择都要回头评估 prompt。



## 6.1.7 — 2026-05-05（model-router pickModel 加 capability 验证：修 image 路由被死 entry 覆盖事故）

### 触发

ZhaoBo 在 wecom 发了张图片，LLM 没识别。看 gateway.log：

```
[model-router] auto-task | image 输入 → 硬路由到 MiniMax M2.7（capability table 唯一支持 image） | auto-task → vl priority=1 | tier=vl | → minimax/MiniMax-VL-01
                                       ↑ routeTask 给的对：M2.7                                                    ↑ 最终发出去的：VL-01（不存在！）
```

`routeTask` 已经基于 v6.1.4 的动态 capability 扫描给出正确硬路由（`minimax/MiniMax-M2.7`），但 `pickModel` 内部 `selectProvider(runtimeConfig, "vl")` 又用**用户 `~/.openclaw/enhance/model-route.json` 的老 vl tier 配置**覆盖回 `minimax/MiniMax-VL-01`——后者**根本没在 openclaw.json `models.providers.minimax.models` 注册**，是 v5.x 时代留下的死 entry。

→ OpenClaw runtime 收到不存在的 model id → fallback 到默认 model（无 image 能力的 deepseek-v4-flash）→ LLM 看不到图片，回了句"我看不到图片"。

### 改动

`src/modules/model-router.ts:pickModel` 给 `selectProvider` 返回值加 capability 验证：

```typescript
const picked = selectProvider(runtimeConfig, tier);
if (picked && !CAPABILITY_BY_ID.has(picked.id)) {
  // 用户 model-route.json 残留的死 entry → 抛弃，回退到 routeTask 的硬路由
  api?.logger.warn(`selectProvider 返回 ${picked.id} 但不在 capability 表，回退到硬路由 ${taskDecision.model}`);
  decision = { ...taskDecision, reason: `... | ⚠ ${picked.id} 不存在，回退硬路由` };
}
```

`CAPABILITY_BY_ID` 是 v6.1.4 的启动期扫描产物（动态读 `~/.openclaw/openclaw.json` 实际注册的 model）—— 任何 model-route.json 写错的 model id 都会被自动跳过，**不再覆盖硬路由**。

### 为什么 v6.1.4 的动态扫描没解决这个？

v6.1.4 改了 `routeTask`（image 硬路由 + capability 表派生），但**没改** `pickModel` 里 `selectProvider` 返回的优先级——routeTask 给的硬路由仍然被 selectProvider 覆盖。这次一并补齐。

### 红线自查

- ✅ 不修 openclaw 核心、不复制龙虾原生
- ✅ 不擅自改用户 model-route.json（红线 §6.4 诊断不修复）—— 只 log warn 提示用户，不动文件
- ✅ 无 `child_process`、pluginApi `>=2026.4.24` 仍 ranged
- ✅ 性能零成本：CAPABILITY_BY_ID 是 v6.1.4 启动期 build 的内存 Map，O(1) 查表

### 用户使用

正常情况无需做任何事——image 路由现在自动走 capability 表唯一可用的 image model。

可选：清理 `~/.openclaw/enhance/model-route.json` 里 `vl` / `hailuo` tier 的死 entry（如 `MiniMax-VL-01`），改成实际可用的 `MiniMax-M2.7`，或直接置空让 routeTask 自动选——清理后 log 不再有 ⚠ 警告。

## 6.1.6 — 2026-05-05（model-router quota-aware 即时切换）

### 触发

用户实测某 model provider 返回：

```
HTTP/1.1 422 Unprocessable Entity
{"status":20125,"message":"成员月度消费额度已超限","result":null,"timestamp":1777942606632}
```

v6.1.4 的 circuit breaker 是 **errRate 累积式**（5 样本 / errRate > 50%）—— 这种"配额耗尽"是确定性硬错（后续每次都会 422），等 5 个样本累积纯属浪费。**应该单次命中就立刻切**。

### 改动

`src/utils/latency-tracker.ts` 新增 quota-aware ban list（~150 行）：

- `recordError(providerId, errorMessage, httpStatus)` — 检测 quota 类硬错命中后**立刻** ban
- `detectQuotaError`：HTTP **402 / 422 / 429** 状态码、或错误消息含中英文关键词（`额度`/`超限`/`余额不足`/`quota`/`exceeded`/`exhausted`/`insufficient_quota`/`rate limit`/`billing`/`out of credits` 等 17 条）
- `banModel` / `isModelBanned` / `unbanModel` / `listBannedModels` — 内存 Map<modelId, BanEntry>，TTL 默认 1 小时
- 过期自动清理（lazy）

`src/modules/model-router.ts` 接入：

- `model_call_ended` hook 在 `errored=true` 时尝试拿 `errorMessage`/`httpStatus`（多字段 fallback：`event.errorMessage` / `event.error.message` / `event.outcomeReason` / `event.body` / `event.httpStatus` / `event.statusCode` / `event.error.status`），调用 `recordError`。命中 ban → log warn + 清 routeCache
- `applyCircuitBreaker` 拆成两层检查：① quota-ban（v6.1.6 新增，优先级最高，单次硬错就切）② circuit-breaker（v6.1.4 errRate 累积式）。共用 `pickFallbackCandidate(failedId)` 候选选择
- `pickFallbackCandidate`：跳过当前 banned 的同模态/同 reasoning 候选，按 errRate + cost 升序排
- 2 个新工具：
  - `enhance_model_route_ban_status` — 查当前 ban 列表（含触发关键词、剩余分钟、手动解除命令）
  - `enhance_model_route_unban(providerId)` — 提前解除（用户额度立即补了的场景）

### 设计哲学

**两层 circuit 互补**：

- **quota-ban（即时）**：明确告诉你"不行了"的硬错（HTTP 4xx + 关键词）→ 单次命中就切
- **circuit-breaker（累积）**：网络抖动 / 偶发 5xx / 不确定故障 → 5+ 样本 + errRate > 50% 才切

加起来覆盖 LLM provider 两类典型故障：「确定性的没钱了」和「不确定的网络糟」。

### 红线自查

- ✅ 不修 openclaw 核心、不复制龙虾原生（quota 检测 / ban 全在 enhance 自家）
- ✅ 无 `child_process`
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ ban list 是内存 Map，hook 路径只读 + O(1)，零额外 IO
- ✅ event 字段读取多 fallback，OpenClaw 任何版本字段命名漂移不影响功能

### 用户使用

正常情况无需做任何事——LLM 报 quota 错时路由器自动切。可观测：

```
# AI / 用户调:
- enhance_model_route_ban_status              # 看当前哪些 model 在 ban 期
- enhance_model_route_unban("minimax/MiniMax-M2.7")   # 手动解除
```

启动 log 在 ban 触发时会大字 warn：
```
[model-router] ⛔ quota-ban: minimax/MiniMax-M2.7 触发 HTTP 422 → 1h 内不再路由到此 model（其他备选自动接管）
```

## 6.1.5 — 2026-05-05（蓝火 dashboard 引导：prompt supplement 强约束 LLM 附 dashboard URL）

**触发**：5/5 zhaobo 反馈在 `agent:main:wecom:direct:zhaobo` 会话里 LLM 列蓝火任务 / 看任务详情时常常忘附 dashboard 链接（`https://keepermac.huo15.com/dashboard`），用户得自己记 URL。但蓝火（cc-media-bridge）跑出来的 claude CLI session **不会**进 Claude App pinned/recents（IndexedDB 白名单），dashboard 是 IM 用户唯一的可视化入口——不附 = 用户无法在群里直接点开看进度/历史。

cc-media-bridge SKILL.md v2.7.7 已经写过这条规则，但属"按需加载"——LLM 看 SKILL 时记得，离开 SKILL 上下文容易漏。**v5.7.27 enhance_share_file 用同样套路解决过类似问题**：tool description 写得再清楚也只是 LLM "可以读"，没有 prompt level 强约束 → 走 `registerMemoryPromptSupplement` 把规则注入 system prompt 才稳。

> 用户原意还提过"把 cc-media-bridge 整个项目合到 enhance"——拒绝该方案，因为：
> (1) 红线 #3「插件不内嵌 skill 内容」；(2) bridge 是 LaunchAgent 长进程 + bash 脚本 + SQLite WAL，跟 enhance 插件运行时（同 gateway 进程、不能 child_process、不能起独立 HTTP server）架构生命周期不匹配；(3) 真因不是 skill 分离而是 prompt 力度。
> 改用 prompt supplement 是正确切口——零跨项目耦合、零 bridge 改动、零红线违反、~30 行解决。

### 改动

新增 1 个文件 / 改 2 个：

- **`src/modules/cc-bridge-prompt.ts`**（74 行新）：
  - `bridgeInstalled()` — capability detection by filesystem path：先看 `~/.openclaw-media-bridge/` 是否存在（bridge LaunchAgent / setup.sh 跑过会自动建），fallback 看 `~/.local/bin/cc-media-task` 是否在 PATH。两者皆无 → bridge 没装 → 跳过 supplement，避免 enhance 单装用户看到无意义指令。
  - `resolveDashboardBaseUrl()` — 跟 bot-share-link 一致的 baseUrl 解析：env BOT_BASE_URL > `~/.openclaw/share/config.json` baseUrl > `http://127.0.0.1:18790` localhost 兜底。**复用** enhance 已有的 baseUrl 配置，用户配过一次 bot-share 就同时给 dashboard URL 用。
  - `registerCcBridgePrompt()` — `api.registerMemoryPromptSupplement` 注入 6 条强引导文案：
    - 解释为什么必附（Claude App 看不到外部 session）
    - 强制规则：响应里出现 `cc-YYYYMMDD-HHMMSS-XXXX` 格式 ID 必附 dashboard 链接
    - 列表 → `<base>/dashboard`，详情 → `<base>/dashboard?task=<id>`
    - 当 baseUrl 是 localhost 时额外提示用户先调 `enhance_share_set_baseurl` 设公网域名（不然 IM 群里其他人点不开）
- **`src/types.ts`**：`EnhancePluginConfig` 加 `ccBridgePrompt?: { enabled?: boolean }`
- **`index.ts`**：import + 注册新模块（`tier=1` minimal 也启用，与 bot-share / hook-profiler 同级）

### 红线自查

- ✅ 不修 openclaw 核心（红线 #1）
- ✅ 不复制龙虾原生（红线 #2）—— prompt supplement 是 enhance 范围
- ✅ 不内嵌 skill 内容（红线 #3）—— supplement 是 prompt-level 注入，不是 skill markdown
- ✅ 无 `child_process`（红线 #4）—— 仅 fs.existsSync + fs.readFileSync 内置 module
- ✅ 不替用户改配置（红线 #5）—— 只读 `~/.openclaw/share/config.json` + env，不写
- ✅ pluginApi `>=2026.4.24` 仍 ranged
- ✅ capability detection by filesystem path —— enhance 单装 / bridge 没装时静默跳过，零硬耦合

### 验证

启动 OpenClaw 后日志应有：

```
[enhance-cc-bridge-prompt] prompt supplement 已注册（强引导 LLM 给蓝火任务附 dashboard 链接）
```

或（bridge 没装时）：

```
[enhance-cc-bridge-prompt] cc-media-bridge 未装（…），跳过 prompt supplement
```

OpenClaw LLM 下次列任务 / 看详情时会自动附 `<baseUrl>/dashboard?task=<id>`，不再漏。

## 6.1.4 — 2026-05-05（model-router 智能路由大重构：动态 capability 扫描 + 5 维路由）

> **核心**：让 model-router 不再硬编码 model id——启动期扫 `~/.openclaw/openclaw.json` 的 `models.providers.<id>.models[]` 自动构建 capability 表。用户加新 provider/model 不用改 enhance 代码。

### 触发

调研 `model-router` 时发现 v6.1.2 的 PROVIDER_REGISTRY 写的是 `sidus`（用户机器实际未注册的 provider id），实际 openclaw.json 里只有 `minimax` + `deepseek` 两个 native provider——**一半路由决策在打空炮**（runtime 找不到 provider，把 model id 整串发给随机 fallback，被远端 400）。jsonl 历史显示路由实际选的是 `deepseek-v4-pro` P50=14.4s P95=31.6s，**deepseek-v4-flash 才是用户最快+最便宜的 model**。

### 改动（src/modules/model-router.ts +400 / -100）

#### A. 启动期 capability 扫描（动态、不死）

新增 `scanAvailableModels(api)` 在 `register()` 启动期 read `~/.openclaw/openclaw.json` 的 `models.providers.<id>.models[]`，按 OpenClaw 4.x 标准 schema 转成 `ModelCapability[]`：

```ts
interface ModelCapability {
  id: string;        // "<providerId>/<modelId>" 跟 openclaw.json 完全对齐
  modalities: { text, image?, video?, audio? };
  reasoning: boolean;
  contextWindow: number;
  maxTokens: number;
  costInPerM: number;
  costOutPerM: number;
  speedScore: number; // 由 cost 反推（启发式）
}
```

派生 6 个内存索引：
- `CAPABILITY_BY_ID` 主键查
- `IMAGE_CAPABLE_MODELS` 按 cost 升序
- `VIDEO_CAPABLE_MODELS` / `AUDIO_CAPABLE_MODELS` 同上
- `REASONING_CAPABLE_MODELS` 按 cost 升序
- `LONG_CONTEXT_MODELS` ≥500K ctx 按 cost 升序
- `CHEAP_FAST_MODELS` 非 reasoning 按 cost 升序

`DERIVED_TIER_MAP` 自动从 capability 表派生（flash/fast → 最便宜非 reasoning，pro/reasoner → 最便宜 reasoning，vl → 第一个 image-capable）。

未来加 model：用户在 openclaw.json `models.providers` 加一项 → 重启 OpenClaw → 路由器自动看见。**enhance 不用升级**。

#### B. 5 维智能路由

1. **multimodal 硬路由**：image → 强制 IMAGE_CAPABLE_MODELS[0]（之前 v6.1.2 用 sidus pro 文本兜底是错的，文本 model 收到 image 引用会 400）
2. **ctx-aware**：估算 token = `prompt.length * 0.6`（中文）—— ≥50K token 强制 LONG_CONTEXT_MODELS（≥500K ctx）的最便宜
3. **channel-aware**：`ctx.channelId` 透传到 `applyChannelPreference`，wecom/dingtalk/wechat 渠道默认 flash 偏好；只调 tier preference，不写死 model
4. **circuit breaker**：每次决策后查 latency tracker `getProviderSpeedSample(model)`——errRate > 50% within 1h（≥5 样本）→ 切到同模态、同 reasoning 能力的备选（按 errRate + cost 排）
5. **cost-budget mode**：新 RouteMode `cost-budget`——按 priority 升序（用户把便宜 model 放高 priority 即生效）；为以后加 monthly budget cap 留扩展点

#### C. cache key 加 channelId

防止跨渠道污染（wecom 群偏 flash vs odoo 偏 pro 不会撞 cache 命中）。

#### D. 老 hardcode 全部清理

- `routeTask` 兜底字符串 `sidus/DeepSeek-V4-*` → `deepseek/deepseek-v4-*`（实际可用的）
- `provider: "sidus"` → `"deepseek"` 全量替换（17 处）
- 极短 prompt 短路从 minimax → deepseek-v4-flash（speedScore 9 vs 7、$0.14 vs $0.3、1M ctx vs 200K）

### 性能（红线自查）

- ✅ scanAvailableModels 在 register() 启动期跑一次（IO），hook 路径只查内存表（O(1)）
- ✅ circuit breaker 用 latency-tracker 内存数据，零额外 IO
- ✅ channel preference 纯字符串前缀匹配，纳秒级
- ✅ ctx-aware token 估算就是 `length * 0.6` 算术
- ✅ cache key 加 channelId 不增加 IO，只是 string concat
- ✅ 完全没引入新 hook，复用现有 `before_model_resolve` 和 `model_call_ended`

### 红线自查

- ✅ 不修 openclaw 核心、不复制龙虾原生（model 路由是 enhance 范围）
- ✅ 无 `child_process`（grep 命中均为注释）
- ✅ `compat.pluginApi >=2026.4.24` 仍 ranged
- ✅ register() 用 `require("node:fs")` dynamic（非 child_process）
- ✅ scanAvailableModels 失败 fallback 空表，hook 路径仍可工作（走 OpenClaw 原生 fallback）

### latency-tracker.ts 新增 export

`getProviderSpeedSample(providerId): SpeedSample | null` —— 给 circuit breaker 拿实时样本（之前只有 internal `computeSample`）。

### 设计哲学

> **路由器不是越聪明越好，而是"在 hook 路径不死"前提下尽量利用所有"已有的便宜信号"**。

不用 LLM 分类器（RouteLLM-style 50-200ms 慢死）；不用嵌入向量；不查 SQLite；不调外部 HTTP。只用：
- ctx 已有的 channelId / agentId（O(1)）
- prompt 已有的 length（O(1)）
- attachments 已有的 mimeType（O(1)）
- latency tracker 内存里的 errRate（O(1)）
- 启动期一次性扫描的 capability 表（O(1) 查表）

每条路径决策 < 1ms。

## 6.1.3 — 2026-05-04（bot-share prompt supplement 去 10MB 阈值 + 强化"小文件无例外"）

**触发**：群会话 `agent:main:wecom:group:wrgzumeqaadcsaffbvgfobppv-_6ccwg` 里赵博让 `@贾维斯 打包zip发给我`，LLM 把 7754 字节的 zip cp 到 `~/.openclaw/media/outbound/` 后只 emit 了文本 `MEDIA: ~/.openclaw/media/outbound/huo15-rustdesk-deploy.zip`，wecom outbound 不识别这个字面量约定，文件没发出去。用户问"怎么还没发"，LLM 又重复 emit 了一次"MEDIA:"，仍然没下文。

### 根因

bot-share-link.ts 的 prompt supplement 写「需要让用户从企微/钉钉/微信等 IM 渠道下载本地文件（**≥ 10MB 或不确定大小**）时，必须先调用 enhance_share_file」——LLM 解读为"小文件不用调"，于是脑补了一个`MEDIA:` 字面量当成 wecom 约定。但 wecom outbound 只识别 `![alt](url)` markdown 图片语法，不识别 `MEDIA:` / `FILE:` / `📎` 等任何文件路径字面量。

### 改动

[`src/modules/bot-share-link.ts`](src/modules/bot-share-link.ts):

1. **prompt supplement 标题去掉"大文件"**：`## 大文件分享` → `## 文件分享（强制规则，无大小阈值）`
2. **第一条规则**：`(≥ 10MB 或不确定大小)` → `（任意大小，包括几 KB 的小文件）`
3. **新增一条针对小文件的明确规则**：
   - "小文件没有例外：不要因为文件 < 10MB 就跳过这个工具去 emit `MEDIA: <path>` / `FILE: <path>` / `📎 <path>` 等任何字面量约定——wecom / 钉钉 outbound **不识别**这些约定，发出去的就是普通文本，用户什么都收不到。"
   - "如果上游渠道（如 v2.8.19+ 的 wecom）暴露了 `wecom_send_file` 之类的直发工具，可以优先用它（直接群里收到附件）；没有的话一律走 `enhance_share_file` 给链接。"
4. **`enhance_share_file` 工具 description 同步加 'small file no exception'**：开头加「**任意大小都用这个工具**（包括 < 10MB 的小文件）—— wecom/钉钉等 IM 渠道的 outbound 不识别 'MEDIA:'/'FILE:' 等文本约定，不调本工具就只能发普通文字，用户什么也收不到。」

### 配套上游变化

wecom v2.8.19（同日发布）暴露 `wecom_send_file` 工具支持"群里直接附件"——本版 prompt supplement 已经知道引导 LLM 优先用它（capability detection by name），不依赖 wecom 必须升级。wecom 不升时 LLM 自动降级到 `enhance_share_file` 链接路径，仍可工作。

### 红线自查

- ✅ 不修改 openclaw 核心 / 不复制龙虾原生功能
- ✅ 没引入 `child_process`（grep 命中均为注释）
- ✅ `compat.pluginApi` 仍是 `>=2026.4.24` ranged
- ✅ 不假设 wecom 必须装（capability detection 按 `availableTools.has` 决定）—— enhance 单装即用

## 6.1.2 — 2026-05-04（model-router PROVIDER_REGISTRY 修复）

详见 git log v6.1.2 commit `5cdad3b`。修复钉钉/企微等渠道用户被回 `model deepseek/deepseek-v4-pro is not supported` 错误字符串的 bug：旧的 deepseek/google-ai-studio/custom-sidus-ai 三个 provider id 都不存在，runtime 找不到 → 把 model id 整串塞给 sidus → 拒 400。重写为只用实际注册的 sidus + minimax。

## 6.1.1 — 2026-05-03（chore-only：刷 ClawHub tag）

**触发**：6.1.0 publish 时 ClawHub 端 record 半成功但 tag 没刷新——`clawhub inspect` 显示 `Latest: 6.0.0` 但 publish 6.1.0 报 `Version already exists`。按 §7.6 不重试同版本号 → bump patch 跳过。

零代码改动，零 src/ 变化。

## 6.1.0 — 2026-05-02（trajectory-archiver v2 路径策略：移出 sessions/ 子树）

**触发**：用户报"打开 https://keepermac.huo15.com/chat?session=...wecom:direct:zhaobo 超级慢"。早上发了 v5.8.0 hook-profiler 拿数据，晚上接着诊断。

### 故障复盘

1. **trajectory 体量翻倍**：早上 266MB / 141 文件 → 晚上 543MB / 160 文件（12 小时增 277MB），自动归档没起作用
2. **gateway event-loop 卡 30s**：`liveness warning eventLoopDelayMaxMs=30752.6`，频率每隔几分钟来一次
3. **第一次清 trajectory 释放 364MB（543→31MB）后用户反映还是慢** —— 证伪 trajectory 体量假设
4. **`sample 27442 30` 采样 30 秒**：21478/21645 hits（**99.2%**）卡在 V8 `JsonParser::ParseJsonObject` 递归调用 + `Builtins_ArrayMap` —— 典型 `array.map(JSON.parse)` 模式 = `sessions.list` 在 JSON.parse 全部 .jsonl 文件。
5. **真因**：openclaw 的 `sessions.list` **递归扫整个 sessions/ 子树**，包括旧版 archiver mv 进去的 `sessions/.archive/` 子目录。所以 v1 把文件 mv 到子目录里 = 把垃圾从一个抽屉挪到另一个抽屉，主线程仍然 JSON.parse 全套。

### 根治方案：路径策略修正

把归档目录从 `sessions/.archive`（**子目录**，被扫）提升到 `sessions-archive`（**跟 sessions/ 平级**，不在子树）→ openclaw 看不见 → 主线程不扫。

实测验证（用户本机 5/2 20:27）：

| 指标 | v1 路径策略 | v2 路径策略 |
|---|---|---|
| sessions/ 子树体量 | 68 MB / 155 files | **29 MB / 32 files** |
| keepermac TTFB 5 连测 | 49/34/31/**776**/**3449** ms | **30/32/33/32/32** ms 全部稳定 |
| liveness 11s 警告频率 | 每 3-4 分钟一次 | 60s 内 0 次 |

### 改动

**`src/modules/trajectory-archiver.ts`**（重写 ~200 行）：

- `archiveDir` 路径：`sessions/.archive` → `sessions-archive`（move-out-of-subtree）
- 部署模式：从 plist inline `find ... mv ...` 单行命令 → 抽脚本到 `~/.openclaw/scripts/trajectory-archiver.sh`，plist 调脚本路径
- 脚本内容（`buildArchiveScript`）三步：
  1. per-agent 循环 `for AGENT_DIR in agents/*/`：mv >ageDays + >minSizeMB 的 trajectory + checkpoint 到 `$AGENT_DIR/sessions-archive/`
  2. delete sessions-archive 里 >7 天的（彻底释放磁盘）
  3. delete `*.jsonl.reset.*` / `*.jsonl.bak-*` >3 天
- 启动期检测：旧版 v1 plist（含 `sessions/.archive` 字面量）→ `api.logger.warn` 强烈建议跑 setup 拿 v2 部署命令重装
- 新配置：`archiveCheckpoints?: boolean`（默认 true）— 同时归档 `*.checkpoint.*.jsonl`
- `enhance_trajectory_archiver_setup` 工具升级：v1 检测时输出"重新部署"消息；v2 命令含自动 unload 旧 plist 防 label 冲突

**`src/modules/session-doctor.ts`**：

- `archiveDir` 同步改成 `sessions-archive`
- `trajectory-total-huge` warning message 加入 v6.1.0 升级路径说明 + 推 enhance_trajectory_archiver_setup 部署
- fixCommand 模板更新

### 红线自查

- ✅ 不修 openclaw 核心（红线 #1）—— 完全只读 sessions/ 目录树，靠"避开扫描范围"而非"修改扫描逻辑"解决问题
- ✅ 不复制龙虾原生（archiver 是 enhance 范围，openclaw 没归档机制）
- ✅ 无 `child_process`（红线 #4）—— LaunchAgent 由 launchd 跑 bash 脚本，不在 plugin 进程
- ✅ 不替用户改 openclaw.json（红线 #5）—— 只输出 cli-cmd 让用户复制粘贴
- ✅ `compat.pluginApi >=2026.4.24` 仍为 ranged
- ✅ 启动期纯 fs.existsSync + readFileSync（只读检测），不写不改用户配置
- ✅ 不归档活跃 session（mtime > ageDays 才动；`.jsonl` 对话原文一律保留）

### 用户升级路径

```bash
# 装新版（自动替换旧 plugin record，配置不需迁移）
openclaw plugins install @huo15/huo15-openclaw-enhance@latest --force
openclaw restart

# 重启后 enhance 启动 log 会 warn：检测到 v1 LaunchAgent
# 调用工具拿 v2 部署命令：
#   AI: 帮我跑一下 enhance_trajectory_archiver_setup
# 复制返回的 bash 块粘贴到 shell 跑一次即可（自动 unload 旧的、写新脚本和 plist、立即跑一次验证）
```

## 6.0.0 — 2026-05-02（**重大改名：npm 包名变更 + ClawHub 重新注册**）

> **BREAKING（npm 包名）**：`@huo15/openclaw-enhance` → `@huo15/huo15-openclaw-enhance`

### 触发

老 npm 包 `@huo15/openclaw-enhance` 在 ClawHub 上的 plugin entry 被一段历史 ghost manifest 钉死：

| enhance 历史版本 | pluginApi |
|---|---|
| 1.3.0 - 5.1.0（27 个版本） | **`2026.2.24` (bare!)** ← ClawHub 端 plugin entry record 极可能在此期间首次注册时缓存了这个值 |
| 5.1.3+ | 已全部改 ranged `>=2026.4.x` |

`clawhub publish --tags latest,plugin` 只刷 tag 指针不刷 plugin entry record 字段，OpenClaw 走 `clawhub:` 协议解析时仍报 `requires plugin API 2026.2.24`。

实测对照：`@huo15/wecom@2.8.18` / `@huo15/wechat-service@2.2.2` 两个**新注册**的 plugin entry slug 完全干净（OpenClaw 协议装包成功），证实坑只是 enhance 老 slug 的历史死结，不是 ClawHub 普遍 bug。

### 改动

- **`package.json.name`**：`@huo15/openclaw-enhance` → `@huo15/huo15-openclaw-enhance`（与 `huo15-huihuoyun-odoo` 等其他 huo15-* 包命名规范对齐）
- **`SKILL.md` frontmatter `name`**：`huo15-openclaw-enhance` → `huo15-huo15-openclaw-enhance`（ClawHub slug 同步）
- **版本号**：5.8.7 → **6.0.0**（major bump 标识 npm 包名 breaking）
- **`scripts/release.sh`**：重新启用 `clawhub publish --tags latest,plugin`（新 slug 是干净起点，不会再撞 ghost manifest）
- **`README.md`**：安装命令更新到新名 + 老用户迁移指引
- **OpenClaw plugin id 保持 `enhance` 不变**：升级时新包替换旧 plugin record；用户 `~/.openclaw/openclaw.json` 里 `plugins.entries.enhance.config.botShare.baseUrl` 等配置无需迁移

### 用户迁移路径

```bash
# 1. 卸载老包（OpenClaw 内部 plugin id 保持 enhance，新装会被替换；保险起见先 uninstall）
openclaw plugins uninstall enhance

# 2. 装新包
openclaw plugins install @huo15/huo15-openclaw-enhance --force

# 3. 重启
openclaw restart
```

老 npm 包 `@huo15/openclaw-enhance` 已 deprecate，老 ClawHub slug `huo15-openclaw-enhance` 已 hide（已装用户仍可 update 兜底，新搜索看不到）。

### 红线自查

- ✅ 不修 openclaw 核心（红线 #1）
- ✅ 不复制龙虾原生（红线 #2）
- ✅ 无 `child_process`（红线 #4）
- ✅ pluginApi `>=2026.4.24` 仍 ranged（红线 #6.1）
- ✅ 仓库 git remote 不变（cnb.cool 主 + GitHub 镜像）
- ✅ OpenClaw plugin id 不变（用户配置兼容）

## 5.8.2 — 2026-05-02（chore-only：刷 ClawHub plugin tag + release.sh 修复）

**触发**：用户跑 `openclaw plugins update` 报错：

```
Resolving clawhub:@huo15/openclaw-enhance
Plugin "@huo15/openclaw-enhance" requires plugin API 2026.2.24, but this OpenClaw runtime exposes 2026.4.29.
```

但 npm 上 5.7.9 / 5.7.27 / 5.8.1 三个历史版本的 `package.json.openclaw.compat.pluginApi` 全都是 `>=2026.4.24`（ranged ✓）—— bare `2026.2.24` 跟 npm 实际包内容**完全脱节**。

### 根因

`clawhub inspect huo15-openclaw-enhance` 显示：

```
Latest: 5.8.1
Tags: latest=5.8.1, plugin=5.7.9
```

ClawHub `plugin` tag（被 `clawhub:@huo15/openclaw-enhance` 协议解析时使用）还卡在 5.7.9——那个 5.7.9 是 ClawHub 端**第一次以 plugin entry 注册**时的 manifest 快照，里面的 `pluginApi: "2026.2.24"` 是 **ClawHub 端缓存的元数据**，跟后续 npm publish 完全脱节。

`scripts/release.sh` 调用 `clawhub publish "$(pwd)" --version $VERSION` —— **没传 `--tags`**，CLI 默认只刷 `latest`，所以从 5.7.9 之后每次发版 ClawHub `plugin` tag 都没动。10 多个版本下来用户才碰到。

### 改动

- `scripts/release.sh`: clawhub publish 加 `--tags latest,plugin`，让 plugin tag 跟 latest 一起刷。dry-run 输出和 fallback 提示同步更新。
- 三处版本 bump 5.8.1 → 5.8.2 触发 chore-only re-publish 把 ClawHub plugin tag 从 5.7.9 一次拉齐到 5.8.2。
- 零代码逻辑改动（src/ 不动）。

## 5.8.1 — 2026-05-02（postinstall hint：装完直接引导配 BOT_BASE_URL）

**触发**：v5.7.27 加了运行时 `logger.warn` 在 enhance 启动时如果 baseUrl 是 fallback/LAN 就警告——但用户得翻 `~/.openclaw/logs/gateway.err.log` 才能看到，新机器装完根本没意识到要配。zhaobo 实测 5/2 在企微聊天里看到 LLM 自己拼了 `192.168.1.177:18789` 链接发给群成员就是这个问题——LLM 都没机会引导用户去设。

→ 直接在 `npm install` 终端输出里印一段 friendly 提示，最早能介入的时刻。**不是**改用户配置、不是替用户做决定，只是**告知 + 给三种配置路径**。

### 改动

- **`scripts/postinstall.cjs`** 新文件（126 行）：装完后写 stderr 一段中文提示。
  - **三层智能跳过**：① `~/.openclaw/share/config.json` 已有 baseUrl（升级安装不重复唠叨）；② env `BOT_BASE_URL` 已设；③ `process.env.CI` 或 `npm_config_loglevel=silent`（CI 噪音）
  - **零依赖**：只 `require('fs') + require('path')`（node 内置，不算 §6.2 禁的 child_process）
  - **零 fs 写**：纯 `process.stderr.write`，绝不动用户文件
  - **TTY 自适应**：terminal 着色，pipe / log 文件无色
  - **`.cjs` 后缀**：因为 `package.json` `type=module`，`.js` 会被当 ESM 解析、`require()` 不存在；`.cjs` 强制 CommonJS
- **`package.json`**:
  - `scripts.postinstall = "node scripts/postinstall.cjs"`
  - `version 5.8.0 → 5.8.1`
  - description 改成 v5.8.1 摘要
- 提示文案给三种配置方式（按用户偏好排序）：
  1. shell rc（`export BOT_BASE_URL=...`）— 最简单
  2. openclaw.json（`enhance.config.botShare.baseUrl`）— 显式 per-account
  3. **让 LLM 自动持久化**（说一句话即可，LLM 调 `enhance_share_set_baseurl` 写到 ~/.openclaw/share/config.json）— 最自然

### 为什么不能做"真正的安装时 wizard"

OpenClaw plugin SDK 的 `WizardPrompter` / `setupSurface` 只暴露给 **channel 插件**（discord/feishu/wecom 等），non-channel augmentation 插件（如 enhance）没有交互式 setup hook 入口。npm postinstall 是当前能做到的最早提醒时机。

### 验证

```bash
# 已配置（你机器实际情况）→ 0 字节 stderr
node scripts/postinstall.cjs

# 新机器无配置 → 1100+ 字节提示
HOME=/tmp/fake-home node scripts/postinstall.cjs

# CI 跳过
CI=1 node scripts/postinstall.cjs

# env 已设跳过
BOT_BASE_URL=https://x node scripts/postinstall.cjs
```

四路全对：skip × 3 / print × 1。

## 5.8.0 — 2026-05-02（hook-profiler：量化 OpenClaw 端到端首字延迟）

**触发**：用户实测 OpenClaw 首字延迟 p50=9.9s / p95=38.8s（取自 `gateway.err.log` 72 个 `[trace:embedded-run] prep stages` 样本），但**不知道慢在哪**。openclaw 自己其实在日志里写得很清楚——每次 turn 的 `core-plugin-tools / system-prompt / bundle-tools / stream-setup` 各阶段耗时都打在 stream-ready 行——只是从来没人聚合 + 趋势 + 排行。同时 `[hooks] X handler from <plugin> failed: timed out` 等异常事件也只是单行 log，没追踪。

→ 把它做成 enhance 自家的 APM。**不是**重写 openclaw、不是复制龙虾原生（openclaw 没 hook profiling 能力）、不是替用户改配置——只是**读 + 解析 + 出诊断**。

### 改动

新增 4 个文件 / 改 3 个：

- **`src/utils/hook-profile-db.ts`**（285 行新）— schema migration v5 → v6：建两张表 `prep_stage_metrics`（端到端 stage 耗时）+ `hook_profile`（单 hook 调用记录，source ∈ {`wrap`, `log-timeout`, `log-error`}）。配 `getPrepStageStats / getHookProfileStats / listKnownHookEvents` 查询 helpers + `purgeOldHookProfiles` retention（默认 30 天）。
- **`src/utils/profile-hook.ts`**（77 行新）— `profileHook(api, event, moduleName, handler, options?)` 包装器。行为零变化（`await` 透传 + 异常 rethrow），副作用只是写一条 `wrap` source 记录。本版**未替换**现有 14 处 `api.on`，留作未来分阶段迁移；先靠 log-tailer 抓数据。
- **`src/modules/hook-profiler.ts`**（441 行新）— 模块主入口：
  1. **log-tailer**：fs.watch + readSync 增量读 `~/.openclaw/logs/gateway.err.log`，三条 regex 解析 `[trace:embedded-run] prep stages` / `[hooks] handler from <plugin> failed: timed out after Nms` / `[hooks] handler from <plugin> threw: ...`。启动跳到 EOF 防历史回灌。单次 ≤1MB chunk 防大日志爆 memory。
  2. **`enhance_hook_doctor` 工具**：输出近 N 天 prep-stages 趋势 P50/P95/max（total / core_plugin / system_prompt / bundle_tools / session_loader / bootstrap_ctx / stream_setup）+ 各 hook event 的 plugin × module 排行（按 P95 降序）+ 行动建议（system_prompt P95>3s 提示看 hook 排行 / core_plugin>4s 提示跑 config_doctor / 其它 plugin timeout 提示反馈维护方）。
- **`src/utils/sqlite-store.ts`**：+2 行（import + `migrateV5ToV6` 调用，链在 v4→v5 之后）
- **`src/types.ts`**：+21 行（`HookProfilerConfig` interface + `EnhancePluginConfig.hookProfiler` 字段）
- **`index.ts`**：+10 行（import + module 注册，tier=1 minimal 也启用，依赖 `dbAvailable`）
- **`openclaw.plugin.json`**：uiHints 加 `hookProfiler.enabled` 开关 + configSchema 加 `hookProfiler` 段（含 `retentionDays / tailer.enabled`）

### 设计权衡

- **三路数据汇合**：A. log-tailer（间接但抓得到其它 plugin 的 timeout/error）；B. profileHook 包装器（精确但只覆盖 enhance 自家）；C. 未来 openclaw 若暴露其它 plugin 成功 handler 事件可补 D 路。**不抓其它 plugin 成功耗时**因为 openclaw 不暴露这个事件——只能通过 prep-stages 总 system_prompt 耗时反推"集合"贡献。
- **log-tailer 改成 register 期常驻**（之前 review 时讨论过 SessionStart/End 起停）：fs.watch + persistent:false 不阻塞退出，开销极低（仅日志变更触发回调），按 session 起停徒增 ~30 行没必要。
- **写表全 try/catch 静默**：profiler 是观察者，不能影响主流程。

### 红线自查

- ✅ 不修 openclaw 核心（红线 #1）
- ✅ 不复制龙虾原生（openclaw 没 hook profiling 能力，红线 #2）
- ✅ 无 `child_process`（fs.watch + readSync，红线 #4）
- ✅ 不替用户改 openclaw.json（only return-cliCmd advice，红线 #5 + 6.4 诊断不修复）
- ✅ `compat.pluginApi >=2026.4.24` 仍 ranged（红线 6.1）
- ✅ tool 用 `parameters / execute` 新字段
- ✅ 无新依赖

### 验收（用户安装后跑）

1. `enhance_hook_doctor` 应返回 prep-stages 趋势报表（运行几次 turn 后才有数据）
2. 对比 `~/.openclaw/logs/gateway.err.log` 里同时段的 `[hooks] ... timed out` 行，`hook_profile` 表里 `source='log-timeout'` 条数应一致
3. `enhance-memory.sqlite` 两张新表自动建出（migrateV5ToV6 自动跑）

## 5.7.27 — 2026-05-02（bot-share 持久化 + 强引导 LLM 调 enhance_share_file）

**触发**：v5.7.26 修复 wecom 失忆事故的同时复盘到一个姊妹问题——

- AI 知道企微 IM 渠道有 20MB 文件大小限制后，**直接在文本里凭空编一个下载 URL** 给用户（`http://192.168.x.x:9999/<file>` 这种用户网络相关但完全错误的链接），既没调 `enhance_share_file` 工具，也没让 wecom fallback 接管。
- 根因 1：`enhance_share_file` 的 tool description 写得再清楚，也只是 LLM "可以读"——没有 prompt level 的强约束。
- 根因 2：用户首装 enhance 没人提示要配 `BOT_BASE_URL`，链接落到 `localhost` / LAN IP 兜底，外网用户访问不了；AI 看到这种"显然不对"的 URL 自己又编一个看起来更合理的——错上加错。

→ 三件套联动一次性修：让用户能保存一次、让插件主动提示首装问题、让 LLM 在 prompt 层被强约束。

### 改动

`src/modules/bot-share-link.ts`（v5.7.27 新增 248 行）：

1. **持久化 baseUrl**：`~/.openclaw/share/config.json` 本地保存 `{baseUrl, setAt, setBy}`。新工具 `enhance_share_set_baseurl(url=...)` 让 AI 一次性写入（带 URL 校验：必 http/https、不能带路径/query/hash）。
2. **baseUrl 优先级链**（5 层 → 6 层）：env `BOT_BASE_URL` > `openclaw.json` 里的 `enhance.config.botShare.baseUrl` > 本地保存（新加）> host header 自动检测 > localhost 兜底。
3. **首装检测 startup warning**：模块 `register` 期主动跑一次 `describeBaseUrlSource`，命中 `fallback` / `LAN IP detected` 时直接 `api.logger.warn` 在 OpenClaw 启动 log 提示用户。
4. **`enhance_share_file` 输出升级**：`structuredContent` 加 `baseUrlSource / baseUrlIsFallback / baseUrlIsLanDetected` 三字段，让 LLM 能感知"我这次返回的 URL 是不是真的可外网访问"。
5. **memory prompt supplement 强引导**（核心修复）：通过 `api.registerMemoryPromptSupplement` 注入"## 大文件分享（强制规则）"四条到 system prompt：
   - IM 渠道发文件必须先调 `enhance_share_file`，把 `structuredContent.url` 原样发给用户
   - **严禁**手写、拼接、猜测、回忆下载 URL
   - 文件不在本地时先落盘到绝对路径再调
   - 看到 `baseUrlIsFallback` / `baseUrlIsLanDetected` 时**先**问用户公网域名，**再**调 `enhance_share_set_baseurl` 保存

### 红线自查

- ✅ 不修 openclaw 核心（红线 #1）
- ✅ 不复制龙虾原生（openclaw 没本地配置持久化能力，亦无 IM 渠道文件分享桥）
- ✅ 无 `child_process`（红线 #4）
- ✅ 写文件只写 plugin 自己的 `~/.openclaw/share/`，不动用户 `~/.openclaw/openclaw.json`（红线 #5 + 6.4 诊断不修复）
- ✅ `registerMemoryPromptSupplement` 单参（红线 6.3）
- ✅ `compat.pluginApi >=2026.4.24` 仍为 ranged
- ✅ tool 用 `parameters / execute` 新字段（不是旧 `schema / handler`）

## 5.7.26 — 2026-05-02（session-bridge：跨 reset 自动桥接上次会话尾段）

**触发**：今天用户在 `wecom:direct:zhaobo` DM 里反映"openclaw 忘了昨天上下午聊的内容"。复盘发现：

- 5/1 23:13:26 openclaw runtime 把活跃 session 硬 reset（`*.jsonl` → `*.jsonl.reset.<ts>`），新 session 立刻在 23:13:38 起点 — 全空白上下文。
- enhance 已有的 `before_reset` hook 当时**未触发**（动作不是事件级 reset 而是文件级硬 wipe），lifecycle 抢救 = 0；同期 memories 表里也没 `[lifecycle:reset] ... 2026-05-01` 条目佐证。
- enhance 既有的 `session-recap` 只用结构化元数据（chapters / todos / decisions）填回顾，对"昨天具体聊了啥"完全无能为力。
- `transcript-search` 是手动工具，不会自动注入。

→ 结论是出现了"reset 不发 hook 时的盲区"。

### 改动

新增 `src/modules/session-bridge.ts`（tier=1，minimal 也启用）：

- 挂 `before_prompt_build` hook，**每个 fresh session（jsonl < 200KB）启动时主动扫一次**
- 扫 `~/.openclaw/agents/<agentId>/sessions/*.jsonl.reset.<ts>` 文件，限 48h 内
- 用 `chat_id` (case-insensitive) 而非 sessionKey 匹配 — 比 sessionKey 大小写归一更鲁棒
- 命中 + idle ≥ 75min（防活跃流自污染）→ 拉末 8 条 `type=message` 的原始 user/assistant 对话
- 拼成 `prependContext` 注入；同 (agentId,sessionId) 6h dedup 防重复污染
- 字符上限 4000（含模板），单条 message 上限 ≈ `maxChars / tailMessages`

### 红线自查

- ✅ 完全只读 sessions/ 目录（红线 #1，#2 不修改龙虾任何状态）
- ✅ 无 `child_process` / `execSync`（红线 #4）
- ✅ 不复制龙虾原生记忆系统 — 只在原生 hook 之上补盲（红线 #2）
- ✅ `prependContext` 只追加，不覆盖原 system prompt
- ✅ 进程内 6h dedup + LRU cap 防内存泄漏

### 配置

```json
"sessionBridge": {
  "enabled": true,
  "bridgeIdleMinutes": 75,
  "priorMaxAgeHours": 48,
  "tailMessages": 8,
  "maxChars": 4000,
  "freshSessionMaxBytes": 204800,
  "debug": false
}
```

### 关联模块

- `session-recap`（v5.7.x）：结构化元数据回顾，依赖 chapters/todos/decisions 已填好 → 仍然有用，但需要"提前埋点"
- `session-lifecycle`（v5.7.7）：`before_reset` 时抢救 → reset 没发事件就盲区
- `transcript-search`（v5.7.x）：手动工具
- **session-bridge** = 上面三者全部失灵时的最后一道兜底

## 5.7.25 — 2026-05-01（config-doctor 加扫 channel-plugin 缺顶层 channelConfigs）

**触发**：今天为 `@huo15/wechat-service` 修「runtime 启动报 *channel plugin manifest declares wechat-service without channelConfigs metadata*」时，发现 enhance 的 config-doctor 已经扫了 bare pluginApi / async register / 旧版 tool 字段三类反模式，但**没扫这条**。channel 类插件如果 manifest 顶层只声明 `configSchema.properties.channels.<id>` 而没有顶层 `channelConfigs.<id>`，runtime setup 流程在加载前就拿不到 label / description / schema，就会报这个警告。

### 改动

- `src/modules/config-doctor.ts` 新增 `scanInstalledPluginsForMissingChannelConfigs(openclawDir)`：
  - 遍历 `~/.openclaw/extensions/*` 与 `~/.openclaw/node_modules/{,@scope/}*` 下的 `openclaw.plugin.json`
  - 取顶层 `channels`（数组）+ `channelConfigs`（对象），找出 `channels` 声明了但 `channelConfigs` 没覆盖到的 channelId
  - 给出可粘贴的 manifest 补丁示例（参考 `@huo15/wechat-service@2.2.1` 的结构 `channelConfigs.<id>.{label,description,schema}`）
- `checkOpenClawConfig()` 末尾追加调用此扫描，与现有三类扫描并列

### 触发场景

```bash
# 启动期会在 stderr 看到：
[enhance-config-doctor] 检测到 N 项 openclaw.json 配置问题:
  • [warn] plugin-missing-channelConfigs: 已装 channel 插件 @huo15/foo（.../openclaw.plugin.json）
    声明 channels=[foo] 但 manifest 顶层 channelConfigs 缺 [foo]。openclaw runtime setup
    流程需要 channelConfigs.<id>.{label,description,schema} 在 runtime 加载前可用，
    否则启动报警告且 setup 向导无法渲染该 channel
    → 修复: # 在 .../openclaw.plugin.json 顶层加 channelConfigs 字段...

# 或 agent 主动跑：
enhance_config_doctor()
```

### 红线自查

- ✅ 完全只读扫描，不修改任何 manifest（红线 #1）
- ✅ 无 `child_process`（红线 #4）
- ✅ 修复给的是 manifest 补丁示例文本，不自动 patch（红线 #1 + #5）
- ✅ 不复制龙虾原生告警内容，只**主动提供修复命令**（与 bare pluginApi / async register / legacy tool 字段三类扫描同模式）

### KB 关联

- 起因 post-mortem：`~/knowledge/huo15/2026-05-01-wechat-service-v221-channelconfigs-and-stuck-v220-rescue.md`

---

## 5.7.24 — 2026-05-01（bot-share URL 独立兄弟 prefix /plugins/enhance-share）

**用户反馈**：「你应该模仿 https://keepermac.huo15.com/plugins/enhance，把所有的临时下载链接做成这样 `https://keepermac.huo15.com/plugins/enhancexx/{download-url}`，类似把。你自己规划」

—— v5.7.23 把 share 挂在 dashboard 子路径 `/plugins/enhance/share/...` 下，路径耦合 dashboard。用户希望 share 跟 dashboard 平级、各管各的。

### 关键发现：兄弟前缀不算 overlap

重读 SDK 的 [http-route-overlap.js](node_modules/openclaw/dist/http-route-overlap-*.js)：

```js
function prefixMatchPath(pathname, prefix) {
  return pathname === prefix || pathname.startsWith(`${prefix}/`) || pathname.startsWith(`${prefix}%`);
}
```

`startsWith(\`${prefix}/\`)` 要求**斜杠分隔**——所以：

| a.path | b.path | overlap? |
|---|---|---|
| `/plugins/enhance` | `/plugins/enhance/share` | ✅ overlap（子前缀） |
| `/plugins/enhance` | `/plugins/enhance-share` | ❌ 不 overlap（兄弟前缀，分隔字符是 `-` 不是 `/`） |

→ bot-share 可以**直接注册**自己的兄弟 prefix `/plugins/enhance-share`，不再需要 bridge dispatch。

### 设计调整

- **URL 形态**：`https://keepermac.huo15.com/plugins/enhance/share/<token>-<basename>` → `https://keepermac.huo15.com/plugins/enhance-share/<token>-<basename>`
- **HTTP 路由**：bot-share 自己 `api.registerHttpRoute({ path: "/plugins/enhance-share", match: "prefix", auth: "plugin" })`，不再借道 dashboard handler
- **dashboard.ts**：回退到 v5.7.22 状态，只保留 `detectBaseUrlFromRequest(req)` 一行（baseUrl 自动检测仍要走 dashboard 入口才能命中）
- **http-route-bridge.ts**：简化为只导出 `detectBaseUrlFromRequest` / `resolveBaseUrl`，去掉 `registerSubRouteHandler` / `tryHandleSubRoute`
- **share handler**：自己也调一下 `detectBaseUrlFromRequest(req)`——用户即使没访问过 dashboard，第一次点过的下载链接也能让 bridge 缓存 baseUrl

### nginx 兼容性

只要 nginx 反代是 `location /plugins/` proxy_pass（一般都是），新 URL 直接可达。如果用户只反代了 `/plugins/enhance/`（只代理 enhance 一个 plugin），需要补一条：

```nginx
location /plugins/enhance-share/ {
    proxy_pass http://localhost:18789;
    # （跟 /plugins/enhance/ 同样的 proxy headers）
}
```

### 文件影响

- [src/utils/http-route-bridge.ts](src/utils/http-route-bridge.ts)：从 102 行简化到 76 行（去掉 SubRoute 相关导出）
- [src/modules/bot-share-link.ts](src/modules/bot-share-link.ts)：`registerSubRouteHandler` → `api.registerHttpRoute`，urlPrefix 默认 `/plugins/enhance-share`
- [src/modules/dashboard.ts](src/modules/dashboard.ts)：去掉 `tryHandleSubRoute` import 和调用
- npm `5.7.23 → 5.7.24`，plugin `2.4.14 → 2.4.15`

### 红线一致

- 零 child_process（仍用 fs.copyFileSync / linkSync / createReadStream）
- 不修改 openclaw 配置
- HTTP handler 防越界：filename 不能含 `/ \\ ..`，必须 manifest 命中防文件系统枚举
- pluginApi 仍是 `>=2026.4.24`

## 5.7.23 — 2026-05-01（bot-share zero-config：复用 dashboard route + 自动检测 baseUrl）

**用户反馈**：「上次实现增强包面板就没配那么多东西。第一步 nginx 加 alias 和第二步 export BOT_BASE_URL 能不能不做？参考 https://keepermac.huo15.com/plugins/enhance」

—— 用户已经把 dashboard 的 `/plugins/enhance` prefix route 反代到公网，没必要为大文件分享再加一条 nginx alias 或一个 env 变量。

### 设计调整

**问题**：SDK 的 `registerHttpRoute` 不允许两条 prefix route 互为子前缀（[node_modules/openclaw/dist/http-route-overlap-*.js](http-route-overlap-C2701fGQ.js) 的 `doPluginHttpRoutesOverlap` 会拒）。dashboard 已经占了 `/plugins/enhance`，bot-share 想注册 `/plugins/enhance/share` 会被 overlap-denied。

**解决**：新增 [http-route-bridge.ts](src/utils/http-route-bridge.ts)，做两件事：

1. **子路由 dispatch**：bot-share register 时把自己的 handler 挂到 bridge；dashboard handler 顶部 `await tryHandleSubRoute(req, res)`，命中即返。一条 SDK route，多个模块共用。
2. **baseUrl 自动检测**：dashboard handler 顶部 `detectBaseUrlFromRequest(req)`——从 `x-forwarded-host` / `host` + `x-forwarded-proto` 抽出公网 baseUrl 缓存。区分 external（含 `.` 且非纯 IP / localhost）和 internal，external 优先。

**用户体验变化**：

| 维度 | v5.7.22 | v5.7.23 |
|---|---|---|
| nginx 配置 | 需要加 `/share` alias 反代 `~/.openclaw/share/files/` | 不需要——直接复用 dashboard 已经反代过的 `/plugins/enhance/*` |
| BOT_BASE_URL env | 需要 `export` | 不需要——访问一次 dashboard 就自动检测；仍可手动 export 覆盖 |
| 默认 urlPrefix | `/share` | `/plugins/enhance/share` |
| 部署步骤 | 2 步 | 0 步（升级即用，重启 openclaw 后访问一次仪表盘即可） |

### URL 形态

```
旧：https://keepermac.huo15.com/share/<token>-podcast.mp3
新：https://keepermac.huo15.com/plugins/enhance/share/<token>-podcast.mp3
```

文件流式响应（`createReadStream(...).pipe(res)`），HTTP 头：`Content-Type: application/octet-stream` + `Content-Disposition: attachment; filename*=UTF-8''<encoded>` + `X-Content-Type-Options: nosniff`。

### baseUrl resolve 优先级（最终版）

1. `process.env.BOT_BASE_URL`（运行时动态）
2. `pluginConfig.botShare.baseUrl`（启动时静态）
3. **bridge 检测到的 external host**（含 `.` 且非纯 IP / localhost）
4. bridge 检测到的 internal host（localhost）
5. `http://localhost:18789` fallback（仅当上述都没命中，工具响应里会提示用户去访问一次 dashboard）

### 文件影响

- 新增 [src/utils/http-route-bridge.ts](src/utils/http-route-bridge.ts)（76 行）
- [src/modules/bot-share-link.ts](src/modules/bot-share-link.ts) 重写：新增 SDK HTTP handler（流式 GET + HEAD + 405/404/410/400 响应）；删本地 resolveBaseUrl 改用 bridge；urlPrefix 默认 `/plugins/enhance/share`
- [src/modules/dashboard.ts](src/modules/dashboard.ts) handler 顶部加 `detectBaseUrlFromRequest` + `tryHandleSubRoute` 两行
- npm `5.7.22 → 5.7.23`，plugin `2.4.13 → 2.4.14`

### 红线一致

- 零 child_process（continue 用 fs.copyFileSync / linkSync / createReadStream）
- 不修改 openclaw 配置（写自己的 `~/.openclaw/share/`）
- HTTP handler 防越界：filename 不能含 `/ \\ ..`，必须 manifest 命中（防文件系统枚举）
- pluginApi 仍是 `>=2026.4.24`

## 5.7.22 — 2026-05-01（BOT 文件分享桥：企微/钉钉大文件兜底）

**用户反馈**：「最近播客生成 90MB mp3，企微插件直接传不了。每次遇到大文件都卡死。我跑了 FRP 把内网 18789 反代到 Keepermac.huo15.com，希望 enhance 提供一个工具，把本地文件投到一个目录、返回临时 URL 给用户下载。」

### 新增模块：`bot-share-link`

**三个工具**：

| 工具 | 作用 |
|---|---|
| `enhance_share_file(filePath, label?, expireHours?, copyMode?)` | 把本地文件投递到 `<shareRoot>/files/<token>-<basename>`，返回 `<BOT_BASE_URL><urlPrefix>/<token>-<basename>` 临时 URL |
| `enhance_share_list()` | 列当前活跃分享 + 顺手清过期 |
| `enhance_share_revoke(token \| filename)` | 立刻撤销（删本地文件 + manifest 条目） |

**配置（`enhance.botShare`）**：

| 字段 | 默认值 | 说明 |
|---|---|---|
| `enabled` | `true` | tier=1（minimal/balanced/full 都启用） |
| `baseUrl` | env `BOT_BASE_URL` 优先 → 配置 → `http://localhost:18789` | 公网 URL（不含尾部 /） |
| `shareRoot` | `~/.openclaw/share` | 落盘根目录；web server alias 应指向 `<shareRoot>/files` |
| `urlPrefix` | `/share` | URL 路径前缀 |
| `expireHours` | `24` | 默认有效期 |
| `maxFileSizeMB` | `500` | 单文件上限 |

**典型部署**（用户场景）：

```bash
# FRP 把 localhost:18789 反代到 Keepermac.huo15.com
# Nginx 把 /share/* alias 到 ~/.openclaw/share/files/

export BOT_BASE_URL=https://Keepermac.huo15.com
# 然后重启 openclaw，工具返回的 URL 就是 https://Keepermac.huo15.com/share/<token>-<filename>
```

**安全闸门**（防 LLM 输入污染）：

1. `filePath` 必须是绝对路径，不能含 `..` 段
2. 敏感目录黑名单：`/.ssh/ /.gnupg/ /.aws/ /.config/ /.docker/ /.kube/ /.npmrc /.netrc /etc/`
3. 大小上限 `maxFileSizeMB`（默认 500MB），防误传系统盘大文件
4. dest 路径校验：必须 `startsWith` filesDir，防 token 越界
5. `crypto.randomBytes(6)` → 12 hex token，URL 不可枚举遍历

**红线一致**：

- 零 `child_process`：用 `fs.copyFileSync` / `linkSync`
- 不修改用户 openclaw 配置（写的是插件自己的 `~/.openclaw/share/`）
- lazy cleanup：每次 share/list 调用时顺手清过期；不在 register 期跑后台任务
- pluginApi 仍是 `>=2026.4.24`（无新 SDK 依赖）

### 影响面

- `index.ts` 新增 `registerBotShareLink` 注册块（tier=1）
- `src/types.ts` 新增 `BotShareConfig` + `EnhancePluginConfig.botShare`
- `openclaw.plugin.json` 新增 `botShare` configSchema + `botShare.enabled` uiHint，plugin version `2.4.12 → 2.4.13`
- 工具数 `+3`（minimal/balanced/full 都含）

## 5.7.12 — 2026-05-01（模型路由器增强：速度+精度+覆盖率）

### model-router 三方面增强

**1. 响应速度**
- 路由决策缓存（TTL 30s）：相同 prompt 结构命中直接返回，跳过全部检测
- 极短 prompt 短路（<50 字符 + 无媒体）：直接走 MiniMax M2.7，零 regex 开销
- `getBestModel` 结果缓存：provider 遍历结果只算一次
- 定期清理过期缓存条目（>500 条时触发）

**2. 任务识别精度**
- 新增 `matchAny()` 辅助函数，统一 pattern 匹配逻辑
- 超长 prompt（>2000 字符）视为复杂任务直接进 pro，不遍历 pattern
- 中文关键词优化：更多中文业务词汇覆盖，减少误判
- 写作/文案/创作按长度分叉：<300 字符→flash，≥300 字符→pro
- 摘要按长度分叉：<500 字符→flash，≥500 字符→pro

**3. 新增任务类型覆盖**
| 任务类型 | 路由 | 触发示例 |
|---------|------|---------|
| 翻译任务 | flash | 翻译/translate/译成/中译英 |
| 写作/文案/创作 | flash/pro | 写文章/文案/脚本/创意/润色/改写 |
| 数据分析/统计 | pro | 数据分析/统计/报表/图表/可视化 |
| Debug/报错分析 | pro | 报错/error/exception/怎么不行 |
| 情绪/情感分析 | flash | 情绪/情感/心情/sentiment/emotion |
| 数学计算/公式推导 | pro | 计算/推导/证明/公式/方程/微积分 |
| 长文本摘要/总结 | pro(>500) | 总结/摘要/概括/归纳/梳理要点 |
| 信息检索/查找 | flash | 搜索/查一下/什么是/是谁/多少钱 |
| 客服/闲聊 | flash | 你好/hi/谢谢/天气/怎么样 |
| 报告生成 | pro | 合同/协议/标书/投标/方案书 |
| 多步骤推理 | pro | 步骤/逐步/先再然后/chain of thought |
| 快速问答 | flash | 几点/星期几/日期/多少/哪 |

## 5.7.11 — 2026-04-30（修复 WeCom 图片路由）

**用户反馈**："图片路由到 M2.7 报 content empty，M2.7 是 text-only 模型不支持图片"

问题根因：`detectPromptInlineMedia` 只检测 `[image]` 和 `[media attached` 标记，但 WeCom 图片到达时 prompt 里只有文件路径（`~/.openclaw/media/inbound/xxx.png`），没有这些标记，导致图片检测失败，一直路由到 text-only 的 M2.7。

修复：在 `detectPromptInlineMedia` 中新增 WeCom 媒体路径格式检测——任何包含 `~/.openclaw/media/inbound/*.png|jpg|jpeg|gif|webp|bmp` 的 prompt 都会被识别为图片，自动路由到 `MiniMax-VL-01`（vision 模型）。

## 5.7.8 — 2026-04-26（全面适配 openclaw 2026.4.24：typed hooks + manifest 元数据补齐）

**用户反馈**："enhance 插件帮我全面适配 openclaw 最新版本"

跑 SOP 第 1+2 步：(a) `npm view openclaw version` → **2026.4.24**（latest，比当前用的 4.22 多 1 个 minor）；(b) 升级本地 SDK + 跑 typecheck 看不兼容点；(c) 盘点 `as any` 找清理空间。

### 关键发现

读 openclaw 4.24 SDK 类型定义 `node_modules/openclaw/dist/plugin-sdk/src/plugins/types.d.ts`：

```typescript
on: <K extends PluginHookName>(
  hookName: K,
  handler: PluginHookHandlerMap[K],
  opts?: { priority?: number }
) => void;
```

`api.on` 是**完全 typed**！每个 hook 名都对应具体的 `(event, ctx)` 类型：
- `before_tool_call: (event: PluginHookBeforeToolCallEvent, ctx: PluginHookToolContext) => PluginHookBeforeToolCallResult | void`
- `session_start: (event: PluginHookSessionStartEvent, ctx: PluginHookSessionContext) => void`
- `subagent_spawned: (event: PluginHookSubagentSpawnedEvent, ctx: PluginHookSubagentContext) => void`
- ... 全 29 个 hook 都有 typed signature

但 enhance 当前 **14 处 `api.on(...as any, (event: any, ctx: any) => ...)`** —— 把 SDK 的 typed 体验全屏蔽了。这是历史遗留，因为最早期某些版本的 openclaw SDK 没有 typed hook。现在 SDK 完全支持，enhance 该跟上。

### 新增

- **`peerDependencies.openclaw: ^2026.4.22 → ^2026.4.24`** — 跟随 latest tag
- **`openclaw.build.openclawVersion: 2026.4.11 → 2026.4.24`** — 同步（落后了 13 个 patch）
- **`openclaw.compat.pluginApi: >=2026.4.11 → >=2026.4.24`** — 同步
- **`openclaw.plugin.json` 加 3 个新字段**：
  - `enabledByDefault: true` — 装上后默认启用，免去用户手工 `enabled: true` 配置
  - `uiHints` — control-ui 渲染配置面板时用的 widget 提示（switch / select / 中文 label）
  - `activation.onAgentHarnesses: ["claude", "openclaw-default"]` — 声明在哪些 agent harness 下激活

### 修改

- **`api.on(...as any) → api.on(...)` 14 处全清理**：
  - `src/modules/session-lifecycle.ts`（5 个 hook：session_start/end/before_reset/subagent_spawned/subagent_ended）
  - `src/modules/scheduled-tasks-bridge.ts`（before_prompt_build）
  - `src/modules/self-check.ts`（before_agent_reply）
  - `src/modules/session-recap.ts`（before_prompt_build）
  - `src/modules/task-planner.ts`（before_prompt_build）
  - `src/modules/workflow-hooks.ts`（before_prompt_build）
  - `src/modules/tool-safety.ts`（before_tool_call + after_tool_call）
  - `src/modules/mode-gate.ts`（before_tool_call）
- **`(event: any, ctx: any) → (event, ctx)` 5 处**：让 TS 自动从 PluginHookHandlerMap[K] 推断
- **`(ctx as any)?.agentId → ctx?.agentId` 9 处**：每个 PluginHook*Context 都有 `agentId?: string` 字段，无需 cast
- **`pickAgentId(ctx: unknown) → pickAgentId(ctx: { agentId?: string } | undefined)`** 6 个文件：structural typing 兼容 hook ctx 和 tool ctx 两种调用源

### 修复（typecheck 暴露的隐藏 bug）

- **`src/modules/self-check.ts`**：去掉 `as any` 后 TS 报 `Type '{ handled?: undefined; ... }' is not assignable to PluginHookBeforeAgentReplyResult`。根因是 `PluginHookBeforeAgentReplyResult.handled: boolean` **必填**，但 enhance 之前在"不接管"分支返回 `{};`。修法：所有 "不接管"分支改成 `return;`（void），仅"阻断空回复"分支返回 `{ handled: true, reply: {...}, reason: "..." }`。

### 不破坏

- 全部 14 处 hook handler **return undefined（void）** 时跟之前 `return {}` 行为完全一致 —— openclaw 把"void 返回值"和"空对象"等同视为"不接管"
- typed handler 跟 untyped 运行时无差异，只是编译期能 narrow 类型
- 没改任何 SQLite schema、没引入新 npm 依赖
- 老用户从 v5.7.7 升级零成本

### 剩余 `as any` 统计

| 用途 | 数量 | 是否合理 |
|---|---|---|
| `api.on(...as any)` | **0**（之前 14） | ✅ 完全清理 |
| SQLite `.get() as any[]` / `.all() as any[]` | 8 | ✅ better-sqlite3 设计返回 unknown，必须 cast |
| `registerTool factory ((ctx) => ({...})) as any` | 8 | ✅ SDK factory 模式 type-erasure 限制 |
| `(globalThis as any).process` | 1 | ✅ globalThis 类型限制 |
| `(event as any).prompt` | 2 | ⚠️ 待 SDK 暴露 PluginHookBeforePromptBuildEvent 类型时清 |
| `(ctx as any)` 在 helper 内部 | 4 | ⚠️ structural typing 不收紧也可（runtime 行为正确） |
| 其它（错误/边界） | ~32 | 大多是 ts-pattern 风格的边界处理 |
| **总计** | **55** | （从 v5.7.7 的 ~98 降到 55，约 -44%）|

### 设计决策

- **为什么不再追求 0 个 `as any`**：剩下的 55 处都是 SDK / 第三方库设计限制（better-sqlite3 / TypeBox factory），强行清理会引入运行时风险或 schema 复杂度
- **为什么 manifest 加 `activation.onAgentHarnesses`**：当 openclaw 之后引入 lazy plugin loading（现在还没），enhance 能精确声明在哪种 agent 类型下激活，避免 `claude` 之外的 agent harness 误加载
- **为什么 typed handler return `void` 而非 `{}`**：openclaw runtime 对 hook 返回值的处理是 `if (result && typeof result === "object") { ...apply hints... }`，`undefined` 跟 `{}` 行为一致；但 typed signature 要求 `PluginHookXxxResult | void`，`{}` 不满足"必填字段都填"
- **为什么不展开 `(event as any).prompt`**：`PluginHookBeforePromptBuildEvent` 类型存在但 SDK 没顶层 export；强制从子路径导入会增加耦合，等下次 SDK 升级 export 表了再清

### 不冲突 openclaw 4.24 的检查清单

| 检查项 | 状态 |
|---|---|
| 不修改 openclaw 源码 | ✅ |
| 所有 hook handler return void / 已知合法 result | ✅（已通过 typecheck 验证）|
| openclaw 4.24 hook 名都仍存在 | ✅（PluginHookName union 包含全部 29 个）|
| 不复制龙虾原生 memory / cron / tools.allow/deny / channel manifest | ✅ |
| `enabledByDefault` / `uiHints` / `activation` 字段在 4.24 manifest type 里都已定义 | ✅（PluginManifest 含这三个字段）|
| 模块清单中没有跟 openclaw 4.x 重叠的功能 | ✅（之前 v5.2 重写已经把 context-pruner 删了改成 corpus supplement，本轮再次 verify） |

### 调研依据

- `npm view openclaw version` → 2026.4.24
- `node_modules/openclaw/dist/plugin-sdk/src/plugins/hook-types.d.ts: PluginHookHandlerMap`：29 个 hook 完整 typed signature
- `node_modules/openclaw/dist/plugin-sdk/src/plugins/manifest.d.ts: PluginManifest`：完整 manifest 字段（含未用过的 enabledByDefault / uiHints / activation）
- 详见 KB `~/knowledge/huo15/2026-04-27-openclaw-enhance-v578-typed-hooks-postmortem.md`

---

## 5.7.7 — 2026-04-26（session-lifecycle：接入 openclaw 4.22 五个 hook 闭环 session 生命周期）

**用户反馈**："结合 claude 官网的能力描述和本地 claude code 源码看看我们的 enhance 插件还有哪些可以完善的。但是不能干扰 openclaw 最新版的既有能力和跟 openclaw 最新版冲突。"

跑了完整 SELF_ITERATE.md SOP 第 1+2 步（信息更新 + gap 比对）：

### 调研发现

- **Claude Code 官方 docs**（hooks 页）暴露 27 个 hook event names：SessionStart / UserPromptSubmit / PreToolUse / PermissionRequest / PermissionDenied / PostToolBatch / Stop / SubagentStart / SubagentStop / TaskCreated / TaskCompleted / InstructionsLoaded / ConfigChange / CwdChanged / FileChanged / PreCompact / PostCompact / Elicitation / Notification / WorktreeCreate / WorktreeRemove / SessionEnd 等
- **openclaw 2026.4.22 SDK** (`hook-types.d.ts: PluginHookName`) 暴露 **29 个 hook**，跟 Claude Code 一一对应（命名风格不同：`before_/after_/_end` 而非 Claude 的 `Pre/Post/Stop`）
- **enhance 之前只用 4 个 hook**：`before_prompt_build` / `before_tool_call` / `after_tool_call` / `before_agent_reply`
- **反编译 Claude.app** 看到 29 张 SQLite 表，最有价值的没用过：artifacts 多版本 + frames 树状对话历史 + notes 用户批注

### ROI top 5 候选

| # | 候选 | 工作量 | 价值 |
|---|---|---|---|
| **1** | **session-lifecycle**（接 session_start + session_end + before_reset + subagent_*）| ~250 行 | **🔴 立即闭环 session 生命周期** |
| 2 | tool-result-optimizer（接 tool_result_persist 大结果截断+摘要）| ~100 行 | 🟡 长 session 减负 |
| 3 | message_received hook 自动 skill 推荐 | ~60 行 | 🟡 跟 v5.7.5 接合 |
| 4 | artifacts 多版本管理（轻量 SQLite）| ~250 行 | 🔴 但量大留 v5.8 |
| 5 | frames 父子 session 关系跟踪 | ~150 行 | 🟠 留 v5.8 |

**v5.7.7 落地候选 #1**（最高 ROI）。

### 新增

- **`src/modules/session-lifecycle.ts`**（~250 行）— 接入 5 个 hook：
  - `session_start` → idle > 30min 时插入"🚀 会话开始 / 续启"章节占位（不强制每个 session 都加章节，避免噪音）
  - `session_end` → 加"🏁 会话结束"章节 + flush 未完成 in_progress todo 到 project memory（专用 tag `session-flush`, importance=4）
  - `before_reset` → reset 前最后机会抢救最近 3 章节 + 全部未完成 todo 到 decision memory（专用 tag `reset-rescue`, importance=6）+ 推 notification 提醒
  - `subagent_spawned` → 派生子 agent 时插入"🤖 派生子 agent: X"章节
  - `subagent_ended` → 子 agent 结束插入"✅/❌ 子 agent 结束: X"章节
- **`types.ts: SessionLifecycleConfig`** — 5 个 hook 各自可关，含 `debug` 开关
- **`openclaw.plugin.json`** configSchema 加 `sessionLifecycle` 段
- **模块 `tier=1`** minimal 也启用——这是核心生命周期补全，**零工具 schema**（纯 hook 监听，不占 prompt 容量）

### 防 noise factory 三层防御（吸收 v5.7.1 教训）

v5.7.1 删了 `before_compaction` 噪音 hook 后总结了"不要在高频 hook 里无脑写记忆"。新增的 5 个 hook 也是高频（`session_start` 在多 agent 场景每分钟可能多次触发），所以严格控写：

1. **30 秒 dedup**：每个 hook 触发按 `event:agentId:sessionId` 拼 key 进 LRU Map（`MAX_RECENT_ENTRIES=500` + FIFO 淘汰），30 秒内重复触发跳过
2. **重要性低 + 专用 tag**：`session-flush` importance=4（不是用户主动决策）；`reset-rescue` importance=6（reset 前抢救偏重要）。**故意不进 corpus pruner 黑名单**——这些是用户下次想恢复的实质内容，让 pruner 按相关度自然评分
3. **try-catch 包裹**：每个 hook handler 全包，错误只 log 不抛——绝不让插件因 hook 异常 crash

### 不破坏

- 完全只读 openclaw 状态，不修改任何龙虾原生表/文件
- 写入 `chapters` / `memories` 是 enhance 自有表（不污染龙虾原生 memory，v5.5.0 的 corpus supplement 边界保持）
- 没改 SQLite schema、没引入新 npm 依赖
- 没新增 enhance_* 工具（纯 hook 监听）
- 用户可单独关任意 hook（`config.sessionLifecycle.enableSessionStart = false`）

### 设计决策

- **为什么 tier=1**：纯 hook 监听零工具 schema，不占 prompt 容量；session 生命周期是核心补全（minimal 用户也该有）；
- **为什么 session_start 不是每次都加章节**：避免每分钟一个 session 都新加章节造成 chapter 表膨胀；只在 idle > 30min 时加（用户真正"重启"的场景）
- **为什么 before_reset 比 session_end 重要性高**：reset 是用户主动清理，比自然结束激进；importance=6 vs 4 让 corpus pruner 优先返回 reset 抢救的内容
- **为什么不进 corpus pruner 黑名单**：tag=session-flush / reset-rescue 的内容是用户下次想恢复的工作（"上次未完成的 X"），跟 v5.7.1 删的 auto-compact noise（信息量为 0）本质不同
- **为什么 subagent hook 也加章节而非 memory**：spawn 链路属于"事件流"（用户想看时间线），章节比记忆更适合；下游可以用 chapter timeline 看派生关系

### 跟 openclaw 4.22 不冲突的检查

- ✅ openclaw 自己的 `before_compaction` 等 hook 仍正常工作（enhance 不复制不抢占）
- ✅ openclaw 原生 memory 系统不受影响（enhance 只写 enhance-memory.sqlite）
- ✅ openclaw 原生 cron-cli / tools.allow/deny / memory 向量库 enhance 全部不复制
- ✅ openclaw 4.22 类型定义 `PluginHookName` 包含全部 5 个 hook，无破坏性变更

### 调研依据

- 反编译 `/Applications/Claude.app/Contents/Resources/app.asar`：`loadSkills` / `loadSkillContent` / artifacts 多版本 / frames 树状历史
- WebFetch `code.claude.com/docs/en/hooks`：27 个 hook event names + 输入字段
- `/Users/jobzhao/workspace/projects/openclaw/huo15-openclaw-enhance/node_modules/openclaw/dist/plugin-sdk/src/plugins/hook-types.d.ts: PluginHookName`：openclaw 4.22 的 29 个 hook 完整列表
- 详见 KB `~/knowledge/huo15/2026-04-26-openclaw-enhance-v577-session-lifecycle-postmortem.md`

---

## 5.7.5 — 2026-04-26（skill-recommender：按需求自动挑 skill / 推荐未装 / 给自建规划）

**用户反馈**："新增自动根据用户的需求自动挑选已经安装的技能，如果没有技能就把规划方案给出来。看看 Claude 是如何做的"

### 调研：反编译 Claude Desktop 看它怎么做的

反编译 `/Applications/Claude.app/Contents/Resources/app.asar`（参见 SELF_ITERATE.md 第 1 节"反编译 Claude Desktop"）发现：

- `index.js` 里有 `loadSkills()` / `loadSkillContent()` 函数
- system prompt 拼接处有这一句：`"Available skills: ${i.join(", ")}."`
- 也就是说 Claude Desktop 的 skill auto-discovery 算法**本质是 "name+description 列表注入 system prompt 让 LLM 自己挑"**——没有复杂算法

但 enhance 不能照搬"每轮 prompt 注入"——会增加每轮 token 量、抹掉 v5.6 toolTier 减负的努力。所以改成**按需工具**。

### 新增

- **`src/modules/skill-recommender.ts`** — 三段式推荐器：
  1. **启动期扫多路径**（关键修复，WeCom 多 agent 场景）：
     - `~/.openclaw/skills/`
     - `~/.openclaw/workspace/skills/`
     - `~/.openclaw/workspace-*/skills/` ← **WeCom / DingTalk 多 agent 动态 workspace**
     - `~/.openclaw/agents/*/skills/`
     - `<cwd>/.claude/skills/`、`~/.claude/skills/`
     - 用户实测扫到 56 个 skill 跨 27 个路径（一开始只扫 4 个固定路径漏扫，烟测才发现）
  2. **解析 SKILL.md frontmatter**：轻量正则提取 `name` / `description` / `aliases`，**无 yaml 依赖**（zero-deps 红线）
  3. **CJK-aware 评分**：
     - 问题：JS `\w` 不含中日韩，直接 `split(/\s\W/)` 会让"代码简化"变成空数组
     - 解决：连续 CJK 段当整体 phrase + 长 ≥4 时滑动 2-grams（`"代码简化" → ["代码简化","代码","码简","简化"]`）
     - alias exact 命中保底 0.7（典型场景：query "规划XX" → alias "规划" 严格命中）
  4. **未装候选 + 自建规划**（fallback 阶梯）：
     - 已装命中 < threshold=0.25 → 列 ClawHub 上未装的 huo15-* + `openclaw skills install <slug>` 命令
     - 都没合适 → **自建 skill 规划**：建议 slug（含中文 placeholder） + frontmatter 模板 + 触发关键词 + 内容大纲 6 章 + **红线 #3 提醒**（先 ClawHub publish 再让 enhance 引用，插件绝不内嵌 skill 内容）

- **工具：`enhance_skill_recommend`** — `query` 必填，可选 `limit`(1-20) / `includeUninstalled`(默认 true) / `includePlanning`(默认 true)
- **`types.ts: SkillRecommenderConfig`** — `enabled` / `installedThreshold` / `cacheTtlSec`
- **`openclaw.plugin.json`** configSchema 加 `skillRecommender` 段
- **`KNOWN_HUO15_SKILLS` 内置 metadata 表** — 11 个 huo15-openclaw-* skill 的 description + aliases 硬编码兜底（避免运行时查 ClawHub 网络依赖）

### 实测精度

| 查询 | 命中 skill | 分数 |
|---|---|---|
| "帮我 review 这个 PR" | huo15-openclaw-code-review | 0.60（首位）|
| "设计一个 Web UI 原型" | huo15-openclaw-frontend-design | 0.94（首位）|
| "代码简化" | huo15-openclaw-simplify | 1.00（满分）|
| "做安全审查" | huo15-openclaw-security-review | 0.96（首位）|
| "规划这个任务" | huo15-openclaw-plan-mode | 0.70（alias exact 命中保底）|
| "深度探索这块代码" | huo15-openclaw-explore-mode | 0.30（首位）|

### 设计决策

- **为什么按需工具而非每轮 prompt 注入**：v5.6 toolTier 已经在为 prompt cache 减负，注入 56 个 skill 描述会让每轮多 ~3-5k token；改成工具用户/agent 主动调更省
- **为什么 tier=2 而非 tier=1**：用户多半已知道自己装了什么 skill，按需查询不是常驻刚需；balanced/full 默认可见即可
- **为什么内置 KNOWN_HUO15_SKILLS metadata 表**：未装的 skill 没有 SKILL.md 可解析，但要给推荐就需要 description；硬编码 11 个 huo15-* 的 metadata 跟 `CLAW_HUB_SKILLS` 列表保持一致，零网络依赖
- **为什么 CJK 双字滑窗而非真正分词**：上 jieba 是 ~5MB 词典 + 1MB 引擎；双字滑窗虽然有少量误命中（"代码简化" 也产 "码简"），但召回率显著提升且 zero-deps
- **为什么自建规划在结尾强调红线 #3**：用户硬约束"skill 必须先发 ClawHub 再让 enhance 引用，插件不内嵌"，每次给规划都要复刻这个工作流

### 不破坏

- 完全只读 skill 目录，不修改任何 SKILL.md
- 没改 SQLite schema、没引入新 npm 依赖
- 启动期 fire-and-forget 扫描，缓存 60 秒（可调）；扫不到不影响插件正常工作
- 工具 schema 极简（4 参数）；按需调用不占常驻 prompt

### 调研依据

- 反编译 Claude Desktop loadSkills + "Available skills: ${list}." 注入模式
- 用户实测 query 烟测：6 类查询全部首位命中
- 详见 KB `~/knowledge/huo15/2026-04-26-openclaw-enhance-v575-skill-recommender-postmortem.md`

---

## 5.7.4 — 2026-04-26（config-doctor 扩展：扫已装插件 bare pluginApi）

用户反馈：**"提示插件要求 2026.2.24，但是我的 openclaw 已经是 2026.4.22"**。第一反应是 enhance 自己的问题，但实际是另外两个插件违反了 openclaw plugin compat 规则。

### 根因

按 [`MEMORY/openclaw_plugin_compat_rules.md`](https://...): "compat.pluginApi MUST be ">=X.Y.Z" range, never bare version (bare = exact match, breaks on runtime drift)"。

用户实测两处违规：
- `~/.openclaw/extensions/tips/package.json` v1.0.0 → `pluginApi: "2026.4.11"`（bare）
- `~/.openclaw/node_modules/@huo15/huo15-huihuoyun-odoo/package.json` v1.2.0（npm peerDep 残留）→ `pluginApi: "2026.2.24"`（bare）

openclaw 启动扫 node_modules 看到 bare → 解读为精确匹配 2026.2.24 → 跟当前 4.22 不匹配 → 报错"插件要求 2026.2.24"。

### 新增

- **`src/modules/config-doctor.ts: isBarePluginApi(spec)`** — 检测字符串是否是 ranged spec：
  - 带前缀 `>=` `<=` `>` `<` `^` `~` `*` `=` → 合规
  - 含空格组合 range（如 `">=1.0 <2.0"`）→ 合规
  - 数字开头无前缀（如 `"2026.4.11"`）→ **bare 违规**
- **`src/modules/config-doctor.ts: scanInstalledPluginsForBarePluginApi(openclawDir)`** — 扫描三类路径下的 `package.json`：
  1. `{openclawDir}/extensions/*/package.json`（openclaw 实际启用的）
  2. `{openclawDir}/node_modules/@huo15/*/package.json`（@huo15 scope 下的）
  3. `{openclawDir}/node_modules/*/package.json`（无 scope 的）
  - 只检查声明了 `openclaw.extensions` 或 `peerDependencies.openclaw` 的包
  - 命中 bare → 加 `CheckResult` 推到主报告 + 给 python3 inline fix 命令
- 工具 `enhance_config_doctor` 输出自动多一段"已装插件 pluginApi 健康度"

### 不破坏

- 完全只读用户文件系统，绝不修改任何 package.json
- 启动检查失败 try-catch 静默
- 扫描复杂度 O(已装插件数)，单次启动 < 50ms（实测 5 个插件 < 10ms）

### 已立即修用户当前安装

- `~/.openclaw/extensions/tips/package.json`: bare `2026.4.11` → `>=2026.4.11`
- `~/.openclaw/node_modules/@huo15/huo15-huihuoyun-odoo/package.json`: bare `2026.2.24` → `>=2026.2.24`
- 备份分别在同目录 `.bak.before-bare-fix` / `.bak`

### 经验沉淀

- **bare pluginApi 是 silent breakage 的常见来源** —— 插件作者写时通常想表达"最低版本"，但忘了加 `>=`，部署时被解读为精确匹配
- **enhance config-doctor 的诊断范围应该覆盖整个 openclaw 状态目录**，不只 openclaw.json —— 任何会让 openclaw 启动失败的配置陷阱都该报警
- **写在 SELF_ITERATE.md 第 5 节作为发布前自查项**：发版前 npm pack && grep `pluginApi` 看是不是 ranged

### 调研依据

- 用户反馈："提示插件要求 2026.2.24，但是我的 openclaw 已经是 2026.4.22"
- KB `~/knowledge/huo15/2026-04-26-openclaw-enhance-v574-plugin-bare-pluginApi-postmortem.md`

---

## 5.7.3 — 2026-04-26（config-doctor：'Context limit exceeded' 高频反馈兜底）

用户实测：装了 v5.7.2 之后仍然报 `Context limit exceeded. ... agents.defaults.compaction.reserveTokensFloor to 20000 or higher`。**这不是 enhance 插件的问题**，而是 openclaw 自身配置：(1) 缺失 `agents.defaults.compaction.reserveTokensFloor`（4.22 把这个字段从顶层 `compaction.*` 移到 `agents.defaults.compaction.*`，老用户配置文件没自动迁移）；(2) MiniMax-M2.7 maxTokens=131072 / contextWindow=204800，每轮预留输出吃 64% budget，剩 73k 给 input + tools + memory + history，几轮必爆。但用户**装的就是 enhance**，看到爆 context 第一反应是"插件的锅"，所以 enhance 必须主动诊断 + 报警把根因信号给到用户。

### 新增

- **`src/modules/config-doctor.ts`** — 启动期同步读 `~/.openclaw/openclaw.json` 检查：
  1. `agents.defaults.compaction.reserveTokensFloor` 缺失 / < `minReserveTokensFloor`(default 5000) / > `maxReserveTokensFloor`(default 100000)
  2. 任意 `models.providers[*].models[*].maxTokens ≥ contextWindow/2 && > maxModelMaxTokens`(default 32000)
  - 检查到问题：`api.logger.warn` + `notifyQueue.emit(level=warn, source="config-doctor", ...)` 推仪表盘
  - **完全只读，绝不修改用户配置**（红线 #1）
  - 修复命令是 python3 inline JSON 改写一行（红线 #4：不调 child_process / 红线 #5：不在插件里 exec 安装命令）
- **工具：`enhance_config_doctor`** — 无参数，按需重跑诊断（修完用来确认 ✅）
- **`types.ts: ConfigDoctorConfig`** + **`openclaw.plugin.json: configSchema.configDoctor`**
- **`NotificationSource`** 加 `"config-doctor"` 通道

### 设计决策

- **不让插件自动改配置** — 违反零侵入红线 + 用户失去掌控感。给可粘贴命令是平衡点
- **tier=1 minimal 也启用** — 这是关键防爆 context 诊断；minimal 用户更需要这个警告
- **fix 命令选 python3 而非 jq** — python3 macOS/Linux 默认装；jq 不一定有
- **maxModelMaxTokens 默认 32000** — 常用模型 maxTokens 8192-16384，32000 是合理保守阈值

### 不破坏

- 没改任何 openclaw 文件 / enhance SQLite schema 没动
- 新工具 schema 极简（0 参数），单轮 prompt 增加约 30 token
- 老配置无 `configDoctor` 段时默认 enabled=true（用户被动获益）

### 调研依据

- 用户反馈截图：`Context limit exceeded. ... reserveTokensFloor to 20000 or higher`
- 用户当前 `~/.openclaw/openclaw.json` 实测：缺 `agents.defaults.compaction` 段；MiniMax-M2.7 配置 wizard 默认 maxTokens=131072 太大
- 已修用户配置（备份在 `~/.openclaw/openclaw.json.bak.before-compaction-fix-*`）
- 详见 KB `~/knowledge/huo15/2026-04-26-openclaw-enhance-v573-config-doctor-postmortem.md`

---

## 5.7.2 — 2026-04-26（hardening：审计 + 4 类潜在 bug 修复 + 升 peerDep ^2026.4.22）

继 v5.7.1 hot-fix 之后，对全代码库做了一次彻底审计（详见 `docs/SELF_ITERATE.md` 第 4 节 fast-track 流程 + KB post-mortem），用 Explore agent 列了 15 项候选，挑了 4 项 ROI 最高的批量修复。**这是 v5.7.1 的延伸防御层 — 修的都是"现在还没炸但长期运行会炸"的渐进式退化 bug**。

### 修复

- **`src/modules/mode-gate.ts`** — `modeState` / `plannedActions` 两个进程内 Map 之前 keyed by `agentId::sessionId` 永不清理（plan→normal 只清 plannedActions 不清 modeState）。WeCom 多 agent 场景 24h 内可能累积数千 session 状态。
  - 加 `MAX_STATE_ENTRIES = 200` / `MAX_PLANNED_ENTRIES = 200`
  - 新增 `evictOldest()` helper：利用 Map 的 insertion-order 迭代特性，FIFO 淘汰最早 entry
  - 写入前 `if (map.has(key)) map.delete(key)` 让活跃 session 刷新到队尾，避免被误淘汰
- **`src/modules/session-recap.ts`** — 同上，`lastRecapAt` Map 加 `MAX_RECAP_ENTRIES = 500` cap
- **`src/utils/sqlite-store.ts`** — `getDb()` 启动时跑一次 `DELETE FROM safety_log/notifications WHERE created_at < datetime('now', '-90 days')`，try-catch 包裹失败静默；新增 `purgeOldSafetyLogs(db, retentionDays = 90)` helper 给运维 / 工具调用
- **`src/modules/memory-integrator.ts`** — 新增 `TAG_BLACKLIST = {auto-compact, auto-checkpoint, audit, internal}`，`scoreRelevance()` 入口若 `isBlacklisted(memory.tags)` 直接 `return 0`。**这是 v5.7.1 修复的最终兜底**：即便未来某个 hook 又写入 noise，pruner 也不会召回到 prompt
- **`src/modules/structured-memory.ts`** — `enhance_memory_store` 工具检查 tags，若含保留词立即返回错误 `❌ 拒绝存储：tag "..." 是 enhance 保留的系统类标签` 而非写入。防止用户/agent 显式滥用保留 tag
- **`package.json`** — `peerDependencies.openclaw` 从 `>=2026.4.11` 升到 `^2026.4.22`；本地 node_modules openclaw 同步到 4.22；typecheck 通过；hook 名验证全部存在无破坏性变更

### 设计决策

- **为什么 cap 选 200 / 200 / 500**：mode-gate 状态比较"决策性"（200 个活跃 session 对单 agent 已经很多），session-recap 防抖表偏审计性（500 个 session 的 lastRecapAt 也只有 ~12KB 内存）。值故意保守以防误淘活跃数据
- **为什么 TTL 选 90 天而非 30**：safety_log 是审计性数据，跨季度排查事故场景需要保留至少 1 季度。90 天是"季度复盘 + 一周缓冲"
- **为什么 corpus 黑名单做兜底而非依赖 v5.7.1 的删 hook**：删 hook 只解决了已知一个 noise 来源，未来若有新模块又自动写入 audit/internal tag，黑名单这一层能保证 prompt 不被污染。**深度防御**

### 不破坏

- 所有现有 SQLite schema 没改（v5 schema 兼容）；老用户升级无需迁移
- 所有工具名 / API 没改；老脚本兼容
- LRU cap 只影响进程内 Map，重启后恢复，**不影响任何持久化数据**
- 升 peerDep 后老用户仍跑 4.11 的话仍可用（`as any` 屏蔽类型差异，hook 名都还在）

### 调研依据

- 用 Explore agent 跑了一遍审计（详见 KB `~/knowledge/huo15/2026-04-26-openclaw-enhance-v572-hardening-postmortem.md`），输出 15 项候选 bug 清单 + ROI top 3
- 升级 openclaw 4.22 后看 `dist/plugin-sdk/*.d.ts` 确认 hook 名和 ctx 字段无破坏性变更

---

## 5.7.1 — 2026-04-26（hot-fix：删除 before_compaction 噪音 hook + 新增 memory_purge 工具）

**线上 bug 修复**：v5.5.x 引入的 `before_compaction` hook 会在每次 openclaw auto-compact 时把"已压缩"事件作为 `decision` 类、`auto-compact` tag 写入 SQLite — 单条信息量为 0，但因为 tag/content 含 `auto / compact / enhance_memory_search` 等通用词，相关度普遍 0.43-0.51，过 corpus pruner 默认 0.5 阈值。**用户实测库里 613 条全是这种噪音**，把真正的 user/project/feedback 决策完全挤出了 prompt 上下文。

### 删除

- **`src/modules/structured-memory.ts`** — 移除 `api.on("before_compaction", ...)` 那段 hook（22 行）。从此 enhance 不再因为 compact 事件本身写入任何记忆。如果用户真要审计「啥时候 compact 过」，应当走 openclaw 自己的 session 日志，不该污染 enhance 结构化记忆库。

### 新增

- **`src/utils/sqlite-store.ts: purgeMemories()`** — 按 `agentId + tag/category/contentLike` 批量删除 + 可选 dry-run。`tag`/`contentLike` 用 SQL `LIKE %?%` 子串匹配。
- **工具：`enhance_memory_purge`** — 暴露给 agent。`tag` / `category` / `contentLike` 至少传一个；`dry_run` 默认 true（仅返回匹配数，不删除）。一键清理本 bug 历史残留：
  ```
  enhance_memory_purge tag="auto-compact" dry_run=false
  ```

### 用户侧手工清理（如果还没升级）

```bash
sqlite3 ~/.openclaw/memory/enhance-memory.sqlite \
  "DELETE FROM memories WHERE tags LIKE '%auto-compact%'; VACUUM;"
```

### 经验沉淀

- **不要在 `before_compaction` / `before_agent_reply` / `after_tool_call` 这类高频 hook 里无脑写记忆**。本来想做"留时间戳方便回查"的好心，结果变成 noise factory
- **写记忆前过 importance + tag 黑名单**：以后 enhance 自动写入的记忆必须在 corpus supplement 检索阶段再过一遍黑名单（计划 v5.8 实施）
- **审计能力 ≠ 决策记忆**：审计性事件（compact / mode 切换 / hook 触发统计）应该单独写到 audit log 文件或独立表，不能跟 user/project/feedback/reference/decision 这五类决策性记忆混存

### 调研依据

参见本仓库 [`docs/SELF_ITERATE.md`](./docs/SELF_ITERATE.md) v5.7.1 条目，本地 KB `~/knowledge/huo15/2026-04-26-openclaw-enhance-v571-memory-noise-bug-postmortem.md`。

---

## 5.7.0 — 2026-04-25（transcript-search：照搬 Claude Desktop 算法）

延续 v5.5.1 路线图里的 v5.7 候选「⭐ transcript search 会话搜索」。**反编译参考**了 `/Applications/Claude.app/Contents/Resources/app.asar` 里的 `transcript-search-worker/transcriptSearchWorker.js`（94 行官方实现），发现 Claude Desktop **不用 SQL FTS5**，是流式扫 JSONL + `indexOf` 的极简方案。直接照搬到 openclaw 的 session 目录，省下了 v5.5.1 路线图里"建 session_messages 新表 + FTS"的工作量。

### 新增

- **`src/modules/transcript-search.ts`** — 流式扫 `~/.openclaw/agents/<agentId>/sessions/*.jsonl`：
  - `extractText`：兼容 `string` / `[{type:"text", text}]` 数组 / 单 block 对象三种 content 形态（与 Anthropic 标准对齐）
  - `makeSnippet`：±80 字符 radius，开头/结尾用 `…` 表示截断
  - `listSessionFiles`：mtime 倒序，跳过 `.deleted.` / `.checkpoint.` / `.trajectory.`，可选包含 `.reset.`（默认不包含）
  - `scanFile`：单文件 first-match 策略 — 每个 session 只贡献一条 hit（与 Claude Desktop 一致），保证 limit=10 是"找 10 个不同 session"
  - 实测：79 个 session 中扫 30 个 → **3-5 ms** 找到 5 hits
- **工具：`enhance_transcript_search`** — `query` 必填，可选 `agentId / limit (1-50) / includeReset / caseSensitive`
- **`types.ts: TranscriptSearchConfig`** — 新配置段 `config.transcriptSearch.enabled`
- **`openclaw.plugin.json`** — `configSchema.transcriptSearch` 暴露给龙虾配置 UI
- **`index.ts`** — 模块清单加「历史会话搜索」，**tier=2**（balanced 默认就启用，minimal 下不暴露）

### 设计原则

- **零侵入**：完全只读 openclaw session 目录，不建表、不建索引、不写任何文件
- **零依赖**：用 `node:fs` + `node:readline` + `node:path`，没引新包
- **零侵犯隐私**：搜索范围严格限制在当前 ctx.agentId（除非显式传 agentId 参数）

### 设计决策：为什么不用 SQL FTS5

参照 Claude Desktop 反编译实现：

| 维度 | SQL FTS5 | 流式扫 JSONL（照搬） |
|------|---------|---------------------|
| 实现复杂度 | 高（建表 + 触发器同步 + 索引重建） | 低（一个 worker，~200 行） |
| 写入开销 | 每次消息要 INSERT FTS | 0 |
| 跟 openclaw 同步 | 容易 drift（agent reset / 删除时索引脏） | 永远是源数据 |
| 性能 | 查询 ms 级，但需要持续维护 | 3-5 ms（79 个 session 扫 30 个）— **同 SLA** |
| 故障域 | 索引坏了影响搜索 | 单文件坏了不影响其它 session |

结论：在 session 数量级 ≤ 100 的场景下，FTS5 没有任何价值。Claude Desktop 用了几年都没建 FTS，我们也不建。

### 不破坏的兼容点

- 不改任何 openclaw 文件、不动 enhance 自己的 SQLite 库
- 工具 schema 极简（5 个参数），不增加 prompt 负担
- minimal toolTier 用户不会看到这个工具

---

## 5.6.0 — 2026-04-24（工具分层 + workflow 5→2 合并 + 描述压缩）

针对实际使用中"long session 仅 15% 上下文使用率即触发 Context limit exceeded"的现象做容量优化。根因有二：(a) 用户的 `~/.openclaw/openclaw.json` 把 `compaction.reserveTokensFloor` 误设为 `200000`（>205k 总窗），每次压缩都失败 — 需要用户侧改回 `20000`；(b) 插件这边一次性暴露 29 个工具 schema，每轮 prompt 固定底座过重。本版本聚焦 (b)。

### 新增

- **`types.ts: ToolTier` 类型 + `EnhancePluginConfig.toolTier`** — 新增工具分层枚举 `"minimal" | "balanced" | "full"`，默认 `"balanced"`。
- **`openclaw.plugin.json: configSchema.toolTier`** — 暴露给龙虾配置 UI，三档可选。

### 变更

- **`index.ts`** — 模块清单增加 `tier: 1 | 2 | 3` 字段；启动期按 `TIER_MAX[toolTier]` 过滤，超出层级的工具模块整个不 register（连 schema 都不进 prompt）。
  - tier 1 常驻层（minimal 即可见，10 工具）：结构化记忆 / 状态栏 / spawn / 模式闸门 / 章节标记 / installer / integrator
  - tier 2 均衡层（balanced 默认，+8 工具，共 18）：todo / 章节 / 定时任务桥
  - tier 3 完整层（full，+8 工具，共 26）：workflow / safety / task-planner / session-recap / skill-doctor
  - 非工具模块（仪表盘、通知、自检、prompt-enhancer、kb-corpus）一律 tier 1：它们不占 tool schema、不影响 per-turn 成本。
- **`workflow-hooks.ts` 5→2 工具合并** — `enhance_workflow_define / _list / _delete` 三个独立工具合并为单一 `enhance_workflow`（`action=define/list/delete/tasks`）；`enhance_task` 保留独立但仍是 action 派发器。`before_prompt_build` 触发逻辑、所有工作流持久化和评估辅助函数全部保留。
- **批量描述压缩** — 24 个工具的 description 字段从多行 `[...].join("\n")` 压成单行 ≤ 80 字符；总字符量 ~4610 → ~1750（-62%），按中文 ≈0.5 token/字 估算每轮 prompt 节省约 1400 token。压缩注重保留触发关键词，不改 parameters schema。
  - 最大幅压缩：`enhance_memory_store`（~700 字 → 38 字）、`enhance_exit_plan_mode`、`enhance_install_skills`
  - `enhance_todo_list` 已经 ≤ 80 字，未改

### 行为变化

- 默认 `balanced` 模式下 **不暴露** workflow / safety / task-planner / session-recap / skill-doctor 工具。如果你需要这些能力（特别是工作流自动化和 plan-mode-审批闭环），请在 `openclaw.json.plugins.enhance` 配置里加 `"toolTier": "full"` 并重启。
- session-recap 的 `before_prompt_build` hook 在 balanced 下**不**生效（模块整体没注册）；如果你依赖 75min idle 自动回顾，需 `toolTier: "full"`。
- 升级后总工具数 29 → 26（workflow 5→2），即使切回 full 也比 v5.5.1 少 3 个。

### 配置示例

```jsonc
// ~/.openclaw/openclaw.json
{
  "plugins": {
    "enhance": {
      "toolTier": "minimal"   // 极致省 schema，仅留 10 工具
      // "toolTier": "full"   // 全功能，26 工具
    }
  },
  "compaction": {
    "reserveTokensFloor": 20000   // ⚠️ 不要设 200000，会比总窗还大
  }
}
```

### 不破坏的兼容点

- 所有工具名（`enhance_*`）都保留，旧的 `enhance_workflow_define` 等命名外部没用过（只在内部 register），改成 `enhance_workflow` 不破坏任何用户脚本。
- SQLite schema 完全没动；现有记忆 / 任务 / 章节数据无需迁移。
- npm 包对外 API 没变（`definePluginEntry` 出口不变）。

### 修复（顺手）

- **session-recap.ts** — `buildRecapText` 引用了 `MemoryEntry` 上不存在的 `key` / `rule` 字段（v5.5.1 编译错但未被 CI 拦下），全 full tier 场景下生成 decision 段会运行时抛 `TypeError`。修正为 `d.content` 后兼容正确字段并裁切 80 字符。

### 调研依据

参见本仓库 [`docs/v5.6-context-pressure-postmortem.md`](./docs/v5.6-context-pressure-postmortem.md)（如该文件存在），以及本地 KB 条目 `~/knowledge/huo15/2026-04-24-openclaw-context-pressure-postmortem.md`。

---

## 5.5.1 — 2026-04-24（session-recap + 3 个开发辅助 skill）

在 v5.5.0「三层记忆协调」基础上，对齐 Claude Code 2026 Q2 最新能力谱调研结果，补齐两块高频能力：**会话回顾**与**开发辅助三件套**。

### 新增（plugin 模块）

- **`src/modules/session-recap.ts`** — 对齐 Claude Code 75min idle auto-summary。当检测到当前 agent/session 距上次活动 > `recapIdleMinutes`（默认 75），在 `before_prompt_build` 自动 prependContext 一段"你上次到这儿"的回顾（最近章节 + in_progress/pending todo + 最近 decision 记忆）。
  - 工具 `enhance_session_recap` 支持手动触发（不受 idle 阈值限制）
  - 进程内防抖表避免重复 recap：两次间隔 < `recapMinIntervalMinutes`（默认 30）直接 skip
  - 非侵入：只读三张已有表（chapters / todos / memories），**不建新表、不改现有 schema**
  - 可通过 `config.sessionRecap.enabled = false` 关闭
- **`types.ts: SessionRecapConfigType`** — 新配置段 `config.sessionRecap`。

### 新增（3 个开发辅助 skill，通过 huo15-skills 分发）

对齐 Claude Code 原生 `/simplify` / `/security-review` / `/review` 三件套，全部自研、MIT：

- **`huo15-openclaw-simplify` v1.0.0** — 代码简化三维审查（复用 / 质量 / 效率）+ 分级修复清单 + 🔴必改/🟡建议/🟢可选。严格硬红线：不跨文件重命名、不改测试断言、不引入新依赖、不跑格式化器、不碰 generated 代码。
- **`huo15-openclaw-security-review` v1.0.0** — 六类漏洞矩阵（密钥 / 注入 / XSS / SSRF / 权限 / 危险依赖）+ CVSS-like 四档严重度（🔴Critical / 🟠High / 🟡Medium / 🟢Low）+ CWE 编号对照。硬红线：不 exec `npm audit`、不改历史、不明文打印密钥。
- **`huo15-openclaw-code-review` v1.0.0** — PR 五维综合评审（设计 / 实现 / 测试 / 安全 / 可维护）+ 可粘贴 markdown 评论。`gh` CLI 命令走 return-cliCmd 模式（禁 child_process 铁律）。硬红线：不 `gh pr review --approve`、不 `gh pr merge`、不自动 `gh pr comment`。

### 变更（enhance 插件内）

- **`skill-installer.ts`**：`CLAW_HUB_SKILLS` 从 8 扩到 **11**（+simplify / security-review / code-review）。
- **`skill-doctor.ts`**：`EXPECTED_SKILLS` 同步到 11；tool description 从"8 个"改"11 个"。
- **`index.ts`**：新增「会话回顾」模块条目，默认启用。

### 设计决策：为什么 session-recap 是 Plugin 而非 Skill

参照 [MEMORY.md Plugin vs Skill Decision](../../../.claude/projects/-Users-jobzhao/memory/plugin_vs_skill_decision.md)：
- 需要 `before_prompt_build` hook → Skill 做不了
- 需要跨进程状态（lastRecapAt 防抖表 + SQLite 只读查询）→ Skill 做不了
- 触发条件是"idle 时长"的系统级信号，不是用户语义意图 → Plugin 更合适

反之，3 个开发辅助能力是"用户说'帮我 review'时自动加载最佳实践"的语义触发场景，天然 Skill。

### 调研依据

[2026-04-24 Claude Code 能力全景调研（115 条）](../../../knowledge/huo15/2026-04-24-claude-code-capability-survey-and-enhance-roadmap.md)：enhance v5.4 已覆盖 TodoWrite/mark_chapter/plan-mode/ExitPlanMode/statusline 等核心 harness；本版本补齐 session-recap；后续 v5.6/5.7 规划补 hook-observer / path-rules / transcript search。

---

## 5.5.0 — 2026-04-23（三层记忆/知识库协调）

本次聚焦「龙虾原生 memory / enhance 结构化记忆 / KB wiki」三者的职责切分和聚合搜索。

### 新增

- **`src/modules/kb-corpus.ts`** — 新增 corpus supplement，把 huo15-openclaw-openai-knowledge-base 技能的**共享知识库**（`~/.openclaw/kb/shared/wiki/`）注册为龙虾 `memory` 的 `corpus="kb"`。调用 `memory_search` 会同时搜到 enhance-memory + shared KB wiki，无需切换工具。
- **`types.ts: KbCorpusConfigType`** — 新配置段 `config.kbCorpus`，可调阈值、路径、debug。
- **`index.ts`** — 注册「共享知识库语料」模块，默认启用（`kbCorpus.enabled !== false`）。

### 变更

- **`structured-memory.ts: enhance_memory_store` 的 tool description** — 增加 L2/L3 边界提示：「本工具只存规则/为什么/怎么做的短条目；长文档请走 `kb-ingest` 入共享 KB」。

### 三层协调总览

| 层 | 存什么 | 存储 | 隔离 | corpus |
|----|--------|------|------|--------|
| L1 龙虾原生 memory | 向量+FTS 底座 | `~/.openclaw/memory/<agent>.sqlite` | per-agent | `memory` |
| L2 enhance 结构化记忆 | 规则/反馈/决策（短） | `enhance-memory.sqlite` | per-agent | `enhance` |
| L3 共享知识库 | 事实/文档/教程（长） | `~/.openclaw/kb/shared/wiki/*.md` | 跨 agent | `kb` |

### 配套更新

- `huo15-openclaw-openai-knowledge-base` skill v2.5.0 — 所有 `kb-*` 脚本新增 `--scope agent|shared`；`kb-search` 默认聚合搜 agent+shared+obsidian；新增 `kb-scope.sh` 公共库。

---

## 5.4.0 — 2026-04-23（对齐 2026 Q2 设计能力生态）

本次聚焦"设计能力"这一纵向领域，对标 Anthropic 官方 `frontend-design` skill（277k+ 安装）与中文圈 `alchaincyf/huashu-design`（画术，4.6k★）的设计理念，但**全部内容自研**（避开 huashu 仅限个人使用的 license 限制）。

### 新增（4 个设计能力 skill）

通过 [huo15-skills monorepo](https://cnb.cool/huo15/ai/huo15-skills) 分发，首次安装会自动从 clawhub 拉取：

- **`huo15-openclaw-frontend-design` v1.0.0** — 高保真 Web UI 原型生成。5 大美学流派（BOLD-MINIMAL / EDITORIAL / BRUTALIST / RETRO-FUTURE / ORGANIC）+ 8 条反 AI Slop 硬红线（禁 Inter/Roboto、禁紫渐变、禁 emoji 当图标等）+ Junior/Full 两趟渲染工作流 + Playwright 自验证 CLI（延续"禁 child_process"铁律）。对标 Anthropic frontend-design。
- **`huo15-openclaw-design-director` v1.0.0** — 设计方向顾问。内置 20 条设计哲学库（极简/编辑/前卫/东方/功能 5 派）+ 3 方向反差生成规则（1 保守 + 1 反差 + 1 中间）+ 五维对比矩阵 + 强制推荐表态。
- **`huo15-openclaw-brand-protocol` v1.0.0** — 品牌规范抓取。5 步硬流程 Ask / Search / Download / Verify+Extract / Codify，产出结构化 `brand-spec.md`。返回 curl / Playwright CLI 命令让用户执行，**不调 child_process**。
- **`huo15-openclaw-design-critique` v1.0.0** — 5 维设计评审（美学/可用性/品牌一致/内容/实现）+ Keep/Fix/Quick Wins 三分类 + ASCII 雷达图。木桶短板决定总分，命中硬红线美学直接 ≤ 2。

### 变更（enhance 插件内）

- **`skill-installer.ts`**：`CLAW_HUB_SKILLS` 列表从 4 扩展到 8，加入 4 个设计 skill。
- **`skill-doctor.ts`**：`EXPECTED_SKILLS` 同步到 8；tool description 更新。
- **README.md / SKILL.md**：技能清单分为「工作流模式」和「设计能力」两段，加入新增 4 个 skill 的说明。

### 设计决策（为什么做成 Skill 而非 Plugin 模块）

遵循 [MEMORY.md Plugin vs Skill Decision](../../../.claude/projects/-Users-jobzhao/memory/plugin_vs_skill_decision.md) 框架：设计能力是"当用户做 X 时自动应用最佳实践"的**语义触发场景**，不需要 hook / 新 tool / 跨进程状态，因此 Skill-first。Plugin 仅扩展了 `CLAW_HUB_SKILLS` 列表做发现和巡检。

### 与 OpenClaw 原生 / 其他 huo15 技能的边界

| 能力 | 归属 |
|------|------|
| Web UI / HTML 原型 | `huo15-openclaw-frontend-design`（新） |
| 设计方向选型 | `huo15-openclaw-design-director`（新） |
| 品牌规范抓取 | `huo15-openclaw-brand-protocol`（新） |
| 设计评审打分 | `huo15-openclaw-design-critique`（新） |
| PPT 演示稿 | `huo15-openclaw-ppt`（已有） |
| Word / PDF | `huo15-openclaw-office-doc`（已有） |

### 商用合规

本批 4 个 skill 内容**全部自研**，仅参考 Anthropic frontend-design（Anthropic 自有 license）和 huashu-design（仅限个人使用）的**结构设计与设计理念**，不 vendor 其 markdown 文本。@huo15/* 系列所有发布物为商用合规，License 保持 MIT。

---

## 5.2.0 — 2026-04-22（对齐 OpenClaw 2026.4.11）

本次是一次**方向性重写**：把之前"跟着龙虾跑"的模式彻底倒转为"给龙虾打补丁"。核心原则——**凡是龙虾有的，我们绝不复制；凡是龙虾没的 Claude-Code 体验，我们填平**。

### 破坏性变更

- **记忆整合从 prompt-inject 改为 corpus supplement**：
  - 旧版本 `context-pruner` 模块通过 `before_prompt_build` 把打分后的记忆直接 `prependContext`，**与龙虾原生 memory injection 重复/竞争**。
  - 新版本删除 `context-pruner`，在 `memory-integrator` 中改用 `api.registerMemoryCorpusSupplement(...)`（2026.4.11 新增 API），把 enhance 分类记忆作为**并列 corpus** 交给龙虾排序——龙虾是主，插件是补。
- **tool-safety 降级为观察员**：
  - 旧版本尝试"重试"（在 `after_tool_call` 中"retry"并不会真的重新调用工具，是假动作）。
  - 新版本只做错误分类 + 指数退避建议 + 60s TTL 观察窗，**完全不与龙虾原生 `tools.allow/deny` 竞争**。每个工具描述都声明"若与龙虾配置冲突以龙虾为准"。
- `package.json` peerDep：`openclaw >= 2026.4.11`；旧版本不再支持。
- `openclaw.plugin.json` 升至 v2.2.0，重写了 configSchema（新增 7 个模块的开关）。

### 新增（对齐 Claude Code Agent Harness）

- **`enhance_todo_write` / `enhance_todo_update` / `enhance_todo_list`**：对齐 Claude Code `TodoWrite`；SQLite `todos` 表 + 会话隔离；出现多个 `in_progress` 自动发通知警告。
- **`enhance_mark_chapter` / `enhance_chapter_list`**：对齐 Claude Code `mark_chapter`，为 session 打时间线。
- **`enhance_set_mode` / `enhance_current_mode`**：plan / explore / normal 三模式；前两者下 `before_tool_call`（priority=950）阻止 Write/Edit/NotebookEdit + 破坏性 Bash（`rm`、`mv`、`curl -X POST` 等），直到模式切回 normal 或 `exec()` 显式批准。
- **`enhance_statusline`**：line/detail/json 三格式状态快照；HTTP 路由交给 dashboard 统一托管。
- **`enhance_skill_doctor`**：只读巡检 4 个 huo15-\*-mode 技能；缺失时给出 `clawhub install` 命令，**不擅自安装**。
- **`enhance_spawn_task`**：孵化子任务；由于龙虾无 spawn 原语，**只记录不伪装执行**，存为 `category=project, tag=spawn-task` 记忆条目。
- **`enhance_loop_register` / `enhance_loop_list` / `enhance_loop_disable`**：登记定时工作流并返回**一条 `openclaw cron add` CLI 命令**，调度生命周期归龙虾 `cron-cli` 管理；触发时 `before_prompt_build` 识别 `[enhance-loop:{name}]` 前缀并注入 instructions。

### 仪表盘增强

- `/plugins/enhance/api/statusline` — 供 Control UI / 外部嵌入
- `/plugins/enhance/api/todos` — 最近 session 的 todo 快照
- `/plugins/enhance/api/chapters` — 章节时间线
- `/plugins/enhance/api/loops` — 定时工作流登记
- `/plugins/enhance/api/spawn-tasks` — 已孵化子任务
- UI 新增 4 个面板（Todos / Chapters / Loops / Spawn Tasks），切 agent 时全量刷新

### 修复

- 修复 `tool-safety.ts` 中因 `)),` 误写导致的多 tool 注册被串成逗号表达式的 bug。
- 修复 `memory-integrator.ts` 的 `registerMemoryCorpusSupplement` 签名误用（2026.4.11 SDK 公共面是单参，内部全局是双参，之前混了）。
- 移除 `statusline.ts` 内对不存在的 `api.http.registerRoute` 的调用。

### 迁移指引（从 v1.x 升级）

1. 在你的 `openclaw.json` 里把 `plugins.entries.enhance.version` 升到 `^5.2`。
2. 若你之前依赖 `contextPruner.*` 配置段，**现在可以删除**；打分逻辑已并入 corpus supplement（配置项改名为 `memory.relevanceThreshold` / `memory.maxContextEntries`）。
3. 若你期望 enhance 实现自动重试，请**改用龙虾原生的 `tools.retry.*` 配置**；enhance 只给观察数据。
4. Cron 工作流：旧版 `workflows` 触发词仍可用；若要真正定时触发，改用 `enhance_loop_register`，按返回的命令手动跑 `openclaw cron add`。

---

## 5.1.2 — 历史版本

见 git 历史。
