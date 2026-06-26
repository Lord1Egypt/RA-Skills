## Description: <br>
Access overseas or external URLs through the JumpOnce proxy service for HTTP forwarding and WebSocket relay using the documented jumptox.top API and a required API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[men459](https://clawhub.ai/user/men459) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route approved HTTP or WebSocket requests through JumpOnce when the current network cannot directly reach an external API or website. It is intended for intentional proxying of authorized targets. <br>

### Deployment Geography for Use: <br>
Global; documented proxy exit is Oracle Cloud Phoenix, USA. <br>

## Known Risks and Mitigations: <br>
Risk: Requests, headers, cookies, personal data, internal URLs, or WebSocket streams may be routed through a third-party proxy provider. <br>
Mitigation: Use the skill only for intentional proxying through JumpOnce, inspect requests before sending, and avoid forwarding sensitive traffic unless the provider is trusted and the use is authorized. <br>
Risk: The artifact includes plain-HTTP examples for JumpOnce API endpoints. <br>
Mitigation: Prefer HTTPS-only endpoints where supported and treat plain-HTTP examples as unsafe for sensitive credentials or data. <br>


## Reference(s): <br>
- [JumpOnce API Reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/men459/jump-once-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell and Python examples; forwarded HTTP calls can return JSON or raw responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUMPONCE_API_KEY or an --api-key argument; structured responses may include status code, headers, body, elapsed time, and final URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
