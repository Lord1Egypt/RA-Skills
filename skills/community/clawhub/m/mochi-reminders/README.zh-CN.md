# 提醒与定时任务

[English](README.md)

检查定时任务、记录真实投递回执，并导出可导入日历的 ICS 文件。

## 实际功能

检查定时任务、记录真实投递回执，并导出可导入日历的 ICS 文件。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
每周五北京时间20点提醒我交周报，发到当前聊天；创建后告诉我任务编号和下次执行时间。
```

```text
检查我已有的提醒任务，列出执行时间和可查到的投递回执。
```

```text
把明天15点的复诊提醒导出为ICS文件，方便我导入手机日历。
```

## 导出结果

reminder.ics / receipt.md

文件保存在当前助手工作区，返回路径和 SHA256；记录与历史导出保留。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+、当前助手工作区的读写权限。OpenClaw 定时任务工具、运行中的 Gateway、当前聊天渠道的投递能力。首次使用会核对可用工具及账号路由。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-reminders
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-reminders)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-reminders
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-reminders)。下载仓库 ZIP，将 `skills/mochi-reminders` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
