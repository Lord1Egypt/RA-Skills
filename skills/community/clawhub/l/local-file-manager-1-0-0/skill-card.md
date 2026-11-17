## Description:

Local File Manager reads, writes, appends, lists, creates, and deletes local files in a session working directory for text, JSON, CSV, and Markdown workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[000sonic](https://clawhub.ai/user/000sonic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation roles use this skill to persist generated outputs, read local inputs, append logs or results, and create Markdown, JSON, CSV, or text files within a session workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The implementation can run unintended shell commands.

Mitigation: Review before installing and use only in a disposable or tightly sandboxed workspace until shell-string execution is replaced with argument-safe execution.

Risk: Paths can break the promised workspace boundary.

Mitigation: Require package-relative script resolution and real cwd containment before use in a trusted workspace.

Risk: Home-directory logging and destructive file actions may create operational exposure.

Mitigation: Document or remove home-directory logging, review delete behavior, and prefer dry-run validation before allowing destructive actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/000sonic/skills/local-file-manager-1-0-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Code, Shell commands, Configuration]

**Output Format:** [Plain text command results and local file contents; written files may be text, Markdown, JSON, CSV, code, shell commands, or configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write, append, list, create directories, delete files, and return operation status or errors.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
