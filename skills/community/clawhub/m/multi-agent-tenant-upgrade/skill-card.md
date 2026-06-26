## Description: <br>
Multi-agent UX for OpenClaw Control UI: agent selector, per-agent sessions, session history viewer with search, agent-filtered Sessions tab with friendly names, Create Agent wizard, emoji picker, backend agent CRUD, and auth mode badge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to patch OpenClaw with multi-agent tenant UX, session history, agent creation and editing, agent-scoped scheduling status, model selector fixes, and auth-mode visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently patches core OpenClaw source files. <br>
Mitigation: Review the full patch set before installation, apply it on a git branch or backup, and rebuild only after confirming the patch scope. <br>
Risk: Auth badge changes can expose auth profile identifiers in browser or client state. <br>
Mitigation: Restrict the Control UI to trusted users and prefer sending only display-safe auth modes such as oauth, api, fallback, or unknown. <br>
Risk: The AI wizard makes outbound model-provider API calls using configured credentials. <br>
Mitigation: Confirm the selected provider, keep API keys in trusted profiles or environment variables, and avoid submitting sensitive descriptions to the wizard. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maverick-software/multi-agent-tenant-upgrade) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Agents view patch](artifact/references/agents-view.txt) <br>
- [Server agents patch](artifact/references/server-agents.txt) <br>
- [Sessions history RPC patch](artifact/references/v1.4.0/patch-01-sessions-history-rpc.txt) <br>
- [Sessions tab overhaul patch](artifact/references/v1.4.0/patch-02-sessions-tab-overhaul.txt) <br>
- [Auth badge patch](artifact/references/v1.5.0/patch-auth-badge.txt) <br>
- [Pipedream agent switch patch](artifact/references/v1.5.0/patch-pipedream-agent-switch.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with patch code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies persistent source patches and requires an OpenClaw UI and gateway rebuild.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
