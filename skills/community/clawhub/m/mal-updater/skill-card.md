## Description:

Multi-provider anime to MyAnimeList sync and recommendations skill with guarded auth, review-queue triage, health checks, bootstrap auditing, and user-systemd daemon support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklouzal](https://clawhub.ai/user/kklouzal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to install, audit, operate, and troubleshoot conservative anime sync from Crunchyroll and HIDIVE into MyAnimeList. It also guides review-queue triage, recommendations, health checks, and optional unattended maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived MAL, Crunchyroll, and HIDIVE credentials and tokens.

Mitigation: Keep secrets in the configured external secrets directory, use restrictive local permissions, and do not commit real credentials.

Risk: Optional unattended operation can sync on the user's behalf.

Mitigation: Review service behavior before enabling the daemon and prefer read-only checks and dry runs before live apply commands.

Risk: Untrusted profile names or unreviewed maintenance commands can broaden local operational impact.

Mitigation: Use default profile names, avoid passing untrusted profile values, and keep auto-remediation disabled unless the exact commands have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kklouzal/skills/mal-updater)
- [Project homepage](https://github.com/kklouzal/mal-updater)
- [Bootstrap flow](references/bootstrap-onboarding.md)
- [Command cookbook](references/cli-recipes.md)
- [Operations](references/OPERATIONS.md)
- [Automation](references/AUTOMATION.md)
- [MAL OAuth details](references/MAL_OAUTH.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only status summaries, bootstrap checklists, review-queue triage, guarded sync commands, and configuration guidance.]

## Skill Version(s):

0.1.6 (source: server release evidence; artifact pyproject.toml reports 0.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
