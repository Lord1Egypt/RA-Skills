## Description:

Creates podcast chapters, highlights, and show notes from podcast audio or transcripts, with multilingual and configurable output support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to turn podcast audio or transcripts into chapter markers, highlights, and show notes for publication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad media-task wording and generic read/write/exec authority can cause the skill to operate outside podcast chaptering workflows.

Mitigation: Limit use to podcast audio or transcript tasks, review planned file reads/writes and commands before execution, and prefer a revised release with explicit allowed commands, inputs, outputs, and data handling.

Risk: Podcast audio or transcripts may contain sensitive or copyrighted content.

Mitigation: Confirm rights and consent before processing media, and remove sensitive information before providing content to the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/podcast-chaptering-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown or JSON podcast chapters, highlights, show notes, and processing status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write media or transcript files and may propose or run commands depending on agent permissions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
