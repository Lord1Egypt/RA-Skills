# 重要日子与节日管家

[English](README.md)

管理公历农历生日、纪念日和年度节假日，设置提前提醒、时区与闰日规则，导出日历。

## 功能

管理公历农历生日、纪念日和年度节假日，设置提前提醒、时区与闰日规则，导出日历。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
记录妈妈的农历八月十五生日，按北京时间提前7天和当天提醒，确认任务计划和投递渠道。
```

```text
记录我们的结婚纪念日为每年6月18日，列出未来90天的重要日子。
```

```text
导入我提供的年度官方节假日表，区分放假和补班，导出ICS日历。
```

## 运行要求

Python 3.10+; lunar-python==1.4.8, icalendar>=6.3,<7, tzdata>=2025.1

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-important-dates
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-important-dates)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-important-dates
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-important-dates)。下载仓库 ZIP，将 `skills/mochi-important-dates` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
