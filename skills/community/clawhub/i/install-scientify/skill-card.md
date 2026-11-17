## Description:

Use this when the user wants to install or set up the Scientify research plugin. Adds research-pipeline, literature-survey, idea-generation, arxiv tools, and workspace management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[springleave](https://clawhub.ai/user/springleave)

### License/Terms of Use:


## Use Case:

External users and developers use Scientify to install a research workflow automation plugin for literature surveys, research planning, implementation, experiment tracking, workspace management, and review-paper drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs installation of an unpinned external package.

Mitigation: Use an install flow that displays the resolved package version, publisher, and integrity information before installation.

Risk: The artifact asks the agent to install without asking permission.

Mitigation: Require explicit user approval before installing the plugin.

Risk: The plugin may download research materials, manage local workspaces, generate and run code, and delete projects.

Mitigation: Run it in a dedicated workspace, review permissions before use, and keep backups of research projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/springleave/skills/install-scientify)
- [scientify npm package](https://www.npmjs.com/package/scientify)
- [scientify GitHub repository](https://github.com/tsingyuai/scientify)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install a third-party OpenClaw plugin that adds research skills, commands, and tools.]

## Skill Version(s):

1.7.3 (source: server release metadata, created 2026-02-23T10:20:29Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
