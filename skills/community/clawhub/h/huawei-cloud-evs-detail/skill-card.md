## Description:

Read-only skill for querying Huawei Cloud EVS disk lists and monitoring metrics, including IOPS, throughput, and latency, using Huawei Cloud KooCLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect Huawei Cloud EVS volumes in cn-north-4 and retrieve read-only Cloud Eye metrics for a selected disk. It supports inventory review and operational troubleshooting without creating, modifying, or deleting cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal Huawei Cloud disk inventory, attachment, and monitoring metadata.

Mitigation: Use it only for intended EVS lookup workflows and confirm ambiguous EVS requests before running commands.

Risk: Cloud credentials with broad permissions increase impact if misused.

Mitigation: Configure read-only IAM permissions for EVS volume listing and Cloud Eye metric reads, and avoid storing AK/SK values in files, logs, or command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/huawei-cloud-evs-detail)
- [Publisher profile](https://clawhub.ai/user/yangaiwu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and cloud CLI result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Huawei Cloud EVS and Cloud Eye query guidance; output can include cloud infrastructure metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
