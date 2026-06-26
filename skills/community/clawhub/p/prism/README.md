# PRISM v2 🔮

**Parallel Review by Independent Specialist Models**

Multi-agent review protocol that eliminates confirmation bias through structured adversarial analysis. v2 adds **memory** — the system learns from its own review history.

## What It Does

- 🔒 Deploys 5+ specialist reviewers in parallel (Security, Performance, Simplicity, Integration, Devil's Advocate)
- 🧠 **Remembers** — searches for prior reviews on the same topic, tracks what was fixed
- 🎯 Surfaces disagreements as the most valuable signal
- 😈 Devil's Advocate reviews **blind** — no prior findings, guaranteed independence
- 📋 Requires evidence — every finding must cite a specific file, line, or command output
- 🔧 Findings include shell commands or file paths — actionable, not just advisory
- ⚡ Works with parallel subagents OR sequential single-agent review

## The Core Insights

> "Disagreements are MORE valuable than consensus."

When 4/5 reviewers agree and 1 dissents, pay attention to that dissent.

> "Findings without evidence are noise."

Every finding must cite a specific file. Assertions without citations are lowest priority.

> "A finding flagged 3 times tells you about governance, not about the code."

PRISM v2 tracks how many times a finding appears — repeat findings escalate automatically.

## What's New in v2

| Feature | v1 | v2 |
|---------|----|----|
| Prior review awareness | None — starts fresh every time | Searches for prior reviews, injects open findings |
| Devil's Advocate | Receives same context as others | **Structurally blind** to prior findings |
| Evidence requirement | Optional | **Mandatory** — cite files or it's deprioritized |
| Verdict scale | APPROVE / AWC / REJECT | + **NEEDS WORK** (fixable but not shippable) |
| Findings format | General observations | Must include specific fix (command or file path) |
| Synthesis | Flat list of findings | Evidence hierarchy (Tier 1/2/3) + Limitations section |
| History | No archive | Searchable archive in `analysis/prism/archive/<slug>/` |
| Governance | Manual tracking | `--governance` flag for Stuck Findings |
| Verification | Trust claims at face value | **Verification Auditor** role (Extended mode) |

## Install

### OpenClaw / Claude Code

```bash
# Clone to your skills directory
git clone https://github.com/jeremyknows/PRISM.git ~/.openclaw/skills/prism
```

### Other Agents (Cursor, Windsurf, etc.)

```bash
git clone https://github.com/jeremyknows/PRISM.git
# Reference SKILL.md from your agent's configuration
```

## Usage

Just say it:

```
"PRISM this API change"
"Budget PRISM on the auth flow"
"Full PRISM audit on the deployment pipeline"
```

| Mode | Agents | Cost (Sonnet) |
|------|--------|---------------|
| **Budget** | 3 (Security + Performance + Devil's Advocate) | ~$0.30-0.50 |
| **Standard** | 5 (+ Simplicity + Integration) | ~$0.50-1.00 |
| **Extended** | 7+ (+ Code Reviewers + Verification Auditor) | ~$1.50-2.50 |

### Options

- `--opus` — Use Opus model for all reviewers (2-3x cost, for critical decisions)
- `--haiku` — Use Haiku model (fast/cheap, for quick sanity checks)
- `--governance` — Surface Stuck Findings (issues flagged 3+ times without resolution)

## How It Works

```
1. You say "PRISM this"
2. Orchestrator derives topic slug (e.g., api-authentication-redesign)
3. Searches for prior PRISM reviews on that topic
4. Spawns reviewers in parallel:
   - Security, Performance, Simplicity, Integration get prior findings
   - Devil's Advocate reviews BLIND (no prior findings — by design)
5. Each reviewer reads files, cites evidence, proposes specific fixes
6. Orchestrator synthesizes: Tier 1 (cross-validated) → Tier 2 (cited) → Tier 3 (uncited)
7. Archives the synthesis for future reviews
```

**First run:** No prior findings exist. PRISM runs like v1 but with evidence requirements. No empty sections, no confusion.

**Subsequent runs:** Prior findings are injected. Reviewers verify what's fixed and hunt for what's new. The Devil's Advocate stays blind — their independence is the control group.

## Evidence Hierarchy

| Tier | Definition | Action |
|------|-----------|--------|
| **Tier 1** | 2+ reviewers found independently, citing different files | Act immediately |
| **Tier 2** | Single reviewer, specific file/line citation | High confidence |
| **Tier 3** | Single reviewer, no citation | Verify before acting |

## Verdict Scale

| Verdict | Meaning |
|---------|---------|
| **APPROVE** | Clean — no issues, prior issues resolved |
| **APPROVE WITH CONDITIONS** | New issues found, none critical |
| **NEEDS WORK** | Fixable but not shippable — prior criticals still open, or significant new issues |
| **REJECT** | Fundamental problems — requires rethink |

## Anti-Patterns

**Don't:**
- ❌ Let reviewers see each other's findings (groupthink)
- ❌ Give Devil's Advocate the Prior Findings Brief (breaks independence)
- ❌ Accept findings without file citations (noise)
- ❌ Skip synthesis (raw findings aren't actionable)
- ❌ Ask reviewers to "find everything" (overwhelms)

**Do:**
- ✅ Spawn reviewers in parallel (independent perspectives)
- ✅ Give each reviewer narrow focus (depth > breadth)
- ✅ Require citations in every finding
- ✅ Archive every synthesis
- ✅ Run two rounds for important decisions

## Optional: Search-Enhanced Context

If your environment has [qmd](https://github.com/tobilu/qmd) or similar search tools, reviewers can forage for their own context:

```bash
# Reviewers search for relevant context instead of being hand-fed files
qmd search "authentication rate limiting" -n 5
```

PRISM works without search tools — they just improve context precision and reduce token cost.

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| All reviewers find same issues | Roles not distinct enough | Sharpen role prompts |
| >100 issues found | Scope too broad | Narrow the review target |
| Vague findings | Missing evidence requirement | Enforce citation rules |
| DA has no concerns | Topic too simple or DA too soft | Re-run: "find something wrong" |
| Same finding appears 3+ times | Governance gap, not review gap | Enable `--governance` |

## Development

Validated through 10 PRISM reviews across 2 rounds (eating our own cooking). Key design decisions:

- **DA blindness** — Security + DA + Simplicity all independently flagged anchoring risk. Resolution: DA is structurally blind, not optionally blind.
- **Evidence requirement** — Pattern Fidelity reviewer analyzed 106 real PRISM reviews. Finding: run-05 (highest quality) cited specific files in every finding. Mediocre reviews were assertion-based.
- **"Just works" default** — UX reviewer walked the first-run journey. Finding: empty sections look broken. Resolution: conditional rendering, omit history sections when no prior reviews exist.

## Contributing

PRs welcome! Especially:

- New reviewer perspectives
- Example reviews from real usage
- Integration guides for other agents
- Evidence of v2 memory improving review quality over time

## License

MIT — See [LICENSE.txt](LICENSE.txt)

---

*"The specialists optimize. The Devil protects you from yourself. The archive remembers what you forgot."*
