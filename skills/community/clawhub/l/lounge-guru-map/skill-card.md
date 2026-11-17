## Description:

Provides offline or air-gapped access to a bundled airport lounge catalog for lounge lookup, facility filtering, airport briefs, and lounge comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skylinehk](https://clawhub.ai/user/skylinehk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to answer airport lounge questions from a bundled offline snapshot when live internet access is unavailable or disallowed. It supports covered lounge search, facility and location filtering, airport lounge briefs, catalog metadata lookup, and comparisons across returned records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm installation path is not reproducibly pinned and the referenced dependency metadata is missing.

Mitigation: Install only in a constrained environment, or require exact pinned dependency metadata and a lockfile from the publisher before deployment.

Risk: The offline catalog can be stale or lack requested lounges because it is a bundled snapshot, not live data.

Mitigation: Tell users when the bundle lacks coverage or freshness, and avoid guessing beyond the returned catalog records.

Risk: Catalog results may include airport-adjacent dining, spa, rest, and work-pod records rather than only traditional lounges.

Mitigation: Preserve the record type in answers and comparisons so users can distinguish lounges from other airport services.

Risk: Using remote endpoints, secrets, deploys, or rebuild workflows would exceed the skill's documented offline safety boundary.

Mitigation: Keep runtime use local and read-only, avoid API keys or remote MCP endpoints, and reject deploy or data rebuild requests.

## Reference(s):

- [Local MCP setup](artifact/references/mcp.md)
- [Offline trust boundary](artifact/references/safety.md)
- [Marketplace packaging notes](artifact/references/publishing.md)
- [ClawHub skill page](https://clawhub.ai/skylinehk/skills/lounge-guru-map)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown answers with local MCP structured JSON results and optional shell command/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in the bundled offline catalog snapshot; no live data fetches at runtime.]

## Skill Version(s):

1.3.27 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
