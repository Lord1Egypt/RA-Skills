## Description:

Search and retrieve Rust crate metadata, versions, and download stats from the crates.io REST API without authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Rust maintainers use this skill to search crates.io packages and retrieve crate metadata, version history, download counts, and related package details through a Pipeworx-hosted MCP gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crate metadata is routed through a disclosed third-party Pipeworx gateway rather than direct official crates.io responses.

Mitigation: For security-sensitive dependency choices, verify package names, versions, and metadata against crates.io or another trusted source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-crates)
- [Pipeworx crates MCP endpoint](https://gateway.pipeworx.io/crates/mcp)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns third-party crate lookup results; verify security-sensitive dependency choices against crates.io or another trusted source.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
