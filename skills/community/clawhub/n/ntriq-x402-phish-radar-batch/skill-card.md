## Description:

Batch phishing detection for up to 500 URLs or domains with flat $9.00 USDC payment via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to submit batches of URLs or domains to an external phishing-check service and receive risk levels and recommendations for each target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends submitted URLs or domains to the publisher's external service.

Mitigation: Do not submit private internal URLs or domains unless sharing them with the publisher is acceptable for the user's environment.

Risk: The skill requires authorization of a disclosed USDC payment before using the service.

Mitigation: Confirm the flat $9.00 USDC price, x402 payment header, and Base mainnet payment context before making requests.

Risk: Automated phishing classifications can affect blocking, avoidance, or investigation decisions.

Mitigation: Review high-impact results before taking irreversible enforcement action.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-phish-radar-batch)
- [Publisher profile](https://clawhub.ai/user/ntriq-gh)
- [Ntriq x402 homepage](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline HTTP, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to call a paid external API that returns per-target JSON phishing risk levels and recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
