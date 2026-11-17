# 会议纪要与行动清单

[English](README.md)

将会议文字整理为纪要、决定和行动清单，每项附原文依据。

## 功能

用已有模型整理会议文字，提取摘要、决定、待办和待确认问题。脚本校对原文引用、负责人和日期，再导出 `meeting.md`、`meeting.json` 与 `tasks.csv`。原文未写明的负责人或日期会标为未知。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
根据这份会议文字整理摘要、决定和待办，每项附原文引用。
```

```text
从会议记录提取负责人和截止日期，没写明的标为待确认。
```

```text
把这份会议的行动项导出为tasks.csv，同时保存Markdown纪要。
```

## 高级用法：在终端手动运行

下面是开发者手动运行命令。在安装 OpenClaw 的电脑或服务器终端执行；日常使用直接发送上面的对话示例即可。

先把命令中的占位名称换成实际路径：

- `SKILL_DIRECTORY`：已安装的这个Skill文件夹。
- `NEW_REPORT_DIRECTORY`：新建的报告目录。
- `TRANSCRIPT.txt`：会议文字文件。
- `NEW_EVIDENCE_DIRECTORY`：新建的原文材料目录。
- `EVIDENCE_FILE`：上一步生成的证据文件路径。
- `EXTRACTION_JSON`：根据模板填写的提取结果JSON。

先准备带行号的材料：

```text
node "SKILL_DIRECTORY/scripts/meeting.mjs" prepare --input "TRANSCRIPT.txt" --out "NEW_EVIDENCE_DIRECTORY"
```

让 OpenClaw 根据返回的模板填写提取 JSON，再导出：

```text
node "SKILL_DIRECTORY/scripts/meeting.mjs" render --evidence "EVIDENCE_FILE" --draft "EXTRACTION_JSON" --out "NEW_REPORT_DIRECTORY"
```

路径替换为自己的文件和新目录；首次可用 `samples/sample-input.txt`。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-meeting-actions
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-meeting-actions)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-meeting-actions
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-meeting-actions)。下载仓库 ZIP，将 `skills/mochi-meeting-actions` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

