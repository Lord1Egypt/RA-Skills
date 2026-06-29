# PostFlow AI - AI 内容中台

多平台 AI 内容管理系统：生成 → 评分 → 适配 → 排期 → 发布通知 完整闭环。

## 功能特性

### AI 内容生成
- 多平台内容生成（小红书、抖音、知乎、微信公众号、微博、Twitter/X、Reddit、TikTok）
- 批量内容生成（一次输入主题，生成 1-20 篇多平台内容）
- 内置 10+ 内容模板（产品发布、干货分享、热点追踪、SEO博客等）
- 跨平台内容智能适配

### SEO 优化
- 多维度 SEO 评分（标题、可读性、关键词密度）
- 关键词分析与密度检测
- Meta Description 自动生成
- LSI 关键词推荐
- 标题结构分析

### 内容管理
- 内容对比（AI 适配前后对比）
- 内容评分（6 维度评分 + 改进建议）
- 发布排期日历
- Webhook 通知（内容发布事件）

### 变现系统
- SaaS 订阅（免费/专业/企业）
- API 调用套餐
- 授权码分销系统
- 用量配额管理
- 多级定价

### 技术栈
- Next.js 15 (App Router)
- Prisma + SQLite/PostgreSQL
- DeepSeek AI (OpenAI SDK 兼容)
- NextAuth.js v5
- Tailwind CSS
- 支持 Docker 部署

## 快速开始

1. 复制 `.env.example` 为 `.env`，配置 DeepSeek API Key
2. `npm install && npx prisma db push`
3. `npm run dev`

## 部署

详见 `docs/DEPLOY-AND-MONETIZE.md`
