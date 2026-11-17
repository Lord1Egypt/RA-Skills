## Description:

QQ Music (y.qq.com). Use this skill for any QQ Music request involving searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using QQ Music through an OOMOL-connected account can search music and read charts, playlists, radio recommendations, and listening reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run an unverified remote installer with insufficient user control; the hosted connector implementation is also unverified, and it mediates access to a connected QQ Music account and personal music data.

Mitigation: Review and install the oo CLI separately from a verified release where available, check its automatic skill installation and synchronization settings, and review the account access before connecting QQ Music.

## Reference(s):

- [QQ Music](https://y.qq.com/)
- [QQ Music API documentation](https://github.com/tencentmusic/qqmusic-skills)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [OOMOL QQ Music connection](https://console.oomol.com/connections/qqmusic)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [JSON connector responses and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only music search, chart, playlist, radio, recommendation, and listening-report data.]

## Skill Version(s):

1.0.2 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
