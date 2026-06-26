---
name: human-style-writing
description: Human-like writing for **daily chat + social media only** (CN/EN/mixed). Routes requests into daily chat (texts/DMs) or platform-specific social posts: X/Twitter (tweet/thread), Reddit (post/comment), LinkedIn, Instagram caption, TikTok caption, 小红书/RedNote 笔记, WeChat Moments/朋友圈, plus generic social posts. Use when the user asks to make writing sound human, less "AI", or explicitly mentions tweet/X/Twitter thread, Reddit post/comment, LinkedIn post, Instagram/TikTok caption, 小红书/RedNote, 朋友圈/WeChat Moments, or a social post/caption.
---

# Human Style Writing

This skill is a **router + prompt library** for human-like writing.

## Scope (hard constraint)
This skill is for **daily chat (texts/DMs)** and **social media posts/captions** only.

If the user asks for **academic writing, news/press, legal/compliance, marketing copy, customer support macros, work emails/reports**, or other “document/brand” writing:
- do **not** attempt to produce that register
- ask **one** clarifying question: DM/text vs social post (and platform)
- then rewrite into that chosen surface

(We’re improving “human-likeness” for chat/social, not optimizing other registers.)

## What it does
1) **Classify** the task into an on-scope scenario: daily chat vs social (platform-specific)
2) **Apply** the correct prompt recipe + humanization passes to generate output that reads like a real person

It supports **Chinese, English, mixed bilingual**, and is designed to be extended to additional languages.

---

## Workflow Decision Tree (do this first)

### Step 0 — Identify language + target surface
- Language: 中文 / English / 混合 / other
- Surface: **DM/text** or **social post/caption**

If the user didn’t specify, ask one question:
> “Do you want this as (A) a DM/text message, or (B) a social post? If social, which platform (X/Reddit/LinkedIn/IG/TikTok/小红书/朋友圈)?”

### Step 1 — Scenario classification (router)
Use `references/scenario-router.md`.

Router outputs MUST include:
- **scenario_id** (daily_chat / social_* )
- **platform** (generic/x/reddit/linkedin/instagram/tiktok/xiaohongshu/wechat_moments)
- **formality** (0–3)
- **tone** (friendly / neutral / urgent / apologetic / assertive / playful)
- **audience relationship** (friend/peer/partner/manager/client/public)

### Step 2 — Load the matching prompt recipe
Use `references/prompt-recipes.md` and select:
- a **system-style instruction** (genre constraints)
- a **style card** template
- optional **few-shot pack** structure

### Step 3 — Generate or rewrite
Follow the universal drafting procedure:
1) collect minimum inputs
2) create a compact style card (5–10 bullets)
3) draft in the target genre
4) humanization passes
5) anti-AI checklist gate

### Step 4 — Quality gate
Use `references/human-checklist.md` (score 0–2 each). If ≤15, revise once.

---

## Universal drafting procedure (applies to all scenarios)

### A) Collect the minimum inputs
Ask for (or infer):
1) **Language**
2) **Scenario** (or run router)
3) **Style requirements** (if any): voice/persona, tone, formality, “像谁/像哪种文风”
4) **Audience + relationship**
5) **Goal**: inform / persuade / apologize / request / report / argue
6) **Constraints**: length, must-keep facts, forbidden phrases, sensitive topics
7) **Source material**: (a) user draft to rewrite, or (b) bullet points to expand

Default style (when user provides no style requirements):
- “general human”: clear, specific, slightly imperfect, non-salesy
- formality: 1–2 (casual-professional depending on scenario)
- tone: neutral-friendly
- no assistant meta-phrases

### B) Build a “Style Card” (1 minute)
Include:
- persona/voice (e.g., “busy PM”, “grad student”, “journalist”)
- sentence-length mix
- vocabulary level
- stance calibration (confident/cautious)
- emotional temperature (0–3)
- structural preference (short paragraphs vs bullets)
- banned AI-tells (see `references/ai-tells.md`)

### C) Humanization passes (mandatory)
1) **Specificity**: add concrete anchors (time, numbers, examples) *without inventing facts*.
2) **Rhythm**: vary sentence length; reduce template symmetry.
3) **Agency**: explicit subject (“I/we/you”) where appropriate; remove passive fog.
4) **Friction**: add realistic constraints/tradeoffs when appropriate; no fake experiences.
5) **Compression**: delete filler + repeated points.
6) **Phrase scrub (scenario-specific, manual rewrite)**: scan for high-frequency AI/PR/marketing phrases and templated closers (see `references/phrase-blacklist.md`). Then **rewrite in-context** (or delete filler) rather than doing mechanical search/replace. Do **not** globally normalize punctuation/quotes.

### D) Anti-AI checklist gate
Use `references/human-checklist.md`.

Deliver:
- final text
- optional: 3–6 bullets of “what changed” for iterative refinement

---

## Training an AI to sound human (practical, scalable)

Inside OpenClaw we usually improve “human-ness” via **routing + recipes + examples** (not weight training).

### Level 1 — Prompting + few-shot (fast)
- Collect 10–30 human samples per scenario.
- Derive a style card.
- Create 3–8 few-shot pairs (bullets → output).
- Add the anti-AI checklist as a constraint.

### Level 2 — Post-edit loop (best quality, no infra)
- Draft → human edits → store before/after + rationale → reuse as examples.

### Level 3 — Fine-tuning (if you have infra)
- SFT on curated corpora + your edited pairs.
- Preference tuning (DPO/RLHF) using “human-likeness + task success” rankings.
- Evaluate with blinded A/B by scenario.

### Extending to new languages
Use `references/language-extension.md`.

---

## Bundled references
- `references/scenario-router.md` — how to classify scenario/platform (CN/EN)
- `references/prompt-recipes.md` — prompt templates per scenario + what to include/avoid
- `references/registers.md` — detailed conventions across registers (CN/EN)
- `references/ai-tells.md` — common AI tells and fixes
- `references/phrase-blacklist.md` — scenario-specific blacklist phrases + human alternatives (use in the phrase scrub pass)
- `references/human-checklist.md` — final QA checklist + scoring
- `references/fewshot-pack.md` — how to build few-shot datasets
- `references/language-extension.md` — how to add more languages safely
