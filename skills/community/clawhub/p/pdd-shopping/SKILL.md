---
name: pdd-shopping
description: "Pinduoduo shopping assistant. Input a product name or PDD link; evaluate 百亿补贴, 拼团 rules, seller risk, visible price, review signals, refund caveats, and whether the low price is worth it. Safe boundary: no login, no order submission, no payment."
---
## When to Use

User wants to shop on Pinduoduo (拼多多). Agent helps with group buying strategies, seller verification, quality assessment, and navigating China's social e-commerce platform known for extreme discounts.

What makes this skill useful:
- It does not treat every low price as a good deal.
- It checks whether the price depends on 拼团, 补贴, or weak seller trust.
- It is strongest when the user wants the cheapest practical option, not just the most convenient one.

## Commerce Matrix

This skill is the low-price and subsidy-first node in the shopping matrix.

Prefer nearby skills when the user's priority changes:
- `taobao-competitor-analyzer` for same-item comparison across Taobao, JD, PDD, and Vipshop
- `jd-shopping` when trust and fulfillment matter more than absolute low price
- `vip` when the user is shopping branded discount inventory rather than marketplace deals

## Capabilities

### v2.0 - Browser Automation Support

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| **Search** | Optional | Search products, filter by category/price |
| **百亿补贴** | Optional | Browse platform-subsidized deals |
| **拼团** | Optional | View group buying options, join existing groups |
| **Seller Vetting** | Optional | Check store ratings, reviews, badges |
| **Product Detail** | Optional | View specs, prices, service guarantees |
| **Add to Cart** | ✅ Required | Add items to shopping cart |
| **View Cart** | ✅ Required | Review cart contents |
| **Join Group Buy** | ✅ Required | Initiate or join 拼团 |
| **Apply Coupons** | ✅ Required | Check and apply platform/seller coupons |
| **Generate Order Preview** | ✅ Required | Calculate final price with subsidies |
| **Payment** | ❌ Blocked | User must complete payment manually |

**Safety Rule**: Agent stops before payment. User retains full control over final purchase.

### Legacy: Guidance-Only Mode (No Browser)

- Group buying strategies
- Seller vetting guidance
- Quality assessment tips
- 百亿补贴 navigation
- Category-specific advice

## Quick Reference

| Topic | File |
|-------|------|
| Group buying guide | `groupbuy.md` |
| Seller vetting | `sellers.md` |
| Quality assessment | `quality.md` |
| Browser automation | `browser-workflow.md` |

## Workflow

### Phase 1: Discovery (Agent-Assisted)
1. **Search** - Agent searches PDD for target products
2. **百亿补贴** - Check platform-subsidized deals
3. **Filter & Sort** - Apply filters (price, sales, ratings)
4. **Seller Vetting** - Agent checks store badges, ratings, reviews
5. **Group Buy Options** - View 拼团 prices vs solo prices

### Phase 2: Selection (Agent-Assisted)
1. **Product Detail** - Agent opens selected product page
2. **Price Analysis** - Compare 当前价 / 百亿补贴价 / 拼团价
3. **Service Verification** - Check 假一赔十, 退货包运费, 品质险
4. **Review Check** - Read recent reviews, photo reviews
5. **Group Decision** - Solo buy vs join group vs start group

### Phase 3: Cart & Pre-Order (Agent-Assisted with Login)
1. **Add to Cart** - Agent adds item to cart (requires login)
2. **Group Buy Action** - Initiate or join 拼团 (requires login)
3. **Cart Review** - Agent shows cart contents
4. **Coupon Application** - Agent checks platform + seller coupons
5. **Order Summary** - Agent generates complete order preview

### Phase 4: Checkout (User-Controlled)
1. **Handoff** - Agent presents final order details
2. **User Review** - User confirms all details
3. **Payment** - ⚠️ **User completes payment manually**
4. **Confirmation** - User shares order confirmation if desired

**Agent Boundary**: Stops at Phase 3. Never executes payment or final order submission.

## Browser Workflow Upgrade

When the user needs live PDD page validation, follow the shared **browser-commerce-base** workflow:
- public browsing → `openclaw`
- logged-in assets such as cart/orders/coupons → `user` only when necessary
- re-snapshot after subsidy overlays, 拼团 panels, or SKU switches
- capture service badges and compensation promises in screenshots

Key browser extraction order on PDD:
- 标题
- 当前价 / 百亿补贴价 / 拼团价
- 店铺类型
- 服务保障（假一赔十 / 退货包运费 / 品质险）
- 拼团门槛
- 发货承诺与评价风险

## Core Rules

### 1. Understanding PDD's Model

**Social Commerce + Group Buying:**

