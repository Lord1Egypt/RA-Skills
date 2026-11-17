## Description:

Organizes scattered requirements, conversations, and meeting notes into a structured project brief with scope, acceptance criteria, risks, and milestones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to turn raw requirements, meeting notes, constraints, and chat context into reviewable project briefs. It is intended for project kickoff, requirements organization, delivery definition, and explicit clarification tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script contains local audit and secret-pattern scanning modes outside the stated brief-writing purpose.

Mitigation: Use the skill for structured brief generation unless the user explicitly requests local auditing, and scope any audit input to intended, non-private paths.

Risk: Generated project briefs may include assumptions or unconfirmed requirements when source material is incomplete.

Mitigation: Treat output as a review draft and resolve listed clarification items before approval, execution, publication, or system changes.

Risk: Input materials can contain personal, confidential, or sensitive project information.

Mitigation: Redact sensitive content before processing and avoid enabling directory or pattern scans on private directories without explicit user intent.

## Reference(s):

- [Project Brief Writer on ClawHub](https://clawhub.ai/52yuanchangxing/skills/project-brief-writer)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Skill Specification](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown, with optional JSON output when the local script is invoked with --format json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft outputs emphasize reviewable assumptions, open questions, boundaries, dependencies, risks, and milestones.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
