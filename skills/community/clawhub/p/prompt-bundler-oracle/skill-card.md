## Description:

Best practices for using the oracle CLI (prompt + file bundling, engines, sessions, and file attachment patterns).

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose effective oracle CLI workflows for bundling prompts and repository files, previewing token usage, selecting browser or API engines, and resuming long-running sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running the oracle CLI through an unpinned npm package can introduce supply-chain risk.

Mitigation: Verify the @steipete/oracle package source before installation and pin a reviewed package version where possible.

Risk: Attached files may include secrets or unnecessary sensitive project context.

Mitigation: Use dry-run and files-report first, attach only required files, and redact secrets such as .env files, keys, and tokens.

Risk: Browser sessions and oracle run history may persist locally after use.

Mitigation: Review stored sessions under ~/.oracle/sessions or the configured ORACLE_HOME_DIR and remove sensitive sessions when no longer needed.

Risk: Oracle responses are advisory and may contain incorrect or misleading guidance.

Mitigation: Verify recommendations against the codebase and run appropriate tests before applying changes.

## Reference(s):

- [Oracle homepage](https://askoracle.dev)
- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/prompt-bundler-oracle)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advises dry-run previews, targeted file attachment, session reattachment, and credential redaction before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
