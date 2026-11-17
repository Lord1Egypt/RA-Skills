## Description:

Send HTTP requests with Python requests instead of curl when quoting and escaping would be error-prone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pumpkinttl](https://clawhub.ai/user/pumpkinttl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to make GET, POST, PUT, and DELETE HTTP requests with headers, query parameters, JSON bodies, form data, timeout control, and concise response inspection when curl quoting would be fragile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound HTTP requests to arbitrary network targets.

Mitigation: Install and use it only in environments where agent-initiated outbound HTTP requests are acceptable.

Risk: Full request URLs are kept in local logs by default.

Mitigation: Avoid credential-bearing query strings, signed URLs, production secrets, and use --no-log when requests may include sensitive data.

Risk: Requests to internal services or metadata endpoints can expose sensitive environment data.

Mitigation: Do not use the skill for internal services or metadata endpoints unless the runtime network boundary and target are explicitly approved.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [ClawHub skill page](https://clawhub.ai/pumpkinttl/skills/httprequests)
- [Publisher profile](https://clawhub.ai/user/pumpkinttl)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown summaries of request commands, status, headers when requested, response body excerpts, and errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response body output is truncated by the script's max-body setting unless changed by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
