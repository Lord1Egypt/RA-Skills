## Description:

Generate OSOP session logs by creating .osop workflow definitions and .osoplog.yaml execution records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archie0125](https://clawhub.ai/user/archie0125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill after completing a task to produce structured OSOP workflow and execution-log records for the session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local session records may include task outputs, decision summaries, private prompts, credentials, or other sensitive details.

Mitigation: Store logs outside version control for sensitive work and redact secrets, credentials, private prompts, and sensitive output details before sharing.

## Reference(s):

- [OSOP](https://osop.ai)
- [OSOP Editor](https://osop-editor.vercel.app)
- [ClawHub skill page](https://clawhub.ai/archie0125/skills/osop-log)
- [Publisher profile](https://clawhub.ai/user/archie0125)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown guidance with YAML file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a workflow definition and execution record under sessions/.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
