---
name: instagram-ins-ecommerce-image-generation-editing
description: "Create and edit Instagram Shop product posts, carousel stories, Reels covers, Stories, creator seeding assets and cohesive social-commerce grids. Use this skill for Instagram电商图片、INS商品图、Instagram Shop、Feed帖子、Carousel轮播、Story、Reels封面、UGC种草、社交广告和品牌账号视觉；supports AI Hive reference generation."
---

# Instagram INS Ecommerce Image Generation and Editing

Build a social-commerce narrative rather than copying one listing image into every placement. Feed, carousel, Stories, Reels cover and creator assets should share a product and brand system while each performs a different communication job.

## Social brief

Define audience, product truth, brand palette, feed style, content pillar, approved claim, target action and creator rights. Decide whether the asset is organic, shoppable, creator seeding or paid. Product tags, prices, handles and stickers are platform/UI data and should not be generated into the image.

## Scenarios and commands

### 1. Shoppable feed post

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Instagram Shop feed image for the reference product. Preserve exact product, package, color and logo. Show one aspirational but credible use moment, strong square crop, recognizable product and calm caption-safe area. Do not generate product tag, handle, price, likes, comments or platform UI.' \
  --image /path/to/product.png
```

### 2. Educational carousel

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create a 5-slide Instagram carousel visual system: problem context, product introduction, how-to step, detail proof and final use result. Keep the same product and brand palette; each slide has one clear image task and blank concise-copy area. No fabricated claim, review or UI.' \
  --image /path/to/product.png \
  --batch 5
```

### 3. Reels cover

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Vertical Instagram Reels cover showing the product in action, with one strong focal point and clean short-title area that remains legible in profile-grid crop. Preserve product accuracy and keep key content away from edge overlays; no play icon, view count or handle.' \
  --image /path/to/product.png
```

### 4. Stories launch sequence

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create three Instagram Stories launch bases: teaser detail, full product reveal, real use scene. Maintain product and visual identity, vertical safe zones and blank areas for approved poll/link/CTA stickers. Do not generate sticker UI, countdown, price or availability.' \
  --image /path/to/product.png \
  --batch 3
```

### 5. Creator seeding pack

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create four creator-ready reference assets: accurate cutout, in-hand scale, key material detail and natural lifestyle use. Keep product consistent and give flexible negative space; do not fabricate creator identity, testimonial, caption, partnership label or result.' \
  --image /path/to/product.png \
  --batch 4
```

## Social QA

- Product and brand remain consistent across placements.
- Feed, carousel, Story and cover each have a distinct job.
- Profile-grid and vertical crops preserve the subject and title space.
- Handles, tags, stickers, prices and UI are added in the platform or design tool.
- No fabricated engagement, creator endorsement, claim or result.
- Confirm rights and current Instagram commerce/advertising rules before posting.

## Run

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name instagram-ins-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

The image CLI supports references, batches, live parameters, routing, output directory and submit-only tasks. Export separate source masters for each placement rather than relying only on automatic crops.
