## Description:

Use for a short local human handoff when an AI workflow is blocked on a visual or interactive step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metalony](https://clawhub.ai/user/metalony)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use HumanCanHelp to hand a blocked visual or interactive browser or desktop step to a human helper for short-lived completion. It is suited to CDP browser-tab sharing, VNC desktop sharing, and workflows where the agent needs human observation or input before continuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A helper session can expose live browser or desktop control over a network or the public internet.

Mitigation: Use the skill only with trusted helpers, prefer CDP browser-tab sharing over VNC desktop sharing, keep access local or firewalled, and avoid --public unless it is necessary.

Risk: Sessions do not require authentication unless the operator configures a password.

Mitigation: Set a strong, unique password for each session, especially when exposing a public tunnel or working outside a trusted local network.

Risk: Mask regions are helper-side controls and should not be treated as full redaction of the underlying CDP or VNC stream.

Mitigation: Do not use masking as the only protection for secrets, payments, privileged administration, sensitive recovery flows, or other information that must not be visible or controllable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metalony/skills/hcl)
- [Publisher profile](https://clawhub.ai/user/metalony)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and CLI options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to run a local helper session and interpret completion, owner-action-required, cannot-solve, and timeout outcomes.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
