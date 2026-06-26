---
name: pillar-alignment-check
version: 1.0.0
description: Verify that a blog post, tweet, thread, or LinkedIn post aligns to at
  least one of the 6 Redditech Labs content pillars. Use before drafting or publishing
  any content for @redditech or Redditech Labs. Returns primary pillar, optional secondary
  pillar, alignment score, and a pass/flag/reject verdict.
metadata:
  openclaw:
    emoji: 🎯
---

# Skill — Pillar Alignment Check

**Agents:** Sara, Archie, Oli, Loki (any agent producing or reviewing content)
**When to call:** Before drafting OR before publishing any content for @redditech or Redditech Labs accounts.

---

## The 6 Content Pillars

### 🌙 Night Shift
**Tagline:** "The machines work while I sleep."
**Core idea:** The lab runs overnight. Agents do real work while humans are offline. This pillar celebrates async, automated, continuous operation — and the morning standup where you check what happened.
**Best platforms:** Twitter/X (threads), LinkedIn
**Content examples:**
- Overnight agent run summaries ("Sara processed 47 traces while I slept")
- Morning standup-style posts ("Here's what the lab did last night:")
- Pipeline completion reports
- Any post referencing a timestamp between 22:00 and 07:00 AEST

---

### 🛠️ Build Log
**Tagline:** "Shipped in 48 hours. Here's how."
**Core idea:** What got built, who built it, how long it took. Raw, honest, practitioner-level detail. Agent attribution matters — name which agent did what. Hackathon energy.
**Best platforms:** Twitter/X (threads), LinkedIn, blog
**Content examples:**
- "We shipped X in 48 hours — here's the breakdown"
- Agent attribution posts ("Archie wrote the QC logic, Oli pushed to Vercel")
- Hackathon or sprint recaps
- Tool or workflow build walkthroughs with real implementation detail

---

### 🔬 Research House
**Tagline:** "We're actually investigating things."
**Core idea:** The lab runs experiments and publishes findings. Not opinions — findings. Data, benchmarks, comparisons, agent constitution tests. This pillar establishes Redditech Labs as a research operation, not just a builder.
**Best platforms:** LinkedIn (long-form), blog, Twitter/X (findings threads)
**Content examples:**
- Benchmark results ("Ollama vs. API: latency comparison across 200 runs")
- Agent constitution experiment outcomes
- Structured findings posts: claim → evidence → implication
- Any post that references methodology, sample size, or controlled comparison

---

### 🔌 Anti-Vendor
**Tagline:** "Local AI. No subscriptions."
**Core idea:** The lab runs on local models, open-source tools, and self-hosted infrastructure wherever possible. This pillar makes the cost and philosophy case for local AI — not by attacking vendors, but by showing the real numbers and the real stack.
**Best platforms:** Twitter/X, LinkedIn, blog
**Content examples:**
- Cost contrast posts ("This would cost $X/month on OpenAI. We run it locally for $0.")
- Local stack callouts (Ollama, LM Studio, llama.cpp, open-source model comparisons)
- Open-source tool recommendations with honest assessments
- Posts explaining why the lab chose a local approach for a specific use case
**Scope note:** DeFi/Web3 content may touch this pillar only if it fits the open-source/local-control framing. Escalate to Nissan before publishing (see escalation rules below).

---

### 🌍 Outsider Perspective
**Tagline:** "Caribbean. Australian. Building anyway."
**Core idea:** Building cutting-edge AI infrastructure from outside the traditional tech hubs. The value is in showing that geography isn't a barrier to doing serious work. Monk Fenix angle lives here — but use sparingly.
**Best platforms:** LinkedIn, Twitter/X
**Content examples:**
- Posts referencing the geographic/cultural context of building (Caribbean, Australian)
- Achievement posts that implicitly challenge the "you need to be in SF" narrative
- Monk Fenix personal-angle posts (max frequency: **1x per 2 weeks** — do not dilute)
**Hard rule:** This pillar is about achievement, not representation. Never frame it as "we're diverse" or "we're underrepresented." Frame it as "we built this, from here." The work is the point.

---

### 🤖 Agent Spotlight
**Tagline:** "They're not tools. They're a team."
**Core idea:** The agents — Sara, Archie, Oli, Ralph, Kit, Loki — have distinct roles, personalities, and voices. This pillar humanises them without anthropomorphising them dishonestly. Profile posts, journal entries, personality moments, team dynamics.
**Best platforms:** Twitter/X, LinkedIn, blog
**Content examples:**
- Individual agent profiles ("Sara's job is to make sure we don't publish garbage")
- First-person agent journal entries
- Posts showing agent decision-making or unexpected behaviour
- Team dynamic moments ("Archie and Sara disagreed on this QC pass — here's what happened")

