## Description:

Performs authorized network reconnaissance and port scanning with Nmap to find open ports, detect services, identify vulnerabilities, and enumerate targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nsahal](https://clawhub.ai/user/nsahal)

### License/Terms of Use:

MIT

## Use Case:

Security practitioners and developers use this skill to draft and interpret Nmap commands for authorized network reconnaissance, port scanning, service detection, and vulnerability checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide broad, privileged, or evasive network-scanning commands.

Mitigation: Confirm authorization before each scan and avoid sudo or stealth/evasion modes unless they are explicitly needed.

Risk: Generated scan commands may be run against an unintended or invalid target.

Mitigation: Require an explicit target and validate targets as hostnames, IP addresses, or CIDR ranges before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nsahal/skills/nmap-recon)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an explicit target and authorization review before executing generated commands.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
