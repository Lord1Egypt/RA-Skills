# Protected Content

## Activation Gate

Load this module automatically only for serious factual output: academic papers,
official documents, news reports, legal documents, and technical documentation. Require strong document
signals for untyped drafts; an isolated number, URL, or proper noun is not enough.

Do not auto-load it for fiction, webnovels, casual Q&A, playful text, roleplay, or
self-media posts. Explicit user requests such as `--protect-content` and
`--protect-term` override the gate.

In a multi-stage audit, auto-load this module in one final selected stage only.
Do not repeat the same manifest in every stage unless the user explicitly requests it.

## Aim

Preserve facts and exact spans that stylistic rewriting must not change.

## Protected Categories

- Numbers, dates, percentages, prices, measurements, dosages, and identifiers
- Citations, citation keys, footnote markers, equations, and symbols
- URLs, file paths, code spans, and fenced code blocks
- Directly quoted source passages and attributed statements
- User-specified names, terminology, product names, legal language, and house terms
- Claim polarity, reported findings, limitations, attribution, and conclusion direction

## Rules

- Do not silently normalize, translate, shorten, reorder, or "improve" protected content.
- Preserve occurrence counts when repetition carries factual or structural meaning.
- If grammar requires a change around a protected span, rewrite the surrounding sentence.
- If a protected item appears wrong, flag it for the user; do not correct it without authority.
- Do not invent a missing citation, statistic, result, source, partner, or quotation.
- Before rewriting, record the main claim, evidence relation, uncertainty level,
  limitations, and conclusion polarity. Preserve them unless the user asks for a
  substantive correction rather than stylistic editing.
- Treat mechanically detected acronyms and formal identifiers as candidates, not a
  complete named-entity recognizer. Use explicit protected terms for important person,
  organization, product, standard, statute, and project names.
- After rewriting, compare the source and candidate mechanically. A fluent rewrite that
  changes a result or citation is a failed rewrite.

## Output Check

```text
Protected Content Check
- Preserved exactly:
- Missing or changed:
- Added factual-looking content requiring verification:
- Rewrite status: pass / fail
```
