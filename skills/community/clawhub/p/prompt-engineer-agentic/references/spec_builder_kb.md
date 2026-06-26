# SPEC BUILDER KNOWLEDGE BASE
## How to Write Specifications That Translate Into High-Accuracy System Prompts

**Purpose:** This document is your operating manual. It tells you what makes a spec buildable, what gaps cause prompt engineers to guess (which degrades accuracy), and exactly what to include in every section so the prompt engineer can encode it cleanly. Follow this and the prompts built from your specs will be measurably better.

**How to use this:** Reference this document every time you build a spec. The checklists at the end of each section are your quality gates — don't ship a spec that fails them.

---

## PART 1: WHAT YOUR SPECS DO WELL (KEEP DOING THIS)

Before we fix anything, here's what you're already doing right. These are non-negotiable strengths — maintain them.

### 1.1 Strong Identity Definition
Your identity sections establish clear expertise domains, communication style, and relationship to the user. The iMovie spec's identity section — "Patient but efficient. Recommends the best approach for current skill level, not the most impressive approach possible. Develops capability, not dependence." — is exactly the kind of behavioral calibration that produces consistent outputs. Keep writing identities this way.

### 1.2 Explicit Scope with Both Inclusions and Exclusions
You naturally define what the tool DOES and what it DOESN'T do. This is the single highest-impact component in prompt engineering research. Your core mission sections are consistently strong.

### 1.3 Response Protocol Design
Your response modes (Task Execution, Script Translation, Troubleshooting, Capability Assessment) are well-structured and give the prompt engineer clear behavioral contracts to encode. The numbered steps within each mode are buildable.

### 1.4 Limitations Awareness
Including a limitations table with workarounds is excellent practice. This prevents the most frustrating failure mode — the tool confidently recommending something the platform can't do.

### 1.5 Design Principles That Drive Behavior
Your design principles section ("The viewer is the mission," "Simple and clean beats complex and distracting") gives the prompt engineer decision-making heuristics to encode. These are far more valuable than abstract values because they resolve real ambiguity the model will face.

---

## PART 2: THE CRITICAL GAPS (FIX THESE)

These are the structural gaps that force the prompt engineer to make assumptions. Every assumption is a potential accuracy failure. Closing these gaps will meaningfully improve the quality of every prompt built from your specs.

---

### GAP 1: No Verification Mechanism Specified

**The problem:** Your specs define what the tool should DO but never how it should CHECK its own work. Research shows verification mechanisms reduce hallucinations by 23-68%. For a tool giving step-by-step instructions, an unchecked hallucination means telling the user to click a button that doesn't exist or use a menu path that's wrong.

**What to include in every spec:**

```
### Verification Protocol

Claims requiring verification:
- [Category 1: e.g., interface element references]
- [Category 2: e.g., feature availability by version]
- [Category 3: e.g., recommended settings/values]

Verification behavior:
- [What the tool does before delivering these claims]

Uncertainty handling:
- [What happens when the tool isn't confident]
- [How it communicates uncertainty to the user]
- [Fallback behavior]
```

---

### GAP 2: No Confidence/Uncertainty Framework

**The problem:** Your specs never tell the tool how to handle situations where it's not sure. Without uncertainty handling, the tool either hallucinates confidently or hedges everything. Neither serves the user.

```
### Confidence Protocol

HIGH CONFIDENCE — Verified or repeatedly confirmed knowledge:
- Deliver directly without hedging

MODERATE CONFIDENCE — Likely correct but version-dependent or edge-case:
- Deliver with a brief qualifier

LOW CONFIDENCE — Uncertain, rarely encountered, or version-specific:
- State explicitly: "I'm not certain about this specific behavior."
- Provide best available guidance with clear fallback

OUTSIDE KNOWLEDGE — Don't know:
- Never guess. State the boundary.
- Direct to authoritative source with specific search terms.
```

---

### GAP 3: Knowledge Base vs. In-Prompt Encoding Not Differentiated

**The problem:** Your specs mix behavioral instructions and reference knowledge without distinguishing them. They have completely different optimal implementations:
- **Behavioral instructions** → system prompt
- **Reference knowledge** → knowledge base files attached to the project

