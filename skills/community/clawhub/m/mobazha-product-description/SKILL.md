---
name: product-description
description: Generate SEO-optimized, conversion-focused product descriptions for your Mobazha store. Use when creating new listings, improving existing copy, or bulk-generating descriptions for imported products.
---

# Product Description Generator

Generate high-converting product descriptions tailored for your Mobazha store. Works with the MCP `listings_create` and `listings_update` tools to publish directly.

## When to Use

- Writing description for a new listing
- Improving copy on existing products
- Generating descriptions after bulk import (see `product-import` skill)
- Translating descriptions for international buyers

## Description Structure

Follow this proven structure for Mobazha listings:

1. **Hook** — Attention-grabbing opening line
2. **Problem/Need** — What pain point does this solve?
3. **Solution** — How the product helps
4. **Features to Benefits** — What it does → why it matters
5. **Use Cases** — When and how to use it
6. **Specifications** — Technical details, materials, dimensions
7. **Trust Signals** — Warranty, guarantees, escrow protection
8. **CTA** — Clear next step for the buyer

## Mobazha Field Mapping

| Field | Guidelines | Max Length |
|-------|-----------|-----------|
| `title` | Primary keyword first, specific and descriptive | ~140 chars |
| `shortDescription` | One-sentence hook — appears in search results and cards | ~160 chars |
| `description` | Full product story with HTML formatting | No hard limit |
| `tags` | Relevant search terms for marketplace discovery | 10-15 tags |

## Quick Start

### Generate for a New Product

Tell your AI agent:

> "Write a product description for [product name]. Key features: [list]. Target audience: [who]. Tone: [professional/conversational/playful/luxury]."

The agent will produce:

- Title with primary keyword
- Short description (tagline)
- Full description (HTML)
- Suggested tags

### Improve an Existing Listing

> "Get my listing [slug] and improve the description. Focus on benefits over features."

The agent calls `listings_get` → rewrites → `listings_update`.

### Bulk Generate After Import

> "List my products and generate better descriptions for any that have short or generic descriptions."

## Writing Principles

### Benefits Over Features

| Feature (weak) | Benefit (strong) |
|----------------|-----------------|
| "100% organic cotton" | "Breathes naturally — stays comfortable all day in any climate" |
| "256GB storage" | "Store your entire music library, photo collection, and apps without ever worrying about space" |
| "Handmade ceramic" | "Each piece is one-of-a-kind, crafted by artisans with decades of experience" |

### Tone Guidelines

| Tone | Best For | Example |
|------|----------|---------|
| **Professional** | Tech, B2B, high-ticket | "Engineered for performance. Backed by rigorous testing." |
| **Conversational** | Consumer, lifestyle | "You're going to love how this fits into your daily routine." |
| **Playful** | Trendy, youth-oriented | "Ready to level up your style game? Let's go." |
| **Luxury** | Premium, designer, artisan | "Experience unparalleled craftsmanship. A statement piece." |

### Mobazha-Specific Trust Elements

Mobazha stores have unique trust advantages. Weave these into descriptions where relevant:

- **Escrow protection** — "Your payment is held in escrow until you confirm delivery"
- **Decentralized** — "Buy directly from the creator — no middlemen, no commissions"
- **Crypto + fiat** — "Pay with crypto or credit card — your choice"
- **Privacy** — "No tracking, no data harvesting — just a fair transaction"
- **Peer reviews** — "Verified on-chain ratings from real buyers"

### SEO for Mobazha Search

- Place the primary keyword in the first 5 words of the title
- Include it naturally in the first sentence of `description`
- Use long-tail variations in `tags`
- Fill `shortDescription` — it's shown in search result cards

## Product Type Templates

### Physical Goods

```
Title: [Primary keyword] — [Key benefit or differentiator]
Short: [One-sentence value proposition]
Description:
  - Hook (why this product matters)
  - Material/build quality
  - Key features → benefits (3-5)
  - Size/dimensions/weight
  - Care instructions
  - Shipping note
Tags: [material], [category], [use-case], [style], [audience]
```

### Digital Goods

```
Title: [What it is] — [Instant delivery callout]
Short: [What you get + format]
Description:
  - What's included (file list, formats)
  - Who it's for
  - How to use it
  - Sample/preview mention
  - Instant delivery via Mobazha
Tags: [format], [category], [skill-level], [tool-compatibility]
```

### Services

```
Title: [Service name] — [Outcome promised]
Short: [What you deliver + timeframe]
Description:
  - What the service includes
  - Process/timeline (3-4 steps)
  - What the buyer needs to provide
  - Deliverables and format
  - Revision policy
Tags: [service-type], [industry], [turnaround], [expertise]
```

## Avoid These Mistakes

- **All caps titles** — Looks spammy; use title case instead
- **Keyword stuffing** — Write for humans first, search second
- **Vague claims** — "Best quality" means nothing; be specific
- **Missing specs** — Buyers need dimensions, materials, compatibility
- **No CTA** — Always end with a clear next step
- **Fabricated reviews** — Never invent testimonials or statistics
- **Ignoring mobile** — Most Mobazha browsing happens on mobile; keep paragraphs short

## Integration with Other Skills

| After | Use This Skill To |
|-------|-------------------|
| `product-import` | Generate better descriptions for imported products |
| `store-onboarding` | Write your store's About section and first listing |
| `store-management` | Update listings via MCP with improved copy |

## Example Prompt

> "I'm selling handmade leather wallets. They're made from full-grain vegetable-tanned leather, hand-stitched with waxed thread, slim bifold design, fits 6 cards + cash. Target: men 25-45 who appreciate craftsmanship. Tone: luxury. Generate a complete Mobazha listing."

The agent should produce a title, short description, full HTML description, and tags — ready to publish via `listings_create`.
