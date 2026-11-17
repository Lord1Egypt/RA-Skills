## Description:

Operate Simple Analytics to read website statistics and export or send analytics data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can list connected websites, inspect aggregated statistics, export datapoints, and send events or pageviews to Simple Analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs a downloaded CLI installer whose remote contents have not been verified.

Mitigation: Review and approve the installer and the CLI's skill-installation behavior before allowing setup to proceed.

Risk: Connecting Simple Analytics authorizes OOMOL to mediate access to the account.

Mitigation: Review the account connection and grant access only for the intended Simple Analytics account.

Risk: Exporting datapoints or sending events changes or transmits analytics data.

Mitigation: Keep the skill's confirmation requirement and confirm the exact payload and effect before each write action.

## Reference(s):

- [Simple Analytics API authentication documentation](https://docs.simpleanalytics.com/api/authenticate)
- [Simple Analytics](https://simpleanalytics.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-simple-analytics)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Guidance]

**Output Format:** [Analytics data returned as JSON and summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available output depends on the selected analytics action; write actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
