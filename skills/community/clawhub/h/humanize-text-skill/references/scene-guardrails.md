<!--
  Migrated from shuorenhua/references/scene-guardrails.md (MIT, MrGeDiao).
  humanize-text-skill absorbs shuorenhua's Chinese completeness verbatim;
  cross-references updated to humanize-text-skill paths where needed.
-->

# Scene Guardrails

Judge the scene first, then decide what must not be disturbed. Removing template residue does not mean forcing every kind of text into one shared tone.

Whenever `references/` is available, start by using [Protected Spans](./protected-spans.md) to fence off text that must not drift. Then use the scene guardrails here to narrow the allowed rewrite range.

This file defines only large-scene boundaries. Publishable sub-scenes such as README intros, release notes, forum posts, and issue replies should also consult [Scene Packs](./scene-packs.md), even if the coarse first-pass scene looks like `docs` or `status`. Keep the more conservative fact and terminology guardrails from this file.

## `chat`

Goal:

- natural
- direct
- responsive

Default tier:

- `minimal`

Default strategy for unsupported attribution:

- `rewrite-safe`

Do not disturb:

- do not make the reply harsher in the name of "less AI"
- do not invent value judgments or performative intensity
- do not turn a simple reply into a closing speech
- do not replace a response with psychology, relationship diagnosis, or vague reassurance

Prefer to preserve:

- conversational rhythm
- the actual reply relationship
- natural spoken pauses
- any original wording or quoted span the user explicitly wants to keep

## `status`

Goal:

- high fact density
- the reader should leave knowing progress, problems, and next steps

Default tier:

- `minimal` or `standard`

Default strategy for unsupported attribution:

- `audit-only`

Do not disturb:

- do not delete the timeline
- do not delete ownership
- do not soften risk
- do not sacrifice reporting efficiency just to sound "more human"

Prefer to preserve:

- time
- actions
- results
- risks
- blockers
- numbers, dates, scope, and ownership

## `docs`

Goal:

- searchable
- reproducible
- quotable

Default tier:

- `minimal`

Default strategy for unsupported attribution:

- `audit-only`

Do not disturb:

- do not break terminology stability
- do not rewrite search terms, commands, API names, or field names away
- do not trade system-subject precision for casual phrasing
- do not turn formal documentation into chat

Prefer to preserve:

- terminology
- system-behavior subjects
- step order
- constraints
- commands, paths, parameters, fields, errors, and status codes

## `public-writing`

Goal:

- coherent register
- clear judgment without stiffness or pose

Default tier:

- `standard`

Default strategy for unsupported attribution:

- `rewrite-safe`

Do not disturb:

- do not manufacture exaggerated judgment for rhythm
- do not turn restrained prose into hype or creator-copy
- do not force quote-ready one-liners
- do not turn formal announcements into social comments

Prefer to preserve:

- the author’s actual stance
- the appropriate level of formality
- necessary rhetorical pacing
- existing facts, ownership, and checkable citations

Long-form addendum:

- Chinese long-form public writing (roughly `1000+` characters) should default to `bounded` scope, especially for essays, postmortems, commentary, and prose with paragraph rhythm. Clean real sentences in place, and send fully empty shell sentences to a "suggested deletions (needs confirmation)" list. Do not merge sentences or reorder paragraphs.
- If the user explicitly says "keep everything", "do not delete any sentence", or reports that `bounded` still deletes too much, switch to stricter `in-place`, where even empty shell sentences stay and only receive internal tone reduction.
- If the prompt contains signals like `preserve length`, `do not shrink`, `keep the rhythm`, `do not delete`, or `stay close to the original`, treat it like long-form preservation even if the text is shorter than 1000 characters.
- Under both `bounded` and `in-place`, do not compress the whole piece into a short summary. Preserve paragraph rhythm and repetition that carries transitions. The difference is only whether empty shell sentences move into a deletion list or remain for lighter in-sentence cleanup.

## Mixed-scene handling

If a passage hits multiple scenes:

1. identify the primary purpose first
2. fence protected spans, then let the main-scene guardrails define the ceiling
3. clean only the obviously jarring wording from the secondary scene instead of chasing perfect scene purity
