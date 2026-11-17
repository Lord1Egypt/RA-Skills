## Description:

OpenClaw Bastion scans agent workspace content for prompt injection patterns, boundary confusion, hidden instructions, and command policy concerns using local Python commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to check workspace files, user-supplied documents, web content, and command policies for prompt injection risks before an agent acts on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports broad file-changing and persistent hook behavior with unsafe scoping and restoration logic.

Mitigation: Review the script behavior before installation, start with read-only scan/check/status commands, and inspect generated hook configuration before enabling it.

Risk: Quarantine and unquarantine actions can affect files outside the intended workspace if used with unsafe paths.

Mitigation: Run quarantine and unquarantine only against reviewed paths inside the intended workspace.

Risk: Scanning secret-bearing files can print matched text to the console.

Mitigation: Avoid scanning files that contain secrets or review console output handling before scanning sensitive workspaces.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atlaspa/skills/openclaw-bastion)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text CLI reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3; some subcommands may modify workspace files or generate hook configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
