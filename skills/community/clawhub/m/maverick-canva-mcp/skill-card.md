## Description:

Search, read, and manage Canva designs, assets, exports, and templates through Canva's hosted MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and Canva account holders can use the skill to find and review designs, assets, exports, and templates, and to manage Canva content through the account they connect. Developers can use it to connect an agent to Canva's hosted MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Edits, sharing, comments, or publishing can affect content visible to the connected Canva account or team.

Mitigation: Confirm clear user intent before changes, review the affected content and granted account permissions, and avoid sending unrelated sensitive information.

Risk: Rerunning setup with stale OAuth credentials can overwrite newer credentials stored by the integration.

Mitigation: Only rerun setup with freshly issued credentials; revoke the Canva integration when it is no longer needed.

## Reference(s):

- [Canva MCP documentation](https://www.canva.dev/docs/mcp/)
- [Canva MCP troubleshooting](https://www.canva.dev/docs/mcp/troubleshooting/)
- [ClawHub skill page](https://clawhub.ai/maverick/skills/maverick-canva-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Files, Guidance]

**Output Format:** [Natural-language responses and Canva design or asset exports, depending on available server tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available actions and export formats depend on the live Canva MCP tool catalog and the connected account's permissions.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
