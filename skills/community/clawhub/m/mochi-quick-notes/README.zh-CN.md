# 随手记与待办

[English](README.md)

记录、修改和检索笔记待办，按标签与日期筛选，导出 Markdown 和 CSV。

## 实际功能

记录、修改和检索笔记待办，按标签与日期筛选，导出 Markdown 和 CSV。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
记一条待办：周末买滤芯，型号ABC-200，标签家务。
```

```text
查找最近一个月带装修标签的笔记，按日期列出。
```

```text
把买滤芯标记为完成，将剩余待办导出为Markdown和CSV。
```

## 导出结果

notes.md / notes.csv

文件保存在当前助手工作区，返回路径和 SHA256；记录与历史导出保留。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+、当前助手工作区的读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-quick-notes
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-quick-notes)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-quick-notes
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-quick-notes)。下载仓库 ZIP，将 `skills/mochi-quick-notes` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
