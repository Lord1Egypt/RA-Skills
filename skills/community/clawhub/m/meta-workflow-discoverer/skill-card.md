## Description: <br>
AI-powered workflow automation discoverer that observes user patterns, identifies repetitive tasks, and automatically generates executable automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation-focused users use this skill to record task histories, identify repeated task, sequence, and time patterns, and generate candidate workflow automations for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow history and conversation-derived intent may include secrets, regulated data, private business processes, trading actions, or customer information. <br>
Mitigation: Use explicit opt-in, redact sensitive values before recording, and define local retention and deletion controls before installation or use. <br>
Risk: Generated, scheduled, or event-triggered automations may perform incorrect or unintended actions if enabled without review. <br>
Mitigation: Require manual approval, testing, and monitoring before any generated automation is enabled, shared, scheduled, or run. <br>
Risk: Cross-user sharing could expose private workflow patterns without clear privacy controls. <br>
Mitigation: Disable sharing unless the deployment has documented consent, access controls, redaction, and review of shared workflow data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/meta-workflow-discoverer) <br>
- [Publisher profile](https://clawhub.ai/user/jason-aka-chen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks; runtime methods return JSON-like dictionaries for workflows, triggers, automations, and analysis results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores workflow history and generated automation records locally under the configured user storage path.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
