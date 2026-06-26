# 发布指南：ClawHub（免费）+ OpenClawMart（付费）

---

## 路线一：ClawHub 免费发布（引流 + 曝光）

ClawHub 是 OpenClaw 官方技能注册表，相当于"AI 技能的 npm"，免费发布，用于建立信誉和引流。

### 前置条件
- GitHub 账号（注册满 7 天）
- 本机已安装 OpenClaw CLI

### 步骤

**1. 安装 clawhub CLI**
```bash
npm install -g clawhub
# 或
npx clawhub --version   # 确认可用
```

**2. 登录**
```bash
clawhub login
# 浏览器弹出 GitHub OAuth 授权，点允许
clawhub whoami   # 确认登录成功
```

**3. 进入技能目录，发布**
```bash
cd ~/openclaw-listing-skill
clawhub publish .
# 首次发布会自动读取 SKILL.md 中的 YAML frontmatter
```

**4. 发布成功后验证**
```bash
clawhub info ecommerce-listing-generator
# 可以看到你的技能页面链接
```

**5. 用户安装命令（发给买家/用户的）**
```bash
clawhub install ecommerce-listing-generator
```

### 注意
- `slug` 字段必须全局唯一，如果 `ecommerce-listing-generator` 被占用，改成 `ecommerce-listing-generator-cn` 或加你的用户名前缀
- 发布后可在 clawhub.ai 搜索你的技能名验证是否上线

---

## 路线二：OpenClawMart 付费上架（一次性收费）

OpenClawMart（openclawmart.com）支持付费技能销售，带 Stripe 结账和卖家 Dashboard。

### 步骤

**1. 注册卖家账号**
- 打开 https://openclawmart.com/dashboard
- 用 GitHub 或 Email 注册
- 完成 Stripe 绑定（用于收款，需要手机验证）

**2. 创建 Listing**
进入 Dashboard → Sell → New Listing，填写：

| 字段 | 填写内容 |
|------|----------|
| Product Type | Skill |
| Title | 跨境电商多平台 Listing 生成器 |
| Subtitle | Amazon + AliExpress 标题/卖点/SEO关键词一键生成 |
| Category | Marketing |
| Price | 建议 $9–$19（见定价建议） |
| Description | 见下方文案模板 |
| Upload Package | 上传 `openclaw-listing-skill.zip` |

**3. 商品描述文案（直接复制）**

```
Turn any product image or spec sheet into a complete,
platform-ready listing in seconds.

✅ Amazon: Title (≤200 chars) + 5 Bullet Points + Description + Backend Keywords
✅ AliExpress: Title (≤128 chars) + Layered Keyword Strategy + Product Tags
✅ Built-in compliance check: auto-flags banned words before you publish
✅ Vision-enabled: send a product photo and get a full listing

Perfect for: cross-border sellers, sourcing agents, Amazon/AliExpress operators

What's included:
• SKILL.md — drop into your OpenClaw workspace, works immediately
• AGENTS.md snippet — agent config with trigger rules and quality gates
• 2 full example outputs (headphones + pet product)
• install.sh — one-command deployment

Requires: OpenClaw with a vision-capable model (e.g. Kimi K2.5, Claude, GPT-4o)
```

**4. 定价建议**

| 定价 | 适合情况 |
|------|----------|
| $9 | 冷启动期，快速积累前10个销售和评价 |
| $14 | 有几个好评后涨价，主流区间 |
| $19 | 加入"批量生成"或"多语言版"后的升级版 |

建议先定 $9，跑出 10 个销售后改 $14。

**5. 发布并验证**
- 点 Publish，进入审核（通常 24–48 小时）
- 审核通过后获得专属购买链接

---

## 路线三：ClawMart 备选（shopclawmart.com）

如果 OpenClawMart 审核慢或未通过，备选 shopclawmart.com，流程基本相同，
同样支持付费 Skill 上架。

---

## 双轨策略建议

```
ClawHub（免费）
  └─ 作用：建立可信度，免费用户发现你
  └─ 在描述里加一句：
     "Premium version with examples & install script: openclawmart.com/[你的链接]"

OpenClawMart（付费）
  └─ 作用：变现
  └─ 在商品页加：
     "Free community version available on ClawHub: clawhub.ai/skills/ecommerce-listing-generator"
```

两个平台互相引流，免费版当钩子，付费版收钱。

---

## 常见问题

**Q: clawhub publish 报错 "slug already exists"？**
A: 修改 SKILL.md 中的 `slug` 字段，加上你的用户名前缀，如 `yourname-ecommerce-listing-generator`

**Q: OpenClawMart 的 Stripe 在中国大陆能用吗？**
A: 需要绑定支持国际收款的卡（Visa/Mastercard）。如果收款有问题，可以先用 ClawMart（shopclawmart.com）看是否支持其他收款方式。

**Q: 怎么更新版本？**
A: 修改 SKILL.md 中的 `version` 字段（如改为 1.1.0），然后重新 `clawhub publish .`
