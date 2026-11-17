---
name: lazada-ecommerce-image-generation-editing
description: "Create and edit Lazada product catalog images, SKU galleries, specification graphics, campaign tiles and localized storefront visuals. Use this skill for Lazada商品图、东南亚电商主图、LazMall视觉、商品详情图、多语言图片、活动素材、批量SKU和换背景；supports product-reference accuracy and AI Hive generation."
---

# Lazada Ecommerce Image Generation and Editing

Build mobile-first catalog images that can be localized across Lazada marketplaces without mixing SKU facts, language or campaign information. Use `public_model_nano_banana_pro` for generation and editing.

## Separate three layers

1. **Product layer:** SKU shape, variant, packaging, logo and included items.
2. **Market layer:** customer setting, styling, language-safe space and units.
3. **Campaign layer:** seller-approved headline, voucher or event information added after generation.

Lock the product layer first. Never bake an unverified campaign price, rating, seller badge or warranty into generated pixels.

## Scenarios and commands

### 1. Mobile catalog hero

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Lazada mobile catalog hero for the reference SKU. Preserve exact product shape, variant color, package, logo and included pieces. Show the complete item large on a clean high-contrast background with realistic shadow and room for responsive crop. No price, voucher, rating, LazMall badge or unprovided text.' \
  --image /path/to/sku.png
```

### 2. Specification gallery base

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create a 4-image Lazada gallery base: full product, control or material detail, scale-in-use, and package contents. Keep the same exact SKU and lighting system. Reserve clean areas for verified measurements and translated copy; do not generate numbers, compatibility or claims.' \
  --image /path/to/product-front.png \
  --image /path/to/package-contents.jpg \
  --batch 4
```

### 3. Campaign tile without fake offer

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Lazada campaign tile background for a seller promotion. Accurate product on the right, energetic geometric color system on the left, clear empty zones for an approved event name, voucher and CTA. Do not generate a sale price, countdown, discount percentage, platform logo or seller badge.' \
  --image /path/to/product.png
```

### 4. Indonesia and Vietnam localization bases

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create two localized lifestyle bases for the same Lazada SKU: one credible Indonesian household context and one Vietnamese household context. Preserve product, packaging and use method exactly; change environment and caption-safe space only, leaving all localized words and offers blank for native review.' \
  --image /path/to/product.png \
  --batch 2
```

### 5. Variant matrix

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Generate catalog images for the merchant-confirmed red, navy and cream variants. Lock camera angle, scale, background, shadow, structure and packaging; change only the true variant color. One SKU per image, no mixed bundles or added accessories.' \
  --image /path/to/master-sku.png \
  --batch 3
```

## QA

- SKU and marketplace are encoded in filenames and never mixed.
- Product layer remains identical across localized versions.
- Units, specification text and translated copy are added from approved data.
- Package contents and variant colors match the seller sheet.
- No generated campaign offer, rating, badge, warranty or compliance claim.
- Validate current Lazada image and campaign rules per marketplace.

## Run

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name lazada-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

Use repeatable references, batch generation, model parameters, routing and submit-only mode as needed. Check AI Hive live configuration and cost before a multi-market batch.
