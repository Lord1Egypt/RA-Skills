## Description:

HTTP客户端 helps developers send GET, POST, PUT, DELETE, and PATCH requests with custom headers, request bodies, response checks, timeouts, retries, and authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft or adapt HTTP client workflows for REST, GraphQL, webhook testing, API integration, data collection, and automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided URLs, headers, request bodies, bearer tokens, API keys, or basic-auth values may be sent to the selected remote service.

Mitigation: Use the skill only for intended API targets, review request destinations before execution, and keep real credentials in environment variables or a secret manager.

Risk: Request history can retain sensitive request metadata such as URLs and headers.

Mitigation: Avoid placing secrets directly in URLs or headers shown to the agent, mask sensitive values in examples, and clear or limit retained history when handling confidential requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-http-client)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python code examples and request configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTP request examples, response validation guidance, timeout settings, retry settings, and authentication guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
