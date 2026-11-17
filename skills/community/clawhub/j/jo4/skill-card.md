## Description:

URL shortener, QR code generator, and link analytics API. Create short links, generate QR codes, and track click analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anandrathnas](https://clawhub.ai/user/anandrathnas)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create and manage Jo4 short links, QR codes, campaign parameters, and link analytics through the Jo4 API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create, update, or delete Jo4 links using a user's JO4_API_KEY.

Mitigation: Install only when the agent is intended to manage Jo4 links, and review requests before allowing create, update, or delete operations.

Risk: Analytics responses can include visitor behavior data such as clicks, geography, devices, browsers, and referrers.

Mitigation: Share raw analytics only when authorized to disclose visitor behavior data.

## Reference(s):

- [Jo4 Website](https://jo4.io)
- [Jo4 API Documentation](https://jo4-api.jo4.io/swagger-ui/index.html)
- [Jo4 API Keys](https://jo4.io/api-keys)
- [ClawHub Skill Page](https://clawhub.ai/anandrathnas/skills/jo4)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JO4_API_KEY for protected Jo4 API operations; anonymous URL creation has limited features and no analytics access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
