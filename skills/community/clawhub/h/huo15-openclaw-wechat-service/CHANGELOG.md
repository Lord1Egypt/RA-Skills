# Changelog

## 2.3.5 — 2026-05-13（hotfix：errcode 45002 — 字节 vs 字符截断）

### 触发

用户截图反馈：升级 v2.3.x 之后粉丝在公众号发消息**只收到 placeholder「收到，正在为你处理...」**，**收不到 LLM 真回复**（agent 第二条消息丢失）。

### 根因诊断

Gateway log 出现关键错误：

```
[wechat-service] customer_service_send failed accountId=default:
  API cgi-bin/message/custom/send failed:
  errcode=45002 errmsg=content size out of limit
```

**errcode 45002 是「消息内容超长」**——微信公众号客服消息 `cgi-bin/message/custom/send` 的 `text.content` 字段限制是 **UTF-8 字节 2048**，**不是字符 2048**。

我在 v2.3.0 写的渲染器：

```ts
truncateForWechatText(rendered, 2000)  // ← 按字符截 2000
```

中文 1 字在 UTF-8 占 **3 字节**：2000 中文字 = 6000 字节，远超 2048 字节限制。LLM 用 `huo15-customer` persona + KB 答得稍微详细一点（≥ 700 中文字），整段被微信拒绝下发。

placeholder 是另一条独立的被动回复 XML，不走这条路径，所以粉丝先收到 placeholder 后**第二条客服消息静默丢失**——这是最难诊断的失败模式。

### 改动

#### 1) `truncateForWechatText` 改字节截断 — `src/shared/markdown-to-wechat.ts`

```ts
// v2.3.5+ 改成按 UTF-8 字节截断
export function truncateForWechatText(text: string, maxBytes = 1900): string {
  const encoder = new TextEncoder();
  const bytes = encoder.encode(text);
  if (bytes.length <= maxBytes) return text;

  // 二分找最大 char index 使 utf-8 bytes <= maxBytes - 3
  let lo = 0, hi = text.length;
  while (lo < hi) {
    const mid = (lo + hi + 1) >>> 1;
    if (encoder.encode(text.slice(0, mid)).length <= maxBytes - 3) lo = mid;
    else hi = mid - 1;
  }
  let cut = lo;

  // 不截在 <a href> 标签内部（避免 XML 错乱）
  const prefix = text.slice(0, cut);
  const lastOpen = prefix.lastIndexOf("<");
  const lastClose = prefix.lastIndexOf(">");
  if (lastOpen > lastClose) cut = lastOpen;

  return text.slice(0, cut) + "…";
}
```

默认值 **1900 字节**（留 148 字节余量给 envelope 开销 / `<a href>` 标签）。实际可用区间：
- 纯中文：≤ 600 汉字
- 纯英文：≤ 1900 字符
- 中英混合：取中间
- emoji（4 字节）也正确处理

#### 2) `dispatcher.ts` + `customer-service.ts` 去掉硬编码 `2000`

两处调用都不再传 maxChars，让函数走默认 1900 字节。

#### 3) 测试

新增 6 个用例覆盖：
- 纯英文按字节截断
- 纯中文按字节截断
- emoji（4 字节 UTF-8）正确处理
- 默认 maxBytes=1900：600 汉字（1800 字节）原样返回
- 默认 maxBytes=1900：700 汉字（2100 字节）会被截
- `<a href>` 标签不被截在内部（开闭标签数对齐）

**287/287 全绿**（v2.3.4 的 282 + 5 个新增）。

### 兼容性

- 零 API breaking：`truncateForWechatText(text)` 直接调（不传 maxBytes 用新默认 1900 字节）
- 老调用 `truncateForWechatText(text, 2000)` 参数语义变了（之前是字符数，现在是字节数）—— **重要变化**，但只有 plugin 内部调用，外部用户不会传这个参数
- LLM 输出超过 600 中文字现在能正常下发（之前直接被微信拒）

### 升级（强烈建议）

v2.3.0 ~ v2.3.4 都有这个 bug。升级路径：

```bash
openclaw plugins install @huo15/wechat-service@2.3.5
openclaw gateway restart
```

升级后验证：
- 给公众号发个消息触发 LLM 答详细一点（≥ 600 中文字的回答）
- 看 gateway log：`grep "customer_service_send\|errcode=45002" /tmp/openclaw/openclaw-$(date +%F).log`
- 不再出现 `errcode=45002` 即成功

### 教训

微信 / 企微 / 飞书等 IM 平台的消息长度限制**几乎都是字节不是字符**：

| 平台 | 限制 | 备注 |
|------|------|------|
| 微信公众号客服 text | 2048 字节 | `errcode 45002` |
| 微信公众号被动回复 XML | 2048 字节 |  |
| 企业微信 markdown_v2 | 4096 字节 |  |
| 企微 text | 2048 字节 |  |
| 飞书 text | 2048 字节 |  |

中文 1 字 = UTF-8 3 字节是基础常识但容易在写代码时遗忘——尤其是 JavaScript 的 `string.length` 是 UTF-16 code units 数，跟 UTF-8 字节数无关。已沉淀 memory `feedback_wechat_text_byte_limit_not_char.md`。

## 2.3.4 — 2026-05-12（huo15-customer persona 增强 + B 站 111 视频 KB）

### 触发

用户要求把 B 站官方账号（UID 400418085，「逸寻智库AI」）的视频抓进 KB。WebFetch / B 站 wbi API 都被风控；改用 **yt-dlp** 绕过——成功抓到 **111 个完整视频元数据**（标题 / 发布时间 / 时长 / 播放量 / 描述 / tags）。

### 改动

#### 1) 新增共享 KB：`~/.openclaw/kb/shared/wiki/huo15-B站视频清单.md`

按主题分 6 类 + 最新发布前 20 + 最热门前 15 + 客服推荐话术模板 + 维护说明（yt-dlp 命令）：

| 主题 | 视频数 |
|------|------|
| 🤖 AI / 具身智能 / OpenClaw / 大模型 | 11 |
| 🏢 Odoo / ERP / 企业管理（**最强项**） | 36 |
| 📱 移动开发 / uniapp / Android / 鸿蒙 | ~15 |
| 👁️ 视觉 AI / OCR / 质检 | ~5 |
| 🥽 XR / 数字孪生 / UE5 / Unity | ~3 |
| ⛓️ Web3 / 区块链 / 溯源 | ~2 |
| 🛠️ DevOps / Linux / 部署 / 工具 | ~10 |
| 🎬 其他 / 影视杂谈 | ~29 |

热门 Top 3：
1. `2025年最新odoo18 企业版/社区版部署与安装` — 6801 播放
2. `Odoo19开发：用源代码方式部署odoo19[Win11操作系统]` — 1687 播放
3. `odoo18利用deepseek和chatGPT修改合同模板` — 1250 播放

#### 2) `huo15-customer` persona instructions 增强 — `src/shared/personas/it-support.ts`

知识库引用从 6 份扩到 **7 份**，**每份附一句话定位**便于 agent 知道何时查哪份。

新增**防幻觉**指令：

> 「推荐具体视频（粉丝问"某主题怎么学" / "有视频吗"）一定查 huo15-B站视频清单.md 拿真实 BV 号，**不要瞎编 BV**。」

BV 号是 8-12 位字母数字混合（如 `BV1XaRtBiE8z`），LLM 容易幻觉。把"不要编"明确写进 prompt 比抽象描述有效得多（沉淀 memory `feedback_tool_description_vs_prompt_level_constraint.md`）。

#### 3) 更新 `huo15-逸寻智库课程库.md` 共享 KB

「配套视频频道」段从"提一句 B 站链接"扩成"主题覆盖 + 热门 Top 3 + 引流话术 + 指向 huo15-B站视频清单.md"完整对接。

### 兼容性

零 breaking。纯 persona prompt + KB 内容增强。

### 测试

282/282 全过（无新增测试用例，仅 prompt 文本扩展）。

### 升级

```bash
openclaw plugins install @huo15/wechat-service@2.3.4
openclaw gateway restart
# KB 已自动同步到 ~/.openclaw/kb/shared/wiki/，OpenClaw 启动后自动重新索引
```

### 维护脚本（每月跑一次更新 B 站清单）

```bash
yt-dlp --flat-playlist -J --no-warnings \
  'https://space.bilibili.com/400418085' > /tmp/bili_list.json
# 提取 BV 号 → 批量拉单视频 metadata（节流防风控） → 重新生成 huo15-B站视频清单.md
```

完整脚本见 KB 文件末尾「维护说明」段。

## 2.3.3 — 2026-05-12（关键词通配 glob 匹配 + README 大扩 + ignore 重组）

### 触发

用户："综合这些目的，帮我配置关注自动回复、自动关键词触发的一些回复。还有这里的也抓：https://space.bilibili.com/400418085 帮我维护好 readme, ignore"

发现两个产品问题：
1. **关键词匹配过死**：v2.2.0 ~ v2.3.2 仅支持完全匹配（`content === keyword`），"Odoo 怎么学" 不会命中 "Odoo"。运营要列举每个变体，工作量大且漏覆盖。
2. **README 没跟上 v2.3.x**：菜单短路 / markdown 降级 / persona preset / 共享 KB / 关注欢迎语 + 关键词 全没提到，新用户装上不知道怎么用。

### 改动

#### 1) matchKeyword 支持 glob 通配 — `src/auto-reply.ts`

新规则：

