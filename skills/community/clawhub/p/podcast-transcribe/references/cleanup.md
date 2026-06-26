# Cleanup Guidance

Use this branch when:

- the user says yes after transcription
- the user already has a raw `.txt` transcript that needs cleanup

## Inputs

| Required | Optional |
|----------|----------|
| Raw transcript `.txt` | `.srt` file |
| Original episode URL when available | Original audio file |

## Context Fetch

Fetch the episode page through Jina Reader:

```bash
curl https://r.jina.ai/<podcast-url>
```

Example:

```bash
curl https://r.jina.ai/https://www.xiaoyuzhoufm.com/episode/69b4d2f9f8b8079bfa3ae7f2
```

## Editing Rules

Use the page content as reference context to:

- fix obvious homophone and ASR mistakes
- recover names, products, titles, and other proper nouns
- remove clearly redundant filler words and repetitions
- normalize punctuation and paragraph breaks for readability

Do not:

- invent missing material
- summarize instead of cleaning
- change speaker intent or factual meaning
- overwrite the raw transcript

## Output Naming

Keep the raw transcript unchanged and write a sibling file:

- raw: `episode.txt`
- cleaned: `episode.cleaned.txt`

If the episode URL is unavailable, clean conservatively using transcript-only evidence and explicitly state that no external episode context was used.
