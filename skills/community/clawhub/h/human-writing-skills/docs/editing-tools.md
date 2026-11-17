# Fidelity, Statistics, and Conservative Fixes

These tools are optional. They are deliberately separated so ordinary generation
does not load rewrite comparison rules, statistics, or mechanical cleanup logic.

## Three Input Channels

| Input | Authority | Activation |
| --- | --- | --- |
| `--original` | Meaning of text being rewritten | Only when supplied; enables `rewrite-fidelity` |
| `--reference` | Transferable style features | Only with an explicit reference or style request |
| `--source` | Factual evidence | Only for serious academic, formal, news, legal, or technical work |

Do not use `--reference` as evidence for facts. Do not imitate the style of
`--original` unless it is also deliberately supplied as a reference.

## Meaning-Preserving Rewrite

```powershell
human-writing-skills build --style self-media --original original.md --task "Rewrite for clarity without adding facts."
human-writing-skills audit --draft revised.md --original original.md --profile fidelity
human-writing-skills pipeline --draft revised.md --original original.md --auto --output-dir audit
```

The fidelity pass compares entities, numbers, polarity, uncertainty, chronology,
causality, comparison axes, attribution, and constraints. It reports omitted,
broadened, reversed, reattributed, reordered, or invented meaning. It does not ask
the model to preserve awkward wording.

## Quick Humanize And Voice Preservation

```powershell
human-writing-skills humanize --draft original.md --style fiction --mode quick
human-writing-skills humanize --draft original.md --style fiction --mode deep
human-writing-skills audit --draft revised.md --original original.md --profile preservation
```

`quick` loads surface-pattern review, rewrite fidelity, and
`voice-ambiguity-preservation`. `deep` additionally loads high-cost cliche,
formulaic-structure, prose-progress, imperfect-prose, and editor-loop guidance.
Examples remain absent unless `--with-examples` is passed.

The preservation audit compares the original with the rewrite for useful ambiguity,
intentional repetition, motifs, hesitation, subtext, speaker markers, and unresolved
interaction pressure. It requires `--original`, stays out of automatic pipelines,
and must distinguish those features from unclear reference or missing grammar.

## Optional Style Statistics

```powershell
human-writing-skills stats --draft article.md --style self-media
human-writing-skills pipeline --draft article.md --auto --with-stats --output-dir audit
```

The report includes sentence and paragraph length variation, moving-average
type-token ratio (MATTR), repeated trigram ratio, and explicit-transition density.
For Chinese and Japanese, MATTR uses character-oriented Han/kana tokens; Latin-script
and Arabic profiles use Unicode word-like tokens. Values from different tokenization
families must not be compared directly. Short samples are marked low confidence. Raw
type-token ratio is intentionally omitted because it changes sharply with sample length.

These metrics are editing diagnostics, not evidence of AI authorship. Compare a
draft with its own genre, language, and intended voice rather than a universal
threshold.

## Conservative Fix Preview

```powershell
human-writing-skills fix --draft article.md --preview
human-writing-skills fix --draft article.md --output cleaned.md
human-writing-skills fix --draft article.md --apply
```

Preview is the default. Automatic edits are limited to high-confidence mechanical
residue such as finished-prose chatbot closings and a few meaning-equivalent filler
or wordiness reductions. The command never automatically rewrites claims, numbers,
comparisons, character voice, or contextual syntax.

## Repeated Comparison Ladders

The linter treats two valid Chinese `比` clauses as a review signal (`STR002`). Three
or more in one sentence become high risk (`STR004`) in fiction, webnovels,
self-media, and general prose. Necessary data comparisons in news and academic
writing are suppressed. The repair is contextual: keep distinct facts with a clear
comparison axis; rewrite decorative escalation into one observation, action, image,
or consequence. `fix` does not delete these structures automatically.