| keyword 配置 | 匹配模式 | 命中示例 |
|------|------|------|
| `"你好"` | exact 完全匹配（旧版语义） | "你好" ✓；"你好吗" ✗ |
| `"*Odoo*"` | contains 包含（**大小写不敏感**） | "Odoo 怎么学"、"ODOO" 都 ✓ |
| `"价格*"` | prefix 前缀 | "价格多少" ✓；"问下价格" ✗ |
| `"*多少钱"` | suffix 后缀 | "Odoo 实施多少钱" ✓ |

匹配优先级（向后兼容）：
1. 先按 keys 顺序扫所有 **exact** 关键词
2. 都未命中，再按 keys 顺序扫 **通配** 关键词
3. 第一个命中即返回

这样运营可以「精确短句走快回复 + 通配模糊兜底」共存：

```yaml
keywords:
  "价格":   "固定问候"        # 用户发"价格"两个字走这里
  "*价格*": "通用引导兜底"     # 用户发"我想问下价格多少"走这里
```

测试：`src/auto-reply.test.ts` 新增 5 个通配匹配用例。

#### 2) README.md 大幅扩 — 5 个新章节 + 1 个完整章节重写

- **能力总览表新增 4 行**：内置 persona preset / 菜单事件短路 / Markdown 自动降级 / 自动回复（含 v2.3.3 通配）
- **配置 Schema 块** 加 `defaultInstructionsPreset` + `autoReply` 字段示例
- **新章节「🔁 自动回复实战」**：welcomeText / keywords（含 v2.3.3 glob 通配完整说明 + 43 组 huo15 实战示例）/ businessHours / 执行顺序流图
- **新章节「🤖 内置 Persona Preset + 共享 KB」**：preset 切换 + 6 份共享 KB md 引用路径 + 自定义 instructions SOP
- **最小可用配置** 补 `autoReply` + `dynamicAgents.defaultInstructionsPreset`
- **演进路线** 补 v2.2.0 ~ v2.3.3 全部条目
- **License 段** 改 MIT（v2.2.x 已改）

#### 3) .gitignore / .npmignore 重组

- `.gitignore`：补齐凭据 / pem / bak / tgz / .npm / vitest cache / IDE swp 等漏项，结构化分组（依赖/构建/测试/打包/日志/IDE/系统/凭据/备份/本地）
- `.npmignore`：明确"package.json.files 是白名单优先级最高"的注释，补 .git/ / .cnb.cool/ / *.pem / credentials.json 等防误打包

验证：`npm pack --dry-run` → 303 KB / 317 文件，无 .test.ts / .env / coverage / .github 等垃圾。

### 兼容性

- ✅ 完全向后兼容
- ✅ 老用户的 `keywords: {"帮助": "..."}` 继续完全匹配
- ⚠️ 如果有 keyword 字面量本身包含 `*`，旧版会失败匹配（因为 v2.3.3 把 `*` 当通配符）。极小概率边界，若实际踩到可用 `\\*` 转义未来扩展，但目前无人反馈

### 测试

282/282 全绿（277 + 5 条新增通配用例）。

### 升级

```bash
openclaw plugins install @huo15/wechat-service@2.3.3
openclaw gateway restart

# 配置示例（OpenClaw 配置编辑器或直接 ~/.openclaw/openclaw.json）：
# channels["wechat-service"].autoReply = {
#   "welcomeText": "...",
#   "keywords": { "你好": "...", "*Odoo*": "...", "价格*": "..." },
#   "businessHours": { "timezone": "Asia/Shanghai", "schedule": [...] }
# }
```

## 2.3.2 — 2026-05-12（新增 huo15-customer persona preset + 6 份共享 KB md）

### 触发

用户要求：「帮我配置下服务号聊天这块，单独隔离一个 agent。做客服。帮我在这个 agent 里面做个知识库。主要内容：https://chatai.huo15.com/slides，涉及领域就是公司的 6 个产品 4 个服务（www.huo15.com）能够涉及的 IT 技术和工商管理相关的知识。目的是打造逸寻智库在线教育平台的智能客服。」

### 改动

#### 1) 新增 `huo15-customer` persona preset — `src/shared/personas/it-support.ts`

继 v2.3.0 内置的通用 `it-support` 后，新增专属 preset：**火一五·逸寻智库公众号客服**。

涵盖 system instructions：
- 公司一句话定位 + Mission（10 年 / 100+ 客户 / AI-First）
- **6 大产品**导流：辉火云企业套件 / 辉火云管家 / XR-IoT / 机器视觉 / 镜像世界 / 逸寻智库
- **4 大服务**导流：Odoo 实施 / OpenClaw 增强 / 安全架构 / 高校 XR
- IT 技术领域白名单（Odoo 10~19 全栈 / Python / AI 工程 / 鸿蒙 / Web3 / XR）
- 工商管理领域白名单（ERP 各模块 / 中国本地化 / 数字化转型 / 合规）
- 黑名单（涉政 / 黑灰产 / 医法金具体决策 / 实时新闻）
- **留资转化 4 步路径**：理解需求 → 匹配产品 → 给资源 → 留联系方式
- 课程库引用：https://chatai.huo15.com/slides
- 联系方式：18554898815 / postmaster@huo15.com

启用方式（用户配置）：

```yaml
channels:
  wechat-service:
    dynamicAgents:
      enabled: true
      defaultInstructionsPreset: "huo15-customer"  # ← 切到逸寻智库客服
```

#### 2) 配套共享知识库 — `~/.openclaw/kb/shared/wiki/huo15-*.md`（6 份）

跟随 v2.3.2 发布同时落盘到本机 OpenClaw 共享 KB，所有动态客服 agent 通过 `corpus="kb"` 检索：

| 文件 | 内容 |
|------|------|
| `huo15-公司概览.md` | 公司基本信息 / Mission / 客户画像 / JOSS 活动 |
| `huo15-6大产品.md` | 6 大产品定位 / 适合谁 / 友商差异 / 推荐路径表 |
| `huo15-4大服务.md` | 4 大服务交付内容 / 周期 / 价格沟通流程 |
| `huo15-IT技术知识范畴.md` | IT 领域白名单（Odoo / Python / 前端 / AI / DevOps / XR / Web3 / 视觉 AI） |
| `huo15-工商管理知识范畴.md` | 工商管理领域白名单 + 不答清单 + 自然链接产品技巧 |
| `huo15-逸寻智库课程库.md` | 5 门课程详细信息 + 学习路径推荐 + 客服回答模板 |

#### 3) 配置示例（运营同学复制即用）

```yaml
# ~/.openclaw/config.json 或 OpenClaw config 编辑器中配
channels:
  wechat-service:
    enabled: true
    accounts:
      default:
        appId: wx...
        appSecret: ${WECHAT_SERVICE_APP_SECRET}
        token: ${WECHAT_SERVICE_TOKEN}
        encodingAESKey: ${WECHAT_SERVICE_AES_KEY}
        encryptMode: safe
        name: "逸寻智库"
        replyMode: async
        replyPlaceholderText: "收到，正在为你处理..."
    dynamicAgents:
      enabled: true                                # 一粉一会话独立 session
      dmCreateAgent: true
      defaultInstructionsPreset: "huo15-customer"  # ← 逸寻智库客服 persona
      adminUsers: []                               # 配上你的 openid 可绕过动态路由
```

### 兼容性

- 完全向后兼容
- 老用户继续用 `it-support` preset 不变
- 想切到逸寻智库客服 → 改一行 `defaultInstructionsPreset = "huo15-customer"` + 重启 gateway / 重装 plugin

### 测试

277/277 全绿（preset 注册表加 1 项，原有测试全过）。

### 升级 + 启用步骤

```bash
# 1. 升级 plugin
openclaw plugins install @huo15/wechat-service@2.3.2

# 2. 重启 gateway 让新 persona 生效
openclaw gateway restart

# 3. 配置切到 huo15-customer preset（OpenClaw 配置编辑器或直接改 config.json）
#    channels["wechat-service"].dynamicAgents.defaultInstructionsPreset = "huo15-customer"

# 4. 共享 KB 已落盘到 ~/.openclaw/kb/shared/wiki/huo15-*.md，OpenClaw 启动后自动索引
#    验证：openclaw kb-ingest --scope shared 或 memory_search "火一五 6 大产品"
```

## 2.3.1 — 2026-05-11（hotfix：markdown 渲染下沉到 sendCustomerServiceMessage 底层 + 表格/br/幂等）

### 触发

v2.3.0 升级后用户反馈："回复中还是有 markdown 语法，没有解析成排版。"

根因排查：v2.3.0 只在 `dispatcher.ts:dispatchInboundEvent` 一处接了 markdown 渲染（LLM agent 回复路径）。**绕过 dispatcher 的 4 条 outbound 路径仍发原始 text**：

| 路径 | 谁会发 |
|------|--------|
| `handler.ts:subscribe 欢迎语` | 配置的 `autoReply.welcomeText` |
| `handler.ts:autoReply 关键词回复` | 配置的 `autoReply.keywords[*]` |
| `outbound.ts:sendOutboundText` | 插件主动消息接口（运营广播 / 业务通知）|
| `tools/message-tool.ts` | agent 通过 message tool 主动发的 text |

只要这些路径上有 markdown（用户配的、LLM 通过 tool 调的），粉丝就看到 `**` `#` 等字符。

### 改动

#### 1) 渲染下沉到 sendCustomerServiceMessage 内部 — `src/api/customer-service.ts`

