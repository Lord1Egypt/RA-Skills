## Description:

Manage and navigate a multi-layered, branch-based memory system that organizes agent context into Root, Domain, and Project layers to reduce context bloat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balkanblbn](https://clawhub.ai/user/balkanblbn)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to structure long-lived workspace memory into root, domain, and project markdown files so agents can recall only the context needed for a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can overwrite or append to files outside the intended memory folders.

Mitigation: Before use, restrict branch names, reject traversal and absolute paths, resolve paths with containment checks, and constrain parent files to the memory/domain hierarchy.

Risk: Creating a memory branch can replace an existing markdown file without confirmation.

Mitigation: Change the helper script to refuse existing target files by default or require an explicit overwrite flag.

## Reference(s):

- [Hierarchical Memory on ClawHub](https://clawhub.ai/balkanblbn/skills/hierarchical-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and local markdown memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can create or append local markdown files for memory branches.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
