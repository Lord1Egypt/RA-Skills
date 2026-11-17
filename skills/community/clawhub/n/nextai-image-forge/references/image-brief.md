# Image Brief Brainstorming Workflow

Use this before every ImageForge generation or edit after configuration is ready. It is adapted from `superpowers:brainstorming`: turn a vague image request into a finished visual brief through step-by-step dialogue, then generate only after user approval.

Default to the user's language. If the user writes Chinese, guide the whole flow in Chinese.

<HARD-GATE>
Do NOT run `generate` or `edit` until this workflow is complete and the user has approved the final brief. Do NOT answer with an Approved Image Brief in the first response. Do not compress the workflow into one message. Do not replace dialogue with a checklist dump.
Do not compress this into one message.
</HARD-GATE>

## Required visible checklist

MUST complete these steps in order.

Create and maintain a visible checklist for these steps, then complete them in order:

1. **Explore context** — understand purpose, audience, use case, existing assets, source images, brand/product constraints, and success criteria.
2. **Offer visual companion** — if the agent environment supports visual previews and upcoming decisions involve visual direction, layout, composition, or style, offer that support in its own message. If unsupported, continue text-only.
3. **Ask clarifying questions** — ask one question at a time; stop after the first question and wait. Prefer multiple choice when helpful.
4. **Propose 2-3 approaches** — present distinct visual directions with trade-offs and a recommendation. Do not jump straight to a prompt.
5. **Present design sections** — confirm goal/output, subject, style, composition, text, constraints, and edit scope in small sections. Ask whether each section is right before moving on.
6. **Write Approved Image Brief** — only after the design is clear, write the final structured brief in chat.
7. **Brief self-review** — scan for placeholders, contradictions, missing constraints, unclear text, impossible composition, and edit-preservation risks. Fix issues inline.
8. **User approves** — ask the user to approve or revise the brief. Wait for approval.
9. **Run ImageForge** — pass the approved structured brief with `--brief '<approved brief>'`. Use `--direct` only in Direct mode.

## First response rule

For normal generation/editing requests, the first response after `ensure-ready` must be one of these:

- A visual companion offer, if visual comparison would help and the environment supports it.
- A short context summary plus one clarifying question.

It must not include a final prompt, provider prompt, final brief, or generation command. If you already know enough from the user's message, still propose 2-3 approaches and get confirmation before writing the Approved Image Brief.

## Clarifying question map

Ask the single question that unlocks the most quality. Do not interrogate the user with the full list.

- **Purpose**: what the image is for, such as ad, poster, avatar, article cover, product mockup, UI asset, social media, or internal draft.
- **Audience**: who will see it and what they should feel or do.
- **Deliverable**: quantity, aspect ratio, size, platform, transparent background, and whether text must be readable.
- **Subject**: main subject, product, character, scene, action, era, location, materials, clothing, props, and non-negotiable details.
- **Style**: photo, illustration, 3D, flat graphic, cinematic, minimal, luxury, playful, realistic, brand-like, color palette, lighting, lens, mood, and visual references.
- **Composition**: framing, camera angle, focal hierarchy, whitespace, foreground/background, layout, crop safety, and where text or QR codes should sit.
- **Text**: exact copy, language, line breaks, typography tone, and whether the model should avoid rendering text.
- **Constraints**: what to avoid, brand restrictions, cultural/market constraints, legal or safety constraints, no watermark, no extra logos, no distorted hands/faces/text.
- **Edit-Specific**: source image path, what must stay unchanged, what to remove/add/replace, target area, acceptable drift, and whether the edit should preserve identity, pose, layout, color, or text.

Good first questions:

- “这张图最终用在哪里？海报、封面、广告图、头像，还是别的？”
- “你想要偏真实摄影、插画、3D，还是极简平面风格？”
- “画面里必须出现哪些主体和文字？”
- “改图时，哪些部分必须保持不变？”

## Approach proposal

After enough context is known, propose 2-3 approaches before writing the final brief:

- **A:** strongest default option and why.
- **B:** useful alternate direction and trade-off.
- **C:** optional bolder or safer direction.

Recommend one direction. Ask the user to choose or adjust it.

## Design confirmations

Do not treat “looks good” as global approval if important sections are still undefined. Confirm the sections that affect image quality:

- Goal/output: use case, format, aspect ratio, quantity.
- Subject: main objects, people, product, scene, and non-negotiables.
- Style: medium, mood, lighting, palette, realism level, references.
- Composition: framing, camera angle, hierarchy, whitespace, crop safety.
- Text: exact copy or explicit “no text”.
- Constraints: avoid list, brand/legal/safety requirements.
- Edit scope: what must remain unchanged and acceptable drift.

## Approved Image Brief

The old shorthand “Approved Brief” is not enough; the required artifact is the full Approved Image Brief below.

Before calling ImageForge, present this exact structured brief format. The helper rejects empty fields, placeholders, missing question/answer evidence, missing 2-3 approaches, missing design confirmation evidence, and missing explicit user approval.

```text
Approved Image Brief
Context:
Questions answered:
- Q:
  A:
Approaches considered:
- A:
- B:
- C:
Selected direction:
Design confirmations:
Output:
Subject:
Style:
Composition:
Text:
Constraints:
Edit scope:
Brief self-review:
User approval: yes
```

If `Edit scope` does not apply, write `Edit scope: not applicable`. Do not leave placeholders. End with “确认后我再生成。” Do not run `generate` or `edit` until the user approves this brief, except in Direct mode.

## Direct mode

Direct mode applies only when the user explicitly says things like “直接生成”, “别问”, “按这个 prompt 做”, or “use this exact prompt”. In Direct mode:

- Do not ask clarifying questions.
- Briefly restate the execution understanding in one or two sentences.
- Keep the prompt faithful to the user's wording.
- Proceed with ImageForge after the restatement by passing `--direct`.

## Prompt construction

After approval, convert the brief into a provider prompt:

- Put the core subject and purpose first.
- Include style, composition, lighting, color, and exact text requirements.
- Include constraints as direct negative instructions.
- For edits, state preservation requirements before requested changes.
- Keep prompts specific but not bloated; avoid contradictory style words.
