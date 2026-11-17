## Description:

Lists Huawei Cloud ECS instances for a selected Region and returns a compact name and ID summary for cloud inventory, operations checks, and automation preflight work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangaiwu](https://clawhub.ai/user/yangaiwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and SREs use this skill to run a read-only Huawei Cloud ECS inventory query for one Region before audits, operational checks, or automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Huawei Cloud AK/SK credentials are stored in a local plaintext config.json file managed by the user.

Mitigation: Use a dedicated read-only credential, restrict config.json permissions to the owner, avoid sharing or archiving the skill directory with config.json, and rotate the credential if exposure is suspected.

Risk: The skill makes authenticated calls to Huawei Cloud ECS and, when project_id is omitted, IAM project-list APIs.

Mitigation: Grant only ecs:cloudServers:list and, if automatic project resolution is needed, iam:projects:listProjects; provide project_id directly when IAM listing is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangaiwu/skills/huaweicloud-ecs-list)
- [IAM permissions statement](artifact/iam-policies.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text terminal output with Markdown documentation and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ECS instance names and IDs for one Huawei Cloud Region; exits with status 0 for success or no instances and status 1 for configuration, authentication, network, or API errors.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
