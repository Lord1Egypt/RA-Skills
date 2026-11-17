## Description:

Connect OpenClaw to Shopify with guided setup, local secret storage, Shopify OAuth, webhook validation, product and content operations, and host or Docker-sidecar deployment support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dave8172](https://clawhub.ai/user/dave8172)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators use this skill to connect a Shopify store to OpenClaw, complete Shopify app setup, run a local connector, read store data, and make confirmed product or content updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Shopify API credentials and offline access tokens.

Mitigation: Store secrets only in the local .env runtime file, protect the runtime directory with owner-only permissions, and keep .env, state, and logs out of version control.

Risk: Default or excessive Shopify scopes can grant more store access than a workflow needs.

Mitigation: Start with read-only scopes, remove read_orders unless it is required, and add write scopes only for approved product or content workflows.

Risk: Product or content mutation helpers can change live Shopify store data.

Mitigation: Require explicit user confirmation before each write and use read-only or approved-operation modes for normal operation.

Risk: OAuth and webhook endpoints must be exposed over public HTTPS and can be misconfigured.

Mitigation: Validate the shop domain, verify callback URL alignment before OAuth, keep the connector bound locally when possible, and add webhook size and rate limits for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dave8172/skills/openclaw-shopify-manager)
- [Setup](references/setup.md)
- [Shopify scopes and safety](references/scopes-and-safety.md)
- [Security and behavior](references/security-and-behavior.md)
- [Tailscale](references/tailscale.md)
- [systemd](references/systemd.md)
- [Docker and container edge cases](references/docker.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON status output, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local runtime files, a .env-backed connector configuration, logs, state files, and Shopify Admin API JSON responses when the bundled scripts are run.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
