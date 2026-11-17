## Description:

AI-powered OSINT intelligence reports via API, including categorized intelligence briefings, domain reconnaissance, social lookup, and breach checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsan3274](https://clawhub.ai/user/ahsan3274)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and security teams use this skill to retrieve OSINT briefings and run API-backed lookups for domains, usernames, and email breach exposure. It is intended for authorized investigations where sending targets to the hosted OSINT service is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OSINT targets and the bearer API key are sent to osint.ahsan-tariq-ai.xyz.

Mitigation: Use the skill only for authorized targets, avoid submitting sensitive third-party email addresses without permission, and rotate the API key if service behavior is unexpected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahsan3274/skills/osint-api)
- [OSINT API base endpoint](https://osint.ahsan-tariq-ai.xyz/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OSINT_API_KEY and sends queries to osint.ahsan-tariq-ai.xyz.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
