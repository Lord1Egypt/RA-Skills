## Description: <br>
Query and summarize Twitter/X information using Grok AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danetteceola](https://clawhub.ai/user/danetteceola) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to send Twitter/X-related prompts to Grok and receive concise summaries about trends, tweets, accounts, or current topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Twitter/X prompts and the GROK_API_KEY bearer token are sent to the configured external API endpoint. <br>
Mitigation: Use a trusted GROK_API_URL, verify that api.cheaprouter.club is intended for your use case, and avoid sending private or confidential prompts. <br>
Risk: The skill relies on an external Grok-compatible API service to return Twitter/X summaries. <br>
Mitigation: Review returned summaries before relying on them and confirm that the configured provider meets your availability and data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/danetteceola/grok-twitter) <br>
- [Default Grok API Endpoint](https://api.cheaprouter.club/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text responses with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GROK_API_KEY and sends prompts to the configured GROK_API_URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
