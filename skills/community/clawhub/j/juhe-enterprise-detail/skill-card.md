## Description:

Queries Juhe.cn for exact Chinese enterprise registration details by full company name, registration number, or unified social credit code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve detailed Chinese business registration information, including legal representative, capital, address, shareholders, branches, changes, and business abnormality records. It is intended for exact lookups after the user provides a full company name, registration number, or unified social credit code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Juhe API credentials may be exposed locally if passed on the command line or stored in an unprotected .env file.

Mitigation: Prefer JUHE_ENTERPRISE_DETAIL_KEY, avoid putting keys in command history or URLs, and protect any local .env file with restrictive permissions.

Risk: Enterprise names or identifiers submitted for lookup are sent to Juhe.cn.

Mitigation: Use the skill only when sharing the queried company name, registration number, or unified social credit code with Juhe.cn is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/juhemcp/skills/juhe-enterprise-detail)
- [Juhe Enterprise Detail API Documentation](https://www.juhe.cn/docs/api/id/319)
- [Juhe Data Platform](https://www.juhe.cn)
- [Juhe Enterprise Detail API Endpoint](https://japi.juhe.cn/enterprise/getDetailByName)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text enterprise-detail summary followed by formatted JSON; setup and usage guidance in Markdown with bash examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Juhe API key configured through JUHE_ENTERPRISE_DETAIL_KEY, a local .env file, or a command-line key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