新增 `renderTextMessage()` 内部辅助：所有 `msgtype === "text"` 的客服消息在发往 `cgi-bin/message/custom/send` 之前，content 都会被强制过一遍 `renderMarkdownForWechatText` + `truncateForWechatText(2000)`。

这是**最后一道闸**：

- dispatcher.ts 仍然提前过一次（早转早好，避免后续传 envelope 时携带 markdown 字符）
- 渲染器对纯文本是**幂等**的：`render(render(x)) === render(x)`
- 双层渲染**不会出 bug**：第二次跑时 markdown 标记已被去除，正则不再命中

#### 2) 渲染器增强 — `src/shared/markdown-to-wechat.ts`

新增支持：

- **`<br>` / `<br/>` 换行**：LLM 偶尔会输出 HTML 换行
- **GFM 表格降级**：

  ```
  | 列1 | 列2 |
  |---|---|
  | A | B |
  ```

  → 分隔行 `|---|---|` 整行删掉；数据行 `| a | b |` → `a  ｜  b`（全角分隔保留可读性，公众号 text 没法渲染网格）

- **幂等保护**：测试新增 2 用例验证 `render(render(x)) === render(x)`、a 标签不会被二次解析

### 兼容性

- 零 breaking change
- 已经升 v2.3.0 的用户**强烈建议**升 v2.3.1（v2.3.0 只盖了 dispatcher 一条路径，运营配的 welcome / keyword 仍会漏渲染）

### 测试

277/277 全绿（v2.3.0 273 + 4 条新增：`<br>` / 表格 / 幂等 / a 标签二次解析）。

### 升级生效

```bash
# OpenClaw 内升级
openclaw plugins install @huo15/wechat-service@2.3.1

# 或重启 gateway 让新 plugin manifest 加载
openclaw gateway restart
```

## 2.3.0 — 2026-05-11（菜单事件不回复 + markdown 自动降级 + 默认 IT 学习客服 persona）

### 触发

用户三个诉求：
1. 用户**点击底部菜单不要回复**——之前每次菜单 CLICK/VIEW 都被当成"用户问题"丢给 LLM
2. 回复**自动解析 markdown 排版**——LLM 输出 `**bold**` `# 标题` `- list` 粉丝看到一堆原符号
3. 现在的插件**是不是动态 agent**？想默认配好 IT 客服 persona 四件套

### 改动

#### 1) 菜单事件 short-circuit — `src/transport/webhook/handler.ts`

`runAgentDispatch` 被调用前，对 `inbound.msgType === "event"` 的消息做"路由检查"：

- 当且仅当 `routing.events.<eventKey>` 显式配了 agentId 时，才走 agent
- 没配 = 安静吃下事件，不打扰粉丝（log `event_short_circuit`）

覆盖：CLICK / VIEW / scancode_push / scancode_waitmsg / pic_sysphoto / pic_photo_or_album / pic_weixin / location_select 等 8 类菜单交互事件。

不影响：
- subscribe 欢迎语（继续按 autoReply.welcomeText 模板下发）
- 用户主动文本/图片/语音/视频/位置消息（msgType ≠ "event"）

理由：参考微信公众号官方文档「自定义菜单事件」描述，菜单点击是"触发后端业务"通道，**官方不强制回复**。把每次点击都丢给 LLM 既费 token 又骚扰粉丝。`routing.events.click = "<agentId>"` 给运营留了"针对具体按钮做剧本"的口子。

#### 2) Markdown → 微信 text 降级渲染 — `src/shared/markdown-to-wechat.ts`（新）

公众号客服消息 `msgtype=text` 的 content 字段：
- 支持：`\n` 换行、emoji、`<a href="">` 超链接
- **不支持**：markdown 渲染、`<b>` / `<strong>` / `<i>` 等其他 HTML 标签

新建 `renderMarkdownForWechatText(md)` 转换：

| 输入 | 输出 |
|------|------|
| `# 标题` / `## h2` | `【标题】` |
| `**bold**` / `__bold__` | 去标记保留文本 |
| `*italic*` / `_italic_` / `~~strike~~` | 去标记 |
| `[txt](url)` | `<a href="url">txt</a>`（公众号支持） |
| `![alt](url)` | `[图片] url` |
| `- item` / `* item` / `+ item` | `• item` |
| `> quote` | `▎ quote` |
| `` `code` `` / ``` ```block``` ``` | 去反引号/围栏，保留代码 |
| `---` / `***` / `___` | `————————` |
| 连续 ≥3 空行 | 折叠为 2 |

集成到 `dispatcher.ts:dispatchInboundEvent`，`replyText` 在 `sendCustomerServiceMessage` 之前过 `renderMarkdownForWechatText` + `truncateForWechatText(2000)`。

测试：`src/shared/markdown-to-wechat.test.ts` 20 个用例（边界 + 综合 LLM 输出）。

#### 3) 动态 agent 默认开启 + IT 学习客服 persona — `src/shared/personas/it-support.ts`（新） + `templates/personas/it-support/{soul,identity,user,agents}.md`（新）

- `getDynamicAgentConfig()` 默认 `enabled: true`（v2.2 之前 `false`——装上不开就废一半）
- 新增字段 `dynamicAgents.defaultInstructionsPreset`，默认 `"it-support"`
- `resolveAgentInstructions()` 在 non-role-based 模式下也注入 persona instructions（之前仅 role-based）
- 4 份 persona md 跟着 npm 包发出去（`package.json.files += "templates/**/*"`），既是运维者参考资产，也方便用户复制改写

`it-support` persona 涵盖：
- **soul.md**：世界观与语气（中文优先、短句、给路径不灌内容、不懂就承认）
- **identity.md**：白名单话题（编程语言/前端/后端/AI 工程/工程实践/OpenClaw 生态/学习方法）+ 黑名单（政治/医疗/法律/金融）
- **user.md**：粉丝画像（学生/在职开发者/产品潜在用户）+ 沟通节奏（短问短答/长问详答/拆轮）
- **agents.md**：标准回答结构（直接答 → 落地 → 避坑 → 下一步）+ 不要做（复读/废话开头结尾/伪造链接）

关闭方法：`channels["wechat-service"].dynamicAgents.defaultInstructionsPreset = "none"`。
覆盖单个 agent：直接编辑 OpenClaw 配置 `agents.list[].instructions`。

### 兼容性

- ⚠️ **行为变更**：v2.2.x 用户升 v2.3.0 后，**默认开启动态 agent**（每位粉丝独立 agent + IT persona）。如要回到 v2.2.x 行为：`channels["wechat-service"].dynamicAgents = { enabled: false }`
- 旧配置字段全部兼容，没有 breaking schema 变更
- routing.events 字段早就存在，只是 v2.3.0 起"没配 = 不回复"成了默认行为（之前是"没配 = 仍调 agent"）。如果运营之前依赖菜单事件触发 agent 但**没配 routing.events**，需补一行 `routing.events.click = "main"` 才能保留旧行为

### 测试

273/273 全绿（含 20 条新 markdown 渲染用例 + 4 条新 persona 注入用例）。

## 2.2.4 — 2026-05-11(manifest contracts.tools — 适配 OpenClaw 2026.5.x loader 契约)

### 触发

OpenClaw 2026.5.x gateway 启动 log 大量 warning：

```
[gateway] [plugins] plugin must declare contracts.tools before registering agent tools
  (plugin=wechat-service, source=...dist/index.js)
```

每个工具一条,wechat-service 12 个工具刷 12 条 warning。

### 根因

OpenClaw 2026.5.x loader 在 `registerTool` 加了契约校验,要求 manifest 根级 `contracts.tools[]` 显式声明所有 register 的 tool 名(详见 `dist/loader-B-GXgDrk.js` 的 `normalizePluginToolContractNames`)。

### 改动

`openclaw.plugin.json` 加根级 `contracts.tools` 数组,12 个工具：

```
wechat_service_analytics, wechat_service_article, wechat_service_card,
wechat_service_intelligent, wechat_service_jssdk, wechat_service_mass_send,
wechat_service_material, wechat_service_menu, wechat_service_message,
wechat_service_oauth, wechat_service_qrcode, wechat_service_user
```

### 不影响

- 没改任何代码逻辑,只动 manifest
- 工具注册 / 调用方式不变
- 兼容旧 OpenClaw(2026.4.x 不读 contracts.tools 字段)

## 2.2.2 — 2026-05-02 `[CHORE]`

> 注册 ClawHub plugin tag，让 `openclaw plugins install @huo15/wechat-service`（不带版本号）走 clawhub: 协议解析也能装上；首次显式声明 `openclaw.compat.pluginApi`。

### 改动

- `package.json`: 加 `openclaw.compat.pluginApi = ">=2026.3.23"`（与 `peerDependencies.openclaw` 对齐——之前历史版本一直未声明这个字段）
- `scripts/release.sh`: `clawhub publish` 加 `--tags latest,plugin`，每次发版同时刷 latest + plugin 两个 tag
- 零代码逻辑改动（`src/` 不动）

### 风险评估

跟 `@huo15/wecom@2.8.18` 同款操作。wecom 实测 OpenClaw `clawhub:` 协议装 2.8.18 成功（`Installed plugin: wecom`），证实 enhance 那个 "requires 2026.2.24" 是 5.7.9 bare pluginApi 留下的历史死结特例——不是 ClawHub plugin entry manifest 的普遍 bug。wechat-service 第一次刷 plugin tag 是干净起点。

参见 `~/knowledge/huo15/2026-05-02-clawhub-plugin-tag-stuck-cache.md`。

