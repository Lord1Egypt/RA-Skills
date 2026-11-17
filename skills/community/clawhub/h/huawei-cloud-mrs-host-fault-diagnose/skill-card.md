## Description:

Diagnoses Huawei Cloud MRS cluster service, instance, and host faults using LakeWatch or MRS Manager APIs plus bundled knowledge-base workflows to localize root causes and propose repair guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to triage unhealthy Huawei Cloud MRS services, instances, or hosts when they have a cluster ID and optional service or node details. The skill guides read-oriented diagnosis and produces a fault report with root cause localization and repair suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manager API definitions can change cluster or user state despite the skill's stated read-only posture.

Mitigation: Before installation, remove or block Manager API definitions that mutate users, alarms, commands, or cluster state unless administrative control is intended and separately confirmed.

Risk: Risky TLS defaults can expose credentials or cluster data if used outside a trusted environment.

Mitigation: Set verify_ssl to true and configure a trusted CA before entering LakeWatch or MRS Manager credentials.

Risk: Credentialed API access can exceed the diagnostic purpose if broad accounts are used.

Mitigation: Use a least-privilege read-only Manager or LakeWatch account for diagnosis.

## Reference(s):

- [CLI Installation Guide - MRS Fault Diagnosis](references/cli-installation-guide.md)
- [Fault Diagnosis Workflow Design](references/fault-diagnosis-workflow.md)
- [IAM Policies - MRS Fault Diagnosis](references/iam-policies.md)
- [LakeWatch API Client](references/lakewatch-api-client.md)
- [MRS Manager API Client](references/manager-api-client.md)
- [Related Commands - MRS Fault Diagnosis](references/related-commands.md)
- [Verification Method - MRS Fault Diagnosis](references/verification-method.md)
- [Acceptance Criteria - MRS Fault Diagnosis](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnosis report with command excerpts and repair suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes fault metadata, diagnosis process, propagation path, root cause, and repair suggestions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
