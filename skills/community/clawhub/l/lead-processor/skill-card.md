## Description:

Automates B2B lead cleaning and classification by analyzing client websites, grading leads A/B/C, updating Feishu tables, and sending reports to Feishu groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clonbrowser](https://clawhub.ai/user/clonbrowser)

### License/Terms of Use:


## Use Case:

Sales and operations teams use this skill to process B2B lead records, classify companies by fit, write structured lead fields, and send follow-up reports through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports live-looking Feishu credentials in the release.

Mitigation: Rotate the exposed app secret, remove embedded credentials, and require environment or secret-manager configuration before installing.

Risk: The security scan reports automatic writes to a specific Feishu table and group chat.

Mitigation: Verify the Bitable and chat IDs and add an explicit confirmation step before records are updated or reports are posted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clonbrowser/skills/lead-processor)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Structured lead classifications, mapped table fields, and Feishu text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu tenant, Bitable, and chat configuration before use.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
