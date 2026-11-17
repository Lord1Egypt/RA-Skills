## Description:

Find the documentation of a project's direct dependencies from package.json, pyproject.toml, requirements.txt, Cargo.toml or go.mod using public registry metadata, then build an attributed llms.ink context pack. Use when the user wants their agent to know the libraries a project uses; not for private registries or vendored code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukax](https://clawhub.ai/user/lukax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find public documentation for a project's direct dependencies and assemble an attributed context pack for an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious and notes an unpinned CLI download, a dependency lookup issue, and partial inspection of a bundled script.

Mitigation: Follow the security guidance: do not install until a reviewed, pinned CLI version is available and local or Git Cargo dependencies are confirmed excluded from public lookups.

Risk: Dependency names may be sent to public registries during documentation lookup.

Mitigation: Check for private registry configuration and ask before any public lookup when a private registry is used; keep local and Git Cargo dependencies out of public lookups.

## Reference(s):

- [llms.ink workflows](https://llms.ink/workflows/)
- [Read dependency docs on ClawHub](https://clawhub.ai/lukax/skills/ink-deps)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON and Markdown dependency documentation context packs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports skipped dependencies and reasons; each pack contains up to five distinct sources by default.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
