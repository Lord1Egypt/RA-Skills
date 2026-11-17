# 文档模板与批量出稿

[English](README.md)

从 DOCX、文本或 HTML 模板批量生成通知、证明和业务文档，检查缺漏字段并保留 Word 排版。

## 功能

从 DOCX、文本或 HTML 模板批量生成通知、证明和业务文档，检查缺漏字段并保留 Word 排版。

在当前助手工作区运行，数据保存在本机。连接邮箱、网盘和日历时使用自己的账户参数。定时提醒通过 OpenClaw 的任务计划运行。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
读取我上传的通知模板.docx，列出所有 {{字段}}，告诉我还缺哪些资料。
```

```text
用这份人员CSV逐行填写证明模板.docx，每人生成一份，保留模板排版。
```

```text
用我提供的标题、日期和正文填写HTML通知模板，输出到新文件。
```

## 运行要求

Python 3.10+; python-docx>=1.2,<2

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-document-templates
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-document-templates)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-document-templates
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-document-templates)。下载仓库 ZIP，将 `skills/mochi-document-templates` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