```
### Prompt Content (Behavioral — goes in system prompt)
- Role definition
- Scope and boundaries
- Response protocols
- Verification mechanisms
- Skill calibration logic
- Design principles

### Knowledge Base Content (Reference — goes in attached files)
- Technical capability inventories
- Limitations tables with workarounds
- Settings references
- Platform version differences
- Keyboard shortcut references
```

**Rule of thumb:** If the content is a list of facts the tool looks up, it's knowledge base. If it shapes how the tool behaves, decides, or communicates, it's prompt.

---

### GAP 4: No Edge Case / Failure Mode Specification

**The problem:** Your specs handle the happy path well but don't define behavior for predictable failure scenarios.

```
### Edge Cases

IMPOSSIBLE REQUEST:
- [Specified behavior]

VAGUE PROBLEM REPORT:
- [Specified behavior — e.g., ask max 3 diagnostic questions]

CONFLICTING PRINCIPLES:
- [Specified hierarchy — which principle wins]

INTERFACE MISMATCH:
- [Specified behavior]

EXTERNAL TOOL REQUIRED BUT UNAVAILABLE:
- [Specified behavior]
```

---

### GAP 5: No Output Format Specification for Complex Deliverables

For every response mode that can produce long output, specify:

```
### Output Format — [Mode Name]

STRUCTURE:
1. [Section 1]
2. [Section 2]

LENGTH MANAGEMENT:
- If output exceeds [X], deliver in phases
- Always end each phase with: what's coming next, what the user should do before requesting the next phase

NAVIGATION AIDS:
- [Markers or flags to help user navigate long outputs]
```

---

### GAP 6: No Anti-Pattern Specification

```
### Anti-Patterns (Critical Avoidances)

NEVER:
- [Anti-pattern 1]
- [Anti-pattern 2]

REASONING: [One sentence per anti-pattern explaining why it's harmful]
```

---

### GAP 7: No Cross-Session Continuity Specification

```
### Continuity and Skill Tracking

ADVANCEMENT SIGNALS:
- [Signal 1]
- [Signal 2]

REGRESSION SIGNALS:
- [Signal 1]
- [Signal 2]

CONTINUITY BEHAVIOR:
- Reference previous work when relevant
- Don't re-explain demonstrated concepts
- When uncertain about current level, briefly check
```

---

### GAP 8: No Examples Specification

For each response mode, provide ONE concrete example showing ideal behavior:

```
### Example Interactions

[MODE NAME] EXAMPLE:
User: [message]
Ideal response: [Write exactly what you'd want the tool to say]
```

---

## PART 3: STRUCTURAL TEMPLATE FOR ALL FUTURE SPECS

```
# [TOOL NAME] — SYSTEM PROMPT BUILD REQUEST

## TASK
[One paragraph: what needs to be built and what the deliverable is]

## CONTEXT
[Operational context: where this fits, who uses it, what drives need]

## DELIVERABLE
[Exact deliverable format]

---

## TOOL SPECIFICATION

### 1. Identity [REQUIRED]
- Expertise domain and depth
- Communication style
- Relationship to user
- Behavioral disposition

### 2. Core Mission [REQUIRED]
- 3-5 specific functions (what the tool DOES)
- 2-3 explicit exclusions (what it does NOT do)

### 3. Technical Knowledge — Primary Domain [REQUIRED]
- Clearly labeled: PROMPT CONTENT vs. KNOWLEDGE BASE CONTENT

### 4. Technical Knowledge — Supporting Domains [IF APPLICABLE]
- Same labeling convention

### 5. Response Protocols [REQUIRED]
- Distinct modes with triggering conditions
- Numbered steps per mode
- Output format specs for complex deliverables

### 6. Verification Protocol [REQUIRED]
- What claims require verification
- Verification behavior
- Uncertainty handling per confidence level

### 7. Confidence Framework [REQUIRED]
- High / Moderate / Low / Outside Knowledge behaviors
- Domain-specific examples for each level

### 8. Limitations and Constraints [RECOMMENDED]
- Known tool/platform limitations
- Workarounds per limitation
- Label as KNOWLEDGE BASE CONTENT

### 9. Skill Calibration [IF APPLICABLE]
- Level definitions with behavioral differences
- Advancement and regression signals
- Cross-session continuity behavior

### 10. Edge Cases [REQUIRED]
- 5-10 predictable failure scenarios
- Specified behavior for each

### 11. Anti-Patterns [REQUIRED]
- Critical behaviors to avoid
- One-sentence reasoning for each

### 12. Design Principles [RECOMMENDED]
- Decision-making heuristics
- Priority hierarchy when principles conflict

### 13. User Context [REQUIRED]
- Who the user is
- What they're trying to accomplish
- Their skill level and constraints

### 14. Example Interactions [RECOMMENDED]
- One example per response mode
- Written as ideal conversations

### 15. Platform/Version Notes [IF APPLICABLE]
- Default platform
- Version-specific considerations
```

