## Description: <br>
Securely expose an OpenClaw Gateway WebUI on a VPS via Cloudflare Zero Trust Access + Cloudflare Tunnel (cloudflared), including DNS cutover for custom hostnames and optional cleanup of Tailscale Serve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jskoiz](https://clawhub.ai/user/jskoiz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to publish an OpenClaw Gateway WebUI through Cloudflare Tunnel and protect it with Cloudflare Access policies. It also supports DNS cutover for custom hostnames and optional cleanup of a previous Tailscale Serve setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Cloudflare DNS records and tunnel routing for the selected zone. <br>
Mitigation: Use a zone-scoped Cloudflare API token, inspect or back up existing DNS records before cutover, and run it only against the VPS and Cloudflare zone you intend to manage. <br>
Risk: A public hostname could expose the OpenClaw WebUI if Cloudflare Access is misconfigured. <br>
Mitigation: Confirm the Cloudflare Access allowlist and block policy before relying on the hostname. <br>
Risk: The installer fetches a cloudflared package during setup. <br>
Mitigation: Verify the cloudflared package source where possible before installation. <br>


## Reference(s): <br>
- [OpenClaw Cloudflare Secure release page](https://clawhub.ai/jskoiz/openclaw-cloudflare-secure) <br>
- [cloudflared Linux AMD64 release package](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb) <br>
- [Cloudflare API endpoint used by bundled DNS helper](https://api.cloudflare.com/client/v4) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash commands and bundled helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational setup guidance for Cloudflare Tunnel, Cloudflare Access, DNS records, and cloudflared service management.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
