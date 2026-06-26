# Mythos Skill — Examples

Showcase examples of the skill in action across its three execution modes. For deeper annotated transcripts and edge-case walkthroughs, see [`../references/examples.md`](../references/examples.md).

## Quick reference

```
/mythos <question>             # complexity-based auto-routing
/mythos trace <question>       # force trace mode (visible rounds)
/mythos deep <question>        # force agent mode (parallel subagents)
/mythos agent <question>       # alias for deep
/mythos quick <question>       # force silent mode (compact answer)
```

Keywords are case-insensitive. When multiple appear, the **last one wins**, and only the leading bare word in the slash-command argument is parsed.

---

## Example 1 — Silent mode (default)

**Question:**

> Should we cache user permissions in Redis or query Postgres each request?

**Routing:** complexity score 3 (multi-hop tradeoff + hidden assumptions). Default routes to Silent mode — the recurrent block runs in extended-thinking, the user sees only the Coda.

**Output shape:**

> Cache in Redis with a short TTL (60s) and an explicit invalidation hook on permission change. Querying Postgres each request is fine until ~500 RPS; beyond that the connection pool becomes the bottleneck. Trade-off: a 60s window of stale permissions versus DB load. If permission changes are rare and correlate with user actions, the invalidation hook keeps practical staleness near zero.
>
> *Lens path: Clarify → Deepen → Tradeoff-Map → Synthesize (4 rounds, converged).*

The single-line lens-path footnote is the auditability surface for Silent mode. It tells you which lenses ran without dumping the per-round chain.

---

## Example 2 — Trace mode

**Invocation:** `/mythos trace Should we adopt Conventional Commits?`

**Routing:** keyword forces Trace, regardless of complexity score.

**Output shape:** Prelude block + per-round visible reasoning with explicit insight chain + Answer. Use Trace when the audience is reviewers who need to verify each step (design-decision posts, RFC threads, teaching).

Cost: more tokens than Silent. Worth it only when auditability is the actual goal.

---

## Example 3 — Agent mode

**Question:**

> Evaluate three engine paths for our strategy game: in-house, Godot, Unity.

**Routing:** complexity score 5 (high-stakes + multi-driver + novel-domain). Default routes to Agent mode.

**What happens:** Four lenses — Clarify, Challenge, Tradeoff-Map, First-Principles — dispatched as **parallel subagents**, each exploring independently with no visibility into the others. A merge phase synthesizes their independent perspectives into one answer.

**Why parallel rather than sequential:** sequential dispatch would make each later lens read earlier lenses' outputs. By round three, the conversation has already committed to whichever path round one chose — and "independent perspective" becomes fiction. Parallel + a merge step preserves the latent-multiplicity property the mode is designed for.

**Cost note:** Agent mode is roughly 5× the token cost of Silent mode for the same question (each parallel subagent is a full forward pass, plus the merge). Use it only when the question has multiple genuinely-independent angles worth exploring in parallel.

---

## When to use which mode

| Mode | Use when |
|---|---|
| Direct (auto, complexity 1) | Lookup-shaped or trivial questions |
| Silent (default for 2–3) | Most thoughtful questions where you want the answer, not the work-showing |
| Trace (keyword) | You need to publish or review the reasoning step-by-step |
| Agent (auto for 4–5, or `deep`/`agent` keyword) | High-stakes decisions where multiple genuinely-independent angles need parallel exploration |

For the full theory of mode selection (complexity scoring, primary-driver detection, lens-budget allocation), see the SKILL.md walkthrough and `../references/lenses.md`.
