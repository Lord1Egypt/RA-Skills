## Description: <br>
Analyze memory logs to detect recurring patterns and suggest automations such as cron jobs, skill drafts, workflow shortcuts, and monitoring proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to review local memory logs for recurring work patterns and turn supported patterns into proposed automations or workflow shortcuts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes local memory logs and stores derived summaries in state.json, which may retain sensitive workflow information. <br>
Mitigation: Run it only in a trusted local workspace, inspect state.json when needed, and reset state when prior memory-derived patterns should not be retained. <br>
Risk: Generated cron definitions, skill drafts, or workflow shortcuts may be incorrect or unsuitable for the user's environment. <br>
Mitigation: Review generated proposals before approving, scheduling, or deploying them. <br>


## Reference(s): <br>
- [Workflow Crystallizer on ClawHub](https://clawhub.ai/newageinvestments25-byte/nai-workflow-crystallizer) <br>
- [Pattern Types](references/pattern-types.md) <br>
- [Suggestion Templates](references/suggestion-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON suggestions, cron definitions, and draft SKILL.md content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local state for cached analysis, suggestion lifecycle tracking, and deduplication.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
