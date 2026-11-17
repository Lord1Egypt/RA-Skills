## Description:

Find corporate alumni and former colleagues with company ID and personnel ID lookups for recruitment, B2B lead development, and professional network mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sales teams, and B2B lead generation specialists use this skill to retrieve alumni rosters for a person and school, trace career relationships, and expand contact research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation asks agents to display the local API-key file, which can expose credentials.

Mitigation: Do not print the API-key file contents; store the key in a dedicated file or environment variable with restrictive permissions.

Risk: Alumni lookup, pricing, and account top-up actions can involve paid API usage.

Mitigation: Confirm each paid query, pagination request, or top-up action with the user before running the corresponding script.

Risk: Error reporting and account operations can transmit request context or account details to the service provider.

Mitigation: Use error reporting only after user confirmation and avoid sending unnecessary sensitive context.

Risk: The security summary flags under-disclosed local credential, billing, telemetry, and version-check behavior.

Mitigation: Review the skill and scan findings before installation, and run it only in an environment appropriate for third-party network calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/global-company-person-alumni)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Alumni List API Reference](references/person-alumni-list-api.md)
- [Skill Error Report API Reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses include alumni records, pagination cursor, fee information, and request identifiers.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
