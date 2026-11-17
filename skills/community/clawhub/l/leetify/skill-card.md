## Description:

Get CS2 player statistics, match analysis, and gameplay insights from Leetify API. Supports player comparison and season stats. Use for stat queries and demo analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeminay](https://clawhub.ai/user/jeminay)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve CS2 player statistics, compare players, inspect match details, and generate tactical demo-analysis summaries from Leetify data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Demo-analysis behavior uses API-supplied data for downloads and cache paths, which can create local file, network, and resource-exhaustion risks.

Mitigation: Run in a constrained environment; prefer a revised version that sanitizes cache filenames, confines cache reads and writes, allowlists replay hosts, and enforces download, decompression, parsing, and HTTP timeouts.

Risk: The skill requires a Leetify API key and local Steam ID mappings.

Mitigation: Provide only a scoped API key, protect local mapping data, and avoid sharing generated logs or JSON outputs without reviewing them for player-identifying details.

Risk: Runtime dependencies are declared but not pinned in the release evidence.

Mitigation: Install in an isolated environment and pin dependency versions before repeated or production use.

## Reference(s):

- [Leetify API Documentation](https://api-public-docs.cs-prod.leetify.com/)
- [Leetify Skill Page](https://clawhub.ai/jeminay/skills/leetify)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payloads, and text analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LEETIFY_API_KEY, local Steam ID mappings, Python dependencies requests and demoparser2, and system utilities bash, bunzip2, and gunzip.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
