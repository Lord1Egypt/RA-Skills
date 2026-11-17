# Git 项目检查与快照

[English](README.md)

查看指定 Git 项目的改动和提交记录，区分暂存内容，生成带校验清单的私有工作快照。

## 功能

查看指定 Git 项目的改动和提交记录，区分暂存内容，生成带校验清单的私有工作快照。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
检查我指定的 Git 项目，分别列出已暂存、未暂存和未跟踪文件。
```

```text
查看这个项目最近十次提交，整理改动摘要。
```

```text
为这个项目创建私有工作快照，包含我选定的未跟踪文件，并生成校验清单。
```

## 运行要求

Python 3.10+; 标准库; Git CLI

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-git-desk
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-git-desk)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-git-desk
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-git-desk)。下载仓库 ZIP，将 `skills/mochi-git-desk` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
