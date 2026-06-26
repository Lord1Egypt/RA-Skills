---
name: Naming
slug: naming
version: 1.0.0
homepage: https://clawic.com/skills/naming
description: "Create, test, and choose names for products, features, APIs, files, and systems with constraint-first briefs and collision checks."
changelog: "Initial release with a naming brief, scoring rubric, surface patterns, and safer rename guidance."
metadata: {"clawdbot":{"emoji":"🏷️","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/naming/"]}}
---

## When to Use

Naming work appears when the user needs a name that other people must understand, remember, say, search, or implement correctly.

Use this for products, brands, features, APIs, packages, files, folders, internal codenames, taxonomy cleanups, and risky renames where bad naming creates confusion, rework, or avoidable collisions.

## Architecture

Memory lives in `~/naming/`. If `~/naming/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/naming/
├── memory.md      # Stable naming taste, banned patterns, durable constraints
├── briefs.md      # Reusable naming briefs by asset or project
├── winners.md     # Approved names, backups, and rationale
├── collisions.md  # Rejected candidates and collision notes
└── archive/       # Retired names, old briefs, and obsolete language
```

## Quick Reference

Load the smallest file that removes the current naming uncertainty.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Constraint-first brief | `brief-template.md` |
| Candidate scoring rubric | `scorecard.md` |
| Naming patterns by surface | `surface-patterns.md` |
| Safe rename protocol | `rename-playbook.md` |

## Output Contract

When this skill is active, produce a naming deliverable that is decision-ready, not just a brainstorm dump.

| Output | Purpose |
|--------|---------|
| Brief summary | Lock the object, audience, constraints, and success criteria |
| Option families | Show structured variation instead of random isolated names |
| Shortlist with scores | Explain why finalists survive the filters |
| Recommendation | Pick one winner plus two backups |
| Risk notes | Flag collisions, ambiguity, rollout risk, or missing verification |

If the user only asks for ideas, still keep the internal structure. Raw lists without rationale usually create another round of confusion instead of a decision.

## Naming Lanes

First identify which lane the work belongs to. Good names are surface-specific.

| Lane | Optimize for | Common failure | File |
|------|--------------|----------------|------|
| Product or brand | Memorability, distinction, room to grow | Sounds clever but says nothing | `brief-template.md` |
| Feature or workflow | Instant comprehension in UI and docs | Marketing language hides the job | `surface-patterns.md` |
| API, endpoint, schema, method | Consistency, predictability, low ambiguity | Mixed verbs, nouns, and tense | `surface-patterns.md` |
| Package, repo, command, file, folder | Scan speed, exactness, maintainability | Decorative naming hurts retrieval | `surface-patterns.md` |
| Internal codename | Fast alignment and low collision | Leaks into public language accidentally | `rename-playbook.md` |

## Core Rules

### 1. Start with the RALLY brief before generating names
- Use `brief-template.md` to lock the asset, audience, lexical guardrails, and why the name matters.
- RALLY stands for **Role, Audience, Limits, Lexicon, Yardstick**.
- If the brief is vague, do not pretend ideation quality will save it. Ambiguous briefs create attractive but unusable names.

### 2. Separate utility naming from brand naming
- Utility surfaces such as features, APIs, files, and commands should bias toward clarity and predictability.
- Brand surfaces can trade a little exactness for recall, story, and distinctiveness, but still need to pass comprehension fast enough for the context.
- Never judge a feature name with the same rubric used for a company name. The lane defines the winning tradeoff.

### 3. Generate option families, not one flat list
- Create at least three families with different angles: descriptive, metaphorical, compound, outcome-first, or system-consistent.
- Keep siblings internally coherent so the user can compare strategies, not just individual words.
- A strong family often reveals the right direction even when none of the exact first-pass candidates survive.

### 4. Run every finalist through the CLASH scorecard
- Use `scorecard.md` before recommending a winner.
- CLASH stands for **Clarity, Load, Adjacency, Search collision, Harm**.
- A name is not done because it sounds good. It must also survive spelling, pronunciation, ambiguity, namespace overlap, and negative connotations.

### 5. Match the surrounding system before optimizing the single name
- Check product architecture, menu hierarchy, endpoint family, file layout, or taxonomy before choosing the local label.
- A slightly less exciting name is better if it makes the whole system easier to scan and predict.
- Prefer consistency across sibling names over isolated cleverness.

### 6. Recommend one winner, two backups, and the deciding reason
- Do not leave the user with ten equally weighted options unless they explicitly asked for open exploration.
- State why the winner wins in this context: better comprehension, lower collision risk, stronger recall, better family fit, or safer rollout.
- If legal, trademark, domain, or live namespace verification still matters, say that explicitly instead of implying clearance.

### 7. Treat renames as migrations, not word swaps
- A rename can break routes, docs, API clients, analytics, onboarding, and mental models.
- Use `rename-playbook.md` whenever the job touches live systems or published language.
- Always map what changes, what aliases are needed, and what must remain backward-compatible during transition.

### 8. Learn durable naming taste, not one-off opinions
- Store recurring constraints in local memory: words the user avoids, tone preferences, naming style, and family patterns that keep winning.
- Do not store every brainstorm. Store only reusable signals that improve future naming quality.
- If the user rejects multiple options for the same reason, promote that reason into a durable rule.

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Brainstorming before defining the object | Different people optimize for different jobs | Lock the brief first |
| Picking the cleverest name in the room | Clever often decays into explanation debt | Score for clarity and retrieval first |
| Mixing external and internal names | Teams start leaking placeholder language | Decide what is public, internal, and transitional |
| Renaming one node without the system | Adjacent labels become inconsistent and confusing | Audit sibling names before final choice |
| Using invented spelling to look distinctive | Search, pronunciation, and trust all get worse | Prefer real words unless the lane truly justifies invention |
| Confusing category fit with legal clearance | Similarity risk stays hidden | Mark live trademark or namespace verification as still required |
| Leaving the decision at "here are some ideas" | The user still has no recommendation | Pick a winner and defend it |

## Security & Privacy

**Data that stays local:**
- Naming briefs, durable constraints, approved names, and rejected patterns in `~/naming/`

**This skill does NOT:**
- Claim trademark, domain, or regulatory clearance without explicit live verification
- Make undeclared network requests
- Register names, buy domains, or mutate production systems by itself
- Rename live assets without an explicit migration plan

If the user wants live checks for search results, domains, trademarks, package registries, or repository availability, say what is being checked before using external services.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `branding` — define positioning and voice before committing to a public-facing name
- `product` — shape product framing and packaging around the chosen name
- `product-manager` — align feature and workflow names with user language and roadmap context
- `strategy` — evaluate category, portfolio, and market tradeoffs behind naming decisions
- `api` — keep API naming, endpoint language, and auth terminology consistent

## Feedback

- If useful: `clawhub star naming`
- Stay updated: `clawhub sync`