| Feature | How It Works | Benefit |
|---------|--------------|---------|
| **拼团** (Group Buy) | Join others for lower price | 10-40% savings |
| **百亿补贴** (Billion Subsidy) | Platform-subsidized deals | Guaranteed low prices |
| **砍价** (Price Chop) | Share to friends for discounts | Free/discounted items |
| **多多果园** (Orchard Game) | Gamified discounts | Play for coupons |

**Platform Positioning:**
- Lowest prices among major platforms
- Higher risk, requires more diligence
- Best for: non-branded goods, daily essentials, agricultural products
- Avoid for: high-end electronics, luxury, time-sensitive needs

### 2. Store Type Hierarchy

| Badge | Meaning | Trust Level |
|-------|---------|-------------|
| **品牌** (Brand) | Official brand store | ⭐⭐⭐⭐⭐ |
| **旗舰店** (Flagship) | Authorized flagship | ⭐⭐⭐⭐⭐ |
| **专卖店** (Specialty) | Category specialist | ⭐⭐⭐⭐☆ |
| **普通店** (Regular) | Individual seller | ⭐⭐⭐☆☆ |

**PDD-Specific Indicators:**

| Indicator | Good Sign |
|-----------|-----------|
| 假一赔十 | Counterfeit = 10x compensation |
| 退货包运费 | Free return shipping |
| 极速退款 | Fast refund processing |
| 品质险 | Quality insurance |

### 3. Group Buying Mastery

**How 拼团 Works:**

| Stage | Action | Time Limit |
|-------|--------|------------|
| **发起** (Initiate) | Start a group | 24 hours |
| **参团** (Join) | Join existing group | Until full |
| **成团** (Complete) | Minimum members reached | - |
| **发货** (Ship) | Order processes | 1-3 days |

**Group Size Typical:**
- Small: 2 people (easy to complete)
- Medium: 3-5 people
- Large: 10+ people (biggest discounts)

**Strategies:**
1. Join existing groups (faster)
2. Share with family/friends
3. Use PDD's "免拼" (skip group) for urgent orders
4. Check "即将成团" (about to complete) for quick wins

### 4. The 百亿补贴 Program

**What It Is:**
- Platform subsidizes prices
- Guaranteed lowest price
- Usually on branded goods
- Limited quantity/time

**How to Spot:**
- Look for "百亿补贴" red badge
- Prices often 20-50% below market
- Includes iPhones, Dyson, Nike, etc.

**Cautions:**
- Verify it's "官方补贴" (official subsidy)
- Check seller is authorized
- Compare with JD/Tmall prices
- Read recent reviews carefully

### 5. Seller Vetting on PDD

**Critical Checks:**

| Metric | Minimum Threshold | Ideal |
|--------|-------------------|-------|
| **店铺评分** | >4.5 | >4.7 |
| **销量** | >100 | >1000 |
| **评价数** | >50 | >500 |
| **店铺年龄** | >6 months | >1 year |

**Review Analysis:**
- Look for photo reviews (真实晒图)
- Check "默认" (default) reviews, not just "好评"
- Read 1-2 star reviews for common issues
- Verify "已拼" (grouped) count is high

**Red Flags:**
- No photo reviews
- Generic/duplicate review text
- Price too good to be true
- Store opened <3 months ago
- High return rate mentioned

### 6. Category-Specific Strategies

**Agricultural Products (农产品):**
- PDD's strength
- Direct from farmers
- Check origin (产地)
- Seasonal buying = best prices

**Daily Essentials:**
- Extremely competitive pricing
- Bulk buying saves more
- Generic brands often sufficient

**Electronics:**
- High risk category
- Only buy from 百亿补贴 or brand stores
- Verify warranty terms
- Record unboxing video

**Clothing:**
- Check size charts carefully
- Sizing often runs small
- Read "尺码反馈" (sizing feedback)
- Photo reviews essential

### 7. Payment & Protection

**Payment Options:**
- 微信支付 (WeChat Pay) - Most common
- 支付宝 (Alipay) - Also accepted
- 多多钱包 (PDD Wallet) - Occasional discounts

**PDD Buyer Protection:**

| Issue | Resolution |
|-------|------------|
| Wrong item | Full refund, keep or return |
| Quality issue | Refund or partial refund |
| Not received | Automatic refund after timeout |
| Counterfeit | 假一赔十 (10x compensation) |

**Return Policy:**
- 7-day return for most items
- 退货包运费 = free return shipping
- Some items non-returnable (food, custom)

## Common Traps

- **Joining any group without checking seller** → Quality varies wildly
- **Ignoring shipping times** → Can be 5-10 days
- **Assuming 百亿补贴 = always authentic** → Still verify seller
- **Not reading 1-star reviews** → Pattern of issues
- **Buying time-sensitive items** → Shipping slower than JD/Tmall
- **Forgetting to claim orchard rewards** → Free money
- **Impulse buying due to low prices** → Buy what you need

