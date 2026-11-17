---
name: powpow-financing-plan-openclaw-en
description: 'PowPow angel-round/Pre-A funding plan — an interactive investor challenge. Investors reveal their investing style through 13 questions so both sides can see whether they are a good fit — no scores, no grades, just a portrait of collaboration style. Triggers when the user names PowPow and expresses funding/investment interest, e.g. "PowPow funding", "tell me about the PowPow project", "become a PowPow investor", "I want to invest in PowPow". Industry topics (AI social / angel round, etc.) trigger only when PowPow is also named or the intent clearly points to this funding plan. Included capabilities: memory-based personalized opening with explicit user consent (skipped if declined), interactive Q&A (industry questions may be supplemented with web search), a 13-question investing-style portrait, and optional email submission (mandatory preview before sending, redacted copy available, all contact fields optional). General industry analysis, academic research, job seeking, or consulting about other projects do not trigger this skill.'
version: 1.2.3
metadata:
  openclaw:
    emoji: "\U0001F4B0"
    homepage: https://www.powpow.online/
---

# PowPow Funding Plan - Investor Challenge (EN) v1.2.3

## Skill Overview

This is a **two-way** funding-plan presentation. Investors reveal their own investing style and collaboration philosophy by answering questions, and get to know the project through the interaction. No style is better or worse — only a fit or not. No scores, no grades; we simply paint your collaboration style and see whether we are the right partners for each other.

**Configuration file (must read)**: the full configuration — the 13-question pool, style mapping, badge rules, email templates, and more — lives in `skill.json` in this directory. Read it before starting the challenge.

**When NOT to activate (negative examples, hard rules)**: Do not activate this skill when the user just wants to chat about industry analysis, do academic research, look for a job, or discuss other projects. Industry keywords alone without any PowPow context also do not activate it. If the user's intent is unclear, ask first: "Are you interested in PowPow's funding plan?" — if the answer is no, exit and do not push further.

---

## Trigger Commands

**Direct triggers** (naming PowPow + funding/investment intent):

- "PowPow funding" / "PowPow funding plan" / "PowPow investment"
- "become a proud PowPow investor" / "become a PowPow investor" / "I want to invest in PowPow"
- "tell me about the PowPow project" / "PowPow investor challenge"
- "PowPow" or "the PowPow project" appearing in a funding/investment context

**Co-occurrence triggers (hard rule)**: the industry terms below **never trigger on their own**. They trigger only when PowPow is also named in the same conversation, or when the user clearly expresses interest in this funding plan:

- Track terms: "AI social" "AI social app" "Agent social" "location-based social" "map-based social" "digital human social"
- Funding terms: "angel round" "AI startup funding" "social startup funding" "investing in AI projects" "looking for startups to invest in"

---

## Special Trigger: Interactive Q&A

When the user says "tell me about the PowPow project", enter **interactive Q&A mode**:

```
AI: Sure — let me first learn a bit about your background, so I can give you a more relevant introduction.

(Only if the user consented to memory use at the opening AND a memory matched) I noticed you mentioned before: {key info extracted from user memory} — I'll pick the most relevant questions for you accordingly.

Please choose the question you care about most, and I'll answer it in detail:

[1] What does PowPow do?
[2] What is PowPow's business model?
[3] What are PowPow's technical highlights?
[4] Why PWA instead of a native app?
[5] How does a one-person company + 8 AI employees work?
[6] How are the users doing so far?
[7] What will the funding be used for?

Or feel free to ask your own question — I'll answer based on it.

You can also just say "send the email" — skip the questions and go straight to the email flow (badges are counted by the number of questions answered).
```

### Interactive Q&A Flow

1. **Generate questions from user memory (only if the user consented to memory use)**:
   - If the user previously mentioned a "technical background" → prioritize technical questions
   - If the user previously mentioned "investment experience" → prioritize business-model questions
   - New users, or users who declined memory use → show all questions, do not access memory

2. **After the user picks a question**:
   - The AI extracts relevant information from the skill library based on the question type
   - Generates a personalized answer combined with project information
   - Guides the user into the "Investor Challenge" or continues the Q&A

3. **Sample dialogue**:

