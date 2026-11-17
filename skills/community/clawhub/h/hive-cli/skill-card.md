## Description:

Hive CLI helps agents operate Hive task pipelines, inspect current and historical task state, answer waiting brainstorm questions, create project-local workflows, run pre-release QA checks, and diagnose recovery state through Hive's native CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivankuznetsov](https://clawhub.ai/user/ivankuznetsov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Hive-managed work, follow bounded status and watch flows, answer task brainstorm prompts, create local workflow descriptors, run release-candidate QA checks, and diagnose recovery state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route agents toward powerful local workflow tooling with broad execution permissions.

Mitigation: Use read-only inspection where possible, require explicit consent for destructive or administrative actions, and review generated workflows before execution.

Risk: Installation paths and external workflow installs depend on third-party publisher and package sources.

Mitigation: Install only from trusted Hive publisher channels, verify the selected package source, and prefer explicit previews or narrower permissions when workflows do not need unrestricted local execution.

## Reference(s):

- [Hive project homepage](https://github.com/ivankuznetsov/hive)
- [Hive 0.7.3 release notes](https://github.com/ivankuznetsov/hive/releases/tag/v0.7.3)
- [Current format migration guide](https://github.com/ivankuznetsov/hive/blob/main/docs/guides/current-format-migration.md)
- [Daily activity digest](references/daily-digest.md)
- [Status and watch](references/status-and-watch.md)
- [Brainstorm answering](references/brainstorm-answering.md)
- [Natural-language workflow creator](references/workflow-creator.md)
- [Owner-authored workflow schema](references/workflow-schema.md)
- [Workflow actions](references/workflow-actions.md)
- [Recovery](references/recovery.md)
- [Release candidate QA](references/release-candidate-qa.md)
- [Setup and platforms](references/setup-and-platforms.md)
- [Safety](references/safety.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline CLI commands and JSON-oriented inspection routes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve Hive's bounded action and consent boundaries and should not expose credentials.]

## Skill Version(s):

0.1.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
