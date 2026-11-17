## Description:

Use when the operator asks to merge configured transit notes into domain wiki pages with source metadata, index updates, status transitions, and audit checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arroncn993-sys](https://clawhub.ai/user/arroncn993-sys)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and developers use this skill to merge compiled Markdown transit notes into a configured local wiki, update source metadata and indexes, move completed notes, and audit consistency before treating an entry run as complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts permit broad local file writes and moves during wiki maintenance.

Mitigation: Install only in a high-trust local vault, keep the vault under version control or backups, and run the skill with the least filesystem privileges needed for the configured vault.

Risk: Checkpoint auditing can execute raw shell commands through the audit command path.

Mitigation: Restrict or patch raw audit command execution before broader use, and allow only reviewed audit commands in trusted workspaces.

Risk: Absolute paths or parent-directory path segments could write outside the intended vault boundary.

Mitigation: Reject absolute and parent-directory paths and canonicalize every target path under the configured vault before execution.

Risk: Note content and wikilinks can influence generated wiki output and link synchronization.

Mitigation: Treat note content and wikilinks as untrusted input, review proposed edits, and require the final audit to pass before marking work complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arroncn993-sys/skills/openclaw-wiki-entry-skill)
- [Workflow](references/workflow.md)
- [Path Decision](references/path-decision.md)
- [Self-Check Checklist](references/self-check-checklist.md)
- [Error Playbook](references/error-playbook.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs local file edits and audit steps for Markdown wiki maintenance.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
