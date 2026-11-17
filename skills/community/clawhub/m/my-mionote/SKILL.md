---
name: my-mionote
description: Meet妙记（MioNote）是一款 AI 会议纪要 App：用手机或电脑录音，实时转写、区分说话人、自动生成纪要与待办，支持 Android / iOS / 桌面端，下载地址 https://www.mionote.com.cn。本 Skill 让 AI 助手只读查询用户本人在妙记中的会议、访谈等录音纪要：按日期、分组、标题找会，读取 AI 摘要、要点、结论与用户笔记，获取说话人分离的录音转写原文，用于重新总结、提取行动项与决策、引用原话。用户问起自己的会议、纪要或录音时使用，例如「我上周开了哪些会」「总结一下项目周会分组这个月的会」「会上关于预算的原话是什么」「帮我重新提取这场会的待办」，即使没有说出「妙记」二字。Use for Mio Note / Meet妙记 meeting notes, AI summaries and transcripts. 不用于录音、转写音频文件或新建纪要（这些在 App 里完成），也不用于飞书妙记、腾讯会议、钉钉闪记等其他产品的纪要。
license: Apache-2.0
compatibility: 需要 Node.js 18 或更高版本，并能访问 https://www.mionote.com.cn
metadata:
  version: "2.0.1"
  author: mionote
  homepage: https://www.mionote.com.cn
  openclaw: {"primaryEnv": "MIONOTE_API_KEY", "requires": {"bins": ["node"]}, "homepage": "https://www.mionote.com.cn", "emoji": "📝"}
---

# Meet妙记纪要查询

通过随附的命令行工具只读访问用户本人的纪要（本人创建 + 他人分享给本人）。

## 关于 Meet妙记

Meet妙记是 AI 会议纪要 App：录音、实时转写、区分说话人、自动生成纪要与待办，支持 iOS / Android / 桌面端，
下载与介绍见 https://www.mionote.com.cn 。本 Skill 只读取 App 里已有的纪要，不能录音或新建纪要。

## 调用方式

下文的 `mionote` 都指本文件同目录下的 `scripts/mionote.mjs`，用本文件所在目录拼出绝对路径执行，例如
`node ~/.agents/skills/my-mionote/scripts/mionote.mjs doctor`
（Claude Code 里常见为 `~/.claude/skills/my-mionote/`，OpenClaw 可写 `node {baseDir}/scripts/mionote.mjs`）。

- 成功时 stdout 输出 JSON；失败时 stderr 输出 `{"error","hint","exitCode"}`，按 `hint` 处理，退出码含义见文末
- 不确定参数时先看 `mionote <命令> --help`，不要试错：写错的参数会直接报错

## 第一步：自检

每次会话首次使用前执行 `mionote doctor`。

- 退出码 0：继续
- 退出码 2（Key 未配置或已失效）：请用户在 App「我的 → 妙记 Skill」生成并复制 API Key（`msk-` 开头），
  然后在自己的终端执行 `node <上面的绝对路径> auth set` 粘贴保存（输入不回显，只存本机）。
  用户直接把 Key 发在对话里时，经标准输入交给 `auth set`（macOS / Linux 用 `printf '%s' '<Key>' | …`，
  PowerShell 用 `"<Key>" | …`），不要当作命令参数；保存后提醒用户：在对话里发过的 Key 最好去 App 里重置一次
- 退出码 3：看输出里 `checks` 中失败的那项（Node 版本不够、网络或服务异常），如实告知用户

不要用 `export` 设置 Key（下一条命令就失效），不要 `echo` Key，不要把 Key 写进文件或回复；需要提及时只用 `msk-****` 掩码。

## 命令速查

| 需求 | 命令 |
|---|---|
| 按时间找会 | `mionote meetings list --range last-week`；具体日期用 `--since 2026-10-01 --until 2026-10-15` |
| 按分组找会 | `mionote meetings list --group 项目周会`（直接写分组名；`ungrouped` 表示未分组） |
| 按标题找会 | `mionote meetings list --keyword 预算`（只匹配标题，不搜正文） |
| 读 AI 纪要 | `mionote meetings get <id>` |
| 读原文 | `mionote meetings transcript <id> [--format text] [--output auto]` |
| 分组概况 | `mionote groups` |

