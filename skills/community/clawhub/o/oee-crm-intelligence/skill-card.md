## Description: <br>
Two-stage intelligent filtering and scoring of CRM contacts using keywords and AI, adapting over time to prioritize leads that matter most to you. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OdinBot33](https://clawhub.ai/user/OdinBot33) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, relationship-management, and personal CRM users use this skill to filter contact lists, score leads, and prioritize outreach with rule-based checks plus optional Anthropic classification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI scoring can send CRM contact details and message subject context to Anthropic. <br>
Mitigation: Use a dedicated API key, process only contacts you are permitted to send to a third-party model provider, and avoid highly sensitive records unless approved. <br>
Risk: Rejected contacts may be persisted in learning.json and filtered out in later runs. <br>
Mitigation: Periodically inspect, edit, or reset learning.json so contacts are not permanently excluded by mistake. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/OdinBot33/oee-crm-intelligence) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python and bash examples; the runtime script prints text summaries and returns JSON-compatible evaluation records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses learning.json for filtering preferences and persisted rejected contacts; optional Stage 2 scoring requires ANTHROPIC_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
