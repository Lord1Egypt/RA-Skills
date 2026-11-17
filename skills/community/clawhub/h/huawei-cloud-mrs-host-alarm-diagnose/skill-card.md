## Description:

Huawei Cloud MRS cluster alarm diagnosis skill. Analyzes the root cause of an MRS alarm based on user-provided alarm information (alarm ID, alarm name, alarm details, occurrence time, node IP, related service and logs), then outputs the root cause, repair steps, and verification method.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MRS operators use the skill to investigate a cluster alarm from its ID and event details, review likely causes, and obtain diagnostic and verification guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure and TLS handling weaknesses may affect access to the LakeWatch or MRS Manager APIs.

Mitigation: Review credential storage and TLS settings, keep secrets out of conversation and command output, and protect cached tokens.

Risk: An API account with broad permissions could expose or affect more cluster information than diagnosis requires.

Mitigation: Use a dedicated account with read-only access and only the permissions needed for alarm, host, instance, and log queries.

Risk: Suggested repair steps may include disruptive deletion, firewall, service, or configuration changes.

Mitigation: Have a responsible operator independently review each proposed change and obtain user confirmation before applying it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-mrs-host-alarm-diagnose)
- [IAM Policies](references/iam-policies.md)
- [LakeWatch API Client](references/lakewatch-api-client.md)
- [MRS Manager API Client](references/manager-api-client.md)
- [Verification Method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown diagnosis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes alarm context, likely root cause, suggested repair steps, and verification guidance; repair actions are for review and require user confirmation.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
