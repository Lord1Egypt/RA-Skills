## Description:

OpenCode CLI guidance for submitting coding tasks, managing sessions, delegating work to coding agents, checking status, and configuring OpenCode settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tornado404](https://clawhub.ai/user/tornado404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent operators use this skill to drive OpenCode and oho CLI workflows for submitting tasks, managing sessions, checking task status, and configuring providers or project settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server startup examples include a hard-coded password, broad network binding, and mDNS exposure that could expose powerful coding-agent controls if copied as written.

Mitigation: Use a unique password, bind to localhost by default, and enable remote access or mDNS only on trusted networks with intentional access controls.

Risk: Session deletion, session sharing, shell execution, process killing, and file attachment commands can change projects or disclose private files.

Mitigation: Require explicit user confirmation before destructive actions, sharing sessions, executing shell commands, killing processes, or sending private project files to external models.

## Reference(s):

- [OpenCode Official Docs](https://opencode.ai/docs/)
- [oho CLI Repository](https://github.com/tornado404/opencode_cli)
- [OpenCode Configuration Schema](https://opencode.ai/config.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON output flags, file attachment examples, and environment-variable settings when relevant.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
