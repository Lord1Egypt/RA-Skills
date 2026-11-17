# Evidence for promotional blurb

## Sources

### [User-supplied product spec — internal]
- Date: 2026-05
- Tier: 1 (primary, user-supplied)
- Claims it supports:
  - "The product has three named features: voice profiling, AI-pattern cleanup, and a claim review pass."
  - "It runs as a skill inside an agent (Codex, Claude Code, OpenCode). It is not a standalone CLI."
  - "It does not claim a productivity gain number. The user has not measured one."
- Limitations: internal spec; no external benchmark. Treat the three-feature list as the only product claim we can defend.

### [Independent review, Oumi HallOumi blog, 2024]
- URL: https://oumi.ai/blog/introducing-halloumi-a-state-of-the
- Date: 2024-09
- Tier: 2 (reputable secondary; vendor blog)
- Claims it supports:
  - "HallOumi-style fact-check passes can reduce unsupported claims in a draft by surfacing them as a review step."
  - The review is a step, not an elimination of unsupported claims.
- Limitations: vendor blog; describes the inspiration for the fact-check pass, not a benchmark of the user's product.

### [Wikipedia: Signs of AI writing]
- URL: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Date: accessed 2026-06
- Tier: 2 (community-maintained reference)
- Claims it supports (as canonical AI tells to remove from the rewrite):
  - "Pivotal", "groundbreaking", "cutting-edge", "seamless", "testament", "ecosystem" are in the canonical cluster of AI vocabulary.
  - "Studies show" / "experts say" with no named source is in the canonical fuzzy-attribution cluster.
  - "Not just X, but Y" is the canonical negative-parallelism pattern.
- Limitations: a diagnostic list, not a benchmark.

## Cross-source analysis

- Source 1 (user spec) is the only product-defining evidence. It does not support the 300% claim, the "experts say" claim, or any productivity number.
- No source in this evidence file supports "300% productivity increase". Status: `wrong` (no source exists) — the claim is invented.
- No source in this evidence file supports "experts say this is the future of work". Status: `wrong` (vague attribution) — cut.
- Source 3 (Wikipedia) confirms that the draft's vocabulary belongs to the canonical AI cluster. Status: `style_only` for the lexical hits (they are not factual claims, but they are diagnostic markers and should be removed).

## Status of every claim in the draft

| Claim | Type | Source | Status | Fix |
| --- | --- | --- | --- | --- |
| 300% productivity increase | number, attribution | None | `wrong` | Remove |
| "Experts say this is the future of work" | attribution | None | `wrong` (vague attribution) | Remove |
| "Studies show..." (vague) | attribution | None | `wrong` (vague attribution) | Remove |
| "Pivotal solution" / "groundbreaking" / "cutting-edge" / "seamless" | promotional, AI vocabulary | None needed (Wikipedia confirms the cluster) | `style_only` | Rewrite in plain verbs |
| "Boasts" | AI vocabulary | None | `style_only` | Replace with a plain verb |
| "Showcasing" / "stands as a testament" | AI vocabulary | None | `style_only` | Cut |
| "Not just X, but Y" | negative parallelism | None needed | `style_only` | Rewrite as a complete thought |
| "In order to achieve optimal results" | filler | None | `style_only` | Cut to "to" |
| "Great question!" | chatbot residue | None | `style_only` | Remove |
| "Ecosystem" | AI vocabulary | None | `style_only` | Replace with a specific noun |
| The product has voice profiling, AI-pattern cleanup, and a claim review | descriptive, product | Source 1 (user spec) | `supported` | Keep |
| The product runs as a skill inside an agent | descriptive, product | Source 1 | `supported` | Keep |
| The product is not a standalone CLI | descriptive, product | Source 1 | `supported` | Keep |
