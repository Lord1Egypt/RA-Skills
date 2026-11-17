## Description:

Deploy a scientific research team with 4 agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research teams use this skill to configure a four-agent scientific research pipeline for literature review, hypothesis generation, experiment execution, and report writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill configures broad setup, trust, and external publishing capabilities without enough scoping or safety checks.

Mitigation: Review the skill before installing, keep external publishing disabled until a human approves the content and destination, and limit deployment to reviewed environments.

Risk: Unreviewed dependencies or mutable dependency versions could change the behavior of the deployed research-agent pipeline.

Mitigation: Use reviewed and pinned dependency versions for required skills and binaries before deployment.

Risk: An unsafe deployment prefix or unverified peer identity could create incorrect hostnames or unintended trust relationships.

Mitigation: Validate the deployment prefix as a hostname-safe label and manually verify peer identities before handshakes.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-scientific-research-team-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, the pilot-protocol skill, and a running daemon.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
