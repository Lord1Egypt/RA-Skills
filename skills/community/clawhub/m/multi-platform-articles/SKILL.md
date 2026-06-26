---
name: "multi-platform-articles"
description: "将 Markdown 转换为数十种精美主题 HTML，并一键推送到微信公众号草稿箱（支持自动解析文内图片并生成封面）。用户提到“排版/主题/发布公众号/草稿/小红书/头条”时调用。"
---

# Multi-Platform Articles (MPA)

本 Skill 是一个将 Markdown 一键排版并发布到微信公众号等平台的自动化助手。
它依赖于底层的 `mpa` CLI 工具执行具体的渲染和网络请求。

## 🔧 前置要求 (依赖安装)
如果用户的终端中没有 `mpa` 命令，请**首先指导用户在终端中执行以下命令**安装底层依赖：
```bash
curl -fsSL https://raw.githubusercontent.com/shijianzhong/multi-platform-articles/main/scripts/install.sh | sh
```
*安装完成后，`mpa` 会自动配置在用户的 `~/.local/bin` 中。*

## ⚙️ 配置账号 (TUI)
如果用户是第一次使用，或需要修改微信公众号的 AppID/Secret 及 AI 绘图的配置，请让用户在终端运行：
```bash
mpa
```
这会打开一个交互式的 TUI 界面，用户可以在里面配置并在底部按提示操作（`Ctrl+s` 保存）。

## 🚀 核心工作流
当用户要求排版或发布文章时，请按照以下步骤调用底层工具：

### 1. 查找可用主题
如果用户没有指定主题，或者想看看有哪些主题，运行：
```bash
mpa themes list
```

### 2. 转换排版 (本地渲染 HTML)
如果用户只想排版并预览，运行：
```bash
mpa convert path/to/article.md --mode local --theme <主题名, 例如 github-readme> -o out.html
```

### 3. 一键推送到微信公众号草稿箱
如果用户要求发布，请确保他提供了文章的 Markdown 文件。如果用户没有提供封面图，你可以利用 `mpa` 的内置能力自动生成：
```bash
mpa publish wechat-draft --md path/to/article.md --theme <主题名> --title "文章标题" --cover path/to/cover.jpg
```
*注：发布时 `mpa` 会自动提取 Markdown 里的图片、自动上传素材并替换回填 HTML，最终生成一篇完整的图文推送到公众号草稿箱。*

## ⚠️ 关键约束
1. 不要尝试自己去写 Python/Node 脚本调微信 API，**必须且只能**通过调用 `mpa` 命令来完成排版和发布任务。
2. 遇到 `wechat api error` 时，请将完整的错误码和信息反馈给用户。
