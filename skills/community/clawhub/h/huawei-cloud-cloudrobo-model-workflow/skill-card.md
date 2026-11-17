## Description:

Orchestrates CloudRobo model asset discovery, training, inference deployment, and real-robot evaluation as a complete or partial workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to prepare model and dataset assets, train models, deploy inference services, and evaluate tasks on a selected real robot. It also supports workflows that start from an intermediate stage when the required outputs are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery guidance recommends repeating cancelled robot tasks without checking that physical conditions remain safe.

Mitigation: After cancellation, stop the workflow until an operator requests a fresh run; before dispatch or retry, confirm the robot has stopped and its work area is safe.

Risk: Dataset uploads and exported robot certificates can expose data or access credentials if handled carelessly.

Mitigation: Verify the dataset directory and upload destination before transfer, preserve approval for cloud writes, and protect cloud keys and exported robot certificates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cloudrobo-model-workflow)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [Fault recovery guide](artifact/references/fault-recovery.md)
- [IAM policies](artifact/references/iam-policies.md)
- [Model extension metadata guide](artifact/references/model-ext-metadata.md)
- [Robot selection guide](artifact/references/robot-selection-guide.md)
- [Workflow constraints](artifact/references/constraints.md)
- [Pipeline templates](artifact/references/pipeline-templates.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown guidance with CloudRobo CLI examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include workflow status summaries and real-robot evaluation results.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
