---
name: multi-variant-scripting
version: 1.0.0
description: "Produce 2-4 genuinely distinct video script variants from a single brief — technical/cinematic (A), general/walkthrough (B), developer/explainer (C). Uses interleaved scene-by-scene writing to prevent drift, jargon bleed, and length creep. Includes word count targets and an output checklist for Finn handoff."
metadata:
  {
    "openclaw": {
      "emoji": "🎬",
      "requires": {
        "bins": [],
        "env": []
      },
      "primaryEnv": null,
      "network": {
        "outbound": false,
        "reason": "Document writing only. No network calls required."
      },
      "security_notes": "All operations are performed locally. No data leaves the user's machine."
    }
  }
---

# Skill: Multi-Variant Scripting

**Owner:** Sara  
**Version:** 1.0  
**First used:** 2026-03-24 (Reddi Agent Protocol — 3-variant pipeline)

---

## What This Does

Produces 2–4 distinct script variants for the same product from a single brief. Each variant serves a different audience or communication style. Variants must be genuinely distinct — not the same script with synonyms swapped.

**When to use this skill:** Any time the demo-video playbook calls for 2+ variants. Read this before writing the first word of any script.

---

## The Variant Differentiation Test

Before writing a single scene, define these three things for each variant:

1. **What does this audience already know?** (Don't explain what they know — assume it)
2. **What's the ONE thing this variant needs them to feel or understand?** (Not a list — one thing)
3. **What's the register?** (cinematic / conversational / technical)

**If two variants have the same answers to all three → they are not distinct → collapse them into one.**

Running this test upfront prevents the most common failure: writing three scripts that tell the same story three different ways, rather than three genuinely different stories about the same product.

---

## Variant Labelling Convention

Use these labels consistently across all projects so Finn knows the production approach without reading the script:

| Label | Audience | Style | VO Density |
|---|---|---|---|
| **A** | Technical or sophisticated | Cinematic — minimal VO, UI carries story | Sparse |
| **B** | General / accessible | Walkthrough — guided, second person | Medium |
| **C** | Developer / architect | Explainer — structured, covers architecture | Dense |

---

## Word Count Targets

Check these before calling any script done:

| Target Length | Narration Word Count |
|---|---|
| 60s | 110–130 words |
| 90s | 160–195 words |
| 2min | 220–260 words |
| 3min | 330–390 words |

At natural TTS pace: ~130 words/min. Count words in the **clean narration section only** (no stage directions).

---

## Interleaved Writing Technique

**The wrong way:**
Write A fully → Write B fully → Write C fully

By the time you write C, it has unconsciously borrowed A's metaphors and B's sentence structure. C ends up sounding like a compressed remix of the first two.

**The right way (interleaved):**
Write Scene 1 for A, B, C → Write Scene 2 for A, B, C → continue scene by scene

This forces explicit differentiation at each narrative beat. When you write Scene 2 for C, you've just written Scene 2 for A and B — so you're actively thinking "how is C different here?" rather than just continuing a flow.

---

## Common Failure Modes

### Drift
**What it is:** Writing C after A and B causes C to unconsciously borrow A's metaphors and B's structural patterns.  
**Fix:** Use interleaved writing. Never fully complete one variant before starting the others.

### Jargon Bleed
**What it is:** Technical terms written for C leak into B because they were written in the same session.  
**Fix:** Before writing, define a jargon whitelist per variant. Terms on C's whitelist should not appear in B. Terms on B's whitelist should not appear in A unless they're genuinely plain-language.

**Example:**
- A whitelist: (none — no jargon, let the UI speak)
- B whitelist: "agent", "automates", "dashboard"
- C whitelist: "MCP protocol", "orchestrator", "tool-call", "mesh routing"

### Length Creep
**What it is:** All variants drift toward the same word count because the writer fills to a comfortable length.  
**Fix:** Count words in the clean narration section after writing each scene. Stop when you hit the ceiling. Tighten, don't pad.

---

## Output Checklist — Before Handoff to Finn

Run this check on all variants together, not one at a time:

- [ ] Each variant has a **clean narration section** (narration only — no stage directions, no scene headers)
- [ ] Word counts checked against length targets (count them, don't estimate by feel)
- [ ] **No variant shares an opening line with another** (first sentence must be unique per variant)
- [ ] Jargon that appears in C does not appear in B
- [ ] Jargon that appears in B does not appear in A
- [ ] Screenshot/recording requirements section is complete and specific
- [ ] "Notes for Finn" section includes timing gotchas, transition notes, any unusual assembly requirements
- [ ] Differentiation test re-run on final drafts — confirm answers to all three questions are still distinct

---

## Handoff Format

Each script file must follow the standard format:

```markdown
# Video Script [A/B/C] — [Title]
**Version:** 1.0
**Target length:** X seconds
**Audience:** [who]
**Style:** [description]

## Scene-by-scene
### Scene N — [Title] (M:SS–M:SS)
**Screen:** [page/state]
**Action:** [interaction if any]
**Narration:** "[exact spoken words]"
**Music/mood:** [description]

## Full narration (clean read)
[narration only — this is the direct TTS input]

## Screenshot/recording requirements
[specific assets needed, with reuse notes]

## Notes for Finn
[timing, transitions, assembly gotchas]
```

All three script files are handed to Finn together. Finn does not start production until Nissan has approved all scripts.
