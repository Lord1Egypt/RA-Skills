## Description: <br>
AI-driven lead discovery for B2B export. Searches web for potential buyers matching ICP, evaluates fit, and creates CRM records for follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and business development teams use this skill to discover, enrich, score, and prioritize B2B export prospects against an ICP. It can prepare owner-facing lead reports and create CRM follow-up records when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect contact details, store prospect research, and create CRM records without enough scope or control details. <br>
Mitigation: Review before installing, limit it to approved CRM and memory workspaces, and require manual approval before CRM writes or outreach queues. <br>
Risk: Lead discovery may collect or retain contact data in markets with different legal requirements. <br>
Mitigation: Confirm what contact data may legally be collected in each target market, define retention expectations for research notes, and ensure scheduled runs can be paused and audited. <br>


## Reference(s): <br>
- [Jina AI](https://jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with lead summaries, scores, contact signals, and recommended follow-up actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create CRM records and Supermemory research notes when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
