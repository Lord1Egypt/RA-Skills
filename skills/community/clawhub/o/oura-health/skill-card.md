## Description:

Query Oura Ring sleep, readiness, activity, heart rate, trends, and health alerts via the Oura API v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis563](https://clawhub.ai/user/jarvis563)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Oura accounts use this skill to let an agent retrieve and summarize personal sleep, readiness, activity, heart-rate, and trend data. It can also run a local alert checker for notable health signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The credentials file can configure a non-Oura base_url, which could send the Oura bearer token and health/profile requests to an unintended service.

Mitigation: Keep base_url set to https://api.ouraring.com/v2 or hard-code it before scheduled use; rotate the token if the credentials file or output is exposed.

Risk: The skill reads sensitive personal, sleep, readiness, activity, heart-rate, and profile data from Oura.

Mitigation: Install only where that local data access is acceptable, keep ~/.config/oura/credentials.json private with restrictive permissions, and avoid sharing command output externally.

## Reference(s):

- [Oura API v2](https://api.ouraring.com/v2)
- [Oura Personal Access Tokens](https://cloud.ouraring.com/personal-access-tokens)
- [ClawHub Skill Page](https://clawhub.ai/jarvis563/skills/oura-health)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Human-readable text and Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local credentials at ~/.config/oura/credentials.json and prints one-line alerts when notable health thresholds are met.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
