## Description:

Collects public Kuaishou video engagement metrics in batches and exports the results as CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use the skill to measure public Kuaishou video engagement for campaign reporting, activity monitoring, and content analysis. It accepts batches of video links and can export collected metrics as CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default service address uses HTTP, which can expose credentials during transmission.

Mitigation: Configure a valid HTTPS service address and verify its certificate before authenticating or sending a token.

Risk: The client can automatically migrate a saved credential from a legacy configuration file.

Mitigation: Use a dedicated XHS_CONFIG_PATH and review the configuration and token source before running authenticated commands.

Risk: The security review reports capabilities beyond the stated Kuaishou metrics purpose, and its scan covered only part of the release.

Mitigation: Review the complete release before deployment and limit use to the documented Kuaishou metric workflow and public video links.

## Reference(s):

- [Ks-Collect on ClawHub](https://clawhub.ai/mystery77777777/skills/ks-collect)
- [Publisher profile](https://clawhub.ai/user/mystery77777777)

## Skill Output:

**Output Type(s):** [JSON, CSV files, Shell commands]

**Output Format:** [JSON command responses and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch results cover up to 50 video links; CSV exports contain collected video metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
