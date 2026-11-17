---
name: long-to-cards
description: Transform long-form content, outlines, transcripts, research notes, or article drafts into a standard card package and platform publishing copy, then hand publish-ready packages to cards-to-images. Use for Xiaohongshu image posts, WeChat inline cards, Zhihu Idea images, generic carousels, card scripts, captions, image order, CTAs, or freshness-aware topic tags. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/long-to-cards
---

# Long To Cards

## Goal

Convert long-form source material into a clear card-based content package.

Preserve the source argument and evidence. Compress, sequence, and adapt the material for skimmable cards without inventing facts or turning the content into shallow slogans.

Use `delivery_mode=publish_ready` by default. In that mode, this skill finishes the content package and hands it to `cards-to-images`; the distribution workflow continues until real images and a checked manifest exist. Use `delivery_mode=copy_only` only when the user explicitly requests card copy, scripts, or visual prompts without image production.

## Inputs

Collect:

- source material: article, outline, transcript, notes, or research brief
- `delivery_mode`: `publish_ready` by default or explicit `copy_only`
- `platform_profile`: `xiaohongshu`, `wechat-inline`, `zhihu-idea`, or `generic`
- `asset_url_policy`: `local` by default or `public` when stable URLs are required
- audience
- desired card count
- content goal: explain, persuade, teach, summarize, promote, or archive
- tone and claims to avoid
- reviewed publish-package fields when available

If the source material is missing, ask for it before producing final cards. If the material is too long to process safely, first create a section map and ask which sections to prioritize.

## Process

### 1. Diagnose The Source

Identify:

- central claim
- reader problem
- strongest examples or evidence
- reusable framework or steps
- weak sections to drop
- claims that need verification

Do not preserve every paragraph. Keep the parts that help a reader understand, decide, or act.

### 2. Choose A Card Narrative

Pick one primary structure:

- Problem to method: pain point -> mistake -> method -> example -> takeaway
- Myth to clarity: common belief -> correction -> proof -> practical advice
- Step-by-step: goal -> steps -> pitfalls -> checklist -> next action
- Case breakdown: situation -> decision -> action -> result -> lesson
- Summary: key idea -> 3-7 points -> conclusion -> save/share prompt

Use one structure per card package. Avoid mixing unrelated storylines.

### 3. Build The Card Plan

Create a card sequence:

1. cover hook
2. context or reader pain
3. core idea
4. supporting points or steps
5. example, evidence, or contrast
6. checklist or method
7. conclusion and action

Adjust the sequence to the target platform:

- Xiaohongshu: stronger hook, practical takeaway, save-worthy checklist
- WeChat inline cards: clearer logic, fewer claims per card, stronger summary, adaptive vertical-card or horizontal-diagram shape
- Zhihu Idea: one defensible judgment per card, enough context to stand alone, 3:4 by default
- Generic cards: prioritize clarity and reuse

### 4. Write Card Copy

For each card, output:

- card number
- card title
- main copy
- optional microcopy
- visual direction
- source anchor or note

Keep each card focused on one idea. If a card needs more than one paragraph, split it.

### 5. Add Publishing Assets

Add the publishing fields required by the selected profile:

- cover title and first-line hook
- body caption or post description
- image order and CTA
- grouped topic tags with freshness state when the platform uses tags
- alt text guidance
- source caveats
- optional follow-up card ideas

Use these tag groups:

- `core_tags`: stable topic terms
- `scene_tags`: reader situation or use case
- `series_tags`: recurring author or content-series label
- `verified_hot_tags`: only current tags supported by a source and check time

When current trend evidence is unavailable, leave `verified_hot_tags.values` empty and set its status to `unverified`. Do not infer current popularity from model memory.

### 6. Hand Off Image Production

Write a complete image-production handoff containing:

- delivery mode and platform profile
- ordered card ids
- exact card copy and approved visual direction
- source anchors and factual constraints
- target ratio and dimensions
- stable output filenames
- alt text
- visual-system constraints
- asset URL policy

With `delivery_mode=publish_ready`, set the next skill to `cards-to-images`. Do not report the package as an uploadable card delivery until real files and a `cards-manifest` return from that skill.

With explicit `delivery_mode=copy_only`, stop after the card package and record that image production was intentionally skipped.

## Output Format

Use this structure:

```markdown
# Card Package

## Source Diagnosis
- Core claim:
- Reader problem:
- Best reusable material:
- Dropped material:
- Claims needing verification:

## Card Strategy
- Delivery mode:
- Platform profile:
- Asset URL policy:
- Audience:
- Card count:
- Narrative structure:
- Hook direction:

## Cards
### Card 1
- Title:
- Copy:
- Microcopy:
- Visual direction:
- Source anchor:

### Card 2
...

## Publishing Assets
- Cover title:
- First-line hook:
- Body caption:
- Image order:
- CTA:
- Core tags:
- Scene tags:
- Series tags:
- Verified hot tags:
  - Status:
  - Checked at:
  - Source:
  - Values:
- Alt text guidance:
- Source caveats:
- Follow-up ideas:

## Image Production Handoff
- Next skill: cards-to-images / none
- Ordered card ids:
- Target ratio and dimensions:
- Stable filenames:
- Visual-system constraints:
- Human decision needed:
- Stop condition:
```

## Quality Rules

- Each card must carry one clear idea.
- The card sequence must be readable without the original long article.
- Keep the cover specific; avoid vague motivation-style hooks.
- Preserve uncertainty and source caveats.
- Convert dense paragraphs into reader-facing steps, contrasts, examples, or checklists.
- Keep visual direction practical: layout, emphasis, icon idea, chart idea, or image type.
- Keep the approved publish package as the source of truth when one exists; report proposed metadata changes instead of silently replacing it.
- Keep one canonical card package across rendering and final publish checks.

## Boundaries

- Do not invent examples, data, quotes, or results absent from the source.
- Do not stop at copy in the distribution workflow when `delivery_mode=publish_ready`.
- Do not claim that image assets exist before `cards-to-images` returns real checked files.
- Do not include private paths, private accounts, or unpublished personal material unless the user supplied it for the current task.
- Do not optimize for a platform in ways that distort the source argument.
- Do not claim the package is ready to publish if source claims still need verification.
- Do not claim a tag is currently hot without a current source and check time.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
