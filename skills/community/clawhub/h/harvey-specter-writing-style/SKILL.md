---
name: harvey-specter-writing-style
description: Rewrite or draft text in a Harvey Specter (Suits)-inspired writing style: confident, concise, sharp-witted, leverage-focused, and decisive. Use when the user asks to "write like Harvey Specter," "make it more confident," "add swagger," "make it punchier," or needs a hard-nosed negotiation/email/script that stays professional.
metadata: {"openclaw":{"homepage":"https://screenrant.com/suits-iconic-harvey-spectre-quotes/"}}
---

# Harvey Specter (Suits)-inspired writing style

## Goal

Transform input text into a voice that feels:

- Decisive and controlled (no hedging, no apology loops)
- Short and punchy (tight sentences, strong verbs)
- Strategically assertive (frames, terms, leverage, boundaries)
- Witty when appropriate (one "zinger", not a stand-up routine)

## Non-negotiables (guardrails)

- Do **not** copy dialogue/quotes verbatim from *Suits*.
- Keep it **professional by default**: confident without harassment, threats, or crude insults.
- If the user asks for intimidation, convert it into **firm boundaries** and **consequences** (policy, timeline, escalation), not personal attacks.

## Anti-AI-tells guardrails (from Wikipedia)

When rewriting/drafting, avoid common LLM-sounding patterns listed in
`Wikipedia:Signs of AI writing` by:

- Avoid promotional/puffery phrasing; stay specific and practical instead of "crucial/vital/pivotal."
- Avoid vague attribution (no "experts say" / "it is believed") unless the user provided the source.
- Avoid outline-like wrap-ups ("in conclusion / overall") that restate the thesis instead of moving forward.
- Avoid template-y negation patterns like "Not X, but Y" or repeated "not ... but ..." structures.
- Avoid excessive em-dashes; prefer commas/periods/parentheses.
- Avoid AI-vocabulary stacking: do not pile "Additionally/Furthermore/Moreover/Notably" transitions in the same passage.
- Use normal copulas freely ("is/are"); do not over-replace with "serves as/stands as/marks/represents."
- Limit rigid parallel lists; if you use bullets, keep them short and don't add bold inline headers for each item.

## Workflow (use every time)

1. **Clarify the objective** (in your head): persuade, refuse, negotiate, motivate, or close.
2. **Pick the stance**:
   - **Close**: "Here is what is happening next."
   - **Refuse**: "No. Here is why. Here is the alternative."
   - **Negotiate**: "Here are the terms. Choose A or B."
   - **Correct**: "That is not the problem. This is."
3. **Compress**:
   - Prefer 1–3 short paragraphs or 5–9 lines total.
   - Use short sentences. Cut filler, qualifiers, throat-clearing.
4. **Add leverage** (without melodrama):
   - Name constraints: time, risk, budget, authority, policy.
   - Use options: "If X, then Y. If not, then Z."
5. **Add one signature device** (pick one):
   - A crisp rhetorical question.
   - A clean pivot line: "Real constraint: Y." (no "Not X, but Y" template)
   - A metaphor/idiom (one only).
6. **Land the ending**:
   - A single next step with a deadline or decision point.

## Language rules

### Do

- Use **active voice** and **strong verbs**: "deliver", "decide", "ship", "sign".
- Use **boundaries**: "I'm not available for ...", "That doesn't work."
- Use **terms**: "By Friday", "in writing", "single owner", "one approval path".
- Use **calm dominance**: fewer exclamation points, fewer adjectives.

### Avoid

- Hedging: "maybe", "kind of", "I think", "just", "hopefully".
- Rambling context dumps. Don't explain; **frame**.
- Over-sass. One zinger max; skip it in serious contexts (legal, HR, medical).

Additional formatting avoids:

- Avoid starting multiple consecutive sentences with "Additionally/Furthermore/Moreover/Notably."
- Avoid emoji and avoid bolding most words.

## Output formats

### 1) Rewrite (same meaning, new voice)

Return:

1. Harvey-style rewrite (just the rewritten text)
2. One-line rationale (max 1 sentence) describing the main change (tone, structure, leverage)

### 2) Draft from scratch (user gives scenario)

Return:

1. Draft
2. Optional variants (only if requested): "more aggressive" / "more diplomatic"

## Templates

### Boundary / refusal

- Opening: "No." or "That doesn't work."
- Reason: one sentence (fact, constraint).
- Alternative: one clear option.
- Close: "Confirm by <time>."

### Negotiation / terms

- Frame: "Here is what I can do."
- Terms: 2–4 bullets max.
- Choice: "Pick A or B."
- Close: "Decide by <time>."

### Correction / accountability

- Frame: "Explaining isn't solving."
- Ask: "What are you doing to fix it by <time>?"
- Close: "Send the plan. Then execute."

## Examples

See [examples.md](examples.md) for ready-to-copy rewrites and original drafts.
