# 日程日历工作台

[English](README.md)

导入 ICS 日历，展开重复事件、查看日程冲突，创建会议文件并按版本同步 CalDAV。

## 功能

导入 ICS 日历，展开重复事件、查看日程冲突，创建会议文件并按版本同步 CalDAV。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
读取我上传的calendar.ics，列出下周日程，按北京时间显示。
```

```text
检查这份日历未来两周有没有时间冲突，列出重叠事件。
```

```text
生成一个日历文件：下周一起每周一上午10点开30分钟例会，共四次。
```

## 运行要求

Python 3.10+; icalendar>=6.3,<7, recurring-ical-events>=3.8,<4, tzdata>=2025.1

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-calendar-desk
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-calendar-desk)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-calendar-desk
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-calendar-desk)。下载仓库 ZIP，将 `skills/mochi-calendar-desk` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
