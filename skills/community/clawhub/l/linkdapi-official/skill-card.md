## Description:

LinkdAPI helps agents use LinkdAPI's LinkedIn data API for profile lookups, people and company search, job and post research, lead enrichment, and API workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethcipher](https://clawhub.ai/user/ethcipher)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to retrieve LinkedIn-derived profile, company, job, post, article, and services data through LinkdAPI and to build API workflows for research, enrichment, and market intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: People lookup, lead generation, recruiting, and outreach workflows can involve LinkedIn-derived personal data without adequate privacy or consent guardrails.

Mitigation: Use the skill only where there is a legitimate and compliant reason to process the data, and review planned usage for privacy, consent, and outreach requirements before execution.

Risk: The skill can support bulk collection or unsolicited contact workflows.

Mitigation: Avoid bulk collection and unsolicited contact use cases; scope requests narrowly and apply appropriate data minimization.

Risk: API key exposure could allow unauthorized LinkdAPI access.

Mitigation: Protect the LINKDAPI_KEY value, avoid placing it in shared logs or generated files, and prefer isolated environments for REST calls or pinned SDK versions.

## Reference(s):

- [LinkdAPI ClawHub skill page](https://clawhub.ai/ethcipher/skills/linkdapi-official)
- [LinkdAPI API specification](https://linkdapi.com/apispec.yml)
- [LinkdAPI API reference](references/api-ref.md)
- [LinkdAPI endpoint manifest](references/skills.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST endpoint paths, request parameters, authentication header guidance, SDK references, and response handling notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
