## Description:

Delegates to the MiniMax CLI (mmx).

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when delegation-core selects MiniMax, or when a large-context MiniMax task is appropriate, to run batch processing, summarization, and multi-file analysis through an authenticated mmx CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local file contents may be sent to MiniMax during delegation.

Mitigation: Review the files and their contents before delegating, and exclude secrets or data you are not comfortable sending to the service.

Risk: The security scan was partial and could not resolve several local path-like references, leaving the evidence incomplete.

Mitigation: Inspect unresolved referenced files and confirm their behavior before enabling the skill.

Risk: Model choices may affect account usage limits.

Mitigation: Choose a model that fits the task and check the applicable MiniMax account limits and pricing before large delegations.

## Reference(s):

- [MiniMax CLI documentation](https://platform.minimax.io/docs)
- [MiniMax pricing documentation](https://platform.minimax.io/docs/pricing/overview)
- [MiniMax CLI project (metadata link)](https://github.com/MiniMax-AI/cli)
- [Conjure project (skill metadata homepage)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-conjure-minimax-delegation)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [MiniMax CLI response in the format requested by the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requested file contents may be truncated at 96 KiB, with any remainder reported; delegated results are saved as timestamped Markdown files.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
