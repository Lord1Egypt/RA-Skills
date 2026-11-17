## Description:

Query homes.com (US real-estate portal) from a shell with the fpx CLI (@fetchproxy/cli) instead of running the homes-mcp server — search listings, resolve street addresses, fetch property detail/photos/history, and read the signed-in user's saved homes, all through a one-shot call over their own signed-in browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search homes.com listings, inspect property details and history, resolve addresses, or read their saved homes and searches from shell workflows that use their signed-in browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI and browser extension use the user's signed-in homes.com session.

Mitigation: Use them only if trusted, restrict extension site access to homes.com, review pairing permissions, and revoke pairing when no longer needed.

Risk: Saved-page recipes can leave account HTML in temporary files.

Mitigation: Protect those files and remove them after use.

Risk: External dependency binaries were not audited.

Mitigation: Verify the extension release zip against its published SHA-256 checksum or build it from source.

## Reference(s):

- [homes.com request recipes](references/homes-requests.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [homes.com](https://www.homes.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Homes.com query results as HTML or JSON, with shell, Node.js, and jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saved-home and saved-search results require a signed-in homes.com browser session.]

## Skill Version(s):

2.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
