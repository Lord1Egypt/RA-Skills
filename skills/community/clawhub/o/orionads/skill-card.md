## Description: <br>
Search for physical products, hardware, AI tools, and APIs via the Orion Ad Protocol. Returns structured data (JSON) optimized for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[celsojr2013](https://clawhub.ai/user/celsojr2013) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search OrionAds for structured product, hardware, API, SaaS, and tool results, and to prepare account, balance, or ad-posting API calls when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide account registration, balance checks, and ad posting against OrionAds, including actions that may use ORION_API_KEY or set a bid. <br>
Mitigation: Provide ORION_API_KEY only when account features are intended, and require explicit user review before registering an account, posting an ad, or setting any bid. <br>
Risk: Shell commands built from user search terms or ad payloads can be unsafe if raw input is interpolated. <br>
Mitigation: Use encoded query parameters for searches and safely escape or file-load JSON payloads before running curl commands. <br>


## Reference(s): <br>
- [Orion Ads on ClawHub](https://clawhub.ai/celsojr2013/orionads) <br>
- [OrionAds Search API](https://orionads.net/api/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search responses are expected to be structured JSON from OrionAds; ORION_API_KEY is optional and only needed for account features.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
