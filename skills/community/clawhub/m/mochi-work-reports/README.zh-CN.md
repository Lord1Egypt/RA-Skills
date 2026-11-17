# 工作日报与周报

[English](README.md)

导入工作记录、更新进度并保留修改历史，按日期导出日报周报和明细。

## 实际功能

导入工作记录、更新进度并保留修改历史，按日期导出日报周报和明细。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
根据我提供的本周工作记录，整理已完成、进行中和下周计划，保存周报。
```

```text
合并这几天的工作记录，标出没有负责人或截止日期的事项。
```

```text
把上周和本周的记录对照，列出新增、完成和延期事项，导出报告。
```

## 导出结果

work-report.md / work-records.csv

文件保存在当前助手工作区，返回路径和 SHA256；记录与历史导出保留。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+、当前助手工作区的读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-work-reports
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-work-reports)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-work-reports
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-work-reports)。下载仓库 ZIP，将 `skills/mochi-work-reports` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
