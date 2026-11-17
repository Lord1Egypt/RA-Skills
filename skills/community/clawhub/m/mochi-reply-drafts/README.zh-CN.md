# 回复草稿助手

[English](README.md)

根据来信和已确认资料写回复草稿，附引用依据与待核查事项。

## 功能

整理客户来信、已确认事实和适用规则，用已有模型撰写邮件或客服回复。检查收件人、事实引用、数字、链接和承诺用语，保存本地 `draft.txt` 与核查清单，供你审阅后使用。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
客户询问订单进度，根据我提供的处理记录写一封礼貌的中文回复草稿。
```

```text
根据这封来信和退款规则写英文回复，核对金额、日期和链接，列出待确认信息。
```

```text
把这封回复改得简短一些，保留已确认事实，保存draft.txt供我审阅。
```

## 高级用法：在终端手动运行

下面是开发者手动运行命令。在安装 OpenClaw 的电脑或服务器终端执行；日常使用直接发送上面的对话示例即可。

先把命令中的占位名称换成实际路径：

- `SKILL_DIRECTORY`：已安装的这个Skill文件夹。
- `WORKSPACE`：助手工作区路径。
- `INPUT_JSON`：准备好的输入JSON文件。

让 OpenClaw 参照 `samples/reply.json` 准备来信、事实和草稿，再运行：

```text
node "SKILL_DIRECTORY/scripts/check.mjs" --input "INPUT_JSON" --output-dir "WORKSPACE"
```

将路径替换为实际文件和已存在的工作目录。结果包含回复草稿、`checklist.md` 和结构化报告。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-reply-drafts
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-reply-drafts)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-reply-drafts
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-reply-drafts)。下载仓库 ZIP，将 `skills/mochi-reply-drafts` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

