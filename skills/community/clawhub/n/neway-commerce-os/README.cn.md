# Neway Commerce OS

> 一个 WorkBuddy Skill：用**一句话产品创意**生成可运行的全栈电商站点，并强制它通过质量门禁。

> 推荐 WorkBuddy Bot 生成；把本 Skill 喂给 Cursor、Claude、GPT 等助手，同样能跑。

[English](README.md) · **简体中文**

---

## 一句话上手

对 Bot 说：

> **「帮我生成一个时尚轻奢电商网站，卖大衣和包袋的」**

Bot 会：检测语言 → 归一化需求 → 用内置模板脚手架 → 填充内容 → **跑质量门禁** → **跑构建** → 交付带证据的 Handoff Notes。

开箱即用的默认形态是一套**英文文案**的时尚店（外套 / 裙装 / 上衣 / 针织 / 包袋 / 配饰，12 件商品，本地图片池），价格默认 ¥（CNY），可在 [换币种](#自定义与扩展) 里切成 USD。你可以直接改文案和数据。

---

## 三条铁律（硬约束，非建议）

| # | 规则 | 机器门禁 |
|---|------|----------|
| IR-1 | 字号必须**偶数**且**不低于 12px** | `G-02` |
| IR-2 | UI 内**严禁 emoji** | `G-01` |
| IR-3 | 图标统一 **lucide 线性风格** | `T-04` + 人工复核 |

违反任一条 = 生成失败，必须回炉，不允许交付。

---

## 质量门禁

生成完不跑门禁的产物不算交付物。

```bash
python scripts/validate_generated_project.py <项目目录> --lang zh-CN --currency CNY
```

29 项检查，覆盖：结构完整性、占位符与占位文案残留、emoji、字号、币种一致性、
商品数量/分类/主副图差异、Product 接口字段、store 契约、SPA 路由、
AI 导购场景数、双色板、组件类、语言属性、图片可解析性。

退出码 0 才允许交付。**不通过就改产物，不要改门禁。**

构建门禁（脚本之外，必须自己跑）：

```bash
cd <项目目录> && npm install && npm run build   # tsc --noEmit && vite build
```

---

## 生成的项目结构

```
site-name/
├── index.html                  ← lang 属性 + Google Fonts
├── package.json                ← 依赖清单（不要新增依赖）
├── tailwind.config.js          ← 双色板 brand + fresh
├── postcss.config.js
├── vite.config.ts              ← publicDir: 'static'
├── tsconfig.json               ← strict: true
├── .env.example                ← 环境变量占位
├── edgeone.json                ← EdgeOne Pages 部署配置
├── README.md
├── static/images/              ← 16 张内置演示图（构建后进入 dist/images/）
├── src/
│   ├── main.tsx
│   ├── App.tsx                 ← 7 个路由 + 全局 CartDrawer + AIChatWidget
│   ├── styles.css              ← 组件类：btn-* / tag / section-* / input-field
│   ├── utils/format.ts         ← formatPrice() 唯一的金额格式化入口
│   ├── components/             ← Navbar / Footer / ProductCard / CartDrawer / AIChatWidget
│   ├── pages/                  ← Home / Shop / Product / Cart / Checkout / Wishlist / Admin
│   ├── data/products.ts        ← 商品数据唯一来源（TypeScript，不是 JSON）
│   ├── store/cartStore.ts      ← 购物车 + 收藏夹两个 persist store
│   └── types/index.ts          ← Product / Category / CartItem / PromoCode
└── functions/
    ├── api/{products,checkout,assistant}.ts   ← Edge Functions
    └── node/stripe-webhook.ts                 ← Node Function
```

### 路由表（7 个全部必须存在）

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | HomePage | 首页 |
| `/shop` | ShopPage | 分类 tab + 筛选 + 排序 + 网格/列表 |
| `/product/:id` | ProductPage | 商品详情，未命中显示 404 态 |
| `/cart` | CartPage | 购物车整页 |
| `/checkout` | CheckoutPage | 三步结算 |
| `/wishlist` | WishlistPage | 收藏夹 |
| `/admin` | AdminPage | 管理后台 |

---

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | React 18 + TypeScript 5 + Vite 5 + Tailwind CSS 3 |
| 图标 | lucide-react（线性，禁止 emoji） |
| 动画 | framer-motion |
| 状态 | Zustand + `persist` |
| 路由 | react-router-dom v6 |
| 字体 | Inter + Playfair Display，Noto Sans SC / Noto Serif SC 作 CJK 回退 |
| API | Hono 风格 Edge Functions + Node Functions |
| 支付 | Stripe（mock / live 双模式） |
| 部署 | EdgeOne Pages |

---

## 常用命令

```bash
# 脚手架（不会删除已有目录，重跑会改名备份为 <slug>.bak-<时间戳>）
python scripts/scaffold_project.py "<一句话需求>" --output <输出目录> --brand "<品牌>"

# 质量门禁
python scripts/validate_generated_project.py <项目目录> --lang zh-CN --currency CNY

# 校验内置模板自身是否仍然合规（模板出货为英文，所以 --lang en）
python scripts/validate_generated_project.py templates/base --template --lang en --currency CNY

# 远程图片可达性（默认关闭，本地图片池不需要）
python scripts/validate_generated_project.py <项目目录> --check-images

# 仓库自检：技能本体混入中文就报错
python scripts/check_skill_language.py
```

---

## 玩法示例

> 「生成一个时尚潮牌电商，主打年轻潮流品牌，有新品区和限时折扣，暗色炫酷风，AI 导购帮忙搭配推荐」

> 「搭一个独立创作者商店，卖模板、预设、电子书，按分类展示，购物车实时更新，Mock 支付预览流程」

> 「做一个 SaaS 产品官网，三个定价套餐，带功能对比表和 AI 销售助手」

> 「Build a premium multi-product storefront for NewayStudio that sells UI kits, AI workflow packs and creator tools, with an AI shopping concierge and Stripe checkout.」

英文需求会生成英文 UI（`lang="en"`），中文需求生成中文 UI —— 门禁的 `L-01` 会校验。

---

## 图片策略

内置 16 张演示图在 `templates/base/static/images/`，`vite.config.ts` 把 `static`
设为 `publicDir`，页面统一用 `/images/<文件名>.jpg` 引用。

**默认用本地图**：确定性高、离线可用、不受代理/网络影响，门禁 `I-01` 会校验文件存在。
只有当品类确实没有匹配素材时才用外链，并用 `--check-images` 验证可达后替换。

---

## 自定义与扩展

**接入真实 AI 导购**：`functions/api/assistant.ts` 顶部注释说明了替换路径，设置
`AI_API_BASE` / `AI_API_KEY` / `AI_MODEL` 即可。前端关键词逻辑在
`AIChatWidget.tsx` 的 `mockAIResponse()`，关键词语言必须与 UI 一致（英文站用英文关键词，中文站用中文关键词）。

**切换支付**：`.env` 设 `VITE_PAYMENT_MODE=stripe`，配置
`STRIPE_SECRET_KEY` + `STRIPE_WEBHOOK_SECRET`。

**换币种**：改 `src/utils/format.ts` 的 `CURRENCY_SYMBOL`（以及 `toLocaleString` 的 locale）
与 `.env` 的 `VITE_DEFAULT_CURRENCY`，然后用 `--currency USD` 跑门禁。

**加页面**：在 `src/pages/` 新增并在 `App.tsx` 注册路由，同时更新门禁的
`REQUIRED_FILES`（如需强制存在）。

---

## 注意事项

- 产物是**脚手架 + 可点击的演示**：UI、流程、状态管理完整；支付、AI、订单持久化是占位实现。
- 交付时必须区分 **scaffold-ready / demo-ready / production-ready** 三种状态，不要把演示说成生产可用。
- 每次生成都是独立目录，**不会修改已有项目**。
- 商品数据唯一来源是 `src/data/products.ts`；`products.json` 属于必须删除的残留。
- 金额展示一律走 `formatPrice()`，组件里硬编码货币符号会被门禁拦下。

---

## 许可

MIT
