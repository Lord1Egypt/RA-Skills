## Description:

Lets an agent inspect Replicate account, model, collection, version, and prediction data, and create or cancel predictions through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Replicate users can use the skill to discover models and inspect account data, collections, model versions, and predictions. It can also create or cancel predictions through their connected Replicate account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency may persistently install skills across other agents, and the remote installer has not been verified.

Mitigation: Review the CLI before setup, use an independently verified release, and set OO_SKILLS_SYNC_DISABLED=1 if cross-agent skill installation is unwanted.

Risk: Creating or cancelling a prediction changes Replicate state.

Mitigation: Confirm the exact action, target, and payload with the user before running a write or destructive action.

## Reference(s):

- [Replicate](https://replicate.com)
- [Replicate API documentation](https://replicate.com/docs/reference/http)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-replicate)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON request payloads and connector results, with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The action and payload depend on the requested Replicate operation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
