## Description:

Migrate a user's OpenClaw customization footprint into Hermes Agent, including compatible memories, SOUL.md, command allowlists, user skills, selected workspace assets, and a report of items that could not be migrated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agungprabowo123](https://clawhub.ai/user/agungprabowo123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate an OpenClaw setup into Hermes Agent with dry-run previews, conflict handling, and a structured migration report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration can copy sensitive tokens or environment values in ways broader than the user-facing instructions imply.

Mitigation: Run a dry run first, avoid modes that copy tokens unless explicitly acceptable, and protect the target Hermes .env with owner-only permissions.

Risk: Imported command allowlist entries can persist broad execution permissions.

Mitigation: Inspect command allowlist entries before importing them and remove entries that are not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agungprabowo123/skills/openclaw-migration-2)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, text]

**Output Format:** [Markdown with inline shell commands and structured migration summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide file migration, configuration updates, conflict choices, dry-run review, and post-run reporting.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
