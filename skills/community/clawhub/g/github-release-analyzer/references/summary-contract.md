# Summary Contract

Flow:

```text
prepare -> summarize -> render -> deliver -> commit
```

Each selected release produces exactly one summary string.

## Requirements

- Output in the primary language of the invocation instruction (zh → 中文, en → 英文)
- Keep facts anchored to the release body
- Keep the summary distilled and high-signal, but do not force it into a fixed length budget
- Output JSON only. Each summary item must be a single non-empty string, not an object.
- Distill the release into a readable, high-signal summary rather than mirroring the changelog.
- Use markdown to make the result easy to scan. Prefer short sections, bullet lists, and compact grouping over long continuous prose.
- Do not force a fixed internal structure, but the summary should still feel organized and easy to skim.
- Prioritize the most important themes and expand when the release has multiple genuinely meaningful areas of change.
- Summarize fixes and improvements clearly, not inflated counts or vague praise.
- Focus on the most directly affected users or maintainers, and expand when that adds real decision value.
- Summary text must be in the same language as the invocation instruction, regardless of the source release language
- Do not translate the changelog line by line
- Do not invent scope, quantities, or recommendations not clearly supported by the source
- Avoid hype such as `大幅重构`, `显著提升`, `建议所有用户升级` unless the source clearly justifies it

## Render payload

`run.py render` reads stdin JSON in this shape:

```json
{
  "outputTemplate": "default",
  "language": "zh",
  "releases": [{ "tag_name": "v2026.4.26", "published_at": "2026-04-28T01:11:02Z", "html_url": "..." }],
  "summaries": [
    "..."
  ]
}
```

Validation rules:

- `releases.length == summaries.length`
- when building the render payload, keep the release fields required by `render`, especially `tag_name`, `published_at`, and `html_url`
- each `summaries[i]` must be a non-empty string
- each summary should be organized for scanning, not written as one large undifferentiated block of prose
- `language` should match the invocation instruction language, use `zh` or `en`
- one release uses single-release template, multiple releases use multi-release template