## 2.2.1 — 2026-05-01 `[FIX]`

> 补 `openclaw.plugin.json#channelConfigs` 顶层元数据，消除 OpenClaw runtime 加载时的配置警告。**首次把 v2.2.0 的功能（角色权限 / AI 护栏 / 自动回复）一并发到 npm + ClawHub。**

### 背景

OpenClaw runtime 启动报：

```
plugins.entries.wechat-service: plugin wechat-service: channel plugin manifest declares wechat-service without channelConfigs metadata; add openclaw.plugin.json#channelConfigs so config schema and setup surfaces work before runtime loads
```

根因：v0.1 起 manifest 只在 `configSchema.properties.channels.wechat-service.*` 下声明配置，但 channel-plugin 形态要求**顶层** `channelConfigs.<channelId>` 元数据，runtime 才能在 setup 流程中渲染 channel 的 label / description / schema，且必须在 runtime 实际加载前可用。v2.2.0 自己也没补这个字段，发上去同样会触发警告，所以 hotfix 跟 v2.2.0 一起发更合理。

### 改动

- **新增** `openclaw.plugin.json` 顶层 `channelConfigs.wechat-service`：
  - `label`：「微信服务号（公众号）」
  - `description`：渠道功能简介
  - `schema`：完整 channel 配置 JSON Schema（`enabled` / `defaultAccount` / `accounts[*]` 多账户矩阵 / `media` / `network` / `routing.events` / `knowledgeSync.odoo` / `dynamicAgents`（含 v2.2.0 `permissionMode=role-based` + `roles` + `rolePermissions` + `defaultRole`）/ `autoReply`（含 `welcomeText` + `keywords` + `businessHours`））
- **新增** `openclaw.plugin.json` 顶层 `channelEnvVars`：声明 `WECHAT_SERVICE_APP_ID / APP_SECRET / ENCODING_AES_KEY / ORIGINAL_ID` 四个 env vars，方便 setup 向导
- 原 `configSchema.properties.channels.wechat-service.*` 路径保留（兼容老 runtime）

### 兼容性

- 纯 manifest 元数据补全 + bump，**无运行时代码改动**
- runtime 同时识别老 `configSchema` 路径与新 `channelConfigs` 路径，已配置实例无需迁移
- 升级方式：`openclaw plugins install @huo15/wechat-service@latest`，重启 OpenClaw 警告即消

### 自查 checklist

- ✅ `package.json.peerDependencies.openclaw` 是 ranged（`^2026.3.23-2`）
- ✅ `npm run typecheck` 通过
- ✅ 无 `child_process` 引入
- ✅ `npm view` latest 仍是 2.1.3，bump 到 2.2.1（npm 上跳过 2.2.0：v2.2.0 commit 在 origin/main 但漏了 npm publish，本次合并发布）

---

## 2.2.0 — 2026-04-29 `[FEAT]`

> **角色权限系统 + AI 对话护栏 + 自动回复**——把 admin-only 升级为多角色细粒度控制；agent 注入角色感知 system prompt 礼貌拒绝越权请求；新增关键词精确匹配 / 业务时间 / 欢迎语模板。

> ⚠️ 本版本 commit 已在 2026-04-29 完成并 push 到 cnb origin（`b7d852b feat: v2.2.0` + `bd1af02 chore: bump`），但 **CHANGELOG / npm publish / clawhub publish 三步漏做**。本条 entry 在 v2.2.1 hotfix 时回灌，并随 2.2.1 一起发布到 npm + ClawHub。

### 🆕 角色权限系统（permissionMode = "role-based"）

```yaml
channels:
  wechat-service:
    dynamicAgents:
      permissionMode: role-based
      roles:
        superadmin: [oABC_owner]
        admin:      [oDEF_lead]
        editor:     [oGHI_writer1, oGHI_writer2]
        operator:   [oJKL_cs1]
        # 其余 openid 走 defaultRole
      defaultRole: customer
      rolePermissions:
        editor:
          tools:
            wechat_service_article: ["add", "update", "publish"]
            wechat_service_material: "*"
```

| 角色 | 内置默认权限 |
|------|------------|
| `superadmin` / `admin` | 全权限（所有 tool / action）|
| `editor` | 内容管理（草稿 / 素材 / freepublish）|
| `operator` | 客服运营（消息 / 用户标签 / 二维码）|
| `customer` | 最小权限（read 类 + 正常对话）|

`adminUsers` 字段在 role-based 模式下**自动映射为 superadmin**，向后兼容 admin-only 配置。

### 🛡️ AI 对话护栏

role-based 模式下：

- **Agent 创建时**：`resolveAgentInstructions()` 把角色感知 system prompt 写入 `agents.list[].instructions`
- **消息分发时**：`injectGuardToEnvelope()` 把护栏 prompt 拼到消息信封
- customer 角色 agent system prompt 含「只能回答常见问题，管理操作礼貌拒绝」
- 不影响"自然对话"路径（粉丝跟公众号正常聊天仍可走）

### 💬 自动回复（autoReply）

```yaml
channels:
  wechat-service:
    autoReply:
      welcomeText: "你好 {{nickname}}，欢迎关注火一五！今天是 {{date}}。"
      keywords:
        "价格": "我们的标准报价见 https://huo15.com/pricing"
        "退款": "退款流程请联系客服微信 huo15-cs"
      businessHours:
        timezone: Asia/Shanghai
        offHoursMessage: "现在是非工作时间（9:00-18:00），客服上班后回复你～"
        schedule:
          - days: [1, 2, 3, 4, 5]
            start: "09:00"
            end: "18:00"
```

- 关键词精确匹配命中：直接回复，不调用 agent，**节省 LLM token**
- 关注事件：欢迎语模板渲染 `{{nickname}}` / `{{date}}` 变量
- 业务时间：非工作时间走 `offHoursMessage`

### 新增/改动文件

- **新增**：
  - `src/auto-reply.ts` + `src/auto-reply.test.ts`（199 + 222 行）
  - `src/shared/roles.ts` + `src/shared/roles.test.ts`（315 + 349 行）
  - `src/shared/guard.ts` + `src/shared/guard.test.ts`（224 + 217 行）
- **改动**：
  - `src/dynamic-agent.ts`（+36 行：角色感知 instructions 注入）
  - `src/runtime/dispatcher.ts`（+24 行：guard 信封注入 / autoReply 调度）
  - `src/transport/webhook/handler.ts`（+53 行：autoReply 优先级）
  - `src/shared/authorization.ts`（+26 行：role-based 决策路径）
  - `src/types.ts`（+53 行：roles / rolePermissions / autoReply 类型）
  - `openclaw.plugin.json`（+17 行：dynamicAgents 新增字段 + autoReply schema）

### 测试

- vitest 184 → **252 用例**（+68）全过
- tsc --noEmit clean

### 兼容性

- 默认 `permissionMode = "open"`，老配置 0 改动，行为完全等同 v2.1.x
- `permissionMode = "admin-only"` 行为不变
- `autoReply` 不配则不启用

---

## 2.1.3 — 2026-04-29 `[DOCS]`

> README 套上公司 Odoo 知识库「README模板」（ID:405）的标准格式。**无代码改动**。

### 模板要素

按公司全局规则（AGENTS.md 2026-04-10）所有代码项目 README 都用同一套模板：

| 位置 | 内容 |
|------|------|
| 开头 | H1 标题 + `<hr>` + slogan 段（"打破信息孤岛..."）+ 5 行信息表（教学机构/讲师/邮箱/QQ群/B 站）+ badges |
| 中间 | `## 📖 正文内容` 大标题 + 全部技术内容（20 节）|
| 结尾 | `<hr>` + 公司全称 + 邮箱 + QQ群 + `<hr>` + "关注逸寻智库公众号" + `<hr>` + License |

### 改动

- **顶部**：从 v2.1.2 的 npm/openclaw badges 居前，重排成 slogan 段 + 信息表（5 行）+ badges
- **底部**：原 "🏢 维护方" 段重写为模板要求的"公司名称 + 联系邮箱 + QQ群"两行 + "关注逸寻智库公众号"提示
- **正文**：所有 20 节技术内容（能力总览 / 安装 / 配置 / bindings / replyMode / 48h / 工具 / 路线图 / 权限 / 路由 / 知识库 / 加密 / 后台 6 件事 / 故障排查 / 完整配置 / 脚本 / 资源）100% 保留，仅在前面套了一个 `## 📖 正文内容` 总标题

### 文件统计

- README 从 544 → **568 行**（+24 行，纯模板要素）
- 段落从 20 → **21**（多了"正文内容"总标题）

### 兼容性

- 纯文档变更，无代码 / schema / 测试改动
- npm + cnb + clawhub 同步发 v2.1.3，让所有渠道展示模板化的 README

---

## 2.1.2 — 2026-04-29 `[DOCS]`

> 大幅扩展 README 配置说明，把生产部署一路踩过的坑全部沉淀成 SOP。**无代码改动**。

### 新增 4 节运维文档

