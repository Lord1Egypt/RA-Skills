## Description:

Analyzes memory logs to detect recurring workflow patterns and suggest automations such as cron jobs, skill drafts, workflow shortcuts, and monitoring proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn recurring memory-log patterns into reviewable automation proposals and reusable workflow assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private memory-log content and stores derived excerpts in state.json.

Mitigation: Use it only with memory logs you are comfortable analyzing, keep state.json private, and avoid committing or syncing generated state publicly.

Risk: The skill converts untrusted history into cron definitions, draft skills, workflow shortcuts, and monitoring proposals.

Mitigation: Treat generated automations as proposals; inspect cron definitions and skill drafts before approval or deployment.

Risk: Generated evidence may be incomplete or misleading for deciding whether to automate a workflow.

Mitigation: Review the underlying memory evidence and do not approve automations solely from generated output.

## Reference(s):

- [Pattern Types - Detection Logic](artifact/references/pattern-types.md)
- [Suggestion Templates](artifact/references/suggestion-templates.md)
- [Workflow Crystallizer on ClawHub](https://clawhub.ai/newageinvestments25-byte/skills/nai-workflow-crystallizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON snippets, draft SKILL.md content, cron definitions, and workflow guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists derived event and suggestion state in state.json; limits reports to at most three suggestions per run by default.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
