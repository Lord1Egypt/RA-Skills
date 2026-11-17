## Description:

OpenClaw Memory-OS helps agents capture, store, and search local personal memories, including conversation-derived facts and file-based notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add local memory workflows to an agent, including remembering conversation facts, importing selected files, and searching stored memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist private conversation or file contents as plaintext under ~/.memory-os/.

Mitigation: Do not store secrets or sensitive personal data unless plaintext local storage is acceptable; inspect and delete local JSON memory files as needed.

Risk: The installation guidance includes an open-ended global npm install.

Mitigation: Use an exact audited npm version or a reviewed source checkout before installation.

Risk: Broad collection paths or auto-trigger memory capture can store unintended information.

Mitigation: Use narrow explicit paths, review files before collection, and disable or tightly control auto-trigger memory capture.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/memory-opportunity)
- [Project homepage](https://github.com/ZhenRobotics/openclaw-memory-opportunity)
- [npm package](https://www.npmjs.com/package/openclaw-memory-opportunity)
- [Security details](https://github.com/ZhenRobotics/openclaw-memory-opportunity/blob/main/SECURITY.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Text]

**Output Format:** [Markdown with inline shell commands and TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or inspect local JSON memory files under ~/.memory-os/ when commands are executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
