# RSS 订阅与阅读中心

[English](README.md)

订阅 RSS/Atom，导入导出 OPML、保存已读状态、搜索历史条目，并生成新内容提醒。

## 功能

订阅 RSS/Atom，导入导出 OPML、保存已读状态、搜索历史条目，并生成新内容提醒。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
添加我提供的RSS地址，建立首次基线，先不要把历史文章当成新消息。
```

```text
导入这份OPML订阅清单，抓取更新并列出未读文章和来源。
```

```text
搜索已保存文章中包含OpenClaw的内容，把我看完的这些条目标为已读。
```

## 运行要求

Python 3.10+; feedparser>=6.0.12,<7

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-feed-hub
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-feed-hub)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-feed-hub
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-feed-hub)。下载仓库 ZIP，将 `skills/mochi-feed-hub` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
