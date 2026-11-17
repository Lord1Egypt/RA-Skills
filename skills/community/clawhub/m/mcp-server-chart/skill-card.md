## Description:

Auto-generated skill for mcp-server-chart tools via OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data-focused agents use this skill to send structured chart, map, diagram, and spreadsheet requests through OneKey Gateway and receive generated visualization outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends chart, map, diagram, and spreadsheet payloads to an external gateway.

Mitigation: Avoid private spreadsheet data and sensitive home, work, medical, or travel locations in payloads.

Risk: The scripts and documentation include unpinned npm, pip, and npx dependency usage.

Mitigation: Use pinned, audited dependency versions and run the tools in a constrained environment.

Risk: The scripts fall back to a shared demo access key when no OneKey key is configured.

Mitigation: Set DEEPNLP_ONEKEY_ROUTER_ACCESS to an owned key before use and avoid relying on the fallback key.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/mcp-server-chart)
- [OneKey MCP Router Doc](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway Doc](https://deepnlp.org/doc/onekey_agent_router)
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent)
- [GitHub AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON responses printed by Python wrapper scripts and documented shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a OneKey Gateway access key; chart payloads are supplied as JSON strings or JSON files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
