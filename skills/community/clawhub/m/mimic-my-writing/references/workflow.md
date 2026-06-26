# Workflow Patterns

## Pattern A: Cold mimic (first request for a new author)

1. Ask the user for 2-4 writing samples (1k+ words total). Markdown, plain text, or paste. Save under `samples/<author-slug>/`.
2. Run `scripts/analyze_voice.py samples/<author-slug>/` and read the JSON.
3. Load `references/fingerprint.md` and walk the JSON top-to-bottom, writing out the imitation constraints in plain English (sentence rhythm, vocab anchors, punctuation rate, quirks).
4. Draft.
5. Self-check with the `references/anti-ai-tells.md` hit-list.
6. Deliver.

## Pattern B: Warm mimic (author already has a fingerprint)

If `samples/<author-slug>/` already exists from a prior session, skip to step 2. Re-running the analyzer is cheap (<1s) and keeps the fingerprint fresh.

## Pattern C: Refresh / add samples

If the user provides a new sample for an existing author, drop it into `samples/<author-slug>/` and re-run the analyzer. The fingerprint averages across all samples; more is better up to a point (~10k words is plenty).

## Pattern D: Hybrid voice (mimic + topic shift)

If asked to write in author X's voice about topic Y that the samples don't cover:

1. Build the fingerprint normally from X's samples.
2. List the signature phrases and quirks.
3. Draft topic Y, force-fitting at least 2 signature phrases and every quirk.
4. The lexicon of topic Y is allowed to be new -- the SHAPE of the writing is what carries the voice.

## Pattern E: Critique mode

If asked to grade a draft on "how much does this sound like me":

1. Run the analyzer on the draft AND on the reference samples.
2. Compare burstiness, TTR, profanity rate, em-dash rate, signature-phrase overlap.
3. Score each dimension and call out the biggest miss.
4. Suggest concrete revisions (rewrite one paragraph as a demo).

## Sample organization

```
samples/
  chad/
    soul.md
    ask-for-the-money.md
    origin-stories.md
  vivian/
    email-1.md
    biotech-pitch.md
```

One folder per author. Slug = lowercase, hyphens. If you only have one author, `samples/<their-name>/` still beats dumping files at the top level.

## When NOT to use this skill

- "Write me a haiku" -- no voice context, no need.
- "Summarize this PDF" -- different job.
- "Help me draft an email" with no specified voice and no samples -- ask if they want their own voice mimicked (and which prior samples to use) or just a clean draft.
