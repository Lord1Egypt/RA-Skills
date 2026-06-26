## Description: <br>
Single-file bash CLI for the *arr media stack with SSH remote support, intended for agents running on a different machine than the media services while tunneling API calls through existing SSH config so services stay on localhost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and homelab operators use this skill to let an agent manage a remote media stack from the terminal, including searching, adding, monitoring, refreshing, pausing, resuming, and removing media-related downloads and library entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables shell-level control over media services, including actions that can mutate libraries, downloads, queues, and refresh state. <br>
Mitigation: Require confirmation before add, pause, remove, refresh, or other state-changing actions. <br>
Risk: Download removal can include file deletion when invoked with delete-file behavior. <br>
Mitigation: Require explicit user confirmation before delete-file actions and state whether files will be kept or deleted. <br>
Risk: Stored service API keys and SSH access can expose control over the media stack if mishandled. <br>
Mitigation: Protect API keys and SSH credentials, keep configuration permissions restricted, and review the external script before running it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/solomonneas/media-cli) <br>
- [Publisher Profile](https://clawhub.ai/user/solomonneas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing CLI guidance for a bash media-control tool; mutation and deletion actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
