---
name: knowledge-chat
version: 1.0.2
description: Knowledge Chat 知识库对话助手 - 支持连接外部知识库、语义搜索、上下文对话、图片/附件理解。具备思考进度提示、Markdown渲染、后续建议、向量索引构建等功能。
trigger:
  - knowledge-chat
  - 知识库
  - 语义搜索
  - 知识检索
  - 小新同学
category:
  - 效率工具
  - 数据分析
tags:
  - 知识库
  - 语义搜索
  - API集成
  - OpenClaw
  - RAG
  - 多模态
  - 向量数据库
---

# Knowledge Chat 知识库对话助手 v1.0.2

## 📋 版本更新

### v1.0.2 新增功能 (2026-04-13)
- ✅ **向量索引构建** - 知识库管理界面新增"索引"按钮，手动构建向量索引
- ✅ **PDF 内容解析** - pdf-parse v1.1.1 正确解析 PDF 内容
- ✅ **语义搜索优化** - 检索数量从 5→10，阈值从 0.3→0.25，内容更全面
- ✅ **回复更详细** - 更新 system prompt，回复更详细完整，包含引用原文
- ✅ **嵌入 API 修复** - 批次大小改为 10，符合 Dashscope API 限制

### v1.1.0 新增功能 (2026-04-13)
- ✅ **思考进度条** - 发送消息时显示"正在思考中..."动画，实时反馈
- ✅ **Markdown 正确渲染** - 表格、列表、引用块、代码块完美显示
- ✅ **后续建议** - AI 自动生成 2-3 个相关追问，引导深入探索
- ✅ **图片/附件支持** - 发送图片和文档，AI 自动理解内容
- ✅ **紧凑 UI 布局** - 100% 缩放即可查看完整界面，无需拖动

---

## 🎯 功能概述

Knowledge Chat 是一个专业的知识库对话助手，具备以下核心能力：

| 功能模块 | 说明 |
|---------|------|
| **知识库连接** | 连接外部知识库 API，支持多种认证方式 |
| **语义搜索** | 基于 RAG 的智能检索，比关键词搜索更精准 |
| **上下文对话** | 多轮问答，记住对话历史 |
| **多模态理解** | 支持图片、文档附件，AI 自动分析内容 |
| **来源标注** | 回答末尾标注信息来源（文件名/网页链接） |

---

## 🚀 使用场景

1. 企业知识库接入
2. 智能问答系统
3. 文档检索助手
4. RAG (检索增强生成) 应用
5. 多模态内容分析

---

## 📁 项目结构

```
knowledge-chat-skill/
├── SKILL.md              # 技能说明文档
├── README.md             # 项目简介
├── references/           # 参考资料
│   └── kb_connector.py   # 知识库连接示例
├── scripts/              # 脚本文件
│   └── setup.sh          # 安装脚本
```

---

## 🔧 核心技术栈

| 技术 | 用途 |
|------|------|
| Next.js 14 | 前端框架 |
| TypeScript | 类型安全 |
| Tailwind CSS | UI 样式 |
| Dashscope API | AI 模型（qwen-plus, qwen-vl-max） |
| SQLite + better-sqlite3 | 本地数据库 |
| react-markdown | Markdown 渲染 |
| remark-gfm | GitHub Flavored Markdown |

---

## 💡 API 端点

### 聊天相关
- `POST /api/chat/messages` - 发送消息（支持附件）
- `GET /api/chat/sessions` - 获取会话列表
- `GET /api/chat/sessions/:id/messages` - 获取历史消息
- `POST /api/chat/upload` - 上传图片/文件
- `GET /api/chat/files/:fileId` - 获取文件

### 知识库相关
- `GET /api/knowledge` - 知识库列表
- `POST /api/knowledge/:id/upload` - 上传知识文档
- `POST /api/knowledge/:id/ingest` - 解析知识内容

---

## 🎨 UI 功能详解

### 1. 思考进度条 (ThinkingIndicator)
发送消息后，显示三个弹跳圆点动画 + "小新正在思考中..." 提示，让用户知道 AI 正在处理。

### 2. Markdown 渲染器 (MarkdownRenderer)
- 自动转换 `<br>` 为换行
- 表格：带边框、悬停高亮
- 列表：每项独立一行，带图标
- 代码块：语法高亮背景
- 引用块：左侧彩色边框

### 3. 后续建议 (FollowUpQuestions)
AI 在回答末尾生成 2-3 个相关问题，用户点击可直接发送，无需手动输入。

### 4. 文件上传 (FileUpload)
- 图片：支持 JPG/PNG/GIF，显示预览
- 文档：txt/md/pdf 等，自动读取内容
- 限制：单文件最大 10MB

---

## 🔐 安全说明

- 所有文件上传需登录验证
- 文件大小限制 10MB
- 图片支持格式：JPG, PNG, GIF, WEBP
- 文档支持格式：TXT, MD, PDF, DOC, DOCX

---

## 📊 数据库表

| 表名 | 说明 |
|------|------|
| `chat_sessions` | 对话会话 |
| `chat_messages` | 对话消息 |
| `chat_files` | 上传的文件附件 |
| `knowledge_base` | 知识库配置 |
| `knowledge_files` | 知识库文档 |

---

## 📝 示例对话

**用户**: 如何进行 Salesforce 数据备份？

**小新**: 
```
## ✅ Salesforce 数据备份方案

**推荐方案：**

1. **OwnBackup** - 市场占有率第一
   - 自动化备份
   - 一键恢复
   - 审计日志

2. **Git + SFDX** - 元数据备份
   - 版本追溯
   - 变更可回滚

📚 信息来源：CRM知识库 - 备份策略章节

---
接下来，你可能想了解：
[数据恢复流程] [备份频率设置] [成本对比分析]
```

---

## 🔄 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.2 | 2026-04-13 | 向量索引构建按钮、PDF解析修复、语义搜索优化、回复更详细 |
| v1.1.0 | 2026-04-13 | 思考进度、Markdown渲染、后续建议、图片/附件支持、UI优化 |
| v1.0.0 | 2026-04-10 | 初始版本：知识库连接、语义搜索、上下文对话 |

---

## 🙏 使用说明

1. 部署 Next.js 项目到服务器
2. 配置 `.env.local` 中的 `DASHSCOPE_API_KEY`
3. 运行 `npm run build && pm2 start`
4. 访问 `/dashboard/chat` 开始对话

---

**分享链接**: https://xiaping.coze.site/skill/4dd4f1c0-d0d8-4f66-9ca2-588583beba92