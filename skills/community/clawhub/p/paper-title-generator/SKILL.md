---
name: paper-title-generator
description: "Generate optimized paper titles for different academic venues and styles. Activated when Chopin submits a paper draft and needs title suggestions, or when struggling to name a paper. Input: full paper draft or abstract plus key contributions. Output: 3-5 title options tailored to specific target venues (IEEE Transactions, IFAC, ACC, CDC, Automatica, etc.) with explanations of why each works for its venue. Use when Chopin asks: help me name this paper, suggest titles for a venue, or shares a draft seeking title feedback."
---

# Paper Title Generator

Generate compelling, venue-appropriate paper titles from draft content.

## Input Needed

Provide one or more of:
- Full paper draft (preferred)
- Abstract
- Key contributions list
- Method name / algorithm name
- Target venue(s)

## Output

### Per Venue: 3-5 Title Options

Each title comes with:
- **Rationale:** Why this title fits the venue's style
- **Tone tags:** [Formal] [Technical] [Catchy] [Method-focused] [Application-focused]
- **Word count:** Short / Medium / Long

### Title Styles Explained

- **Descriptive:** States the method/problem directly (e.g., "Event-Triggered Formation Control for Multi-UAV Systems")
- **Innovative:** Emphasizes novelty (e.g., "Breaking the Communication Barrier: Adaptive Event-Triggered Formation")
- **Question-based:** Engages reader curiosity (e.g., "How Can Multi-Agent Systems Reduce Communication Without Losing Control?")
- **Compound:** Method + Application (e.g., "Consensus-Based Event Triggering for Formation Reconfiguration in UAV Swarms")

## Venue-Specific Guidelines

### IEEE Transactions (TAC, TIE, TRO, TCST)
- Formal, technical, method-first
- Avoid: catchy phrases, questions, colons
- Length: 10-15 words
- Example: "Event-Triggered Consensus Control for Linear Multi-Agent Systems"

### Automatica
- Mathematical rigor emphasized
- Balance theory and application
- Clean, precise language
- Length: 12-18 words

### IFAC (CDC, ACC, ECC)
- Method + contribution clearly stated
- Technical but accessible
- Length: 12-16 words

### ICRA / IROS (Robotics conferences)
- Application-relevant, engaging
- Can be slightly more creative
- Often include robot/vehicle type
- Length: 8-12 words

### Nature / Science
- Broad impact, accessible to non-specialists
- Catchy but not hyperbolic
- Avoid jargon
- Length: 10-15 words

## Workflow

1. **Analyze input:** Extract problem, method, contribution, novelty
2. **Identify keywords:** Technical terms that must appear
3. **Map to venue:** Apply venue-specific constraints
4. **Generate titles:** 3-5 per venue, varied styles
5. **Rank & explain:** Explain why each fits

## Title Red Flags

- Too vague: "A Study on Formation Control"
- Too long: >20 words
- Missing contribution: "Formation Control Using Event-Triggered Communication"
- Too generic: "A New Approach to..."
- Jargon-heavy for broad venues

See `references/title-styles.md` for detailed venue analysis and 20+ example titles.
