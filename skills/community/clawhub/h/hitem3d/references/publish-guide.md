# Hitem3D Publish Guide

## One-line positioning
Turn images into production-grade 3D assets from chat, with smart defaults, multi-view support, batch automation, and cost-aware execution.

## What makes this skill strong

- Outcome-first: it prefers submit → wait → download instead of dumping task IDs
- Intent routing: distinguishes single-image, portrait, multi-view, 3D-print, AR, and batch flows
- Cost-aware: warns before expensive runs and uses sane defaults for normal jobs
- Operator-style UX: reports saved path, format, model, resolution, and estimated credits
- Production-minded: validates files early, blocks invalid model/type combos, and avoids leaking secrets

## Current truth

This skill is strong at the design, workflow, and packaging level.
It is not yet fully live-validated end to end because real Hitem3D API credentials were not available during this audit.
Do not market it as battle-tested until the live checklist in `references/live-validation.md` is completed.

## Best-fit users

- AIGC 3D teams
- E-commerce and product-visual teams
- 3D printing workflows
- Game / toy / collectible concept pipelines
- AR content teams that need GLB or USDZ export

## Example prompts

- 把这张产品图变成 3D
- 给我一个 STL，我要拿去打印
- 这 4 张前后左右图生成一个更准的模型
- 把 designs/ 里的图全部转成 GLB
- 查下 Hitem3D 还剩多少积分

## Recommended ClawHub listing copy

### Title
Hitem3D

### Short description
Image-to-3D generation for OpenClaw. Turn photos, renders, portraits, and multi-view image sets into downloadable 3D assets with smart mode selection, batch support, and cost-aware defaults.

### Long description
Hitem3D is a production-oriented OpenClaw skill for turning images into usable 3D assets without forcing the user into a browser workflow.

It supports:
- single-image object generation
- portrait / bust generation
- multi-view reconstruction from 2–4 images
- printable STL export
- AR-ready GLB / USDZ output
- batch folder processing
- credit balance checks
- unattended wait + download flows

Unlike a thin API wrapper, this skill is designed to behave like a 3D operator. It picks sane defaults, separates multi-view from batch, warns before expensive runs, validates inputs early, and returns useful outputs like saved file path, output format, model, resolution, and estimated credit cost.

### Trust note
This skill has been audited for structure, flow, and safety. Complete the live-validation checklist before claiming full production validation in public marketing.

## Publish checklist

- Keep `SKILL.md` concise and trigger-rich
- Keep detailed product/marketing copy in references, not SKILL body
- Ship only necessary files
- Publish from a clean staging folder, not directly from a backup/archive tree
- Exclude local backup metadata such as `_meta.json` and `.clawhub/` from release packages
- Run validation and packaging before publish
- Finish live API validation before claiming production-proof reliability
