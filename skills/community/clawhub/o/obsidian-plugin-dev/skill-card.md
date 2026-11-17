## Description:

Create and develop Obsidian plugins from scratch. Use when building a new Obsidian plugin, scaffolding from the sample-plugin-plus template, or developing plugin features. Covers project setup, manifest configuration, TypeScript development, settings UI, commands, ribbons, modals, and Obsidian API patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidvkimball](https://clawhub.ai/user/davidvkimball)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scaffold, configure, build, test, and release Obsidian plugins. It provides guidance for TypeScript plugin architecture, settings UI, commands, ribbon icons, modals, lifecycle events, file operations, and editor manipulation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to use an unpinned third-party template repository and run setup commands from that checkout.

Mitigation: Review the template repository, package scripts, lockfile, and setup scripts before execution; prefer a pinned commit or trusted fork in a constrained development environment.

Risk: The skill includes steps that can create public GitHub repositories or publish releases.

Mitigation: Require explicit user approval before GitHub repository creation, commits, pushes, release creation, or public publishing.

## Reference(s):

- [Settings UI Pattern](references/settings.md)
- [Common Obsidian Plugin Patterns](references/patterns.md)
- [obsidian-sample-plugin-plus template](https://github.com/davidvkimball/obsidian-sample-plugin-plus)
- [Obsidian API Docs](https://docs.obsidian.md)
- [Hot Reload plugin](https://github.com/pjeby/hot-reload)
- [Lucide icons](https://lucide.dev/icons/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, JSON, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local development commands and release steps that require explicit user approval before publishing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
