## Description: <br>
Generate QR code image URLs from text or URLs and decode QR codes from publicly accessible image URLs without configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create QR code image URLs for text or web links and to decode QR contents from public image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR payloads and decode targets are sent to a Pipeworx-hosted service. <br>
Mitigation: Avoid submitting passwords, API keys, confidential text, private documents, internal network URLs, or signed links unless that service use is acceptable. <br>
Risk: Decoding requires an image URL that the service can access. <br>
Mitigation: Use public, non-sensitive image URLs and verify decoded text before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-qrcode) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>
- [Pipeworx QR code MCP endpoint](https://gateway.pipeworx.io/qrcode/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON-compatible tool responses with QR image URLs or decoded QR text, plus Markdown setup examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated QR output is an externally hosted image URL; decoding requires a publicly accessible image URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
