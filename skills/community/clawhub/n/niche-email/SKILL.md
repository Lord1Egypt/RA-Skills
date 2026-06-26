---
name: niche-email
description: Generate targeted, research-driven email copy for niche audiences and topics. Use when: crafting outreach emails, newsletters, pitches, or promotions for specific niches (e.g., AI agent builders, indie hackers, ClawHub developers, homesteading, SaaS founders, acreage businesses). Triggers: 'write email to [niche]', 'pitch [product] to [audience]', 'niche newsletter on [topic]'. Integrates web_search for trends/pain points, copywriting frameworks (AIDA, PAS), and personalization best practices.
---

# Niche Email Generator

## Overview
This skill turns vague email ideas into high-ROI copy tailored to niche audiences. By combining real-time research with proven copy structures, it creates emails that resonate—boosting opens, clicks, and conversions.

Key capabilities:
- Niche research (trends, pain points, language)
- Multi-variant subject lines and body copy
- Personalization hooks
- AIDA/PAS frameworks
- Mobile-optimized formatting

## Quick Start
1. Define niche + goal: e.g., "Pitch ClawHub skills to indie AI devs"
2. Research: Use `web_search` for niche insights
3. Generate: Pick framework, request variants
4. Refine: Test readability, add CTAs

Example prompt: "Using niche-email skill, write a pitch email for ClawHub's skill-creator to Python automation enthusiasts."

## Workflow

### 1. Niche & Goal Clarification
- Identify: Audience (who), Goal (sell/demo/educate), Channel (cold email/newsletter)
- Examples:
  | Niche | Audience | Goal |
  |-------|----------|------|
  | AI agents | Indie devs | Demo OpenClaw skills |
  | Homesteading | Acreage owners | Promote land tools |
  | Hockey scouting | WHL analysts | Share data dashboards |

### 2. Research Phase
Run `web_search` queries like:
- "[niche] pain points 2026"
- "top [niche] newsletters"
- "[niche] trends site:reddit.com"
- "[product] competitors [niche]"

Synthesize: 3-5 key insights (trends, objections, language).

### 3. Copy Structure (Choose Framework)
**AIDA (Attention-Interest-Desire-Action):**
- Attention: Provocative question/hook from research
- Interest: Story or stat
- Desire: Benefits + proof
- Action: Clear CTA

**PAS (Problem-Agitate-Solution):**
- Problem: Niche pain
- Agitate: Consequences
- Solution: Your offer

### 4. Subject Lines (5 Variants)
- Curiosity: "The [niche] hack I wish I knew sooner"
- Benefit: "Boost your [niche] output 3x with this"
- Urgency: "[Niche] alert: Don't miss this before [date]"

### 5. Full Email Generation
Keep under 150 words. Structure:
```
Subject: [variant]

Hey [First Name],

[Hook from research]

[2-3 benefits, personalized]

[Social proof or stat]

[CTA button/link]

Best,
[Your Name]
[Signature]
```

### 6. Polish & Test
- Emojis: 1-2 max
- Line length: <60 chars
- Personalization: [First Name], niche refs
- Variants: A/B test 2-3 full emails

## Examples

**Pitch ClawHub to AI Devs:**
Research: "AI agent tools reddit", "OpenClaw alternatives"
Hook: "Tired of brittle AI wrappers?"
Solution: "ClawHub skills: Plug-and-play for OpenClaw"

**Acreage Newsletter:**
Research: "Saskatchewan acreage business ideas"
Content: Weather skill integration, land dev tips.

## Pro Tips
- Always research first—stale copy flops.
- Use `canvas` for email previews.
- A/B subjects with `message` polls.
- Track: UTM links for analytics.
