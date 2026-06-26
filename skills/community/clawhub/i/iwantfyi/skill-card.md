## Description: <br>
Buy, shop for, and find products for your user. Post what they want and get ranked product matches across sources, with condition and spec constraints enforced. Demand-side commerce for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staugs](https://clawhub.ai/user/staugs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill to search for products or services, enforce shopping constraints, present ranked matches, optionally create persistent wants, and report user shopping outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping searches, product constraints, and optional persistent wants may be sent to iwant.fyi. <br>
Mitigation: Use the skill only when the user is comfortable sharing the request with iwant.fyi, and ask before creating persistent wants. <br>
Risk: The skill can store and use a service API key. <br>
Mitigation: Store IWANTFYI_API_KEY as a secret, avoid exposing it in logs or transcripts, and rotate it if disclosure is suspected. <br>
Risk: Outcome reporting can send user activity events such as views, clicks, checkout starts, or purchases. <br>
Mitigation: Ask for user consent before reporting outcome events. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/staugs/iwantfyi) <br>
- [Publisher profile](https://clawhub.ai/user/staugs) <br>
- [iwant.fyi homepage](https://iwant.fyi) <br>
- [Bootstrap docs for agents](https://iwant.fyi/skill.md) <br>
- [iwant.fyi protocol v1](https://iwant.fyi/protocol/v1) <br>
- [Health check](https://iwant.fyi/api/v1/health) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, json] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request and response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses IWANTFYI_API_KEY when available; can register for an API key and call iwant.fyi HTTP endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
