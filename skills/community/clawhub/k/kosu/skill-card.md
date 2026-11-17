## Description:

Add, reorder, and manage content in a Kosu queue via API. Use when adding URLs, checking what's queued, suggesting content, reordering items, or tracking what's been read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewspear](https://clawhub.ai/user/matthewspear)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use an AI agent to add links to their Kosu queue, review and reorder queued items, manage suggestions, and track reading progress through Kosu's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation instructions download and overwrite a local skill file from usekosu.com, and the downloaded contents were not assessed in the release scan.

Mitigation: Review the fetched skill file before replacing an existing local copy, and inspect its contents before following its instructions.

Risk: Authenticated API actions use the user's Kosu API key.

Mitigation: Use a dedicated key with minimal scope, send it only to usekosu.com, and rotate or revoke it if anything unexpected happens.

## Reference(s):

- [Kosu](https://usekosu.com)
- [Authentication setup guide](https://usekosu.com/docs/getting-started#authentication)
- [Kosu OpenAPI specification](https://usekosu.com/openapi.json)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses are JSON; requires a KOSU_API_KEY for authenticated actions.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
