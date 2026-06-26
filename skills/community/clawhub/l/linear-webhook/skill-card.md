## Description: <br>
Comment @mason or @eureka in Linear issues to dispatch tasks to agents. Webhook receives Linear comments and routes to correct agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Arnarsson](https://clawhub.ai/user/Arnarsson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn authenticated Linear issue comments into agent tasks for implementation, debugging, planning, and strategy work. It extracts issue context and routes the request to configured Clawdbot agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Linear comments can dispatch local agent sessions and may include confidential issue context. <br>
Mitigation: Use a dedicated webhook token, restrict webhook exposure to HTTPS endpoints, verify Linear source authenticity where possible, and avoid routing sensitive issues unless local agent logs and sessions are approved for that data. <br>
Risk: The generated task prompt includes a mandatory local shell command that can post back to Linear using write credentials. <br>
Mitigation: Remove or replace the mandatory command before deployment and require human review before any agent-posted Linear response uses configured write credentials. <br>
Risk: Linear write credentials can be read from environment variables or local files and used to create comments. <br>
Mitigation: Use a dedicated least-privilege Linear bot token, rotate it regularly, and keep credentials out of source control and shared logs. <br>
Risk: The artifact behavior includes an @forge route in code while the public documentation mainly describes @mason and @eureka. <br>
Mitigation: Document whether @forge is intentionally enabled or remove it from the agent mention map before production use. <br>
Risk: Helper scripts interpolate command-line arguments into shell or node snippets for posting responses. <br>
Mitigation: Sanitize helper-script inputs or replace shell interpolation with structured API calls before accepting untrusted response text. <br>


## Reference(s): <br>
- [ClawHub Linear Webhook release page](https://clawhub.ai/Arnarsson/linear-webhook) <br>
- [Clawdbot Webhook Docs](/automation/webhook) <br>
- [Linear Webhooks API](https://developers.linear.app/docs/graphql/webhooks) <br>
- [Linear API settings](https://linear.app/settings/api) <br>
- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown task prompts with inline shell commands and JSON/JSON5 configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include Linear issue metadata and optional API calls to post agent responses back to Linear.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
