# 我的每日简报

[English](README.md)

按主题整理公开资讯，生成附来源链接和日期的本地简报。

## 功能

从 OpenAI News、Google AI、GitHub Changelog 等公开 RSS/Atom 订阅源收集资讯，按主题、日期和时区筛选、去重，再用 OpenClaw 已连接的模型整理成中文或英文简报。

简报以 Markdown 保存在 `daily-briefs/`，附原文链接、发布日期和来源信息。支持最近 1—30 个日历日、最多 20 条，也可配置自己的公开订阅源。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
从已支持的RSS来源整理过去24小时的AI资讯，按北京时间筛选并去重，附原文链接。
```

```text
整理过去七天的GitHub Changelog更新，按日期列出重点并保存Markdown。
```

```text
从我提供的RSS订阅源制作今天的中文简报，标明筛选时段和每条发布时间。
```

把主题改成你关注的方向，并在 `references/options.md` 中配置对应订阅源。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。访问所选公开 HTTPS 来源的网络权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-daily-brief
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-daily-brief)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-daily-brief
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-daily-brief)。下载仓库 ZIP，将 `skills/mochi-daily-brief` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

## 补充示例与操作要点

- Add a short **“值得关注 / Why it matters”** section when useful. Label interpretation or uncertainty explicitly and connect it to a cited item. Do not infer technical specifications, prices, availability or outcomes absent from the evidence.

- “用我的每日简报，整理今天的 AI 和开源资讯，中文 5 条，上海时区。”

- “今天没有内容就告诉我，不要拿旧新闻补齐。”
