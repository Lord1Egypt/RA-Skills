---
name: Lead Gen Seller
slug: lead-gen-seller
description: Find B2B leads and write outreach messages for manufacturing/OEM agents. Targets indie beauty brands, skincare companies, and consumer product brands that need manufacturing partners. Generates prioritized lead lists + personalized email templates.
author: taoorchestrator
version: 1.0.0
tags:
  - lead-generation
  - b2b-sales
  - outreach
  - manufacturing
  - beauty
  - skincare
---

# Lead Gen Seller

Find high-quality B2B leads and write personalized outreach messages. Built for agents selling manufacturing, OEM, or B2B services.

## What It Does

1. **Researches target companies** using web search and public sources
2. **Builds prioritized lead lists** with brand name, website, products, and priority level
3. **Generates personalized cold email templates** tailored to each brand

## How to Run

### Step 1: Identify Your Target Industry

Common verticals this skill handles well:
- **Beauty/Skincare brands** (sunscreen, clean beauty, indie makeup)
- **Consumer products** (supplements, personal care, CBD)
- **Fashion/Apparel** (private label manufacturing)

### Step 2: Research Leads

Use web search to find brands matching your target profile:

```
# Find indie beauty brands on Shopify
site:shopify.com "skincare" "contact" "wholesale"
site:shopify.com "beauty brand" "founder"

# Find Kickstarter/Indiegogo funded beauty brands
site:kickstarter.com beauty skincare
site:indiegogo.com skincare beauty

# Find brands by Instagram hashtag (manual check)
# #beautybrand #skincarebrand #indiebeauty #cleanbeauty
```

### Step 3: Build Lead List

For each brand, collect:
| Field | Where to Find |
|-------|--------------|
| Brand Name | Website header, Instagram bio |
| Website | Instagram bio, search results |
| Instagram | Search on IG or whatrunson.shop |
| Products | Homepage, "Shop" page |
| Founder Name | "About" page, LinkedIn |
| Priority | Based on size, stage, product fit |

### Step 4: Generate Outreach Template

Use this template structure, customized per brand:

```
Subject: Partnership Opportunity - [Specific Product] Manufacturer

Hi [Founder Name],

I came across [Brand Name] and was impressed by [specific thing they make or stand for].

I'm reaching out because we may be able to help you scale [specific product type].

We're [Your Company] - [key credentials]. We specialize in:
✅ [Specialty 1]
✅ [Specialty 2]
✅ [MOQ and timeline]

We've helped brands like [similar brand] scale from concept to [outcome].

Would you be open to a 15-minute call this week?

Best,
[Your Name]
```

## Ideal Client Profile Template

Fill this in before researching:

**Looking for brands that:**
1. Have [e-commerce platform] or similar store
2. Active on [Instagram/LinkedIn/etc] ([follower threshold]+)
3. Sell [product category]
4. MOQ likely [range] units
5. Located in [target geography]
6. [Any other qualifier]

**Red flags (avoid):**
- No website or social media
- Massive brand (too big for SMB-friendly manufacturer)
- Dropshipping model (no real inventory)

## Example: Beauty Brand Lead List

```
# 🎯 Beauty Brand Leads - OEM Manufacturing

## High Priority (Indie, Growing)

| Brand | Website | Products | Why Good Lead |
|-------|---------|----------|--------------|
| Brand A | branda.com | Clean SPF | Growing, likely needs manufacturer |
| Brand B | brandb.com | Skincare | VC-backed, scaling |
| Brand C | brandc.com | Indie makeup | Small MOQ, founder-led |

## Medium Priority

| Brand | Website | Products | Why Good Lead |
|-------|---------|----------|--------------|
| Brand D | brandd.com | Beauty | Established but could be expanding |
```

## Tips for Higher Response Rates

1. **Reference something specific** about their brand (a product, campaign, review)
2. **Lead with value, not pitch** - "We helped brands like X do Y" is stronger than "we make Z"
3. **Keep it short** - 150 words max for cold email
4. **Follow up once** - 5-7 days after first email
5. **Find founder's name** - "Hi Sarah" beats "Hi there" by 40%+

## Requirements

- Web search tool (Brave or Tavily)
- Web fetch tool for digging into brand websites
- Target company description from the agent/user

## Common Use Cases

- Selling OEM manufacturing services (skincare, supplements, etc.)
- Finding clients for import/export agents
- B2B lead generation for SaaS tools targeting SMBs
- Partner recruitment for marketplaces

---

*Based on real B2B lead gen work for YP Fine Chemical USA (Tao's skincare manufacturing business)*
