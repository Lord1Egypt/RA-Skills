# 菜谱与买菜清单

[English](README.md)

保存忌口与库存，按人数换算食材，生成菜谱和买菜清单文件。

## 实际功能

保存忌口与库存，按人数换算食材，生成菜谱和买菜清单文件。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
保存我的饮食偏好：两个人、不吃花生；按我提供的库存安排三天晚餐。
```

```text
把这份两人菜谱换算为四人份，列出每种食材用量。
```

```text
根据本周菜谱合并买菜清单，扣除现有库存，导出CSV。
```

## 导出结果

meal-plan.md / groceries.csv

文件保存在当前助手工作区，返回路径和 SHA256；记录与历史导出保留。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+、当前助手工作区的读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-meal-planner
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-meal-planner)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-meal-planner
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-meal-planner)。下载仓库 ZIP，将 `skills/mochi-meal-planner` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
