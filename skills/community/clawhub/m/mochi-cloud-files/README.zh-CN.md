# WebDAV 网盘工作台

[English](README.md)

连接 WebDAV 网盘，查看文件、比较目录、上传下载，按文件版本处理冲突并生成校验值。

## 功能

连接 WebDAV 网盘，查看文件、比较目录、上传下载，按文件版本处理冲突并生成校验值。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
使用已配置的WebDAV账户，列出 /Documents 下的文件和大小。
```

```text
比较本地reports目录和网盘Reports目录，先生成上传方案，标出冲突。
```

```text
把我选定的网盘文件下载到新目录，检查版本变化并生成SHA256校验值。
```

## 运行要求

Python 3.10+; 标准库

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-cloud-files
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-cloud-files)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-cloud-files
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-cloud-files)。下载仓库 ZIP，将 `skills/mochi-cloud-files` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
