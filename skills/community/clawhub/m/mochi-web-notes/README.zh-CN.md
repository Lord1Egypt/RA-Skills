# 网页资料笔记

[English](README.md)

阅读指定网页，整理带来源和日期的本地资料笔记。

## 功能

读取你指定的 1—3 个公开 HTTPS 网页，提取静态正文、来源日期和摘录，再用已有模型生成带引用的 Markdown 笔记，适合比较几篇文章或整理主题资料。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
阅读我提供的两个公开网页，比较主要观点，标出来源链接和日期。
```

```text
把这三个网页里关于安装要求的原文整理成资料笔记，附摘录。
```

```text
根据我提供的网页资料整理中文摘要，保存Markdown笔记和来源记录。
```

## 高级用法：在终端手动运行

下面是开发者手动运行命令。在安装 OpenClaw 的电脑或服务器终端执行；日常使用直接发送上面的对话示例即可。

先把命令中的占位名称换成实际路径：

- `SKILL_DIRECTORY`：已安装的这个Skill文件夹。
- `WORKSPACE`：助手工作区路径。
- `EVIDENCE_FILE`：上一步生成的证据文件路径。

在工作目录创建 `urls.json`，填入网址数组，然后采集：

```text
node "SKILL_DIRECTORY/scripts/web-notes.mjs" collect --workspace "WORKSPACE" --urls "WORKSPACE/urls.json" --language zh-CN
```

让 OpenClaw 根据返回材料写入草稿，再保存：

```text
node "SKILL_DIRECTORY/scripts/web-notes.mjs" save --workspace "WORKSPACE" --evidence "EVIDENCE_FILE"
```

将占位路径替换为实际路径；成品保存在工作目录的 `web-notes/`。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。访问所选公开 HTTPS 来源的网络权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-web-notes
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-web-notes)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-web-notes
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-web-notes)。下载仓库 ZIP，将 `skills/mochi-web-notes` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
