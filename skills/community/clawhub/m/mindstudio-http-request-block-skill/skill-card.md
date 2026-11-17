## Description:

Configure and use the MindStudio HTTP Request block to send data to external APIs, webhooks, and web services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sol1986](https://clawhub.ai/user/sol1986)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MindStudio builders use this skill to configure HTTP Request blocks for REST APIs, webhooks, external automations, and record operations. It guides scenario-specific questions, request construction, response handling, and pre-flight checks before a workflow sends data outside MindStudio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTP Request blocks can send credentials, webhook URLs, or sensitive workflow data to external services.

Mitigation: Verify the destination service and hostname, send only the minimum required fields, avoid unauthorized sensitive data transfer, and treat webhook URLs as credentials.

Risk: PATCH, PUT, and DELETE configurations can modify or remove real records.

Mitigation: Require explicit user confirmation and review before generated update or delete workflows affect production records.

Risk: Tokens in URLs or query strings can be logged or exposed by downstream systems.

Mitigation: Prefer authentication headers over query-string tokens whenever the destination API supports them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sol1986/skills/mindstudio-http-request-block-skill)
- [Publisher profile](https://clawhub.ai/user/sol1986)
- [README.md](artifact/README.md)
- [examples.md](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Markdown]

**Output Format:** [Markdown with ready-to-paste HTTP block configuration snippets, JSON body examples, and downstream handling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include URL, method, content type, headers, parameters, body, output variable naming, success and failure handling, and a pre-flight checklist.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
