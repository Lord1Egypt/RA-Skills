# Neway Commerce OS

> 一款 WorkBuddy AI Skill，基于简短的**产品创意描述**，一键生成全栈电商网站骨架。

> 推荐 WorkBuddy Bot 生成，其它 Bot（如 Cursor、Claude、GPT）也可以出色完成同样效果。

---

## 🎁 入门 Demo：时尚轻奢电商

想最快了解本 Skill 能做什么？对 Bot 说一句就够：

> **「帮我生成一个时尚轻奢电商网站」**

Bot 会使用 `templates/base/static/images/` 内置的 16 张样例图，1:1 复原对标 `project/fashion-store` 品质的完整电商站——LUMIÈRE 时尚轻奢品牌，包含 Hero 轮播、分类导航、商品详情、购物车、三步结算、AI 导购等全部功能，中文/英文按系统语言自适应。

📂 Demo 参考输出：`D:\claw\workspace\workbuddy\work\project\lumiere`

> ⚠️ `static/images/` 为 Skill 入门演示用途，生产项目请替换为你自己的商品图片。

---

## 📖 概述

Neway Commerce OS 是一个可复用的电商操作系统 Skill，专为以下场景设计：

- **数字商品**（UI Kit、模板、课程、软件许可）
- **创作者店铺**（独立创作者的一站式商店）
- **实物商品店铺**（服装、配饰等支持尺码/颜色/材质的品类）
- **多产品工作室**（如 NewayStudio 风格的产品矩阵）
- **AI 辅助销售**（内置 AI 导购对话入口）

**核心思路**：输入一句话的产品想法 → 输出一个可直接运行的 React + Vite + Hono 全栈网站，包含前台店铺、购物车、结账、愿望清单、管理后台、AI 导购，以及 EdgeOne Pages 部署配置。

---

## 🚀 快速开始

### 前置条件

- Node.js >= 18
- （可选）EdgeOne Pages 账号，用于部署
- （可选）Stripe 账号，用于生产支付

### 使用方式

**推荐：通过 WorkBuddy Bot 对话生成**

直接向 AI 说出你的想法，比如：

> 🎯 **「帮我整一个时尚电商网站，卖潮牌联名卫衣的」**

> 🎯 **「来一套数字产品商店，卖我的 AI 提示词模板包」**

> 🎯 **「给我弄个创作者订阅站，月付会员制，带 AI 导购」**

> 🎯 **「生成一个多产品工作室官网，同时卖课程 + 设计素材 + SaaS 订阅」**

Bot 会自动分析需求、完成整套生成流程。**简单到只说一句话就行。**

> 💡 不只是 WorkBuddy Bot 能用，把这个 Skill 喂给 Cursor、Claude、GPT 等任何 AI 助手，它们也能出色完成同样的任务。

---

## 📂 生成的项目结构

```
site-name/
├── index.html                  ← Google Fonts + lang 属性
├── package.json                ← 包含所有必需依赖
├── tailwind.config.js          ← 字体 + 品牌色定义
├── postcss.config.js           ← Tailwind + Autoprefixer
├── vite.config.ts
├── tsconfig.json
├── .env.example
├── .gitignore
├── edgeone.json               ← EdgeOne Pages 部署配置
├── src/
│   ├── main.tsx
│   ├── App.tsx                 ← 路由定义（7 个路由）
│   ├── styles.css              ← Tailwind 指令 + 组件样式
│   ├── components/
│   │   ├── Navbar.tsx         ← 顶部导航（移动端菜单 + 搜索）
│   │   ├── Footer.tsx         ← 站点底部（4 栏布局 + 邮件订阅）
│   │   ├── ProductCard.tsx    ← 商品卡片（网格/列表双模式）
│   │   ├── CartDrawer.tsx     ← 滑出式购物车（必需，非可选）
│   │   └── AIChatWidget.tsx  ← AI 导购对话组件
│   ├── pages/
│   │   ├── HomePage.tsx       ← 首页（Hero + 分类 + 新品 + 畅销）
│   │   ├── ShopPage.tsx       ← 商品浏览/筛选/排序页（必需）
│   │   ├── ProductPage.tsx    ← 商品详情页 /product/:id
│   │   ├── CartPage.tsx       ← 完整购物车页面
│   │   ├── CheckoutPage.tsx   ← 三步结账流程
│   │   ├── WishlistPage.tsx   ← 愿望清单页面
│   │   └── AdminPage.tsx      ← 管理后台页面
│   ├── data/
│   │   └── products.ts         ← TypeScript 类型化商品数据
│   ├── store/
│   │   └── cartStore.ts       ← Zustand + persist 中间件
│   └── types/
│       └── index.ts            ← Product, Category, CartItem 等接口
└── functions/
    ├── api/
    │   ├── products.ts
    │   ├── checkout.ts
    │   └── assistant.ts
    └── node/
        └── stripe-webhook.ts
```

### 路由表（全部 7 个路由必须存在）

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | HomePage | 首页 |
| `/shop` | ShopPage | 商品浏览 |
| `/product/:id` | ProductPage | 商品详情 |
| `/wishlist` | WishlistPage | 愿望清单 |
| `/cart` | CartPage | 购物车 |
| `/checkout` | CheckoutPage | 三步结账 |
| `/admin` | AdminPage | 管理后台 |

---

