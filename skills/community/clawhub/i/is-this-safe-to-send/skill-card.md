## Description:

Checks whether an outbound message is going to the intended conversation and whether it contains secret-shaped values or credential paths before sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill before forwarding, cross-posting, or sending copied content to confirm the target and detect secrets or credential paths. It returns a send, confirmation, or do-not-send verdict with reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required local plugin observes message activity and keeps a local activity ledger.

Mitigation: Review or install the plugin separately before use, and enable it only in workspaces where a local activity ledger is acceptable.

Risk: In enforce mode, the plugin can hook outbound sends and cancel messages containing secret-shaped values.

Mitigation: Start with observe-only behavior where possible and enable enforce mode only after confirming the workflow matches user and workspace expectations.

Risk: The skill may install and enable the plugin automatically when plugin tooling is available.

Mitigation: Require explicit approval before plugin installation in managed or sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/is-this-safe-to-send)
- [Project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status report with an ACTION verdict and evidence sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [First line is ACTION: SEND, ACTION: CONFIRM_WITH_USER, or ACTION: DO_NOT_SEND; secret values are masked.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
