## Description:

Develop, extend, and contribute to Lobster AI, a multi-agent bioinformatics engine for building agents, services, tests, and plugin packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cewinharhar](https://clawhub.ai/user/cewinharhar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to work on Lobster AI code: understand the architecture, scaffold bioinformatics agents and plugins, create services, apply AQUADIF metadata and provenance rules, and validate tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt automatic installation of unpinned Lobster packages, which may pull an unexpected package version or source.

Mitigation: Review the exact Lobster package source and version before installation, and prefer pinned dependencies or a lockfile.

Risk: API keys or long-lived credentials could be exposed if pasted into chat or passed directly on command lines.

Mitigation: Use safer secret handling such as restricted-permission credential files or environment management, and avoid sharing secrets in chat.

Risk: Broad development trigger phrases could activate the skill outside its intended Lobster-specific context.

Mitigation: Use the skill only for Lobster AI development, plugin, service, and validation tasks.

## Reference(s):

- [LobsterBio - Dev release page](https://clawhub.ai/cewinharhar/skills/lobsterbio-dev)
- [Planning Workflow for New Capabilities](references/planning-workflow.md)
- [Scaffold Reference](references/scaffold.md)
- [Creating Agents](references/creating-agents.md)
- [Creating Services](references/creating-services.md)
- [AQUADIF Tool Taxonomy Contract](references/aquadif-contract.md)
- [AQUADIF Migration Guide](references/aquadif-migration.md)
- [Architecture Reference](references/architecture.md)
- [Code Layout](references/code-layout.md)
- [Omics Plugin Architecture](references/plugin-architecture.md)
- [CLI Reference](references/cli.md)
- [Testing Guide](references/testing.md)
- [Domain Knowledge Bridge: GPTomics Bio-Skills](references/bioskills-bridge.md)
- [Omics-OS Component Registry docs](https://docs.omics-os.com/docs/core/component-registry)
- [Omics-OS Architecture docs](https://docs.omics-os.com/docs/architecture/overview)
- [Omics-OS Entry Points docs](https://docs.omics-os.com/docs/extending/entry-points)
- [Omics-OS Plugin Contract docs](https://docs.omics-os.com/docs/extending/plugin-contract)
- [GPTomics BioSkills repository](https://github.com/GPTomics/bioSkills)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code snippets, shell commands, validation checklists, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for Lobster-specific development workflows and may include local install, scaffold, test, and validation steps.]

## Skill Version(s):

1.1.402 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
