## Description: <br>
Extension for Bitwarden usage: adds an ephemeral HTTPS web unlock helper for rbw (TTL default 10m) so you can unlock remotely without pasting secrets into chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hans00](https://clawhub.ai/user/hans00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to unlock an rbw-backed Bitwarden vault from a short-lived web helper when direct secret entry in chat is inappropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper handles a Bitwarden vault password through a web form and ClawScan flags weak scoping and transport assumptions. <br>
Mitigation: Use localhost-only access or verified TLS, keep the helper short-lived, require one-time approval, and avoid default public tunneling unless it is explicitly needed. <br>
Risk: A printed public unlock URL contains the one-time token and could expose the form during the TTL window if shared or logged. <br>
Mitigation: Treat the full unlock URL as a secret, avoid posting it in issues, logs, screenshots, or shared channels, and stop the helper after use. <br>
Risk: The password exists briefly in process memory and same-user process scope while rbw unlock runs. <br>
Mitigation: Run the helper only on trusted systems, keep the TTL short, avoid unnecessary retries, and rely on the helper's documented no-disk-persistence and cleanup behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hans00/headless-bitwarden) <br>
- [Cloudflare tunnel downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides a localhost-first, token-gated unlock workflow with optional temporary HTTPS tunneling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
