# 内容改写工作台

[English](README.md)

把一份素材改写成不同渠道的文案，核对事实依据和字数。

## 功能

将发布说明、产品材料或文章整理为事实清单，用已有模型生成不同渠道、语言和语气的文案。按你指定的字数预算检查长度、引用、语言和相似内容，保存 `drafts.md`、`facts.md` 与 JSON。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
根据我提供的产品资料，写一条150字以内的中文朋友圈文案和一条英文X草稿，保留事实依据。
```

```text
把这份更新说明改成正式邮件和简短公告，各保存一份，检查数字和链接。
```

```text
把这篇草稿缩短到300字，保留价格、日期和核心功能，输出修改前后对照。
```

## 高级用法：在终端手动运行

下面是开发者手动运行命令。在安装 OpenClaw 的电脑或服务器终端执行；日常使用直接发送上面的对话示例即可。

先把命令中的占位名称换成实际路径：

- `SKILL_DIRECTORY`：已安装的这个Skill文件夹。
- `WORKSPACE`：助手工作区路径。
- `INPUT_JSON`：准备好的输入JSON文件。

让 OpenClaw 参照 `samples/campaign.json` 准备素材、事实和草稿，再运行：

```text
node "SKILL_DIRECTORY/scripts/check.mjs" --input "INPUT_JSON" --output-dir "WORKSPACE"
```

将路径替换为实际文件和已存在的工作目录。字符预算按 Unicode 码点计算，包含空格与换行。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-content-workbench
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-content-workbench)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-content-workbench
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-content-workbench)。下载仓库 ZIP，将 `skills/mochi-content-workbench` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

