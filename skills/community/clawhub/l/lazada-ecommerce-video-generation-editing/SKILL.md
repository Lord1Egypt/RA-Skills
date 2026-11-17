---
name: lazada-ecommerce-video-generation-editing
description: "Create and edit Lazada product listing videos, localized demonstrations, LazMall brand clips and campaign-ready seller assets. Use this skill for Lazada商品视频、东南亚电商视频、商品详情演示、多语言版本、LazMall内容、活动素材、开箱和跨市场本地化；supports generation, reference, editing and AI Hive delivery."
---

# Lazada Ecommerce Video Generation and Editing

Produce one accurate product demonstration, then create marketplace-specific versions without mixing languages, variants, package contents or campaign facts.

## Localization matrix

For every task record marketplace, language, SKU, package list, approved benefit, correct usage, units, seller type and destination. Keep visual product truth separate from captions and offers so local teams can review copy independently.

## Scenarios and commands

### 1. Listing demonstration master

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt 'Lazada mobile listing video master. Preserve exact SKU, variant, packaging, logo and included parts. Show complete product, one correct setup, one feature detail and final use context with simple visual sequencing and caption-safe zones. No price, voucher, rating, warranty or unsupported claim.'
```

### 2. Bahasa Indonesia localized version

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/listing-master.mp4 \
  --prompt 'Localize the master for Lazada Indonesia. Preserve product, demonstration, timing of proof and commercial facts; adapt household context and reserve clean areas for merchant-approved Bahasa Indonesia captions. Remove old-market words and do not invent voucher, warranty, units or claims.'
```

### 3. LazMall brand-store clip

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Short LazMall brand-store clip connecting three approved products through one morning routine. Keep each SKU visually distinct and accurate, use consistent brand color and calm mobile pacing, end on a clean brand collection composition. No platform badge, sale event, review or guarantee.'
```

### 4. Campaign-ready video base

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/campaign-rhythm.mp4 \
  --image /path/to/product.png \
  --prompt 'Use the reference only for energetic edit rhythm and transition timing. Create an original Lazada seller campaign base with accurate product action and empty regions for approved event, voucher and CTA overlays. Do not copy branding, music, price, countdown or text.'
```

### 5. Clarify package contents

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/unboxing-short.mp4 \
  --prompt 'Extend the unboxing by placing every included component in a clear row and showing first setup. Preserve quantity, connector type, labels, hands and table continuity. Do not add a gift, spare part or accessory.'
```

## QA

- Marketplace, language, SKU, units and package list remain linked.
- Demonstration follows real instructions and supports the stated benefit.
- Localized versions preserve commercial meaning and product identity.
- Offers and translated copy use merchant-approved text only.
- No generated badge, rating, warranty, voucher, price or unsupported result.
- Check current Lazada seller and campaign requirements per marketplace.

## Runtime

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name lazada-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

The CLI supports Seedance 2.5 generation, reference, editing and extension modes, media uploads, live parameters, routing and submit-only tasks. Validate one market before batching.
