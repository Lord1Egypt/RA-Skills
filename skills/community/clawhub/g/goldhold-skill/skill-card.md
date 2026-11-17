## Description:

GoldHold provides persistent, encrypted memory for AI agents across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerrysrodz](https://clawhub.ai/user/jerrysrodz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use GoldHold to let AI agents store, search, and retrieve decisions, facts, corrections, and session context across sessions through a REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send selected session context, decisions, messages, and summaries to GoldHold for persistent remote storage.

Mitigation: Use the skill only with approved data flows, and avoid secrets, credentials, customer data, regulated information, and confidential work unless retention, deletion, project separation, and access controls are understood.

Risk: Retrieved memories may be stale, incomplete, or inconsistent with current user or platform instructions.

Mitigation: Treat retrieved memories as notes to verify, and keep current user and platform instructions authoritative.

Risk: Automatic persistent memory can create scoping and consent issues across sessions or projects.

Mitigation: Scope use to approved projects and review what is stored, searched, or reused before relying on it.

## Reference(s):

- [GoldHold website](https://goldhold.ai)
- [GoldHold API base URL](https://relay.goldhold.ai)
- [Goldhold Skill on ClawHub](https://clawhub.ai/jerrysrodz/skills/goldhold-skill)
- [Publisher profile](https://clawhub.ai/user/jerrysrodz)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOLDHOLD_API_KEY and sends selected memory payloads to the GoldHold API.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
