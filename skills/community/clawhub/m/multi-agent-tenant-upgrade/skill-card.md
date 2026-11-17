## Description:

Multi-agent UX for OpenClaw Control UI: agent selector, per-agent sessions, session history, agent-filtered Sessions tab, Create Agent wizard, emoji picker, backend agent CRUD, and auth mode badge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to patch the OpenClaw Control UI and gateway for multi-agent management, session browsing, wizard-based agent creation, and auth visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently patches sensitive auth, session, and gateway code.

Mitigation: Review each patch before applying, back up or branch the OpenClaw checkout, rebuild the UI and gateway, and scan the result before use.

Risk: The auth badge behavior may expose raw auth profile identifiers in the UI.

Mitigation: Review the auth badge changes before applying and prefer returning only coarse modes such as oauth, api, or fallback.

Risk: The session history feature exposes stored conversations through the Control UI.

Mitigation: Treat session transcripts as sensitive data and limit installation and access to trusted OpenClaw operators.

Risk: Temporary Python-based config repair can be unsafe for JSONC-style configuration files.

Mitigation: Make a backup first and use a JSONC-aware, atomic edit process instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/multi-agent-tenant-upgrade)
- [Skill source and installation notes](artifact/SKILL.md)
- [Agent gateway patch](artifact/references/server-agents.txt)
- [Session history RPC patch](artifact/references/v1.4.0/patch-01-sessions-history-rpc.txt)
- [Sessions tab overhaul patch](artifact/references/v1.4.0/patch-02-sessions-tab-overhaul.txt)
- [Auth badge patch](artifact/references/v1.5.0/patch-auth-badge.txt)
- [Pipedream and Zapier agent switch patch](artifact/references/v1.5.0/patch-pipedream-agent-switch.txt)
- [Anthropic Messages API endpoint used by the wizard](https://api.anthropic.com/v1/messages)
- [OpenAI Chat Completions endpoint used by the wizard](https://api.openai.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with TypeScript patch files and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applies persistent OpenClaw source patches and requires UI and gateway rebuilds.]

## Skill Version(s):

1.5.2 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
