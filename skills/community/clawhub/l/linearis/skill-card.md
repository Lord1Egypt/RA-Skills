## Description:

Linear.app CLI for issue tracking. Use for listing, creating, updating, and searching Linear issues, comments, documents, cycles, and projects. Optimized for LLM agents with JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whoisnnamdi](https://clawhub.ai/user/whoisnnamdi)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agents use Linearis to inspect and manage Linear issues, comments, documents, teams, users, projects, cycles, uploads, and downloads through a JSON-oriented CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned global npm CLI.

Mitigation: Pin and independently verify the npm package version before installation.

Risk: The CLI can use a Linear API token for create, update, delete, upload, and download operations.

Mitigation: Use a least-privilege Linear token and require confirmation before allowing agents to run write, delete, upload, or download commands.

Risk: Passing API tokens directly through shell commands can expose secrets in shell history or process listings.

Mitigation: Prefer restrictive token storage or a secret manager, and avoid command-line token flags when possible.

## Reference(s):

- [Linearis skill page](https://clawhub.ai/whoisnnamdi/skills/linearis)
- [Linearis documentation](https://github.com/czottmann/linearis)
- [Linearis blog post](https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html)
- [Linear](https://linear.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI returns JSON by default for downstream processing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
