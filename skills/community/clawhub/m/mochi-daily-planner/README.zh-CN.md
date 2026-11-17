# 每日计划与复盘

[English](README.md)

按优先级排时间块，保留休息和超时待办，修改计划并导出日程文件。

## 实际功能

按优先级排时间块，保留休息和超时待办，修改计划并导出日程文件。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
今天9点到12点有三小时：写报告90分钟、回邮件30分钟、整理文件30分钟，安排休息并保存计划。
```

```text
下午临时增加一个一小时会议，调整今天的计划，把放不下的任务列出来。
```

```text
根据我提供的实际完成情况复盘今天，导出明天的时间块清单。
```

## 导出结果

daily-plan.md / time-blocks.csv

文件保存在当前助手工作区，返回路径和 SHA256；记录与历史导出保留。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+、当前助手工作区的读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-daily-planner
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-daily-planner)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-daily-planner
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-daily-planner)。下载仓库 ZIP，将 `skills/mochi-daily-planner` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
