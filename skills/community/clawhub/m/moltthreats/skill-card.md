## Description: <br>
Agent-native security signal feed by PromptIntel for reporting threats, fetching protection feeds, applying security rules, and updating SHIELD.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr0gger](https://clawhub.ai/user/fr0gger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use MoltThreats to submit agent-security threat reports, retrieve curated threat protections, and maintain local SHIELD.md enforcement policy. It is intended for environments that want PromptIntel threat intelligence integrated into agent runtime decisions with explicit user consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead to persistent agent-policy changes in SHIELD.md, SOUL.md, AGENTS.md, or HEARTBEAT.md. <br>
Mitigation: Review and approve proposed policy or configuration edits before relying on them, and disable autonomous enforcement if background feed updates are not desired. <br>
Risk: The skill requires PROMPTINTEL_API_KEY and sends authenticated requests to the PromptIntel API. <br>
Mitigation: Keep the key in an environment variable only, never hardcode it, and send it only to api.promptintel.novahunting.ai. <br>
Risk: Threat report samples and indicators may accidentally include secrets or private data. <br>
Mitigation: Inspect and redact reports before submission, and confirm that samples contain only the evidence needed for review. <br>


## Reference(s): <br>
- [MoltThreats Homepage](https://promptintel.novahunting.ai/molt) <br>
- [PromptIntel API Base](https://api.promptintel.novahunting.ai/api/v1) <br>
- [SHIELD.md Specification](https://nova-hunting.github.io/shield.md/) <br>
- [Feed Consumption and Enforcement](references/feed-and-enforcement.md) <br>
- [Reporting Guide](references/reporting-guide.md) <br>
- [SHIELD.md Template](references/shield-md-template.md) <br>
- [Integration Example](references/integration-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and SHIELD.md policy updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update SHIELD.md and propose agent configuration changes that require user review.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
