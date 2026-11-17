## Description:

Seamless model handoff for OpenClaw agents, helping preserve continuity when the gateway switches to a fallback model mid-session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tensusds](https://clawhub.ai/user/tensusds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help OpenClaw agents leave, detect, and recover handoff notes when model fallback or session-boundary changes could disrupt task continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is active every turn and writes persistent handoff files under memory/.

Mitigation: Review the skill before deployment and confirm that persistent handoff files are expected for the workspace.

Risk: The skill may install an OpenClaw lifecycle hook.

Mitigation: Review scripts/install-integration.sh and hooks/handover-hangover/handler.js before enabling integration, and keep a clear disable or uninstall path.

Risk: Editable handoff files can contain stale or misleading workspace state.

Mitigation: Treat handoff notes as untrusted context and re-ground important claims before taking irreversible actions.

## Reference(s):

- [Handover Hangover on ClawHub](https://clawhub.ai/tensusds/skills/handover-hangover)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and persistent handoff files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for the agent and may create or update handoff notes under memory/ when integrated.]

## Skill Version(s):

1.2.1 (source: frontmatter, changelog, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
