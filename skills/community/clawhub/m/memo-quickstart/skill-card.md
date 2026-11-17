## Description:

记忆快速启动 helps agents initialize and operate a local memory workflow using session state, JSON memory storage, markdown archives, and CLI-based retrieval commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add local memory routines to ClawHub-compatible coding or assistant workflows. It provides setup steps, storage conventions, retrieval commands, and maintenance guidance for session state and long-term memory records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent storage of conversation details in local memory files.

Mitigation: Avoid storing secrets, regulated data, or sensitive personal information, and review memory files as persistent records before using the skill in private or business-sensitive workspaces.

Risk: The artifact gives inconsistent guidance about local-only behavior, callback URLs, and optional Gist-style cloud sync.

Mitigation: Keep callback and cloud-sync features disabled unless external transmission is explicitly acceptable for the workspace.

Risk: The workflow requires installing and running the external npm package simple-local-memory.

Mitigation: Verify the package source, version, and install command before global installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memo-quickstart)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local file conventions for SESSION-STATE.json, MEMORY.md, and memories/.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
