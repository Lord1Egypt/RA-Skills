## Description:

Komari (github.com). Use this skill for ANY Komari request — reading, creating, updating, and deleting data. Whenever a task involves Komari, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers use Komari through an OOMOL-connected account to inspect monitoring data and manage clients, alerts, settings, sessions, and remote execution tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses a remotely hosted CLI installer that was unavailable for inspection, and the CLI may synchronize agent skills at startup.

Mitigation: Review the CLI and installer before use; disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1 if appropriate.

Risk: Komari actions can expose secrets, change configuration, delete data, or run commands on selected clients.

Mitigation: Use limited Komari permissions, confirm exact targets and effects before approving changes or remote commands, and protect secret-bearing results.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Komari API documentation](https://komari-document.pages.dev/en/dev/api)
- [Komari project](https://github.com/komari-monitor/komari)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs depend on the live Komari action schema; inspect it before preparing a request.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
