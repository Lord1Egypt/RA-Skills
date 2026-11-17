## Description:

Humanizer by JZ helps agents rewrite AI-sounding text into more natural prose by detecting patterns such as inflated significance, promotional wording, vague attribution, em dash overuse, rule-of-three phrasing, and overused AI vocabulary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzocb](https://clawhub.ai/user/jzocb)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, and agents use this skill to review drafts for common AI-writing patterns and produce a more natural rewrite while preserving meaning, audience, and tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer command uses `latest`, which can resolve to different installer code over time.

Mitigation: Use a pinned and trusted ClawHub installer version when possible, and review the release before installation.

Risk: The skill can rewrite broadly and may over-edit text if the request is underspecified.

Mitigation: State whether you want an in-place edit or only a proposed rewrite, and provide the target language, audience, and tone.

Risk: When file edits are requested, the skill may change user drafts directly.

Mitigation: Review diffs before accepting edited files, especially for high-value or externally published writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jzocb/skills/jz-humanizer)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text rewrite with an optional change summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose rewrites or edit files when the user explicitly asks for file edits.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
