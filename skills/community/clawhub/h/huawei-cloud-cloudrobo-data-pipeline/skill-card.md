## Description:

Guides users in designing and running CloudRobo sim/teleop data pipelines, drafting pipeline configurations, and monitoring their tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

CloudRobo developers and data engineers use this skill to create or revise sim/teleop data processing workflows, prepare pipeline configuration, and track task progress and outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a mismatch between the CLI-only submission description and the web monitor's ability to submit cloud tasks.

Mitigation: Review the submission path and required permissions before using the monitor; use the documented CLI flow when CLI-only submission is required.

Risk: Disabling SSL verification weakens protection for cloud API connections.

Mitigation: Keep SSL verification enabled in production; disable it only temporarily for debugging in a trusted environment.

Risk: The security analysis inspected only part of the artifact, so it does not establish that unreviewed components are safe.

Mitigation: Review the remaining components and assess the skill before installation or use with production credentials.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-data-pipeline)
- [Custom pipeline authoring](references/custom-pipeline-authoring.md)
- [Web monitor guide](references/web-monitor.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [IAM policies and security notes](references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown guidance, YAML pipeline configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validated pipeline drafts, execution summaries, and monitoring guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter says 2.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
