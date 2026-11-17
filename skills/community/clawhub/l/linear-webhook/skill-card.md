## Description:

Comment @mason or @eureka in Linear issues to dispatch tasks to agents. Webhook receives Linear comments and routes to correct agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnarsson](https://clawhub.ai/user/arnarsson)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to route Linear issue comments that mention configured agents into Clawdbot agent sessions, then optionally post agent responses back to Linear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Linear comments and issue content are untrusted input that can be routed into agent prompts and response workflows.

Mitigation: Treat all Linear content as untrusted data, limit which Linear projects and users can trigger agents, and require review or approval before any agent-produced action is posted back.

Risk: The artifact includes mandatory shell/node postback instructions and helper scripts that can execute commands while posting responses.

Mitigation: Remove mandatory postback command instructions and replace them with a fixed, trusted postback path that validates issue IDs, agent names, and response content before execution.

Risk: The response-posting code can read Linear credentials from local files such as ~/.linear_api_key.

Mitigation: Use scoped secret injection or environment-managed credentials instead of local credential file reads, and grant only the Linear scopes required for comment posting.

## Reference(s):

- [Linear Webhooks API](https://developers.linear.app/docs/graphql/webhooks)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [Linear API settings](https://linear.app/settings/api)
- [ClawHub skill page](https://clawhub.ai/arnarsson/skills/linear-webhook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown task prompts, JSON-style configuration, JavaScript transforms, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes the first supported Linear @mention in a comment to a configured agent session and can include Linear issue context plus response-posting instructions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
