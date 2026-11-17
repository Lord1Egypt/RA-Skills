## Description:

Connects an OOMOL account to Anthropic for model discovery, token counting, and message creation through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the oo CLI to inspect Anthropic action schemas, list or retrieve models, count message tokens, and create messages through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup directs the agent to run remote installers without a clear approval step.

Mitigation: Verify the installer and CLI source separately, then approve installation before execution.

Risk: Requests pass through OOMOL using the connected account.

Mitigation: Review submitted content and verify the connected account before running actions; retain required message-payload confirmations.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-anthropic)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Anthropic](https://www.anthropic.com)
- [Anthropic API documentation](https://platform.claude.com/docs/en/api/overview)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to inspect each action schema before constructing a request.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
