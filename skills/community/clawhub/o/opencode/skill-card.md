## Description:

OpenCode AI helps agents delegate complex coding, refactoring, pull request review, and multi-file codebase work to the OpenCode CLI/TUI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[csuwl](https://clawhub.ai/user/csuwl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to run OpenCode for AI-assisted coding, codebase exploration, refactoring, pull request work, and session-based implementation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged global installation commands can modify system-owned OpenClaw skill directories.

Mitigation: Review installation commands before running them and prefer a user-owned skills directory when OpenClaw supports one.

Risk: A symlink-based development workflow can expose OpenClaw to untrusted or changing skill content.

Mitigation: Avoid symlink installation for untrusted content and review the linked directory before loading the skill.

Risk: Web or server mode can expose OpenCode over the network when bound broadly.

Mitigation: Do not bind the web interface to `0.0.0.0` unless authentication, firewalling, and a trusted network are in place.

Risk: Running OpenCode with attached files or project directories may send code or context to configured AI providers.

Mitigation: Review provider settings and attached context before running OpenCode on sensitive repositories.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/csuwl/skills/opencode)
- [Publisher Profile](https://clawhub.ai/user/csuwl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands that run OpenCode against local projects, attach files for context, continue sessions, or start server and web modes.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