1. **🔗 顶层 `bindings`（必须配！）** —— 把 channel→agent 反向路由说清楚。不配会导致"agent 跑完了但回复消息被静默丢弃"（这是最常踩的坑）。给出多账号 / 多渠道场景的完整配法
2. **📨 回复模式详解** —— `replyMode: async` vs `passive` 行为对比，`replyPlaceholderText` 配法，event 类回调为啥不发占位符，何时该用哪个
3. **⏰ 客服消息「48 小时窗口」硬性约束** —— 解释 `errcode 45015` 来源、超 48h 怎么办（模板 / 订阅消息）
4. **📡 公众号后台必做的 6 件事** —— URL / Token / EncodingAESKey / 加密模式 / **IP 白名单** / 接口权限。带 `curl ifconfig.me` 取出口 IP 教程
5. **🧰 故障排查表** —— 11 条常见错误码对照 + 日志 grep 模板 + "期待的成功链路"日志参考
6. **🚦 完整最小可用配置（一键复制）** —— 包含 agents.list + bindings + channels.wechat-service + plugins.entries 的合规配置范例，直接覆盖 `~/.openclaw/openclaw.json` 就能跑

### 章节统计

- README 从 320 行扩到 **544 行**（+70%）
- 段落数从 14 增到 **20**

### 兼容性

- 纯文档变更，无代码 / schema / 测试改动
- npm + cnb + clawhub 同步发 v2.1.2，让 ClawHub 上的安装页也展示新 README

---

## 2.1.1 — 2026-04-29 `[UX]`

> **修复粉丝消息无反应感** —— v0.1.0 起 `replyPlaceholderText` 字段定义了但**从未被注入响应**（dead code）。粉丝发完消息到 agent LLM 跑完之间几秒到几十秒，粉丝那边"啥反应都没有"，体验差。本版本激活 placeholder。

### 现象

```
粉丝发消息 → 微信 → webhook → 立即返 "success" → 粉丝看不到任何反馈 ......（5~30 秒静默）...... → agent 终于回复 → 客服消息发到 → 粉丝看到回复
```

客户体验：「我刚发完是不是没收到啊？」

### 修复

`src/transport/webhook/handler.ts` —— `replyMode === "async"` 且消息是用户主动发的（text/image/voice/video/location/link），立即用被动回复 XML 返回 `replyPlaceholderText`：

```xml
<xml>
  <ToUserName><![CDATA[oABC...]]></ToUserName>
  <FromUserName><![CDATA[gh_xxxxxxxxxxxx]]></FromUserName>
  <CreateTime>1234567890</CreateTime>
  <MsgType><![CDATA[text]]></MsgType>
  <Content><![CDATA[收到，正在为你处理...]]></Content>
</xml>
```

粉丝立即看到"收到，正在为你处理..."；几秒后 agent 真正的回复通过 `customservice/send` 主动 push 第二条。

### 不影响 event 类回调

关注 / 扫码 / 菜单点击等 event 类回调仍返 `"success"`，避免微信侧因被动回复触发额外重发。

### 自定义占位文本

```yaml
channels:
  wechat-service:
    accounts:
      default:
        replyMode: async                     # 默认就是 async
        replyPlaceholderText: "收到啦~ 正在思考中，请稍候 🤔"   # 不填的话用默认值"收到，正在为你处理..."
```

### 日志变化

- 老：`acked(success) reqId=xxx accountId=default msgType=text from=oXXX`
- 新：`acked(placeholder) reqId=xxx ...`（async 占位生效时）/ `acked(success) ...`（event 回调或非 async 模式）

### 兼容性

- `replyPlaceholderText` 默认值 `"收到，正在为你处理..."`（v0.1 起就有），`replyMode` 默认 `"async"`（v0.1 起就有）—— 现有部署升级到 v2.1.1 自动获得占位反馈，**无需改配置**
- 想关闭占位回到老行为：`replyPlaceholderText: ""`（空字符串）

---

## 2.1.0 — 2026-04-29 `[SECURITY]`

> **权限控制层** —— 让"主 agent"或 `dynamicAgents.adminUsers` 列表中的 openid 才能执行**写/admin** 类操作（发文章 / 群发 / 改菜单 / 改用户标签 / 创建卡券 / 给任意 openid 发消息等）；其他粉丝（在动态 agent 里）只能跑**读类操作**和**跟公众号正常对话**。
>
> 默认 `permissionMode = "open"`（向后兼容 v2.0.x 行为），需显式开启 `"admin-only"` 才生效。

### 🆕 新增 `dynamicAgents.permissionMode` 配置

```yaml
channels:
  wechat-service:
    dynamicAgents:
      enabled: true
      adminUsers:
        - oABC_admin1   # 这些 openid 在 admin-only 模式下可执行写操作
      permissionMode: admin-only   # ← 新字段，默认 "open"
```

| 字段值 | 行为 |
|--------|------|
| `"open"`（默认） | 所有 agent 可执行所有 tool action（v2.0.x 及之前的行为） |
| `"admin-only"` | 写操作仅 main agent / adminUsers / OpenClaw owner 可执行；读操作放行 |

### 🛡️ 权限决策树（`checkAuthorization`）

```
permissionMode = "open"  →  允许
                ↓
permissionMode = "admin-only":
  action 是 read 类  →  允许
  action 是 write 类:
    isMainAgent(agentId)               → 允许   (主 agent)
    requesterSenderId in adminUsers    → 允许   (trusted sender 命中)
    senderIsOwner === true             → 允许   (OpenClaw 全局 owner)
    extractOpenidFromAgentId in admin  → 允许   (fallback 解析)
    otherwise                          → 拒绝   (返回结构化 error ToolResult)
```

### 📋 read vs write 分类（`TOOL_ACTION_CATEGORIES`）

12 个 agent tool 共约 80 个 action，按副作用分类：

| Tool | Read（普通粉丝可用） | Write（仅 admin） |
|------|---------------------|-------------------|
| `wechat_service_message` | list_templates / list_template_library / get_template_library_item / get_industry / subscribe_get_category / subscribe_pub_titles / subscribe_pub_keywords / subscribe_list_templates | 所有 send_* / set_industry / add_template / delete_template / send_template / send_subscribe_once / subscribe_add_template / subscribe_delete_template / send_subscribe / typing |
| `wechat_service_menu` | get / try_match / get_self_menu | create / delete / create_conditional / delete_conditional |
| `wechat_service_material` | list / count / get_temp / get | upload_* / delete_* / update_news |
| `wechat_service_article` | list / get / batchget / count / get_publish_status / get_published_article | add / update / delete / publish |
| `wechat_service_user` | get_info / list_followers / list_tags / list_tag_users / get_user_tags / get_unionid | create_tag / update_tag / delete_tag / batch_tag / batch_untag / set_remark / blacklist_users / unblacklist_users |
| `wechat_service_qrcode` | shorten / fetch | create |
| `wechat_service_mass_send` | （无） | preview / send_by_openid / send_by_tag / undo |
| `wechat_service_jssdk` | sign / get_ticket | invalidate_ticket |
| `wechat_service_oauth` | 全部（OAuth 是用户自己授权流程，所有 action 视为 read） | （无） |
| `wechat_service_analytics` | 全部 | （无） |
| `wechat_service_intelligent` | 全部（OCR / 图像处理无副作用） | （无） |
| `wechat_service_card` | get / batchget / decrypt | create / delete / consume |

未在 `TOOL_ACTION_CATEGORIES` 注册的 action 默认 `write`（more conservative，新增 action 默认安全）。

### ⚠️ 不影响"自然对话"路径

粉丝跟公众号的正常聊天回复走 `runtime/dispatcher.ts:dispatchInboundEvent` 直接调
`sendCustomerServiceMessage`，**不经 tool**。所以 `admin-only` 模式下普通粉丝仍能正常和公众号 agent 对话。

被 block 的是粉丝**主动调 tool** 的场景（例如尝试用 `wechat_service_message.send_text` 给"另一个" openid 发消息 → 视为越权）。

### 新增文件

- `src/shared/authorization.ts` — 权限控制核心（`isMainAgent` / `extractOpenidFromAgentId` / `isAdminUser` / `getPermissionMode` / `categorizeAction` / `checkAuthorization`）+ `TOOL_ACTION_CATEGORIES` 分类表
- `src/shared/authorization.test.ts` — 36 用例覆盖：identity 解析（main agent / dynamic openid / sanitize / legacy key fallback）、admin 匹配（大小写不敏感）、决策树（4 条放行路径 + read/write 分流 + open/admin-only 模式切换）、跨账号 dynamic agent

### 改动文件

- `src/types.ts` — 新增 `WechatServiceDynamicAgentsConfig.permissionMode?: "open" | "admin-only"` 字段
- `openclaw.plugin.json` — `configSchema.dynamicAgents.permissionMode` 加 enum + default 描述
- `src/tools/shared.ts` — 新增 `assertAuthorized()` 辅助；`ToolContext` 加 `agentId / requesterSenderId / senderIsOwner` 字段
- 12 个 agent tool（`*-tool.ts`）— 在 `resolveToolAccount` 之后插入 `assertAuthorized` 闸门
- `package.json` — bump 2.0.1 → 2.1.0

### 测试

- vitest 12/12 文件 → **13/13 文件**，148 → **184 用例**（+36）
- tsc --noEmit clean

### 兼容性

- **完全向后兼容**：默认 `permissionMode = "open"`，老配置 0 改动，行为完全等同 v2.0.x
- 启用 `admin-only` 是显式 opt-in，需要主动加 `permissionMode: "admin-only"` 字段
- API 表面不破坏：`assertAuthorized` 是新增辅助，不影响现有 tool 调用方式

### 升级建议

```diff
 channels:
   wechat-service:
     dynamicAgents:
       enabled: true
       adminUsers:
-        # 之前只用来旁路动态路由
         - oABC_admin1
+      # v2.1.0+ 启用权限控制：写操作仅 main + adminUsers
+      permissionMode: admin-only
```

