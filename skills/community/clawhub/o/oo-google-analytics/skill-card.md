## Description:

Google Analytics (analytics.google.com). Use this skill for ANY Google Analytics request — reading, creating, updating, and deleting data. Whenever a task involves Google Analytics, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts can use the skill to inspect Google Analytics accounts, properties, reports, metadata, and quotas, and to manage selected property settings or custom dimensions and metrics. Confirm the exact effect before actions that change or delete Analytics data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing-tool setup can execute downloaded CLI software without a separate approval step.

Mitigation: Review and approve CLI installation separately, preferably using a verified release.

Risk: The CLI can automatically synchronize agent skills.

Mitigation: Review the oo CLI command reference for the synchronization opt-out and disable automatic synchronization if it is not intended.

Risk: Analytics actions can expose account data or change or delete property configuration.

Mitigation: Connect only the intended Analytics account and retain confirmation before changes or deletions.

## Reference(s):

- [Google Analytics](https://analytics.google.com)
- [Google Analytics Data API documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-google-analytics)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Configuration instructions]

**Output Format:** [JSON connector responses with natural-language summaries and instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change Analytics state require confirmation; destructive actions require explicit approval.]

## Skill Version(s):

1.0.6 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
