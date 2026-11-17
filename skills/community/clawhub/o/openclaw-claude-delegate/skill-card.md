## Description:

Provides an OpenClaw skill and CLI wrapper for delegating work to a locally authenticated Claude Code worker with dispatch, polling, result retrieval, resume, profile-based workspace scoping, and optional non-root execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henryclaw007-lgtm](https://clawhub.ai/user/henryclaw007-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to route selected tasks to a local Claude Code worker while keeping task dispatch, monitoring, results, resume, and workspace profile selection explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The delegated Claude worker can have broad file and command authority in configured workspaces.

Mitigation: Use narrow project profiles, review the selected workdir and add_dirs values, and avoid the packaged HOME workspace for routine use.

Risk: The non-root runner setup can copy privileged Claude credentials into another account.

Mitigation: Do not copy root Claude credentials into a runner unless that boundary change is intentional and reviewed.

Risk: Remote bootstrap paths such as curl-to-bash or unpinned npx increase supply-chain exposure.

Mitigation: Prefer a reviewed local install or a pinned release before running installer scripts.

Risk: Notification hooks can execute arbitrary local commands.

Mitigation: Treat --notify-cmd values as local code execution and only use reviewed commands.

## Reference(s):

- [Claude Delegate setup](references/setup.md)
- [OpenClaw Claude Delegate ClawHub listing](https://clawhub.ai/henryclaw007-lgtm/skills/openclaw-claude-delegate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, shell command output, and JSON task result records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task runs can produce status, session, cost, duration, model, and result metadata through the local runner.]

## Skill Version(s):

0.2.6 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
