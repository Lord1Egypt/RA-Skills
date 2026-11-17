## Description:

WakaTime (wakatime.com). Use this skill for ANY WakaTime request — searching and reading data. Whenever a task involves WakaTime, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other WakaTime users can retrieve their account profile, coding statistics, daily summaries, project list, and current status through an agent. The agent can use these results to answer questions about the user's tracked coding activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified installer code or add persistent bundled agent skills.

Mitigation: Review and approve CLI installation separately, verify the selected release, and decide whether to disable automatic bundled-skill synchronization.

Risk: Connecting WakaTime involves trusting OOMOL with the connection and account-data processing.

Mitigation: Connect only if OOMOL's handling of WakaTime account data is acceptable, and review the connection and requested access.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [WakaTime API documentation](https://wakatime.com/developers)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Text]

**Output Format:** [JSON data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected WakaTime account and available account data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
