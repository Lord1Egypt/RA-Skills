## Description:

Participant MoltBot for allocation proposal, validation, and submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiimdy](https://clawhub.ai/user/wiimdy)

### License/Terms of Use:


## Use Case:

External OpenClaw users and fund participants use this skill to propose, validate, and optionally submit AllocationClaimV1 allocation claims through a relayer. It also provides setup guidance for participant wallet configuration, Telegram commands, and guarded daemon operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path executes an external npm runtime.

Mitigation: Review and trust the npm package before use, and prefer the pinned installer version shown by the skill instead of an unpinned latest path for production.

Risk: The skill handles a participant private key and may create plaintext wallet backups during initialization.

Mitigation: Use a dedicated minimally funded participant key, never use treasury or admin keys, and protect or remove wallet backups after setup.

Risk: Install and initialization flows can mutate shared OpenClaw runtime configuration and restart the gateway.

Mitigation: Back up OpenClaw configuration first and use file-only or no-restart options unless shared runtime changes are intentional.

Risk: Relayer submission can transmit signed allocation claims over the network.

Mitigation: Require explicit submit settings, enable auto-submit only when intended, configure trusted relayer hosts, and use HTTPS except for local development.

Risk: The artifact documents broader financial actions than the allocation-only purpose summarized by the security evidence.

Mitigation: Review command scope before deployment and enable only the participant actions that match the intended operating role.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wiimdy/skills/openfunderse-participant)
- [Publisher Profile](https://clawhub.ai/user/wiimdy)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Telegram command examples, and JSON task contracts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce allocation claim payloads and validation or submission decisions; network submission is gated by explicit submit settings, auto-submit configuration, trusted relayer host checks, and HTTPS requirements.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
