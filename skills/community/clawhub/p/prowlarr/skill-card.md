## Description:

Search indexers and manage Prowlarr. Use when the user asks to "search for a torrent", "search indexers", "find a release", "check indexer status", "list indexers", "prowlarr search", "sync indexers", or mentions Prowlarr/indexer management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmagar](https://clawhub.ai/user/jmagar)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to search Prowlarr indexers, inspect indexer health, manage indexer state, and sync configured indexers to connected media applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent API access that can change or delete Prowlarr indexer configuration.

Mitigation: Manually confirm destructive operations such as delete and sync before execution, and restrict use to agents and users trusted to manage Prowlarr.

Risk: The skill requires a Prowlarr API key and may read it from a config file or environment variable.

Mitigation: Store the config file with owner-only permissions, avoid putting the key in shell history or shared environment files, and prefer HTTPS for the Prowlarr URL.

## Reference(s):

- [ClawHub Prowlarr Skill](https://clawhub.ai/jmagar/skills/prowlarr)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Prowlarr URL and API key.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
