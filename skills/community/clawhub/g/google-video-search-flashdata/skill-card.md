## Description:

Search Google Videos with FlashData for video pages across websites. Use for cross-platform video discovery, finding tutorials or talks, and collecting video titles, links, sources and duration labels. Requires a FlashData API key and paid Credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flashdatadev](https://clawhub.ai/user/flashdatadev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search Google Videos across websites to find tutorials, talks, demonstrations, or coverage of a topic, then review original page links and available duration labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to FlashData, and data searches use paid Credits.

Mitigation: Avoid sensitive query terms and check pricing and the approved budget before searching.

Risk: The API key could be exposed if placed in prompts, logs, or skill files.

Mitigation: Keep FLASHDATA_API_KEY in protected environment or secret-manager configuration.

Risk: A timed-out paid request may have been charged, so resubmitting can duplicate the charge.

Mitigation: Check the existing job or FlashData Jobs console before retrying; do not resubmit automatically.

Risk: The benign scan verdict has medium confidence and partial coverage because two local path-like references were unresolved.

Mitigation: Review the skill and resolve or inspect the referenced materials before deployment.

## Reference(s):

- [FlashData Google Videos documentation](https://flashdata.dev/docs/sources/google_videos?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_videos-task)
- [FlashData pricing](https://flashdata.dev/pricing?utm_source=clawhub&utm_medium=integration&utm_campaign=intent_gtm_2026q4&utm_content=google_videos-task)
- [Tool argument schema](references/schema.json)
- [Example query](references/query.json)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown with video titles, original page links, sources, and available duration labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available result fields and result count vary by query; results link to video pages and do not include media files or transcripts.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
