# Feed Optimization Guide

## Overview

The product feed is the foundation of Google Shopping performance. Every impression, click, and conversion starts with Google matching a search query to your product data. A poorly optimized feed doesn't just reduce performance — it can prevent products from showing entirely. This guide covers attribute-by-attribute best practices, common errors and their fixes, and strategies for maximizing feed quality scores.

## Required Attributes

### Product Identity

**id**
- Must be unique and stable — never reuse IDs for different products
- Use the same ID consistently across feed updates (changing IDs loses product history)
- Alphanumeric, up to 50 characters
- Common mistake: Using variant IDs that change when inventory is restocked

**title** (Max 150 characters, first 70 most important)
- The single most impactful attribute for query matching and CTR
- Front-load the most important keywords — Google weights the beginning of titles more heavily
- Category-specific templates:

| Category | Template | Example |
|---|---|---|
| Apparel | Brand + Gender + Product Type + Feature + Color + Size | "Nike Women's Running Shoes Air Zoom Pegasus 40 Black Size 8" |
| Electronics | Brand + Product Type + Model + Key Spec + Variant | "Samsung 65-Inch 4K Smart TV OLED S95C 2024 Model" |
| Home & Garden | Brand + Product Type + Material + Dimensions + Color | "KitchenAid Stand Mixer 5-Quart Tilt-Head Artisan Series Empire Red" |
| Beauty | Brand + Product Name + Type + Size/Volume + Variant | "CeraVe Moisturizing Cream Face Body Lotion 19oz for Dry Skin" |
| Toys & Games | Brand + Product Name + Type + Age Range + Feature | "LEGO Star Wars Millennium Falcon Building Set 75375 Ages 18+" |

- Title optimization rules:
  1. Never start with promotional text ("Sale!", "Free shipping", "Best seller")
  2. Include the product type early (not just the brand name)
  3. Add size, color, material, and other variant-specific attributes
  4. Use common search terms, not internal jargon
  5. Don't repeat information already in other attributes
  6. Capitalize properly — don't use ALL CAPS

**description** (Max 5,000 characters)
- First 160 characters are critical — may display in free listings
- Include primary keywords naturally within the first two sentences
- Describe features, specifications, and use cases
- Avoid promotional language, HTML tags, or links
- Don't repeat the title verbatim — expand on it

**link**
- Must point directly to the product's landing page (not a category or search page)
- URL must be accessible to Googlebot (not behind login/paywall)
- Landing page price and availability must match the feed exactly
- Use canonical URLs to avoid duplicate content issues

**image_link**
- Minimum 100×100 pixels (250×250 for apparel), recommended 800×800+
- White or transparent background preferred for primary image
- Product must fill 75%+ of the image frame
- No text overlays, watermarks, borders, or promotional badges
- No placeholder or stock images
- File size under 16MB

**availability**
- Must match the landing page in real-time: "in_stock", "out_of_stock", "preorder", "backorder"
- Mismatches trigger disapproval — automate feed updates to sync with inventory
- For products frequently going in/out of stock, increase feed refresh frequency

**price**
- Must match the landing page price exactly (including currency)
- Include the correct currency code (e.g., "29.99 USD")
- If using sale pricing, submit both `price` (original) and `sale_price` (discounted)
- Price mismatches are the #1 cause of disapprovals — automate price sync

**brand**
- Required for all products with a recognized brand
- Use the brand name as consumers know it (not parent company name)
- For private label / unbranded products, use your store brand name

**gtin** (Global Trade Item Number)
- Required for all products with a manufacturer-assigned GTIN (UPC, EAN, ISBN, JAN)
- 8, 12, 13, or 14 digits depending on format
- Incorrect GTINs trigger disapproval — verify against the GS1 database
- For handmade/custom products with no GTIN: set `identifier_exists` to "no"

**condition**
- "new", "refurbished", or "used"
- Must match the landing page description
- Refurbished items need clear disclosure on the landing page

## Recommended Attributes (High Impact)

### additional_image_link (Up to 10 additional images)
- Add lifestyle images showing the product in use
- Include detail shots (close-ups of materials, features, textures)
- Show different angles and perspectives
- Include size/scale reference images
- Products with 3+ images see 15–30% higher CTR than single-image listings

### sale_price and sale_price_effective_date
- Triggers the "Sale" badge on Shopping ads — significantly improves CTR
- `sale_price`: The discounted price
- `sale_price_effective_date`: ISO 8601 format date range (start/end)
- Must reflect actual sale pricing on the landing page
- Remove sale_price when the promotion ends (stale sale prices trigger disapprovals)

### google_product_category
- Use the most specific category from Google's taxonomy (deepest level available)
- More specific categorization improves query matching accuracy
- Example: Don't use "Home & Garden" when "Home & Garden > Lawn & Garden > Gardening > Planters" is available
- Map every product — don't rely on Google's auto-classification

