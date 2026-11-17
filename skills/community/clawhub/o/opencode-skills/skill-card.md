## Description:

Opencode helps agents automate website creation, project analysis, script execution, file management, local server preview, and code generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linshuikeji](https://clawhub.ai/user/linshuikeji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation-focused users can use this skill to guide opencode-based site generation, project inspection, command execution, file operations, preview-server startup, and project reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup examples may remove caches or temporary files destructively.

Mitigation: Require explicit confirmation before cleanup commands and scope deletion paths to known project-owned directories.

Risk: Privileged ownership and firewall examples can change system state.

Mitigation: Review privileged commands before execution and avoid sudo operations unless an operator has confirmed the target host and port.

Risk: Unpinned npx examples can execute package code that changes over time.

Mitigation: Prefer pinned package versions or built-in tooling when starting local preview servers.

Risk: Archive extraction examples can overwrite files or unpack unexpected paths.

Mitigation: Inspect archive contents before extraction and extract into an isolated destination directory.

Risk: Opencode server examples can expose an unsecured service if run without authentication.

Mitigation: Bind servers to localhost where possible and configure authentication before exposing any service beyond the local machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linshuikeji/skills/opencode-skills)
- [Publisher profile](https://clawhub.ai/user/linshuikeji)
- [Opencode documentation](https://opencode.ai/docs)
- [Opencode GitHub](https://github.com/opencode)
- [Opencode user guide](https://opencode.ai/docs/user-guide)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational examples for opencode commands, filesystem operations, local preview servers, and project reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
