## Description: <br>
Automate secure HTTPS setup for OpenClaw Gateway on a VPS by configuring Nginx reverse proxy with SSL certificates and domain redirection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanue1](https://clawhub.ai/user/nanue1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to expose an existing OpenClaw Gateway through a custom domain with Nginx, Certbot-managed TLS certificates, HTTPS redirection, and reverse proxy settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup exposes OpenClaw Gateway to the internet through Nginx. <br>
Mitigation: Confirm the gateway should be publicly reachable and add authentication, IP restrictions, or other access controls where needed. <br>
Risk: The generated Nginx, Certbot, and cron changes can affect production traffic or existing server configuration. <br>
Mitigation: Review the configuration before running it, back up existing Nginx and cron settings, and avoid applying changes during critical traffic windows. <br>
Risk: Certificate renewal may duplicate or conflict with existing renewal automation. <br>
Mitigation: Prefer the packaged Certbot renewal timer or verify that any cron entry is idempotent before installing it. <br>


## Reference(s): <br>
- [OpenClaw HTTPS Setup on ClawHub](https://clawhub.ai/nanue1/openclaw-https-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and Nginx configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privileged server administration commands and TLS certificate setup steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact META.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
