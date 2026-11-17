## Description:

Manage Plane.so projects and work items using the `plane` CLI. List projects, create/update/search issues, manage cycles and modules, add comments, and assign members.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honluk](https://clawhub.ai/user/honluk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to operate Plane.so workspaces from an agent through the `plane` CLI, including project lookup, issue creation and updates, assignment, comments, cycles, modules, states, and labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unverified remote executable.

Mitigation: Review the upstream CLI before installation and prefer a pinned release with checksum or signature verification.

Risk: The documented commands can change workspace data, including issue deletion and other broad mutations.

Mitigation: Use a least-privilege Plane token and require explicit confirmation before destructive or broad mutation commands in a production workspace.

## Reference(s):

- [Plane.so](https://plane.so)
- [My Plane GitHub Repository](https://github.com/HonLuk/my-plane)
- [plane CLI Release Download](https://github.com/HonLuk/my-plane/releases/latest/download/plane)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run Plane CLI commands that return formatted tables or JSON when `-f json` is used.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