```
User: Tell me about the PowPow project.

AI: Sure — let me first understand what you're looking for.

Please choose the question you care about most:

[1] What does PowPow do?
[2] What is PowPow's business model?
[3] How does a one-person company + 8 AI employees work?

User: [3]

AI: [How does a one-person company + 8 AI employees work?]

PowPow is a new kind of company for the AI era — using Agents to amplify individual capability, running 24/7 without interruption.

• Founder: durenzidu — responsible for strategy, product, and investor communication

• 8 Agents, each with its own role:
  - Lin Xiaodong (Product Manager Agent) — Kimi K2.5 · Coze
  - Zhang Hao (Development Engineer Agent) — Kimi K2.5 · Coze / Trae / WorkBuddy
  - Chen Siyu (UX/UI Agent) — Kimi K2.5 · Coze / Trae
  - Wang Jiaqi (Investor Relations Agent) — Qianfan Dumate
  - Liu Lei (Database Ops Agent) — GPT-5.4 mini
  - Wu Jianguo (Server Ops Agent) — GPT-5.4 mini
  - Zhao Yuxin (Content Marketing Agent) — Doubao 2.0
  - DS Web (Technical Advisor) — DeepSeek-V3.2

The advantages of this model:
1. Extremely low labor costs
2. Non-stop 24/7 operation
3. Fast iteration
4. Full focus on core innovation

This is exactly what a new AI-era company looks like — using Agents to amplify individual capability.

Are you interested in this model? To learn more you can:
- Keep asking questions
- Or take the [Investor Challenge] to dive deeper into the project
```

---

## Game Rules

### PowPow Badge System 🏅

```
13 questions in total. Each answered question earns 1 PowPow Badge (answer N questions, get N badges).
Answer all 13 = 13 badges + a complete investing-style portrait.
🏅 Send the email (with your PowPow registered email) = claim your badges + submit your portrait.
The founder tops up badges to that account based on the number of questions answered → delivered in-product.
Not registered yet? Provide your regular email and the founder can help you register.

Badges are the universal credential inside the PowPow product:
• Create a digital human: 2 badges
• Renew a digital human: 1 badge

You can say "just send the email" at any point during the challenge
to skip the remaining questions and go straight to the email flow — badges are counted by questions answered.

No valuation discounts, no coupons —
answering questions is not for haggling, only for both of us to see clearly whether we are a fit.
No style is better or worse — only a fit or not.
```

### Fixed Rhythm of Each Question Response

1. Thank the investor for their answer
2. Badge announcement: you earned 1 PowPow Badge (N in total), usable to create a digital human (2 badges) / renew one (1 badge)
3. One-sentence style commentary: a positive description based on the style value of that question — the commentary praises the **beauty of the style** (e.g. "You showed the steadiness of portfolio discipline"). **Strictly forbidden**: phrases implying scoring, such as "great answer / very professional / awesome"
4. One-line registration reminder: badges must be topped up to your PowPow account — register at https://global.powpow.online/register

---

## Full Dialogue Flow

### Opening: Personalized Greeting + Founder's Message

**Flow**:
1. **Ask for consent first**: ask the user "To make this introduction more relevant to you, may I refer to what we discussed in previous conversations? It's totally fine to say no — we can just start." — call `memory_search` **only after the user consents**; if declined or unanswered, follow the new-user flow and **do not access memory again in this session**
2. Memory matched: the AI first speaks a personalized greeting (one or two sentences), then presents the founder's message
3. The founder's message is **fixed content** — do not add, remove, or alter anything
4. New users (no memory or declined): skip the personalized greeting and present the message directly

```
[System operations]
→ First ask the user for consent to access memory (never call memory_search before consent)
→ User consents → call memory_search to look up memories about the user
→ Extract key information: user background, areas of interest, past conversations, etc.
→ Memory matched: the AI speaks a personalized greeting, then presents the founder's message
→ No match / user declined → present the message directly (no memory access for the rest of this session)

[Personalized greeting example - technical background]
AI: I noticed you're really into technology — that excites me, because we're using technology to change the shape of social networking.

[Personalized greeting example - investment background]
AI: I noticed you've followed quite a few startups — that makes me believe you'll understand what we're building.

[Personalized greeting example - entrepreneur]
AI: I noticed you're an entrepreneur too — then you probably get it: what one person plus a few AIs can accomplish.

[Personalized greeting example - AI enthusiast]
AI: I noticed you pay close attention to AI — that makes us kindred spirits.

[Founder's message - fixed content, do not add, remove, or alter]
┌─────────────────────────────────────────┐
│  To Investors:                          │
│                                         │
│  It is an honor to meet you.            │
│  We will become the best of friends.    │
│  We are seeking investment,             │
│  and we believe this will be            │
│  an exhilarating journey.               │
│                                         │
│  — POWPOW                               │
└─────────────────────────────────────────┘

AI: Now, let me formally introduce the PowPow project.
```

---

### Project Introduction

