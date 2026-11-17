## Description:

Validates vague product requirements and user stories against five closure rules and returns follow-up questions when incomplete or JSON tasks when the story is ready.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoelaine80-boop](https://clawhub.ai/user/zhaoelaine80-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External builders and developers use this skill to turn rough product ideas, PRDs, user stories, or feature specs into reviewable requirement checks before delegating implementation to an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated FileEditor tasks could direct an agent to write files based on incomplete or misunderstood requirements.

Mitigation: Review the returned task instructions and target path before allowing downstream file edits.

Risk: The skill depends on Pydantic from a package index.

Mitigation: Install dependencies from a trusted index and pin or lock Pydantic in production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoelaine80-boop/skills/logic-bridge-protocol)
- [Publisher profile](https://clawhub.ai/user/zhaoelaine80-boop)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON with natural-language messages, follow-up questions, and FileEditor-ready task instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Success output includes a stable sha256 digest of the normalized input for traceability.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
