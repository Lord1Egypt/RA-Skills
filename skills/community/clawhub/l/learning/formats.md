# Format Ladder — Choosing and Building Each Rung

The ladder (SKILL.md Rule 6): plain prose → concrete example → analogy → table or diagram → worked problem. Enter at the learner's confirmed rung (`entry_format` in config), move one rung on failure, never repeat a failed rung louder.

## Entry Rung

- Novices: concrete example first, definition second — a definition without an instance has nothing to bind to.
- Advanced learners: prose and formal statements directly; forcing them through scaffolds costs attention (expertise reversal, Rule 7).
- Programmers on executable topics: `code-first` — a runnable snippet is a concrete example and a worked problem at once.

## Building Examples

- Two positives plus one near-miss non-example define a concept's boundary; positives alone let the learner overgeneralize.
- Vary surface features across examples, hold the deep structure constant — varied examples cost more effort during practice and transfer better (variability effect, Paas and van Merrienboer).
- The second example must not share the first's surface domain: two banking examples teach "banking", not the concept.
- Before revealing an example's outcome, ask the learner to predict it — generated content outlasts presented content (generation effect, Slamecka and Graf).

## Building Analogies

- Map explicitly — "X is like Y in that [mapping]" — and state where the analogy breaks in the same turn (SKILL.md Traps).
- One analogy per concept. A second analogy for the same concept forces the learner to reconcile two source domains instead of learning one target.
- Retire the analogy once the learner uses the target vocabulary unprompted; an analogy that lingers becomes the model (`misconceptions.md`).

## Tables and Diagrams

- Use when the content is relational — comparisons, flows, hierarchies. Words plus structure beat words alone (dual coding, Paivio); a two-dimension table beats prose that lists the pairs.
- The diagram replaces the prose; do not present the same content in both simultaneously (redundancy effect, Sweller) — duplication adds load, not clarity.
- In a text channel, tables and ASCII/mermaid sketches are the visual rung; offer them, don't describe what a diagram would show.

## Worked Problems and Fading

- Novice sequence: full worked example → completion problem (learner supplies the last steps) → full problem (backward fading, Renkl).
- Pair every worked example with a self-explanation prompt — "why does step 2 work?" — self-explainers learn more from identical examples (Chi).
- Remove scaffolds on evidence: two clean completions → full problems (Rule 7). Scaffolds kept "for safety" cap the advanced learner.

## Abstract Topics

- Concreteness fading: concrete instance → stripped representation → formal notation (Goldstone and Son). Run the stages in order; skipping the middle stage is where formalism-first teaching loses people.
- Introducing notation before any instance is the most common origin of the "has vocabulary, fails the transfer" intermediate profile (SKILL.md Diagnostic Probes).

## Choosing Under Preference

- `entry_format` and confirmed format preferences pick where you START on the ladder, not where you may go — a failed rung still forces a move (SKILL.md Preference Memory ceiling).
- When two rungs both fit, prefer the one that lets the learner produce something checkable this exchange.
