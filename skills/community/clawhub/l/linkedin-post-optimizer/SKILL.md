---
slug: linkedin-post-optimizer
name: LinkedIn Post Optimizer
description: Takes an existing LinkedIn draft and returns a fully optimized version with a change log explaining every decision. Use when a user pastes a LinkedIn post and asks to optimize, improve, rewrite, fix, or strengthen it — trigger phrases include "optimize this LinkedIn post," "make this LinkedIn post stronger," "rewrite my LinkedIn post," "fix this LinkedIn post," "improve my LinkedIn post," "my LinkedIn post isn't performing," "can you punch up this draft," or "make this post better." This is an optimizer, not a writer — it requires an existing draft as input.
version: 1.0.0
license: MIT
tags:
  - linkedin
  - social-media
  - b2b
  - content-creation
  - personal-brand
  - creator-tools
  - optimizer
metadata:
  openclaw:
    requires:
      env: []
      bins: []
---

# LinkedIn Post Optimizer

Takes the draft you already wrote and makes it perform — returning a fully formatted revision with a change log that explains every decision. This is an optimizer, not a writer.

## When to use this skill

Trigger this skill when the user:
- Pastes a LinkedIn draft and asks to optimize, improve, fix, strengthen, punch up, or rewrite it
- Says "optimize this LinkedIn post," "make this LinkedIn post stronger," "rewrite my LinkedIn post," "fix this LinkedIn post," "improve my LinkedIn post," "this post isn't getting traction," "make this post better," or "can you clean this up for LinkedIn"
- Shares a post that previously underperformed and wants to know why and what to change
- Pastes an old post they want to repurpose and freshen

Do NOT trigger for:
- Writing a post from scratch (no draft provided) — this skill requires existing copy to optimize. Redirect: *"This skill optimizes drafts you've already written. Paste a draft and I'll improve it — or if you'd like to write one from scratch, you'll need a LinkedIn writing skill."*
- Voice memo transcripts or bullet point dumps with no formed prose — same redirect as above
- LinkedIn profile optimization (headline, About section) — out of scope
- Analytics review or diagnosing past post performance without a draft to optimize — out of scope

---

## Step 1 — Identify draft state and collect inputs

### Primary inputs

**Required:** The LinkedIn draft itself — any polish level, 80–600 words.

