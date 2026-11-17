## Description:

Provide consistent status updates and concise summaries after each action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szpili](https://clawhub.ai/user/szpili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep tool-driven work visible through structured status updates and concise completion or blocked summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to override other skills and default response style, which can conflict with higher-priority instructions or workflow-specific output formats.

Mitigation: Keep its formatting rules subordinate to system, developer, safety, and user instructions, and review fit before installation.

Risk: Tool-by-tool status messages could reveal too much operational detail in sensitive workflows.

Mitigation: Avoid installing it for workflows where intermediate operational details should remain hidden or tightly controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szpili/skills/interaction-pipeline)
- [ClawHub publisher profile](https://clawhub.ai/user/szpili)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with structured status and summary lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; formats assistant responses after actions or blocks.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
