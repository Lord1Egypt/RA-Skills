---
name: md2mindmap
version: 1.1.0
description: Markdown 转思维导图工具 - 一键生成可交互思维导图，支持 HTML + PDF 输出！
author: sukimgit
license: MIT
tags: [markdown, mindmap, 思维导图, 知识整理, 学习, 表格]
metadata:
  {"openclaw": {"emoji": "🧠", "requires": {"bins": ["python"], "python_packages": ["playwright"]}}}
---

# 🧠 Md2Mindmap - Markdown 思维导图工具

**一句话介绍：** 将 Markdown 文档一键转换为可交互的思维导图，支持 HTML + PDF 输出！

---

## 为什么需要 Md2Mindmap？

| 痛点 | Md2Mindmap 解决方案 |
|------|---------------------|
| ❌ Markdown 只有文字，不够直观 | ✅ 一键生成可视化思维导图 |
| ❌ 整理思路效率低 | ✅ 自动识别层级结构 |
| ❌ 分享给别人看不懂 | ✅ HTML 可交互，PDF 可分享 |
| ❌ 没有合适的思维导图工具 | ✅ Markdown 写完自动生成 |

---

## 谁需要使用？

| 用户类型 | 使用场景 | 价值 |
|---------|---------|------|
| **学习者** | 整理知识、复习笔记 | 知识可视化 |
| **讲师** | 课堂演示、培训材料 | 直观展示 |
| **知识工作者** | 方案梳理、项目规划 | 提升效率 |
| **写作者** | 大纲整理、思路梳理 | 写作辅助 |

---

## 核心功能

### ✅ Markdown 解析

| 支持 | 说明 |
|------|------|
| **标题层级** | # ## ### #### 自动识别 |
| **列表** | - * 无序列表 |
| **表格** | 表格内容自动转换为节点（v1.1.0新增） |
| **嵌套** | 缩进自动识别 |

### ✅ 输出格式

| 格式 | 说明 |
|------|------|
| **HTML** | 可交互思维导图（推荐） |
| **PDF** | 适合打印、分享 |

### ✅ 交互功能

| 功能 | 说明 |
|------|------|
| **缩放** | 鼠标滚轮缩放 |
| **拖拽** | 拖动查看 |
| **展开/折叠** | 点击节点展开 |
| **暗色主题** | 自动检测系统主题 |

---

## 快速开始

### 安装

```bash
# ClawHub 安装（推荐）
clawhub install md2mindmap

# 或手动安装
git clone <repo-url> md2mindmap
cd md2mindmap
pip install playwright
playwright install chromium
```

### 使用

```bash
# 生成 HTML
python markmap_generator.py --file input.md --output output.html

# 生成 HTML + PDF
python markmap_generator.py --file input.md --output output.html --pdf output.pdf
```

---

## 使用案例

### 案例 1：学习笔记整理

**场景：** 学习 Python，整理知识结构

**步骤：**
```markdown
# Python 学习笔记

## 基础语法
### 变量
### 数据类型
### 控制流

## 面向对象
### 类
### 继承
### 多态
```

```bash
python markmap_generator.py --file python-note.md --output python-mindmap.html
```

**效果：** 自动生成可交互思维导图，方便复习！

---

### 案例 2：培训课程大纲

**场景：** 准备企业培训课程

**步骤：**
```markdown
# AI 办公培训

## 第一天
### AI 基础概念
### 常用工具介绍

## 第二天
### 实操演练
### 案例分析

## 第三天
### 企业应用
### 效率提升
```

```bash
python markmap_generator.py --file training.md --output training.html --pdf training.pdf
```

**效果：** 课堂演示 HTML，课后发 PDF！

---

### 案例 3：项目规划

**场景：** 新项目启动，梳理架构

**步骤：**
```markdown
# 项目架构

## 前端
### Vue3
### TypeScript

## 后端
### Python FastAPI
### PostgreSQL

## 部署
### Docker
### CI/CD
```

```bash
python markmap_generator.py --file architecture.md --output architecture.html
```

**效果：** 团队快速理解项目架构！

---

## 输出示例

### HTML 思维导图

```
可交互思维导图

特点：
- ✅ 可缩放、拖拽
- ✅ 节点可展开/折叠
- ✅ 自动适应屏幕
- ✅ 暗色主题支持
```

### PDF 输出

```
A4 横向 PDF

特点：
- ✅ 适合打印
- ✅ 方便分享
- ✅ 高清输出
```

---

## 常见问题

### Q1: 支持哪些 Markdown 语法？

**回答：** 支持标题层级（# ## ### ####）、无序列表（- *）和表格（v1.1.0新增）

### Q2: PDF 生成失败怎么办？

**回答：** 需要先安装 Playwright：
```bash
pip install playwright
playwright install chromium
```

### Q3: 中文显示有问题吗？

**回答：** 完美支持中文，无乱码问题！

### Q4: 可以自定义样式吗？

**回答：** 当前版本使用默认样式，后续版本支持自定义！

---

## 与 Md2docx 配合使用

**同一个 Markdown，两种输出！**

| 工具 | 输出 | 用途 |
|------|------|------|
| **Md2docx** | Word 文档 | 文档提交、公文写作 |
| **Md2Mindmap** | 思维导图 | 知识整理、演示展示 |

**安装 Md2docx：**
```bash
clawhub install md2docx
```

---

## 更新日志

### v1.1.0 (2026-03-27)
- ✅ 新增表格解析支持
- ✅ 表格内容自动转换为思维导图节点
- ✅ 支持表格多列内容层次化展示

### v1.0.0 (2026-03-26)
- 🎉 首次发布
- ✅ Markdown 转 HTML 思维导图
- ✅ PDF 输出支持
- ✅ 交互功能（缩放、拖拽、展开/折叠）

---

## 许可证

MIT License

---

## 作者

**OpenClaw Team**

---

**让思维可视化，从 Markdown 开始！** 🧠