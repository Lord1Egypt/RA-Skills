## Description:

Route plain-language requests for Pi, Claude Code, Codex, OpenCode, Gemini CLI, or ACP harness work into either OpenClaw ACP runtime sessions or direct acpx-driven sessions ("telephone game" flow).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zch-danny](https://clawhub.ai/user/zch-danny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route coding-harness requests into OpenClaw ACP runtime sessions or direct acpx-driven sessions while preserving thread, session, and one-shot handling rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to run local harness commands, install packages, restart gateways, and modify persistent ACP configuration.

Mitigation: Require explicit approval for package installs, gateway restarts, session cancellation or closure, and edits or deletion of ~/.acpx/config.json.

Risk: Shell command templates for acpx sessions can be unsafe if prompts, session names, or workspace paths are interpolated without care.

Mitigation: Prefer pinned adapter binaries, locked versions, explicit working directories, and safe argument-array execution when implementing the commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zch-danny/skills/openclaw-acp-router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes requests to ACP runtime sessions or direct acpx sessions; does not produce files as its primary output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
