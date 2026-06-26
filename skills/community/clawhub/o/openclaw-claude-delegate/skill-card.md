## Description: <br>
OpenClaw Claude Delegate gives OpenClaw agents a local Claude Code delegation lane with dispatch, polling, results, resume support, bounded work directories, and an optional non-root runner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henryclaw007-lgtm](https://clawhub.ai/user/henryclaw007-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to delegate selected work to a locally authenticated Claude Code worker while keeping task tracking, resume, and workspace scoping inside their OpenClaw workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let OpenClaw agents run work through a locally authenticated Claude Code account with broad local execution capability. <br>
Mitigation: Install it only when that delegation path is intentional, use a dedicated non-root runner where possible, and keep profiles scoped to specific project directories. <br>
Risk: Credential handling can copy or source sensitive Claude authentication material for runner execution. <br>
Mitigation: Use separate runner credentials where practical, review copied credentials during setup, and revoke or remove them when uninstalling. <br>
Risk: Remote installer and notification hooks can execute local shell commands. <br>
Mitigation: Prefer the native skill installer or a reviewed local clone over curl-to-bash, and avoid --notify-cmd unless the command source is fully trusted. <br>


## Reference(s): <br>
- [Claude Delegate setup](references/setup.md) <br>
- [OpenClaw Claude Delegate README](README.md) <br>
- [ClawHub skill listing](https://clawhub.ai/henryclaw007-lgtm/openclaw-claude-delegate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and task-status text from local CLI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured local profiles and Claude Code authentication; task execution may create local logs and result files.] <br>

## Skill Version(s): <br>
0.2.6 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
