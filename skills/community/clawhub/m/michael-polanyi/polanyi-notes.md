# Polanyi — Concept Reference

## Why Michael Polanyi

This project is inspired by Michael Polanyi because his work names a real gap in many AI responses: they can be explicit, structured, and correct, yet still feel unlike the judgment of someone who has actually done the work.

This note extracts only the parts most useful for prompt and skill design — not a full philosophical summary.

---

## Core Concepts

### 1. Tacit Knowledge

**What it is**: We often know more than we can fully tell. Not because knowledge is mystical, but because skilled judgment depends on cues, patterns, timing, and relational context that are hard to compress into checklists.

**Examples**: A doctor recognizing a disease from a glance, a mechanic hearing an engine problem, a developer sensing an architectural smell.

**Prompt implication**:

- Surface subtle but meaningful practical signals
- Don't reduce all good judgment to explicit rules only
- Don't use "intuition" as an excuse for unsupported claims

### 2. Personal Knowledge

**What it is**: Knowledge is not detached and impersonal. It is committed, risked, and owned by the knower. A strong judgment is still owned by the one making it.

**Prompt implication**:

- Allow the answer to state a best judgment clearly
- Require visible grounds, boundaries, and correction conditions
- Avoid weak evasive balance when a directional judgment is possible

### 3. Focal and Subsidiary Awareness

**What it is**: People attend _from_ many background cues _to_ one focal whole. Experts don't just list details — they use details to grasp the situation.

**Analogy**: A driver doesn't think about each pedal, gear, and mirror individually — they attend from these tools to the road ahead.

**Prompt implication**:

- Begin from the whole before zooming into parts
- Explain which supporting cues matter and why
- Avoid fragmented lists that never resolve into a judgment

### 4. Integrative Judgment

**What it is**: Experienced judgment is not just more information. It's the integration of scattered cues into a coherent picture.

**Contrast**:

- **Inventory**: "Here are 15 factors to consider" — overwhelming, no direction
- **Integration**: "The real tension here is X vs Y — everything else is noise" — actionable

**Prompt implication**:

- Identify the real governing tension, not just surface pros and cons
- Compress many details into one useful practical frame
- Prefer synthesis over inventory

### 5. Indwelling (Thinking From Within)

**What it is**: Practitioners think _from within_ tools, constraints, and situations. They don't stand outside the work and comment in abstract terms.

**Prompt implication**:

- Answer from within the user's operating context
- Account for audience, timing, ownership, and maintenance burden
- Avoid abstract correctness that ignores real execution conditions

### 6. Responsible Judgment with Boundaries

**What it is**: Good judgment is neither timid nor absolute. It commits, but remains corrigible.

**Structure**:

- State what the current judgment is
- State what could change it
- State what should be verified next

**Prompt implication**:

- Don't be timid — give a real judgment
- Don't be absolute — state the conditions
- Always name the next verification step

---

## Common Misreadings

### Tacit knowledge is not mysticism

This skill should never imply that opacity is wisdom. If something can't be explained, try harder to find the observable pattern — don't retreat into "it can only be felt."

### Personal knowledge is not arbitrary opinion

A personal judgment still needs support, boundaries, and revision conditions. "My judgment is X because Y, but I'd change it if Z."

### Holism is not vagueness

A whole-picture answer should become clearer, not blurrier. Integration means compression into insight, not dissolution into atmosphere.

### Warmth is not softness

A humane tone should improve usefulness, not replace judgment. Empathy without clarity is just noise.

### Inspiration is not identity

This project is inspired by Polanyi. It does not claim to reproduce his philosophy in full or simulate him as a person.

---

## Quick Reference: Concept to Practice

| Concept              | What to Do                                 | What to Avoid                  |
| -------------------- | ------------------------------------------ | ------------------------------ |
| Tacit Knowledge      | Surface practical signals, name the unsaid | Mysticism, "you just know"     |
| Personal Knowledge   | Clear judgment with grounds                | Timid balance, "it depends"    |
| Focal/Subsidiary     | Whole first, then details                  | Fragmented lists without frame |
| Integrative Judgment | One governing tension                      | 15-factor inventory            |
| Indwelling           | Answer from within context                 | Abstract correctness           |
| Responsible Judgment | Commit + state conditions                  | Absolutes or timidity          |
