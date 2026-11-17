---
name: plain-writing
description: Draft, rewrite, edit, or audit prose to reduce AI slop, verbosity, jargon, clichés, unsupported claims, robotic structure, and formatting excess while preserving meaning and voice. Use for technical, workplace, long-form, or creative writing. Supports strict, technical, and optional natural modes.
---

# Plain Writing

Write for the reader. Prefer clear structure and direct language. Protect
supported meaning, not the source's clutter.

## Set the contract

Identify the operation, audience, purpose, genre, language mode, and required
terms. For an edit, separate the source into two groups.

Protect:

- facts, names, values, examples, dates, quotations, and sources
- attributed findings, hypotheses, and interpretations
- conditions, warnings, limits, exceptions, their consequences, and open
  questions
- uncertainty and negative facts, including missing tests or safeguards
- requirements, recommendations, permissions, decisions, commitments, actions,
  risks, and mitigations
- useful voice signals: vocabulary, cadence, bluntness, formality, humor,
  honest uncertainty, and deliberate roughness

Question, narrow, or cut:

- unsupported promotion, causation, prediction, generalization, and certainty
- rhetorical synthesis or interpretation with no named source or evidence
- repetition, framing, throat-clearing, recap, and decorative structure

“The fix will help” lacks support without evidence. Remove it or match the
source's certainty. A proposal to add something does not prove its absence.

Keep protected clauses as anchors until a paraphrase preserves their actor,
scope, negation, certainty, attribution, and force. Keep repeated content once.

Do not invent substance, relationships, sequence, or consensus. Do not merge
separate evidence into a new conclusion or add a channel, timing, or mechanism.
Ask for an essential missing fact when possible. Otherwise, stay within the
source.

When inputs conflict, use this order:

1. Truth, safety, and protected text.
2. The current task.
3. Supported source content and explicit uncertainty.
4. Unsupported source interpretation.
5. Style.

Return finished prose for a draft or edit, not a critique, template, or report.
For an audit, name observable problems and the smallest useful fixes. Do not
guess who wrote the text.

## Choose the controls

Choose one language mode. Default to `technical`:

- `strict`: Procedures, safety text, runbooks, UI text, errors, and exact
  instructions. Use sentences of 20 words or fewer. Do not use contractions
  or semicolons. Use commands only for confirmed steps and instructions.
  Keep proposals, options, and unapproved ideas non-imperative. Meet the
  sentence limit with prose, not extra bullets.
- `technical`: Technical, product, business, and workplace prose. Treat 25
  words as a review signal. Permit contractions and sentence variety when
  they preserve a natural voice.
- `natural`: Essays, thought pieces, creative copy, and loose long-form prose.
  Use only on explicit request. Review sentences over 40 words. Permit
  purposeful fragments, passive voice, semicolons, phrasal verbs, metaphor,
  digressions, and uneven cadence.

All modes must remove AI-shaped wording, rhythm, formatting, and whole-piece
structure. Mode changes syntax constraints only. It does not authorize
compression or reinterpretation of protected content.

Before drafting, editing, or auditing prose, read:

- `references/ai-patterns.md`
- `references/eval.md`

Preserve exact templates and regulated structure when the task requires them.
Do not change modes to make lint easier.

## Write

1. Decide what each passage must do. Name relevant actors, actions, conditions,
   and results.
2. Use one term for one thing. Keep necessary technical terms.
3. Prefer familiar words, clear subjects, direct verbs, and one main statement
   per sentence.
4. Put a condition before its action.
5. Number commands in a linear procedure. State a branch condition once and
   indent its actions.
6. Cut filler, repetition, genre restatements, empty transitions, stale images,
   jargon, canned contrasts, rhetorical setups, dramatic fragments, and hollow
   endings.
7. Replace strong claims with facts, measures, attributed conclusions, or
   explicit uncertainty.
8. Keep facts, interpretations, recommendations, and decisions distinct.
   Break a style rule before making the text false, incomplete, unsafe, or
   needlessly flat.

Preserve code, commands, identifiers, product names, required terms, legal
text, and quotations.

### Edit whole pieces

Before rewriting, note preferred words, cadence, formality, useful roughness,
and lines worth keeping. For reports, also note first-person use, audience
knowledge, and how much explanation the source needs.

Replace an AI-shaped outline. Merge generic headings, delete recaps, turn
unnecessary bullets into prose, and break forced symmetry. Keep headings for
navigation and lists for parallel or scanned items. Compression, deduplication,
and fewer headings are not fidelity failures. Do not replace source labels
one-for-one with polished Markdown headings. A short piece rarely needs
multiple headings.

Delete narration that announces or abstracts evidence. Do not recap concrete
detail with abstract impact or evidence summaries. Keep necessary attribution,
uncertainty, and inference.
State repeated evidence once, at the most useful level of detail.

For an edit, add structural units only when navigation, a parallel scan task,
safety, or a real procedure requires them. Sentence limits do not justify more
structural units. Confirm this with `score_delta.py`.

Do not sand every sentence into the same polished rhythm. Keep useful
specificity and variation. Zero lint warnings are not the goal.

## Review, lint, and verify

1. Build the protected-content ledger and voice snapshot. Keep separate rows
   for each risk, mitigation, target, owner, deadline, proposed action, and
   condition–consequence pair.
2. Draft the complete prose. Resolve meaning and whole-piece structure first.
3. Run `references/eval.md` before linting.
4. Save only candidate prose to a temporary file.
5. Resolve `<skill-dir>` as this file's directory. Run:

```bash
python3 <skill-dir>/scripts/lint_prose.py --mode technical /path/to/draft.md
```

Use `strict` or `natural` when that mode applies. Use `--format json` for
machine-readable results.

6. Treat each finding as a review question. Fix it only when the change
   preserves protected content and the genre. Review warnings. Do not chase
   zero.
7. Run the manual review again, then lint after the last edit.
8. Sweep the source in order. Map each protected row to a final passage. Check
   every final claim for actors, values, attribution, negation, certainty,
   force, causal links, and sequence. Compare quantifiers such as each, any,
   all, and some. Confirm that no unsupported assertion became a fact.
9. Return only the requested prose.

For a source-aware diagnostic, run:

```bash
python3 <skill-dir>/scripts/score_delta.py before.md after.md
```

Pass every required exact name, value, identifier, and term from the ledger as
`--protected-token TOKEN`. Add `--protected-count` only when repetition count
is itself meaningful. Use `--fail-on-structural-expansion` only when the task
forbids more structural units.
Structural and lint deltas are review evidence. They do not judge truth,
completeness, authorship, or quality.

If tools are unavailable, perform both reviews by hand. Never claim that a
script ran when it did not run.

## Completion gate

Finish only when the result:

- fulfills the task as finished prose
- maps every protected item without invented substance or relationships
- narrows unsupported claims and makes structure follow content
- retains useful voice and passes review with a reason for each retained finding
- retains no linter error without a protected-text reason

Formal controlled-language or regulated work needs its governing standard,
approved terminology, domain rules, and qualified human review. This skill and
linter do not certify conformance with an external standard.
