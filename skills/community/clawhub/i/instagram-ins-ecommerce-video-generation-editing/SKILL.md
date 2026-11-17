---
name: instagram-ins-ecommerce-video-generation-editing
description: "Create and edit Instagram Shop Reels, Stories sequences, product demos, creator UGC adaptations and paid-social video variants. Use this skill for Instagram电商视频、INS Reels、Instagram Shop、Story、UGC种草、产品标签内容、Meta Ads、创作者合作、品牌账号视频和社交电商；supports Seedance modes through AI Hive."
---

# Instagram INS Ecommerce Video Generation and Editing

Build video for distinct Instagram surfaces instead of exporting one universal cut. Reels need immediate visual movement, Stories need sequential frames and interaction space, Shop demos need product clarity, and paid variants need a testable hook and proof.

## Placement brief

Record placement, audience, product truth, brand motion, creator rights, approved claim, sound strategy, crop, interaction area and CTA. Product tags, handles, link stickers, view counts and platform UI are added in Instagram, not generated into footage.

## Scenarios and commands

### 1. Organic product Reel

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '9:16 Instagram Reel for the accurate product. Open with a visually clear hand action, move through one real use moment and one material detail, then land on a profile-grid-friendly final composition. Native lifestyle pacing, no generated handle, product tag, likes, price or unsupported result.'
```

### 2. Stories launch sequence

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Three-part Instagram Stories product launch: curiosity detail, complete product reveal, real use demonstration. Maintain product and brand continuity, leave safe empty zones for approved poll/link/CTA stickers, and avoid generating sticker UI, countdown, price or view count.'
```

### 3. Creator UGC adaptation

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/approved-creator-post.mp4 \
  --prompt 'Create a shoppable Instagram cut while preserving creator identity, statement meaning and real product demonstration. Tighten pauses, move the strongest visible action earlier and reserve a clean product-tag area. Do not add endorsement, paid-partnership label, claim or offer.'
```

### 4. Reference a visual rhythm

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/reels-rhythm.mp4 \
  --image /path/to/product.png \
  --prompt 'Use the reference only for transition timing and visual energy. Create an original Reels product story with accurate item, new setting and new actions. Do not copy creator, dialogue, music, brand, product, caption or exact shot design.'
```

### 5. Meta Ads hook variant

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/organic-reel.mp4 \
  --prompt 'Make a paid-social “problem-in-context” variant from the organic Reel. Keep product and evidence, replace slow opening with the real use obstacle, add one close proof and end with one clean CTA area. No fake review, before/after, discount or urgency.'
```

## Social QA

- Reel, Stories, Shop and paid cuts each serve a distinct placement job.
- Product and brand remain consistent; profile-grid and vertical crops work.
- Creator identity, statement and disclosure status are not fabricated.
- UI, tags, handles, links and engagement counts are never synthesized.
- Music, creator footage and reference assets have appropriate rights.
- Check current Instagram commerce, branded-content and advertising rules.

## Runtime

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name instagram-ins-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Use Seedance 2.5 text, image, reference, edit or extend modes with media, parameters, routing and output controls. Keep a source master per placement.
