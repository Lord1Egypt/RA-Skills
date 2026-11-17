## Description:

Delegates to the MiniMax CLI (mmx)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when the shared delegation core selects MiniMax, including for large-context batch processing, summarization, and multi-file analysis. It helps prepare and run authenticated mmx requests and save the resulting response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected file contents may be sent to MiniMax during delegation.

Mitigation: Review requested files for sensitive content before sending them.

Risk: The security scan was partial, and behavior in unresolved references was not established.

Mitigation: Review the referenced delegation components before relying on their behavior.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conjure-minimax-delegation)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [MiniMax CLI](https://github.com/MiniMax-AI/cli)
- [MiniMax documentation](https://platform.minimax.io/docs)
- [MiniMax pricing](https://platform.minimax.io/docs/pricing/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [MiniMax response as text or JSON, with Markdown output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requested file contents are included in the prompt (up to 96 KiB); delegated output can be saved as a timestamped Markdown file.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
