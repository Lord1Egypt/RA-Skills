## Description:

Read, write, append, delete, create directories, and list local files in a session working directory for agents that need local file persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyico](https://clawhub.ai/user/liyico)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to save generated output, read local input files, append logs or results, create directories, list workspace files, or remove files during a session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can run unsafe shell commands and may cause filesystem effects outside the intended working-directory boundary.

Mitigation: Review before installation, run only in a disposable tightly sandboxed environment, and prefer an implementation that uses native filesystem APIs or execFile/spawn with argument arrays.

Risk: Path handling may not reliably prevent workspace escape, including symlink-based escape or insufficient canonicalization.

Mitigation: Canonicalize paths against the session cwd, block symlink escapes, and enforce workspace-bound read, write, and delete permissions.

Risk: The skill may log file operations outside the workspace by default.

Mitigation: Make logging opt-in or direct logs to a workspace-local path before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyico/skills/local-file-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text or file contents returned through command output; configuration and usage guidance may be Markdown or inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local file operations such as read, write, append, list, mkdir, and delete; maximum file size is documented as 10MB.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
