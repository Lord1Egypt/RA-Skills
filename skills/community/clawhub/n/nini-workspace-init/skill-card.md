## Description:

Use this skill to initialize or update a multi-repo workspace created from dev-config-template, including workspace cloning, CLAUDE.md customization, sub-repository setup, development environment configuration, and template synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn a dev-config-template workspace into a working multi-repo development environment. It collects project details, writes workspace configuration files, clones repositories, initializes OpenSpec, configures Python or TypeScript environments, installs available pre-commit hooks, and validates the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad workspace changes, including generating agent-facing files and workspace configuration.

Mitigation: Review the planned repository list, generated CLAUDE.md content, OpenSpec configuration, and template-update diff before allowing execution.

Risk: The skill can clone user-provided repositories and run package installation steps that may execute code from those repositories.

Mitigation: Use trusted repository URLs only, inspect dependency install steps, and avoid accepting free-form repository values supplied by an untrusted party.

Risk: The skill may install persistent pre-commit hooks in cloned repositories.

Mitigation: Review hook configuration before installation and disable or remove hooks that are not required for the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niracler/skills/nini-workspace-init)
- [dev-config-template](https://github.com/niracler/dev-config-template)
- [CLAUDE.md Placeholder Fields](references/claude-md-fields.md)
- [OpenSpec OPSX Configuration Template](references/config-template.yaml)
- [Release v0.3.0](https://github.com/niracler/skill/releases/tag/v0.3.0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, JSON snippets, YAML configuration, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace setup instructions and may create or update repos.json, CLAUDE.md, openspec/config.yaml, VSCode workspace files, .workspace-init-version, virtual environments, node_modules, and pre-commit hooks.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