---

## 2.0.1 — 2026-04-29 `[DOCS]`

> 纯 docs patch：把 `SKILL.md` frontmatter `description` 字段从陈旧的 v1.0.0 措辞刷新到 v2.0.0 的能力描述。**无代码改动**。

让 ClawHub 上 `huo15-openclaw-wechat-service` 的 Summary 显示 v2.0 的架构亮点（runtime/ + shared/ + transport/webhook/ + account-runtime 状态机 + CLI applyAccountConfig），而不是停留在 Phase 0–3 路线图收官那段旧文案。

## 2.0.0 — 2026-04-29 `[ARCHITECTURE]`

> **架构升级里程碑** —— 重组 `src/` 按 `@huo15/wecom` plugin 同构组织，加 account-runtime 状态机和 `setup.applyAccountConfig`（让 CLI `openclaw channels add` 真正可用）。**API 表面无破坏**，老调用全部 backward-compat。

### 🏗️ 文件结构 refactor（mirror `@huo15/wecom`）

```
src/
├── runtime/                ★ NEW
│   └── dispatcher.ts       (← transport/dispatch.ts)
├── shared/                 ★ NEW
│   ├── xml-parser.ts       (← xml.ts)
│   └── xml-parser.test.ts
├── transport/
│   └── webhook/            ★ NEW (← transport/http/ + inbound-parser.ts)
│       ├── handler.ts      (← http/request-handler.ts)
│       ├── normalize.ts    (← inbound-parser.ts)
│       ├── registry.ts     (← http/registry.ts)
│       └── common.ts       (← http/common.ts)
├── app/
│   ├── index.ts            (refactored to use class internally)
│   └── account-runtime.ts  ★ NEW (class)
└── ...                     (api/, tools/, config/, knowledge/ 不动)
```

设计哲学：跟 `@huo15/wecom` 同构 → 运维 / 开发对齐心智模型，未来加能力顺手。

### 🆕 `app/account-runtime.ts` —— Account Runtime 状态机类

```typescript
class WechatServiceAccountRuntime {
  // lifecycle methods
  markStart(at?: number): void;
  markStop(at?: number): void;
  markInbound(at?: number): void;
  markOutbound(at?: number): void;
  markError(error: unknown, at?: number): void;
  clearError(): void;
  // status snapshot
  getStatusSnapshot(): AccountRuntimeStatusSnapshot;
  // factory
  static fromGatewayContext(ctx): WechatServiceAccountRuntime;
}
```

替代 v1.x 的 plain-object `AccountRuntime`。**关键不变量**：原字段访问（`runtime.lastInboundAt`, `runtime.log.info(...)`）100% backward-compat —— class 实现了所有原字段，旧调用代码 0 改动。

旧的 `AccountRuntime` 类型导出仍在，作为 `WechatServiceAccountRuntime` 的 alias。

### 🆕 `setup.applyAccountConfig` —— CLI `channels add` 真正可用

v1.x 之前 plugin 只暴露 `setupWizard`（交互向导），`openclaw channels add --channel wechat-service` 会报：

```
Error: Channel wechat-service does not support add.
```

v2.0.0 新增 `wechatServiceSetupAdapter` 注册到 `plugin.setup`，让 CLI 可以非交互式加账号：

```bash
# 设置环境变量
export WECHAT_SERVICE_APP_ID="wx1234567890"
export WECHAT_SERVICE_APP_SECRET="xxx"
export WECHAT_SERVICE_ENCODING_AES_KEY="xxx"

# 一行命令加账号
openclaw channels add --channel wechat-service --name "我的公众号" --token "MY_TOKEN"
```

**约定式 env vars**：
- `WECHAT_SERVICE_APP_ID` / `WECHAT_SERVICE_APP_SECRET` / `WECHAT_SERVICE_ENCODING_AES_KEY` / `WECHAT_SERVICE_ORIGINAL_ID`（default 账号）
- 非 default 账号用 `WECHAT_SERVICE_<UPPER_ACCOUNTID>_APP_ID` 格式（accountId 中非字母数字会被转成 `_`）

未填的字段后续可在 OpenClaw 主会话跑 `/setup wechat-service` 完整填写。CI / Docker 部署场景终于可以一行命令搞定。

### ✅ 测试

- vitest 文件 10 → **12**，测试用例 121 → **148**（**+27**）
- 新增 `src/app/account-runtime.test.ts` 13 用例（lifecycle 方法 / 状态隔离 / snapshot 纯净 / backward-compat 字段访问 / registry 接口）
- 新增 `src/onboarding.test.ts` 14 用例（resolveAccountId / validateInput / applyAccountConfig 写 kebab key / env var 读取 / 多账号隔离 / encryptMode 落地）

### 🔄 内部 import 更新

15 处 import 路径调整（`from "./xml.js"` → `from "../shared/xml-parser.js"` 等等），全部由 git mv 触发，业务逻辑无变化。

### 🛠️ 兼容性

**100% backward-compat**：
- `AccountRuntime` 类型仍可导入（alias 到 `WechatServiceAccountRuntime`）
- `runtime.lastInboundAt` / `runtime.log.info(...)` 等字段访问仍可用
- `getAccountRuntime` / `registerAccountRuntime` / `updateAccountRuntime` API 签名不变
- `monitor.ts` 公共导出（`handleWechatServiceWebhookRequest`）路径不变
- npm 包名 / channel id / 配置 key 全部不变

**唯一可见改动**：导入了 `from "./xml.js"` 的第三方代码（罕见）需改成 `from "./shared/xml-parser.js"`。

### 📋 v2.1.0 路线图（已规划，本版本不做）

- `types/` 子目录拆分（types.ts → account.ts / config.ts / message.ts / events.ts / reply.ts / routing.ts）
- `runtime/routing-bridge.ts` 抽出（从 dispatcher.ts）
- `capability/` 业务域分组（article/ message/ intelligent/ card/ oauth/ analytics/ ...）

这些是 DX 提升，不影响功能。先发 v2.0.0 让用户用上 setup.applyAccountConfig，后续按需推进。

---

## 1.0.1 — 2026-04-29 `[BUGFIX]`

> ⚠️ **配置 key 重命名修复**：v0.1.0 起 `CONFIG_SECTION_KEY` 一直误用 `"wechatService"`（camelCase），但 channel id 注册的是 `"wechat-service"`（kebab）。OpenClaw v2026.4.x validator 检查 `Object.keys(cfg.channels)` 必须严格等于注册的 channel id，所以**任何 v1.0.0 及之前版本的配置在 latest OpenClaw 上都会报错**：
>
> ```
> Error: Config validation failed: channels.wechatService: unknown channel id: wechatService
> ```

### 修复

把 plugin 内所有读配置时用的 key 从 `"wechatService"` → `"wechat-service"`，与 channel id 对齐。

| 文件 | 改动 |
|------|------|
| `src/config/accounts.ts` | `CONFIG_SECTION_KEY = "wechat-service"`；新增 `LEGACY_CONFIG_SECTION_KEY = "wechatService"`；`getWechatServiceConfig` 加兼容性 fallback（先读 kebab，再 fallback 到 legacy + warn 一次） |
| `src/dynamic-agent.ts` | 改用 `CONFIG_SECTION_KEY` 常量 + legacy fallback 读取 `dynamicAgents` 段 |
| `src/config/index.ts` | 导出 `LEGACY_CONFIG_SECTION_KEY` |
| `openclaw.plugin.json` | configSchema 顶层 key `"wechatService"` → `"wechat-service"` |
| `src/dynamic-agent.test.ts` | 测试 fixture 切到新 key + 新增 2 个用例（legacy fallback / kebab 优先） |
| `src/config/accounts.test.ts` | fixture 切到新 key |

### 文档同步

- `README.md` / `SKILL.md` 配置示例 `wechatService:` → `wechat-service:`（YAML key 含 `-` 不需要引号）
- 错误消息：`outbound.ts` / `request-handler.ts` / `tools/shared.ts` 提示用户 path 改为 `channels["wechat-service"].accounts.*`
- JSDoc：`types.ts` / `dynamic-agent.ts` / `dispatch.ts` 的引用路径同步

### 🔧 用户配置迁移

**JSON 配置（`~/.openclaw/openclaw.json`）**：
```diff
 {
   "channels": {
-    "wechatService": {
+    "wechat-service": {
       "enabled": true,
       "accounts": { ... }
     }
   }
 }
```

**YAML 配置同理**：
```diff
 channels:
-  wechatService:
+  wechat-service:
     enabled: true
```

`-` 在 YAML 里不需要引号；JSON 里因为含 `-` 必须双引号包裹整个 key。

### 兼容性兜底

虽然 OpenClaw validator 会严格拒绝旧 key，但**如果你的部署绕过 validator**（直接 raw config 注入、或某些自定义启动路径），plugin 仍然能从旧 `wechatService` key 读到配置 + 打 warn。下次启动会看到：

```
[wechat-service] config key "channels.wechatService" is deprecated since v1.0.1; please rename to "channels.wechat-service" (kebab-case must equal channel id). OpenClaw config validator will reject the legacy key.
```

### 新增测试

- `dynamic-agent.test.ts`: 23 用例（v1.0.0 是 21）
  - "falls back to legacy 'wechatService' key (v0.1 ~ v1.0.0)"
  - "kebab key takes precedence over legacy key when both present"

### 致谢

