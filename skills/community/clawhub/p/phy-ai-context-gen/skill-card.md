## Description:

Analyzes a codebase to generate precise, project-specific AI coding assistant context files for Claude, OpenClaw, Cursor, Windsurf, and GitHub Copilot tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a repository and generate assistant instruction files based on detected tech stack, architecture, conventions, and testing setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated context files may include secret values or private internal details discovered during repository scanning.

Mitigation: Review generated files before committing or reusing them, and remove secrets or private details.

Risk: Generated agent instructions may include overly broad repository access or command permissions.

Mitigation: Narrow permissions to the project's actual workflow before sharing or deploying the files.

Risk: Undetected project facts can lead to incomplete TODO sections or inaccurate assistant guidance.

Mitigation: Resolve generated TODOs and confirm commands, tools, and conventions before relying on the files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-ai-context-gen)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and plain-text rule files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates CLAUDE.md, AGENTS.md, .cursorrules, .windsurfrules, and .github/copilot-instructions.md after repository inspection and user confirmation.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
