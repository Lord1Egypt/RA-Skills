## Description:

A Kimi/OpenClaw adaptation bundle of six Matt Pocock developer workflow skills for requirement alignment, codebase-aware planning, handoffs, test-driven development, bug diagnosis, and PRD creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolingrabbit](https://clawhub.ai/user/coolingrabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this meta-skill to install and invoke structured software-development workflows in Kimi Work or OpenClaw. It helps agents align requirements, maintain project context, write handoff notes, drive TDD loops, diagnose bugs, and convert aligned conversations into PRDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic triggers can change future agent behavior by adding multiple auto-invoked developer workflow skills.

Mitigation: Review the bundle before installing and prefer explicit invocation or clear user confirmation for sensitive workflows.

Risk: The bundled skills may read repositories and create persistent workspace documents such as context files, ADRs, handoff summaries, PRDs, tests, or implementation changes.

Mitigation: Require confirmation before file writes, review generated files before committing, and keep repository access scoped to the active workspace.

Risk: PRD publishing workflows can configure issue tracking or create GitHub issues when external access is available.

Mitigation: Confirm issue-tracker configuration and destination before publishing, and use local Markdown fallback when external publishing is not intended.

Risk: Unpinned installer commands can install changing upstream content.

Mitigation: Avoid the unpinned npx install path unless the installer source is trusted; prefer a reviewed release artifact or pinned source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolingrabbit/skills/mattpocock-skills-kimi)
- [README](README.md)
- [Adaptation Notes](docs/ADAPTATION-NOTES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, inline code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace documentation, handoff files, issue-tracker configuration, PRD markdown, tests, and implementation code when the active agent has appropriate tool access.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
