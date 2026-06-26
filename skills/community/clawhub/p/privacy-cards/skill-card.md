## Description: <br>
Create and manage Privacy.com virtual cards. Use for generating single-use cards, merchant-locked cards, listing cards, setting spending limits, pausing/closing cards, and viewing transactions via the Privacy.com API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JohnieLee](https://clawhub.ai/user/JohnieLee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare Privacy.com API requests for virtual card creation, card state changes, spend limits, card listing, and transaction lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide direct production financial-card management actions, including creating, updating, pausing, or closing virtual cards. <br>
Mitigation: Use a least-privileged Privacy.com API key, prefer sandbox testing, and require explicit confirmation before create, update, pause, or close requests. <br>
Risk: Card data, CVVs, full card numbers, or API keys could be exposed through chat, logs, terminal history, or shared files. <br>
Mitigation: Avoid displaying or storing full card numbers, CVVs, or API keys; redact sensitive outputs and keep credentials out of shared logs and files. <br>
Risk: Closing or modifying the wrong card can cause irreversible or unintended account changes. <br>
Mitigation: Verify the exact card token, intended state, and spend limit before running any card update or close command. <br>


## Reference(s): <br>
- [Privacy.com API Reference](references/api.md) <br>
- [Privacy.com](https://privacy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Privacy.com API endpoints, curl commands, request parameters, and response field descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
