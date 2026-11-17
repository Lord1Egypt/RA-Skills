# 学习卡片与原文验证

[English](README.md)

把笔记变成附原文依据的问答卡片，导出 Markdown 和 Anki TSV。

## 功能

将你提供的笔记分段，用已有模型生成问答卡片。脚本检查原文引用、重复问题和卡片数量，导出 Markdown、Anki TSV 与本地复习清单。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
把我提供的笔记做成8张中文问答卡，每张附原文依据。
```

```text
检查这些卡片是否有重复问题或找不到依据的答案，列出要修改的卡片。
```

```text
把确认好的卡片导出为Markdown和Anki TSV，并生成复习清单。
```

## 高级用法：在终端手动运行

下面是开发者手动运行命令。在安装 OpenClaw 的电脑或服务器终端执行；日常使用直接发送上面的对话示例即可。

先把命令中的占位名称换成实际路径：

- `SKILL_DIRECTORY`：已安装的这个Skill文件夹。
- `WORKSPACE`：助手工作区路径。
- `EVIDENCE_FILE`：上一步生成的证据文件路径。

先准备材料：

```text
node "SKILL_DIRECTORY/scripts/learning-cards.mjs" prepare --workspace "WORKSPACE" --source "WORKSPACE/source.md" --language zh-CN --max-cards 8
```

OpenClaw 填好返回的卡片 JSON 后导出：

```text
node "SKILL_DIRECTORY/scripts/learning-cards.mjs" export --workspace "WORKSPACE" --evidence "EVIDENCE_FILE"
```

`WORKSPACE` 使用已存在的工作目录；包内有 `samples/source.zh-CN.md` 样例。导入 Anki 时选择基础卡片并预览 Front/Back 两列。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-learning-cards
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-learning-cards)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-learning-cards
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-learning-cards)。下载仓库 ZIP，将 `skills/mochi-learning-cards` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