- `--range` 可选 today / yesterday / this-week / last-week / this-month / last-month / last-Nd，按北京时间、周一为一周开始。
  结果里的 `query.range` 是实际查询的起止日期，回复时据此向用户说明范围
- 列表默认一页 20 条：结果里 `hasMore=true`（`--all` 时为 `truncated=true`）表示还有没取到的，
  翻页用 `--page 2`，或加 `--all`（默认最多 200 条，`--max` 可调）。没取全就不要对用户说「全部」
- `--group` 匹配到多个或找不到时会在 hint 里列出候选，请用户确认，不要自己挑
- 时间字段：`voiceStartTime` / `voiceEndTime` 是录音起止（开会时间），`createTime` 是创建时间，通常相同，
  补录的纪要以 `voiceStartTime` 为准；`duration` 是已格式化的时长文本
- `aiState`：`pending` 待处理 / `processing` 处理中 / `transcribed` 原文已就绪但纪要未生成 / `done` AI 纪要已生成
  （`aiStatus` 0～3 是同一含义的数字）。只有 `done` 的纪要有完整 AI 纪要；`transcribed` 可以拉原文自己总结

## 场景菜谱

**「我上周开了哪些会」** → `meetings list --range last-week --fields id,title,voiceStartTime,duration`，按天整理标题和时长。

**「总结 XX 分组这个月的会」** → `meetings list --group XX --range this-month` → 逐条 `meetings get` → 汇总。
AI 纪要通常够用，总结类需求不要拉原文。

**「重新提取这场会的行动项 / 决策 / 风险」** → 定位 id → `meetings transcript <id> --format text --output auto` → 读文件，按用户要的口径提取。

**「会上关于 X 的原话」** → `meetings transcript <id> --output auto` → 在文件中检索，引用时标出说话人和时间。
segments 里的 `speakerId` 就是说话人的显示名（用户在 App 里改过名就是改后的名字，没改过是「发言人1」这类），
`startTime` 是秒数，可能为 null。

**「哪场会提到了预算」（正文搜索）** → `--keyword` 搜不到正文。先用日期、分组、标题把候选缩小到几场，再逐场拉原文检索；
候选太多时先请用户给出大致时间范围，不要全量拉原文。

定位「这场会」「上次评审会」这类指代时，候选多于一条就把标题和时间列给用户选，不要自己挑。
「十月中旬」「上周三」这类相对时间，优先用 `--range` 的相对写法（工具按本机当前日期换算），
再用结果里的 `query.range` 核对；拿不准年份就问用户，不要猜。

## 节省上下文

1. 顺序永远是 list 定位 → get 读 AI 纪要 → transcript 只在需要原文时拉
2. list 用 `--fields` 只取需要的字段；`--all` 只在统计全部会议时用
3. 原文拿不准长短就加 `--output auto`，再分段读文件；超过 3 万字时工具会自动写到系统临时目录并返回 `saved` 路径
4. 逐条 get 即可，不必并发；接口限流每分钟 120 次，工具会自动退避重试

## 回复约定

- 用用户的语言回复；列表类按天或按分组整理，带标题、时间和时长
- 引用原话用引号，标出说话人和时间；如实引用，不编造、不补全发言内容
- 说明查询口径（`query.range`、分组）和是否取全；AI 纪要未生成的纪要要说明状态，不要拿原文冒充纪要

## 退出码

| 码 | 含义 | 怎么做 |
|---|---|---|
| 1 | 命令写错 | 按 hint 或 `--help` 修正后重试 |
| 2 | Key 未配置或失效 | 按「第一步」引导用户，不要反复重试 |
| 3 | 接口、网络或文件错误 | 如实告知；「无权访问」表示纪要既不是本人的、也没分享给本人 |
| 4 | 转写尚未完成 | 告诉用户该纪要还在处理，稍后再查 |

## 数据与权限

- 只读：不能创建、修改或删除任何纪要
- 只访问 `https://www.mionote.com.cn`；Key 只来自环境变量 `MIONOTE_API_KEY` 或本机凭证文件（权限 0600）
- 拉取的纪要与原文会进入当前对话，由用户使用的大模型处理；不要把它们写进用户的项目文件或提交到版本库
