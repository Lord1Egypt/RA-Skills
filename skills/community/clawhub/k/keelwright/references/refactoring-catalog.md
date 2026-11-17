# Refactoring catalog — name the smell, then apply one technique

This is the disciplined side of the anti-erosion gate (`writing-code.md`). Mechanical tools
(jscpd, lizard, scc) tell you *that* code is degrading; this file tells you *what to call it*
and *how to fix it by name*. Naming a smell before fixing it is cheaper and safer than
re-inventing a fix each time.

**Vocabulary source (industry-standard, not copyrightable terminology):** the smell and
technique names come from Martin Fowler, *Refactoring* (1999, 2nd ed. 2018, with Beck, Roberts,
Opdyke); design-pattern names from Gamma/Helm/Johnson/Vlissides ("Gang of Four", 1994). We use
the established *names* (facts/terminology, freely usable) — the descriptions below are our own
wording, not copied text. Credited in `provenance.md`.

Three moves, always in this order: **detect → name → fix (one at a time)**.

---

## 1. Smell catalog — name it before you touch it

When something "feels wrong," stop and match it to a named smell instead of patching blindly.

| Smell | Signal | Usual fix (see §2) |
|---|---|---|
| **Long Method** | function > ~20 lines / does several things | Extract Method |
| **Large Class** | class holds too many responsibilities | Extract Class / Extract Subclass |
| **Long Parameter List** | > 3 params | Introduce Parameter Object / Preserve Whole Object |
| **Duplicated Code** | same logic in 2+ places (jscpd flags it) | Extract Method / Pull Up Method |
| **Feature Envy** | a method uses another object's data more than its own | Move Method |
| **Data Clumps** | same group of fields/args travels together | Extract Class / Parameter Object |
| **Primitive Obsession** | primitives instead of small types (stringly-typed) | Replace Primitive with Object / enum |
| **Switch Statements** | repeated switch/if on a type code | Replace Conditional with Polymorphism |
| **Shotgun Surgery** | one change forces edits in many files | Move Method/Field to consolidate |
| **Divergent Change** | one class changes for many unrelated reasons | Extract Class along the axes of change |
| **Message Chains** | `a.b().c().d()` | Hide Delegate |
| **Speculative Generality** | abstraction with only one caller / "for the future" | Inline / Collapse Hierarchy (YAGNI) |
| **Comments explaining what** | comment compensates for unclear code | Extract Method + Rename (comment the *why* only) |
| **Dead Code** | unreachable / unused | Delete it (git remembers) |

Cross-links: Duplicated Code is what jscpd measures; Long Method / high nesting is what lizard's
CCN measures. The mechanical gate and this catalog describe the same problems in two languages.

---

## 2. Technique catalog — one technique per iteration, no drive-by edits

Apply **exactly one** named transformation at a time. The commit should show that transformation
and nothing else — this is what keeps loop diffs small and reviewable (and counters erosion).

| Technique | What it does | Post-step (mandatory) |
|---|---|---|
| **Extract Method/Function** | pull a block into a named function | call-site sweep + typecheck |
| **Inline Method/Variable** | remove needless indirection | typecheck |
| **Rename** | make intent obvious (kills "comment-what") | update all references |
| **Extract Class** | split a class doing 2+ jobs | move tests with it |
| **Move Method/Field** | put behavior next to the data it uses (fixes Feature Envy) | typecheck |
| **Introduce Parameter Object** | group a long/clumped param list | update all callers |
| **Replace Conditional with Polymorphism** | kill repeated type-switches | keep behavior identical |
| **Replace Primitive with Object** | give a concept a type | migrate usages |
| **Collapse Hierarchy / Inline Class** | undo speculative generality | verify no external callers |

**Rule:** run tests + typecheck after each single technique. Refactoring changes structure,
not behavior — if a test result changes, you didn't refactor, you rewrote. Revert and retry.

---

## 3. Pattern-justify — a design pattern must earn its place

Before introducing a design pattern (Strategy, Factory, Observer, Adapter, …), answer all three.
If any answer is weak, use the simpler alternative.

1. **Which current smell does it resolve?** Name it from §1. "It's cleaner" is not a smell.
2. **How many real callers/variants exist right now?** Count actual, not hypothetical. One
   variant → you don't need the pattern yet (Speculative Generality).
3. **Is there a simpler option?** A function, a map, or a plain conditional often beats a pattern.

This is YAGNI applied to architecture: the wrong abstraction is more expensive than none.

---

## 4. Pink Flag procedure — "feels wrong" is a signal, not noise

When code feels off during an iteration:

1. **Stop** — don't write more code on top of the smell.
2. **Name it** — match §1. If nothing matches, it may be an architecture-layer issue (a
   different concern) — note it and continue; don't force a label.
3. **Decide by tier:**
   - High (SRP break, duplication, security-adjacent) → fix **now**, in this iteration.
   - Medium/Low → log in `todo` as tech debt, keep moving (don't stall trivial work).
4. **Fix with one named technique** (§2), tests green, then continue.

This is the human-judgment complement to the machine anti-erosion gate: the tools catch what's
measurable, the Pink Flag catches what's felt. Both feed the same "fix before proceeding" rule.
