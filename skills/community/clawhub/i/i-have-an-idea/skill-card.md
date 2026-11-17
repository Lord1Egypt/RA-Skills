## Description:

Captures and co-develops new product, feature, experience, architecture, or creative-workflow ideas into one traceable, AI-friendly Markdown document without starting implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isdou](https://clawhub.ai/user/isdou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preserve early-stage ideas as living Markdown records, refine them through focused discussion, and keep implementation gated behind explicit authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-confidence idea-like messages may cause the assistant to create or update Markdown files when the user expected only a conversation.

Mitigation: Review changed Markdown files after invocation, and rely on the skill's ambiguity check when a request could mean either idea exploration or immediate execution.

Risk: Idea records can become duplicated or misleading if a similar idea or existing product, architecture, or ADR document already exists.

Mitigation: Search existing Markdown documentation before creating a new idea record and update or link the existing source of truth when it already covers the topic.

Risk: A captured or shaped idea could be mistaken for approval to implement.

Mitigation: Keep implementation authorization separate from idea status and require explicit author language before recording authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/isdou/skills/i-have-an-idea)
- [Idea record template](artifact/assets/idea-record-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown document updates plus concise conversational status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a single living idea Markdown document; does not produce implementation artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
