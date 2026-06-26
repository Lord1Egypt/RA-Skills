## Description: <br>
Manage social media across 9 platforms, track App Store analytics, monitor ASO keywords, analyze competitors, and control subscription pricing through conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makepost](https://clawhub.ai/user/makepost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External app developers and growth teams use this skill to publish and schedule social content, review App Store analytics and ASO data, monitor competitors, and manage subscription pricing from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, schedule, edit, or delete social media content across connected accounts. <br>
Mitigation: Require explicit user confirmation before publishing live content, deleting scheduled content or drafts, or running bulk social operations. <br>
Risk: The skill can push App Store subscription price changes that may take effect immediately. <br>
Mitigation: Review staged prices with current territory pricing and require explicit confirmation before calling push_price_changes. <br>
Risk: The MakePost API key grants access to connected MakePost, social, and App Store-related account data and actions. <br>
Mitigation: Use a dedicated, revocable API key and avoid placing real keys in chats, source files, or shared logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/makepost/makepost-com-app-growth) <br>
- [MakePost OpenClaw integration guide](https://makepost.com/openclaw) <br>
- [MakePost MCP documentation](https://makepost.com/mcp) <br>
- [MakePost API documentation](https://api.makepost.com) <br>
- [MakePost MCP endpoint](https://makepost.com/api/mcp/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown and agent-readable tool instructions with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAKEPOST_API_KEY and npx; actions use the MakePost MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
