## Description:

Monitors 50+ bidding platforms for Weinen-focused procurement notices and filters results to power-sector tenders only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powerzzjohn](https://clawhub.ai/user/powerzzjohn)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and procurement users use this skill to monitor public and supplier bidding platforms for power-related tender opportunities and produce concise daily results for follow-up.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Bundled plaintext passwords, sub-account credentials, personal contact details, and an electronic-seal PIN may expose third-party systems and individuals.

Mitigation: Remove secrets and personal data from the package and history, rotate exposed credentials, and require user-supplied secret references before installation or publication.

Risk: Automated monitoring results may be delivered to an unintended WeChat destination or retained locally in result files.

Mitigation: Review the configured delivery destination and local output retention before deployment, and route results only to approved recipients.

## Reference(s):

- [Configuration Guide](references/config-guide.md)
- [GX Websites Configuration](references/gx_websites.json)
- [ClawHub Skill Page](https://clawhub.ai/powerzzjohn/skills/gx-bidding-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON or text result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write daily bidding result JSON and WeChat message text files when executed in its configured workspace.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
