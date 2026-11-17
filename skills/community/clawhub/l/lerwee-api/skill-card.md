## Description:

Integrates agents with the Lerwee monitoring system API, including signed authentication, monitoring object management, alert queries, event workflows, and more than 86 documented interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lerwee](https://clawhub.ai/user/lerwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to generate signed Lerwee API requests, configure API clients, query monitoring and alert data, and perform authorized infrastructure administration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support broad infrastructure administration workflows with high-impact operations.

Mitigation: Use it only with an authorized Lerwee environment and require explicit human confirmation before delete, uninstall, user-management, credential-bearing, file-transfer, or script-execution operations.

Risk: Examples and configuration use plaintext HTTP and include credential fields.

Mitigation: Prefer HTTPS with certificate validation, replace example credentials and tokens, and store real secrets outside prompts and files.

Risk: Generated API requests may affect monitoring objects, alerts, users, scripts, and remote agents.

Mitigation: Review requests before execution, verify target IDs and parameters, and test changes in a non-production environment when possible.

## Reference(s):

- [API endpoint index](references/api_endpoints.md)
- [Monitor API details](references/api_details_monitor.md)
- [Device detection API details](references/api_details_device.md)
- [Alert and event API details](references/api_details_alert.md)
- [Business view and topology API details](references/api_details_business.md)
- [User and administration API details](references/api_details_user.md)
- [Monitoring type reference](references/monitoring_types.md)
- [Error code reference](references/error_codes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include signed API request examples, client configuration, response-handling guidance, and operational cautions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
