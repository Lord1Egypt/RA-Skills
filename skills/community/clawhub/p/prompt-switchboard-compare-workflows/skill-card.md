## Description:

Teach an agent to install Prompt Switchboard's local MCP sidecar, connect it in a host, and run a compare-first browser workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect a local Prompt Switchboard MCP sidecar to OpenHands/OpenClaw-style hosts, verify ready AI chat tabs, and run compare-first browser workflows that produce inspectable compare artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unpinned external MCP server whose behavior can change after review.

Mitigation: Review the external Prompt Switchboard repository before installing, prefer a pinned reviewed commit, run npm ci from a lockfile when available, and point host configuration only at that verified checkout.

Risk: The local MCP sidecar and browser extension workflow can interact with local files, environment, and active browser tabs depending on host permissions.

Mitigation: Limit the MCP process's file, environment, and browser-tab access, and run bridge_status and check_readiness before compare so blocked tabs or setup issues are reported rather than bypassed.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/xiaojiou176/skills/prompt-switchboard-compare-workflows)
- [ClawHub Publisher Profile](https://clawhub.ai/user/xiaojiou176)
- [Skill README](artifact/README.md)
- [Install and Connect Prompt Switchboard MCP](artifact/references/INSTALL.md)
- [Prompt Switchboard MCP Capabilities](artifact/references/CAPABILITIES.md)
- [OpenHands / OpenClaw Demo Walkthrough](artifact/references/DEMO.md)
- [Prompt Switchboard Troubleshooting](artifact/references/TROUBLESHOOTING.md)
- [OpenHands MCP Config](artifact/references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP Config](artifact/references/OPENCLAW_MCP_CONFIG.json)
- [Prompt Switchboard install target](https://github.com/xiaojiou176-open/multi-ai-sidepanel)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON host configuration snippets, and MCP tool names.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to check bridge and tab readiness before compare, then inspect session and turn artifacts.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
