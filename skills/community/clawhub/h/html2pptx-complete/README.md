# 🎨 html2pptx-complete

HTML 转 PPTX 完整工作流 — 自动内嵌外部 CSS，使用 pptxgenjs 解析，生成可编辑 PPTX

---

## 🚀 三步流程

```
HTML (带外部 CSS)
    ↓ [步骤 1: CSS 内嵌]
HTML (内嵌 CSS，可独立运行)
    ↓ [步骤 2: pptxgenjs 解析]
PPTX 结构
    ↓ [步骤 3: 导出]
可编辑 PPTX 文件
```

---

## 📦 快速开始

### 安装依赖

```bash
cd /Users/panda/.openclaw/workspace/skills/html2pptx-complete

# Python 依赖（CSS 内嵌）
pip3 install -r requirements-python.txt

# Node.js 依赖（PPTX 生成）
npm install
```

### 一键转换

```bash
# 基本用法
node scripts/convert.js input.html output.pptx

# 示例
node scripts/convert.js examples/demo.html
```

---

## 📋 功能特点

| 步骤 | 功能 | 说明 |
|------|------|------|
| **步骤 1** | CSS 内嵌 | 外部 CSS → `<style>` 标签 |
| **步骤 2** | pptxgenjs 解析 | HTML 结构 → PPTX 形状 |
| **步骤 3** | 导出 | 可编辑 PPTX 文件 |

---

## 📊 分页规则

**优先级:**
1. `section.slide` 结构（最高）
2. `<h1>` 标题（备选）
3. 单页（无上述结构）

---

## 📖 完整文档

详见 `SKILL.md`

---

**版本:** v1.0.0  
**License:** MIT
