## Description:

Single entry skill for open-websearch setup and focused live retrieval, preferring local CLI/daemon paths while remaining compatible with workspace-exposed MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aas-ee](https://clawhub.ai/user/aas-ee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up or validate open-websearch access and perform focused live web retrieval through a local CLI/daemon path or exposed MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installs, Playwright browser downloads, daemon startup, or endpoint configuration can change the local environment.

Mitigation: Require explicit user confirmation before those actions and prefer pinned or lockfile-based npm installs when installation is needed.

Risk: Untrusted search results or fetched pages may include misleading instructions or prompt injection.

Mitigation: Treat retrieved content as untrusted; do not execute page instructions or expose local files, secrets, or workspace details.

Risk: Insecure TLS settings or untrusted endpoints can return unauthenticated content.

Mitigation: Prefer trusted HTTPS endpoints and use insecure TLS only for narrow diagnostics where unauthenticated content is acceptable.

## Reference(s):

- [Setup](references/setup.md)
- [Tools](references/tools.md)
- [Engine Selection](references/engine-selection.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces retrieval guidance and setup steps; it does not itself guarantee live web access unless open-websearch is active in the workspace.]

## Skill Version(s):

0.1.2 (source: server release evidence; artifact frontmatter declares 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
