## Description:

Add, reorder, and manage content in a Kosu queue via API. Use when adding URLs, checking what's queued, suggesting content, reordering items, or tracking what's been read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewspear](https://clawhub.ai/user/matthewspear)

### License/Terms of Use:

MIT-0

## Use Case:

People using AI agents to curate a Kosu reading queue can add links, organize and reorder items, manage suggestions, and track what they have read through the Kosu API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installation command downloads remote skill content and writes it over a local skill definition; the remote content was unavailable for the partial scan.

Mitigation: Review the current remote skill.md and destination before installing, and avoid overwriting a local skill file without checking its contents.

Risk: API requests use an account credential, and the security guidance notes the scan evidence is incomplete.

Mitigation: Use a dedicated API key with minimal scope, send it only to usekosu.com, and revoke it if unexpected activity occurs.

## Reference(s):

- [Kosu homepage](https://usekosu.com)
- [Authentication setup guide](https://usekosu.com/docs/getting-started#authentication)
- [Kosu API v1](https://usekosu.com/api/v1)
- [OpenAPI specification](https://usekosu.com/openapi.json)
- [Kosu pricing](https://usekosu.com/pricing)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated API requests use the KOSU_API_KEY environment variable.]

## Skill Version(s):

1.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
