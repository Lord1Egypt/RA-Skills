## Description:

Haike AI assistant is a Chinese workplace assistant for Guangzhou Haike Electronics employees across 13 departments, guiding task scoping before producing role-specific reports, drafts, analyses, reminders, and daily work summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beargzhaike](https://clawhub.ai/user/beargzhaike)

### License/Terms of Use:

MIT-0

## Use Case:

Employees at Guangzhou Haike Electronics use this assistant for routine departmental work such as drafting documents, analyzing business data, preparing daily reports, tracking tasks, writing emails, and generating role-specific operational guidance. It is tailored for internal workplace workflows across executive, sales, ecommerce, finance, HR, manufacturing, quality, purchasing, R&D, and foreign-trade teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The assistant persists employee profiles, conversation history, learned preferences, pending tasks, and departmental knowledge across sessions.

Mitigation: Require explicit opt-in before memory is created, show what will be stored, and provide clear controls for review, deletion, retention limits, and disabling memory.

Risk: Daily reports may use screenshot logs and work-memory summaries to infer employee activity and produce status reports.

Mitigation: Use only with employee approval, preview sources before report generation, redact sensitive content, and allow screenshot analysis and scheduled reports to be disabled.

Risk: The assistant can read Tencent Docs data and route feedback or knowledge to the named reviewer, which may expose business or employee information.

Mitigation: Limit document access to authorized sources, confirm the destination before sharing feedback or knowledge, and avoid sending confidential financial, identity, or account data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beargzhaike/skills/haike-ai-assistant)
- [ClawHub publisher profile](https://clawhub.ai/user/beargzhaike)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown, structured text, tables, email drafts, HTML report content, and JSON-like configuration records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are primarily Simplified Chinese and may be customized by department, user role, task history, templates, schedules, and shortcut commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
