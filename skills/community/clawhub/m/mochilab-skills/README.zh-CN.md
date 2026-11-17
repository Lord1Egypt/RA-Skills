# MochiLab Skills 助手

[English](README.md)

在对话中查找、安装和维护 MochiLab Skills，检查依赖、运行测试，保留配置并支持版本回退。

## 功能

查找并安装 MochiLab Skills，检查文件完整性、运行环境和依赖。支持选择 Python 等运行程序、运行安装包自带测试、检查更新和回退旧版本。配置保存在安装目录之外，更新时保留；本地修改过的文件会提示处理。

## 用法示例

安装并连接助手后，把下面任意一条发给 AI。

```text
安装 MochiLab 翻译校对，检查依赖并运行自带测试，告诉我版本、安装位置和测试结果。
```

```text
检查我安装的 MochiLab Skills 有没有更新，先列出版本变化；等我选好，再更新并测试。
```

```text
这个 MochiLab Skill 运行失败了，帮我检查配置和依赖，保留我的文件；如果需要回退，先列出可用的旧版本。
```

## 如何使用

首次按[接入教程](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)连接账户，之后在当前助手对话中提出需求。新增 Skill 后开启新对话。

测试报告会区分自带测试通过、仅完成语法检查、缺少依赖和测试失败。邮箱、网盘及定时提醒还需按各自要求完成账户配置和实际任务测试。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+、HTTPS 网络和工作区写入权限。

## 安装与开始使用

### MochiLab Skills 助手

[按接入教程安装并连接账户](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)。

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochilab-skills)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochilab-skills
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochilab-skills)。下载仓库 ZIP，将 `skills/mochilab-skills` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。
通过 ClawHub 或 GitHub 安装后，也需[连接 MochiLab 账户](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

