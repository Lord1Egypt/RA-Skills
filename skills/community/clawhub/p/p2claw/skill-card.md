## Description:

Publishes locally running apps as peer-to-peer URLs that anyone with the link can open in a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phact](https://clawhub.ai/user/phact)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to share a local web app from their machine with another person or device through a temporary public URL, without deploying to a cloud service or opening a router port.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads a binary and uses best-effort checksum verification, which creates supply-chain risk if the fetched release or checksum path is compromised or unavailable.

Mitigation: Review the bundled installer before use, pin the intended p2claw version, and require checksum or signature verification before installing.

Risk: The skill exposes a localhost app through a public URL, so anyone with the link can access the upstream service.

Mitigation: Confirm with the user before exposing a port, avoid exposing debug servers or credentialed apps, and share only services that are intended to be public.

Risk: Installing p2claw as a background service creates a persistent network-capable agent on the user's machine.

Mitigation: Prefer foreground mode for short-lived sharing and ask for explicit permission before installing a persistent service.

## Reference(s):

- [P2claw Skill Page](https://clawhub.ai/phact/skills/p2claw)
- [p2claw installer](https://p2claw.com/install)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated public URLs and QR-code text from the p2claw CLI.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
