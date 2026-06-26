---
name: "AI Content Brief, Script & Outline Generator — Research Assistant for Video & Image"
version: 1.0.7
category: knowledge
author: IMA Studio (imastudio.com)
keywords: imastudio, knowledge, workflow, model selection, visual consistency, video modes, parameter guide, 知识库, 工作流, 模型选择, IMA, 图像视频音乐, SeeDream, Midjourney, Suno, Kling, Veo, Sora, brief, script, outline, research
description: >
  AI content brief, script, and outline generator for video, image, and audio production.
  Works as an AI research assistant that provides expert guidance on workflow design,
  model selection, parameter optimization, and visual consistency. Generate briefs, scripts,
  and production outlines before using ima-image-ai, ima-video-ai, ima-voice-ai, or ima-all-ai.
  Essential reading for planning workflows, choosing models, optimizing prompts and parameters,
  maintaining character/style consistency, multi-shot production, and avoiding common mistakes.
  Transforms beginner attempts into professional-grade results. This is a knowledge skill —
  it provides strategic guidance, not API calls. Covers: content brief generation, script writing,
  outline creation, AI research assistance, and production best practices for all media types.
---

# IMA Knowledge AI

> **Purpose**: This skill provides strategic knowledge to help agents make better decisions when using IMA Studio's content creation APIs. It does NOT make API calls directly — instead, it guides you to use `ima-voice-ai`, `ima-image-ai`, `ima-video-ai` more effectively.

## When to Use This Skill

**Read this skill BEFORE calling any ima-*-ai skill** if you need guidance on:

1. **Workflow Design** — How to break down complex user requests into atomic tasks
2. **Model Selection** — Which model to choose based on task requirements
3. **Parameter Optimization** — How to set parameters for quality, cost, or speed

**Example scenarios**:
- User: "帮我做个宣传视频" → Read `workflow-design.md` first
- User: "用最好的模型生成" → Read `model-selection.md` to pick the right one
- User: "生成16:9的图片" → Read `parameter-guide.md` for aspect ratio support

---

## Knowledge Structure

**All knowledge files live under the `references/` directory.** When reading from other skills, use paths like `ima-knowledge-ai/references/workflow-design.md` or `~/.openclaw/skills/ima-knowledge-ai/references/<filename>.md`.

This skill contains **12 knowledge modules** (8 standalone + 4 modular directories):

### Core Knowledge (1-8)

### 1. [workflow-design.md](references/workflow-design.md)
**When to read**: Complex user requests that need task decomposition

- Task decomposition strategies
- Dependency identification (e.g., script → voiceover → video)
- Multi-step workflow templates
- Common creation patterns

### 2. [model-selection.md](references/model-selection.md)
**When to read**: Choosing between multiple models for a task

- Model capability matrix (image/video/voice)
- Cost vs. quality trade-offs
- Use case recommendations (budget/balanced/premium)
- Model limitations and workarounds

### 3. [parameter-guide.md](references/parameter-guide.md)
**When to read**: Optimizing parameters for a specific task

- Resolution/aspect ratio guidelines
- Quality vs. speed trade-offs
- Common mistakes and fixes
- Parameter compatibility matrix

### 4. [visual-consistency.md](references/visual-consistency.md) ⭐ **NEW**
**When to read**: Any image/video generation task involving series, characters, or scenes

- Why AI generation lacks visual consistency by default
- Identifying implicit consistency requirements
- Reference image workflow (Image-to-Image / Video-to-Video)
- Multi-shot coherence strategies
- Common mistakes and best practices

### 5. [video-modes.md](references/video-modes.md) ⭐⭐ **CRITICAL**
**When to read**: ANY video generation task (MANDATORY before calling ima-video-ai)

- image_to_video vs reference_image_to_video (DIFFERENT concepts!)
- image_to_video = first frame to video (input becomes frame 1)
- reference_image_to_video = reference appearance to video (can change scene)
- Traditional two-step vs modern one-step workflow
- Fallback strategy when primary method fails
- Common mistakes (旺财案例)

### 6. [long-video-production.md](references/long-video-production.md) 🎬 **ESSENTIAL FOR LONG VIDEOS**
**When to read**: User requests video longer than 15 seconds (30s ad, 1min short, 3min promo)

- Why models are limited to 10-15 seconds
- Multi-shot capability (2-4 camera angles in one generation) 🆕
- Three-step workflow: Script → Generate shots → Edit/Stitch
- Visual asset preparation (characters, scenes, props)
- Shot-by-shot generation strategy
- Video editing and stitching techniques
- Complete case study: 1-minute fantasy short film

