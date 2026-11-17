# Photo Imprint (印痕)

> Keep the photo, remember it in a different stroke.

[简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

You shot a week of travel — cups, streets, cabin windows. You want one journal carousel for IG / Xiaohongshu, not ten mismatched filters. Direct prompting makes a pretty picture but the small cup becomes big and the street invents a tower.

`locoda/photo-imprint-skill` · English skill, Chinese name 印痕

```
Please help me install this skill: https://github.com/locoda/photo-imprint-skill
```

![license MIT](https://img.shields.io/badge/license-MIT-green) ![version 1.6.0](https://img.shields.io/badge/version-1.6.0-blue) ![tests 34 gates](https://img.shields.io/badge/tests-34%20gates-lightgrey)

| Photo Imprint (bottom-center, caption above — sample) | Source (blurred 12px for privacy) |
|---|---|
| ![imprint 01](assets/samples/01-sjc-small-cup-paper-locked-v11.webp) | ![source 01](assets/samples/source-01.webp) |
| Same small cup, lid locked, 50% paper-white, bottom-center | SJC small cup |
| ![imprint 02](assets/samples/02-in-flight-paper-locked-v11.webp) | ![source 02](assets/samples/source-02.webp) |
| Cabin simplified to cool wash, no invented skyline | In-flight cup |
| ![imprint 03](assets/samples/03-roppongi-paper-locked-v11.webp) | ![source 03](assets/samples/source-03.webp) |
| Background strongly simplified, no Tokyo Tower invented | Roppongi street cup |

All samples webp <100KB in `assets/samples/`. Full finals 1152×2048 jpg ~400KB, no EXIF/GPS/XMP.

## When 10 loose travel photos finally look like one journal

**You:** You have 10 photos from Japan — small cups, in-flight trays, Roppongi streets. You want to post a carousel, but originals are messy, you don't want to show faces, and you don't want the model to invent a Tokyo Tower. You tried one prompt for all and the cup changed size on page 2.

**Photo Imprint:** Locks silhouette, proportions, cap/lid, logo position for every page. It shows 8 real style thumbnails, you pick one, it builds a production plan and renders only page 1. You see the plan + sample together, with 6-field style contract, and approve with your exact words before any batch.

**Now you can:** Judge the whole set from one page, keep the small cup small across all pages, and get a verified ZIP where all pages share the same warm paper #F1EBDD, 55% top whitespace, bottom-center placement, and no invented facts.

## How to talk to your AI

You don't run scripts. Your AI does.

**Install once:**
```
Please help me install this skill: https://github.com/locoda/photo-imprint-skill
```
(You already have it above — this block is for copy-paste.)

**Start a set:**
> I have 10 photos from Japan in /path/to/photos, make them watercolor journal, keep cups small, bottom-center, 55% top whitespace, no caption. Preserve cup height and logo position.

**Pick a style:**
> Use sumi-e-ink / 你定 / use default watercolor

**Approve:**
> Approve page 1, continue / 批准第1张，继续

**Fix one page:**
> Page 2 background too busy, simplify / 第2张背景太满，简化一下

**Change style (goes back to style gate, expected):**
> Change to hiroshige-bokashi / 换成广重去雨版

Tips: Small cup stays small is locked by default. Captions are EXIF-confirmed only — say "no caption" if you don't want them. Private references stay local unless you say "you may upload to X".

## How it works

### Lock what matters, abstract only the stroke

Source photo is authority. Template B `drink-minimal` and Template A `travel-scene` now both use bottom-center flow: subject centered at y=0.72, 1152×2048, warm paper, 50% blank minimum. Shape-lock preserves cup/bottle silhouette, height, lid, logo position. Abstraction is only in brushwork, with 2–3 edge bleeds ≤10% width right / ≤8% height bottom, colors sampled from subject itself. No hand, cloth, invented skyline, or open-book mockup.

### One style, frozen contract, no blending

Eight bundled style packs contribute only technique, never subjects: `watercolor-journal` (default), `blue-lavender-watercolor`, `highway-485-lithograph`, `sumi-e-ink` (Zeshin 1847), `hiroshige-bokashi` (Hiroshige 1833 no-rain), `seurat-conte` (Seurat 1882). Single-select only. Choice is recorded in `work/style_choice.json` with `selected`, `user_delegated`, `timestamp`, `alternatives_shown`, frozen into `work/sample_style_contract.json` 6 keys. Batch prompts hash-lock style choice, contract, render-plan locks, and source hashes. Blending is rejected.

### Plan + sample gate, you stay in control

Not a prompt collection. A gated workflow: EXIF order → per-page `production_brief` (preserve / simplify / omit) → `production-plan.md` → render page 1 only → discuss plan+sample → explicit approval → batch 2..N with frozen contract → clean-plate normalization → deterministic composition → two-level QA (page-level compliance vs set-level cohesion) → verified ZIP. You talk to your AI in plain language:

> I have 10 photos in /path/to/photos, make them watercolor journal, keep cups small, bottom-center, 55% top whitespace, no caption.

AI checks EXIF, shows 5 thumbnails, renders sample, waits for "批准第1张，继续". Page-local fix like "page 2 background too busy, simplify" only marks page 2 stale. Style change invalidates approval and returns to style gate — expected, not a bug. Private references stay local unless you explicitly say "you may upload to X". `python3 bin/workflow.py status|next` never writes, only tells next step.

<details>
<summary>For AI / Implementation — scripts, gates, contracts</summary>

**Purpose:** `presets/travel-food-journal.json` supplies defaults; renderer requires validated receipt.

**6 layers:** Config (`presets/*.json` + `profiles/styles/*.json` → `work/resolved-config.json` SHA256) → Plan (`manifest.json` → `render-plan.json` → `production-plan.md` + `approval-state.json` + `sample-scope.json`) → Gate (2.5 style gate mandatory → `style_choice.json`; Step 3 sample 🔴 CHECKPOINT; Step 4 approval 🛑 STOP) → Render (`renderer_receipt.py` → `clean_plate.py` → `compose.py`) → QA (`qa_images.py`) → Package (`package_verified.py stage + verify`).

Invariants: EXIF order immutable; sample = first EXIF only; sample never becomes reference; every plate has receipt; no EXIF/GPS/XMP in outputs; no invention of location/date/caption.

**Explicit defaults:** Canvas 9:16 1152×2048, paper #F1EBDD 50% blank, Noto Sans Light 30px #3B3832 at 1080px, default `watercolor-journal`, order EXIF asc, QA full + 360×640, renderer none by default.

**Workflow (AI runs):** `check_environment.py` → `resolve_config.py` + `preprocess.py` → `build_render_plan.py` + `build_production_plan.py` → 2.5 style gate → sample → `review_gate.py approve` + `compose.py batch` → batch compose → QA → revision scope → `package_verified.py`.

Validation: `python3 -m unittest discover -s tests -v` / `python3 bin/validate_skill.py --json`

Layout: `SKILL.md`, `presets/`, `profiles/{themes,styles,layers,compositions,unification}/`, `assets/samples/`, `assets/style-packs/`, `bin/`, `tests/`

</details>

## References

- Behavior and boundaries: `SKILL.md`, `references/configuration.md`, `references/review-gate.md`, `references/quality-checks.md`
- Regression and boundary cases: `tests/`, `references/test-cases.md` (34 gates), `bin/validate_skill.py`
- Storage and archiving: `work/resolved-config.json` (SHA256), `work/manifest.json` (EXIF-ordered), `work/style_choice.json`, `work/composition-manifest.json`, `work/verify-report.json`
- No extra-licensed fonts or images beyond Smithsonian public-domain packs in `assets/style-packs/`; samples in `assets/samples/` are webp <100KB, source blurred 12px for privacy; finals contain no EXIF/GPS/XMP; no copyrighted excerpts

## License

MIT License — Copyright (c) 2026 locoda. Code and docs under MIT; style packs under their respective Smithsonian public-domain terms; sample images under same repo license with privacy blur applied to sources.

---
Made by [1mether](https://1mether.me).

*Keep the photo, just remember it in a different stroke.*
