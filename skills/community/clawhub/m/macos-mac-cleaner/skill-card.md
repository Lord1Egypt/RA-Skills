## Description:

Mac Cleaner installs a local macOS cleanup agent that removes selected caches, logs, Trash items, npm/Homebrew cache, and stale build artifacts, with a Mission Control dashboard and optional weekly scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephtandle](https://clawhub.ai/user/josephtandle)

### License/Terms of Use:

MIT-0

## Use Case:

External macOS users and developers use this skill to install and operate a local disk-cleanup agent for freeing storage and reviewing cleanup results in Mission Control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the documented dry-run preview can delete files immediately.

Mitigation: Do not run the preview or cleanup path until the dry-run behavior is fixed and verified with non-destructive tests.

Risk: The skill adds persistent and manual ways to trigger cleanup through a cron job and dashboard Run Now endpoint.

Mitigation: Keep scheduling disabled unless explicitly approved, and review authentication, authorization, and operator confirmation before enabling dashboard-triggered cleanup.

Risk: Cleanup removes filesystem content from cache, log, Trash, npm, Homebrew, and build-artifact locations.

Mitigation: Review the exact target paths before use, preserve the explicit path allowlist and symlink checks, and keep backups for data that should not be deleted.

## Reference(s):

- [Mac Cleaner on ClawHub](https://clawhub.ai/josephtandle/skills/macos-mac-cleaner)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash, JavaScript, TypeScript, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local cleanup scripts and configuration that run with the current user's macOS permissions.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
