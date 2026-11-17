# OnePilot CLI

OnePilot CLI 是给本地 agent 使用的命令行工具，通过 Skill、Extension 等适配形态接入不同平台。

它可以让 Codex、Claude Code、OpenClaw、Gemini CLI、Qwen Code、WorkBuddy 等本地 agent 连接 OnePilot；其他支持本地命令、Skill、Extension 或 MCP 的 agent 也可以接入。

- 官网：[https://onepilot.zeabur.app](https://onepilot.zeabur.app)
- 小红书：`@One Pilot`

第一版不是 MCP server，而是：

```text
Skill 说明 + onepilot-agent.mjs CLI + OnePilot 服务端 API
```

## 能做什么

- 通过网站绑定码或用户粘贴的邮箱验证码，把本地 agent 绑定到 OnePilot 账号；只有用户明确要求时才使用邮箱工具读取最新 OnePilot 验证码邮件。
- 根据用户偏好、时间、地点和需求推荐 OPC 和 AI 创业相关活动，默认最多返回 3 条。
- 用户同意后，可读取最小必要的日历空闲时间来辅助推荐。
- 推荐结果只返回 OnePilot 站内活动 URL，不直接暴露外部报名链接。
- 用户同意后，保存、查看和删除 agent 维护的长期记忆，例如偏好、可用时间、报名资料、常用回答素材。
- 用户同意后，记录用户对推荐活动的反应，把“什么画像喜欢什么活动”的数据沉淀到 OnePilot 云端。
- 当用户找活动、偏好保存、订阅提醒或报名协作时，使用 OnePilot CLI 的本地命令完成。
- 用户同意后，反馈 OnePilot CLI 使用中的 bug，或把脱敏问题报告给 OnePilot 云端。
- 支持本地订阅：用 `subscription due` 判断是否到期，用 `subscription run-now` 获取推荐。
- 支持报名协作：结合活动上下文、用户记忆和报名问题，帮助 agent 生成报名答案草稿；提交 OnePilot 托管报名表前必须确认。
- 主办方账号可使用 organizer 命令提交/修订活动、资料和报名模板；Owner 确认后可以查看或导出报名数据。

## 通用使用方式

当前版本以仓库根目录的 `VERSION` 文件为准。agent 使用 OnePilot 前可以检查是否有新版；升级由 ClawHub、Codex skill manager、其他 agent 平台或 OnePilot 官方安装器完成：

```bash
node ./scripts/onepilot-agent.mjs version
node ./scripts/onepilot-agent.mjs check-update
```

以上命令默认在 OnePilot CLI 包根目录执行，也就是包含 `SKILL.md`、`scripts/` 和 `references/` 的目录。不同平台只需要把这个目录安装到自己的 Skill 或 Extension 位置，不要改核心脚本。

平台托管升级不需要删除本地绑定配置：

```text
~/.config/onepilot/agent.json
```

## 安装到 Codex

把这个仓库 clone 到 Codex skills 目录：

```bash
mkdir -p "$HOME/.codex/skills"
git clone https://github.com/y09749204-gif/onepilot-skill.git "$HOME/.codex/skills/onepilot"
chmod +x "$HOME/.codex/skills/onepilot/scripts/onepilot-agent.mjs"
```

检查状态：

```bash
cd "$HOME/.codex/skills/onepilot"
node ./scripts/onepilot-agent.mjs status
```

如果返回 `bound: false`，说明还没有绑定 OnePilot 账号。agent 应主动告诉用户 OnePilot 已安装但未绑定，并询问是否现在通过邮箱验证码或网站绑定码完成绑定。

同一 OnePilot 账号同时只保留一个有效 agent。新设备或新 agent 绑定成功后，旧设备上的 agent token 会自动失效；推荐额度按账号共享，不按设备或 agent 单独计算。

## 第一阶段分发渠道

第一阶段优先维护这些入口：

- OnePilot 官网下载页：[https://onepilot.zeabur.app](https://onepilot.zeabur.app)，给普通用户复制安装口令。
- GitHub Release：给海外开发者和可访问 GitHub 的 agent 下载 zip。
- Qwen Code Extension：使用 `qwen-extension.json` 做薄适配，核心仍调用同一个 CLI。
- ClawHub：以 Skill 形态发布同一份 OnePilot CLI 包，不复制业务逻辑。
- WorkBuddy / SkillHub：按 OpenClaw/SkillHub 兼容结构做实验性安装验证；正式上架前确认目标市场要求的元数据和审核入口。

这些文件用于发布准备：

```text
README.md
SKILL.md
references/adapters.md
agents/openai.yaml
CHANGELOG.md
LICENSE
SECURITY.md
qwen-extension.json
.claude-plugin/plugin.json
package.json
```

不同平台只负责“怎么安装、怎么让 agent 执行命令、有没有邮箱/日程工具”。推荐、记忆、订阅、反馈和报名协作逻辑都在 `SKILL.md` 与 `scripts/onepilot-agent.mjs` 里维护。

## WorkBuddy 兼容验证

WorkBuddy 适配应保持薄包装：把同一份 OnePilot CLI 包安装到 WorkBuddy 或 SkillHub 要求的位置，然后从该目录调用 `node ./scripts/onepilot-agent.mjs`。绑定时使用：

```bash
node ./scripts/onepilot-agent.mjs bind --code OPB-XXXXXXXXXXXX --agent-name WorkBuddy
```

如果 WorkBuddy 只允许 MCP、不允许本地命令执行，后续再增加 OnePilot MCP server；不要把 OnePilot 推荐、记忆、订阅、反馈或报名逻辑复制成 WorkBuddy 专用实现。

## 邮箱验证码绑定

可以用邮箱验证码绑定 OnePilot。默认做法是用户把验证码贴给 agent；如果用户明确要求使用 Gmail、Outlook 或其他邮箱 connector，agent 只读取完成绑定所需的最新 OnePilot 验证码邮件，然后把验证码交给 CLI。

```bash
node ./scripts/onepilot-agent.mjs bind-email start --email user@example.com --agent-name AgentName
mail-tool-read-latest-onepilot-code | node ./scripts/onepilot-agent.mjs bind-email verify --email user@example.com --code-stdin --agent-name AgentName
```

如果当前 agent 没有邮箱工具，直接让用户粘贴验证码即可：

```bash
node ./scripts/onepilot-agent.mjs bind-email verify --email user@example.com --code 123456 --agent-name AgentName
```

## 网站绑定码绑定

如果你已经在 OnePilot 网站里生成了绑定码：

```bash
node ./scripts/onepilot-agent.mjs bind --code OPB-XXXXXXXXXXXX --agent-name AgentName
```

## 推荐活动

推荐前，如果用户没有说明可参加时间，agent 应先询问：

```text
你有没有本地日程工具，并且是否同意我读取你的空闲时间？如果没有或不同意，我也可以直接通过对话了解你的可用时间。
```

如果用户同意且 agent 有飞书日历、Google Calendar、本地日历或其他日程工具，就只读取本次推荐所需的空闲时间。没有工具或用户不同意时，再通过对话收集时间范围。OnePilot 云端第一版不直接连接用户日历。

```bash
node ./scripts/onepilot-agent.mjs recommend \
  --query "这周有什么适合我的 AI agent 创业活动" \
  --topics "AI agent,创业" \
  --districts "徐汇,静安" \
  --limit 3
```

agent 应该先说明最推荐的一条，再列出其他选项，并附上 OnePilot 站内活动 URL。`recommend` 返回里会包含 `requiredClosingReminder`，agent 必须把它作为每次活动推荐回答的最后一句。

如果用户问“哪一场更值得去”“帮我判断要不要报名”，agent 可以用推荐结果里的 `detailToken` 调用 `event-context` 获取更完整的活动上下文。

## 精选推荐优先

当用户不是在找具体活动，而是在找仍存在于 `references/featured-recommendations.json` 的精选资源类型时，agent 可以先查 OnePilot 精选推荐：

```bash
node ./scripts/onepilot-agent.mjs featured search --query "我想找工位或 OPC 社区" --limit 3
```

如果命中结果，先推荐 OnePilot 精选项，再补充其他建议。不要从 OnePilot CLI 包推荐已移除的非活动资源。

## 当前限额

这些限额按 OnePilot 账号计算，同一账号下不同设备或 agent 共享：

- 活动推荐：每天 5 次请求。
- 单次推荐结果：最多 3 条活动。
- 活动上下文 / 报名协作上下文：每天 20 次。
- 站内报名提交尝试：每天 20 次。
- 网站绑定码：每天最多生成 5 个。
- 本地订阅：第一版只支持 `daily`，最多每天触发一次。

其他限制：

- 邮箱验证码有效期 600 秒；邮件发送可能被 Supabase Auth 限流，但 OnePilot 没有单独写死每日邮箱验证码次数。
- 云端记忆没有每日次数限制，但只支持 `preferences`、`availability`、`application_profile`、`answer_examples` 四类，每个账号每类一条。
- 反馈没有每日次数限制，但必须引用当前绑定 agent 实际拿到过的推荐 ID。
- 问题反馈没有每日次数限制，但不能上传 token、验证码、完整私聊内容或未脱敏截图。

活动推荐次数用完时，agent 应提示：

```text
今天的 OnePilot 活动推荐次数已经用完（每天 5 次）。你可以明天再让我推荐，或者直接打开 OnePilot 网站查看活动列表。
```

## 画像学习反馈

当用户对推荐活动有明确反应时，agent 可以把这个信号记录到 OnePilot 云端，例如：感兴趣、已报名、不适合、保存、分享、选择某一条。

```bash
node ./scripts/onepilot-agent.mjs feedback record \
  --recommendation-id rec_xxx \
  --action interested \
  --position 0 \
  --profile-json '{"topics":["AI agent"],"stage":"early founder"}' \
  --target-profile-json '{"wantsToMeet":["AI 产品创业者","投资人"]}'
```

这不会替代用户记忆；它用于长期分析“什么画像的用户喜欢报名什么活动”，后续可以反过来优化推荐排序。

如果用户说要报名、已经报名或已经提交，并且 agent 能连接到用户的日程工具，agent 要先问用户是否需要把活动加入日程。用户确认后再创建日程；如果时间地点不完整，先用 `event-context` 补充或追问用户。没有日程工具时，agent 可以给一段可复制的日程信息。

## 问题反馈

如果 OnePilot CLI 使用中出现 bug，用户可以在 OnePilot 网站的“Agent 与账号”面板提交反馈。agent 自己发现异常时，应先询问用户是否同意上报脱敏问题：

```bash
node ./scripts/onepilot-agent.mjs issue report \
  --title "推荐链接打开空白" \
  --description "用户打开推荐活动的 OnePilot 站内链接后页面空白。" \
  --command "recommend --limit 3" \
  --error-code "blank_event_url"
```

不要上报 agent token、邮箱验证码、完整私人对话、截图、日程内容或报名答案。

## 本地订阅

第一版不由 OnePilot 云端主动发邮件。订阅由本地 agent 负责调度和发送，OnePilot 只提供推荐结果。

设置订阅：

```bash
node ./scripts/onepilot-agent.mjs subscription set \
  --query "每天最多一次提醒我适合 AI agent 创业者的活动" \
  --topics "AI agent,创业"
```

本地定时器或 agent 唤醒后，先判断今天是否该推：

```bash
node ./scripts/onepilot-agent.mjs subscription due
```

只有 `due: true` 时，再获取推荐：

```bash
node ./scripts/onepilot-agent.mjs subscription run-now
```

`run-now` 会优先返回匹配活动；如果活动不足 3 条，会额外返回 `featuredFallback` 精选资源。agent 写邮件时不要硬凑活动：

- 有 3 条活动：正常推荐 3 条，并说明最推荐哪条。
- 只有 1-2 条活动：只推真实活动，可以补充精选资源。
- 没有活动：说明今天没有找到强匹配活动，再用精选资源补位。
- 使用精选资源时必须带 `url` 和 `mustMention`。

如果用户选择邮件提醒，agent 应该使用用户授权的邮箱工具发送推荐摘要。邮件末尾固定加上：

```text
--
OnePilot 官网：https://onepilot.zeabur.app
小红书：@One Pilot
```

## 报名协作

如果用户已经给了 OnePilot 站内活动链接，agent 可以直接读取站内报名表字段，不需要先调用推荐接口获取 `detailToken`：

```bash
node ./scripts/onepilot-agent.mjs application form \
  --event-url "https://onepilot.zeabur.app/events/EVENT_ID"
```

如果 agent 已经知道 OnePilot 活动 id，也可以直接用：

```bash
node ./scripts/onepilot-agent.mjs application form \
  --event-id EVENT_ID
```

如果活动来自推荐结果，agent 可以用推荐结果里的 `detailToken` 读取报名表字段：

```bash
node ./scripts/onepilot-agent.mjs application form \
  --detail-token dt_xxx
```

agent 根据返回的字段和已保存记忆生成报名草稿。正式提交前必须把草稿展示给用户确认；用户确认后再提交：

```bash
printf '%s' '{"name":"张三","company":"OnePilot","jobTitle":"创始人","wechat":"wx_123"}' | \
node ./scripts/onepilot-agent.mjs application submit \
  --event-id EVENT_ID \
  --form-version FORM_VERSION \
  --answers-json-stdin
```

提交成功后，CLI 返回 `nextStep`。如果里面有 `groupQrImageUrl`，agent 应优先下载成本地图片并直接发给用户：

```bash
node ./scripts/onepilot-agent.mjs application qr \
  --url GROUP_QR_IMAGE_URL
```

命令会返回 `imagePath`。支持发图的渠道就把这个本地图片上传/内嵌发送，支持 Markdown 图片的渠道就渲染为图片；只有当前渠道不能发图或渲染图片时，才退回发送二维码链接。如果没有二维码，就使用 `nextStep.message` 告诉用户后续等待活动方通知。

如果 `application form` 返回不支持站内直报名，agent 应直接使用这次返回的活动信息和记忆，结合用户提供的截图/OCR/问题文本生成草稿。如果这次是用 `--detail-token` 拉取的，不要再用同一个 `detailToken` 调 `application prepare`，因为它已经被 `application form` 消耗。

外部报名表不由 OnePilot 自动提交。用户一开始就提供报名问题文本，或者让 agent 从截图 OCR 出问题后，可以运行：

```bash
node ./scripts/onepilot-agent.mjs application prepare \
  --detail-token dt_xxx \
  --questions "报名问题文本"
```

CLI 会返回活动上下文、已保存记忆和报名问题。最终答案由本地 agent 生成。缺少真实个人信息时，agent 应该追问用户，不要编造；外部表单答案由用户自行复制粘贴。

用户确认报名完成后，如果 agent 有日程工具，应询问是否添加到日程；不能静默创建、修改或删除用户日程。

## 适配说明

OnePilot 只维护一套核心 CLI，并通过 Skill、Extension 等薄适配接入不同平台，不复制业务逻辑。

平台差异只放在 `references/adapters.md`，包括 Codex、Claude Code、OpenClaw、Gemini CLI、Qwen Code、opencode、Trae、WorkBuddy 等 agent 的安装方式、命令权限、邮箱工具和本地调度差异。

`qwen-extension.json` 和 `.claude-plugin/plugin.json` 是薄包装元数据，方便后续上架对应平台；第一版不把它们做成独立业务实现。

## 本地 token

CLI 会把本地 agent token 保存到：

```text
~/.config/onepilot/agent.json
```

不要把这个文件复制、粘贴、提交到 GitHub 或发给别人。

## 当前状态

`v0.1.0-alpha` 是早期测试版本。后续可能提供 MCP 版本，让支持原生工具调用的平台更容易接入。