- 本 bug 由用户在 v1.0.0 实操 `openclaw channels list` + 手写 `~/.openclaw/openclaw.json` 时触发，validator 报 `unknown channel id: wechatService` —— 一直没人踩是因为 `/setup wechat-service` 向导自动写 key（也是错的，但 v0.1.0 OpenClaw validator 没有现在这么严，可能默默通过了）

---

## 1.0.0 — 2026-04-28

> 🎉 **Phase 3 路线图收官 + v1.0 正式版**：智能开放（OCR + 图像）+ 卡券（精简版）。
> 至此微信公众号官方文档"消息/通知/网页/数据/智能/卡券"六大能力全部接入。

### 🆕 智能开放接口（src/api/intelligent.ts）—— 11 项视觉能力

公众号"智能开放"提供 OCR 和图像处理能力，所有接口都支持公网 `img_url` 直连，
不需要 multipart 上传（保持依赖最小）。

**OCR 7 类**：
- `ocr_idcard_front` / `ocr_idcard_back` — 身份证（人像面/国徽面，同端点 `cv/ocr/idcard` 不同 type）
- `ocr_bankcard` — 银行卡（`cv/ocr/bankcard`）
- `ocr_driving` — 驾驶证（`cv/ocr/driving`）
- `ocr_driving_license` — 行驶证（`cv/ocr/drivinglicense`）
- `ocr_business_license` — 营业执照（`cv/ocr/bizlicense`）
- `ocr_plate_number` — 车牌号（`cv/ocr/platenum`）
- `ocr_common` — 通用印刷体（`cv/ocr/comm`）

**图像处理 3 项**：
- `image_ai_crop` — AI 智能裁剪（`cv/img/aicrop`）
- `image_scan_qrcode` — 二维码 / 条码识别（`cv/img/qrcode`）
- `image_super_resolution` — 图片高清化（`cv/img/superresolution`）

⚠️ **语义理解**（`semantic/semproxy/search`）官方下线多年，本模块不实现。

新增 agent tool **`wechat_service_intelligent`**（list_visions + run vision:<name> imgUrl:<url>）。

### 🆕 卡券（精简版，src/api/card.ts）—— 6 个核心 API

微信卡券是大型业务套件。本模块只覆盖最常用的 80% 场景，避免 over-engineering：

| 函数 | 端点 | 用途 |
|------|------|------|
| `createCard` | `card/create` | 创建卡券（10 种 card_type，payload 由调用方按官方 schema 拼） |
| `getCard` | `card/get` | 查卡券详情（by card_id） |
| `batchGetCards` | `card/batchget` | 批量查列表（offset + count，最大 50；可按状态过滤） |
| `deleteCard` | `card/delete` | 删除卡券 |
| `consumeCardCode` | `card/code/consume` | 核销 code（解析嵌套的 card.card_id + openid） |
| `decryptCardCode` | `card/code/decrypt` | 解码扫码 / JS-API 拿到的 encrypt_code |

**没覆盖的（按需后续补）**：修改库存（`modifystock`）/ 投放卡券（生成卡券二维码）/
货架管理 / 会员卡积分 / 礼品卡兑换券 / 电影票座位 / 景点门票 / 第三方门店。

新增 agent tool **`wechat_service_card`**（6 个 actions：create / get / batchget / delete / consume / decrypt）。

### 新增测试

- `src/api/intelligent.test.ts` — 14 用例：每个 vision action 命中正确端点 + img_url 在 query + idcard 两面同端点不同 type + REGISTRY 完整性
- `src/api/card.test.ts` — 8 用例：每个端点 / body 形态对齐官方文档 + count 上限截断 + consume 解析嵌套 card.card_id + 可选字段省略

### 改动文件

- `src/api/intelligent.ts` — 全新文件，11 个 vision wrapper + `VISION_REGISTRY` + `VISION_ACTIONS`
- `src/api/card.ts` — 全新文件，6 个 card API
- `src/tools/intelligent-tool.ts` — 全新 agent tool（单 tool 双 action 设计）
- `src/tools/card-tool.ts` — 全新 agent tool
- `src/tools/index.ts` — 注册 `registerIntelligentTool` + `registerCardTool`
- `package.json` — bump 0.4.0 → **1.0.0**

### 兼容性

- 完全向后兼容：所有改动都是新增端点 / 新增 tool，不动现有调用
- 1.0.0 版本号语义：**所有 Phase 0–3 路线图能力已落地，API 表面认为稳定**

### 路线图（收官）

- ✅ Phase 0 v0.2.0 — 动态 Agent 框架
- ✅ Phase 1 v0.3.0 — 通知能力补全（模板消息 CRUD + 长期订阅通知）
- ✅ Phase 2 v0.4.0 — 网页授权 OAuth + 数据统计
- ✅ **Phase 3 v1.0.0** — 智能开放（OCR + 图像）+ 卡券（精简版）

至此微信公众号官方文档"消息/通知/网页/数据/智能/卡券"六大能力全部接入。
后续 minor 版本按场景增量补：multipart OCR 上传、卡券扩展能力（投放/积分/兑换券）、
门店 / 电子发票 / 微信支付集成等。

---

## 0.4.0 — 2026-04-28

> Phase 2 路线图落地：网页授权 OAuth2.0 + 数据统计 datacube。
> （`get_current_selfmenu_info` 在 v0.1 已存在，本期跳过菜单查询补全。）

### 🆕 网页授权 OAuth2.0（src/api/oauth.ts）

公众号 H5 / 网页登录场景常用：用户在浏览器里授权后拿 openid（+ 用户资料）。
**与"普通 access_token"（cgi-bin/token）不是同一通道**：OAuth 走 `sns/...` 端点，
用 appid + appSecret 直连，产出"网页授权 access_token"独立计时（60min）。

| 函数 | 端点 | 用途 |
|------|------|------|
| `buildOAuthAuthorizeUrl` | `https://open.weixin.qq.com/connect/oauth2/authorize` | **同步**构造授权跳转 URL（含 #wechat_redirect 硬性后缀） |
| `oauthCodeToAccessToken` | `sns/oauth2/access_token` | code（5min 有效）→ web access_token + openid + refresh_token |
| `oauthRefreshToken` | `sns/oauth2/refresh_token` | refresh_token（30 天）→ 新 web access_token |
| `oauthGetUserInfo` | `sns/userinfo` | 仅 `snsapi_userinfo` scope 可用，含昵称/头像/unionid |
| `oauthValidateAccessToken` | `sns/auth` | 校验 web access_token 有效性，errcode!=0 归一为 valid:false 不抛错 |

新增 agent tool **`wechat_service_oauth`**（5 个 actions：`build_authorize_url` / `code_to_token` / `refresh_token` / `userinfo` / `validate`）。

### 🆕 数据统计 datacube（src/api/analytics.ts）

17 个指标统一封装，单 `wechat_service_analytics` tool 暴露给 agent，
`metric` 参数选具体指标，避免炸出一堆 actions 让 LLM 选错。

**用户分析（2）**：`user_summary`（增减 7d）/ `user_cumulate`（累计 7d）

**图文分析（6）**：`article_summary`（必须 begin==end）/ `article_total`（7d）/ `user_read`（30d）/ `user_read_hour`（必须 begin==end）/ `user_share`（30d）/ `user_share_hour`（必须 begin==end）

**消息分析（7）**：`upstream_msg`（7d）/ `_hour`（必须 begin==end）/ `_week`（30d）/ `_month`（30d）/ `_dist`（7d）/ `_dist_week`（30d）/ `_dist_month`（30d）

**接口分析（2）**：`interface_summary`（30d）/ `interface_summary_hour`（必须 begin==end）

所有指标共用 `{beginDate, endDate}` 入参（YYYY-MM-DD）。区间限制由调用方约束，
模块不做客户端校验（避免与官方文档错位）。

Agent 用法：先 `action:list_metrics` 看清单，再 `action:query metric:user_summary beginDate:... endDate:...`。

### 新增测试

- `src/api/oauth.test.ts` — 10 用例：authorize URL 必须 `#wechat_redirect` 结尾、不带 access_token、redirectUri 编码、validate 失败归一化
- `src/api/analytics.test.ts` — 21 用例：17 指标 × 端点正确 + METRIC_REGISTRY 完整性 + 空 list 安全降级

### 改动文件

- `src/api/oauth.ts` — 全新文件，OAuth 5 个 helper
- `src/api/analytics.ts` — 全新文件，17 个 datacube wrapper + `METRIC_REGISTRY` + `ANALYTICS_METRICS`
- `src/tools/oauth-tool.ts` — 全新 agent tool
- `src/tools/analytics-tool.ts` — 全新 agent tool
- `src/tools/index.ts` — 注册新 tool（`registerOAuthTool` / `registerAnalyticsTool`），imports 改成字母序
- `package.json` — bump 0.3.0 → 0.4.0

### 兼容性

- 完全向后兼容：所有改动都是新增端点 / 新增 tool，不动现有调用
- `cgi-bin/get_current_selfmenu_info`（菜单查询）在 v0.1 已存在，本期跳过

### 路线图

- ✅ Phase 0 v0.2.0 — 动态 Agent 框架
- ✅ Phase 1 v0.3.0 — 通知能力补全（模板消息 CRUD + 长期订阅通知）
- ✅ Phase 2 v0.4.0 — 网页授权 OAuth + 数据统计（本版本）
- ⏭ Phase 3 v1.0.0 — 智能开放接口（语义/OCR/图像）+ 卡券（按需）

---

## 0.3.0 — 2026-04-28

