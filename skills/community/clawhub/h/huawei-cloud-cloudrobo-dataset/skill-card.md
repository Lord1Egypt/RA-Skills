## Description:

Manage Huawei Cloud CloudRobo processing and evaluation tasks, troubleshoot results, onboard custom operators, and prepare LeRobot manifests from ROS 2 bags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

CloudRobo developers and data engineers use this skill to manage processing and chained evaluation tasks, inspect logs and outputs, coordinate task pipelines, and onboard custom operators. Robotics dataset teams can also prepare LeRobot manifests from local ROS 2 bags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be exposed in diagnostics or full login commands.

Mitigation: Use narrowly scoped cloud credentials, an isolated build host, and avoid sharing complete login commands.

Risk: Cleanup instructions may affect resources outside the current run.

Mitigation: Restrict cleanup to artifacts created by the current run.

Risk: Conflicting Mode B push instructions can lead to an incorrect delivery workflow.

Mitigation: Resolve the conflicting instructions before carrying out a push.

Risk: Remote recording access can expose a local web workbench.

Mitigation: Use the loopback web launcher and verified TLS.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-dataset)
- [CloudRobo interactive workflow](references/interactive-workflow.md)
- [Custom operator workflow](references/custom-operator/custom-operator-workflow.md)
- [Custom operator reference](references/custom-operator/custom-operator-reference.md)
- [Bag to manifest guide](references/bag2manifest.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [IAM policies](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Huawei Cloud API Explorer](https://console.huaweicloud.com/apiexplorer/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON and YAML configurations, and generated LeRobot manifest.yaml files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task status and logs, output previews, temporary links, manifests, and operator setup files.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
