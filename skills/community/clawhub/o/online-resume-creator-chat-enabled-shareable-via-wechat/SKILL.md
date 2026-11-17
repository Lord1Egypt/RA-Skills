---
name: talkable-resume
description: Generate a "talkable single-file HTML resume" — a webpage with a built-in keyword-matched resume assistant that answers visitor questions instantly, plus WeChat sharing assets (cover image and QR-code share card), deployable as a shareable link. Use when the user wants a conversational/talkable personal resume webpage, an interactive resume assistant, an AI resume, an HTML resume, a personal homepage/portfolio, or a shareable resume link/card for WeChat/IM/job hunting/personal branding.
agent_created: true
---

# 可对话的个人简历 (Talkable Resume)

**EN:** Turn any resume into a single-file HTML page with a built-in conversational assistant (front-end keyword matching, no backend/LLM needed), generate WeChat sharing assets, and deploy as a shareable link.

把一份简历变成一个**单文件 HTML 网页**，网页里内置"简历助手"对话框。访客用中文提问（工作经历 / 项目 / 技能 / 教育 / 论文等），网页按关键词匹配即时回答。全程**前端、零依赖、纯离线**，无需后端、无需大模型、无需联网。

## 何时使用
- 用户要让简历"能对话 / 能互动 / 能问"
- 用户要做一个简历网页并发微信 / IM 链接给朋友、HR、客户
- 用户要"个人主页式简历""AI 简历"

## 核心设计取舍
- 单文件 HTML：CSS 内联、JS 内联，无 CDN、无外部图片、无 API、无 fetch
- "对话"=**前端关键词匹配**，不是真 AI：
  - 答案写死在 `SECTION` 对象（各板块文本）
  - 靠 `RULES` 关键词表映射到板块
  - 未命中 / 空输入 → 返回引导语"仅能介绍简历相关内容"
- 优点：离线可跑、永久免费、零运维、发给任何人即开即用
- 局限：不能自由聊天；若要真 AI，需接大模型后端（见 references/wechat-sharing.md）

## 工作流程

### 1. 收集简历信息
向用户收集结构化字段：基本信息（姓名 / 电话 / 邮箱 / 头衔）、工作经历、核心技能、重点项目、教育背景、论文专著。
无现成简历时，请用户提供文本 / 文档，或简要访谈后结构化。

### 2. 生成单文件 HTML → `scripts/make_resume.py`
- 数据驱动：修改脚本顶部的 `RESUME` 字典（或传 `--data resume.json`），运行即生成 `index.html`
- 模板含内联样式 + 聊天窗口 + 关键词匹配引擎（`SECTION` / `RULES`）
- 匹配逻辑：遍历 RULES，命中关键词返回对应 SECTION；多命中取最长匹配；未命中返回引导语

### 3. 生成微信分享素材
微信聊天框**粘贴链接只显示纯蓝链、不渲染 OG 封面卡片**（微信机制，与 og:image 无关）。因此分享用"图"而非"裸链"：
- `scripts/gen_cover.py`：生成 1200×630 封面图，`og:image` 引用，让链接卡片（极少数场景）带图
- `scripts/gen_share_card.py`：生成**带二维码的分享卡片图**——发给朋友，对方长按二维码识别即开网页（最稳方案）

### 4. 部署成链接（CloudStudio 静态托管）
- 把目录（index.html + cover.png + share_card.png）部署到 CloudStudio
- 得到 `https://xxxx.gz3.agentos-app.net` 公开链接
- 同一沙箱复用、链接不变；管理在「设置 - 数据管理 - 我发布的应用」

### 5. 防丢失
- 本地副本放 `~/Pictures/`（图片库，不易误删），不要只放桌面
- 线上直链 `.../share_card.png` 永久可重新下载

## 关键坑（必读）
- 微信不渲染链接卡片 → 用"带二维码分享卡片图"绕过
- 隐私：页面含真实电话 / 邮箱 / 年薪，链接公开即任何人可见；敏感场景加访问口令或真后端鉴权
- 过期控制：`new Date()` 前端校验 + 整页替换提示（仅礼貌提示，非强鉴权，可改本地时间绕过）
- 字体：Windows 用 `C:/Windows/Fonts/msyh.ttc`（雅黑，**是 .ttc 不是 .ttf**）
- 依赖：Python venv + Pillow + qrcode

## 分享 / 复用本 Skill
- 打包 zip 发给同事，或发布到 SkillHub 技能市场，或生成分享链接
- 详见 references/wechat-sharing.md 的"分发与扩展"

## Resources
- `scripts/make_resume.py` — 简历数据 → 单文件 HTML（含对话引擎）
- `scripts/gen_cover.py` — 微信封面图（og:image）
- `scripts/gen_share_card.py` — 带二维码分享卡片图
- `references/wechat-sharing.md` — 微信分享机制、真 AI 扩展、隐私与过期、Skill 分发