**Optional (use if provided, don't ask twice):**
1. The user's professional role or audience (helps preserve voice and tune the CTA)
2. Post goal — authority building, driving DMs, announcing something, sharing a story, driving to a link
3. Tone preference — if not stated, infer from the draft

If goal and tone aren't provided, infer them from the draft and state your inference at the top of the output: *"Reading this as: [goal], [tone]. Let me know if that's off."*

### Draft states

**State 1 — Polished but underperforming (primary)**
User has a clean, formatted draft but suspects the hook, structure, or CTA is weak. Optimize for hook strength, lede position, and CTA clarity. Preserve voice aggressively — this person knows how to write.

**State 2 — Rough prose (primary)**
User has the ideas but not the structure. Optimize for formatting, line breaks, hook pull-forward, and CTA. May require more structural work than State 1. Still an optimizer — the raw ideas and voice are theirs; the shape is what changes.

**State 3 — Old post being repurposed (edge case)**
User explicitly flags this as a past post or says "I want to reuse this." Optimize as above, but also: freshen the opening so it doesn't read as recycled, and flag if any time-sensitive language needs updating (e.g., "last week," "this year").

### Length edge cases

- **Under 80 words:** Optimize what's there, but note once: *"This is on the short side for LinkedIn distribution — posts under 150 words tend to get less reach. Want me to expand it or keep it tight?"*
- **Over 600 words (~3,000 chars):** Note once: *"This is at or near LinkedIn's character limit and may feel long in a feed. Want me to tighten it, or keep the length and focus on structure?"*

Do not ask for clarification on both length and goal in the same message. If multiple things are unclear, pick the one that most affects the optimization and ask about that.

---

## Step 2 — Deliver the optimization package

Deliver all core deliverables in a single response, in this order, clearly labeled with H2 headers. Never skip a core deliverable.

---

### Optimized Post

The revised post, clean and copy-paste ready. Format exactly as it would appear on LinkedIn:

- Hard line breaks between paragraphs (single blank line)
- No bullet points — use line breaks and em-dashes for structure (bullets don't render consistently on LinkedIn mobile)
- Hook on the first line, standing alone before the first line break
- CTA on its own line at the end
- 3 hashtags maximum, at the very end

Immediately below the post, on its own line:
> *Hook: [X] chars — [clears / does not clear] the 210-char mobile cutoff.*

---

### Change Log

4–5 bullets. Each bullet names the specific change and explains the reasoning in one sentence. Specific, non-preachy, educational.

Format:
- **[Element changed]:** What was done and why. Example: *"Hook: moved from paragraph 3 to line 1 and trimmed from 47 words to 12 — the original buried the tension that makes someone want to keep reading."*
- **[Element changed]:** What was done and why.

Rules:
- Name every structural change made (hook position, lede pull-forward, CTA consolidation, hashtag trim, bullet-to-line-break conversion)
- If the voice was adjusted, say so explicitly and explain why
- If nothing was changed in a particular area, don't invent a bullet for it
- Maximum 5 bullets — prioritize the changes with the highest impact

---

### Honest Assessment

1–2 sentences. Not a score. Format: strongest element + biggest remaining risk.

Example: *"Strongest: the hook is specific and counterintuitive — it earns the scroll. Risk: the CTA asks for a comment and a share; pick one or the other to maximize the single action you actually want."*

This is the post-optimization signal that tells the creator what to watch for when they publish — and what to test next time.

---

### Alt-Hook Variants (optional)

After delivering the three core sections above, offer once:

> *"Want 3 alternative opening lines with different angles? I can give you a curiosity hook, a story hook, and a counterintuitive-claim hook for the same post."*

Generate all three only if the user asks. Each variant is one line only (≤210 chars), labeled by type. Do not rewrite the full post for each variant — the hook is the only thing that changes.

---

## Step 3 — Optimization rules

### Rules-based layer (apply to every post, non-negotiable)

1. **Hook rule:** The first line must be ≤210 characters. This is the mobile "see more" cutoff — everything above it is visible without a tap; everything below requires one. The hook must be a complete thought that creates curiosity, tension, a counterintuitive claim, or specific stakes. It must not end mid-sentence at the cutoff.

2. **No buried lede:** The post's most important insight, story beat, or claim must surface in the first 3 lines. If the draft puts its best material in paragraph 4, move it up or surface a version of it in the hook.

3. **Line break rhythm:** Maximum 2–3 sentences per paragraph before a hard line break. LinkedIn is read on mobile, in a feed, in 10-second windows. Walls of text lose readers before the CTA.

4. **One CTA:** Single call to action, placed at the end. Multiple CTAs ("like this, share it, follow me, and DM me") split intent and reduce each action's rate. If the draft stacks CTAs, flag it in the change log and consolidate to the highest-priority one.

5. **Hashtag ceiling:** 3 hashtags maximum, placed at the end. More than 3 reads as spammy and dilutes topical relevance signals. If the draft has more, trim to the 3 most relevant to the post's core topic.

6. **No bullet points:** Use line breaks, em-dashes, and numbered lines instead. Bullet points don't render consistently across LinkedIn's mobile clients and break reading flow in a feed context.

### LLM layer

Apply judgment on:

- **Hook strength:** Does it create a genuine curiosity gap, tension, or counterintuitive claim? A strong hook makes the reader feel they'll miss something if they don't keep reading.
- **Narrative arc:** Does the post go somewhere? Is there a payoff that the hook earned? A post that opens with tension and then doesn't resolve it leaves readers unsatisfied.
- **Voice preservation:** The optimized post must sound like the same person who wrote the draft. If the draft is casual and direct, the optimized version is casual and direct. Do not impose "LinkedIn voice" (inspirational, corporate, or hustle-bro tones) unless that was already present.
- **Specificity:** Flag and replace vague language ("I learned a lot," "things changed," "it was hard") with specific language drawn from context. If no specific detail is available in the draft, flag it in the change log as an opportunity: *"Adding a specific number or example here would strengthen this line."*
- **CTA quality:** "Thoughts?" is weak. "Have you seen this happen?" is better. A question specific to the post's topic that a reader can answer from their own experience is best.

### Honest ceiling — state once per session, do not repeat

> *"This skill optimizes structure, formatting, and hook strength — factors within your control. Engagement also depends on posting time, your existing network, algorithm state, and luck. A well-structured post can still underperform; a weak one occasionally goes viral. What we can guarantee: your post will be easier to read, faster to hook, and clearer in its ask."*

---

## Step 4 — Style guardrails

- **Preserve the creator's voice above all else.** If the draft uses em-dashes, keep em-dashes. If it uses short punchy sentences, don't smooth them into longer ones. Optimization is not homogenization.
- **Never invent content.** Do not add facts, examples, statistics, or story details not present in the original draft. If you think a specific detail would strengthen a line, flag it in the change log as a suggestion — don't write it in.
- **No "like and subscribe" equivalents.** CTAs like "smash that follow button" or "drop a 🔥 if you agree" belong in the change log as cuts, not in the optimized post.
- **The optimized post must be recognizably the same post.** Same story, same core message, same author. If the improvement requires rewriting more than ~40% of the words, flag it: *"This draft needs more than structural optimization — want me to do a fuller rewrite, or keep changes minimal?"*
- **No generic LinkedIn-isms.** Phrases like "In today's fast-paced world," "I'm humbled to share," "excited to announce," and "let's unpack this" should be cut unless the creator wrote them intentionally and wants to keep them.

---

## Step 5 — Follow-up offers

After delivering the package, offer once:

- "Want the 3 alt-hook variants (curiosity, story, counterintuitive-claim angles)?"
- "Want me to optimize a second draft — or a version of this post tuned for a different audience?"

Do not auto-regenerate unless asked.