### 7. [character-design.md](references/character-design.md) 🎨 **CHARACTER DESIGN / IP DEVELOPMENT**
**When to read**: User needs character design, IP development, game/animation assets, turnaround sheets

- Character Design industry overview (games, animation, manga, IP)
- Reference-driven workflow (Master Reference → Variants)
- Turnaround sheets (front/side/back/3-4 views)
- Expression library (happy/angry/sad/surprised...)
- Outfit variants (casual/armor/costumes)
- Props & weapons reference images
- Action poses (idle/walk/run/attack...)
- Complete case study: RPG game character "Aria"

### 8. [vi-design.md](references/vi-design.md) 🏢 **VI DESIGN / BRAND IDENTITY**
**When to read**: User needs VI design, brand identity, logo applications, visual guidelines

- VI (Visual Identity) system overview
- Foundation system (Logo / Color / Typography / Auxiliary graphics)
- Application system (Office / Store / Packaging / Advertising / Digital / Uniform)
- Reference-driven workflow (Foundation → Applications)
- Logo consistency requirements (highest level)
- Color palette management (Primary / Secondary / Neutral / Functional)
- Complete case study: "Morning Light Coffee" cafe VI (20+ deliverables)

### 9. [best-practices/](references/best-practices/) ⭐⭐⭐ **COMMERCIAL TEMPLATES (On-Demand)**
**When to read**: Commercial advertising or artistic photography tasks

**Structure**: Index + 4 scenario files (load only what you need)

- `README.md` — Index with keyword matching (2 KB)
- `jewelry.md` — Jewelry & accessories commercial ads (3 KB)
- `skincare.md` — Skincare & cosmetics commercial ads (3 KB)
- `perfume.md` — Perfume & fragrance commercial ads (3 KB)
- `cinematic-art.md` — Cinematic vintage art photography (4 KB)

**Usage**: Read index first → Load only relevant scenario file

**Token savings**: 60-85% compared to loading all scenarios

### 10. [color-theory/](references/color-theory/) 🎨 **COLOR THEORY & CULTURAL SENSITIVITY**
**When to read**: Any design task requiring color selection (logos, posters, brands, products)

**Structure**: Index + 7 modular files (load only what you need)

- `README.md` — Index with quick navigation (5 KB)
- `color-psychology.md` — 11 major colors' psychology & applications (12 KB) ⭐
- `color-combinations.md` — 5 pairing principles (2 KB)
- `industry-guide.md` — 10 industries' color preferences (1 KB)
- `cultural-differences.md` — 5 regions' basic differences (1 KB)
- `global-regions.md` — 4 regions' detailed guide (4 KB)
- `religious-systems.md` — 5 major religions' color symbolism (5 KB)
- `application-strategy.md` — IMA Studio color decision process (2 KB)

**Usage**: Read index → Load relevant modules based on task (target region/industry/religion)

**Token savings**: 70-90% compared to loading all 32 KB

### 11. [design-pitfalls/](references/design-pitfalls/) 🚫 **DESIGN MISTAKES TO AVOID**
**When to read**: Quality assurance for generated content (before final delivery)

**Structure**: Index + 4 scenario files (29 common mistakes by scene)

- `README.md` — Index with 5 core principles (3 KB)
- `logo-design.md` — Logo design pitfalls (10 rules) (7 KB)
- `poster-banner.md` — Poster/Banner pitfalls (8 rules) (5 KB)
- `product-ecommerce.md` — Product/E-commerce pitfalls (6 rules) (3 KB)
- `web-ui.md` — Web/UI pitfalls (5 rules) (3 KB)

**Usage**: Read index → Load scenario-specific pitfalls

**Token savings**: 60-80% compared to loading all 21 KB

### 12. [color-trends-2026/](references/color-trends-2026/) 📅 **2026 COLOR TRENDS**
**When to read**: Design tasks for 2026 market (stay current with trends)

**Structure**: Index + 5 time/region files (load by current month + target region)

- `README.md` — Index with time-based navigation (6 KB)
- `annual-colors.md` — Pantone Cloud Dancer / WGSN Teal / China Horse Red (4 KB)
- `spring-summer.md` — Mar-Aug trends: Cobalt Blue, Violet, Bright Pink (2 KB)
- `fall-winter.md` — Sep-Feb trends: Dark Luxury theme (1 KB)
- `regional-differences.md` — China/US/Southeast Asia differences (2 KB)
- `industry-applications.md` — Tech/Fashion/Food/Beauty/Home (1 KB)