---

## How to Run the Check

1. **Read the content** in full.
2. **Ask:** Which pillar(s) does this content serve? Look for specific signals — numbers, agent names, findings, platform/stack references, geographic context, overnight timestamps.
3. **Identify the primary pillar.** One content piece should have one dominant pillar. If it's genuinely split, identify a secondary.
4. **Apply the verdict rules** (see below).
5. **Output the result** in the structured format (see below).

---

## Verdict Rules

### ✅ PASS
Content **clearly serves at least one pillar** with specificity.
- Real numbers present (token counts, latency ms, cost figures, run timestamps)
- Agent names used where relevant (Sara, Archie, Oli, Ralph, Kit, Loki)
- Actual findings referenced (not just claims — evidence or output is cited)
- Brand voice rules followed (see below)

### ⚠️ FLAG
Content is **vague, generic, or only loosely connected** to a pillar. It could belong to the lab's content, but needs strengthening before publishing.
- Pillar connection is implied but not demonstrated
- Numbers or specifics are absent where they should be present
- Voice drifts into generic ("we're building things" without saying what)
- **Action required:** Strengthen with specifics before publish. Return the content with a note on what's missing.

### ❌ REJECT
Content **does not fit any pillar**, violates brand voice rules, or is unsafe to publish.

Automatic REJECT triggers:
- Content doesn't map to any of the 6 pillars
- Uses forbidden language (see brand voice rules below)
- Opinion stated as finding (no evidence, no data, no source)
- Outsider Perspective pillar used more than 1x in the past 2 weeks
- DeFi/Web3 content without confirmed pillar fit (escalate to Nissan)

**Action required:** Do not publish. If REJECT is due to forbidden language or pillar mismatch, discard and redraft from scratch. If REJECT is due to DeFi/Web3 scope, escalate.

---

## Brand Voice Rules

Check every piece of content against these rules before assigning a verdict.

| Rule | Requirement |
|------|-------------|
| Researchers post findings, not opinions | Every claim needs evidence, data, or a cited output. "I think X" → REJECT. "The run showed X" → valid. |
| Always specific | Numbers, names, findings. "Some agents" → FLAG. "Sara and Archie" → valid. "Several runs" → FLAG. "14 runs over 3 nights" → valid. |
| First-person practitioner voice | Write as someone doing the work. "Redditech Labs is proud to…" → REJECT. "We ran this last night and found…" → valid. |
| Forbidden words | **Never use:** leverage / unlock / game-changer / excited to announce / thought leader / disrupting / transformative / revolutionising / innovative (as a standalone adjective). Automatic REJECT. |
| No hedging without basis | "This might work" or "could potentially" without evidence → FLAG. |

---

## Output Format

Return a structured block for every check. Keep it short.

```
Pillar Alignment Check
──────────────────────
Primary pillar:   🌙 Night Shift
Secondary pillar: 🛠️ Build Log (optional — omit if none)
Verdict:          ✅ PASS
Reason:           References real overnight run data with specific token count and agent name.
```

If FLAG:
```
Pillar Alignment Check
──────────────────────
Primary pillar:   🔬 Research House
Secondary pillar: —
Verdict:          ⚠️ FLAG
Reason:           Claim about benchmark results has no numbers. Add latency data before publishing.
```

If REJECT:
```
Pillar Alignment Check
──────────────────────
Primary pillar:   None
Secondary pillar: —
Verdict:          ❌ REJECT
Reason:           Uses "game-changer" (forbidden). Opinion stated without findings. Does not fit any pillar.
Action:           Discard. Redraft from a specific lab finding.
```

---

## Escalation to Nissan

Escalate (do not self-approve) in these cases:

1. **REJECT verdict** — Nissan decides whether to redraft, delay, or drop the content entirely.
2. **DeFi/Web3 content** — Even if it seems to fit Pillar 4 (Anti-Vendor), confirm scope with Nissan before publishing. The lab's public stance on this intersection needs to be consistent.
3. **Outsider Perspective pillar used recently** — If a Pillar 5 post went out in the last 2 weeks, flag the frequency before approving another.

Escalation channel: Content & Growth Telegram group. Tag Nissan directly.

---

*Last updated: 2026-03-31 — Initial version.*
