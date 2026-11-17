## Description:

Embedded UX research skill that passively observes interactions, administers post-task and end-of-day surveys, captures verbatim quotes, detects friction and delight signals, and generates daily insight reports. All data stays local.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giulianomorse](https://clawhub.ai/user/giulianomorse)

### License/Terms of Use:

MIT

## Use Case:

Developers, product teams, and UX researchers use this skill to observe OpenClaw sessions, collect post-task and end-of-day feedback, and generate local daily insight reports grounded in user verbatims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records exact interaction details and survey responses locally, which can include sensitive project or personal information.

Mitigation: Use it only for sessions where local UX logging is intended, avoid secrets or regulated data, and regularly review or delete ~/.uxr-observer/ data.

Risk: Local logs and generated reports may contain verbatim content that is sensitive if shared.

Mitigation: Review and redact reports before sharing, and share only through explicit user-directed actions.

Risk: The security review notes limited evidence of strong opt-in or storage safeguards.

Mitigation: Confirm study participation before activation, pause observation when requested, and restrict access to the local data directory.

## Reference(s):

- [Clawsight Analysis Framework](references/analysis-framework.md)
- [ClawHub skill page](https://clawhub.ai/giulianomorse/skills/observer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Conversational prompts, JSONL observation and survey records, and Markdown daily reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local session data and reports under ~/.uxr-observer/.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
