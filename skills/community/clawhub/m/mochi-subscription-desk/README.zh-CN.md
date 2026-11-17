# 订阅续费与账单管家

[English](README.md)

管理软件、会员和服务的续费周期，计算取消期限、按币种预测开销并提醒到期。

## 功能

管理软件、会员和服务的续费周期，计算取消期限、按币种预测开销并提醒到期。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
记录一个订阅：网盘每月15元，每月20日续费，需提前3天取消。
```

```text
列出未来30天要续费的服务，按人民币和美元分别汇总金额。
```

```text
把这个订阅设为已取消，重新生成本月续费清单和提醒记录。
```

## 运行要求

Python 3.10+; 标准库

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-subscription-desk
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-subscription-desk)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-subscription-desk
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-subscription-desk)。下载仓库 ZIP，将 `skills/mochi-subscription-desk` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
