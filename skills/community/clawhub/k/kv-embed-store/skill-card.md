## Description:

Key-embedding value store with memory integration for fuzzy search by embedding similarity, multi-alias deduplication, and optional memory indexing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaojun0](https://clawhub.ai/user/shaojun0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to store structured key-value data, find entries by semantic similarity, merge aliases, remove duplicates, and optionally expose stored entries through memory search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote embedding providers receive key and query text and require an API key.

Mitigation: Use only a trusted HTTPS embedding provider, avoid custom base URLs unless controlled by the user, and do not store secrets or regulated data in the KV store.

Risk: The standalone script may read an undocumented local credential file and uses environment variable names that differ from the plugin documentation.

Mitigation: Review credential resolution before standalone use and prefer explicit environment configuration for the selected provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaojun0/skills/kv-embed-store)
- [Publisher profile](https://clawhub.ai/user/shaojun0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON and shell command examples; standalone CLI returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plugin tools and the standalone CLI can create, search, list, remove, merge, and deduplicate JSON-backed entries.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
