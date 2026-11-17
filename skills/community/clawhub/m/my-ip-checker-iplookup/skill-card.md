## Description:

Query the public MyIPChecker IP information API and explain or return the geolocation and network fields it provides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanzhengyang](https://clawhub.ai/user/tanzhengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query MyIPChecker for IPv4 geolocation and network metadata, fetch caller-IP metadata when no IP is supplied, and summarize or troubleshoot returned JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-IP lookups can reveal the runtime's apparent IP address and location metadata.

Mitigation: Use no-parameter lookups only when the user intends to expose that metadata to MyIPChecker.

Risk: The helper accepts a custom base URL, which can broaden where the agent sends network requests.

Mitigation: Do not allow arbitrary --base-url values unless the agent is network-sandboxed or the destination has been reviewed.

Risk: Upstream API and transport failures can return empty or non-JSON bodies.

Mitigation: Treat non-200 responses, empty bodies, and invalid JSON as failed lookups rather than successful results.

## Reference(s):

- [MyIPChecker API Reference](references/myipchecker-api.md)
- [MyIPChecker IP API](https://myipchecker.ai/api/ip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, JSON]

**Output Format:** [Markdown summaries with optional shell commands or raw JSON from the API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to MyIPChecker; failures may be reported as structured transport_error JSON.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