## PDD vs Other Platforms

| Factor | PDD | Taobao | JD |
|--------|-----|--------|-----|
| Price | Lowest | Medium | Highest |
| Quality | Variable | Variable | Consistent |
| Shipping | Slowest | Medium | Fastest |
| Authenticity | Riskier | Medium | Safest |
| Fun Factor | High (games) | Medium | Low |

**When to Use PDD:**
- Price is primary concern
- Buying everyday items
- Not in a hurry
- Willing to research sellers
- Agricultural products

## Agent Execution Guide

### When User Says "帮我买..." / "帮我下单..."

```
User: "帮我买拼多多的耳机"
  ↓
Step 1: Confirm Intent
  "我来帮你搜索拼多多的耳机，对比百亿补贴和拼团价，检查卖家信誉。
   最后需要你确认订单并完成支付。可以吗？"
  ↓
Step 2: Discovery Phase (No login required)
  - Search PDD for "耳机"
  - Filter: 百亿补贴, 品牌店
  - Check seller ratings (>4.5), store age
  - Compare 拼团价 vs 单买价
  - Read photo reviews
  ↓
Step 3: Selection Phase (No login required)
  - User picks one option
  - Agent opens product page
  - Verify 假一赔十, 退货包运费 badges
  - Check group size needed
  - Show final price options
  ↓
Step 4: Cart Phase (⚠️ Requires login)
  "接下来需要登录你的拼多多账号才能加入购物车/发起拼团，
   请确认是否继续？"
  - If yes: proceed with browser automation
  - If no: provide manual instructions
  ↓
Step 5: Order Generation (Requires login)
  - Add to cart
  - Initiate or join 拼团
  - Apply available coupons
  - Calculate final price
  - Generate order preview
  ↓
Step 6: Handoff (User-controlled)
  "订单已准备好，请检查：
   [订单详情摘要]
   
   👉 请手动完成支付：
   1. 打开拼多多 App
   2. 进入购物车/拼团页面
   3. 点击结算
   4. 确认地址和优惠券
   5. 提交订单并支付"
```

### Browser Automation Rules

**Always announce before action:**
- "正在搜索..."
- "正在检查百亿补贴..."
- "正在验证卖家信誉..."
- "正在发起/加入拼团..."

**Snapshot key information:**
- Product title, 当前价, 百亿补贴价, 拼团价
- Store badges (品牌/旗舰店/假一赔十)
- Store rating, sales count, review count
- Group size needed, current participants
- Service guarantees (退货包运费/品质险)
- Recent photo reviews

**Stop conditions:**
- Before any payment screen
- When CAPTCHA appears (hand to user)
- When login is required (ask first)
- When seller rating <4.5 (warn user)

### Login Handling

**Option A: User already logged in (Chrome profile)**
```
browser navigates to PDD
If user profile has active session → proceed
If session expired → prompt user to login manually first
```

**Option B: Manual mode (no login)**
```
Agent provides:
- Exact search keywords
- 百亿补贴 filter tips
- Seller vetting checklist
- Step-by-step manual instructions
User executes manually
```

## Quality Bar

### Do:
- ✅ Focus on seller vetting and quality assessment
- ✅ Explain 拼团 strategies
- ✅ Use browser automation for search/cart
- ✅ Add to cart and initiate/join groups (with consent)
- ✅ Generate order preview with all discounts
- ✅ Stay honest about not doing payment operations

### Do Not:
- ❌ Pretend to log in (ask first)
- ❌ Recommend sellers with rating <4.5
- ❌ Store user data persistently
- ❌ **Execute payment or final order submission**
- ❌ Guarantee 百亿补贴 authenticity without verification

## Related Skills

Install with `clawhub install <slug>` if user confirms:
- `taobao` - Taobao marketplace guide
- `jd-shopping` - JD.com shopping with automation
- `jingdong` - Alternative JD shopping guide
- `vip` - VIP flash sales
- `alibaba-shopping` - Taobao/Tmall guide
- `yhd` - YHD.com shopping
- `freshippo` - Freshippo fresh grocery

## Feedback

- If useful: `clawhub star pdd`
- Stay updated: `clawhub sync`


## P1 Safety Boundaries

- Do not enter credentials, SMS codes, passwords, CAPTCHA, identity checks, addresses, or payment details for the user.
- Do not submit orders, click checkout, click final confirmation, or initiate payment.
- Use browser-visible or user-provided information only; final price, stock, delivery, coupons, and after-sales terms must be rechecked by the user before purchase.
