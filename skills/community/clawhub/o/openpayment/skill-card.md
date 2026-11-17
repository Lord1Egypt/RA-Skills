## Description:

Create x402 USDC payment links using the OpenPayment CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vittominacori](https://clawhub.ai/user/vittominacori)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, merchants, creators, and AI agents use this skill to create shareable USDC payment links on Base with the OpenPayment CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create production Base USDC payment links from agent-collected inputs.

Mitigation: Confirm the amount, recipient wallet address, network, payment type, and description with the user before running the CLI.

Risk: User-provided payment fields or PROXY resource URLs may be unsafe when passed into Bash commands.

Mitigation: Avoid direct shell interpolation of untrusted text and confirm any PROXY resource URL before execution.

Risk: The installed OpenPayment npm package is part of the trusted computing base for creating links.

Mitigation: Install and run the skill only when the OpenPayment npm package is trusted for the deployment environment.

## Reference(s):

- [OpenPayment homepage](https://openpayment.link)
- [ClawHub skill page](https://clawhub.ai/vittominacori/skills/openpayment)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces payment-link command guidance and may return an OpenPayment paymentId and URL.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
