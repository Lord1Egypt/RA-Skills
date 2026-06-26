## Description: <br>
OpenClaw plugin for Otto Travel that searches, compares, and books flights and hotels via Otto's MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cd-otto](https://clawhub.ai/user/cd-otto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this plugin to search travel options, compare results, book flights or hotels, and manage Otto preferences and loyalty programs through an authenticated Otto account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can run real booking and account-changing actions through Otto's remote MCP server. <br>
Mitigation: Require explicit human approval before book_flight, book_hotel, preference, or loyalty-program write actions are executed. <br>
Risk: OAuth tokens are stored locally for subsequent authenticated travel actions. <br>
Mitigation: Treat ~/.openclaw/.otto-tokens.json like a password and avoid syncing, sharing, or exposing it. <br>
Risk: Authenticated requests are sent to the configured MCP server URL. <br>
Mitigation: Install and use the plugin only when you trust Otto and the configured server URL. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration] <br>
**Output Format:** [Text responses from Otto Travel tools and configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tools are discovered dynamically from the configured Otto MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