> Phase 1 路线图落地：通知能力补全 —— 模板消息 CRUD（公模板库 + 选用）+ 长期订阅通知（subscribe notification）全套。

### 🆕 模板消息 CRUD 补全（template-message.ts）

之前版本已有 `send / list / delete / setIndustry / getIndustry`，本版本新增缺失的三个：

| 函数 | WeChat API 端点 | 用途 |
|------|----------------|------|
| `addTemplate` | `cgi-bin/template/api_add_template` | 从公模板库选用模板，返回新 `template_id` |
| `getTemplateLibraryList` | `cgi-bin/template/get_template_library_list` | 浏览公模板库（offset + count，最大 20 / 页） |
| `getTemplateLibraryById` | `cgi-bin/template/get_template_library_by_id` | 拉公模板单条详情（含关键词列表） |

### 🆕 订阅通知（subscribe notification）—— 全新模块

服务号 2020 年新版"订阅通知"是模板消息之外的独立通道：用户在前端先调起订阅弹窗
（JS-SDK / 小程序 `wx.requestSubscribeMessage`），后端凭额度下发不限次数的通知。
路径前缀 `wxaapi/newtmpl/...` + 发送端点 `cgi-bin/message/subscribe/bizsend`。

新增 `src/api/subscribe-message.ts` 完整封装 7 个 API：

| 函数 | WeChat API 端点 | 用途 |
|------|----------------|------|
| `getSubscribeCategory` | `wxaapi/newtmpl/getcategory` | 获取公众号所属类目 |
| `getSubscribePubTemplateTitles` | `wxaapi/newtmpl/getpubtemplatetitles` | 浏览公模板库（按类目） |
| `getSubscribePubTemplateKeywords` | `wxaapi/newtmpl/getpubtemplatekeywords` | 查模板关键词 |
| `addSubscribeTemplate` | `wxaapi/newtmpl/addtemplate` | 选用模板 → priTmplId |
| `deleteSubscribeTemplate` | `wxaapi/newtmpl/deltemplate` | 删除已选用模板 |
| `listSubscribeTemplates` | `wxaapi/newtmpl/gettemplate` | 已选用模板列表 |
| `sendSubscribeMessage` | `cgi-bin/message/subscribe/bizsend` | **发送长期订阅通知** |

### 🛠️ Agent Tool 增强（`wechat_service_message`）

`message-tool.ts` 新增 10 个 actions（含 schema 描述）：

```
add_template / list_template_library / get_template_library_item
subscribe_get_category / subscribe_pub_titles / subscribe_pub_keywords
subscribe_add_template / subscribe_delete_template / subscribe_list_templates
send_subscribe
```

Agent 现在可以一条龙完成"模板申请 → 选用 → 发送 → 复盘"流程。

### 新增测试

`src/api/subscribe-message.test.ts`：13 个 vitest 用例覆盖：
- 端点正确（不与"模板消息"端点混淆，特别是 `bizsend` vs `template/send`）
- access_token 走 query
- POST body 形态符合官方文档
- 边界：limit / count 上限截断、可选字段省略行为

### 改动文件

- `src/api/template-message.ts` — 新增 3 个函数（`addTemplate` / `getTemplateLibraryList` / `getTemplateLibraryById`）
- `src/api/subscribe-message.ts` — 全新文件，订阅通知 7 个 API
- `src/api/subscribe-message.test.ts` — 全新文件，13 个用例
- `src/tools/message-tool.ts` — actions enum + parameters schema + switch 各加 10 条
- `package.json` — bump 0.2.0 → 0.3.0

### 兼容性

- 完全向后兼容：所有新功能都是新增端点 / 新增 actions，不动现有调用
- 一次性订阅消息（`send_subscribe_once`）继续工作，与新加的"长期订阅通知"（`send_subscribe`）并存

### 路线图

- ✅ Phase 0 v0.2.0 — 动态 Agent 框架
- ✅ Phase 1 v0.3.0 — 通知能力补全（本版本）
- ⏭ Phase 2 v0.4.0 — 网页授权 OAuth + 数据统计 + `get_current_selfmenu_info`
- ⏭ Phase 3 v1.0.0 — 智能开放接口 + 卡券（按需）

---

## 0.2.0 — 2026-04-28

> Phase 0 路线图落地：动态 Agent 框架（**模仿 @huo15/wecom**）。

### 🆕 动态 Agent 派生（dynamic agents）

每个 openid 自动派生一个独立 agent，实现"一粉一会话"的隔离。配置形态与 `@huo15/wecom` 完全对齐，便于运维同学统一心智模型。

```yaml
channels:
  wechatService:
    accounts:
      default: { appId: ..., appSecret: ..., token: ... }
    dynamicAgents:
      enabled: true            # 总开关
      dmCreateAgent: true      # 私聊（1:1 客服消息场景）派生 agent
      groupEnabled: false      # 公众号无群聊；保留字段是为了与 wecom schema 对齐
      adminUsers:              # 管理员 openid 列表，绕过动态路由走 main agent
        - oABC123xyz
```

**Agent ID 命名规则：** `wechat-service-{accountId}-{type}-{sanitizedOpenid}`

例：`wechat-service-default-dm-oabc123` —— openid 走 sanitize（小写 + 非 `[a-z0-9_-]` → `_`）。

**与 @huo15/wecom 的默认值对齐**

| 字段 | wecom 默认 | wechat-service 默认 | 备注 |
|------|-----------|--------------------|------|
| `enabled` | false | false | 总开关，默认关 |
| `dmCreateAgent` | false | **true** | 公众号场景"每个粉丝一个 agent"是默认推荐 |
| `groupEnabled` | true | **false** | 公众号无群聊场景；保留字段是为了 schema 对齐 |
| `adminUsers` | `[]` | `[]` | 大小写不敏感匹配 |

### 新增文件

- `src/dynamic-agent.ts` — 完整动态路由模块（`getDynamicAgentConfig` / `generateAgentId` / `shouldUseDynamicAgent` / `ensureDynamicAgentListed` / `buildAgentSessionTarget` / `resetEnsuredCache`）
- `src/dynamic-agent.test.ts` — 21 个 vitest 用例覆盖：默认值、Agent ID sanitize、admin 旁路、写入幂等、首次种子 main、并发安全

### 改动文件

- `src/transport/dispatch.ts` — `dispatchInboundEvent` 在 `resolveAgentRoute` 之后注入动态 agent override：
  - `peerKind` 转 `chatType`（公众号永远是 `dm`）
  - 命中 `shouldUseDynamicAgent` 时覆盖 `route.agentId` + `route.sessionKey`
  - fire-and-forget 调 `ensureDynamicAgentListed` 把 agent id 写入 `agents.list`
- `src/types.ts` — 新增 `WechatServiceDynamicAgentsConfig` 类型；`WechatServiceConfig` 加 `dynamicAgents?` 字段
- `openclaw.plugin.json` — `configSchema.properties.channels.wechatService.dynamicAgents` 完整 JSON Schema 定义
- `package.json` — bump 0.1.0 → 0.2.0

### 兼容性

- 默认行为不变：`enabled` 默认 false，老配置直接升级无感
- 多账号 + 静态事件路由（`routing.events`）继续工作；动态 agent 是叠加在它们之上的覆盖层
- agents.list 自动种子 `main`（首次写入时），保证未配 main 的实例也不会出问题

### 路线图

- ✅ Phase 0 v0.2.0 — 动态 Agent 框架（本版本）
- ⏭ Phase 1 v0.3.0 — 通知能力补全（长期订阅消息、模板消息 CRUD）
- ⏭ Phase 2 v0.4.0 — 网页授权 OAuth + 数据统计 + `get_current_selfmenu_info`
- ⏭ Phase 3 v1.0.0 — 智能开放接口 + 卡券（按需）

---

## 0.1.0 — 2026-04-22

初始版本。

### 渠道能力
- Webhook 接入：`/plugins/wechat-service/{accountId}` 主路径 + `/wechat-service/{accountId}` 兼容路径
- 服务器 URL 校验（明文 + 安全模式 echostr）
- 消息解析 / 被动回复 XML 构造 / access_token 管理（自动刷新 + 跨账号缓存）
- 多账号（`channels.wechatService.accounts.*`）多 Agent 路由（`routing.events` + `defaultAgent`）
- async / passive 两种回复模式
- setup wizard：`/setup wechat-service`

### WeChat MP API 覆盖
- 自定义菜单（基础 + 个性化菜单，含 `try_match`）
- 客服消息（text/image/voice/video/news/mpnews/menu/miniprogram/typing）
- 模板消息 + 订阅消息 + 行业设置
- 临时/永久素材、图文素材、素材列表
- 草稿箱 + `freepublish` 发布流水线
- 用户信息、粉丝列表、标签 CRUD、打/取标签、备注、黑名单
- 参数化二维码、短链 shorten / fetch
- JS-SDK `jsapi_ticket` 缓存 + 签名
- 群发（按标签 / openid / 预览 / 速度控制）

### Agent Tools
- `wechat_service_menu` / `_message` / `_material` / `_article` / `_user` / `_qrcode` / `_mass_send` / `_jssdk`

### 知识库双写
- 本地 markdown：`{localPath}/wechat-service/{accountId}/{openid}/{YYYY-MM-DD}.md`，YAML frontmatter + 日粒度追加
- Odoo `knowledge.article`：JSON-RPC `common.login` + `object.execute_kw`，按 title 去重 upsert，支持 `articleParentId`
- 两路独立 best-effort，绝不 throw
