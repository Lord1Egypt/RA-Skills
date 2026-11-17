## Description:

Guides agents in using authenticated Make APIs to manage workflows, scenarios, connections, hooks, and other account resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Make users can inspect and manage Make resources through their authorized connection, and build approved workflow automations using scenarios, hosted functions, and triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: New scenarios, hooks, functions, triggers, and destinations can keep running or forwarding events after the conversation ends.

Mitigation: Review each proposed automation, destination, and write; obtain explicit user approval before creating, changing, or starting it.

Risk: Account credentials or sensitive event data may be exposed through files, logs, or destination settings.

Mitigation: Prefer OAuth sign-in, keep credentials out of files and templates, and confirm exactly what data a destination receives.

## Reference(s):

- [Make API documentation](https://developers.make.com/api-documentation)
- [Make API reference](https://developers.make.com/api-documentation/api-reference)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)
- [Make skill on ClawHub](https://clawhub.ai/byungkyu/skills/make-api)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with shell commands, API examples, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a Maton account, and an authorized Make connection.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
