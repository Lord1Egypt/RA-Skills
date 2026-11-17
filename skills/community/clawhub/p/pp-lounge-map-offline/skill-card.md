## Description:

Provides offline or air-gapped access to a bundled Priority Pass airport experience catalog for local lounge lookup, facility filtering, airport briefs, and lounge comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skylinehk](https://clawhub.ai/user/skylinehk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query and compare bundled Priority Pass airport records in offline or air-gapped environments when live internet access is unavailable or disallowed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm dependency setup is incomplete and unpinned.

Mitigation: Install only in a restricted environment until the publisher adds a minimal package.json, pins @modelcontextprotocol/sdk and zod, and includes a lockfile.

Risk: The bundled catalog is an offline snapshot and may be stale.

Mitigation: State when fresher data is required and keep answers grounded in the bundled snapshot instead of guessing.

Risk: The catalog covers broader Priority Pass airport experiences, not only lounges.

Mitigation: Clarify the returned experience type and use available type filters before describing records as lounges.

Risk: Using network, deploy, or data rebuild workflows would exceed the skill's offline boundary.

Mitigation: Keep runtime behavior local and read-only; do not call remote MCP endpoints, fetch network resources, request secrets, deploy, or rebuild data.

## Reference(s):

- [Offline MCP Setup](artifact/references/mcp.md)
- [Offline Safety](artifact/references/safety.md)
- [Offline Publishing Notes](artifact/references/publishing.md)
- [ClawHub Skill Page](https://clawhub.ai/skylinehk/skills/pp-lounge-map-offline)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and structured JSON returned by local MCP tools and resources.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a bundled offline snapshot; search results are paginated and limited to at most 25 records per request.]

## Skill Version(s):

1.3.26 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
