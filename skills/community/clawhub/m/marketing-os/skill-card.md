## Description: <br>
AI Agent marketing operating system with a Virtual CMO for market analysis and strategy and a Marketing Operator for campaign planning, execution tracking, and feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forevercrab321-svg](https://clawhub.ai/user/forevercrab321-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, growth operators, and agent developers use this skill to turn business context and market signals into scored opportunities, structured campaign plans, execution tasks, metrics, and feedback loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store campaign state, learnings, logs, and market insight data that may include sensitive customer or business information. <br>
Mitigation: Review and purge memory and logs periodically, avoid storing unnecessary sensitive data, and apply retention controls before connecting production sources. <br>
Risk: Optional CRM, content, and analytics adapters could write to external systems or publish campaign content when enabled. <br>
Mitigation: Keep adapters disabled unless needed, use least-privilege credentials, and require human approval for publishing, CRM writes, paid campaigns, budget changes, and external integrations. <br>
Risk: Autonomous workflow execution could act on weak market signals or incomplete data. <br>
Mitigation: Keep auto_mode off until tested, enforce confidence thresholds and schema validation, and require review gates for campaign planning and execution sprints. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/forevercrab321-svg/marketing-os) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Runtime configuration](artifact/configs/system.config.json) <br>
- [CMO output schema](artifact/schemas/cmo_output.schema.json) <br>
- [CMO to Operator schema](artifact/schemas/cmo_to_operator.schema.json) <br>
- [Campaign schema](artifact/schemas/campaign.schema.json) <br>
- [Feedback schema](artifact/schemas/feedback.schema.json) <br>
- [Operator task schema](artifact/schemas/operator_task.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Structured JSON objects and Markdown guidance for strategy, campaign plans, task records, metrics, and feedback.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to follow bundled JSON schemas and distinguish facts, inferences, recommendations, confidence, risks, and data gaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