### product_type
- Your own product taxonomy (can differ from Google's)
- Used for organizing product groups in campaigns
- Use consistent, hierarchical naming: "Home > Outdoor > Planters > Raised Beds"
- Include 2–4 levels of hierarchy

### custom_label_0 through custom_label_4
- Five slots for business-specific tags
- Used for campaign segmentation and bid management
- Recommended labeling strategy:

| Slot | Purpose | Example Values |
|---|---|---|
| custom_label_0 | Margin tier | margin_high, margin_mid, margin_low |
| custom_label_1 | Performance tier | star_performer, core, long_tail, underperformer |
| custom_label_2 | Seasonality | seasonal_spring, seasonal_summer, seasonal_fall, seasonal_winter, evergreen |
| custom_label_3 | Promotion status | promo_active, clearance, full_price |
| custom_label_4 | Product lifecycle | new_launch, growth, mature, end_of_life |

### shipping
- Specify shipping cost and speed per product or at account level
- Free shipping products get a "Free shipping" badge — strong CTR signal
- Accurate shipping data prevents post-click abandonment
- Include all shipping methods available (standard, express, overnight)

### product_highlight (Up to 6 bullet points, 150 chars each)
- Key selling points displayed in free listings
- Focus on features that differentiate from competitors
- Include specifications shoppers compare (size, weight, compatibility)
- Use natural language, not keyword stuffing

## Feed Quality Scoring Framework

### Scoring Model

| Factor | Weight | Scoring Criteria |
|---|---|---|
| Required attribute completeness | 25% | All required attributes present and correctly formatted |
| Recommended attribute coverage | 20% | Percentage of recommended attributes populated |
| Title quality | 20% | Length (70+ chars), keyword inclusion, template compliance |
| Image quality | 15% | Resolution, background, product framing, additional images |
| Data accuracy | 10% | Price match, availability match, GTIN validation |
| Update freshness | 10% | Feed update frequency, time since last refresh |

### Score Interpretation

| Score | Assessment | Expected Performance |
|---|---|---|
| 90–100 | Excellent | Maximum impression share potential, competitive advantage |
| 75–89 | Good | Strong performance, minor optimizations remaining |
| 60–74 | Needs improvement | Missing significant opportunities, below-average placement |
| 40–59 | Poor | Major feed issues, many products underperforming or suppressed |
| Below 40 | Critical | Significant disapprovals, minimal Shopping visibility |

## Common Feed Errors and Fixes

### Disapproval: Price Mismatch

**Cause**: Feed price doesn't match landing page price (including tax/shipping if applicable).

**Fixes**:
1. Automate feed generation from the same pricing database that serves the website
2. Increase feed refresh frequency (at least every 6 hours for dynamic pricing)
3. Use the Content API for real-time price updates on high-velocity products
4. Verify that coupon/discount codes don't change the displayed price
5. Check for currency mismatches (especially for multi-country feeds)

### Disapproval: Missing Identifier (GTIN/MPN)

**Cause**: Products with manufacturer GTINs submitted without them.

**Fixes**:
1. Source GTINs from supplier catalogs, manufacturer databases, or product packaging
2. For products genuinely without a GTIN (custom, handmade, vintage): set `identifier_exists` to "no"
3. Verify GTIN accuracy against GS1 GEPIR database
4. Never fabricate or reuse GTINs across different products

### Disapproval: Image Violation

**Cause**: Images with text overlays, watermarks, promotional badges, wrong backgrounds, or poor quality.

**Fixes**:
1. Use clean product photos on white/transparent backgrounds for primary image
2. Move lifestyle images to `additional_image_link` slots
3. Remove all text, logos, and promotional overlays from the primary image
4. Ensure minimum resolution requirements are met (100×100, 250×250 for apparel)
5. Check that the product fills at least 75% of the image frame

### Warning: Missing Recommended Attributes

**Cause**: Products submitted with only required attributes, missing recommended ones.

**Fixes**:
1. Prioritize by impact: google_product_category > additional_image_link > sale_price > product_highlight
2. Batch-update categories using a mapping spreadsheet
3. Add lifestyle images from existing marketing materials
4. Configure custom labels for campaign segmentation

## Feed Management Best Practices

### Update Frequency

| Feed Type | Recommended Frequency | When to Increase |
|---|---|---|
| Full feed | Daily | Major catalog changes, seasonal transitions |
| Supplemental feed | Every 6 hours | Price changes, promotions, inventory updates |
| Content API | Real-time | High-velocity products, dynamic pricing |
| Inventory feed | Every 4–6 hours | Products frequently going in/out of stock |

### Multi-Country / Multi-Language Feeds

- Create separate feeds per target country + language combination
- Translate titles and descriptions (don't just change currency and shipping)
- Use country-specific GTINs where applicable
- Verify compliance with local product data requirements (EU energy labels, etc.)
- Set up separate Merchant Center accounts or sub-accounts per country if needed

### Supplemental Feeds

Use supplemental feeds to:
- Add/update custom labels without touching the primary feed
- Apply promotional pricing on a schedule
- Override specific attributes for testing (e.g., title A/B testing)
- Add product_highlight and product_detail attributes separately from the main feed
- Manage seasonal attribute changes (descriptions, images)

Supplemental feeds merge with the primary feed using the `id` field as the key. They can add or override attributes but cannot create new products.
