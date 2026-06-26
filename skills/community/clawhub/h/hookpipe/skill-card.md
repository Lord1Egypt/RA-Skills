## Description: <br>
hookpipe helps agents receive, verify, queue, and retry webhooks from services such as Stripe, GitHub, Slack, Shopify, and Vercel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linyiru](https://clawhub.ai/user/linyiru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure hookpipe CLI workflows that deliver external webhook events to an OpenClaw gateway during local development and production operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook signing secrets and hookpipe tokens can be exposed through shared terminals, logs, screenshots, commits, or chat. <br>
Mitigation: Treat these values as credentials; avoid sharing or committing them and rotate them if exposure is suspected. <br>
Risk: Broad webhook subscriptions can route more event data through the queue than intended. <br>
Mitigation: Use narrow event filters, keep only needed connections active, and remove unused connections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linyiru/hookpipe) <br>
- [hookpipe GitHub repository](https://github.com/hookpipe/hookpipe) <br>
- [Provider Design Guide](https://github.com/hookpipe/hookpipe/blob/main/packages/providers/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides hookpipe CLI command patterns for connecting providers, running a local tunnel, discovering providers, streaming events, and checking health.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
