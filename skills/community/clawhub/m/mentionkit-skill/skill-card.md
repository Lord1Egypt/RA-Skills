## Description: <br>
Query and manage Mentionkit social monitoring workflows to review brand mentions, find reply opportunities, shortlist lead-generation conversations, inspect source links, and create tracked keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shash7](https://clawhub.ai/user/shash7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to work with Mentionkit social monitoring data through MCP when available, or the Public API v1 for narrower scripting and basic data access. It supports mention review, opportunity shortlisting, source inspection, keyword creation through MCP, and concise confidence summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Mentionkit actions can affect a live workspace, especially keyword creation through MCP write scope. <br>
Mitigation: Use MCP write actions only with the intended workspace and token scope, and do not invent project values, platform settings, subreddit lists, banned words, or classifier prompts. <br>
Risk: Mention source fetches can fail while still returning a response envelope, which could lead to overconfident review conclusions. <br>
Mitigation: Check fetch status before treating a source as verified and lower confidence when source inspection fails. <br>
Risk: The skill depends on Mentionkit MCP or API access and may be unusable without workspace credentials or internet connectivity. <br>
Mitigation: Confirm the MCP server connection or API key before relying on the workflow, and fall back to API v1 only for its documented narrower data access. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/shash7/mentionkit-skill) <br>
- [Mentionkit skill page](https://clawhub.ai/shash7/skills/mentionkit-skill) <br>
- [Mentionkit API OpenAPI JSON](https://api.mentionkit.com/openapi.json) <br>
- [Mentionkit API OpenAPI YAML](https://api.mentionkit.com/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, markdown] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Mentionkit MCP tools or Public API v1 when the required workspace access, MCP connection, internet access, and API key are available.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
