## Description:

Guides an agent through a six-phase process for creating, researching, testing, and validating Huawei Cloud skills using CLI, SDK, or REST API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use it to gather requirements, research Huawei Cloud interfaces, and create and verify task-specific skill packages for cloud workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates this release suspicious with high confidence, citing live cloud changes, automatic telemetry, and capabilities beyond the described skill-generation purpose; only 11 of 13 components were fully inspected.

Mitigation: Review the scripts and scanner report before installation, use least-privilege credentials for cloud testing, and set SKILL_QUALITY_REPORT=0 if telemetry is unwanted.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-skill-creator)
- [Huawei Cloud KooCLI installation](https://support.huaweicloud.com/cli/index.html)
- [Huawei Cloud API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi)
- [Huawei Cloud SDK Center](https://console.huaweicloud.com/apiexplorer/#/sdkcenter)
- [Acceptance criteria](references/acceptance-criteria.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [Verification method](references/verification-method.md)
- [IAM policies](references/iam-policies.md)
- [Data flow diagram](references/dataflow-diagram.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration]

**Output Format:** [A skill directory with Markdown guidance, scripts, JSON templates, and CLI, SDK, or REST API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a required sequential six-phase workflow and generates phase summaries during skill creation.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
