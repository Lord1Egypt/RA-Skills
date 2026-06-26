---
name: instruction-web
description: 创建Web界面操作指南网页。用于生成介绍Web UI界面、常用功能、操作说明的HTML页面。触发场景：(1) 用户要求创建Web操作指南 (2) 需要介绍某个Web UI界面 (3) 需要包含UI截图、功能说明、导入智能体教程 (4) 用户发送"创建指南"、"操作说明"、"界面介绍"等关键词

## 默认配置（已保存）

**GitHub 仓库**: 2239721014-ops/ai-hardwork-report
**分支**: master
**输出目录**: ~/.openclaw/workspace-aiquanzi/workplace-doc/
**jsDelivr 格式**: https://cdn.jsdelivr.net/gh/2239721014-ops/ai-hardwork-report@master/workplace-doc/{filename}
**预览格式**: https://htmlpreview.github.io/?https://cdn.jsdelivr.net/gh/2239721014-ops/ai-hardwork-report@master/workplace-doc/{filename}
---

# Instruction Web Publisher

创建 Web 界面操作指南网页的完整工作流。

## ⚠️ 输出目录规则（重要）

**生成的 HTML 文件必须统一放到 `workplace-doc` 文件夹**，不要散落在其他位置。

示例路径：
```
/Users/jasperchen/.openclaw/workspace-aiquanzi/workplace-doc/xxx.html
```

## 适用场景

- 创建 Web UI 操作指南
- 介绍软件界面和功能
- 制作导入智能体/Agent 的教程页面
- 生成图文并茂的使用说明

## ⚠️ 触发条件（重要）

当用户发送以下内容时，**必须**自动触发此skill：
- 包含"创建指南"、"操作说明"、"界面介绍"
- 包含"Web教程"、"UI介绍"、"使用手册"
- 包含"如何导入"、"导入智能体"、"导入Agent"
- 要求创建介绍某个Web界面的网页

**重要：内容排版要求**
- 必须**图文并茂**，不能是纯文字
- 需要包含截图占位符、图标、UI元素示意图
- 排版要美观专业，适合在线阅读
- 使用卡片式布局、徽章、代码块、步骤条等元素
- 重点突出**导入智能体**的操作步骤

## 工作流程

### 1. 收集需求

与用户确认：
- 要介绍的软件/Web界面名称
- 主要功能列表
- 导入智能体的具体步骤
- 是否需要包含截图（用户提供或使用占位符）

### 2. HTML 生成

生成美观的 HTML 页面，包含：
- Hero 区域（软件名称、Logo、标语）
- 功能介绍卡片
- 步骤指南（带编号）
- 代码块（用于命令示例）
- 截图占位符区域
- FAQ / 常见问题

### 3. 推送到 GitHub

```bash
cd <repo-path>
git add <file>
git commit -m "Add: <title> guide"
git push
```

### 4. 生成国内访问链接

使用 jsDelivr CDN：
```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/<filename>
```

预览链接：
```
https://htmlpreview.github.io/?<jsdelivr-url>
```

## 输出格式

完成后向用户返回：
1. jsDelivr 国内镜像链接（主要）
