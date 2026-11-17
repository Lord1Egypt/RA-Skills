## Description:

Queries MiniMax Token Plan usage, remaining quota, and reset timing for supported text, image, video, music, and speech models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MiniMax API users use this skill to query Token Plan quotas and understand remaining capacity and reset timing before running text, image, video, music, or speech workloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MiniMax API keys may be exposed if pasted directly into shell commands, logs, shared transcripts, or shell history.

Mitigation: Prefer MINIMAX_API_KEY from a protected environment or secret manager, avoid command-line key arguments, and rotate any key that may have been exposed.

## Reference(s):

- [MiniMax Token Plan remains API endpoint](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains)
- [ClawHub release page](https://clawhub.ai/hongjiahao371-pixel/skills/minimax-quota)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text quota output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a MiniMax API key supplied as an argument or through MINIMAX_API_KEY; the script prints formatted quota summaries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
