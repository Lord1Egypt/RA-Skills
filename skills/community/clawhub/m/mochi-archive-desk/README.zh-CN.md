# 压缩归档与完整性工具箱

[English](README.md)

检查 ZIP/TAR 内容，安全解压到新目录，按指定文件生成 ZIP 并输出逐文件校验值。

## 功能

检查 ZIP/TAR 内容，安全解压到新目录，按指定文件生成 ZIP 并输出逐文件校验值。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
检查我上传的 backup.zip，列出文件、大小和异常路径，先不要解压。
```

```text
把 backup.zip 解压到一个新目录，生成文件清单和 SHA256 校验值。
```

```text
把我指定的三份文件打成 documents.zip，检查压缩包完整性。
```

## 运行要求

Python 3.10+; 标准库

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-archive-desk
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-archive-desk)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-archive-desk
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-archive-desk)。下载仓库 ZIP，将 `skills/mochi-archive-desk` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
