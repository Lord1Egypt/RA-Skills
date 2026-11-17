## Description:

Guides users in designing, validating, executing, and monitoring CloudRobo data pipelines, with optional sim and teleoperation data processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

CloudRobo users and data engineers use this skill to turn natural-language requirements or existing pipeline definitions into validated drafts, then run or monitor selected data processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may grant access beyond the intended workspace or storage paths.

Mitigation: Use credentials limited to the intended workspace and storage paths.

Risk: Execution or Web retries can affect selected data, operators, resources, and costs; stopping monitoring or orchestration does not stop existing cloud jobs.

Mitigation: Review the selected data, operators, resources, and costs before confirming execution or a retry, and track or stop cloud jobs separately when needed.

Risk: Disabling TLS verification weakens the security of cloud connections.

Mitigation: Keep TLS verification enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-data-pipeline)
- [CloudRobo user guide](artifact/references/user-guide.md)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [IAM policies and access guidance](artifact/references/iam-policies.md)
- [Pipeline templates and quick reference](artifact/references/pipeline-templates.md)
- [Custom pipeline authoring](artifact/references/custom-pipeline-authoring.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Markdown, JSON, Shell commands]

**Output Format:** [Markdown guidance, YAML pipeline files, JSON drafts, and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pipeline.yaml, pipeline.draft.json, and a Markdown preview; local draft validation does not confirm live operator availability.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