## 🧱 技术栈

| 层 | 技术 |
|----|------|
| **前端** | React 18 + TypeScript 5 + Vite 5 + Tailwind CSS 3 |
| **动画** | Framer Motion |
| **图标** | Lucide React（禁止 emoji） |
| **状态管理** | Zustand + `persist` 中间件 |
| **路由** | React Router v6 |
| **API** | Hono Edge Functions / Node Functions |
| **支付** | Stripe（Mock 模式 + 生产模式） |
| **AI 导购** | 自定义 API 端点，预留 AI 集成 |
| **部署** | EdgeOne Pages |

---

## 🎮 玩法示例

### 玩法一：时尚潮牌电商 🧥

> "生成一个时尚的电商购物网站，主打年轻潮流品牌，有新品区、联名款专区、限时折扣倒计时，配色要炫酷的暗黑风，AI 导购帮忙搭配推荐"

生成结果包含：首页新品轮播、联名款专区、折扣倒计时组件、暗色主题 + 渐变强调色、AI 风格导购

### 玩法二：数字创作者店铺 🎨

> "帮我搭一个独立创作者的商店，卖模板、预设、电子书，按分类展示，购物车实时更新，Mock 支付就能预览流程"

生成结果包含：分类筛选栏、商品卡片网格、实时购物车抽屉、一步式 Mock 结账

### 玩法三：SaaS 订阅站 🔄

> "做一个 SaaS 产品官网，三个定价套餐（免费版/Pro/企业版），带功能对比表和 AI 销售助手"

生成结果包含：定价卡片对比、Feature Grid、AI 导购（帮你选套餐）、账户管理页（订阅状态）

### 玩法四：全功能产品矩阵 📦

> "Build a premium multi-product storefront for NewayStudio that sells UI kits, AI workflow packs, and creator tools, with an AI shopping concierge and Stripe checkout."

生成结果包含：Studio 风格首页、商品跨品类矩阵、完整结账 + 后台、Stripe 支付 + Webhook

---

## 🧪 支付模式

### Mock 模式（默认，适合开发/演示）

- 生成假订单 ID
- 模拟支付成功
- 跳转到成功/账户页面
- 不需要任何外部服务

### Stripe 模式（生产）

- 创建 Stripe Checkout Session
- 跳转至 Stripe 托管结账页
- 通过 Webhook 处理支付结果
- 需要：`STRIPE_SECRET_KEY` + `STRIPE_WEBHOOK_SECRET`

**切换方式**：在 `.env` 中设置 `VITE_PAYMENT_MODE=stripe`

---

## 🚢 部署（EdgeOne Pages）

### 本地开发

```bash
npm install
npm run dev      # 启动 Vite 开发服务器
```

### 生产部署

1. 在 EdgeOne Pages 中设置环境变量
2. 将支付模式切换为 `stripe`
3. 配置 Webhook 端点
4. 部署前端 + 函数处理器
5. 验证结账重定向和 Webhook 回调

### 部署检查清单

- [ ] 首页正常渲染
- [ ] 商品数据加载正常
- [ ] 购物车更新正常
- [ ] 结账端点正常响应
- [ ] AI 导购端点正常响应
- [ ] Webhook 端点已配置
- [ ] 管理后台可访问
- [ ] 环境变量占位已替换为真实值

---

## 🔧 自定义与扩展

### 接入真实 AI 导购

`functions/api/assistant.ts` 预留了 AI 导购 API 端点。接入方式：

1. 设置 `AI_API_BASE`、`AI_API_KEY`、`AI_MODEL` 环境变量
2. 在端点中调用外部 AI API
3. 或直接在文件中实现自定义推荐逻辑

### 添加更多页面

直接在 `src/pages/` 下添加，并在 `App.tsx` 中注册路由即可。

### 自定义样式

编辑 `src/styles.css` 中的 `@layer components` 和 `@layer utilities` 来自定义组件样式。主题色在 `tailwind.config.js` 中的 `brand` 色系定义。

---

## 📐 架构层次

```
┌─────────────────────────────────────┐
│   Presentation Layer (React + Vite) │  ← 首页 / 商品 / 购物车 / 结账 / 后台
├─────────────────────────────────────┤
│   Application Layer (Zustand + API) │  ← 状态管理、路由、API 封装
├─────────────────────────────────────┤
│   API Layer (Hono Functions)        │  ← 商品 / 结账 / AI 导购 / Webhook
├─────────────────────────────────────┤
│   Commerce Layer                    │  ← 商品、购物车、结账、支付切换
├─────────────────────────────────────┤
│   Deployment Layer (EdgeOne Pages)  │  ← 静态托管 + Edge Func + Node Func
└─────────────────────────────────────┘
```

---

## ⚠️ 注意事项

- 生成的项目是**骨架/脚手架级别**，包含完整的 UI 结构和 API 端点占位
- **Mock 数据**和**模拟行为**默认启用，生产环境需要接入真实服务
- 每次生成都是独立的，**不会修改已有项目**
- AI 导购端点是**集成点预留**，默认返回 mock 响应
- 生成的 `NEWAY_BRIEF.md` 会说明哪些是脚手架就绪、哪些需进一步实现
- 遵循 Convention 0 语言检测规则：系统 `zh-*` 则生成中文 UI，否则生成英文 UI

---

## 📄 许可

MIT
