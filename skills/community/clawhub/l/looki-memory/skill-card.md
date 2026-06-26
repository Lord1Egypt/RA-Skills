## Description: <br>
Access the user's digital personal memory to retrieve context and generate more personalized, data-driven responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haibo-looki](https://clawhub.ai/user/haibo-looki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to let an agent retrieve Looki profile, memory, highlight, and realtime-event context so responses can reflect the user's real-world activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private wearable memory data and account profile details. <br>
Mitigation: Install it only when you trust Looki and the configured base URL, and use narrow date or topic requests when possible. <br>
Risk: The Looki API key is a sensitive credential that could expose personal memory data if mishandled. <br>
Mitigation: Treat the API key like a password, avoid saving it unless persistence is needed, and remove ~/.config/looki/credentials.json when the skill is no longer used. <br>
Risk: Sending the API key to an untrusted endpoint could disclose credentials. <br>
Mitigation: Validate the base URL before first use and send the X-API-Key header only to the configured base URL. <br>


## Reference(s): <br>
- [Looki Base URL Verification API](https://open.looki.ai/api/v1/verify?endpoint={base_url}) <br>
- [Looki Memory on ClawHub](https://clawhub.ai/haibo-looki/looki-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Looki base URL and API key; documented API requests are limited to 60 requests per minute.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
