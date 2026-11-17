# Protected Content Verification

## Conditional Activation

Automatic protection is deliberately narrow:

- `academic-paper`, `formal-document`, and `news-report` generation enable it by document type.
- Legal and technical drafts require multiple matching document cues.
- Fiction, webnovels, self-media, casual Q&A, playful output, and roleplay do not
  auto-enable it. A number or proper noun by itself is never sufficient.
- `--protect-content` or `--protect-term` always overrides automatic selection.

For untyped audits, use `--document-type legal`, `technical`, `academic-paper`, `formal-document`, or
`news-report` when the automatic evidence is too sparse. Use a narrative document
type to suppress a false positive. In a pipeline, automatic protection is loaded in
one final selected stage only to avoid repeating the same token-heavy manifest.

The skill also locks claim polarity, findings, limitations, attribution, and
conclusion direction. The CLI can mechanically recognize some acronyms, standards,
product identifiers, and formal `《titles》`, but it is not a complete named-entity
recognizer. Pass important names with `--protect-term`.

Rewriting can silently alter a percentage, citation, equation, URL, code fragment,
quotation, or required term. Protection has two steps:

1. Add `--protect-content` or `--protect-term` to an audit so the model receives a
   manifest and must flag questionable facts instead of changing them.
2. Run `verify` after revision for a deterministic source-to-candidate comparison.

```powershell
human-writing-skills audit --draft original.md --protect-content --protect-term "Project Atlas"
human-writing-skills verify --source original.md --candidate revised.md --protect-term "Project Atlas"
```

Exit code `0` means all source items remain present; exit code `1` means at least
one is missing or changed. Added protected-looking values are reported separately.
`verify` checks literal preservation only. It cannot determine whether the same
percentage was assigned to the wrong group or a cautious claim became certain.

For a consequential rewrite, also run the opt-in semantic-risk triage:

```powershell
human-writing-skills verify-fidelity --source original.md --candidate revised.md
```

`verify-fidelity` lists every changed claim span with source/candidate offsets and
lines. Shared numbers and citations are anchors for detecting changes in actor,
negation, uncertainty, scope, or attribution. `pass-exact` (exit `0`) requires
identical text; a changed literal is `fail-literal` (exit `1`); changed prose with
unchanged protected tokens is `needs-review` (exit `2`). The cue scan is not a
semantic proof. Resolve each changed claim against the original and, for factual
documents, its supplied source. The original may itself be wrong.
