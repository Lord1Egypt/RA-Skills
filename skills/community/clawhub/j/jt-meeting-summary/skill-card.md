## Description:

Provides prompt-only guidance for faithfully summarizing meeting and call transcripts into structured minutes, concise summaries, speaker summaries, action items, titles and tags, JSON output, or visual-summary prompts without external API or tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quent1nq](https://clawhub.ai/user/quent1nq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn meeting or phone-call transcripts into faithful Chinese-oriented minutes, summaries, action items, JSON records, title/tag components, or visual-summary prompts. It is best suited for transcript summarization workflows that need explicit handling of speakers, decisions, deadlines, unresolved questions, and missing information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting and call transcripts may contain phone numbers or other personal data.

Mitigation: Review generated summaries before sharing or storing them, and omit or mask identifiers unless the user explicitly requires raw identifiers.

Risk: The skill is strongly oriented toward Chinese-language meeting and call summary formats.

Mitigation: Use it when Chinese-oriented output is desired, or explicitly request another language or format before generating the summary.

Risk: Summaries can misstate speaker ownership, deadlines, decisions, or conclusions if the transcript is ambiguous.

Mitigation: Compare speaker names, task owners, deadlines, and conclusions against the transcript, and use missing-information markers when the source does not support a field.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quent1nq/skills/jt-meeting-summary)
- [Phone-call summary](references/call-summary.md)
- [Concise minutes Markdown](references/concise-minutes.md)
- [Full meeting minutes JSON](references/full-minutes-json.md)
- [Summary components](references/summary-components.md)
- [Ten-minute / long-meeting summary](references/ten-minute-summary.md)
- [Visual / comic summary prompt](references/visual-summary-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown, strict JSON when requested, or a Markdown image-generation prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only; security evidence reports no code execution, network access, persistence, or hidden data movement.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
