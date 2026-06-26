---
description: Generate daily batch of Hacker News comments in founder's expertise areas. Trigger phrases: "draft HN comments", "generate HN karma", "write HN posts", "HN comment batch", "build HN karma", "compose HN replies".
---

# Improve HN Karma

Daily workflow to produce 4–5 ready-to-post Hacker News comments (80–150 words, up to 200 on highly technical threads) on active, relevant threads to build karma on a low-karma account. User supplies expertise area(s); skill identifies high-visibility threads, mines underexplored angles, and drafts copy-paste-ready comments with threading instructions.

## Step 1 — Fetch HN front page and secondary pool

Fetch `[url] and extract story titles, item IDs, points, comment counts, and age for top ~30 items. Cross-reference with HN /best for the week to widen candidate pool to ~12 threads. Capture raw thread data in a structured list.

**What to capture:** Thread ID, title, URL, points, comment count, age (minutes/hours), topic keywords.

## Step 2 — Apply sweet-spot filter

Retain only threads matching ALL criteria:
- Points: 50–200 (not 1000+, which buries comments)
- Comment count: 30–150 (not 900+, which buries visibility)
- Age: 1–8 hours old (not 1+ day, which decays)
- Topic: In founder's stated expertise area (AI/dev tools/agents/data-eng/infrastructure/etc.); exclude politicized threads

**Decision point:** If fewer than 4 threads pass the filter, expand age window to 12 hours or broaden expertise keywords. If still thin, note in output and proceed with available candidates.

**What to capture:** Shortlist of 4–8 qualifying threads with full metadata.

## Step 3 — Mine existing comment angles for each thread

For each shortlisted thread, fetch the item page (HN comments section) and extract the top 5–10 comments, capturing username and quoted text. Analyze: What perspective, technical detail, or counterexample has NOT been mentioned yet? Identify the gap.

**Angle-selection rule:** Reframe at one level of granularity finer than the current thread discussion. Move from broad claim to specific technical counterexample. Concede a named commenter's point, then add a new lever. Never echo the top criticism or obvious take.

**What to capture:** Per-thread gap analysis: "Angle not yet covered: [specific technical insight or framing]"; identify 1–2 named users to engage with or acknowledge.

## Step 4 — Draft comment copy for each angle

For each shortlisted thread + identified angle, write a comment:
- **Length:** 80–150 words; up to 200 words on highly technical threads only
- **Style:** Sentence case, technical first-person, no em-dashes (replace with commas, colons, or semicolons)
- **Structure:** State the angle clearly; cite a specific technical example, counterexample, or design principle; offer a lever or next-step question (optional)
- **List form:** Only if items are mutually exclusive and independent; trim ruthlessly

**What to capture:** 4–5 ready-to-post comments, each tagged with thread URL, reply target (top-level or reply-to username), character count, why-this-thread, why-this-angle.

## Step 5 — Write plan document

Output a markdown file (karma-plan-YYYY-MM-DD.md) with:
1. 4–5 comments in copy-paste-ready form, each with: thread URL, reply target username, why-this-thread (topic relevance), why-this-angle (gap it fills)
2. Posting order + spacing guidance (e.g., "Post #1 immediately, wait 2 hours before #2 to avoid clustering")
3. Quality checklist: character count, no em-dashes, no self-promo, sentence case, engagement signal (question or concession)

**What to capture:** Complete, executable plan file with all comments and meta-instructions.

## What's next?

```
Review the karma plan and post the comments in the recommended order, then track upvote counts over 24–48 hours.
```

```
If a comment gets buried (0 or negative votes after 12 hours), analyze why and refine the angle-selection rule for tomorrow's batch.
```

```
Once the account reaches 50+ karma, test a URL submission on a moderately active thread to measure community reception.
```

## Notes for the model

- **Sweet-spot justification:** Threads with 50–200 points and 30–150 comments are in the "rising" phase—high visibility, not yet buried. Threads 1–8 hours old are still accumulating comments and upvotes. Older threads decay; hotter threads drown out new voices.
- **Angle mining is critical:** The skill's ROI depends on surfacing a perspective no one else has articulated. Read the top comments carefully. Look for contradictions, unstated assumptions, or domain-specific details the mainstream discussion glosses over. This is where karma comes from.
- **Word count exception:** Allow up to 200 words only on threads already rich in technical discussion (e.g., deep dives on Rust internals, distributed systems, compiler design). Stay strict on 80–150 for softer topics.
- **Em-dash rule:** HN's classic style eschews em-dashes. Replace "—" with commas, colons, or semicolons. "tool A — which does X" becomes "tool A, which does X" or "tool A: does X."
- **No self-promo:** Do not link to personal projects, products, or blog unless it is a direct, earned reference to prior art. Do not mention the founder's own account or business.
- **Timing:** Post during hours when the target thread is still active (check comment velocity). Avoid posting all at once; space them 2–4 hours apart to maximize independent visibility.
- **Fallback if thread is slow:** If fewer than 4 threads qualify, include a note in the plan: "Only 3 threads qualified today; recommend expanding expertise scope or checking HN/best again in 4 hours."

## Error handling

| Error | Diagnosis | Tell the user |
|-------|-----------|---------------|
| HN front page unreachable (HTTP 5xx) | Server issue or rate-limiting. | "HN is temporarily unavailable. Retry in 10 minutes or fetch /best instead." |
| Fewer than 4 qualifying threads after filtering | Too few active threads in expertise area today, or filter is too strict. | "Only N threads qualified today. Consider broadening expertise keywords or lowering point floor to 40. Proceeding with N comments." |
| All top comments on a thread are already 200+ words | Angle may be saturated. | "This thread's top comments are already exhaustive. Consider skipping it or waiting 2 hours for decay." |
| Identified angle requires 250+ words to explain | Scope creep; angle is too complex for the format. | "This angle needs too much context. Simplify to one technical counterexample or pick a different thread." |

