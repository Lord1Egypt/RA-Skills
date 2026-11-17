# 翻译校对

[English](README.md)

翻译或校对文本，核对术语、数字和链接，输出双语对照与问题清单。

## 功能

用已有模型翻译或润色你提供的文字，再核对段落对应、指定术语、数字和链接。保存 Markdown、CSV 双语对照与具体问题，便于逐项修改。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
英文：The Starter plan costs USD 9.90 per month and supports 3 projects. 待校中文：Starter计划每年收费99美元，支持30个项目。请找出三处错误，给出正确译文。
```

```text
把我提供的产品说明译成英文，OpenClaw保留原文，核对日期、数字和链接。
```

```text
按我提供的术语表校对这份双语稿，导出对照CSV和问题清单。
```

## 高级用法：在终端手动运行

下面是开发者手动运行命令。在安装 OpenClaw 的电脑或服务器终端执行；日常使用直接发送上面的对话示例即可。

先把命令中的占位名称换成实际路径：

- `SKILL_DIRECTORY`：已安装的这个Skill文件夹。
- `WORKSPACE`：助手工作区路径。
- `INPUT_JSON`：准备好的输入JSON文件。

让 OpenClaw 按包内 `samples/review.json` 的格式准备原文与译文，再运行：

```text
node "SKILL_DIRECTORY/scripts/check.mjs" --input "INPUT_JSON" --output-dir "WORKSPACE"
```

将路径替换为实际文件和已存在的工作目录。每次结果保存在独立子目录，包含 `comparison.md`、`comparison.csv` 和 `report.json`。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-translation-qa
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-translation-qa)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-translation-qa
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-translation-qa)。下载仓库 ZIP，将 `skills/mochi-translation-qa` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

