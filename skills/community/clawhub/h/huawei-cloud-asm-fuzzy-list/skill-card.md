## Description:

Queries Huawei Cloud ASM meshes for the current tenant or project, then returns mesh names, IDs, status phases, and creation timestamps for all meshes or for meshes whose names match a case-insensitive keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erickeyhu-hug](https://clawhub.ai/user/erickeyhu-hug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inventory Huawei Cloud ASM meshes, locate meshes by fuzzy name match, and support routine inspection or troubleshooting without modifying ASM resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires credentials that can list Huawei Cloud ASM mesh metadata for the selected project and region.

Mitigation: Grant only read-only mesh list access such as asm:mesh:list, keep AK/SK values in environment variables, and avoid pasting credentials into prompts or files.

Risk: Mesh names, IDs, phases, and creation timestamps may reveal infrastructure metadata.

Mitigation: Run the skill only in environments where returning ASM mesh inventory for the selected tenant or project is acceptable.

Risk: The ASM list API has no server-side name filter, so fuzzy matching lists all meshes before filtering locally.

Mitigation: Use the skill only for read-only inventory workflows and review outputs before sharing them outside the authorized operations context.

## Reference(s):

- [IAM Policies](references/iam-policies.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Verification Method](references/verification-method.md)
- [Dataflow Diagram](references/dataflow-diagram.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Huawei Cloud ASM cn-north-4 Endpoint](https://asm.cn-north-4.myhuaweicloud.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline Python and shell command examples; query results are plain text rows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result rows include mesh name, mesh ID, status phase, and creation timestamp; fuzzy searches may also report matched count.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
