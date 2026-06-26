# 🎨 HTML Slides — OpenClaw Skill

> 为 OpenClaw 打造的网页幻灯片创建技能。零依赖、动画丰富、可部署分享。

**原项目**：[zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) · 12k⭐  
**适配版本**：OpenClaw 专用

---

## 🚀 一键安装

在 OpenClaw 中发送以下命令即可安装：

```
skill install https://github.com/838997125/openclaw-html-slides
```

或者通过 ClawHub：

```
/clawhub install openclaw-html-slides
```

---

## ⚡ 快速开始

安装完成后，直接对小小说：

> **"帮我做个 PPT"** / **"做个路演幻灯片"** / **"做网页版自我介绍"** / **"把这份 PPT 转成网页"**

技能自动激活，按以下流程工作：

```
收集需求（主题/页数/内容）
        ↓
生成 3 种风格预览让你选
        ↓
选完 → 生成完整 HTML
        ↓
浏览器自动打开预览
        ↓（可选）
部署到 Vercel / 导出 PDF
```

---

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 从零创建 | 描述需求，AI 生成完整演示文稿 |
| PPT 转换 | 上传 .pptx，自动提取内容再生成网页版 |
| 12 种风格 | Neon Cyber / Terminal Green / Bold Signal 等 |
| 零依赖 | 单 HTML 文件，浏览器直接打开 |
| 动画丰富 | 进出场动画、粒子背景、霓虹特效 |
| 移动适配 | 手机/平板/电脑均可演示 |
| 部署分享 | 一键部署到 Vercel，生成永久链接 |
| 导出 PDF | 生成高清 PDF 用于邮件/打印 |

---

## 📁 目录结构

```
openclaw-html-slides/
├── SKILL.md                  # OpenClaw 技能定义（安装后被读取）
├── IDENTITY.md               # 技能身份与能力边界
├── SOUL.md                   # 设计哲学
├── README.md                 # 本文件
├── STYLE_PRESETS.md          # 12 种视觉预设详细规格
├── viewport-base.css         # 强制响应式 CSS（每个演示必须包含）
├── html-template.md          # HTML 架构模板
├── animation-patterns.md     # 动画参考
├── LICENSE                   # MIT
└── scripts/
    ├── extract-pptx.py      # PPT 内容提取（需要 python-pptx）
    ├── deploy.ps1            # Vercel 部署（Windows PowerShell）
    ├── deploy.sh              # Vercel 部署（Bash/Linux/macOS）
    ├── export-pdf.ps1        # PDF 导出（Windows PowerShell）
    └── export-pdf.sh          # PDF 导出（Bash/Linux/macOS）
```

---

## 🎨 12 种视觉预设

| 编号 | 预设名称 | 风格 | 适合场景 |
|------|---------|------|---------|
| 1 | Neon Cyber | 深色·霓虹科技 | 技术分享、工具演示 |
| 2 | Terminal Green | 深色·终端极客 | 开发者演示、代码展示 |
| 3 | Bold Signal | 深色·大色块 | 路演、高冲击演讲 |
| 4 | Electric Studio | 分屏·专业 | 大会演讲 |
| 5 | Creative Voltage | 赛博朋克 | 产品发布 |
| 6 | Dark Botanical | 优雅·艺术 | 创意展示 |
| 7 | Notebook Tabs | 活页笔记·精致 | 教学教程 |
| 8 | Pastel Geometry | 马卡龙·清新 | 友好型演示 |
| 9 | Split Pastel | 撞色·活力 | 团队汇报 |
| 10 | Vintage Editorial | 复古杂志 | 个性表达 |
| 11 | Swiss Modern | 瑞士极简 | 精确、专业 |
| 12 | Paper & Ink | 纸墨·文学 | 文字内容为主 |

---

## 🔧 工具脚本

### PPT 内容提取

```bash
pip install python-pptx
python scripts/extract-pptx.py input.pptx output_dir/
```

### 部署到 Vercel

```powershell
# Windows
.\scripts\deploy.ps1 .\my-deck\

# Linux/macOS
bash scripts/deploy.sh ./my-deck/
```

### 导出 PDF

```powershell
# Windows
.\scripts\export-pdf.ps1 .\presentation.html

# Linux/macOS
bash scripts/export-pdf.sh ./presentation.html
```

---

## 🔒 信任账号

本技能由 **838997125**（ZYQ）维护，基于 [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides)（MIT License）改编。

---

## 📌 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-04-02 | 初始 OpenClaw 适配版本，Windows 脚本支持 |
