## Description: <br>
Connect OpenClaw to Shopify with guided setup, local `.env` secret storage, Shopify OAuth, webhook validation, product and content operations, and host or Docker-sidecar deployment support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dave8172](https://clawhub.ai/user/dave8172) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw to a Shopify store, complete app setup and OAuth, inspect store and product data, and run user-confirmed product or content updates through a local connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security assessment says the skill asks for more Shopify access than its documented features need. <br>
Mitigation: Start with read-only verification, remove `read_orders` unless order access is required, and keep Shopify scopes limited to the intended workflow. <br>
Risk: The skill includes commands that can change Shopify product or content data. <br>
Mitigation: Require explicit user approval before any product or content mutation and keep mutation controls such as `require-confirmation-for-mutations` enabled. <br>
Risk: The local connector stores Shopify secrets and tokens in a runtime `.env` file. <br>
Mitigation: Keep the runtime `.env` outside repositories, restrict file permissions, and avoid placing secrets in config files, docs, screenshots, or command-line arguments. <br>
Risk: Tailscale, systemd, or public HTTPS exposure can affect the host environment and callback surface. <br>
Mitigation: Bind the connector locally by default, expose only the intended callback path, verify health endpoints after changes, and enable Tailscale or systemd only when the operator understands the host impact. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/dave8172/openclaw-shopify-manager) <br>
- [Setup](references/setup.md) <br>
- [Shopify scopes and safety](references/scopes-and-safety.md) <br>
- [Security and behavior](references/security-and-behavior.md) <br>
- [Docker and container edge cases](references/docker.md) <br>
- [systemd](references/systemd.md) <br>
- [Tailscale](references/tailscale.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and local runtime script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Shopify app credentials and local runtime configuration; store-changing actions should require explicit confirmation.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
