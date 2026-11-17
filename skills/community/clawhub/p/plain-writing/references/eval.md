# Writing completion test

Run this test before linting and after the last edit. The linter does not
replace it.

## Blocking checks

Revise the draft if any answer is yes:

1. Did it keep an unsupported source prediction, causal claim, generalization,
   or synthesis as though it were a protected fact?
2. Did it lose or alter a concrete fact, attribution, negative fact,
   uncertainty, requirement, recommendation, permission, decision, commitment,
   requested action, risk, mitigation, condition, or consequence?
3. Did it invent an actor, fact, motive, link, order, conclusion, consensus,
   channel, timing, or mechanism, or state an implication as fact?
4. Is the response a critique of the source instead of finished prose?
5. Does the outline still follow an AI template that the content does not
   need?
6. Do generic headings, short sections, expanded bullets, repeated recaps, or
   forced symmetry make the piece longer or flatter?
7. Does it contain a banned pattern from `ai-patterns.md` without a concrete
   contextual reason?
8. Did the rewrite replace the source voice with generic professional polish?
9. Did the ending add a lesson, metaphor, or flourish that the source did not
   support?
10. Did a proposal to explore, add, or test something become a claim that it
    does not exist or has already started?
11. Did strict mode turn ordinary prose into bullets only to meet its sentence
    limit?
12. Did strict mode turn a proposal, option, hypothesis, or unapproved idea
    into a command?
13. Did an edit increase headings or list items without clearer navigation, a
    parallel scan task, safety, or a procedural need?
14. Does any sentence only announce, classify, or interpret evidence that can
    speak directly? Delete it and retest. Restore only necessary attribution,
    uncertainty, or inference.
15. Did scope or certainty grow during the edit: some to all, one to each, may
    to will, appears to confirmed, or association to cause?

## Comparative checks

- Each remaining heading helps a reader find a distinct part.
- Each list is parallel or easier to scan than prose.
- Sentence and paragraph shapes vary because the ideas vary.
- The opening starts with useful content.
- The ending stops at the last supported result, decision, or action.
- Repeated content appears once unless repetition serves a real purpose.
- Concrete traces, measurements, examples, and effects replace abstract
  evidence summaries when the detail helps the reader.
- The whole piece sounds like its intended author, not a report generator.
- Each protected item maps to a final passage in an in-order source sweep.
- Retained warnings have an internal reason; zero warnings is not a target.

Pass only when the draft clears every blocking check and the comparative review
finds no change that would make the reader's work easier.
