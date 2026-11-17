## Description:

Plane.so: Create, update, and manage issues, projects, states, labels, and pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzakirov](https://clawhub.ai/user/jzakirov)

### License/Terms of Use:


## Use Case:

Developers and project teams use this skill to manage Plane.so workspaces from an agent through the Plane CLI, including issue, project, state, label, page, and comment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Plane API key can authorize project-management changes in the connected workspace.

Mitigation: Use a least-privilege Plane API key and keep PLANE_API_KEY out of shared logs, prompts, and committed configuration.

Risk: Deleting Plane resources is destructive.

Mitigation: Confirm destructive delete actions with the user before execution and require explicit --yes only after confirmation.

Risk: Piped stdin such as git diffs may include sensitive or unintended content before being posted to Plane comments.

Mitigation: Review stdin content before submitting it to Plane, especially when using --body -.

Risk: An unreviewed plane-cli package source could introduce unexpected behavior.

Mitigation: Verify the package source before installing and consider pinning a reviewed plane-cli version.

## Reference(s):

- [Plane.so](https://plane.so)
- [Plane CLI Skill Page](https://clawhub.ai/jzakirov/skills/plane-cli-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends JSON output for scripting and stderr JSON for errors; destructive delete commands require explicit confirmation.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
