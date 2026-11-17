## Description:

Queries Guotai Haitong Research Institute reports across macro strategy, industry research, and market analysis to support investment research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtht-tech](https://clawhub.ai/user/gtht-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investment research workflows use this skill to search Guotai Haitong research reports for macro strategy, industry analysis, investment strategy, and market-analysis queries. Outputs should be treated as objective report data, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores API-key material locally and may ask users to provide API-key material through chat.

Mitigation: Review the source before installation, use only approved secret-handoff channels, and rotate or revoke keys if they are exposed.

Risk: The skill sends credentialed requests to configured gateways.

Mitigation: Confirm the gateway allowlist and network destinations before deployment, and monitor credentialed traffic according to organizational policy.

Risk: Authorization uses a device identifier and the security review recommends stronger nonce handling.

Mitigation: Prefer a release that uses random short-lived device nonces and avoids persistent hardware-derived identifiers.

Risk: Skill instructions include forced response text and inspection-limiting language.

Mitigation: Treat artifact files as evidence during review, keep platform and safety policies higher priority, and require human review before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtht-tech/skills/lingxi-researchreport-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/gtht-tech)
- [Guotai Haitong Lingxi research-report gateway](https://zx.app.gtja.com:8443/mcp/researchReport/lingxi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown or text responses with command snippets and structured research-report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorization before credentialed report searches; responses include an investment-advice disclaimer.]

## Skill Version(s):

1.11.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