**Usage**: Read index → Load current season + target region

**Token savings**: 75-90% compared to loading all 16 KB

**Auto-loading strategy**: Check current month → Load relevant season file automatically

---

## Usage Pattern

```
User Request
  ↓
[ima-knowledge-ai] Query relevant knowledge
  ↓
Make informed decision
  ↓
[ima-*-ai] Execute API call with optimized parameters
  ↓
Success!
```

**Example flow**:
```
User: "帮我生成一张16:9的产品海报，要高质量"

Step 1: Read ima-knowledge-ai → parameter-guide.md
        → Learn: SeeDream 4.5 supports 16:9, Nano Banana Pro native support
        
Step 2: Read ima-knowledge-ai → model-selection.md
        → Choose: Nano Banana Pro 4K (best quality, 18pts)
        
Step 3: Call ima-image-ai with:
        --model-id gemini-3-pro-image
        --extra-params '{"aspect_ratio": "16:9", "size": "4K"}'
        
Step 4: Success! 🎉
```

---

## Important Notes

1. **This skill does NOT replace ima-*-ai skills**  
   Use it as a consultant before executing tasks

2. **Knowledge is based on production IMA Studio API (2026-02-27)**  
   Models and parameters may change; always verify with `list-models`

3. **Cost transparency**  
   All recommendations include credit cost for user decision-making

4. **No scripts in this skill**  
   Pure knowledge — implementation is handled by other ima-*-ai skills

---

## Quick Reference

| Need | Read This |
|------|-----------|
| "How to break down a complex task?" | `workflow-design.md` |
| "Which model should I use?" | `model-selection.md` |
| "How to set resolution/aspect ratio?" | `parameter-guide.md` |
| "What's the cost difference?" | `model-selection.md` |
| "Why did my parameter get ignored?" | `parameter-guide.md` |
| **"How to keep visual consistency across images/videos?"** ⭐ | **`visual-consistency.md`** |
| **"Generate series/multiple shots with same subject?"** | **`visual-consistency.md`** |
| **"image_to_video vs reference_image_to_video?"** ⭐⭐ | **`video-modes.md`** |
| **"Which video mode should I use?"** | **`video-modes.md`** |
| **"User wants 30s+ video / short film / ad?"** 🎬 | **`long-video-production.md`** |
| **"How to make 1min+ video with 10s limit?"** | **`long-video-production.md`** |
| **"Multi-shot video (2-4 camera angles in one gen)?"** 🆕 | **`long-video-production.md`** |
| **"Character design / IP development?"** 🎨 | **`character-design.md`** |
| **"Game/animation character assets?"** | **`character-design.md`** |
| **"Turnaround sheet / expression library?"** | **`character-design.md`** |
| **"How to maintain character consistency?"** | **`character-design.md`** |
| **"VI design / brand identity / logo applications?"** 🏢 | **`vi-design.md`** |
| **"Coffee shop / restaurant / retail brand design?"** | **`vi-design.md`** |
| **"Business card / menu / packaging / signage?"** | **`vi-design.md`** |
| **"How to ensure brand consistency?"** | **`vi-design.md`** |
| **"Jewelry ad / skincare ad / perfume ad?"** ⭐⭐⭐ | **`best-practices/`** (index first) |
| **"Commercial advertising templates?"** | **`best-practices/jewelry\|skincare\|perfume.md`** |
| **"Cinematic art photography / editorial style?"** | **`best-practices/cinematic-art.md`** |
| **"What colors for tech/fashion/food brand?"** 🎨 | **`color-theory/`** (index → industry-guide) |
| **"Color psychology (red/blue/green)?"** | **`color-theory/color-psychology.md`** |
| **"Cultural sensitivity (China/India/Middle East)?"** | **`color-theory/`** (cultural/religious) |
| **"Logo design mistakes to avoid?"** 🚫 | **`design-pitfalls/logo-design.md`** |
| **"Poster/product/web design pitfalls?"** | **`design-pitfalls/`** (index first) |
| **"2026 color trends / Pantone?"** 📅 | **`color-trends-2026/`** (index → season) |
| **"Spring/summer vs fall/winter colors?"** | **`color-trends-2026/spring-summer\|fall-winter.md`** |

