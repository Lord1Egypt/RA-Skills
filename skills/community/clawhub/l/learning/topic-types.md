# Matching Method to Material

The session loop (SKILL.md) is constant; the emphasis shifts with the material. Misclassifying the material wastes the technique: mnemonics on conceptual material, discussion on verbatim material, reading on procedural material.

| Material | Examples | What carries the load | What fails |
|---|---|---|---|
| Factual / arbitrary mappings | Vocabulary, terminology, flags, syntax tables | Spaced retrieval from day one; keyword mnemonics for stubborn mappings (Atkinson) | Trying to derive it — arbitrary facts have nothing to derive from |
| Conceptual | How DNS works, supply and demand, evolution | Misconception surfacing, contrast cases, concreteness fading, self-explanation | Definition drilling — produces recitation without transfer |
| Procedural | Coding tasks, math procedures, tool workflows | Worked example → completion → full problem (`formats.md`); practice in the real tool | Watching or reading only — understanding a procedure is not executing it |
| Verbatim | Formulas, quotes, scripts, keybindings | Exact-recall checks on tight spacing | Paraphrase checks — verbatim material needs verbatim testing |
| Discrimination pairs | affect/effect, TCP/UDP, two similar APIs | Deliberate interleaving of the confusable pair (`retention.md`) | Teaching each separately in its own clean block |
| Problem-solving domains | Math, physics, debugging | Interleaved mixed problem sets — choosing the method is the skill | Blocked practice by problem type: feels smooth, fails delayed tests (SKILL.md Session Structure) |

## Notes per Type

- **Languages**: mixed material — vocabulary is factual (SRS handoff, `retention.md`), grammar is procedural plus conceptual, and listening/speaking need production practice this channel can only rehearse; say so rather than simulating immersion.
- **Code**: the learner's editor is the worked-problem surface — set tasks to run for real; predicted output vs actual output is the cheapest generation check available.
- **Math**: notation is verbatim, methods are procedural, "why it works" is conceptual — a struggling math learner usually lacks exactly one of the three; probe which before re-teaching all three.
- **History and essay domains**: conceptual with factual scaffolding — causal-chain explain-backs ("why did X lead to Y") beat date drilling, except where dates are the deliverable (then treat them as factual material).
- **Physical and motor skills**: teach the theory, route the practice to the real activity or a coach; text feedback closes no motor loop (SKILL.md Traps).

## Mixed Topics

Most real topics blend rows: decompose before choosing method. "Learn Kubernetes" = terminology (factual) + architecture (conceptual) + kubectl workflows (procedural). Run each strand with its own method and its own checks; a single blended approach defaults to conceptual-style explanation and quietly starves the other two.
