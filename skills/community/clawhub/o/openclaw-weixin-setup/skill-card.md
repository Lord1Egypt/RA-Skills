## Description:

Install and connect the WeChat channel plugin for OpenClaw, including plugin installation, QR code login, connection verification, gateway restart guidance, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinr](https://clawhub.ai/user/kylinr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and connect WeChat as an OpenClaw messaging channel, then verify and troubleshoot the channel login flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a mutable npm installer and link a personal WeChat account for ongoing OpenClaw channel access.

Mitigation: Review before installing, use a trusted machine, verify the npm package and resolved version, consider pinning a reviewed version instead of @latest, and understand the account-linking implications before scanning the QR code.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and troubleshooting table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that install an npm package, update OpenClaw configuration, trigger QR code login, and verify channel status.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
