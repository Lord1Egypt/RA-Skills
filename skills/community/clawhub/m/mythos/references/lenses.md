# Lens Library

Each lens is a specific angle of analysis applied during one recurrent round. Select 2-5 lenses based on the problem type. The order matters — later lenses build on (and challenge) earlier ones.

## Core Lenses (apply to most problems)

### Clarify
**Question:** What exactly is being asked? Where is the ambiguity?
**Method:** Define key terms precisely. Identify what's explicit vs implicit. Separate the question from its framing. A surprising number of hard problems become easy once you define terms precisely.
**Best for:** Round 1 of any problem.

### Deepen
**Question:** What's one level deeper? What are the root causes or first principles?
**Method:** Ask "why" repeatedly. Trace surface phenomena to underlying mechanisms. Identify the generating function, not just its outputs.
**Best for:** Round 2, after the problem is clear.

### Challenge
**Question:** What assumptions am I making? What if the opposite were true?
**Method:** List every premise you're relying on. Try to break each one. Consider: what would make this entire line of reasoning wrong? What's the strongest counterargument?
**Best for:** Round 3, when an answer is forming but untested.

### Expand
**Question:** What alternatives exist? How would someone with different expertise approach this?
**Method:** Generate at least 2 genuinely different answers (not variations of the same idea). Consider: domain expert, contrarian, beginner's mind, adjacent field. What would Munger's inversion say? What would Taleb's fragility lens reveal?
**Best for:** Round 4, before converging.

### Synthesize
**Question:** How do all perspectives fit together? What's the integrated answer?
**Method:** Weave insights from all previous rounds. Resolve tensions (don't paper over them). Identify: what's the core insight that explains the most? What pattern emerges?
**Best for:** Final round before Coda.

## Specialized Lenses

### System-Think
**Question:** What system is this embedded in? What are the feedback loops?
**Method:** Map inputs → processes → outputs → feedback. Identify stocks, flows, delays, and nonlinearities. Where are the leverage points?
**Best for:** Organizational problems, platform design, ecosystem questions.

### Edge-Hunt
**Question:** What happens at the boundaries? What breaks?
**Method:** Stress-test every condition. Find the inputs that produce undefined/wrong/dangerous outputs. Consider: empty, maximum, negative, concurrent, stale, malicious.
**Best for:** Technical design, API design, safety-critical decisions.

### Tradeoff-Map
**Question:** What am I trading against what? What's the Pareto frontier?
**Method:** For each option, list what you gain and what you sacrifice. Identify false dichotomies (options that seem opposed but aren't). Find the dominated options (strictly worse on all dimensions).
**Best for:** Architecture decisions, resource allocation, strategy.

### Invert
**Question:** What would guarantee failure? What's the anti-goal?
**Method:** Instead of asking "how to succeed," ask "how to guarantee catastrophic failure." Then avoid those things. This is Munger's inversion — often more powerful than forward reasoning.
**Best for:** Risk assessment, investment decisions, career choices.

### Scar-Tissue
**Question:** What does painful experience say about this?
**Method:** Recall specific past failures in similar situations. What was the root cause? What was the false assumption? How does that pattern manifest here? This is not generic "lessons learned" — it's specific scar tissue from real failures.
**Best for:** Decisions where the cost of being wrong is high.

### First-Principles
**Question:** What do I know with certainty? What can I derive from that?
**Method:** Strip away all analogy, convention, and "best practice." Build up from what's provably true. What would you do if you were inventing this from scratch with no legacy constraints?
**Best for:** Novel problems, disruptive innovation, when "best practice" feels wrong.

### Steelman
**Question:** What's the strongest version of the position I disagree with?
**Method:** Build the best possible argument for the opposing view. Make it stronger than your opponents would. Then engage with that argument honestly. If you can't steelman it, you don't understand it well enough to refute it.
**Best for:** Controversial topics, strategy debates, when you're too confident.

## Lens Selection Guide

### By Problem Type

> **These are alternates, not the canonical sequence.** SKILL.md's standard rotation (Clarify → Deepen → Challenge → Expand → Synthesize) is the default. Use a problem-type sequence below ONLY when the standard rotation clearly mismatches the problem (e.g., debate problems benefit from leading with Steelman; investment problems from leading with Invert). When you swap, document the rationale in the Prelude's Lens-sequence line.

| Problem Type | Recommended Lens Sequence |
|---|---|
| Technical design | Clarify → Deepen → Edge-Hunt → Challenge → Synthesize |
| Strategic decision | Clarify → Invert → Expand → Tradeoff-Map → Synthesize |
| Debugging / root cause | Clarify → Deepen → System-Think → Edge-Hunt → Synthesize |
| Creative / innovation | Clarify → First-Principles → Expand → Challenge → Synthesize |
| Debate / disagreement | Clarify → Steelman → Challenge → Expand → Synthesize |
| Investment / risk | Clarify → Invert → Scar-Tissue → Challenge → Synthesize |
| Quick but thorough | Clarify → Deepen → Challenge → Synthesize |

### Adaptive Budget: Complexity Driver → Lens Boost

Not all lenses deserve equal rounds. Diagnose the primary complexity driver in Prelude, then allocate extra rounds to the lens that directly addresses that driver.

| Primary Driver | Lenses boosted to ×2 | Rationale |
|---------------|---------------------|-----------|
| **Ambiguity** — key terms vague or undefined | Clarify | Ambiguity is the bottleneck; spend 2 rounds defining before moving on |
| **Hidden assumptions** — question rests on unexamined premises | Challenge, Steelman | Need one round to surface assumptions, one to stress-test the strongest one |
| **Multi-hop** — answer requires chaining multiple reasoning steps | Deepen, System-Think | Need one round to trace the chain, one to verify each link |
| **Trade-offs** — core difficulty is weighing competing values | Tradeoff-Map, Expand | Need one round to map the frontier, one to explore alternatives beyond it |
| **Novel domain** — problem space is unfamiliar or unprecedented | First-Principles, Expand | Need one round to strip to fundamentals, one to explore what fundamentals enable |
| **System dynamics** — embedded in complex system with feedback loops | System-Think, Edge-Hunt | Need one round to map the system, one to find where it breaks |

**Budget rules:**
- Synthesize always gets 1 round (integration is a single act, not an iterative process)
- A lens boosted to ×2 runs twice CONSECUTIVELY before moving to the next lens in sequence
- Within a lens's 2nd round: find a new angle, stress-test the 1st round's conclusion, or go one level further — do NOT rephrase the 1st round
- If the 1st round under a lens already produced status = stable (converged), skip the 2nd round
- Total visible rounds: typically 4-8 (depends on driver count and budget allocation)
