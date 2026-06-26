## Description: <br>
Build a knowledge consultant Agent on OpenClaw that turns domain expertise into a 24/7 AI assistant for client questions in Feishu groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonlin1212](https://clawhub.ai/user/simonlin1212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Professionals and OpenClaw users use this skill to package domain knowledge into a client-facing consulting agent. It guides setup of dedicated agent workspaces, knowledge layering, safety constraints, search verification, and Feishu group delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated consulting bot may receive broad write and browser permissions. <br>
Mitigation: Remove write and browser permissions unless the deployment has a concrete need for them. <br>
Risk: Feishu no-mention handling can make the bot respond broadly in groups. <br>
Mitigation: Prefer allowlisted Feishu groups and keep @mention mode unless every participant consents to automatic processing. <br>
Risk: Privacy and transparency guardrails may be incomplete for client-facing consulting use. <br>
Mitigation: Clearly disclose that the bot is an AI consulting assistant and provide a human escalation path. <br>
Risk: The setup script changes workspace files and Feishu-related configuration workflows. <br>
Mitigation: Review or patch setup inputs before use and back up openclaw.json before changing Feishu settings. <br>


## Reference(s): <br>
- [Knowledge Agent ClawHub page](https://clawhub.ai/simonlin1212/knowledge-agent) <br>
- [Publisher profile](https://clawhub.ai/user/simonlin1212) <br>
- [Three-Layer Knowledge Architecture](references/knowledge-layers.md) <br>
- [Safety Constraints for Paid Consulting](references/safety-constraints.md) <br>
- [Anti-Hallucination: Quality Controls](references/anti-hallucination.md) <br>
- [Feishu Group Delivery Setup](references/feishu-delivery.md) <br>
- [Example: Douyin Operations Consultant](references/example-douyin.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell snippets, JSON-like configuration examples, and generated Markdown configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent workspace guidance and templates for AGENTS.md, SOUL.md, IDENTITY.md, MEMORY.md, TOOLS.md, and knowledge reference organization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
