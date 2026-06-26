# Narrative Focus

**[English](README.md)** | [中文](README.zh-CN.md)

> Narrative weight misalignment is the most insidious structural problem in technical writing. It's not "poorly written" — it's "wrongly weighted." Familiar but superficial implementation details steal the spotlight from the architectural mechanisms that actually determine behavior. The reader's mental model gets anchored to the wrong position, and subsequent learning keeps circling back to reconstruct what should have been clear from the start.

An AgentSkill for detecting and fixing **Narrative Weight Misalignment** in technical tutorials and interview prep articles. Compatible with OpenClaw, CodeBuddy, and any AI coding agent.

## The Problem

Technical tutorials have a pervasive, almost universally unaddressed problem: **the narrative weight of concepts doesn't match their actual importance.**

An article on the React event system devotes an entire chapter to "Event Delegation" as one of its "Three Core Mechanisms" — but event delegation is just the signal delivery pipe. The actual core, Fiber-tree traversal, gets compressed into a few lines in a flow chart. The reader walks away thinking "event delegation" is the key concept, then gets confused when debugging `stopPropagation()` behavior in production.

This is not an isolated case. We tested 8 cross-domain articles (Kubernetes, PostgreSQL, Transformer, Rust, TLS, MySQL, Linux CFS, Git) and found **narrative weight misalignment in every single one**, with a misalignment rate of 75.8%. The universality of this problem is beyond doubt.

## Core Idea: Narrative Focus Is a Precondition

Most technical articles don't suffer from insufficient content — they suffer from confused weight distribution.

A misweighted article lets readers recite concepts but prevents them from building causal understanding. Their time goes to structural confusion — "why does this concept get its own section?" — rather than pursuing genuinely meaningful deeper questions.

Conversely, **when narrative weight is correct, it far more efficiently triggers the reader's positive chain of inquiry and learning.** Readers naturally generate the next question along the correct causal chain — questions that can be filled by other articles, documentation, or practice, or by asking the agent for specifics. No single article needs to exhaust all content.

**Getting readers to the main battlefield of knowledge faster, instead of tripping over poorly designed thresholds, is a higher-priority design goal than content completeness in technical writing.**

Narrative focus is a precondition for content quality. Calibrate weight first, then pursue depth.

## How It Works

### Substitution Test (the core judgment rule)

For any technical detail, ask: **If the proposition conveyed by this detail were replaced with an alternative, would the user's observable behavior change?**

- **Yes** → Architectural (determines system behavior) → deserves high narrative weight
- **No, only the delivery method changes** → Transport (pipe to get signals to the architecture) → low narrative weight
- **Behavior unchanged, only configuration differs** → Configurable (switch/option on existing mechanism) → medium narrative weight

**Critical: Proposition identification before substitution.** The same technical detail can convey different propositions depending on context. You must identify what proposition the detail is actually conveying in the article before applying the substitution test — do not substitute the literal term/implementation, substitute the proposition.

For example, "JSX is `React.createElement()` syntax sugar" — if the article is actually asserting "JSX has no independent runtime semantics," replacing this proposition would fundamentally change the reader's understanding of React → Architectural. But if the article is merely saying "JSX compiles to the specific function `createElement`," swapping it for `jsx()` doesn't affect reader behavior → Transport. The correct judgment depends on what the article is actually asserting.

**Proposition granularity.** The same detail can be read at different granularities (e.g., "positional encoding provides location info" vs "sine/cosine formulas implement position encoding"). The correct granularity depends on what the article actually elaborates. See `references/proposition-granularity-guide.md` for the decision flowchart and worked examples.

## Scope

| In scope | Out of scope |
|----------|-------------|
| Technical tutorials, deep-dive explainers | API reference docs |
| Interview prep articles | Opinion pieces, news/changelog |
| Framework comparison articles | Non-technical content |

This skill answers one question: **"Does the narrative weight of each concept match its actual role?"** It does not check for missing content, theme boundaries, or genre consistency.

### Two Modes

| Mode | When | Purpose |
|------|------|---------|
| **Pre-processing** | During research/collection phase | Label collected details with role tags to prevent misalignment before writing |
| **Post-processing** | After a draft is complete | Detect misalignment in existing articles and surgically fix it |

### Post-processing Safeguards

Post-processing includes two safeguard steps after correction:

