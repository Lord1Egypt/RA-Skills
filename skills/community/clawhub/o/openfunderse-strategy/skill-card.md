## Description:

Participant MoltBot for allocation proposal, validation, and submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiimdy](https://clawhub.ai/user/wiimdy)

### License/Terms of Use:


## Use Case:

External fund participants and operators use this skill to propose allocation weights, validate AllocationClaimV1 claims, and optionally submit participant actions through a configured relayer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles participant wallet private keys and can support financial actions.

Mitigation: Use an isolated OpenClaw environment with a dedicated low-value participant wallet; do not use treasury, custody, or admin keys.

Risk: Installer execution and floating install paths can run remote package code before it is reviewed.

Mitigation: Review or pin installer provenance before production use and prefer the pinned package version shown in the release metadata.

Risk: Environment synchronization and gateway restarts can mutate global OpenClaw runtime state.

Mitigation: Back up OpenClaw configuration, restrict file permissions, and disable env sync or gateway restart until the behavior is reviewed.

Risk: Relayer submission can transmit claims or other participant actions to a network service.

Mitigation: Require explicit submit gates, configure trusted relayer hosts, prefer HTTPS relayer URLs, and confirm deposit, withdraw, and redeem commands are intended before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wiimdy/skills/openfunderse-strategy)
- [Publisher profile](https://clawhub.ai/user/wiimdy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce allocation claim structures, validation results, relayer submission guidance, and OpenClaw environment setup instructions.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
