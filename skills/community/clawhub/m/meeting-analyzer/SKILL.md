---
slug: meeting-analyzer-user-c7fbb74e
displayName: Meeting Analyzer
version: 1.0.0
summary: 输入腾讯会议 / 飞书会议链接，输出结构化 JSON、drawio 概要图、Markdown 与 HTML 会议报告
license: MIT
icon: assets/logo/color/logo-256.svg
iconMono: assets/logo/mono/logo-256.svg
brandColor: "#2563EB"
author: samonysh
homepage: https://github.com/samonysh/meeting-analyzer
repository: https://github.com/samonysh/meeting-analyzer
keywords: [meeting, transcript, tencent-meeting, feishu, lark, drawio, llm, skillhub]
name: "meeting-analyzer"
description: "会议逐字稿精细化分析工具：输入腾讯会议或飞书会议链接，输出结构化分析 JSON（阶段/关键点/决策/待办/参与者画像）、drawio 概要图与 Markdown/HTML 报告。当用户要分析会议逐字稿、生成会议纪要可视化、提取会议关键内容截图、制作会议总结网页时使用。"
tags: [会议, 逐字稿, 分析, drawio, 腾讯会议, 飞书会议, 效率]
---

# 会议逐字稿精细化分析 (Meeting Analyzer)

将一场会议的逐字稿，转化为结构化的、可供 LLM/可视化直接消费的分析档案。支持腾讯会议（tmeet CLI）与飞书会议（lark-cli vc）两条数据来源，输入为一个会议链接。

## 何时调用本技能

当用户出现以下任一意图时调用：

- "分析这场会议"、"帮我整理这场会议的逐字稿"、"这个会议讲了什么"
- "生成会议概要图 / 会议可视化 / drawio 会议图"
- "做一份会议纪要网页 / HTML 报告 / Markdown 报告"
- 提供了腾讯会议链接（meeting.tencent.com / wemeet.qq.com / 9-12 位会议号）或飞书链接（*.feishu.cn / *.larksuite.com 的 minutes/meetings 路径）
- 需要从会议逐字稿中提取关键观点、决策、待办、未决问题

## 前置依赖

| 依赖 | 用途 | 安装 |
|---|---|---|
| Node.js ≥ 18 | 运行本工具 | — |
| `tmeet` CLI | 腾讯会议逐字稿（可选） | `npm i -g @tencentcloud/tmeet@latest` 然后 `tmeet auth login` |
| `lark-cli` | 飞书会议逐字稿（可选） | 参见 `lark-shared` 完成初始化与授权 |
| `ffmpeg` | 关键截图抽取（可选） | 系统安装 |

未安装对应 CLI 时，对那条链路会自动给出明确提示；若仅需测试，可使用 `--mock` 模式。

## 输入

- **会议链接**（必填）：腾讯会议链接 / 飞书会议链接 / 妙记链接 / 9-12 位会议号
- 可选：会议录制视频本地路径（`--video`，用于抽取关键截图）

## 输出

输出到指定目录（默认 `./output`），文件名按会议标题自动命名：

| 文件 | 内容 |
|---|---|
| `<title>.json` | 完整结构化分析数据（Meeting 完整结构，可直接喂给 LLM） |
| `<title>.drawio` | drawio 概要图：会议标题 + 阶段流 + 关键观点/决策/待办节点 + 参会人面板 |
| `<title>.md` | Markdown 报告：概要 + 概要图引用 + 关键截图 + 阶段详情 + 决策/待办汇总 |
| `<title>.html` | 自包含 HTML 网页（内联 CSS，可独立分享） |
| `snapshots/*.jpg` | 关键时刻截图（启用 `--video` 时） |

## 数据结构（核心）

```
Meeting
 ├─ metadata          会议元信息
 ├─ segments[]        原始逐字稿片段
 ├─ utterances[]      合并后的完整发言（含意图/情绪/实体/关键词）
 ├─ stages[]          阶段（按时间+话题切分，含摘要/情绪曲线）
 ├─ topics[]          主题（跨阶段的语义聚合）
 ├─ key_points[]      关键观点（带重要性评分与证据回指）
 ├─ decisions[]       决策
 ├─ action_items[]    待办
 ├─ open_questions[]  未决问题
 ├─ interactions[]   互动关系（问答/反对/追问）
 ├─ snapshots[]       关键截图（绑定到阶段/关键点/决策）
 └─ summary          整体摘要（一句话/执行摘要/排名/集中度）
```

所有实体通过 ID 互相回指，序列化为 JSON 后可按需切片喂给 LLM（详见项目 `scripts/src/schemas/meeting.ts`）。

## 使用方式

```bash
# 1. 安装依赖（在项目目录）
npm install

# 2. 运行分析（默认：使用真实 CLI）
npx tsx scripts/src/cli.ts analyze "https://meeting.tencent.com/..."

# 3. 携带视频做截图
npx tsx scripts/src/cli.ts analyze "https://xxx.feishu.cn/minutes/..." --video ./recording.mp4 -o ./output

# 4. 仅检测链接平台
npx tsx scripts/src/cli.ts detect "https://meeting.tencent.com/..."

# 5. Mock 模式（无 CLI 时测试）
npx tsx scripts/src/cli.ts analyze mock --mock --mock-path assets/examples/sample-tencent.json
```

## 链路说明

- **腾讯会议**：链接 → `tmeet meeting get` 取 meeting_id → `tmeet record list` 取 record_file_id → `tmeet record transcript-paragraphs` 获取带时间戳/说话人的逐字稿；`tmeet record address` 取录制 URL。
- **飞书会议**：链接 → `lark-cli vc +detail` 取 note_id / minute_token → 优先 `minutes +detail --transcript`，备选 `note +detail` → `docs +fetch` 获取逐字稿。

## 投喂 LLM 的推荐切片

| 任务 | 投喂层 |
|---|---|
| 快速理解全貌 | `summary` + 每个 `stage.summary` |
| 提取重点 | `key_points[]` + `decisions[]` + `action_items[]` |
| 分析某人表现 | 对应 `participants[*]` + 其 `utterances` |
| 追溯某结论原话 | 由 `decision_id` → `supporting_utterances` 回指原文 |

## 限制与注意

- 逐字稿质量依赖平台 ASR；若置信度低，关键点抽取可能漏检。
- 截图依赖会议已开启云录制，且录制画面含共享内容。
- 未配置 LLM API Key 时自动使用规则启发式分析；配置后可增强摘要质量。
- 会议内容涉及隐私，产物应按企业合规要求存储与分享。
