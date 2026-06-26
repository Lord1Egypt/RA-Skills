---
name: storefront-cro
description: Analyze and optimize your Mobazha storefront for higher conversion rates. Use when your store isn't converting visitors to buyers, or when you want to improve sales performance.
---

# Storefront Conversion Rate Optimization (CRO)

Analyze your Mobazha store's setup and provide actionable recommendations to turn more visitors into buyers.

## When to Use

- "My store has traffic but few sales"
- "How can I improve my store's conversion?"
- "Why aren't people buying?"
- After initial setup, to audit your storefront
- Before a product launch or marketing push

## How It Works

The agent reads your store data via MCP tools, analyzes it against proven e-commerce CRO principles, and provides prioritized recommendations you can implement immediately.

## Assessment Framework

### Step 1: Gather Store Data

The agent calls these MCP tools to audit your store:

| Tool | What It Reveals |
|------|----------------|
| `profile_get` | Store name, about, avatar, header image |
| `listings_list_mine` | Product catalog: titles, prices, images, descriptions |
| `settings_get_storefront` | Store configuration and enabled features |
| `orders_get_sales` | Sales history and patterns |
| `exchange_rates_get` | Pricing context |

### Step 2: Analyze Across CRO Dimensions

#### 1. First Impression (Highest Impact)

**Check:**

- Can a visitor understand what you sell within 5 seconds?
- Is the store name clear and memorable?
- Does the `shortDescription` communicate value?
- Is the header image professional and relevant?
- Does the avatar build trust (logo or personal photo)?

**Common issues:**

- Generic or empty store descriptions
- Missing or low-quality header/avatar images
- Store name that doesn't communicate what you sell

#### 2. Product Catalog Quality

**Check:**

- Do listings have clear, descriptive titles?
- Are product images high-quality and showing the product well?
- Do descriptions focus on benefits, not just features?
- Is pricing clear and competitive?
- Are variants (size, color) properly configured?
- Are tags filled in for search discoverability?

**Common issues:**

- Single product image (multiple angles convert better)
- Missing `shortDescription` (hurts search card appearance)
- No tags (invisible in marketplace search)
- Copy-pasted or minimal descriptions

#### 3. Trust Signals

**Check:**

- Does the About section tell a credible story?
- Are there ratings/reviews from past buyers?
- Is contact information provided?
- Are policies (shipping, returns) clearly stated?
- Is escrow protection mentioned to reassure first-time buyers?

**Common issues:**

- Empty About section
- No mention of escrow/buyer protection
- No shipping information

#### 4. Pricing and Perceived Value

**Check:**

- Are prices appropriate for the target market?
- Is the value clear relative to price?
- Are crypto and fiat options both enabled?
- Are there any promotions or bundles?

#### 5. Product Organization

**Check:**

- Are products organized into logical collections?
- Is the catalog easy to browse?
- Are featured/best products prominently placed?
- Is there a good mix of price points?

#### 6. Mobile Experience

**Check:**

- Are images properly sized for mobile?
- Are descriptions readable on small screens?
- Is the purchase flow smooth on mobile / Mini App?

## Output Format

### Quick Wins (Do Today)

Low-effort changes with immediate impact. Examples:

- Add missing product images
- Write `shortDescription` for products missing it
- Add tags to all listings
- Upload a professional header image

### High-Impact Changes (This Week)

Bigger changes that significantly improve conversions:

- Rewrite store About section (use `store-copywriting` skill)
- Improve product descriptions (use `product-description` skill)
- Add more product images from different angles
- Set up collections to organize your catalog

### Strategic Improvements (This Month)

Longer-term optimizations:

- Build review history through excellent service
- Add complementary products for cross-selling
- Create seasonal or themed collections
- Consider digital goods to diversify

### Specific Rewrites

For key elements, provide 2-3 alternatives with rationale:

- Store headline / `shortDescription`
- Top product descriptions
- About section

## Scoring Rubric

Rate each dimension 1-5:

| Dimension | 1 (Poor) | 3 (Average) | 5 (Excellent) |
|-----------|----------|-------------|----------------|
| First Impression | No images, generic name | Basic images, clear name | Professional branding, compelling tagline |
| Catalog Quality | Single image, no descriptions | Multiple images, basic copy | Rich media, benefit-focused copy, tags |
| Trust | Empty profile, no history | Some info, few reviews | Complete profile, reviews, policies |
| Pricing | Unclear, no fiat option | Clear pricing, single currency | Competitive, multi-currency, value articulated |
| Organization | Flat list, no collections | Some grouping | Collections, featured products, logical flow |

## Integration with Other Skills

| After CRO Audit | Use This Skill |
|-----------------|----------------|
| Product descriptions need work | `product-description` |
| Store About needs rewriting | `store-copywriting` |
| Need product images | `product-image-prompt` |
| Want to import more products | `product-import` |
| Need to update via MCP | `store-management` |

## Example Prompts

> "Audit my store and tell me how to get more sales."
>
> "I have 20 products but zero sales this month. What's wrong?"
>
> "Review my top 5 listings and suggest improvements."
>
> "Score my store's conversion readiness and give me a priority list."
