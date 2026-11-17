## Description:

Trajectory compiler that converts OpenClaw session traces or raw trajectory logs into a parameterized, reusable skill through trace interception, DAG abstraction, schema and code synthesis, and registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[la1850](https://clawhub.ai/user/la1850)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn concrete OpenClaw tool-call traces into reusable skills with dynamic inputs, generated schemas, plans, run scripts, and run-flow documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted trace content can control generated skill files and persistent skill instructions.

Mitigation: Use sanitized non-production traces and inspect the generated SKILL.md, plan, schema, run-flow, and run script before refreshing or loading the generated skill.

Risk: Using the latest session can capture unintended or sensitive session content.

Mitigation: Prefer an explicit session path or time window, avoid traces that may contain secrets, and pass a deliberate safe output directory and skill name.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/la1850/skills/meta-skill)
- [Compiler specification](artifact/references/compiler-spec.md)
- [Pipeline guide](artifact/references/pipeline.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Generated skill files, JSON schemas and plans, JavaScript run code, Markdown run-flow documentation, and console status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compiler output includes SKILL.md, references/schema.json, references/plan.json, references/run-flow.md, and scripts/run.js in the configured skills directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-12T12:20:35.525Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
