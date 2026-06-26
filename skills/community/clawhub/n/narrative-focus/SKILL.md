---
name: narrative-focus
description: |
  Narrative Focus — detect and fix "narrative weight misalignment" in technical tutorials and interview prep articles.
  Trigger when users ask to review technical articles for concept weight misalignment, fix narrative focus,
  or label technical details by role during research/collection to prevent misalignment.
  Also triggers on: "检测叙述重心", "叙述重心错位", "概念权重", "角色标注", "按叙述重心规范收集",
  "审稿重心", "narrative focus", "narrative weight", "concept weight", "review narrative".
---

# 叙述重心规范 / Narrative Focus

## Purpose

Prevent **narrative weight misalignment** in technical tutorials and interview prep articles — where a technical detail's narrative prominence doesn't match its actual role in the reader's mental model. Typical symptom: a transport-layer detail gets treated as a core architectural concept because it has a catchy or familiar name, causing readers to anchor their mental model on the wrong concept.

**Target article types**: Technical tutorials, deep-dive explainers, interview preparation articles, framework comparison articles — any technical content where concepts have clear causal hierarchies (architectural mechanisms vs transport details) and the reader is building a mental model.

**Not applicable**: API reference docs, opinion pieces, news/changelog, non-technical content.

This skill uses the AgentSkill-compatible SKILL.md format and works natively with OpenClaw and CodeBuddy. For other AI coding agents (Claude Code, Cursor, etc.), load SKILL.md and the appropriate reference file as context.

## Core Concepts

### Substitution Test (shared judgment rule)

The sole method for determining a detail's role: **If the proposition conveyed by this detail were replaced with an alternative, would the user's observable behavior change?**

- **Yes** → Architectural (mechanism that determines system behavior)
- **No, only the delivery method changes** → Transport (pipe that gets signals/data to the architectural mechanism)
- **Behavior unchanged, only choice/configuration differs** → Configurable (switch/option on an existing mechanism)

**Critical: Proposition identification before substitution.** The same technical detail can convey different propositions depending on context. You must identify **what proposition the detail is actually conveying in this article** before applying the substitution test — do not substitute the literal term/implementation, substitute the proposition.

Example:
- "JSX is `React.createElement()` syntax sugar" — the **proposition** is "JSX has no independent runtime semantics, it's just JS function calls." Substituting this proposition (e.g., with "JSX is a template with its own directive system") would fundamentally change user behavior → Architectural.
- If the same sentence were read as the proposition "JSX compiles to the specific function `createElement`" — substituting this (e.g., with `jsx()`) would not change user behavior → Transport.
- The correct reading depends on what the article is **actually asserting**, not what term appears in the sentence.

**Proposition granularity.** The same detail can be read at different granularities — e.g., "positional encoding provides location info" (conceptual) vs "sine/cosine formulas implement position encoding" (mathematical). The correct granularity depends on **what the article actually elaborates**. If the article spends a full section on the math, the proposition is at the math level. If it only mentions the math in passing, the proposition is at the conceptual level. See `references/proposition-granularity-guide.md` for detailed guidance and examples.

### Three-Layer Role Labels

| Label | Definition | Narrative Weight |
|-------|-----------|-----------------|
| Architectural | Mechanism that determines system behavior | High — core section, independent elaboration |
| Transport | Pipe that gets signals/data to the architectural mechanism | Low — one paragraph, labeled as means |
| Configurable | Switch/option on an existing mechanism | Medium — mention as needed, downgraded to supplement |

## Two Modes

### Mode 1: Pre-processing (collection phase)

Use when the user is doing deep research / knowledge collection and wants to label collected details by role to prevent misalignment.

**Entry recognition**: User mentions "按叙述重心规范收集", "角色标注", "前处理", "collect with narrative focus rules", "role labeling", etc.

**Workflow**: Load `references/pre-processing.md` and follow its SOP.

### Mode 2: Post-processing (detection + correction)

Use when the user wants to detect and fix narrative weight misalignment in a completed article/document.

**Entry recognition**: User mentions "检测叙述重心", "叙述重心错位", "审稿重心", "后处理", "detect narrative focus", "narrative weight misalignment", etc.

**Workflow**: Load `references/post-processing.md` and follow its SOP.

## Notes

- Both modes share the substitution test and three-layer role labels, but have completely different workflows
- Pre-processing aims to "label collected items to prevent misalignment later"; post-processing aims to "detect misalignment in existing articles and surgically fix it"
- Post-processing correction only does local weight migration — it does not rewrite the entire article. It downgrades transport concepts and upgrades architectural concepts without altering correct facts
- Post-processing includes an **authoritative verification** step after correction: modified sections are checked against authoritative sources (official docs, team blogs, MDN) to ensure weight migration did not introduce technical semantic errors. If errors are found, they are reported to the user rather than auto-corrected
