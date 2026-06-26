# Elicitation flow — UX rules with rationale

These are not style preferences. Each rule is borrowed from a validated methodology; if you break the rule you reintroduce a failure mode the methodology was designed to prevent.

## Rule 1: Grade before criteria (EvalGen, UIST 2024)

**The rule**: ask for examples before asking for criteria.

**The failure mode it prevents**: *criteria drift* — Shankar et al. found that users cannot reliably define evaluation criteria upfront. When asked "what makes a good memory?", they produce vague or incomplete answers. But when shown concrete examples, they can grade "keep this / discard this" reliably, and the criteria fall out of the pattern.

**How to apply**: Turn 1 of Understanding asks for 1–2 "keep" and 1–2 "discard" examples. Do not ask for a definition of "good memory" anywhere in the conversation. Let the examples carry that weight.

## Rule 2: Cap decisions at 7, prefer 3 (AdaTest, ACL 2022)

**The rule**: never show more than 7 items to choose between; prefer 3.

**The failure mode it prevents**: *choice overload*. Ribeiro et al. generated hundreds of test candidates but only surfaced the top 3–7 to the user. More items degraded selection quality and dragged out sessions.

**How to apply**:
- When showing archetype mix candidates: show 3, ranked by relevance to the user's description
- When asking about dimensions: show 4 families first, then 2 dimensions per chosen family — never all 8 at once
- When offering template patterns: 4 canonical ones total, but only surface the 1–2 closest matches to the user's description

## Rule 3: Ranking always visible (AdaTest)

**The rule**: when you show candidates, show why they're ranked in that order.

**Example done wrong**:
> Here are 3 scenarios: A, B, C. Which do you want?

**Example done right**:
> Here are 3 scenarios ranked by fit to what you described:
> 1. Pattern A — matches your "long-running companion" description directly
> 2. Pattern B — similar archetypes but assumes higher noise than you described
> 3. Pattern C — closest to the evolution you described but different archetype mix
>
> Pick 1, or tell me what to adjust in the top match.

**Why this matters**: opaque ranking forces the user to reverse-engineer your reasoning. Transparent ranking lets them push back on the part you got wrong — "you assumed higher noise, but my case is lower" — which is the fast path to a good scenario.

## Rule 4: Iterate every 5–8 interactions (EvalGen)

**The rule**: pause every ~5–8 turns and surface a pattern summary.

**The failure mode**: conversations wander. Users forget earlier turns, contradict themselves, or add constraints you've already captured.

**How to apply**: after Stage 1 Turn 3, restate what you've learned in 3 bullets. After Stage 4, restate the scenario + winner + recommendation. Don't let >5 turns elapse without a summary checkpoint.

## Rule 5: Organization optional (AdaTest)

**The rule**: don't force a taxonomy on the user upfront.

**The failure mode**: when users are pushed to categorize their use case before they've explored it, they pattern-match to whatever's nearest and stop thinking. AdaTest explicitly allowed users to add structure *after* exploring examples, not before.

**How to apply**: the 4-family taxonomy appears in Turn 3, *after* the user has given examples in Turns 1–2. Never open the conversation with "which family matters most?" — you'll get a guess, not a considered answer.

## Rule 6: Let silence be silence

**The rule**: if the user's description doesn't mention a dimension, don't assume it doesn't matter. But also don't assume it does.

**Example failure**: user describes a coding agent, doesn't mention noise. Skill defaults to "noise = 10%" (low). This is *probably* correct but you should flag the inference, not hide it.

**How to apply**: when you make an inference from silence, state it. *"You didn't mention noise — I'm defaulting to 10% based on typical coding-agent setups. Bump that if your agent sees a lot of irrelevant content."*

## Rule 7: Refine is a first-class action (AdaTest inner/outer loop)

**The rule**: after Judgment, always offer a refinement loop. Make it trivial to re-run with a tweaked scenario.

**The failure mode**: users get a result, feel like they "should" accept it, and move on even when the scenario was slightly wrong. AdaTest's inner-loop UX explicitly prevented this by making iteration the default next action, not a special request.

**How to apply**: end every Judgment with *"Want to refine the scenario and re-run?"* and a 1–3 item list of likely tweaks. If the user says yes, edit the scenario.yaml directly and re-invoke the CLI — don't redo Stage 1 from scratch.

## What success looks like

A typical session hits these milestones:
- **Turn 1–2**: user describes use case + gives examples
- **Turn 3**: skill surfaces the 4 families, user picks 2–3
- **Turn 4**: skill shows 1–3 pattern candidates ranked by fit
- **Turn 5 (Ideation)**: skill writes scenario.yaml and asks for confirmation
- **Rollout**: CLI runs (1–5 min)
- **Turn 6 (Judgment)**: skill delivers the 3-section interpretation
- **Turn 7 (optional refinement)**: user requests a tweak, skill re-runs

Total: 5–7 turns of conversation, one CLI run, one optional refinement. Budget: ~30 minutes.

If the conversation is taking longer than this, check which rule you broke — usually Rule 2 (you showed too many candidates) or Rule 4 (you skipped a summary checkpoint).