---

## PART 4: THE SPEC-TO-PROMPT TRANSLATION PIPELINE

| Your Spec Content | Where It Goes |
|---|---|
| Identity, mission, scope | System prompt — Foundation Layer |
| Response protocols, instructions | System prompt — Structure Layer |
| Verification, constraints, edge cases | System prompt — Execution Layer |
| Technical knowledge inventories | Knowledge base files |
| Limitations tables | Knowledge base files |
| Settings references | Knowledge base files |
| Example interactions | System prompt — Structure Layer |
| Design principles | System prompt — Foundation Layer |

### Token Budget

| Component | Optimal Size |
|---|---|
| Core system prompt | 1,500–2,500 tokens |
| Knowledge base files | Up to 80K tokens total |
| Examples in prompt | 300–500 tokens per example |
| Total active context | <3,000 tokens for reasoning |

### What Makes the Prompt Engineer's Job Easy vs. Hard

**EASY:**
- Specific behavioral instructions with clear triggering conditions
- Concrete examples showing ideal behavior
- Explicit priority hierarchies
- Clear labeling of behavioral vs. reference knowledge
- Edge cases with specified behavior

**HARD:**
- Vague instructions like "be helpful" or "use good judgment"
- Massive inventories without indication of what's critical
- Missing failure mode specs
- No examples
- Ambiguous priority between competing design principles

---

## PART 5: QUALITY CHECKLIST

Run every spec through this before handoff.

### Foundation Checks
- [ ] Identity defines expertise domain, communication style, and disposition
- [ ] Mission has 3-5 specific DO functions and 2-3 explicit DON'T exclusions
- [ ] User context is specific (not generic "anyone")
- [ ] Design principles include a priority hierarchy for conflicts

### Structure Checks
- [ ] Response modes have clear triggering conditions
- [ ] Each response mode has numbered steps
- [ ] Complex output modes have format specs (length, structure, phasing)
- [ ] At least one example interaction per response mode is included

### Execution Checks
- [ ] Verification protocol specifies what claims need checking
- [ ] Confidence framework has graduated behaviors per level
- [ ] 5+ edge cases are listed with specified behaviors
- [ ] Anti-patterns are listed with reasoning
- [ ] Cross-session continuity is addressed (if the tool tracks user state)

### Architecture Checks
- [ ] Behavioral content is clearly separated from reference knowledge
- [ ] Reference knowledge sections are labeled "KNOWLEDGE BASE CONTENT"
- [ ] No single behavioral section exceeds ~500 tokens
- [ ] The spec doesn't require the prompt engineer to make domain-specific judgment calls

---

## SUMMARY: THE 8 RULES FOR SPEC BUILDERS

1. **Separate behavior from knowledge.** Behavioral instructions go in the prompt. Reference knowledge goes in files. Label them.
2. **Specify verification.** Every spec must define what the tool checks before delivering answers and what happens when it's not sure.
3. **Include a confidence framework.** The tool needs graduated behaviors for different certainty levels. Define them per domain.
4. **Define edge cases.** 5-10 predictable failure scenarios with specified behavior.
5. **Include anti-patterns.** Tell the tool what NOT to do, with reasoning.
6. **Provide examples.** One per response mode minimum.
7. **Spec output formats for complex deliverables.** Define structure, length management, and navigation.
8. **Respect the token budget.** Behavioral specs should be encodable in ~2,500 tokens. Everything else is knowledge base material.

---

*End of Spec Builder Knowledge Base — v1.0*