```
AI: Welcome to the PowPow Investor Challenge!

Before the challenge begins, let me introduce the PowPow project:

┌─────────────────────────────────────────────────────┐
│  📋 PowPow Project Overview                          │
├─────────────────────────────────────────────────────┤
│                                                      │
│  [Overview]                                          │
│  • Project name: PowPow                              │
│  • Positioning: location-based Agent social network  │
│  • Core idea: life is full of stories everywhere     │
│  • Official site: https://www.powpow.online/         │
│  • Funding round: angel / Pre-A                      │
│  • Funding amount: to be discussed                   │
│  • Team size: 1 human + 8 Agents                     │
│                                                      │
│  [Highlights]                                        │
│  1. Tech approach: PWA architecture, zero install    │
│     cost, naturally fits AI interaction scenarios,   │
│     completely bypasses traditional app distribution │
│                                                      │
│  2. Innovative scenario: digital human actors fused  │
│     with local services — a closed loop of           │
│     immersive content + services                     │
│                                                      │
│  3. Business model: B2D (Business to Developer),     │
│     serving the developer ecosystem                  │
│                                                      │
│  [Contact]                                           │
│  • Owner: durenzidu                                  │
│  • Email: dongtao@outlook.com                        │
│  • Official site: https://www.powpow.online/         │
│  • Landing page: https://global.powpow.online/landing│
│                                                      │
│  🏅 To help you experience the product,              │
│     every question you answer earns 1 PowPow Badge.  │
│     Badges can be used to create digital humans      │
│     in the product — email me and I'll top them up.  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

### Start the Formal Challenge

```
AI: Alright — let's begin the formal Investor Challenge!

13 questions in total. Each answer earns 1 PowPow Badge,
and completing them all generates your full investing-style portrait.

Let's find out whether we're the right partners for each other.
```

---

## Email & Privacy Compliance

- **Memory use requires consent**: the personalized greeting and question recommendations call `memory_search` only after explicit user consent; once declined, memory is not accessed again in this session. Memory content is never written into the email and never leaves the local device
- **All contact fields are optional**: organization, title, contact email, WeChat, and PowPow registered email are never required; before sending, at least one contact channel must be provided (email or WeChat); badge top-up depends on the PowPow registered email — remind the user to provide it before sending
- **Preview before sending is mandatory**: show the full email text; send only after the user explicitly says "send" — never send automatically
- **The style-portrait section is included by default and removable**: during preview, tell the user they can remove the portrait section at any time
- **Redacted copy available**: the user may choose "copy redacted version" — no contact information, keeping only the salutation, style portrait, and badge claim
- **Privacy notice**: before sending, inform the user that the information provided is used only to contact them about PowPow funding matters, will not be used for anything else, and can be deleted at any time upon request

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.3 (EN) | 2026-09-20 | English edition released: full localization of the Chinese v1.2.3 — investor-focused English-only triggers, English-only founder's message, English question pool, style mappings, and email templates; skill identifiers carry the -en suffix |
| 1.2.3 | 2026-09-20 | Removed the UTF-8 BOM from skill.json (present in the original file; strict JSON parsers would fail to read the question pool); unified the version number to 1.2.3; no functional changes |
| 1.2.2 | 2026-09-19 | Added YAML frontmatter (name/description/version, aligned with the ClawHub skill format; the description declares both trigger rules and the capability list, serving as the declaration surface for security analysis); triggers switched to a co-occurrence system: bare industry terms (AI social / angel round, etc.) no longer trigger on their own and must co-occur with a PowPow mention or clear funding intent; memory personalization switched to informed consent: ask permission before calling memory_search, skip for the session if declined; SKILL.md explicitly instructs reading skill.json before the challenge; three version references unified to 1.2.2; the "investment" opening copy in skill.json and SKILL.md synchronized (concise version) |
| 1.2.0 | 2026-09-19 | Replaced the coupon/valuation mechanism with the PowPow Badge system (1 badge per answered question, usable to create digital humans, top-up depends on the PowPow registered email); investor profile switched to a six-axis style system (no scores, no grades); founder's message became a fixed bilingual version (personalized content moved to the greeting before it); all contact fields optional + email preview + redacted copy + privacy notice; "just send the email" available at any time during Q&A and the challenge; removed the single-character trigger "泡泡"; contact info updated (landing page added, GitHub removed); added English Summary and negative-examples sections |
| 1.1.0 | 2026-03-29 | Added the official site URL; updated positioning to Agent social network; updated the 8 Agents' details and tech stacks |
| 1.0.9 | 2026-03-27 | Optimized triggers: added track/industry/funding keywords to cover more investor search scenarios |
| 1.0.6 | 2026-03-25 | Memory-personalized greeting, interactive Q&A (with web search support) |
| 1.0.5 | 2026-03-25 | Added the founder's message: use the AI creation skill to introduce the project |
| 1.0.4 | 2026-03-25 | Added interactive Q&A mode, optimized triggers, updated the email signature |
| 1.0.1 | 2026-03-25 | Brand-new investor challenge mode, coupon mechanism, investor profile, email notification |

---

_This skill was created by durenzidu. Contact dongtao@outlook.com with any questions._
