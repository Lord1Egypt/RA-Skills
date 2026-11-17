# 文件阅读与重点问答

[English](README.md)

直接读取 DOCX 和文本，跨文件检索原文，导出文本与带行号的证据清单。

## 实际功能

直接读取 DOCX 和文本，跨文件检索原文，导出文本与带行号的证据清单。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
读取我上传的通知.docx，列出要做的事和截止日期，每条附原文位置。
```

```text
在这几份文本文件里查找退款条件，引用原文并标出文件名和行号。
```

```text
把这份DOCX导出为文本，再生成带行号的重点证据清单。
```

## 导出结果

document.txt / source.json / evidence.md / citations.json

文件保存在当前助手工作区，返回路径和 SHA256；记录与历史导出保留。

## 运行要求

OpenClaw、已连接模型、Node.js 24.16+、当前工作区读写权限。DOCX 本地读取；PDF 和图片使用环境已有读取工具。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-document-reader
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-document-reader)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-document-reader
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-document-reader)。下载仓库 ZIP，将 `skills/mochi-document-reader` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
