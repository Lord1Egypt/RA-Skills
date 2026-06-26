---
name: product-page-copywriter
description: Turn product briefs, pain points, competitor notes, and platform constraints into product page titles, hero benefit blocks, detail-module structure, and FAQ or closing copy. Use when operators, designers, sellers, or founders need multi-version PDP copy without live CMS, feed, or compliance integrations.
---

# Product Page Copywriter

## Overview

Use this skill to translate product parameters, user pain points, selling angles, competitor context, and platform rules into structured product page copy. It is designed for teams that need conversion-oriented copy while still respecting platform and compliance constraints.

This MVP is heuristic. It does **not** connect to live storefront CMS, marketplace feeds, compliance systems, or creative tools. It relies on the user's product brief, market context, and constraints.

## Trigger

Use this skill when the user wants to:
- write better PDP or product-detail-page copy from a rough brief
- produce multiple copy versions for different channels or tones
- structure hero claims, detail modules, FAQ, and closing copy in one pack
- separate user benefits from feature dumping
- prepare copy that designers, operators, and compliance reviewers can quickly inspect

### Example prompts
- "Write product page copy for this new kitchen gadget"
- "Create a Tmall and JD version of our PDP copy"
- "Help us rewrite our detail page around clearer user benefits"
- "Turn these product notes into a copy pack with compliance watchouts"

## Workflow
1. Capture the product, platform, target audience, and whether the main tension is conversion, tone, or compliance.
2. Extract the likely value angles, such as convenience, performance, trust, premium feel, or scenario fit.
3. Turn those angles into title options, hero selling points, module structure, and FAQ or closing copy.
4. Mark where copy may need legal or platform review.
5. Return a markdown copy pack that is practical for design and operations handoff.

## Inputs
The user can provide any mix of:
- product name, parameters, and category
- target audience and use scenarios
- pain points, benefits, or proof points
- competitor differences and platform requirements
- restricted words, compliance concerns, or sensitive claims
- preferred tone such as conversion-led, premium, concise, or cautious

## Outputs
Return a markdown copy pack with:
- title candidates
- hero selling points
- detail-module structure
- FAQ and closing copy
- compliance watchouts and assumptions

## Safety
- Do not claim access to live CMS, marketplace feeds, or compliance systems.
- Avoid absolute, medical, efficacy, or unsubstantiated comparative claims.
- Keep final legal or platform-sensitive approval human-reviewed.
- When proof is weak, downgrade bold claims into softer benefit framing.

## Best-fit Scenarios
- ecommerce PDP rewrite and launch support
- marketplace and DTC copy adaptation
- teams that need copy structure before design work starts
- operator-led businesses that need faster copy iteration with clear guardrails

## Not Ideal For
- final legal review of regulated claims
- visual design generation or image production
- product categories with no usable source material at all
- fully automated publishing into a live storefront or marketplace

## Acceptance Criteria
- Return markdown text.
- Include title, hero, structure, FAQ, and compliance sections.
- Provide at least two stylistic options or angles.
- Keep the copy pack practical for design, operations, and compliance review.
