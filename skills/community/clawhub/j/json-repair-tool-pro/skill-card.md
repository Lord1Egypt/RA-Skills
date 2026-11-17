## Description:

JSON修复工具专业版 helps agents repair JSON files in bulk, stream large files, apply custom rules, preview diffs, and manage incremental repair and rollback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, DevOps engineers, and operations teams use this skill to repair malformed JSON across directories, large logs, migration datasets, and CI/CD quality gates while previewing changes and preserving rollback options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use read, write, and command execution access to modify many local JSON files.

Mitigation: Run it first on a limited directory, require previews, and keep backups or snapshots before applying changes.

Risk: Custom script or regex rules can corrupt valid JSON or execute unsafe logic if they come from an untrusted source.

Mitigation: Use trusted rule files, test rules on small samples, review diffs, and avoid untrusted custom script rules.

Risk: Callback URLs or external rule sources may send data outside the local environment.

Mitigation: Do not provide callback URLs or external rule sources unless the destination is trusted and data sharing is understood.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/json-repair-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, diff snippets, shell commands, and structured repair reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local file edits, backups, snapshots, logs, and repair reports when the agent applies the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