1. **Second-pass detection** — re-run the detection workflow on the corrected article to confirm all misalignments are resolved
2. **Authoritative verification** — check modified sections against authoritative sources (official docs, team blogs, MDN) to ensure weight migration did not introduce technical semantic errors. Only **technical facts** are verified against authorities; **narrative framing** is not (official docs serve a different purpose than mental-model-oriented articles)

## Installation

### OpenClaw / CodeBuddy (native AgentSkill)

This skill uses the AgentSkill-compatible `SKILL.md` format and works natively with OpenClaw and CodeBuddy:

**OpenClaw** — install from ClawHub or copy to your skills directory:
```bash
# Via ClawHub (recommended)
openclaw skill install narrative-focus

# Or manually
cp -r narrative-focus/ ~/.openclaw/skills/
```

**CodeBuddy** — copy to your skills directory:
```bash
cp -r narrative-focus/ ~/.codebuddy/skills/
```

### Other AI Coding Agents (Claude Code, Cursor, Windsurf, etc.)

Load `SKILL.md` as context, then load the appropriate reference file (`references/pre-processing.md` or `references/post-processing.md`) based on which mode you need. The substitution test and role labels are defined in SKILL.md; the detailed SOPs are in the reference files.

For example, with Claude Code:
```
# Add to CLAUDE.md or instruct directly:
Read narrative-focus/SKILL.md and follow its workflow for post-processing detection on this article.
```

## Usage

### Pre-processing (collection phase)

Tell your agent something like:
- "按叙述重心规范收集" (Collect with narrative focus rules)
- "角色标注" (Role labeling)
- "Label these technical details by role using the substitution test"

The agent will identify the proposition conveyed by each detail, apply the substitution test, and tag it as Architectural / Transport / Configurable.

### Post-processing (review & fix)

Tell your agent something like:
- "检测叙述重心错位" (Detect narrative weight misalignment)
- "审稿重心" (Review narrative focus)
- "Check this article for narrative weight misalignment"

The agent will scan the article, identify misalignments, fix them — upgrading architectural concepts and downgrading transport/configurable ones — then verify modified sections against authoritative sources to ensure no technical errors were introduced.

## Examples

| Example | What it shows |
|---------|--------------|
| [`react-event-system/`](examples/react-event-system/) | Classic misalignment: event delegation over-highlighted, Fiber traversal obscured. Full Step 1–5 detection + correction + second-pass. Includes **proposition granularity analysis**. |
| [`docker-orchestration/`](examples/docker-orchestration/) | Title-content mismatch: build details crowd out orchestration. Multiple Transport/Configurable items over-highlighted. |
| [`v8-gc/`](examples/v8-gc/) | **Borderline case**: most weights correct, 2 borderline items. Shows how the skill handles "almost right" articles and its own scope boundary. |

## File Structure

```
narrative-focus/
├── SKILL.md                              # Core concepts + mode routing
├── README.md                             # English
├── README.zh-CN.md                       # 中文版
├── LICENSE
├── references/
│   ├── pre-processing.md                 # SOP: collection & labeling phase
│   ├── post-processing.md                # SOP: detection, correction & verification
│   └── proposition-granularity-guide.md  # How to read propositions at the right depth
├── examples/
│   ├── react-event-system/               # Classic misalignment + granularity analysis
│   │   ├── before.md
│   │   └── after.md
│   ├── docker-orchestration/             # Title-content mismatch
│   │   ├── before.md
│   │   └── after.md
│   └── v8-gc/                            # Borderline case + scope boundary
│       └── before.md
└── experiments/                           # 3-round validation experiments
    ├── README.md                          #   Experiment overview
    ├── final-evaluation.md                #   Final comprehensive evaluation
    ├── round1-cross-domain/               #   R1: 5 synthetic articles, cross-domain robustness
    │   ├── articles/                      #     K8s, PostgreSQL, Transformer, Rust, TLS
    │   ├── detection-results/             #     Skill detection reports (5)
    │   └── summary.md
    ├── round2-controlled/                 #   R2: 3 real articles, Skill vs no-Skill control
    │   ├── articles/                      #     MySQL, Linux CFS, Git
    │   ├── no-skill-control-results/      #     No-Skill control (same model, no Skill input) (3)
    │   ├── skill-detection-results/       #     Skill detection (same model + Skill input) (3)
    │   └── summary.md
    └── round3-correction/                 #   R3: correction pipeline verification
        ├── corrected-articles/            #     Post-correction articles (2)
        ├── correction-reports/            #     Correction + verification reports (2)
        ├── re-evaluation/                 #     No-Skill control re-evaluation (2)
        └── summary.md
```

## License

MIT
