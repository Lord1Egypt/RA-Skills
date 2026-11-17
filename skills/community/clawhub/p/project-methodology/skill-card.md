## Description:

Complete project lifecycle methodology for Hermes Agent sessions, covering warmup, planning, build work, recaps, wrapup, context loading, handoff verification, and project scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelvillar1](https://clawhub.ai/user/adelvillar1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to run a repeatable agent session lifecycle: load project context, plan non-trivial work, implement against acceptance criteria, draft recaps, and verify handoff state before ending a session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may inspect or index files beyond the current project and invoke an existing local Hermes indexer.

Mitigation: Restrict discovery and indexing to the current repository unless the user explicitly approves named additional directories and the local indexer command.

Risk: The workflow includes paths that can involve local environment files, direct database checks, API calls, or production operations.

Mitigation: Require explicit approval in the current turn before reading CLAUDE.local.md, querying databases or APIs, using production systems, or running destructive operations.

Risk: The workflow can write recap and plan files and update project memory or plan frontmatter.

Mitigation: Review generated Markdown and frontmatter changes before accepting them, and do not auto-commit generated files.

## Reference(s):

- [Project Scaffold Reference](references/project-scaffold.md)
- [Stale Data Verification](references/stale-data-verification.md)
- [Project Methodology on ClawHub](https://clawhub.ai/adelvillar1/skills/project-methodology)
- [Publisher GitHub Homepage](https://github.com/adelvillar1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project memory, plan, and recap Markdown files when the user approves file writes.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
