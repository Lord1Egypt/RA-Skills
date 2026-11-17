# 多邮箱邮件工作台

[English](README.md)

接入 IMAP/SMTP/POP3 邮箱，收信搜索、处理附件、准备并发送邮件，保存新邮件提醒状态。

## 功能

接入 IMAP/SMTP/POP3 邮箱，收信搜索、处理附件、准备并发送邮件，保存新邮件提醒状态。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
使用已配置的工作邮箱，读取最近10封邮件，列出发件人、主题和时间。
```

```text
搜索工作邮箱里本月主题含发票的邮件，把我选中的附件保存到新目录。
```

```text
给我指定的收件人准备一封会议确认邮件，附上我提供的文件，先展示草稿，等我确认再发送。
```

## 运行要求

Python 3.10+; 标准库

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-email-desk
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-email-desk)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-email-desk
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-email-desk)。下载仓库 ZIP，将 `skills/mochi-email-desk` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
