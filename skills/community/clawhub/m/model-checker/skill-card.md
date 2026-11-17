## Description:

Queries the company's available AI model list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcp98252302](https://clawhub.ai/user/mcp98252302)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, or operators can use this skill in OpenClaw to request the currently available internal AI model list from the configured company API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a company API endpoint to retrieve model-list data.

Mitigation: Install only in environments where outbound access to that endpoint is approved.

Risk: HTTP dependencies and transitive dependencies may become stale before broad deployment.

Mitigation: Update axios and transitive dependencies, regenerate the lockfile, and use exact reviewed versions before wider deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mcp98252302/skills/model-checker)
- [Publisher Profile](https://clawhub.ai/user/mcp98252302)
- [Configured Model List API Endpoint](https://cwork-api-test.xgjktech.com.cn/filegpt/t_ai/nologin/aiTypeList)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON response data or a concise error object returned to the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires outbound HTTPS access to the configured company API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
