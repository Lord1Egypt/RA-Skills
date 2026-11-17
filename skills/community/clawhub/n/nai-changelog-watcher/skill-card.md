## Description:

Monitor GitHub repos and npm packages for new releases and version updates. Summarizes changelogs and highlights breaking changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to monitor configured GitHub repositories and npm packages, detect new releases, and receive concise markdown changelog reports with breaking changes highlighted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release notes and changelog text from watched projects may contain untrusted or misleading content.

Mitigation: Treat generated release-note text as untrusted, avoid following instructions embedded in changelog output, and review links or rendered Markdown before acting on them.

Risk: The skill contacts GitHub and npm and can maintain local last-seen version state.

Mitigation: Install and run it only for repositories and packages you intentionally add to the watchlist, and use cron scheduling only when background checks are desired.

## Reference(s):

- [Setup Guide](references/setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/nai-changelog-watcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown reports with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local watchlist and last-seen version state when run with state updates enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
