## Description:

Helps agents collaborate in PerMark by inspecting the current Markdown document, finding tagged specifications, reading shared notes, and handling inline review comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edelmarschneider](https://clawhub.ai/user/edelmarschneider)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other PerMark users can help an agent locate relevant Markdown sections, understand their current selection, review shared notes, and address inline feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read document passages and notes shared through PerMark.

Mitigation: Enable the connection only for projects and shared notes the agent is permitted to inspect.

Risk: Review comments may be marked resolved before the requested work is complete.

Mitigation: Resolve a comment only after addressing its feedback and verifying the change.

## Reference(s):

- [PerMark skill on ClawHub](https://clawhub.ai/edelmarschneider/skills/permark)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language responses and Markdown document edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can navigate documents and mark review comments resolved when requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
