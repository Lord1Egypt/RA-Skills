## Description:

Google Maps tools via OneKey Gateway (geocode, places, distance matrix, elevation, directions).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to call Google Maps geocoding, reverse geocoding, place search, place details, distance matrix, elevation, and directions workflows through OneKey Gateway from CLI commands or Python scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends location, place, route, and travel queries to external OneKey/Google-backed services.

Mitigation: Avoid submitting highly sensitive home, workplace, or travel locations unless the user is comfortable with that external data flow.

Risk: Scripts fall back to a bundled shared demo gateway key when DEEPNLP_ONEKEY_ROUTER_ACCESS is unset.

Mitigation: Set a scoped OneKey Gateway API key in DEEPNLP_ONEKEY_ROUTER_ACCESS and avoid relying on the demo key for normal use.

Risk: The skill uses unpinned npm and Python dependency installs.

Mitigation: Review and pin @aiagenta2z/onekey-gateway and ai-agent-marketplace versions before deployment.

## Reference(s):

- [ClawHub Google Maps Skill](https://clawhub.ai/ai-hub-admin/skills/google-maps-onekey-gateway)
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys)
- [OneKey MCP Router Documentation](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway Documentation](https://deepnlp.org/doc/onekey_agent_router)
- [AI Agent Marketplace GitHub](https://github.com/aiagenta2z/ai-agent-marketplace)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Code, Configuration guidance]

**Output Format:** [JSON responses with Markdown usage examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on external Google Maps access through OneKey Gateway and the configured API key.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
